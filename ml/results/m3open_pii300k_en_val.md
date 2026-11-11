## PII-Masking-300k, English validation

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **95.9%** | **8.2%** | **35.1%** | **51.3%** | **41.8%** | **7.8%** | **32.3%** | **42.0%** | **38.0%** |
| Span leak rate | 85.4% | 2.8% | 12.7% | 20.8% | 13.9% | 2.7% | 11.4% | 17.1% | 12.2% |
| Any-PII char precision | 96.5 | 93.4 | 95.0 | 94.8 | 94.9 | 93.2 | 94.9 | 94.8 | 94.8 |
| Any-PII char recall | 20.1 | 97.6 | 92.2 | 83.9 | 88.9 | 97.8 | 93.0 | 87.3 | 90.6 |
| Any-PII char F1 | 33.2 | 95.5 | 93.6 | 89.0 | 91.8 | 95.5 | 93.9 | 90.9 | 92.6 |
| Exact-span F1 (all categories) | 23.9 | 81.8 | 77.1 | 70.0 | 71.3 | 84.1 | 77.9 | 73.4 | 72.4 |
| Median ms per document | 0.01 | 283.56 | 17.08 | 14.09 | 16.70 | 283.57 | 17.09 | 14.10 | 16.71 |

Span leak rate by category (lower is better):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5808 spans) | 99.9% | 3.9% | 5.4% | 21.8% | 3.8% | 3.8% | 5.4% | 21.7% | 3.8% |
| ADDRESS (8852 spans) | 100.0% | 4.2% | 18.4% | 26.2% | 15.0% | 4.2% | 18.4% | 26.2% | 15.0% |
| EMAIL (2612 spans) | 0.6% | 1.1% | 1.0% | 19.8% | 1.1% | 0.1% | 0.1% | 0.1% | 0.1% |
| PHONE (1997 spans) | 99.3% | 1.5% | 1.9% | 2.4% | 1.5% | 1.5% | 1.9% | 2.3% | 1.5% |
| IP_ADDRESS (2166 spans) | 50.4% | 2.3% | 0.6% | 1.1% | 0.6% | 1.9% | 0.6% | 0.7% | 0.6% |
| DATE (2317 spans) | 66.0% | 1.1% | 75.1% | 98.1% | 79.9% | 1.1% | 56.3% | 65.2% | 57.3% |
| ID (10054 spans) | 97.0% | 1.8% | 3.4% | 8.1% | 13.6% | 1.8% | 3.4% | 8.1% | 13.0% |
| SECRET (1620 spans) | 76.5% | 4.2% | 24.1% | 7.0% | 4.6% | 4.2% | 24.1% | 7.0% | 4.6% |

Character-level F1 by category (category must match):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 88.3 | 91.3 | 83.0 | 93.3 | 88.3 | 91.3 | 83.0 | 93.2 |
| ADDRESS | 0.0 | 95.0 | 90.1 | 85.3 | 92.5 | 95.0 | 90.1 | 85.3 | 92.5 |
| EMAIL | 98.1 | 96.7 | 96.9 | 92.6 | 97.1 | 97.3 | 97.3 | 97.3 | 97.4 |
| PHONE | 2.7 | 95.1 | 87.4 | 87.3 | 83.9 | 91.7 | 84.6 | 85.1 | 82.1 |
| IP_ADDRESS | 39.2 | 0.0 | 93.4 | 95.1 | 93.7 | 39.2 | 93.4 | 95.0 | 93.7 |
| DATE | 49.8 | 92.4 | 59.1 | 10.2 | 49.5 | 92.4 | 69.0 | 52.9 | 68.4 |
| ID | 2.9 | 96.9 | 93.1 | 90.9 | 85.0 | 96.0 | 92.3 | 90.2 | 84.9 |
| SECRET | 40.4 | 93.2 | 79.3 | 79.5 | 85.7 | 91.3 | 78.7 | 78.8 | 84.5 |
