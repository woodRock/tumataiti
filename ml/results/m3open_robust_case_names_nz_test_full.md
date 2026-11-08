## int4 open students, case_names: test_full

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **95.9%** | **96.3%** | **56.9%** |
| Span leak rate | 64.1% | 45.5% | 42.9% | 21.1% |
| Any-PII char precision | 88.8 | 92.6 | 90.7 | 92.7 |
| Any-PII char recall | 38.6 | 69.4 | 71.8 | 88.6 |
| Any-PII char F1 | 53.8 | 79.3 | 80.2 | 90.6 |
| Exact-span F1 (all categories) | 51.9 | 63.9 | 63.2 | 58.0 |
| Median ms per document | 0.05 | 70.72 | 165.14 | 125.96 |

Span leak rate by category (lower is better):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON (5250 spans) | 100.0% | 84.5% | 79.6% | 39.1% |
| ADDRESS (1000 spans) | 100.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON | 0.0 | 35.2 | 41.7 | 80.4 |
| ADDRESS | 0.0 | 100.0 | 99.8 | 100.0 |
| EMAIL | 100.0 | 100.0 | 99.9 | 100.0 |
| PHONE | 100.0 | 100.0 | 98.9 | 100.0 |
| DATE | 100.0 | 100.0 | 97.2 | 100.0 |
| ID | 100.0 | 100.0 | 100.0 | 99.9 |
