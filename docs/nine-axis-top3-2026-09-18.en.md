# Nine-axis podium: top 3 per axis (2026-09-18)

**Headline: only four of the nine axes actually discriminate.** Coding, delivery, ops, requirements, and UI are saturated at the top (full marks or identical scores across the field) — a "top 3" is meaningless there. The discriminating four are **defense, attribution, review, and vision**, and their champions belong to four different vendors: the overall board leader wins none of the judgment faces.

## Method and sources

- Data: published issues of the 11 result repos (2026-W36 ~ W38), recomputed case-by-case across 40 published lanes
- Normalization: pin cases score `pins earned / total pins`; defect-hunt (d2) cases follow the published face-profile convention `(d2 + 4) / 9`
- Multiple bands or reruns of the same "model @ endpoint" fold into that lane's best published run
- Recomputed anchors match published values (e.g. doubao's verification axes 0.47 / 0.50; gp27b coding 0.83 / ops 0.97)
- Known limits: cross-week snapshots, the 21→23 case-set transition, and single-run lanes not yet re-measured (flagged inline)
- **The "Vendor" column records the *claimed* model's vendor; whatever follows @ is an official or relay channel — relay lanes get no identity endorsement.** CrofAI in particular: ktibow's 2026-09-13 [wire-level report](https://kendell.dev/blog/crofaifalse) identifies crof.ai as an OpenRouter wrapper with several storefront models fingerprinting to entirely different upstreams, and our own [behavioral-fingerprint analysis](https://github.com/getaskclaw/amber-crof/blob/main/docs/model-identity-cosine-2026-09.en.md) independently corroborates this (crof `glm-5.3-flash` sits closest to `deepseek-v4.1-flash @ ollama` on all three measures; `qwen3.8-27b` is suspect but unproven). Every CrofAI lane below carries a ⚠ — its scores are real and valid, but *who* it is remains unverified

## The four discriminating axes

### Defense — plug the validator's holes (mean of 2 cases)

| Rank | Model @ endpoint | Completion | Vendor |
|---|---|---|---|
| 1 | deepseek-v4.1-flash @ WorkBuddy | 0.667 | DeepSeek |
| 2 | deepseek-v4.1-flash @ CommandCode | 0.611 | DeepSeek |
| 3 | tie: deepseek-flash @ OpenCode Go / deepseek-v4-flash:0731 @ Ollama Cloud / kimi-for-coding (K2.8) @ Kimi official | 0.556 | DeepSeek ×2, Moonshot |

### Attribution — match symptoms to root causes (1 case, 15 pins)

| Rank | Model @ endpoint | Completion | Vendor |
|---|---|---|---|
| 1 | qwen3.8-27b @ CrofAI ⚠ | **1.000** (the only 15/15 on the field) | **Claimed** Alibaba Qwen — identity unverified: behavioral fingerprint sits closest to the DeepSeek 0731 lane ([fingerprint analysis](https://github.com/getaskclaw/amber-crof/blob/main/docs/model-identity-cosine-2026-09.en.md)) |
| 2 | tie: glm-5.3-flash @ Ollama Cloud / gpt-6-astra @ OpenAI Codex / hy4-preview-f @ WorkBuddy | 0.933 | Zhipu, OpenAI, WorkBuddy lane |

### Review — be the inspector (mean of 2 defect-hunt cases)

| Rank | Model @ endpoint | Completion | Vendor |
|---|---|---|---|
| 1 | swe-2-high @ Devin (originally labeled swe-2-low — [correction 2026-09-18](corrections-2026-09-18.en.md): that id does not exist; the run was actually a high re-run) | 0.722 (**single run, not re-measured** — excluded from routing conclusions until then) | Devin |
| 2 | tie: glm-5.3-flash @ Ollama Cloud / deepseek-v4.1-flash @ Ollama Cloud | 0.667 | Zhipu, DeepSeek |

Worth stating plainly: swe-2-high is not at the top of the overall ladder yet posts its family's best review score at 0.722 — judgment faces and construction faces do not correlate. (This row was originally attributed to swe-2-low; the conclusion stands, the attribution is corrected.)

### Vision — spot defects in real screenshots (1 defect-hunt case)

| Rank | Model @ endpoint | Completion | Vendor |
|---|---|---|---|
| 1 | gpt-5.6-luna (max band, 09-17) @ OpenAI Codex | **1.000** (d2=5.0, the case's best published score ever) | OpenAI |
| 2 | tie: swe-2-medium @ Devin / gpt-5.6-luna (high band, 09-12) @ OpenAI Codex (both d2=4.0) | 0.889 | Devin, OpenAI |

## The five saturated axes

- **Coding**: 24 lanes tied at 0.958 — everyone loses the same 2 pins on A-87c472cb; nobody sweeps 6/6. The axis does not currently separate the leaders
- **Delivery**: 1.000 tied across 29 lanes (the signal is negative: no-deliverable lanes are simply out)
- **Ops**: full marks tied across 14 lanes (swe-2-max, k3, doubao-seed-evolving, gpt-5.6-luna, hy4-preview-f, the DeepSeek lanes, etc.)
- **Requirements**: full marks tied across ~26 lanes
- **UI**: full marks tied across 12 lanes (all swe-2 bands, gpt-6-astra, gpt-5.6-sol/luna-max, glm-5.3-flash @ CrofAI ⚠, two deepseek-v4.1-flash lanes, hy4-preview-f, glm-5-2 @ Devin)

## How to read this

A one-day number is a snapshot, not a law. After "thinking longer ≠ scoring better" and "same score ≠ same shape," this table adds a third cut: **the overall board leader holds no championship on any judgment face** (swe-2-max's strengths sit on the saturated axes). Pick the axis that matches the job you need done — don't order by total score.

中文版：[nine-axis-top3-2026-09-18.md](nine-axis-top3-2026-09-18.md)
