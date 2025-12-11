#!/usr/bin/env bash
# run_tests.sh - Ejecuta el runner Python y abre el HTML en Linux/WSL
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
python "$SCRIPT_DIR/run_tests_and_report.py"
HTML="$SCRIPT_DIR/tests/test_report.html"
if [ -f "$HTML" ]; then
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$HTML" &
  elif command -v sensible-browser >/dev/null 2>&1; then
    sensible-browser "$HTML" &
  else
    echo "Reporte HTML generado en: $HTML"
  fi
else
  cat "$SCRIPT_DIR/tests/test_report.txt"
fi
