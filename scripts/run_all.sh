#!/usr/bin/env bash
# run_all.sh -- builds the Lean project, checks its axioms and runs the checks.
#
# Usage: scripts/run_all.sh             (all steps)
#        scripts/run_all.sh --no-lean   (skip the Lean build)
# Environment:
#   CHECKS="python julia c cpp"   the checks to run (default: all four; "" runs none)
#   SKIP_LEAN=1                   same as --no-lean
# Requirements: elan (Lean 4) for the Lean build; python3 with python-flint, julia, a C
# compiler and a C++20 compiler for the checks that are run.
#
# The python check is the proof: the interval certificate of the two inequalities away
# from the point of contact (verify_exact.py, about ninety seconds) and the ball-arithmetic
# Hessian certificate on the square S around it (tangency.py). The C, C++ and Julia
# programs are independent floating-point and high-precision cross-checks.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD="$(mktemp -d)"
trap 'rm -rf "$BUILD"' EXIT
CC_BIN="${CC:-cc}"
CXX_BIN="${CXX:-c++}"
CHECKS="${CHECKS-python julia c cpp}"
SKIP_LEAN="${SKIP_LEAN:-0}"
[ "${1:-}" = "--no-lean" ] && SKIP_LEAN=1

step() { printf '\n=== %s\n' "$1"; }
need() { command -v "$1" >/dev/null 2>&1 || { echo "missing tool: $1" >&2; exit 2; }; }

for c in $CHECKS; do
  case "$c" in
    python) need python3 ;;
    julia) need julia ;;
    c) need "$CC_BIN" ;;
    cpp) need "$CXX_BIN" ;;
    *) echo "unknown check: $c" >&2; exit 2 ;;
  esac
done

if [ "$SKIP_LEAN" != 1 ]; then
  need lake
  step "Lean 4: lake build"
  ( cd "$ROOT/lean" && lake build 2>&1 | tee "$BUILD/lean.log" | grep -E "error|Build completed|axioms" ) || true
  if ! grep -q "Build completed successfully" "$BUILD/lean.log" || grep -q "error" "$BUILD/lean.log"; then
    echo "Lean build failed" >&2; exit 1
  fi
  step "Lean 4: axioms of the breakpoint theorems"
  n=0
  for thm in z_sq_add_z_gt_one z_lt_inv_sqrt_two A_gt_inv_sqrt_two U_gt_inv_sqrt_two \
             A_B_order tangency_square_in_middle tangency_square_below_A inv_sqrt_two_lt_B; do
    grep -q "'UnionClosed.$thm' does not depend on any axioms" "$BUILD/lean.log" \
      || { echo "unexpected axioms for $thm" >&2; exit 1; }
    n=$((n + 1))
  done
  echo "$n theorems, none depends on any axiom"
  if grep -rnwE "sorry|admit|native_decide|bv_decide" "$ROOT/lean/UnionClosed" "$ROOT/lean/UnionClosed.lean"; then
    echo "sorry, admit, native_decide or bv_decide found" >&2; exit 1
  fi
  if grep -rnE "^[[:space:]]*axiom[[:space:]]" "$ROOT/lean/UnionClosed" "$ROOT/lean/UnionClosed.lean"; then
    echo "axiom declaration found" >&2; exit 1
  fi
  echo "no sorry, admit, native_decide, bv_decide or axiom declarations"
fi

for c in $CHECKS; do
  case "$c" in
    python)
      step "Python: Hessian certificate on S"
      python3 -I "$ROOT/checks/python/tangency.py"
      step "Python: interval certificate on the rest of the square"
      VERIFY_OUT="$BUILD" python3 -I "$ROOT/checks/python/verify_exact.py" ;;
    julia)
      step "Julia"
      julia "$ROOT/checks/julia/check.jl" ;;
    c)
      step "C"
      "$CC_BIN" -O2 -std=c99 -o "$BUILD/check_c" "$ROOT/checks/c/check.c" -lm
      "$BUILD/check_c" ;;
    cpp)
      step "C++"
      "$CXX_BIN" -O2 -std=c++20 -o "$BUILD/check_cpp" "$ROOT/checks/cpp/check.cpp"
      "$BUILD/check_cpp" ;;
  esac
done

printf '\nAll steps passed.\n'
