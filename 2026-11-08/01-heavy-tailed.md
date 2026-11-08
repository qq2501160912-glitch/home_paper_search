# arXiv 论文记录

> 查询：heavy-tailed · 共 2 篇 · 生成 2026-11-08T14:38:54+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [STATE: A Robust ATE Estimator of Heavy-Tailed Metrics for Variance Reduction in Online Controlled Experiments](https://arxiv.org/abs/2407.16337) | cs.LG | 2024-07-23 | [abs](https://arxiv.org/abs/2407.16337) · [pdf](https://arxiv.org/pdf/2407.16337) |
| 2 | [Variance Reduction for Heavy-Tailed Monetization Metrics in Ranking Experiments via Post-Stratification](https://arxiv.org/abs/2606.04110) | cs.LG | 2026-06-02 | [abs](https://arxiv.org/abs/2606.04110) · [pdf](https://arxiv.org/pdf/2606.04110) |

## 摘要

### 1. STATE: A Robust ATE Estimator of Heavy-Tailed Metrics for Variance Reduction in Online Controlled Experiments

- 作者：Hao Zhou, Kun Sun, Shaoming Li, Yangfeng Fan, Guibin Jiang, Jiaqi Zheng, Tao Li
- 领域：`cs.LG`（全部：cs.LG）
- 发布：2024-07-23 · 更新：2024-07-23
- 链接：https://arxiv.org/abs/2407.16337 · PDF：https://arxiv.org/pdf/2407.16337
- 备注：Accepted by KDD 2024
- 入库：2026-11-08T14:38:54+08:00

> Online controlled experiments play a crucial role in enabling data-driven decisions across a wide range of companies. Variance reduction is an effective technique to improve the sensitivity of experiments, achieving higher statistical power while using fewer samples and shorter experimental periods. However, typical variance reduction methods (e.g., regression-adjusted estimators) are built upon the intuitional assumption of Gaussian distributions and cannot properly characterize the real business metrics with heavy-tailed distributions. Furthermore, outliers diminish the correlation between pre-experiment covariates and outcome metrics, greatly limiting the effectiveness of variance reduction. In this paper, we develop a novel framework that integrates the Student's t-distribution with machine learning tools to fit heavy-tailed metrics and construct a robust average treatment effect estimator in online controlled experiments, which we call STATE. By adopting a variational EM method to optimize the loglikehood function, we can infer a robust solution that greatly eliminates the negative impact of outliers and achieves significant variance reduction. Moreover, we extend the STATE method from count metrics to ratio metrics by utilizing linear transformation that preserves unbiased estimation, whose variance reduction is more complex but less investigated in existing works. Finally, both simulations on synthetic data and long-term empirical results on Meituan experiment platform demonstrate the effectiveness of our method. Compared with the state-of-the-art estimators (CUPAC/MLRATE), STATE achieves over 50% variance reduction, indicating it can reach the same statistical power with only half of the observations, or half the experimental duration.

### 2. Variance Reduction for Heavy-Tailed Monetization Metrics in Ranking Experiments via Post-Stratification

- 作者：Neeti Pokharna, Olivier Jeunen, Yatharth Saraf, Aleksei Ustimenko
- 领域：`cs.LG`（全部：cs.LG, stat.ML）
- 发布：2026-06-02 · 更新：2026-06-02
- 链接：https://arxiv.org/abs/2606.04110 · PDF：https://arxiv.org/pdf/2606.04110
- 备注：Accepted as Industry Track paper in the 2026 ACM SIGIR Conference on Research and Development in Information Retrieval
- DOI：10.1145/3805712.3808428
- 入库：2026-11-08T14:38:54+08:00

> Online evaluation of ranking and retrieval systems often relies on downstream monetization metrics such as app revenue or creator earnings. These metrics are typically heavy-tailed, with a small fraction of users dominating both mean and variance, leading to low statistical power and unreliable conclusions in A/B experiments -- especially under limited traffic. We present a practical framework for variance reduction in online experiments by combining post-stratification with CUPED. Our approach leverages pre-experiment covariates to improve the sensitivity of monetization experiments without requiring additional traffic. Deployed at ShareChat across ranking-driven monetization experiments, the method substantially reduces variance and improves decision stability, achieving equivalent statistical confidence with ~45\% less traffic than standard metrics. We further discuss practical design choices, guardrails, and limitations, providing guidance on when post-stratification is appropriate for real-world information retrieval and Recommendation systems.
