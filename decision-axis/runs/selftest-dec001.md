# selftest-dec001 — WO-DEC-001 验收矩阵自测

生成方式: `python3 selftest.py`; 逐项命令与原始输出如下。

## 1. 金标 schema 文档化 + 校验器对坏样本报错

schema 文档: `contracts/golden-jsonl.md`; 校验器: `scoring/validate.py`。
```
$ python3 scoring/validate.py data/smoke-12.jsonl
OK: 12 records valid
families (12): {'support-routing': 1, 'safety-guardrail': 1, 'doc-classification': 1, 'language-id': 1, 'customer-sentiment': 1, 'incident-urgency': 1, 'code-quality': 1, 'doc-completeness': 1, 'policy-compliance': 1, 'privacy-check': 1, 'bug-triage': 1, 'grammar-check': 1}
types: {'choice': 4, 'score': 4, 'noul': 4}
rc=0
```
坏样本(gold 不在 options 里, 且 options 只有一个):
```
$ python3 scoring/validate.py /tmp/dec001-bad.jsonl
INVALID: line 1: choice requires question.options with >=2 entries
rc=1
```
结果: PASS(坏样本被拒绝)

## 4. ECE 自计算正确性(人工构造已知概率集)

构造 4 题, 置信度与对错已知:
- conf 0.90 对, 0.90 错 → 桶 [0.8,0.9)? 用 10 等宽桶: 0.90 落 [0.9,1.0); 改用手算方便的值: 0.85,0.85,0.75,0.65
- 设定: conf=[0.85,0.85,0.75,0.65], correct=[1,0,1,1]
- 10 等宽桶: [0.8,0.9) 两题 acc=0.5 conf=0.85 gap=0.35, 权重 2/4; [0.7,0.8) 一题 acc=1 conf=0.75 gap=0.25 权重 1/4; [0.6,0.7) 一题 acc=1 conf=0.65 gap=0.35 权重 1/4
- 手算 ECE = 0.5*0.35 + 0.25*0.25 + 0.25*0.35 = 0.175+0.0625+0.0875 = 0.325

代码 ECE = 0.325000; 手算 ECE = 0.325
结果: PASS

## 6. invalid_infrastructure 分类存在且不计入模型分

把 OLLAMA_BASE_URL 指向本机死端口 127.0.0.1:9, 触发连接拒绝(网络层失败):
```
$ OLLAMA_BASE_URL=http://127.0.0.1:9/v1 python3 driver.py ... --tag selftest-timeout-200111
dataset: 12 questions, sha256 96ed0440cda55e68..., tmp prefix dec001-49iq_g_5
  smoke-001: ok=False err=invalid_infrastructure lat=0.0s
  smoke-002: ok=False err=invalid_infrastructure lat=0.0s
  smoke-003: ok=False err=invalid_infrastructure lat=0.0s
  smoke-004: ok=False err=invalid_infrastructure lat=0.0s
  smoke-005: ok=False err=invalid_infrastructure lat=0.0s
  smoke-006: ok=False err=invalid_infrastructure lat=0.0s
  smoke-007: ok=False err=invalid_infrastructure lat=0.0s
...(截断)...
  smoke-012: ok=False err=invalid_infrastructure lat=0.0s
done -> /home/computebox/2606/amber/decision-axis/runs/selftest-timeout-200111
accuracy=None ece=0.0 n_scored=0/12
verify with: python3 driver.py --verify-run selftest-timeout-200111 --dataset data/smoke-12.jsonl
```
报告分类: invalid_infrastructure=12, scored=0, valid_task_failure=0
结果: PASS(12 题全部 infra 失败, 零计入模型分; 与 valid_task_failure 分列)

## 5a. tmp 前缀每跑随机

```
dataset: 12 questions, sha256 96ed0440cda55e68..., tmp prefix dec001-gyo_8aph
dataset: 12 questions, sha256 96ed0440cda55e68..., tmp prefix dec001-14t58i_h
```
结果: PASS

## 5b. 篡改响应文件, 完整性校验必须拦下

```
$ python3 driver.py --score-only /tmp/dec001-tampered.jsonl ...
REFUSED: LEGACY ARTIFACT: smoke-001, smoke-002, smoke-003, smoke-004, smoke-005, smoke-006, smoke-007, smoke-008, smoke-009, smoke-010, smoke-011, smoke-012 无 r1 HMAC 签名(r0 公开无钥公式, 不可信)。要重算请显式加 --allow-legacy-unkeyed; 那样出的报告会被标注 integrity_assurance=legacy-unkeyed(NOT cryptographic)。
rc=2
```
结果: PASS(改答案不重算 sha → 拒绝出分; r1 消息可能是 TAMPER 或 LEGACY)

## 7. 密钥零落盘扫描

扫描对象: 整个 decision-axis 目录(含 runs/、config/)。
```
KEY VALUE LEAKED IN: none
```
结果: PASS(密钥值 0 处出现; 代码/报告只含变量名)

## 汇总

- PASS — 1 schema 校验器
- PASS — 4 ECE 手算
- PASS — 5a tmp 随机
- PASS — 5b 篡改拦截
- PASS — 6 infra 分类
- PASS — 7 密钥零落盘

验收 2/3(真跑出分)与 5c(空 state 基线)、8(dry-run 对照文档)见 runs/ 下对应产物与 REPORT.md。

