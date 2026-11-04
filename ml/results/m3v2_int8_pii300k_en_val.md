## PII-Masking-300k, English validation (7,946 documents)

| Metric | rules | deberta-v3-small | deberta-v3-small-int8 | modernbert-base | modernbert-base-int8 | mdeberta-v3-base | mdeberta-v3-base-int8 | rules+deberta-v3-small | rules+deberta-v3-small-int8 | rules+modernbert-base | rules+modernbert-base-int8 | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **95.9%** | **5.0%** | **6.5%** | **4.8%** | **16.9%** | **5.8%** | **81.4%** | **4.7%** | **6.1%** | **4.6%** | **15.4%** | **5.5%** | **69.7%** |
| Span leak rate | 85.4% | 1.3% | 1.6% | 1.4% | 4.8% | 1.6% | 41.8% | 1.2% | 1.5% | 1.4% | 4.3% | 1.6% | 30.1% |
| Any-PII char precision | 96.5 | 98.1 | 98.4 | 98.8 | 98.9 | 98.6 | 99.2 | 97.6 | 97.8 | 98.2 | 98.3 | 98.0 | 98.4 |
| Any-PII char recall | 20.1 | 98.9 | 98.7 | 99.0 | 97.0 | 98.7 | 63.1 | 99.0 | 98.8 | 99.0 | 97.3 | 98.8 | 74.8 |
| Any-PII char F1 | 33.2 | 98.5 | 98.6 | 98.9 | 98.0 | 98.6 | 77.1 | 98.3 | 98.3 | 98.6 | 97.8 | 98.4 | 85.0 |
| Exact-span F1 (all categories) | 23.9 | 96.7 | 96.8 | 95.7 | 90.6 | 88.3 | 55.1 | 95.8 | 95.9 | 94.9 | 90.9 | 87.8 | 66.5 |
| Median ms per document | 0.01 | 9.09 | 25.12 | 13.45 | 61.93 | 18.01 | 59.91 | 9.10 | 25.13 | 13.46 | 61.94 | 18.02 | 59.92 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small | deberta-v3-small-int8 | modernbert-base | modernbert-base-int8 | mdeberta-v3-base | mdeberta-v3-base-int8 | rules+deberta-v3-small | rules+deberta-v3-small-int8 | rules+modernbert-base | rules+modernbert-base-int8 | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5808 spans) | 99.9% | 2.1% | 2.8% | 2.7% | 6.3% | 2.9% | 27.9% | 2.1% | 2.8% | 2.7% | 6.2% | 2.9% | 27.9% |
| ADDRESS (8852 spans) | 100.0% | 1.1% | 1.5% | 1.1% | 2.8% | 1.2% | 23.3% | 1.1% | 1.5% | 1.1% | 2.8% | 1.2% | 23.3% |
| EMAIL (2612 spans) | 0.6% | 0.5% | 0.7% | 0.3% | 1.4% | 0.6% | 82.6% | 0.1% | 0.1% | 0.2% | 0.2% | 0.2% | 0.4% |
| PHONE (1997 spans) | 99.3% | 1.3% | 1.7% | 1.1% | 5.3% | 1.7% | 99.3% | 1.3% | 1.7% | 1.1% | 5.2% | 1.7% | 98.1% |
| IP_ADDRESS (2166 spans) | 50.4% | 1.3% | 1.4% | 0.6% | 13.7% | 1.2% | 99.4% | 1.0% | 1.0% | 0.6% | 8.4% | 0.9% | 50.4% |
| DATE (2317 spans) | 66.0% | 1.3% | 1.3% | 1.9% | 5.5% | 2.4% | 95.3% | 1.3% | 1.2% | 1.7% | 4.9% | 2.3% | 63.0% |
| ID (10054 spans) | 97.0% | 1.2% | 1.3% | 1.2% | 3.1% | 1.4% | 20.0% | 1.2% | 1.3% | 1.2% | 3.0% | 1.4% | 19.5% |
| SECRET (1620 spans) | 76.5% | 1.7% | 1.8% | 2.5% | 12.9% | 1.9% | 37.2% | 1.6% | 1.7% | 2.3% | 12.3% | 1.9% | 29.8% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small | deberta-v3-small-int8 | modernbert-base | modernbert-base-int8 | mdeberta-v3-base | mdeberta-v3-base-int8 | rules+deberta-v3-small | rules+deberta-v3-small-int8 | rules+modernbert-base | rules+modernbert-base-int8 | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 96.3 | 96.3 | 97.2 | 96.2 | 97.2 | 89.1 | 96.2 | 96.3 | 97.2 | 96.2 | 97.2 | 89.1 |
| ADDRESS | 0.0 | 97.9 | 98.0 | 98.1 | 97.7 | 98.4 | 89.7 | 97.9 | 98.0 | 98.1 | 97.7 | 98.4 | 89.7 |
| EMAIL | 98.1 | 99.1 | 99.1 | 99.3 | 99.1 | 99.0 | 57.3 | 98.2 | 98.2 | 98.1 | 98.1 | 98.1 | 98.2 |
| PHONE | 2.7 | 97.8 | 97.9 | 98.8 | 97.6 | 97.6 | 8.8 | 94.1 | 94.3 | 95.1 | 94.0 | 93.8 | 10.7 |
| IP_ADDRESS | 39.2 | 99.4 | 99.4 | 99.7 | 96.7 | 99.5 | 10.7 | 99.1 | 99.0 | 99.3 | 97.1 | 99.1 | 40.2 |
| DATE | 49.8 | 98.2 | 98.4 | 98.4 | 97.5 | 98.3 | 50.8 | 98.2 | 98.4 | 98.4 | 97.5 | 98.3 | 71.6 |
| ID | 2.9 | 98.6 | 98.6 | 99.0 | 98.5 | 98.5 | 92.9 | 97.6 | 97.7 | 98.1 | 97.5 | 97.6 | 92.0 |
| SECRET | 40.4 | 96.4 | 96.6 | 96.3 | 92.9 | 96.6 | 87.4 | 94.4 | 94.5 | 94.2 | 91.0 | 94.5 | 87.4 |
