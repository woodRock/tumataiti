## open_en_test: review layer without and with transaction labels

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| **Document leak rate** (lower is better) | **3.8%** | **4.3%** |
| Span leak rate | 1.2% | 1.4% |
| Any-PII char precision | 98.8 | 98.9 |
| Any-PII char recall | 99.2 | 99.2 |
| Any-PII char F1 | 99.0 | 99.0 |
| Exact-span F1 (all categories) | 95.6 | 95.5 |
| Median ms per document | 17.07 | 17.07 |

Span leak rate by category (lower is better):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON (2011 spans) | 2.1% | 2.1% |
| ADDRESS (839 spans) | 3.0% | 3.0% |
| EMAIL (792 spans) | 0.4% | 0.4% |
| PHONE (505 spans) | 0.4% | 0.4% |
| URL (394 spans) | 0.3% | 0.3% |
| IP_ADDRESS (314 spans) | 0.0% | 0.0% |
| DATE (629 spans) | 1.6% | 1.6% |
| ID (2818 spans) | 0.3% | 0.7% |
| SECRET (334 spans) | 4.8% | 4.8% |

Character-level F1 by category (category must match):

| Metric | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|
| PERSON | 98.0 | 98.0 |
| ADDRESS | 98.6 | 98.6 |
| EMAIL | 99.7 | 99.7 |
| PHONE | 97.1 | 97.1 |
| URL | 95.7 | 95.7 |
| IP_ADDRESS | 88.1 | 88.1 |
| DATE | 98.6 | 98.6 |
| ID | 98.6 | 98.5 |
| SECRET | 97.7 | 97.7 |
