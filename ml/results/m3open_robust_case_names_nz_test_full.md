## int4 open students, case_names: test_full

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **92.8%** | **93.6%** | **55.7%** |
| Span leak rate | 76.6% | 33.7% | 33.3% | 16.8% |
| Any-PII char precision | 90.0 | 91.0 | 90.7 | 91.4 |
| Any-PII char recall | 26.0 | 76.7 | 76.2 | 89.9 |
| Any-PII char F1 | 40.4 | 83.2 | 82.8 | 90.6 |
| Exact-span F1 (all categories) | 37.5 | 69.3 | 67.2 | 65.1 |
| Median ms per document | 0.04 | 58.99 | 153.05 | 118.83 |

Span leak rate by category (lower is better):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON (6250 spans) | 100.0% | 85.4% | 84.4% | 42.9% |
| ADDRESS (1000 spans) | 100.0% | 0.0% | 0.1% | 0.0% |
| EMAIL (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (5000 spans) | 100.0% | 1.1% | 1.2% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON | 0.0 | 34.4 | 31.2 | 74.1 |
| ADDRESS | 0.0 | 96.7 | 98.7 | 97.7 |
| EMAIL | 100.0 | 100.0 | 97.3 | 100.0 |
| PHONE | 100.0 | 100.0 | 98.2 | 100.0 |
| DATE | 100.0 | 100.0 | 91.2 | 100.0 |
| ID | 100.0 | 100.0 | 100.0 | 100.0 |
| AFFILIATION | 0.0 | 94.4 | 96.6 | 94.6 |
