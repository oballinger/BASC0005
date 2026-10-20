"""Three figures for the W03 centrality slides: one made-up network, coloured and sized by
degree, betweenness and eigenvector centrality in turn. Each measure crowns a different node.

    uv run -p 3.12 --with networkx --with matplotlib python lectures/tools/figures/centrality_figs.py
"""
import math
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import LinearSegmentedColormap

OUT = Path(__file__).with_name("out")
OUT.mkdir(exist_ok=True)
plt.rcParams["font.family"] = "Arial"

# a school: H mentors six new Year 7s who know no one else (left), K sits in the popular crowd
# where everyone is friends with everyone (right), there's a chess club (bottom),
# and B has exactly one friend in each
G = nx.Graph()
pos = {"H": (-3.4, 0.9), "B": (0, 0), "K": (3.6, 0.9)}
for i in range(6):
    a = math.radians(95 + i * 34); G.add_edge("H", f"h{i}"); pos[f"h{i}"] = (-3.4 + 1.8 * math.cos(a), 0.9 + 1.8 * math.sin(a))
qs = [f"q{i}" for i in range(1, 6)]
for i, q in enumerate(qs):
    a = math.radians(-150 + i * 72); pos[q] = (3.6 + 1.9 * math.cos(a), 0.9 + 1.9 * math.sin(a)); G.add_edge("K", q)
for i in range(5): G.add_edge(qs[i], qs[(i + 1) % 5])
G.add_edges_from([("q1", "q3"), ("q2", "q4")])
rs = [f"r{i}" for i in range(6)]
for i, r in enumerate(rs):
    a = math.radians(90 + i * 60); pos[r] = (0 + 1.25 * math.cos(a), -2.5 + 1.25 * math.sin(a)); G.add_edge(r, rs[(i + 1) % 6])
G.add_edge("r0", "r3")
G.add_edges_from([("B", "H"), ("B", "q1"), ("B", "r0")])

MEASURES = {
    "degree": (dict(G.degree()), "#3d6fb6", lambda v: f"{v:.0f}"),
    "betweenness": (nx.betweenness_centrality(G, normalized=False), "#d6336c", lambda v: f"{v:.0f}"),
    "eigenvector": (nx.eigenvector_centrality(G, max_iter=5000), "#5b2a86", lambda v: f"{v:.2f}"),
}

# the formula, what its symbols mean, and the worked number for this measure's winner
ev = MEASURES["eigenvector"][0]
lam = sum(ev[q] for q in G["K"]) / ev["K"]
EQ = {
    "degree": (r"$C_D(i) = \sum_j A_{ij}$", r"$A_{ij} = 1$ if $i$ and $j$ are friends", r"H: $1+1+1+1+1+1+1 = 7$"),
    "betweenness": (r"$C_B(i) = \sum_{s \neq i \neq t} \dfrac{\sigma_{st}(i)}{\sigma_{st}}$",
                    r"$\sigma_{st}$: shortest paths from $s$ to $t$; $\sigma_{st}(i)$: those through $i$",
                    r"B: $7{\times}6 + 7{\times}6 + 6{\times}6 = 120$"),
    "eigenvector": (r"$x_i = \dfrac{1}{\lambda} \sum_j A_{ij}\, x_j$", r"$x_j$: your friends' scores; $\lambda$: a constant",
                    r"K: $(" + "{+}".join(f"{ev[q]:.2f}" for q in sorted(G["K"], key=ev.get, reverse=True)) + rf") / {lam:.1f} = {ev['K']:.2f}$"),
}

for name, (c, col, fmt) in MEASURES.items():
    cmap = LinearSegmentedColormap.from_list(name, ["#f1eef6", col])
    lo, hi = min(c.values()), max(c.values())
    t = {k: (v - lo) / (hi - lo) for k, v in c.items()}
    top = max(c, key=c.get)
    fig = plt.figure(figsize=(10, 8.1), dpi=200); ax = fig.add_axes([0, 0, 1, 1])   # fixed canvas: all three the same size
    for u, v in G.edges():
        on = top in (u, v)
        ax.plot(*zip(pos[u], pos[v]), color=col if on else "#9a9a9a", lw=4 if on else 2.2, zorder=1, solid_capstyle="round")
    for k, (x, y) in pos.items():
        r = 0.34 + 0.3 * t[k]
        ax.add_patch(plt.Circle((x, y), r, facecolor=cmap(0.15 + 0.85 * t[k]), edgecolor="#000" if k == top else "#fff", lw=4 if k == top else 2, zorder=2))
        ax.text(x, y, fmt(c[k]), ha="center", va="center", zorder=3, fontsize=(13 if name == "eigenvector" and t[k] < .5 else 16) + 6 * t[k], fontweight="bold",
                color="#fff" if t[k] > 0.45 else "#222")
    for k, ang in {"H": 30, "B": 90, "K": 102}.items():         # letter in a gap between the node's edges
        x, y = pos[k]; r = 0.34 + 0.3 * t[k] + 0.42; a = math.radians(ang)
        ax.text(x + r * math.cos(a), y + r * math.sin(a), k, ha="center", va="center", fontsize=26, fontweight="bold",
                color=col if k == top else "#555", zorder=4)
    for (x, y), text in {(-3.4, -1.55): "New Year 7s", (3.6, -2.0): "Popular crowd", (1.55, -3.75): "Chess club"}.items():
        ax.text(x, y, text, ha="center" if x < 1 or x > 3 else "left", va="center", fontsize=20, style="italic", color="#777")
    eq, key, worked = EQ[name]
    ax.plot([-5.7, 6.2], [-4.5, -4.5], color="#ddd", lw=1.5)          # equation band under the network
    ax.text(-5.7, -5.45, eq, ha="left", va="center", fontsize=30, color="#000")
    ax.text(-0.7, -5.15, worked, ha="left", va="center", fontsize=17, color=col)
    ax.text(-0.7, -5.8, key, ha="left", va="center", fontsize=14, color="#555")
    ax.set_xlim(-5.8, 6.3); ax.set_ylim(-6.35, 3.45); ax.set_aspect("equal"); ax.axis("off")
    fig.savefig(OUT / f"centrality_{name}.png", facecolor="white")
    plt.close(fig)
    print(name, sorted(((round(v, 3), k) for k, v in c.items()), reverse=True)[:4])
