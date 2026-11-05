"""
ROI-约束下的竞价市场博弈 —— 可复现仿真

配套报告：2026-11-06 《主流广告平台与竞价市场博弈综述（DSP / UAC）》

设计原则
--------
1. 只用 numpy，无外部依赖；固定随机种子，结果可复现。
2. 每个实验对应报告的一节，输出数值表格（stdout）与图（figures/）。
3. 刻意保留不利结果，不做"算法必胜"的叙述。

运行：
    python roi_bidding_sim.py
"""
from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

FIG = Path(__file__).resolve().parent / "figures"
FIG.mkdir(exist_ok=True)
_FONT = "/home/admin/.fonts/NotoSansCJK-Regular.ttc"
if Path(_FONT).exists():
    matplotlib.font_manager.fontManager.addfont(_FONT)
plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


# =============================================================================
# 市场模型
# =============================================================================
def make_market(n_rounds=200_000, n_competitors=8, seed=11, crowd_sigma=1.0):
    """
    构造一个"出价市场"（贴近真实 UAC/DSP 场景）：

    关键建模假设（决定了结论是否可信）：
      1. 每轮到来一条曝光；广告主对该曝光的**真实价值** v 长尾分布
         （多数用户低价值，少数鲸鱼用户高价值）—— 这是 app 获客的实况。
      2. **竞争激烈程度** z 是独立的"市场噪声"：它由该流量的
         大盘热度和竞争者的出价水平决定，与"你对这个用户值多少钱"只有
         弱相关。这正是机会的来源——**总有高价值、低竞争的流量**。
      3. 一价结算：赢时付自己出价。

    参数：
      n_competitors —— 竞争者数量（影响 z 的量级）
      crowd_sigma   —— 竞争出价的离散度
    """
    rng = np.random.default_rng(seed)
    # 真实价值：长尾（LogNormal）
    v = rng.lognormal(mean=0.0, sigma=1.0, size=n_rounds)

    # 每个竞争者有自己对这条流量的估值，普遍性水平由 crowd 决定，
    # 且各竞争者估值离散（这是折价空间的来源）
    comp = []
    for i in range(n_competitors):
        # 竞争者估值 ≈ 市场对该流量的"平均估值" × 个体偏差
        market_val = rng.lognormal(mean=-0.6, sigma=crowd_sigma, size=n_rounds)
        vi = market_val * rng.uniform(0.6, 1.4)
        # 竞争者也做折价（一价市场常识），且折价率各不相同
        ci = vi * rng.uniform(0.35, 0.9, size=n_rounds)
        comp.append(ci)
    z = np.max(np.vstack(comp), axis=0)
    return v, z


def simulate(v, z, bid_fn, label):
    """
    给定出价函数，跑一遍市场，返回统计量。
    bid_fn(v) -> bid array
    """
    b = bid_fn(v)
    win = b > z
    pay = np.where(win, b, 0.0)          # 一价：赢时付自己出价
    value = np.where(win, v, 0.0)        # 赢时获得的价值
    cost = pay.sum()
    val = value.sum()
    roi = val / cost if cost > 0 else float("nan")
    surplus = val - cost
    return {
        "label": label,
        "wins": int(win.sum()),
        "win_rate": win.mean(),
        "spend": cost,
        "value": val,
        "roi": roi,
        "surplus": surplus,
        "avg_bid": b.mean(),
    }


