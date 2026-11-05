# Sourced by grid jobs: a CPU-only venv on shared storage, because the ECS Grid
# has no torch and the rules binding isn't built there. Versions match the
# laptop's, so quantised models and predictions are comparable.
STORE=/vol/ecrg-solar/woodj4
VENV="${VENV:-$STORE/venvs/tumataiti-grid}"
(
  flock 9
  [ -x "$VENV/bin/python" ] || /usr/local/bin/python3 -m venv "$VENV"
  "$VENV/bin/python" -c 'import tumataiti_ml, onnxruntime, onnx, onnx_ir, transformers, sentencepiece' 2>/dev/null ||
    "$VENV/bin/pip" install -q -e . onnxruntime==1.31.1 onnx==1.23.2 onnx-ir numpy==2.5.4 \
      transformers==5.22.1 tokenizers==0.23.3 sentencepiece protobuf
) 9>"$STORE/venvs/.tumataiti-grid.lock"
export HF_HUB_OFFLINE=1
export TUMATAITI_THREADS="${TUMATAITI_THREADS:-1}"  # SGE gives a job one slot
export OMP_NUM_THREADS=$TUMATAITI_THREADS
export PATH="$VENV/bin:$PATH"
