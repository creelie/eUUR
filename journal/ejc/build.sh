#!/usr/bin/env bash
# build.sh -- the paper in the format of The Electronic Journal of Combinatorics.
#
#   journal/ejc/main.tex                  written from paper/main.tex by make_ejc.py
#   dist/UnionClosedLimit_EJC.pdf         the paper in the journal's format
#   dist/UnionClosedLimit_EJC-tex.zip     main.tex, e-jc.sty and the figures as PNG
#
# Needs python3, pdflatex (with orcidlink) and zip. Run from anywhere.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
for t in python3 pdflatex zip; do
  command -v "$t" >/dev/null || { echo "missing tool: $t" >&2; exit 2; }
done
python3 "$ROOT/journal/ejc/make_ejc.py"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/figures"
cp "$HERE/main.tex" "$HERE/e-jc.sty" "$WORK/"
grep -o 'figures/[A-Za-z0-9_]*\.png' "$HERE/main.tex" | sort -u | while read -r f; do
  cp "$ROOT/paper/$f" "$WORK/$f"
done
( cd "$WORK"
  for run in 1 2 3 4; do
    pdflatex -interaction=nonstopmode -halt-on-error main.tex > /dev/null
    [ "$run" -ge 2 ] && ! grep -q "Rerun to get" main.log && break
  done
  if grep -E "Overfull|Underfull|undefined|Rerun to get" main.log; then
    echo "build.sh: fix the warnings above" >&2; exit 1
  fi
  rm -f main.aux main.log main.out main.toc
  mkdir -p "$ROOT/dist"
  mv main.pdf "$ROOT/dist/UnionClosedLimit_EJC.pdf"
  rm -f "$ROOT/dist/UnionClosedLimit_EJC-tex.zip"
  zip -qrX "$ROOT/dist/UnionClosedLimit_EJC-tex.zip" main.tex e-jc.sty figures )
echo "built: dist/UnionClosedLimit_EJC.pdf dist/UnionClosedLimit_EJC-tex.zip"
