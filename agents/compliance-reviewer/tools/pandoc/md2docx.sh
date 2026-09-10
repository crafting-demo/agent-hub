#!/bin/bash
# Deliver a Markdown memo or redlines file as .docx, which is what counsel works in.
# Usage: md2docx.sh INPUT.md OUTPUT.docx
set -euo pipefail

in="${1:?usage: md2docx.sh INPUT.md OUTPUT.docx}"
out="${2:?usage: md2docx.sh INPUT.md OUTPUT.docx}"
exec "$HOME/legal/bin/pandoc" "$in" -f gfm -o "$out"
