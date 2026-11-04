## NZ synthetic v1, held-out templates and names (1,750 documents)

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **47.4%** | **0.3%** | **12.8%** | **5.4%** | **44.2%** | **0.3%** | **4.1%** | **2.7%** |
| Span leak rate | 64.1% | 22.1% | 0.1% | 2.4% | 1.0% | 19.2% | 0.1% | 0.8% | 0.5% |
| Any-PII char precision | 88.8 | 89.6 | 99.0 | 93.4 | 98.8 | 85.6 | 94.4 | 92.1 | 94.4 |
| Any-PII char recall | 38.6 | 85.1 | 100.0 | 98.3 | 99.5 | 87.7 | 100.0 | 99.6 | 99.7 |
| Any-PII char F1 | 53.8 | 87.3 | 99.5 | 95.8 | 99.2 | 86.6 | 97.1 | 95.7 | 97.0 |
| Exact-span F1 (all categories) | 51.9 | 59.3 | 93.4 | 85.4 | 62.7 | 64.2 | 92.2 | 87.8 | 73.3 |
| Median ms per document | 0.05 | 369.41 | 11.03 | 17.96 | 23.40 | 369.45 | 11.08 | 18.01 | 23.45 |

Span leak rate by category (lower is better):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5250 spans) | 100.0% | 35.0% | 0.1% | 1.5% | 1.0% | 35.0% | 0.1% | 1.5% | 1.0% |
| ADDRESS (1000 spans) | 100.0% | 3.3% | 0.0% | 0.0% | 0.0% | 3.3% | 0.0% | 0.0% | 0.0% |
| EMAIL (750 spans) | 0.0% | 0.3% | 0.0% | 0.5% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 12.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 12.8% | 0.0% | 30.4% | 9.8% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 4.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 76.0 | 98.5 | 94.8 | 98.3 | 76.7 | 98.5 | 94.8 | 98.3 |
| ADDRESS | 0.0 | 95.8 | 100.0 | 99.2 | 100.0 | 96.0 | 100.0 | 99.2 | 100.0 |
| EMAIL | 100.0 | 99.9 | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 84.3 | 100.0 | 99.0 | 99.7 | 99.8 | 100.0 | 99.0 | 99.9 |
| DATE | 100.0 | 54.8 | 100.0 | 83.9 | 97.2 | 63.6 | 100.0 | 98.6 | 100.0 |
| ID | 100.0 | 80.3 | 100.0 | 99.9 | 99.6 | 100.0 | 100.0 | 100.0 | 100.0 |
