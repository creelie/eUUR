# AI provenance: Attaining the entropy limit for union-closed families

Authors: Deep Bhattacharjee (corresponding author, ORCID 0000-0003-0466-750X)
and Ushashi Bhattacharya (ORCID 0009-0002-2254-3914).

- Paper: https://github.com/creelie/eUUR/blob/main/preprintUnionClosedLimit/UnionClosedLimit.pdf
- Repository: https://github.com/creelie/eUUR
- Archive: release v1.0.0, doi:10.5281/zenodo.23480219; release v1.1.0, doi:10.5281/zenodo.23484214, adds Theorem C; release v1.2.0, doi:10.5281/zenodo.23645624, extends it to 54 members (all versions doi:10.5281/zenodo.23480218)

## Result

Frankl's union-closed sets conjecture asks for an element in at least half of
the members of every finite union-closed family with a nonempty member. The
entropy method of Gilmer, refined by Liu and by Jiang, reduces the frequency
bound to two inequalities on the unit square, and no choice of the functions
in them gives a constant above C* = 0.38288525996679779... The paper proves
that the constant C* itself holds for every family, and, with Jiang's global
coupling, a strictly larger bound depending on the number of members. The best
constants proved before were 0.38288525 (Jiang) and 0.3828852549667978 (Costa
and Sadhu).

The paper also proves the conjecture itself for every family of at most 54
members (known before: 50). A smallest counterexample with at most 54 members
would have 51 or 53 members on 13 elements; Appendix G reduces each case by
hand to families of down-sets of an unknown order on 11 points, and the
satisfiability solver CaDiCaL refutes both configurations, with every DRAT
proof checked by drat-trim (checks/sat/run_sat.sh) and every LRAT proof checked
by lrat-check while it is written (checks/sat/run_sat53.sh, run on GitHub
Actions by .github/workflows/sat53.yml). The reduction, the encoding, the hand proofs and the
checks were made with AI assistance (Claude, Anthropic) in Claude Code.

## Who did what

Deep Bhattacharjee chose the problem, directed the work, set the format and
the target journal, and ran the computations. Claude (Anthropic), used
through Claude Code under Deep Bhattacharjee's direction, produced the
following:

- the choice of the parameters at the limit and the tangency and convexity
  argument of Section 4;
- the ball-arithmetic Hessian certificate and the adaptation of Jiang's
  interval program;
- the cross-checks in C, C++ and Julia and the Lean check of the breakpoints;
- the figures;
- the LaTeX text of the paper.

The BLLM engine Anaxia (release v3.0.5, doi:10.5281/zenodo.23469389; github.com/creelie/eBLLM) supplied the status check, from its indexes of DeepMind's formal-conjectures collection and of the OpenRefute archive, and the record of the routes tried beyond C*, among them Roos's conjecture, which implies Frankl's conjecture. The paper says so in a footnote of Section VII, in the data availability section and in its bibliography. The construction, the proofs and the certificates were not produced by the engine. No other AI system took part. The reduction, the profile shape and the
covering of the unit square are Jiang's, and the paper credits them.

## How the result is checked

- **Ball arithmetic (python-flint, 200 bits).** `checks/python/tangency.py`
  shows that the value and gradient of the three gap functions vanish at
  (q*, q*) and that their Hessians are positive definite on every one of the
  1600 subsquares of S = [q* − 0.008, q* + 0.008]².
- **Interval arithmetic (35 digits, outward rounding).**
  `checks/python/verify_exact.py` covers the rest of the unit square and
  certifies the eleven scalar inequalities of the analytic estimates.
- **Cross-checks.** C (double precision on a 1601 × 1601 grid), C++ (long
  double, Hessians by central differences) and Julia (256-bit Newton for q*
  and C*).
- **Lean 4.** The order relations of the rational breakpoints, checked by the
  kernel with no axioms.

## What is not claimed

The paper does not prove Frankl's conjecture. It shows that the entropy method
in the form of Liu and Jiang reaches its own limit C*; going further needs a
different inequality. The limit C* and the fact that it bounds the method are
due to Jiang and to Moffat. The authors checked on 19 October 2026, on arXiv,
the openai/math release, OpenRefute, Zenodo and GitHub, that no earlier work
proves the constant C* itself.

## Text and references

The bibliography contains, besides the works on the union-closed sets
conjecture that the paper builds on, three self-citations of the authors.
Every entry was checked against its DOI record or the arXiv listing, and none
comes from TechRxiv, Qeios, Authorea or EasyChair.
