#!/usr/bin/env bash
# Validate hub manifests, compiled LLMAgent YAML, and exec templates.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 "$ROOT/scripts/validate.py"

if ! command -v cs >/dev/null 2>&1; then
  echo "warn: cs not on PATH; skipping template validate" >&2
  exit 0
fi

shopt -s nullglob
templates=(dist/*/template.yaml)
if [[ ${#templates[@]} -eq 0 ]]; then
  echo "ok   no compiled templates"
  exit 0
fi

if ! cs whoami >/dev/null 2>&1; then
  echo "warn: cs is not authenticated; skipping cs template validate" >&2
  exit 0
fi

for tmpl in "${templates[@]}"; do
  echo "cs template validate ${tmpl}"
  cs template validate "$tmpl"
done
