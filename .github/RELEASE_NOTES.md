**Attaining the entropy limit for union-closed families**, by Deep Bhattacharjee (corresponding author) and Ushashi Bhattacharya.

Frankl's union-closed sets conjecture states that every finite union-closed family with a nonempty member has an element in at least half of its members. The entropy method of Gilmer, refined by Liu and by Jiang (arXiv:2609.08291), reduces the frequency bound to two inequalities (K) and (M) on the unit square, and no choice of the functions in them gives a constant above

C* = 1/2 − (1 − q*) ln(1 + q*) / (2 ln 2) = 0.38288525996679779…,

where q* = 0.69090773872540775… is the root in (0, 1) of (1 − q) ln(1 − q) + q ln(1 + q) = 0. The best constants proved before were 0.38288525 (Jiang) and 0.3828852549667978 (Costa and Sadhu, arXiv:2610.02295), and Moffat showed that C* bounds every single-letter certificate of this kind.

**Theorem A.** Every finite union-closed family containing a nonempty set has an element lying in at least a fraction C* of its members.

**Theorem B.** If the family has N ≥ 2 members, it has an element in at least a fraction C* + ln²(2N − 1)/(128 N² ln² N) of them.

**Theorem C.** Every union-closed family with at most 52 members that contains a nonempty set has an element in at least half of its members (known before: at most 50).

| Step | Content |
|---|---|
| Section 3 | the construction with every parameter at its limiting value: centre q*, scale 1, m·w₀ = 1/2 |
| Proposition IV.1 | the gaps of (K) and (M) and their gradients vanish at (q*, q*) |
| Proposition IV.2 | the Hessians are positive definite on the square S of radius 0.008 around (q*, q*), certified in ball arithmetic on 1600 subsquares; hence both gaps are nonnegative on S |
| Section 5, Appendix D | the rest of the unit square: analytic strips and edges, and an interval covering (bridge 39 boxes, kernel 1572, mixture 8193) |
| Appendix F | the strict bound from Jiang's global coupling |
| Section 8, Appendix G | Theorem C: a smallest counterexample with 51 members on 13 elements gives two families of down-sets on 11 points (Lemma VIII.2, by hand); with no domination they are impossible for every m (Proposition VIII.3, by hand); with any order they are refuted by CaDiCaL for m = 3, …, 13, every DRAT proof checked by drat-trim (Theorem VIII.4) |

Checks: `checks/python/tangency.py` (Hessian certificate on S) and `checks/python/verify_exact.py` (interval certificate on the rest, adapted from the program of Jiang's Appendix B) are the proof; C, C++ and Julia programs cross-check q*, C*, the Hessians and the sign of the two gaps on fine grids; Lean 4 checks the rational breakpoints with no axioms. `checks/sat/run_sat.sh` repeats the computer part of Theorem C.

Files:
- `UnionClosedLimit_final2.pdf`: the paper
- `UnionClosedLimit_final2-tex.zip`: LaTeX source (`main.tex`, figures as PNG)
- `UnionClosedLimit_final2-arxiv.tar.gz`: the same source, ready for arXiv

The repository also holds `preprintUnionClosedLimit/UnionClosedLimit.pdf` and `MasterUnionClosedLimit_masterzipfinal2.zip`, which holds every file of the repository. Run `scripts/run_all.sh` to repeat the checks and `scripts/build_paper.sh` to rebuild the files above.
