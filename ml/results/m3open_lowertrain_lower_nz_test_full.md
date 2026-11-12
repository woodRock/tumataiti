## Deployed and lowercase-trained students, lower: test_full

| Metric | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **96.5%** | **98.0%** | **57.6%** | **16.5%** | **16.1%** | **11.2%** | **18.5%** |
| Span leak rate | 61.2% | 53.8% | 16.6% | 3.6% | 3.7% | 2.2% | 4.3% |
| Any-PII char precision | 93.7 | 92.1 | 92.9 | 92.6 | 89.8 | 91.0 | 92.6 |
| Any-PII char recall | 51.0 | 59.4 | 91.2 | 97.9 | 97.9 | 99.0 | 97.5 |
| Any-PII char F1 | 66.0 | 72.2 | 92.1 | 95.2 | 93.7 | 94.8 | 95.0 |
| Exact-span F1 (all categories) | 45.4 | 47.9 | 59.6 | 78.9 | 78.2 | 63.5 | 78.8 |
| Median ms per document | 68.91 | 170.69 | 118.10 | 9.22 | 17.19 | 17.04 | 56.43 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON (6250 spans) | 82.9% | 72.9% | 25.1% | 4.7% | 6.8% | 1.6% | 6.1% |
| ADDRESS (1000 spans) | 22.3% | 0.6% | 8.8% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 2.7% | 21.1% | 30.3% | 0.0% | 0.0% | 0.7% | 0.0% |
| AFFILIATION (5000 spans) | 87.4% | 77.9% | 15.4% | 5.9% | 3.3% | 4.8% | 6.2% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 39.2 | 53.8 | 86.6 | 91.0 | 87.5 | 93.2 | 90.5 |
| ADDRESS | 94.2 | 99.2 | 98.4 | 96.1 | 94.7 | 99.9 | 96.0 |
| EMAIL | 100.0 | 96.8 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 98.1 | 99.9 | 100.0 | 97.7 | 98.7 | 100.0 |
| DATE | 99.9 | 92.2 | 99.8 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 98.9 | 91.7 | 88.1 | 99.9 | 99.7 | 99.6 | 99.7 |
| AFFILIATION | 30.4 | 46.8 | 90.9 | 93.0 | 92.1 | 89.7 | 93.1 |
