## Open-data students, quantised: held-out templates and names (fp32 on GPU, others on laptop CPU)

| Metric | rules+deberta-v3-small-open | rules+deberta-v3-small-open-int8 | rules+deberta-v3-small-open-int8-fp16 | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open | rules+modernbert-base-open-int8 | rules+modernbert-base-open-int8-fp16 | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open | rules+mdeberta-v3-base-open-int8 | rules+mdeberta-v3-base-open-int8-fp16 | rules+mdeberta-v3-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-gather | rules+mdeberta-v3-base-open-int8-matmul |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **0.3%** | **5.6%** | **0.3%** | **0.7%** | **4.1%** | **17.6%** | **3.9%** | **2.7%** | **2.7%** | **23.0%** | **2.7%** | **1.4%** | **2.7%** | **22.4%** |
| Span leak rate | 0.1% | 1.2% | 0.1% | 0.1% | 0.8% | 4.2% | 0.8% | 0.6% | 0.5% | 9.3% | 0.5% | 0.2% | 0.5% | 9.2% |
| Any-PII char precision | 94.4 | 94.5 | 94.4 | 94.4 | 92.1 | 91.4 | 92.1 | 92.4 | 94.4 | 90.4 | 94.4 | 93.8 | 94.4 | 90.4 |
| Any-PII char recall | 100.0 | 99.5 | 100.0 | 99.9 | 99.6 | 98.1 | 99.6 | 99.7 | 99.7 | 95.5 | 99.7 | 99.9 | 99.7 | 95.6 |
| Any-PII char F1 | 97.1 | 96.9 | 97.1 | 97.1 | 95.7 | 94.6 | 95.7 | 95.9 | 97.0 | 92.9 | 97.0 | 96.7 | 97.0 | 92.9 |
| Exact-span F1 (all categories) | 92.2 | 91.4 | 92.1 | 92.2 | 87.8 | 84.5 | 87.8 | 87.1 | 73.3 | 53.6 | 73.3 | 73.0 | 73.3 | 53.5 |
| Median ms per document | 11.43 | 14.48 | 26.54 | 29.48 | 18.01 | 33.36 | 81.83 | 103.76 | 23.45 | 33.05 | 73.80 | 78.27 | 66.36 | 46.82 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open | rules+deberta-v3-small-open-int8 | rules+deberta-v3-small-open-int8-fp16 | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open | rules+modernbert-base-open-int8 | rules+modernbert-base-open-int8-fp16 | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open | rules+mdeberta-v3-base-open-int8 | rules+mdeberta-v3-base-open-int8-fp16 | rules+mdeberta-v3-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-gather | rules+mdeberta-v3-base-open-int8-matmul |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON (5250 spans) | 0.1% | 2.2% | 0.1% | 0.2% | 1.5% | 7.6% | 1.4% | 1.0% | 1.0% | 17.2% | 1.0% | 0.5% | 1.0% | 16.9% |
| ADDRESS (1000 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.8% | 0.0% | 0.0% | 0.0% | 0.7% | 0.0% | 0.0% | 0.0% | 0.8% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open | rules+deberta-v3-small-open-int8 | rules+deberta-v3-small-open-int8-fp16 | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open | rules+modernbert-base-open-int8 | rules+modernbert-base-open-int8-fp16 | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open | rules+mdeberta-v3-base-open-int8 | rules+mdeberta-v3-base-open-int8-fp16 | rules+mdeberta-v3-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-gather | rules+mdeberta-v3-base-open-int8-matmul |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 98.5 | 98.1 | 98.5 | 98.3 | 94.8 | 94.1 | 94.8 | 94.4 | 98.3 | 90.8 | 98.3 | 97.6 | 98.3 | 90.8 |
| ADDRESS | 100.0 | 100.0 | 100.0 | 99.9 | 99.2 | 99.1 | 99.1 | 97.6 | 100.0 | 97.2 | 100.0 | 100.0 | 100.0 | 97.2 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 96.3 | 100.0 | 100.0 | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 100.0 | 100.0 | 99.0 | 99.1 | 98.9 | 99.0 | 99.9 | 99.9 | 99.9 | 99.9 | 99.9 | 99.9 |
| DATE | 100.0 | 100.0 | 100.0 | 100.0 | 98.6 | 99.1 | 98.8 | 98.2 | 100.0 | 97.2 | 100.0 | 100.0 | 100.0 | 96.8 |
| ID | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 99.9 | 100.0 | 100.0 |
