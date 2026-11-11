## NZ synthetic v4, held-out templates, names and affiliations

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **2.2%** | **7.7%** | **2.8%** | **2.1%** | **6.5%** | **2.3%** |
| Span leak rate | 76.6% | 0.4% | 1.4% | 0.5% | 0.4% | 1.2% | 0.4% |
| Any-PII char precision | 90.0 | 94.8 | 95.2 | 94.5 | 92.3 | 92.7 | 92.4 |
| Any-PII char recall | 26.0 | 99.8 | 99.4 | 99.7 | 99.8 | 99.5 | 99.7 |
| Any-PII char F1 | 40.4 | 97.3 | 97.3 | 97.0 | 95.9 | 96.0 | 95.9 |
| Exact-span F1 (all categories) | 37.5 | 85.6 | 85.5 | 69.8 | 85.1 | 85.1 | 76.0 |
| Median ms per document | 0.05 | 29.81 | 81.41 | 61.12 | 29.86 | 81.45 | 61.16 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON (6250 spans) | 100.0% | 0.0% | 2.1% | 1.0% | 0.0% | 2.1% | 1.0% |
| ADDRESS (1000 spans) | 100.0% | 0.0% | 0.1% | 0.0% | 0.0% | 0.1% | 0.0% |
| EMAIL (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.2% | 6.2% | 2.4% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (5000 spans) | 100.0% | 1.1% | 1.2% | 0.0% | 1.1% | 1.2% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 95.7 | 94.4 | 94.8 | 95.7 | 94.4 | 94.8 |
| ADDRESS | 0.0 | 96.9 | 97.9 | 97.9 | 96.9 | 97.9 | 97.9 |
| EMAIL | 100.0 | 100.0 | 97.7 | 100.0 | 100.0 | 97.7 | 100.0 |
| PHONE | 100.0 | 100.0 | 98.5 | 100.0 | 100.0 | 98.5 | 100.0 |
| DATE | 100.0 | 99.9 | 88.8 | 99.7 | 100.0 | 90.4 | 100.0 |
| ID | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| AFFILIATION | 0.0 | 92.0 | 95.3 | 95.6 | 92.0 | 95.3 | 95.6 |
