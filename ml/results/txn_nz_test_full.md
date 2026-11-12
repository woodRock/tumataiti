## nz_test_full: review layer without and with transaction labels

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| **Document leak rate** (lower is better) | **2.0%** | **2.0%** |
| Span leak rate | 0.4% | 0.4% |
| Any-PII char precision | 92.3 | 92.3 |
| Any-PII char recall | 99.8 | 99.8 |
| Any-PII char F1 | 95.9 | 95.9 |
| Exact-span F1 (all categories) | 83.8 | 83.8 |
| Median ms per document | 9.91 | 9.91 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON (6250 spans) | 0.1% | 0.1% |
| ADDRESS (1000 spans) | 0.0% | 0.0% |
| EMAIL (1000 spans) | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% |
| AFFILIATION (5000 spans) | 1.0% | 1.0% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON | 96.8 | 96.8 |
| ADDRESS | 96.3 | 96.3 |
| EMAIL | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 |
| ID | 100.0 | 100.0 |
| AFFILIATION | 91.7 | 91.7 |
