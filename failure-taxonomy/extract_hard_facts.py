#!/usr/bin/env python3
"""AMBER failure-taxonomy — hard-fact layer extractor (rule-based, no LLM).

Reads each ~/.hermes/profiles/amber-*/state.db strictly read-only
(`file:...?mode=ro`) and extracts *hard facts* per bench session.

Hard facts are only what the transcript literally shows:
  timeout            — tool result exit_code 124 / timeout error envelope / cap-length wall clock
  billing_exhausted  — quota/billing/credit signals in an error envelope
  tool_failure       — tool result with non-zero exit_code or error/blocked status (a count, not a
                       capability judgement)
  test_modified      — a write_file/patch tool call whose target path matches a test-file pattern
  completion_claimed — the final assistant text turn contains a completion declaration

No inference of *why* something failed. Nothing is written back to any state.db.

Usage:
  python3 extract_hard_facts.py [--out PATH] [--profiles P1,P2] [--limit N]

Output: JSONL, one record per bench session (see --help / README).
"""

import argparse
import glob
import json
import os
import re
import sqlite3
import sys
import time

PROFDIR = os.path.expanduser("~/.hermes/profiles")
DEFAULT_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hard-facts.jsonl")

# ---------------------------------------------------------------------------
# Case registry. Internal case ids NEVER appear in published files; the
# attribution table maps them to public aliases. This list is the bench case
# set (source: ~/2608/sandbox/amber-run/case-number-map.csv +
# amber-crof-alias-map.json + INDEX.md). Longest match wins.
# ---------------------------------------------------------------------------
# (internal id, variant, public alias or None, face)
CASES = [
    ("REQ-001", "visible",     "A-0676097b", "req-drift"),
    ("REQ-001", "drift",       "A-0676097b", "req-drift"),
    ("REQ-001", "leaf-swap",   "A-0676097b", "req-drift"),
    ("REQ-001", "signed-sync", "A-0676097b", "req-drift"),
    ("BD-R001", "",            "A-cdc3d11a", "review"),
    ("BD-R003", "",            "A-47eea242", "review"),
    ("BD-V001", "",            "A-ea80d793", "vision"),
    ("BD-001",  "",            "A-77d62143", "build"),
    ("BD-002",  "",            "A-569dbe0d", "build"),
    ("BD-003",  "",            "A-87c472cb", "build"),
    ("BD-004",  "",            "A-641195e2", "build"),
    ("BD-005",  "",            "A-442d4aab", "build"),
    ("BD-006",  "",            "A-61f7ad01", "build"),
    ("BE-001",  "",            "A-d511f9e8", "verify"),
    ("BE-002",  "",            "A-a317e74b", "verify"),
    ("BE-003",  "",            "A-be92627f", "verify"),
    ("OPS-01",  "",            "A-a5608487", "ops"),
    ("OPS-02",  "",            "A-984e80ee", "ops"),
    ("OPS-03",  "",            "A-24bcf707", "ops"),
    ("OPS-06",  "",            "A-8d4bc770", "ops"),
    ("OPS-07",  "",            "A-6fbeb363", "ops"),
    ("OPS-08",  "",            "A-8c909d0a", "ops"),
    ("FTM-001", "",            "A-791e90ac", "text"),
    ("FTM-002", "",            "A-1fd3683a", "text"),
    ("FTM-004", "",            "A-13854d9d", "text"),
    ("JJA-BRAND-01", "",       "A-d9b79b46", "ui-build"),
    # in-progress / retired / non-scoring — no public alias, still case-shaped
    ("CONV-001", "", None, "convergence"),
    ("ORCH-AVAIL-001", "", None, "orchestration"),
    ("META-001", "", None, "-"),
    ("OPS-09", "", None, "ops"),
    ("OPS-04", "", None, "ops"),
    ("CE-001", "", None, "-"),
    ("AUTH-FLOW-01", "", None, "-"),
    ("DLV-001", "", None, "delivery"),
    ("FTM-003", "", None, "text"),
    ("FTM-005", "", None, "text"),
    ("PA-001", "", None, "-"),
    ("RB-001", "", None, "-"),
    ("RB-002", "", None, "-"),
    ("RB-003", "", None, "-"),
]
# longest internal id first so BD-R001 beats BD-001
CASES.sort(key=lambda c: -len(c[0]))

