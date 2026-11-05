## int4 open students, nomacron: test_full

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **0.9%** | **3.0%** | **1.1%** |
| Span leak rate | 64.1% | 0.2% | 0.6% | 0.2% |
| Any-PII char precision | 88.8 | 93.7 | 91.9 | 94.6 |
| Any-PII char recall | 38.6 | 99.9 | 99.7 | 99.9 |
| Any-PII char F1 | 53.8 | 96.7 | 95.7 | 97.2 |
| Exact-span F1 (all categories) | 51.9 | 91.4 | 85.7 | 75.2 |
| Median ms per document | 0.01 | 46.20 | 114.38 | 87.49 |

Span leak rate by category (lower is better):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON (5250 spans) | 100.0% | 0.3% | 1.0% | 0.4% |
| ADDRESS (1000 spans) | 100.0% | 0.1% | 0.0% | 0.0% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON | 0.0 | 97.4 | 93.9 | 98.8 |
| ADDRESS | 0.0 | 99.9 | 97.6 | 100.0 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 99.0 | 100.0 |
| DATE | 100.0 | 100.0 | 98.5 | 100.0 |
| ID | 100.0 | 100.0 | 100.0 | 99.9 |
