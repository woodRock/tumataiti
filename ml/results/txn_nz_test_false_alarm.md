## nz_test_false_alarm: review layer without and with transaction labels

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| **Document leak rate** (lower is better) | **1.5%** | **1.5%** |
| Span leak rate | 0.6% | 0.6% |
| Any-PII char precision | 77.3 | 80.8 |
| Any-PII char recall | 99.8 | 99.8 |
| Any-PII char F1 | 87.1 | 89.3 |
| Exact-span F1 (all categories) | 66.0 | 68.1 |
| Median ms per document | 16.65 | 16.65 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON (800 spans) | 1.1% | 1.1% |
| ADDRESS (100 spans) | 0.0% | 0.0% |
| EMAIL (100 spans) | 0.0% | 0.0% |
| PHONE (200 spans) | 0.0% | 0.0% |
| ID (200 spans) | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON | 91.7 | 91.7 |
| ADDRESS | 99.9 | 99.9 |
| EMAIL | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 |
| ID | 50.5 | 57.9 |
