## int4 open students, case_words: test_full

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **1.7%** | **12.7%** | **3.6%** |
| Span leak rate | 64.1% | 0.3% | 2.4% | 0.8% |
| Any-PII char precision | 88.8 | 88.6 | 83.0 | 88.7 |
| Any-PII char recall | 38.6 | 99.8 | 98.9 | 99.6 |
| Any-PII char F1 | 53.8 | 93.9 | 90.3 | 93.8 |
| Exact-span F1 (all categories) | 51.9 | 85.8 | 74.3 | 68.4 |
| Median ms per document | 0.05 | 59.13 | 157.28 | 125.61 |

Span leak rate by category (lower is better):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON (5250 spans) | 100.0% | 0.6% | 4.4% | 1.5% |
| ADDRESS (1000 spans) | 100.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON | 0.0 | 90.1 | 79.8 | 90.4 |
| ADDRESS | 0.0 | 99.7 | 94.8 | 100.0 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 94.5 | 100.0 |
| DATE | 100.0 | 100.0 | 98.6 | 100.0 |
| ID | 100.0 | 100.0 | 99.5 | 100.0 |
