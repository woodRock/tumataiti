# Sourced by grid jobs: a CPU-only venv on shared storage, because the ECS Grid
# has no torch. Versions match the laptop's, so quantised models and predictions
# are comparable. The rules binding is rebuilt when its Rust source changes.
STORE=/vol/ecrg-solar/woodj4
VENV="${VENV:-$STORE/venvs/tumataiti-grid}"
(
  flock 9
  [ -x "$VENV/bin/python" ] || /usr/local/bin/python3 -m venv "$VENV"
  "$VENV/bin/python" -c 'import tumataiti_ml, onnxruntime, onnx, onnx_ir, transformers, sentencepiece' 2>/dev/null ||
    "$VENV/bin/pip" install -q -e . onnxruntime==1.31.1 onnx==1.23.2 onnx-ir numpy==2.5.4 \
      transformers==5.22.1 tokenizers==0.23.3 sentencepiece protobuf
  stamp=$(cat ../Cargo.lock ../crates/tumataiti-rules/src/* ../crates/tumataiti-py/src/* | sha256sum)
  if [ "$stamp" != "$(cat "$VENV/.rules-stamp" 2>/dev/null)" ]; then
    # The laptop's Rust, apart from the user's own toolchains: the grid's is older.
    export RUSTUP_HOME="$STORE/rustup" RUSTUP_TOOLCHAIN=1.93.1
    "$HOME/.cargo/bin/rustup" toolchain install "$RUSTUP_TOOLCHAIN" --profile minimal --no-self-update
    PATH="$HOME/.cargo/bin:$PATH" CARGO_TARGET_DIR="${TMPDIR:-/tmp}/tumataiti-cargo" \
      "$VENV/bin/pip" install -q --force-reinstall ../crates/tumataiti-py
    echo "$stamp" > "$VENV/.rules-stamp"
  fi
) 9>"$STORE/venvs/.tumataiti-grid.lock"
export HF_HUB_OFFLINE=1
export TUMATAITI_THREADS="${TUMATAITI_THREADS:-1}"  # SGE gives a job one slot
export OMP_NUM_THREADS=$TUMATAITI_THREADS
export PATH="$VENV/bin:$PATH"
