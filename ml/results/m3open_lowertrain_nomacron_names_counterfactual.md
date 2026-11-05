Name leak rate by community, counterfactual audit (lower is better):

| Names (same documents, only names swapped) | rules+deberta-v3-small-open | rules+modernbert-base-open | rules+mdeberta-v3-base-open | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Māori | 0.4% | 0.3% | 0.4% | 0.1% | 2.4% | 0.0% | 0.2% |
| Pākehā | 0.7% | 5.1% | 1.0% | 0.0% | 1.3% | 0.0% | 0.0% |
| Pasifika | 0.0% | 0.0% | 0.3% | 0.0% | 1.0% | 0.0% | 0.0% |
| Asian NZ | 0.0% | 2.4% | 0.0% | 0.0% | 0.9% | 0.0% | 0.0% |
| **Māori − Pākehā gap (points)** | **-0.3** | **-4.8** | **-0.6** | **+0.1** | **+1.2** | **+0.0** | **+0.2** |
