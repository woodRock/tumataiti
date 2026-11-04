## NZ synthetic v1, training templates with held-out names (1,600 documents)

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **93.8%** | **49.2%** | **0.1%** | **0.0%** | **3.2%** | **42.0%** | **0.1%** | **0.0%** | **3.1%** |
| Span leak rate | 45.8% | 21.8% | 0.0% | 0.0% | 0.7% | 14.4% | 0.0% | 0.0% | 0.7% |
| Any-PII char precision | 89.4 | 88.3 | 100.0 | 100.0 | 100.0 | 84.0 | 93.7 | 93.7 | 93.6 |
| Any-PII char recall | 57.3 | 81.3 | 100.0 | 100.0 | 99.6 | 88.1 | 100.0 | 100.0 | 99.6 |
| Any-PII char F1 | 69.8 | 84.7 | 100.0 | 100.0 | 99.8 | 86.0 | 96.7 | 96.7 | 96.5 |
| Exact-span F1 (all categories) | 67.0 | 69.5 | 99.9 | 99.4 | 68.0 | 75.6 | 96.6 | 96.4 | 79.2 |
| Median ms per document | 0.04 | 247.69 | 13.25 | 21.21 | 22.84 | 247.74 | 13.29 | 21.26 | 22.89 |

Span leak rate by category (lower is better):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (3100 spans) | 100.0% | 31.1% | 0.0% | 0.0% | 1.7% | 31.1% | 0.0% | 0.0% | 1.7% |
| ADDRESS (700 spans) | 100.0% | 32.4% | 0.0% | 0.0% | 0.0% | 32.4% | 0.0% | 0.0% | 0.0% |
| EMAIL (1100 spans) | 0.0% | 0.8% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1200 spans) | 0.0% | 18.1% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| URL (100 spans) | 0.0% | 25.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| IP_ADDRESS (200 spans) | 0.0% | 11.5% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (600 spans) | 0.0% | 26.2% | 0.0% | 0.0% | 0.2% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (1200 spans) | 0.0% | 15.4% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| SECRET (100 spans) | 0.0% | 2.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 76.6 | 99.7 | 100.0 | 99.3 | 76.9 | 99.7 | 100.0 | 99.3 |
| ADDRESS | 0.0 | 78.5 | 100.0 | 100.0 | 99.9 | 78.8 | 100.0 | 100.0 | 99.9 |
| EMAIL | 100.0 | 99.5 | 100.0 | 100.0 | 100.0 | 99.8 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 85.6 | 100.0 | 100.0 | 100.0 | 99.2 | 100.0 | 100.0 | 100.0 |
| URL | 51.0 | 66.4 | 100.0 | 100.0 | 100.0 | 51.0 | 51.0 | 51.0 | 51.0 |
| IP_ADDRESS | 100.0 | 0.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| DATE | 100.0 | 63.3 | 100.0 | 100.0 | 100.0 | 83.1 | 100.0 | 100.0 | 100.0 |
| ID | 96.8 | 78.6 | 100.0 | 100.0 | 100.0 | 89.1 | 96.8 | 96.8 | 96.8 |
| SECRET | 100.0 | 89.6 | 100.0 | 100.0 | 100.0 | 92.6 | 100.0 | 100.0 | 100.0 |
