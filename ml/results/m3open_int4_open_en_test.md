## Open English PII test set: Nemotron-PII + Gretel-en

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **96.4%** | **3.6%** | **3.1%** | **3.5%** | **3.4%** | **2.7%** | **2.9%** |
| Span leak rate | 74.5% | 1.2% | 1.2% | 1.2% | 1.2% | 1.1% | 1.0% |
| Any-PII char precision | 98.8 | 99.0 | 97.2 | 99.1 | 98.9 | 97.1 | 99.0 |
| Any-PII char recall | 38.6 | 99.2 | 99.3 | 99.2 | 99.3 | 99.4 | 99.4 |
| Any-PII char F1 | 55.5 | 99.1 | 98.3 | 99.1 | 99.1 | 98.2 | 99.2 |
| Exact-span F1 (all categories) | 39.5 | 96.3 | 90.6 | 82.3 | 95.7 | 90.1 | 83.7 |
| Median ms per document | 0.01 | 48.12 | 87.73 | 84.31 | 48.14 | 87.74 | 84.32 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON (2011 spans) | 100.0% | 2.0% | 1.7% | 1.6% | 2.0% | 1.7% | 1.6% |
| ADDRESS (839 spans) | 100.0% | 2.3% | 2.6% | 1.7% | 2.3% | 2.6% | 1.7% |
| EMAIL (792 spans) | 0.4% | 0.4% | 0.6% | 0.5% | 0.4% | 0.4% | 0.4% |
| PHONE (505 spans) | 97.2% | 0.4% | 0.6% | 0.4% | 0.4% | 0.6% | 0.4% |
| URL (394 spans) | 7.4% | 0.3% | 0.8% | 1.8% | 0.3% | 0.3% | 0.3% |
| IP_ADDRESS (314 spans) | 15.9% | 0.6% | 0.6% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (629 spans) | 20.3% | 2.1% | 1.7% | 3.2% | 1.9% | 1.6% | 2.9% |
| ID (2818 spans) | 91.5% | 0.3% | 0.5% | 0.4% | 0.3% | 0.5% | 0.3% |
| SECRET (334 spans) | 91.9% | 4.8% | 1.8% | 3.6% | 4.8% | 1.8% | 3.6% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 98.1 | 98.7 | 98.6 | 98.1 | 98.7 | 98.6 |
| ADDRESS | 0.0 | 98.8 | 98.9 | 99.0 | 98.8 | 98.9 | 99.0 |
| EMAIL | 99.7 | 99.7 | 95.5 | 99.6 | 99.7 | 95.5 | 99.7 |
| PHONE | 4.7 | 98.5 | 98.7 | 98.5 | 97.2 | 97.3 | 97.1 |
| URL | 91.1 | 98.9 | 99.0 | 98.7 | 95.7 | 95.7 | 95.7 |
| IP_ADDRESS | 67.5 | 99.5 | 99.5 | 99.6 | 88.1 | 88.1 | 88.1 |
| DATE | 88.3 | 98.5 | 91.8 | 98.2 | 98.5 | 91.8 | 98.2 |
| ID | 21.0 | 98.9 | 99.2 | 99.0 | 98.6 | 98.8 | 98.8 |
| SECRET | 16.3 | 98.0 | 98.6 | 98.5 | 97.8 | 98.4 | 98.4 |
