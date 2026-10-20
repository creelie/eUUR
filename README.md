# Attaining the entropy limit for union-closed families

Deep Bhattacharjee (corresponding author, ORCID 0000-0003-0466-750X) and Ushashi Bhattacharya (ORCID 0009-0002-2254-3914).

**Theorem A.** Every finite union-closed family containing a nonempty set has an element lying in at least a fraction

C* = 1/2 − (1 − q*) ln(1 + q*) / (2 ln 2) = 0.38288525996679779…

of its members, where q* = 0.69090773872540775… is the root in (0, 1) of (1 − q) ln(1 − q) + q ln(1 + q) = 0.

**Theorem B.** A union-closed family of N ≥ 2 sets containing a nonempty set has an element in at least a fraction C* + ln²(2N − 1)/(128 N² ln² N) of its members.

**Theorem C.** Every union-closed family with at most 54 members that contains a nonempty set has an element lying in at least half of its members. (Known before: at most 50 members.)

C* is the exact limit of the entropy method in the form of Liu and Jiang: no choice of the functions in the two inequalities (K) and (M) gives more. The best constants proved before were 0.38288525 (Y. Jiang, arXiv:2609.08291) and 0.3828852549667978 (S. Costa and A. Sadhu, arXiv:2610.02295). The paper reaches C* by placing the centre of Jiang's profile exactly at q* and every weight at its limiting value, so that both gaps and their gradients vanish at (q*, q*), and proves that the Hessians are positive definite on a square around that point.

Theorem C reduces a smallest counterexample with 51 members on 13 elements to two families of down-sets of an unknown partial order on 11 points with four constraints proved by hand (Lemma VIII.2 of the paper), and refutes them with CaDiCaL; every proof is checked by drat-trim. Without the computer, the same reduction shows that in a smallest counterexample with 4m − 1 members on m elements some element is dominated by another, for every m.

Frankl's conjecture itself (the constant 1/2) remains open.

Archive: release v1.1.0, [doi:10.5281/zenodo.23484214](https://doi.org/10.5281/zenodo.23484214) (Theorems A, B, C); release v1.0.0, [doi:10.5281/zenodo.23480219](https://doi.org/10.5281/zenodo.23480219) (Theorems A, B); all versions [doi:10.5281/zenodo.23480218](https://doi.org/10.5281/zenodo.23480218).

## Layout

| Path | Content |
|---|---|
| `paper/` | LaTeX source (REVTeX 4.2, single `main.tex`, bibliography inline) and the figures as PNG |
| `preprintUnionClosedLimit/` | the paper as a PDF |
| `dist/` | the PDF, the LaTeX source zip and the arXiv tarball, and the version for The Electronic Journal of Combinatorics (`UnionClosedLimit_EJC.pdf`, `UnionClosedLimit_EJC-tex.zip`) |
| `journal/ejc/` | the journal's style file `e-jc.sty`, `make_ejc.py`, which writes the journal version of `paper/main.tex`, and `build.sh`, which builds it |
| `checks/python/tangency.py` | ball-arithmetic certificate (python-flint, 200 bits) that the Hessians of the three gap functions are positive definite on S = [q* − 0.008, q* + 0.008]², and that the values and gradients vanish at (q*, q*) |
| `checks/python/verify_exact.py` | interval certificate of (K), (M) and the scalar inequalities on the rest of the unit square, adapted from the program of Appendix B of Jiang's paper |
| `checks/c`, `checks/cpp`, `checks/julia` | cross-checks of q*, C*, the closed-form Hessians and the sign of the gaps on fine grids |
| `checks/sat/boundary_cnf.py` | writes the CNF of the boundary configuration of Theorem C for a given m |
| `checks/sat/run_sat.sh` | solves it with CaDiCaL for m = 3, …, 13 and checks each DRAT proof with drat-trim |
| `checks/sat/results.txt` | sizes of the formulas and solving times (m, variables, clauses, seconds) |
| `lean/` | Lean 4 (core, no Mathlib): the order relations of the rational breakpoints, checked by the kernel with no axioms |
| `figures/make_figures.py` | the five figures |
| `scripts/run_all.sh` | Lean build and axiom check, then every check |
| `scripts/build_paper.sh` | the paper, `dist/`, the preprint folder and the master zip |

## Running the checks

```
python3 -m pip install -r checks/python/requirements.txt
scripts/run_all.sh                 # needs elan, python3, julia, cc and c++
CHECKS=python SKIP_LEAN=1 scripts/run_all.sh   # the proof programs only (about ninety seconds)
CHECKS=sat SKIP_LEAN=1 scripts/run_all.sh      # Theorem C for m = 3..11 (about two minutes; needs cadical, drat-trim)
checks/sat/run_sat.sh 12 13                    # the two largest cases (about 20 minutes to solve, longer to check)
```

## Licence

MIT. The program `checks/python/verify_exact.py` is adapted from the verification program published in Appendix B of Y. Jiang, arXiv:2609.08291, which is distributed under CC BY 4.0; the changes are the parameters at the limit and the convexity acceptance of the square S.