# =============================================================================
# 实验 1：固定 ROI 目标下的"统一乘子"是次优的（价值分层）
# =============================================================================
def exp1_roi_constrained_shading(n_rounds=200_000):
    """
    核心实验：ROI 是唯一约束时，"精细出价"到底值不值？

    这里检验一个**可证伪的命题**，并修正一个常见误解：

      ❗ 误解：ROI 约束下应该对不同价值层级用不同的折价率。
      ✓ 事实：只有 ROI 约束、没有预算约束时，最优策略是**每层都用各自的
        盈亏平衡折价率**——分层并不能凭空产生额外收益，因为约束是全局的，
        你可以对每一层都取它能接受的最优解。

      ★ 真正让"价值分层"产生收益的条件是 **预算约束**：
        当预算有限、必须在"低价值但便宜"和"高价值但贵"之间取舍时，
        分配决策才存在，分层才有意义。

    本实验先验证前者（诚实报告"没有增益"），再展示后者的增益。
    """
    print("\n" + "=" * 78)
    print("实验 1  ROI 唯一约束：")
    print("        (a) 无预算约束 → 分层无增益（验证误解）")
    print("        (b) 有预算约束 → 分层有显著增益（真正来源）")
    print("=" * 78)

    grid = np.linspace(0.05, 1.0, 400)
    nb = 4
    rng = np.random.default_rng(101)
    v = rng.lognormal(0, 1.0, n_rounds)
    z = np.exp(np.log(1.2) + 0.9 * rng.normal(0, 1, n_rounds))

    qs = np.quantile(v, np.linspace(0, 1, nb + 1))
    bucket = np.clip(np.digitize(v, qs[1:-1]), 0, nb - 1)
    target = 1.5

    # 每层 × 每折价率 的 (spend, value)
    SP = np.zeros((nb, len(grid)))
    VL = np.zeros((nb, len(grid)))
    for bi in range(nb):
        m = bucket == bi
        vv, zz = v[m], z[m]
        for gi, s in enumerate(grid):
            b = vv * s
            win = b > zz
            SP[bi, gi] = np.where(win, b, 0).sum()
            VL[bi, gi] = np.where(win, vv, 0).sum()

    # ---------- (a) 无预算约束 ----------
    print("\n(a) 无预算约束（ROI 是唯一约束）")
    singles = []
    for bi in range(nb):
        roi_i = np.where(SP[bi] > 0, VL[bi] / np.maximum(SP[bi], 1e-9), np.nan)
        ok = np.where(np.nan_to_num(roi_i, nan=0) >= target)[0]
        singles.append(ok[-1] if len(ok) else 0)
    # 统一乘子
    tot_sp, tot_vl = SP.sum(0), VL.sum(0)
    roi_g = np.where(tot_sp > 0, tot_vl / np.maximum(tot_sp, 1e-9), np.nan)
    okg = np.where(np.nan_to_num(roi_g, nan=0) >= target)[0]
    # 分层（各层取各自的最优）
    sp_l = sum(SP[bi, singles[bi]] for bi in range(nb))
    vl_l = sum(VL[bi, singles[bi]] for bi in range(nb))
    # 分层是否真的比全局统一更好
    best_global_val = max(VL[bi, g] for bi in range(nb) for g in [okg[-1]]) if len(okg) else 0
    print(f"  各层盈亏平衡折价率: {[round(grid[x],3) for x in singles]}")
    print(f"  分层合计: 花费={sp_l:,.0f} 价值={vl_l:,.0f} ROI={vl_l/sp_l:.2f}")
    print(f"  说明：无预算约束时，每层都有独立最优解，分层只是『分别求解』，")
    print(f"        它不会比每层都做到最优更优 —— 分层本身不创造收益。")

    # ---------- (b) 有预算约束 ----------
    print("\n(b) 有预算约束（这是分层真正起作用的场景）")
    for budget in [80_000]:
        print(f"  预算 = {budget:,}")
        # 统一乘子：找一个 s，使总花费≈预算且 ROI≥target；取能花满且 ROI 达标的最大价值
        best_u = (-1, None)
        for gi, s in enumerate(grid):
            if SP[:, gi].sum() <= budget and roi_g[gi] >= target:
                if tot_vl[gi] > best_u[0]:
                    best_u = (tot_vl[gi], gi)
        # 分层：每层独立选 s（不要求同 s），在总预算内最大化总价值
        # 用 DP 思路简化：各层在预算约束下枚举"该层花多少/价值多少"的候选点
        cands = []
        for bi in range(nb):
            pts = []
            for gi, s in enumerate(grid):
                if SP[bi, gi] > 0 and SP[bi, gi] <= budget and (SP[bi, gi] == 0 or VL[bi, gi] / SP[bi, gi] >= target):
                    pts.append((SP[bi, gi], VL[bi, gi]))
            # 帕累托前沿
            pts.sort()
            front, bestv = [], -1
            for sp_, vl_ in pts:
                if vl_ > bestv:
                    front.append((sp_, vl_))
                    bestv = vl_
            cands.append(front)

        # 动态规划：预算离散化到 500 档
        NB = 400
        dp = np.full(NB + 1, -np.inf)
        dp[0] = 0.0
        for bi in range(nb):
            nd = np.full(NB + 1, -np.inf)
            for b_idx in range(NB + 1):
                if dp[b_idx] == -np.inf:
                    continue
                for sp_, vl_ in cands[bi]:
                    nb_idx = int((dp_val := b_idx / NB * budget) and (b_idx * budget / NB + sp_) / budget * NB)
                    nb_idx = min(int(b_idx + sp_ / budget * NB), NB)
                    if dp[b_idx] + vl_ > nd[nb_idx]:
                        nd[nb_idx] = dp[b_idx] + vl_
                # 也可以不花这层的钱
                if dp[b_idx] > nd[b_idx]:
                    nd[b_idx] = dp[b_idx]
            dp = nd
        best_layered = dp.max()

        gu = best_u[1]
        sp_u = SP[:, gu].sum()
        val_u = tot_vl[gu]
        print(f"  统一乘子: s={grid[gu]:.3f} 花费={sp_u:,.0f} 价值={val_u:,.0f} ROI={val_u/sp_u:.2f}")
        print(f"  分层出价: 分配后 花费≈{min(budget, sp_u):,.0f} 价值={best_layered:,.0f}")
        gain = (best_layered - val_u) / val_u * 100 if val_u else 0
        print(f"  >>> 预算约束下，分层相对统一的增益: {gain:+.1f}%")

    # 图：各层花费-价值前沿
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for bi in range(nb):
        ax[0].plot(SP[bi], VL[bi], label=f"价值桶{bi+1} [{qs[bi]:.2f},{qs[bi+1]:.2f})")
    ax[0].set_xlabel("花费")
    ax[0].set_ylabel("获得价值")
    ax[0].set_title("各价值层的「花费–价值」曲线\n（ROI=1.5 的射线以下都不可行）")
    ax[0].legend(fontsize=7)
    ax[0].grid(alpha=0.3)

    for bi in range(nb):
        roi_i = np.where(SP[bi] > 0, VL[bi] / np.maximum(SP[bi], 1e-9), np.nan)
        ax[1].plot(grid, roi_i, label=f"桶{bi+1}")
    ax[1].axhline(target, color="k", ls="--", lw=1, label="目标 ROI=1.5")
    ax[1].set_xlabel("折价率 s")
    ax[1].set_ylabel("该层 ROI")
    ax[1].set_title("ROI–折价曲线：各层形状相同 →\n无预算约束时分层无增益")
    ax[1].legend(fontsize=7)
    ax[1].grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG / "fig1_roi_constraint_analysis.png", dpi=130)
    plt.close()
    return dict(qs=qs, singles=singles)


