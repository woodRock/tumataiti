## Deployed and retrained, int4: false-alarm set

False alarms on text that is not PII (lower is better), and leaks of the PII beside it:

| Slot | n | rules+deployed | rules+deployed+review | rules+deployed+txn | rules+retrained | rules+retrained+review | rules+retrained+txn |
|---|---:|---:|---:|---:|---:|---:|---:|
| not PII: booking_code | 200 | 99.5% redacted | 99.5% redacted | 99.5% redacted | 99.5% redacted | 99.5% redacted | 99.5% redacted |
| not PII: hui_date | 300 | 0.0% redacted | 0.0% redacted | 0.0% redacted | 0.0% redacted | 0.0% redacted | 0.0% redacted |
| not PII: invoice | 100 | 0.0% redacted | 0.0% redacted | 0.0% redacted | 92.0% redacted | 92.0% redacted | 92.0% redacted |
| not PII: kin | 700 | 71.7% redacted | 22.7% redacted, 49.0% flagged | 22.7% redacted, 49.0% flagged | 71.6% redacted | 23.4% redacted, 48.1% flagged | 23.4% redacted, 48.1% flagged |
| not PII: order_ref | 200 | 94.5% redacted | 94.5% redacted | 50.0% redacted, 44.5% flagged | 100.0% redacted | 100.0% redacted | 50.0% redacted, 50.0% flagged |
| not PII: town | 100 | 17.0% redacted | 17.0% redacted | 17.0% redacted | 0.0% redacted | 0.0% redacted | 0.0% redacted |
| PII: address | 100 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: email | 100 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: full | 200 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: given | 300 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.7% leaked | 0.7% leaked | 0.7% leaked |
| PII: ird | 100 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: landline | 100 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: mobile | 100 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: nan_full | 100 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: nhi | 100 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: plain | 100 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: surname | 100 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
