## Deployed and retrained, int4: nz_test_names

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| **Document leak rate** (lower is better) | **0.0%** | **0.1%** |
| Span leak rate | 0.0% | 0.0% |
| Any-PII char precision | 93.7 | 93.7 |
| Any-PII char recall | 100.0 | 100.0 |
| Any-PII char F1 | 96.7 | 96.7 |
| Exact-span F1 (all categories) | 96.6 | 96.7 |
| Median ms per document | 27.19 | 56.31 |

Span leak rate by category (lower is better):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON (3100 spans) | 0.0% | 0.1% |
| ADDRESS (700 spans) | 0.0% | 0.0% |
| EMAIL (1100 spans) | 0.0% | 0.0% |
| PHONE (1200 spans) | 0.0% | 0.0% |
| URL (100 spans) | 0.0% | 0.0% |
| IP_ADDRESS (200 spans) | 0.0% | 0.0% |
| DATE (600 spans) | 0.0% | 0.0% |
| ID (1200 spans) | 0.0% | 0.0% |
| SECRET (100 spans) | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON | 99.7 | 100.0 |
| ADDRESS | 100.0 | 100.0 |
| EMAIL | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 |
| URL | 51.0 | 51.0 |
| IP_ADDRESS | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 |
| ID | 96.8 | 96.8 |
| SECRET | 100.0 | 100.0 |
