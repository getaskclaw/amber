#!/usr/bin/env python3
"""Rebuild docs/data/case-run-matrix-2026-09-14.csv from published amber-* result matrices.

Every published per-case markdown matrix is described by an explicit table spec:
file, header line, and a column->(arm_id, run_tag) mapping. Nothing is inferred
from column position, so a missing optional column (e.g. bundle_sha) cannot
silently eat an arm column.

arm_id is canonical: `model@lane` (+ `:band` where the lane separates bands).
Lane is part of the arm — a model name alone is not.

republished=1 marks cells that re-print an observation whose home results repo
is elsewhere (cross-vendor comparison columns, digest tables, signature
reprints). They are real published cells but NOT independent observations;
dedupe on (case, arm_id) before counting repeats.
"""

import csv
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]  # ~/2606
OUT = Path(__file__).resolve().parent / "case-run-matrix-2026-09-14.csv"

GPT36 = "amber-gpt/results/2026-W36.md"
GPT37 = "amber-gpt/results/2026-W37.md"
CROF36 = "amber-crof/results/2026-W36.md"
CROF37 = "amber-crof/results/2026-W37.md"
OLL36 = "amber-ollama/results/2026-W36.md"
OLL37 = "amber-ollama/results/2026-W37.md"
DS37 = "amber-deepseek/results/2026-W37.md"
CC37 = "amber-commandcode/results/2026-W37.md"
OC37 = "amber-opencode/results/2026-W37.md"
WB37 = "amber-workbuddy/results/2026-W37.md"
DV37 = "amber-devin/results/2026-W37.md"

