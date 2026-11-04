## open_en_test: review layer without and with transaction labels

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| **Document leak rate** (lower is better) | **3.1%** | **3.7%** |
| Span leak rate | 1.1% | 1.2% |
| Any-PII char precision | 98.9 | 98.9 |
| Any-PII char recall | 99.3 | 99.3 |
| Any-PII char F1 | 99.1 | 99.1 |
| Exact-span F1 (all categories) | 95.6 | 95.6 |
| Median ms per document | 10.91 | 10.91 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON (2011 spans) | 1.9% | 1.9% |
| ADDRESS (839 spans) | 2.5% | 2.5% |
| EMAIL (792 spans) | 0.4% | 0.4% |
| PHONE (505 spans) | 0.4% | 0.4% |
| URL (394 spans) | 0.3% | 0.3% |
| IP_ADDRESS (314 spans) | 0.0% | 0.0% |
| DATE (629 spans) | 1.4% | 1.4% |
| ID (2818 spans) | 0.2% | 0.6% |
| SECRET (334 spans) | 4.5% | 4.5% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON | 98.2 | 98.2 |
| ADDRESS | 98.8 | 98.8 |
| EMAIL | 99.6 | 99.6 |
| PHONE | 97.2 | 97.2 |
| URL | 95.5 | 95.5 |
| IP_ADDRESS | 88.2 | 88.2 |
| DATE | 98.7 | 98.7 |
| ID | 98.7 | 98.5 |
| SECRET | 97.4 | 97.4 |
