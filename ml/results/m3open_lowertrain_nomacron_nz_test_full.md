## Deployed and lowercase-trained students, nomacron: test_full

| Metric | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **5.9%** | **9.3%** | **2.7%** | **11.9%** | **2.0%** | **0.9%** | **12.6%** |
| Span leak rate | 1.2% | 1.8% | 0.5% | 3.1% | 0.4% | 0.2% | 3.1% |
| Any-PII char precision | 91.2 | 92.7 | 91.4 | 92.7 | 91.2 | 91.0 | 92.9 |
| Any-PII char recall | 99.3 | 99.2 | 99.7 | 98.0 | 99.8 | 99.9 | 98.0 |
| Any-PII char F1 | 95.1 | 95.8 | 95.4 | 95.3 | 95.3 | 95.2 | 95.3 |
| Exact-span F1 (all categories) | 79.5 | 83.0 | 67.5 | 82.5 | 80.9 | 70.8 | 82.2 |
| Median ms per document | 58.09 | 157.12 | 117.97 | 8.69 | 17.04 | 19.33 | 52.63 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON (6250 spans) | 0.0% | 2.2% | 1.1% | 0.1% | 0.4% | 0.0% | 0.1% |
| ADDRESS (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (5000 spans) | 3.9% | 3.0% | 0.1% | 9.8% | 0.6% | 0.5% | 9.9% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 94.7 | 95.6 | 82.8 | 92.3 | 91.2 | 88.6 | 92.4 |
| ADDRESS | 90.5 | 97.5 | 94.7 | 96.9 | 94.5 | 99.8 | 96.9 |
| EMAIL | 100.0 | 97.1 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 98.3 | 100.0 | 100.0 | 97.6 | 100.0 | 100.0 |
| DATE | 100.0 | 90.1 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 |
| AFFILIATION | 89.0 | 96.1 | 78.9 | 90.6 | 92.0 | 85.2 | 91.4 |