# (source, section, {printed column header: (arm_id, run_tag, republished)})
SPECS = [
    (GPT36, "Full matrix", {
        "low": ("gpt-6-astra-900k@openai-codex:low", "primary", 0),
        "medium": ("gpt-6-astra-900k@openai-codex:medium", "primary", 0),
        "high": ("gpt-6-astra-900k@openai-codex:high", "primary", 0),
        "xhigh": ("gpt-6-astra-900k@openai-codex:xhigh", "primary", 0),
        "max": ("gpt-6-astra-900k@openai-codex:max", "primary", 0),
    }),
    (GPT37, "Full matrix", {
        "luna m": ("gpt-5.6-luna-900k@openai-codex:medium", "primary", 0),
        "luna h": ("gpt-5.6-luna-900k@openai-codex:high", "primary", 0),
        "luna xh": ("gpt-5.6-luna-900k@openai-codex:xhigh", "primary", 0),
        "sol m": ("gpt-5.6-sol-900k@openai-codex:medium", "primary", 0),
        "sol h": ("gpt-5.6-sol-900k@openai-codex:high", "primary", 0),
    }),
    (GPT37, "Makeup matrix (2 new ops cases)", {
        "gpt-6-astra（裸）": ("gpt-6-astra@openai-codex", "makeup", 0),
    }),
    (CROF36, "Full matrix", {
        "d4f": ("deepseek-v4-flash:0731@crof", "primary", 0),
        "d4fv": ("deepseek-v4-flash-vision-exp@crof", "primary", 0),
        "g53f": ("glm-5.3-flash@crof", "primary", 0),
        "q38": ("qwen3.8-27b@crof", "primary", 0),
        "q35": ("qwen3.5-9b@crof", "primary", 0),
    }),
    (CROF37, "Makeup matrix", {
        "qwen3.8-27b": ("qwen3.8-27b@crof", "makeup", 0),
        "d4f-0731": ("deepseek-v4-flash:0731@crof", "makeup", 0),
        "glm-5.3-flash": ("glm-5.3-flash@crof", "makeup", 0),
    }),
    (OLL36, "Full matrix", {
        "d4f": ("deepseek-v4-flash:0731@ollama", "primary", 0),
        "g53f": ("glm-5.3-flash@ollama", "primary", 0),
    }),
    (OLL36, "Cross-vendor digest", {
        "glm-5.3-flash crof": ("glm-5.3-flash@crof", "primary", 1),
        "glm-5.3-flash ollama": ("glm-5.3-flash@ollama", "primary", 1),
        "d4f-0731 crof": ("deepseek-v4-flash:0731@crof", "primary", 1),
        "d4f-0731 ollama": ("deepseek-v4-flash:0731@ollama", "primary", 1),
    }),
    (OLL37, "Makeup matrix", {
        "glm-5.3-flash": ("glm-5.3-flash@ollama", "makeup", 0),
        "deepseek-v4-flash:0731": ("deepseek-v4-flash:0731@ollama", "makeup", 0),
    }),
    (OLL37, "Head-to-head matrix (same day/band/endpoint)", {
        "glm-5.3-flash": ("glm-5.3-flash@ollama", "retest", 0),
        "deepseek-v4.1-flash": ("deepseek-v4.1-flash@ollama", "primary", 0),
    }),
    (DS37, "Full matrix (same-family comparison)", {
        "deepseek-flash（官方 GA,W37）": ("deepseek-flash@deepseek-official", "primary", 0),
        "v4.1-flash-exp（官方，W37）": ("deepseek-v4.1-flash-exp@deepseek-official", "primary", 0),
        "d4f-0731(CrofAI,W36)": ("deepseek-v4-flash:0731@crof", "primary", 1),
        "d4f:0731(Ollama,W36)": ("deepseek-v4-flash:0731@ollama", "primary", 1),
    }),
    (DS37, "Addendum signature matrix", {
        "预览版 W37": ("deepseek-v4.1-flash-exp@deepseek-official", "primary", 1),
        "正代 2026-09-10": ("deepseek-flash@deepseek-official", "primary", 1),
    }),
    (CC37, "Full matrix (same-name cross-vendor)", {
        "v4.1-flash @ CommandCode": ("deepseek-v4.1-flash@commandcode", "primary", 0),
        "v4.1-flash @ OpenCode Go": ("deepseek-v4.1-flash@opencode-go", "primary", 1),
        "v4.1-flash-exp 预览 @ 官方": ("deepseek-v4.1-flash-exp@deepseek-official", "primary", 1),
    }),
    (OC37, "Full matrix (same-name cross-vendor)", {
        "v4.1-flash @ OpenCode Go": ("deepseek-v4.1-flash@opencode-go", "primary", 0),
        "v4.1-flash @ CommandCode": ("deepseek-v4.1-flash@commandcode", "primary", 1),
        "v4.1-flash-exp 预览 @ 官方": ("deepseek-v4.1-flash-exp@deepseek-official", "primary", 1),
    }),
    (WB37, "Full matrix", {
        "deepseek-v4.1-flash (wb)": ("deepseek-v4.1-flash@workbuddy", "primary", 0),
        "hy4-preview-f (wb)": ("hy4-preview-f@workbuddy", "primary", 0),
        "deepseek-flash（官方 GA，对照）": ("deepseek-flash@deepseek-official", "primary", 1),
    }),
    (DV37, "Full matrix", {
        "swe-1-7-medium": ("swe-1-7-medium@devin", "primary", 0),
        "glm-5-2": ("glm-5-2@devin", "primary", 0),
        "swe-2-high": ("swe-2-high@devin", "primary", 0),
        "swe-2-medium": ("swe-2-medium@devin", "primary", 0),
        "swe-2-max": ("swe-2-max@devin", "primary", 0),
        "swe-2-low": ("swe-2-low@devin", "primary", 0),
    }),
]

CASE_ALIAS = re.compile(r"A-[0-9a-f]{8}")
FACES = {"req-drift", "text", "ops", "build", "review", "verify", "vision",
         "ui-build"}
# annotations seen folded into case cells (digest tables have no face column)
FACE_NORM = {
    "vision review": "vision",
    "adversarial review": "review",
    "hardest build": "build",
    "ui-build": "ui-build",
}


