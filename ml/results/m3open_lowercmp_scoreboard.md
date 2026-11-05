## Deployed and retrained, int4

{'retrained': 12, 'deployed': 20, 'tie': 5}

| Row | Deployed | Retrained | Better |
|---|---:|---:|---|
| nz_test_full/plain: document leak | 0.7 | 0.3 | retrained |
| nz_test_full/plain: span leak | 0.1 | 0.1 | tie |
| nz_test_full/plain: char F1 | 97.1 | 96.3 | deployed |
| nz_test_full/plain: exact-span F1 | 92.2 | 91.0 | deployed |
| nz_test_full/nomacron: document leak | 0.9 | 0.3 | retrained |
| nz_test_full/nomacron: span leak | 0.2 | 0.1 | retrained |
| nz_test_full/nomacron: char F1 | 96.7 | 96.4 | deployed |
| nz_test_full/nomacron: exact-span F1 | 91.4 | 90.9 | deployed |
| nz_test_full/lower: document leak | 94.7 | 7.7 | retrained |
| nz_test_full/lower: span leak | 45.2 | 2.0 | retrained |
| nz_test_full/lower: char F1 | 80.5 | 95.6 | retrained |
| nz_test_full/lower: exact-span F1 | 59.2 | 78.8 | retrained |
| nz_test_names: document leak | 0.0 | 0.1 | deployed |
| nz_test_names: span leak | 0.0 | 0.0 | tie |
| nz_test_names: char F1 | 96.7 | 96.7 | tie |
| nz_test_names: exact-span F1 | 96.6 | 96.7 | retrained |
| open_en_test: document leak | 3.2 | 4.0 | deployed |
| open_en_test: span leak | 1.1 | 1.3 | deployed |
| open_en_test: char F1 | 99.1 | 99.0 | deployed |
| open_en_test: exact-span F1 | 95.4 | 94.4 | deployed |
| pii300k_en_val: document leak | 33.2 | 39.7 | deployed |
| pii300k_en_val: span leak | 11.8 | 14.0 | deployed |
| pii300k_en_val: char F1 | 93.8 | 92.9 | deployed |
| pii300k_en_val: exact-span F1 | 76.2 | 75.5 | deployed |
| nz_test_false_alarm: document leak | 0.0 | 0.3 | deployed |
| nz_test_false_alarm: span leak | 0.0 | 0.1 | deployed |
| nz_test_false_alarm: char F1 | 82.4 | 80.5 | deployed |
| nz_test_false_alarm: exact-span F1 | 59.4 | 56.2 | deployed |
| plain: size of the Māori − Pākehā gap | 0.3 | 0.2 | retrained |
| nomacron: size of the Māori − Pākehā gap | 0.3 | 0.2 | retrained |
| lower: size of the Māori − Pākehā gap | 26.8 | 5.9 | retrained |
| false alarm after review: booking_code | 99.5 | 99.5 | tie |
| false alarm after review: hui_date | 0.0 | 0.0 | tie |
| false alarm after review: invoice | 0.0 | 92.0 | deployed |
| false alarm after review: kin | 22.7 | 23.4 | deployed |
| false alarm after review: order_ref | 94.5 | 100.0 | deployed |
| false alarm after review: town | 17.0 | 0.0 | retrained |
