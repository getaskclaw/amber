# AMBER — Archived-Moment Behavioral Evaluation Replay

`封进琥珀，重做当时的题。` — pack the moment in amber; work the problem of that time again.

AMBER is a formal evaluation method: take a real, auditable historical event; restore its exact pre-outcome state; give the candidate only cutoff-available information; physically seal all later evidence and evaluator materials; let the candidate diagnose, decide, act, abstain, refuse, or escalate; judge against criteria fixed before any output is viewed; preserve everything for audit.

**Why:** public benchmarks are static public question sets — training contamination is common and unauditable, scores inflate, and static Q&A does not measure what real work demands (multi-step diagnosis, abstention, refusal, escalation under uncertainty). AMBER replays real events whose leak status is checkable because the source is controlled. It runs alongside public benchmarks, never as their replacement.

## Status

Draft v0.2.2. The normative Core is stable; `schemas/` and `profiles/` are inherited from the predecessor corpus and are not yet published here.

## Contents

- [AMBER-Core-Specification.md](AMBER-Core-Specification.md) — the normative cross-domain core: purpose, definition, mechanism, 8 invariants, 8 boundaries, epistemic limits, naming review, adoption rules.
- [protocols/distribution.md](protocols/distribution.md) — moving cases between hosts: the public/private channel split, pinned bundle construction, signed manifests, the public hash index, seal probes, run records, comparability.
- [PLAN.md](PLAN.md) — status, milestones (case tooling, reference runner, oracles, statistics, public index), and open design questions.

## License

Apache-2.0 — see [LICENSE](LICENSE).
