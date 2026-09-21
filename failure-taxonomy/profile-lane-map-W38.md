# AMBER 第 0 步：profile → lane → bench 会话数 映射表（W38）

判据：`sessions.source` 形如 `amber-lib-<案>-<lane>-<band>`；`sessions.model` 为钉住模型。
lane 归属由 `runs-*/manifest.jsonl` 的 session-id 实证 join（见 `lane-registry.json`）与各成绩仓 run-identity 表核对。

| profile | 对应 lane (2606 成绩仓) | 总会话 | bench 会话 | 非 bench | 模型 | 档位 |
|---|---|---:|---:|---:|---|---|
| amber-a | — (early foreman-round1 / r1-r2 probes) | 19 | 0 | 19 |  |  |
| amber-b | amber-ollama (glmflash low probe) | 40 | 25 | 15 | glm-5.3-flash:cloud×25 | low×25 |
| amber-cc | amber-commandcode | 132 | 130 | 2 | deepseek/deepseek-v4.1-flash×130 | high×26, xhigh×26, medium×26, low×26, none×26 |
| amber-cline-d4f | — (cline-pass lane; no 2606 results repo) | 34 | 31 | 3 | cline-pass/deepseek-v4-flash×31 | high×31 |
| amber-cline-g53f | — (cline-pass lane; no 2606 results repo) | 37 | 35 | 2 | cline-pass/glm-5.3-flash×29, z-ai/glm-5.3-flash×6 | high×35 |
| amber-cline-q35 | — (cline-pass lane; no 2606 results repo) | 44 | 43 | 1 | qwen/qwen3.5-9b×43 | high×43 |
| amber-cline-q38 | — (cline-pass lane; no 2606 results repo) | 44 | 43 | 1 | qwen/qwen3.8-27b×43 | high×43 |
| amber-crof-d4fv | amber-crof | 26 | 25 | 1 | deepseek-v4-flash-vision-exp×25 | high×25 |
| amber-crof-g53f | amber-crof | 30 | 29 | 1 | glm-5.3-flash×29 | high×29 |
| amber-crof-q35 | amber-crof | 31 | 30 | 1 | qwen3.5-9b×30 | high×30 |
| amber-crof-q38 | amber-crof | 27 | 26 | 1 | qwen3.8-27b×26 | high×26 |
| amber-crof | amber-crof | 29 | 26 | 3 | deepseek-v4-flash-0731×26 | high×26 |
| amber-doubao | amber-doubao | 80 | 65 | 15 | doubao-seed-evolving×35, deepseek-v4.1-flash×30 | high×65 |
| amber-ds41 | amber-deepseek | 61 | 54 | 7 | deepseek-v4.1-flash-expires-on-0910×28, deepseek-v4-flash×26 | high×54 |
| amber-gp27b | amber-goldenpotato | 30 | 27 | 3 | Qwen3.8-27B×27 | high×27 |
| amber-gpt-luna | amber-gpt | 186 | 166 | 20 | gpt-5.6-luna-900k×166 | high×50, max×38, none×26, low×26, medium×26 |
| amber-gpt-sol | amber-gpt | 33 | 32 | 1 | gpt-5.6-sol-900k×32 | high×32 |
| amber-gpt | amber-gpt | 537 | 517 | 20 | gpt-5.6-sol-900k×219, gpt-5.6-luna-900k×142, gpt-6-astra-900k×67 | high×233, medium×160, xhigh×95, max×28, low×1 |
| amber-k28 | amber-kimi (kimi-for-coding) | 33 | 32 | 1 | kimi-for-coding×32 | high×32 |
| amber-ocgo | amber-opencode | 73 | 28 | 45 | deepseek-flash×28 | high×28 |
| amber-oll2-g53f | amber-ollama | 35 | 34 | 1 | glm-5.3-flash×34 | xhigh×34 |
| amber-ollama-d41f | amber-ollama | 89 | 72 | 17 | glm-5.3-flash×44, deepseek-v4.1-flash×28 | high×72 |
| amber-ollama-d4f | amber-ollama | 44 | 42 | 2 | deepseek-v4-flash:0731×42 | high×42 |
| amber-ollama-d4p | — (deepseek-v4-pro:0813; probe, no 2606 repo) | 25 | 24 | 1 | deepseek-v4-pro:0813×24 | high×24 |
| amber-ollama-g53 | amber-ollama (W36 pre-clean-room) | 42 | 40 | 2 | glm-5.3×40 | high×40 |
| amber-ollama-g53f | amber-ollama | 186 | 154 | 32 | glm-5.3-flash×154 | high×154 |
| amber-ollama-kk3 | amber-kimi (k3) | 55 | 54 | 1 | kimi-k3×54 | high×54 |
| amber-orch-k3 | — (seat-avail001 orchestration probes) | 18 | 0 | 18 |  |  |
| amber-step5p | — (step-5-preview; no 2606 results repo) | 43 | 42 | 1 | step-5-preview×42 | high×42 |
| amber-ualpha | — (union-alpha; refuse-walled probe) | 7 | 5 | 2 | union-alpha×5 | high×5 |
| amber-wb | amber-workbuddy | 96 | 87 | 9 | hy4-preview-f×33, hy3×29, deepseek-v4.1-flash×25 | high×87 |

合计 bench 会话 = **1918**（= `hard-facts.jsonl` 行数）

## 说明

- 一个 2606 成绩仓可由多个 bench profile 贡献（例如 amber-ollama 由 g53f/d4f/d41f/oll2 四个 profile 拼成，跨 W36/W37）。
- 非 bench 会话 = smoke/probe/quota/test/orchestration 等，不属成绩卷面；已在提取器中按 `source LIKE 'amber-lib-%'` 排除。
- `—` = 有 bench transcript 但 2606 无对应公开成绩仓（cline-pass / step5p / union-alpha / 早 foreman 探针），这些 lane 的成绩真源须另找，归因表按 `no_transcript`/无成绩处理。
- amber-devin 道在外部 host 上跑，local state.db 无 transcript —— 该仓的 ✗ 案在归因表中标 `no_transcript`。

