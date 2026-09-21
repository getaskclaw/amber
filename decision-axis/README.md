# AMBER decision-axis 评测管道 (WO-DEC-001 / r1)

对「决策轴」模型(不生成文本、只对给定 state 回答封闭问题的模型, 代表 = TypeSafe Jev)的
评测管道: 金标判断题集(JSONL)进 → 多 adapter 调用 → 出分族准确率 + 校准分桶 + ECE +
阈值扫描 + 成本/延迟报告。

**r1 (WO-DEC-001-r1) 改动摘要** —— 红道双盲破检抓出 6 条 Blocker(诚信闸), 逐条修:

| # | r0 漏洞 | r1 修法 |
|---|---|---|
| 1 | 完整性用公开无钥 `sha256(adapter\|model\|qid\|answer)`, 改响应重算即放行 | 改 **HMAC-SHA256**, 签名覆盖**整条记录**(answer/ok/error_class/latency_s/cost_usd/tokens/run_nonce/dataset_sha256)。密钥经环境变量 `AMBER_DECISION_HMAC_SECRET` 或 0600 文件(路径在外, 不进仓) |
| 2 | `--score-only` 无行数/id 对账, 删错答行即抬分 | 强制对账: question_id 集合 == 数据集 id 集合 + 行数一致 + 无重复 + 内嵌 dataset 哈希匹配; 任一不符 rc≠0 |
| 3 | 401 记成 `valid_task_failure` | 401 归 `invalid_infrastructure` |
| 4 | 404 等 4xx 记成 `valid_task_failure` | 4xx 一律归 infra; 唯一例外=400/422 且响应体 error code 命中语义枚举 |
| 5 | choice 看 argmax / score 看 `round(score)` 双口径; 平票依赖 dict 键序 | 统一为**模型自报答案单一 oracle**; argmax 只作交叉校验; 平票/恰 0.5 判错(确定性); score 用**显式 half-up** `floor(x+0.5)`, 不用裸 `round()` |
| 6 | manifest 不记跑参数、数值不可重算; README d41f 数字错 | manifest 补 effort/timeout/max_tokens/max_attempts/temperature/seed/run_nonce + report/responses sha256; 新增 `--verify-run <tag>` 重算对账; README 数字按 r1 口径复算 |

## 目录

```
decision-axis/
├── README.md                  ← 本文件
├── contracts/                 ← 接口契约(派单时冻结; r1 按 WO-DEC-001-r1 修订)
│   ├── golden-jsonl.md        ← 金标 JSONL schema + 判分规则(r1 统一口径/tie/half-up)
│   └── adapter-interface.md   ← 三 adapter 传输契约 + 错误分类(r1 表) + 密钥纪律
├── signing.py                 ← HMAC 签名件(密钥加载/生成, 0600 文件在外)
├── driver.py                  ← 管道主控(读题→adapter→签名→对账→评分→报告→锁 append manifest)
├── selftest.py                ← r0 验收自测(已做 r1 兼容修正, 输出 runs/selftest-dec001.md)
├── selftest_r1.py             ← r1 验收自测, 12 条三段式, 输出 runs/selftest-dec001-r1.md
├── adapters/
│   ├── base.py                ← ResponseRecord 构造 + 整条记录 HMAC + Timer
│   ├── typesafe_native.py     ← Jev 原生 API (真跑需 TYPESAFE_API_KEY; 无 key 拒真调)
│   ├── openrouter.py          ← OpenRouter Decisions 端点 (同上)
│   └── openai_baseline.py     ← ollama-cloud OpenAI 兼容 chat (真跑; 4xx 归 infra)
├── scoring/
│   ├── validate.py            ← 金标 schema 校验器(CLI + 模块)
│   └── metrics.py             ← 统一 oracle + 分族准确率/校准分桶/ECE/阈值扫描
├── data/smoke-12.jsonl        ← 冒烟集 12 题(4 choice + 4 score + 4 noul, 12 个用途族)
├── config/prices.json         ← 目录价表; 查不到可靠公开价时保持 null(宁缺毋滥)
└── runs/
    ├── manifest.jsonl         ← 每次真跑锁 append 一行(全参数 + 双 sha256 + 分数/分类)
    ├── smoke-g53f-1/          ← g53f 真跑(r0 产物: 12/12, ECE 0.0242)
    ├── smoke-d41f-1/          ← d41f 真跑(r0 产物: 12/12, ECE 0.0108)
    ├── smoke-jev-1/           ← Jev 真跑(r0 产物: 12/12, ECE 0.0167)
    ├── empty-state-g53f/      ← 空 state 基线(r0 产物, 见下「口径变更」)
    ├── r1-smoke-jev-1/        ← r1 真 Jev 冒烟(12/12, ECE 0.0183; 验收 9)
    ├── r1-empty-state-jev/    ← r1 真 Jev 空 state 基线(5/12, ECE 0.5317; 验收 10)
    ├── timeout-sim/           ← infra 分类复现(12/12 invalid_infrastructure)
    └── */responses.jsonl + report.json + REPORT.md
```

