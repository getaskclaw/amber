# Decision-axis run: r1-smoke-jev-1

- adapter: `typesafe-native`  model: `jev-latest`
- dataset: `data/smoke-12.jsonl` sha256 `96ed0440cda55e68...`
- driver: dec001-r1.1.0  tmp_prefix: dec001-f8qyu4ia
- run_nonce: `5711e774252c503ffe5b977eba723445`
- integrity: hmac-sha256   assurance: hmac-sha256 (keyed; whole-record coverage)
- report.json sha256: `7e92b150251d7614456177f2b74af358323a67129d3879e27aa6e4e90bf40139`
- responses.jsonl sha256: `d26e4d340de741e0f1be8ec0f9cd08e29ac0d220e5fb6230b86af1e4e7b2158b`

 scored: 12 / expected 12  accuracy: 1.0
 abstentions (valid_task_failure, excluded from denominator): 0
 oracle: stated-answer (argmax cross-check only); tie rule: tie or exact 0.5 -> judged wrong (deterministic); rounding: explicit half-up floor(x+0.5), not Python round()
 ties seen: 0  stated/argmax inconsistent: 0/8
 ECE: 0.0183333333333332
 latency mean: 0.59475s max: 0.663s
 cost: {'per_decision_mean_usd': None, 'total_usd': None, 'n_priced': 0, 'note': 'no price table entry for this model; cost left null rather than fabricated'}

## by family
- bug-triage: 1/1 = 1.0
- code-quality: 1/1 = 1.0
- customer-sentiment: 1/1 = 1.0
- doc-classification: 1/1 = 1.0
- doc-completeness: 1/1 = 1.0
- grammar-check: 1/1 = 1.0
- incident-urgency: 1/1 = 1.0
- language-id: 1/1 = 1.0
- policy-compliance: 1/1 = 1.0
- privacy-check: 1/1 = 1.0
- safety-guardrail: 1/1 = 1.0
- support-routing: 1/1 = 1.0

## calibration buckets (10, equal-width)
| conf lo-hi | n | acc | conf | gap |
|---|---|---|---|---|
| 0.0-0.1 | 0 | - | - | - |
| 0.1-0.2 | 0 | - | - | - |
| 0.2-0.3 | 0 | - | - | - |
| 0.3-0.4 | 0 | - | - | - |
| 0.4-0.5 | 0 | - | - | - |
| 0.5-0.6 | 0 | - | - | - |
| 0.6-0.7 | 0 | - | - | - |
| 0.7-0.8 | 0 | - | - | - |
| 0.8-0.9 | 0 | - | - | - |
| 0.9-1.0 | 12 | 1.00 | 0.98 | 0.018 |

## threshold scan
| threshold | auto_exec_rate | n | accuracy |
|---|---|---|---|
| 0.00 | 1.00 | 12 | 1.00 |
| 0.05 | 1.00 | 12 | 1.00 |
| 0.10 | 1.00 | 12 | 1.00 |
| 0.15 | 1.00 | 12 | 1.00 |
| 0.20 | 1.00 | 12 | 1.00 |
| 0.25 | 1.00 | 12 | 1.00 |
| 0.30 | 1.00 | 12 | 1.00 |
| 0.35 | 1.00 | 12 | 1.00 |
| 0.40 | 1.00 | 12 | 1.00 |
| 0.45 | 1.00 | 12 | 1.00 |
| 0.50 | 1.00 | 12 | 1.00 |
| 0.55 | 1.00 | 12 | 1.00 |
| 0.60 | 1.00 | 12 | 1.00 |
| 0.65 | 1.00 | 12 | 1.00 |
| 0.70 | 1.00 | 12 | 1.00 |
| 0.75 | 1.00 | 12 | 1.00 |
| 0.80 | 1.00 | 12 | 1.00 |
| 0.85 | 1.00 | 12 | 1.00 |
| 0.90 | 1.00 | 12 | 1.00 |
| 0.95 | 0.83 | 10 | 1.00 |
| 1.00 | 0.58 | 7 | 1.00 |

## failures
- invalid_infrastructure: 0
- valid_task_failure: 0

## per question
- smoke-001: scored correct=True pred='billing' conf=1.0
- smoke-002: scored correct=True pred='destructive' conf=1.0
- smoke-003: scored correct=True pred='invoice' conf=1.0
- smoke-004: scored correct=True pred='python' conf=1.0
- smoke-005: scored correct=True pred=2 conf=1.0
- smoke-006: scored correct=True pred=2 conf=1.0
- smoke-007: scored correct=True pred=0 conf=1.0
- smoke-008: scored correct=True pred=2 conf=0.91
- smoke-009: scored correct=True pred=False conf=0.97
- smoke-010: scored correct=True pred=True conf=0.99
- smoke-011: scored correct=True pred=True conf=0.98
- smoke-012: scored correct=True pred=False conf=0.93
