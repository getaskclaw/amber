# Decision-axis run: red-smoke-g53f

- adapter: `openai-compatible-baseline`  model: `glm-5.3-flash`
- dataset: `data/smoke-12.jsonl` sha256 `96ed0440cda55e68...`
- driver: dec001-r1.1.0  tmp_prefix: dec001-nmriiff0
- run_nonce: `366cc6220b87f718fd60b34d3371e3f0`
- integrity: hmac-sha256   assurance: hmac-sha256 (keyed; whole-record coverage)
- report.json sha256: `1925b1f591878199175f71d290ff2a2b8fbcafff899215bddffcadde8eceb876`
- responses.jsonl sha256: `f3e41180c17ed605242682477968c94fb05da66a0ed5ba947ae5f53be93597ea`

 scored: 12 / expected 12  accuracy: 1.0
 abstentions (valid_task_failure, excluded from denominator): 0
 oracle: stated-answer (argmax cross-check only); tie rule: tie or exact 0.5 -> judged wrong (deterministic); rounding: explicit half-up floor(x+0.5), not Python round()
 ties seen: 0  stated/argmax inconsistent: 0/8
 ECE: 0.03083333333333337
 latency mean: 0.9685833333333335s max: 1.409s
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
| 0.8-0.9 | 1 | 1.00 | 0.80 | 0.200 |
| 0.9-1.0 | 11 | 1.00 | 0.98 | 0.015 |

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
| 0.85 | 0.92 | 11 | 1.00 |
| 0.90 | 0.92 | 11 | 1.00 |
| 0.95 | 0.75 | 9 | 1.00 |
| 1.00 | 0.67 | 8 | 1.00 |

## failures
- invalid_infrastructure: 0
- valid_task_failure: 0

## per question
- smoke-001: scored correct=True pred='billing' conf=0.98
- smoke-002: scored correct=True pred='destructive' conf=1.0
- smoke-003: scored correct=True pred='invoice' conf=1.0
- smoke-004: scored correct=True pred='python' conf=1.0
- smoke-005: scored correct=True pred=2 conf=0.9
- smoke-006: scored correct=True pred=2 conf=1.0
- smoke-007: scored correct=True pred=0 conf=0.95
- smoke-008: scored correct=True pred=2 conf=0.8
- smoke-009: scored correct=True pred=False conf=1.0
- smoke-010: scored correct=True pred=True conf=1.0
- smoke-011: scored correct=True pred=True conf=1.0
- smoke-012: scored correct=True pred=False conf=1.0
