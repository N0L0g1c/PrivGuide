#!/usr/bin/env bash
# Start PrivGuide static server in the background
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
PORT="${1:-8765}"
PID_FILE="${ROOT}/.serve.pid"
LOG_FILE="${ROOT}/.serve.log"

cd "$ROOT"

# Already running?
if [[ -f "$PID_FILE" ]]; then
  old_pid="$(cat "$PID_FILE" 2>/dev/null || true)"
  if [[ -n "${old_pid}" ]] && kill -0 "$old_pid" 2>/dev/null; then
    echo "Already running (pid ${old_pid}) → http://127.0.0.1:${PORT}/"
    echo "Stop with:  ./stop.sh   or   kill ${old_pid}"
    exit 0
  fi
  rm -f "$PID_FILE"
fi

if command -v ss >/dev/null 2>&1 && ss -tln 2>/dev/null | grep -qE ":${PORT}\\s"; then
  echo "Port ${PORT} is already in use by another process."
  echo "Try:  ./serve.sh 9000"
  exit 1
fi

nohup python3 -m http.server "$PORT" >>"$LOG_FILE" 2>&1 &
pid=$!
echo "$pid" >"$PID_FILE"

# Brief check that it stayed up
sleep 0.3
if ! kill -0 "$pid" 2>/dev/null; then
  echo "Failed to start. See ${LOG_FILE}"
  rm -f "$PID_FILE"
  exit 1
fi

echo "PrivGuide started in background (pid ${pid})"
echo "  URL:  http://127.0.0.1:${PORT}/"
echo "  Log:  ${LOG_FILE}"
echo "  Stop: ./stop.sh"
