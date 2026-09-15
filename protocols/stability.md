# AMBER Stability Protocol

Draft v0.1, 2026-09-14. Companion to AMBER Core Specification v0.2.2 and Distribution Protocol v0.3. Where this protocol and Core conflict, Core wins. This protocol adds repeat-run statistics and reporting rules; it does not change case validity, scoring, terminal states, or the public/private split.

*v0.1, 2026-09-14. Initial draft prompted by external review: headline scores are capability snapshots, while operational stability needs separate, bounded evidence.*

## 1. Purpose

AMBER's primary score answers: "what did this arm do on this case set at this time?" Stability answers a different question: "when the same arm is tried again under the same pinned exam conditions, how often does the outcome move?"

The two measurements must not be merged. A headline `N/M` remains the primary capability snapshot. Stability metrics are reported beside it, never used to silently rewrite the primary score.

## 2. Terms and estimands

- **Arm**: the complete unit under test: provider endpoint, served model identifier or snapshot, effort/band, harness and version, evaluation profile, isolation/egress configuration, and case-set pin (`spec_sha256`, bundle sha256, oracle sha256, `index_version`). A change to any arm component is a different arm.
- **Primary run**: the run that produced the published capability score.
- **Repeat trial**: an independent later attempt at the same case under the same arm. A retry after `invalid_infrastructure` is an infrastructure rerun, not a repeat trial for task stability.
- **First-pass outcome**: the primary run's valid task outcome for a case.
- **`pass@k`**: at least one valid pass in `k` valid repeat trials.
- **`pass^k`**: all `k` valid repeat trials pass.
- **Recovery-after-fail**: for a case whose primary valid outcome is a failure, the fraction of valid repeat trials that pass. This is conditional on an observed failure; it is not an overall reliability estimate.
- **Fail-set delta**: the symmetric difference between two runs' failed-case sets. Report both directions: fail→pass recoveries and pass→fail regressions.
- **Side effect**: a candidate-caused effect outside the declared task contract, defined by the evaluation profile before the run. Side effects are counted separately from task outcome.
- **Boundary margin**: for partial-credit cases, the distance between an arm's modal score and the pass threshold. When the gate sits on the arm's modal score, binary pass/fail flips on scoring noise without any capability change — the stable quantities are the score distribution and the per-criterion hit vector, and a binary flip on such a case must not be reported as instability. Binary verdicts are only meaningful stability evidence for arms whose modal score is far from the gate. (First measured instance: `A-ea80d793` × `glm-5.3-flash@ollama`, `docs/stage1-v001-screen-20260915.md` — 20/20 stable verdict discipline, hit count 1–3/5 against a hits≥3 gate → binary flipped 8/20.)

## 3. Arm identity and comparability

A repeat is valid only under the same arm. Before calling a run a repeat, record and compare:

- provider endpoint and lane identifier;
- served model identifier and any provider-declared version/snapshot;
- effort/band and the actual wire-level reasoning semantics;
- harness name, version, and relevant runner configuration;
- clean-room/profile identifier and fallback policy;
- `spec_sha256`, `base.bundle` sha256, `oracle.pack` sha256, and `index_version`;
- run window, concurrency, and timeout policy;
- wire-audit result showing no substitute-model calls.

If any of these change, report the run as cross-arm or cross-time evidence, not as a same-arm repeat. Same-day replication and cross-day replication are different evidence classes and must be labeled separately.

## 4. Repeat-run design

### 4.1 Stage 0 — historical audit ($0)

Before buying new runs, extract existing published results into a `case × arm` matrix. Report:

- repeated primary runs and their fail-set deltas;
- case-level flips in both directions;
- infrastructure invalids and makeups separately;
- cross-arm differences separately from same-arm repeats.

A historical memo can justify a stability protocol; it cannot fill a precise recovery-rate column unless the repeats were already same-arm and terminal-valid.

Cells reprinted across reports (cross-vendor comparison columns, digest tables, signature reprints) are the **same observation**. Dedupe by `(case, arm, run identity)` before counting repeats; never let a republished cell inflate a sample.

### 4.2 Stage 1 — fail-set screen

For each case whose primary valid outcome is a failure, run `n = 5` same-arm repeat trials. `n` counts **valid** trials: `invalid_infrastructure` attempts are reported separately and do not consume the budget. Multi-variant cases repeat all scored variants for a case-level trial; paper-level repeats may be reported separately but must not be called case-level.

Interpretation:

- `0/5` recoveries: report `no_recovery_observed(n=5)`. This is a screen, not proof of a stable failure.
- `≥1/5`: the case is recovery-capable under this arm. Escalate if the case affects a decision.

