# Sourced by grid jobs: a CPU-only venv on shared storage, because the ECS Grid
# has no torch. Versions match the laptop's, so quantised models and predictions
# are comparable.
STORE=/vol/ecrg-solar/woodj4
VENV="${VENV:-$STORE/venvs/tumataiti-grid}"
# Set up only when these inputs change: all jobs share this venv, so reinstalling
# while others run crashes them (SIGBUS, stale file handles).
(
  flock 9
  stamp=$(cat scripts/grid_env.sh pyproject.toml ../Cargo.lock ../crates/tumataiti-rules/src/* ../crates/tumataiti-py/src/* | sha256sum)
  if [ "$stamp" != "$(cat "$VENV/.stamp" 2>/dev/null)" ]; then
    [ -x "$VENV/bin/python" ] || /usr/local/bin/python3 -m venv "$VENV"
    "$VENV/bin/pip" install -q -e . onnxruntime==1.31.1 onnx==1.23.2 onnx-ir numpy==2.5.4 \
      transformers==5.22.1 tokenizers==0.23.3 sentencepiece protobuf
    # The laptop's Rust, apart from the user's own toolchains: the grid's is older.
    export RUSTUP_HOME="$STORE/rustup" RUSTUP_TOOLCHAIN=1.93.1
    "$HOME/.cargo/bin/rustup" toolchain install "$RUSTUP_TOOLCHAIN" --profile minimal --no-self-update
    PATH="$HOME/.cargo/bin:$PATH" CARGO_TARGET_DIR="${TMPDIR:-/tmp}/tumataiti-cargo" \
      "$VENV/bin/pip" install -q --force-reinstall ../crates/tumataiti-py
    echo "$stamp" > "$VENV/.stamp"
  fi
) 9>"$STORE/venvs/.tumataiti-grid.lock"
export HF_HUB_OFFLINE=1
export TUMATAITI_THREADS="${TUMATAITI_THREADS:-1}"  # SGE gives a job one slot
export OMP_NUM_THREADS=$TUMATAITI_THREADS
export PATH="$VENV/bin:$PATH"
