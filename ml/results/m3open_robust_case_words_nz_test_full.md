## int4 open students, case_words: test_full

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **3.5%** | **15.9%** | **3.5%** |
| Span leak rate | 76.6% | 0.6% | 3.4% | 0.7% |
| Any-PII char precision | 90.0 | 75.3 | 78.4 | 79.4 |
| Any-PII char recall | 26.0 | 99.7 | 98.5 | 99.6 |
| Any-PII char F1 | 40.4 | 85.8 | 87.3 | 88.4 |
| Exact-span F1 (all categories) | 37.5 | 63.2 | 61.6 | 55.9 |
| Median ms per document | 0.05 | 58.63 | 145.12 | 114.40 |

Span leak rate by category (lower is better):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON (6250 spans) | 100.0% | 0.4% | 6.4% | 1.4% |
| ADDRESS (1000 spans) | 100.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (5000 spans) | 100.0% | 1.5% | 2.9% | 0.3% |

Character-level F1 by category (category must match):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON | 0.0 | 87.7 | 82.8 | 77.8 |
| ADDRESS | 0.0 | 97.1 | 98.5 | 98.4 |
| EMAIL | 100.0 | 100.0 | 98.1 | 100.0 |
| PHONE | 100.0 | 100.0 | 96.3 | 98.8 |
| DATE | 100.0 | 100.0 | 97.1 | 100.0 |
| ID | 100.0 | 100.0 | 99.7 | 100.0 |
| AFFILIATION | 0.0 | 70.1 | 76.5 | 84.3 |
