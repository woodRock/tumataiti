## int4 open students, case_upper: test_full

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **28.9%** | **99.1%** | **33.1%** |
| Span leak rate | 76.6% | 6.6% | 63.6% | 10.4% |
| Any-PII char precision | 90.0 | 78.0 | 90.8 | 89.7 |
| Any-PII char recall | 26.0 | 97.9 | 47.5 | 94.3 |
| Any-PII char F1 | 40.4 | 86.8 | 62.3 | 92.0 |
| Exact-span F1 (all categories) | 37.5 | 52.3 | 41.2 | 44.0 |
| Median ms per document | 0.05 | 64.35 | 188.77 | 139.92 |

Span leak rate by category (lower is better):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON (6250 spans) | 100.0% | 9.3% | 82.6% | 11.9% |
| ADDRESS (1000 spans) | 100.0% | 2.7% | 2.1% | 0.8% |
| EMAIL (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (5000 spans) | 100.0% | 8.9% | 100.0% | 18.3% |

Character-level F1 by category (category must match):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON | 0.0 | 58.1 | 40.6 | 67.0 |
| ADDRESS | 0.0 | 94.8 | 99.8 | 99.5 |
| EMAIL | 100.0 | 100.0 | 98.7 | 100.0 |
| PHONE | 100.0 | 100.0 | 99.1 | 99.9 |
| DATE | 100.0 | 100.0 | 97.7 | 98.3 |
| ID | 100.0 | 100.0 | 99.5 | 100.0 |
| AFFILIATION | 0.0 | 48.8 | 1.7 | 46.4 |
