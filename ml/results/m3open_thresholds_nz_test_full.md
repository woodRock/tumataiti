## int4 open students across decoding thresholds

| Metric | rules+deberta-v3-small-open-t0.1 | rules+deberta-v3-small-open-t0.3 | rules+deberta-v3-small-open-t0.5 | rules+deberta-v3-small-open-t0.7 | rules+deberta-v3-small-open-t0.9 | rules+modernbert-base-open-t0.1 | rules+modernbert-base-open-t0.3 | rules+modernbert-base-open-t0.5 | rules+modernbert-base-open-t0.7 | rules+modernbert-base-open-t0.9 | rules+mdeberta-v3-base-open-t0.1 | rules+mdeberta-v3-base-open-t0.3 | rules+mdeberta-v3-base-open-t0.5 | rules+mdeberta-v3-base-open-t0.7 | rules+mdeberta-v3-base-open-t0.9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **1.8%** | **2.0%** | **2.1%** | **2.6%** | **5.7%** | **2.5%** | **4.1%** | **6.5%** | **11.0%** | **21.9%** | **1.6%** | **1.9%** | **2.3%** | **2.9%** | **4.7%** |
| Span leak rate | 0.3% | 0.3% | 0.4% | 0.4% | 1.0% | 0.4% | 0.7% | 1.2% | 2.1% | 4.6% | 0.3% | 0.3% | 0.4% | 0.5% | 0.9% |
| Any-PII char precision | 91.6 | 92.0 | 92.3 | 92.6 | 93.3 | 91.0 | 92.1 | 92.7 | 93.3 | 94.7 | 91.1 | 92.0 | 92.4 | 92.8 | 93.4 |
| Any-PII char recall | 99.9 | 99.8 | 99.8 | 99.8 | 99.5 | 99.8 | 99.7 | 99.5 | 99.0 | 97.7 | 99.8 | 99.8 | 99.7 | 99.7 | 99.5 |
| Any-PII char F1 | 95.6 | 95.8 | 95.9 | 96.1 | 96.3 | 95.2 | 95.7 | 96.0 | 96.1 | 96.2 | 95.2 | 95.7 | 95.9 | 96.1 | 96.3 |
| Exact-span F1 (all categories) | 84.1 | 84.7 | 85.1 | 85.4 | 85.7 | 83.0 | 84.6 | 85.1 | 85.4 | 86.4 | 74.1 | 75.5 | 76.0 | 76.6 | 77.3 |
| Median ms per document | 61.69 | 55.69 | 57.60 | 55.83 | 55.65 | 144.30 | 161.97 | 144.43 | 161.90 | 162.26 | 114.09 | 114.43 | 118.85 | 119.23 | 120.32 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open-t0.1 | rules+deberta-v3-small-open-t0.3 | rules+deberta-v3-small-open-t0.5 | rules+deberta-v3-small-open-t0.7 | rules+deberta-v3-small-open-t0.9 | rules+modernbert-base-open-t0.1 | rules+modernbert-base-open-t0.3 | rules+modernbert-base-open-t0.5 | rules+modernbert-base-open-t0.7 | rules+modernbert-base-open-t0.9 | rules+mdeberta-v3-base-open-t0.1 | rules+mdeberta-v3-base-open-t0.3 | rules+mdeberta-v3-base-open-t0.5 | rules+mdeberta-v3-base-open-t0.7 | rules+mdeberta-v3-base-open-t0.9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (6250 spans) | 0.0% | 0.0% | 0.0% | 0.2% | 1.7% | 1.1% | 1.5% | 2.1% | 3.4% | 8.6% | 0.7% | 0.8% | 1.0% | 1.3% | 2.2% |
| ADDRESS (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.1% | 0.3% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (5000 spans) | 1.0% | 1.1% | 1.1% | 1.1% | 1.2% | 0.0% | 0.5% | 1.2% | 2.4% | 3.8% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open-t0.1 | rules+deberta-v3-small-open-t0.3 | rules+deberta-v3-small-open-t0.5 | rules+deberta-v3-small-open-t0.7 | rules+deberta-v3-small-open-t0.9 | rules+modernbert-base-open-t0.1 | rules+modernbert-base-open-t0.3 | rules+modernbert-base-open-t0.5 | rules+modernbert-base-open-t0.7 | rules+modernbert-base-open-t0.9 | rules+mdeberta-v3-base-open-t0.1 | rules+mdeberta-v3-base-open-t0.3 | rules+mdeberta-v3-base-open-t0.5 | rules+mdeberta-v3-base-open-t0.7 | rules+mdeberta-v3-base-open-t0.9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 95.2 | 95.5 | 95.7 | 95.8 | 95.7 | 93.2 | 93.8 | 94.4 | 94.8 | 93.8 | 94.0 | 94.7 | 94.8 | 94.9 | 95.1 |
| ADDRESS | 96.7 | 96.8 | 96.9 | 97.2 | 97.9 | 97.6 | 97.8 | 97.9 | 98.2 | 98.9 | 95.3 | 97.1 | 97.9 | 98.9 | 99.8 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 97.7 | 97.7 | 97.7 | 97.9 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 97.6 | 98.2 | 98.5 | 98.7 | 99.2 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 82.3 | 88.8 | 90.4 | 91.8 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| AFFILIATION | 91.5 | 91.8 | 92.0 | 92.3 | 92.8 | 95.2 | 95.4 | 95.3 | 95.1 | 94.9 | 95.4 | 95.5 | 95.6 | 95.7 | 95.9 |
