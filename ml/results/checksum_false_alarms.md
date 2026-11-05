## Rules with and without check digits

False alarms on text that is not PII (lower is better), and leaks of the PII beside it:

| Slot | n | rules | rules-format-only |
|---|---:|---:|---:|
| not PII: booking_code | 200 | 0.0% redacted | 100.0% redacted |
| not PII: hui_date | 300 | 0.0% redacted | 0.0% redacted |
| not PII: invoice | 100 | 0.0% redacted | 0.0% redacted |
| not PII: kin | 700 | 0.0% redacted | 0.0% redacted |
| not PII: order_ref | 200 | 0.0% redacted | 100.0% redacted |
| not PII: town | 100 | 0.0% redacted | 0.0% redacted |
| PII: address | 100 | 100.0% leaked | 100.0% leaked |
| PII: email | 100 | 0.0% leaked | 0.0% leaked |
| PII: full | 200 | 100.0% leaked | 100.0% leaked |
| PII: given | 300 | 100.0% leaked | 100.0% leaked |
| PII: ird | 100 | 0.0% leaked | 0.0% leaked |
| PII: landline | 100 | 0.0% leaked | 0.0% leaked |
| PII: mobile | 100 | 0.0% leaked | 0.0% leaked |
| PII: nan_full | 100 | 100.0% leaked | 100.0% leaked |
| PII: nhi | 100 | 0.0% leaked | 0.0% leaked |
| PII: plain | 100 | 100.0% leaked | 100.0% leaked |
| PII: surname | 100 | 100.0% leaked | 100.0% leaked |
