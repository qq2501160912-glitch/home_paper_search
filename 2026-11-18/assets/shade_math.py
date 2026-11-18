"""解析量级：竞争价分布族 -> 赢率弹性 eps -> 最优折价因子 s* = eps/(1+eps)。

对应报告第 1.2 节表 1-1、第 2.3 节表 2-1。
只依赖 Python 标准库。运行：python3 shade_math.py
"""
import math
from statistics import NormalDist

ND = NormalDist()


def eps_uniform(b, M):
    """G = U[0,M] => eps 恒为 1。"""
    return 1.0


def eps_uniform_ipv(b, n_opponents):
    """G = F^(n-1)，F = U[0,1] => eps 恒为 n-1（经典结果 b*=(n-1)/n v）。"""
    return float(n_opponents)


def eps_pareto(b, xm, alpha):
    """G = 1-(xm/b)^alpha，b>xm。令 t=xm/b，则 eps = alpha*t^alpha/(1-t^alpha)。"""
    if b <= xm:
        return float('inf')
    t = xm / b
    return alpha * t ** alpha / (1 - t ** alpha)


def eps_lognormal(b, mu, sigma):
    """G = Phi((ln b - mu)/sigma)，则 eps = phi(z)/(sigma*Phi(z))。"""
    if b <= 0:
        return 0.0
    z = (math.log(b) - mu) / sigma
    return ND.pdf(z) / (sigma * ND.cdf(z))


def eps_exp(b, theta):
    """G = 1-exp(-b/theta)，则 eps = (b/theta)*exp(-b/theta)/(1-exp(-b/theta))。"""
    x = b / theta
    return x * math.exp(-x) / (1 - math.exp(-x))


def shade(e):
    return e / (1 + e)


print('== 1) 弹性 -> 折价因子（表 1-1）')
for e in (0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 9.0):
    print('  eps=%-4.1f  s*=%.3f  ds/deps=%.3f' % (e, shade(e), 1 / (1 + e) ** 2))

print('\n== 2) 均匀竞争价 U[0,M]：eps 恒为 1，s* 恒为 0.5（与 M 无关）')
for frac in (0.25, 0.5, 0.75, 0.9):
    e = eps_uniform(frac, 1.0)
    print('  b/M=%.2f  eps=%.2f  s*=%.2f' % (frac, e, shade(e)))

print('\n== 3) 均匀 IPV、n 个对手：s*=(n-1)/n；期望成交价 (n-1)/(n+1)')
for n in (1, 2, 3, 5, 10, 20):
    e = eps_uniform_ipv(0, n)
    print('  n=%-3d  eps=%-4.0f  s*=%.3f  E[price]=%.3f' % (n, e, shade(e), (n - 1) / (n + 1)))

print('\n== 4) Pareto：eps 随 b 递减（从 inf 到 0），s* 从 1 降到 0')
for alpha in (1.0, 2.0, 3.0):
    row = []
    for mult in (1.1, 2.0, 5.0, 20.0):
        e = eps_pareto(mult, 1.0, alpha)
        row.append('b=%gxm: eps=%.2f s*=%.2f' % (mult, e, shade(e)))
    print('  alpha=%.1f  ' % alpha + ' | '.join(row))

def G_lognormal(b, mu, sigma):
    return ND.cdf((math.log(b) - mu) / sigma) if b > 0 else 0.0


def opt_shade(v, mu, sigma, steps=200):
    """网格搜索真实最优折价（含边界解），不是把公式套在任意点上。"""
    best_s, best_val = 0.5, -1e18
    for i in range(1, steps + 1):
        s = i / steps
        val = (v - s * v) * G_lognormal(s * v, mu, sigma)
        if val > best_val:
            best_s, best_val = s, val
    return best_s


print('\n== 5) 对数正态：价值处在竞争价分布不同分位时的最优折价（表 2-1，网格搜索）')
for sigma in (0.3, 0.6, 1.0, 1.5):
    row = []
    for q in (0.50, 0.70, 0.85, 0.95):
        v = math.exp(ND.inv_cdf(q) * sigma)
        row.append('q%.2f: s*=%.2f' % (q, opt_shade(v, 0.0, sigma)))
    print('  sigma=%.1f  ' % sigma + ' | '.join(row))

print('\n== 5b) 对照：把公式 eps/(1+eps) 直接套在"分位点"上会错多少')
for sigma in (0.6, 1.5):
    for q in (0.50, 0.95):
        b = math.exp(ND.inv_cdf(q) * sigma)      # 若在此点出价，G=q
        wrong = shade(eps_lognormal(b, 0.0, sigma))
        right = opt_shade(b, 0.0, sigma)
        print('  sigma=%.1f q=%.2f  公式在分位点上=%.2f  真实最优=%.2f' % (sigma, q, wrong, right))

print('\n== 6) 指数分布：eps 从 1 起随 b 上升，s* 从 0.5 趋于 1')
for x in (0.1, 0.5, 1.0, 3.0, 10.0):
    e = eps_exp(x, 1.0)
    print('  b/theta=%-4.1f  eps=%.2f  s*=%.2f' % (x, e, shade(e)))
