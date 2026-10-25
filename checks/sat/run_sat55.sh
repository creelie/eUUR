#!/usr/bin/env bash
# run_sat55.sh -- the computer part of the 55-member step.
#
# A smallest counterexample with 55 members has m = 14 elements and n = 2m-1
# (the boundary case), or m = 13 and n = 2m+1, where Appendix G leaves three
# block patterns. Each case is a configuration of family_cnf.py:
#
#   boundary   m = 14   R, S, T of 14, 14, 14 down-sets, frequency >= 28
#   i-a        m = 13   R, S, T of 15, 14, 14 down-sets, frequency >= 28
#   i-b        m = 13   R, S, T of 15, 15, 13 down-sets, frequency >= 28
#   ii         m = 13   R, S, T of 14, 14, 14 down-sets and one extra set,
#                       frequency >= 28
#
# For each case given (default: all four) the script writes the CNF, solves it
# with CaDiCaL writing an LRAT proof into a pipe, and checks the proof while it
# is written with lrat-check, so no proof file is stored. Every line must end in
# "UNSAT, proof VERIFIED". "m=K" before the cases replaces m (for tests: the
# sizes then follow the same pattern).
#
# Needs python3, cadical >= 1.7 and lrat-check on the PATH, or CADICAL and
# LRATCHECK set to their paths.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CADICAL="${CADICAL:-cadical}"
LRATCHECK="${LRATCHECK:-lrat-check}"
for t in python3 "$CADICAL" "$LRATCHECK"; do
  command -v "$t" >/dev/null || { echo "missing tool: $t" >&2; exit 2; }
done
mset=""
if [ $# -gt 0 ] && [[ "$1" == m=* ]]; then mset="${1#m=}"; shift; fi
cases=("$@")
[ ${#cases[@]} -gt 0 ] || cases=(boundary i-a i-b ii)
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
fail=0
for c in "${cases[@]}"; do
  case "$c" in
    boundary) m=${mset:-14}; args=("$m" "$m" "$m" "$m" $((2*m))) ;;
    i-a) m=${mset:-13}; args=("$m" $((m+2)) $((m+1)) $((m+1)) $((2*m+2))) ;;
    i-b) m=${mset:-13}; args=("$m" $((m+2)) $((m+2)) "$m" $((2*m+2))) ;;
    ii)  m=${mset:-13}; args=("$m" $((m+1)) $((m+1)) $((m+1)) $((2*m+2))) ;;
    *) echo "unknown case: $c" >&2; exit 2 ;;
  esac
  cnf="$WORK/$c.cnf"; pipe="$WORK/$c.lrat"
  if [ "$c" = ii ]; then python3 "$HERE/family_cnf.py" "${args[@]}" "$cnf" extra
  else python3 "$HERE/family_cnf.py" "${args[@]}" "$cnf"; fi
  mkfifo "$pipe"
  start=$(date +%s)
  "$LRATCHECK" "$cnf" "$pipe" > "$WORK/check-$c.out" 2>&1 &
  checker=$!
  set +e
  "$CADICAL" -q --lrat=true --binary=false "$cnf" "$pipe" > /dev/null; rc=$?
  wait "$checker"; crc=$?
  set -e
  secs=$(( $(date +%s) - start ))
  if [ "$rc" -ne 20 ]; then echo "$c (m=$m): solver exit $rc, not UNSAT"; fail=1; continue; fi
  if [ "$crc" -eq 0 ] && grep -q "^c VERIFIED" "$WORK/check-$c.out"; then
    echo "$c (m=$m): $(head -1 "$cnf" | cut -d' ' -f3-4) (variables, clauses): UNSAT, proof VERIFIED (${secs} s)"
  else
    echo "$c (m=$m): proof NOT verified"; tail -3 "$WORK/check-$c.out"; fail=1
  fi
done
exit $fail
