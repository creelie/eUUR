# Target journal: The Electronic Journal of Combinatorics

| Item | Details |
|---|---|
| Journal | The Electronic Journal of Combinatorics (EJC) |
| Publisher | the journal itself (diamond open access, no fees) |
| ISSN | 1077-8926 |
| Submission | https://www.combinatorics.org/ojs/index.php/eljc/about/submissions |
| Preprints | the journal accepts papers posted as preprints |
| Format | the journal's style file `e-jc.sty` with its sample article's front matter; `journal/ejc/` |

## Scope fit

EJC publishes research in all areas of combinatorics, and the entropy line of
work on the union-closed sets conjecture has a paper there: R. Alweiss,
B. Huang and M. Sellke, *Improved lower bound for Frankl's union-closed sets
conjecture*, EJC 31(3) (2024), P3.35. The paper proves the constant
0.38288525996..., the exact limit of the method in the form of Liu and Jiang,
and the conjecture itself for every family of at most 52 members.

MSC 2020: primary 05D05; secondary 94A17, 65G30, 68V15.

## Length and format

- `journal/ejc/build.sh` writes `journal/ejc/main.tex` from `paper/main.tex`
  with the journal's front matter (`\dateline`, `\MSC`, `\Copyright`,
  `\authornote` and `\authortext`; no `\thanks`) and builds
  `dist/UnionClosedLimit_EJC.pdf` (25 pages, one column, 12 pt) and
  `dist/UnionClosedLimit_EJC-tex.zip` (`main.tex`, `e-jc.sty`, the figures
  as PNG), with no overfull or underfull boxes and no undefined references.
- Licence line: CC BY 4.0, the journal's recommendation.
- Abstract with no formulas, four keywords, MSC 2020 05D05, 94A17, 65G30,
  68V15, and a short table of contents.
- Two authors: Deep Bhattacharjee (corresponding author) and Ushashi
  Bhattacharya, with addresses, e-mail addresses and ORCID iDs.
- References inline, so no `.bib` or `.bbl` file is needed.
- Declarations at the end: "Data and code availability" (the repository and
  its Zenodo archive, and the statement on AI assistance from Claude,
  Anthropic), "Ethical declarations" (funding none, competing interests
  none) and "Author contributions". Appendices A to G give every derivation.

## Before submitting

- Reread the journal's current instructions on AI assistance; the paper
  states the use of Claude in the data availability section, and
  `AI_PROVENANCE_UnionClosedLimit.md` gives the details.
- The computer-assisted parts are the two Python programs in
  `checks/python/` and the satisfiability check in `checks/sat/`; cite the Zenodo DOI of the release so that referees can
  run them.
