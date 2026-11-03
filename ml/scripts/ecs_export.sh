#!/usr/bin/env bash
# Export a trained student to ONNX (needs PyTorch, so it runs on ECS).
#   task submit -t "RTX A5000" -n export -- ./scripts/ecs_export.sh deberta-v3-small
#   task fetch runs/m3/deberta-v3-small/onnx
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/ecs_env.sh
( flock 9; "$VENV/bin/python" -c 'import onnxscript' 2>/dev/null || "$VENV/bin/pip" install -q onnxscript onnx ) 9>"$STORE/venvs/.tumataiti.lock"
"$CLI" export --model "runs/m3/$1/model" --out "runs/m3/$1/onnx"
ls -la "runs/m3/$1/onnx"
