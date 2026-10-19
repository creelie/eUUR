#!/usr/bin/env python3
"""CNF for a smallest counterexample with 4m-1+2e members (e = 0 boundary, e = 1: n = 2m).

Points: W = {0..w-1}, w = m-2, naturally labelled order d(y,j) (y<j means y dominated by j).
Families of complements in W (all down-sets):
  R from P10 (m+e members), S from P01 (m+e), T from P00 (m members).
Constraints (all consequences of union-closure):
  - each family distinct (strict lex order), closed under intersection;
  - R & T in R, S & T in S;
  - R & S, R & D(j), S & D(j), T & D(j), D(i) & D(j): empty or some D(k);
  - frequency: r(x)+s(x)+t(x)+d(x) >= 2m-1+2e, d(x) = #{j in W: x <= j}.
Usage: above_cnf.py m e out.cnf [capdelta]
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

    def add(self, c):
        self.clauses.append(c)


def at_least(P, lits, k):
    n = len(lits)
    if k <= 0:
        return
    neg = [-l for l in lits]
    bound = n - k
    if bound < 0:
        P.add([]); return
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


def build(m, e, capdelta=0, nontriv=False):
    P = Pool()
    w = m - 2
    W = range(w)
    size = {"R": m + e, "S": m + e, "T": m}

    def D(y, j):  # literal "y <= j", or True/False
        if y == j:
            return True
        if y > j:
            return False
        return P.v("d", y, j)

    for a, b, c in itertools.combinations(W, 3):
        P.add([-P.v("d", a, b), -P.v("d", b, c), P.v("d", a, c)])

    def mem(F, a, y):
        return P.v(F, a, y)

    for F in "RST":
        M = range(size[F])
        for a in M:
            for y, j in itertools.combinations(W, 2):
                P.add([-P.v("d", y, j), -mem(F, a, j), mem(F, a, y)])
        for a in range(size[F] - 1):
            prev, lts = None, []
            for k in reversed(W):
                x, y = mem(F, a, k), mem(F, a + 1, k)
                lt, eq = P.v("lt", F, a, k), P.v("eq", F, a, k)
                lts.append(lt)
                P.add([-lt, -x]); P.add([-lt, y])
                if prev is not None:
                    P.add([-lt, prev]); P.add([-eq, prev])
                P.add([-eq, -x, y]); P.add([-eq, x, -y])
                prev = eq
            P.add(lts)

    def inter_in_family(key, A, B, F):
        """set A & set B equals some member of family F. A, B: functions y -> literal."""
        hs = [P.v("h", key, c) for c in range(size[F])]
        P.add(hs)
        for c, h in enumerate(hs):
            for y in W:
                a, b, z = A(y), B(y), mem(F, c, y)
                P.add([-h, -z, a]); P.add([-h, -z, b]); P.add([-h, -a, -b, z])

    def lit_clause(lits):
        """Add clause; literals may be True/False."""
        out = []
        for l in lits:
            if l is True:
                return
            if l is False:
                continue
            out.append(l)
        P.add(out)

    def inter_principal(key, A, B):
        """A & B empty or D(j) for some j."""
        sel = [P.v("p", key, j) for j in W] + [P.v("p", key, "none")]
        P.add(sel)
        for y in W:
            a, b = A(y), B(y)
            lit_clause([-sel[-1], neg(a), neg(b)])
            for j in W:
                s = sel[j]
                dyj = D(y, j)
                # s -> (y in A&B <-> y <= j)
                lit_clause([-s, neg(a), neg(b), dyj])
                lit_clause([-s, neg(dyj), a])
                lit_clause([-s, neg(dyj), b])

    def neg(l):
        if l is True:
            return False
        if l is False:
            return True
        return -l

    def fam(F, a):
        return lambda y: mem(F, a, y)

    def prin(j):
        return lambda y: D(y, j)

    # intersection closure
    for F in "RST":
        for a, b in itertools.combinations(range(size[F]), 2):
            inter_in_family(("cl", F, a, b), fam(F, a), fam(F, b), F)
    for F in "RS":
        for a in range(size[F]):
            for c in range(size["T"]):
                inter_in_family(("T", F, a, c), fam(F, a), fam("T", c), F)
    for a in range(size["R"]):
        for b in range(size["S"]):
            inter_principal(("RS", a, b), fam("R", a), fam("S", b))
    for F in "RST":
        for a in range(size[F]):
            for j in W:
                inter_principal(("FD", F, a, j), fam(F, a), prin(j))
    for i, j in itertools.combinations(W, 2):
        inter_principal(("DD", i, j), prin(i), prin(j))


    # a point in every R (dominated by p) or every S (dominated by t) avoids every P00 member
    for F in "RS":
        for y in W:
            allv = P.v("all", F, y)
            for a in range(size[F]):
                P.add([-allv, mem(F, a, y)])
            P.add([allv] + [-mem(F, a, y) for a in range(size[F])])
            for c in range(size["T"]):
                P.add([-allv, mem("T", c, y)])

    # nontrivial order (the trivial one is excluded by hand); label a maximal
    # element that dominates something last
    if nontriv:
        P.add([P.v("d", y, w - 1) for y in range(w - 1)])
    # frequency
    for y in W:
        lits = [mem(F, a, y) for F in "RST" for a in range(size[F])]
        lits += [l for l in (D(y, j) for j in W) if l is not True and l is not False]
        const = 1  # y <= y
        at_least(P, lits, 2 * m - 1 + 2 * e - const - capdelta)
    return P


def main():
    m, e, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    cd = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    nt = 'nontriv' in sys.argv[5:]
    P = build(m, e, cd, nt)
    with open(out, "w") as f:
        f.write(f"p cnf {len(P.ids)} {len(P.clauses)}\n")
        for c in P.clauses:
            f.write(" ".join(map(str, c)) + " 0\n")


if __name__ == "__main__":
    main()
