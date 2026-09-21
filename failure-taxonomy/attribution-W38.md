# AMBER 挂案归因表 — W38（硬事实层 v0.1）

生成器: `failure-taxonomy/build_attribution.py` + `extract_hard_facts.py`（纯规则，无 LLM）。
数据源: 各 `amber-<lane>/results/*.md` 的 full matrix（挂案真源）+ bench session transcript 硬事实。
join: repo → bench profile 映射由 manifest session-id 实证（见 `lane-registry.json`）；
标签按「该 lane 该案的所有 transcript 会话」聚合，一行可多标签。
纪律: 只有公开别名；内部案号不出现在本文件。端点/工具故障（invalid causes）优先于能力归因；信号不够一律标 `unknown`，不硬塞。

## 图例

| 标签 | 含义 |
|---|---|
| `timeout` | transcript 命中超时帽（1800s/3600s/7200s 墙钟附近，或 rc=124 + 帽文本） |
| `billing_exhausted` | transcript 机器信封出现配额/计费耗尽信号 |
| `tool_failure` | 工具调用非零 exit / error（端点或候选环境故障，非直接能力判定） |
| `test_modified` | 写操作落在测试文件路径上（路径信号） |
| `completion_claimed` | 最后一条 assistant 消息含完成声明 |
| `unknown` | 有 transcript 但硬事实层没命中任何信号 |
| `no_transcript` | 找不到对应 bench session（外部 host 上跑 / 墙前未成交 / 早于记账） |

### amber-commandcode — deepseek-v4.1-flash @ CommandCode (high)

| 案别名 | face | lane列 | 硬事实标签 | 证据 (profile/session@ts) | 声明-结果一致性 |
|---|---|---|---|---|---|
| A-47eea242 | review | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-791e90ac | text | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-87c472cb | build | v4.1-flash @ CommandCode | completion_claimed, tool_failure | amber-cc (5 sess, e.g. 20260910_084953_4876e4) | ② 未跑验证/未过仍称完成（假报） |
| A-87c472cb | build | v4.1-flash @ OpenCode Go | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-87c472cb | build | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-a317e74b | verify | v4.1-flash @ CommandCode | completion_claimed, test_modified, tool_failure | amber-cc (5 sess, e.g. 20260910_085402_d2719c) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | v4.1-flash @ OpenCode Go | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-a317e74b | verify | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-be92627f | verify | v4.1-flash @ CommandCode | completion_claimed, tool_failure | amber-cc (5 sess, e.g. 20260910_090248_7b16c4) | ② 未跑验证/未过仍称完成（假报） |
| A-be92627f | verify | v4.1-flash @ OpenCode Go | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-be92627f | verify | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-cdc3d11a | review | v4.1-flash @ CommandCode | unknown | amber-cc (5 sess, e.g. 20260910_090600_367853) | — |
| A-cdc3d11a | review | v4.1-flash @ OpenCode Go | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-cdc3d11a | review | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-d511f9e8 | verify | v4.1-flash @ CommandCode | completion_claimed, tool_failure | amber-cc (5 sess, e.g. 20260910_085225_243ddd) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | v4.1-flash @ OpenCode Go | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-d511f9e8 | verify | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-d9b79b46 | ui-build | v4.1-flash @ OpenCode Go | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-d9b79b46 | ui-build | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-ea80d793 | vision | v4.1-flash @ CommandCode | unknown | amber-cc (5 sess, e.g. 20260910_090824_0412df) | — |
| A-ea80d793 | vision | v4.1-flash @ OpenCode Go | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-ea80d793 | vision | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |

### amber-crof — qwen3.8-27b / qwen3.5-9b / glm-5.3-flash / deepseek-v4-flash-0731 / deepseek-v4-flash-vision-exp @ CrofAI (high)

| 案别名 | face | lane列 | 硬事实标签 | 证据 (profile/session@ts) | 声明-结果一致性 |
|---|---|---|---|---|---|
| A-0676097b | req-drift | d4fv | tool_failure | amber-crof-d4fv (4 sess, e.g. 20260906_102528_03a50d) | — |
| A-0676097b | req-drift | q35 | completion_claimed, tool_failure | amber-crof-q35 (4 sess, e.g. 20260906_120248_54f7e5) | ② 未跑验证/未过仍称完成（假报） |
| A-13854d9d | text | q35 | unknown | amber-crof-q35 (1 sess, e.g. 20260906_095449_7a39c6) | — |
| A-1fd3683a | text | g53f | unknown | amber-crof-g53f (1 sess, e.g. 20260906_095225_010867) | — |
| A-1fd3683a | text | q35 | unknown | amber-crof-q35 (2 sess, e.g. 20260906_095225_8a224b) | — |
| A-442d4aab | build | g53f | tool_failure | amber-crof-g53f (1 sess, e.g. 20260906_100441_d73d27) | — |
| A-61f7ad01 | build | d4f | completion_claimed, tool_failure | amber-crof (2 sess, e.g. 20260906_061852_0f0b9b) | ① 跑了验证但 oracle 判挂 |
| A-641195e2 | build | q35 | completion_claimed, tool_failure | amber-crof-q35 (1 sess, e.g. 20260906_102723_caed51) | ② 未跑验证/未过仍称完成（假报） |
| A-87c472cb | build | d4f | completion_claimed, tool_failure | amber-crof (2 sess, e.g. 20260906_061215_b1c6f2) | ② 未跑验证/未过仍称完成（假报） |
| A-87c472cb | build | d4fv | completion_claimed, tool_failure | amber-crof-d4fv (1 sess, e.g. 20260906_095548_601bfe) | ② 未跑验证/未过仍称完成（假报） |
| A-87c472cb | build | g53f | tool_failure | amber-crof-g53f (1 sess, e.g. 20260906_095527_7d3d19) | — |
| A-87c472cb | build | q35 | tool_failure | amber-crof-q35 (1 sess, e.g. 20260906_102240_bf24cd) | — |
| A-87c472cb | build | q38 | tool_failure | amber-crof-q38 (1 sess, e.g. 20260906_100102_d4cae1) | — |
| A-8c909d0a | ops | glm-5.3-flash | unknown | amber-crof-g53f (1 sess, e.g. 20260908_121457_455a70) | — |
| A-984e80ee | ops | d4fv | completion_claimed, tool_failure | amber-crof-d4fv (1 sess, e.g. 20260906_102100_09d507) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | d4f | completion_claimed, test_modified, tool_failure | amber-crof (2 sess, e.g. 20260906_062310_1d34c6) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | d4fv | completion_claimed, test_modified, tool_failure | amber-crof-d4fv (1 sess, e.g. 20260906_101048_905545) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | g53f | completion_claimed, test_modified, tool_failure | amber-crof-g53f (1 sess, e.g. 20260906_100948_abbf0a) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | q35 | tool_failure | amber-crof-q35 (1 sess, e.g. 20260906_103417_b49593) | — |
| A-a5608487 | ops | q35 | tool_failure | amber-crof-q35 (1 sess, e.g. 20260906_105117_1664be) | — |
| A-a5608487 | ops | q38 | tool_failure | amber-crof-q38 (1 sess, e.g. 20260906_103458_3026e9) | — |
| A-be92627f | verify | d4f | completion_claimed, tool_failure | amber-crof (2 sess, e.g. 20260906_063819_02d5bd) | ② 未跑验证/未过仍称完成（假报） |
| A-be92627f | verify | d4fv | completion_claimed, tool_failure | amber-crof-d4fv (1 sess, e.g. 20260906_101147_48b7ae) | ② 未跑验证/未过仍称完成（假报） |
| A-be92627f | verify | g53f | tool_failure | amber-crof-g53f (2 sess, e.g. 20260906_102940_5552c6) | — |
| A-be92627f | verify | q35 | completion_claimed, tool_failure | amber-crof-q35 (1 sess, e.g. 20260906_103614_b13bde) | ② 未跑验证/未过仍称完成（假报） |
| A-be92627f | verify | q38 | completion_claimed, tool_failure | amber-crof-q38 (1 sess, e.g. 20260906_102822_f342d4) | ② 未跑验证/未过仍称完成（假报） |
| A-cdc3d11a | review | d4f | unknown | amber-crof (2 sess, e.g. 20260906_063825_e3e1df) | — |
| A-cdc3d11a | review | d4fv | unknown | amber-crof-d4fv (1 sess, e.g. 20260906_101600_f5469b) | — |
| A-cdc3d11a | review | g53f | unknown | amber-crof-g53f (1 sess, e.g. 20260906_105015_5a136d) | — |
| A-cdc3d11a | review | q35 | unknown | amber-crof-q35 (3 sess, e.g. 20260906_104730_3be4db) | — |
| A-cdc3d11a | review | q38 | unknown | amber-crof-q38 (1 sess, e.g. 20260906_103144_f98f42) | — |
| A-d511f9e8 | verify | d4f | completion_claimed, tool_failure | amber-crof (2 sess, e.g. 20260906_062016_25063c) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | d4fv | completion_claimed, tool_failure | amber-crof-d4fv (1 sess, e.g. 20260906_100537_8360a3) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | g53f | completion_claimed, tool_failure | amber-crof-g53f (2 sess, e.g. 20260906_100545_e092e8) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | q35 | completion_claimed, tool_failure | amber-crof-q35 (1 sess, e.g. 20260906_103259_9c14db) | ② 未跑验证/未过仍称完成（假报） |
| A-d511f9e8 | verify | q38 | completion_claimed, test_modified, tool_failure | amber-crof-q38 (1 sess, e.g. 20260906_101040_fb5caa) | ① 跑了验证但 oracle 判挂 |
| A-d9b79b46 | ui-build | d4f | unknown | amber-crof (3 sess, e.g. 20260906_065443_b5fcc6) | — |
| A-d9b79b46 | ui-build | d4fv | unknown | amber-crof-d4fv (2 sess, e.g. 20260906_102831_9afcb4) | — |
| A-d9b79b46 | ui-build | q35 | unknown | amber-crof-q35 (2 sess, e.g. 20260906_121158_e50b23) | — |
| A-d9b79b46 | ui-build | q38 | unknown | amber-crof-q38 (1 sess, e.g. 20260906_104452_40dc71) | — |
| A-ea80d793 | vision | d4f | unknown | amber-crof (2 sess, e.g. 20260906_064257_da834b) | — |
| A-ea80d793 | vision | d4fv | unknown | amber-crof-d4fv (1 sess, e.g. 20260906_101850_545115) | — |
| A-ea80d793 | vision | g53f | unknown | amber-crof-g53f (1 sess, e.g. 20260906_105224_eeeb33) | — |
| A-ea80d793 | vision | q35 | unknown | amber-crof-q35 (1 sess, e.g. 20260906_105106_4f7cdd) | — |
| A-ea80d793 | vision | q38 | unknown | amber-crof-q38 (1 sess, e.g. 20260906_103452_bd82bb) | — |