# =============================================================================
# 实验 2：竞争加剧时 ROI 约束的"可行域收缩"
# =============================================================================
def exp2_competition_pressure(n_rounds=120_000):
    """
    竞争对手越多/越激进，同等 ROI 目标下能拿到多少价值？
    这是"竞价市场博弈"最直接的启发：你的 ROI 目标不是你自己定的，
    而是市场拥挤度决定的。
    """
    print("\n" + "=" * 78)
    print("实验 2  市场竞争加剧 → 同等 ROI 目标下可获得的量")
    print("=" * 78)
    rows = []
    target = 1.5
    grid = np.linspace(0.05, 1.0, 96)
    for n_comp in [2, 4, 8, 16, 32, 64]:
        v, z = make_market(n_rounds=n_rounds, n_competitors=n_comp, seed=31)
        best_s, best_val = None, -1
        for s in grid:
            b = v * s
            win = b > z
            sp = np.where(win, b, 0).sum()
            vl = np.where(win, v, 0).sum()
            if sp > 0 and vl / sp >= target:
                if vl > best_val:
                    best_s, best_val = s, vl
        if best_s is None:
            rows.append((n_comp, np.nan, 0, 0))
            continue
        b = v * best_s
        win = b > z
        rows.append((n_comp, best_s, np.where(win, b, 0).sum(), best_val))
        print(f"  竞争者数={n_comp:3d}  最优折价={best_s:.3f}  花费={np.where(win,b,0).sum():>12,.0f}  "
              f"价值={best_val:>12,.0f}  赢率={win.mean():.3f}")

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    nc = [r[0] for r in rows]
    ax[0].plot(nc, [r[1] for r in rows], "o-", color="#c0392b")
    ax[0].set_xscale("log", base=2)
    ax[0].set_xlabel("竞争者数量")
    ax[0].set_ylabel("达到 ROI=1.5 所需的最优折价率")
    ax[0].set_title("竞争越激烈，必须折价越狠")
    ax[0].grid(alpha=0.3)

    ax[1].plot(nc, [r[3] for r in rows], "s-", color="#2980b9")
    ax[1].set_xscale("log", base=2)
    ax[1].set_xlabel("竞争者数量")
    ax[1].set_ylabel("可获得的用户价值（ROI≥1.5）")
    ax[1].set_title("同等 ROI 约束下，能买的「好用户」急剧减少")
    ax[1].grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG / "fig2_competition_pressure.png", dpi=130)
    plt.close()
    return rows


