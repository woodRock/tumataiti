## NZ synthetic v4, training templates with held-out names and affiliations

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Document leak rate** (lower is better) | **95.7%** | **0.1%** | **1.0%** | **3.3%** | **0.1%** | **1.0%** | **3.3%** |
| Span leak rate | 63.4% | 0.0% | 0.2% | 0.6% | 0.0% | 0.2% | 0.6% |
| Any-PII char precision | 90.2 | 100.0 | 99.2 | 100.0 | 95.8 | 95.1 | 95.8 |
| Any-PII char recall | 40.3 | 100.0 | 99.9 | 99.7 | 100.0 | 99.9 | 99.7 |
| Any-PII char F1 | 55.8 | 100.0 | 99.6 | 99.8 | 97.9 | 97.5 | 97.7 |
| Exact-span F1 (all categories) | 51.6 | 99.5 | 97.0 | 77.8 | 97.4 | 95.0 | 85.5 |
| Median ms per document | 0.04 | 27.43 | 70.91 | 51.78 | 27.48 | 70.96 | 51.83 |

Span leak rate by category (lower is better):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON (3900 spans) | 100.0% | 0.1% | 0.4% | 2.0% | 0.1% | 0.4% | 2.0% |
| ADDRESS (700 spans) | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| EMAIL (1200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| PHONE (1400 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| URL (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| IP_ADDRESS (200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| DATE (600 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| ID (1200 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| SECRET (100 spans) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| AFFILIATION (3700 spans) | 100.0% | 0.0% | 0.3% | 0.0% | 0.0% | 0.3% | 0.0% |

Character-level F1 by category (category must match):

| Metric | rules | deberta-v3-small-open-int8-int4-block | modernbert-base-open-int8-int4-block | mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block |
|---|---:|---:|---:|---:|---:|---:|---:|
| PERSON | 0.0 | 99.3 | 99.5 | 99.2 | 99.3 | 99.5 | 99.2 |
| ADDRESS | 0.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| EMAIL | 100.0 | 100.0 | 98.8 | 100.0 | 100.0 | 98.8 | 100.0 |
| PHONE | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| URL | 51.6 | 100.0 | 100.0 | 100.0 | 51.6 | 51.6 | 51.6 |
| IP_ADDRESS | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| DATE | 100.0 | 100.0 | 95.8 | 100.0 | 100.0 | 95.8 | 100.0 |
| ID | 96.7 | 100.0 | 100.0 | 100.0 | 96.7 | 96.7 | 96.7 |
| SECRET | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| AFFILIATION | 0.0 | 99.4 | 99.6 | 100.0 | 99.4 | 99.6 | 100.0 |
