"""Export a trained student to ONNX and quantise it to int8 (SPEC §10.0 step 6).

Export needs PyTorch (run on ECS); quantisation and evaluation only need
onnxruntime, so they run on a laptop CPU, which is also the latency target.
"""

from __future__ import annotations

import shutil
from pathlib import Path


def export_onnx(model_dir: Path, out: Path, opset: int = 18) -> Path:
    import torch
    from transformers import AutoModelForTokenClassification, AutoTokenizer

    out.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForTokenClassification.from_pretrained(model_dir).eval()
    enc = tokenizer("Kia ora Aroha, ring 021 123 4567.", return_tensors="pt")
    args = (enc["input_ids"], enc["attention_mask"])
    path = out / "model.onnx"
    batch, seq = torch.export.Dim("batch"), torch.export.Dim("sequence", max=512)
    torch.onnx.export(
        model,
        args,
        str(path),
        input_names=["input_ids", "attention_mask"],
        output_names=["logits"],
        dynamic_shapes=({0: batch, 1: seq}, {0: batch, 1: seq}),
        opset_version=opset,
        dynamo=True,
        external_data=False,
    )
    # Tokenizer and label config travel with the ONNX file.
    tokenizer.save_pretrained(out)
    shutil.copy(model_dir / "config.json", out / "config.json")
    return path


def quantise_int8(onnx_path: Path, out_path: Path) -> Path:
    """Dynamic per-channel int8 weights for MatMul/Gemm and the embedding lookup
    (Gather), which is most of a DeBERTa-v3 model; activations stay float.

    M3 found this costs rare classes more than the literature suggests (name
    leakage up to ~1.7x on some name groups), so always re-score after quantising.
    """
    from onnxruntime.quantization import QuantType, quantize_dynamic

    quantize_dynamic(
        str(onnx_path),
        str(out_path),
        weight_type=QuantType.QInt8,
        op_types_to_quantize=["MatMul", "Gemm", "Gather"],
        per_channel=True,
    )
    return out_path
