## NZ synthetic v1, training templates with held-out names (1,600 documents)

| Metric | rules | deberta-v3-small | deberta-v3-small-int8 | modernbert-base | modernbert-base-int8 | mdeberta-v3-base | mdeberta-v3-base-int8 | rules+deberta-v3-small | rules+deberta-v3-small-int8 | rules+modernbert-base | rules+modernbert-base-int8 | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **93.8%** | **0.0%** | **0.1%** | **0.1%** | **39.2%** | **0.1%** | **88.4%** | **0.0%** | **0.1%** | **0.1%** | **23.7%** | **0.1%** | **39.5%** |
| Span leak rate | 45.8% | 0.0% | 0.0% | 0.0% | 9.8% | 0.0% | 54.2% | 0.0% | 0.0% | 0.0% | 5.1% | 0.0% | 13.7% |
| Any-PII char precision | 89.4 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.8 | 93.7 | 93.7 | 93.7 | 93.6 | 93.7 | 93.2 |
| Any-PII char recall | 57.3 | 100.0 | 100.0 | 100.0 | 94.0 | 100.0 | 61.8 | 100.0 | 100.0 | 100.0 | 98.2 | 100.0 | 93.8 |
| Any-PII char F1 | 69.8 | 100.0 | 100.0 | 100.0 | 96.9 | 100.0 | 76.4 | 96.7 | 96.7 | 96.7 | 95.8 | 96.7 | 93.5 |
| Exact-span F1 (all categories) | 67.0 | 100.0 | 100.0 | 99.7 | 85.2 | 68.6 | 24.9 | 96.7 | 96.7 | 96.5 | 88.8 | 79.8 | 62.4 |
| Median ms per document | 0.04 | 8.89 | 14.05 | 13.47 | 42.15 | 17.19 | 37.00 | 8.93 | 14.09 | 13.52 | 42.19 | 17.23 | 37.04 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small | deberta-v3-small-int8 | modernbert-base | modernbert-base-int8 | mdeberta-v3-base | mdeberta-v3-base-int8 | rules+deberta-v3-small | rules+deberta-v3-small-int8 | rules+modernbert-base | rules+modernbert-base-int8 | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (3100 spans) | 100.0% | 0.0% | 0.0% | 0.1% | 11.3% | 0.0% | 32.6% | 0.0% | 0.0% | 0.1% | 11.3% | 0.0% | 32.6% |
| ADDRESS (700 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 10.6% | 0.0% | 17.9% | 0.0% | 0.0% | 0.0% | 10.6% | 0.0% | 17.9% |
| EMAIL (1100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% | 88.4% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 1.8% | 0.0% | 92.4% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| URL (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 99.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| IP_ADDRESS (200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 35.5% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (600 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 14.2% | 0.0% | 98.5% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (1200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 3.2% | 0.0% | 24.1% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| SECRET (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 69.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small | deberta-v3-small-int8 | modernbert-base | modernbert-base-int8 | mdeberta-v3-base | mdeberta-v3-base-int8 | rules+deberta-v3-small | rules+deberta-v3-small-int8 | rules+modernbert-base | rules+modernbert-base-int8 | rules+mdeberta-v3-base | rules+mdeberta-v3-base-int8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 100.0 | 100.0 | 100.0 | 97.2 | 99.9 | 88.2 | 100.0 | 100.0 | 100.0 | 97.2 | 99.9 | 88.8 |
| ADDRESS | 0.0 | 100.0 | 100.0 | 100.0 | 98.6 | 100.0 | 89.3 | 100.0 | 100.0 | 100.0 | 98.6 | 100.0 | 96.2 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 99.6 | 100.0 | 55.4 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 100.0 | 100.0 | 99.6 | 100.0 | 15.6 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| URL | 51.0 | 100.0 | 100.0 | 100.0 | 29.6 | 100.0 | 0.1 | 51.0 | 51.0 | 51.0 | 51.0 | 51.0 | 51.0 |
| IP_ADDRESS | 100.0 | 100.0 | 100.0 | 100.0 | 88.2 | 100.0 | 22.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 | 100.0 | 100.0 | 95.5 | 100.0 | 32.7 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 96.8 | 100.0 | 100.0 | 100.0 | 99.0 | 100.0 | 87.3 | 96.8 | 96.8 | 96.8 | 96.5 | 96.8 | 96.8 |
| SECRET | 100.0 | 100.0 | 100.0 | 100.0 | 88.1 | 100.0 | 39.6 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.6 |
