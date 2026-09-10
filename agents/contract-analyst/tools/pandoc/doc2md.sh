#!/bin/bash
# Convert a contract to Markdown so it can be reviewed as text.
# Usage: doc2md.sh INPUT [OUTPUT.md]   (prints to stdout when OUTPUT is omitted)
set -euo pipefail

in="${1:?usage: doc2md.sh INPUT [OUTPUT.md]}"
out="${2:-}"

case "${in,,}" in
  *.doc)
    echo "doc2md: '$in' is legacy binary Word (.doc). pandoc cannot read it; ask for a .docx export (Word or LibreOffice: File > Save As > .docx)." >&2
    exit 2 ;;
  *.pdf)
    echo "doc2md: '$in' is a PDF. pandoc cannot read PDF input; ask for the .docx the PDF was produced from." >&2
    exit 2 ;;
esac

# --track-changes=all keeps the counterparty's redlines visible as
# insertion/deletion spans instead of silently accepting them.
args=("$in" -t gfm --wrap=none --track-changes=all)
[[ -n "$out" ]] && args+=(-o "$out")
exec "$HOME/legal/bin/pandoc" "${args[@]}"
