## PII-Masking-300k, English validation (7,946 documents)

| Metric | rules | deberta-v3-small | deberta-v3-small-int8-int4-block | modernbert-base | modernbert-base-int8-int4-block | mdeberta-v3-base | mdeberta-v3-base-int8-int4-block | rules+deberta-v3-small | rules+deberta-v3-small-int8-int4-block | rules+modernbert-base | rules+modernbert-base-int8-int4-block | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **95.9%** | **5.0%** | **5.2%** | **4.8%** | **5.2%** | **5.8%** | **6.4%** | **4.7%** | **4.9%** | **4.6%** | **5.0%** | **5.5%** | **6.0%** |
| Span leak rate | 85.4% | 1.3% | 1.3% | 1.4% | 1.5% | 1.6% | 1.7% | 1.2% | 1.3% | 1.4% | 1.5% | 1.6% | 1.7% |
| Any-PII char precision | 96.5 | 98.1 | 98.1 | 98.8 | 98.5 | 98.6 | 98.5 | 97.6 | 97.6 | 98.2 | 97.9 | 98.0 | 98.0 |
| Any-PII char recall | 20.1 | 98.9 | 98.9 | 99.0 | 98.9 | 98.7 | 98.7 | 99.0 | 98.9 | 99.0 | 99.0 | 98.8 | 98.7 |
| Any-PII char F1 | 33.2 | 98.5 | 98.5 | 98.9 | 98.7 | 98.6 | 98.6 | 98.3 | 98.3 | 98.6 | 98.4 | 98.4 | 98.4 |
| Exact-span F1 (all categories) | 23.9 | 96.7 | 96.7 | 95.7 | 93.8 | 88.3 | 88.2 | 95.8 | 95.8 | 94.9 | 92.9 | 87.8 | 87.7 |
| Median ms per document | 0.01 | 9.09 | 65.04 | 13.45 | 159.35 | 18.01 | 122.06 | 9.10 | 65.05 | 13.46 | 159.36 | 18.02 | 122.07 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small | deberta-v3-small-int8-int4-block | modernbert-base | modernbert-base-int8-int4-block | mdeberta-v3-base | mdeberta-v3-base-int8-int4-block | rules+deberta-v3-small | rules+deberta-v3-small-int8-int4-block | rules+modernbert-base | rules+modernbert-base-int8-int4-block | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5808 spans) | 99.9% | 2.1% | 2.2% | 2.7% | 3.0% | 2.9% | 3.0% | 2.1% | 2.2% | 2.7% | 3.0% | 2.9% | 3.0% |
| ADDRESS (8852 spans) | 100.0% | 1.1% | 1.2% | 1.1% | 1.1% | 1.2% | 1.3% | 1.1% | 1.2% | 1.1% | 1.1% | 1.2% | 1.3% |
| EMAIL (2612 spans) | 0.6% | 0.5% | 0.5% | 0.3% | 0.3% | 0.6% | 0.7% | 0.1% | 0.1% | 0.2% | 0.1% | 0.2% | 0.2% |
| PHONE (1997 spans) | 99.3% | 1.3% | 1.3% | 1.1% | 1.4% | 1.7% | 1.9% | 1.3% | 1.3% | 1.1% | 1.4% | 1.7% | 1.9% |
| IP_ADDRESS (2166 spans) | 50.4% | 1.3% | 1.2% | 0.6% | 0.6% | 1.2% | 1.4% | 1.0% | 1.0% | 0.6% | 0.6% | 0.9% | 1.0% |
| DATE (2317 spans) | 66.0% | 1.3% | 1.4% | 1.9% | 2.0% | 2.4% | 2.5% | 1.3% | 1.3% | 1.7% | 1.8% | 2.3% | 2.5% |
| ID (10054 spans) | 97.0% | 1.2% | 1.1% | 1.2% | 1.4% | 1.4% | 1.5% | 1.2% | 1.1% | 1.2% | 1.4% | 1.4% | 1.5% |
| SECRET (1620 spans) | 76.5% | 1.7% | 2.1% | 2.5% | 2.0% | 1.9% | 1.9% | 1.6% | 2.0% | 2.3% | 1.9% | 1.9% | 1.9% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small | deberta-v3-small-int8-int4-block | modernbert-base | modernbert-base-int8-int4-block | mdeberta-v3-base | mdeberta-v3-base-int8-int4-block | rules+deberta-v3-small | rules+deberta-v3-small-int8-int4-block | rules+modernbert-base | rules+modernbert-base-int8-int4-block | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 96.3 | 96.5 | 97.2 | 96.9 | 97.2 | 97.3 | 96.2 | 96.4 | 97.2 | 96.9 | 97.2 | 97.2 |
| ADDRESS | 0.0 | 97.9 | 97.9 | 98.1 | 98.0 | 98.4 | 98.3 | 97.9 | 97.9 | 98.1 | 98.0 | 98.4 | 98.3 |
| EMAIL | 98.1 | 99.1 | 99.1 | 99.3 | 99.0 | 99.0 | 99.0 | 98.2 | 98.2 | 98.1 | 97.8 | 98.1 | 98.2 |
| PHONE | 2.7 | 97.8 | 97.8 | 98.8 | 98.7 | 97.6 | 97.2 | 94.1 | 94.1 | 95.1 | 95.0 | 93.8 | 93.5 |
| IP_ADDRESS | 39.2 | 99.4 | 99.4 | 99.7 | 99.7 | 99.5 | 99.5 | 99.1 | 99.1 | 99.3 | 99.3 | 99.1 | 99.1 |
| DATE | 49.8 | 98.2 | 98.2 | 98.4 | 96.8 | 98.3 | 98.2 | 98.2 | 98.2 | 98.4 | 96.8 | 98.3 | 98.2 |
| ID | 2.9 | 98.6 | 98.6 | 99.0 | 99.0 | 98.5 | 98.5 | 97.6 | 97.6 | 98.1 | 98.1 | 97.6 | 97.5 |
| SECRET | 40.4 | 96.4 | 96.4 | 96.3 | 96.1 | 96.6 | 96.6 | 94.4 | 94.4 | 94.2 | 94.0 | 94.5 | 94.5 |