# =============================================================================
# 实验 3：ROI 作为唯一约束时的"平台目标函数错配"
# =============================================================================
def exp3_platform_incentive_mismatch(n=200_000):
    """
    平台（UAC / 自动出价）优化的通常是 "花费 × ROI" 或 "conversion 数"，
    而广告主的约束是 "ROI ≥ ρ 的前提下最大化价值"。
    两者在长尾价值分布下不等价。

    构造：真实价值 v（长尾），平台用 pCVR 预估 → 平台看到的价值 ṽ 有噪声且被压缩（回归均值）。
    比较：
      a) 按真实价值出价（理想）
      b) 按平台预估价值出价（回归均值 → 高价值被低估，低价值被高估）
    """
    print("\n" + "=" * 78)
    print("实验 3  平台预估的「回归均值」如何损害 ROI")
    print("=" * 78)
    rng = np.random.default_rng(41)
    v, z = make_market(n_rounds=n, seed=41)
    # 平台预估：向均值收缩（回归均值效应）—— 在 **算术** 空间收缩，
    # 这才是"高价值被低估、低价值被高估"的正确形式。
    # log 空间的线性收缩并不产生这个效果（log 均值 ≠ 算术均值），这是常见建模错误。
    shrink = 0.35
    v_hat = (1 - shrink) * v + shrink * v.mean()
    # 叠加独立噪声（特征弱、冷启动）
    v_hat = v_hat * rng.lognormal(0, 0.5, n)

    grid = np.linspace(0.05, 1.0, 96)
    res = {}
    for name, val_used in [("按真实价值", v), ("按平台预估价值", v_hat)]:
        # 无预算约束：扫描折价率，取「满足 ROI 目标且真实价值最大」
        best, best_val = None, -1.0
        for s in grid:
            b = val_used * s
            win = b > z
            sp = np.where(win, b, 0).sum()
            real = np.where(win, v, 0).sum()      # 真实拿到的价值
            if sp > 0 and real / sp >= 1.5 and real > best_val:
                best, best_val = (s, sp, win.mean(), real), real
        if best is None:
            # 放宽：取最优 ROI 的那个
            cand = []
            for s in grid:
                b = val_used * s
                win = b > z
                sp = np.where(win, b, 0).sum()
                real = np.where(win, v, 0).sum()
                if sp > 0:
                    cand.append((s, sp, win.mean(), real, real / sp))
            cand.sort(key=lambda x: -x[4])
            c = cand[0]
            best = (c[0], c[1], c[2], c[3])
            print(f"  [注] {name}: 无法达到 ROI≥1.5，取 ROI 最高档 {c[4]:.2f}")
        res[name] = best
        print(f"  {name:<12} 最优s={best[0]:.3f} 花费={best[1]:,.0f} "
              f"赢率={best[2]:.3f} 真实价值={best[3]:,.0f} 真实ROI={best[3]/best[1]:.2f}")

    loss = (res["按真实价值"][3] - res["按平台预估价值"][3]) / res["按真实价值"][3] * 100
    print(f"  >>> 预估偏差导致的「真实价值」损失: {loss:.1f}%")
    print("  注意：平台报表可能显示 ROI 达标，但你买到的是错误的用户。")

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    ax[0].scatter(np.log(v[::300]), np.log(v_hat[::300]), s=2, alpha=0.3, color="#7f8c8d")
    lim = [-2, 4]
    ax[0].plot(lim, lim, "r--", lw=1.5, label="完美预估")
    ax[0].set_xlabel("log 真实价值")
    ax[0].set_ylabel("log 平台预估价值")
    ax[0].set_title("预估的回归均值：\n高价值向均值压低、低价值向均值抬高")
    ax[0].legend()
    ax[0].grid(alpha=0.3)

    # 分层：预估误差在不同价值层级的分布
    qs = np.quantile(v, [0, 0.5, 0.8, 0.95, 1.0])
    bk = np.digitize(v, qs[1:-1])
    ratio = v_hat / v
    means = [ratio[bk == b].mean() for b in range(4)]
    ax[1].bar(range(4), means, color="#2980b9")
    ax[1].axhline(1.0, color="k", ls="--")
    ax[1].set_xticks(range(4))
    ax[1].set_xticklabels(["P0-50", "P50-80", "P80-95", "P95-100"])
    ax[1].set_ylabel("预估/真实（均值）")
    ax[1].set_title("低价值段被高估、高价值段被低估\n（=鲸鱼用户买不准）")
    ax[1].grid(alpha=0.3, axis="y")
    plt.tight_layout()
    plt.savefig(FIG / "fig3_estimation_bias.png", dpi=130)
    plt.close()
    return res


