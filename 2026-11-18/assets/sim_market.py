"""一价竞价市场模拟：市场级信息能识别什么、值多少钱（纯标准库，可直接运行）。

对应报告第 8 章。三个实验：
  E1 折价决策：不同信息/估计方案相对 oracle 的期望 surplus
  E2 因子系数偏误：潜在竞争价 H vs 观测最低竞胜价 m=max(H,floor) 的回归差异
  E3 竞争水平 -> 最优折价因子 的弹性

模型：
  H ~ LogNormal(mu_c, sigma), mu_c = a0 + a1*log(floor_c) + a2*demand_c + a3*log(1+slots_c)
  m = max(H, floor_c)
  v ~ LogNormal(nu0, nu1) 独立于 H
  出价 b = s*v，竞胜当且仅当 b >= m

运行：python3 sim_market.py
"""
import math
import random
from statistics import NormalDist

ND = NormalDist()
RNG = random.Random(20261118)

A0, A1, A2, A3 = math.log(1.6), 0.45, 0.35, 0.10
SIGMA = 0.55
NU0, NU1 = math.log(2.2), 0.75
N_CELL = 24
N_AUC = 240000
GRID = [i / 100 for i in range(5, 101, 5)]


def ln(x):
    return math.log(x) if x > 0 else float('-inf')


cells = []
for c in range(N_CELL):
    floor = math.exp(RNG.uniform(math.log(0.4), math.log(3.0)))
    demand = RNG.gauss(0, 1)
    slots = RNG.choice([1, 1, 1, 2, 3])
    mu = A0 + A1 * math.log(floor) + A2 * demand + A3 * math.log(1 + slots)
    cells.append(dict(id=c, floor=floor, demand=demand, slots=slots, mu=mu))

data = []
for t in range(N_AUC):
    c = cells[RNG.randrange(N_CELL)]
    H = math.exp(c['mu'] + SIGMA * RNG.gauss(0, 1))
    data.append((c['id'], math.exp(NU0 + NU1 * RNG.gauss(0, 1)), max(H, c['floor']), H))


def G_true(c, b):
    if b <= 0 or b < c['floor']:
        return 0.0
    return ND.cdf((ln(b) - c['mu']) / SIGMA)


def surplus_true(c, v, s):
    return (v - s * v) * G_true(c, s * v)


def grid_opt(v, G):
    best_s, best = 0.5, -1e18
    for s in GRID:
        val = (v - s * v) * G(s * v)
        if val > best:
            best_s, best = s, val
    return best_s


def eval_policy(policy, sample):
    tot = orc = 0.0
    for (cid, v, m, H) in sample:
        c = cells[cid]
        tot += surplus_true(c, v, policy(c, v))
        orc += max(surplus_true(c, v, s) for s in GRID)
    return tot / len(sample), tot / orc


def pava(bins):
    blocks = [[c, e, w] for (c, e, w) in bins]
    i = 0
    while i < len(blocks) - 1:
        if blocks[i][1] > blocks[i + 1][1]:
            c1, e1, w1 = blocks[i]
            c2, e2, w2 = blocks[i + 1]
            w = w1 + w2
            blocks[i:i + 2] = [[(c1 * w1 + c2 * w2) / w, (e1 * w1 + e2 * w2) / w, w]]
            i = max(i - 1, 0)
        else:
            i += 1
    return [(c, e) for c, e, w in blocks]


def interp(pts):
    def G(b):
        if b <= pts[0][0]:
            return 0.0
        if b >= pts[-1][0]:
            return pts[-1][1]
        for k in range(1, len(pts)):
            if b <= pts[k][0]:
                x0, y0 = pts[k - 1]
                x1, y1 = pts[k]
                return y0 + (y1 - y0) * (b - x0) / (x1 - x0)
        return pts[-1][1]
    return G


