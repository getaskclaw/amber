# Decision-axis run: smoke-d41f-1

- adapter: `openai-compatible-baseline`  model: `deepseek-v4.1-flash`
- dataset: `data/smoke-12.jsonl` sha256 `96ed0440cda55e68...`
- driver: dec001-1.0  tmp_prefix: dec001-8uvq8wab

 scored: 12  accuracy: 1.0
 ECE: 0.01083333333333325
 latency mean: 4.722416666666667s max: 39.251s
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
| 0.9-1.0 | 12 | 1.00 | 0.99 | 0.011 |

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
| 0.95 | 0.92 | 11 | 1.00 |
| 1.00 | 0.75 | 9 | 1.00 |

## failures
- invalid_infrastructure: 0
- valid_task_failure: 0

## per question
- smoke-001: scored correct=True conf=0.98
- smoke-002: scored correct=True conf=1.0
- smoke-003: scored correct=True conf=0.99
- smoke-004: scored correct=True conf=1.0
- smoke-005: scored correct=True conf=1.0
- smoke-006: scored correct=True conf=1.0
- smoke-007: scored correct=True conf=1.0
- smoke-008: scored correct=True conf=0.9
- smoke-009: scored correct=True conf=1.0
- smoke-010: scored correct=True conf=1.0
- smoke-011: scored correct=True conf=1.0
- smoke-012: scored correct=True conf=1.0
