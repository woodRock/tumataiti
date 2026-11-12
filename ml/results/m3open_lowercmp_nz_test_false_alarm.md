## Deployed and retrained, int4: nz_test_false_alarm

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| **Document leak rate** (lower is better) | **0.0%** | **0.0%** |
| Span leak rate | 0.0% | 0.0% |
| Any-PII char precision | 70.1 | 69.1 |
| Any-PII char recall | 100.0 | 100.0 |
| Any-PII char F1 | 82.4 | 81.8 |
| Exact-span F1 (all categories) | 59.4 | 58.1 |
| Median ms per document | 19.41 | 35.70 |

Span leak rate by category (lower is better):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON (800 spans) | 0.0% | 0.0% |
| ADDRESS (100 spans) | 0.0% | 0.0% |
| EMAIL (100 spans) | 0.0% | 0.0% |
| PHONE (200 spans) | 0.0% | 0.0% |
| ID (200 spans) | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON | 80.3 | 80.6 |
| ADDRESS | 99.9 | 100.0 |
| EMAIL | 100.0 | 100.0 |
| PHONE | 100.0 | 99.7 |
| ID | 50.6 | 48.0 |
