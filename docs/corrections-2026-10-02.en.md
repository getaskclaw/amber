# Correction 2026-10-02: 9 papers touched grading material while being answered; now NA

> 更正声明。中文版：[corrections-2026-10-02.md](corrections-2026-10-02.md)

## What is corrected

Among AMBER's published results, **9 papers scored as passes** were answered by a candidate that read material it should never have seen: the grading program, the reference answer, the original case description, or other lanes' grading records. Those passes do not count.

The 9 papers are now **NA** (held, counted neither as a pass nor as a fail). The denominator stays the same. Six lanes are affected:

| lane | issue | case (public alias) | was | now |
|---|---|---|---|---|
| deepseek-v4.1-flash @ CommandCode | W37 | A-61f7ad01, A-24bcf707 | 17/23 | **15'/23** |
| deepseek-flash @ OpenCode Go | W37 | A-24bcf707, A-8d4bc770 | 17/24 | **15'/24** |
| space-bunny-alpha @ CommandCode | W39 | A-a5608487, A-be92627f | 15/24 | **13'/24** |
| deepseek-flash (GA) @ DeepSeek official | W37 | A-a5608487 | 17/24 | **16'/24** |
| mimo-v2.6-pro @ CommandCode | W39 | A-a5608487 | 17'/24 | **16'/24** |
| step-5-preview @ stepfun plan endpoint | W38 | A-61f7ad01 | 16'/24 | **15'/24** |

`'` marks a lane with at least one NA cell. No other lane's score changes.

## How it happened

Lanes that answer through [Hermes](https://github.com/NousResearch/hermes-agent) ("hermes lanes") used to receive their paper as an ordinary directory on the exam machine. With tools on, a candidate could see files outside its paper, including the case library and the exam tree's version history. Most candidates worked only inside their own paper. On these 9 papers, the candidate stepped outside it and read grading material; some also ran the grading program to check their own answer.

One of the 9 (A-61f7ad01 @ CommandCode) never left its paper. A cached copy of the grading program, left behind by the case author's own testing, was copied into the paper when it was staged; the candidate decompiled it and used it as a grader. That is also a defect of the exam setup, so this paper is voided too.

This is an isolation defect in our exam setup. The fault is ours, not the candidates'.

## How we checked

- We read the tool-call record of every scored hermes-lane paper and flagged every call that reached a path outside the paper. A person then reviewed each flagged call, including both the command and what it returned.
- These did not count as touching grading material, and those scores stand:
  - listing a directory name without reading its contents;
  - reading material that the case hands to the candidate anyway.
- Coverage: 467 scored hermes-lane papers. 456 have a full session record and were all reviewed. **The other 11 have no session record. They cannot be reviewed, so their published results stand.**
- **Lanes that do not answer through Hermes** (Devin, WorkBuddy ACP direct) run in their vendors' own environments and are outside the scope of this review.

## How scores change

- The 9 papers are NA. They count neither as a pass nor as a fail, and the denominator is unchanged.
- There are no retakes: a retake would run under the new exam setup, not the conditions of the original issue.
- The askclaw.dev board shows the corrected scores from the publication of this notice.
- The original issue write-ups stay as published. Where they differ, this notice governs.
- Separately, every other published score was re-graded independently: every scored paper that could be reproduced matched its original verdict.

## What we changed

From 2026-10-01, each hermes-lane paper is answered inside a disposable container:

- the container has no network, and the candidate cannot see the case library, other papers or the exam tree;
- papers are staged only from registered paper packs, with a fingerprint check and a grader self-check before the sitting.

claude-sonnet-5-5 (2026-W40) was the first sitting run in an isolated container. From the next sitting on, paper directories also live outside any git repository. See [method change 2026-10-01](method-change-2026-10-01.en.md).