BENCH_SOURCE_RE = re.compile(r"^amber-lib-(?P<rest>.+)$")

# ---------------------------------------------------------------------------
# Rule patterns. Kept narrow on purpose: we only look at machine envelopes
# (tool-result JSON) for failure facts, never at prose/code the candidate
# merely read.
# ---------------------------------------------------------------------------
# Harness CAP timeouts only (a candidate's own command timing out is a tool
# failure, not a harness wall). Anchor on the cap length or explicit wall words.
TIMEOUT_CAP_RE = re.compile(
    r"(\[?Command timed out after (1[89]\d\d|3[56]\d\d|7200)s\]?|"
    r"timed out after (1[89]\d\d|3[56]\d\d|7200)\s*s|"
    r"harness_timeout|killed at the cap|"
    r"(1800|3600|7200)\s*s\b.{0,40}(cap|wall|timeout|kill)|"
    r"(cap|wall|timeout|kill).{0,40}(1800|3600|7200)\s*s)", re.I)
# any timeout at all (for the tool_failure bucket)
TIMEOUT_ANY_RE = re.compile(
    r"(timeout|timed out|TimeoutExpired|killed at the cap)", re.I)

BILLING_RE = re.compile(
    r"(insufficient_quota|exceeded your current quota|billing_hard_limit|"
    r"billing_hard_limit_reached|out of credits|no credits|"
    r"credit balance is too low|quota.{0,24}(exhaust|exceed|deplet|dead|burn)|"
    r"rate_limit_exceeded|billing_exhausted)", re.I)

COMPLETION_RE = re.compile(
    r"(交付完成|已完成|已交付|已完成修复|修复完成|已修复|已实现|"
    r"全部通过|全部检查通过|自测(均|全部)?通过|测试(均|全部)?通过|验证通过|"
    r"\bdelivered\b|\bimplementation complete\b|\ball tests pass\b|"
    r"\btests pass\b|\bcompleted successfully\b|\bdone\b|"
    r"\bfinished\b|\bimplemented\b)", re.I)

TEST_PATH_RE = re.compile(
    r"(^|/)(tests?/|test_[^/]*\.py$|[^/]*_test\.py$|conftest\.py$|"
    r"[^/]*\.test\.(js|ts|tsx|jsx)$|spec/)", re.I)

# A candidate "ran verification" when it executes a checker itself.
VERIFY_CMD_RE = re.compile(
    r"(pytest|unittest|oracle_test|oracle/|npm (run )?test|npm test|"
    r"yarn test|pnpm test|python3? [^\n]*test[^\n]*\.py|"
    r"python3? -m (pytest|unittest)|jest|vitest|go test|cargo test|"
    r"selftest|self_test|自测)", re.I)

# tools that mutate files, and where the target path lives in their args
WRITE_TOOLS = {"write_file", "patch", "apply_patch", "edit_file", "str_replace"}
PATH_KEYS = ("path", "file_path", "filePath", "filename", "target")


def pick_case(rest):
    """rest = session source minus 'amber-lib-'. Returns (case_key, variant, alias, face)."""
    for cid, var, alias, face in CASES:
        if rest.startswith(cid + "-") or rest == cid:
            # REQ-001 variants are encoded as REQ-001-<variant>-<lane>-...
            if var and not rest.startswith(cid + "-" + var):
                continue
            return cid, var, alias, face
    return None, None, None, None


def split_lane_band(rest, case_id, variant):
    """Everything after the case token: first token = lane, last = band (informational)."""
    tail = rest
    prefix = case_id if not variant else f"{case_id}-{variant}"
    if tail.startswith(prefix):
        tail = tail[len(prefix):].lstrip("-")
    toks = [t for t in tail.split("-") if t]
    if not toks:
        return None, None
    if len(toks) == 1:
        return toks[0], None
    return toks[0], toks[-1]


