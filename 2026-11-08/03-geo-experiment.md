# arXiv 论文记录

> 查询：geo experiment · 共 2 篇 · 生成 2026-11-08T14:43:16+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [Robust Causal Inference for Incremental Return on Ad Spend with Randomized Paired Geo Experiments](https://arxiv.org/abs/1908.02922) | stat.ME | 2019-08-08 | [abs](https://arxiv.org/abs/1908.02922) · [pdf](https://arxiv.org/pdf/1908.02922) |
| 2 | [Trimmed Match Design for Randomized Paired Geo Experiments](https://arxiv.org/abs/2105.07060) | stat.ME | 2021-05-14 | [abs](https://arxiv.org/abs/2105.07060) · [pdf](https://arxiv.org/pdf/2105.07060) |

## 摘要

### 1. Robust Causal Inference for Incremental Return on Ad Spend with Randomized Paired Geo Experiments

- 作者：Aiyou Chen, Timothy C. Au
- 领域：`stat.ME`（全部：stat.ME）
- 发布：2019-08-08 · 更新：2021-06-06
- 链接：https://arxiv.org/abs/1908.02922 · PDF：https://arxiv.org/pdf/1908.02922
- 期刊/会议：Annals of Applied Statistics, 2022
- 入库：2026-11-08T14:43:16+08:00

> Evaluating the incremental return on ad spend (iROAS) of a prospective online marketing strategy (i.e., the ratio of the strategy's causal effect on some response metric of interest relative to its causal effect on the ad spend) has become increasingly more important. Although randomized ``geo experiments'' are frequently employed for this evaluation, obtaining reliable estimates of iROAS can be challenging as oftentimes only a small number of highly heterogeneous units are used. Moreover, advertisers frequently impose budget constraints on their ad spends, which further complicates causal inference by introducing interference between the experimental units. In this paper, we formulate a novel statistical framework for inferring the iROAS of online advertising from randomized paired geo experiment which further motivates and provides new insights into Rosenbaum's arguments on instrumental variables, and we propose and develop a robust, distribution-free and interpretable estimator ``Trimmed Match'', as well as a data-driven choice of the tuning parameter which may be of independent interest. We investigate the sensitivity of Trimmed Match to some violations of its assumptions and show that it can be more efficient than some alternative estimators based on simulated data. We then demonstrate its practical utility with real case studies.

### 2. Trimmed Match Design for Randomized Paired Geo Experiments

- 作者：Aiyou Chen, Marco Longfils, Nicolas Remy
- 领域：`stat.ME`（全部：stat.ME, stat.AP）
- 发布：2021-05-14 · 更新：2021-05-19
- 链接：https://arxiv.org/abs/2105.07060 · PDF：https://arxiv.org/pdf/2105.07060
- 备注：19 pages, 11 figures
- 入库：2026-11-08T14:43:16+08:00

> How to measure the incremental Return On Ad Spend (iROAS) is a fundamental problem for the online advertising industry. A standard modern tool is to run randomized geo experiments, where experimental units are non-overlapping ad-targetable geographical areas (Vaver & Koehler 2011). However, how to design a reliable and cost-effective geo experiment can be complicated, for example: 1) the number of geos is often small, 2) the response metric (e.g. revenue) across geos can be very heavy-tailed due to geo heterogeneity, and furthermore 3) the response metric can vary dramatically over time. To address these issues, we propose a robust nonparametric method for the design, called Trimmed Match Design (TMD), which extends the idea of Trimmed Match (Chen & Au 2019) and furthermore integrates the techniques of optimal subset pairing and sample splitting in a novel and systematic manner. Some simulation and real case studies are presented. We also point out a few open problems for future research.
