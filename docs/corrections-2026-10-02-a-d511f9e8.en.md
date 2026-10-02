# Correction notice 2026-10-02 (second): A-d511f9e8 is now NA on every lane

> 中文: [corrections-2026-10-02-a-d511f9e8.md](corrections-2026-10-02-a-d511f9e8.md)
>
> This is the second correction of 2026-10-02. It is separate from [the one about 9 papers that touched grading material](corrections-2026-10-02.en.md).

## What changes

One defense-axis case, **A-d511f9e8**, is now **NA** (on hold, neither a win nor a loss) on **every lane**.

- The denominator does not change: 24 cases (frozen lanes keep their own sealed denominator).
- **The number of passed cases does not change.** This case was a loss before (on a few lanes it was already NA); now it is NA everywhere.
- So **every lane's total now carries `'`**. A `'` means the lane has an NA cell.

Ten lanes on the askclaw.dev board get a new apostrophe. The numbers stay the same:

| Lane | Before | After |
|---|---|---|
| claude-sonnet-5-5 @ Anthropic subscription lane | 19/24 | **19'/24** |
| k3 @ Kimi official coding | 18/24 | **18'/24** |
| hy4-preview-f @ WorkBuddy | 18/24 | **18'/24** |
| glm-5.3-flash @ Ollama Cloud | 18/24 | **18'/24** |
| gpt-6-sol-900k @ OpenAI Codex | 17/24 | **17'/24** |
| gpt-6-astra-900k @ OpenAI Codex | 16/24 | **16'/24** |
| gpt-6.1-sol @ OpenAI Codex | 16/24 | **16'/24** |
| gpt-6-luna-900k @ OpenAI Codex | 15/24 | **15'/24** |
| Qwen3.8-27B @ goldenpotato self-hosted | 15/24 | **15'/24** |
| qwen3.8-27b @ CrofAI (frozen) | 16/23∅ | **16'/23∅** |

The other lanes on the board already carried `'` (they have an NA on another case), so their numbers stay the same; this case is now NA for them too (on a few lanes it was already NA). Lanes that are not on the askclaw.dev board (for example the older Devin, Ollama and Kimi lanes in the top-five table of the spec repo) were graded by the same exam-room grader, so the same applies, and their totals in that table also carry `'`.

## Why

The exam-room grading of this case has two problems.

1. **The grader did not grade the file the candidate delivered.** Of the 104 recorded sittings, 79 (76%) were graded on the original file of the task, not on the file the candidate delivered. The candidate had written the hardened checker somewhere else, and the original file scores exactly 4/12. The task text says the file name is free.
2. **The grader asks for something the task text does not say.** The grader requires that a failure is blamed only on the one named check; reporting one more check fails the paper. The task text does not state this. Some candidates blocked the bad data correctly and still failed because they reported one check too many.

An independent reviewer re-ran both points and confirmed the main finding. So the result on this case cannot be used as evidence of a lane's defense ability, and it is held on every lane.

## Effect on results

- **On the 22 lanes of the board, re-grading the delivered file would not turn this case into a pass for any lane.** So no pass count changes.
- What changes is the **defense-axis completion** (the 0–1 reading prorated by required checks). It used to include this case; now the case is not counted, so each lane's defense-axis completion changes.
- No original record is changed. This was a read-only re-grading check.

## Which pages are affected

- **The askclaw.dev board and the tables on issue pages that are generated from the score database:** regenerated with the new rule.
- **Hand-written older issue pages:** kept as they were. Please read the A-d511f9e8 cell through this notice.
- **The top-five table and chart in the spec repo:** `'` added, chart redrawn.
- **The completion matrix chart (`completion-matrix-7way`):** not redrawn yet. Its defense-axis values include A-d511f9e8, so read it with the old rule; this note stays here until it is redrawn.

## Next

This case is not scored for now. How the task text and the grader are fixed, and whether the case is taken again, will be announced separately.
