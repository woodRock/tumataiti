## PII-Masking-300k, English validation (7,946 documents)

| Metric | rules | openai-privacy-filter | deberta-v3-small-v1 | deberta-v3-small | modernbert-base-v1 | modernbert-base | mdeberta-v3-base-v1 | mdeberta-v3-base | rules+openai-privacy-filter | rules+deberta-v3-small-v1 | rules+deberta-v3-small | rules+modernbert-base-v1 | rules+modernbert-base | rules+mdeberta-v3-base-v1 | rules+mdeberta-v3-base |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **95.9%** | **8.2%** | **5.0%** | **5.0%** | **5.9%** | **4.8%** | **5.0%** | **5.8%** | **7.8%** | **4.7%** | **4.7%** | **5.1%** | **4.6%** | **4.7%** | **5.5%** |
| Span leak rate | 85.4% | 2.8% | 1.3% | 1.3% | 1.7% | 1.4% | 1.4% | 1.6% | 2.7% | 1.3% | 1.2% | 1.5% | 1.4% | 1.4% | 1.6% |
| Any-PII char precision | 96.5 | 93.4 | 98.2 | 98.1 | 99.2 | 98.8 | 98.3 | 98.6 | 93.2 | 97.7 | 97.6 | 98.5 | 98.2 | 97.8 | 98.0 |
| Any-PII char recall | 20.1 | 97.6 | 98.9 | 98.9 | 98.8 | 99.0 | 98.8 | 98.7 | 97.8 | 98.9 | 99.0 | 99.0 | 99.0 | 98.9 | 98.8 |
| Any-PII char F1 | 33.2 | 95.5 | 98.6 | 98.5 | 99.0 | 98.9 | 98.6 | 98.6 | 95.5 | 98.3 | 98.3 | 98.8 | 98.6 | 98.3 | 98.4 |
| Exact-span F1 (all categories) | 23.9 | 81.8 | 96.8 | 96.7 | 95.9 | 95.7 | 88.2 | 88.3 | 84.1 | 95.9 | 95.8 | 95.2 | 94.9 | 87.7 | 87.8 |
| Median ms per document | 0.01 | 283.56 | 12.01 | 9.09 | 13.77 | 13.45 | 17.41 | 18.01 | 283.57 | 12.02 | 9.10 | 13.78 | 13.46 | 17.42 | 18.02 |

Span leak rate by category (lower is better):

| Metric | rules | openai-privacy-filter | deberta-v3-small-v1 | deberta-v3-small | modernbert-base-v1 | modernbert-base | mdeberta-v3-base-v1 | mdeberta-v3-base | rules+openai-privacy-filter | rules+deberta-v3-small-v1 | rules+deberta-v3-small | rules+modernbert-base-v1 | rules+modernbert-base | rules+mdeberta-v3-base-v1 | rules+mdeberta-v3-base |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5808 spans) | 99.9% | 3.9% | 2.2% | 2.1% | 2.6% | 2.7% | 2.6% | 2.9% | 3.8% | 2.2% | 2.1% | 2.6% | 2.7% | 2.6% | 2.9% |
| ADDRESS (8852 spans) | 100.0% | 4.2% | 1.0% | 1.1% | 1.4% | 1.1% | 1.0% | 1.2% | 4.2% | 1.0% | 1.1% | 1.4% | 1.1% | 1.0% | 1.2% |
| EMAIL (2612 spans) | 0.6% | 1.1% | 0.5% | 0.5% | 2.9% | 0.3% | 0.4% | 0.6% | 0.1% | 0.1% | 0.1% | 0.1% | 0.2% | 0.2% | 0.2% |
| PHONE (1997 spans) | 99.3% | 1.5% | 1.5% | 1.3% | 1.6% | 1.1% | 1.6% | 1.7% | 1.5% | 1.5% | 1.3% | 1.5% | 1.1% | 1.6% | 1.7% |
| IP_ADDRESS (2166 spans) | 50.4% | 2.3% | 1.2% | 1.3% | 0.5% | 0.6% | 1.3% | 1.2% | 1.9% | 0.9% | 1.0% | 0.5% | 0.6% | 1.0% | 0.9% |
| DATE (2317 spans) | 66.0% | 1.1% | 1.1% | 1.3% | 2.9% | 1.9% | 1.8% | 2.4% | 1.1% | 1.1% | 1.3% | 2.5% | 1.7% | 1.7% | 2.3% |
| ID (10054 spans) | 97.0% | 1.8% | 1.3% | 1.2% | 1.3% | 1.2% | 1.3% | 1.4% | 1.8% | 1.3% | 1.2% | 1.3% | 1.2% | 1.3% | 1.4% |
| SECRET (1620 spans) | 76.5% | 4.2% | 1.5% | 1.7% | 1.8% | 2.5% | 1.8% | 1.9% | 4.2% | 1.5% | 1.6% | 1.7% | 2.3% | 1.7% | 1.9% |

Character-level F1 by category (category must match):

| Metric | rules | openai-privacy-filter | deberta-v3-small-v1 | deberta-v3-small | modernbert-base-v1 | modernbert-base | mdeberta-v3-base-v1 | mdeberta-v3-base | rules+openai-privacy-filter | rules+deberta-v3-small-v1 | rules+deberta-v3-small | rules+modernbert-base-v1 | rules+modernbert-base | rules+mdeberta-v3-base-v1 | rules+mdeberta-v3-base |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 88.3 | 96.7 | 96.3 | 97.2 | 97.2 | 97.1 | 97.2 | 88.3 | 96.6 | 96.2 | 97.3 | 97.2 | 97.1 | 97.2 |
| ADDRESS | 0.0 | 95.0 | 97.9 | 97.9 | 98.9 | 98.1 | 98.0 | 98.4 | 95.0 | 97.9 | 97.9 | 98.9 | 98.1 | 98.0 | 98.4 |
| EMAIL | 98.1 | 96.7 | 99.1 | 99.1 | 98.7 | 99.3 | 99.0 | 99.0 | 97.3 | 98.2 | 98.2 | 98.2 | 98.1 | 98.1 | 98.1 |
| PHONE | 2.7 | 95.1 | 98.0 | 97.8 | 98.8 | 98.8 | 98.1 | 97.6 | 91.7 | 94.3 | 94.1 | 95.1 | 95.1 | 94.4 | 93.8 |
| IP_ADDRESS | 39.2 | 0.0 | 99.5 | 99.4 | 99.8 | 99.7 | 99.5 | 99.5 | 39.2 | 99.1 | 99.1 | 99.4 | 99.3 | 99.2 | 99.1 |
| DATE | 49.8 | 92.4 | 98.3 | 98.2 | 97.8 | 98.4 | 98.4 | 98.3 | 92.4 | 98.3 | 98.2 | 97.9 | 98.4 | 98.3 | 98.3 |
| ID | 2.9 | 96.9 | 98.5 | 98.6 | 99.1 | 99.0 | 98.6 | 98.5 | 96.0 | 97.6 | 97.6 | 98.1 | 98.1 | 97.7 | 97.6 |
| SECRET | 40.4 | 93.2 | 96.4 | 96.4 | 97.0 | 96.3 | 96.4 | 96.6 | 91.3 | 94.4 | 94.4 | 94.8 | 94.2 | 94.3 | 94.5 |
