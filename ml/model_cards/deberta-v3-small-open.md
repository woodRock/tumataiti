---
license: apache-2.0
language:
  - en
  - mi
base_model: microsoft/deberta-v3-small
pipeline_tag: token-classification
library_name: transformers
datasets:
  - nvidia/Nemotron-PII
  - gretelai/gretel-pii-masking-en-v1
tags:
  - pii
  - redaction
  - privacy
  - new-zealand
  - te-reo-maori
  - onnx
---

# Tūmataiti DeBERTa-v3-small (open data)

A small token classifier that finds personal information in English and New Zealand text, including te reo Māori, Pasifika and Asian New Zealand names. It is the name model in [Tūmataiti](https://github.com/woodRock/tumataiti), a local redaction tool that removes personal details before text is sent to a cloud AI model. It is built to run on the user's device: the int4 ONNX file is 152 MB and takes about 30 ms per document on a laptop CPU.

Tūmataiti pairs it with Rust rules for identifiers with check digits (IRD, NHI, cards). The model finds what rules cannot: names, addresses, iwi, hapū and marae affiliation, and dates of birth in context.

**Try it:** [woodrock.github.io/tumataiti](https://woodrock.github.io/tumataiti/) runs this model in the browser. Text never leaves the page.

## Labels

BIO tags for `PERSON`, `ADDRESS`, `EMAIL`, `PHONE`, `URL`, `IP_ADDRESS`, `DATE` (dates of birth or death only), `ID` (government, card and bank numbers), `SECRET` (passwords and keys) and `AFFILIATION` (iwi, hapū, marae).

## Files

| File | What it is |
|---|---|
| `model.safetensors`, `config.json`, `tokenizer.json` | fp32 checkpoint for 🤗 Transformers |
| `onnx/model_int4.onnx` | int8 embeddings and an int4 block-quantised encoder (32 weights per scale, fp32 activations) for ONNX Runtime. Inputs `input_ids`, `attention_mask`; output `logits` |

## Use

```python
from transformers import pipeline

ner = pipeline("token-classification", model="woodrock/tumataiti-deberta-v3-small-open",
               aggregation_strategy="simple")
ner("Kia ora, Hōhepa Ngata will collect the kai. Call him on 022 012 3456.")
```

Tūmataiti's own decoder ([`student/encode.py`](https://github.com/woodRock/tumataiti/blob/main/ml/src/tumataiti_ml/student/encode.py), and a Rust port for the browser) splits long text into 512-token windows with 128 tokens of overlap, keeps a token when P(not O) ≥ 0.5, widens spans to whole words, and drops spans that are only a field label such as "NHI". Results below use it.

## Training

Fine-tuned from [microsoft/deberta-v3-small](https://huggingface.co/microsoft/deberta-v3-small) (MIT) for 3 epochs (lr 5e-5, batch 16, seed 0), keeping the checkpoint after the first epoch, which had the best dev score, on 38,000 synthetic documents:

- **Tūmataiti NZ synthetic v2** (8,000 documents): generated from templates (hui notes, referrals, forms, interviews, text messages, chat logs, minutes and more) with names drawn 25% from each of Māori, Pākehā, Pasifika and Asian New Zealand lists. Names are randomly combined, so no generated person is meant to be real. Te reo words that are not names in context (tūī, kōwhai, "aroha mai") are included as negatives.
- **[nvidia/Nemotron-PII](https://huggingface.co/datasets/nvidia/Nemotron-PII)** (20,000 documents), © NVIDIA, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Labels were mapped onto the categories above; documents were not modified.
- **[gretelai/gretel-pii-masking-en-v1](https://huggingface.co/datasets/gretelai/gretel-pii-masking-en-v1)** (10,000 documents), Apache-2.0. Entity strings were located in the text by exact word-bounded matching; documents with an entity that could not be found were dropped.

No PII-Masking-300k data was used in training.

## Evaluation

Document leak rate is the share of documents where at least one piece of personal information is left unredacted, the number that matters for privacy. The model alone, without the rules:

| Test set | Documents | fp32 doc leak | int4 doc leak | int4 char precision | Teacher doc leak |
|---|---:|---:|---:|---:|---:|
| NZ synthetic, held-out templates and names | 1,750 | 0.3% | 0.7% | 98.9 | 47.4% |
| NZ synthetic, held-out names | 1,600 | 0.1% | 0.0% | 100.0 | 49.2% |
| Nemotron-PII + Gretel-en test splits | 2,000 | 3.3% | 3.3% | 99.0 | 40.0% |
| PII-Masking-300k, English validation | 7,946 | 32.7% | 34.2% | 95.0 | 8.2% |

The teacher is [openai/privacy-filter](https://huggingface.co/openai/privacy-filter) at its default operating point.

**Names by community.** The same held-out documents, with only the names swapped. Share of names left unredacted:

| Names | fp32 | int4 |
|---|---:|---:|
| Māori | 0.2% | 0.3% |
| Pākehā | 0.2% | 0.6% |
| Pasifika | 0.0% | 0.0% |
| Asian NZ | 0.0% | 0.0% |

## Limitations

- **Every test set is synthetic.** The NZ sets come from the same generator as the training data, with different templates and names held out, so they measure generalisation within that generator. A human-annotated NZ test set is planned; until then, treat these numbers as an upper bound on real-world performance.
- **PII-Masking-300k leakage is high** (34%). Much of it is labelling convention: that set labels any date in a JSON field as a birth date, bare building numbers and postcodes as addresses, and unusual strings as passwords. It also misses some unusual European surnames in markup. Expect weaker results on structured data (JSON, HTML) than on prose.
- **Kinship words used as names are tagged as people** ("Koro's IRD number", "Nan's"), and some unlabelled reference numbers shaped like IRD numbers are tagged as IDs.
- **No redaction tool is complete.** Use it to reduce exposure, with human review for sensitive material, not as a guarantee.

## Licence and attribution

Apache-2.0. This model was trained on [Nemotron-PII](https://huggingface.co/datasets/nvidia/Nemotron-PII) by NVIDIA (CC BY 4.0) and [gretel-pii-masking-en-v1](https://huggingface.co/datasets/gretelai/gretel-pii-masking-en-v1) by Gretel (Apache-2.0), and fine-tuned from [DeBERTa-v3-small](https://huggingface.co/microsoft/deberta-v3-small) by Microsoft (MIT).
