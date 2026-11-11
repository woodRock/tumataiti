## NZ synthetic v4, held-out templates, names and affiliations

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **66.7%** | **2.3%** | **6.9%** | **2.7%** | **64.7%** | **2.0%** | **3.8%** | **2.5%** |
| Span leak rate | 76.6% | 42.7% | 0.4% | 1.2% | 0.5% | 40.8% | 0.4% | 0.7% | 0.4% |
| Any-PII char precision | 90.0 | 89.2 | 94.5 | 96.2 | 94.8 | 86.0 | 92.0 | 93.6 | 92.4 |
| Any-PII char recall | 26.0 | 62.5 | 99.8 | 99.4 | 99.7 | 64.2 | 99.8 | 99.7 | 99.7 |
| Any-PII char F1 | 40.4 | 73.5 | 97.1 | 97.7 | 97.2 | 73.5 | 95.7 | 96.5 | 95.9 |
| Exact-span F1 (all categories) | 37.5 | 45.7 | 83.9 | 87.4 | 69.9 | 49.3 | 83.5 | 87.4 | 76.1 |
| Median ms per document | 0.05 | 293.44 | 9.86 | 13.80 | 18.52 | 293.49 | 9.91 | 13.84 | 18.56 |

Span leak rate by category (lower is better):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (6250 spans) | 100.0% | 40.9% | 0.1% | 1.2% | 1.1% | 40.9% | 0.1% | 1.2% | 1.1% |
| ADDRESS (1000 spans) | 100.0% | 4.0% | 0.0% | 0.0% | 0.0% | 4.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (1000 spans) | 0.0% | 0.5% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 12.7% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 12.8% | 1.4% | 17.0% | 0.6% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 6.1% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (5000 spans) | 100.0% | 78.7% | 1.0% | 0.6% | 0.0% | 78.7% | 1.0% | 0.6% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 64.1 | 96.2 | 94.8 | 96.0 | 64.4 | 96.2 | 94.8 | 96.0 |
| ADDRESS | 0.0 | 93.0 | 96.3 | 97.8 | 97.4 | 93.4 | 96.3 | 97.8 | 97.4 |
| EMAIL | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 84.6 | 100.0 | 98.6 | 100.0 | 99.8 | 100.0 | 98.6 | 100.0 |
| DATE | 100.0 | 49.2 | 99.7 | 92.1 | 99.9 | 57.2 | 100.0 | 98.2 | 100.0 |
| ID | 100.0 | 81.1 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| AFFILIATION | 0.0 | 0.0 | 91.7 | 95.3 | 95.6 | 0.0 | 91.7 | 95.3 | 95.6 |
