"""Figures for the DSMC VLEO CubeSat drag study README."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "text.color": INK,
    "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.edgecolor": GRID, "figure.facecolor": SURF, "axes.facecolor": SURF})

def style(ax):
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0)

# ---------- Figure 1: nose designs ----------
designs = [  # name, volume L, Cd diffuse, Cd specular  (fins flat, total)
    ("SOAR baseline", 3.47, 0.395, 0.439),
    ("Obtuse wedge", 3.52, 0.395, 0.350),
    ("Wedge", 3.41, 0.390, 0.261),
    ("Acute wedge", 2.73, 0.361, 0.114),
    ("Square blunt bullet", 3.31, 0.379, 0.186),
    ("Square pointed bullet", 2.77, 0.357, 0.121),
    ("Round blunt bullet", 2.68, 0.326, 0.185),
    ("Round pointed bullet", 2.33, 0.310, 0.117),
]
n = len(designs); y = np.arange(n)[::-1]; h = 0.36
fig, ax = plt.subplots(figsize=(9, 6.2), dpi=200)
style(ax)
ax.xaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
for i, (name, vol, cdd, cds) in enumerate(designs):
    for val, off, col in [(cdd, h/2 + 0.02, BLUE), (cds, -h/2 - 0.02, ORANGE)]:
        ax.barh(y[i] + off, val, height=h, color=col, edgecolor=SURF, linewidth=1)
        base = designs[0][2] if col == BLUE else designs[0][3]
        pct = "" if i == 0 else f"  ({100*(val/base-1):+.0f}%)"
        ax.text(val + 0.006, y[i] + off, f"{val:.3f}{pct}", va="center", fontsize=9, color=INK2)
ax.set_yticks(y)
ax.set_yticklabels([f"{d[0]}\n{d[1]:.2f} L" for d in designs], fontsize=10)
for lab in ax.get_yticklabels()[:1]:
    lab.set_fontweight("bold")
ax.set_xlim(0, 0.56)
ax.set_xlabel("Total drag coefficient  (A_ref = 0.1125 m², fins flat)")
fig.text(0.02, 0.965, "Nose shape cuts drag only when the surface reflects molecules",
         fontsize=14, fontweight="bold", ha="left")
fig.text(0.02, 0.925, "SPARTA DSMC, ~400 km, all designs inside the 3U envelope (100 × 100 × 366 mm); "
         "% change vs SOAR baseline", fontsize=10, color=INK2, ha="left")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=BLUE, label="Diffuse walls (realistic, atomic oxygen)"),
                   Patch(color=ORANGE, label="Specular walls (ideal low-drag material)")],
          loc="lower left", bbox_to_anchor=(-0.33, 1.0), ncol=2, frameon=False, fontsize=9.5)
fig.subplots_adjust(left=0.24, right=0.97, top=0.86, bottom=0.09)
fig.savefig("drag_comparison.png")

# ---------- Figure 2: validation ----------
ang = np.array([0, 15, 30, 45, 60, 75, 90])
dsmc  = np.array([0.395, 0.510, 0.657, 0.786, 0.885, 0.946, 0.964])
adb   = np.array([0.405, 0.524, 0.677, 0.810, 0.913, 0.976, 0.996])
paper = np.array([np.nan, 0.325, 0.49, 0.625, 0.735, 0.80, 0.82])
fig, ax = plt.subplots(figsize=(9, 5.6), dpi=200)
style(ax); ax.spines["left"].set_visible(True); ax.spines["left"].set_color(GRID)
ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
series = [(adb, "ADBSat, this geometry", ORANGE, "s"),
          (dsmc, "SPARTA DSMC, this geometry", BLUE, "o"),
          (paper, "Crisp et al. 2021, Fig. 10", AQUA, "^")]
for data, lab, col, mk in series:
    ax.plot(ang, data, color=col, lw=2, marker=mk, ms=7, mec=SURF, mew=1.5, label=lab, zorder=3)
ax.text(91.5, 1.004, "ADBSat", color=INK, fontsize=10, va="bottom")
ax.text(91.5, 0.958, "DSMC", color=INK, fontsize=10, va="top")
ax.text(91.5, 0.82, "Crisp et al.\n2021, Fig. 10", color=INK, fontsize=10, va="center")
ax.annotate("", xy=(75, 0.808), xytext=(75, 0.938),
            arrowprops=dict(arrowstyle="<->", color=INK2, lw=1))
ax.text(76.5, 0.873, "near-constant\n0.17–0.20 offset", fontsize=9, color=INK2, va="center")
ax.set_xlim(-3, 106); ax.set_ylim(0.25, 1.08)
ax.set_xticks(ang); ax.set_xticklabels([f"{a}°" for a in ang])
ax.set_xlabel("Counter-rotated fin deflection")
ax.set_ylabel("Drag coefficient  (A_ref = 0.1125 m²)")
ax.legend(loc="lower right", frameon=False, fontsize=9.5)
fig.text(0.02, 0.965, "DSMC matches ADBSat within 3% on the same SOAR geometry",
         fontsize=14, fontweight="bold", ha="left")
fig.text(0.02, 0.925, "~400 km, fully diffuse walls (α = 1, 300 K). Both sit above the published "
         "reference curves by a near-constant offset", fontsize=10, color=INK2, ha="left")
fig.subplots_adjust(left=0.1, right=0.97, top=0.88, bottom=0.11)
fig.savefig("dsmc_validation.png")
print("done")
