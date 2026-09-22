# Correction notice 2026-W38: first wave of reversals and holds from the full-library review

> 中文版:[corrections-2026-W38.md](corrections-2026-W38.md)

## What is being corrected

AMBER ran a full-library review of its published 2026-09 scores, signed 2026-09-22. The first wave separates two classes: **reversals** (cause of failure attributed to the bench side; the capability score is withheld) and **holds** (evidence incomplete — named and removed from the board, excluded from all aggregates pending re-exam). Per-repo reversal and hold tables live in each of the 12 result repos' `results/2026-W38-correction.md`; this declaration is the hub's entry point and the statement of terms.

This repo has no `results/`; the affected surface is a published **methodological record** under `docs/`: the observation chain in `docs/stage1-sfail-screen-20260915.md` draws 4 observation points from papers in this review. **That document is not a scoreboard**: this notice only **annotates** it — no reversal, no aggregate, no ranking, and it counts toward no repo's headline.

## The 4 observation points (annotation only, not score cells)

| Alias | bundle_sha | Nature of observation | Annotation |
|---|---|---|---|
| A-cdc3d11a | `dbb207a3118d` | 4th item in the stable-failure sequence (1 screen-sequence item) | If that paper is later adjudicated, the sequence table must be annotated "observation may contain an infrastructure artefact"; the sequence figures are not recomputed for now |
| A-d9b79b46 | `d6d63130ecc6` | 1 failure observation in the stage-2 n=20 aggregate (6/20 pass) | Same; the aggregate rate is not recomputed for now |
| A-d9b79b46 | `d6d63130ecc6` | 1 failure observation in the stage-2 n=20 aggregate | Same |
| A-d9b79b46 | `d6d63130ecc6` | 1 failure observation in the stage-2 n=20 aggregate | Same |

> Total: 1 screen-sequence item + 3 stage-2 aggregate items = 4 observation points.

## Terms

- **Ledger**: 105 suspected papers library-wide = **34 adjudicated** + **71 held**; for undecided papers the public effect is "**may move up**", not "already reversed".
- **Two layers kept strictly apart**: "reversal" = adjudicated, and only this layer rewrites published conclusions; "held — may move up" = undecided, named only, excluded from all aggregates and rankings pending re-exam.
- **No balanced books, no board**: papers with incomplete evidence are always named, never reported as a bare count.
- **This wave does not touch amber-devin**: none of its published issues contains an affected cell.
- Handles: every affected cell = stable alias `A-xxxxxxxx` + `bundle_sha` (12 chars), matching the [public hash index v2026-09](hash-index/v2026-09.md) case by case, zero mismatches.
- Past issues stay as published; reversals appear as an appendix. Publication order: this hub declaration first, the per-repo notices after.

## Method

## Method: why we correct, how we checked, how we prevent

**Why we correct.**
These are our published numbers; if they are wrong, we are the ones who fix them. This review
found that some published failures were not the model failing the task, but the bench side —
a pre-scoring step cut off a healthy attempt, and the paper was recorded as a model failure.
Errors run both ways: judging good work as bad, and bad work as good. We checked both.
The point of a correction is not to look better or worse; it is to make the numbers on the
board match what actually happened.

**How we checked.**
Every paper was independently re-verified by multiple seats. Verifiers read the raw record
first-hand (the attempt log, the scorer output, the ledger timestamps, the fix commit) and
accepted no second-hand conclusion. Two independent directions worked in parallel — one
looking for wrongful failures, one looking for what was missed — and only papers where both
agreed went to adjudication; disagreements were held. Each verdict rests on the same evidence
chain and is re-computable paper by paper, with a signed confirmation on file. Outcomes fall
into four classes: exonerated (cause on the bench side; the capability score is withheld),
confirmed (a genuine model-side failure), held (evidence incomplete — **no quiet conviction
and no quiet pardon**), and report-level corrections that leave history untouched.

**How we prevent it.**
Three small things, one line each: ① **Evidence chain** — each paper's raw process is
recorded out of the driver's reach, append-only and sealed at the end; scoring trusts evidence
completeness only. Cause of death is a conclusion, not a fact — it can be recomputed from the
evidence, and when a rule is wrong we fix the rule and recompute; the raw facts never move.
② **Reconciliation gate** — papers in must equal papers out (scored + bench + held; no bucket
missing, no cell extra). **No balanced books, no board** — there is no "publish first, patch
later." ③ **Brain-identity double-check** — an identity assertion per paper, and no assertion
means no score; we also re-check *passed* papers against the reverse error.
No set of controls stops everything (hardware breaks), but it can make a bad verdict live
less than one reconciliation cycle.

**In one line.** What we sell is not a bench that never errs — it is one that cannot walk away
from a wrong call.

## Per-repo notice entry points

- [amber-gpt](https://github.com/getaskclaw/amber-gpt/blob/main/results/2026-W38-correction.md)
- [amber-commandcode](https://github.com/getaskclaw/amber-commandcode/blob/main/results/2026-W38-correction.md)
- [amber-ollama](https://github.com/getaskclaw/amber-ollama/blob/main/results/2026-W38-correction.md)
- [amber-crof](https://github.com/getaskclaw/amber-crof/blob/main/results/2026-W38-correction.md)
- [amber-deepseek](https://github.com/getaskclaw/amber-deepseek/blob/main/results/2026-W38-correction.md)
- [amber-kimi](https://github.com/getaskclaw/amber-kimi/blob/main/results/2026-W38-correction.md)
- [amber-stepfun](https://github.com/getaskclaw/amber-stepfun/blob/main/results/2026-W38-correction.md)
- [amber-opencode](https://github.com/getaskclaw/amber-opencode/blob/main/results/2026-W38-correction.md)
- [amber-workbuddy](https://github.com/getaskclaw/amber-workbuddy/blob/main/results/2026-W38-correction.md)
- [amber-doubao](https://github.com/getaskclaw/amber-doubao/blob/main/results/2026-W38-correction.md)
- [amber-goldenpotato](https://github.com/getaskclaw/amber-goldenpotato/blob/main/results/2026-W38-correction.md)
