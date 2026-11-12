## Deployed and lowercase-trained students, plain: test_full

| Metric | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **2.1%** | **6.5%** | **2.3%** | **1.5%** | **2.1%** | **1.1%** | **2.6%** |
| Span leak rate | 0.4% | 1.2% | 0.4% | 0.3% | 0.5% | 0.2% | 0.5% |
| Any-PII char precision | 92.3 | 92.7 | 92.4 | 93.3 | 91.9 | 91.7 | 93.6 |
| Any-PII char recall | 99.8 | 99.5 | 99.7 | 99.8 | 99.8 | 99.9 | 99.7 |
| Any-PII char F1 | 95.9 | 96.0 | 95.9 | 96.4 | 95.7 | 95.7 | 96.5 |
| Exact-span F1 (all categories) | 85.1 | 85.1 | 76.0 | 87.8 | 84.8 | 75.1 | 87.5 |
| Median ms per document | 29.86 | 81.45 | 61.16 | 10.37 | 5.75 | 16.72 | 55.62 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON (6250 spans) | 0.0% | 2.1% | 1.0% | 0.2% | 1.2% | 0.0% | 0.3% |
| ADDRESS (1000 spans) | 0.0% | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (5000 spans) | 1.1% | 1.2% | 0.0% | 0.6% | 0.0% | 0.6% | 1.2% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 95.7 | 94.4 | 94.8 | 94.7 | 94.4 | 94.6 | 94.7 |
| ADDRESS | 96.9 | 97.9 | 97.9 | 97.6 | 95.8 | 100.0 | 97.5 |
| EMAIL | 100.0 | 97.7 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 98.5 | 100.0 | 100.0 | 97.7 | 100.0 | 100.0 |
| DATE | 100.0 | 90.4 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 |
| AFFILIATION | 92.0 | 95.3 | 95.6 | 95.1 | 95.8 | 93.8 | 95.0 |