def ols3(rows, yfun):
    X = [(1.0, math.log(cells[r[0]]['floor']), cells[r[0]]['demand']) for r in rows]
    y = [yfun(r) for r in rows]
    n = len(rows)
    XtX = [[sum(X[i][a] * X[i][b] for i in range(n)) for b in range(3)] for a in range(3)]
    Xty = [sum(X[i][a] * y[i] for i in range(n)) for a in range(3)]
    M = [XtX[i][:] + [1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    for col in range(3):
        p = max(range(col, 3), key=lambda r: abs(M[r][col]))
        M[col], M[p] = M[p], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(3):
            if r != col:
                f = M[r][col]
                M[r] = [M[r][k] - f * M[col][k] for k in range(6)]
    inv = [row[3:] for row in M]
    return [sum(inv[a][b] * Xty[b] for b in range(3)) for a in range(3)]


def run():
    train, test = data[:80000], data[80000:140000]
    by_cell = {}
    for row in train:
        by_cell.setdefault(row[0], []).append(row)

    print('E1 折价决策（测试集 6 万次拍卖，surplus 按真实分布结算）')
    print('方案\t\t\t\t期望surplus\t占oracle\t平均折价因子')

    # (a) oracle
    pol_oracle = lambda c, v: grid_opt(v, lambda b: G_true(c, b))

    # (b) 完整 m：逐 cell 经验分布
    emp = {}
    for cid, rows in by_cell.items():
        emp[cid] = interp(sorted((r[2], (k + 1) / len(rows)) for k, r in enumerate(sorted(rows, key=lambda x: x[2]))))
    pol_full = lambda c, v: grid_opt(v, emp[c['id']])

    # (c) 只有胜负：10% 随机折价探索 + 保序回归
    obs = {}
    for cid, rows in by_cell.items():
        for (_, v, m, H) in rows:
            s = RNG.choice(GRID) if RNG.random() < 0.10 else 0.6
            b = s * v
            obs.setdefault(cid, []).append((b, 1 if b >= m else 0))
    iso = {}
    for cid, rows in obs.items():
        rows.sort()
        bins = []
        for k in range(20):
            seg = rows[k * len(rows) // 20:(k + 1) * len(rows) // 20]
            if seg:
                bins.append((sum(x[0] for x in seg) / len(seg),
                             sum(x[1] for x in seg) / len(seg), len(seg)))
        iso[cid] = interp(pava(bins))
    pol_wl = lambda c, v: grid_opt(v, iso[c['id']])

    # (d) 只有胜负、且价值无差异（所有 v 相同）：b 只有一点，G 不可识别
    const_G = {}
    for cid, rows in by_cell.items():
        wins = sum(1 for (_, v, m, H) in rows if 0.6 * 2.2 >= m)
        const_G[cid] = wins / len(rows)
    pol_const = lambda c, v: grid_opt(v, lambda b: const_G[c['id']] if b >= 0.6 * 2.2 else 0.0)

    # (e) 固定折价
    pol_fix = lambda c, v: 0.6

    for name, pol in [('oracle（真实竞争分布）', pol_oracle),
                      ('full_m（每次都有最低竞胜价）', pol_full),
                      ('winloss（仅胜负+10%探索）', pol_wl),
                      ('winloss_constv（价值无差异）', pol_const),
                      ('fixed_s=0.6（固定折价）', pol_fix)]:
        s, r = eval_policy(pol, test)
        ss = [pol(cells[r0[0]], r0[1]) for r0 in test[:30000]]
        print('%-32s\t%.4f\t\t%.2f%%\t\t%.3f' % (name, s, 100 * r, sum(ss) / len(ss)))

    print('\nE2 因子系数（因变量 log 竞争价；解释变量：常数, log floor, demand）')
    print('  真实 mu 设定         : %.3f, %.3f, %.3f' % (A0, A1, A2))
    print('  潜在 H 回归（正确）   : %.3f, %.3f, %.3f' % tuple(ols3(train, lambda r: math.log(r[3]))))
    print('  观测 m=max(H,f) 回归  : %.3f, %.3f, %.3f' % tuple(ols3(train, lambda r: math.log(r[2]))))
    loss_rows = [r for r in train if 0.6 * r[1] < r[2]]
    print('  只保留输的样本        : %.3f, %.3f, %.3f' % tuple(ols3(loss_rows, lambda r: math.log(r[2]))))

    print('\nE3 竞争位置与竞争水平 -> 最优折价因子')
    # (a) 位置效应：把自己的价值放在该 cell 竞争价分布的 q 分位
    qs = (0.50, 0.70, 0.85, 0.95)
    pos = {}
    for q in qs:
        vals = []
        for c in cells:
            v = math.exp(c['mu'] + SIGMA * ND.inv_cdf(q))
            if v <= c['floor']:
                continue
            vals.append(grid_opt(v, lambda b: G_true(c, b)))
        pos[q] = sum(vals) / len(vals) if vals else float('nan')
        print('  v 位于竞争价 P%-3.0f 处：平均 s*=%.3f' % (100 * q, pos[q]))
    print('  位置从 P50 升到 P95，s* 变化 %+.3f' % (pos[0.95] - pos[0.50]))

    # (b) 水平效应：价值固定（=1.5*floor），把该 cell 的竞争价水平翻倍
    base, dbl = [], []
    for c in cells:
        v = 1.5 * c['floor']
        base.append(grid_opt(v, lambda b: G_true(c, b)))
        c2 = dict(c)
        c2['mu'] = c['mu'] + math.log(2)
        dbl.append(grid_opt(v, lambda b: G_true(c2, b)))
    mb, md = sum(base) / len(base), sum(dbl) / len(dbl)
    print('  价值固定、竞争价中位数翻倍：平均 s* %.3f -> %.3f（%+.3f）' % (mb, md, md - mb))


if __name__ == '__main__':
    run()
