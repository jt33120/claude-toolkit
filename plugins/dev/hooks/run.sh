#!/bin/sh
# Hook entry: pick a working Python (the Windows Store "python3" stub fails, "python" works).
# pre_pr runs on every Bash call, so skip Python start-up unless the command opens a PR/MR.
name="$1"; shift
input=$(cat)
if [ "$name" = pre_pr ]; then
  case "$input" in
    *"pr create"*|*"mr create"*) ;;
    *) exit 0 ;;
  esac
fi
for py in python3 python; do
  if "$py" -c "" >/dev/null 2>&1; then
    printf '%s' "$input" | "$py" "$(dirname "$0")/$name.py" "$@"
    exit $?
  fi
done
exit 0
