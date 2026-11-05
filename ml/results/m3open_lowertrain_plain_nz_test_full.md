## Deployed and lowercase-trained students, plain: test_full

| Metric | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower |
|---|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **0.7%** | **2.7%** | **1.4%** | **0.1%** | **14.2%** | **0.1%** |
| Span leak rate | 0.1% | 0.6% | 0.2% | 0.0% | 3.2% | 0.0% |
| Any-PII char precision | 94.4 | 92.4 | 93.8 | 92.8 | 92.5 | 92.7 |
| Any-PII char recall | 99.9 | 99.7 | 99.9 | 100.0 | 98.4 | 100.0 |
| Any-PII char F1 | 97.1 | 95.9 | 96.7 | 96.3 | 95.3 | 96.2 |
| Exact-span F1 (all categories) | 92.2 | 87.1 | 73.0 | 90.5 | 87.5 | 66.7 |
| Median ms per document | 29.48 | 103.76 | 78.27 | 8.98 | 17.50 | 17.85 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower |
|---|---:|---:|---:|---:|---:|---:|
| PERSON (5250 spans) | 0.2% | 1.0% | 0.5% | 0.0% | 5.9% | 0.0% |
| ADDRESS (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower |
|---|---:|---:|---:|---:|---:|---:|
| PERSON | 98.3 | 94.4 | 97.6 | 96.3 | 93.9 | 96.6 |
| ADDRESS | 99.9 | 97.6 | 100.0 | 99.9 | 100.0 | 100.0 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 99.0 | 99.9 | 99.9 | 99.7 | 99.1 |
| DATE | 100.0 | 98.2 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 100.0 | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 |
