## int4 open students across decoding thresholds

| Metric | rules+deberta-v3-small-open-t0.1 | rules+deberta-v3-small-open-t0.3 | rules+deberta-v3-small-open-t0.5 | rules+deberta-v3-small-open-t0.7 | rules+deberta-v3-small-open-t0.9 | rules+modernbert-base-open-t0.1 | rules+modernbert-base-open-t0.3 | rules+modernbert-base-open-t0.5 | rules+modernbert-base-open-t0.7 | rules+modernbert-base-open-t0.9 | rules+mdeberta-v3-base-open-t0.1 | rules+mdeberta-v3-base-open-t0.3 | rules+mdeberta-v3-base-open-t0.5 | rules+mdeberta-v3-base-open-t0.7 | rules+mdeberta-v3-base-open-t0.9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **0.1%** | **0.2%** | **0.7%** | **1.9%** | **5.7%** | **0.9%** | **1.5%** | **2.7%** | **5.8%** | **14.1%** | **0.9%** | **1.1%** | **1.4%** | **1.8%** | **3.4%** |
| Span leak rate | 0.0% | 0.0% | 0.1% | 0.3% | 1.1% | 0.2% | 0.3% | 0.6% | 1.2% | 3.1% | 0.2% | 0.2% | 0.2% | 0.3% | 0.7% |
| Any-PII char precision | 94.1 | 94.3 | 94.4 | 94.4 | 94.5 | 90.8 | 91.9 | 92.4 | 92.6 | 93.2 | 93.4 | 93.6 | 93.8 | 93.9 | 94.2 |
| Any-PII char recall | 100.0 | 100.0 | 99.9 | 99.8 | 99.4 | 99.9 | 99.8 | 99.7 | 99.4 | 98.5 | 99.9 | 99.9 | 99.9 | 99.8 | 99.7 |
| Any-PII char F1 | 97.0 | 97.1 | 97.1 | 97.0 | 96.9 | 95.1 | 95.7 | 95.9 | 95.9 | 95.8 | 96.6 | 96.6 | 96.7 | 96.8 | 96.9 |
| Exact-span F1 (all categories) | 91.5 | 92.2 | 92.2 | 92.1 | 91.6 | 83.9 | 86.1 | 87.1 | 87.2 | 86.8 | 71.6 | 72.5 | 73.0 | 73.4 | 74.1 |
| Median ms per document | 62.43 | 62.78 | 62.77 | 62.78 | 59.25 | 153.69 | 163.35 | 163.43 | 153.65 | 200.29 | 126.12 | 136.36 | 126.37 | 125.48 | 119.76 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open-t0.1 | rules+deberta-v3-small-open-t0.3 | rules+deberta-v3-small-open-t0.5 | rules+deberta-v3-small-open-t0.7 | rules+deberta-v3-small-open-t0.9 | rules+modernbert-base-open-t0.1 | rules+modernbert-base-open-t0.3 | rules+modernbert-base-open-t0.5 | rules+modernbert-base-open-t0.7 | rules+modernbert-base-open-t0.9 | rules+mdeberta-v3-base-open-t0.1 | rules+mdeberta-v3-base-open-t0.3 | rules+mdeberta-v3-base-open-t0.5 | rules+mdeberta-v3-base-open-t0.7 | rules+mdeberta-v3-base-open-t0.9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5250 spans) | 0.0% | 0.1% | 0.2% | 0.6% | 2.0% | 0.4% | 0.6% | 1.0% | 2.2% | 5.7% | 0.3% | 0.4% | 0.5% | 0.6% | 1.2% |
| ADDRESS (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open-t0.1 | rules+deberta-v3-small-open-t0.3 | rules+deberta-v3-small-open-t0.5 | rules+deberta-v3-small-open-t0.7 | rules+deberta-v3-small-open-t0.9 | rules+modernbert-base-open-t0.1 | rules+modernbert-base-open-t0.3 | rules+modernbert-base-open-t0.5 | rules+modernbert-base-open-t0.7 | rules+modernbert-base-open-t0.9 | rules+mdeberta-v3-base-open-t0.1 | rules+mdeberta-v3-base-open-t0.3 | rules+mdeberta-v3-base-open-t0.5 | rules+mdeberta-v3-base-open-t0.7 | rules+mdeberta-v3-base-open-t0.9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 98.1 | 98.3 | 98.3 | 98.2 | 97.8 | 94.0 | 94.4 | 94.4 | 94.2 | 93.7 | 97.2 | 97.4 | 97.6 | 97.8 | 98.0 |
| ADDRESS | 99.9 | 99.9 | 99.9 | 99.9 | 99.9 | 97.3 | 97.6 | 97.6 | 97.6 | 97.8 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 98.4 | 98.7 | 99.0 | 99.1 | 99.4 | 99.9 | 99.9 | 99.9 | 100.0 | 100.0 |
| DATE | 99.8 | 100.0 | 100.0 | 100.0 | 100.0 | 88.7 | 94.8 | 98.2 | 99.0 | 99.8 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 | 99.9 | 99.9 | 99.9 | 100.0 |
