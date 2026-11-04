## PII-Masking-300k, English validation (7,946 documents)

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **95.9%** | **8.2%** | **32.7%** | **44.0%** | **43.0%** | **7.8%** | **31.4%** | **35.9%** | **38.4%** |
| Span leak rate | 85.4% | 2.8% | 11.9% | 15.9% | 15.9% | 2.7% | 11.0% | 12.9% | 14.0% |
| Any-PII char precision | 96.5 | 93.4 | 95.0 | 94.6 | 95.1 | 93.2 | 94.9 | 94.5 | 94.9 |
| Any-PII char recall | 20.1 | 97.6 | 92.5 | 87.9 | 88.2 | 97.8 | 93.2 | 90.7 | 90.0 |
| Any-PII char F1 | 33.2 | 95.5 | 93.7 | 91.1 | 91.5 | 95.5 | 94.0 | 92.6 | 92.4 |
| Exact-span F1 (all categories) | 23.9 | 81.8 | 76.6 | 73.0 | 70.7 | 84.1 | 76.8 | 74.8 | 71.8 |
| Median ms per document | 0.01 | 283.56 | 11.45 | 18.11 | 23.39 | 283.57 | 11.46 | 18.12 | 23.40 |

Span leak rate by category (lower is better):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5808 spans) | 99.9% | 3.9% | 7.4% | 12.4% | 6.4% | 3.8% | 7.4% | 12.4% | 6.4% |
| ADDRESS (8852 spans) | 100.0% | 4.2% | 15.1% | 18.5% | 26.2% | 4.2% | 15.1% | 18.5% | 26.2% |
| EMAIL (2612 spans) | 0.6% | 1.1% | 0.1% | 10.3% | 0.3% | 0.1% | 0.1% | 0.1% | 0.1% |
| PHONE (1997 spans) | 99.3% | 1.5% | 1.8% | 3.1% | 2.2% | 1.5% | 1.8% | 3.1% | 2.2% |
| IP_ADDRESS (2166 spans) | 50.4% | 2.3% | 0.6% | 1.2% | 0.7% | 1.9% | 0.6% | 0.7% | 0.6% |
| DATE (2317 spans) | 66.0% | 1.1% | 67.2% | 98.9% | 88.0% | 1.1% | 54.3% | 65.2% | 59.0% |
| ID (10054 spans) | 97.0% | 1.8% | 3.2% | 5.0% | 7.5% | 1.8% | 3.2% | 5.0% | 7.4% |
| SECRET (1620 spans) | 76.5% | 4.2% | 31.6% | 8.0% | 5.6% | 4.2% | 31.4% | 7.9% | 5.6% |

Character-level F1 by category (category must match):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 88.3 | 89.9 | 84.4 | 91.2 | 88.3 | 89.9 | 84.4 | 91.2 |
| ADDRESS | 0.0 | 95.0 | 90.6 | 87.0 | 86.6 | 95.0 | 90.6 | 87.0 | 86.6 |
| EMAIL | 98.1 | 96.7 | 97.2 | 95.2 | 97.4 | 97.3 | 97.2 | 97.1 | 97.3 |
| PHONE | 2.7 | 95.1 | 84.8 | 88.6 | 86.8 | 91.7 | 82.1 | 85.7 | 83.6 |
| IP_ADDRESS | 39.2 | 0.0 | 92.1 | 95.0 | 95.7 | 39.2 | 92.1 | 95.0 | 95.6 |
| DATE | 49.8 | 92.4 | 63.2 | 9.0 | 37.7 | 92.4 | 70.9 | 54.2 | 64.6 |
| ID | 2.9 | 96.9 | 92.1 | 93.2 | 90.8 | 96.0 | 91.3 | 92.4 | 90.1 |
| SECRET | 40.4 | 93.2 | 76.1 | 79.2 | 90.0 | 91.3 | 74.4 | 78.1 | 88.2 |
