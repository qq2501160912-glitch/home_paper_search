# arXiv 论文记录

> 查询：bidding · 共 10 篇 · 生成 2026-11-27T20:04:24+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [Real-Time Bidding Benchmarking with iPinYou Dataset](https://arxiv.org/abs/1407.7073) | cs.GT | 2014-07-25 | [abs](https://arxiv.org/abs/1407.7073) · [pdf](https://arxiv.org/pdf/1407.7073) |
| 2 | [Deep Landscape Forecasting for Real-time Bidding Advertising](https://arxiv.org/abs/1905.03028) | cs.IR | 2019-05-07 | [abs](https://arxiv.org/abs/1905.03028) · [pdf](https://arxiv.org/pdf/1905.03028) |
| 3 | [Real-Time Bidding by Reinforcement Learning in Display Advertising](https://arxiv.org/abs/1701.02490) | cs.LG | 2017-01-10 | [abs](https://arxiv.org/abs/1701.02490) · [pdf](https://arxiv.org/pdf/1701.02490) |
| 4 | [Auctions without commitment in the auto-bidding world](https://arxiv.org/abs/2301.07312) | econ.TH | 2023-01-18 | [abs](https://arxiv.org/abs/2301.07312) · [pdf](https://arxiv.org/pdf/2301.07312) |
| 5 | [AIGB: Generative Auto-bidding via Conditional Diffusion Modeling](https://arxiv.org/abs/2405.16141) | cs.LG | 2024-05-25 | [abs](https://arxiv.org/abs/2405.16141) · [pdf](https://arxiv.org/pdf/2405.16141) |
| 6 | [Multi-agent Auto-Bidding with Latent Graph Diffusion Models](https://arxiv.org/abs/2503.05805) | cs.LG | 2025-03-04 | [abs](https://arxiv.org/abs/2503.05805) · [pdf](https://arxiv.org/pdf/2503.05805) |
| 7 | [Permutation Equivariant Model-based Offline Reinforcement Learning for Auto-bidding](https://arxiv.org/abs/2506.17919) | cs.LG | 2025-06-22 | [abs](https://arxiv.org/abs/2506.17919) · [pdf](https://arxiv.org/pdf/2506.17919) |
| 8 | [PlatformBid: An Auto-Bidding Benchmark from a Unified Advertising Platform's Perspective](https://arxiv.org/abs/2607.27265) | cs.LG | 2026-07-29 | [abs](https://arxiv.org/abs/2607.27265) · [pdf](https://arxiv.org/pdf/2607.27265) |
| 9 | [Double Distributionally Robust Bid Shading for First Price Auctions](https://arxiv.org/abs/2410.14864) | cs.GT | 2024-10-18 | [abs](https://arxiv.org/abs/2410.14864) · [pdf](https://arxiv.org/pdf/2410.14864) |
| 10 | [Budget, Readout or Reasoning? Where Small Reasoning Models Lose Value in Auction Bidding](https://arxiv.org/abs/2611.34068) | cs.AI | 2026-11-25 | [abs](https://arxiv.org/abs/2611.34068) · [pdf](https://arxiv.org/pdf/2611.34068) |

## 摘要

### 1. Real-Time Bidding Benchmarking with iPinYou Dataset

- 作者：Weinan Zhang, Shuai Yuan, Jun Wang, Xuehua Shen
- 领域：`cs.GT`（全部：cs.GT, cs.CY）
- 发布：2014-07-25 · 更新：2015-05-21
- 链接：https://arxiv.org/abs/1407.7073 · PDF：https://arxiv.org/pdf/1407.7073
- 备注：UCL Technical Report 2014
- 入库：2026-11-27T20:04:24+08:00

> Being an emerging paradigm for display advertising, Real-Time Bidding (RTB) drives the focus of the bidding strategy from context to users' interest by computing a bid for each impression in real time. The data mining work and particularly the bidding strategy development becomes crucial in this performance-driven business. However, researchers in computational advertising area have been suffering from lack of publicly available benchmark datasets, which are essential to compare different algorithms and systems. Fortunately, a leading Chinese advertising technology company iPinYou decided to release the dataset used in its global RTB algorithm competition in 2013. The dataset includes logs of ad auctions, bids, impressions, clicks, and final conversions. These logs reflect the market environment as well as form a complete path of users' responses from advertisers' perspective. This dataset directly supports the experiments of some important research problems such as bid optimisation and CTR estimation. To the best of our knowledge, this is the first publicly available dataset on RTB display advertising. Thus, they are valuable for reproducible research and understanding the whole RTB ecosystem. In this paper, we first provide the detailed statistical analysis of this dataset. Then we introduce the research problem of bid optimisation in RTB and the simple yet comprehensive evaluation protocol. Besides, a series of benchmark experiments are also conducted, including both click-through rate (CTR) estimation and bid optimisation.

### 2. Deep Landscape Forecasting for Real-time Bidding Advertising

- 作者：Kan Ren, Jiarui Qin, Lei Zheng, Zhengyu Yang, Weinan Zhang, Yong Yu
- 领域：`cs.IR`（全部：cs.IR, cs.GT, cs.LG）
- 发布：2019-05-07 · 更新：2019-05-12
- 链接：https://arxiv.org/abs/1905.03028 · PDF：https://arxiv.org/pdf/1905.03028
- 备注：KDD 2019. The reproducible code and dataset link is https://github.com/rk2900/DLF
- DOI：10.1145/3292500.3330870
- 入库：2026-11-27T20:04:24+08:00

> The emergence of real-time auction in online advertising has drawn huge attention of modeling the market competition, i.e., bid landscape forecasting. The problem is formulated as to forecast the probability distribution of market price for each ad auction. With the consideration of the censorship issue which is caused by the second-price auction mechanism, many researchers have devoted their efforts on bid landscape forecasting by incorporating survival analysis from medical research field. However, most existing solutions mainly focus on either counting-based statistics of the segmented sample clusters, or learning a parameterized model based on some heuristic assumptions of distribution forms. Moreover, they neither consider the sequential patterns of the feature over the price space. In order to capture more sophisticated yet flexible patterns at fine-grained level of the data, we propose a Deep Landscape Forecasting (DLF) model which combines deep learning for probability distribution forecasting and survival analysis for censorship handling. Specifically, we utilize a recurrent neural network to flexibly model the conditional winning probability w.r.t. each bid price. Then we conduct the bid landscape forecasting through probability chain rule with strict mathematical derivations. And, in an end-to-end manner, we optimize the model by minimizing two negative likelihood losses with comprehensive motivations. Without any specific assumption for the distribution form of bid landscape, our model shows great advantages over previous works on fitting various sophisticated market price distributions. In the experiments over two large-scale real-world datasets, our model significantly outperforms the state-of-the-art solutions under various metrics.

### 3. Real-Time Bidding by Reinforcement Learning in Display Advertising

- 作者：Han Cai, Kan Ren, Weinan Zhang, Kleanthis Malialis, Jun Wang, Yong Yu, Defeng Guo
- 领域：`cs.LG`（全部：cs.LG, cs.AI, cs.GT）
- 发布：2017-01-10 · 更新：2017-01-12
- 链接：https://arxiv.org/abs/1701.02490 · PDF：https://arxiv.org/pdf/1701.02490
- 备注：WSDM 2017
- DOI：10.1145/3018661.3018702
- 入库：2026-11-27T20:04:24+08:00

> The majority of online display ads are served through real-time bidding (RTB) --- each ad display impression is auctioned off in real-time when it is just being generated from a user visit. To place an ad automatically and optimally, it is critical for advertisers to devise a learning algorithm to cleverly bid an ad impression in real-time. Most previous works consider the bid decision as a static optimization problem of either treating the value of each impression independently or setting a bid price to each segment of ad volume. However, the bidding for a given ad campaign would repeatedly happen during its life span before the budget runs out. As such, each bid is strategically correlated by the constrained budget and the overall effectiveness of the campaign (e.g., the rewards from generated clicks), which is only observed after the campaign has completed. Thus, it is of great interest to devise an optimal bidding strategy sequentially so that the campaign budget can be dynamically allocated across all the available impressions on the basis of both the immediate and future rewards. In this paper, we formulate the bid decision process as a reinforcement learning problem, where the state space is represented by the auction information and the campaign's real-time parameters, while an action is the bid price to set. By modeling the state transition via auction competition, we build a Markov Decision Process framework for learning the optimal bidding policy to optimize the advertising performance in the dynamic real-time bidding environment. Furthermore, the scalability problem from the large real-world auction volume and campaign budget is well handled by state value approximation using neural networks.

### 4. Auctions without commitment in the auto-bidding world

- 作者：Aranyak Mehta, Andres Perlroth
- 领域：`econ.TH`（全部：econ.TH, cs.GT）
- 发布：2023-01-18 · 更新：2023-03-14
- 链接：https://arxiv.org/abs/2301.07312 · PDF：https://arxiv.org/pdf/2301.07312
- 入库：2026-11-27T20:04:24+08:00

> Advertisers in online ad auctions are increasingly using auto-bidding mechanisms to bid into auctions instead of directly bidding their value manually. One prominent auto-bidding format is the target cost-per-acquisition (tCPA) which maximizes the volume of conversions subject to a return-of-investment constraint. From an auction theoretic perspective however, this trend seems to go against foundational results that postulate that for profit-maximizing bidders, it is optimal to use a classic bidding system like marginal CPA (mCPA) bidding rather than using strategies like tCPA. In this paper we rationalize the adoption of such seemingly sub-optimal bidding within the canonical quasi-linear framework. The crux of the argument lies in the notion of commitment. We consider a multi-stage game where first the auctioneer declares the auction rules; then bidders select either the tCPA or mCPA bidding format and then, if the auctioneer lacks commitment, it can revisit the rules of the auction (e.g., may readjust reserve prices depending on the observed bids). Our main result is that so long as a bidder believes that the auctioneer lacks commitment to follow the rule of the declared auction then the bidder will make a higher profit by choosing the tCPA format over the mCPA format. We then explore the commitment consequences for the auctioneer. In a simplified version of the model where there is only one bidder, we show that the tCPA subgame admits a credible equilibrium while the mCPA format does not. That is, when the bidder chooses the tCPA format the auctioneer can credibly implement the auction rules announced at the beginning of the game. We also show that, under some mild conditions, the auctioneer's revenue is larger when the bidder uses the tCPA format rather than mCPA. We further quantify the value for the auctioneer to be able to commit to the declared auction rules.

### 5. AIGB: Generative Auto-bidding via Conditional Diffusion Modeling

- 作者：Jiayan Guo, Yusen Huo, Zhilin Zhang, Tianyu Wang, Chuan Yu, Jian Xu, Yan Zhang, Bo Zheng
- 领域：`cs.LG`（全部：cs.LG, cs.AI, cs.CE）
- 发布：2024-05-25 · 更新：2024-10-08
- 链接：https://arxiv.org/abs/2405.16141 · PDF：https://arxiv.org/pdf/2405.16141
- 备注：Accepted by KDD 2024
- 入库：2026-11-27T20:04:24+08:00

> Auto-bidding plays a crucial role in facilitating online advertising by automatically providing bids for advertisers. Reinforcement learning (RL) has gained popularity for auto-bidding. However, most current RL auto-bidding methods are modeled through the Markovian Decision Process (MDP), which assumes the Markovian state transition. This assumption restricts the ability to perform in long horizon scenarios and makes the model unstable when dealing with highly random online advertising environments. To tackle this issue, this paper introduces AI-Generated Bidding (AIGB), a novel paradigm for auto-bidding through generative modeling. In this paradigm, we propose DiffBid, a conditional diffusion modeling approach for bid generation. DiffBid directly models the correlation between the return and the entire trajectory, effectively avoiding error propagation across time steps in long horizons. Additionally, DiffBid offers a versatile approach for generating trajectories that maximize given targets while adhering to specific constraints. Extensive experiments conducted on the real-world dataset and online A/B test on Alibaba advertising platform demonstrate the effectiveness of DiffBid, achieving 2.81% increase in GMV and 3.36% increase in ROI.

### 6. Multi-agent Auto-Bidding with Latent Graph Diffusion Models

- 作者：Dom Huh, Prasant Mohapatra
- 领域：`cs.LG`（全部：cs.LG, cs.AI, cs.MA）
- 发布：2025-03-04 · 更新：2025-04-19
- 链接：https://arxiv.org/abs/2503.05805 · PDF：https://arxiv.org/pdf/2503.05805
- 入库：2026-11-27T20:04:24+08:00

> This paper proposes a diffusion-based auto-bidding framework that leverages graph representations to model large-scale auction environments. In such settings, agents must dynamically optimize bidding strategies under constraints defined by key performance indicator (KPI) metrics, all while operating in competitive environments characterized by uncertain, sparse, and stochastic variables. To address these challenges, we introduce a novel approach combining learnable graph-based embeddings with a planning-based latent diffusion model (LDM). By capturing patterns and nuances underlying the interdependence of impression opportunities and the multi-agent dynamics of the auction environment, the graph representation enable expressive computations regarding auto-bidding outcomes. With reward alignment techniques, the LDM's posterior is fine-tuned to generate auto-bidding trajectories that maximize KPI metrics while satisfying constraint thresholds. Empirical evaluations on both real-world and synthetic auction environments demonstrate significant improvements in auto-bidding performance across multiple common KPI metrics, as well as accuracy in forecasting auction outcomes.

### 7. Permutation Equivariant Model-based Offline Reinforcement Learning for Auto-bidding

- 作者：Zhiyu Mou, Miao Xu, Wei Chen, Rongquan Bai, Chuan Yu, Jian Xu
- 领域：`cs.LG`（全部：cs.LG, cs.AI）
- 发布：2025-06-22 · 更新：2025-06-22
- 链接：https://arxiv.org/abs/2506.17919 · PDF：https://arxiv.org/pdf/2506.17919
- 入库：2026-11-27T20:04:24+08:00

> Reinforcement learning (RL) for auto-bidding has shifted from using simplistic offline simulators (Simulation-based RL Bidding, SRLB) to offline RL on fixed real datasets (Offline RL Bidding, ORLB). However, ORLB policies are limited by the dataset's state space coverage, offering modest gains. While SRLB expands state coverage, its simulator-reality gap risks misleading policies. This paper introduces Model-based RL Bidding (MRLB), which learns an environment model from real data to bridge this gap. MRLB trains policies using both real and model-generated data, expanding state coverage beyond ORLB. To ensure model reliability, we propose: 1) A permutation equivariant model architecture for better generalization, and 2) A robust offline Q-learning method that pessimistically penalizes model errors. These form the Permutation Equivariant Model-based Offline RL (PE-MORL) algorithm. Real-world experiments show that PE-MORL outperforms state-of-the-art auto-bidding methods.

### 8. PlatformBid: An Auto-Bidding Benchmark from a Unified Advertising Platform's Perspective

- 作者：Shengtian Yang, Yewen Li, Peng Jiang, Zhiyi Lyu, Bo An, Peng Jiang, Qingpeng Cai, Lei Feng
- 领域：`cs.LG`（全部：cs.LG）
- 发布：2026-07-29 · 更新：2026-07-29
- 链接：https://arxiv.org/abs/2607.27265 · PDF：https://arxiv.org/pdf/2607.27265
- 入库：2026-11-27T20:04:24+08:00

> Real-time bidding is central to computational advertising, comprising three elements: Supply Side Platform (SSP) selling ad impressions, Demand Side Platform (DSP) bidding for advertisers, and Ad Exchange conducting auctions between them. Traditional auto-bidding algorithms focus solely on the DSP side, maximizing advertiser conversions by adjusting bids against competitors. However, current big ad platforms, such as social media and e-commerce companies, now integrate SSP, DSP, and Ad Exchange functions internally. From such ad platforms' perspective, the goal of the auto-bidding algorithms is not only to maximize the advertisers' conversions, but also the total revenue of the platform. Given the lack of platform-centric evaluation frameworks and the pressing need to advance auto-bidding research, we propose PlatformBid - the first comprehensive benchmark designed from a unified ad platform's perspective. To accurately reflect the real-world auto-bidding scenarios, we define three representative settings: (1) homogeneous competition with identical algorithms across advertisers, (2) heterogeneous competition with diverse algorithmic strategies, and (3) promotional competition where some advertisers surge budgets for boosting sales during promotional events like Black Friday. We systematically evaluate a broad spectrum of existing auto-bidding methods across these settings, encompassing classical control methods, RL-based methods, and recent generative methods. Besides these methods, we further propose a novel auto-bidding method based on flow-matching, termed BidFlow, which leverages the flow-matching method's expressive policy representation to effectively handle dynamic competitive environments. Online experiments on Kuaishou further show a +0.68\% improvement in target cost, providing deployment evidence for the offline-online consistency of PlatformBid.

### 9. Double Distributionally Robust Bid Shading for First Price Auctions

- 作者：Yanlin Qu, Ravi Kant, Yan Chen, Brendan Kitts, San Gultekin, Aaron Flores, Jose Blanchet
- 领域：`cs.GT`（全部：cs.GT, math.OC）
- 发布：2024-10-18 · 更新：2024-10-18
- 链接：https://arxiv.org/abs/2410.14864 · PDF：https://arxiv.org/pdf/2410.14864
- 入库：2026-11-27T20:04:24+08:00

> Bid shading has become a standard practice in the digital advertising industry, in which most auctions for advertising (ad) opportunities are now of first price type. Given an ad opportunity, performing bid shading requires estimating not only the value of the opportunity but also the distribution of the highest bid from competitors (i.e. the competitive landscape). Since these two estimates tend to be very noisy in practice, first-price auction participants need a bid shading policy that is robust against relatively significant estimation errors. In this work, we provide a max-min formulation in which we maximize the surplus against an adversary that chooses a distribution both for the value and the competitive landscape, each from a Kullback-Leibler-based ambiguity set. As we demonstrate, the two ambiguity sets are essential to adjusting the shape of the bid-shading policy in a principled way so as to effectively cope with uncertainty. Our distributionally robust bid shading policy is efficient to compute and systematically outperforms its non-robust counterpart on real datasets provided by Yahoo DSP.

### 10. Budget, Readout or Reasoning? Where Small Reasoning Models Lose Value in Auction Bidding

- 作者：Mahbod Khaleti, Seyed Reza Tavakoli, Baran Hoseini, Alireza Noori, Amir Amini, Koorosh Aslansefat, Marjan Alirezaie, Ali Habibnia
- 领域：`cs.AI`（全部：cs.AI, cs.CL, econ.GN）
- 发布：2026-11-25 · 更新：2026-11-25
- 链接：https://arxiv.org/abs/2611.34068 · PDF：https://arxiv.org/pdf/2611.34068
- 备注：19 pages, 2 figures, 23 tables. Code and data: https://github.com/DataismLab/bid-reasoning
- 入库：2026-11-27T20:04:24+08:00

> Ad platforms and marketplaces show bidders a bid landscape, the estimated chance of winning at each candidate bid, and increasingly let agents built on reasoning language models choose the bid. We give six open reasoning models of 4B to 14B parameters such landscapes, with win curves from eBay closing prices and from a simulated advertising market (AuctionNet), and score their bids on held-out auctions against an exact calculator. Because the agent is handed the estimates, the lost value can be split by cause. Two failures belong to the models. They pass over the best option even when the values written in their own trace already rank it first, and their wrong answers lean toward the highest bid on the menu. The lean is about the bid's size, not its place in the list, and it survives sampling. At 768 forced tokens on eBay, under pay-your-bid pricing, the wrong answers cost bidders 7-17% of the surplus the calculator's bids earn. Arithmetic errors are rare. Two further losses come from operator choices. A token cap cuts traces short: allowed to stop on their own within 4,096 tokens, five models recover 91-100% of the calculator's lead over a model that does no reasoning. Asking for the answer while the reasoning block is still open misreads it: closing the block first lifts the weakest model from 42% to 84% on eBay and from 24% to 81% on AuctionNet. Finally, an audit that flags bids disagreeing with the trace's own numbers, and overrides them with the calculator's bid, raises the share of the calculator's lead recovered at 768 forced tokens from 42-85% to 84-100% on eBay under nested cross-validation, and the same reader settings transfer from eBay to AuctionNet.
