Name leak rate by community, counterfactual audit (lower is better):

| Names (same documents, only names swapped) | rules+deberta-v3-small-open-int8-int4-block | rules+modernbert-base-open-int8-int4-block | rules+mdeberta-v3-base-open-int8-int4-block | rules+deberta-v3-small-open-lower | rules+modernbert-base-open-lower | rules+mdeberta-v3-base-open-lower | rules+deberta-v3-small-open-lower-int4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Māori | 0.3% | 0.7% | 0.5% | 0.1% | 9.1% | 0.0% | 0.3% |
| Pākehā | 0.6% | 5.0% | 0.9% | 0.0% | 2.4% | 0.0% | 0.1% |
| Pasifika | 0.0% | 0.0% | 0.5% | 0.0% | 1.5% | 0.0% | 0.0% |
| Asian NZ | 0.0% | 2.2% | 0.0% | 0.0% | 1.4% | 0.0% | 0.0% |
| **Māori − Pākehā gap (points)** | **-0.3** | **-4.3** | **-0.5** | **+0.1** | **+6.8** | **+0.0** | **+0.2** |
