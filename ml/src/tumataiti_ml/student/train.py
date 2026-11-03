"""Fine-tune a student encoder for BIO token classification (SPEC §10.0).

Supervision: gold spans from the synthetic NZ training split (template slots)
and from PII-Masking-300k's English training split. The checkpoint with the best
character-level F1 on the NZ dev split is kept. Leakage alone is not used for
selection: a broken model that redacts everything has zero leakage.
"""

from __future__ import annotations

import json
import os
import random
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import torch

from .. import metrics
from ..spans import Doc, read_jsonl
from .encode import IGNORE_INDEX, TAG_ID, TAGS, encode_doc
from .infer import spans_for


@dataclass
class Config:
    backbone: str
    train: list[str]
    dev: str
    out: str
    epochs: int = 3
    lr: float = 5e-5
    batch_size: int = 16
    max_length: int = 512
    stride: int = 128
    warmup: float = 0.1
    weight_decay: float = 0.01
    seed: int = 0
    max_steps: int | None = None  # for smoke tests
    dev_limit: int | None = None
    bf16: bool = True
    deterministic: bool = True
    log_every: int = 200


def set_determinism(seed: int, deterministic: bool = True) -> None:
    os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(deterministic, warn_only=True)
    torch.backends.cudnn.benchmark = False


def collate(batch: list[dict], pad_id: int) -> dict[str, torch.Tensor]:
    n = max(len(b["input_ids"]) for b in batch)
    pad = lambda xs, v: [x + [v] * (n - len(x)) for x in xs]  # noqa: E731
    return {
        "input_ids": torch.tensor(pad([b["input_ids"] for b in batch], pad_id)),
        "attention_mask": torch.tensor(pad([b["attention_mask"] for b in batch], 0)),
        "labels": torch.tensor(pad([b["labels"] for b in batch], IGNORE_INDEX)),
    }


def evaluate(model, tokenizer, dev: list[Doc], cfg: Config, device: str) -> dict:
    model.eval()
    preds = {
        d.id: Doc(d.id, "", spans_for(model, tokenizer, d.text, max_length=cfg.max_length, stride=cfg.stride, device=device))
        for d in dev
    }
    model.train()
    r = metrics.score(dev, preds).as_dict()
    return {"doc_leak_rate": r["doc_leak_rate"], "span_leak_rate": r["span_leak_rate"], "char_f1": r["char_any"]["f1"]}


def train(cfg: Config, device: str = "cuda") -> None:
    from transformers import AutoModelForTokenClassification, AutoTokenizer, get_linear_schedule_with_warmup

    set_determinism(cfg.seed, cfg.deterministic)
    out = Path(cfg.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "config.json").write_text(json.dumps(asdict(cfg), indent=2))
    log = (out / "log.jsonl").open("a")

    tokenizer = AutoTokenizer.from_pretrained(cfg.backbone)
    # Transformers 5 loads checkpoints in their stored dtype by default, and the
    # DeBERTa-v3 checkpoints are fp16: AdamW's epsilon underflows there and the
    # first step turns every weight NaN. Train master weights in fp32.
    model = AutoModelForTokenClassification.from_pretrained(
        cfg.backbone,
        dtype=torch.float32,
        num_labels=len(TAGS),
        id2label=dict(enumerate(TAGS)),
        label2id=TAG_ID,
    ).to(device)

    docs = [d for f in cfg.train for d in read_jsonl(Path(f))]
    examples = [ex for d in docs for ex in encode_doc(tokenizer, d, cfg.max_length, cfg.stride)]
    dev = list(read_jsonl(Path(cfg.dev)))[: cfg.dev_limit]
    print(f"{len(docs)} training documents -> {len(examples)} windows; {len(dev)} dev documents", flush=True)

    steps_per_epoch = (len(examples) + cfg.batch_size - 1) // cfg.batch_size
    total = cfg.max_steps or steps_per_epoch * cfg.epochs
    no_decay = ("bias", "LayerNorm.weight", "norm.weight")
    groups = [
        {"params": [p for n, p in model.named_parameters() if not any(k in n for k in no_decay)], "weight_decay": cfg.weight_decay},
        {"params": [p for n, p in model.named_parameters() if any(k in n for k in no_decay)], "weight_decay": 0.0},
    ]
    opt = torch.optim.AdamW(groups, lr=cfg.lr)
    sched = get_linear_schedule_with_warmup(opt, int(cfg.warmup * total), total)
    gen = torch.Generator().manual_seed(cfg.seed)
    pad_id = tokenizer.pad_token_id

    best = None
    step = 0
    model.train()
    for epoch in range(cfg.epochs):
        order = torch.randperm(len(examples), generator=gen).tolist()
        t0 = time.time()
        for i in range(0, len(order), cfg.batch_size):
            batch = collate([examples[j] for j in order[i : i + cfg.batch_size]], pad_id)
            batch = {k: v.to(device) for k, v in batch.items()}
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16, enabled=cfg.bf16 and device.startswith("cuda")):
                loss = model(**batch).loss
            if not torch.isfinite(loss):
                raise RuntimeError(f"non-finite loss {loss.item()} at step {step + 1}; stopping")
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            sched.step()
            opt.zero_grad(set_to_none=True)
            step += 1
            if step % cfg.log_every == 0 or step <= 5:
                print(f"epoch {epoch} step {step}/{total} loss {loss.item():.4f} {time.time() - t0:.0f}s", flush=True)
            if cfg.max_steps and step >= cfg.max_steps:
                break
        score = evaluate(model, tokenizer, dev, cfg, device)
        record = {"epoch": epoch, "step": step, "seconds": time.time() - t0, **score}
        print(json.dumps(record), flush=True)
        log.write(json.dumps(record) + "\n")
        log.flush()
        key = (-score["char_f1"], score["doc_leak_rate"])
        if best is None or key < best:
            best = key
            model.save_pretrained(out / "model")
            tokenizer.save_pretrained(out / "model")
            (out / "best.json").write_text(json.dumps(record, indent=2))
        if cfg.max_steps and step >= cfg.max_steps:
            break
