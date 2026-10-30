"""生成配套图表（PNG），供报告引用。"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from bid_strategy_toolkit import (
    PacingController, elasticity, fit_cdf, make_landscape,
    optimal_bid, simulate,
)

OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

z = make_landscape()
rng = np.random.default_rng(11)
bids = rng.lognormal(-0.2, 0.6, z.size)
win, _ = simulate(z, bids)
grid = np.geomspace(0.02, 8.0, 160)

F_ok = fit_cdf(grid, bids, win)
F_bad = fit_cdf(grid, bids[win], win[win])
true_b = np.linspace(0.02, 8.0, 400)
true_F = np.array([(z < b).mean() for b in true_b])

# ---- 图1：删失 vs 丢弃 -----------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(true_b, true_F, "k-", lw=2.5, label="真实 P(win|b)")
ax.plot(grid, F_ok, "--", color="#1f77b4", lw=2, label="含删失估计（正确）")
ax.plot(grid, F_bad, ":", color="#d62728", lw=2.5, label="丢弃输的记录（有偏）")
ax.axvspan(bids.min(), bids.max(), alpha=0.08, color="green", label="历史出价范围")
ax.set_xscale("log")
ax.set_xlabel("出价 b")
ax.set_ylabel("赢率 P(win | b)")
ax.set_title("图1  删失处理对赢率曲线的影响")
ax.legend(loc="lower right")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "fig1_censoring.png", dpi=150)
plt.close(fig)

# ---- 图2：盈余曲线与最优出价 ----------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
for v, c in [(0.5, "#9467bd"), (1.0, "#1f77b4"), (2.0, "#ff7f0e"), (4.0, "#2ca02c")]:
    cands = np.linspace(0.02, v, 500)
    w = np.interp(cands, grid, F_ok, left=0.0, right=1.0)
    sur = (v - cands) * w
    ax.plot(cands, sur / max(sur.max(), 1e-12), color=c, lw=2, label=f"v={v}")
    b_star, _ = optimal_bid(v, grid, F_ok)
    ax.axvline(b_star, color=c, ls="--", lw=1)
ax.set_xlabel("出价 b")
ax.set_ylabel("期望盈余（按各自最大值归一）")
ax.set_title("图2  不同估值下的盈余曲线与最优点（虚线 = b*）")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "fig2_surplus.png", dpi=150)
plt.close(fig)

# ---- 图3：折价率随估值变化 ------------------------------------------------
vs = np.linspace(0.3, 8, 40)
ratios = [optimal_bid(v, grid, F_ok)[0] / v for v in vs]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(vs, np.array(ratios) * 100, color="#1f77b4", lw=2.5, marker="o", ms=3)
ax.axhline(70, color="#d62728", ls="--", lw=2, label="固定全局折价 ×0.7")
ax.set_xlabel("估值 v")
ax.set_ylabel("最优折价率 b*/v (%)")
ax.set_title("图3  折价率随估值变化 —— 单一全局乘子难以覆盖真实结构")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "fig3_shading_ratio.png", dpi=150)
plt.close(fig)

# ---- 图4：闭环控制收敛 ----------------------------------------------------
ctrl = PacingController(lam0=2.0, eta=0.30)
target, base = 0.25, 0.5
lams, wins = [], []
for _ in range(20):
    lams.append(ctrl.lam)
    r = float((z < base * ctrl.lam).mean())
    wins.append(r)
    ctrl.update(-np.log(r / target))
steps = np.arange(1, len(lams) + 1)

fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(steps, lams, color="#1f77b4", lw=2.5, marker="o", label="λ")
ax1.set_xlabel("控制轮次")
ax1.set_ylabel("pacing 乘子 λ", color="#1f77b4")
ax1.tick_params(axis="y", labelcolor="#1f77b4")
ax2 = ax1.twinx()
ax2.plot(steps, np.array(wins) * 100, color="#2ca02c",
         lw=2, ls="--", marker="s", ms=3, label="实际赢率")
ax2.axhline(target * 100, color="#d62728", ls=":", lw=2)
ax2.set_ylabel("赢率 (%)", color="#2ca02c")
ax2.tick_params(axis="y", labelcolor="#2ca02c")
ax1.set_title("图4  乘性对偶控制的收敛（目标赢率 25%）")
ax1.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "fig4_control.png", dpi=150)
plt.close(fig)

# ---- 图5：探索预算与尾部辨识 ----------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
for cap, c, lbl in [(1.0, "#d62728", "历史出价上界 1.0（无探索）"),
                    (2.0, "#ff7f0e", "历史出价上界 2.0"),
                    (4.0, "#2ca02c", "历史出价上界 4.0（有探索）")]:
    r2 = np.random.default_rng(31)
    b2 = np.minimum(r2.lognormal(-0.2, 0.6, z.size), cap)
    w2 = b2 > z
    F2 = fit_cdf(grid, b2, w2)
    ax.plot(grid, F2, color=c, lw=2, label=lbl)
ax.plot(true_b, true_F, "k--", lw=2, label="真实")
ax.axvline(3.0, color="gray", ls=":", lw=1.5)
ax.set_xscale("log")
ax.set_xlabel("出价 b")
ax.set_ylabel("P(win | b)")
ax.set_title("图5  出价上界决定了赢率曲线的可信区间")
ax.legend(loc="lower right")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "fig5_exploration.png", dpi=150)
plt.close(fig)

print("figures written to", OUT)
for p in sorted(OUT.glob("*.png")):
    print(" -", p.name, f"{p.stat().st_size/1024:.0f} KB")
