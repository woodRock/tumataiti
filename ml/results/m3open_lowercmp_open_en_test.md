## Deployed and retrained, int4: open_en_test

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| **Document leak rate** (lower is better) | **3.2%** | **4.0%** |
| Span leak rate | 1.1% | 1.3% |
| Any-PII char precision | 98.9 | 98.8 |
| Any-PII char recall | 99.4 | 99.3 |
| Any-PII char F1 | 99.1 | 99.0 |
| Exact-span F1 (all categories) | 95.4 | 94.4 |
| Median ms per document | 50.58 | 74.84 |

Span leak rate by category (lower is better):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON (2011 spans) | 2.1% | 2.5% |
| ADDRESS (839 spans) | 2.3% | 3.8% |
| EMAIL (792 spans) | 0.4% | 0.4% |
| PHONE (505 spans) | 0.4% | 0.4% |
| URL (394 spans) | 0.3% | 0.3% |
| IP_ADDRESS (314 spans) | 0.0% | 0.0% |
| DATE (629 spans) | 1.7% | 2.5% |
| ID (2818 spans) | 0.2% | 0.1% |
| SECRET (334 spans) | 4.5% | 2.4% |

Character-level F1 by category (category must match):

| Metric | rules+deployed | rules+retrained |
|---|---:|---:|
| PERSON | 98.2 | 98.0 |
| ADDRESS | 98.8 | 98.7 |
| EMAIL | 99.6 | 99.7 |
| PHONE | 97.0 | 95.7 |
| URL | 95.6 | 95.7 |
| IP_ADDRESS | 88.2 | 88.1 |
| DATE | 98.6 | 98.5 |
| ID | 98.6 | 98.2 |
| SECRET | 97.5 | 97.6 |
