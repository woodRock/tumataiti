## Rules with and without check digits: nz_test_full

| Metric | rules | rules-format-only |
|---|---:|---:|
| **Document leak rate** (lower is better) | **100.0%** | **100.0%** |
| Span leak rate | 76.6% | 76.6% |
| Any-PII char precision | 90.0 | 90.0 |
| Any-PII char recall | 26.0 | 26.0 |
| Any-PII char F1 | 40.4 | 40.4 |
| Exact-span F1 (all categories) | 37.5 | 40.5 |
| Median ms per document | – | – |

Span leak rate by category (lower is better):

| Metric | rules | rules-format-only |
|---|---:|---:|
| PERSON (6250 spans) | 100.0% | 100.0% |
| ADDRESS (1000 spans) | 100.0% | 100.0% |
| EMAIL (1000 spans) | 0.0% | 0.0% |
| PHONE (1500 spans) | 0.0% | 0.0% |
| DATE (500 spans) | 0.0% | 0.0% |
| ID (750 spans) | 0.0% | 0.0% |
| AFFILIATION (5000 spans) | 100.0% | 100.0% |

Character-level F1 by category (category must match):

| Metric | rules | rules-format-only |
|---|---:|---:|
| PERSON | 0.0 | 0.0 |
| ADDRESS | 0.0 | 0.0 |
| EMAIL | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 |
| ID | 100.0 | 100.0 |
| AFFILIATION | 0.0 | 0.0 |
