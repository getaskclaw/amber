#!/usr/bin/env python3
"""Validate an AMBER Case Manifest, or a redacted manifest summary.

Normative sources
-----------------
* AMBER Core Specification v0.2.2 (invariants 2, 4; boundaries 2, 7; §9.4)
* AMBER Distribution Protocol v0.3 (§2, §3, §3.1, §3.2, §4, §5.1, §5.2, §5.3, §6)

What this tool enforces
-----------------------
``manifest`` mode (default when the document looks like a manifest)
  1. the document validates against ``schemas/manifest.schema.json``
     (JSON Schema 2020-12).  That schema's property names are exactly the
     manifest contents enumerated by Distribution §3, plus the construction
     parameters of §3.1; every object in it is closed, so a field the protocol
     does not enumerate is an error rather than a harmless extra.
  2. the cross-field rule of Distribution §5.2/§5.3: an eligibility
     determination of ``full_isolation`` must declare an empty egress
     allowlist.

``summary`` mode (default when the document looks like a redacted summary)
  3. the document's field set is exactly the closed field set of Distribution
     §5.1.  Any field outside it is an error, and every field §5.1 names as
     excluded is reported as such.  §5.1 fixes the field *set*, not a
     serialization, so this validator fixes one canonical spelling per §5.1
     concept (see ``SUMMARY_FIELDS``) and uses it to detect both additions and
     omissions.

Dependencies
------------
JSON input and both summary/manifest checks need nothing outside the standard
library, including a JSON Schema subset evaluator used when ``jsonschema`` is
absent.  YAML input uses PyYAML when it is importable and otherwise falls back
to ``MiniYAML``, a deliberately small reader that parses what a manifest needs
and *refuses* anything else with a clear message -- anchors, aliases, tags,
folded block scalars, multi-line plain scalars, non-empty flow mappings and
multi-document streams.  Refusing beats guessing: a validator that silently
mis-reads a document is worse than one that says it cannot read it.
Install PyYAML for the full language: ``python3 -m pip install pyyaml`` or
``uv run --with pyyaml python3 tools/validate_manifest.py <file>``.

Exit codes
----------
0  the document is valid
1  the document is invalid (schema, closed-set, or cross-field violation)
2  the document could not be read or parsed, its kind could not be detected,
   or the schema could not be loaded
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "manifest.schema.json"

EXIT_OK = 0
EXIT_INVALID = 1
EXIT_UNUSABLE = 2

SHA256_RE = r"^[0-9a-f]{64}$"
CUTOFF_RE = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?Z$"


class LoadError(Exception):
    """Raised when a document cannot be read or parsed safely."""


# ---------------------------------------------------------------------------
# Standard-library YAML subset reader (fallback when PyYAML is unavailable)
# ---------------------------------------------------------------------------

_TRUE = {"true", "True", "TRUE", "yes", "Yes", "YES", "on", "On", "ON"}
_FALSE = {"false", "False", "FALSE", "no", "No", "NO", "off", "Off", "OFF"}
_NULL = {"", "~", "null", "Null", "NULL"}


class _Line:
    __slots__ = ("idx", "indent", "content")

    def __init__(self, idx, indent, content):
        self.idx = idx
        self.indent = indent
        self.content = content


def _scan(text, *, on_colon, on_hash):
    """Walk ``text`` tracking quotes and flow depth; report top-level hits."""
    in_single = in_double = False
    depth = 0
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if in_single:
            if ch == "'":
                if i + 1 < n and text[i + 1] == "'":
                    i += 2
                    continue
                in_single = False
        elif in_double:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                in_double = False
        else:
            if ch == "'":
                in_single = True
            elif ch == '"':
                in_double = True
            elif ch in "[{":
                depth += 1
            elif ch in "]}":
                depth -= 1
            elif ch == ":" and depth == 0 and on_colon and (i + 1 == n or text[i + 1] in " \t"):
                if on_colon(text, i):
                    return
            elif ch == "#" and depth == 0 and i > 0 and text[i - 1] in " \t" and on_hash:
                if on_hash(text, i):
                    return
        i += 1


def _split_key(text):
    """Split ``key: value`` at the first top-level colon; ``(None, None)`` if absent."""
    found = []

    def hit(t, i):
        found.append(i)
        return True

    _scan(text, on_colon=hit, on_hash=None)
    if not found:
        return None, None
    i = found[0]
    return text[:i].strip(), text[i + 1:].strip()


def _strip_comment(text):
    cut = []

    def hit(t, i):
        cut.append(i)
        return True

    _scan(text, on_colon=None, on_hash=hit)
    return text[: cut[0]].rstrip() if cut else text


def _split_flow(text, lineno):
    parts = []
    buf = []
    in_single = in_double = False
    depth = 0
    for ch in text:
        if in_single:
            buf.append(ch)
            if ch == "'":
                in_single = False
            continue
        if in_double:
            buf.append(ch)
            if ch == '"':
                in_double = False
            continue
        if ch == "'":
            in_single = True
        elif ch == '"':
            in_double = True
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append("".join(buf))
            buf = []
            continue
        buf.append(ch)
    parts.append("".join(buf))
    return [p.strip() for p in parts]


class MiniYAML:
    """Parse the YAML subset a manifest needs, or refuse loudly."""

    def __init__(self, text):
        self.raw = text.split("\n")
        self.lines = []
        for n, raw in enumerate(self.raw):
            body = raw.rstrip()
            stripped = body.strip()
            if not stripped:
                continue
            leading = body[: len(body) - len(body.lstrip(" "))]
            if "\t" in leading:
                raise LoadError("line %d: a tab is used for indentation (YAML forbids tabs)" % (n + 1))
            if stripped.startswith("#"):
                continue
            if stripped == "---":
                if self.lines:
                    raise LoadError("line %d: multi-document streams are not supported" % (n + 1))
                continue
            if stripped == "...":
                break
            self.lines.append(_Line(n, len(leading), stripped))

    def load(self):
        if not self.lines:
            return None
        value, index = self._block(0, self.lines[0].indent)
        if index < len(self.lines):
            raise LoadError(
                "line %d: cannot parse %r (unsupported structure)"
                % (self.lines[index].idx + 1, self.lines[index].content)
            )
        return value

    @staticmethod
    def _is_item(content):
        return content == "-" or content.startswith("- ")

    def _block(self, i, indent):
        if self._is_item(self.lines[i].content):
            return self._seq(i, indent)
        return self._map(i, indent)

    def _seq(self, i, indent):
        items = []
        while i < len(self.lines):
            line = self.lines[i]
            if line.indent != indent or not self._is_item(line.content):
                break
            rest = line.content[1:].strip()
            if rest == "":
                if i + 1 < len(self.lines) and self.lines[i + 1].indent > indent:
                    value, i = self._block(i + 1, self.lines[i + 1].indent)
                else:
                    value, i = None, i + 1
                items.append(value)
                continue
            key, _ = _split_key(rest)
            if key is not None:
                sub_indent = indent + 2
                if i + 1 < len(self.lines) and self.lines[i + 1].indent > indent:
                    sub_indent = self.lines[i + 1].indent
                self.lines[i] = _Line(line.idx, sub_indent, rest)
                value, i = self._map(i, sub_indent)
                items.append(value)
                continue
            if self._is_item(rest):
                raise LoadError("line %d: stacked block sequences on one line are not supported" % (line.idx + 1))
            items.append(self._scalar(rest, line.idx + 1))
            i += 1
        return items, i

    def _map(self, i, indent):
        out = {}
        while i < len(self.lines):
            line = self.lines[i]
            if line.indent < indent:
                break
            if line.indent > indent:
                raise LoadError("line %d: unexpected indentation before %r" % (line.idx + 1, line.content))
            if self._is_item(line.content):
                raise LoadError("line %d: a block sequence may not begin inside a mapping here" % (line.idx + 1))
            key, rest = _split_key(line.content)
            if key is None:
                raise LoadError(
                    "line %d: expected 'key: value' in %r; multi-line plain scalars are not "
                    "supported by the standard-library fallback (install PyYAML for these)"
                    % (line.idx + 1, line.content)
                )
            key = self._key(key, line.idx + 1)
            if key in out:
                raise LoadError("line %d: duplicate key %r" % (line.idx + 1, key))
            if rest == "":
                if i + 1 < len(self.lines) and self.lines[i + 1].indent > indent:
                    value, i = self._block(i + 1, self.lines[i + 1].indent)
                else:
                    value, i = None, i + 1
            elif rest[0] in "|>":
                value, i = self._block_scalar(line, rest, i)
            else:
                value = self._scalar(rest, line.idx + 1)
                i += 1
            out[key] = value
        return out, i

    def _block_scalar(self, line, marker, i):
        if marker[0] == ">":
            raise LoadError(
                "line %d: folded block scalars ('>') are not supported by the standard-library "
                "fallback (install PyYAML for these)" % (line.idx + 1)
            )
        chomp = marker[1:2]
        if len(marker) > 2 or (chomp and chomp not in "-+"):
            raise LoadError("line %d: unsupported block scalar header %r" % (line.idx + 1, marker))
        body = []
        base = None
        j = line.idx + 1
        while j < len(self.raw):
            raw = self.raw[j]
            if raw.strip() == "":
                body.append("")
                j += 1
                continue
            width = len(raw) - len(raw.lstrip(" "))
            if width <= line.indent:
                break
            if base is None:
                base = width
            body.append(raw[base:].rstrip())
            j += 1
        trailing = 0
        while body and body[-1] == "":
            body.pop()
            trailing += 1
        text = "\n".join(body)
        if body:
            if chomp == "-":
                pass
            elif chomp == "+":
                text += "\n" + "\n" * trailing
            else:
                text += "\n"
        while i < len(self.lines) and self.lines[i].idx < j:
            i += 1
        return text, i

    @staticmethod
    def _key(text, lineno):
        quoted = text[:1]
        if quoted in ("'", '"'):
            if quoted == "'" and len(text) >= 2 and text.endswith("'"):
                return text[1:-1].replace("''", "'")
            if quoted == '"':
                try:
                    return json.loads(text)
                except ValueError:
                    raise LoadError("line %d: invalid quoted key %r" % (lineno, text)) from None
            raise LoadError("line %d: unterminated quoted key %r" % (lineno, text))
        if quoted in ("&", "*", "!", "?", "%"):
            raise LoadError(
                "line %d: anchors, aliases, tags and explicit keys are not supported by the "
                "standard-library fallback (install PyYAML for these)" % lineno
            )
        return text

    def _scalar(self, text, lineno):
        text = text.strip()
        if text == "":
            return None
        first = text[0]
        if first == "'":
            if len(text) < 2 or not text.endswith("'"):
                raise LoadError("line %d: unterminated single-quoted scalar" % lineno)
            return text[1:-1].replace("''", "'")
        if first == '"':
            try:
                return json.loads(text)
            except ValueError:
                raise LoadError("line %d: invalid double-quoted scalar %r" % (lineno, text)) from None
        if first in ("&", "*", "!"):
            raise LoadError(
                "line %d: anchors, aliases and tags are not supported by the standard-library "
                "fallback (install PyYAML for these)" % lineno
            )
        if first == "[":
            if not text.endswith("]"):
                raise LoadError("line %d: unterminated flow sequence" % lineno)
            inner = text[1:-1].strip()
            if inner == "":
                return []
            return [self._scalar(part, lineno) for part in _split_flow(inner, lineno)]
        if first == "{":
            if text == "{}":
                return {}
            raise LoadError(
                "line %d: non-empty flow mappings are not supported by the standard-library "
                "fallback (install PyYAML for these)" % lineno
            )
        text = _strip_comment(text).strip()
        if text in _NULL:
            return None
        if text in _TRUE:
            return True
        if text in _FALSE:
            return False
        if re.fullmatch(r"[-+]?[0-9]+", text):
            return int(text)
        if re.fullmatch(r"[-+]?(?:[0-9]*\.[0-9]+|[0-9]+\.[0-9]*)(?:[eE][-+]?[0-9]+)?", text):
            return float(text)
        return text


# ---------------------------------------------------------------------------
# Document loading
# ---------------------------------------------------------------------------


def _load_json_strict(text):
    """``json.loads`` with duplicates rejected: an ambiguous document must not pass."""

    def no_duplicates(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError("duplicate key %r (ambiguous JSON object)" % key)
            out[key] = value
        return out

    return json.loads(text, object_pairs_hook=no_duplicates)


def _strict_loader(yaml):
    """A SafeLoader subclass that rejects duplicate mapping keys.

    Duplicate keys make a document ambiguous, and an ambiguous document must
    never validate: Distribution §3 makes the detached signature cover every
    byte of the manifest precisely because re-parsing has to be unambiguous.
    """

    class StrictLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader, node, deep=False):
        loader.flatten_mapping(node)
        seen = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            try:
                hashable = key in seen
            except TypeError:
                hashable = False
            if hashable:
                raise LoadError(
                    "duplicate key %r at line %d (an ambiguous document must not validate)"
                    % (key, key_node.start_mark.line + 1)
                )
            try:
                seen[key] = True
            except TypeError:
                pass
        return yaml.SafeLoader.construct_mapping(loader, node, deep)

    StrictLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
    )
    return StrictLoader


def _normalize(value):
    """Normalize a loaded document.

    PyYAML's safe loader resolves ISO dates and timestamps into ``datetime``
    objects.  The protocol writes ``cutoff_utc``/dates as strings, so convert
    them back to their textual form; a naive datetime keeps no ``Z`` and is
    then rejected by the schema pattern, which is the honest outcome (Core
    §4.2 requires UTC).
    """
    if isinstance(value, dict):
        return {str(k): _normalize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize(v) for v in value]
    if isinstance(value, _dt.datetime):
        if value.tzinfo is not None:
            utc = value.astimezone(_dt.timezone.utc)
            text = utc.strftime("%Y-%m-%dT%H:%M:%S")
            if utc.microsecond:
                text += ".%06d" % utc.microsecond
            return text + "Z"
        return value.isoformat()
    if isinstance(value, _dt.date):
        return value.isoformat()
    return value


def _looks_like_json(text):
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        return stripped[0] in "[{"
    return False


def load_document(path, loader_mode):
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise LoadError("%s: cannot read: %s" % (path, exc)) from None
    except UnicodeDecodeError as exc:
        raise LoadError("%s: not valid UTF-8: %s" % (path, exc)) from None
    if _looks_like_json(text):
        try:
            return _normalize(_load_json_strict(text)), "json"
        except ValueError as exc:
            raise LoadError("%s: not valid JSON: %s" % (path, exc)) from None
    if loader_mode in ("auto", "pyyaml"):
        try:
            import yaml
        except ImportError:
            if loader_mode == "pyyaml":
                raise LoadError("%s: PyYAML was requested but is not importable" % path) from None
            yaml = None
        if yaml is not None:
            try:
                return _normalize(yaml.load(text, Loader=_strict_loader(yaml))), "pyyaml"
            except yaml.YAMLError as exc:
                raise LoadError("%s: not valid YAML: %s" % (path, exc)) from None
            except LoadError as exc:
                raise LoadError("%s: %s" % (path, exc)) from None
    try:
        return _normalize(MiniYAML(text).load()), "stdlib-yaml"
    except LoadError as exc:
        raise LoadError("%s: %s" % (path, exc)) from None


# ---------------------------------------------------------------------------
# JSON Schema subset evaluator (used when jsonschema is unavailable)
# ---------------------------------------------------------------------------


def _typename(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _type_ok(value, name):
    if name == "object":
        return isinstance(value, dict)
    if name == "array":
        return isinstance(value, list)
    if name == "string":
        return isinstance(value, str)
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "boolean":
        return isinstance(value, bool)
    if name == "null":
        return value is None
    raise LoadError("schema uses an unsupported type name %r" % name)


def _join(base, name):
    return "%s.%s" % (base, name) if base else str(name)


def _resolve(schema, root):
    """Resolve a local ``$ref`` chain against the schema root."""
    seen = 0
    while isinstance(schema, dict) and "$ref" in schema:
        ref = schema["$ref"]
        if not isinstance(ref, str) or not ref.startswith("#/"):
            raise LoadError("only local JSON Pointer $refs are supported, got %r" % (ref,))
        node = root
        for part in ref[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            if not isinstance(node, dict) or part not in node:
                raise LoadError("unresolvable $ref %r" % (ref,))
            node = node[part]
        schema = node
        seen += 1
        if seen > 32:
            raise LoadError("$ref chain is too deep")
    return schema


def _validate(value, schema, root, path, errors):
    schema = _resolve(schema, root)
    if not isinstance(schema, dict):
        errors.append("%s: schema node is not an object" % (path or "<root>"))
        return
    types = schema.get("type")
    if types is not None:
        names = types if isinstance(types, list) else [types]
        if not any(_type_ok(value, name) for name in names):
            errors.append(
                "%s: expected %s, got %s" % (path or "<root>", " or ".join(names), _typename(value))
            )
            return
    if "const" in schema and value != schema["const"]:
        errors.append(
            "%s: must be %r (the schema identifier changes only with an explicit bump, Core §9.4)"
            % (path or "<root>", schema["const"])
        )
    enum = schema.get("enum")
    if enum is not None and value not in enum:
        errors.append("%s: must be one of %s" % (path or "<root>", ", ".join(repr(e) for e in enum)))
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append("%s: must be at least %d character(s) long" % (path, schema["minLength"]))
        pattern = schema.get("pattern")
        if pattern and not re.search(pattern, value):
            errors.append("%s: %r does not match the required form %s" % (path, value, pattern))
    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append("%s: must be >= %s" % (path, schema["minimum"]))
    if isinstance(value, dict):
        if "minProperties" in schema and len(value) < schema["minProperties"]:
            errors.append(
                "%s: must contain at least %d field(s)" % (path or "<root>", schema["minProperties"])
            )
        for name in schema.get("required", []):
            if name not in value:
                errors.append("%s: a required field is missing" % _join(path, name))
        props = schema.get("properties") or {}
        additional = schema.get("additionalProperties", True)
        for name in sorted(value):
            child = _join(path, name)
            if name in props:
                _validate(value[name], props[name], root, child, errors)
            elif additional is False:
                errors.append(
                    "%s: not one of the contents the protocol enumerates (Distribution §3/§3.1); "
                    "the field set is closed, so adding one is a protocol revision" % child
                )
            elif isinstance(additional, dict):
                _validate(value[name], additional, root, child, errors)
    if isinstance(value, list):
        if schema.get("uniqueItems"):
            seen = set()
            for item in value:
                marker = json.dumps(item, sort_keys=True, default=str)
                if marker in seen:
                    errors.append("%s: duplicate item %r" % (path, item))
                seen.add(marker)
        items = schema.get("items")
        if isinstance(items, dict):
            for index, item in enumerate(value):
                _validate(item, items, root, "%s[%d]" % (path, index), errors)


def _validate_with_jsonschema(doc, schema):
    import jsonschema

    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)

    def fmt(absolute_path):
        out = ""
        for part in absolute_path:
            out = "%s[%d]" % (out, part) if isinstance(part, int) else (out + "." + str(part) if out else str(part))
        return out or "<root>"

    return ["%s: %s" % (fmt(err.absolute_path), err.message) for err in validator.iter_errors(doc)]


def _check_manifest(doc, schema):
    errors = []
    try:
        errors.extend(_validate_with_jsonschema(doc, schema))
        engine = "jsonschema"
    except ImportError:
        _validate(doc, schema, schema, "", errors)
        engine = "stdlib-schema"
    errors.extend(_cross_field_manifest(doc))
    return errors, engine


def _cross_field_manifest(doc):
    """Cross-field rules the protocol states in prose rather than in a field."""
    errors = []
    if not isinstance(doc, dict):
        return errors
    eligibility = doc.get("eligibility")
    if isinstance(eligibility, dict):
        if eligibility.get("isolation_class") == "full_isolation":
            allowlist = eligibility.get("egress_allowlist")
            if isinstance(allowlist, list) and allowlist:
                errors.append(
                    "eligibility.egress_allowlist: a full_isolation determination must declare an "
                    "empty allowlist (Distribution §5.2/§5.3: full-isolation runs reach no external "
                    "endpoint by design)"
                )
    return errors


# ---------------------------------------------------------------------------
# Redacted manifest summary (Distribution §5.1 closed field set)
# ---------------------------------------------------------------------------

SUMMARY_FIELDS = (
    "case_id",
    "manifest_sha256",
    "base_bundle_sha256",
    "oracle_pack_sha256",
    "spec_sha256",
    "protocol_sha256",
    "cutoff_utc",
    "profile",
    "isolation_class",
    "construction",
    "producer",
    "retirement",
    "index_version",
)
SUMMARY_CONSTRUCTION_FIELDS = ("git_version", "bundle_format_version", "hash_algorithm", "bundle_size")
SUMMARY_PRODUCER_FIELDS = ("identity", "signing_key_id")

SUMMARY_EXCLUDED = {
    "cutoff_commit": "the resolved cutoff commit",
    "provenance": "source-identifying provenance",
    "source_event": "source-identifying provenance",
    "time_to_topology": "the time-to-topology evidence",
    "available_information_manifest": "the available-information manifest",
    "candidate_input_bundle": "candidate_input_bundle",
    "rubric": "the rubric",
    "oracle_path": "oracle paths",
    "oracle_pack_path": "oracle paths",
    "cutoff_rule": "the cutoff rule and its script-output hash",
    "cutoff_rule_sha256": "the cutoff rule and its script-output hash",
    "leak_check": "the leak-check procedure",
    "leak_check_procedure": "the leak-check procedure",
    "allowlist": "the allowlist itself (only the isolation class is published)",
    "egress_allowlist": "the allowlist itself (only the isolation class is published)",
}


def _check_summary(doc):
    errors = []
    if not isinstance(doc, dict):
        errors.append(
            "<root>: a redacted summary must be a mapping of the Distribution §5.1 field set, got %s"
            % _typename(doc)
        )
        return errors
    keys = set(doc)
    for name in sorted(keys):
        if name in SUMMARY_FIELDS:
            continue
        if name in SUMMARY_EXCLUDED:
            errors.append(
                "%s: excluded from the redacted summary — Distribution §5.1 names %s as excluded and "
                "closes the field set" % (name, SUMMARY_EXCLUDED[name])
            )
        else:
            errors.append(
                "%s: not part of the Distribution §5.1 closed field set — a summary carries exactly "
                "the enumerated fields and no others" % name
            )
    for name in SUMMARY_FIELDS:
        if name not in keys:
            errors.append(
                "%s: missing — Distribution §5.1 closes the field set to exactly the enumerated "
                "fields (this validator uses one canonical spelling per §5.1 concept)" % name
            )
    for name in ("manifest_sha256", "base_bundle_sha256", "oracle_pack_sha256", "spec_sha256", "protocol_sha256"):
        value = doc.get(name)
        if isinstance(value, str) and not re.fullmatch(SHA256_RE, value):
            errors.append("%s: not a lowercase hexadecimal SHA-256 (Distribution §2)" % name)
    isolation = doc.get("isolation_class")
    if isolation is not None and isolation not in ("full_isolation", "allowlisted"):
        errors.append(
            "isolation_class: must be 'full_isolation' or 'allowlisted' (Distribution §5.1/§5.2)"
        )
    cutoff = doc.get("cutoff_utc")
    if isinstance(cutoff, str) and not re.fullmatch(CUTOFF_RE, cutoff):
        errors.append("cutoff_utc: must be UTC at second-or-finer precision (Core §4.2, Distribution §3.2)")
    for group, allowed in (("construction", SUMMARY_CONSTRUCTION_FIELDS), ("producer", SUMMARY_PRODUCER_FIELDS)):
        block = doc.get(group)
        if block is None:
            continue
        if not isinstance(block, dict):
            errors.append("%s: must be a mapping" % group)
            continue
        for name in sorted(set(block) - set(allowed)):
            errors.append("%s.%s: not part of the Distribution §5.1 field set for %s" % (group, name, group))
    index_version = doc.get("index_version")
    if index_version is not None and (
        isinstance(index_version, bool) or not isinstance(index_version, (str, int))
    ):
        errors.append("index_version: must be a sequence number or a head hash (Distribution §4)")
    return errors


# ---------------------------------------------------------------------------
# Kind detection and CLI
# ---------------------------------------------------------------------------

MANIFEST_ONLY = {
    "cutoff_commit",
    "provenance",
    "time_to_topology",
    "cutoff_rule",
    "artifacts",
    "eligibility",
    "leak_check",
    "candidate_input_bundle",
    "available_information_manifest",
}
SUMMARY_ONLY = {"index_version", "manifest_sha256"}


def detect_kind(doc):
    if not isinstance(doc, dict):
        return None
    keys = set(doc)
    # ``manifest_sha256`` is the manifest's own digest: the manifest never
    # carries it, so its presence is a summary signature that survives even
    # when the document also carries an excluded field (e.g. cutoff_commit).
    if "manifest_sha256" in keys or ("index_version" in keys and "provenance" not in keys):
        return "summary"
    if keys & MANIFEST_ONLY:
        return "manifest"
    if keys & SUMMARY_ONLY:
        return "summary"
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="validate_manifest.py",
        description=(
            "Validate an AMBER Case Manifest (Distribution §3) against "
            "schemas/manifest.schema.json, or a redacted manifest summary against "
            "the closed field set of Distribution §5.1."
        ),
    )
    parser.add_argument("paths", nargs="+", type=Path, help="manifest or summary file(s), YAML or JSON")
    parser.add_argument(
        "--kind",
        choices=("auto", "manifest", "summary"),
        default="auto",
        help="document kind (default: auto-detect)",
    )
    parser.add_argument("--schema", type=Path, default=SCHEMA_PATH, help="path to the manifest JSON Schema")
    parser.add_argument(
        "--loader",
        choices=("auto", "pyyaml", "stdlib"),
        default="auto",
        help="YAML backend (default: PyYAML when importable, else the standard-library fallback)",
    )
    parser.add_argument("--verbose", action="store_true", help="report the backend and detected kind on stderr")
    args = parser.parse_args(argv)

    try:
        schema = json.loads(args.schema.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("ERROR  cannot load the schema %s: %s" % (args.schema, exc), file=sys.stderr)
        return EXIT_UNUSABLE

    overall = EXIT_OK
    for path in args.paths:
        try:
            doc, backend = load_document(path, args.loader)
        except LoadError as exc:
            print("FAIL   %s  [unreadable]" % path, file=sys.stderr)
            print("  - %s" % exc, file=sys.stderr)
            overall = EXIT_UNUSABLE
            continue

        kind = args.kind
        if kind == "auto":
            kind = detect_kind(doc)
            if kind is None:
                print("FAIL   %s  [kind not detected]" % path, file=sys.stderr)
                print(
                    "  - the document is neither a manifest (Distribution §3: no provenance/cutoff_commit/"
                    "artifacts/eligibility/leak_check/...) nor a redacted summary (§5.1: no index_version/"
                    "manifest_sha256); pass --kind",
                    file=sys.stderr,
                )
                overall = EXIT_UNUSABLE
                continue

        if args.verbose:
            print("       backend=%s kind=%s" % (backend, kind), file=sys.stderr)

        if kind == "manifest":
            errors, engine = _check_manifest(doc, schema)
        else:
            errors, engine = _check_summary(doc), "closed-set"

        if errors:
            print("FAIL   %s  [%s]" % (path, kind), file=sys.stderr)
            for message in errors:
                print("  - %s" % message, file=sys.stderr)
            if overall == EXIT_OK:
                overall = EXIT_INVALID
        else:
            detail = "  backend=%s" % backend if args.verbose else ""
            if kind == "manifest" and isinstance(doc, dict):
                detail += "  schema_version=%s" % doc.get("schema_version")
            print("PASS   %s  [%s]  engine=%s%s" % (path, kind, engine, detail))

    return overall


if __name__ == "__main__":
    sys.exit(main())
