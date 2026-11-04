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


ENCODERS = ("dynamic", "fp16", "int8-block", "int4-block")


def quantise_int8(onnx_path: Path, out_path: Path, encoder: str = "dynamic", block_size: int = 32) -> Path:
    """int8 embeddings plus a choice of encoder weights.

    The embedding lookup (Gather) is always quantised per channel to int8: it is
    most of a DeBERTa-v3 model's size and quantising it alone costs nothing (M3,
    SPEC §9.6). The encoder MatMuls are where accuracy is lost, so:

    - `dynamic`: int8 weights and dynamically quantised int8 activations (the
      M3 default; breaks mDeBERTa and ModernBERT);
    - `fp16`: weights stored as fp16 and cast to fp32 at load, so compute is
      fp32 and only the stored weights are rounded;
    - `int8-block` / `int4-block`: weight-only block-wise quantisation
      (MatMulNBits, one scale per `block_size` weights), fp32 activations.
    """
    import onnx
    from onnxruntime.quantization import QuantType, quantize_dynamic

    if encoder not in ENCODERS:
        raise ValueError(f"encoder must be one of {ENCODERS}")
    if encoder == "dynamic":
        quantize_dynamic(
            str(onnx_path),
            str(out_path),
            weight_type=QuantType.QInt8,
            op_types_to_quantize=["MatMul", "Gemm", "Gather"],
            per_channel=True,
        )
        return out_path

    model = onnx.load(str(onnx_path))
    if encoder == "fp16":
        model = _fp16_weights(model)
    else:
        from onnxruntime.quantization.matmul_nbits_quantizer import MatMulNBitsQuantizer

        q = MatMulNBitsQuantizer(
            model, bits=8 if encoder == "int8-block" else 4, block_size=block_size, is_symmetric=True,
            op_types_to_quantize=("MatMul",),
        )
        q.process()
        model = q.model.model
    tmp = out_path.with_suffix(".tmp.onnx")
    onnx.save(model, str(tmp))
    quantize_dynamic(str(tmp), str(out_path), weight_type=QuantType.QInt8, op_types_to_quantize=["Gather"], per_channel=True)
    tmp.unlink()
    return out_path


def _fp16_weights(model):
    """Store MatMul/Gemm weight initializers as fp16, each behind a Cast back to
    fp32. ONNX Runtime folds the Casts when the session loads."""
    import collections

    from onnx import TensorProto, helper, numpy_helper

    inits = {i.name: i for i in model.graph.initializer}
    users = collections.Counter(x for n in model.graph.node for x in n.input)
    done: dict[str, str] = {}
    casts = []
    for node in model.graph.node:
        if node.op_type not in ("MatMul", "Gemm"):
            continue
        for k, name in enumerate(node.input):
            init = inits.get(name)
            if init is None or init.data_type != TensorProto.FLOAT or users[name] != 1:
                continue
            if name not in done:
                half = numpy_helper.from_array(numpy_helper.to_array(init).astype("float16"), name + "_fp16")
                model.graph.initializer.remove(init)
                model.graph.initializer.append(half)
                done[name] = name + "_fp32"
                casts.append(helper.make_node("Cast", [half.name], [done[name]], to=TensorProto.FLOAT))
            node.input[k] = done[name]
    nodes = casts + list(model.graph.node)
    del model.graph.node[:]
    model.graph.node.extend(nodes)
    return model
