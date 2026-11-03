## NZ synthetic v1, held-out templates and names (1,750 documents)

| Metric | rules | openai-privacy-filter | deberta-v3-small-v1 | deberta-v3-small | modernbert-base-v1 | modernbert-base | mdeberta-v3-base-v1 | mdeberta-v3-base | rules+openai-privacy-filter | rules+deberta-v3-small-v1 | rules+deberta-v3-small | rules+modernbert-base-v1 | rules+modernbert-base | rules+mdeberta-v3-base-v1 | rules+mdeberta-v3-base |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **47.4%** | **32.6%** | **7.1%** | **46.2%** | **5.6%** | **9.7%** | **1.7%** | **44.2%** | **29.9%** | **4.9%** | **31.4%** | **2.6%** | **9.2%** | **1.1%** |
| Span leak rate | 64.1% | 22.1% | 6.9% | 1.3% | 12.3% | 1.1% | 1.9% | 0.3% | 19.2% | 6.4% | 0.9% | 9.5% | 0.6% | 1.8% | 0.2% |
| Any-PII char precision | 88.8 | 89.6 | 95.4 | 97.8 | 97.4 | 97.7 | 94.4 | 98.2 | 85.6 | 91.0 | 93.4 | 92.8 | 93.3 | 90.3 | 93.7 |
| Any-PII char recall | 38.6 | 85.1 | 97.0 | 99.6 | 93.4 | 99.6 | 99.2 | 99.9 | 87.7 | 97.1 | 99.7 | 94.6 | 99.7 | 99.2 | 99.9 |
| Any-PII char F1 | 53.8 | 87.3 | 96.2 | 98.7 | 95.4 | 98.6 | 96.7 | 99.0 | 86.6 | 94.0 | 96.4 | 93.7 | 96.4 | 94.5 | 96.7 |
| Exact-span F1 (all categories) | 51.9 | 59.3 | 82.6 | 90.8 | 78.9 | 88.9 | 55.8 | 60.4 | 64.2 | 82.8 | 90.1 | 81.5 | 90.0 | 65.3 | 70.9 |
| Median ms per document | 0.05 | 369.41 | 12.01 | 8.85 | 13.19 | 13.12 | 17.47 | 17.21 | 369.45 | 12.06 | 8.89 | 13.24 | 13.17 | 17.52 | 17.26 |

Span leak rate by category (lower is better):

| Metric | rules | openai-privacy-filter | deberta-v3-small-v1 | deberta-v3-small | modernbert-base-v1 | modernbert-base | mdeberta-v3-base-v1 | mdeberta-v3-base | rules+openai-privacy-filter | rules+deberta-v3-small-v1 | rules+deberta-v3-small | rules+modernbert-base-v1 | rules+modernbert-base | rules+mdeberta-v3-base-v1 | rules+mdeberta-v3-base |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5250 spans) | 100.0% | 35.0% | 11.8% | 1.6% | 17.7% | 1.1% | 3.3% | 0.4% | 35.0% | 11.8% | 1.6% | 17.7% | 1.1% | 3.3% | 0.4% |
| ADDRESS (1000 spans) | 100.0% | 3.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 3.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (750 spans) | 0.0% | 0.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 12.3% | 0.0% | 0.0% | 2.9% | 2.1% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 12.8% | 0.0% | 0.0% | 0.4% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 4.3% | 6.3% | 5.2% | 29.2% | 2.7% | 1.1% | 1.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | openai-privacy-filter | deberta-v3-small-v1 | deberta-v3-small | modernbert-base-v1 | modernbert-base | mdeberta-v3-base-v1 | mdeberta-v3-base | rules+openai-privacy-filter | rules+deberta-v3-small-v1 | rules+deberta-v3-small | rules+modernbert-base-v1 | rules+modernbert-base | rules+mdeberta-v3-base-v1 | rules+mdeberta-v3-base |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 76.0 | 93.6 | 98.4 | 89.5 | 97.0 | 95.5 | 99.6 | 76.7 | 93.6 | 98.4 | 89.5 | 97.0 | 95.5 | 99.6 |
| ADDRESS | 0.0 | 95.8 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 96.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| EMAIL | 100.0 | 99.9 | 100.0 | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 84.3 | 98.9 | 99.6 | 97.1 | 97.9 | 95.5 | 97.4 | 99.8 | 100.0 | 99.8 | 100.0 | 99.3 | 98.4 | 99.9 |
| DATE | 100.0 | 54.8 | 79.0 | 88.9 | 99.9 | 99.2 | 79.6 | 86.0 | 63.6 | 79.0 | 88.9 | 100.0 | 99.2 | 79.6 | 86.0 |
| ID | 100.0 | 80.3 | 97.2 | 99.0 | 86.9 | 97.6 | 94.5 | 95.3 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 | 99.9 |
