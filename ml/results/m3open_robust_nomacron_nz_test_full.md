## int4 open students, nomacron: test_full

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **5.9%** | **9.3%** | **2.7%** |
| Span leak rate | 76.6% | 1.2% | 1.8% | 0.5% |
| Any-PII char precision | 90.0 | 91.2 | 92.7 | 91.4 |
| Any-PII char recall | 26.0 | 99.3 | 99.2 | 99.7 |
| Any-PII char F1 | 40.4 | 95.1 | 95.8 | 95.4 |
| Exact-span F1 (all categories) | 37.5 | 79.5 | 83.0 | 67.5 |
| Median ms per document | 0.01 | 58.09 | 157.12 | 117.97 |

Span leak rate by category (lower is better):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON (6250 spans) | 100.0% | 0.0% | 2.2% | 1.1% |
| ADDRESS (1000 spans) | 100.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (5000 spans) | 100.0% | 3.9% | 3.0% | 0.1% |

Character-level F1 by category (category must match):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON | 0.0 | 94.7 | 95.6 | 82.8 |
| ADDRESS | 0.0 | 90.5 | 97.5 | 94.7 |
| EMAIL | 100.0 | 100.0 | 97.1 | 100.0 |
| PHONE | 100.0 | 100.0 | 98.3 | 100.0 |
| DATE | 100.0 | 100.0 | 90.1 | 100.0 |
| ID | 100.0 | 100.0 | 100.0 | 100.0 |
| AFFILIATION | 0.0 | 89.0 | 96.1 | 78.9 |
