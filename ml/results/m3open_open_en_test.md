## Open English PII test set: Nemotron-PII + Gretel-en

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **96.4%** | **40.0%** | **3.9%** | **2.8%** | **2.8%** | **32.3%** | **3.8%** | **2.5%** | **2.5%** |
| Span leak rate | 74.5% | 16.3% | 1.3% | 1.1% | 1.0% | 11.7% | 1.2% | 1.1% | 0.9% |
| Any-PII char precision | 98.8 | 95.7 | 99.0 | 99.2 | 99.1 | 95.9 | 98.8 | 99.1 | 99.0 |
| Any-PII char recall | 38.6 | 78.1 | 99.2 | 99.3 | 99.3 | 90.1 | 99.2 | 99.4 | 99.4 |
| Any-PII char F1 | 55.5 | 86.0 | 99.1 | 99.3 | 99.2 | 92.9 | 99.0 | 99.2 | 99.2 |
| Exact-span F1 (all categories) | 39.5 | 65.1 | 96.1 | 96.3 | 82.5 | 70.8 | 95.6 | 95.7 | 83.9 |
| Median ms per document | 0.01 | 394.82 | 17.06 | 14.26 | 17.23 | 394.83 | 17.07 | 14.27 | 17.24 |

Span leak rate by category (lower is better):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (2011 spans) | 100.0% | 7.3% | 2.1% | 1.7% | 1.5% | 7.3% | 2.1% | 1.7% | 1.5% |
| ADDRESS (839 spans) | 100.0% | 33.6% | 3.0% | 2.1% | 1.7% | 33.6% | 3.0% | 2.1% | 1.7% |
| EMAIL (792 spans) | 0.4% | 2.8% | 0.4% | 0.5% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% |
| PHONE (505 spans) | 97.2% | 12.9% | 0.4% | 0.8% | 0.4% | 12.1% | 0.4% | 0.8% | 0.4% |
| URL (394 spans) | 7.4% | 83.8% | 0.3% | 0.8% | 1.8% | 6.9% | 0.3% | 0.3% | 0.3% |
| IP_ADDRESS (314 spans) | 15.9% | 13.7% | 0.6% | 0.6% | 0.0% | 1.6% | 0.0% | 0.0% | 0.0% |
| DATE (629 spans) | 20.3% | 4.3% | 1.7% | 1.6% | 1.7% | 3.5% | 1.6% | 1.4% | 1.6% |
| ID (2818 spans) | 91.5% | 13.4% | 0.3% | 0.6% | 0.5% | 12.5% | 0.3% | 0.5% | 0.4% |
| SECRET (334 spans) | 91.9% | 34.7% | 4.8% | 2.4% | 2.7% | 34.4% | 4.8% | 2.4% | 2.7% |

Character-level F1 by category (category must match):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 91.0 | 98.0 | 98.7 | 98.8 | 91.0 | 98.0 | 98.7 | 98.8 |
| ADDRESS | 0.0 | 81.6 | 98.6 | 99.0 | 99.1 | 81.6 | 98.6 | 99.0 | 99.1 |
| EMAIL | 99.7 | 98.5 | 99.7 | 99.6 | 99.7 | 99.6 | 99.7 | 99.7 | 99.7 |
| PHONE | 4.7 | 83.4 | 98.5 | 98.9 | 98.6 | 85.3 | 97.1 | 97.5 | 97.3 |
| URL | 91.1 | 25.7 | 99.0 | 99.1 | 98.7 | 87.7 | 95.7 | 95.7 | 95.7 |
| IP_ADDRESS | 67.5 | 0.0 | 99.5 | 99.5 | 99.1 | 67.4 | 88.1 | 88.1 | 88.0 |
| DATE | 88.3 | 85.3 | 98.6 | 98.9 | 98.8 | 85.8 | 98.6 | 98.9 | 98.8 |
| ID | 21.0 | 87.5 | 98.9 | 99.3 | 99.1 | 88.7 | 98.6 | 98.9 | 98.8 |
| SECRET | 16.3 | 78.9 | 97.9 | 98.5 | 98.4 | 79.2 | 97.7 | 98.3 | 98.4 |
