## NZ synthetic v1, held-out templates and names (1,750 documents)

| Metric | rules | deberta-v3-small | deberta-v3-small-int8 | modernbert-base | modernbert-base-int8 | mdeberta-v3-base | mdeberta-v3-base-int8 | rules+deberta-v3-small | rules+deberta-v3-small-int8 | rules+modernbert-base | rules+modernbert-base-int8 | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **7.1%** | **16.2%** | **5.6%** | **60.7%** | **1.7%** | **99.4%** | **4.9%** | **11.8%** | **2.6%** | **25.9%** | **1.1%** | **63.7%** |
| Span leak rate | 64.1% | 1.3% | 3.2% | 1.1% | 15.0% | 0.3% | 51.9% | 0.9% | 2.4% | 0.6% | 6.4% | 0.2% | 23.2% |
| Any-PII char precision | 88.8 | 97.8 | 98.8 | 97.7 | 99.2 | 98.2 | 99.2 | 93.4 | 94.2 | 93.3 | 94.6 | 93.7 | 94.3 |
| Any-PII char recall | 38.6 | 99.6 | 98.9 | 99.6 | 92.6 | 99.9 | 66.3 | 99.7 | 99.1 | 99.7 | 97.7 | 99.9 | 88.7 |
| Any-PII char F1 | 53.8 | 98.7 | 98.9 | 98.6 | 95.8 | 99.0 | 79.5 | 96.4 | 96.6 | 96.4 | 96.1 | 96.7 | 91.4 |
| Exact-span F1 (all categories) | 51.9 | 90.8 | 89.6 | 88.9 | 72.4 | 60.4 | 24.1 | 90.1 | 89.7 | 90.0 | 82.8 | 70.9 | 50.5 |
| Median ms per document | 0.05 | 8.85 | 15.23 | 13.12 | 45.02 | 17.21 | 42.00 | 8.89 | 15.28 | 13.17 | 45.07 | 17.26 | 42.04 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small | deberta-v3-small-int8 | modernbert-base | modernbert-base-int8 | mdeberta-v3-base | mdeberta-v3-base-int8 | rules+deberta-v3-small | rules+deberta-v3-small-int8 | rules+modernbert-base | rules+modernbert-base-int8 | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5250 spans) | 100.0% | 1.6% | 4.5% | 1.1% | 11.4% | 0.4% | 38.8% | 1.6% | 4.5% | 1.1% | 11.4% | 0.4% | 38.8% |
| ADDRESS (1000 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 2.4% | 0.0% | 22.1% | 0.0% | 0.0% | 0.0% | 2.4% | 0.0% | 22.1% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.5% | 0.0% | 79.6% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 2.1% | 23.6% | 0.0% | 94.2% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 38.8% | 0.0% | 99.8% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 5.2% | 10.1% | 2.7% | 39.2% | 1.3% | 39.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small | deberta-v3-small-int8 | modernbert-base | modernbert-base-int8 | mdeberta-v3-base | mdeberta-v3-base-int8 | rules+deberta-v3-small | rules+deberta-v3-small-int8 | rules+modernbert-base | rules+modernbert-base-int8 | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 98.4 | 98.0 | 97.0 | 95.9 | 99.6 | 84.2 | 98.4 | 98.0 | 97.0 | 95.9 | 99.6 | 84.3 |
| ADDRESS | 0.0 | 100.0 | 100.0 | 100.0 | 99.7 | 100.0 | 90.0 | 100.0 | 100.0 | 100.0 | 99.7 | 100.0 | 96.4 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 57.5 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 99.6 | 98.4 | 97.9 | 92.4 | 97.4 | 6.1 | 99.8 | 99.8 | 99.3 | 100.0 | 99.9 | 100.0 |
| DATE | 100.0 | 88.9 | 95.3 | 99.2 | 85.4 | 86.0 | 24.0 | 88.9 | 95.3 | 99.2 | 100.0 | 86.0 | 99.9 |
| ID | 100.0 | 99.0 | 95.8 | 97.6 | 72.6 | 95.3 | 76.5 | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 | 100.0 |
