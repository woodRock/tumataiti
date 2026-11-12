## NZ synthetic v4, held-out templates, names and affiliations

| Metric | rules | deberta-small-open-v4 | deberta-small-open-v4-1ep | deberta-small-open-v4-1ep-s1 | deberta-small-open-v4kin | deberta-small-open-v4kin-s1 | deberta-small-open-v4ids | rules+deberta-small-open-v4 | rules+deberta-small-open-v4-1ep | rules+deberta-small-open-v4-1ep-s1 | rules+deberta-small-open-v4kin | rules+deberta-small-open-v4kin-s1 | rules+deberta-small-open-v4ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **2.3%** | **0.1%** | **0.1%** | **2.7%** | **1.3%** | **0.6%** | **2.0%** | **0.1%** | **0.0%** | **2.0%** | **0.7%** | **0.5%** |
| Span leak rate | 76.6% | 0.4% | 0.0% | 0.0% | 0.5% | 0.2% | 0.1% | 0.4% | 0.0% | 0.0% | 0.3% | 0.1% | 0.1% |
| Any-PII char precision | 90.0 | 94.5 | 93.9 | 94.7 | 94.9 | 96.3 | 95.5 | 92.0 | 91.4 | 92.2 | 92.4 | 93.7 | 92.9 |
| Any-PII char recall | 26.0 | 99.8 | 100.0 | 100.0 | 99.8 | 99.9 | 99.9 | 99.8 | 100.0 | 100.0 | 99.8 | 99.9 | 99.9 |
| Any-PII char F1 | 40.4 | 97.1 | 96.9 | 97.3 | 97.3 | 98.0 | 97.7 | 95.7 | 95.5 | 96.0 | 96.0 | 96.7 | 96.3 |
| Exact-span F1 (all categories) | 37.5 | 83.9 | 87.0 | 86.1 | 86.6 | 89.0 | 89.0 | 83.5 | 86.3 | 85.5 | 86.1 | 88.4 | 88.4 |
| Median ms per document | 0.05 | 9.86 | 11.25 | 9.10 | 8.73 | 9.35 | 4.92 | 9.91 | 11.30 | 9.14 | 8.78 | 9.40 | 4.96 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-small-open-v4 | deberta-small-open-v4-1ep | deberta-small-open-v4-1ep-s1 | deberta-small-open-v4kin | deberta-small-open-v4kin-s1 | deberta-small-open-v4ids | rules+deberta-small-open-v4 | rules+deberta-small-open-v4-1ep | rules+deberta-small-open-v4-1ep-s1 | rules+deberta-small-open-v4kin | rules+deberta-small-open-v4kin-s1 | rules+deberta-small-open-v4ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (6250 spans) | 100.0% | 0.1% | 0.0% | 0.0% | 0.1% | 0.4% | 0.2% | 0.1% | 0.0% | 0.0% | 0.1% | 0.4% | 0.2% |
| ADDRESS (1000 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 1.4% | 0.0% | 0.8% | 4.2% | 3.4% | 0.6% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (5000 spans) | 100.0% | 1.0% | 0.0% | 0.0% | 0.9% | 0.0% | 0.0% | 1.0% | 0.0% | 0.0% | 0.9% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-small-open-v4 | deberta-small-open-v4-1ep | deberta-small-open-v4-1ep-s1 | deberta-small-open-v4kin | deberta-small-open-v4kin-s1 | deberta-small-open-v4ids | rules+deberta-small-open-v4 | rules+deberta-small-open-v4-1ep | rules+deberta-small-open-v4-1ep-s1 | rules+deberta-small-open-v4kin | rules+deberta-small-open-v4kin-s1 | rules+deberta-small-open-v4ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 96.2 | 95.3 | 95.6 | 96.1 | 95.5 | 94.1 | 96.2 | 95.3 | 95.6 | 96.1 | 95.5 | 94.1 |
| ADDRESS | 0.0 | 96.3 | 96.7 | 97.1 | 96.6 | 96.8 | 96.9 | 96.3 | 96.7 | 97.1 | 96.6 | 96.8 | 96.9 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| DATE | 100.0 | 99.7 | 100.0 | 99.8 | 99.1 | 99.3 | 99.9 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| AFFILIATION | 0.0 | 91.7 | 93.7 | 93.0 | 92.9 | 93.7 | 95.7 | 91.7 | 93.7 | 93.0 | 92.9 | 93.7 | 95.7 |
