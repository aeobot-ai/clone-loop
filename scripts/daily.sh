#!/usr/bin/env bash
# Daily entry point (cron/launchd). Runs one loop turn and commits the results.
set -euo pipefail
cd "$(dirname "$0")/.."
if [ -f .env ]; then set -a; . ./.env; set +a; fi  # cloud runs get secrets from the environment instead
export PATH="$HOME/.local/bin:$PATH"
uv run python -m loop run
git add data out learnings.md
git commit -q -m "loop: $(TZ=Asia/Seoul date +%F)" || true
git push -q || true
