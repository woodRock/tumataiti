## Deployed and lowercase-trained students, lower: test_full

| Metric | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower |
|---|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **94.7%** | **83.3%** | **53.4%** | **5.1%** | **25.3%** | **0.9%** |
| Span leak rate | 45.2% | 31.6% | 17.6% | 1.3% | 10.0% | 0.3% |
| Any-PII char precision | 93.5 | 92.0 | 92.5 | 92.4 | 91.8 | 91.8 |
| Any-PII char recall | 70.7 | 82.5 | 91.1 | 99.4 | 94.4 | 99.9 |
| Any-PII char F1 | 80.5 | 87.0 | 91.8 | 95.8 | 93.1 | 95.6 |
| Exact-span F1 (all categories) | 59.2 | 67.5 | 57.7 | 79.3 | 84.8 | 61.9 |
| Median ms per document | 57.28 | 144.27 | 119.79 | 9.26 | 13.74 | 17.78 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower |
|---|---:|---:|---:|---:|---:|---:|
| PERSON (5250 spans) | 80.6% | 57.0% | 29.7% | 2.4% | 18.5% | 0.5% |
| ADDRESS (1000 spans) | 15.3% | 0.1% | 10.5% | 0.0% | 0.0% | 0.0% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 3.2% | 11.5% | 7.3% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower |
|---|---:|---:|---:|---:|---:|---:|
| PERSON | 44.0 | 69.0 | 86.1 | 94.7 | 88.0 | 95.3 |
| ADDRESS | 97.4 | 98.9 | 98.1 | 99.7 | 100.0 | 100.0 |
| EMAIL | 100.0 | 99.4 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 98.7 | 99.4 | 100.0 | 99.3 | 98.5 |
| DATE | 99.9 | 97.6 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 98.8 | 88.5 | 95.7 | 100.0 | 100.0 | 100.0 |
