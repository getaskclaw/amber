# AMBER stability memo — historical drift evidence ($0 pass)

Date: 2026-09-14 (matrix rebuilt 2026-09-15 — see Extraction notes)

Status: evidence memo; no new candidate runs were executed for this document.

## Question

Does AMBER need a separate stability measurement, and can we get decision-grade evidence without paying for a full-library rerun?

## Bottom line

Yes on both counts. Existing published matrices already show that a headline `N/23` is a capability snapshot, not a stability certificate. They also show that the cheap next step is **conditional reruns of the current fail set**, not `full library × 20`.

## Method

Every published per-case matrix in the local `amber-*` checkouts was extracted into a normalized `case × arm` table by an explicit, per-table spec — [`docs/data/build-case-run-matrix.py`](data/build-case-run-matrix.py). Column positions are never inferred, so an optional `bundle_sha` column cannot eat an arm column.

- status: `✓` → pass, `✗` → fail, `∅`/`⊘` → invalid_or_pending, `—` → missing
- `arm_id` is canonical `model@lane[:band]` — the lane is part of the arm, so `glm-5.3-flash@crof` and `glm-5.3-flash@ollama` are different arms
- `run_tag` separates primary / makeup / retest observations of the same arm
- `republished=1` flags cells that re-print another repo's observation (cross-vendor comparison columns, digest tables, signature reprints) — real published cells, **not** independent observations
- `unscored_cause` discloses what a `∅` cell actually is, per the source's own findings: `infrastructure_timeout` / `infrastructure_timeout_owed` vs `model_delivery_budget_burn`. Bare `∅` marks conflate infrastructure and model-side delivery failure; they must not be counted as one bucket
- `face` is read from the table's `face` column when present; digest tables fold it into the case cell as a parenthetical, normalized to canonical face names (e.g. `(vision review)` → `vision`). Tables that publish no face get an empty field, not a guessed one

Output: [`docs/data/case-run-matrix-2026-09-14.csv`](data/case-run-matrix-2026-09-14.csv) — **900 published cells, 31 canonical arms** (701 home-published, 199 republished; 566 pass / 326 fail / 4 unscored `∅` / 4 missing). The 4 `∅` cells are **not** all infrastructure: 3 are `invalid_infrastructure` (swe-2-max `A-a317e74b` owed; sol-high `A-a317e74b`/`A-d511f9e8` timeouts) and 1 is a model-side delivery failure (`qwen3.5-9b` `A-984e80ee` budget burn) — split via the `unscored_cause` column, never merged. This is an extraction of already published evidence, not a new benchmark run.

## What the existing evidence already proves

| Evidence | Observation | Interpretation |
|---|---:|---|
| `glm-5.3-flash@ollama`, W36 primary vs W37 retest (`amber-ollama`) | the only **full-library same-arm repeat** in the set (cross-day): shared-21 pass set 15→14 (`A-ea80d793` pass→fail), headline `17/23 → 16/23`, plus `A-a317e74b` partial collapse `14/15 → 0/15` reproduced on re-run | Same-arm drift exists on the same endpoint and band. The attribution case's collapse — same paper, same band, same endpoint, reproduced — is stronger evidence than a one-case headline delta. |
| `luna-high`, W37 same-day duplicate (`amber-gpt` W37) | `15/23`, `15/23`; identical fail set | Same-day determinism exists for at least one arm. |
| `luna-high`, third high run on 2026-09-12 (`amber-gpt` W37 addendum) | `15/23` again, but `A-ea80d793` flipped fail→pass and `A-0676097b` flipped pass→fail | Headline stayed fixed while the fail set drifted by ±2 across days. Score stability and case-level stability are different measurements. |
| `glm-5.3-flash@ollama`, `A-984e80ee` (`amber-ollama` W37) | first attempt failed, immediate retest passed | Within-session recovery exists. It belongs in `pass@k`, not in the primary score. |
| Internal frontier anchor, `A-ea80d793` clean-wire reruns (`amber-crof`/`amber-ollama` W36 errata) | fail `2.0` / fail `-2` / pass `3.0` | A borderline case can recover on repeat. One case-level recovery in three attempts is real evidence of non-determinism, but too small for a publishable rate. |
| DeepSeek official preview → GA (`amber-deepseek` W37) | `14/23 → 16/23`; `A-791e90ac` and `A-47eea242` flipped | This is version drift, not same-arm stability. It shows why model/version identity must be pinned before a rerun is called a repeat. |
| `deepseek-v4.1-flash` across lanes (`amber-commandcode`, `amber-ollama`, `amber-deepseek`, `amber-opencode`, `amber-workbuddy`) | `17/17/16/16/15` across five lanes | Endpoint/lane is part of the measured arm. "Same model name" is not a stable unit of analysis. |
| Infra-rerun discipline (`amber-devin`, `amber-opencode`, `amber-workbuddy` W37) | `invalid_infrastructure` retries produced both passes (`swe-1-7-medium` `A-8c909d0a`) and valid fails (`swe-2-low` `A-a317e74b` 7/15; `hy4` `A-a317e74b` 14/15; OpenCode `A-a317e74b` 7/15) | Infrastructure retries are not model recovery and must be counted separately. |

