"""Figures for the Week 8 difference-in-differences example (toy NJ vs PA poverty data).

usage: python tools/figures/causal_figs.py   -> writes tools/figures/causal/*.png
The same numbers appear in the tables on the W08 slides; change both, then paste the
new pictures into "W08 Causal Inference.pptx".
"""
from pathlib import Path
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent / "causal"
YEARS = [1989, 1990, 1991, 1992, 1993, 1994]
PA = [3.0, 3.6, 4.2, 4.8, 5.4, 6.0]          # control
NJ = [1.5, 2.1, 2.7, 2.3, 2.9, 3.5]          # treated from 1992: 1.0 below its trend
NJ_CF = [None, None, 2.7, 3.3, 3.9, 4.5]     # counterfactual: NJ on PA's trend
RED, BLUE, GREY = "#e30613", "#1f4e9c", "#555555"

plt.rcParams.update({"font.family": "Helvetica", "font.size": 15, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 150})


def base(ax):
    ax.plot(YEARS, PA, "o-", color=BLUE, lw=2.5, label="Pennsylvania (control)")
    ax.plot(YEARS, NJ, "o-", color=RED, lw=2.5, label="New Jersey (treated)")
    ax.axvline(1991.5, color=GREY, ls=":", lw=1.5)
    ax.text(1991.55, 6.3, "minimum wage rises", color=GREY, fontsize=12, va="top")
    ax.set_xticks(YEARS); ax.set_ylim(0, 6.5); ax.set_ylabel("Poverty rate (%)")
    ax.legend(frameon=False, loc="lower right")


fig, ax = plt.subplots(figsize=(8, 5.2)); base(ax); fig.tight_layout()
fig.savefig(OUT / "did_data.png"); plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 5.2)); base(ax)
ax.plot(YEARS[2:], NJ_CF[2:], "--", color=RED, lw=2, alpha=.55, label="New Jersey without the policy")
ax.annotate("", xy=(1993.5, 3.2), xytext=(1993.5, 4.2),
            arrowprops=dict(arrowstyle="<->", color="black", lw=1.8))
ax.text(1993.6, 3.7, "β₃ = −1.0", fontsize=16, fontweight="bold", va="center")
ax.legend(frameon=False, loc="lower right"); fig.tight_layout()
fig.savefig(OUT / "did_beta3.png"); plt.close(fig)
print("wrote", *sorted(p.name for p in OUT.glob("*.png")))
