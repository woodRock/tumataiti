## nz_test_false_alarm

False alarms on text that is not PII (lower is better), and leaks of the PII beside it:

| Slot | n | rules+deberta-v3-small-open+review | rules+deberta-v3-small-open+review+txn |
|---|---:|---:|---:|
| not PII: booking_code | 200 | 99.5% redacted | 99.5% redacted |
| not PII: hui_date | 300 | 0.0% redacted | 0.0% redacted |
| not PII: invoice | 100 | 0.0% redacted | 0.0% redacted |
| not PII: kin | 700 | 23.6% redacted, 58.4% flagged | 23.6% redacted, 58.4% flagged |
| not PII: order_ref | 200 | 99.0% redacted | 50.0% redacted, 49.0% flagged |
| not PII: town | 100 | 14.0% redacted | 14.0% redacted |
| PII: address | 100 | 0.0% leaked | 0.0% leaked |
| PII: email | 100 | 0.0% leaked | 0.0% leaked |
| PII: full | 200 | 0.0% leaked | 0.0% leaked |
| PII: given | 300 | 0.0% leaked | 0.0% leaked |
| PII: ird | 100 | 0.0% leaked | 0.0% leaked |
| PII: landline | 100 | 0.0% leaked | 0.0% leaked |
| PII: mobile | 100 | 0.0% leaked | 0.0% leaked |
| PII: nan_full | 100 | 0.0% leaked | 0.0% leaked |
| PII: nhi | 100 | 0.0% leaked | 0.0% leaked |
| PII: plain | 100 | 0.0% leaked | 0.0% leaked |
| PII: surname | 100 | 0.0% leaked | 0.0% leaked |
