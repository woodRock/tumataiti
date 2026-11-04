## NZ synthetic v1, training templates with held-out names (1,600 documents)

| Metric | rules | deberta-small-open-v2 | deberta-small-open-v2-1ep | deberta-small-open-v2-1ep-s1 | deberta-small-open-v3 | deberta-small-open-v3-s1 | deberta-small-open-v3ids | rules+deberta-small-open-v2 | rules+deberta-small-open-v2-1ep | rules+deberta-small-open-v2-1ep-s1 | rules+deberta-small-open-v3 | rules+deberta-small-open-v3-s1 | rules+deberta-small-open-v3ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **93.8%** | **0.1%** | **0.1%** | **0.0%** | **0.1%** | **0.0%** | **0.2%** | **0.1%** | **0.1%** | **0.0%** | **0.1%** | **0.0%** | **0.2%** |
| Span leak rate | 45.8% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Any-PII char precision | 89.4 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 93.7 | 93.7 | 93.7 | 93.7 | 93.7 | 93.7 |
| Any-PII char recall | 57.3 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| Any-PII char F1 | 69.8 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 96.7 | 96.7 | 96.7 | 96.7 | 96.7 | 96.7 |
| Exact-span F1 (all categories) | 67.0 | 99.9 | 99.9 | 99.9 | 99.9 | 100.0 | 99.9 | 96.6 | 96.7 | 96.7 | 96.7 | 96.7 | 96.6 |
| Median ms per document | 0.04 | 11.30 | 11.54 | 12.26 | 12.13 | 11.82 | 11.67 | 11.34 | 11.59 | 12.31 | 12.17 | 11.86 | 11.71 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-small-open-v2 | deberta-small-open-v2-1ep | deberta-small-open-v2-1ep-s1 | deberta-small-open-v3 | deberta-small-open-v3-s1 | deberta-small-open-v3ids | rules+deberta-small-open-v2 | rules+deberta-small-open-v2-1ep | rules+deberta-small-open-v2-1ep-s1 | rules+deberta-small-open-v3 | rules+deberta-small-open-v3-s1 | rules+deberta-small-open-v3ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (3100 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| ADDRESS (700 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (1100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| URL (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| IP_ADDRESS (200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (600 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (1200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| SECRET (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-small-open-v2 | deberta-small-open-v2-1ep | deberta-small-open-v2-1ep-s1 | deberta-small-open-v3 | deberta-small-open-v3-s1 | deberta-small-open-v3ids | rules+deberta-small-open-v2 | rules+deberta-small-open-v2-1ep | rules+deberta-small-open-v2-1ep-s1 | rules+deberta-small-open-v3 | rules+deberta-small-open-v3-s1 | rules+deberta-small-open-v3ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 99.7 | 99.9 | 100.0 | 100.0 | 100.0 | 99.9 | 99.7 | 99.9 | 100.0 | 100.0 | 100.0 | 99.9 |
| ADDRESS | 0.0 | 100.0 | 100.0 | 100.0 | 99.9 | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 | 99.9 | 100.0 | 99.9 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| URL | 51.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 51.0 | 51.0 | 51.0 | 51.0 | 51.0 | 51.0 |
| IP_ADDRESS | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 96.8 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 96.8 | 96.8 | 96.8 | 96.8 | 96.8 | 96.8 |
| SECRET | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
