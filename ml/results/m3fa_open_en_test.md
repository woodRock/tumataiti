## Open English PII test set: Nemotron-PII + Gretel-en (2,000 documents)

| Metric | rules | deberta-small-open-v2 | deberta-small-open-v2-1ep | deberta-small-open-v2-1ep-s1 | deberta-small-open-v3 | deberta-small-open-v3-s1 | deberta-small-open-v3ids | rules+deberta-small-open-v2 | rules+deberta-small-open-v2-1ep | rules+deberta-small-open-v2-1ep-s1 | rules+deberta-small-open-v3 | rules+deberta-small-open-v3-s1 | rules+deberta-small-open-v3ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **96.4%** | **3.3%** | **2.8%** | **2.4%** | **2.9%** | **2.4%** | **3.0%** | **3.1%** | **2.4%** | **2.3%** | **2.4%** | **2.3%** | **2.5%** |
| Span leak rate | 74.5% | 1.2% | 1.0% | 0.9% | 1.0% | 0.9% | 1.0% | 1.1% | 0.9% | 0.9% | 0.9% | 0.9% | 0.9% |
| Any-PII char precision | 98.8 | 99.0 | 99.0 | 98.9 | 99.0 | 98.9 | 99.0 | 98.9 | 98.8 | 98.7 | 98.8 | 98.7 | 98.8 |
| Any-PII char recall | 38.6 | 99.3 | 99.3 | 99.4 | 99.3 | 99.5 | 99.3 | 99.3 | 99.5 | 99.5 | 99.5 | 99.5 | 99.5 |
| Any-PII char F1 | 55.5 | 99.1 | 99.2 | 99.2 | 99.2 | 99.2 | 99.1 | 99.1 | 99.2 | 99.1 | 99.2 | 99.1 | 99.1 |
| Exact-span F1 (all categories) | 39.5 | 96.2 | 96.3 | 96.3 | 96.2 | 96.2 | 96.4 | 95.6 | 95.8 | 95.7 | 95.6 | 95.6 | 95.8 |
| Median ms per document | 0.02 | 10.88 | 12.43 | 12.01 | 12.47 | 12.49 | 12.09 | 10.91 | 12.46 | 12.03 | 12.49 | 12.52 | 12.12 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-small-open-v2 | deberta-small-open-v2-1ep | deberta-small-open-v2-1ep-s1 | deberta-small-open-v3 | deberta-small-open-v3-s1 | deberta-small-open-v3ids | rules+deberta-small-open-v2 | rules+deberta-small-open-v2-1ep | rules+deberta-small-open-v2-1ep-s1 | rules+deberta-small-open-v3 | rules+deberta-small-open-v3-s1 | rules+deberta-small-open-v3ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (2011 spans) | 100.0% | 1.9% | 1.6% | 1.5% | 1.5% | 1.5% | 1.7% | 1.9% | 1.6% | 1.5% | 1.5% | 1.5% | 1.7% |
| ADDRESS (839 spans) | 100.0% | 2.5% | 1.5% | 1.8% | 1.7% | 1.8% | 1.4% | 2.5% | 1.5% | 1.8% | 1.7% | 1.8% | 1.4% |
| EMAIL (792 spans) | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% |
| PHONE (505 spans) | 97.2% | 0.4% | 0.6% | 0.6% | 0.6% | 0.6% | 0.6% | 0.4% | 0.6% | 0.6% | 0.6% | 0.6% | 0.6% |
| URL (394 spans) | 7.4% | 1.0% | 1.8% | 0.3% | 2.0% | 0.5% | 1.8% | 0.3% | 0.3% | 0.3% | 0.3% | 0.3% | 0.3% |
| IP_ADDRESS (314 spans) | 15.9% | 0.6% | 0.6% | 0.0% | 0.6% | 0.0% | 0.6% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (629 spans) | 20.3% | 1.6% | 1.7% | 1.1% | 1.7% | 1.1% | 1.6% | 1.4% | 1.6% | 1.0% | 1.6% | 1.0% | 1.4% |
| ID (2818 spans) | 91.5% | 0.2% | 0.2% | 0.2% | 0.2% | 0.2% | 0.2% | 0.2% | 0.1% | 0.2% | 0.1% | 0.1% | 0.1% |
| SECRET (334 spans) | 91.9% | 4.5% | 3.6% | 3.3% | 3.6% | 3.6% | 3.9% | 4.5% | 3.3% | 3.3% | 3.3% | 3.6% | 3.6% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-small-open-v2 | deberta-small-open-v2-1ep | deberta-small-open-v2-1ep-s1 | deberta-small-open-v3 | deberta-small-open-v3-s1 | deberta-small-open-v3ids | rules+deberta-small-open-v2 | rules+deberta-small-open-v2-1ep | rules+deberta-small-open-v2-1ep-s1 | rules+deberta-small-open-v3 | rules+deberta-small-open-v3-s1 | rules+deberta-small-open-v3ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 98.2 | 98.1 | 97.6 | 98.0 | 97.7 | 98.1 | 98.2 | 98.1 | 97.6 | 98.0 | 97.7 | 98.1 |
| ADDRESS | 0.0 | 98.8 | 98.8 | 98.9 | 98.9 | 99.0 | 98.9 | 98.8 | 98.8 | 98.9 | 98.9 | 99.0 | 98.9 |
| EMAIL | 99.7 | 99.6 | 99.7 | 99.7 | 99.7 | 99.7 | 99.7 | 99.6 | 99.7 | 99.7 | 99.7 | 99.7 | 99.7 |
| PHONE | 4.7 | 98.5 | 98.7 | 98.6 | 98.5 | 98.4 | 98.5 | 97.2 | 97.3 | 97.2 | 97.2 | 97.1 | 97.2 |
| URL | 91.1 | 98.5 | 99.0 | 99.1 | 98.9 | 99.1 | 98.8 | 95.5 | 95.7 | 95.7 | 95.7 | 95.7 | 95.7 |
| IP_ADDRESS | 67.5 | 99.6 | 99.5 | 99.8 | 99.6 | 99.8 | 99.6 | 88.2 | 88.2 | 88.2 | 88.2 | 88.2 | 88.1 |
| DATE | 88.3 | 98.7 | 98.7 | 98.9 | 98.7 | 98.9 | 98.8 | 98.7 | 98.7 | 98.9 | 98.7 | 98.9 | 98.8 |
| ID | 21.0 | 99.0 | 99.2 | 99.1 | 99.1 | 99.0 | 99.2 | 98.7 | 98.8 | 98.7 | 98.7 | 98.7 | 98.8 |
| SECRET | 16.3 | 97.5 | 98.8 | 98.9 | 98.5 | 98.4 | 99.0 | 97.4 | 98.5 | 98.5 | 98.4 | 98.2 | 98.7 |
