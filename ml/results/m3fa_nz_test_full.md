## NZ synthetic v1, held-out templates and names (1,750 documents)

| Metric | rules | deberta-small-open-v2 | deberta-small-open-v2-1ep | deberta-small-open-v2-1ep-s1 | deberta-small-open-v3 | deberta-small-open-v3-s1 | deberta-small-open-v3ids | rules+deberta-small-open-v2 | rules+deberta-small-open-v2-1ep | rules+deberta-small-open-v2-1ep-s1 | rules+deberta-small-open-v3 | rules+deberta-small-open-v3-s1 | rules+deberta-small-open-v3ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **0.3%** | **1.4%** | **0.3%** | **2.1%** | **2.6%** | **1.9%** | **0.3%** | **0.0%** | **0.0%** | **1.4%** | **0.9%** | **1.6%** |
| Span leak rate | 64.1% | 0.1% | 0.3% | 0.1% | 0.4% | 0.5% | 0.4% | 0.1% | 0.0% | 0.0% | 0.3% | 0.2% | 0.3% |
| Any-PII char precision | 88.8 | 99.0 | 97.5 | 97.4 | 97.9 | 97.8 | 98.6 | 94.4 | 93.1 | 93.0 | 93.4 | 93.4 | 94.1 |
| Any-PII char recall | 38.6 | 100.0 | 99.9 | 100.0 | 99.8 | 99.8 | 99.8 | 100.0 | 100.0 | 100.0 | 99.9 | 99.9 | 99.8 |
| Any-PII char F1 | 53.8 | 99.5 | 98.7 | 98.7 | 98.8 | 98.8 | 99.2 | 97.1 | 96.5 | 96.4 | 96.6 | 96.6 | 96.9 |
| Exact-span F1 (all categories) | 51.9 | 93.4 | 91.5 | 92.2 | 92.0 | 92.5 | 91.4 | 92.2 | 90.6 | 91.1 | 91.0 | 91.7 | 90.4 |
| Median ms per document | 0.05 | 11.38 | 11.75 | 12.01 | 11.96 | 12.01 | 11.71 | 11.43 | 11.80 | 12.06 | 12.00 | 12.06 | 11.75 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-small-open-v2 | deberta-small-open-v2-1ep | deberta-small-open-v2-1ep-s1 | deberta-small-open-v3 | deberta-small-open-v3-s1 | deberta-small-open-v3ids | rules+deberta-small-open-v2 | rules+deberta-small-open-v2-1ep | rules+deberta-small-open-v2-1ep-s1 | rules+deberta-small-open-v3 | rules+deberta-small-open-v3-s1 | rules+deberta-small-open-v3ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5250 spans) | 100.0% | 0.1% | 0.0% | 0.0% | 0.5% | 0.3% | 0.6% | 0.1% | 0.0% | 0.0% | 0.5% | 0.3% | 0.6% |
| ADDRESS (1000 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 5.0% | 1.2% | 2.8% | 6.2% | 1.4% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-small-open-v2 | deberta-small-open-v2-1ep | deberta-small-open-v2-1ep-s1 | deberta-small-open-v3 | deberta-small-open-v3-s1 | deberta-small-open-v3ids | rules+deberta-small-open-v2 | rules+deberta-small-open-v2-1ep | rules+deberta-small-open-v2-1ep-s1 | rules+deberta-small-open-v3 | rules+deberta-small-open-v3-s1 | rules+deberta-small-open-v3ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 98.5 | 96.8 | 96.7 | 97.1 | 97.2 | 97.8 | 98.5 | 96.8 | 96.7 | 97.1 | 97.2 | 97.8 |
| ADDRESS | 0.0 | 100.0 | 99.8 | 100.0 | 99.9 | 100.0 | 99.6 | 100.0 | 99.8 | 100.0 | 99.9 | 100.0 | 99.6 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 | 98.8 | 99.7 | 99.5 | 98.4 | 99.6 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.8 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
