## NZ synthetic v0 (1,600 documents)

| Metric | rules | openai-privacy-filter | rules+openai-privacy-filter |
|---|---:|---:|---:|
| **Document leak rate** (lower is better) | **93.8%** | **43.2%** | **36.2%** |
| Span leak rate | 45.8% | 16.8% | 11.0% |
| Any-PII char precision | 89.4 | 88.2 | 83.8 |
| Any-PII char recall | 57.8 | 85.6 | 90.7 |
| Any-PII char F1 | 70.2 | 86.9 | 87.1 |
| Exact-span F1 (all categories) | 67.0 | 70.5 | 75.8 |
| Median ms per document | 0.04 | 240.87 | 240.91 |

Span leak rate by category (lower is better):

| Metric | rules | openai-privacy-filter | rules+openai-privacy-filter |
|---|---:|---:|---:|
| PERSON (3100 spans) | 100.0% | 23.4% | 23.4% |
| ADDRESS (700 spans) | 100.0% | 26.3% | 26.3% |
| EMAIL (1100 spans) | 0.0% | 0.7% | 0.0% |
| PHONE (1200 spans) | 0.0% | 14.2% | 0.0% |
| URL (100 spans) | 0.0% | 11.0% | 0.0% |
| IP_ADDRESS (200 spans) | 0.0% | 3.0% | 0.0% |
| DATE (600 spans) | 0.0% | 21.0% | 0.0% |
| ID (1200 spans) | 0.0% | 14.0% | 0.0% |
| SECRET (100 spans) | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | openai-privacy-filter | rules+openai-privacy-filter |
|---|---:|---:|---:|
| PERSON | 0.0 | 79.1 | 79.4 |
| ADDRESS | 0.0 | 81.8 | 82.3 |
| EMAIL | 100.0 | 99.5 | 99.7 |
| PHONE | 100.0 | 87.4 | 98.9 |
| URL | 51.4 | 72.5 | 51.4 |
| IP_ADDRESS | 100.0 | 0.0 | 100.0 |
| DATE | 100.0 | 65.7 | 82.4 |
| ID | 96.8 | 79.5 | 89.2 |
| SECRET | 100.0 | 91.3 | 92.2 |