def norm_face(text):
    t = text.strip().strip("()").strip().lower()
    return FACE_NORM.get(t, t if t in FACES else t)


# printed-mark semantics for unscored cells, keyed by (case, arm_id).
# Sources disclose these in findings/harness notes; they are NOT all
# infrastructure invalids — a model-side delivery failure must never be
# counted as infrastructure noise.
UNSCORED_CAUSE = {
    ("A-a317e74b", "swe-2-max@devin"): "infrastructure_timeout_owed",
    ("A-a317e74b", "gpt-5.6-sol-900k@openai-codex:high"):
        "infrastructure_timeout",
    ("A-d511f9e8", "gpt-5.6-sol-900k@openai-codex:high"):
        "infrastructure_timeout",
    ("A-984e80ee", "qwen3.5-9b@crof"): "model_delivery_budget_burn",
}


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def clean(text):
    return text.replace("**", "").replace("²", "").strip()


def status_of(detail):
    d = clean(detail)
    if "✓" in d:
        return "pass"
    if "✗" in d:
        return "fail"
    if "∅" in d or "⊘" in d:
        return "invalid_or_pending"
    if d in ("—", "", "-"):
        return "missing"
    return "other"


def parse_table(lines, header_idx, colmap):
    header = cells(lines[header_idx])
    face_idx = header.index("face") if "face" in header else None
    rows = []
    for line in lines[header_idx + 2:]:  # skip the |---| separator
        if not line.strip().startswith("|"):
            break
        parts = cells(line)
        if len(parts) < len(header):
            continue
        m = CASE_ALIAS.search(parts[0])
        if not m:
            if "total" in parts[0].lower():
                continue  # digest tables can lead with a total row
            break  # footer ends the matrix
        case = m.group(0)
        if face_idx is not None and face_idx < len(parts):
            face = norm_face(parts[face_idx])
        elif "(" in parts[0]:
            # digest tables fold the face into the case cell as "(vision review)"
            face = norm_face(parts[0][parts[0].index("("):])
        else:
            face = ""
        for pos, name in enumerate(header):
            if name not in colmap:
                continue
            arm_id, run_tag, repub = colmap[name]
            detail = clean(parts[pos]) if pos < len(parts) else ""
            rows.append({
                "case": case,
                "face": face,
                "arm_label": name,
                "arm_id": arm_id,
                "run_tag": run_tag,
                "republished": repub,
                "status": status_of(detail),
                "detail": detail,
                "unscored_cause":
                    UNSCORED_CAUSE.get((case, arm_id), ""),
            })
    return rows


def find_headers(lines):
    out = []
    for i, ln in enumerate(lines):
        if not ln.strip().startswith("|"):
            continue
        c = cells(ln)
        if c and c[0].strip("* ").lower() in ("case", "case alias"):
            out.append(i)
    return out


def main():
    out_rows, report = [], []
    for source, section, colmap in SPECS:
        path = BASE / source
        lines = path.read_text(encoding="utf-8").splitlines()
        wanted = set(colmap)
        matched = 0
        for hi in find_headers(lines):
            if wanted <= set(cells(lines[hi])):
                rows = parse_table(lines, hi, colmap)
                for r in rows:
                    r["source"], r["section"] = source, section
                out_rows.extend(rows)
                matched += 1
                report.append(f"{source} [{section}] header@L{hi+1} -> {len(rows)} cells")
                break
        if not matched:
            report.append(f"{source} [{section}] !! NO MATCHING HEADER")
            print(report[-1], file=sys.stderr)

    fields = ["source", "section", "case", "face", "arm_label", "arm_id",
              "run_tag", "republished", "status", "detail", "unscored_cause"]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in sorted(out_rows, key=lambda r: (r["source"], r["case"], r["arm_id"])):
            w.writerow({k: r[k] for k in fields})

    print("\n".join(report))
    print(f"\nwrote {len(out_rows)} cells -> {OUT.name}")


if __name__ == "__main__":
    main()
