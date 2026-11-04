## NZ synthetic v1, held-out templates and names (1,750 documents)

| Metric | rules | deberta-v3-small | deberta-v3-small-int8-int4-block | modernbert-base | modernbert-base-int8-int4-block | mdeberta-v3-base | mdeberta-v3-base-int8-int4-block | rules+deberta-v3-small | rules+deberta-v3-small-int8-int4-block | rules+modernbert-base | rules+modernbert-base-int8-int4-block | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **7.1%** | **5.9%** | **5.6%** | **5.3%** | **1.7%** | **1.7%** | **4.9%** | **3.5%** | **2.6%** | **4.0%** | **1.1%** | **0.9%** |
| Span leak rate | 64.1% | 1.3% | 1.1% | 1.1% | 1.0% | 0.3% | 0.3% | 0.9% | 0.6% | 0.6% | 0.8% | 0.2% | 0.2% |
| Any-PII char precision | 88.8 | 97.8 | 98.4 | 97.7 | 97.2 | 98.2 | 98.6 | 93.4 | 93.9 | 93.3 | 92.8 | 93.7 | 94.1 |
| Any-PII char recall | 38.6 | 99.6 | 99.7 | 99.6 | 99.6 | 99.9 | 99.9 | 99.7 | 99.8 | 99.7 | 99.7 | 99.9 | 99.9 |
| Any-PII char F1 | 53.8 | 98.7 | 99.0 | 98.6 | 98.4 | 99.0 | 99.2 | 96.4 | 96.7 | 96.4 | 96.1 | 96.7 | 96.9 |
| Exact-span F1 (all categories) | 51.9 | 90.8 | 91.4 | 88.9 | 85.5 | 60.4 | 60.0 | 90.1 | 90.7 | 90.0 | 87.4 | 70.9 | 70.4 |
| Median ms per document | 0.05 | 8.85 | 40.01 | 13.12 | 109.67 | 17.21 | 83.93 | 8.89 | 40.05 | 13.17 | 109.71 | 17.26 | 83.97 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small | deberta-v3-small-int8-int4-block | modernbert-base | modernbert-base-int8-int4-block | mdeberta-v3-base | mdeberta-v3-base-int8-int4-block | rules+deberta-v3-small | rules+deberta-v3-small-int8-int4-block | rules+modernbert-base | rules+modernbert-base-int8-int4-block | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5250 spans) | 100.0% | 1.6% | 1.2% | 1.1% | 1.4% | 0.4% | 0.3% | 1.6% | 1.2% | 1.1% | 1.4% | 0.4% | 0.3% |
| ADDRESS (1000 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 2.1% | 1.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 5.2% | 5.6% | 2.7% | 0.5% | 1.3% | 1.7% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small | deberta-v3-small-int8-int4-block | modernbert-base | modernbert-base-int8-int4-block | mdeberta-v3-base | mdeberta-v3-base-int8-int4-block | rules+deberta-v3-small | rules+deberta-v3-small-int8-int4-block | rules+modernbert-base | rules+modernbert-base-int8-int4-block | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 98.4 | 98.4 | 97.0 | 96.9 | 99.6 | 99.6 | 98.4 | 98.4 | 97.0 | 96.9 | 99.6 | 99.6 |
| ADDRESS | 0.0 | 100.0 | 100.0 | 100.0 | 99.3 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.3 | 100.0 | 100.0 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 99.6 | 99.4 | 97.9 | 96.6 | 97.4 | 95.6 | 99.8 | 99.5 | 99.3 | 99.8 | 99.9 | 99.0 |
| DATE | 100.0 | 88.9 | 94.4 | 99.2 | 95.7 | 86.0 | 91.7 | 88.9 | 94.4 | 99.2 | 95.7 | 86.0 | 91.7 |
| ID | 100.0 | 99.0 | 99.1 | 97.6 | 93.9 | 95.3 | 93.5 | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 | 99.8 |
