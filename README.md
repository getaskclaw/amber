[简体中文](README.zh-CN.md) · English

# AMBER — Sealed-in-Amber Historical Replay Evaluation

`Seal the scene in amber. Retake the exam of that moment.`

**In one line**: we take real past incidents and tasks and have AI models redo them using only what people had in hand at the time. For example, a real operations outage: the model gets only the monitoring and logs of the time, and the evidence revealed afterwards stays sealed. The questions are never published, but every question has a hash fingerprint, and scores and fingerprints are all public, so anyone can check that the questions were not swapped and the scores were not made up.

**Library** 24 cases · **Spec** v0.2.2 (draft) · **Hash index** [v2026-09](hash-index/v2026-09.md) · **Result repos** × 13 · **Rule** scores always public, cases never · **Live board** [askclaw.dev](https://askclaw.dev/en/)

> ⚠️ **Corrections** (original text and the list of affected lanes: [leaderboard in full](docs/leaderboard-notes.en.md))
> - **[2026-10-02](docs/corrections-2026-10-02.en.md)**: 22 published papers whose candidate stepped outside the paper and touched grading material are now NA (neither a pass nor a fail). The fault is ours; since 2026-10-01 papers are answered in isolated containers.
> - **[2026-10-02 (second)](docs/corrections-2026-10-02-a-d511f9e8.en.md)**: one defense-axis case, A-d511f9e8, is now NA on every lane. The denominator and the **number of passed cases do not change**; every lane's total now carries `'`.
> - **[2026-10-07](docs/corrections-2026-10-07-a-24bcf707.en.md)**: one ops-axis case, A-24bcf707, changes from a loss to NA on seven lanes (the grading asked for one more thing than the task text says). The denominator, **totals and rank tiers do not change**, and no sitting is re-run.
> - Earlier: [2026-09-18](docs/corrections-2026-09-18.en.md) (swe-2-low was actually swe-2-high) · [2026-W38](docs/corrections-2026-W38.en.md) (full-library review, per-repo notices)

## Who leads now

![Current top five 2026-W41, including the 2026-10-02 correction, the 2026-10-02 tests, the four WorkBuddy direct lanes of 2026-10-04, the five new sittings of 2026-10-06, one brand-case re-sit of 2026-10-07 and A-d511f9e8 on hold for every lane](docs/images/top5-2026-w41b.en.png?v=20261007)

| # | Total | Model @ endpoint |
|---|---|---|
| 1 | 19'/24 | swe-2-max @ Devin<br>claude-sonnet-5-5 @ Anthropic subscription lane<br>claude-opus-5-5 @ Anthropic subscription lane |
| 2 | 18'/24 | glm-5.3-flash @ Ollama Cloud<br>k3 @ Kimi<br>hy4-preview-f @ WorkBuddy ACP (W37)<br>deepseek-v4.1-flash @ WorkBuddy direct (W40)<br>step-5-preview @ StepFun (W41) |
| 3 | 17'/24 | gpt-6-sol-900k @ OpenAI Codex<br>swe-2-high @ Devin<br>doubao-seed-evolving @ Volcengine Ark<br>glm-5.3-flash @ WorkBuddy direct (W40)<br>gpt-5.6-luna @ OpenAI Codex |
| 4 | 16'/24 | gpt-5.6-luna-900k (high) @ OpenAI Codex<br>gpt-6-astra-900k @ OpenAI Codex<br>gpt-6.1-sol @ OpenAI Codex<br>claude-fable-5-1 @ Anthropic subscription lane<br>deepseek-v4-flash:0731 @ Ollama Cloud<br>swe-2-medium @ Devin<br>deepseek-v4.1-flash @ Ollama Cloud ▼<br>deepseek-flash @ DeepSeek ▼<br>mimo-v2.6-pro @ CommandCode ▼<br>hy4-preview-f @ WorkBuddy direct (W40)<br>minimax-m3 @ WorkBuddy direct (W40)<br>gpt-5.6-luna-900k @ OpenAI Codex (W41)<br>gpt-6-luna @ OpenAI Codex |
| 5 | 15'/24 | kimi-for-coding (K2.8) @ Kimi<br>gpt-6-luna-900k @ OpenAI Codex<br>swe-1-7-medium @ Devin<br>Qwen3.8-27B @ GoldenPotato self-hosted<br>deepseek-flash @ OpenCode Go ▼ |

`'` = at least one case is NA (not scored; it does not count as a loss). Every total carries it now, because A-d511f9e8 is NA on every lane. The same model name on a different endpoint can be a different brain, so scores are always recorded per endpoint × name. claude-opus-5-5 is shown with its W40 re-test (its W39 first test was 17'/24): each test was taken once, in a different exam room, so this does **not** show that it got stronger or weaker; see [amber-claude W40](https://github.com/getaskclaw/amber-claude/blob/main/results/2026-W40.en.md). ▼ = moved down by the 2026-10-02 correction. The four WorkBuddy direct (W40) lanes are new sittings of 2026-10-04 in an isolated exam room, not comparable cell by cell with W37 (ACP lane) or W39 (direct-lane sitting); hy4-preview-f has two rows on the board, ACP (W37, 18') and direct (W40, 16'): different lanes in different exam rooms, so this does **not** show that it got stronger or weaker; see [amber-workbuddy W40](https://github.com/getaskclaw/amber-workbuddy/blob/main/results/2026-W40.en.md). The five new sittings of 2026-10-06 (W41) were also taken in the isolated exam room: gpt-5.6-luna, gpt-5.6-luna-900k (W41) and gpt-6-luna are three new lanes on the board; for step-5-preview and gpt-6-luna-900k the board now takes the 2026-10-06 re-sit: gpt-6-luna-900k is 15'/24; step-5-preview scored 17'/24 in that sitting, and after the prompt of the brand case A-d9b79b46 was revised (see the 2026-10-07 re-issue note in the [hash index](hash-index/v2026-09.md)) that case was re-sat on 2026-10-07 and passed, so it now stands at 18'/24 (3 NA: A-d511f9e8 on hold, and two cases that hit the exam-room time cap). The 15' that step-5-preview scored at its W38 first test (moved down by the 2026-10-02 correction, previously marked ▼) is no longer its board entry, so it no longer carries ▼. These sittings are not comparable cell by cell with those of W37 to W39; for step-5-preview and gpt-6-luna-900k, each of the two sittings was taken once, in a different exam room, so this does **not** show that either got stronger or weaker. There are two gpt-5.6-luna-900k rows, and they are different lanes: the one marked (high) is the W37 baseline (high band) result, the one marked (W41) is a new 2026-10-06 sitting in the isolated exam room. Case-by-case results of the W41 sittings: [amber-gpt W41](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W41.en.md) (gpt-5.6-luna, gpt-5.6-luna-900k, gpt-6-luna and gpt-6-luna-900k) and [amber-stepfun W41](https://github.com/getaskclaw/amber-stepfun/blob/main/results/2026-W41.en.md) (step-5-preview). Sources per lane, footnotes and frozen lanes: [leaderboard in full](docs/leaderboard-notes.en.md).

## Same score, different shape

Lanes with the same total can have very different strengths and weak spots. A bigger, darker dot = higher completion; NA = no scorable case on that axis, not a zero.

![Completion matrix: the 8 lanes with 18+ on the board, ten axes, 24 cases, 2026-10-07](docs/images/completion-matrix-top8-2026-w41.en.png?v=20261007)

*The 8 lanes = every lane with 18 or more on the board (database of 2026-10-07). hy4-preview-f is its ACP (W37) row; the direct (W40, 16') lane of the same name has a total below 18 and is not in the figure. On deepseek-v4.1-flash @ WorkBuddy direct (W40), the UI axis holds one case, A-d9b79b46, which is on hold and counted as NA, so that cell is NA, not a zero; its vision cell is taken from the re-sit paper after the exam-room fix, see [amber-workbuddy W40](https://github.com/getaskclaw/amber-workbuddy/blob/main/results/2026-W40.en.md). The defense axis is computed with A-d511f9e8 as NA on every lane, so each cell there reflects only the other case (a cell where neither case has a scorable result is NA). On step-5-preview (W41), the UI cell is 1.00: the brand case A-d9b79b46 was re-sat alone on 2026-10-07 after its prompt was revised and passed (12/12), see [amber-stepfun W41](https://github.com/getaskclaw/amber-stepfun/blob/main/results/2026-W41.en.md); its defense and attribution cells are NA because on each of those two axes one case hit the exam-room time cap and has no scorable result.*

**How to read it**: the hands-on "building" axes are almost full for everyone; the differences are on the "judging" side. Each cell = the lane's completion (0–1) across that axis's cases. The official board on [askclaw.dev](https://askclaw.dev/en/) uses the same ten axes.

| Side | Axis | What it tests |
|---|---|---|
| Building | Coding | implement the spec correctly |
| | Delivery | done ≠ handed in: no artifact means 0 |
| | Ops | follow the runbook, no skipped steps |
| | Requirements | the client asked for A, not B: ship A |
| | Convergence | real finish, or busywork loops |
| Judging | UI | build the page to the mock, pin-level |
| | Vision | spot defects in real screenshots |
| | Defense | plug validator holes without turning away legit input |
| | Attribution | pin each defect to the right root cause |
| | Review | find real defects in someone's work; misses and false alarms both cost |

Per-axis reading and each lane's numbers: [the ten axes and the completion matrix](docs/axes.en.md).

## How it works

A private case library plus public scores: the cases never go public, the scores and hashes always do. The rubric is frozen before anyone sees the output, and everything is archived.

![What is AMBER](docs/images/what-is-amber-2026-10.en.png?v=20261003)

A result is produced like an exam: papers sealed at authoring, sat in a clean room, audited paper by paper, published redacted, checkable by anyone.

![How a result is produced](docs/images/trust-chain.en.png?v=20260915b)

Three more findings (effort bands, token bills, wall time vs. score): [docs/findings-effort-and-speed.en.md](docs/findings-effort-and-speed.en.md).

## Result repos

Results are public, cases never are. Aliases and bundle hashes are checked case by case against this repo's public hash index.

[amber-claude](https://github.com/getaskclaw/amber-claude) (Claude) · [amber-gpt](https://github.com/getaskclaw/amber-gpt) (GPT) · [amber-devin](https://github.com/getaskclaw/amber-devin) (Devin) · [amber-kimi](https://github.com/getaskclaw/amber-kimi) (Kimi) · [amber-deepseek](https://github.com/getaskclaw/amber-deepseek) (DeepSeek) · [amber-ollama](https://github.com/getaskclaw/amber-ollama) (Ollama Cloud) · [amber-opencode](https://github.com/getaskclaw/amber-opencode) (OpenCode Go) · [amber-commandcode](https://github.com/getaskclaw/amber-commandcode) (CommandCode) · [amber-workbuddy](https://github.com/getaskclaw/amber-workbuddy) (WorkBuddy) · [amber-doubao](https://github.com/getaskclaw/amber-doubao) (Doubao) · [amber-stepfun](https://github.com/getaskclaw/amber-stepfun) (StepFun) · [amber-nous](https://github.com/getaskclaw/amber-nous) (Nous Portal) · [amber-goldenpotato](https://github.com/getaskclaw/amber-goldenpotato) (community self-hosted Qwen3.8-27B)

## FAQ

**If cases are private, why trust the scores?** Trust comes from a verifiable process: clean-room exams, per-paper wire audits (a substitute call voids the paper), a closing gate, alias + hash publishing, and a harness pin in every issue (current: [Hermes](https://github.com/NousResearch/hermes-agent)). Changes to exam conditions are published one by one; the latest: [method change 2026-10-01](docs/method-change-2026-10-01.en.md).

**Why keep cases private at all?** Public corpora get eaten by training data; scores inflate and become unauditable. Private cases make leak status checkable.

**Can I compare two models' scores directly?** Only at the same band and library version, ideally the same day. Cross-week comparisons must carry the date and band.

**Can I reproduce or join?** Not from the public repos alone yet (see [PLAN.md](PLAN.md)). Follow the result repos for scores; methodology questions are welcome as issues.

## Spec and docs

- [AMBER-Core-Specification.md](AMBER-Core-Specification.md) — the normative spec
- [protocols/distribution.md](protocols/distribution.md) · [protocols/stability.md](protocols/stability.md) — distribution and stability protocols
- [hash-index/v2026-09.md](hash-index/v2026-09.md) — the public hash index (24 cases)
- [PLAN.md](PLAN.md) · [CONTRIBUTING.md](CONTRIBUTING.md) — roadmap; contribution rules (**this repo never accepts case content**)
- [docs/](docs/README.en.md) — the full documentation index (leaderboard in full, the ten axes, research notes, correction notices, manifest schema and validator)


- **Status**: draft v0.2.2. The Core spec is stable; `profiles/` and the case-building/runner tooling are not yet published.
- **Two caveats that won't go away**: (1) runtime sealing ≠ training-data purity: we seal runtime evidence and cannot prove the model never saw the future in training. (2) A historical outcome is evidence, not the one correct answer.
- **Why it exists**: public benchmarks are frozen corpora; contamination is rampant and unauditable, and they cannot measure multi-step diagnosis, abstention, refusal or escalation under uncertainty. AMBER replays provenance-controlled real events; it runs alongside public benchmarks and does not replace them.

## License

Apache-2.0 — see [LICENSE](LICENSE).
