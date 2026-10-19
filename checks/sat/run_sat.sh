#!/usr/bin/env bash
# run_sat.sh -- the computer part of Theorem C.
#
# For m = 3, ..., 13 (or the values given as arguments) writes the CNF of the
# boundary configuration with boundary_cnf.py, solves it with CaDiCaL writing a
# DRAT proof, and checks the proof with drat-trim. Every line must end in
# "UNSAT, proof VERIFIED".
#
# Needs python3, cadical (https://github.com/arminbiere/cadical) and drat-trim
# (https://github.com/marijnheule/drat-trim) on the PATH, or CADICAL and DRATTRIM
# set to their paths. On one core m = 12 takes about 5 minutes and m = 13 takes about 15 minutes
# to solve; checking its proof (about 1 GB) takes longer. Proofs are written to
# a temporary directory and deleted.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CADICAL="${CADICAL:-cadical}"
DRATTRIM="${DRATTRIM:-drat-trim}"
for t in python3 "$CADICAL" "$DRATTRIM"; do
  command -v "$t" >/dev/null || { echo "missing tool: $t" >&2; exit 2; }
done
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
ms=("$@")
[ ${#ms[@]} -gt 0 ] || ms=(3 4 5 6 7 8 9 10 11 12 13)
fail=0
for m in "${ms[@]}"; do
  cnf="$WORK/m$m.cnf"; proof="$WORK/m$m.drat"
  python3 "$HERE/boundary_cnf.py" "$m" "$cnf"
  set +e; "$CADICAL" -q "$cnf" "$proof" > /dev/null; rc=$?; set -e
  if [ "$rc" -ne 20 ]; then echo "m=$m: solver exit $rc, not UNSAT"; fail=1; continue; fi
  out="$("$DRATTRIM" "$cnf" "$proof" -t 200000 | tr "\r" "\n" || true)"
  if grep -q "^s VERIFIED" <<< "$out"; then
    echo "m=$m: $(head -1 "$cnf" | cut -d' ' -f3-4) (variables, clauses): UNSAT, proof VERIFIED"
  else
    echo "m=$m: proof NOT verified"; fail=1
  fi
  rm -f "$proof"
done
exit $fail
