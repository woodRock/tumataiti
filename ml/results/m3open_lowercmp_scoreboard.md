## Deployed and retrained, int4

{'retrained': 15, 'deployed': 16, 'tie': 6}

| Row | Deployed | Retrained | Better |
|---|---:|---:|---|
| nz_test_full/plain: document leak | 2.1 | 2.6 | deployed |
| nz_test_full/plain: span leak | 0.4 | 0.5 | deployed |
| nz_test_full/plain: char F1 | 95.9 | 96.5 | retrained |
| nz_test_full/plain: exact-span F1 | 85.1 | 87.5 | retrained |
| nz_test_full/nomacron: document leak | 5.9 | 12.6 | deployed |
| nz_test_full/nomacron: span leak | 1.2 | 3.1 | deployed |
| nz_test_full/nomacron: char F1 | 95.1 | 95.3 | retrained |
| nz_test_full/nomacron: exact-span F1 | 79.5 | 82.2 | retrained |
| nz_test_full/lower: document leak | 96.5 | 18.5 | retrained |
| nz_test_full/lower: span leak | 61.2 | 4.3 | retrained |
| nz_test_full/lower: char F1 | 66.0 | 95.0 | retrained |
| nz_test_full/lower: exact-span F1 | 45.4 | 78.8 | retrained |
| nz_test_names: document leak | 0.1 | 0.4 | deployed |
| nz_test_names: span leak | 0.0 | 0.1 | deployed |
| nz_test_names: char F1 | 97.9 | 97.8 | deployed |
| nz_test_names: exact-span F1 | 97.4 | 97.5 | retrained |
| open_en_test: document leak | 3.4 | 3.1 | retrained |
| open_en_test: span leak | 1.2 | 1.1 | retrained |
| open_en_test: char F1 | 99.1 | 99.1 | tie |
| open_en_test: exact-span F1 | 95.7 | 94.4 | deployed |
| pii300k_en_val: document leak | 32.2 | 33.1 | deployed |
| pii300k_en_val: span leak | 11.3 | 11.1 | retrained |
| pii300k_en_val: char F1 | 93.9 | 93.9 | tie |
| pii300k_en_val: exact-span F1 | 77.5 | 75.3 | deployed |
| nz_test_false_alarm: document leak | 0.0 | 0.0 | tie |
| nz_test_false_alarm: span leak | 0.0 | 0.0 | tie |
| nz_test_false_alarm: char F1 | 82.4 | 81.8 | deployed |
| nz_test_false_alarm: exact-span F1 | 59.4 | 58.1 | deployed |
| plain: size of the Māori − Pākehā gap | 0.1 | 0.9 | deployed |
| nomacron: size of the Māori − Pākehā gap | 0.2 | 0.3 | deployed |
| lower: size of the Māori − Pākehā gap | 31.8 | 8.9 | retrained |
| false alarm after review: booking_code | 99.5 | 99.5 | tie |
| false alarm after review: hui_date | 0.0 | 0.0 | tie |
| false alarm after review: invoice | 0.0 | 79.0 | deployed |
| false alarm after review: kin | 22.1 | 24.6 | deployed |
| false alarm after review: order_ref | 97.5 | 92.0 | retrained |
| false alarm after review: town | 5.0 | 1.0 | retrained |
