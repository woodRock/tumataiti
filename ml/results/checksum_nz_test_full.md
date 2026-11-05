## Rules with and without check digits: nz_test_full

| Metric | rules | rules-format-only |
|---|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **100.0%** |
| Span leak rate | 64.1% | 64.1% |
| Any-PII char precision | 88.8 | 88.8 |
| Any-PII char recall | 38.6 | 38.6 |
| Any-PII char F1 | 53.8 | 53.8 |
| Exact-span F1 (all categories) | 51.9 | 55.2 |
| Median ms per document | – | – |

Span leak rate by category (lower is better):

| Metric | rules | rules-format-only |
|---|---:|---:|
| PERSON (5250 spans) | 100.0% | 100.0% |
| ADDRESS (1000 spans) | 100.0% | 100.0% |
| EMAIL (750 spans) | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | rules-format-only |
|---|---:|---:|
| PERSON | 0.0 | 0.0 |
| ADDRESS | 0.0 | 0.0 |
| EMAIL | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 |
| ID | 100.0 | 100.0 |
