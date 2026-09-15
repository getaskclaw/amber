#!/usr/bin/env python3
"""Derive docs/data/flip-list-2026-09-14.csv from the case-run matrix.

Two evidence layers:
  matrix — mechanically derived from case-run-matrix-2026-09-14.csv
           (republished=0 cells only). Repeat observations of the same
           (case, arm_id) are diffed for status flips and severity drift.
  prose  — events documented in results-file prose where no per-case
           matrix was published (luna r3, 09-12 re-sweep, infra-reruns,
           anchor reruns). Each row carries its source reference.

event_type: status_flip | severity_drift | recovery_in_run | infra_rerun |
            reproduction | evidence_gap
span:       same_run | same_day | cross_day | cross_week
"""

import csv
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
MATRIX = BASE / "case-run-matrix-2026-09-14.csv"
OUT = BASE / "flip-list-2026-09-14.csv"

RUN_ORDER = {"primary": 0, "makeup": 1, "retest": 2}
FIELDS = ["case", "face", "arm_id", "n_obs", "event_type", "observation",
          "direction", "span", "evidence", "source_ref"]

rows_out = []


def emit(case, face, arm, n, etype, obs, direction, span, evidence, src):
    rows_out.append(dict(case=case, face=face, arm_id=arm, n_obs=n,
                         event_type=etype, observation=obs,
                         direction=direction, span=span,
                         evidence=evidence, source_ref=src))


# ---------- matrix-derived layer ----------
rows = [r for r in csv.DictReader(open(MATRIX)) if r["republished"] == "0"]

obs = {}
for r in rows:
    obs.setdefault((r["case"], r["arm_id"]), []).append(r)

def sortkey(r):
    return (r["source"], RUN_ORDER.get(r["run_tag"], 9))


def score_of(detail):
    """Numeric content of a detail cell: '4/4' fraction or signed scalar.
    Returns None when the cell carries no score (bare checkmark or note)."""
    d = re.sub(r"[✓✗∅⊘—]", "", detail)
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*/\s*(\d+)", d)
    if m:
        return (float(m.group(1)), float(m.group(2)))
    m = re.search(r"-?\d+(?:\.\d+)?", d)
    return float(m.group(0)) if m else None

for (case, arm), rs in sorted(obs.items()):
    if len(rs) < 2:
        continue
    rs.sort(key=sortkey)
    face = rs[0]["face"]
    seq = " -> ".join(f'{r["status"]} {r["detail"]}'.strip() for r in rs)
    srcs = "; ".join(f'{r["source"]} [{r["run_tag"]}]' for r in rs)
    statuses = [r["status"] for r in rs]
    span = "cross_week" if len({r["source"] for r in rs}) > 1 else "same_day"
    if len(set(statuses)) > 1:
        direction = "regression" if statuses[-1] == "fail" else "recovery"
        emit(case, face, arm, len(rs), "status_flip", seq, direction, span,
             "matrix", srcs)
    elif all(s == "fail" for s in statuses):
        # a scored fail (x/y) and a bare fail carry different evidence
        sigs = [score_of(r["detail"]) or "bare-fail" for r in rs]
        if len(set(sigs)) > 1:
            emit(case, face, arm, len(rs), "severity_drift", seq,
                 "worsened_or_changed", span, "matrix", srcs)
    for r in rs:
        if re.search(r"复测|重跑|rerun|retest", r["detail"]):
            emit(case, face, arm, len(rs), "recovery_in_run",
                 r["detail"], "recovery", "same_run", "matrix",
                 f'{r["source"]} [{r["run_tag"]}]')

# prose-sourced extra observations the matrix cannot hold (one cell = one
# printed value): amend n_obs / observation of matching matrix-layer rows.
OBS_AMEND = {
    ("A-a317e74b", "glm-5.3-flash@ollama"): (
        3, " ; second same-day 0/15 run reported in W37 prose "
           "(amber-ollama 2026-W37 case-diff notes)"),
}
for r in rows_out:
    key = (r["case"], r["arm_id"])
    if key in OBS_AMEND:
        n, suffix = OBS_AMEND[key]
        r["n_obs"] = n
        r["observation"] += suffix

