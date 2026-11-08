## int4 open students, case_upper: test_full

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **31.3%** | **67.6%** | **13.8%** |
| Span leak rate | 64.1% | 8.3% | 23.4% | 3.5% |
| Any-PII char precision | 88.8 | 82.5 | 89.5 | 84.5 |
| Any-PII char recall | 38.6 | 97.1 | 88.3 | 98.9 |
| Any-PII char F1 | 53.8 | 89.2 | 88.9 | 91.2 |
| Exact-span F1 (all categories) | 51.9 | 76.1 | 66.3 | 54.9 |
| Median ms per document | 0.05 | 66.43 | 192.14 | 144.05 |

Span leak rate by category (lower is better):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON (5250 spans) | 100.0% | 14.8% | 43.4% | 6.4% |
| ADDRESS (1000 spans) | 100.0% | 3.3% | 0.5% | 0.6% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON | 0.0 | 79.9 | 74.7 | 84.2 |
| ADDRESS | 0.0 | 98.8 | 97.2 | 99.9 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 98.3 | 99.8 |
| DATE | 100.0 | 100.0 | 98.1 | 100.0 |
| ID | 100.0 | 100.0 | 99.2 | 100.0 |
