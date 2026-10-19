# Target journal: The Electronic Journal of Combinatorics

| Item | Details |
|---|---|
| Journal | The Electronic Journal of Combinatorics (EJC) |
| Publisher | the journal itself (diamond open access, no fees) |
| ISSN | 1077-8926 |
| Submission | https://www.combinatorics.org/ojs/index.php/eljc/about/submissions |
| Preprints | the journal accepts papers posted as preprints |
| Class file | the paper uses REVTeX 4.2 for review; accepted papers are typeset in the journal's class |

## Scope fit

EJC publishes research in all areas of combinatorics, and the entropy line of
work on the union-closed sets conjecture has a paper there: R. Alweiss,
B. Huang and M. Sellke, *Improved lower bound for Frankl's union-closed sets
conjecture*, EJC 31(3) (2024), P3.35. The paper proves the constant
0.38288525996..., the exact limit of the method in the form of Liu and Jiang.

MSC 2020: primary 05D05; secondary 94A17, 65G30.

## Length and format

- 10 pages, two columns, four 3D figures and three tables; built with no
  overfull or underfull boxes and no undefined references.
- A short italic abstract with no formulas, four keywords, MSC codes and a
  short table of contents.
- Two authors: Deep Bhattacharjee (corresponding author) and Ushashi
  Bhattacharya, with addresses, e-mail addresses and ORCID iDs.
- One file `main.tex` with the references inline, so no `.bib` or `.bbl`
  file is needed. `dist/UnionClosedLimit_final2-tex.zip` and the arXiv
  tarball contain this file and the figures as PNG.
- Declarations at the end: "Data and code availability" (the repository and
  its Zenodo archive, and the statement on AI assistance from Claude,
  Anthropic), "Ethical declarations" (funding none, competing interests
  none) and "Author contributions". Appendices A to F give every derivation.

## Before submitting

- Reread the journal's current instructions on AI assistance; the paper
  states the use of Claude in the data availability section, and
  `AI_PROVENANCE_UnionClosedLimit.md` gives the details.
- The computer-assisted parts are the two Python programs in
  `checks/python/`; cite the Zenodo DOI of the release so that referees can
  run them.
