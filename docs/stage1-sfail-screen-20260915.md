# Stage-1 Stable-Fail Screen — glm-5.3-flash @ Ollama Cloud (2026-09-15)

Stage-1 n=5 screen of the six-case stable-fail set (from the W36→W37 drift analysis),
same arm: `glm-5.3-flash @ ollama-cloud`, high band. Raw manifests live in the
private run ledger (paths stay private).

## Verdicts

| case | valid trials | sequence (oldest→newest) | verdict |
|---|---|---|---|
| A-87c472cb | 0/6 | F6/8 ×6 (r1, r1b, r2q–r5q) | **STABLE FAIL** — partial glued at 6/8, zero variance |
| A-d511f9e8 | 0/4 | F4/12 ×4 (+1 timeout invalid, +1 billing invalid) | **STABLE FAIL** — partial glued at 4/12 |
| A-a317e74b | 0/3 | F0/15 (3600 s cap, 1845 s), F8/15, F9/15; 3× 1800 s timeouts | **STABLE FAIL** at case level; partial wobbles 0→8→9 |
| A-be92627f | 0/5 | F5/9, F6/9, F4/9, F3/9, F1/9 | **STABLE FAIL** — partial declining across the day |
| A-cdc3d11a | 0/5 | F-2, F0, F-1, F-2, F-13 | **STABLE FAIL** — partial wildly unstable (incl. a -13 false-positive burst) |
| A-d9b79b46 | **3/4 pass** | P, P, F, P (+ r1 candidate 11/12 FAIL via manual oracle rerun) | **NOT STABLE FAIL — bimodal ≈60% pass; escalated to stage-2 n=20** |

One recovery in five falsifies "stable fail": A-d9b79b46's label is torn. The other
five cases keep theirs — four of them with zero recoveries in 3–6 valid trials.

## Provenance and discipline

- Arm: `glm-5.3-flash @ ollama-cloud`, high band, `amber-lib-*` bundles, oracle-judged.
- Billing: r1 (+ A-87c472cb second run) on a Pro-tier Ollama account (hit its
  **5-hour session window** mid-round-2 — Ollama session limits reset every 5 h,
  weekly every 7 d; there is no daily tier). 3600 s makeup + rounds r2q–r5q on a
  Max-tier account. Account is the billing pipe, not arm identity: same endpoint,
  model, and band throughout.
- Wire audit: 10/10 sampled sessions (of 28 recorded) pinned `glm-5.3-flash`, zero
  substitution, across both billing accounts.
- `invalid_infrastructure` ledger: 4× 1800 s-cap timeouts (A-a317e74b ×3, A-d511f9e8 ×1) and
  5× billing-exhausted (original screen r2–r5 after quota death). Timeouts at 1800 s
  owe doubled-cap makeups per the infra-rerun discipline.
- JJA r1: candidate completed; oracle could not run (Playwright browser missing in the
  sandbox). Browser installed (`chromium_headless_shell-1234`); manual oracle rerun of
  that exact candidate scored **11/12 FAIL** (missed `no_overlap_1280`) — counted as one
  valid fail observation.
- Data hygiene: 24 `driver_exception` records (PATH accident under systemd, `hermes`
  not on default PATH) removed from r2q–r5q manifests; originals kept as
  `manifest.jsonl.bak-driverexc`. A 05:38 billing-flicker invalid in the A-a317e74b makeup
  manifest is retained.

## Protocol lessons (fed back into protocols/stability.md candidates)

1. **Per-case cap overrides**: A-a317e74b cannot reliably finish in 1800 s on this arm
   (3 of 6 attempts capped); at 3600 s it completed in 1845 s. Recommend
   case-level timeout table instead of one global cap.
2. **Kill-on-billing**: the driver currently converts billing death into instant
   `invalid_infrastructure` retries, letting a dead account burn four more rounds of
   5-second "runs". Screens must abort on first billing signal (now implemented at
   script level; driver-level fix still owed).
3. **Partial-score reporting matters**: all five stable fails keep their label, but
   only A-87c472cb/A-d511f9e8 are glued; A-be92627f drifts down, A-cdc3d11a swings to -13. Stability
   columns should carry the partial distribution, not just the binary.
4. **Timeout ≠ model failure** and **driver exception ≠ trial**: both now separated in
   this screen's accounting; the taxonomy belongs in the protocol's terminal-state list.

Stage-2 follow-up: A-d9b79b46 n=20 **complete 2026-09-15 22:45 UTC** (15 further
trials on the Max-tier account, private run tag on file): stage-2 went 3/15; combined with the
stage-1 observations (3/5) the full sample is **6/20 pass (30%), Wilson 95%
[14.5%, 51.9%]** — passes scattered across the window (t5, t11, t15), no clustering.
Lesson: the n=5 screen's 3/4 (75%) shrank to 30% at n=20 — stage-1 recovery rates
over-read; only the binary "recovery exists / does not exist" is trustworthy at n=5.
