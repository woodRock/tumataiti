## False-alarm set (600 documents)

| Metric | rules | deberta-v3-small-open-int8-int4-block | deberta-v3-small-open-int8-int4-block+review | rules+deberta-v3-small-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block+review |
|---|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **83.3%** | **0.0%** | **0.0%** | **0.0%** | **0.0%** |
| Span leak rate | 64.3% | 0.0% | 0.0% | 0.0% | 0.0% |
| Any-PII char precision | 100.0 | 70.0 | 77.2 | 70.0 | 77.2 |
| Any-PII char recall | 38.8 | 100.0 | 100.0 | 100.0 | 100.0 |
| Any-PII char F1 | 55.9 | 82.4 | 87.2 | 82.4 | 87.2 |
| Exact-span F1 (all categories) | 52.6 | 59.4 | 65.8 | 59.4 | 65.8 |
| Median ms per document | 0.03 | 16.52 | 16.52 | 16.55 | 16.55 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small-open-int8-int4-block | deberta-v3-small-open-int8-int4-block+review | rules+deberta-v3-small-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block+review |
|---|---:|---:|---:|---:|---:|
| PERSON (800 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ADDRESS (100 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small-open-int8-int4-block | deberta-v3-small-open-int8-int4-block+review | rules+deberta-v3-small-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block+review |
|---|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 80.2 | 91.6 | 80.2 | 91.6 |
| ADDRESS | 0.0 | 97.2 | 97.2 | 97.2 | 97.2 |
| EMAIL | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| PHONE | 100.0 | 99.8 | 99.8 | 99.8 | 99.8 |
| ID | 100.0 | 51.7 | 51.7 | 51.7 | 51.7 |
