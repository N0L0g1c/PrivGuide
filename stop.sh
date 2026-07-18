#!/usr/bin/env bash
# Stop the background PrivGuide server started by serve.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="${ROOT}/.serve.pid"
PORT="${1:-8765}"

if [[ -f "$PID_FILE" ]]; then
  pid="$(cat "$PID_FILE" 2>/dev/null || true)"
  if [[ -n "${pid}" ]] && kill -0 "$pid" 2>/dev/null; then
    kill "$pid" 2>/dev/null || true
    # Wait briefly, then force if needed
    for _ in 1 2 3 4 5; do
      kill -0 "$pid" 2>/dev/null || break
      sleep 0.1
    done
    if kill -0 "$pid" 2>/dev/null; then
      kill -9 "$pid" 2>/dev/null || true
    fi
    echo "Stopped PrivGuide server (pid ${pid})"
  else
    echo "No running process for pid in ${PID_FILE}"
  fi
  rm -f "$PID_FILE"
else
  # Fallback: kill whatever is on the default port
  if pkill -f "python3 -m http.server ${PORT}" 2>/dev/null; then
    echo "Stopped process on port ${PORT}"
  else
    echo "Nothing to stop (no pid file, nothing on port ${PORT})"
  fi
fi
