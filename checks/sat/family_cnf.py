#!/usr/bin/env python3
"""CNF for a smallest counterexample, with the block sizes given explicitly.

A top t and a chosen element p split the members into blocks by membership of
t and p. On W = U - {t, p} (m-2 points, naturally labelled order: variable
d(y,j) for y < j means y is dominated by j) the members of P10, P01 and P00
give families R, S, T of down-sets (complements in W), of sizes nR, nS, nT.
The members containing t and p are U, the A_j (j in W) and, with "extra", one
further member B; E = W - B is then a down-set different from the empty set
and from every D(j).
Constraints (each a consequence of union-closure):
  - each family distinct (strict lex order) and closed under intersection;
  - R & T in R, S & T in S;
  - R & S, R & D(j), S & D(j), T & D(j), D(i) & D(j) and, with "extra",
    E & R, E & S, E & T, E & D(j) are empty, some D(k), or E;
  - a point in every member of R, or of S, lies in every member of T;
  - frequency: r(x) + s(x) + t(x) + d(x) [+ (x in E)] >= freq for x in W,
    d(x) = #{j in W: x <= j}.
Usage: family_cnf.py m nR nS nT freq out.cnf [extra] [nontriv]
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


def build(m, nR, nS, nT, freq, extra=False, nontriv=False):
    P = Pool()
    w = m - 2
    W = range(w)
    size = {"R": nR, "S": nS, "T": nT}

    def D(y, j):
        if y == j:
            return True
        if y > j:
            return False
        return P.v("d", y, j)

    def neg(l):
        if l is True:
            return False
        if l is False:
            return True
        return -l

    def clause(lits):
        out = []
        for l in lits:
            if l is True:
                return
            if l is False:
                continue
            out.append(l)
        P.add(out)

    for a, b, c in itertools.combinations(W, 3):
        P.add([-P.v("d", a, b), -P.v("d", b, c), P.v("d", a, c)])

    def mem(F, a, y):
        return P.v(F, a, y)

    def ext(y):
        return P.v("E", y)

    for F in "RST":
        for a in range(size[F]):
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
    if extra:
        for y, j in itertools.combinations(W, 2):
            P.add([-P.v("d", y, j), -ext(j), ext(y)])
        P.add([ext(y) for y in W])              # E is not empty
        for j in W:                             # E is not D(j)
            P.add([P.v("ne", j, y) for y in W])
            for y in W:
                n, e, dy = P.v("ne", j, y), ext(y), D(y, j)
                clause([-n, e, dy]); clause([-n, neg(e), neg(dy)])

    def inter_in_family(key, A, B, F):
        hs = [P.v("h", key, c) for c in range(size[F])]
        P.add(hs)
        for c, h in enumerate(hs):
            for y in W:
                a, b, z = A(y), B(y), mem(F, c, y)
                P.add([-h, -z, a]); P.add([-h, -z, b]); P.add([-h, -a, -b, z])

    def inter_principal(key, A, B):
        """A & B is empty, some D(j), or (with extra) E."""
        sel = [P.v("p", key, j) for j in W] + [P.v("p", key, "none")]
        if extra:
            sel.append(P.v("p", key, "E"))
        P.add(sel)
        for y in W:
            a, b = A(y), B(y)
            clause([-sel[w], neg(a), neg(b)])
            for j in W:
                s, dyj = sel[j], D(y, j)
                clause([-s, neg(a), neg(b), dyj])
                clause([-s, neg(dyj), a])
                clause([-s, neg(dyj), b])
            if extra:
                s, e = sel[w + 1], ext(y)
                clause([-s, neg(a), neg(b), e])
                clause([-s, -e, a])
                clause([-s, -e, b])

    def fam(F, a):
        return lambda y: mem(F, a, y)

    def prin(j):
        return lambda y: D(y, j)

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
            if extra:
                inter_principal(("FE", F, a), fam(F, a), ext)
    for i, j in itertools.combinations(W, 2):
        inter_principal(("DD", i, j), prin(i), prin(j))
    if extra:
        for j in W:
            inter_principal(("ED", j), ext, prin(j))

    for F in "RS":
        for y in W:
            allv = P.v("all", F, y)
            for a in range(size[F]):
                P.add([-allv, mem(F, a, y)])
            P.add([allv] + [-mem(F, a, y) for a in range(size[F])])
            for c in range(size["T"]):
                P.add([-allv, mem("T", c, y)])

    if nontriv:
        P.add([P.v("d", y, w - 1) for y in range(w - 1)])

    for y in W:
        lits = [mem(F, a, y) for F in "RST" for a in range(size[F])]
        lits += [l for l in (D(y, j) for j in W) if l is not True and l is not False]
        if extra:
            lits.append(ext(y))
        at_least(P, lits, freq - 1)   # y <= y counts once
    return P


def main():
    m, nR, nS, nT, freq = map(int, sys.argv[1:6])
    out = sys.argv[6]
    P = build(m, nR, nS, nT, freq, "extra" in sys.argv[7:], "nontriv" in sys.argv[7:])
    with open(out, "w") as f:
        f.write(f"p cnf {len(P.ids)} {len(P.clauses)}\n")
        for c in P.clauses:
            f.write(" ".join(map(str, c)) + " 0\n")


if __name__ == "__main__":
    main()
