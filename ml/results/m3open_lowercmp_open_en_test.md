## Deployed and retrained, int4: open_en_test

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| **Document leak rate** (lower is better) | **3.4%** | **3.1%** |
| Span leak rate | 1.2% | 1.1% |
| Any-PII char precision | 98.9 | 98.8 |
| Any-PII char recall | 99.3 | 99.4 |
| Any-PII char F1 | 99.1 | 99.1 |
| Exact-span F1 (all categories) | 95.7 | 94.4 |
| Median ms per document | 48.14 | 79.92 |

Span leak rate by category (lower is better):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON (2011 spans) | 2.0% | 1.9% |
| ADDRESS (839 spans) | 2.3% | 2.1% |
| EMAIL (792 spans) | 0.4% | 0.4% |
| PHONE (505 spans) | 0.4% | 0.4% |
| URL (394 spans) | 0.3% | 0.3% |
| IP_ADDRESS (314 spans) | 0.0% | 0.0% |
| DATE (629 spans) | 1.9% | 2.4% |
| ID (2818 spans) | 0.3% | 0.2% |
| SECRET (334 spans) | 4.8% | 3.9% |

Character-level F1 by category (category must match):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON | 98.1 | 98.1 |
| ADDRESS | 98.8 | 99.0 |
| EMAIL | 99.7 | 99.6 |
| PHONE | 97.2 | 95.5 |
| URL | 95.7 | 95.7 |
| IP_ADDRESS | 88.1 | 88.1 |
| DATE | 98.5 | 98.4 |
| ID | 98.6 | 98.2 |
| SECRET | 97.8 | 97.8 |
