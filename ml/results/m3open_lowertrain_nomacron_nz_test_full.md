## Deployed and lowercase-trained students, nomacron: test_full

| Metric | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **0.9%** | **3.0%** | **1.1%** | **0.1%** | **6.1%** | **0.0%** | **0.3%** |
| Span leak rate | 0.2% | 0.6% | 0.2% | 0.0% | 1.3% | 0.0% | 0.1% |
| Any-PII char precision | 93.7 | 91.9 | 94.6 | 92.8 | 91.1 | 90.4 | 93.1 |
| Any-PII char recall | 99.9 | 99.7 | 99.9 | 100.0 | 99.3 | 100.0 | 100.0 |
| Any-PII char F1 | 96.7 | 95.7 | 97.2 | 96.2 | 95.0 | 95.0 | 96.4 |
| Exact-span F1 (all categories) | 91.4 | 85.7 | 75.2 | 90.0 | 86.2 | 66.3 | 90.9 |
| Median ms per document | 61.81 | 161.49 | 131.55 | 9.42 | 13.68 | 17.27 | 55.78 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5250 spans) | 0.3% | 1.0% | 0.4% | 0.0% | 2.4% | 0.0% | 0.1% |
| ADDRESS (1000 spans) | 0.1% | 0.0% | 0.0% | 0.1% | 0.0% | 0.0% | 0.1% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 97.4 | 93.9 | 98.8 | 96.3 | 93.5 | 93.4 | 96.8 |
| ADDRESS | 99.9 | 97.6 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 99.0 | 100.0 | 99.9 | 99.3 | 99.1 | 99.8 |
| DATE | 100.0 | 98.5 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 100.0 | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 | 100.0 |
