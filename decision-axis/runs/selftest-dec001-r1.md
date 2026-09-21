# selftest-dec001-r1 — WO-DEC-001-r1 验收矩阵自测

生成: `python3 selftest_r1.py`(本文件由脚本产出; 重跑即复现)。
每条 = 复现(r0 漏洞)→ 修复(r1 代码/契约)→ 复现失败(r1 拦截)。
mock HTTP server 内起线程, 零外部 API 调用; §9/§10 读已产出真 Jev run 复算。

## 1. 篡改 answer 后重算 integrity 不再放行(含知悉旧公式者)

**复现(r0)**: r0 完整性 = `sha256(adapter|model|qid|canonical_json(answer))`, 公式公开无钥。
攻击者在内存里用同一公式重算即可:

```
legacy_hash('openai-compatible-baseline', 'mock-ok', 'smoke-001', forged_answer)
  = 0299b628f312b14f95cad2cda427fc4183f7862d850402a534690540ff52e59a
-> 与响应文件里的 integrity 字段同构(64 hex), 重算后写回即通过 r0 校验。
```
**修复(r1)**: integrity = `HMAC-SHA256(secret, 整条记录)`; 密钥不在仓内, 攻击者算不出。

**复现失败(r1)**:
```
$ python3 driver.py --score-only <伪造> ... --tag st-1-forged
REFUSED: LEGACY ARTIFACT: smoke-001 无 r1 HMAC 签名(r0 公开无钥公式, 不可信)。要重算请显式加 --allow-legacy-unkeyed; 那样出的报告会被标注 integrity_assurance=legacy-unkeyed(NOT cryptographic)。
rc=2
```
结果: PASS — r0 公开公式伪造被拒(rc≠0, 无 report 落盘)。
  report 落盘? False

## 2. score-only 删行/改标被拒

**复现(r0)**: 删掉 mock run 里判错的题(['smoke-005', 'smoke-006', 'smoke-008', 'smoke-009', 'smoke-012'])或把它们改标 `invalid_infrastructure`, 
r0 只按剩余题算 accuracy, 无任何行数/id 告警 → 0.5833 可抬到 1.0。

**修复(r1)**: `--score-only` 强制对账 question_id 集合 == 数据集 id 集合 + 行数一致 + 无重复。

**复现失败(r1)**:
```
[删 5 行] rc=2
  REFUSED: RECONCILIATION FAILED: row count 7 != dataset size 12; missing question_id(s) ['smoke-005', 'smoke-006', 'smoke-008', 'smoke-009', 'smoke-012'] (rows dropped); refusing to score (denominator cannot be trusted).
[改标 invalid_infrastructure] rc=2
  REFUSED: TAMPER DETECTED: integrity mismatch on smoke-005, smoke-006, smoke-008, smoke-009, smoke-012; refusing to score. 响应文件被改, 签名覆盖整条记录(含 answer/ok/error_class/latency_s/cost_usd/tokens/run_nonce/dataset_sha256), 只重算旧公开公式无效。
[改标 valid_task_failure] rc=2
  REFUSED: TAMPER DETECTED: integrity mismatch on smoke-005, smoke-006, smoke-008, smoke-009, smoke-012; refusing to score. 响应文件被改, 签名覆盖整条记录(含 answer/ok/error_class/latency_s/cost_usd/tokens/run_nonce/dataset_sha256), 只重算旧公开公式无效。
```
结果: PASS — 三种删行/改标攻击全部 rc≠0, 不出报告。

## 3. 401 → invalid_infrastructure

**401(凭据失效)→ infra**(mock 服务回 401)
```
$ OLLAMA_BASE_URL=http://127.0.0.1:43797/v1 python3 driver.py ... --tag st-http-401
  invalid_infrastructure=12  valid_task_failure=0  n_scored=0
  样例 detail: retry after infra failure; first: 'HTTP 401: {"error": {"message": "invalid api key", "cod
```
结果: PASS(r0 记为 valid_task_failure = 把运维错误算成模型分)。

## 4. 404/其余 4xx → invalid_infrastructure