def load_json_maybe(s):
    if not s:
        return None
    s = s.strip()
    if not (s.startswith("{") or s.startswith("[")):
        return None
    try:
        return json.loads(s)
    except Exception:
        return None


def extract_session(cur, sid, profile, source, sess_row):
    (started_at, ended_at, end_reason, message_count, tool_call_count, model,
     title, cwd) = sess_row
    m = BENCH_SOURCE_RE.match(source)
    rest = m.group("rest") if m else source
    cid, var, alias, face = pick_case(rest)
    lane, band = split_lane_band(rest, cid, var) if cid else (None, None)
    case_key = cid if not var else f"{cid}/{var}"

    signals = {
        "timeout": {"hit": False, "evidence": []},
        "billing_exhausted": {"hit": False, "evidence": []},
        "tool_failure": {"count": 0, "evidence": [], "last_fail_ts": None},
        "test_modified": {"hit": False, "paths": []},
        "completion_claimed": {"hit": False, "snippet": None, "timestamp": None},
        "verification_run": {"hit": False, "count": 0, "last_ts": None},
    }

    last_assistant = None
    rows = cur.execute(
        "SELECT role, tool_name, content, tool_calls, timestamp "
        "FROM messages WHERE session_id=? ORDER BY timestamp, id", (sid,))
    for role, tool_name, content, tool_calls, ts in rows:
        # ---- completion candidate: remember the last assistant text turn ----
        if role == "assistant" and content:
            last_assistant = (content, ts)

        # ---- test file modification + verification runs: from tool CALL arguments ----
        if role == "assistant" and tool_calls:
            tc = load_json_maybe(tool_calls)
            if isinstance(tc, list):
                for item in tc:
                    fn = (item or {}).get("function") or {}
                    name = fn.get("name") or item.get("name")
                    if name in WRITE_TOOLS:
                        args = load_json_maybe(fn.get("arguments") or "{}") or {}
                        for k in PATH_KEYS:
                            p = args.get(k)
                            if isinstance(p, str) and TEST_PATH_RE.search(p):
                                signals["test_modified"]["hit"] = True
                                if p not in signals["test_modified"]["paths"]:
                                    signals["test_modified"]["paths"].append(p)
                    elif name in ("terminal", "execute_code", "process_manage", "browser_exec"):
                        args = load_json_maybe(fn.get("arguments") or "{}") or {}
                        cmd = args.get("command") or args.get("code") or ""
                        if isinstance(cmd, str) and VERIFY_CMD_RE.search(cmd):
                            signals["verification_run"]["hit"] = True
                            signals["verification_run"]["count"] += 1
                            signals["verification_run"]["last_ts"] = ts

        # ---- machine envelopes: only tool results ----
        if role == "tool":
            obj = load_json_maybe(content or "")
            if isinstance(obj, dict):
                ec = obj.get("exit_code")
                err = obj.get("error")
                status = obj.get("status")
                out = obj.get("output") or ""
                cap_hit = (ec == 124 and TIMEOUT_CAP_RE.search(out or "")) or \
                          (isinstance(err, str) and TIMEOUT_CAP_RE.search(err))
                if cap_hit:
                    signals["timeout"]["hit"] = True
                    signals["timeout"]["evidence"].append(
                        {"ts": ts, "tool": tool_name, "kind": "harness_cap_124_or_wall",
                         "snippet": (out or err or content or "")[-200:]})
                if isinstance(ec, int) and ec not in (0,):
                    signals["tool_failure"]["count"] += 1
                    signals["tool_failure"]["last_fail_ts"] = ts
                    kind = "exit"
                    if TIMEOUT_ANY_RE.search(out or "") or TIMEOUT_ANY_RE.search(err or ""):
                        kind = "candidate_timeout"   # not a harness cap wall
                    if len(signals["tool_failure"]["evidence"]) < 12:
                        signals["tool_failure"]["evidence"].append(
                            {"ts": ts, "tool": tool_name, "exit_code": ec, "kind": kind,
                             "snippet": (out or "")[-200:]})
                if status == "error" or (isinstance(err, str) and err):
                    if len(signals["tool_failure"]["evidence"]) < 12:
                        signals["tool_failure"]["evidence"].append(
                            {"ts": ts, "tool": tool_name, "kind": "error_status",
                             "snippet": str(err or obj.get("error"))[:200]})
                    if signals["tool_failure"]["count"] == 0 and status == "error":
                        signals["tool_failure"]["count"] += 1
                blob = str(err) if err else ""
                bm = BILLING_RE.search(blob)
                if bm:
                    signals["billing_exhausted"]["hit"] = True
                    signals["billing_exhausted"]["evidence"].append(
                        {"ts": ts, "tool": tool_name,
                         "snippet": blob[max(0, bm.start() - 60):bm.end() + 100]})
        # ---- billing is deliberately NOT scanned from prose: bench cases exist
        #      that discuss quota triage (OPS-08), so candidate text about
        #      "no_credits" is task content, not a billing wall. Only machine
        #      envelopes above count.

    # ---- completion claim from final assistant turn ----
    if last_assistant is not None:
        c, ts = last_assistant
        m = COMPLETION_RE.search(c)
        if m:
            signals["completion_claimed"] = {
                "hit": True, "timestamp": ts,
                "match": m.group(0),
                "snippet": c[max(0, m.start() - 80):m.end() + 120],
            }

    # ---- wall-clock corroboration for timeout: only near a known cap boundary ----
    wall = None
    if started_at and ended_at:
        wall = round(ended_at - started_at, 1)
    if wall is not None:
        for cap in (1800, 3600, 7200):
            if cap - 20 <= wall <= cap + 120:
                signals["timeout"]["hit"] = True
                signals["timeout"]["evidence"].append(
                    {"ts": ended_at, "kind": f"wall_clock_near_{cap}s_cap", "wall_s": wall})
                break

    # trim evidence lists for a compact file
    signals["timeout"]["evidence"] = signals["timeout"]["evidence"][:6]
    signals["billing_exhausted"]["evidence"] = signals["billing_exhausted"]["evidence"][:6]

    return {
        "profile": profile,
        "session_id": sid,
        "source": source,
        "case_hint": case_key,
        "case_alias": alias,
        "face": face,
        "lane_token": lane,
        "band_token": band,
        "model": model,
        "started_at": started_at,
        "ended_at": ended_at,
        "wall_s": wall,
        "end_reason": end_reason,
        "message_count": message_count,
        "tool_call_count": tool_call_count,
        "cwd": cwd,
        "signals": signals,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--profiles", default="", help="comma-separated profile list")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    if a.profiles:
        profs = [p.strip() for p in a.profiles.split(",") if p.strip()]
    else:
        profs = sorted(os.path.basename(os.path.dirname(p))
                       for p in glob.glob(os.path.join(PROFDIR, "amber-*", "state.db")))

    n = 0
    t0 = time.time()
    with open(a.out, "w", encoding="utf-8") as fh:
        for prof in profs:
            db = os.path.join(PROFDIR, prof, "state.db")
            if not os.path.exists(db):
                continue
            try:
                con = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=30)
            except Exception as e:
                print(f"WARN {prof}: {e}", file=sys.stderr)
                continue
            try:
                cur = con.cursor()
                rows = cur.execute(
                    "SELECT id, source, started_at, ended_at, end_reason, message_count, "
                    "tool_call_count, model, title, cwd FROM sessions "
                    "WHERE source LIKE 'amber-lib-%' ORDER BY started_at").fetchall()
                for sid, source, st, en, er, mc, tcc, model, title, cwd in rows:
                    rec = extract_session(
                        cur, sid, prof, source,
                        (st, en, er, mc, tcc, model, title, cwd))
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    n += 1
                    if a.limit and n >= a.limit:
                        break
            finally:
                con.close()
            print(f"  {prof}: done ({n} so far, {time.time() - t0:.0f}s)", file=sys.stderr)
            if a.limit and n >= a.limit:
                break
    print(f"wrote {n} session records -> {a.out} in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
