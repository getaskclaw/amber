# Method change 2026-10-01: hermes-lane system prompts keep only the clean-room content

> 方法变更。中文版：[method-change-2026-10-01.md](method-change-2026-10-01.md)

## What changed

On AMBER lanes that answer through [Hermes](https://github.com/NousResearch/hermes-agent) ("hermes lanes"), the system prompt of a tools-on exam session used to carry two extra blocks. Besides the published clean-room SOUL and Hermes's own tool and environment notes, Hermes added on its own:

1. a role brief along the lines of "you are a coding agent pairing with the user inside their codebase";
2. a workspace snapshot: the root path and branch of the git repository that contains the paper directory, plus the subjects of that repository's last three commits.

**Why**: since 2026-06-10 (upstream #43316), Hermes decides whether a session is a "coding" session by walking up from the session's working directory, on the machine it runs on, looking for a git repository. AMBER papers sat inside the exam tree's git repository, so every tools-on session was treated as a coding session.

The snapshot contained no case text, no oracle and no answers; the commit subjects are maintenance records of the exam tree. These blocks are still not part of the clean-room conditions we publish, so we turned them off.

## From which sitting

From exam-harness version 2026-10-01 on, that is, sittings started after amber-run `65bea1bc`:

- every paper's Hermes config sets `agent.coding_context: off`;
- paper directories live outside any git repository, checked automatically before a sitting; if the check fails, the sitting does not start;
- each issue's Run identity names the harness version.

From then on the system prompt is the clean-room SOUL plus Hermes's built-in tool and environment notes, which are unchanged.

## Effect on published scores

- **Hermes-lane scores up to and including 2026-W40** were all sat with these two blocks present, so they share the same conditions. They stand as published; no score changes. The behavior predates AMBER's first issue, but we have not checked the exact Hermes version of every past sitting, so this statement holds for the versions we did check.
- **Lanes that do not answer through Hermes** (Devin, WorkBuddy ACP direct) are not affected.
- **Comparing across this date**: when you compare hermes-lane scores from before and after it, treat this as a change in exam conditions.
