# Documentation index

> Moved from the "Contents" section of the front-page [README](../README.en.md); text unchanged. 中文: [README.md](README.md)

- [Leaderboard in full](leaderboard-notes.en.md) — complete top-five lists, footnotes, original correction banners
- [The ten axes and the completion matrix](axes.en.md)
- [Three findings: effort, tokens, wall time](findings-effort-and-speed.en.md)
- [Manifest schema and validator](manifest-schema.en.md)

- [AMBER-Core-Specification.md](../AMBER-Core-Specification.md) — the normative spec: purpose, definitions, mechanisms, 8 invariants, 8 boundaries, epistemic limits, naming review, adoption rules
- [protocols/distribution.md](../protocols/distribution.md) — cross-host case distribution protocol (v0.3): public/private channel split, fixed-form git bundles, detached signature manifests, public index, sealing probes, leak-window adjudication, run records, comparability and verification matrices
- [protocols/stability.md](../protocols/stability.md) — stability protocol draft (v0.1): same-arm repeats, recovery-after-fail, side-effect counts, separate infrastructure accounting, decision-driven sample sizes
- [docs/instability-memo-2026-09-14.md](instability-memo-2026-09-14.md) — $0 historical-drift memo: 900 published matrix cells across 31 canonical arms (republished columns flagged), showing why a score snapshot is not a stability certificate
- [docs/stage0-flip-analysis-2026-09-14.md](stage0-flip-analysis-2026-09-14.md) — stage-0 flip inventory: 17 drift/recovery events (matrix-derived + prose-flagged) with the stage-1 screening candidate list
- [docs/stage1-v001-screen-20260915.md](stage1-v001-screen-20260915.md) — first designed-stability dataset: `A-ea80d793` × `glm-5.3-flash@ollama` n=20 same-arm repeats, 8/20 pass (~40%, verdict discipline stable 20/20) — boundary-margin cases must report score distributions, not binary flips
- [docs/stage1-reqdrift-screen-20260915.md](stage1-reqdrift-screen-20260915.md) — `A-0676097b` × `luna-high` n=5 case attempts: 3/5 pass; the r3 regression reproduces twice in one sitting on the same two variants (names private) — an escalation-classification boundary case, incl. one hallucinated-delivery `no deliverable`
- [docs/stage1-sfail-screen-20260915.md](stage1-sfail-screen-20260915.md) — six-case stable-fail set × `glm-5.3-flash@ollama` n=5 screen: five cases keep the label with zero recoveries (A-87c472cb/A-d511f9e8 partials glued), **A-d9b79b46 goes 3/4 pass — label torn** (stage-2 n=20 complete: 6/20 ≈30% combined, Wilson [14.5%, 51.9%] — the n=5 screen's 75% over-read; only the binary verdict is trustworthy at n=5); A-a317e74b needs a 3600 s cap to finish — protocol gains per-case timeout table and abort-on-billing
- [docs/nine-axis-top3-2026-09-18.en.md](nine-axis-top3-2026-09-18.en.md) — nine-axis podium (40 lanes recomputed, written before the Convergence axis joined): only defense/attribution/review/vision discriminate, and the four champions belong to four different vendors; the other five axes are saturated at the top
- [hash-index/v2026-09.md](../hash-index/v2026-09.md) — the public hash index: alias + bundle/oracle dual hashes for every case in the current library (24 cases); every results-repo matrix is checked against it
- [schemas/manifest.schema.json](../schemas/manifest.schema.json) · [tools/validate_manifest.py](../tools/validate_manifest.py) · [schemas/shre-amber-mapping.md](../schemas/shre-amber-mapping.md) — the Case Manifest JSON Schema, its validator (including the closed-set Distribution §5.1 redacted-summary check), and the SHRE→AMBER identifier mapping
- [PLAN.md](../PLAN.md) — status, milestones (case tooling → reference runner → scoring/adjudication → statistics → public index), open design questions
- [CONTRIBUTING.md](../CONTRIBUTING.md) — contribution rules: **this repo never accepts case content**, document versioning and revision policy, what byte-hash-locking the Core spec means

Chart sources (`.puml` for PlantUML, `.vega-lite.json` / `.vg.json` for Vega) sit next to the PNGs in `docs/images/` — edit a source, re-render, done.
