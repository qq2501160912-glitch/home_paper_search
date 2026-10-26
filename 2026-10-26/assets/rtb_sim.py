"""Numerical experiments for the RTB buyer-side survey (2026-10-26).

Runs four mechanism-level checks on synthetic data. Deterministic (fixed seeds).

  A. Conservative bid shading under noisy valuation + landscape estimates
  B. Dual-gradient pacing with vs without a hard budget cut-off
  C. Calibration of a pCVR model: AUC vs calibration error and realised CPI
  D. Cross-channel budget allocation: fixed split vs adaptive split vs oracle
"""

import json

import numpy as np

RESULT = {}

SHADE = 0.5          # best-response shading for H ~ U[0, v]


def _surplus(v, bid, pay):
    return np.where(pay < bid, v - pay, 0.0)


# ---------------------------------------------------------------- A. shading
def experiment_shading(seed=7, n=2_000_000):
    rng = np.random.default_rng(seed)
    v = rng.lognormal(0.0, 0.5, n)          # true value
    h = rng.lognormal(-0.3, 0.6, n)         # true highest competing bid

    sigma_v, sigma_h = 0.25, 0.45           # estimation noise (log scale)
    v_hat = v * np.exp(rng.normal(0, sigma_v, n))
    h_hat = h * np.exp(rng.normal(0, sigma_h, n))

    def run(strategy, raw_bid, h_landscape):
        if strategy == "bayes":
            b = SHADE * raw_bid + (1 - SHADE) * h_landscape
        else:
            b = raw_bid
        win = h < b
        return dict(win_rate=round(float(win.mean()), 4),
                    true_surplus=round(float(_surplus(v, b, h).mean()), 4),
                    mean_paid=round(float(np.where(win, h, 0).mean()), 4),
                    overpay_per_win=round(
                        float(np.where(win, b - h, 0.0).sum() /
                              max(win.sum(), 1)), 4))

    rows = [
        dict(value="noisy", landscape="estimated", strategy="bayes",
             **run("bayes", v_hat, h_hat)),
        dict(value="noisy", landscape="true", strategy="bayes",
             **run("bayes", v_hat, h)),
        dict(value="exact", landscape="estimated", strategy="bayes",
             **run("bayes", v, h_hat)),
        dict(value="exact", landscape="true", strategy="bayes",
             **run("bayes", v, h)),
        dict(value="noisy", landscape="none", strategy="truthful",
             **run("truthful", v_hat, None)),
        dict(value="exact", landscape="none", strategy="truthful",
             **run("truthful", v, None)),
    ]
    RESULT["A_shading"] = dict(n=n, shade=SHADE, sigma_v=sigma_v,
                               sigma_h=sigma_h, rows=rows)


