## Open-data students, quantised: held-out templates and names (fp32 on GPU, others on laptop CPU)

| Metric | rules+deberta-v3-small-open | rules+deberta-v3-small-open-int8 | rules+deberta-v3-small-open-int8-fp16 | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open | rules+modernbert-base-open-int8 | rules+modernbert-base-open-int8-fp16 | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open | rules+mdeberta-v3-base-open-int8 | rules+mdeberta-v3-base-open-int8-fp16 | rules+mdeberta-v3-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-gather | rules+mdeberta-v3-base-open-int8-matmul |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **2.0%** | **6.3%** | **2.3%** | **2.1%** | **3.8%** | **27.4%** | **4.2%** | **6.5%** | **2.5%** | **32.4%** | **2.5%** | **2.3%** | **2.5%** | **32.2%** |
| Span leak rate | 0.4% | 1.1% | 0.4% | 0.4% | 0.7% | 6.3% | 0.7% | 1.2% | 0.4% | 9.5% | 0.4% | 0.4% | 0.4% | 9.1% |
| Any-PII char precision | 92.0 | 92.9 | 91.8 | 92.3 | 93.6 | 94.5 | 93.6 | 92.7 | 92.4 | 92.0 | 92.4 | 92.4 | 92.4 | 92.0 |
| Any-PII char recall | 99.8 | 99.2 | 99.8 | 99.8 | 99.7 | 97.0 | 99.7 | 99.5 | 99.7 | 95.2 | 99.7 | 99.7 | 99.7 | 95.5 |
| Any-PII char F1 | 95.7 | 95.9 | 95.7 | 95.9 | 96.5 | 95.7 | 96.5 | 96.0 | 95.9 | 93.6 | 95.9 | 95.9 | 95.9 | 93.7 |
| Exact-span F1 (all categories) | 83.5 | 84.9 | 83.2 | 85.1 | 87.4 | 81.6 | 87.1 | 85.1 | 76.1 | 33.5 | 76.2 | 76.0 | 76.2 | 33.2 |
| Median ms per document | 9.91 | 14.69 | 27.97 | 29.86 | 13.84 | 33.43 | 86.65 | 81.45 | 18.56 | 38.14 | 65.57 | 61.16 | 70.33 | 45.45 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open | rules+deberta-v3-small-open-int8 | rules+deberta-v3-small-open-int8-fp16 | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open | rules+modernbert-base-open-int8 | rules+modernbert-base-open-int8-fp16 | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open | rules+mdeberta-v3-base-open-int8 | rules+mdeberta-v3-base-open-int8-fp16 | rules+mdeberta-v3-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-gather | rules+mdeberta-v3-base-open-int8-matmul |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (6250 spans) | 0.1% | 1.0% | 0.1% | 0.0% | 1.2% | 11.7% | 1.4% | 2.1% | 1.1% | 15.7% | 1.1% | 1.0% | 1.1% | 15.3% |
| ADDRESS (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 0.0% | 7.4% | 0.0% | 0.0% | 0.0% | 7.1% |
| EMAIL (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (5000 spans) | 1.0% | 2.4% | 1.1% | 1.1% | 0.6% | 5.6% | 0.6% | 1.2% | 0.0% | 9.1% | 0.0% | 0.0% | 0.0% | 8.5% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open | rules+deberta-v3-small-open-int8 | rules+deberta-v3-small-open-int8-fp16 | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open | rules+modernbert-base-open-int8 | rules+modernbert-base-open-int8-fp16 | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open | rules+mdeberta-v3-base-open-int8 | rules+mdeberta-v3-base-open-int8-fp16 | rules+mdeberta-v3-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-gather | rules+mdeberta-v3-base-open-int8-matmul |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 96.2 | 94.7 | 96.0 | 95.7 | 94.8 | 90.9 | 94.8 | 94.4 | 96.0 | 60.8 | 96.0 | 94.8 | 96.0 | 60.7 |
| ADDRESS | 96.3 | 95.7 | 96.3 | 96.9 | 97.8 | 98.2 | 97.7 | 97.9 | 97.4 | 94.0 | 97.1 | 97.9 | 97.1 | 93.9 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 97.7 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 |
| PHONE | 100.0 | 100.0 | 100.0 | 100.0 | 98.6 | 99.8 | 98.4 | 98.5 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 | 100.0 | 100.0 | 98.2 | 99.2 | 98.2 | 90.4 | 100.0 | 99.6 | 100.0 | 100.0 | 100.0 | 99.7 |
| ID | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| AFFILIATION | 91.7 | 90.4 | 91.6 | 92.0 | 95.3 | 92.4 | 95.2 | 95.3 | 95.6 | 10.4 | 95.6 | 95.6 | 95.6 | 10.4 |
