## fp16 encoder

| Metric | rules+deberta-v3-small-int8-fp16 | rules+modernbert-base-int8-fp16 | rules+mdeberta-v3-base-int8-fp16 |
|---|---:|---:|---:|
| **Document leak rate** (lower is better) | **4.6%** | **2.6%** | **1.1%** |
| Span leak rate | 0.8% | 0.6% | 0.2% |
| Any-PII char precision | 93.4 | 93.3 | 93.7 |
| Any-PII char recall | 99.7 | 99.7 | 99.9 |
| Any-PII char F1 | 96.5 | 96.4 | 96.7 |
| Exact-span F1 (all categories) | 90.2 | 89.8 | 70.9 |
| Median ms per document | 38.77 | 114.84 | 59.35 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-int8-fp16 | rules+modernbert-base-int8-fp16 | rules+mdeberta-v3-base-int8-fp16 |
|---|---:|---:|---:|
| PERSON (5250 spans) | 1.6% | 1.1% | 0.4% |
| ADDRESS (1000 spans) | 0.0% | 0.0% | 0.0% |
| EMAIL (750 spans) | 0.0% | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-int8-fp16 | rules+modernbert-base-int8-fp16 | rules+mdeberta-v3-base-int8-fp16 |
|---|---:|---:|---:|
| PERSON | 98.3 | 97.0 | 99.6 |
| ADDRESS | 100.0 | 100.0 | 100.0 |
| EMAIL | 100.0 | 100.0 | 100.0 |
| PHONE | 99.8 | 99.1 | 99.9 |
| DATE | 89.6 | 99.2 | 86.0 |
| ID | 100.0 | 100.0 | 99.9 |
