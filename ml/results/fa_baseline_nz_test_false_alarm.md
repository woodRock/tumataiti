## False-alarm set (600 documents)

| Metric | rules | deberta-v3-small-open-int8-int4-block | deberta-v3-small-open-int8-int4-block+review | rules+deberta-v3-small-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block+review |
|---|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **83.3%** | **0.0%** | **1.0%** | **0.0%** | **1.0%** |
| Span leak rate | 64.3% | 0.0% | 0.4% | 0.0% | 0.4% |
| Any-PII char precision | 100.0 | 70.1 | 78.2 | 70.1 | 78.2 |
| Any-PII char recall | 38.8 | 100.0 | 99.9 | 100.0 | 99.9 |
| Any-PII char F1 | 55.9 | 82.4 | 87.7 | 82.4 | 87.7 |
| Exact-span F1 (all categories) | 52.6 | 59.4 | 66.6 | 59.4 | 66.6 |
| Median ms per document | 0.03 | 19.38 | 19.38 | 19.41 | 19.41 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small-open-int8-int4-block | deberta-v3-small-open-int8-int4-block+review | rules+deberta-v3-small-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block+review |
|---|---:|---:|---:|---:|---:|
| PERSON (800 spans) | 100.0% | 0.0% | 0.8% | 0.0% | 0.8% |
| ADDRESS (100 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small-open-int8-int4-block | deberta-v3-small-open-int8-int4-block+review | rules+deberta-v3-small-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block+review |
|---|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 80.3 | 93.1 | 80.3 | 93.1 |
| ADDRESS | 0.0 | 99.9 | 99.9 | 99.9 | 99.9 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| ID | 100.0 | 50.6 | 50.6 | 50.6 | 50.6 |