### amber-deepseek — deepseek-flash / deepseek-v4.1-flash-exp @ DeepSeek official (high)

| 案别名 | face | lane列 | 硬事实标签 | 证据 (profile/session@ts) | 声明-结果一致性 |
|---|---|---|---|---|---|
| A-47eea242 | review | v4.1-flash-exp（官方，W37） | completion_claimed | amber-ds41 (1 sess, e.g. 20260908_110222_86d692) | ② 未跑验证/未过仍称完成（假报） |
| A-61f7ad01 | build | d4f-0731(CrofAI,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-791e90ac | text | v4.1-flash-exp（官方，W37） | unknown | amber-ds41 (1 sess, e.g. 20260908_103637_deace2) | — |
| A-791e90ac | ? | 预览版 W37 | unknown, scope=profile | amber-ds41 (2 sess, e.g. 20260908_103637_deace2) | — |
| A-87c472cb | build | d4f-0731(CrofAI,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-87c472cb | build | d4f:0731(Ollama,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-87c472cb | build | deepseek-flash（官方 GA,W37） | completion_claimed, tool_failure, scope=profile | amber-ds41 (2 sess, e.g. 20260908_103738_a7534d) | ② 未跑验证/未过仍称完成（假报） |
| A-87c472cb | build | v4.1-flash-exp（官方，W37） | completion_claimed, tool_failure | amber-ds41 (1 sess, e.g. 20260908_103738_a7534d) | ② 未跑验证/未过仍称完成（假报） |
| A-a317e74b | verify | d4f-0731(CrofAI,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-a317e74b | verify | d4f:0731(Ollama,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-a317e74b | verify | deepseek-flash（官方 GA,W37） | completion_claimed, test_modified, tool_failure, scope=profile | amber-ds41 (3 sess, e.g. 20260908_104320_72c479) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | v4.1-flash-exp（官方，W37） | test_modified, tool_failure | amber-ds41 (2 sess, e.g. 20260908_104320_72c479) | — |
| A-a5608487 | ops | d4f:0731(Ollama,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-be92627f | verify | d4f-0731(CrofAI,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-be92627f | verify | d4f:0731(Ollama,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-be92627f | verify | deepseek-flash（官方 GA,W37） | completion_claimed, test_modified, tool_failure, scope=profile | amber-ds41 (2 sess, e.g. 20260908_105239_848fca) | ① 跑了验证但 oracle 判挂 |
| A-be92627f | verify | v4.1-flash-exp（官方，W37） | completion_claimed, test_modified, tool_failure | amber-ds41 (1 sess, e.g. 20260908_105239_848fca) | ① 跑了验证但 oracle 判挂 |
| A-cdc3d11a | review | d4f-0731(CrofAI,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-cdc3d11a | review | d4f:0731(Ollama,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-cdc3d11a | review | deepseek-flash（官方 GA,W37） | unknown, scope=profile | amber-ds41 (2 sess, e.g. 20260908_110206_c84d3b) | — |
| A-cdc3d11a | review | v4.1-flash-exp（官方，W37） | unknown | amber-ds41 (1 sess, e.g. 20260908_110206_c84d3b) | — |
| A-d511f9e8 | verify | d4f-0731(CrofAI,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-d511f9e8 | verify | d4f:0731(Ollama,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-d511f9e8 | verify | deepseek-flash（官方 GA,W37） | completion_claimed, tool_failure, scope=profile | amber-ds41 (2 sess, e.g. 20260908_104216_6e380c) | ② 未跑验证/未过仍称完成（假报） |
| A-d511f9e8 | verify | v4.1-flash-exp（官方，W37） | completion_claimed, tool_failure | amber-ds41 (1 sess, e.g. 20260908_104216_6e380c) | ② 未跑验证/未过仍称完成（假报） |
| A-d9b79b46 | ui-build | d4f-0731(CrofAI,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-d9b79b46 | ui-build | d4f:0731(Ollama,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-d9b79b46 | ui-build | deepseek-flash（官方 GA,W37） | unknown, scope=profile | amber-ds41 (2 sess, e.g. 20260908_111029_6e3708) | — |
| A-d9b79b46 | ui-build | v4.1-flash-exp（官方，W37） | unknown | amber-ds41 (1 sess, e.g. 20260908_111029_6e3708) | — |
| A-ea80d793 | vision | d4f-0731(CrofAI,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-ea80d793 | vision | d4f:0731(Ollama,W36) | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-ea80d793 | vision | deepseek-flash（官方 GA,W37） | unknown, scope=profile | amber-ds41 (3 sess, e.g. 20260908_115445_94c18f) | — |
| A-ea80d793 | vision | v4.1-flash-exp（官方，W37） | unknown | amber-ds41 (2 sess, e.g. 20260908_115445_94c18f) | — |

### amber-devin — swe-2-max/high/medium / swe-1-7-medium / glm-5-2 @ Devin (external host) (uid-suffix)

| 案别名 | face | lane列 | 硬事实标签 | 证据 (profile/session@ts) | 声明-结果一致性 |
|---|---|---|---|---|---|
| A-0676097b | req-drift | glm-5-2 | no_transcript | — | n/a |
| A-0676097b | req-drift | swe-1-7-medium | no_transcript | — | n/a |
| A-24bcf707 | ops | glm-5-2 | no_transcript | — | n/a |
| A-24bcf707 | ops | swe-1-7-medium | no_transcript | — | n/a |
| A-24bcf707 | ops | swe-2-low | no_transcript | — | n/a |
| A-442d4aab | build | glm-5-2 | no_transcript | — | n/a |
| A-442d4aab | build | swe-2-medium | no_transcript | — | n/a |
| A-47eea242 | review | swe-1-7-medium | no_transcript | — | n/a |
| A-569dbe0d | build | glm-5-2 | no_transcript | — | n/a |
| A-641195e2 | build | glm-5-2 | no_transcript | — | n/a |
| A-6fbeb363 | ops | glm-5-2 | no_transcript | — | n/a |
| A-77d62143 | build | glm-5-2 | no_transcript | — | n/a |
| A-87c472cb | build | glm-5-2 | no_transcript | — | n/a |
| A-87c472cb | build | swe-1-7-medium | no_transcript | — | n/a |
| A-87c472cb | build | swe-2-high | no_transcript | — | n/a |
| A-87c472cb | build | swe-2-low | no_transcript | — | n/a |
| A-87c472cb | build | swe-2-max | no_transcript | — | n/a |
| A-87c472cb | build | swe-2-medium | no_transcript | — | n/a |
| A-8c909d0a | ops | glm-5-2 | no_transcript | — | n/a |
| A-8d4bc770 | ops | glm-5-2 | no_transcript | — | n/a |
| A-8d4bc770 | ops | swe-1-7-medium | no_transcript | — | n/a |
| A-8d4bc770 | ops | swe-2-high | no_transcript | — | n/a |
| A-8d4bc770 | ops | swe-2-low | no_transcript | — | n/a |
| A-8d4bc770 | ops | swe-2-medium | no_transcript | — | n/a |
| A-984e80ee | ops | glm-5-2 | no_transcript | — | n/a |
| A-a317e74b | verify | glm-5-2 | no_transcript | — | n/a |
| A-a317e74b | verify | swe-1-7-medium | no_transcript | — | n/a |
| A-a317e74b | verify | swe-2-high | no_transcript | — | n/a |
| A-a317e74b | verify | swe-2-low | no_transcript | — | n/a |
| A-a317e74b | verify | swe-2-medium | no_transcript | — | n/a |
| A-a5608487 | ops | glm-5-2 | no_transcript | — | n/a |
| A-a5608487 | ops | swe-2-high | no_transcript | — | n/a |
| A-a5608487 | ops | swe-2-low | no_transcript | — | n/a |
| A-a5608487 | ops | swe-2-medium | no_transcript | — | n/a |
| A-be92627f | verify | glm-5-2 | no_transcript | — | n/a |
| A-be92627f | verify | swe-1-7-medium | no_transcript | — | n/a |
| A-be92627f | verify | swe-2-high | no_transcript | — | n/a |
| A-be92627f | verify | swe-2-low | no_transcript | — | n/a |
| A-be92627f | verify | swe-2-max | no_transcript | — | n/a |
| A-be92627f | verify | swe-2-medium | no_transcript | — | n/a |
| A-cdc3d11a | review | glm-5-2 | no_transcript | — | n/a |
| A-cdc3d11a | review | swe-2-high | no_transcript | — | n/a |
| A-cdc3d11a | review | swe-2-low | no_transcript | — | n/a |
| A-cdc3d11a | review | swe-2-max | no_transcript | — | n/a |
| A-cdc3d11a | review | swe-2-medium | no_transcript | — | n/a |
| A-d511f9e8 | verify | glm-5-2 | no_transcript | — | n/a |
| A-d511f9e8 | verify | swe-1-7-medium | no_transcript | — | n/a |
| A-d511f9e8 | verify | swe-2-high | no_transcript | — | n/a |
| A-d511f9e8 | verify | swe-2-low | no_transcript | — | n/a |
| A-d511f9e8 | verify | swe-2-max | no_transcript | — | n/a |
| A-d511f9e8 | verify | swe-2-medium | no_transcript | — | n/a |
| A-d9b79b46 | ui-build | swe-1-7-medium | no_transcript | — | n/a |
| A-ea80d793 | vision | glm-5-2 | no_transcript | — | n/a |

### amber-doubao — doubao-seed-evolving @ Volcengine Ark Agent Plan (high)

| 案别名 | face | lane列 | 硬事实标签 | 证据 (profile/session@ts) | 声明-结果一致性 |
|---|---|---|---|---|---|
| A-87c472cb | build | result | completion_claimed, tool_failure, scope=profile | amber-doubao (3 sess, e.g. 20260916_233301_648342) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | ? | 补考 | tool_failure, scope=profile | amber-doubao (7 sess, e.g. 20260917_001859_8e0970) | — |
| A-be92627f | ? | 补考 | tool_failure, scope=profile | amber-doubao (4 sess, e.g. 20260917_005923_85029d) | — |
| A-cdc3d11a | review | result | unknown, scope=profile | amber-doubao (2 sess, e.g. 20260917_015923_c3211d) | — |
| A-d511f9e8 | ? | 补考 | tool_failure, scope=profile | amber-doubao (7 sess, e.g. 20260916_235923_f0a150) | — |
| A-d9b79b46 | ui-build | result | unknown, scope=profile | amber-doubao (2 sess, e.g. 20260917_023955_26784b) | — |
| A-ea80d793 | vision | result | unknown, scope=profile | amber-doubao (2 sess, e.g. 20260917_021430_78d054) | — |

### amber-goldenpotato — Qwen3.8-27B @ goldenpotato community endpoint (high)

| 案别名 | face | lane列 | 硬事实标签 | 证据 (profile/session@ts) | 声明-结果一致性 |
|---|---|---|---|---|---|
| A-24bcf707 | ops | result | completion_claimed, scope=profile | amber-gp27b (1 sess, e.g. 20260917_205137_a226af) | ② 未跑验证/未过仍称完成（假报） |
| A-47eea242 | review | result | unknown, scope=profile | amber-gp27b (1 sess, e.g. 20260917_203413_7460d5) | — |
| A-87c472cb | build | result | tool_failure, scope=profile | amber-gp27b (1 sess, e.g. 20260917_145335_afe041) | — |
| A-a317e74b | verify | result | test_modified, tool_failure, scope=profile | amber-gp27b (1 sess, e.g. 20260917_190005_f6eeca) | — |
| A-be92627f | verify | result | completion_claimed, test_modified, tool_failure, scope=profile | amber-gp27b (1 sess, e.g. 20260917_193904_c3d300) | ① 跑了验证但 oracle 判挂 |
| A-cdc3d11a | review | result | unknown, scope=profile | amber-gp27b (1 sess, e.g. 20260917_203219_a07f92) | — |
| A-d511f9e8 | verify | result | tool_failure, scope=profile | amber-gp27b (2 sess, e.g. 20260917_170056_173a97) | — |
| A-d9b79b46 | ui-build | result | unknown, scope=profile | amber-gp27b (1 sess, e.g. 20260917_211134_ec3bf9) | — |
| A-ea80d793 | vision | result | unknown, scope=profile | amber-gp27b (1 sess, e.g. 20260917_204048_9d3589) | — |

### amber-gpt — gpt-6-astra-900k / gpt-5.6-luna-900k / gpt-5.6-sol-900k @ OpenAI codex lane (low/medium/high/xhigh/max)

| 案别名 | face | lane列 | 硬事实标签 | 证据 (profile/session@ts) | 声明-结果一致性 |
|---|---|---|---|---|---|
| A-0676097b | req-drift | high (09-12) | completion_claimed, tool_failure | amber-gpt (52 sess, e.g. 20260906_235253_0ce23f) | ② 未跑验证/未过仍称完成（假报） |
| A-13854d9d | text | low | unknown | amber-gpt-luna (1 sess, e.g. 20260912_172259_85c2d8) | — |
| A-13854d9d | text | max | unknown | amber-gpt (1 sess, e.g. 20260907_000302_f0fc2f) | — |
| A-13854d9d | text | medium | unknown | amber-gpt (6 sess, e.g. 20260907_020504_3cfa00) | — |
| A-13854d9d | text | xhigh | unknown | amber-gpt (1 sess, e.g. 20260907_000322_cb5353) | — |
| A-1fd3683a | text | max | unknown | amber-gpt (1 sess, e.g. 20260907_000218_a3b0cc) | — |
| A-1fd3683a | text | xhigh | unknown | amber-gpt (1 sess, e.g. 20260907_000217_043205) | — |
| A-24bcf707 | ops | **max (09-17)** | completion_claimed, tool_failure | amber-gpt (2 sess, e.g. 20260907_011437_52105a) | ② 未跑验证/未过仍称完成（假报） |
| A-24bcf707 | ops | W37 sol h | completion_claimed, tool_failure | amber-gpt (5 sess, e.g. 20260907_085628_f1daa0) | ② 未跑验证/未过仍称完成（假报） |
| A-24bcf707 | ops | W38 sol h | completion_claimed, tool_failure | amber-gpt (5 sess, e.g. 20260907_085628_f1daa0) | ② 未跑验证/未过仍称完成（假报） |
| A-24bcf707 | ops | high | completion_claimed, tool_failure | amber-gpt (10 sess, e.g. 20260907_074740_553fe6) | ② 未跑验证/未过仍称完成（假报） |
| A-24bcf707 | ops | low | completion_claimed, tool_failure | amber-gpt-luna (1 sess, e.g. 20260912_173342_d466f1) | ② 未跑验证/未过仍称完成（假报） |
| A-24bcf707 | ops | max | completion_claimed, tool_failure | amber-gpt (1 sess, e.g. 20260907_011437_52105a) | ② 未跑验证/未过仍称完成（假报） |
| A-24bcf707 | ops | medium | completion_claimed, tool_failure | amber-gpt (11 sess, e.g. 20260907_022300_a0fedd) | ② 未跑验证/未过仍称完成（假报） |
| A-24bcf707 | ops | sol h | completion_claimed, tool_failure | amber-gpt (5 sess, e.g. 20260907_085628_f1daa0) | ② 未跑验证/未过仍称完成（假报） |
| A-24bcf707 | ops | sol m | completion_claimed, tool_failure | amber-gpt (7 sess, e.g. 20260907_083958_87485a) | ② 未跑验证/未过仍称完成（假报） |
| A-24bcf707 | ops | xhigh | completion_claimed, tool_failure | amber-gpt (1 sess, e.g. 20260907_011112_0af3f5) | ② 未跑验证/未过仍称完成（假报） |
| A-47eea242 | review | **max (09-17)** | timeout | amber-gpt-luna/20260917_170556_f54dd0@1789666566 | — |
| A-47eea242 | review | W37 sol h | unknown | amber-gpt (2 sess, e.g. 20260907_083153_f0ed5c) | — |
| A-47eea242 | review | W38 sol h | unknown | amber-gpt (2 sess, e.g. 20260907_083153_f0ed5c) | — |
| A-47eea242 | review | high (09-12) | unknown | amber-gpt (7 sess, e.g. 20260907_023318_483595) | — |
| A-47eea242 | review | luna h | unknown | amber-gpt (3 sess, e.g. 20260907_084208_0c6c71) | — |
| A-47eea242 | review | luna m | unknown | amber-gpt (3 sess, e.g. 20260907_021910_5e6388) | — |
| A-47eea242 | review | luna xh | unknown | amber-gpt (1 sess, e.g. 20260907_170308_3e02ab) | — |
| A-47eea242 | review | max | unknown | amber-gpt (1 sess, e.g. 20260907_010257_06e1c3) | — |
| A-47eea242 | review | sol h | unknown | amber-gpt (2 sess, e.g. 20260907_083153_f0ed5c) | — |
| A-47eea242 | review | sol m | unknown | amber-gpt (2 sess, e.g. 20260907_082759_46798f) | — |
| A-47eea242 | review | xhigh | unknown | amber-gpt (1 sess, e.g. 20260907_005721_d91ab6) | — |
| A-87c472cb | build | **max (09-17)** | completion_claimed, tool_failure | amber-gpt (2 sess, e.g. 20260907_000900_372da8) | ① 跑了验证但 oracle 判挂 |
| A-87c472cb | build | W37 sol h | completion_claimed, tool_failure | amber-gpt (3 sess, e.g. 20260907_020944_17e16b) | ① 跑了验证但 oracle 判挂 |
| A-87c472cb | build | W38 sol h | completion_claimed, tool_failure | amber-gpt (3 sess, e.g. 20260907_020944_17e16b) | ① 跑了验证但 oracle 判挂 |
| A-87c472cb | build | high | completion_claimed, tool_failure | amber-gpt (8 sess, e.g. 20260907_020833_e12b67) | ① 跑了验证但 oracle 判挂 |
| A-87c472cb | build | high (09-12) | completion_claimed, tool_failure | amber-gpt (8 sess, e.g. 20260907_020833_e12b67) | ① 跑了验证但 oracle 判挂 |
| A-87c472cb | build | low | completion_claimed, tool_failure | amber-gpt-luna (1 sess, e.g. 20260912_172405_029dc6) | ② 未跑验证/未过仍称完成（假报） |
| A-87c472cb | build | luna h | completion_claimed, tool_failure | amber-gpt (3 sess, e.g. 20260907_020833_e12b67) | ① 跑了验证但 oracle 判挂 |
| A-87c472cb | build | luna m | completion_claimed, tool_failure | amber-gpt (3 sess, e.g. 20260907_020654_caef9c) | ① 跑了验证但 oracle 判挂 |
| A-87c472cb | build | luna xh | completion_claimed, tool_failure | amber-gpt (1 sess, e.g. 20260907_162126_c23968) | ② 未跑验证/未过仍称完成（假报） |
| A-87c472cb | build | max | completion_claimed, tool_failure | amber-gpt (1 sess, e.g. 20260907_000900_372da8) | ① 跑了验证但 oracle 判挂 |
| A-87c472cb | build | medium | completion_claimed, tool_failure | amber-gpt (6 sess, e.g. 20260907_020654_caef9c) | ① 跑了验证但 oracle 判挂 |
| A-87c472cb | build | sol h | completion_claimed, tool_failure | amber-gpt (3 sess, e.g. 20260907_020944_17e16b) | ① 跑了验证但 oracle 判挂 |
| A-87c472cb | build | sol m | completion_claimed, tool_failure | amber-gpt (2 sess, e.g. 20260907_020755_5b2c4f) | ① 跑了验证但 oracle 判挂 |
| A-87c472cb | build | xhigh | completion_claimed, tool_failure | amber-gpt (1 sess, e.g. 20260907_000947_5de6ad) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | **max (09-17)** | completion_claimed, test_modified, timeout, tool_failure | amber-gpt-luna/20260917_180756_1a43e8@1789672115 | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | W38 sol h | completion_claimed, test_modified, timeout, tool_failure | amber-gpt-sol/20260912_140150_13c2ce@1789223572 | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | high | completion_claimed, test_modified, timeout, tool_failure | amber-gpt-sol/20260912_140150_13c2ce@1789223572 | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | high (09-12) | completion_claimed, test_modified, timeout, tool_failure | amber-gpt-sol/20260912_140150_13c2ce@1789223572 | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | low | completion_claimed, tool_failure | amber-gpt-luna (1 sess, e.g. 20260912_172826_4f8611) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | luna h | completion_claimed, test_modified, tool_failure | amber-gpt (11 sess, e.g. 20260907_022038_a5ac18) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | luna m | completion_claimed, test_modified, tool_failure | amber-gpt (3 sess, e.g. 20260907_021129_3883fe) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | luna xh | completion_claimed, test_modified, tool_failure | amber-gpt (5 sess, e.g. 20260907_163535_b08460) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | max | completion_claimed, test_modified, tool_failure | amber-gpt (2 sess, e.g. 20260907_002013_aa46da) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | medium | completion_claimed, test_modified, tool_failure | amber-gpt (18 sess, e.g. 20260907_021129_3883fe) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | sol m | completion_claimed, test_modified, tool_failure | amber-gpt (12 sess, e.g. 20260907_021553_07ab7e) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | xhigh | completion_claimed, test_modified, tool_failure | amber-gpt (4 sess, e.g. 20260907_002406_119f74) | ① 跑了验证但 oracle 判挂 |
| A-a5608487 | ops | low | completion_claimed, tool_failure | amber-gpt-luna (1 sess, e.g. 20260912_173227_f721e6) | ② 未跑验证/未过仍称完成（假报） |
| A-be92627f | verify | **max (09-17)** | completion_claimed, tool_failure | amber-gpt (2 sess, e.g. 20260907_004753_75ff78) | ① 跑了验证但 oracle 判挂 |
| A-be92627f | verify | W37 sol h | completion_claimed, test_modified, tool_failure | amber-gpt (19 sess, e.g. 20260907_023534_ce1d97) | ① 跑了验证但 oracle 判挂 |
| A-be92627f | verify | W38 sol h | completion_claimed, test_modified, tool_failure | amber-gpt (19 sess, e.g. 20260907_023534_ce1d97) | ① 跑了验证但 oracle 判挂 |
| A-be92627f | verify | high | completion_claimed, test_modified, tool_failure | amber-gpt (28 sess, e.g. 20260907_022450_b0c9cc) | ① 跑了验证但 oracle 判挂 |
| A-be92627f | verify | high (09-12) | completion_claimed, test_modified, tool_failure | amber-gpt (28 sess, e.g. 20260907_022450_b0c9cc) | ① 跑了验证但 oracle 判挂 |
| A-be92627f | verify | low | tool_failure | amber-gpt-luna (1 sess, e.g. 20260912_173010_e4fda0) | — |
| A-be92627f | verify | luna h | completion_claimed, test_modified, tool_failure | amber-gpt (7 sess, e.g. 20260907_022750_85df69) | ① 跑了验证但 oracle 判挂 |
| A-be92627f | verify | luna m | completion_claimed, tool_failure | amber-gpt (3 sess, e.g. 20260907_021551_52d3c3) | ① 跑了验证但 oracle 判挂 |
| A-be92627f | verify | luna xh | completion_claimed, tool_failure | amber-gpt (1 sess, e.g. 20260907_164140_7d8642) | ② 未跑验证/未过仍称完成（假报） |
| A-be92627f | verify | max | completion_claimed, tool_failure | amber-gpt (1 sess, e.g. 20260907_004753_75ff78) | ① 跑了验证但 oracle 判挂 |
| A-be92627f | verify | medium | completion_claimed, test_modified, tool_failure | amber-gpt (8 sess, e.g. 20260907_021551_52d3c3) | ① 跑了验证但 oracle 判挂 |
| A-be92627f | verify | sol h | completion_claimed, test_modified, tool_failure | amber-gpt (19 sess, e.g. 20260907_023534_ce1d97) | ① 跑了验证但 oracle 判挂 |
| A-be92627f | verify | sol m | completion_claimed, test_modified, tool_failure | amber-gpt (4 sess, e.g. 20260907_023533_3dd941) | ① 跑了验证但 oracle 判挂 |
| A-be92627f | verify | xhigh | completion_claimed, test_modified, tool_failure | amber-gpt (1 sess, e.g. 20260907_004411_ba881e) | ① 跑了验证但 oracle 判挂 |
| A-cdc3d11a | review | **max (09-17)** | unknown | amber-gpt (2 sess, e.g. 20260907_010058_51e716) | — |
| A-cdc3d11a | review | W37 sol h | unknown | amber-gpt (3 sess, e.g. 20260907_023539_d9a3f7) | — |
| A-cdc3d11a | review | W38 sol h | unknown | amber-gpt (3 sess, e.g. 20260907_023539_d9a3f7) | — |
| A-cdc3d11a | review | high | unknown | amber-gpt (9 sess, e.g. 20260907_023255_154ae9) | — |
| A-cdc3d11a | review | high (09-12) | unknown | amber-gpt (9 sess, e.g. 20260907_023255_154ae9) | — |
| A-cdc3d11a | review | low | unknown | amber-gpt-luna (1 sess, e.g. 20260912_173100_323828) | — |
| A-cdc3d11a | review | luna h | unknown | amber-gpt (3 sess, e.g. 20260907_083726_3f1260) | — |
| A-cdc3d11a | review | luna m | unknown | amber-gpt (3 sess, e.g. 20260907_021818_646189) | — |
| A-cdc3d11a | review | luna xh | unknown | amber-gpt (1 sess, e.g. 20260907_165826_cb4de1) | — |
| A-cdc3d11a | review | max | unknown | amber-gpt (1 sess, e.g. 20260907_010058_51e716) | — |
| A-cdc3d11a | review | medium | unknown | amber-gpt (7 sess, e.g. 20260907_021818_646189) | — |
| A-cdc3d11a | review | sol h | unknown | amber-gpt (3 sess, e.g. 20260907_023539_d9a3f7) | — |
| A-cdc3d11a | review | sol m | unknown | amber-gpt (3 sess, e.g. 20260907_023539_f27b5d) | — |
| A-cdc3d11a | review | xhigh | unknown | amber-gpt (1 sess, e.g. 20260907_005328_1c352c) | — |
| A-d511f9e8 | verify | **max (09-17)** | completion_claimed, test_modified, tool_failure | amber-gpt (7 sess, e.g. 20260907_002012_2a9795) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | W38 sol h | completion_claimed, test_modified, timeout, tool_failure | amber-gpt-sol/20260912_140150_5dacba@1789223572 | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | high | completion_claimed, test_modified, timeout, tool_failure | amber-gpt-sol/20260912_140150_5dacba@1789223572 | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | high (09-12) | completion_claimed, test_modified, timeout, tool_failure | amber-gpt-sol/20260912_140150_5dacba@1789223572 | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | low | completion_claimed, tool_failure | amber-gpt-luna (1 sess, e.g. 20260912_172749_f086d6) | ② 未跑验证/未过仍称完成（假报） |
| A-d511f9e8 | verify | luna h | completion_claimed, test_modified, tool_failure | amber-gpt (3 sess, e.g. 20260907_021608_2a1df2) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | luna m | completion_claimed, tool_failure | amber-gpt (3 sess, e.g. 20260907_021053_edd343) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | luna xh | completion_claimed, test_modified, tool_failure | amber-gpt (3 sess, e.g. 20260907_163021_dd1777) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | max | completion_claimed, test_modified, tool_failure | amber-gpt (3 sess, e.g. 20260907_002012_2a9795) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | medium | completion_claimed, test_modified, tool_failure | amber-gpt (16 sess, e.g. 20260907_021053_edd343) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | sol m | completion_claimed, test_modified, tool_failure | amber-gpt (11 sess, e.g. 20260907_021448_d65ea0) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | xhigh | completion_claimed, test_modified, tool_failure | amber-gpt (1 sess, e.g. 20260907_002105_8be3bd) | ① 跑了验证但 oracle 判挂 |
| A-d9b79b46 | ui-build | W37 sol h | completion_claimed | amber-gpt (2 sess, e.g. 20260907_092806_a57b51) | ② 未跑验证/未过仍称完成（假报） |
| A-d9b79b46 | ui-build | high (09-12) | completion_claimed | amber-gpt (8 sess, e.g. 20260906_235653_6c3366) | ② 未跑验证/未过仍称完成（假报） |
| A-d9b79b46 | ui-build | luna h | unknown | amber-gpt (3 sess, e.g. 20260907_085948_82a274) | — |
| A-d9b79b46 | ui-build | luna m | unknown | amber-gpt (3 sess, e.g. 20260907_022720_4883dd) | — |
| A-d9b79b46 | ui-build | luna xh | unknown | amber-gpt (1 sess, e.g. 20260907_173604_5c96bf) | — |
| A-d9b79b46 | ui-build | max | unknown | amber-gpt (2 sess, e.g. 20260907_013003_c0214d) | — |
| A-d9b79b46 | ui-build | sol h | completion_claimed | amber-gpt (2 sess, e.g. 20260907_092806_a57b51) | ② 未跑验证/未过仍称完成（假报） |
| A-d9b79b46 | ui-build | sol m | unknown | amber-gpt (2 sess, e.g. 20260907_085250_8bc7d3) | — |
| A-d9b79b46 | ui-build | xhigh | unknown | amber-gpt (2 sess, e.g. 20260907_012324_1a3814) | — |
| A-ea80d793 | vision | W37 sol h | unknown | amber-gpt (2 sess, e.g. 20260907_083634_d01d8f) | — |
| A-ea80d793 | vision | W38 sol h | unknown | amber-gpt (2 sess, e.g. 20260907_083634_d01d8f) | — |
| A-ea80d793 | vision | high | unknown | amber-gpt (3 sess, e.g. 20260906_235253_613497) | — |
| A-ea80d793 | vision | low | unknown | amber-gpt-luna (1 sess, e.g. 20260912_173159_4a9a3d) | — |
| A-ea80d793 | vision | luna h | unknown | amber-gpt (3 sess, e.g. 20260907_084641_092c23) | — |
| A-ea80d793 | vision | luna m | unknown | amber-gpt (3 sess, e.g. 20260907_022006_392522) | — |
| A-ea80d793 | vision | luna xh | unknown | amber-gpt (1 sess, e.g. 20260907_170749_1e30c6) | — |
| A-ea80d793 | vision | max | unknown | amber-gpt (1 sess, e.g. 20260907_010539_9fc38b) | — |
| A-ea80d793 | vision | sol h | unknown | amber-gpt (2 sess, e.g. 20260907_083634_d01d8f) | — |
| A-ea80d793 | vision | sol m | unknown | amber-gpt (2 sess, e.g. 20260907_083045_f5c250) | — |
| A-ea80d793 | vision | xhigh | unknown | amber-gpt (1 sess, e.g. 20260907_005907_e9a99c) | — |

### amber-kimi — k3 / kimi-for-coding @ Kimi coding endpoint (high)

| 案别名 | face | lane列 | 硬事实标签 | 证据 (profile/session@ts) | 声明-结果一致性 |
|---|---|---|---|---|---|
| A-24bcf707 | ops | K2.8（kimi-for-coding） | completion_claimed, tool_failure | amber-k28 (1 sess, e.g. 20260917_132609_ced1a9) | ② 未跑验证/未过仍称完成（假报） |
| A-87c472cb | build | K2.8（kimi-for-coding） | tool_failure | amber-k28 (1 sess, e.g. 20260917_122226_0e13f2) | — |
| A-87c472cb | build | k3 | tool_failure | amber-ollama-kk3 (1 sess, e.g. 20260906_230849_c78d59) | — |
| A-87c472cb | build | k3 (kimi-coding) | tool_failure | amber-ollama-kk3 (1 sess, e.g. 20260906_230849_c78d59) | — |
| A-87c472cb | build | k3-low | tool_failure | amber-ollama-kk3 (1 sess, e.g. 20260906_230849_c78d59) | — |
| A-a317e74b | verify | K2.8（kimi-for-coding） | completion_claimed, test_modified, tool_failure | amber-k28 (1 sess, e.g. 20260917_123932_dcc77a) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | k3 | tool_failure | amber-ollama-kk3 (3 sess, e.g. 20260906_231449_9b9955) | — |
| A-a317e74b | verify | k3 (kimi-coding) | tool_failure | amber-ollama-kk3 (3 sess, e.g. 20260906_231449_9b9955) | — |
| A-a317e74b | verify | k3-low | tool_failure | amber-ollama-kk3 (3 sess, e.g. 20260906_231449_9b9955) | — |
| A-a5608487 | ops | K2.8（kimi-for-coding） | tool_failure | amber-k28 (1 sess, e.g. 20260917_132312_21cc26) | — |
| A-a5608487 | ops | k3-low | unknown | amber-ollama-kk3 (3 sess, e.g. 20260906_232257_909403) | — |
| A-be92627f | verify | K2.8（kimi-for-coding） | completion_claimed, test_modified, tool_failure | amber-k28 (1 sess, e.g. 20260917_130048_5ced0c) | ① 跑了验证但 oracle 判挂 |
| A-be92627f | verify | k3 | unknown | amber-ollama-kk3 (3 sess, e.g. 20260906_232242_62f49a) | — |
| A-be92627f | verify | k3 (kimi-coding) | unknown | amber-ollama-kk3 (3 sess, e.g. 20260906_232242_62f49a) | — |
| A-be92627f | verify | k3-low | unknown | amber-ollama-kk3 (3 sess, e.g. 20260906_232242_62f49a) | — |
| A-cdc3d11a | review | K2.8（kimi-for-coding） | unknown | amber-k28 (1 sess, e.g. 20260917_131551_1e83f5) | — |
| A-cdc3d11a | review | k3 | unknown | amber-ollama-kk3 (3 sess, e.g. 20260906_232248_bc84d0) | — |
| A-cdc3d11a | review | k3 (kimi-coding) | unknown | amber-ollama-kk3 (3 sess, e.g. 20260906_232248_bc84d0) | — |
| A-cdc3d11a | review | k3-low | unknown | amber-ollama-kk3 (3 sess, e.g. 20260906_232248_bc84d0) | — |
| A-d511f9e8 | verify | K2.8（kimi-for-coding） | completion_claimed, test_modified, tool_failure | amber-k28 (2 sess, e.g. 20260917_123116_d46945) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | k3 | completion_claimed, tool_failure | amber-ollama-kk3 (3 sess, e.g. 20260906_231446_841323) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | k3 (kimi-coding) | completion_claimed, tool_failure | amber-ollama-kk3 (3 sess, e.g. 20260906_231446_841323) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | k3-low | completion_claimed, tool_failure | amber-ollama-kk3 (3 sess, e.g. 20260906_231446_841323) | ① 跑了验证但 oracle 判挂 |
| A-d9b79b46 | ui-build | K2.8（kimi-for-coding） | unknown | amber-k28 (1 sess, e.g. 20260917_133325_b11007) | — |
| A-d9b79b46 | ui-build | k3 | unknown | amber-ollama-kk3 (3 sess, e.g. 20260906_232321_d53458) | — |
| A-d9b79b46 | ui-build | k3 (kimi-coding) | unknown | amber-ollama-kk3 (3 sess, e.g. 20260906_232321_d53458) | — |
| A-d9b79b46 | ui-build | k3-low | unknown | amber-ollama-kk3 (3 sess, e.g. 20260906_232321_d53458) | — |
| A-ea80d793 | vision | K2.8（kimi-for-coding） | unknown | amber-k28 (1 sess, e.g. 20260917_131741_2d4db6) | — |
| A-ea80d793 | vision | k3-low | unknown | amber-ollama-kk3 (3 sess, e.g. 20260906_232253_d97294) | — |

### amber-ollama — glm-5.3-flash / deepseek-v4-flash:0731 @ Ollama Cloud (high)

| 案别名 | face | lane列 | 硬事实标签 | 证据 (profile/session@ts) | 声明-结果一致性 |
|---|---|---|---|---|---|
| A-87c472cb | build | d4f | completion_claimed, test_modified, tool_failure | amber-ollama-d4f (2 sess, e.g. 20260906_140744_81a513) | ① 跑了验证但 oracle 判挂 |
| A-87c472cb | build | deepseek-v4.1-flash | completion_claimed, tool_failure | amber-ollama-d41f (1 sess, e.g. 20260911_011622_48f0cd) | ② 未跑验证/未过仍称完成（假报） |
| A-87c472cb | build | g53f | completion_claimed, test_modified, tool_failure | amber-ollama-g53f (17 sess, e.g. 20260906_140756_7c933a) | ① 跑了验证但 oracle 判挂 |
| A-87c472cb | build | glm-5.3-flash | completion_claimed, test_modified, tool_failure | amber-ollama-g53f (18 sess, e.g. 20260906_140756_7c933a) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | d4f | completion_claimed, test_modified, timeout, tool_failure | amber-ollama-d4f/20260906_142940_d06003@1788706788 | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | deepseek-v4.1-flash | completion_claimed, test_modified, tool_failure | amber-ollama-d41f (2 sess, e.g. 20260911_013957_8d319d) | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | g53f | completion_claimed, test_modified, timeout, tool_failure | amber-ollama-g53f/20260915_114653_3402e2@1789474655 | ① 跑了验证但 oracle 判挂 |
| A-a317e74b | verify | glm-5.3-flash | completion_claimed, test_modified, timeout, tool_failure | amber-ollama-g53f/20260915_114653_3402e2@1789474655 | ① 跑了验证但 oracle 判挂 |
| A-a5608487 | ops | d4f | tool_failure | amber-ollama-d4f (1 sess, e.g. 20260906_155719_bbc6e5) | — |
| A-be92627f | verify | d4f | completion_claimed, tool_failure | amber-ollama-d4f (2 sess, e.g. 20260906_150555_c54c44) | ② 未跑验证/未过仍称完成（假报） |
| A-be92627f | verify | deepseek-v4.1-flash | tool_failure | amber-ollama-d41f (2 sess, e.g. 20260911_020927_f66a13) | — |
| A-be92627f | verify | g53f | completion_claimed, tool_failure | amber-ollama-g53f (19 sess, e.g. 20260906_142516_35e9bb) | ① 跑了验证但 oracle 判挂 |
| A-be92627f | verify | glm-5.3-flash | completion_claimed, tool_failure | amber-ollama-g53f (20 sess, e.g. 20260906_142516_35e9bb) | ① 跑了验证但 oracle 判挂 |
| A-cdc3d11a | review | d4f | unknown | amber-ollama-d4f (1 sess, e.g. 20260906_155011_9c1a93) | — |
| A-cdc3d11a | review | deepseek-v4.1-flash | unknown | amber-ollama-d41f (1 sess, e.g. 20260911_031934_4dd99a) | — |
| A-cdc3d11a | review | g53f | unknown | amber-ollama-g53f (16 sess, e.g. 20260906_150247_3af7a1) | — |
| A-cdc3d11a | review | glm-5.3-flash | unknown | amber-ollama-g53f (17 sess, e.g. 20260906_150247_3af7a1) | — |
| A-d511f9e8 | verify | d4f | completion_claimed, test_modified, tool_failure | amber-ollama-d4f (3 sess, e.g. 20260906_141821_0a0637) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | deepseek-v4.1-flash | completion_claimed, tool_failure | amber-ollama-d41f (1 sess, e.g. 20260911_012604_a8f6aa) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | g53f | completion_claimed, test_modified, tool_failure | amber-ollama-g53f (22 sess, e.g. 20260906_141514_d3821f) | ① 跑了验证但 oracle 判挂 |
| A-d511f9e8 | verify | glm-5.3-flash | completion_claimed, test_modified, tool_failure | amber-ollama-g53f (23 sess, e.g. 20260906_141514_d3821f) | ① 跑了验证但 oracle 判挂 |
| A-d9b79b46 | ui-build | d4f | unknown | amber-ollama-d4f (1 sess, e.g. 20260906_160556_8727f6) | — |
| A-d9b79b46 | ui-build | g53f | unknown | amber-ollama-g53f (35 sess, e.g. 20260906_151958_06a385) | — |
| A-d9b79b46 | ui-build | glm-5.3-flash | unknown | amber-ollama-g53f (36 sess, e.g. 20260906_151958_06a385) | — |
| A-ea80d793 | vision | d4f | unknown | amber-ollama-d4f (1 sess, e.g. 20260906_155710_29e113) | — |
| A-ea80d793 | vision | deepseek-v4.1-flash | unknown | amber-ollama-d41f (1 sess, e.g. 20260911_032643_b235d5) | — |
| A-ea80d793 | vision | glm-5.3-flash | unknown | amber-ollama-g53f (24 sess, e.g. 20260906_150426_1710cb) | — |

### amber-opencode — deepseek-flash @ OpenCode Go (high)

| 案别名 | face | lane列 | 硬事实标签 | 证据 (profile/session@ts) | 声明-结果一致性 |
|---|---|---|---|---|---|
| A-47eea242 | review | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-791e90ac | text | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-87c472cb | build | v4.1-flash @ CommandCode | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-87c472cb | build | v4.1-flash @ OpenCode Go | completion_claimed, tool_failure, scope=profile | amber-ocgo (1 sess, e.g. 20260910_085017_b00196) | ② 未跑验证/未过仍称完成（假报） |
| A-87c472cb | build | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-a317e74b | verify | v4.1-flash @ CommandCode | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-a317e74b | verify | v4.1-flash @ OpenCode Go | test_modified, tool_failure, scope=profile | amber-ocgo (3 sess, e.g. 20260910_085454_8cabdc) | — |
| A-a317e74b | verify | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-be92627f | verify | v4.1-flash @ CommandCode | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-be92627f | verify | v4.1-flash @ OpenCode Go | completion_claimed, tool_failure, scope=profile | amber-ocgo (1 sess, e.g. 20260910_090531_a822fe) | ② 未跑验证/未过仍称完成（假报） |
| A-be92627f | verify | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-cdc3d11a | review | v4.1-flash @ CommandCode | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-cdc3d11a | review | v4.1-flash @ OpenCode Go | unknown, scope=profile | amber-ocgo (1 sess, e.g. 20260910_091955_5d8797) | — |
| A-cdc3d11a | review | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-d511f9e8 | verify | v4.1-flash @ CommandCode | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-d511f9e8 | verify | v4.1-flash @ OpenCode Go | completion_claimed, tool_failure, scope=profile | amber-ocgo (1 sess, e.g. 20260910_085302_64e3d2) | ② 未跑验证/未过仍称完成（假报） |
| A-d511f9e8 | verify | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-d9b79b46 | ui-build | v4.1-flash @ OpenCode Go | unknown, scope=profile | amber-ocgo (1 sess, e.g. 20260910_093609_c57383) | — |
| A-d9b79b46 | ui-build | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-ea80d793 | vision | v4.1-flash @ CommandCode | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-ea80d793 | vision | v4.1-flash @ OpenCode Go | unknown, scope=profile | amber-ocgo (1 sess, e.g. 20260910_092248_b8db75) | — |
| A-ea80d793 | vision | v4.1-flash-exp 预览 @ 官方 | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |

### amber-workbuddy — hy4-preview-f / deepseek-v4.1-flash / hy3 @ WorkBuddy ACP (high)

| 案别名 | face | lane列 | 硬事实标签 | 证据 (profile/session@ts) | 声明-结果一致性 |
|---|---|---|---|---|---|
| A-569dbe0d | build | deepseek-v4.1-flash (wb) | completion_claimed | amber-wb (3 sess, e.g. 20260912_110252_df596c) | ② 未跑验证/未过仍称完成（假报） |
| A-61f7ad01 | build | deepseek-v4.1-flash (wb) | completion_claimed | amber-wb (4 sess, e.g. 20260912_110901_b1e499) | ② 未跑验证/未过仍称完成（假报） |
| A-87c472cb | build | deepseek-flash（官方 GA，对照） | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-87c472cb | build | deepseek-v4.1-flash (wb) | completion_claimed | amber-wb (4 sess, e.g. 20260912_110310_66e385) | ② 未跑验证/未过仍称完成（假报） |
| A-87c472cb | build | hy4-preview-f (wb) | unknown | amber-wb (1 sess, e.g. 20260912_121850_2980ab) | — |
| A-a317e74b | verify | deepseek-flash（官方 GA，对照） | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-a317e74b | verify | deepseek-v4.1-flash (wb) | completion_claimed | amber-wb (5 sess, e.g. 20260912_111401_ca1d6b) | ② 未跑验证/未过仍称完成（假报） |
| A-a317e74b | verify | hy4-preview-f (wb) | completion_claimed | amber-wb (3 sess, e.g. 20260913_024040_b2f5fc) | ② 未跑验证/未过仍称完成（假报） |
| A-be92627f | verify | deepseek-flash（官方 GA，对照） | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-be92627f | verify | hy4-preview-f (wb) | completion_claimed | amber-wb (1 sess, e.g. 20260913_025721_77314c) | ② 未跑验证/未过仍称完成（假报） |
| A-cdc3d11a | review | deepseek-flash（官方 GA，对照） | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-cdc3d11a | review | deepseek-v4.1-flash (wb) | completion_claimed | amber-wb (3 sess, e.g. 20260912_112001_0b9151) | ② 未跑验证/未过仍称完成（假报） |
| A-cdc3d11a | review | hy4-preview-f (wb) | completion_claimed | amber-wb (1 sess, e.g. 20260913_031505_7cf5e6) | ② 未跑验证/未过仍称完成（假报） |
| A-d511f9e8 | verify | deepseek-flash（官方 GA，对照） | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-d511f9e8 | verify | deepseek-v4.1-flash (wb) | completion_claimed | amber-wb (3 sess, e.g. 20260912_111128_c399b3) | ② 未跑验证/未过仍称完成（假报） |
| A-d511f9e8 | verify | hy4-preview-f (wb) | completion_claimed | amber-wb (1 sess, e.g. 20260913_023703_c6e8f2) | ② 未跑验证/未过仍称完成（假报） |
| A-d9b79b46 | ui-build | deepseek-flash（官方 GA，对照） | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-d9b79b46 | ui-build | deepseek-v4.1-flash (wb) | completion_claimed | amber-wb (3 sess, e.g. 20260912_113431_3c7176) | ② 未跑验证/未过仍称完成（假报） |
| A-ea80d793 | vision | deepseek-flash（官方 GA，对照） | ref_column | — (跨厂商引用列，无本地 transcript) | n/a |
| A-ea80d793 | vision | deepseek-v4.1-flash (wb) | no_transcript | — | n/a |
| A-ea80d793 | vision | hy4-preview-f (wb) | no_transcript | — | n/a |

## 汇总

- 挂案行数（去重后，按 lane 列计）: **383**
- 硬事实标签计数: `tool_failure`=147, `completion_claimed`=135, `unknown`=110, `test_modified`=55, `no_transcript`=55, `ref_column`=54, `scope=profile`=31, `timeout`=11
- 声明-结果不一致: ① 跑了验证但 oracle 判挂 = **82**；② 未跑/未过仍称完成（假报）= **53**（合计声称完成且 published 判挂 = 135）

标签为会话级硬事实；一个挂案行可带多标签。`timeout`/`billing_exhausted` 属 invalid causes，优先于能力归因。

## 端点故障 vs 能力答错（先分，invalid causes 优先）

口径：本表主体来自 transcript 硬事实；下面这节来自各 `runs-*/manifest.jsonl` 的 run 终态
（scoring 真源，含无 session 记录的考墙卷）。`invalid_infrastructure` / `driver_exception` 属端点/工具故障，
不得计入模型能力。

| lane | valid_task_success | valid_task_failure | invalid_infrastructure | driver_exception | 挂案(invalid/failure 分列) |
|---|---:|---:|---:|---:|---|
| amber-commandcode | 94 | 37 | 0 | 0 | 端点故障 0 / 能力判挂 37 |
| amber-crof | 77 | 51 | 2 | 0 | 端点故障 2 / 能力判挂 51 |
| amber-deepseek | 36 | 17 | 0 | 0 | 端点故障 0 / 能力判挂 17 |
| amber-devin | 0 | 0 | 0 | 0 | 端点故障 0 / 能力判挂 0 |
| amber-doubao | 21 | 30 | 6 | 0 | 端点故障 6 / 能力判挂 30 |
| amber-goldenpotato | 17 | 9 | 0 | 0 | 端点故障 0 / 能力判挂 9 |
| amber-gpt | 404 | 200 | 7 | 0 | 端点故障 7 / 能力判挂 200 |
| amber-kimi | 25 | 25 | 15 | 0 | 端点故障 15 / 能力判挂 25 |
| amber-ollama | 138 | 119 | 20 | 0 | 端点故障 20 / 能力判挂 119 |
| amber-opencode | 19 | 7 | 1 | 0 | 端点故障 1 / 能力判挂 7 |
| amber-workbuddy | 47 | 28 | 4 | 1 | 端点故障 5 / 能力判挂 28 |

全库合计：valid_success=1200 valid_failure=704 invalid_infrastructure=156 driver_exception=1

invalid_infrastructure 明细（考墙/基建卷，按 lane）：

- amber-crof: `harness_timeout`=2
- amber-doubao: `harness_timeout`=4, `other`=2
- amber-gpt: `other`=4, `harness_timeout`=3
- amber-kimi: `other`=15
- amber-ollama: `other`=12, `harness_timeout`=8
- amber-opencode: `harness_timeout`=1
- amber-workbuddy: `harness_timeout`=2, `other`=2

