# Correction notice 2026-10-07: A-24bcf707 is now NA on seven lanes

> 中文: [corrections-2026-10-07-a-24bcf707.md](corrections-2026-10-07-a-24bcf707.md)
>
> This correction of 2026-10-07 is separate from the two of 2026-10-02 ([the one about grading material](corrections-2026-10-02.en.md) and [the A-d511f9e8 one](corrections-2026-10-02-a-d511f9e8.en.md)).

## What changes

One ops-axis case, **A-24bcf707**, changes from a loss to **NA** (on hold, neither a win nor a loss) on the **seven lanes** below.

- The denominator does not change: 24 cases.
- **Totals do not change, rank tiers do not change, and neither the top-five table nor the board chart needs a redraw.** On these seven lanes the case was a loss and is now NA: each lane has one loss fewer and one NA more, and the number of passed cases is the same.
- This is a scoring-rule correction on the board (a loss becomes NA). **No sitting is re-run**, and no original record is changed.

The seven lanes (each total already carries `'`, and the numbers are the same before and after; wins / losses / NA are case counts out of 24, taken from the score database):

| Lane | Total | Before: wins / losses / NA | After: wins / losses / NA |
|---|---|---|---|
| gpt-6-sol-900k @ OpenAI Codex | 17'/24 | 17 / 6 / 1 | 17 / **5** / **2** |
| gpt-6-astra-900k @ OpenAI Codex | 16'/24 | 16 / 7 / 1 | 16 / **6** / **2** |
| gpt-6.1-sol @ OpenAI Codex | 16'/24 | 16 / 7 / 1 | 16 / **6** / **2** |
| gpt-6-luna @ OpenAI Codex | 16'/24 | 16 / 7 / 1 | 16 / **6** / **2** |
| claude-fable-5-1 @ Anthropic subscription lane | 16'/24 | 16 / 6 / 2 | 16 / **5** / **3** |
| gpt-6-luna-900k @ OpenAI Codex | 15'/24 | 15 / 8 / 1 | 15 / **7** / **2** |
| Qwen3.8-27B @ goldenpotato self-hosted | 15'/24 | 15 / 8 / 1 | 15 / **7** / **2** |

The case A-d511f9e8 stays NA on every lane under the [correction of 2026-10-02](corrections-2026-10-02-a-d511f9e8.en.md), and the NA column above already includes it. The 2 NA of claude-fable-5-1 before this correction were A-d511f9e8 and one case that ran out of the exam time limit (its brand case A-d9b79b46 was re-sat on 2026-10-07 after its prompt was revised and counts as a loss, see the [hash index](../hash-index/v2026-09.md)).

## Why

The grading of this case asks for one more thing than the task text says.

- **What the grader required**: the named removal commit had to have deleted lines inside the feature's own files.
- **What the prompt asks for**: the commit where the feature was removed or lost; it does not state that requirement.

On these seven lanes the case failed only on that requirement; the other requirements were met. A requirement that the task text does not state, but the grader enforces, is not evidence of a difference in ability, so this case is now NA for these seven lanes instead of a loss. **This is not a conclusion about any model's ability.**

## Effect on results

- The totals and rank tiers of the seven lanes do not change, and the other lanes are not affected.
- What changes is the **ops axis**: on these seven lanes the case goes from a loss to NA, so the ops-axis completion (the 0–1 reading prorated by required checks) changes, because the case is no longer counted.
- **No lane with 18 or more on the board is among the seven**, so the completion matrix chart does not change.

## Which pages are affected

- **The askclaw.dev board and the tables on issue pages that are generated from the score database:** regenerated with the new rule.
- **Already published issue pages in the result repos of these seven lanes:** each will carry an update note that points to this notice; the original text is not changed. Please read the A-24bcf707 cell through this notice.
- **The spec repo:** the top-five table and chart do not change; the lane notes in the full leaderboard gain one sentence about the NA.

## Not covered by this correction

- **gpt-5.6-sol-900k (high band, frozen)** is not covered by this correction.
- The scoring of this case on all other lanes does not change.

## Next

No sitting is re-run. How the grading requirement of this case is fixed will be announced separately.
