## Rules with and without check digits: nz_test_false_alarm

| Metric | rules | rules-format-only |
|---|---:|---:|
| **Document leak rate** (lower is better) | **83.3%** | **83.3%** |
| Span leak rate | 64.3% | 64.3% |
| Any-PII char precision | 100.0 | 63.7 |
| Any-PII char recall | 38.8 | 38.8 |
| Any-PII char F1 | 55.9 | 48.2 |
| Exact-span F1 (all categories) | 52.6 | 51.9 |
| Median ms per document | – | – |

Span leak rate by category (lower is better):

| Metric | rules | rules-format-only |
|---|---:|---:|
| PERSON (800 spans) | 100.0% | 100.0% |
| ADDRESS (100 spans) | 100.0% | 100.0% |
| EMAIL (100 spans) | 0.0% | 0.0% |
| PHONE (200 spans) | 0.0% | 0.0% |
| ID (200 spans) | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | rules-format-only |
|---|---:|---:|
| PERSON | 0.0 | 0.0 |
| ADDRESS | 0.0 | 0.0 |
| EMAIL | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 |
| ID | 100.0 | 50.0 |
