## Rules with and without check digits: pii300k_en_val

| Metric | rules | rules-format-only |
|---|---:|---:|
| **Document leak rate** (lower is better) | **95.9%** | **93.8%** |
| Span leak rate | 85.4% | 78.3% |
| Any-PII char precision | 96.5 | 96.7 |
| Any-PII char recall | 20.1 | 26.8 |
| Any-PII char F1 | 33.2 | 42.0 |
| Exact-span F1 (all categories) | 23.9 | 34.7 |
| Median ms per document | – | – |

Span leak rate by category (lower is better):

| Metric | rules | rules-format-only |
|---|---:|---:|
| PERSON (5808 spans) | 99.9% | 99.9% |
| ADDRESS (8852 spans) | 100.0% | 100.0% |
| EMAIL (2612 spans) | 0.6% | 0.6% |
| PHONE (1997 spans) | 99.3% | 99.3% |
| IP_ADDRESS (2166 spans) | 50.4% | 50.4% |
| DATE (2317 spans) | 66.0% | 66.0% |
| ID (10054 spans) | 97.0% | 71.8% |
| SECRET (1620 spans) | 76.5% | 76.5% |

Character-level F1 by category (category must match):

| Metric | rules | rules-format-only |
|---|---:|---:|
| PERSON | 0.0 | 0.0 |
| ADDRESS | 0.0 | 0.0 |
| EMAIL | 98.1 | 98.1 |
| PHONE | 2.7 | 2.3 |
| IP_ADDRESS | 39.2 | 39.2 |
| DATE | 49.8 | 49.8 |
| ID | 2.9 | 39.0 |
| SECRET | 40.4 | 40.4 |
