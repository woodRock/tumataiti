#!/usr/bin/env bash
# Submit scripts/jobs.py to the ECS Grid in stages and wait for each, from the
# repo root on the laptop, with the code committed and synced (`task sync`) and
# inputs copied (grid_push.sh). Lists failed tasks. Without the spooler, the same
# jobs run with `python ml/scripts/jobs.py all`.
#   ml/scripts/grid_submit.sh gold rules threshold robust report checksum uncertainty
#   task fetch --force ml/results ml/runs/thresholds ml/runs/robust
# Jobs write ml/results in the shared copy, so `task sync` refuses until those
# edits are gone: restore them there (git checkout -- ml/results) after fetching.
set -uo pipefail
PY=ml/.venv/bin/python
for prefix in "$@"; do
  ids=()
  for job in $($PY ml/scripts/jobs.py list "$prefix"); do
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
