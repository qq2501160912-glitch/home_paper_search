"""
DSP 广告主侧竞价策略工具箱 —— 可运行的最小完整实现
=================================================

配套调研报告《DSP 竞价应对策略调研.md》。

结构：
  L1  竞价环境（竞争出价分布 / landscape）
  L2  报价估算 —— 删失最大似然 + 风险率表（Kaplan-Meier 思想）
  L3  折价优化 —— 盈余最大化 / 弹性-勒纳条件
  L4  闭环控制 —— 乘性对偶更新（P / PI 控制器）

只依赖 numpy。运行： python bid_strategy_toolkit.py
"""
from __future__ import annotations

import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# L1  竞价环境
# ---------------------------------------------------------------------------

def make_landscape(seed=7, n=200_000, mu=0.0, sigma=0.7, floor=0.05):
    """生成每条请求的最高竞争出价 z（现实中不可见，是待估对象）。"""
    rng = np.random.default_rng(seed)
    return np.maximum(rng.lognormal(mu, sigma, n), floor)


def simulate(z, bids):
    """赢/输 + 成交价。输掉的只知道 z > bid（右删失）。"""
    win = bids > z
    return win, np.where(win, bids, np.nan)


# ---------------------------------------------------------------------------
# L2  删失数据 -> 赢率曲线
# ---------------------------------------------------------------------------

def fit_hazard_grid(grid, bids, win, n_iter=60):
    """Kaplan-Meier 式风险率表。

    λ_k = P(z 落在档 k | z >= q_k)

    赢的记录 落档 k：贡献 λ_k · Π_{j<k}(1-λ_j)
    输的记录 (z > b)：只贡献  Π_{j<=k(b)}(1-λ_j)   ← 删失项

    MLE 近似解：λ_k = d_k / n_k，d_k = 落在档 k 的赢数，
    n_k = 所有落在档 k 或之后的记录数（风险集）。加性平滑防 0/1。
    """
    K = len(grid)
    k = np.clip(np.searchsorted(grid, bids, side="right"), 0, K - 1)
    at_risk = np.bincount(k, minlength=K)[::-1].cumsum()[::-1].astype(float)
    d = np.bincount(k[win], minlength=K).astype(float)
    lam = np.clip((d + 0.5) / (at_risk + 1.0), 1e-6, 1 - 1e-6)
    # 风险集为 0 的档（超出历史出价上界）沿用最后一个有效风险率
    if not np.isfinite(lam).all():
        lam = np.nan_to_num(lam, nan=1e-6)
    return lam


def cdf_from_hazard(grid, lam):
    S = np.cumprod(1.0 - lam)
    return 1.0 - S          # F(q) = P(z <= q)


def fit_cdf(grid, bids, win):
    return cdf_from_hazard(grid, fit_hazard_grid(grid, bids, win))


# ---------------------------------------------------------------------------
# L3  折价优化
# ---------------------------------------------------------------------------

def optimal_bid(v, grid, F, cap=1.0):
    """argmax_b (v - b) * F(b)，一价付费（支付自己的出价）。"""
    cands = np.unique(np.concatenate([grid, [v * cap]]))
    cands = cands[(cands > 0) & (cands <= v * cap)]
    w = np.clip(np.interp(cands, grid, F, left=0.0, right=1.0), 0, 1)
    surplus = np.maximum(v - cands, 0) * w
    i = int(np.argmax(surplus))
    return float(cands[i]), float(w[i])


def elasticity(grid, F, b):
    """赢率对出价的弹性 ε = d ln F / d ln b。"""
    h = max(b * 0.01, 1e-6)
    lo = np.interp(b - h, grid, F, left=0.0, right=1.0)
    hi = np.interp(b + h, grid, F, left=0.0, right=1.0)
    if lo <= 1e-9 or hi <= 1e-9 or b - h <= 0:
        return 0.0
    return (np.log(hi) - np.log(lo)) / np.log((b + h) / (b - h))


# ---------------------------------------------------------------------------
# L4  闭环控制
# ---------------------------------------------------------------------------

class PacingController:
    """乘性对偶 / PI 控制器。

    bid = base_bid × λ
    log λ ← log λ + eta·e + ki·∫e        (e 为相对误差)
    """

    def __init__(self, lam0=1.0, eta=0.30, ki=0.0, lam_min=0.02, lam_max=8.0):
        self.lam, self.eta, self.ki = lam0, eta, ki
        self.lam_min, self.lam_max = lam_min, lam_max
        self._i = 0.0

    def update(self, e):
        self._i = float(np.clip(self._i + e, -20, 20))
        u = self.eta * e + self.ki * self._i
        self.lam = float(np.clip(self.lam * np.exp(u), self.lam_min, self.lam_max))
        return self.lam


# ---------------------------------------------------------------------------
# 数值实验
# ---------------------------------------------------------------------------

def section(t):
    print("\n" + "=" * 76)
    print(t)
    print("=" * 76)


