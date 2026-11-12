## Open English PII test set: Nemotron-PII + Gretel-en

| Metric | rules | deberta-small-open-v4 | deberta-small-open-v4-1ep | deberta-small-open-v4-1ep-s1 | deberta-small-open-v4kin | deberta-small-open-v4kin-s1 | deberta-small-open-v4ids | rules+deberta-small-open-v4 | rules+deberta-small-open-v4-1ep | rules+deberta-small-open-v4-1ep-s1 | rules+deberta-small-open-v4kin | rules+deberta-small-open-v4kin-s1 | rules+deberta-small-open-v4ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **96.4%** | **3.9%** | **2.7%** | **2.4%** | **3.0%** | **2.4%** | **2.5%** | **3.8%** | **2.2%** | **2.2%** | **2.6%** | **2.2%** | **2.1%** |
| Span leak rate | 74.5% | 1.3% | 1.0% | 0.9% | 1.0% | 0.9% | 0.9% | 1.2% | 0.8% | 0.8% | 0.9% | 0.8% | 0.8% |
| Any-PII char precision | 98.8 | 99.0 | 99.0 | 98.9 | 99.0 | 99.0 | 98.9 | 98.8 | 98.8 | 98.8 | 98.8 | 98.8 | 98.8 |
| Any-PII char recall | 38.6 | 99.2 | 99.4 | 99.5 | 99.4 | 99.5 | 99.4 | 99.2 | 99.5 | 99.5 | 99.4 | 99.5 | 99.5 |
| Any-PII char F1 | 55.5 | 99.1 | 99.2 | 99.2 | 99.2 | 99.2 | 99.2 | 99.0 | 99.2 | 99.1 | 99.1 | 99.2 | 99.1 |
| Exact-span F1 (all categories) | 39.5 | 96.1 | 96.1 | 96.3 | 96.0 | 96.2 | 96.3 | 95.6 | 95.6 | 95.8 | 95.4 | 95.7 | 95.8 |
| Median ms per document | 0.01 | 17.06 | 9.34 | 9.79 | 9.86 | 10.43 | 6.20 | 17.07 | 9.35 | 9.80 | 9.87 | 10.44 | 6.21 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-small-open-v4 | deberta-small-open-v4-1ep | deberta-small-open-v4-1ep-s1 | deberta-small-open-v4kin | deberta-small-open-v4kin-s1 | deberta-small-open-v4ids | rules+deberta-small-open-v4 | rules+deberta-small-open-v4-1ep | rules+deberta-small-open-v4-1ep-s1 | rules+deberta-small-open-v4kin | rules+deberta-small-open-v4kin-s1 | rules+deberta-small-open-v4ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (2011 spans) | 100.0% | 2.1% | 1.6% | 1.4% | 1.7% | 1.5% | 1.5% | 2.1% | 1.6% | 1.4% | 1.7% | 1.5% | 1.5% |
| ADDRESS (839 spans) | 100.0% | 3.0% | 1.3% | 2.0% | 1.3% | 2.0% | 1.3% | 3.0% | 1.3% | 2.0% | 1.3% | 2.0% | 1.3% |
| EMAIL (792 spans) | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% |
| PHONE (505 spans) | 97.2% | 0.4% | 0.6% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.6% | 0.4% | 0.4% | 0.4% | 0.4% |
| URL (394 spans) | 7.4% | 0.3% | 1.8% | 0.5% | 1.0% | 0.3% | 1.0% | 0.3% | 0.3% | 0.3% | 0.3% | 0.3% | 0.3% |
| IP_ADDRESS (314 spans) | 15.9% | 0.6% | 0.3% | 0.3% | 0.3% | 0.0% | 0.6% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (629 spans) | 20.3% | 1.7% | 1.6% | 1.3% | 1.9% | 1.1% | 1.7% | 1.6% | 1.4% | 1.1% | 1.7% | 1.0% | 1.6% |
| ID (2818 spans) | 91.5% | 0.3% | 0.2% | 0.2% | 0.3% | 0.2% | 0.2% | 0.3% | 0.1% | 0.1% | 0.2% | 0.1% | 0.1% |
| SECRET (334 spans) | 91.9% | 4.8% | 3.0% | 3.0% | 3.9% | 3.0% | 3.3% | 4.8% | 2.7% | 3.0% | 3.6% | 2.7% | 3.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-small-open-v4 | deberta-small-open-v4-1ep | deberta-small-open-v4-1ep-s1 | deberta-small-open-v4kin | deberta-small-open-v4kin-s1 | deberta-small-open-v4ids | rules+deberta-small-open-v4 | rules+deberta-small-open-v4-1ep | rules+deberta-small-open-v4-1ep-s1 | rules+deberta-small-open-v4kin | rules+deberta-small-open-v4kin-s1 | rules+deberta-small-open-v4ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 98.0 | 98.1 | 98.0 | 98.0 | 98.1 | 98.0 | 98.0 | 98.1 | 98.0 | 98.0 | 98.1 | 98.0 |
| ADDRESS | 0.0 | 98.6 | 98.9 | 98.9 | 99.0 | 99.0 | 98.9 | 98.6 | 98.9 | 98.9 | 99.0 | 99.0 | 98.9 |
| EMAIL | 99.7 | 99.7 | 99.7 | 99.7 | 99.7 | 99.7 | 99.7 | 99.7 | 99.7 | 99.7 | 99.7 | 99.7 | 99.7 |
| PHONE | 4.7 | 98.5 | 98.6 | 98.6 | 98.5 | 98.8 | 98.8 | 97.1 | 97.2 | 97.3 | 97.1 | 97.4 | 97.5 |
| URL | 91.1 | 99.0 | 98.9 | 99.0 | 99.0 | 99.0 | 98.9 | 95.7 | 95.7 | 95.7 | 95.7 | 95.7 | 95.7 |
| IP_ADDRESS | 67.5 | 99.5 | 99.7 | 99.5 | 99.7 | 99.7 | 99.5 | 88.1 | 88.1 | 88.1 | 88.1 | 88.1 | 88.1 |
| DATE | 88.3 | 98.6 | 98.6 | 98.7 | 98.7 | 98.7 | 98.7 | 98.6 | 98.6 | 98.7 | 98.7 | 98.7 | 98.7 |
| ID | 21.0 | 98.9 | 99.1 | 99.2 | 99.0 | 99.2 | 99.2 | 98.6 | 98.8 | 98.8 | 98.7 | 98.8 | 98.8 |
| SECRET | 16.3 | 97.9 | 98.8 | 98.6 | 98.8 | 98.7 | 98.8 | 97.7 | 98.6 | 98.4 | 98.5 | 98.4 | 98.5 |
