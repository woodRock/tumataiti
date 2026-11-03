## PII-Masking-300k, English validation (7,946 documents)

| Metric | rules | openai-privacy-filter | rules+openai-privacy-filter |
|---|---:|---:|---:|
| **Document leak rate** (lower is better) | **95.9%** | **8.2%** | **7.8%** |
| Span leak rate | 85.6% | 2.8% | 2.7% |
| Any-PII char precision | 96.5 | 93.4 | 93.2 |
| Any-PII char recall | 19.9 | 97.6 | 97.8 |
| Any-PII char F1 | 32.9 | 95.5 | 95.5 |
| Exact-span F1 (all categories) | 23.7 | 81.8 | 84.1 |
| Median ms per document | 0.01 | 283.56 | 283.57 |

Span leak rate by category (lower is better):

| Metric | rules | openai-privacy-filter | rules+openai-privacy-filter |
|---|---:|---:|---:|
| PERSON (5808 spans) | 99.9% | 3.9% | 3.8% |
| ADDRESS (8852 spans) | 100.0% | 4.2% | 4.2% |
| EMAIL (2612 spans) | 0.6% | 1.1% | 0.1% |
| PHONE (1997 spans) | 99.3% | 1.5% | 1.5% |
| IP_ADDRESS (2166 spans) | 50.4% | 2.3% | 1.9% |
| DATE (2317 spans) | 66.0% | 1.1% | 1.1% |
| ID (10054 spans) | 97.5% | 1.8% | 1.8% |
| SECRET (1620 spans) | 76.5% | 4.2% | 4.2% |

Character-level F1 by category (category must match):

| Metric | rules | openai-privacy-filter | rules+openai-privacy-filter |
|---|---:|---:|---:|
| PERSON | 0.0 | 88.3 | 88.3 |
| ADDRESS | 0.0 | 95.0 | 95.0 |
| EMAIL | 98.1 | 96.7 | 97.3 |
| PHONE | 2.7 | 95.1 | 91.7 |
| IP_ADDRESS | 39.2 | 0.0 | 39.2 |
| DATE | 49.8 | 92.4 | 92.4 |
| ID | 1.4 | 96.9 | 96.0 |
| SECRET | 40.4 | 93.2 | 91.3 |
