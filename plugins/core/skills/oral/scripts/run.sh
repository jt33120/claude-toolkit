#!/bin/sh
# Stop hook entry: return at once while oral mode is off (no Python start-up on every turn),
# then pick a working Python (the Windows Store "python3" stub fails, "python" works).
[ "$1" = hook ] && [ ! -f "$HOME/.claude/oral/on" ] && exit 0
for py in python3 python; do
  if "$py" -c "" >/dev/null 2>&1; then
    exec "$py" "$(dirname "$0")/oral.py" "$@"
  fi
done
exit 0
