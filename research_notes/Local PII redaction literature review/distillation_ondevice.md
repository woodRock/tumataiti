# Compressing Transformer NER / Token-Classification Models and Running Them On-Device or In-Browser

Scope note for the report writer. Works were checked in two ways, and each entry says which:
- **[V]**: bibliographic details and claims were checked this session against arXiv, the ACL Anthology, ACM, AAAI or official docs (URLs given).
- **[C]**: canonical, widely cited works whose arXiv IDs and venues are standard and well established. They were **not re-fetched this session**. They are listed so the review is complete, but the writer should spot-check the DOI/arXiv link before final citation.
- "Preprint" means it is only on arXiv, with no peer-reviewed version found.

Project pipeline these notes map onto: teacher `openai/privacy-filter` (MoE, ~1.5B total / ~50M active) labels data → distil into a ~100–150M student encoder (DeBERTa-v3-small / ModernBERT-base) → ONNX → int8 (~70–150 MB) → Transformers.js / ONNX Runtime Web in the browser, alongside Rust→Wasm rules.

---

## Q1. Knowledge distillation for sequence labelling / NER (incl. LLM→small-model distillation, soft vs hard pseudo-labels, mismatched label sets)

### Takeaway
There are two well-established lines of work. (a) Task-agnostic compression of BERT (DistilBERT, TinyBERT, MiniLM, MobileBERT) gives general small backbones. (b) Task-specific teacher→student distillation for NER (XtremeDistil, Structural KD) keeps about 95% of teacher F1 at 35x compression. Since 2023 a third line, "targeted distillation" from LLMs (UniversalNER, GLiNER, NuNER), shows that **hard pseudo-labels produced by a large generative teacher on unlabelled text** can train students that match or beat the teacher on NER. That is the regime Tūmataiti's teacher-labelling pipeline sits in.

### Cited Findings

