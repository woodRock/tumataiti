## False-alarm set (600 documents)

False alarms on text that is not PII (lower is better), and leaks of the PII beside it:

| Slot | n | rules | deberta-v3-small-open-int8-int4-block | deberta-v3-small-open-int8-int4-block+review | rules+deberta-v3-small-open-int8-int4-block | rules+deberta-v3-small-open-int8-int4-block+review |
|---|---:|---:|---:|---:|---:|---:|
| not PII: booking_code | 200 | 0.0% redacted | 99.5% redacted | 99.5% redacted | 99.5% redacted | 99.5% redacted |
| not PII: hui_date | 300 | 0.0% redacted | 0.0% redacted | 0.0% redacted | 0.0% redacted | 0.0% redacted |
| not PII: invoice | 100 | 0.0% redacted | 0.0% redacted | 0.0% redacted | 0.0% redacted | 0.0% redacted |
| not PII: kin | 700 | 0.0% redacted | 75.6% redacted | 22.1% redacted, 53.4% flagged | 75.6% redacted | 22.1% redacted, 53.4% flagged |
| not PII: order_ref | 200 | 0.0% redacted | 97.5% redacted | 97.5% redacted | 97.5% redacted | 97.5% redacted |
| not PII: town | 100 | 0.0% redacted | 5.0% redacted | 5.0% redacted | 5.0% redacted | 5.0% redacted |
| PII: address | 100 | 100.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: email | 100 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: full | 200 | 100.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: given | 300 | 100.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: ird | 100 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: landline | 100 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: mobile | 100 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: nan_full | 100 | 100.0% leaked | 0.0% leaked | 6.0% leaked | 0.0% leaked | 6.0% leaked |
| PII: nhi | 100 | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: plain | 100 | 100.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
| PII: surname | 100 | 100.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked | 0.0% leaked |
