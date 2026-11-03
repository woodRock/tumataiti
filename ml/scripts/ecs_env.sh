# Sourced by the ECS job scripts: a venv on shared storage that reuses the
# servers' system PyTorch and adds transformers and tokenizer dependencies.
STORE=/vol/ecrg-solar/woodj4
export HF_HOME="${HF_HOME:-$STORE/hf}"
export CUBLAS_WORKSPACE_CONFIG=:4096:8
VENV="${VENV:-$STORE/venvs/tumataiti-teacher}"
# Several jobs may start at once on the shared venv, so set it up under a lock,
# and only install when something is missing (the package is editable, so code
# changes need no reinstall).
(
  flock 9
  [ -x "$VENV/bin/python" ] || python3 -m venv --system-site-packages "$VENV"
  "$VENV/bin/python" -c 'import tumataiti_ml.student, transformers, sentencepiece' 2>/dev/null ||
    "$VENV/bin/pip" install -q -e . "transformers>=5.6" sentencepiece protobuf
) 9>"$STORE/venvs/.tumataiti.lock"
"$VENV/bin/python" -c 'import torch, transformers; print("torch", torch.__version__, "transformers", transformers.__version__, torch.cuda.get_device_name())'
CLI="$VENV/bin/tumataiti-ml"
