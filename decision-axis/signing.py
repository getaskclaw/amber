"""Run-level signing for decision-axis artifacts (HMAC-SHA256).

Trust root = the signing secret. It is NEVER written into the product tree:
  1. env `AMBER_DECISION_HMAC_SECRET` (preferred), else
  2. file `$AMBER_DECISION_HMAC_KEY_FILE` (default `~/.local/state/amber-decision/hmac.key`),
     created 0600 on first signed run if absent (dir 0700).
The key file path is deliberately outside this repository so a whole-tree secret
scan finds nothing, and it is never printed into logs, reports or manifests.

Why keyed: the r0 gate used a public unkeyed formula
`sha256(adapter|model|qid|json(answer))`, so anyone who knew the formula could
edit a response and recompute the tag. See WO-DEC-001-r1 Blocker 1.
"""
import hashlib
import hmac
import json
import os
import secrets

ENV_SECRET = "AMBER_DECISION_HMAC_SECRET"
ENV_KEY_FILE = "AMBER_DECISION_HMAC_KEY_FILE"
ALGO = "hmac-sha256"
DEFAULT_KEY_FILE = os.path.join(
    os.path.expanduser("~"), ".local", "state", "amber-decision", "hmac.key")

_cached = None


class SigningError(Exception):
    pass


def key_file_path():
    return os.environ.get(ENV_KEY_FILE) or DEFAULT_KEY_FILE


def _read_key_file():
    path = key_file_path()
    with open(path, "rb") as f:
        data = f.read().strip()
    if not data:
        raise SigningError(f"signing key file {path!r} is empty")
    return data


def _write_key_file(key):
    path = key_file_path()
    d = os.path.dirname(path)
    os.makedirs(d, mode=0o700, exist_ok=True)
    try:
        os.chmod(d, 0o700)
    except OSError:
        pass
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(key + b"\n")
    os.chmod(path, 0o600)


def get_secret(create=True):
    """Return the signing secret bytes.

    create=True  -> running a new run: env, else key file, else generate + store 0600.
    create=False -> verifying: env, else key file; never invent a key (an invented
                    key would make every existing artifact look tampered).
    """
    global _cached
    if _cached is not None:
        return _cached
    env = os.environ.get(ENV_SECRET)
    if env:
        _cached = env.encode("utf-8")
        return _cached
    try:
        _cached = _read_key_file()
        return _cached
    except FileNotFoundError:
        if not create:
            raise SigningError(
                f"no signing secret: set {ENV_SECRET} or create {key_file_path()!r}; "
                "refusing to verify artifacts with an invented key")
    key = secrets.token_hex(32).encode("ascii")
    _write_key_file(key)
    _cached = key
    return _cached


def secret_source():
    """Where the secret came from. Never returns the value."""
    if os.environ.get(ENV_SECRET):
        return f"env:{ENV_SECRET}"
    try:
        _read_key_file()
        return "file"
    except FileNotFoundError:
        return "none"


def canonical(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def sign(payload, secret=None):
    """HMAC-SHA256 hex digest of a JSON-serializable payload (sorted keys)."""
    sec = secret if secret is not None else get_secret()
    return hmac.new(sec, canonical(payload), hashlib.sha256).hexdigest()


def sign_record(record, secret=None):
    """Tag for one normalized response record: every field except `integrity`.

    Coverage is the whole record (answer, ok, error_class/error_detail, latency_s,
    cost_usd, tokens, run_nonce, dataset_sha256, ...), so metadata tampering is
    detected too -- not only a changed answer.
    """
    payload = {k: v for k, v in record.items() if k != "integrity"}
    return sign(payload, secret=secret)


def matches(record, secret=None):
    """True when record['integrity'] is a valid tag for that record."""
    want = sign_record(record, secret=secret)
    got = record.get("integrity")
    return isinstance(got, str) and hmac.compare_digest(got, want)
