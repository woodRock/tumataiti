Name leak rate by community, counterfactual audit (lower is better):

| Names (same documents, only names swapped) | openai-privacy-filter | deberta-v3-small | deberta-v3-small-int8 | modernbert-base | mdeberta-v3-base | rules+openai-privacy-filter | rules+deberta-v3-small | rules+deberta-v3-small-int8 | rules+modernbert-base | rules+mdeberta-v3-base |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Māori | 52.4% | 11.7% | 14.1% | 17.9% | 0.2% | 52.4% | 11.7% | 14.1% | 17.9% | 0.2% |
| Pākehā | 14.3% | 13.3% | 28.5% | 24.6% | 20.8% | 14.3% | 13.3% | 28.5% | 24.6% | 20.8% |
| Pasifika | 37.4% | 14.3% | 19.7% | 12.2% | 3.2% | 37.4% | 14.3% | 19.7% | 12.2% | 3.2% |
| Asian NZ | 14.7% | 6.4% | 13.4% | 18.1% | 7.0% | 14.7% | 6.4% | 13.4% | 18.1% | 7.0% |
| **Māori − Pākehā gap (points)** | **+38.1** | **-1.5** | **-14.4** | **-6.8** | **-20.6** | **+38.1** | **-1.5** | **-14.4** | **-6.8** | **-20.6** |
