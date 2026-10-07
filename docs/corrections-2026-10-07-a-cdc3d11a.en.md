# Correction notice 2026-10-07 (second): A-cdc3d11a is now NA on every lane

> 中文: [corrections-2026-10-07-a-cdc3d11a.md](corrections-2026-10-07-a-cdc3d11a.md)
>
> This is the second correction of 2026-10-07. Similar ones: [2026-10-02: A-d511f9e8 is now NA](corrections-2026-10-02-a-d511f9e8.en.md) and [2026-10-07: A-24bcf707 is now NA on seven lanes](corrections-2026-10-07-a-24bcf707.en.md). The three are separate.

## What changes

One review-axis case, **A-cdc3d11a**, is now **NA** (on hold, neither a win nor a loss) on **every lane**.

- The denominator does not change: 24 cases (frozen lanes keep their own sealed denominator).
- **Totals do not change, rank tiers do not change, and neither the top-five table nor the top-five chart needs a redraw.**
- On 27 lanes this case was a loss and is now NA: each has one loss fewer and one NA more, and the number of passed cases is the same. Two more lanes already had NA on this case and stay as they are.
- This is a scoring-rule correction on the board (a loss becomes NA). **No sitting is re-run**, and no original record is changed.

Before and after for each of the 29 lanes (each total already carries `'`, and the numbers are the same before and after; wins / losses / NA are case counts per lane, taken from the score database; the NA column already includes the NA recorded under the [A-d511f9e8 correction](corrections-2026-10-02-a-d511f9e8.en.md) and the [A-24bcf707 correction](corrections-2026-10-07-a-24bcf707.en.md); ∅ on frozen lanes keeps their own sealed denominator):

| Lane | Total | Before: wins / losses / NA | After: wins / losses / NA |
|---|---|---|---|
| claude-opus-5-5 @ Anthropic subscription lane | 19'/24 | 19 / 2 / 3 | 19 / **1** / **4** |
| claude-sonnet-5-5 @ Anthropic subscription lane | 19'/24 | 19 / 4 / 1 | 19 / **3** / **2** |
| swe-2-max @ Devin | 19'/24 | 19 / 3 / 2 | 19 / **2** / **3** |
| k3 @ Kimi | 18'/24 | 18 / 5 / 1 | 18 / **4** / **2** |
| glm-5.3-flash @ Ollama Cloud | 18'/24 | 18 / 5 / 1 | 18 / **4** / **2** |
| step-5-preview @ StepFun | 18'/24 | 18 / 3 / 3 | 18 / **2** / **4** |
| hy4-preview-f @ WorkBuddy ACP (W37) | 18'/24 | 18 / 5 / 1 | 18 / **4** / **2** |
| deepseek-v4.1-flash @ WorkBuddy direct (W40) | 18'/24 | 18 / 4 / 2 | 18 / **3** / **3** |
| doubao-seed-evolving @ Volcengine Ark | 17'/24 | 17 / 4 / 3 | 17 / **3** / **4** |
| gpt-6-sol-900k @ OpenAI Codex | 17'/24 | 17 / 5 / 2 | 17 / **4** / **3** |
| gpt-5.6-luna @ OpenAI Codex | 17'/24 | 17 / 6 / 1 | 17 / **5** / **2** |
| glm-5.3-flash @ WorkBuddy direct (W40) | 17'/24 | 17 / 5 / 2 | 17 / **4** / **3** |
| gpt-6-astra-900k @ OpenAI Codex | 16'/24 | 16 / 6 / 2 | 16 / **5** / **3** |
| mimo-v2.6-pro @ CommandCode | 16'/24 | 16 / 6 / 2 | 16 / **5** / **3** |
| claude-fable-5-1 @ Anthropic subscription lane | 16'/24 | 16 / 5 / 3 | 16 / **4** / **4** |
| deepseek-flash @ DeepSeek | 16'/24 | 16 / 6 / 2 | 16 / **5** / **3** |
| gpt-5.6-luna-900k (high) @ OpenAI Codex | 16'/24 | 16 / 3 / 5 | 16 / 3 / 5 (already NA) |
| gpt-6.1-sol @ OpenAI Codex | 16'/24 | 16 / 6 / 2 | 16 / **5** / **3** |
| gpt-5.6-luna-900k @ OpenAI Codex (W41) | 16'/24 | 16 / 7 / 1 | 16 / **6** / **2** |
| gpt-6-luna @ OpenAI Codex | 16'/24 | 16 / 6 / 2 | 16 / **5** / **3** |
| hy4-preview-f @ WorkBuddy direct (W40) | 16'/24 | 16 / 5 / 3 | 16 / **4** / **4** |
| minimax-m3 @ WorkBuddy direct (W40) | 16'/24 | 16 / 6 / 2 | 16 / **5** / **3** |
| deepseek-v4.1-flash @ CommandCode (frozen) | 15'/23∅ | 15 / 5 / 3 | 15 / **4** / **4** |
| Qwen3.8-27B @ goldenpotato self-hosted | 15'/24 | 15 / 7 / 2 | 15 / **6** / **3** |
| gpt-5.6-sol-900k @ OpenAI Codex (high band, frozen) | 15'/23∅ | 15 / 4 / 4 | 15 / 4 / 4 (already NA) |
| gpt-6-luna-900k @ OpenAI Codex | 15'/24 | 15 / 7 / 2 | 15 / **6** / **3** |
| deepseek-flash @ OpenCode Go | 15'/24 | 15 / 6 / 3 | 15 / **5** / **4** |
| qwen3.8-27b @ CrofAI (frozen) | 14'/21∅ | 14 / 6 / 1 | 14 / **5** / **2** |
| space-bunny-alpha @ CommandCode | 13'/24 | 13 / 8 / 3 | 13 / **7** / **4** |

## Why

On one review case the grader counted every sub-point of a well-formed finding as a separate unproven claim and treated real defects outside its short answer list as false alarms, so a correct, well-formatted review could not reach the passing line; the case is held on every lane, denominator unchanged, until the grader and exam room are repaired and the case is re-sat. **This is not a conclusion about any model's ability.**

## Effect on results

- Totals and rank tiers of all lanes do not change.
- What changes is the **review axis**: the review cell of every lane now rests on its other review case only, so the review-axis completion (the 0–1 reading prorated by required checks) changes.
- **The completion matrix chart is redrawn:** as a new file, `completion-matrix-top8-2026-w41b` (the one the README and the [ten-axes page](axes.en.md) now use). The old figure stays as history; its review axis includes A-cdc3d11a, so read it with the old rule.

## Which pages are affected

- **The askclaw.dev board and the tables on issue pages that are generated from the score database:** regenerated with the new rule.
- **Already published issue pages in the result repos of all lanes:** each will carry an update note that points to this notice; the original text is not changed. Please read the A-cdc3d11a cell through this notice.
- **The spec repo:** the top-five table and chart do not change; the completion matrix chart is redrawn; the lane notes in the [full leaderboard](leaderboard-notes.en.md) gain one sentence about the NA where affected.

## Next

No sitting is re-run. How the grader and the exam room are repaired, and when the case is re-sat, will be announced separately.