# ---------------------------------------------------------------- B. pacing
def experiment_pacing(seed=11, m=40_000, B=1000.0):
    """Dual-gradient pacing (Balseiro-Gur style) in a first-price market."""
    rng = np.random.default_rng(seed)
    v = rng.lognormal(0.0, 0.5, m)
    h = rng.lognormal(-0.3, 0.6, m)
    eta = 1.0 / np.sqrt(m)

    def simulate(hard_cap):
        alpha, spend, wins, value = 0.0, 0.0, 0, 0.0
        curve = []
        for j in range(m):
            if hard_cap and spend >= B:
                break
            b = (SHADE * v[j] + (1 - SHADE) * h[j]) / (1.0 + alpha)
            pay = 0.0
            if h[j] < b:
                pay = min(b, B - spend) if hard_cap else b
                spend += pay
                wins += 1
                value += v[j]
            alpha = max(alpha + eta * pay - eta * (B / m), 0.0)
            if j in (0, m // 2, m - 1):
                curve.append([j + 1, round(spend, 2), round(alpha, 5)])
        return dict(hard_cap=hard_cap, spend=round(spend, 2), wins=wins,
                    overspend_x=round(spend / B, 3), alpha=round(alpha, 5),
                    curve=curve)

    RESULT["B_pacing"] = dict(m=m, B=B, eta_E=round(float(eta), 6),
                              runs=[simulate(False), simulate(True)])


# ---------------------------------------------------------------- C. calibration
def experiment_calibration(seed=3, n=400_000, bins=10, cpa_target=50.0):
    rng = np.random.default_rng(seed)
    score = rng.normal(0, 1, n)
    true_p = 1 / (1 + np.exp(-(-6.2 + 2.2 * score)))
    conv = rng.random(n) < true_p

    prod = 1 / (1 + np.exp(-(-6.2 + 0.9 * score)))
    models = {
        "production (rank ok, scale off)": prod,
        "weaker rank, 2x scale": prod * 2.0,
        "weaker rank, 0.5x scale": prod * 0.5,
    }

    def auc_of(p):
        order = np.argsort(p)
        y = conv[order]
        ranks = np.arange(1, n + 1)
        n_pos, n_neg = y.sum(), n - y.sum()
        return (ranks[y].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)

    def ece_of(p):
        idx = np.argsort(p)
        ece = 0.0
        for c in np.array_split(idx, bins):
            if len(c):
                ece += len(c) / n * abs(p[c].mean() - conv[c].mean())
        return ece

    rows = []
    for name, p in models.items():
        order = np.argsort(-p)
        won = order[:119]                     # fixed campaign size
        true_convs = conv[won].sum()
        # in CVR units the campaign pays its own pCVR (first price, per click)
        paid = p[won].sum()
        rows.append(dict(model=name, auc=round(float(auc_of(p)), 4),
                         ece=round(float(ece_of(p)), 4),
                         mean_pcr=round(float(p.mean()), 5),
                         true_pcr=round(float(true_p.mean()), 5),
                         scale=round(float(p.mean() / true_p.mean()), 3),
                         true_convs=int(true_convs),
                         paid_per_conv=round(float(paid / max(true_convs, 1)), 4),
                         budget_units=round(float(true_convs * cpa_target), 1),
                         spend_units=round(float(paid * cpa_target), 1)))
    RESULT["C_calibration"] = dict(n=n, bins=bins, cpa_target=cpa_target,
                                   n_won=119, rows=rows)


# ---------------------------------------------------------------- D. allocation
def experiment_allocation(seed=5, channels=4, rounds=400, repeats=400):
    """Cross-channel budget allocation against a drifting optimum.

    y_i(x) = A_i (1 - exp(-lam_i x_i)) - kappa (x_i - x*_i)^2,  sum(x) = 1.
    Compares a fixed equal split against a controller that learns each
    channel's marginal return from noisy feedback.
    """
    rng = np.random.default_rng(seed)
    kappa = 6.0
    fixed, adaptive, oracle = [], [], []
    for _ in range(repeats):
        x_star = rng.dirichlet(np.full(channels, 4.0))
        A = rng.uniform(2.0, 4.0, channels)
        lam = rng.uniform(1.0, 3.0, channels)

        def surplus(x, noise=0.0):
            y = A * (1 - np.exp(-lam * x)) - kappa * (x - x_star) ** 2
            return float(y.sum() + noise)

        fixed.append(surplus(np.ones(channels) / channels))

        x = np.ones(channels) / channels
        eta, lr = 0.35, 0.9
        grad_hat = np.zeros(channels)
        for _ in range(rounds):
            m = A * lam * np.exp(-lam * x) - 2 * kappa * (x - x_star)
            grad_hat = lr * grad_hat + (1 - lr) * (m + rng.normal(0, 0.05, channels))
            x = x * np.exp(eta * grad_hat)
            x = np.clip(x, 1e-3, None)
            x = x / x.sum()
        adaptive.append(surplus(x))
        oracle.append(surplus(x_star))

    RESULT["D_allocation"] = dict(channels=channels, rounds=rounds,
                                  repeats=repeats, kappa=kappa,
                                  mean_surplus_fixed=round(float(np.mean(fixed)), 4),
                                  mean_surplus_adaptive=round(float(np.mean(adaptive)), 4),
                                  mean_surplus_oracle=round(float(np.mean(oracle)), 4),
                                  adaptive_share_of_oracle=round(
                                      float(np.mean(adaptive) / np.mean(oracle)), 4),
                                  fixed_share_of_oracle=round(
                                      float(np.mean(fixed) / np.mean(oracle)), 4))


if __name__ == "__main__":
    experiment_shading()
    experiment_pacing()
    experiment_calibration()
    experiment_allocation()
    print(json.dumps(RESULT, ensure_ascii=False, indent=2))
