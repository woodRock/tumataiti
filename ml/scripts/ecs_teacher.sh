#!/usr/bin/env bash
# Run the openai/privacy-filter teacher over both evaluation sets on one ECS GPU.
#
# Submit from ml/ on the laptop:
#   task sync
#   task submit -t "RTX A5000" -n teacher-eval -- ./scripts/ecs_teacher.sh
#   task fetch ml/runs/openai-privacy-filter
#
# The venv reuses the servers' system PyTorch and only adds transformers.
set -euo pipefail
cd "$(dirname "$0")/.."

STORE=/vol/ecrg-solar/woodj4
export HF_HOME="${HF_HOME:-$STORE/hf}"
VENV="${VENV:-$STORE/venvs/tumataiti-teacher}"

if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv --system-site-packages "$VENV"
fi
"$VENV/bin/pip" install -q -e . "transformers>=5.6"
"$VENV/bin/python" -c 'import torch, transformers; print("torch", torch.__version__, "transformers", transformers.__version__, torch.cuda.get_device_name())'

CLI="$VENV/bin/tumataiti-ml"
"$CLI" generate --n 1600 --seed 0 --out data/nz_synth_v0.jsonl
"$CLI" prepare-pii300k --raw data/raw/pii300k_en_validation.jsonl --out data/pii300k_en_val.jsonl

for ds in nz_synth_v0 pii300k_en_val; do
  "$CLI" predict --detector openai-privacy-filter --device cuda \
    --gold "data/$ds.jsonl" --out "runs/openai-privacy-filter/$ds.jsonl"
done