## What the evidence does not yet prove

There is no publishable per-case recovery-rate table yet. Same-arm repeats exist but are shallow: one full-library `n=2` (glm@ollama), one `n=3` cross-day (luna-high), one `n=3` borderline-case rerun (the anchor). That is enough to justify a stability protocol, not enough to fill the column with percentages.

## Cheapest decision protocol

1. Freeze the latest valid primary run and its fail set.
2. Run **only the primary failures** for stage 1: `n = 5` valid repeat trials per failed case.
   - `0/5` means "no recovery observed"; it is a screen, not proof of a stable failure.
   - `≥1/5` means the case is flaky enough to justify confirmation.
3. Escalate to `n = 20` total valid trials only for cases with a recovery or cases that are decision-critical.
   - `0/20` supports "recovery is rare or unobserved": one-sided ~95% upper bound ≈ 14%.
   - `0/20` does **not** prove the recovery probability is zero.
4. Report `invalid_infrastructure`, `protocol_violation`, and owed/missing trials separately. Never fold them into model recovery.
5. Publish stability columns beside the capability score: `first-pass`, `pass@k`, `pass^k`, `recovery-after-fail`, side effects, and fail-set delta.

## Cost bound

Conditional reruns scale with the fail set, not the whole library.

- `18/23` primary: 5 failed cases → 25 case trials at `n=5`, at most 100 total case trials at `n=20` (screening trials count).
- `15/23` primary: 8 failed cases → 40 case trials at `n=5`, at most 160 total at `n=20`.
- For expensive lanes, use subscription/free lanes for the first drift evidence; reserve paid lanes for confirmation on cases that matter.

## Limits

- Failed-case reruns estimate **recovery after an observed failure**, not overall reliability.
- Repeats are not strictly iid: endpoint behavior, serving version, harness state, and wall-clock date can all drift.
- Same-day replication is not cross-day stability; cross-day drift is the more decision-relevant risk — and the only full-library same-arm repeat in this set is cross-day.
- Side effects need harness instrumentation; a markdown matrix can show pass/fail movement but cannot prove clean isolation by itself.
- Republished comparison cells are not independent observations; the matrix flags them instead of silently doubling the sample.

## Extraction notes

The first-pass CSV (also dated 2026-09-14) undercounted and mislabeled:

- Tables without a `bundle_sha` column lost their **first arm column** — 70 published cells were missing (astra `low` 21, `luna m` 23, `swe-1-7-medium` 23, preview-signature 3), plus one entire 2-cell makeup table (`gpt-6-astra（裸）`).
- Same-name columns on different lanes were merged into one "arm" (`g53f`, `d4f` across crof/ollama), producing 7 false same-arm conflicts; the same arm also appeared under up to three different labels.
- Republished cross-vendor columns were indistinguishable from home observations.

All three are fixed by the explicit-spec rebuild; this memo's numbers refer to the rebuilt matrix.

Derived artifact: [`docs/stage0-flip-analysis-2026-09-14.md`](stage0-flip-analysis-2026-09-14.md) — the case × arm flip inventory built on this matrix (17 events, matrix-derived + prose-flagged), with the stage-1 screening candidate list.

## Source set

- `amber-crof/results/2026-W36.md`, `2026-W37.md`
- `amber-deepseek/results/2026-W37.md`
- `amber-devin/results/2026-W37.md`
- `amber-gpt/results/2026-W36.md`, `2026-W37.md`
- `amber-ollama/results/2026-W36.md`, `2026-W37.md`
- `amber-commandcode/results/2026-W37.md`
- `amber-opencode/results/2026-W37.md`
- `amber-workbuddy/results/2026-W37.md`
