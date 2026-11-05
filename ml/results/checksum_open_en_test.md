## Rules with and without check digits: open_en_test

| Metric | rules | rules-format-only |
|---|---:|---:|
| **Document leak rate** (lower is better) | **96.4%** | **95.5%** |
| Span leak rate | 74.5% | 71.4% |
| Any-PII char precision | 98.8 | 98.6 |
| Any-PII char recall | 38.6 | 41.6 |
| Any-PII char F1 | 55.5 | 58.5 |
| Exact-span F1 (all categories) | 39.5 | 43.0 |
| Median ms per document | – | – |

Span leak rate by category (lower is better):

| Metric | rules | rules-format-only |
|---|---:|---:|
| PERSON (2011 spans) | 100.0% | 100.0% |
| ADDRESS (839 spans) | 100.0% | 100.0% |
| EMAIL (792 spans) | 0.4% | 0.4% |
| PHONE (505 spans) | 97.2% | 96.2% |
| URL (394 spans) | 7.4% | 7.4% |
| IP_ADDRESS (314 spans) | 15.9% | 15.9% |
| DATE (629 spans) | 20.3% | 20.3% |
| ID (2818 spans) | 91.5% | 82.2% |
| SECRET (334 spans) | 91.9% | 91.9% |

Character-level F1 by category (category must match):

| Metric | rules | rules-format-only |
|---|---:|---:|
| PERSON | 0.0 | 0.0 |
| ADDRESS | 0.0 | 0.0 |
| EMAIL | 99.7 | 99.7 |
| PHONE | 4.7 | 4.9 |
| URL | 91.1 | 91.1 |
| IP_ADDRESS | 67.5 | 67.5 |
| DATE | 88.3 | 88.3 |
| ID | 21.0 | 36.6 |
| SECRET | 16.3 | 16.3 |
