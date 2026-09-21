"""金标 JSONL 校验器(契约: contracts/golden-jsonl.md)。
用法: python3 scoring/validate.py data/smoke-12.jsonl
也作为模块被 driver 调用。校验失败抛 DatasetError(含行号与原因)。
"""
import json
import sys

VALID_TYPES = {"choice", "score", "noul"}
REQUIRED_TOP = ("id", "family", "state", "question", "gold", "source")


class DatasetError(Exception):
    pass


def _check(cond, lineno, msg):
    if not cond:
        raise DatasetError(f"line {lineno}: {msg}")


def validate_record(rec, lineno):
    for f in REQUIRED_TOP:
        _check(f in rec, lineno, f"missing field '{f}'")
    q = rec["question"]
    _check(isinstance(q, dict), lineno, "'question' must be an object")
    _check(q.get("id") == rec["id"], lineno,
           f"question.id ({q.get('id')!r}) must equal top-level id ({rec['id']!r})")
    t = q.get("type")
    _check(t in VALID_TYPES, lineno, f"question.type must be one of {sorted(VALID_TYPES)}, got {t!r}")
    _check(isinstance(q.get("instructions"), str) and q["instructions"].strip(),
           lineno, "question.instructions must be a non-empty string")
    gold = rec["gold"]
    if t == "choice":
        opts = q.get("options")
        _check(isinstance(opts, dict) and len(opts) >= 2, lineno,
               "choice requires question.options with >=2 entries")
        _check(all(isinstance(k, str) and isinstance(v, str) for k, v in opts.items()),
               lineno, "options must map str->str")
        _check(gold in opts, lineno, f"gold {gold!r} not in options keys {list(opts)}")
    elif t == "score":
        crit = q.get("criteria")
        _check(isinstance(crit, list) and len(crit) >= 2, lineno,
               "score requires question.criteria list with >=2 levels")
        _check(all(isinstance(c, str) for c in crit), lineno, "criteria must be strings")
        _check(isinstance(gold, int) and not isinstance(gold, bool), lineno,
               "score gold must be an int level index")
        _check(0 <= gold < len(crit), lineno,
               f"score gold {gold} out of range 0..{len(crit)-1}")
    else:  # noul
        _check(isinstance(gold, bool), lineno, "noul gold must be a boolean")
    return rec


def load_dataset(path):
    """读 JSONL, 校验全部行, 返回 (records, errors)。任何错误即整体拒绝。"""
    records = []
    seen = set()
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                raise DatasetError(f"line {lineno}: invalid JSON: {e}") from e
            _check(isinstance(rec, dict), lineno, "record must be a JSON object")
            _check(rec["id"] not in seen, lineno, f"duplicate id {rec['id']!r}")
            seen.add(rec["id"])
            records.append(validate_record(rec, lineno))
    _check(len(records) > 0, 0, "dataset is empty")
    return records


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 scoring/validate.py <dataset.jsonl>", file=sys.stderr)
        sys.exit(2)
    try:
        recs = load_dataset(sys.argv[1])
    except DatasetError as e:
        print(f"INVALID: {e}", file=sys.stderr)
        sys.exit(1)
    fams = {}
    types = {}
    for r in recs:
        fams[r["family"]] = fams.get(r["family"], 0) + 1
        types[r["question"]["type"]] = types.get(r["question"]["type"], 0) + 1
    print(f"OK: {len(recs)} records valid")
    print(f"families ({len(fams)}): {fams}")
    print(f"types: {types}")
