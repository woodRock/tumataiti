## PII-Masking-300k, English validation (7,946 documents)

| Metric | rules | deberta-small-open-v2 | deberta-small-open-v2-1ep | deberta-small-open-v2-1ep-s1 | deberta-small-open-v3 | deberta-small-open-v3-s1 | deberta-small-open-v3ids | rules+deberta-small-open-v2 | rules+deberta-small-open-v2-1ep | rules+deberta-small-open-v2-1ep-s1 | rules+deberta-small-open-v3 | rules+deberta-small-open-v3-s1 | rules+deberta-small-open-v3ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **95.9%** | **32.7%** | **27.9%** | **35.0%** | **28.3%** | **36.8%** | **29.2%** | **31.4%** | **25.6%** | **32.8%** | **25.9%** | **34.3%** | **26.8%** |
| Span leak rate | 85.4% | 11.9% | 9.2% | 12.1% | 9.2% | 12.9% | 9.6% | 11.0% | 8.1% | 10.9% | 8.2% | 11.6% | 8.6% |
| Any-PII char precision | 96.5 | 95.0 | 94.7 | 94.9 | 94.7 | 94.8 | 94.7 | 94.9 | 94.6 | 94.7 | 94.6 | 94.7 | 94.6 |
| Any-PII char recall | 20.1 | 92.5 | 93.0 | 92.0 | 93.2 | 91.3 | 92.8 | 93.2 | 93.8 | 92.9 | 94.0 | 92.3 | 93.6 |
| Any-PII char F1 | 33.2 | 93.7 | 93.8 | 93.4 | 94.0 | 93.0 | 93.7 | 94.0 | 94.2 | 93.8 | 94.3 | 93.5 | 94.1 |
| Exact-span F1 (all categories) | 23.9 | 76.6 | 77.6 | 76.7 | 77.9 | 75.7 | 77.5 | 76.8 | 77.9 | 77.2 | 78.2 | 76.4 | 77.7 |
| Median ms per document | 0.01 | 11.90 | 11.87 | 11.87 | 12.07 | 12.13 | 12.21 | 11.91 | 11.87 | 11.88 | 12.08 | 12.14 | 12.22 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-small-open-v2 | deberta-small-open-v2-1ep | deberta-small-open-v2-1ep-s1 | deberta-small-open-v3 | deberta-small-open-v3-s1 | deberta-small-open-v3ids | rules+deberta-small-open-v2 | rules+deberta-small-open-v2-1ep | rules+deberta-small-open-v2-1ep-s1 | rules+deberta-small-open-v3 | rules+deberta-small-open-v3-s1 | rules+deberta-small-open-v3ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5808 spans) | 99.9% | 7.4% | 3.8% | 4.3% | 3.3% | 6.0% | 3.9% | 7.4% | 3.8% | 4.3% | 3.3% | 5.9% | 3.8% |
| ADDRESS (8852 spans) | 100.0% | 15.1% | 8.1% | 16.8% | 8.0% | 16.6% | 9.1% | 15.1% | 8.1% | 16.8% | 8.0% | 16.6% | 9.1% |
| EMAIL (2612 spans) | 0.6% | 0.1% | 0.2% | 0.5% | 0.1% | 0.8% | 0.1% | 0.1% | 0.1% | 0.1% | 0.1% | 0.1% | 0.1% |
| PHONE (1997 spans) | 99.3% | 1.8% | 1.9% | 1.2% | 1.9% | 1.2% | 1.9% | 1.8% | 1.9% | 1.2% | 1.9% | 1.2% | 1.9% |
| IP_ADDRESS (2166 spans) | 50.4% | 0.6% | 0.6% | 0.6% | 0.6% | 0.6% | 0.6% | 0.6% | 0.6% | 0.6% | 0.6% | 0.6% | 0.6% |
| DATE (2317 spans) | 66.0% | 67.2% | 71.9% | 74.1% | 71.3% | 77.3% | 71.0% | 54.3% | 56.3% | 56.8% | 56.0% | 58.9% | 56.1% |
| ID (10054 spans) | 97.0% | 3.2% | 3.4% | 4.0% | 3.7% | 5.4% | 3.5% | 3.2% | 3.4% | 4.0% | 3.6% | 5.4% | 3.5% |
| SECRET (1620 spans) | 76.5% | 31.6% | 15.7% | 23.0% | 17.0% | 22.3% | 19.8% | 31.4% | 15.4% | 22.9% | 17.0% | 22.2% | 19.6% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-small-open-v2 | deberta-small-open-v2-1ep | deberta-small-open-v2-1ep-s1 | deberta-small-open-v3 | deberta-small-open-v3-s1 | deberta-small-open-v3ids | rules+deberta-small-open-v2 | rules+deberta-small-open-v2-1ep | rules+deberta-small-open-v2-1ep-s1 | rules+deberta-small-open-v3 | rules+deberta-small-open-v3-s1 | rules+deberta-small-open-v3ids |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 89.9 | 91.4 | 91.3 | 91.6 | 90.7 | 91.6 | 89.9 | 91.4 | 91.3 | 91.6 | 90.7 | 91.6 |
| ADDRESS | 0.0 | 90.6 | 92.6 | 90.1 | 92.5 | 90.2 | 91.9 | 90.6 | 92.6 | 90.1 | 92.5 | 90.2 | 91.9 |
| EMAIL | 98.1 | 97.2 | 97.2 | 97.1 | 97.2 | 97.0 | 97.2 | 97.2 | 97.2 | 97.2 | 97.2 | 97.2 | 97.1 |
| PHONE | 2.7 | 84.8 | 86.3 | 85.9 | 85.7 | 85.4 | 85.1 | 82.1 | 83.6 | 83.5 | 83.0 | 83.0 | 82.4 |
| IP_ADDRESS | 39.2 | 92.1 | 93.0 | 92.9 | 93.6 | 92.9 | 92.9 | 92.1 | 93.0 | 92.9 | 93.6 | 92.9 | 92.9 |
| DATE | 49.8 | 63.2 | 51.7 | 57.4 | 56.9 | 55.1 | 52.1 | 70.9 | 63.4 | 68.8 | 66.7 | 67.6 | 63.1 |
| ID | 2.9 | 92.1 | 92.7 | 92.4 | 92.5 | 91.4 | 92.1 | 91.3 | 91.9 | 91.7 | 91.7 | 90.6 | 91.3 |
| SECRET | 40.4 | 76.1 | 86.4 | 83.0 | 85.7 | 82.5 | 84.3 | 74.4 | 84.7 | 81.4 | 84.0 | 81.4 | 82.6 |