**Foundations**
- [C] Hinton, G., Vinyals, O., Dean, J. (2015). *Distilling the Knowledge in a Neural Network.* NIPS 2014 Deep Learning Workshop; arXiv:1503.02531 (preprint). Introduces temperature-softened soft-target KD. This is the basis for soft-label versus hard-label distillation — [arXiv](https://arxiv.org/abs/1503.02531)
- [C] Kim, Y., Rush, A. M. (2016). *Sequence-Level Knowledge Distillation.* EMNLP 2016; arXiv:1606.07947. Shows that training on the teacher's argmax (beam) outputs, i.e. hard sequence-level pseudo-labels, works well for structured outputs. This is the theoretical precedent for hard-label teacher labelling — [arXiv](https://arxiv.org/abs/1606.07947)

**Task-agnostic BERT compression (student backbones)**
- [C] Sanh, V., Debut, L., Chaumond, J., Wolf, T. (2019). *DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter.* NeurIPS 2019 EMC² Workshop; arXiv:1910.01108. A 6-layer student trained with soft-target + MLM + cosine losses; 40% smaller, 60% faster, keeps ~97% of BERT's GLUE performance — [arXiv](https://arxiv.org/abs/1910.01108)
- [C] Jiao, X. et al. (2020). *TinyBERT: Distilling BERT for Natural Language Understanding.* Findings of EMNLP 2020; arXiv:1909.10351. Two-stage (general + task-specific) layer-wise distillation of embeddings, attention and hidden states, plus data augmentation; 4-layer TinyBERT is 7.5x smaller and 9.4x faster — [arXiv](https://arxiv.org/abs/1909.10351)
- [C] Wang, W. et al. (2020). *MiniLM: Deep Self-Attention Distillation for Task-Agnostic Compression of Pre-Trained Transformers.* NeurIPS 2020; arXiv:2002.10957. Distils the last-layer self-attention distributions and value relations, so the student's depth and width are unconstrained — [arXiv](https://arxiv.org/abs/2002.10957)
- [C] Sun, Z. et al. (2020). *MobileBERT: a Compact Task-Agnostic BERT for Resource-Limited Devices.* ACL 2020; arXiv:2004.02984. Bottleneck architecture designed for phones; 4.3x smaller and 5.5x faster than BERT-base; 62 ms latency on a Pixel 4 — [arXiv](https://arxiv.org/abs/2004.02984)

**Task-specific KD for NER / sequence labelling**
- [V] Mukherjee, S., Awadallah, A. H. (2020). *XtremeDistil: Multi-stage Distillation for Massive Multilingual Models.* ACL 2020, pp. 2221–2234. DOI 10.18653/v1/2020.acl-main.202; arXiv:2004.05686. Distils an mBERT NER teacher into small students with stage-wise optimisation over teacher internal representations; up to **35x parameter compression and 51x batch-inference speed-up while keeping ~95% of teacher F1 across 41 languages**. This is the closest prior work to the project's distil-for-NER step — [ACL Anthology](https://aclanthology.org/2020.acl-main.202); [arXiv](https://arxiv.org/abs/2004.05686v2)
- [V] Wang, X., Jiang, Y., Yan, Z., Jia, Z., Bach, N., Wang, T., Huang, Z., Huang, F., Tu, K. (2021). *Structural Knowledge Distillation: Tractably Distilling Information for Structured Predictor.* ACL-IJCNLP 2021, pp. 550–564; arXiv:2010.05010. Derives a factorised KD objective for exponential output spaces, e.g. a CRF teacher, and covers cases where **teacher and student factorisations are incompatible** (e.g. CRF teacher → softmax student). Relevant when distilling a teacher with a different output structure or decoder. Code: Alibaba-NLP/StructuralKD — [ACL Anthology](https://aclanthology.org/2021.acl-long.46); [arXiv](https://arxiv.org/abs/2010.05010v4)
- [C] Wang, X. et al. (2020). *Structure-Level Knowledge Distillation for Multilingual Sequence Labeling.* ACL 2020; arXiv:2004.03846. Distils several monolingual CRF teachers into one multilingual student using structure-level (top-K / posterior) distillation — [arXiv](https://arxiv.org/abs/2004.03846)
- [C] Wu, Q. et al. (2020). *Single-/Multi-Source Cross-Lingual NER via Teacher-Student Learning on Unlabeled Data in Target Language.* ACL 2020; arXiv:2004.12440. Uses teacher soft labels on unlabelled target-language text and finds **soft-label distillation beats hard pseudo-labels** for cross-lingual NER — [arXiv](https://arxiv.org/abs/2004.12440)
- [C] Liang, C. et al. (2020). *BOND: BERT-Assisted Open-Domain Named Entity Recognition with Distant Supervision.* KDD 2020; arXiv:2006.15509. A self-training teacher–student scheme with soft/high-confidence pseudo-labels for noisy, distantly supervised NER. Relevant for handling a noisy teacher — [arXiv](https://arxiv.org/abs/2006.15509)

**Distilling LLMs into small NER models ("targeted distillation")**
- [V] Zhou, W., Zhang, S., Gu, Y., Chen, M., Poon, H. (2024). *UniversalNER: Targeted Distillation from Large Language Models for Open Named Entity Recognition.* ICLR 2024; arXiv:2308.03279. "Mission-focused instruction tuning": ChatGPT annotates unlabelled text, then a 7B/13B LLaMA student is trained. The paper builds a 43-dataset, 9-domain NER benchmark (incl. biomedicine, law, finance, social media). Students **beat ChatGPT by 7–9 absolute F1 on average** and beat Alpaca/Vicuna by >30 F1, with no direct human supervision. This shows a student can surpass its teacher on the distilled task — [arXiv](https://arxiv.org/abs/2308.03279)
- [V] Zaratiana, U., Tomeh, N., Holat, P., Charnois, T. (2024). *GLiNER: Generalist Model for Named Entity Recognition using Bidirectional Transformer.* NAACL 2024, pp. 5364–5376; arXiv:2311.08526. A span-matching bidirectional encoder (DeBERTa-v3 backbone) trained on **Pile-NER**, the ChatGPT-annotated UniversalNER data (~45k passages, ~240k spans, ~13k entity types, per a secondary source). Beats ChatGPT and fine-tuned LLMs zero-shot. Small/medium variants run on CPU. This is the best evidence that an **encoder-sized student (tens to a few hundred M params) can absorb LLM-teacher NER knowledge** — [ACL Anthology](https://aclanthology.org/2024.naacl-long.300); [arXiv](https://arxiv.org/abs/2311.08526v1); Pile-NER stats from [Zilliz blog](https://zilliz.com/blog/gliner-generalist-model-for-named-entity-recognition-using-bidirectional-transformer) (secondary)
- [V] Bogdanov, S. et al. (2024). *NuNER: Entity Recognition Encoder Pre-training via LLM-Annotated Data.* EMNLP 2024, pp. 11829–11841; arXiv:2402.15343. A 125M encoder (RoBERTa-base per a secondary source) pre-trained on 4.38M GPT-3.5 annotations covering 200k entity types. Beats similar-size encoders in few-shot NER and competes with the 7–13B UniversalNER. The paper finds **dataset size and entity-type diversity** are the key drivers. MIT licence — [arXiv](https://arxiv.org/pdf/2402.15343); [ACL Anthology preview](https://preview.aclanthology.org/setup/2024.emnlp-main.660)
- [V] Third-party (vendor) benchmarking reports that zero-shot GLiNER on CoNLL-03 scores only ~0.55–0.61 F1, and that a dedicated fine-tuned model wins on a fixed label set — [Superlinked](https://superlinked.com/glossary/what-is-gliner) (vendor blog; low confidence)

### Inferences
- Tūmataiti's design (a large teacher labels in-domain text, then a fixed-label encoder student) matches the UniversalNER/NuNER/GLiNER recipe, but with a fixed PII label set. Given the Superlinked observation, a fixed-label fine-tuned token classifier should beat a zero-shot generalist on the target taxonomy.
- Soft vs hard: the literature is mixed. Wu et al. 2020 favour soft labels for cross-lingual NER. Kim & Rush 2016 and the LLM-distillation works succeed with hard labels, often because the LLM teacher exposes no usable token distribution. `openai/privacy-filter` is itself a token classifier, so it exposes per-token posteriors, which makes soft-label (logit/KL) distillation possible. Precedent suggests trying soft + hard (Hinton-style mixed loss).
- Mismatched label sets: Structural KD (Wang et al. 2021) is the formal tool when the teacher and student output structures differ. When the label *inventories* differ, the practical approach is to map teacher labels into the student taxonomy (merge/split) before computing a KL loss over the mapped distribution. No paper found here addresses this exactly for PII.

### Gaps
- No peer-reviewed paper was found on distilling a **PII-specific** token-classification teacher into a browser-sized student. This appears to be a genuine gap.
- I did not verify the paper "Distilling LLMs for NER with different label taxonomies". No dedicated study of label-set-mismatch KD for NER was found in this session.
- GLiNER's exact parameter counts per variant were not verified from the paper itself: 50M/90M/205M figures come from secondary sources.

---

## Q2. Encoder backbones for token classification (BERT, RoBERTa, DeBERTa-v3, ModernBERT, XLM-R, mDeBERTa)

### Takeaway
DeBERTa-v3 remains the strongest backbone at a given size for NLU/token-level accuracy and sample efficiency under controlled data. ModernBERT (Dec 2024) is substantially faster (unpadding, FlashAttention, RoPE, 8k context), but a controlled 2025 study attributes much of its benchmark advantage to training data rather than architecture.

### Cited Findings
- [C] Devlin, J., Chang, M.-W., Lee, K., Toutanova, K. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding.* NAACL 2019; arXiv:1810.04805. Introduces the token-classification fine-tuning head (softmax per WordPiece, first sub-token); CoNLL-03 F1 92.4 (base) / 92.8 (large) — [arXiv](https://arxiv.org/abs/1810.04805)
- [C] Liu, Y. et al. (2019). *RoBERTa: A Robustly Optimized BERT Pretraining Approach.* arXiv:1907.11692 (preprint) — [arXiv](https://arxiv.org/abs/1907.11692)
- [C] He, P., Gao, J., Chen, W. (2023). *DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing.* ICLR 2023; arXiv:2111.09543. Also releases mDeBERTa-v3-base (multilingual). DeBERTa-v3-small has 44M backbone params + 98M embedding params (128k vocab) — [arXiv](https://arxiv.org/abs/2111.09543)
- [C] Conneau, A. et al. (2020). *Unsupervised Cross-lingual Representation Learning at Scale (XLM-R).* ACL 2020; arXiv:1911.02116. 100-language RoBERTa; a strong multilingual NER baseline — [arXiv](https://arxiv.org/abs/1911.02116)
- [V] Warner, B. et al. (2024). *Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder for Fast, Memory Efficient, and Long Context Finetuning and Inference* (ModernBERT). arXiv:2412.13663, submitted 18 Dec 2024 (preprint at time of checking; ACL 2025 publication not confirmed in this session). 14 authors. Trained on 2T tokens of English + code, native 8,192-token context — [arXiv](https://arxiv.org/abs/2412.13663v1)
- [V] Antoun, W., Sagot, B., Seddah, D. (2025). *ModernBERT or DeBERTaV3? Examining Architecture and Data Influence on Transformer Encoder Models Performance.* IJCNLP-AACL 2025; arXiv:2504.08716. Pre-trains ModernBERT on the same French corpus as CamemBERTaV2 (DeBERTaV3). **With data controlled, DeBERTaV3 wins on overall benchmark performance and sample efficiency** (retrieval excepted). **ModernBERT has a clear advantage in training and inference speed.** The study argues that undisclosed training data makes ModernBERT's original gains hard to attribute — [arXiv](https://arxiv.org/html/2504.08716v2)
- [V] A Turkish ModernBERT study (TabiBERT, arXiv:2512.23065, preprint) reports the same pattern: ModernBERT is faster, DeBERTaV3 is more sample-efficient — [arXiv](https://arxiv.org/pdf/2512.23065)

### Inferences
- For a browser student, the trade-off is accuracy-per-param (DeBERTa-v3-small) versus latency and long context (ModernBERT-base, 149M). DeBERTa-v3-small's 128k-vocab embedding matrix dominates its size, and int8 shrinks it well. Its disentangled-attention ops are heavier to export and run in ORT Web than ModernBERT's.
- For NZ text that includes te reo Māori, multilingual backbones (XLM-R, mDeBERTa-v3) may matter. ModernBERT is English+code only.

### Gaps
- The ModernBERT paper's own token-classification/NER numbers (if any) were not retrieved. A community ModernBERT-large CoNLL card reports token accuracy, not entity F1, so it is not comparable.
- I did not verify any study measuring te reo Māori NER or tokenisation quality on these backbones.
- Multilingual "modern" encoders (e.g. mmBERT, 2025) were not verified this session.

---

## Q3. Post-training quantisation and pruning of BERT-style models, with NER accuracy loss

### Takeaway
8-bit quantisation of BERT is close to lossless on NER. Q-BERT reports CoNLL-03 F1 of 94.79 at w8/a8 against a 95.00 FP32 baseline (−0.21). Hessian-guided mixed precision holds near-baseline F1 down to 3-bit weights, while naive quantisation collapses at ≤4 bits. Pruning combined with distillation and int8 can give ~40x encoder compression at <1% loss (shown on QA).

### Cited Findings
- [C] Zafrir, O., Boudoukh, G., Izsak, P., Wasserblat, M. (2019). *Q8BERT: Quantized 8Bit BERT.* NeurIPS 2019 EMC² Workshop; arXiv:1910.06188. Quantisation-aware training of BERT to int8 (4x smaller); <1% accuracy loss on GLUE/SQuAD — [arXiv](https://arxiv.org/abs/1910.06188)
- [V] Shen, S. et al. (2020). *Q-BERT: Hessian Based Ultra Low Precision Quantization of BERT.* AAAI 2020; DOI 10.1609/aaai.v34i05.6409; arXiv:1909.05840. Evaluates on SST-2, MNLI, **CoNLL-03 NER** and SQuAD. **CoNLL-03 F1:** FP32 baseline 95.00; Q-BERT 8-bit 94.79; 4-bit weights 94.90 (DirectQ 89.86); 3-bit 94.78 (DirectQ 84.92); 2-bit 91.06 (DirectQ 54.50). Overall result: 13x weight compression with ≤2.3% loss — [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/6409); table read from [ar5iv](https://ar5iv.labs.arxiv.org/html/1909.05840)
- [C] Kim, S., Gholami, A., Yao, Z., Mahoney, M. W., Keutzer, K. (2021). *I-BERT: Integer-only BERT Quantization.* ICML 2021; arXiv:2101.01321. Integer-only approximations of GELU, Softmax and LayerNorm; int8 RoBERTa matches or slightly beats FP32 on GLUE, with 2.4–4.0x speed-up on T4 — [arXiv](https://arxiv.org/abs/2101.01321)
- [C] Bondarenko, Y., Nagel, M., Blankevoort, T. (2021). *Understanding and Overcoming the Challenges of Efficient Transformer Quantization.* EMNLP 2021; arXiv:2109.12948. Shows that **activation outliers** in the residual/FFN outputs make W8A8 post-training quantisation of BERT lossy, and proposes mixed-precision and per-embedding-group PTQ. This explains why dynamic (per-batch activation) int8 is safer than static int8 — [arXiv](https://arxiv.org/abs/2109.12948)
- [C] Dettmers, T. et al. (2022). *LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale.* NeurIPS 2022; arXiv:2208.07339. Characterises the outlier features behind int8 degradation — [arXiv](https://arxiv.org/abs/2208.07339)
- [C] Yao, Z. et al. (2022). *ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers.* NeurIPS 2022; arXiv:2206.01861. Fine-grained (group-wise / token-wise) PTQ plus layer-by-layer KD for BERT/GPT — [arXiv](https://arxiv.org/abs/2206.01861)
- [V] Zafrir, O., Larey, A., Boudoukh, G., Shen, H., Wasserblat, M. (2021). *Prune Once for All: Sparse Pre-Trained Language Models.* NeurIPS 2021 ENLSP Workshop; arXiv:2111.05754. Pruning + distillation during pre-training produces sparse BERT/DistilBERT whose sparsity survives fine-tuning. Sparse BERT-Large + int8 reaches **40x encoder compression with <1% loss** on SQuAD v1.1. Intel publishes 90%-sparse DistilBERT checkpoints — [arXiv](https://arxiv.org/abs/2111.05754v1); [NeurIPS virtual](https://neurips.cc/virtual/2021/34289)
- [C] Sanh, V., Wolf, T., Rush, A. M. (2020). *Movement Pruning: Adaptive Sparsity by Fine-Tuning.* NeurIPS 2020; arXiv:2005.07683 — [arXiv](https://arxiv.org/abs/2005.07683)
- [C] Michel, P., Levy, O., Neubig, G. (2019). *Are Sixteen Heads Really Better than One?* NeurIPS 2019; arXiv:1905.10650. Many attention heads can be pruned at test time with little loss — [arXiv](https://arxiv.org/abs/1905.10650)
- [C] Kurtic, E. et al. (2022). *The Optimal BERT Surgeon: Scalable and Accurate Second-Order Pruning for Large Language Models.* EMNLP 2022; arXiv:2203.07259 — [arXiv](https://arxiv.org/abs/2203.07259)
- [V] Transformers.js defaults to `q8` (8-bit) weights on the WASM backend and also offers `fp16` and `q4` dtypes — [Transformers.js docs](https://huggingface.co/docs/transformers.js/index)

### Inferences
- Q-BERT's CoNLL-03 result (−0.21 F1 at 8-bit) is the most direct published evidence that int8 is acceptable for NER. It comes from a BERT-base teacher with QAT-like Hessian-guided treatment, though, not ONNX dynamic quantisation. The project should measure the int8 F1 delta on its own PII test set and watch rare classes (IDs, IRD numbers) in particular.
- The outlier literature (Bondarenko 2021; Dettmers 2022) suggests that if static int8 hurts, ORT dynamic quantisation, or keeping specific layers (embeddings, final classifier, LayerNorm) in fp32, is the standard fix.

### Gaps
- No peer-reviewed paper was found that measures **ONNX Runtime dynamic int8** specifically on NER F1 for DeBERTa-v3 or ModernBERT. DeBERTa-v3 int8 degradation is known anecdotally (community reports) but was not verified here.
- Q8BERT/I-BERT NER results (if any) were not checked. Both mainly report GLUE/SQuAD.

---

## Q4. In-browser / on-device inference (Wasm, WebGPU, ORT Web, Transformers.js, TF.js); privacy arguments; Wasm for privacy/security tools

### Takeaway
The best academic evaluation (Wang et al., TOSEM 2024) finds in-browser inference averages **16.9x slower than native on CPU and 4.9x on GPU (PC)**, with large memory overheads and a 67.2% slowdown in GUI rendering. WebGPU kernel-compilation work (nn-JIT.web, MobiSys 2024) recovers up to 8.2x. For a ~100M-param int8 encoder on short inputs, Wasm CPU is the pragmatic default. The official ORT Web docs explicitly make the privacy argument (input data stays on the client) and the offline argument.

### Cited Findings
- [V] Wang, Q., Jiang, S., Chen, Z., Cao, X., Li, Y., Li, A., Ma, Y., Cao, T., Liu, X. (2024). *Anatomizing Deep Learning Inference in Web Browsers.* ACM Transactions on Software Engineering and Methodology (TOSEM); DOI 10.1145/3688843; arXiv:2402.05981. Tests 9 models with TF.js and ONNX Runtime Web (Wasm CPU, WebGL GPU) on 50 PCs and 20 mobile devices. Findings: CPU 16.9x / GPU 4.9x slower than native on PC; mobile 15.8x / 7.8x; memory sometimes **>334.6x model size**; GUI rendering time +67.2%; GPU warm-up far exceeds per-inference latency. WebGPU was not tested. The published version's GPU figure reportedly differs (30.6x per a search summary), so cite the version used — [arXiv](https://arxiv.org/abs/2402.05981); [ACM](https://dl.acm.org/doi/10.1145/3688843)
- [V] Jia, F., Jiang, S., Cao, T., Cui, W., Xia, T., Cao, X., Li, Y., Zhang, D., Ren, J., Liu, Y., Qiu, L., Yang, M. (2024). *Empowering In-Browser Deep Learning Inference on Edge Devices with Just-in-Time Kernel Optimizations* (nn-JIT.web). MobiSys 2024; arXiv:2309.08978. JIT WebGPU kernel tuning cuts compile cost about 100x and prunes the search space to dozens of options. **Up to 8.2x faster within 30 s** versus baselines on BART, T5 and Llama 2, on laptops and phones — [arXiv](https://arxiv.org/abs/2309.08978)
- [C] Ma, Y., Xiang, D., Zheng, S., Tian, D., Liu, X. (2019). *Moving Deep Learning into Web Browsers: How Far Can We Go?* The Web Conference (WWW) 2019; arXiv:1901.09388. The first empirical study of browser DL frameworks (TF.js, ONNX.js, etc.): browser inference is feasible but several-fold slower than native — [arXiv](https://arxiv.org/abs/1901.09388)
- [C] Smilkov, D. et al. (2019). *TensorFlow.js: Machine Learning for the Web and Beyond.* MLSys (SysML) 2019; arXiv:1901.05350. The design paper; explicitly motivates client-side ML for privacy (data never leaves the device) and low latency — [arXiv](https://arxiv.org/abs/1901.05350)
- [C] Haas, A. et al. (2017). *Bringing the Web up to Speed with WebAssembly.* PLDI 2017; DOI 10.1145/3062341.3062363. The Wasm design paper: a sandboxed, memory-safe, near-native portable bytecode — [ACM](https://dl.acm.org/doi/10.1145/3062341.3062363)
- [C] Jangda, A., Powers, B., Berger, E. D., Guha, A. (2019). *Not So Fast: Analyzing the Performance of WebAssembly vs. Native Code.* USENIX ATC 2019. Wasm runs on average 45% (Firefox) to 55% (Chrome) slower than native on SPEC CPU — [USENIX](https://www.usenix.org/conference/atc19/presentation/jangda)
- [C] Ruan, C. F. et al. (2024). *WebLLM: A High-Performance In-Browser LLM Inference Engine.* arXiv:2412.15803 (preprint). WebGPU + Wasm engine keeping up to ~80% of native decoding speed — [arXiv](https://arxiv.org/abs/2412.15803)
- [V] ONNX Runtime Web official docs: execution providers `wasm`/`cpu` (supports **all** ONNX operators), `webgl`, `webgpu` and `webnn`, which support only a subset. The docs state that in-browser inference keeps input data on the client (privacy), works offline, and cuts serving cost. They recommend ORT-format conversion and custom operator-reduced builds to shrink binary size and peak memory — [ORT Web docs](https://onnxruntime.ai/docs/tutorials/web/)
- [V] Transformers.js official docs: run 🤗 Transformers models in the browser "without a server" via ONNX Runtime. WASM (CPU) is the default backend; `device: 'webgpu'` is experimental in many browsers. Dtypes are `fp32`, `fp16`, `q8` (WASM default) and `q4`. Models are converted with 🤗 Optimum. A `token-classification`/`ner` pipeline is supported — [Transformers.js docs](https://huggingface.co/docs/transformers.js/index)
- [V] Practitioner (non-peer-reviewed) benchmarks report that for small embedding models with <128-token inputs, the Wasm backend matches or beats WebGPU — [SitePoint](https://www.sitepoint.com/webgpu-vs-webasm-transformers-js/) (anecdotal)

### Inferences
- An int8 encoder on Wasm is the robust path: full operator coverage (DeBERTa's disentangled attention may hit unsupported ops on WebGPU) and no GPU warm-up cost (Wang et al. 2024). WebGPU is an optional accelerator for long documents.
- Memory overhead of >300x model size (Wang et al.) is a warning for a 70–150 MB model on mobile. Peak memory should be measured, not just file size.
- The privacy argument is well established in system/docs literature (TF.js paper, ORT Web docs). Wasm's sandbox (Haas et al.) supports the claim that the Rust rules engine can't exfiltrate data by itself. Network egress is still governed by the page's JS/CSP, which the project should state explicitly.

### Gaps
- I found no academic evaluation **specifically of Transformers.js** latency or memory, and no peer-reviewed benchmark of WebNN.
- I found no peer-reviewed paper on **client-side PII redaction in the browser** or on Wasm-compiled privacy rule engines. This looks like a genuine gap the project could claim.
- The exact GPU slowdown figure in the TOSEM published version (4.9x vs 30.6x) is unresolved. Check the ACM PDF.

---

## Q5. Decoding: CRF vs constrained Viterbi over BIO/BIOES; span-based vs token-based NER

### Takeaway
BiLSTM-CRF made CRF decoding standard for NER. With BERT-style encoders, a softmax head plus BIO-constrained Viterbi (forbidding illegal transitions like O→I-X) recovers most of the CRF benefit at no training cost. That fits a browser student that should stay a plain ONNX token classifier. Span-based models (SpanNER, GLiNER) handle nesting and boundaries better, at quadratic span cost.

### Cited Findings
- [C] Lafferty, J., McCallum, A., Pereira, F. (2001). *Conditional Random Fields: Probabilistic Models for Segmenting and Labeling Sequence Data.* ICML 2001 — [ACM DL](https://dl.acm.org/doi/10.5555/645530.655813)
- [C] Lample, G., Ballesteros, M., Subramanian, S., Kawakami, K., Dyer, C. (2016). *Neural Architectures for Named Entity Recognition.* NAACL 2016; arXiv:1603.01360. BiLSTM-CRF. Finds IOBES slightly better than IOB — [arXiv](https://arxiv.org/abs/1603.01360)
- [C] Ma, X., Hovy, E. (2016). *End-to-end Sequence Labeling via Bi-directional LSTM-CNNs-CRF.* ACL 2016; arXiv:1603.01354 — [arXiv](https://arxiv.org/abs/1603.01354)
- [C] Ratinov, L., Roth, D. (2009). *Design Challenges and Misconceptions in Named Entity Recognition.* CoNLL 2009. Finds BILOU/BIOES encoding beats BIO — [ACL Anthology](https://aclanthology.org/W09-1119)
- [C] Fu, J., Huang, X., Liu, P. (2021). *SpanNER: Named Entity Re-/Recognition as Span Prediction.* ACL 2021; arXiv:2106.00641. Span enumeration versus sequence labelling. The two approaches have complementary strengths, and the paper proposes a span-based combiner — [arXiv](https://arxiv.org/abs/2106.00641)
- [V] GLiNER (above) is a span-based encoder that matches entity-type embeddings to span representations — [ACL Anthology](https://aclanthology.org/2024.naacl-long.300)
- [V] Structural KD (Wang et al. 2021, above) covers distilling a CRF teacher into a student with a different factorisation — [ACL Anthology](https://aclanthology.org/2021.acl-long.46)

### Inferences
- For the browser, a softmax token head exported to ONNX, plus a tiny JS/Rust-Wasm constrained Viterbi over BIOES transitions, avoids custom CRF ops in ORT Web while enforcing well-formed spans. That decoder could live in the same Rust→Wasm module as the rules.
- Span-based heads (GLiNER-style) cost O(n·L) span enumeration and need custom post-processing. They are worth it only if nested or overlapping PII matters.

### Gaps
- No session-verified source quantifies how much CRF versus softmax+constrained-Viterbi differ on top of transformer encoders for NER. This is commonly reported as small, but I did not verify a specific citation (the BERT paper itself used no CRF).
