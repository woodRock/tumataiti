## NZ synthetic v4, training templates with held-out names and affiliations

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **95.7%** | **64.5%** | **0.1%** | **0.0%** | **3.0%** | **59.9%** | **0.1%** | **0.0%** | **3.0%** |
| Span leak rate | 63.4% | 43.3% | 0.0% | 0.0% | 0.6% | 38.5% | 0.0% | 0.0% | 0.6% |
| Any-PII char precision | 90.2 | 89.0 | 100.0 | 100.0 | 100.0 | 85.1 | 95.8 | 95.8 | 95.8 |
| Any-PII char recall | 40.3 | 61.3 | 100.0 | 100.0 | 99.7 | 65.6 | 100.0 | 100.0 | 99.7 |
| Any-PII char F1 | 55.8 | 72.6 | 100.0 | 100.0 | 99.8 | 74.1 | 97.9 | 97.9 | 97.7 |
| Exact-span F1 (all categories) | 51.6 | 54.6 | 99.7 | 98.9 | 77.9 | 60.2 | 97.6 | 96.8 | 85.6 |
| Median ms per document | 0.04 | 296.18 | 16.90 | 14.02 | 16.37 | 296.22 | 16.94 | 14.07 | 16.41 |

Span leak rate by category (lower is better):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (3900 spans) | 100.0% | 39.7% | 0.1% | 0.0% | 1.9% | 39.7% | 0.1% | 0.0% | 1.9% |
| ADDRESS (700 spans) | 100.0% | 30.4% | 0.0% | 0.0% | 0.0% | 30.4% | 0.0% | 0.0% | 0.0% |
| EMAIL (1200 spans) | 0.0% | 1.2% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1400 spans) | 0.0% | 15.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| URL (100 spans) | 0.0% | 18.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| IP_ADDRESS (200 spans) | 0.0% | 12.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (600 spans) | 0.0% | 27.8% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (1200 spans) | 0.0% | 15.8% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| SECRET (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (3700 spans) | 100.0% | 88.7% | 0.0% | 0.0% | 0.0% | 88.7% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | openai-privacy-filter | deberta-v3-small-open | modernbert-base-open | mdeberta-v3-base-open | rules+openai-privacy-filter | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 67.1 | 99.7 | 99.3 | 99.3 | 67.4 | 99.7 | 99.3 | 99.3 |
| ADDRESS | 0.0 | 78.2 | 100.0 | 100.0 | 100.0 | 79.0 | 100.0 | 100.0 | 100.0 |
| EMAIL | 100.0 | 99.4 | 100.0 | 100.0 | 100.0 | 99.8 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 86.5 | 100.0 | 100.0 | 100.0 | 99.2 | 100.0 | 100.0 | 100.0 |
| URL | 51.6 | 70.3 | 100.0 | 100.0 | 100.0 | 51.6 | 51.6 | 51.6 | 51.6 |
| IP_ADDRESS | 100.0 | 0.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| DATE | 100.0 | 61.4 | 100.0 | 100.0 | 100.0 | 83.5 | 100.0 | 100.0 | 100.0 |
| ID | 96.7 | 77.3 | 100.0 | 100.0 | 100.0 | 88.6 | 96.7 | 96.7 | 96.7 |
| SECRET | 100.0 | 89.6 | 100.0 | 100.0 | 100.0 | 91.7 | 100.0 | 100.0 | 100.0 |
| AFFILIATION | 0.0 | 0.0 | 99.8 | 99.4 | 100.0 | 0.0 | 99.8 | 99.4 | 100.0 |
