## Open English PII test set: Nemotron-PII + Gretel-en (2,000 documents)

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **96.4%** | **3.3%** | **1.7%** | **5.1%** | **3.2%** | **1.6%** | **4.7%** |
| Span leak rate | 74.5% | 1.2% | 0.7% | 1.6% | 1.1% | 0.7% | 1.5% |
| Any-PII char precision | 98.8 | 99.0 | 99.1 | 99.2 | 98.9 | 99.0 | 99.0 |
| Any-PII char recall | 38.6 | 99.3 | 99.5 | 99.1 | 99.4 | 99.6 | 99.2 |
| Any-PII char F1 | 55.5 | 99.1 | 99.3 | 99.1 | 99.1 | 99.3 | 99.1 |
| Exact-span F1 (all categories) | 39.5 | 96.0 | 95.6 | 81.2 | 95.4 | 95.0 | 82.6 |
| Median ms per document | 0.02 | 50.56 | 112.35 | 90.62 | 50.58 | 112.38 | 90.65 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON (2011 spans) | 100.0% | 2.1% | 1.2% | 2.6% | 2.1% | 1.2% | 2.6% |
| ADDRESS (839 spans) | 100.0% | 2.3% | 1.0% | 2.9% | 2.3% | 1.0% | 2.9% |
| EMAIL (792 spans) | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% | 0.4% |
| PHONE (505 spans) | 97.2% | 0.4% | 0.4% | 0.8% | 0.4% | 0.4% | 0.8% |
| URL (394 spans) | 7.4% | 1.0% | 0.8% | 0.5% | 0.3% | 0.3% | 0.3% |
| IP_ADDRESS (314 spans) | 15.9% | 0.6% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (629 spans) | 20.3% | 1.9% | 1.4% | 3.5% | 1.7% | 1.3% | 2.9% |
| ID (2818 spans) | 91.5% | 0.2% | 0.2% | 0.6% | 0.2% | 0.2% | 0.4% |
| SECRET (334 spans) | 91.9% | 4.5% | 1.8% | 4.5% | 4.5% | 1.8% | 4.5% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 98.2 | 98.7 | 98.0 | 98.2 | 98.7 | 98.0 |
| ADDRESS | 0.0 | 98.8 | 99.1 | 98.9 | 98.8 | 99.1 | 98.9 |
| EMAIL | 99.7 | 99.6 | 99.7 | 99.7 | 99.6 | 99.7 | 99.7 |
| PHONE | 4.7 | 98.3 | 98.4 | 97.7 | 97.0 | 97.0 | 96.4 |
| URL | 91.1 | 98.6 | 99.0 | 98.9 | 95.6 | 95.6 | 95.7 |
| IP_ADDRESS | 67.5 | 99.6 | 99.8 | 99.6 | 88.2 | 88.2 | 88.1 |
| DATE | 88.3 | 98.6 | 99.1 | 98.5 | 98.6 | 98.9 | 98.5 |
| ID | 21.0 | 98.9 | 99.3 | 98.6 | 98.6 | 98.9 | 98.4 |
| SECRET | 16.3 | 97.7 | 98.8 | 98.6 | 97.5 | 98.4 | 98.3 |
