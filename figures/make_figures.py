"""Draw the figures of the paper as opaque 256-colour PNG files about 1600 px wide.

Usage: python3 figures/make_figures.py   (writes paper/figures/*.png)
Requires numpy, matplotlib and Pillow.
"""
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "paper", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 11})

LN2 = np.log(2.0)
A, B, Z = 0.716, 0.721, 181 / 256


def h(x):
    x = np.clip(np.asarray(x, dtype=float), 1e-300, 1 - 1e-16)
    return -(x * np.log(x) + (1 - x) * np.log1p(-x))


q = 0.69
for _ in range(60):
    q -= -((1 - q) * np.log(1 - q) + q * np.log(1 + q)) / (np.log((1 - q) / (1 + q)) + 1 / (1 + q))
QS = q
HS = h(QS)
KS = np.log((1 - QS) / QS) / (2 * HS)
MW4 = (QS * h(QS) - h(QS * QS) / 2) / LN2
CSTAR = 0.5 - MW4


def D(x):
    return np.where(x <= 0.5, h(x), np.where(x <= Z, LN2, LN2 * h(x * x) / h(Z * Z)))


def phi(x):
    d = x - QS
    return np.sqrt(D(x) * h(x) / HS) * np.exp(-KS * d - 0.7 * d * d)


def psi(x):
    t = np.clip((x - A) / (B - A), 0, 1)
    return np.where(x <= A, phi(x), np.where(x >= B, np.sqrt(h(x * x)), (1 - t) * phi(x) + t * np.sqrt(h(x * x))))


def acoef(x):
    with np.errstate(invalid="ignore", divide="ignore"):
        mid = np.sqrt(np.clip((1 - 2 * x * x) / (2 * x * (1 - x)), 0, None))
    return np.where(x <= 0.5, 1.0, np.where(2 * x * x >= 1, 0.0, mid))


def Kgap(x, y):
    r = x * y + acoef(x) * acoef(y) * (np.minimum(x, y) - x * y)
    return h(r) - psi(x) * psi(y)


def Mgap(x, y):
    return h(x * y) + 2 * MW4 * psi(x) * psi(y) - x * h(y) - y * h(x)


def save(fig, name):
    buf = io.BytesIO()
    fig.savefig(buf, dpi=200, facecolor="white")
    plt.close(fig)
    buf.seek(0)
    im = Image.open(buf).convert("RGB")
    w = 1600
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im = im.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.NONE)
    im.save(os.path.join(OUT, name), optimize=True)
    print("wrote", name, im.size)


def style3d(ax):
    ax.xaxis.pane.set_facecolor((0.97, 0.97, 0.97))
    ax.yaxis.pane.set_facecolor((0.97, 0.97, 0.97))
    ax.zaxis.pane.set_facecolor((0.97, 0.97, 0.97))


# Figure 1: the two gaps over the unit square.
def fig_gaps():
    n = 181
    xs = np.linspace(0.002, 0.998, n)
    X, Y = np.meshgrid(xs, xs)
    fig = plt.figure(figsize=(8, 3.9))
    for k, (F, title, cm) in enumerate([(Kgap, r"(K): $h(r(x,y))-\psi(x)\psi(y)$", "viridis"),
                                        (Mgap, r"(M): $2m[w_0h(xy)+w_4\psi\psi]-xh(y)-yh(x)$", "plasma")]):
        ax = fig.add_subplot(1, 2, k + 1, projection="3d")
        Zv = F(X, Y)
        ax.plot_surface(X, Y, Zv, cmap=cm, linewidth=0, antialiased=True, rstride=2, cstride=2, alpha=0.95)
        ax.plot([QS, QS], [QS, QS], [0, Zv.max() * 1.15], color="red", lw=1.5, zorder=10)
        ax.text(QS, QS, Zv.max() * 1.2, r"$(q^*,q^*)$", color="red", fontsize=10, zorder=11)
        ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
        ax.set_title(title, fontsize=10)
        ax.view_init(elev=24, azim=-128)
        style3d(ax)
    fig.tight_layout()
    save(fig, "fig_gaps.png")


# Figure 2: the tangency at (q*, q*).
def fig_tangency():
    R = 0.03
    xs = np.linspace(QS - R, QS + R, 121)
    X, Y = np.meshgrid(xs, xs)
    fig = plt.figure(figsize=(8, 3.9))
    for k, (F, title, cm) in enumerate([(Kgap, "(K) near the tangency point", "viridis"),
                                        (Mgap, "(M) near the tangency point", "plasma")]):
        ax = fig.add_subplot(1, 2, k + 1, projection="3d")
        Zv = F(X, Y)
        ax.plot_surface(X - QS, Y - QS, Zv, cmap=cm, linewidth=0, antialiased=True, alpha=0.9)
        r = 0.008
        sq = np.array([[-r, -r], [r, -r], [r, r], [-r, r], [-r, -r]])
        ax.plot(sq[:, 0], sq[:, 1], 0 * sq[:, 0], color="black", lw=1.4)
        ax.plot_surface(np.array([[-R, R], [-R, R]]), np.array([[-R, -R], [R, R]]), np.zeros((2, 2)),
                        color="grey", alpha=0.18)
        ax.scatter([0], [0], [0], color="red", s=30, depthshade=False)
        ax.set_xlabel("$x-q^*$"); ax.set_ylabel("$y-q^*$")
        ax.set_title(title, fontsize=10)
        ax.view_init(elev=18, azim=-60)
        ax.tick_params(labelsize=7)
        style3d(ax)
    fig.tight_layout()
    save(fig, "fig_tangency.png")


