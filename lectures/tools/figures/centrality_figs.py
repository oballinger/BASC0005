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

# a hub with six one-link spokes (left), a tight group around K (right), a loop (bottom),
# and B, whose only job is to join the three
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

for name, (c, col, fmt) in MEASURES.items():
    cmap = LinearSegmentedColormap.from_list(name, ["#f1eef6", col])
    lo, hi = min(c.values()), max(c.values())
    t = {k: (v - lo) / (hi - lo) for k, v in c.items()}
    top = max(c, key=c.get)
    fig, ax = plt.subplots(figsize=(10, 7.4), dpi=200)
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
    ax.set_xlim(-5.8, 6.3); ax.set_ylim(-4.35, 3.45); ax.set_aspect("equal"); ax.axis("off")
    fig.savefig(OUT / f"centrality_{name}.png", bbox_inches="tight", pad_inches=0.05, transparent=False, facecolor="white")
    plt.close(fig)
    print(name, sorted(((round(v, 3), k) for k, v in c.items()), reverse=True)[:4])
