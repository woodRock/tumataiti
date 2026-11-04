import numpy as np
import pytest

ort = pytest.importorskip("onnxruntime")
onnx = pytest.importorskip("onnx")
pytest.importorskip("onnx_ir")

from onnx import TensorProto, helper, numpy_helper  # noqa: E402

from tumataiti_ml.student.export import quantise_int8  # noqa: E402


def tiny_model(path):
    """Embedding lookup then one linear layer: the two kinds of weight quantise_int8 touches."""
    rng = np.random.default_rng(0)
    emb = numpy_helper.from_array(rng.normal(size=(50, 64)).astype(np.float32), "emb")
    w = numpy_helper.from_array(rng.normal(size=(64, 32)).astype(np.float32), "w")
    graph = helper.make_graph(
        [helper.make_node("Gather", ["emb", "ids"], ["h"]), helper.make_node("MatMul", ["h", "w"], ["y"])],
        "tiny",
        [helper.make_tensor_value_info("ids", TensorProto.INT64, [1, None])],
        [helper.make_tensor_value_info("y", TensorProto.FLOAT, [1, None, 32])],
        [emb, w],
    )
    model = helper.make_model(graph, ir_version=10, opset_imports=[helper.make_opsetid("", 18), helper.make_opsetid("com.microsoft", 1)])
    onnx.save(model, str(path))


def run(path, ids):
    return ort.InferenceSession(str(path), providers=["CPUExecutionProvider"]).run(None, {"ids": ids})[0]


# Tolerances are relative to the output scale; every option has int8 embeddings.
@pytest.mark.parametrize("encoder,tol", [("fp16", 0.03), ("int8-block", 0.03), ("int4-block", 0.2), ("dynamic", 0.2)])
def test_quantised_model_tracks_fp32(tmp_path, encoder, tol):
    src = tmp_path / "model.onnx"
    tiny_model(src)
    out = quantise_int8(src, tmp_path / f"q_{encoder}.onnx", encoder)
    ids = np.arange(50, dtype=np.int64)[None]
    ref, got = run(src, ids), run(out, ids)
    assert got.shape == ref.shape
    assert np.abs(got - ref).max() / np.abs(ref).max() < tol
    assert out.stat().st_size < src.stat().st_size


def test_fp16_keeps_compute_in_fp32(tmp_path):
    src = tmp_path / "model.onnx"
    tiny_model(src)
    out = quantise_int8(src, tmp_path / "q.onnx", "fp16")
    m = onnx.load(str(out))
    assert any(n.op_type == "Cast" for n in m.graph.node)
    assert {i.name: i.data_type for i in m.graph.initializer}["w_fp16"] == TensorProto.FLOAT16