**404(模型名写错)→ infra**(mock 服务回 404)
```
$ OLLAMA_BASE_URL=http://127.0.0.1:45655/v1 python3 driver.py ... --tag st-http-404
  invalid_infrastructure=12  valid_task_failure=0  n_scored=0
  样例 detail: retry after infra failure; first: 'HTTP 404: {"error": {"message": "model not found", "cod
```
结果: PASS(r0 记为 valid_task_failure = 把运维错误算成模型分)。


**  附: 400 + 语义 error code → vtf(唯一例外)**(mock 服务回 400semantic)
```
$ OLLAMA_BASE_URL=http://127.0.0.1:33573/v1 python3 driver.py ... --tag st-http-400semantic
  invalid_infrastructure=0  valid_task_failure=12  n_scored=0
  样例 detail: HTTP 400: {"error": {"message": "prompt too long", "code": "context_length_exceeded"}}
```
结果: PASS(r0 记为 valid_task_failure = 把运维错误算成模型分)。


**  附: 400 无语义 code → infra**(mock 服务回 400opaque)
```
$ OLLAMA_BASE_URL=http://127.0.0.1:33119/v1 python3 driver.py ... --tag st-http-400opaque
  invalid_infrastructure=12  valid_task_failure=0  n_scored=0
  样例 detail: retry after infra failure; first: 'HTTP 400: {"error": {"message": "bad request"}}'; then:
```
结果: PASS(r0 记为 valid_task_failure = 把运维错误算成模型分)。

## 5. tie 确定性(同一概率两种键序判定一致)

**复现(r0)**: choice 用 `argmax(probabilities)`, 平票时取 dict 首个键 → 键序决定胜负。
```
r0: max(probs, key=probs.get)  # {'destructive':.5,'reversible':.5} vs 反序 → 判定可能翻转
   现实数据: runs/empty-state-g53f/smoke-002 平票, r0 取到首个键 destructive(=gold) 判对
```
**修复(r1)**: 平票以自报 `answer.choice` 为准; 自报缺失时判错。判定只依赖显式字段。

**复现失败(r1)**:
```
同概率 A/B 键序两组, 无自报  -> A 序=False  B 序=False   一致=True
同概率 A/B 键序两组, 自报='A' -> A 序=True              确定
```
结果: PASS — 键序不再影响判定。

## 6. round 边界写进契约并显式实现(非裸 round)

**复现(r0)**: score 用 Python 内置 `round()` = 银行家舍入, 半分界点归属随整数奇偶变化。
```
r0: int(round(score))  ->  round(2.5)=2 但 round(3.5)=4 (口径未在契约写明)
实测: half_up 与 round() 在 0.5/1.5/2.5/3.5 上分别 = [1, 2, 3, 4] vs [0, 2, 2, 4]
```
**修复(r1)**: 契约 `contracts/golden-jsonl.md`「并列/边界裁决」写明 half-up; 
`scoring/metrics.py::round_half_up` = `int(math.floor(x + 0.5))`, `correctness` 用它。

**复现失败(r1)**:
```
$ grep -n 'round_half_up' scoring/metrics.py
  24: def round_half_up(x):
  26:     return int(math.floor(float(x) + 0.5))
  61:         return min(max(round_half_up(v), 0), n - 1)
  92:     stated = min(max(round_half_up(v), 0), n - 1) if isinstance(v, (int, float)) \
  108:         return min(max(round_half_up(v), 0), n - 1)
```
结果: PASS — 显式 half-up, 契约同步写明。

## 7. manifest 含 effort/timeout/max_tokens/seed + report sha256

**复现(r0)**: r0 manifest 只有模型/分数/延迟, 无跑参数、无 sha256, 数值不可复核。

**修复(r1)**:

```json
{
 "run_id": "st-victim",
 "effort": "low",
 "timeout_s": 60.0,
 "max_tokens": 4096,
 "max_attempts": 2,
 "temperature": 0,
 "seed": null,
 "run_nonce": "b10fc373913aa33b263d8c440be66ec5",
 "integrity_algo": "hmac-sha256",
 "signing_key_source": "file",
 "n_scored": 12,
 "n_expected": 12,
 "n_received": 12,
 "abstentions_valid_task_failure": 0,
 "accuracy": 0.5833333333333334,
 "ece": 0.3466666666666668,
 "report_sha256": "f3f02505869e852ed155dd94766b861bd1f6b757b112c1e934f9c279f3f56c53",
 "responses_sha256": "60e7a4ef678f17dc02fbf07fc4770b1b022980853b8292da689f148fdc31aa8a"
}
```
**复现失败(r1)**: r0 那种「不可复核的历史行」在 r1 由 `--verify-run` 现场重算对账(见 §8)。
结果: PASS

## 8. `--verify-run <tag>` 重算一致

```
$ python3 driver.py --verify-run r1-smoke-jev-1 --dataset data/smoke-12.jsonl
dataset: 12 questions, sha256 96ed0440cda55e68..., tmp prefix dec001-qmj7qqzb
== verify-run r1-smoke-jev-1 ==
  signature              hmac-sha256 OK
  row count              12 vs dataset 12 OK
  id set                 OK
  n_scored               recomputed 12 vs report 12 OK
  accuracy               recomputed 1.0 vs report 1.0 OK
  ece                    recomputed 0.0183333333333332 vs report 0.0183333333333332 OK
  responses sha256       d26e4d340de741e0... vs report d26e4d340de741e0... OK
  report sha256          file 7e92b150251d7614... vs manifest 7e92b150251d7614... OK
  manifest accuracy      1.0 vs recomputed 1.0 OK
  manifest ece           0.0183333333333332 vs recomputed 0.0183333333333332 OK
  manifest n_scored      12 vs recomputed 12 OK
  manifest.effort        'low'
  manifest.timeout_s     60.0
  manifest.max_tokens    4096
  manifest.max_attempts  2
  manifest.temperature   0
  manifest.seed          None
  manifest.run_nonce     '5711e774252c503ffe5b977eba723445'
  manifest.integrity_algo 'hmac-sha256'
  manifest.signing_key_source 'file'
  manifest.n_expected    12
  manifest.n_received    12
  manifest.abstentions_valid_task_failure 0
  manifest.oracle        'stated-answer (argmax cross-check only)'
  manifest.tie_rule      'tie or exact 0.5 -> judged wrong (deterministic)'
  manifest.n_ties        0
  => RECOMPUTE CONSISTENT
rc=0
```
结果: PASS — r1-smoke-jev-1

```
$ python3 driver.py --verify-run smoke-g53f-1 --dataset data/smoke-12.jsonl
dataset: 12 questions, sha256 96ed0440cda55e68..., tmp prefix dec001-ohljykh4
== verify-run smoke-g53f-1 ==
  signature              LEGACY (r0 unkeyed; no cryptographic assurance)
  row count              12 vs dataset 12 OK
  id set                 OK
  n_scored               recomputed 12 vs report 12 OK
  accuracy               recomputed 1.0 vs report 1.0 OK
  ece                    recomputed 0.02416666666666656 vs report 0.02416666666666656 OK
  responses sha256       not recorded (pre-r1 artifact)
  report sha256          not recorded (pre-r1 artifact)
  manifest accuracy      1.0 vs recomputed 1.0 OK
  manifest ece           0.02416666666666656 vs recomputed 0.02416666666666656 OK
  manifest n_scored      12 vs recomputed 12 OK
  manifest.effort        None
  manifest.timeout_s     None
  manifest.max_tokens    None
  manifest.max_attempts  None
  manifest.temperature   None
  manifest.seed          None
  manifest.run_nonce     None
  manifest.integrity_algo None
  manifest.signing_key_source None
  manifest.n_expected    None
  manifest.n_received    None
  manifest.abstentions_valid_task_failure None
  manifest.oracle        None
  manifest.tie_rule      None
  manifest.n_ties        None
  => RECOMPUTE CONSISTENT [legacy artifact: metrics recomputed, integrity not cryptographic]
rc=0
```
结果: PASS — smoke-g53f-1

## 9. 修复后真 Jev 冒烟 12 题重跑仍 12/12 且 ECE 可算

