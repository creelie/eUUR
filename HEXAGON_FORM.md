# Hexagon submission fields

Title: Attaining the Entropy Limit for Union-Closed Families

Abstract: We prove that every finite union-closed family with a nonempty member has an element that lies in at least 0.38288525996... of its members. This number is the exact limit of the entropy method in the form developed by Liu and Jiang, and earlier work had come within a hundred-millionth of it without reaching it. The proof chooses the auxiliary function so that the two inequalities behind the method touch zero at a single point, and shows by a convexity argument that they stay nonnegative around it. With a global coupling of Jiang, the bound is strict for every family.

Primary subject: math.CO (Combinatorics)
Cross-list subjects: cs.IT (Information Theory), math.PR (Probability), math.NA (Numerical Analysis)
Tags: union-closed sets conjecture, Frankl's conjecture, entropy method, interval arithmetic
MSC2020: 05D05 Extremal set theory; 94A17 Measures of information, entropy; 65G30 Interval and finite arithmetic

Contributor 1 (submitting): Deep Bhattacharjee; ORCID 0000-0003-0466-750X; affiliation: Formerly, Electro-Gravitational Space Propulsion Laboratory (EGSPL), Bhubaneswar, Odisha 751030, India; formerly, University of Calcutta, Senate House, 87/1 College Street, Kolkata 700073, West Bengal, India; itsdeep@live.com (second address d.bhattacharjee@erl-forschung.de)
Contributor 2: Ushashi Bhattacharya; ORCID 0009-0002-2254-3914; affiliation: Formerly, National Taiwan University, Taipei 106319, Taiwan; rai.bhattacharya.in@gmail.com

Text of the contribution: A mix of human-written and AI-generated.
Human understanding: "All parts" only after both authors have read every proof; otherwise "Some parts, but not all".

Provenance statement: The proofs, the text, the figures and the Python, C, C++, Julia, Lean and shell programs were carried out by Deep Bhattacharjee with AI assistance (Claude, Anthropic) in the Claude Code environment. The entropy reduction and the covering of the unit square follow Jiang (arXiv:2609.08291), and the interval program is adapted from Jiang's Appendix B (CC BY 4.0); the paper credits them. The new step is the construction at the exact limit, with both gaps and their gradients vanishing at (q*, q*), and the ball-arithmetic certificate that the Hessians are positive definite on a square around that point. The limit C* itself and the fact that it bounds the method are due to Jiang and to Moffat; the paper proves that it is attained. Frankl's conjecture (the constant 1/2) is not proved. Both authors approved the final version.

Tools used: Anthropic - Claude (Claude Code); Python with python-flint (Arb ball arithmetic); C; C++; Julia; Lean 4 (v4.34.1); shell.
arXiv identifier: none (not posted on arXiv).

Source files or ZIP: UnionClosedLimit_final2-tex.zip (the folder UnionClosedLimit_final2-tex/ with main.tex and figures/ as PNG; compiles with pdflatex in two passes, no BibTeX pass). Do not upload the master zip here.
AI provenance files: AI_PROVENANCE_UnionClosedLimit.md
License: CC BY 4.0

Data availability (in the paper): the programs, the LaTeX source and the figure programs are in https://github.com/creelie/eUUR and its Zenodo archive (release v1.0.0).
AI disclosure (in the paper, Data and code availability): Deep Bhattacharjee carried out the computations and the Python, C, C++, Julia, Lean and shell verifications with AI assistance (Claude, Anthropic). No separate AI declaration.
Funding: none. Competing interests: none.
