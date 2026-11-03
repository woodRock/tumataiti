from __future__ import annotations

import torch

from ..spans import Span
from .encode import union, windows, decode

# AFFILIATION is predicted but not scored yet (SPEC §9.1).
EVAL_CATEGORY = {"AFFILIATION": None}


@torch.inference_mode()
def spans_for(model, tokenizer, text: str, *, threshold=0.5, max_length=512, stride=128, device="cuda") -> list[Span]:
    enc = windows(tokenizer, text, max_length, stride)
    found = []
    for w in range(len(enc["input_ids"])):
        ids = torch.tensor([enc["input_ids"][w]], device=device)
        mask = torch.tensor([enc["attention_mask"][w]], device=device)
        probs = torch.softmax(model(input_ids=ids, attention_mask=mask).logits[0].float(), dim=-1).cpu().numpy()
        offsets = [(a, b) if not sp else (0, 0) for (a, b), sp in zip(enc["offset_mapping"][w], enc["special_tokens_mask"][w])]
        found += decode(text, offsets, probs, threshold)
    return [Span(a, b, label, EVAL_CATEGORY.get(label, label), conf) for a, b, label, conf in union(found)]


def load(model_dir: str, device: str = "cuda"):
    from transformers import AutoModelForTokenClassification, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForTokenClassification.from_pretrained(model_dir, dtype=torch.float32).to(device).eval()
    return model, tokenizer