## 用法

```bash
cd ~/2606/amber/decision-axis
set -a && source ~/.hermes/.env && set +a   # 只注入环境变量, 不落盘

# 真跑基线(冒烟):
python3 driver.py --adapter openai-compatible-baseline --model glm-5.3-flash \
    --dataset data/smoke-12.jsonl --tag smoke-g53f-1
python3 driver.py --adapter typesafe-native --model jev-latest \
    --dataset data/smoke-12.jsonl --tag smoke-jev-1

# dry-run 形状核对(Jev / OpenRouter, 零调用零 key):
python3 driver.py --adapter typesafe-native --model jev-latest --dry-run \
    --dataset data/smoke-12.jsonl --tag dryrun-typesafe
python3 driver.py --adapter openrouter --model typesafe/jev-1.13 --dry-run \
    --dataset data/smoke-12.jsonl --tag dryrun-or

# 空 state 基线 / 只重评分(零调用, 完整性重验 + 行数/id 对账):
python3 driver.py --adapter typesafe-native --model jev-latest \
    --dataset data/smoke-12.jsonl --tag empty-jev --empty-state
python3 driver.py --score-only runs/r1-smoke-jev-1/responses.jsonl \
    --adapter typesafe-native --model jev-latest \
    --dataset data/smoke-12.jsonl --tag rescore-jev

# 复核历史 run(零调用; 重算数值 + 核签名 + 对 manifest):
python3 driver.py --verify-run r1-smoke-jev-1 --dataset data/smoke-12.jsonl
python3 driver.py --verify-run smoke-g53f-1 --dataset data/smoke-12.jsonl   # r0 旧产物, 走 legacy 标注

# 自测(验收矩阵逐项):
python3 selftest.py
```

注意: `--score-only` 需 `--adapter/--model/--tag`(r0 README 的示例缺这三个, 照抄会 argparse 报错, 已修)。
`--verify-run` 只需 `--dataset`。同一 `--tag` 二次运行默认拒绝(防静默覆盖证据), 需显式 `--force`。

## 评分口径(全部自计算, 无任何锚定答案)

**r1 统一口径**(详见 `contracts/golden-jsonl.md`):
- **唯一 oracle = 模型自报答案**: choice→`answer.choice`; score→`answer.score`; noul→`answer.noul`。
  `probabilities` 的 argmax **只作交叉校验**, 不参与判对(记入报告 `oracle.n_inconsistent`)。
  r0 的双口径(choice 看 argmax / score 看 `round(score)`)已废除。
- **score 取整 = 显式 half-up** `floor(x+0.5)` 后钳制到 `[0, len(criteria)-1]`; **不用 Python
  内置 `round()`**(银行家舍入: `round(2.5)=2` 而 `round(3.5)=4`, 边界归属随奇偶变)。
- **平票/边界**: choice 概率平票时以自报 `answer.choice` 为准; 自报缺失时判错。noul 恰为
  0.5 判错。理由: 决策轴要的是「一个决定」, 平票 = 未作出唯一决定; 该规则只依赖响应里的显式
  字段, 与键序、与 gold 都无关 —— 同一份响应永远同一结论(r0 下同一组概率换键序判定翻转)。
- **置信度**: choice/score = max 概率; noul = max(p, 1-p)。
- **ECE**: 10 等宽置信度桶, `ECE = Σ (|B|/N)·|acc(B) − conf(B)|`, 空桶贡献 0。
- **阈值扫描**: t ∈ {0.00, 0.05, …, 1.00}, auto_execute_rate = conf≥t 占比 + 其中准确率。
- **分母透明**: 报告给出 `n_scored / n_expected / n_received` 与 `abstentions`(弃答数与占比)。

## 完整性口径(r1)
- 每题 `integrity = HMAC-SHA256(secret, canonical_json(整条响应记录除 integrity 外))`。
  签名覆盖 `answer / ok / error_class / error_detail / latency_s / cost_usd / tokens /
  run_nonce / dataset_sha256`。评分时全量重算, 任何字段被改 → rc≠0, 不出报告。
