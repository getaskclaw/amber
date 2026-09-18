# AMBER — Sealed-in-Amber Historical Replay Evaluation

`Seal the scene in amber. Retake the exam of that moment.`

**Library** 23 cases / 26 papers · **Spec** v0.2.2 (draft) · **Hash index** [v2026-09](hash-index/v2026-09.md) · **Result repos** × 11 · **Rule** scores always public, cases never

中文说明：[README.md](README.md). The normative document is [AMBER-Core-Specification.md](AMBER-Core-Specification.md).

## What this is

A formal evaluation method. Take a **real, auditable** historical incident and rebuild the scene exactly as it stood before the answer was known. The candidate gets only the information available at that moment; all later evidence and scoring material is **physically sealed**. It diagnoses, decides, acts, abstains, refuses, or escalates. The rubric is frozen before anyone sees the output. Everything is archived, and everything can be audited.

## AMBER in three minutes (for first-time visitors)

**① Current leader** — **swe-2-max @ Devin, 18/23** (2026-W37, full 23-case library; band curve medium 15 < high 16 < max 18). The same model name on a different endpoint can be a different brain, so we record scores per endpoint × name:

![Current top five 2026-W38](docs/images/top5-2026-w38.en.png?v=20260917b)

**② Completion profile: same score, different shape** — five lanes now tied at 17/23; nine-axis completion matrix, all five side by side — same score, five different shapes (pin-level completion; negative d2 scores still count). The new k3 row at a glance: an empty dot on UI (the incomplete-deliverable case), attribution below the top pair, vision tied for best with glm-5.3-flash. Added 09-16, the doubao 16/23 row: full marks on all four construction axes (coding/delivery/ops/requirements), level with the leaders — but empty dots on UI and vision, review at a third — the most lopsided shape on the field. Its two verification axes (attribution/defense) were harness-walled in the main sweep and landed real scores in a 3600s makeup (0.47 / 0.50 — low but real; [amber-doubao W38 addendum](https://github.com/getaskclaw/amber-doubao/blob/main/results/2026-W38.md)). Negative d2 is floored at 0. Added 09-17, the gp27b 14/23 row (Qwen3.8-27B @ goldenpotato community self-hosted): an even more lopsided shape than doubao — construction group at the leaders' level (coding 0.83 / delivery full / ops 0.97 / requirements full) while review/vision/UI sit at absolute zero and attribution/defense at the field's bottom band; aggressive NVFP4 quantization cost nothing on the hands-on faces and everything on the judgment faces ([amber-goldenpotato W38](https://github.com/getaskclaw/amber-goldenpotato/blob/main/results/2026-W38.md)):

![Completion matrix, five-way 17/23 tie + doubao 16/23 + gp27b 14/23](docs/images/completion-matrix-7way.en.png?v=20260917)

> **The nine axes, in plain language** — each cell is the lane's completion (0–1) across that facet's cases; pin-scored cases fold in by pins:
>
> - **Coding** · cook from the recipe: implement the spec correctly (mean of 6 cases)
> - **Delivery** · done ≠ handed in: no artifact means 0, however good the plan (1 case)
> - **Defense** · night-shift guard: plug every hole in the validator without turning away legit input (mean of 2 cases)
> - **Attribution** · a doctor matching symptoms to causes: pin each defect to the right root cause (1 case, 15 pins)
> - **Review** · be the inspector: find real defects in someone's deliverable — misses and false alarms both cost, and the score can go negative (2 cases, d2)
> - **Ops** · follow the runbook: backups, cutovers, reconciliation — no skipped steps (mean of 6 cases)
> - **Requirements** · the client asked for A, not B — ship A (1 case)
> - **UI** · build the page to the mock, pin-level acceptance (1 case, 12 pins)
> - **Vision** · spot defects in real screenshots: overlaps, cropping, missing legends — did it actually see them (1 case, d2)
>
> Facets grow with the library: each new case family can add a column — extend this list the same way.

**③ What it is** — a private case library plus public scores: the cases never go public, the scores and hashes always do.

![What is AMBER](docs/images/what-is-amber.en.png?v=20260917)

**④ How a result is produced** — it works like an exam: papers sealed at authoring, sat in a clean room, audited paper by paper, published redacted, checkable by anyone.

![How a result is produced](docs/images/trust-chain.en.png?v=20260915b)

**⑤ A counterintuitive finding, with limits** — on the families measured so far, high is the sweet spot and top bands backfire (three of the four families plotted). A pattern, not a law: swe-2's band curve is monotone to the top (medium 15 < high 16 < max 18, [amber-devin W37](https://github.com/getaskclaw/amber-devin/blob/main/results/2026-W37.md)), and on some models the band barely moves the score — pick your band by cost and speed, not score; the WorkBuddy and Kimi lanes only have high-band scores so far, no curve to plot.

![effort curves](docs/images/effort-curves-20260911.en.png)

**⑥ Score vs thinking budget** — same band (high), same library, and the output-token bill spans 17× (147K vs 2.5M) for scores within a case of each other (token totals from each lane's published issue). The axis is tokens, not dollars: billing is mixed (subscription lanes have no marginal price; the devin and workbuddy lanes report no usage at all, so swe-2 and the wb pair sit this one out). Within a family, more tokens bought no score (luna flat; astra's top bands lose four cases); across families the shape varies — which is why ⑤ is a pattern, not a law.

![score vs thinking budget W37](docs/images/score-vs-tokens-2026-w37.en.png)

**⑦ High TPS only holds on easy problems** — same library, per-problem wall time (log axis): a vendor's high TPS is decode speed measured on easy problems, and hard problems mean more thinking, slower effective decoding, and ballooning wall time. Dot = one problem, bar = median; problem IDs are anonymized (the mapping stays private; per-point data in [wallclock-2026-w37.csv](docs/data/wallclock-2026-w37.csv)). On the families measured so far, swe-2 gets slower with each higher band yet solves more (median 82 s → 280 s), while v4.1-flash backfires at the top band (68 s median, two fewer solves). Shapes vary by family — a pattern on these families, not a law.

![High TPS only holds on easy problems](docs/images/wallclock-strip-2026-w37.en.png?v=20260911)

Chart sources (`.puml` for PlantUML, `.vega-lite.json` / `.vg.json` for Vega) sit next to the PNGs in `docs/images/` — edit a source, re-render, done.

## Why

Public benchmarks are frozen, public corpora: training contamination is rampant and unauditable, scores keep inflating, and static Q&A can't measure what real work demands — multi-step diagnosis, abstention, refusal, escalation under uncertainty. AMBER replays **provenance-controlled** real events whose leak status can be checked. It runs alongside public benchmarks; it doesn't replace them.

## Two caveats that won't go away

- **Runtime sealing ≠ training-data purity**: we seal runtime evidence; we can't prove the model never saw the future in training.
- **A historical outcome is evidence, not the one correct answer.**

## Status

Draft v0.2.2. The Core spec is stable; `schemas/`, `profiles/`, and the case-building/runner tooling are **not yet published**, so you can't execute a compliant run from this repo alone yet. Roadmap and milestones: [PLAN.md](PLAN.md).

## Contents

- [AMBER-Core-Specification.md](AMBER-Core-Specification.md) — the normative spec: purpose, definitions, mechanisms, 8 invariants, 8 boundaries, epistemic limits, naming review, adoption rules
- [protocols/distribution.md](protocols/distribution.md) — cross-host case distribution protocol (v0.3): public/private channel split, fixed-form git bundles, detached signature manifests, public index, sealing probes, leak-window adjudication, run records, comparability and verification matrices
- [protocols/stability.md](protocols/stability.md) — stability protocol draft (v0.1): same-arm repeats, recovery-after-fail, side-effect counts, separate infrastructure accounting, decision-driven sample sizes
- [docs/instability-memo-2026-09-14.md](docs/instability-memo-2026-09-14.md) — $0 historical-drift memo: 900 published matrix cells across 31 canonical arms (republished columns flagged), showing why a score snapshot is not a stability certificate
- [docs/stage0-flip-analysis-2026-09-14.md](docs/stage0-flip-analysis-2026-09-14.md) — stage-0 flip inventory: 17 drift/recovery events (matrix-derived + prose-flagged) with the stage-1 screening candidate list
- [docs/stage1-v001-screen-20260915.md](docs/stage1-v001-screen-20260915.md) — first designed-stability dataset: `A-ea80d793` × `glm-5.3-flash@ollama` n=20 same-arm repeats, 8/20 pass (~40%, verdict discipline stable 20/20) — boundary-margin cases must report score distributions, not binary flips
- [docs/stage1-reqdrift-screen-20260915.md](docs/stage1-reqdrift-screen-20260915.md) — `A-0676097b` × `luna-high` n=5 case attempts: 3/5 pass; the r3 regression reproduces twice in one sitting on the same two variants (names private) — an escalation-classification boundary case, incl. one hallucinated-delivery `no deliverable`
- [docs/stage1-sfail-screen-20260915.md](docs/stage1-sfail-screen-20260915.md) — six-case stable-fail set × `glm-5.3-flash@ollama` n=5 screen: five cases keep the label with zero recoveries (A-87c472cb/A-d511f9e8 partials glued), **A-d9b79b46 goes 3/4 pass — label torn** (stage-2 n=20 complete: 6/20 ≈30% combined, Wilson [14.5%, 51.9%] — the n=5 screen's 75% over-read; only the binary verdict is trustworthy at n=5); A-a317e74b needs a 3600 s cap to finish — protocol gains per-case timeout table and abort-on-billing
- [hash-index/v2026-09.md](hash-index/v2026-09.md) — the public hash index: alias + bundle/oracle dual hashes for every case in the current library (23 cases); every results-repo matrix is checked against it
- [PLAN.md](PLAN.md) — status, milestones (case tooling → reference runner → scoring/adjudication → statistics → public index), open design questions
- [CONTRIBUTING.md](CONTRIBUTING.md) — contribution rules: **this repo never accepts case content**, document versioning and revision policy, what byte-hash-locking the Core spec means

## Weekly results (sister repos)

Scores and cases are published separately: results are public, cases never are. These repos run the full library weekly (aliases + bundle hashes verifiable against the [public hash index](hash-index/v2026-09.md)):

- [amber-crof](https://github.com/getaskclaw/amber-crof) — CrofAI models
- [amber-commandcode](https://github.com/getaskclaw/amber-commandcode) — CommandCode models
- [amber-deepseek](https://github.com/getaskclaw/amber-deepseek) — official DeepSeek API models
- [amber-devin](https://github.com/getaskclaw/amber-devin) — Devin models
- [amber-doubao](https://github.com/getaskclaw/amber-doubao) — Doubao models on Volcengine Ark Agent Plan
- [amber-kimi](https://github.com/getaskclaw/amber-kimi) — Kimi official coding-endpoint models
- [amber-ollama](https://github.com/getaskclaw/amber-ollama) — Ollama Cloud models
- [amber-opencode](https://github.com/getaskclaw/amber-opencode) — OpenCode Go models
- [amber-gpt](https://github.com/getaskclaw/amber-gpt) — GPT-family models × reasoning-effort bands
- [amber-workbuddy](https://github.com/getaskclaw/amber-workbuddy) — WorkBuddy (CodeBuddy) ACP-channel models

**Current top five** (as of 2026-W38, full 23-case library¹):

| # | model @ endpoint | pass | source |
|---|---|---|---|
| 1 | swe-2-max @ Devin | 18/23 | [amber-devin W37](https://github.com/getaskclaw/amber-devin/blob/main/results/2026-W37.md) |
| 2 | glm-5.3-flash @ Ollama Cloud | 17/23 | [amber-ollama W37](https://github.com/getaskclaw/amber-ollama/blob/main/results/2026-W37.md) (tied: deepseek-v4.1-flash @ CommandCode, [amber-commandcode W37](https://github.com/getaskclaw/amber-commandcode/blob/main/results/2026-W37.md); deepseek-v4.1-flash @ Ollama Cloud, [amber-ollama W37 Addendum 09-11](https://github.com/getaskclaw/amber-ollama/blob/main/results/2026-W37.md); hy4-preview-f @ WorkBuddy, [amber-workbuddy W37](https://github.com/getaskclaw/amber-workbuddy/blob/main/results/2026-W37.md); k3 @ Kimi official coding endpoint, [amber-kimi W38](https://github.com/getaskclaw/amber-kimi/blob/main/results/2026-W38.md)) |
| 3 | gpt-6-astra-900k @ OpenAI Codex | 16/23 | [amber-gpt W37](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W37.md) (tied: qwen3.8-27b @ CrofAI, [amber-crof W37](https://github.com/getaskclaw/amber-crof/blob/main/results/2026-W37.md); deepseek-flash @ OpenCode Go, [amber-opencode W37](https://github.com/getaskclaw/amber-opencode/blob/main/results/2026-W37.md); deepseek-flash @ DeepSeek official, [amber-deepseek W37](https://github.com/getaskclaw/amber-deepseek/blob/main/results/2026-W37.md); swe-2-high @ Devin, [amber-devin W37](https://github.com/getaskclaw/amber-devin/blob/main/results/2026-W37.md); doubao-seed-evolving @ Volcengine Ark Agent Plan, [amber-doubao W38](https://github.com/getaskclaw/amber-doubao/blob/main/results/2026-W38.md)) |
| 4 | gpt-5.6-sol-900k @ OpenAI Codex | 15/23 | [amber-gpt W38](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W38.md) (tied: gpt-5.6-luna-900k @ OpenAI Codex, [amber-gpt W38](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W38.md); deepseek-v4-flash-0731 @ CrofAI, [amber-crof W37](https://github.com/getaskclaw/amber-crof/blob/main/results/2026-W37.md); deepseek-v4-flash:0731 @ Ollama Cloud, [amber-ollama W37](https://github.com/getaskclaw/amber-ollama/blob/main/results/2026-W37.md); swe-2-medium and swe-2-low @ Devin, [amber-devin W37](https://github.com/getaskclaw/amber-devin/blob/main/results/2026-W37.md); deepseek-v4.1-flash @ WorkBuddy, [amber-workbuddy W37](https://github.com/getaskclaw/amber-workbuddy/blob/main/results/2026-W37.md)) |
| 5 | glm-5.3-flash @ CrofAI | 14/23 | [amber-crof W37](https://github.com/getaskclaw/amber-crof/blob/main/results/2026-W37.md) (tied: swe-1-7-medium @ Devin, [amber-devin W37](https://github.com/getaskclaw/amber-devin/blob/main/results/2026-W37.md); deepseek-v4.1-flash-exp (preview) @ DeepSeek official, [amber-deepseek W37](https://github.com/getaskclaw/amber-deepseek/blob/main/results/2026-W37.md); kimi-for-coding (K2.8 Preview) @ Kimi official coding endpoint, [amber-kimi W38](https://github.com/getaskclaw/amber-kimi/blob/main/results/2026-W38.md); Qwen3.8-27B @ goldenpotato community self-hosted endpoint, [amber-goldenpotato W38](https://github.com/getaskclaw/amber-goldenpotato/blob/main/results/2026-W38.md)) |

Not yet on the board: Fable and friends — this week's token budget didn't stretch to their exam fees; they sit the library as soon as the budget lands, and scores publish with the next issue. (kimi-k3 sat the library on 2026-09-15 and entered the board at the #2 tie — see the table above.)

¹ Since 2026-09-08 the board runs on the full 23-case library: CrofAI/Ollama/astra sat makeup runs of the 2 ops cases added 09-07 (12/12 papers wire- and hash-verified). astra's 16/23 = W36 -900k 14 cases + a W37 makeup on bare gpt-6-astra (the -900k variant was revoked server-side; the mixed lineage is noted in the issue). Added 2026-09-10: a three-lane duel on DeepSeek V4.1-Flash's GA day — the CommandCode and OpenCode Go relays plus the official DeepSeek API, same day, same band, full library (26/26 papers wire-verified each; CommandCode 17/23 joins the #2 tie, OpenCode Go and the official lane 16/23 join #3 — result repos in the table). Added 2026-09-11: deepseek-v4.1-flash @ Ollama Cloud debuts 17/23, joining the #2 tie (same-day glm-5.3-flash re-run 16/23, inside the known drift band; amber-ollama W37 Addendum); swe-2-max @ Devin takes the board at 18/23 (16/21 on the public 21-case subset) — band curve monotone to the top (medium 15 < high 16 < max 18), an OPS 6/6 sweep (lane-only — gpt's luna and ollama's g53f swept the ops face earlier), at ~5 h wall clock, roughly 4× the previous leader's (25/25 sessioned rows wire-verified, hashes 26/26 against the public index); swe-2-high 16/23 joins the #3 tie. The devin lane's harness does not forward effort — the true band is the UID suffix — and the lane reports no token usage. Out / not in: glm-5.3-flash @ CrofAI 14/23 (former #3 tie), devin swe-1-7-medium 14/23, deepseek-v4.1-flash-exp (preview, official lane) 14/23, gpt-5.6-sol-900k 15/23 (corrected on the 2026-09-16 re-test: the ui-build "zero delivery" was a client-side watchdog kill — small-prompt tiers vs 100–170s of silent high-effort reasoning — with a makeup 12/12 perfect; zero capability drift vs the prior run, see amber-gpt W38; upstream hermes-agent#112909), gpt-5.6-luna-900k 15/23, deepseek-v4-flash-0731 @ CrofAI 15/23, deepseek-v4-flash:0731 @ Ollama Cloud 15/23 (former #3 tie), swe-2-medium 15/23 (best-ever vision 4.0), swe-2-low 15/23 (same score as medium, opposite signature — keeps the two heavy-judgment cases A-442d4aab 7/7 and A-a317e74b 7/15 that medium drops, loses ops archaeology; 2026-09-12 Addendum, 26/26 wire-verified, 23/23 hashes against the public index), deepseek-v4.1-flash @ WorkBuddy 15/23 (see below). Added 2026-09-12: gpt-5.6-luna-900k's third high run lands 15/23 again (fail-set drifts ±2 across days; board composition unchanged; sol paused at the owner's call, 9/26 unscored — the lane was completed 09-16 as one fresh full-library sweep, 15/23, zero drift). Added 2026-09-13: first WorkBuddy ACP-channel entry, two models — hy4-preview-f 17/23 joins the #2 tie (OPS 6/6 sweep, A-d9b79b46 12/12 perfect; its A-a317e74b main run hit the 1800s cap and the 3600s-cap makeup scored 14/15, tying the case's second-best published score — the only pass remains crof q38's 15/15); deepseek-v4.1-flash 15/23 misses the board but lands A-be92627f 9/9 — the first-ever pass on that case across all published entries — second verify-face pass overall (previous best 8/9; the face's first break was crof q38's A-a317e74b 15/15). Audit: 82/82 usage rows on the pinned lane; both V001 papers via a direct-acp bypass (marked `runner` in the manifest); 23/23 hashes against the public index. Lane caveats: no token usage reported, effort pinned via the ACP set_config_option side channel, native tool surface is bypassPermissions. hy3 halted at the owner's call, unscored. Added 2026-09-15: k3 @ Kimi official coding endpoint debuts 17/23 (15/21 on the public 21-case subset), joining the #2 tie — coding face 5/6 with two perfect scores (hard discriminator A-442d4aab 7/7, A-569dbe0d 10/10), OPS 6/6 sweep, and the riding-line vision case A-ea80d793 passed at 3.0; verification face 0/3, A-d9b79b46 failed on an incomplete deliverable, A-cdc3d11a -2. 26/26 sessioned rows verified (k3, kimi-coding) with zero stand-ins, 23/23 hashes against the public index; 26 papers ~2.8 h wall-clock sum ([amber-kimi W38](https://github.com/getaskclaw/amber-kimi/blob/main/results/2026-W38.md)). Added 2026-09-16: doubao-seed-evolving @ Volcengine Ark Agent Plan debuts 16/23, joining the #3 tie — the channel is officially version-synced with Doubao-Seed-2.1-pro-0915 (the plan catalog carries no version-pinned ID; verified against official plan docs). A sharply split profile: build/text/ops/req-drift sub-scores 92/94 (97.9%) with a perfect 7/7 on the hard discriminator A-442d4aab, while review/vision/ui-build net −2 and all three verify cases hit the harness wall with zero deliveries (a 3600s-cap makeup lands in the result repo's addendum); reasoning tokens = 65% of output and mean wall 557s/paper, ~2× the GPT lane at the same band; 23/23 sessioned rows wire-verified on (doubao-seed-evolving, …/api/plan/v3) with zero stand-ins, 0/26 hash mismatches ([amber-doubao W38](https://github.com/getaskclaw/amber-doubao/blob/main/results/2026-W38.md)). Added 2026-09-17: kimi-for-coding (K2.8 Preview — the ID was silently re-brained on 09-11) @ Kimi official coding endpoint debuts 14/23 (12/21 on the public subset), off the then-top-three board — coding, text, and req-drift faces match k3 paper-for-paper at 27% faster wall clock, and the defense-verify case A-be92627f 7/9 beats k3's 4/9; but the adversarial-review case A-cdc3d11a scores -17 (k3: -2; hallucination-flood class, the worst published band on that case), and the review face is judged unusable. The 3-case gap to k3 sits entirely inside the known drift / riding-line band. 26/26 papers wire-verified (clean-room profile, zero fallback stand-ins), 26/26 hashes against the public index ([amber-kimi W38 Addendum 09-17](https://github.com/getaskclaw/amber-kimi/blob/main/results/2026-W38.md)). Added 2026-09-17: gpt-5.6-luna-900k's first max-band run lands 16/23 — the +1 case is ui-build A-d9b79b46's first-ever delivery at 12/12 (luna becomes the fifth published lane to max that case), but it is confounded with the same-day 09-16 harness watchdog fix (any band re-run would now deliver), so net of the confound it is 15/23, tied with high; the headline stays 15/23 (the cell-level correction is owed a same-band re-run). Vision case A-ea80d793 scores 5.0, a new published best for that case (previous record: swe-2-medium 4.0); attribution case A-a317e74b slides 14/15→7/15, the top-band backfire again ([amber-gpt W38 Addendum 4](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W38.md)). Changed 2026-09-17: the board display widens from top three to top five — #4 (15/23, seven tied lanes) and #5 (14/23, five tied lanes) appear on the table and chart for the first time. Added 2026-09-17: Qwen3.8-27B @ goldenpotato community self-hosted endpoint debuts 14/23, joining the #5 tie — a hobbyist lane on 3× V100 32GB running NVIDIA's official NVFP4 weights via a heavily patched vLLM TP3 (FP8 KV cache); build face 5/6 with a perfect 7/7 on the hard discriminator A-442d4aab, zero passes across the judgment faces (review/verify/vision/ui-build); the effort knob is proven inert (reasoning_tokens = 0 across all 57 usage records, so the row is the endpoint's default band); the endpoint was a time-limited stress test (~one day per its announcement), making this row a one-shot, non-reproducible snapshot; 26/26 papers wire-verified on (Qwen3.8-27B, custom, 27b.goldenpotato.cn) with zero stand-ins, 0/26 hash mismatches ([amber-goldenpotato W38](https://github.com/getaskclaw/amber-goldenpotato/blob/main/results/2026-W38.md)).

## How to read a results matrix

Every issue is a single `results/YYYY-Www.md` built around a matrix. Five things to know:

- **Alias (A-xxxxxxxx)** — the case's public handle. Internal case numbers never appear, so scores can't be reverse-engineered into case content.
- **bundle_sha** — the content hash of the case bundle. Match it against the [hash index](hash-index/v2026-09.md): identical means the library hasn't changed.
- **✓ / ✗ (case level)** — the pass line is "all required checks green": 8/9 still fails — a defense that leaks one pin leaks.
- **d2 (review/vision cases)** — hits − false positives − flattery − verdict penalty. Positive is hard; negative is common.
- **Comparability trio** — compare only at the same effort band and same library version, and read the date; the same model name on another endpoint may be another brain. One day's number is a snapshot, not a law.

## FAQ

**If cases are private, why trust the scores?** Trust comes from the chain, not from showing you the paper: clean-room profiles (no fallback chain), per-paper wire audits (every call reconciled; a substitute call voids the paper), a closing gate (zero pollution or nothing ships), alias + hash publishing (you can verify the library is unchanged, case by case), and a per-issue harness pin (current runs: [Hermes](https://github.com/NousResearch/hermes-agent), version + upstream commit pinned in every issue). Verifiable process is what makes up for secret cases.

**Why keep cases private at all?** Public corpora get eaten by training data; scores inflate and become unauditable. That's the chronic disease of public benchmarks. Private cases make leak status checkable.

**Can I compare two models' scores directly?** Only at the same band and same library version, ideally the same day. Cross-week comparisons must carry explicit date and band declarations (pinned in every issue); cross-repo citations likewise.

**Can I reproduce or join?** Not from the public repos alone yet (spec v0.2.2 draft; `schemas/`, `profiles/`, and tooling unpublished — see [PLAN.md](PLAN.md)). Follow the result repos for scores; methodology questions are welcome as issues.

## License

Apache-2.0 — see [LICENSE](LICENSE).
