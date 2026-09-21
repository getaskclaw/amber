# Decision-axis run: timeout-sim

- adapter: `openai-compatible-baseline`  model: `glm-5.3-flash`
- dataset: `data/smoke-12.jsonl` sha256 `96ed0440cda55e68...`
- driver: dec001-1.0  tmp_prefix: dec001-xmk9ycnt

 scored: 0  accuracy: None
 ECE: 0.0
 latency mean: Nones max: Nones
 cost: {'per_decision_mean_usd': None, 'total_usd': None, 'n_priced': 0, 'note': 'no price table entry for this model; cost left null rather than fabricated'}

## by family

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
| 0.9-1.0 | 0 | - | - | - |

## threshold scan
| threshold | auto_exec_rate | n | accuracy |
|---|---|---|---|
| 0.00 | - | 0 | - |
| 0.05 | - | 0 | - |
| 0.10 | - | 0 | - |
| 0.15 | - | 0 | - |
| 0.20 | - | 0 | - |
| 0.25 | - | 0 | - |
| 0.30 | - | 0 | - |
| 0.35 | - | 0 | - |
| 0.40 | - | 0 | - |
| 0.45 | - | 0 | - |
| 0.50 | - | 0 | - |
| 0.55 | - | 0 | - |
| 0.60 | - | 0 | - |
| 0.65 | - | 0 | - |
| 0.70 | - | 0 | - |
| 0.75 | - | 0 | - |
| 0.80 | - | 0 | - |
| 0.85 | - | 0 | - |
| 0.90 | - | 0 | - |
| 0.95 | - | 0 | - |
| 1.00 | - | 0 | - |

## failures
- invalid_infrastructure: 12
  - smoke-001: retry after infra failure; first: '<urlopen error [Errno 111] Connection refused>'; then: '<urlopen error [Errno 111] Connection refused>'
  - smoke-002: retry after infra failure; first: '<urlopen error [Errno 111] Connection refused>'; then: '<urlopen error [Errno 111] Connection refused>'
  - smoke-003: retry after infra failure; first: '<urlopen error [Errno 111] Connection refused>'; then: '<urlopen error [Errno 111] Connection refused>'
  - smoke-004: retry after infra failure; first: '<urlopen error [Errno 111] Connection refused>'; then: '<urlopen error [Errno 111] Connection refused>'
  - smoke-005: retry after infra failure; first: '<urlopen error [Errno 111] Connection refused>'; then: '<urlopen error [Errno 111] Connection refused>'
  - smoke-006: retry after infra failure; first: '<urlopen error [Errno 111] Connection refused>'; then: '<urlopen error [Errno 111] Connection refused>'
  - smoke-007: retry after infra failure; first: '<urlopen error [Errno 111] Connection refused>'; then: '<urlopen error [Errno 111] Connection refused>'
  - smoke-008: retry after infra failure; first: '<urlopen error [Errno 111] Connection refused>'; then: '<urlopen error [Errno 111] Connection refused>'
  - smoke-009: retry after infra failure; first: '<urlopen error [Errno 111] Connection refused>'; then: '<urlopen error [Errno 111] Connection refused>'
  - smoke-010: retry after infra failure; first: '<urlopen error [Errno 111] Connection refused>'; then: '<urlopen error [Errno 111] Connection refused>'
  - smoke-011: retry after infra failure; first: '<urlopen error [Errno 111] Connection refused>'; then: '<urlopen error [Errno 111] Connection refused>'
  - smoke-012: retry after infra failure; first: '<urlopen error [Errno 111] Connection refused>'; then: '<urlopen error [Errno 111] Connection refused>'
- valid_task_failure: 0

## per question
- smoke-001: invalid_infrastructure
- smoke-002: invalid_infrastructure
- smoke-003: invalid_infrastructure
- smoke-004: invalid_infrastructure
- smoke-005: invalid_infrastructure
- smoke-006: invalid_infrastructure
- smoke-007: invalid_infrastructure
- smoke-008: invalid_infrastructure
- smoke-009: invalid_infrastructure
- smoke-010: invalid_infrastructure
- smoke-011: invalid_infrastructure
- smoke-012: invalid_infrastructure