# ---------- prose-sourced layer ----------
# luna-high third full-library run (2026-09-12), per-case data published
# as prose only; r1/r2 byte-identical fail set is the W37 matrix column.
LH = "gpt-5.6-luna-900k@openai-codex:high"
LM = "gpt-5.6-luna-900k@openai-codex:medium"
SRC_G37 = "amber-gpt/results/2026-W37.md [addendum 2026-09-12, prose]"
emit("A-ea80d793", "vision", LH, 3, "status_flip",
     "r1/r2 fail (printed d2 -2; per-run d2 unpublished) -> r3 pass",
     "recovery", "cross_day", "prose", SRC_G37)
emit("A-0676097b", "req-drift", LH, 3, "status_flip",
     "r1/r2 pass 4/4 -> r3 fail 2/4", "regression", "cross_day", "prose", SRC_G37)
emit("A-a317e74b", "verify", LH, 3, "severity_drift",
     "W37 matrix 12/15 -> r3 14/15 (fail throughout; per-run partials "
     "unpublished)", "improved_still_fail", "cross_day", "prose", SRC_G37)
emit("(unpublished)", "?", LM, 2, "evidence_gap",
     "15/23 (W37) -> 14/23 (2026-09-12 re-sweep); flipped case not published",
     "regression", "cross_day", "prose", SRC_G37)

# frontier anchor clean-wire reruns of the vision case (W36 errata).
emit("A-ea80d793", "vision", "frontier-anchor@openai-codex:high", 3,
     "status_flip", "clean-wire reruns: fail 2.0 / fail -2 / pass 3.0",
     "mixed", "cross_day", "prose",
     "amber-ollama/results/2026-W36.md [errata]; amber-crof W36 errata")

# infra-rerun recoveries (harness-side invalids re-run under infra discipline).
SRC_D37 = "amber-devin/results/2026-W37.md [harness notes, prose]"
emit("A-8c909d0a", "ops", "swe-1-7-medium@devin", 2, "infra_rerun",
     "invalid_infrastructure (38.5 s ACP drop) -> same-day makeup valid pass",
     "recovery", "same_day", "prose", SRC_D37)
emit("A-8c909d0a", "ops", "swe-2-max@devin", 2, "infra_rerun",
     "invalid_infrastructure (49 s ACP drop) -> makeup valid pass",
     "recovery", "same_day", "prose", SRC_D37)
emit("A-a317e74b", "verify", "swe-2-low@devin", 3, "infra_rerun",
     "invalid_infrastructure x2 (v0.21.2 ACP stall) -> terminal-lane makeup "
     "valid fail 7/15", "recovery_of_valid_score", "same_day", "prose", SRC_D37)
emit("A-a317e74b", "verify", "swe-2-max@devin", 4, "infra_rerun",
     "1800 s cap timeout x2 + 3600 s cap makeup timeout x2 -> owed, not scored",
     "no_recovery", "same_day", "prose", SRC_D37)

# glm-5-2 delivery-contract defect reproduced (stability, not flake).
emit("(6 papers)", "delivery-contract", "glm-5-2@devin", 3, "reproduction",
     "delivery failure reproduced on 2 same-day makeup replays - stable "
     "defect, not sampling luck", "stable", "same_day", "prose", SRC_D37)

# wb / opencode infra retries that recovered a valid score (not a pass).
emit("A-a317e74b", "verify", "hy4-preview-f@workbuddy", 2, "infra_rerun",
     "invalid -> retry valid fail 14/15", "recovery_of_valid_score",
     "same_day", "prose", "amber-workbuddy/results/2026-W37.md [prose]")
emit("A-a317e74b", "verify", "deepseek-v4.1-flash@opencode-go", 2,
     "infra_rerun", "invalid -> retry valid fail 7/15",
     "recovery_of_valid_score", "same_day", "prose",
     "amber-opencode/results/2026-W37.md [prose]")

with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows_out)
print(f"wrote {OUT.name}: {len(rows_out)} events")