# Figure 3: a 3D schematic of the proof: how each domain is covered.
def fig_scheme():
    fig = plt.figure(figsize=(8, 4.3))
    def slab(ax, x0, x1, y0, y1, dz, color):
        ax.bar3d(x0, y0, 0, x1 - x0, y1 - y0, dz, color=color, shade=True, edgecolor="k", linewidth=0.3)
    panels = [
        ("(K) on $[0,1]^2$", [((0, 1 / 16, 0, 1), 0.10, "#6baed6"), ((15 / 16, 1, 0, 1), 0.10, "#6baed6"),
                              ((1 / 16, 15 / 16, 0, 1), 0.04, "#fdd0a2"),
                              ((QS - 0.035, QS + 0.035, QS - 0.035, QS + 0.035), 0.45, "#e31a1c")],
         "$x$", "$y$"),
        ("(M) in the coordinates $(t,\\xi)$", [((0, 0.06, 0, 1), 0.10, "#74c476"), ((0.94, 1, 0, 1), 0.10, "#74c476"),
                              ((0.06, 0.94, 0.93, 1), 0.16, "#fd8d3c"),
                              ((0.06, 0.94, 0, 0.93), 0.04, "#fdd0a2"),
                              ((0.34, 0.40, 0, 0.07), 0.45, "#e31a1c")],
         "$t$ (log scale)", "$\\xi$"),
    ]
    for k, (title, slabs, xl, yl) in enumerate(panels):
        ax = fig.add_subplot(1, 2, k + 1, projection="3d")
        for (x0, x1, y0, y1), dz, c in slabs:
            slab(ax, x0, x1, y0, y1, dz, c)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_zlim(0, 0.6)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        ax.set_xlabel(xl, labelpad=-8); ax.set_ylabel(yl, labelpad=-8)
        ax.set_title(title, fontsize=11)
        ax.view_init(elev=30, azim=-60)
        style3d(ax)
    from matplotlib.patches import Patch
    handles = [Patch(color="#6baed6", label="strips: analytic bounds"),
               Patch(color="#74c476", label="small and large $t$: analytic bounds"),
               Patch(color="#fd8d3c", label="edge $\\xi\\to1$: analytic edge bounds"),
               Patch(color="#fdd0a2", label="compact part: interval boxes"),
               Patch(color="#e31a1c", label="tangency square: convexity")]
    fig.legend(handles=handles, loc="lower center", ncol=3, fontsize=8.5, frameon=False)
    fig.subplots_adjust(left=0.0, right=1.0, top=0.92, bottom=0.14, wspace=0.0)
    save(fig, "fig_scheme.png")


# Figure 4: the certified constants, as distances below C*.
def fig_records():
    data = [("Liu", 0.3823455), ("Liu threshold", 0.382709087918735), ("Moffat", 0.38284),
            ("Costa-Sadhu", 0.3828852549667978), ("Jiang", 1531541 / 4000000)]
    fig = plt.figure(figsize=(5.2, 5.6))
    ax = fig.add_axes([0.0, 0.30, 1.0, 0.74], projection="3d")
    for i, (name, c) in enumerate(data):
        hgt = -np.log10(CSTAR - c)
        ax.bar3d(1.6 * i, 0, 0, 0.8, 0.8, hgt, color=plt.cm.Blues(0.35 + 0.12 * i), shade=True,
                 edgecolor="k", linewidth=0.3)
    ax.set_xticks([]); ax.set_yticks([])
    ax.tick_params(axis="z", labelsize=11)
    ax.set_zlabel(r"$-\log_{10}(C^*-c)$", fontsize=12)
    ax.view_init(elev=18, azim=-62)
    style3d(ax)
    fig.canvas.draw()
    from mpl_toolkits.mplot3d import proj3d
    for i, (name, c) in enumerate(data):
        hgt = -np.log10(CSTAR - c)
        px, py, _ = proj3d.proj_transform(1.6 * i + 0.4, 0.0, hgt, ax.get_proj())
        ax.annotate(str(i + 1), (px, py), xytext=(0, 6), textcoords="offset points", fontsize=14,
                    ha="center", va="bottom", fontweight="bold", zorder=10,
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))
    lines = []
    for i, (name, c) in enumerate(data):
        lines.append(f"{i + 1}. {name}: {c:.10f}, gap {CSTAR - c:.1e}")
    lines += [r"This paper: $c = C^* = 0.3828852599\ldots$, gap $0$"]
    fig.text(0.06, 0.18, "\n".join(lines), fontsize=12, va="center", ha="left", linespacing=1.5)
    save(fig, "fig_records.png")


if __name__ == "__main__":
    print("q* =", QS, "C* =", CSTAR)
    fig_gaps(); fig_tangency(); fig_scheme(); fig_records()
