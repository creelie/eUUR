#!/usr/bin/env python3
"""Write journal/ejc/main.tex, the paper in the format of The Electronic Journal of
Combinatorics, from paper/main.tex.

The body (from the introduction to the bibliography) is taken unchanged except for the
float placements that only REVTeX's two-column layout needs; the front matter follows the
journal's sample article (e-jc.sty, https://www.combinatorics.org/files/e-jc.sty).
Usage: python3 journal/ejc/make_ejc.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "paper" / "main.tex"
OUT = ROOT / "journal" / "ejc" / "main.tex"

FRONT = r"""\documentclass[12pt]{article}
\usepackage[amsmath]{e-jc}
\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{xurl}
\usepackage{orcidlink}
\usepackage[protrusion=true,expansion=false]{microtype}
\setcounter{tocdepth}{1}



\theoremstyle{plain}
\newtheorem{mainthm}{Theorem}
\renewcommand{\themainthm}{\Alph{mainthm}}

\newcommand{\EE}{\mathbb{E}}
\newcommand{\cF}{\mathcal{F}}
\newcommand{\cA}{\mathcal{A}}
\newcommand{\qs}{q^{*}}
\newcommand{\Cs}{C^{*}}
\newcommand{\codeDOI}{\href{https://github.com/creelie/eUUR}{\nolinkurl{github.com/creelie/eUUR}}}
\tolerance=2000
\emergencystretch=2em

\dateline{Oct 19, 2026}{TBD}{TBD}
\MSC{05D05, 94A17, 65G30, 68V15}
\Copyright{The authors. Released under the CC BY license (International 4.0).}

\title{Attaining the Entropy Limit\\ for Union-Closed Families}

\author{Deep Bhattacharjee\,\orcidlink{0000-0003-0466-750X}\authornote{1,2}
\and
Ushashi Bhattacharya\,\orcidlink{0009-0002-2254-3914}\authornote{3}}

\authortext{1}{Formerly, Electro-Gravitational Space Propulsion Laboratory (EGSPL), Bhubaneswar, Odisha 751030, India (\email{itsdeep@live.com}, \email{d.bhattacharjee@erl-forschung.de}); corresponding author.}
\authortext{2}{Formerly, University of Calcutta, Senate House, 87/1 College Street, Kolkata 700073, West Bengal, India.}
\authortext{3}{Formerly, National Taiwan University, Taipei 106319, Taiwan (\email{rai.bhattacharya.in@gmail.com}).}

\begin{document}

\maketitle

\begin{abstract}
%ABSTRACT%

\medskip\noindent\textbf{Keywords:} %KEYWORDS%
\end{abstract}

\tableofcontents

"""


def main() -> None:
    src = SRC.read_text()
    abstract = src.split("\\begin{abstract}", 1)[1].split("\\par\\medskip", 1)[0]
    abstract = abstract.replace("\\itshape", "").strip()
    keywords = src.split("\\keywords{", 1)[1].split("}", 1)[0]
    body = src[src.index("\\section{Introduction}"):]
    body = body.replace("\\begin{figure*}", "\\begin{figure}").replace("\\end{figure*}", "\\end{figure}")
    body = body.replace("\\begin{table}[t]", "\\begin{table}[htbp]").replace("\\begin{figure}[t]", "\\begin{figure}[htbp]")
    body = body.replace("width=\\columnwidth", "width=0.62\\textwidth")
    front = FRONT.replace("%ABSTRACT%", abstract).replace("%KEYWORDS%", keywords.replace(";", ";"))
    OUT.write_text(front + body)


if __name__ == "__main__":
    main()
