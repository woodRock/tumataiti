## Open English PII test set: Nemotron-PII + Gretel-en (2,000 documents)

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **96.4%** | **40.0%** | **3.3%** | **1.9%** | **4.0%** | **32.3%** | **3.1%** | **1.7%** | **3.5%** |
| Span leak rate | 74.5% | 16.3% | 1.2% | 0.8% | 1.4% | 11.7% | 1.1% | 0.7% | 1.2% |
| Any-PII char precision | 98.8 | 95.7 | 99.0 | 99.1 | 99.2 | 95.9 | 98.9 | 99.0 | 99.1 |
| Any-PII char recall | 38.6 | 78.1 | 99.3 | 99.5 | 99.1 | 90.1 | 99.3 | 99.6 | 99.2 |
| Any-PII char F1 | 55.5 | 86.0 | 99.1 | 99.3 | 99.2 | 92.9 | 99.1 | 99.3 | 99.1 |
| Exact-span F1 (all categories) | 39.5 | 65.1 | 96.2 | 96.4 | 81.6 | 70.8 | 95.6 | 95.7 | 83.0 |
| Median ms per document | 0.02 | 394.82 | 10.88 | 22.02 | 23.25 | 394.85 | 10.91 | 22.04 | 23.27 |

Span leak rate by category (lower is better):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (2011 spans) | 100.0% | 7.3% | 1.9% | 1.4% | 2.2% | 7.3% | 1.9% | 1.4% | 2.2% |
| ADDRESS (839 spans) | 100.0% | 33.6% | 2.5% | 1.0% | 2.4% | 33.6% | 2.5% | 1.0% | 2.4% |
| EMAIL (792 spans) | 0.4% | 2.8% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% |
| PHONE (505 spans) | 97.2% | 12.9% | 0.4% | 0.4% | 1.0% | 12.1% | 0.4% | 0.4% | 1.0% |
| URL (394 spans) | 7.4% | 83.8% | 1.0% | 0.8% | 0.5% | 6.9% | 0.3% | 0.3% | 0.3% |
| IP_ADDRESS (314 spans) | 15.9% | 13.7% | 0.6% | 0.0% | 0.3% | 1.6% | 0.0% | 0.0% | 0.0% |
| DATE (629 spans) | 20.3% | 4.3% | 1.6% | 1.6% | 1.6% | 3.5% | 1.4% | 1.4% | 1.0% |
| ID (2818 spans) | 91.5% | 13.4% | 0.2% | 0.2% | 0.7% | 12.5% | 0.2% | 0.2% | 0.5% |
| SECRET (334 spans) | 91.9% | 34.7% | 4.5% | 1.8% | 4.2% | 34.4% | 4.5% | 1.8% | 3.9% |

Character-level F1 by category (category must match):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 91.0 | 98.2 | 98.7 | 98.2 | 91.0 | 98.2 | 98.7 | 98.2 |
| ADDRESS | 0.0 | 81.6 | 98.8 | 99.2 | 99.1 | 81.6 | 98.8 | 99.2 | 99.1 |
| EMAIL | 99.7 | 98.5 | 99.6 | 99.7 | 99.7 | 99.6 | 99.6 | 99.7 | 99.7 |
| PHONE | 4.7 | 83.4 | 98.5 | 98.4 | 97.9 | 85.3 | 97.2 | 97.1 | 96.5 |
| URL | 91.1 | 25.7 | 98.5 | 99.1 | 99.0 | 87.7 | 95.5 | 95.7 | 95.7 |
| IP_ADDRESS | 67.5 | 0.0 | 99.6 | 99.7 | 99.6 | 67.4 | 88.2 | 88.1 | 88.1 |
| DATE | 88.3 | 85.3 | 98.7 | 99.1 | 99.0 | 85.8 | 98.7 | 98.9 | 99.0 |
| ID | 21.0 | 87.5 | 99.0 | 99.3 | 98.6 | 88.7 | 98.7 | 98.8 | 98.5 |
| SECRET | 16.3 | 78.9 | 97.5 | 98.8 | 99.0 | 79.2 | 97.4 | 98.3 | 98.7 |
