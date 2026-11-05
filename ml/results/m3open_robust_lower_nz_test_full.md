## int4 open students, lower: test_full

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **94.7%** | **83.3%** | **53.4%** |
| Span leak rate | 66.7% | 45.2% | 31.6% | 17.6% |
| Any-PII char precision | 88.4 | 93.5 | 92.0 | 92.5 |
| Any-PII char recall | 37.0 | 70.7 | 82.5 | 91.1 |
| Any-PII char F1 | 52.2 | 80.5 | 87.0 | 91.8 |
| Exact-span F1 (all categories) | 49.1 | 59.2 | 67.5 | 57.7 |
| Median ms per document | 0.05 | 57.43 | 144.67 | 132.53 |

Span leak rate by category (lower is better):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON (5250 spans) | 100.0% | 80.6% | 57.0% | 29.7% |
| ADDRESS (1000 spans) | 100.0% | 15.3% | 0.1% | 10.5% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 33.3% | 3.2% | 11.5% | 7.3% |

Character-level F1 by category (category must match):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON | 0.0 | 44.0 | 69.0 | 86.1 |
| ADDRESS | 0.0 | 97.4 | 98.9 | 98.1 |
| EMAIL | 100.0 | 100.0 | 99.4 | 100.0 |
| PHONE | 100.0 | 100.0 | 98.7 | 99.4 |
| DATE | 100.0 | 99.9 | 97.6 | 100.0 |
| ID | 87.1 | 98.8 | 88.5 | 95.7 |
