# arXiv 论文记录

> 查询：interference · 共 9 篇 · 生成 2026-11-08T14:39:02+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [Causal Inference in the Presence of Interference in Sponsored Search Advertising](https://arxiv.org/abs/2010.07458) | cs.AI | 2020-10-15 | [abs](https://arxiv.org/abs/2010.07458) · [pdf](https://arxiv.org/pdf/2010.07458) |
| 2 | [Reducing Marketplace Interference Bias Via Shadow Prices](https://arxiv.org/abs/2205.02274) | math.OC | 2022-05-04 | [abs](https://arxiv.org/abs/2205.02274) · [pdf](https://arxiv.org/pdf/2205.02274) |
| 3 | [Reducing Interference Bias in Online Marketplace Pricing Experiments](https://arxiv.org/abs/2004.12489) | stat.ME | 2020-04-26 | [abs](https://arxiv.org/abs/2004.12489) · [pdf](https://arxiv.org/pdf/2004.12489) |
| 4 | [Interference, Bias, and Variance in Two-Sided Marketplace Experimentation: Guidance for Platforms](https://arxiv.org/abs/2104.12222) | stat.ME | 2021-04-25 | [abs](https://arxiv.org/abs/2104.12222) · [pdf](https://arxiv.org/pdf/2104.12222) |
| 5 | [Pricing Experiments in Matching Marketplaces under Interference: Designs and Estimators](https://arxiv.org/abs/2502.18839) | math.OC | 2025-02-26 | [abs](https://arxiv.org/abs/2502.18839) · [pdf](https://arxiv.org/pdf/2502.18839) |
| 6 | [Cluster-Randomized Trials with Cross-Cluster Interference](https://arxiv.org/abs/2310.18836) | stat.ME | 2023-10-28 | [abs](https://arxiv.org/abs/2310.18836) · [pdf](https://arxiv.org/pdf/2310.18836) |
| 7 | [Heterogeneous Treatment and Spillover Effects under Clustered Network Interference](https://arxiv.org/abs/2008.00707) | stat.ME | 2020-08-03 | [abs](https://arxiv.org/abs/2008.00707) · [pdf](https://arxiv.org/pdf/2008.00707) |
| 8 | [Estimating Average Causal Effects Under General Interference, with Application to a Social Network Experiment](https://arxiv.org/abs/1305.6156) | math.ST | 2013-05-27 | [abs](https://arxiv.org/abs/1305.6156) · [pdf](https://arxiv.org/pdf/1305.6156) |
| 9 | [Design and analysis of experiments in networks: Reducing bias from interference](https://arxiv.org/abs/1404.7530) | stat.ME | 2014-04-29 | [abs](https://arxiv.org/abs/1404.7530) · [pdf](https://arxiv.org/pdf/1404.7530) |

## 摘要

### 1. Causal Inference in the Presence of Interference in Sponsored Search Advertising

- 作者：Razieh Nabi, Joel Pfeiffer, Murat Ali Bayir, Denis Charles, Emre Kıcıman
- 领域：`cs.AI`（全部：cs.AI, cs.IR）
- 发布：2020-10-15 · 更新：2020-10-15
- 链接：https://arxiv.org/abs/2010.07458 · PDF：https://arxiv.org/pdf/2010.07458
- 期刊/会议：Special issue on Causal Inference and Machine Learning with Network Data, Frontiers in Big Data, 2022
- DOI：10.3389/fdata.2022.888592
- 入库：2026-11-08T14:39:02+08:00

> In classical causal inference, inferring cause-effect relations from data relies on the assumption that units are independent and identically distributed. This assumption is violated in settings where units are related through a network of dependencies. An example of such a setting is ad placement in sponsored search advertising, where the clickability of a particular ad is potentially influenced by where it is placed and where other ads are placed on the search result page. In such scenarios, confounding arises due to not only the individual ad-level covariates but also the placements and covariates of other ads in the system. In this paper, we leverage the language of causal inference in the presence of interference to model interactions among the ads. Quantification of such interactions allows us to better understand the click behavior of users, which in turn impacts the revenue of the host search engine and enhances user satisfaction. We illustrate the utility of our formalization through experiments carried out on the ad placement system of the Bing search engine.

### 2. Reducing Marketplace Interference Bias Via Shadow Prices

- 作者：Ido Bright, Arthur Delarue, Ilan Lobel
- 领域：`math.OC`（全部：math.OC, econ.EM）
- 发布：2022-05-04 · 更新：2024-03-14
- 链接：https://arxiv.org/abs/2205.02274 · PDF：https://arxiv.org/pdf/2205.02274
- 备注：v4: additional results on asymmetric experiments, trimmed exposition
- 入库：2026-11-08T14:39:02+08:00

> Marketplace companies rely heavily on experimentation when making changes to the design or operation of their platforms. The workhorse of experimentation is the randomized controlled trial (RCT), or A/B test, in which users are randomly assigned to treatment or control groups. However, marketplace interference causes the Stable Unit Treatment Value Assumption (SUTVA) to be violated, leading to bias in the standard RCT metric. In this work, we propose techniques for platforms to run standard RCTs and still obtain meaningful estimates despite the presence of marketplace interference. We specifically consider a generalized matching setting, in which the platform explicitly matches supply with demand via a linear programming algorithm. Our first proposal is for the platform to estimate the value of global treatment and global control via optimization. We prove that this approach is unbiased in the fluid limit. Our second proposal is to compare the average shadow price of the treatment and control groups rather than the total value accrued by each group. We prove that this technique corresponds to the correct first-order approximation (in a Taylor series sense) of the value function of interest even in a finite-size system. We then use this result to prove that, under reasonable assumptions, our estimator is less biased than the RCT estimator. At the heart of our result is the idea that it is relatively easy to model interference in matching-driven marketplaces since, in such markets, the platform mediates the spillover.

### 3. Reducing Interference Bias in Online Marketplace Pricing Experiments

- 作者：David Holtz, Ruben Lobel, Inessa Liskovich, Sinan Aral
- 领域：`stat.ME`（全部：stat.ME, econ.EM, stat.AP）
- 发布：2020-04-26 · 更新：2020-04-26
- 链接：https://arxiv.org/abs/2004.12489 · PDF：https://arxiv.org/pdf/2004.12489
- 入库：2026-11-08T14:39:02+08:00

> Online marketplace designers frequently run A/B tests to measure the impact of proposed product changes. However, given that marketplaces are inherently connected, total average treatment effect estimates obtained through Bernoulli randomized experiments are often biased due to violations of the stable unit treatment value assumption. This can be particularly problematic for experiments that impact sellers' strategic choices, affect buyers' preferences over items in their consideration set, or change buyers' consideration sets altogether. In this work, we measure and reduce bias due to interference in online marketplace experiments by using observational data to create clusters of similar listings, and then using those clusters to conduct cluster-randomized field experiments. We provide a lower bound on the magnitude of bias due to interference by conducting a meta-experiment that randomizes over two experiment designs: one Bernoulli randomized, one cluster randomized. In both meta-experiment arms, treatment sellers are subject to a different platform fee policy than control sellers, resulting in different prices for buyers. By conducting a joint analysis of the two meta-experiment arms, we find a large and statistically significant difference between the total average treatment effect estimates obtained with the two designs, and estimate that 32.60% of the Bernoulli-randomized treatment effect estimate is due to interference bias. We also find weak evidence that the magnitude and/or direction of interference bias depends on extent to which a marketplace is supply- or demand-constrained, and analyze a second meta-experiment to highlight the difficulty of detecting interference bias when treatment interventions require intention-to-treat analysis.

### 4. Interference, Bias, and Variance in Two-Sided Marketplace Experimentation: Guidance for Platforms

- 作者：Hannah Li, Geng Zhao, Ramesh Johari, Gabriel Y. Weintraub
- 领域：`stat.ME`（全部：stat.ME, econ.EM）
- 发布：2021-04-25 · 更新：2021-04-25
- 链接：https://arxiv.org/abs/2104.12222 · PDF：https://arxiv.org/pdf/2104.12222
- 入库：2026-11-08T14:39:02+08:00

> Two-sided marketplace platforms often run experiments to test the effect of an intervention before launching it platform-wide. A typical approach is to randomize individuals into the treatment group, which receives the intervention, and the control group, which does not. The platform then compares the performance in the two groups to estimate the effect if the intervention were launched to everyone. We focus on two common experiment types, where the platform randomizes individuals either on the supply side or on the demand side. The resulting estimates of the treatment effect in these experiments are typically biased: because individuals in the market compete with each other, individuals in the treatment group affect those in the control group and vice versa, creating interference. We develop a simple tractable market model to study bias and variance in these experiments with interference. We focus on two choices available to the platform: (1) Which side of the platform should it randomize on (supply or demand)? (2) What proportion of individuals should be allocated to treatment? We find that both choices affect the bias and variance of the resulting estimators but in different ways. The bias-optimal choice of experiment type depends on the relative amounts of supply and demand in the market, and we discuss how a platform can use market data to select the experiment type. Importantly, we find in many circumstances, choosing the bias-optimal experiment type has little effect on variance. On the other hand, the choice of treatment proportion can induce a bias-variance tradeoff, where the bias-minimizing proportion increases variance. We discuss how a platform can navigate this tradeoff and best choose the treatment proportion, using a combination of modeling as well as contextual knowledge about the market, the risk of the intervention, and reasonable effect sizes of the intervention.

### 5. Pricing Experiments in Matching Marketplaces under Interference: Designs and Estimators

- 作者：Arthur Delarue, Kleanthis Karakolios
- 领域：`math.OC`（全部：math.OC）
- 发布：2025-02-26 · 更新：2025-02-26
- 链接：https://arxiv.org/abs/2502.18839 · PDF：https://arxiv.org/pdf/2502.18839
- 入库：2026-11-08T14:39:02+08:00

> Interference between treated and untreated units is a source of bias in marketplace experiments. In this paper, we specifically consider pricing interventions, in which a platform seeks to adjust base pricing levels at the marketplace level in order to increase demand. In a matching marketplace, this type of experiment leads to a crucial design question: should the platform match treated and untreated units differently because they paid different prices? We find that standard estimation techniques are biased, but the sign of this bias depends strongly on this design choice. Bias can be reduced by using the ``shadow price estimator'', which relies on the optimal dual solution of the platform's supply-demand matching problem -- especially when the platform chooses to ignore pricing differences at matching time. We validate our findings both theoretically in a fluid limit setting, and numerically in a finite-sample setting.

### 6. Cluster-Randomized Trials with Cross-Cluster Interference

- 作者：Michael P. Leung
- 领域：`stat.ME`（全部：stat.ME, econ.EM）
- 发布：2023-10-28 · 更新：2025-10-27
- 链接：https://arxiv.org/abs/2310.18836 · PDF：https://arxiv.org/pdf/2310.18836
- 入库：2026-11-08T14:39:02+08:00

> The literature on cluster-randomized trials typically allows for interference within but not across clusters. This may be implausible when units are irregularly distributed across space without well-separated communities, as clusters in such cases may not align with significant geographic, social, or economic divisions. This paper develops methods for reducing bias due to cross-cluster interference. We first propose an estimation strategy that excludes units not surrounded by clusters assigned to the same treatment arm. We show that this substantially reduces bias relative to conventional difference-in-means estimators without significant cost to variance. Second, we formally establish a bias-variance trade-off in the choice of clusters: constructing fewer, larger clusters reduces bias due to interference but increases variance. We provide a rule for choosing the number of clusters to balance the asymptotic orders of the bias and variance of our estimator. Finally, we consider unsupervised learning for cluster construction and provide theoretical guarantees for $k$-medoids.

### 7. Heterogeneous Treatment and Spillover Effects under Clustered Network Interference

- 作者：Falco J. Bargagli-Stoffi, Costanza Tortù, Laura Forastiere
- 领域：`stat.ME`（全部：stat.ME）
- 发布：2020-08-03 · 更新：2023-11-02
- 链接：https://arxiv.org/abs/2008.00707 · PDF：https://arxiv.org/pdf/2008.00707
- 入库：2026-11-08T14:39:02+08:00

> The bulk of causal inference studies rule out the presence of interference between units. However, in many real-world scenarios, units are interconnected by social, physical, or virtual ties, and the effect of the treatment can spill from one unit to other connected individuals in the network. In this paper, we develop a machine learning method that uses tree-based algorithms and a Horvitz-Thompson estimator to assess the heterogeneity of treatment and spillover effects with respect to individual, neighborhood, and network characteristics in the context of clustered networks and neighborhood interference within clusters. The proposed Network Causal Tree (NCT) algorithm has several advantages. First, it allows the investigation of the treatment effect heterogeneity, avoiding potential bias due to the presence of interference. Second, understanding the heterogeneity of both treatment and spillover effects can guide policy-makers in scaling up interventions, designing targeting strategies, and increasing cost-effectiveness. We investigate the performance of our NCT method using a Monte Carlo simulation study, and we illustrate its application to assess the heterogeneous effects of information sessions on the uptake of a new weather insurance policy in rural China.

### 8. Estimating Average Causal Effects Under General Interference, with Application to a Social Network Experiment

- 作者：Peter M. Aronow, Cyrus Samii
- 领域：`math.ST`（全部：math.ST, stat.ME）
- 发布：2013-05-27 · 更新：2018-06-20
- 链接：https://arxiv.org/abs/1305.6156 · PDF：https://arxiv.org/pdf/1305.6156
- 期刊/会议：Aronow, Peter M.; Samii, Cyrus. Estimating average causal effects under general interference, with application to a social network experiment. Ann. Appl. Stat. 11 (2017), no. 4, 1912--1947
- DOI：10.1214/16-AOAS1005
- 入库：2026-11-08T14:39:02+08:00

> This paper presents a randomization-based framework for estimating causal effects under interference between units, motivated by challenges that arise in analyzing experiments on social networks. The framework integrates three components: (i) an experimental design that defines the probability distribution of treatment assignments, (ii) a mapping that relates experimental treatment assignments to exposures received by units in the experiment, and (iii) estimands that make use of the experiment to answer questions of substantive interest. We develop the case of estimating average unit-level causal effects from a randomized experiment with interference of arbitrary but known form. The resulting estimators are based on inverse probability weighting. We provide randomization-based variance estimators that account for the complex clustering that can occur when interference is present. We also establish consistency and asymptotic normality under local dependence assumptions. We discuss refinements including covariate-adjusted effect estimators and ratio estimation. We evaluate empirical performance in realistic settings with a naturalistic simulation using social network data from American schools. We then present results from a field experiment on the spread of anti-conflict norms and behavior among school students.

### 9. Design and analysis of experiments in networks: Reducing bias from interference

- 作者：Dean Eckles, Brian Karrer, Johan Ugander
- 领域：`stat.ME`（全部：stat.ME, cs.SI, physics.soc-ph）
- 发布：2014-04-29 · 更新：2014-08-13
- 链接：https://arxiv.org/abs/1404.7530 · PDF：https://arxiv.org/pdf/1404.7530
- 备注：32 pages, 7 figures
- 入库：2026-11-08T14:39:02+08:00

> Estimating the effects of interventions in networks is complicated when the units are interacting, such that the outcomes for one unit may depend on the treatment assignment and behavior of many or all other units (i.e., there is interference). When most or all units are in a single connected component, it is impossible to directly experimentally compare outcomes under two or more global treatment assignments since the network can only be observed under a single assignment. Familiar formalism, experimental designs, and analysis methods assume the absence of these interactions, and result in biased estimators of causal effects of interest. While some assumptions can lead to unbiased estimators, these assumptions are generally unrealistic, and we focus this work on realistic assumptions. Thus, in this work, we evaluate methods for designing and analyzing randomized experiments that aim to reduce this bias and thereby reduce overall error. In design, we consider the ability to perform random assignment to treatments that is correlated in the network, such as through graph cluster randomization. In analysis, we consider incorporating information about the treatment assignment of network neighbors. We prove sufficient conditions for bias reduction through both design and analysis in the presence of potentially global interference. Through simulations of the entire process of experimentation in networks, we measure the performance of these methods under varied network structure and varied social behaviors, finding substantial bias and error reductions. These improvements are largest for networks with more clustering and data generating processes with both stronger direct effects of the treatment and stronger interactions between units.