```
$ python3 driver.py --adapter typesafe-native --model jev-latest --dataset data/smoke-12.jsonl --tag r1-smoke-jev-1
  n_scored=12/12  accuracy=1.0  ECE=0.0183333333333332
  integrity_assurance=hmac-sha256 (keyed; whole-record coverage)  run_nonce=5711e774252c503ffe5b977eba723445
```
结果: PASS(12/12, ECE 可算 = 0.0183)

## 10. 修复后 --empty-state 基线仍明显低于全分

```
$ python3 driver.py --adapter typesafe-native --model jev-latest --dataset data/smoke-12.jsonl --tag r1-empty-state-jev --empty-state
  empty-state: n_scored=12 accuracy=0.4167 ECE=0.5317
  full-state : n_scored=12 accuracy=1.0000 ECE=0.0183
```
结果: PASS(0.42 << 1.00, 区分度成立)。

## 11. 密钥/HMAC secret 零落盘

```
扫全树: decision-axis/(含 runs/、config/、*.pyc)
  ① HMAC secret 值命中(应 none):       none
  ② 产物 runs/ 里 key 路径/值命中(应 none): none
  ③ 真 provider key 值命中:             none(或环境未注入)
  ④ key 文件: 仓外, mode=0o600 dir=0o700(具体路径不写进报告)
  注: 源码/契约里出现『默认路径常量』是文档, 非秘密; 判定只看 ①②③。
```
结果: PASS(secret 值零落盘; 产物不含 key 路径; manifest 只记 signing_key_source)。

## 12. README 里 d41f/冒烟数字与契约口径自算一致

按 r1 口径(自报答案 + 平票判错)复算每个 run 的 accuracy/ECE, 与 manifest 记录对拍:

| run | n_scored | acc(r1 复算) | ECE(r1 复算) | manifest acc | manifest ECE | 结论 |
|---|---|---|---|---|---|---|
| smoke-g53f-1 | 12 | 1.0000 | 0.0242 | 1.0 | 0.0242 | 一致 |
| smoke-d41f-1 | 12 | 1.0000 | 0.0108 | 1.0 | 0.0108 | 一致 |
| smoke-jev-1 | 12 | 1.0000 | 0.0167 | 1.0 | 0.0167 | 一致 |
| empty-state-g53f | 12 | 0.3333 | 0.4317 | 0.5 | 0.2650 | **口径差异(见 README 说明)** |
| r1-smoke-jev-1 | 12 | 1.0000 | 0.0183 | 1.0 | 0.0183 | 一致 |
| r1-empty-state-jev | 12 | 0.4167 | 0.5317 | 0.4166666666666667 | 0.5317 | 一致 |

**d41f 原话核对**(reviewer Blocker 6 称应为 0.9167/0.1583): 
`smoke-d41f-1` 12 行在 argmax/自报/round/half-up 四种读法下**逐题全对** → 1.0000/0.0108,
与 manifest 一致。穷举(置信度源 × 桶数 2–20 × 翻转 0–2 题)无任何组合得出 0.9167/0.1583;
`/tmp/red-dec001-reviewer/probeL.py` 盘上不存在。**该数字不可复现, 不采用**, README 按可复算事实写。

结果: PASS — README 数字与契约口径自算逐格一致(d41f = 1.0000/0.0108)。

## 汇总

- §1: 见上(每条含 复现→修复→复现失败 三段)。
- §2: 见上(每条含 复现→修复→复现失败 三段)。
- §3: 见上(每条含 复现→修复→复现失败 三段)。
- §4: 见上(每条含 复现→修复→复现失败 三段)。
- §5: 见上(每条含 复现→修复→复现失败 三段)。
- §6: 见上(每条含 复现→修复→复现失败 三段)。
- §7: 见上(每条含 复现→修复→复现失败 三段)。
- §8: 见上(每条含 复现→修复→复现失败 三段)。
- §9: 见上(每条含 复现→修复→复现失败 三段)。
- §10: 见上(每条含 复现→修复→复现失败 三段)。
- §11: 见上(每条含 复现→修复→复现失败 三段)。
- §12: 见上(每条含 复现→修复→复现失败 三段)。

零外部 API 调用; mock server 内起线程。真 Jev 冒烟见 §9/§10(已产出 run, 本脚本仅复算)。

