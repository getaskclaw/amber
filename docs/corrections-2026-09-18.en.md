# Correction 2026-09-18: results labeled "swe-2-low" were actually swe-2-high

> 中文版本：[corrections-2026-09-18.md](corrections-2026-09-18.md)

## What is being corrected

Every published AMBER result labeled **swe-2-low @ Devin** (the amber-devin 2026-W37 issue
Addendum, this repo's README leaderboard and footnotes, the nine-axis 2026-09-18 issue, and the
case-run-matrix / flip-list data tables) was in fact produced by **swe-2-high**.

**swe-2-low does not exist.** Devin's official catalog (`devin models list`, live) and
Cognition's SWE-2 announcement list exactly three effort levels: medium / high / max.

## How it was found and verified

1. After a reader reported "Devin has no swe-2-low; requests get rerouted", we ran live probes
   and reconciled them against the server-side session ledger.
2. Devin's own session ledger (the CLI's sessions.db, which records the **resolved** model)
   shows **zero** swe-2-low sessions ever; all 82 exam sessions on 2026-09-12 — the day of the
   alleged "swe-2-low full-library debut" — are recorded as **swe-2-high**.
3. Mechanism: the harness asks the ACP channel for a model via `session/set_config_option`.
   When the requested id is not in the server's advertised option list, the selection request is
   **silently skipped** and the session stays on the server default (currently swe-2-high) —
   no error, no refusal.
4. Contemporary control: the 2026-09-10/11 swe-2-medium (62 sessions) and swe-2-max (22+36)
   runs are recorded faithfully in the same ledger, proving the column reflects the resolved
   model, not an echo of the request — and proving the medium/max results are genuine and
   **unaffected by this correction**.
5. Independent re-test (on the day of this notice): valid ids route correctly through the same
   channel (medium→medium, max→max); the channel does resolve legitimate ids. The failure is
   specific to requesting a nonexistent id.

## How the scores change

- "swe-2-low 15/23" becomes a **second full-library run of swe-2-high**. Against the first
  swe-2-high run (16/23 on 2026-09-10), this is same-model run-to-run variance (16 vs 15,
  inside the known ±2 drift band), not a band difference.
- The band ladder "low 15 = medium 15 < high 16 < max 18" is corrected to
  **medium 15 < high 16 ≈ high re-run 15 < max 18**; the monotone medium < high < max
  conclusion is unaffected.
- The "swe-2-low ties medium with the opposite signature" narrative was really
  "swe-2-high's second run vs medium"; the signature difference is real but belongs to
  high's re-run.
- The nine-axis issue's review-axis leader "swe-2-low @ Devin 0.722" is corrected to
  swe-2-high. The score was already flagged "single run, not re-measured — excluded from
  routing conclusions"; that handling stands.
- In the orchestration single-case results, "swe-2 low 29/32 champion" is corrected to
  swe-2-high; "low 29 vs high 24" was same-model variance.

## Audit-discipline lesson (process fix)

Our wire verification audited the **request side** (the model id the harness sent) but not the
**server-resolved side**, so the silent substitution passed a "26/26 verified" audit. From this
correction onward, the Devin lane's verification standard adds: **the server-side ledger's
resolved model must match the requested model row by row**, and model ids are validated against
the live official catalog before a run.

## Affected files

- `README.md` / `README.en.md`: leaderboard tie row and footnote (fixed in this commit, linking here)
- `docs/nine-axis-top3-2026-09-18.md` / `.en.md`: review-axis attribution (fixed in this commit)
- `docs/data/case-run-matrix-2026-09-14.csv`, `docs/data/flip-list-2026-09-14.csv`,
  `docs/data/build-case-run-matrix.py`, `docs/data/build-flip-list.py`: model labels fixed
- `docs/stage0-flip-analysis-2026-09-14.md`, `docs/instability-memo-2026-09-14.md`:
  historical narrative kept as-is, registered here
- amber-devin repo `results/2026-W37.md`: top banner + Addendum 2026-09-18 (body preserved
  as the historical record)