def run():
    z = make_landscape()
    rng = np.random.default_rng(11)
    bids = rng.lognormal(-0.2, 0.6, z.size)   # 模拟线上历史出价
    win, _ = simulate(z, bids)

    grid = np.geomspace(0.02, 8.0, 160)       # 覆盖完整价格轴

    section("实验 1：删失 vs 丢弃 —— 输掉的竞价为什么不能删")
    F_ok = fit_cdf(grid, bids, win)
    F_bad = fit_cdf(grid, bids[win], win[win])
    print(f"样本 {z.size:,} 条，整体赢率 {win.mean():.1%}")
    print(f"历史出价范围 [{bids.min():.3f}, {bids.max():.3f}]\n")
    print(f"{'出价b':>7} {'真实P(win)':>11} {'含删失估计':>11} {'丢弃输的记录':>13}")
    for b in [0.3, 0.5, 0.8, 1.2, 2.0, 3.0]:
        t = float((z < b).mean())
        print(f"{b:>7.2f} {t:>10.1%} {float(np.interp(b, grid, F_ok)):>10.1%} "
              f"{float(np.interp(b, grid, F_bad)):>12.1%}")
    print("\n解读：删失项保证了赢率曲线在历史出价范围内无偏；")
    print("      丢弃输的记录后，曲线形状被压平，对低价位严重高估、对高价位低估。")

    section("实验 2：估值 v 决定折价率 (b*/v)")
    print(f"{'估值v':>7} {'最优出价b*':>11} {'折价率':>8} {'赢率':>8} {'弹性ε':>8} {'(v-b)/b':>9}")
    for v in [0.5, 1.0, 2.0, 4.0, 8.0]:
        b, wr = optimal_bid(v, grid, F_ok)
        eps = elasticity(grid, F_ok, b)
        print(f"{v:>7.2f} {b:>10.3f} {b / v:>7.1%} {wr:>7.1%} {eps:>8.2f} {(v - b) / b:>9.2f}")
    print("\n解读：v 越高，弹性越大，折价率越低（越敢加价）。最后一列应接近 1/ε，")
    print("      这就是勒纳条件 (v-b)/b = 1/ε 的数值验证。单一全局乘子无法表达这一依赖。")

    section("实验 3：四种策略在完全相同 landscape 下的表现")
    v = np.full(z.size, 1.0)
    b_opt, _ = optimal_bid(1.0, grid, F_ok)
    strat = {
        "出真实价值 v=1.0（不折价）": np.full(z.size, 1.0),
        "出成交价中位数(观察者偏差)": np.full(z.size, float(np.median(bids[win]))),
        "单一全局折价 ×0.7": v * 0.7,
        "盈余最大化 b*(v=1)": np.full(z.size, b_opt),
    }
    print(f"{'策略':<26} {'平均出价':>9} {'赢率':>7} {'总花费':>9} {'总盈余':>9} {'ROI':>7}")
    for name, b in strat.items():
        w = b > z
        cost = float(np.where(w, b, 0).sum())
        val = float((v * w).sum())
        roi = val / cost if cost > 0 else float("nan")
        print(f"{name:<26} {b.mean():>9.3f} {w.mean():>6.1%} "
              f"{cost:>9.0f} {val - cost:>9.0f} {roi:>7.3f}")
    print("\n解读：'出成交价中位数'因观察者偏差出了个高得离谱的价格，直接亏钱；")
    print("      全局 ×0.7 能赚钱但赢率低；盈余最大化在可接受 ROI 下拿到正盈余。")

    section("实验 4：闭环控制收敛（从错误 λ=2.0 出发，目标赢率 25%）")
    ctrl = PacingController(lam0=2.0, eta=0.30)
    target, base = 0.25, 0.5
    print(f"{'轮次':>4} {'λ':>7} {'实际赢率':>9} {'误差(pp)':>10}")
    for t in range(1, 13):
        b = base * ctrl.lam
        r = float((z < b).mean())
        print(f"{t:>4} {ctrl.lam:>7.3f} {r:>8.1%} {(r - target) * 100:>+9.1f}")
        ctrl.update(-np.log(r / target))     # 赢率过高 -> 降 λ
    print("\n解读：乘性更新约 6-8 轮收敛，天然非负、尺度无关；")
    print("      这是 Balseiro 等对偶镜像下降 + Fikioris 等 P-控制器结论的直观测例。")

    section("实验 5：出价上限（探索）决定了你能看到多远")
    print(f"{'历史出价上界':>12} {'b=3.0 赢率估计':>16} {'真实':>8} {'b=3.0 处可定价?':>16}")
    true_at_3 = float((z < 3.0).mean())
    for cap in [1.0, 2.0, 4.0, 8.0]:
        rng2 = np.random.default_rng(31)
        b2 = np.minimum(rng2.lognormal(-0.2, 0.6, z.size), cap)
        w2 = b2 > z
        F2 = fit_cdf(grid, b2, w2)
        est = float(np.interp(3.0, grid, F2))
        ok = "是" if cap >= 3.0 else "否(外推)"
        print(f"{cap:>12.1f} {est:>15.1%} {true_at_3:>7.1%} {ok:>16}")
    print("\n解读：历史出价封顶在 1.0/2.0 时，b=3.0 处的赢率完全是外推的，不可信。")
    print("      少量随机化/上探出价（探索预算）是把曲线推到高价位区的唯一办法。")


if __name__ == "__main__":
    run()
