## Deployed and retrained, int4, across decoding thresholds

| Metric | rules+deberta-v3-small-open-t0.1 | rules+retrained-t0.1 | rules+deberta-v3-small-open-t0.3 | rules+retrained-t0.3 | rules+deberta-v3-small-open-t0.5 | rules+retrained-t0.5 | rules+deberta-v3-small-open-t0.7 | rules+retrained-t0.7 | rules+deberta-v3-small-open-t0.9 | rules+retrained-t0.9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **0.1%** | **0.0%** | **0.2%** | **0.0%** | **0.7%** | **0.3%** | **1.9%** | **1.5%** | **5.7%** | **12.6%** |
| Span leak rate | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.1% | 0.3% | 0.3% | 1.1% | 2.6% |
| Any-PII char precision | 94.1 | 92.6 | 94.3 | 92.8 | 94.4 | 93.0 | 94.4 | 93.3 | 94.5 | 94.3 |
| Any-PII char recall | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 | 100.0 | 99.8 | 99.9 | 99.4 | 98.8 |
| Any-PII char F1 | 97.0 | 96.2 | 97.1 | 96.2 | 97.1 | 96.3 | 97.0 | 96.5 | 96.9 | 96.5 |
| Exact-span F1 (all categories) | 91.5 | 88.3 | 92.2 | 90.1 | 92.2 | 91.0 | 92.1 | 91.8 | 91.6 | 91.2 |
| Median ms per document | 62.43 | 58.98 | 62.78 | 62.55 | 62.77 | 58.78 | 62.78 | 79.79 | 59.25 | 56.45 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open-t0.1 | rules+retrained-t0.1 | rules+deberta-v3-small-open-t0.3 | rules+retrained-t0.3 | rules+deberta-v3-small-open-t0.5 | rules+retrained-t0.5 | rules+deberta-v3-small-open-t0.7 | rules+retrained-t0.7 | rules+deberta-v3-small-open-t0.9 | rules+retrained-t0.9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5250 spans) | 0.0% | 0.0% | 0.1% | 0.0% | 0.2% | 0.1% | 0.6% | 0.6% | 2.0% | 4.9% |
| ADDRESS (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open-t0.1 | rules+retrained-t0.1 | rules+deberta-v3-small-open-t0.3 | rules+retrained-t0.3 | rules+deberta-v3-small-open-t0.5 | rules+retrained-t0.5 | rules+deberta-v3-small-open-t0.7 | rules+retrained-t0.7 | rules+deberta-v3-small-open-t0.9 | rules+retrained-t0.9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 98.1 | 96.3 | 98.3 | 96.5 | 98.3 | 96.7 | 98.2 | 96.9 | 97.8 | 97.0 |
| ADDRESS | 99.9 | 99.6 | 99.9 | 99.6 | 99.9 | 99.7 | 99.9 | 99.9 | 99.9 | 100.0 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 99.8 | 100.0 | 99.8 | 100.0 | 99.8 | 100.0 | 99.8 | 100.0 | 99.9 |
| DATE | 99.8 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