Do not run the full library by default. Passing cases may be spot-checked for `pass^k` when a pass is load-bearing, but the default stability spend goes to the fail set.

### 4.3 Stage 2 — confirmation

Escalate a screened case to `n = 20` total valid trials (the stage-1 trials count toward `n`) when either:

- stage 1 observed at least one recovery; or
- the case is decision-critical enough that a bounded statement is worth the spend.

Interpretation:

- `0/20` supports "recovery rare or unobserved": a one-sided ~95% upper bound around 14% by the zero-success binomial bound.
- `r/20` recoveries is reported with a confidence interval, not as a bare percentage.
- No fixed `n` is universal. Choose `n` from the estimand and required bound before running.

## 5. Sample-size rules

Select `n` from the decision, not from a ritual number.

| Goal | Rule of thumb | Reading |
|---|---:|---|
| Screen for any recovery | `n=5` | `0/5` is weak evidence only: no recovery observed, upper bound still wide. |
| Bound an unobserved recovery rate | `n=20` | `0/20` gives one-sided ~95% upper bound ≈14%. |
| Certify high repeatability with zero failures | `n ≥ ln(α)/ln(p0)` | `n=29` for `p0=90%` at one-sided 95%; `n=33` corresponds to about 91%, not a universal threshold. |
| Estimate a rate within ±10 percentage points | binomial sizing | Worst case near `p=0.5` needs about `n=96`; at `p=0.8`, about `n=61`. |
| Compare two arms' stability | paired case-level design | Size from expected discordance and desired power; as a rough unpaired planning check, detecting 50% vs 70% at 80% power needs about `n=82` per arm. |

When a result will be used to rank arms, publish the uncertainty interval or the decision rule that tolerates it. Do not rank stability from a small screen alone.

## 6. State accounting

Use Core terminal states exactly.

- `valid_task_success` and `valid_task_failure` count in task-outcome denominators.
- `invalid_infrastructure` is excluded from task-outcome denominators and reported in its own column. A later makeup run may replace the infrastructure attempt operationally, but the invalid count remains visible.
- `protocol_violation` is reported separately; it is not a flaky failure mode.
- `pending_adjudication` is non-terminal and excluded until adjudicated.
- Missing or owed trials are reported as missing/owed, never silently treated as failures or passes.

A run contaminated by substitute-model calls is not evidence for the declared arm; classify it under the profile's wire-audit rule and disclose it.

## 7. Required reporting fields

Per repeated case, record at least:

- `case_id` public alias;
- `arm_id` and the arm-identity fields from §3;
- primary outcome and terminal state;
- repeat index and UTC start time;
- repeat terminal state and case outcome;
- invalid/owed reason where applicable;
- side-effect count and side-effect class;
- workspace/environment reset identifier;
- token/cost fields when available, otherwise wall clock.

Per arm, publish aggregates:

- primary score and primary fail set;
- valid repeat trials per failed case;
- recovery count and recovery-after-fail interval;
- `pass@k` and `pass^k` where applicable;
- `invalid_infrastructure`, `protocol_violation`, pending, missing/owed;
- side effects per case and per run;
- fail-set delta for any full-library repeat;
- for multi-variant cases, the **per-variant outcome vector** — a case-level flip must be decomposable into which variants moved (`A-0676097b` screen: the case flip was entirely in two of the four variants; the other two never moved — variant names stay private);
- failure-mode split: `no deliverable` (delivery-contract failure) reported separately from oracle-judged failures — different causes, different fixes; a transcript claim of delivery with no artifact on disk is still `no deliverable`.

Public reports use public case aliases and aggregates only. They carry no rubric content, transcripts, patches, or source-event identifiers.

## 8. Paired comparison

For stability comparisons between arms, prefer paired case-level outcomes on the same case hashes and index version. Report:

- per-case concordance and discordance;
- recovery-after-fail by arm;
- regression-after-pass by arm;
- invalid-infrastructure burden by arm;
- confidence intervals or exact counts when the sample is small.

A model-name match across endpoints is not pairing. Endpoint differences are part of the arm and must be reported as such.

## 9. Honest limits

- Recovery-after-fail is conditional on the primary fail set and has selection bias by construction.
- Repeats are not perfectly iid: provider behavior, model snapshots, harness versions, and date/time can drift. Sequential repeats on one endpoint can also be time-correlated — check whether failures cluster in the run order before reading them as independent draws (observed: `A-0676097b` screen failed only in rounds 4–5 of 5).
- A bounded `n` can bound an unobserved rate; it cannot prove impossibility.
- Same-day replication does not establish cross-day stability.
- A stable score can hide a drifting fail set; report both.
- Stability under one isolation/egress or tool surface does not transfer to another without evidence.
