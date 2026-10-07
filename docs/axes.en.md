# The ten axes: how to read the completion matrix

> Moved from the front-page [README](../README.en.md); text unchanged. 中文: [axes.md](axes.md)

**Completion profile: same score, different shape** — lanes with the same total can have very different strengths and weak spots. The chart below shows the 8 lanes with 18 or more on the board across the ten axes: a bigger, darker dot = higher completion, and NA = no scorable case on that axis (voided or on hold), not a zero. The data comes from the score database (the same source as the askclaw.dev board), on the full 24-case library as of 2026-10-07, with A-d511f9e8 and A-cdc3d11a excluded as NA.

![Completion matrix: the 8 lanes with 18+ on the board, ten axes, 24 cases, 2026-10-07](images/completion-matrix-top8-2026-w41b.en.png?v=20261007b)

How to read it:

- **The building side is almost full**: coding is 0.96–1.00, and delivery, ops, requirements and convergence are 1.00 for all eight. On the hands-on axes these eight cannot be told apart.
- **The differences are all on the judging side**: five lanes have 1.00 on UI, while glm-5.3-flash (Ollama Cloud) and k3 have 0.00 (the score database holds no check-by-check detail for that case, so the rule records 0.00), and deepseek-v4.1-flash (WorkBuddy direct) is NA (the one UI case, A-d9b79b46, is on hold); vision runs from 0.22 (step-5-preview) and 0.33 (hy4-preview-f, ACP) to 0.89 (claude-opus-5-5 and deepseek-v4.1-flash on WorkBuddy direct, whose vision cell is taken from the re-sit paper after the exam-room fix); review sits at 0.44–0.89 (the review axis excludes A-cdc3d11a, so each cell reflects only the other case).
- **Defense and attribution spread the most**: claude-opus-5-5 and step-5-preview are NA on both (on each of those axes step-5-preview has one case that hit the exam-room time cap), and swe-2-max is NA on attribution; claude-sonnet-5-5 has the best defense (0.89) but only 0.47 on attribution; glm-5.3-flash (Ollama Cloud), hy4-preview-f (ACP) and deepseek-v4.1-flash (WorkBuddy direct) have the best attribution (0.93).
- Earlier versions: the eight-lane one (2026-10-07, review axis includes A-cdc3d11a, old rule) [completion-matrix-top8-2026-w41.en.png](images/completion-matrix-top8-2026-w41.en.png); the seven-lane one (2026-10-04, without step-5-preview) [completion-matrix-top7-2026-w40.en.png](images/completion-matrix-top7-2026-w40.en.png); the six-lane one (2026-10-02, without deepseek-v4.1-flash @ WorkBuddy direct) [completion-matrix-top6-2026-w40.en.png](images/completion-matrix-top6-2026-w40.en.png); and the earlier seven-lane one (old rule; it includes the lopsided doubao and Qwen3.8-27B lanes, kept as history only) [completion-matrix-7way.en.png](images/completion-matrix-7way.en.png). Each lane's completion is also in its result repo's issue page.

**The ten axes, in plain language** — each cell is the lane's completion (0–1) across that axis's cases; pin-scored cases fold in by pins:

- **Coding** · cook from the recipe: implement the spec correctly (mean of 6 cases)
- **Delivery** · done ≠ handed in: no artifact means 0, however good the plan (mean of 3 cases)
- **Ops** · follow the runbook: backups, cutovers, reconciliation — no skipped steps (mean of 6 cases)
- **Requirements** · the client asked for A, not B — ship A (1 case)
- **Convergence** · real finish or busywork loops: did the work land, how fast, and did it spin in place farming temp files (1 case; joined 2026-09-21; as of 2026-10-02, 18 of the 19 examined lanes on the askclaw.dev board passed and one (space-bunny-alpha) did not; in the older matrix figure a blank cell = not yet examined, not a zero)
- **UI** · build the page to the mock, pin-level acceptance (1 case, 12 pins)
- **Vision** · spot defects in real screenshots: overlaps, cropping, missing legends — did it actually see them (1 case, defect-hunt score)
- **Defense** · night-shift guard: plug every hole in the validator without turning away legit input (mean of 2 cases; A-d511f9e8 has been on hold on every lane since 2026-10-02, see the [correction](corrections-2026-10-02-a-d511f9e8.en.md))
- **Attribution** · a doctor matching symptoms to causes: pin each defect to the right root cause (1 case, 15 pins)
- **Review** · be the inspector: find real defects in someone's deliverable — misses and false alarms both cost, and the score can go negative (2 cases, defect-hunt score)

**From 2026-10-01 the official board on [askclaw.dev](https://askclaw.dev/en/) uses these same ten axes** (the official board counts passes, the matrix above measures completion — two scores on the same axes): the board's former verify axis is split into **Defense** and **Attribution**; every model's total is unchanged. Two groups — **Building**: Coding, Delivery, Ops, Requirements, Convergence; **Judging**: UI, Vision, Defense, Attribution, Review. Axis names, hints and groups are published with the results database, and the site and this page use the same definition.

Axes grow with the library: each new case family can add a column — extend this list the same way.

Who tops each axis? Recomputed across 40 published lanes: [Nine-axis podium 2026-09-18](nine-axis-top3-2026-09-18.en.md) (written before the Convergence axis joined — covers the first nine) — only defense/attribution/review/vision actually rank the field, the four champions belong to four different vendors, and the overall board leader wins none of them; on Convergence every examined lane is tied at full marks, pending more cases.
