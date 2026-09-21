# Decision-axis run: r1-empty-state-jev

- adapter: `typesafe-native`  model: `jev-latest`
- dataset: `data/smoke-12.jsonl` sha256 `96ed0440cda55e68...`
- driver: dec001-r1.1.0  tmp_prefix: dec001-gfl_iecc
- run_nonce: `d0abaff3811e3d3803715d69d1e4b66f`
- integrity: hmac-sha256   assurance: hmac-sha256 (keyed; whole-record coverage)
- report.json sha256: `3b13069977de02a9b8d9e5971eb7d8eec919d8ce0c68bc51e8c44c51189cac72`
- responses.jsonl sha256: `4818da7f459d548f0d17665b0786043d4bb4e0b90fe94765bcdb631328591ccf`

 scored: 12 / expected 12  accuracy: 0.4166666666666667
 abstentions (valid_task_failure, excluded from denominator): 0
 oracle: stated-answer (argmax cross-check only); tie rule: tie or exact 0.5 -> judged wrong (deterministic); rounding: explicit half-up floor(x+0.5), not Python round()
 ties seen: 0  stated/argmax inconsistent: 0/8
 ECE: 0.5316666666666667
 latency mean: 0.5904166666666667s max: 0.65s
 cost: {'per_decision_mean_usd': None, 'total_usd': None, 'n_priced': 0, 'note': 'no price table entry for this model; cost left null rather than fabricated'}

## by family
- bug-triage: 0/1 = 0.0
- code-quality: 1/1 = 1.0
- customer-sentiment: 0/1 = 0.0
- doc-classification: 0/1 = 0.0
- doc-completeness: 1/1 = 1.0
- grammar-check: 1/1 = 1.0
- incident-urgency: 0/1 = 0.0
- language-id: 1/1 = 1.0
- policy-compliance: 1/1 = 1.0
- privacy-check: 0/1 = 0.0
- safety-guardrail: 0/1 = 0.0
- support-routing: 0/1 = 0.0

## calibration buckets (10, equal-width)
| conf lo-hi | n | acc | conf | gap |
|---|---|---|---|---|
| 0.0-0.1 | 0 | - | - | - |
| 0.1-0.2 | 0 | - | - | - |
| 0.2-0.3 | 0 | - | - | - |
| 0.3-0.4 | 0 | - | - | - |
| 0.4-0.5 | 0 | - | - | - |
| 0.5-0.6 | 1 | 1.00 | 0.51 | 0.490 |
| 0.6-0.7 | 2 | 0.50 | 0.65 | 0.150 |
| 0.7-0.8 | 0 | - | - | - |
| 0.8-0.9 | 2 | 0.50 | 0.84 | 0.340 |
| 0.9-1.0 | 7 | 0.29 | 0.99 | 0.701 |

## threshold scan
| threshold | auto_exec_rate | n | accuracy |
|---|---|---|---|
| 0.00 | 1.00 | 12 | 0.42 |
| 0.05 | 1.00 | 12 | 0.42 |
| 0.10 | 1.00 | 12 | 0.42 |
| 0.15 | 1.00 | 12 | 0.42 |
| 0.20 | 1.00 | 12 | 0.42 |
| 0.25 | 1.00 | 12 | 0.42 |
| 0.30 | 1.00 | 12 | 0.42 |
| 0.35 | 1.00 | 12 | 0.42 |
| 0.40 | 1.00 | 12 | 0.42 |
| 0.45 | 1.00 | 12 | 0.42 |
| 0.50 | 1.00 | 12 | 0.42 |
| 0.55 | 0.92 | 11 | 0.36 |
| 0.60 | 0.92 | 11 | 0.36 |
| 0.65 | 0.83 | 10 | 0.40 |
| 0.70 | 0.75 | 9 | 0.33 |
| 0.75 | 0.75 | 9 | 0.33 |
| 0.80 | 0.75 | 9 | 0.33 |
| 0.85 | 0.67 | 8 | 0.25 |
| 0.90 | 0.58 | 7 | 0.29 |
| 0.95 | 0.58 | 7 | 0.29 |
| 1.00 | 0.25 | 3 | 0.33 |

## failures
- invalid_infrastructure: 0
- valid_task_failure: 0

## per question
- smoke-001: scored correct=False pred='technical' conf=1.0
- smoke-002: scored correct=False pred='reversible' conf=0.99
- smoke-003: scored correct=False pred='contract' conf=0.62
- smoke-004: scored correct=True pred='python' conf=0.81
- smoke-005: scored correct=False pred=0 conf=1.0
- smoke-006: scored correct=False pred=0 conf=0.97
- smoke-007: scored correct=True pred=0 conf=0.99
- smoke-008: scored correct=True pred=2 conf=1.0
- smoke-009: scored correct=True pred=False conf=0.68
- smoke-010: scored correct=False pred=False conf=0.96
- smoke-011: scored correct=False pred=False conf=0.87
- smoke-012: scored correct=True pred=False conf=0.51