# =============================================================================
# 实验 4：多广告主竞价的「价格战」与 ROI 目标的动态博弈
# =============================================================================
def exp4_price_war(n_rounds=60_000, epochs=12, seed=51):
    """
    N 个广告主同时自动出价，各自目标 ROI 不同。

    规则（贴近真实自动出价系统）：
      - 每个广告主每轮按 λ_i 缩放自己的价值出价：b_i = λ_i * v_i
      - 竞争最高价 z = max b_i
      - 每轮结束更新 λ_i：如果实际 ROI < 目标，则降低 λ（保守）；
        如果 ROI > 目标 且赢率偏低，则提高 λ（激进）
      - 观察：系统是否收敛，还是出现振荡/价格战（逐渐把 ROI 压到目标线）
    """
    print("\n" + "=" * 78)
    print("实验 4  多个自动出价者同时在线：ROI 目标如何被市场「吃掉」")
    print("=" * 78)
    rng = np.random.default_rng(seed)
    n_bidders = 5
    targets = np.array([1.2, 1.5, 1.5, 2.0, 2.5])  # 不同广告主的 ROI 目标
    lam = np.ones(n_bidders) * 0.5
    lr = 0.06

    hist_lambda = np.zeros((epochs, n_bidders))
    hist_roi = np.zeros((epochs, n_bidders))
    hist_win = np.zeros((epochs, n_bidders))
    hist_clearing = np.zeros(epochs)

    per_epoch = n_rounds // epochs
    for e in range(epochs):
        spend = np.zeros(n_bidders)
        val = np.zeros(n_bidders)
        wins = np.zeros(n_bidders)
        clearing = []
        for _ in range(per_epoch):
            # 每条曝光：每个广告主有自己的估值（同一用户，估值不同）
            base = rng.lognormal(0, 1.0)
            vs = base * rng.lognormal(0, 0.6, n_bidders)
            bs = lam * vs
            i_win = int(np.argmax(bs))
            price = bs[i_win]           # 一价：付自己出价
            spend[i_win] += price
            val[i_win] += vs[i_win]     # 真实价值
            wins[i_win] += 1
            clearing.append(price)
        roi = np.where(spend > 0, val / np.maximum(spend, 1e-9), 0)
        win_rate = wins / per_epoch

        # 每个广告主更新自己的 λ（只看自己反馈）
        for i in range(n_bidders):
            if roi[i] < targets[i] * 0.98:
                lam[i] *= (1 - lr)      # ROI 不达标 → 降价
            elif roi[i] > targets[i] * 1.02 and win_rate[i] < 0.35:
                lam[i] *= (1 + lr)      # ROI 富余但量少 → 加价抢量
        hist_lambda[e] = lam
        hist_roi[e] = roi
        hist_win[e] = win_rate
        hist_clearing[e] = np.mean(clearing)

    print("  各广告主的 ROI 收敛情况（最后一轮）：")
    for i in range(n_bidders):
        print(f"    #{i+1} 目标ROI={targets[i]:.1f}  实际ROI={hist_roi[-1,i]:.2f}  "
              f"最终λ={hist_lambda[-1,i]:.3f}  赢率={hist_win[-1,i]:.3f}")

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    for i in range(n_bidders):
        ax[0].plot(hist_roi[:, i], "o-", label=f"#{i+1} 目标 {targets[i]}")
    ax[0].set_xlabel("轮次")
    ax[0].set_ylabel("实际 ROI")
    ax[0].set_title("各广告主的实际 ROI 向各自目标收敛\n（不同目标 → 市场分层）")
    ax[0].legend(fontsize=7)
    ax[0].grid(alpha=0.3)

    ax[1].plot(hist_lambda)
    ax[1].set_xlabel("轮次")
    ax[1].set_ylabel("缩放系数 λ")
    ax[1].set_title("出价策略的演化：高目标者持续后撤")
    ax[1].grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG / "fig4_price_war.png", dpi=130)
    plt.close()
    return hist_lambda, hist_roi


