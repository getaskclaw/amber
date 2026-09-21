# Decision-axis run: empty-state-g53f

- adapter: `openai-compatible-baseline`  model: `glm-5.3-flash`
- dataset: `data/smoke-12.jsonl` sha256 `96ed0440cda55e68...`
- driver: dec001-1.0  tmp_prefix: dec001-9wm1nfci

 scored: 12  accuracy: 0.5
 ECE: 0.26499999999999996
 latency mean: 0.9439166666666666s max: 1.329s
 cost: {'per_decision_mean_usd': None, 'total_usd': None, 'n_priced': 0, 'note': 'no price table entry for this model; cost left null rather than fabricated'}

## by family
- bug-triage: 1/1 = 1.0
- code-quality: 0/1 = 0.0
- customer-sentiment: 0/1 = 0.0
- doc-classification: 1/1 = 1.0
- doc-completeness: 1/1 = 1.0
- grammar-check: 1/1 = 1.0
- incident-urgency: 0/1 = 0.0
- language-id: 1/1 = 1.0
- policy-compliance: 0/1 = 0.0
- privacy-check: 0/1 = 0.0
- safety-guardrail: 1/1 = 1.0
- support-routing: 0/1 = 0.0

## calibration buckets (10, equal-width)
| conf lo-hi | n | acc | conf | gap |
|---|---|---|---|---|
| 0.0-0.1 | 0 | - | - | - |
| 0.1-0.2 | 0 | - | - | - |
| 0.2-0.3 | 0 | - | - | - |
| 0.3-0.4 | 3 | 0.67 | 0.34 | 0.327 |
| 0.4-0.5 | 1 | 0.00 | 0.40 | 0.400 |
| 0.5-0.6 | 5 | 0.40 | 0.50 | 0.100 |
| 0.6-0.7 | 0 | - | - | - |
| 0.7-0.8 | 1 | 1.00 | 0.70 | 0.300 |
| 0.8-0.9 | 0 | - | - | - |
| 0.9-1.0 | 2 | 0.50 | 1.00 | 0.500 |

## threshold scan
| threshold | auto_exec_rate | n | accuracy |
|---|---|---|---|
| 0.00 | 1.00 | 12 | 0.50 |
| 0.05 | 1.00 | 12 | 0.50 |
| 0.10 | 1.00 | 12 | 0.50 |
| 0.15 | 1.00 | 12 | 0.50 |
| 0.20 | 1.00 | 12 | 0.50 |
| 0.25 | 1.00 | 12 | 0.50 |
| 0.30 | 1.00 | 12 | 0.50 |
| 0.35 | 0.75 | 9 | 0.44 |
| 0.40 | 0.75 | 9 | 0.44 |
| 0.45 | 0.67 | 8 | 0.50 |
| 0.50 | 0.67 | 8 | 0.50 |
| 0.55 | 0.25 | 3 | 0.67 |
| 0.60 | 0.25 | 3 | 0.67 |
| 0.65 | 0.25 | 3 | 0.67 |
| 0.70 | 0.17 | 2 | 0.50 |
| 0.75 | 0.17 | 2 | 0.50 |
| 0.80 | 0.17 | 2 | 0.50 |
| 0.85 | 0.17 | 2 | 0.50 |
| 0.90 | 0.17 | 2 | 0.50 |
| 0.95 | 0.17 | 2 | 0.50 |
| 1.00 | 0.17 | 2 | 0.50 |

## failures
- invalid_infrastructure: 0
- valid_task_failure: 0

## per question
- smoke-001: scored correct=False conf=0.34
- smoke-002: scored correct=True conf=0.5
- smoke-003: scored correct=True conf=0.34
- smoke-004: scored correct=True conf=0.34
- smoke-005: scored correct=False conf=0.5
- smoke-006: scored correct=False conf=0.5
- smoke-007: scored correct=False conf=0.4
- smoke-008: scored correct=True conf=0.7
- smoke-009: scored correct=False conf=0.5
- smoke-010: scored correct=False conf=1.0
- smoke-011: scored correct=True conf=0.5
- smoke-012: scored correct=True conf=1.0
