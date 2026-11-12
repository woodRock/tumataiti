## NZ synthetic v4, training templates with held-out names and affiliations

| Metric | rules | deberta-small-open-v4 | deberta-small-open-v4-1ep | deberta-small-open-v4-1ep-s1 | deberta-small-open-v4kin | deberta-small-open-v4kin-s1 | deberta-small-open-v4ids | rules+deberta-small-open-v4 | rules+deberta-small-open-v4-1ep | rules+deberta-small-open-v4-1ep-s1 | rules+deberta-small-open-v4kin | rules+deberta-small-open-v4kin-s1 | rules+deberta-small-open-v4ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **95.7%** | **0.1%** | **0.0%** | **0.1%** | **0.2%** | **0.2%** | **0.3%** | **0.1%** | **0.0%** | **0.1%** | **0.2%** | **0.2%** | **0.3%** |
| Span leak rate | 63.4% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| Any-PII char precision | 90.2 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 95.8 | 95.8 | 95.8 | 95.8 | 95.8 | 95.8 |
| Any-PII char recall | 40.3 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| Any-PII char F1 | 55.8 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 97.9 | 97.9 | 97.9 | 97.9 | 97.9 | 97.8 |
| Exact-span F1 (all categories) | 51.6 | 99.7 | 99.9 | 99.8 | 99.8 | 99.6 | 99.7 | 97.6 | 97.8 | 97.7 | 97.7 | 97.5 | 97.6 |
| Median ms per document | 0.04 | 16.90 | 9.14 | 9.13 | 8.93 | 10.45 | 4.75 | 16.94 | 9.18 | 9.17 | 8.97 | 10.50 | 4.80 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-small-open-v4 | deberta-small-open-v4-1ep | deberta-small-open-v4-1ep-s1 | deberta-small-open-v4kin | deberta-small-open-v4kin-s1 | deberta-small-open-v4ids | rules+deberta-small-open-v4 | rules+deberta-small-open-v4-1ep | rules+deberta-small-open-v4-1ep-s1 | rules+deberta-small-open-v4kin | rules+deberta-small-open-v4kin-s1 | rules+deberta-small-open-v4ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (3900 spans) | 100.0% | 0.1% | 0.0% | 0.1% | 0.1% | 0.1% | 0.2% | 0.1% | 0.0% | 0.1% | 0.1% | 0.1% | 0.2% |
| ADDRESS (700 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (1200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1400 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| URL (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| IP_ADDRESS (200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (600 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (1200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| SECRET (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (3700 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-small-open-v4 | deberta-small-open-v4-1ep | deberta-small-open-v4-1ep-s1 | deberta-small-open-v4kin | deberta-small-open-v4kin-s1 | deberta-small-open-v4ids | rules+deberta-small-open-v4 | rules+deberta-small-open-v4-1ep | rules+deberta-small-open-v4-1ep-s1 | rules+deberta-small-open-v4kin | rules+deberta-small-open-v4kin-s1 | rules+deberta-small-open-v4ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 99.7 | 100.0 | 99.9 | 99.8 | 99.6 | 99.8 | 99.7 | 100.0 | 99.9 | 99.8 | 99.6 | 99.8 |
| ADDRESS | 0.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| URL | 51.6 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 51.6 | 51.6 | 51.6 | 51.6 | 51.6 | 51.6 |
| IP_ADDRESS | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 96.7 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 96.7 | 96.7 | 96.7 | 96.7 | 96.7 | 96.7 |
| SECRET | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| AFFILIATION | 0.0 | 99.8 | 100.0 | 99.9 | 99.8 | 99.7 | 99.9 | 99.8 | 100.0 | 99.9 | 99.8 | 99.7 | 99.9 |
