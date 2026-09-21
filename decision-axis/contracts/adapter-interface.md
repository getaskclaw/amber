# CONTRACT adapter-interface（冻结于派单时, WO-DEC-001；r1 修订按 WO-DEC-001-r1）

> 修订记录: r1 改动 = ResponseRecord 加 `integrity_algo/run_nonce/dataset_sha256`;
> 完整性改为整条记录 HMAC(见 golden-jsonl.md); 错误分类 4xx 归 infra 并给出唯一例外;
> 密钥纪律补签名密钥。改动范围仅此三项, 其余字段与 r0 一致。

## Adapter 接口
三个 adapter 实现同一接口, driver 按 `--adapter` 切换:

```
ask(state, question, model) -> ResponseRecord
```
- `state`: 金标行的 `state` 原样传入。
- `question`: 金标行的 `question` dict。
- `model`: 模型名(如 `glm-5.3-flash` / `typesafe/jev-1.13`)。

## ResponseRecord(归一化响应, JSON 可序列化)
| 字段 | 说明 |
|---|---|
| `adapter` | adapter 名 |
| `model` | 实际请求的模型名 |
| `question_id` | 题 id |
| `family` | 用途族(透传, 便于报告) |
| `ok` | bool: 是否拿到可评分答案 |
| `answer` | 归一化答案: choice→`{choice, probabilities{key:p}, confidence}`; score→`{score, probabilities{idx:p}, confidence}`; noul→`{noul}`。不可评分时 null |
| `latency_s` | 浮点, 端到端秒数 |
| `cost_usd` | 浮点或 null(无价目时 null, 不许编造) |
| `tokens` | `{input, output}` 或 null |
| `error_class` | null \| `invalid_infrastructure` \| `valid_task_failure` \| `dry_run` |
| `error_detail` | 字符串, 可空 |
| `integrity_algo` | `hmac-sha256`(r1) 或 `sha256-legacy-unkeyed`(r0) |
| `integrity` | 题级完整性标签 = `HMAC-SHA256(secret, canonical_json(整条记录除 integrity 外))`。**r1 覆盖整条记录**, scorer 重算比对 |
| `run_nonce` | 本次运行的随机 nonce(被签名覆盖; 让跨运行的响应文件算不出有效签名) |
| `dataset_sha256` | 本次运行所用数据集文件哈希(被签名覆盖) |
| `raw_excerpt` | 原始响应截断(≤500 字符), 便于人工复核; 不得含密钥 |

## 密钥纪律
adapter 只读环境变量(`TYPESAFE_API_KEY` / `OPENROUTER_API_KEY` / `OLLAMA_API_KEY`), 默认值、报错信息、日志、manifest、报告里一律只许出现变量名, 不许出现值。
完整性签名密钥同规格: 只读环境变量 `AMBER_DECISION_HMAC_SECRET` 或 0600 密钥文件
(路径经 `AMBER_DECISION_HMAC_KEY_FILE` 覆盖, 默认 `~/.local/state/amber-decision/hmac.key`)。
`manifest.jsonl` 只记 `signing_key_source`(如 `env:AMBER_DECISION_HMAC_SECRET` / `file`),
不记值也不记路径。禁把默认 secret 硬编码进代码 —— 那等于没修。

## 错误分类(AMBER 规矩, 不许混) — r1 修订
| 情形 | 归类 |
|---|---|
| 超时、网络层失败、空响应(HTTP 200 无内容) | `invalid_infrastructure` |
| **401/403**(凭据失效/轮换: 运维侧) | `invalid_infrastructure` |
| **402/429**(账单/限流) | `invalid_infrastructure` |
| **5xx** | `invalid_infrastructure` |
| **其余 4xx**(404 模型名写错 / 405 / 409 等): 请求本身写错=**我们的**配置错误 | `invalid_infrastructure` |
| 400/422 且响应体 `error.code`/`type` 命中语义类枚举(`content_filter` / `context_length_exceeded` / `invalid_prompt` / `token_limit_exceeded` 等) | `valid_task_failure` |
| 200 有内容但 JSON 解析/校验不过(重试一次仍不行) | `valid_task_failure` |

r0 只把 402/403/429/5xx 归 infra, 401 及 404 等 4xx 走 `valid_task_failure` —— 那会把
「模型名拼错」「key 失效」记成模型回答失败(红道 Blocker 3/4)。r1 起 4xx 默认按 infra,
**唯一例外**是 400/422 且有语义 code 佐证; 判定函数 `openai_baseline.classify_http_error`,
响应体缺失/非 JSON/未知 code 一律按 infra(宁可把基础设施噪声算进 infra, 也不把运维错误
算成模型分)。

- `invalid_infrastructure`: **不计入模型准确率**, 报告单列, 并触发重跑一次。
- `valid_task_failure`: 模型给了真实输出但格式不可解析/答案不合 schema。不进准确率与 ECE;
  报告首部显式给出弃答数与其占比(`abstentions`), 防止用弃答抬分。

## 三 adapter 的传输契约(dry-run 打印 = 将发送的请求体, 字段名对照官方文档)

### 1. typesafe-native(dry-run only, 无 key 不许真调)
- `POST {TYPESAFE_BASE_URL:-https://api.typesafe.ai}/v1/systemone`
- Headers: `Authorization: Bearer $TYPESAFE_API_KEY`, `Content-Type: application/json`
- Body: `{"state": <state>, "model": <model, 默认 jev-latest>, "questions": {<qid>: {"type": ..., "instructions": ..., "criteria": <options|criteria>}}}`
- 依据: docs.typesafe.ai/introduction/quickstart.md(2026-09-18 抓取): 请求含 state+model+questions; 响应 `{model, answers{qid:{type,choice|score|noul,probabilities,confidence,legend}}, usage{input_tokens,output_tokens}}`。

### 2. openrouter(dry-run only, 本机无 OpenRouter key)
- `POST {OPENROUTER_BASE_URL:-https://openrouter.ai}/api/alpha/decisions`
- Headers: `Authorization: Bearer $OPENROUTER_API_KEY`, `Content-Type: application/json`
- Body: `{"model": <model, typesafe/jev-1.13>, "questions": {...同 typesafe 形状...}, "state": <state>}`(可选 provider/session_id/trace/user, 本管道不填)
- 依据: openrouter.ai/docs "Submit a Decisions (questions and answers) request"(2026-09-18 抓取): 路径 `/api/alpha/decisions`(alpha), 响应 `{answers, id, model, provider, usage{cost, input_tokens, output_tokens}}`。

### 3. openai-compatible-baseline(真跑)
- `POST {OLLAMA_BASE_URL:-https://ollama.com/v1}/chat/completions`
- Headers: `Authorization: Bearer ***` `Content-Type: application/json``
- Body: OpenAI chat 形状, system 提示要求只输出 JSON(`{"answer": ..., "probabilities": {...}, "confidence": ...}` 按题型), user 含 state + instructions + options/criteria。可选 `reasoning_effort`(默认 `low`, 可 --effort 改), `max_tokens` 默认 4096(思考模型留思考余量), `seed`(可选, 默认不发送并如实记 null), `max_attempts` 默认 2。全部参数写入 manifest。
- 解析失败重试一次; 再失败 → `valid_task_failure`。HTTP 错误按上表归类。
