## Deployed and retrained, int4: nz_test_names

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| **Document leak rate** (lower is better) | **0.1%** | **0.4%** |
| Span leak rate | 0.0% | 0.1% |
| Any-PII char precision | 95.8 | 95.8 |
| Any-PII char recall | 100.0 | 100.0 |
| Any-PII char F1 | 97.9 | 97.8 |
| Exact-span F1 (all categories) | 97.4 | 97.5 |
| Median ms per document | 27.48 | 56.08 |

Span leak rate by category (lower is better):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON (3900 spans) | 0.1% | 0.3% |
| ADDRESS (700 spans) | 0.0% | 0.0% |
| EMAIL (1200 spans) | 0.0% | 0.0% |
| PHONE (1400 spans) | 0.0% | 0.0% |
| URL (100 spans) | 0.0% | 0.0% |
| IP_ADDRESS (200 spans) | 0.0% | 0.0% |
| DATE (600 spans) | 0.0% | 0.0% |
| ID (1200 spans) | 0.0% | 0.0% |
| SECRET (100 spans) | 0.0% | 0.0% |
| AFFILIATION (3700 spans) | 0.0% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON | 99.3 | 99.7 |
| ADDRESS | 100.0 | 100.0 |
| EMAIL | 100.0 | 100.0 |
| PHONE | 100.0 | 100.0 |
| URL | 51.6 | 51.6 |
| IP_ADDRESS | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 |
| ID | 96.7 | 96.7 |
| SECRET | 100.0 | 100.0 |
| AFFILIATION | 99.4 | 99.9 |
