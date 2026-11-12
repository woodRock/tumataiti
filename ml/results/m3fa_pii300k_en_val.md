## PII-Masking-300k, English validation

| Metric | rules | deberta-small-open-v4 | deberta-small-open-v4-1ep | deberta-small-open-v4-1ep-s1 | deberta-small-open-v4kin | deberta-small-open-v4kin-s1 | deberta-small-open-v4ids | rules+deberta-small-open-v4 | rules+deberta-small-open-v4-1ep | rules+deberta-small-open-v4-1ep-s1 | rules+deberta-small-open-v4kin | rules+deberta-small-open-v4kin-s1 | rules+deberta-small-open-v4ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **95.9%** | **35.1%** | **30.8%** | **32.8%** | **31.3%** | **32.5%** | **29.2%** | **32.3%** | **28.4%** | **31.7%** | **29.0%** | **31.0%** | **27.6%** |
| Span leak rate | 85.4% | 12.7% | 10.3% | 11.0% | 10.5% | 11.0% | 9.6% | 11.4% | 9.1% | 10.4% | 9.3% | 10.2% | 8.8% |
| Any-PII char precision | 96.5 | 95.0 | 94.8 | 94.9 | 94.9 | 94.9 | 94.8 | 94.9 | 94.7 | 94.8 | 94.8 | 94.8 | 94.6 |
| Any-PII char recall | 20.1 | 92.2 | 92.4 | 92.9 | 92.2 | 92.7 | 93.3 | 93.0 | 93.2 | 93.3 | 93.1 | 93.2 | 93.8 |
| Any-PII char F1 | 33.2 | 93.6 | 93.6 | 93.9 | 93.5 | 93.8 | 94.0 | 93.9 | 93.9 | 94.0 | 93.9 | 94.0 | 94.2 |
| Exact-span F1 (all categories) | 23.9 | 77.1 | 77.8 | 76.5 | 77.9 | 76.9 | 78.1 | 77.9 | 78.1 | 76.5 | 78.3 | 77.1 | 78.3 |
| Median ms per document | 0.01 | 17.08 | 9.70 | 9.17 | 9.69 | 9.92 | 5.20 | 17.09 | 9.71 | 9.18 | 9.70 | 9.93 | 5.21 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-small-open-v4 | deberta-small-open-v4-1ep | deberta-small-open-v4-1ep-s1 | deberta-small-open-v4kin | deberta-small-open-v4kin-s1 | deberta-small-open-v4ids | rules+deberta-small-open-v4 | rules+deberta-small-open-v4-1ep | rules+deberta-small-open-v4-1ep-s1 | rules+deberta-small-open-v4kin | rules+deberta-small-open-v4kin-s1 | rules+deberta-small-open-v4ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5808 spans) | 99.9% | 5.4% | 3.9% | 5.2% | 4.3% | 5.4% | 3.4% | 5.4% | 3.8% | 5.1% | 4.3% | 5.4% | 3.4% |
| ADDRESS (8852 spans) | 100.0% | 18.4% | 9.0% | 15.3% | 9.2% | 13.8% | 9.8% | 18.4% | 9.0% | 15.3% | 9.2% | 13.8% | 9.8% |
| EMAIL (2612 spans) | 0.6% | 1.0% | 0.2% | 0.5% | 0.4% | 0.5% | 0.2% | 0.1% | 0.1% | 0.1% | 0.1% | 0.1% | 0.1% |
| PHONE (1997 spans) | 99.3% | 1.9% | 2.8% | 1.3% | 2.6% | 1.4% | 1.6% | 1.9% | 2.8% | 1.3% | 2.6% | 1.4% | 1.6% |
| IP_ADDRESS (2166 spans) | 50.4% | 0.6% | 0.6% | 0.6% | 0.6% | 0.6% | 0.7% | 0.6% | 0.6% | 0.6% | 0.6% | 0.6% | 0.6% |
| DATE (2317 spans) | 66.0% | 75.1% | 77.9% | 64.4% | 77.4% | 67.6% | 68.2% | 56.3% | 60.8% | 56.3% | 60.9% | 56.6% | 57.3% |
| ID (10054 spans) | 97.0% | 3.4% | 4.1% | 3.8% | 4.2% | 4.6% | 3.5% | 3.4% | 4.0% | 3.7% | 4.1% | 4.5% | 3.5% |
| SECRET (1620 spans) | 76.5% | 24.1% | 19.9% | 20.0% | 21.9% | 16.7% | 20.6% | 24.1% | 19.8% | 19.9% | 21.7% | 16.7% | 20.4% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-small-open-v4 | deberta-small-open-v4-1ep | deberta-small-open-v4-1ep-s1 | deberta-small-open-v4kin | deberta-small-open-v4kin-s1 | deberta-small-open-v4ids | rules+deberta-small-open-v4 | rules+deberta-small-open-v4-1ep | rules+deberta-small-open-v4-1ep-s1 | rules+deberta-small-open-v4kin | rules+deberta-small-open-v4kin-s1 | rules+deberta-small-open-v4ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 91.3 | 91.8 | 90.9 | 91.4 | 90.8 | 91.4 | 91.3 | 91.8 | 90.9 | 91.3 | 90.8 | 91.4 |
| ADDRESS | 0.0 | 90.1 | 92.0 | 90.5 | 92.0 | 91.0 | 91.4 | 90.1 | 92.0 | 90.5 | 92.0 | 91.0 | 91.4 |
| EMAIL | 98.1 | 96.9 | 97.3 | 97.1 | 97.2 | 97.0 | 97.2 | 97.3 | 97.2 | 97.1 | 97.2 | 97.2 | 97.2 |
| PHONE | 2.7 | 87.4 | 86.2 | 84.8 | 85.2 | 85.8 | 84.5 | 84.6 | 83.4 | 82.6 | 82.6 | 83.4 | 82.1 |
| IP_ADDRESS | 39.2 | 93.4 | 93.9 | 92.3 | 94.8 | 92.7 | 95.1 | 93.4 | 93.9 | 92.3 | 94.7 | 92.7 | 95.1 |
| DATE | 49.8 | 59.1 | 49.2 | 65.5 | 51.4 | 63.8 | 60.7 | 69.0 | 61.0 | 69.7 | 63.3 | 69.4 | 67.6 |
| ID | 2.9 | 93.1 | 92.4 | 91.9 | 92.6 | 91.7 | 92.9 | 92.3 | 91.6 | 91.2 | 91.8 | 90.9 | 92.1 |
| SECRET | 40.4 | 79.3 | 85.3 | 83.1 | 85.0 | 82.4 | 85.1 | 78.7 | 83.6 | 81.5 | 83.2 | 81.5 | 83.3 |
