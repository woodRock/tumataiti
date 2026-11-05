## Deployed and retrained, int4: nz_test_false_alarm

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| **Document leak rate** (lower is better) | **0.0%** | **0.3%** |
| Span leak rate | 0.0% | 0.1% |
| Any-PII char precision | 70.0 | 67.3 |
| Any-PII char recall | 100.0 | 99.9 |
| Any-PII char F1 | 82.4 | 80.5 |
| Exact-span F1 (all categories) | 59.4 | 56.2 |
| Median ms per document | 16.55 | 33.89 |

Span leak rate by category (lower is better):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON (800 spans) | 0.0% | 0.2% |
| ADDRESS (100 spans) | 0.0% | 0.0% |
| EMAIL (100 spans) | 0.0% | 0.0% |
| PHONE (200 spans) | 0.0% | 0.0% |
| ID (200 spans) | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON | 80.2 | 78.1 |
| ADDRESS | 97.2 | 98.1 |
| EMAIL | 100.0 | 100.0 |
| PHONE | 99.8 | 100.0 |
| ID | 51.7 | 46.5 |