- 密钥(trust root): 环境变量 `AMBER_DECISION_HMAC_SECRET`, 或 0600 密钥文件
  (默认 `~/.local/state/amber-decision/hmac.key`, 首次签名运行自动生成, 目录 0700)。
  **密钥与密钥路径都不进本目录、不进报告/manifest**; manifest 只记 `signing_key_source`。
- r0 旧产物(无 `integrity_algo`, 用公开无钥公式)默认被拒; 要重算须显式
  `--allow-legacy-unkeyed`, 且报告会被标注 `integrity_assurance=legacy-unkeyed`(无密码学保证)。

## 错误分类(AMBER 规矩)
- `invalid_infrastructure`(超时/网络层/空 200/401/402/403/429/5xx/**其余 4xx**)不计入模型分,
  单列并重跑一次。401(凭据失效)、404(模型名写错) 属运维侧, r0 误记为 `valid_task_failure`, r1 已修。
- 唯一例外: 400/422 且响应体 `error.code`/`type` 命中语义枚举(content_filter 等)→ `valid_task_failure`。
- `valid_task_failure`(真实输出但校验不过)不进准确率与 ECE; 报告首部显式给出弃答数与其占比
  (`abstentions`), 防止用弃答抬分。

## 密钥纪律
adapter 只读环境变量 `TYPESAFE_API_KEY` / `OPENROUTER_API_KEY` / `OLLAMA_API_KEY`。
全目录无任何 key 值(自测逐项扫描 0 命中); dry-run 与报错信息里只出现变量名。
完整性签名密钥同规格(见上)。Jev/OpenRouter 未设 key 且非 dry-run 时 adapter 直接 RuntimeError。

## 冒烟结果

r1 真 Jev 冒烟(2026-09-19, typesafe-native, `jev-latest`, effort=low, 串行):

| run | model | adapter | scored/expected | accuracy | ECE | mean lat | 备注 |
|---|---|---|---|---|---|---|---|
| r1-smoke-jev-1 | jev-latest | typesafe-native | 12/12 | 1.0000 | 0.0183 | 0.59s | r1 修复后真跑, 12/12 |
| r1-empty-state-jev | jev-latest | typesafe-native | 12/12 | 0.4167 | 0.5317 | 0.59s | 空 state 基线, 区分度成立 |

r0 历史产物(保留, r1 口径复算值与 manifest 一致):

| run | model | scored | accuracy(r1 复算) | ECE(r1 复算) | manifest 记录 | 备注 |
|---|---|---|---|---|---|---|
| smoke-g53f-1 | glm-5.3-flash | 12 | 1.0000 | 0.0242 | 1.0 / 0.0242 | 一致 |
| smoke-d41f-1 | deepseek-v4.1-flash | 12 | 1.0000 | 0.0108 | 1.0 / 0.0108 | 一致(见下「关于 d41f 数字」) |
| smoke-jev-1 | jev-latest | 12 | 1.0000 | 0.0167 | 1.0 / 0.0167 | 一致 |
| empty-state-g53f | glm-5.3-flash | 12 | 0.3333 | 0.4317 | 0.5 / 0.2650 | **口径变更, 见下** |
| timeout-sim | glm-5.3-flash | 0 | — | — | 12/12 infra | 一致 |

### 口径变更说明(验收 12)
r1 统一 oracle(自报答案 + 平票判错)后, 个别 r0 产物的分数会变 —— 这是修 Blocker 5 的**必然**
结果, 不是「让分数好看」的调整(方向是变严, 不是变松):
- `empty-state-g53f`: r0 = 6/12 (0.5000) → r1 = 4/12 (0.3333)。两题翻转:
  - `smoke-002`(choice): 概率平票 `{destructive:0.5, reversible:0.5}`。r0 因 `destructive` 恰好
    排在 dict 首位被 argmax 取中而判对; 模型自报是 `reversible`(错)。r1 以自报为准 → 判错。
  - `smoke-011`(noul): `noul = 0.5` 恰在中点, 无态度。r0 判 `>=0.5` → true == gold 判对;
    r1 按「未作出决定」判错。
- `smoke-g53f-1` / `smoke-d41f-1` / `smoke-jev-1` 的模型自报与 argmax 完全一致, 分数不变。
- manifest 里 r0 行的 `accuracy` 是**当时 r0 口径**下的历史值, 原样保留(不改历史), 由
  `--verify-run` 复算并在有差异时点明口径; r1 新行按 r1 口径记录。

### 关于 d41f 数字(红道 Blocker 6 的原话核对)
reviewer 席 Blocker 6 称 `runs/smoke-d41f-1` 应为 `accuracy=0.9167, ECE=0.1583`(据称脚本
`probeL.py`)。逐项核对后**该数字不可复现**, 如实记录如下(不采用):
1. `smoke-d41f-1/responses.jsonl` 的 12 行, 在 argmax / 自报 / `round(score)` / half-up 四种读法下
   **逐题全对** → accuracy = 12/12 = 1.0000, ECE = 0.01083, 与 manifest 第 2 行完全一致。
2. 穷举搜索(置信度取 maxprob/stated/原始 noul × 桶数 2–20 × 翻转 0/1/2 题)没有任何组合能得出
   0.9167 / 0.1583(脚本见自测 `runs/selftest-dec001-r1.md` 验收 12 的复算段)。
3. `/tmp/red-dec001-reviewer/probeL.py` 在盘上不存在(同目录其余 probeA–probeK 均在)。
结论: r0 的 d41f 行 1.0 / 0.0108 与 r1 口径自算一致, 无需改; README 此处按可复算事实写。
(若 reviewer 席另有依据, 请附可重跑脚本路径, 我按证据再核。)


## dry-run 与官方文档逐字段对照(验收 8)

| 字段 | typesafe-native dry-run | openrouter dry-run | 官方依据(2026-09-18 抓取) |
|---|---|---|---|
| endpoint | POST https://api.typesafe.ai/v1/systemone | POST https://openrouter.ai/api/alpha/decisions | docs.typesafe.ai quickstart; openrouter.ai/docs "Submit a Decisions request" |
| auth header | `Authorization: Bearer ***` | `Authorization: Bearer ***` | 两文档一致 |
| body 字段 | `state`, `model`, `questions` | `model`, `questions`, `state` | 官方 curl 示例逐字段一致 |
| question 形状 | `type`, `instructions`, `criteria`(choice=map, score=list) | 同左 | 两文档一致 |
| 响应(真调时解析) | `answers[qid].{choice\|score\|noul, probabilities, confidence, legend}` + `usage.{input_tokens,output_tokens}` | `answers` + `id`, `model`, `provider`, `usage.{cost,input_tokens,output_tokens}` | 官方响应示例 |

r0 README 曾指向不存在的 `runs/dryrun-typesafe/`; 实际 dry-run 证据在 `runs/dryrun-a/`、
`runs/dryrun-b/`、`runs/dryrun-or/`(已修正指路)。

## 验收矩阵对照(WO-DEC-001-r1, 12 条)
逐条「复现→修复→复现失败」三段式证据: `runs/selftest-dec001-r1.md`。
1. 篡改 answer 后重算旧公式不被放行 → selftest §1(tamper + 重算公开 sha256 → rc=2)
2. score-only 删行被拒 → selftest §2(删 6 行 / 改标 infra / 改标 vtf → 全 rc=2)
3. 401 → invalid_infrastructure → selftest §3(mock 401, 12/12 infra)
4. 404 → invalid_infrastructure → selftest §4(mock 404, 12/12 infra; 另附 400 语义例外)
5. tie 确定性(同概率两种键序结果一致) → selftest §5(A/B 互换两组输出一致)
6. round 边界写进契约并显式实现 → selftest §6(契约原文 + metrics 代码 diff)
7. manifest 含 effort/timeout/max_tokens/seed + report sha256 → selftest §7(manifest 行样本)
8. `--verify-run smoke-jev-1` 重算一致 → selftest §8
9. 修复后真 Jev 冒烟 12 题重跑仍 12/12 且 ECE 可算 → selftest §9(`r1-smoke-jev-1`)
10. 修复后 --empty-state 基线仍明显低于全分 → selftest §10(`r1-empty-state-jev` 5/12)
11. 密钥/HMAC secret 零落盘 → selftest §11(全树扫描)
12. README 里 d41f/冒烟数字与契约口径自算一致 → selftest §12(对拍表)

## 断路器遵守记录
未改金标、未改 oracle 判定语义以「让分数好看」(统一口径方向为变严); 未动 case-AMBER-*、
profile 配置、state.db; 全部产物在 `~/2606/amber/decision-axis/` 内, 临时文件在 `/tmp/dec001-*`;
HMAC 密钥在 `~/.local/state/amber-decision/`(0600, 仓外)。真 Jev 调用 2 轮 × 12 题(r1 内)。
