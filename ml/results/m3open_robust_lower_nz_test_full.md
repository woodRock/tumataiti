## int4 open students, lower: test_full

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **96.5%** | **98.0%** | **57.6%** |
| Span leak rate | 78.1% | 61.2% | 53.8% | 16.6% |
| Any-PII char precision | 89.7 | 93.7 | 92.1 | 92.9 |
| Any-PII char recall | 25.1 | 51.0 | 59.4 | 91.2 |
| Any-PII char F1 | 39.2 | 66.0 | 72.2 | 92.1 |
| Exact-span F1 (all categories) | 35.4 | 45.4 | 47.9 | 59.6 |
| Median ms per document | 0.03 | 68.91 | 170.69 | 118.10 |

Span leak rate by category (lower is better):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON (6250 spans) | 100.0% | 82.9% | 72.9% | 25.1% |
| ADDRESS (1000 spans) | 100.0% | 22.3% | 0.6% | 8.8% |
| EMAIL (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 33.3% | 2.7% | 21.1% | 30.3% |
| AFFILIATION (5000 spans) | 100.0% | 87.4% | 77.9% | 15.4% |

Character-level F1 by category (category must match):

| Metric | rules | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|
| PERSON | 0.0 | 39.2 | 53.8 | 86.6 |
| ADDRESS | 0.0 | 94.2 | 99.2 | 98.4 |
| EMAIL | 100.0 | 100.0 | 96.8 | 100.0 |
| PHONE | 100.0 | 100.0 | 98.1 | 99.9 |
| DATE | 100.0 | 99.9 | 92.2 | 99.8 |
| ID | 87.1 | 98.9 | 91.7 | 88.1 |
| AFFILIATION | 0.0 | 30.4 | 46.8 | 90.9 |
