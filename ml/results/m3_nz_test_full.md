## NZ synthetic v1, held-out templates and names (1,750 documents)

| Metric | rules | openai-privacy-filter | deberta-v3-small | deberta-v3-small-int8 | modernbert-base | mdeberta-v3-base | rules+openai-privacy-filter | rules+deberta-v3-small | rules+deberta-v3-small-int8 | rules+modernbert-base | rules+mdeberta-v3-base |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **47.4%** | **32.6%** | **37.0%** | **46.2%** | **9.7%** | **44.2%** | **29.9%** | **32.4%** | **31.4%** | **9.2%** |
| Span leak rate | 64.1% | 22.1% | 6.9% | 9.2% | 12.3% | 1.9% | 19.2% | 6.4% | 8.4% | 9.5% | 1.8% |
| Any-PII char precision | 88.8 | 89.6 | 95.4 | 96.2 | 97.4 | 94.4 | 85.6 | 91.0 | 91.7 | 92.8 | 90.3 |
| Any-PII char recall | 38.6 | 85.1 | 97.0 | 95.3 | 93.4 | 99.2 | 87.7 | 97.1 | 95.5 | 94.6 | 99.2 |
| Any-PII char F1 | 53.8 | 87.3 | 96.2 | 95.7 | 95.4 | 96.7 | 86.6 | 94.0 | 93.6 | 93.7 | 94.5 |
| Exact-span F1 (all categories) | 51.9 | 59.3 | 82.6 | 80.6 | 78.9 | 55.8 | 64.2 | 82.8 | 81.5 | 81.5 | 65.3 |
| Median ms per document | 0.05 | 369.41 | 12.01 | 14.74 | 13.19 | 17.47 | 369.45 | 12.06 | 14.79 | 13.24 | 17.52 |

Span leak rate by category (lower is better):

| Metric | rules | openai-privacy-filter | deberta-v3-small | deberta-v3-small-int8 | modernbert-base | mdeberta-v3-base | rules+openai-privacy-filter | rules+deberta-v3-small | rules+deberta-v3-small-int8 | rules+modernbert-base | rules+mdeberta-v3-base |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5250 spans) | 100.0% | 35.0% | 11.8% | 15.6% | 17.7% | 3.3% | 35.0% | 11.8% | 15.6% | 17.7% | 3.3% |
| ADDRESS (1000 spans) | 100.0% | 3.3% | 0.0% | 0.0% | 0.0% | 0.0% | 3.3% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (750 spans) | 0.0% | 0.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 12.3% | 0.0% | 0.0% | 2.9% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 12.8% | 0.0% | 0.0% | 0.4% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 4.3% | 6.3% | 10.8% | 29.2% | 1.1% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | openai-privacy-filter | deberta-v3-small | deberta-v3-small-int8 | modernbert-base | mdeberta-v3-base | rules+openai-privacy-filter | rules+deberta-v3-small | rules+deberta-v3-small-int8 | rules+modernbert-base | rules+mdeberta-v3-base |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 76.0 | 93.6 | 91.5 | 89.5 | 95.5 | 76.7 | 93.6 | 91.5 | 89.5 | 95.5 |
| ADDRESS | 0.0 | 95.8 | 100.0 | 100.0 | 100.0 | 100.0 | 96.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| EMAIL | 100.0 | 99.9 | 100.0 | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 84.3 | 98.9 | 98.0 | 97.1 | 95.5 | 99.8 | 100.0 | 100.0 | 100.0 | 98.4 |
| DATE | 100.0 | 54.8 | 79.0 | 84.7 | 99.9 | 79.6 | 63.6 | 79.0 | 84.7 | 100.0 | 79.6 |
| ID | 100.0 | 80.3 | 97.2 | 94.3 | 86.9 | 94.5 | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 |