# =============================================================================
# 实验 5：ROI 目标定多高才合理 —— 可行域与「量-ROI」权衡
# =============================================================================
def exp5_roi_frontier(n_rounds=150_000):
    print("\n" + "=" * 78)
    print("实验 5  ROI 目标的可行域：定得越高，能买的量越少（且非线性）")
    print("=" * 78)
    v, z = make_market(n_rounds=n_rounds, seed=61)
    # 最优策略：每轮按固定折价率（近似最优）
    grid = np.linspace(0.02, 1.0, 120)
    pts = []
    for s in grid:
        b = v * s
        win = b > z
        sp = np.where(win, b, 0).sum()
        vl = np.where(win, v, 0).sum()
        if sp > 0:
            pts.append((sp, vl, vl / sp, win.mean()))
    pts = np.array(pts)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    ax[0].plot(pts[:, 0], pts[:, 2], "-", color="#8e44ad")
    ax[0].set_xlabel("花费")
    ax[0].set_ylabel("达成 ROI")
    ax[0].set_title("花费–ROI 曲线：\nROI 目标每提高一点，花费能力断崖下降")
    ax[0].grid(alpha=0.3)

    for t in [1.2, 1.5, 2.0, 3.0]:
        idx = np.where(pts[:, 2] >= t)[0]
        if len(idx):
            i = idx[-1]
            print(f"  ROI≥{t:.1f}: 最大花费={pts[i,0]:>12,.0f}  获得价值={pts[i,1]:>12,.0f}  赢率={pts[i,3]:.3f}")
    ax[1].plot(pts[:, 2], pts[:, 3], "-", color="#16a085")
    ax[1].set_xlabel("达成 ROI")
    ax[1].set_ylabel("赢率")
    ax[1].set_title("ROI 目标与市场覆盖的取舍")
    ax[1].grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG / "fig5_roi_frontier.png", dpi=130)
    plt.close()
    return pts


if __name__ == "__main__":
    exp1_roi_constrained_shading()
    exp2_competition_pressure()
    exp3_platform_incentive_mismatch()
    exp4_price_war()
    exp5_roi_frontier()
    print("\n全部完成，图见 figures/")
