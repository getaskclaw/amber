# AMBER — Sealed-in-Amber Historical Replay Evaluation

`Seal the scene in amber. Sit the exam of that moment, again.`

**Library** 23 cases / 26 papers · **Spec** v0.2.2 (draft) · **Hash index** [v2026-09](hash-index/v2026-09.md) · **Result repos** × 7 · **Rule** scores public, cases never

中文说明:[README.md](README.md). The normative document is [AMBER-Core-Specification.md](AMBER-Core-Specification.md).

## What this is

A formal evaluation method: take a **real, auditable** historical incident and reconstruct the scene exactly as of "before the answer was known". The candidate receives only the information available at that moment; all later evidence and scoring material is **physically sealed**. The candidate diagnoses, decides, acts, abstains, refuses, or escalates. Scoring criteria are frozen before any output is seen. Everything is archived and auditable.

## Why

Public benchmarks are static public corpora: training contamination is rampant and unauditable, scores inflate, and static Q&A doesn't measure what real work demands — multi-step diagnosis, abstention, refusal, escalation under uncertainty. AMBER replays **provenance-controlled** real events whose leak status is checkable. It runs alongside public benchmarks, never replaces them.

## Three visuals

- **What it is** — private case library, public scores: [docs/images/what-is-amber.png](docs/images/what-is-amber.png)
- **How a result is produced** — sealed authoring, clean-room exam, per-paper wire audit, redacted publishing, public verification: [docs/images/trust-chain.png](docs/images/trust-chain.png)
- **Current top three** — same name on different endpoints can be a different brain, so scores are recorded per endpoint × name: [docs/images/top3-2026-w37.png](docs/images/top3-2026-w37.png)

## Two irreducible caveats

- **Runtime sealing ≠ training-data purity**: we seal runtime evidence; we cannot prove the model never saw the future in training.
- **A historical outcome is evidence, not the single correct answer.**

## Status

Draft v0.2.2. The Core spec is stable; `schemas/`, `profiles/`, and case-building/runner tooling are **not yet published** — a compliant run cannot be executed from this repo alone. See [PLAN.md](PLAN.md).

## Weekly results (sister repos)

Scores and cases are published separately: results are public, cases never are. Weekly full-library runs (aliases + bundle hashes verifiable against the [public hash index](hash-index/v2026-09.md)):

- [amber-crof](https://github.com/getaskclaw/amber-crof) — CrofAI models
- [amber-commandcode](https://github.com/getaskclaw/amber-commandcode) — CommandCode models
- [amber-deepseek](https://github.com/getaskclaw/amber-deepseek) — official DeepSeek API models
- [amber-devin](https://github.com/getaskclaw/amber-devin) — Devin models
- [amber-ollama](https://github.com/getaskclaw/amber-ollama) — Ollama Cloud models
- [amber-opencode](https://github.com/getaskclaw/amber-opencode) — OpenCode Go models
- [amber-gpt](https://github.com/getaskclaw/amber-gpt) — GPT-family models × reasoning-effort bands

## How to read a results matrix

Each issue is one `results/YYYY-Www.md` built around a matrix. Five keys:

- **Alias (A-xxxxxxxx)** — the public case handle. Internal case numbers never appear, so scores cannot be reverse-engineered into case content.
- **bundle_sha** — content hash of the case bundle. Match it against the [hash index](hash-index/v2026-09.md): identical = the library hasn't changed.
- **✓ / ✗ (case level)** — the pass line is "all required checks green": 8/9 is still a fail — a defense that leaks one pin leaks.
- **d2 (review/vision cases)** — hits − false positives − praise − verdict penalty. Positive is hard; negative is common.
- **Comparability trio** — compare only at the same effort band, same library version, and read the date; the same model name on another endpoint may be another brain. A single day's number is a snapshot, not a law.

## FAQ

**If cases are private, why trust the scores?** Trust comes from the chain, not from showing the paper: clean-room profiles (no fallback chain), per-paper wire audits (every call reconciled; a substitute call voids the paper), a closing gate (zero pollution or nothing ships), and alias + hash publishing (you can verify the library is unchanged, case by case). Process verifiability compensates for case secrecy.

**Why keep cases private at all?** Public corpora get eaten by training data; scores inflate and become unauditable. Private cases make leak status checkable.

**Can I compare two models' scores directly?** Only at the same band, same library version, ideally same day. Cross-week comparisons must carry explicit date and band declarations (pinned in every issue).

**Can I reproduce or join?** Not from the public repos alone yet (spec v0.2.2 draft; tooling unpublished — see [PLAN.md](PLAN.md)). Follow the result repos for scores; methodology questions welcome as issues.

## License

Apache-2.0 — see [LICENSE](LICENSE).
