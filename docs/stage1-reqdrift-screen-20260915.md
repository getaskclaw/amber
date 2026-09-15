# Stage-1 screen result — `A-0676097b` × `gpt-5.6-luna-900k@openai-codex:high` (2026-09-15)

Second designed-stability dataset under `protocols/stability.md`. Stage-0 flagged
`A-0676097b` (req-drift face, a four-variant bundle) for a **regression** flip on
this arm: r1/r2 pass 4/4 → r3 fail 2/4 across days. This screen reruns the whole
case n=5 in one sitting.

## Setup

| field | value |
|---|---|
| arm | `gpt-5.6-luna-900k@openai-codex:high` (dedicated bench profile) |
| harness | AMBER agentic harness — full-library driver (case-filtered), `hermes chat` tools ON, multi-variant calibration-runner contract |
| case pin | bundle_sha `3c04bb80fe94`, oracle_sha `307238137be9` — identical on all 20 runs |
| unit | one **case attempt** = 4 variant runs (V1–V4; variant names stay private); case passes only if all 4 are green |
| window (UTC) | 2026-09-15 02:45 → 03:05 |
| wire audit | state.db `session_model_usage`: 20/20 sessions on `gpt-5.6-luna-900k @ openai-codex` (39 usage rows, zero substitute); ~766K in / 79K out tokens total |
| artifacts | per-round run dirs in the private sandbox (manifest + transcript + oracle.log per run); driver script and aggregator in the same sandbox |

## Result: 3/5 case pass — regression reproduces, and it is the same two variants

| round | V1 | V2 | V3 | V4 | case |
|---|---|---|---|---|---|
| r1 | ✓ | ✓ | ✓ | ✓ | **PASS 4/4** |
| r2 | ✓ | ✓ | ✓ | ✓ | **PASS 4/4** |
| r3 | ✓ | ✓ | ✓ | ✓ | **PASS 4/4** |
| r4 | ✓ | ✗ no deliverable | ✗ score 50 | ✓ | FAIL 2/4 |
| r5 | ✓ | ✗ score 47 | ✗ score 20 | ✓ | FAIL 2/4 |

Case pass ≈ **0.60**, Wilson 95% CI ≈ **[0.23, 0.88]** — n=5 separates "stable
pass" from "stable fail" but cannot pin the rate tighter. Variant-level:
V1/V4 10/10 pass; V2 3/5; V3 3/5.

## Failure mechanism: facts found, escalation label missed

The oracle expects one specific escalation classification on the hidden variants
(the exact label set is part of the case's private answer key). Every judged
failure still found the **correct requirement IDs** — detection recall is not
the problem. The misses all chose a sibling classification (oracle-scored
20–50) instead of the expected one: the knife edge is a **classification
boundary between two escalation families**, not detection.

Two distinct failure modes appeared:

- **judged-wrong-answer** (r4 V3, r5 V2, r5 V3): deliverable present,
  oracle-scored 20–50.
- **no-deliverable** (r4 V2): the transcript claims the decision file was
  written and validated; the file is absent from the rundir — a
  delivery-contract failure with a **hallucinated delivery claim**.

Failures cluster in rounds 4–5 (02:56–03:05 UTC); n=5 is too small to separate
arm flakiness from a time-correlated condition — flagged, not concluded.

## Interpretation

Published r1/r2 pass + r3 fail was read as possible cross-day drift. This screen
reproduces the 2/4 fail shape twice within 20 minutes, on the same two
variants, with the same misclassification — the arm sits on this case's
decision boundary **within a sitting**. Combined record: r1 ✓, r2 ✓, r3 ✗,
screen 3/5 → the case is **boundary-unstable for this arm**, not regressed.

Consistent with crof W36 (`✓4/4 | ✗2/4 | ✓4/4 | ✓4/4 | ✗1/4` across five arms):
`A-0676097b` discriminates arms on escalation-classification discipline, and
mid-discipline arms flip on it.

## Protocol notes driven by this screen

- Multi-variant cases: report the **per-variant vector**, not just the case
  score — here the case-level flip decomposes cleanly into two stable variants
  and two boundary variants.
- `no deliverable` stays a `valid_task_failure` (model-side), but record it
  separately from oracle-judged failures: the failure modes have different
  causes and different fixes.
- Watch for **time-clustered failures** before treating n runs as iid —
  sequential screens on one endpoint can correlate.
