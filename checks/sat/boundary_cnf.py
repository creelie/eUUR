#!/usr/bin/env python3
"""Write the CNF of the boundary configuration of Section 7 for a given m.

A smallest counterexample with 4m-1 members gives, on the m-2 points of W,
  * a partial order (the domination order restricted to W), naturally labelled;
  * two families R and S of m distinct down-sets of W, each closed under
    intersection;
  * R & S empty or a principal down-set D(j) for every R in R, S in S;
  * at least m-1 members of R and S together containing each point of W.
This script writes those constraints in DIMACS form. Lemma 7.4 of the paper says
that each is a consequence of the counterexample; the CNF is unsatisfiable for
m = 3, ..., 13 (run_sat.sh checks this with CaDiCaL and a DRAT proof).

Usage: python3 boundary_cnf.py m out.cnf
"""
import itertools
import sys


class Pool:
    def __init__(self):
        self.ids = {}
        self.clauses = []

    def v(self, *key):
        if key not in self.ids:
            self.ids[key] = len(self.ids) + 1
        return self.ids[key]

    def fresh(self):
        return self.v("aux", len(self.ids))

    def add(self, clause):
        self.clauses.append(clause)


def at_least(P, lits, k):
    """Sequential counter: at least k of lits are true."""
    n = len(lits)
    if k <= 0:
        return
    neg = [-l for l in lits]          # at most n-k of the negations are true
    bound = n - k
    if bound < 0:
        P.add([])
        return
    if bound == 0:
        for l in lits:
            P.add([l])
        return
    s = [[P.fresh() for _ in range(bound)] for _ in range(n)]
    for i, x in enumerate(neg):
        P.add([-x, s[i][0]])
        if i > 0:
            for j in range(bound):
                P.add([-s[i - 1][j], s[i][j]])
            for j in range(1, bound):
                P.add([-x, -s[i - 1][j - 1], s[i][j]])
            P.add([-x, -s[i - 1][bound - 1]])
        else:
            for j in range(1, bound):
                P.add([-s[0][j]])


def build(m):
    P = Pool()
    w = m - 2
    W = range(w)
    M = range(m)
    # d(y, j) for y < j: y is dominated by j (natural labelling)
    for a, b, c in itertools.combinations(W, 3):
        P.add([-P.v("d", a, b), -P.v("d", b, c), P.v("d", a, c)])
    for F in "RS":
        for a in M:
            for y, j in itertools.combinations(W, 2):
                P.add([-P.v("d", y, j), -P.v(F, a, j), P.v(F, a, y)])
        # rows strictly increasing in the order read from point w-1 down to 0
        for a in range(m - 1):
            prev, lts = None, []
            for k in reversed(W):
                x, y = P.v(F, a, k), P.v(F, a + 1, k)
                lt, eq = P.v("lt", F, a, k), P.v("eq", F, a, k)
                lts.append(lt)
                P.add([-lt, -x]); P.add([-lt, y])
                if prev is not None:
                    P.add([-lt, prev]); P.add([-eq, prev])
                P.add([-eq, -x, y]); P.add([-eq, x, -y])
                prev = eq
            P.add(lts)
        # closure under intersection
        for a, b in itertools.combinations(M, 2):
            P.add([P.v("h", F, a, b, c) for c in M])
            for c in M:
                h = P.v("h", F, a, b, c)
                for y in W:
                    P.add([-h, -P.v(F, c, y), P.v(F, a, y)])
                    P.add([-h, -P.v(F, c, y), P.v(F, b, y)])
                    P.add([-h, -P.v(F, a, y), -P.v(F, b, y), P.v(F, c, y)])
    # R & S is empty or D(j)
    for a in M:
        for b in M:
            P.add([P.v("e", a, b, j) for j in W] + [P.v("e", a, b, "none")])
            for y in W:
                r, s = P.v("R", a, y), P.v("S", b, y)
                P.add([-P.v("e", a, b, "none"), -r, -s])
                for j in W:
                    e = P.v("e", a, b, j)
                    if y == j:
                        P.add([-e, r]); P.add([-e, s])
                    elif y > j:
                        P.add([-e, -r, -s])
                    else:
                        d = P.v("d", y, j)
                        P.add([-e, -r, -s, d]); P.add([-e, -d, r]); P.add([-e, -d, s])
    # frequency: r(y) + s(y) >= m - 1
    for y in W:
        at_least(P, [P.v("R", a, y) for a in M] + [P.v("S", a, y) for a in M], m - 1)
    return P


def main():
    m, out = int(sys.argv[1]), sys.argv[2]
    P = build(m)
    with open(out, "w") as f:
        f.write(f"p cnf {len(P.ids)} {len(P.clauses)}\n")
        for c in P.clauses:
            f.write(" ".join(map(str, c)) + " 0\n")


if __name__ == "__main__":
    main()
