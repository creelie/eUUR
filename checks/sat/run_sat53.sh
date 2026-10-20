#!/usr/bin/env bash
# run_sat53.sh -- the computer part of the 53-member step.
#
# For each m given (default 4 ... 13) writes the CNF of the configuration one
# step above the boundary (n = 2m, |A| = 4m+1) with above_cnf.py, solves it with
# CaDiCaL writing an LRAT proof into a pipe, and checks that proof while it is
# written with lrat-check (from the drat-trim distribution), so no proof file
# is stored. Every line must end in "UNSAT, proof VERIFIED". Extra arguments
# after "--" are passed to above_cnf.py (e.g. "nontriv").
#
# Needs python3, cadical >= 1.7 (https://github.com/arminbiere/cadical) and
# lrat-check (https://github.com/marijnheule/drat-trim) on the PATH, or CADICAL
# and LRATCHECK set to their paths.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CADICAL="${CADICAL:-cadical}"
LRATCHECK="${LRATCHECK:-lrat-check}"
for t in python3 "$CADICAL" "$LRATCHECK"; do
  command -v "$t" >/dev/null || { echo "missing tool: $t" >&2; exit 2; }
done
ms=(); extra=()
while [ $# -gt 0 ]; do
  if [ "$1" = "--" ]; then shift; extra=("$@"); break; fi
  ms+=("$1"); shift
done
[ ${#ms[@]} -gt 0 ] || ms=(4 5 6 7 8 9 10 11 12 13)
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
fail=0
for m in "${ms[@]}"; do
  cnf="$WORK/m$m.cnf"; pipe="$WORK/m$m.lrat"
  python3 "$HERE/above_cnf.py" "$m" 1 "$cnf" 0 ${extra[@]+"${extra[@]}"}
  mkfifo "$pipe"
  start=$(date +%s)
  "$LRATCHECK" "$cnf" "$pipe" > "$WORK/check$m.out" 2>&1 &
  checker=$!
  set +e
  "$CADICAL" -q --lrat=true --binary=false "$cnf" "$pipe" > /dev/null; rc=$?
  wait "$checker"; crc=$?
  set -e
  secs=$(( $(date +%s) - start ))
  if [ "$rc" -ne 20 ]; then echo "m=$m: solver exit $rc, not UNSAT"; fail=1; continue; fi
  if [ "$crc" -eq 0 ] && grep -q "^c VERIFIED" "$WORK/check$m.out"; then
    echo "m=$m: $(head -1 "$cnf" | cut -d' ' -f3-4) (variables, clauses): UNSAT, proof VERIFIED (${secs} s)"
  else
    echo "m=$m: proof NOT verified"; tail -3 "$WORK/check$m.out"; fail=1
  fi
done
exit $fail
