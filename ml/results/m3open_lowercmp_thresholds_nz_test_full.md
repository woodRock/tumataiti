## Deployed and retrained, int4, across decoding thresholds

| Metric | rules+deberta-v3-small-open-t0.1 | rules+retrained-t0.1 | rules+deberta-v3-small-open-t0.3 | rules+retrained-t0.3 | rules+deberta-v3-small-open-t0.5 | rules+retrained-t0.5 | rules+deberta-v3-small-open-t0.7 | rules+retrained-t0.7 | rules+deberta-v3-small-open-t0.9 | rules+retrained-t0.9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **1.8%** | **0.5%** | **2.0%** | **1.7%** | **2.1%** | **2.6%** | **2.6%** | **3.9%** | **5.7%** | **8.1%** |
| Span leak rate | 0.3% | 0.1% | 0.3% | 0.3% | 0.4% | 0.5% | 0.4% | 0.8% | 1.0% | 1.7% |
| Any-PII char precision | 91.6 | 92.2 | 92.0 | 93.0 | 92.3 | 93.6 | 92.6 | 94.0 | 93.3 | 94.6 |
| Any-PII char recall | 99.9 | 99.9 | 99.8 | 99.8 | 99.8 | 99.7 | 99.8 | 99.4 | 99.5 | 98.7 |
| Any-PII char F1 | 95.6 | 95.9 | 95.8 | 96.3 | 95.9 | 96.5 | 96.1 | 96.7 | 96.3 | 96.6 |
| Exact-span F1 (all categories) | 84.1 | 85.0 | 84.7 | 86.4 | 85.1 | 87.5 | 85.4 | 88.2 | 85.7 | 88.1 |
| Median ms per document | 61.69 | 55.82 | 55.69 | 58.18 | 57.60 | 61.52 | 55.83 | 61.67 | 55.65 | 68.20 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open-t0.1 | rules+retrained-t0.1 | rules+deberta-v3-small-open-t0.3 | rules+retrained-t0.3 | rules+deberta-v3-small-open-t0.5 | rules+retrained-t0.5 | rules+deberta-v3-small-open-t0.7 | rules+retrained-t0.7 | rules+deberta-v3-small-open-t0.9 | rules+retrained-t0.9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (6250 spans) | 0.0% | 0.1% | 0.0% | 0.2% | 0.0% | 0.3% | 0.2% | 0.5% | 1.7% | 1.0% |
| ADDRESS (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% |
| EMAIL (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (5000 spans) | 1.0% | 0.2% | 1.1% | 0.7% | 1.1% | 1.2% | 1.1% | 1.9% | 1.2% | 4.1% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open-t0.1 | rules+retrained-t0.1 | rules+deberta-v3-small-open-t0.3 | rules+retrained-t0.3 | rules+deberta-v3-small-open-t0.5 | rules+retrained-t0.5 | rules+deberta-v3-small-open-t0.7 | rules+retrained-t0.7 | rules+deberta-v3-small-open-t0.9 | rules+retrained-t0.9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 95.2 | 93.5 | 95.5 | 94.0 | 95.7 | 94.7 | 95.8 | 95.2 | 95.7 | 95.6 |
| ADDRESS | 96.7 | 96.6 | 96.8 | 97.3 | 96.9 | 97.5 | 97.2 | 97.7 | 97.9 | 98.5 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 100.0 | 99.8 | 100.0 | 99.9 | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 | 100.0 |
| AFFILIATION | 91.5 | 94.7 | 91.8 | 95.0 | 92.0 | 95.0 | 92.3 | 94.8 | 92.8 | 94.0 |
