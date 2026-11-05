#!/usr/bin/env bash
# Submit grid jobs in stages and wait for each, from the repo root on the laptop,
# with the code committed and synced (`task sync`). Prints a failed job's log.
#   ml/scripts/grid_submit.sh gold threshold robust
#   task fetch ml/runs/thresholds ml/runs/robust
set -uo pipefail
PY=ml/.venv/bin/python
for prefix in "$@"; do
  ids=()
  for job in $($PY ml/scripts/grid_job.py list "$prefix"); do
    ids+=("$(task submit -q -g 0 -H grid -C ml -n "${job//\//-}" -- bash scripts/grid_run.sh "$job" 2>/dev/null)")
  done
  echo "$prefix: ${#ids[@]} jobs: ${ids[*]}"
  task wait "${ids[@]}" --timeout "${GRID_TIMEOUT:-21600}"; rc=$?
  if [ $rc -ne 0 ]; then
    echo "$prefix: wait exited $rc" >&2
    task list | grep -E "failed|error|lost" | tail -20 >&2
    exit $rc
  fi
done
