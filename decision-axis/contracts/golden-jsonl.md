# CONTRACT golden-jsonl — 金标判断题集 schema（冻结于派单时, WO-DEC-001）

每个 JSONL 行 = 一道判断题。字段:

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | 是 | 题号, 全数据集唯一, 形如 `smoke-001` |
| `family` | string | 是 | 用途族(决策用途面), 如 `support-routing` / `safety-guardrail`。同族多题可聚合分族准确率 |
| `state` | string \| object \| array | 是 | 被评估的上下文(对应 Jev 的 `state`), 可以是纯文本或 JSON |
| `question` | object | 是 | 见下 |
| `question.id` | string | 是 | 问题在单次请求内的键(本管道一次一问, 恒为题目自身 id) |
| `question.type` | string | 是 | `choice` \| `score` \| `noul` |
| `question.instructions` | string | 是 | 完整题面。不许依赖 id 暗示答案 |
| `question.options` | object | choice 必填 | `{key: 描述}`, 选项集合, key 为 gold 的取值空间 |
| `question.criteria` | array | score 必填 | 有序等级描述, 下标即分值(0..n-1) |
| `gold` | string \| int \| bool | 是 | choice=options 的 key; score=等级下标 int; noul=布尔(yes=true) |
| `source` | string | 是 | 命题来源标记, 如 `handwritten-2026-09-18` |
| `difficulty` | string | 否 | 任意标记, 不进评分 |

## 判分规则(scoring 契约, oracle 自算)

**r1 修订(WO-DEC-001-r1 Blocker 5)**: r0 存在双口径(choice 看 `argmax(probabilities)`,
score 看 `round(answer.score)`), 同一份响应两种题型两套 oracle, 且并列/舍入边界未定义。
r1 起**统一为「模型自报答案」单一 oracle**, `probabilities` 只作交叉校验:

- **唯一 oracle = 模型自报答案**: choice 取 `answer.choice`; score 取 `answer.score`;
  noul 取 `answer.noul`。`probabilities` 的 argmax **不参与判对**, 只记入
  `report.oracle.n_inconsistent` 供人复核(自报与 argmax 打架时两处都留证据)。
- **choice**: `answer.choice == gold` 为对。置信度 = `max(probabilities 值)`。
- **score**: `round_score(answer.score) == gold` 为对, 其中 `round_score` 是**显式
  half-up 取整** `floor(x + 0.5)` 后钳制到 `[0, len(criteria)-1]`。**不用 Python 内置
  `round()`** —— 后者是银行家舍入, 会让半分界点的归属随整数奇偶变化(`round(2.5)=2` 而
  `round(3.5)=4`), 属未声明的口径。置信度 = `max(等级概率)`。
- **noul**: `(answer.noul >= 0.5) == gold` 为对。置信度 = `max(noul, 1-noul)`。

### 并列 / 边界裁决(确定性, 不依赖 dict 键序)
- **choice 概率平票**(最高概率有多个键)时, 以模型自报 `answer.choice` 为准 —— 若自报值
  存在则正常判分, 平票本身不影响结果。**自报值缺失**时才退化为「平票 = 未作出唯一决定」,
  **判错**。
- **noul 恰为 0.5**(完全无态度)判错。
- 理由: 决策轴的语义是「给出一个决定」。自报答案是模型的决定本身; 平票只说明概率分布
  没区分开, 不构成第二个决定。用「按 gold 是否在 argmax 集合」之类的规则会让判定依赖
  gold 与键序的巧合(实测 r0 下同一组概率换个键序判定翻转: `{b:.5,a:.5}` 与 `{a:.5,b:.5}`
  对同一 gold 一个判对一个判错)。统一为「自报答案 + 无自报时判错」后, 判定只取决于响应里
  的显式字段, 与键序、与 gold 都无关 —— 同一份响应永远同一结论。
- 以上全部由 scorer 从 adapter 返回的**原始响应**重算。响应文件若被改(答案/概率/延迟/成本
  等任一字段), 完整性校验必须报错, 评分结果不许落盘; 见下。

## 完整性口径(r1 修订, WO-DEC-001-r1 Blocker 1/2/6)
- r0: 题级 `integrity = sha256(adapter|model|question_id|json(answer))`。**已废除** ——
  公式公开且无密钥, 攻击者改响应后重算同一哈希即可放行(红道双盲各自复现)。
- **r1**: `integrity = HMAC-SHA256(secret, canonical_json(整条响应记录除 integrity 外))`。
  签名覆盖 `answer / ok / error_class / error_detail / latency_s / cost_usd / tokens /
  run_nonce / dataset_sha256` 等全部字段, 改任何一项都会失配。密钥(trust root)只经:
  1. 环境变量 `AMBER_DECISION_HMAC_SECRET`, 或
  2. 0600 权限密钥文件(`$AMBER_DECISION_HMAC_KEY_FILE`, 默认
     `~/.local/state/amber-decision/hmac.key`, 首次签名运行自动生成, 目录 0700)。
  密钥与密钥文件路径**都不进本仓库、不进日志/报告/manifest**。
- `runs/<tag>/responses.jsonl` 内嵌 `run_nonce` 与 `dataset_sha256`(均被签名覆盖):
  非本次运行的文件算不出有效签名, 数据集换一份也过不了对账。
- **score-only 强制对账**: responses 的 `question_id` 集合必须**等于**数据集 id 集合,
  行数必须一致, 无重复; 任一不符 → 非零退出, 不出报告。删掉答错的题以抬准确率不再可行。
- **分母透明**: 报告首部给出 `n_scored / n_expected / n_received` 与
  `abstentions.n_valid_task_failure`。`valid_task_failure` 仍按 AMBER 规矩不计入分母,
  但弃答数被显著暴露 —— 靠弃答抬分会被一眼看见。
- `--verify-run <tag>` 重算历史 run 的 `n_scored / accuracy / ece` 并与 `report.json`、
  `manifest.jsonl` 对账, 同时核签名与文件 sha256。

## 校验器硬规则(`scoring/validate.py`)
缺字段 / type 非法 / options 空 / criteria 空 / gold 不在取值空间 / id 重复 / JSON 解析失败 → 非零退出 + 指出行号与原因。

## 冒烟集约束(WO-DEC-001)
12 题, 答案显而易见; 覆盖三题型(choice/score/noul); ≥4 个用途族。
