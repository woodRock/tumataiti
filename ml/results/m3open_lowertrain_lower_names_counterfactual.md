Name leak rate by community, counterfactual audit (lower is better):

| Names (same documents, only names swapped) | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Māori | 90.1% | 78.2% | 46.3% | 8.9% | 9.9% | 2.5% | 11.0% |
| Pākehā | 58.2% | 70.6% | 4.9% | 1.4% | 1.5% | 0.0% | 2.2% |
| Pasifika | 63.7% | 65.2% | 17.0% | 0.0% | 1.4% | 0.4% | 0.0% |
| Asian NZ | 75.3% | 74.8% | 10.1% | 1.1% | 3.0% | 0.0% | 2.4% |
| **Māori − Pākehā gap (points)** | **+31.8** | **+7.6** | **+41.4** | **+7.5** | **+8.4** | **+2.5** | **+8.9** |
