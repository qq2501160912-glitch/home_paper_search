# arXiv 论文记录

> 查询：auction · 共 6 篇 · 生成 2026-11-27T22:14:11+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [AuctionNet: A Novel Benchmark for Decision-Making in Large-Scale Games](https://arxiv.org/abs/2412.10798) | cs.AI | 2024-12-14 | [abs](https://arxiv.org/abs/2412.10798) · [pdf](https://arxiv.org/pdf/2412.10798) |
| 2 | [DynamAuction: A Reinforcement Learning Environment for Repeated Auctions with Dynamic Value](https://arxiv.org/abs/2611.14000) | stat.AP | 2026-11-10 | [abs](https://arxiv.org/abs/2611.14000) · [pdf](https://arxiv.org/pdf/2611.14000) |
| 3 | [Put Your Money Where Your Mouth Is: Evaluating Strategic Planning and Execution of LLM Agents in an Auction Arena](https://arxiv.org/abs/2310.05746) | cs.CL | 2023-10-09 | [abs](https://arxiv.org/abs/2310.05746) · [pdf](https://arxiv.org/pdf/2310.05746) |
| 4 | [LLM-Auction: Generative Auction towards LLM-Native Advertising](https://arxiv.org/abs/2512.10551) | cs.GT | 2025-12-11 | [abs](https://arxiv.org/abs/2512.10551) · [pdf](https://arxiv.org/pdf/2512.10551) |
| 5 | [Implementing a Hierarchical Deep Learning Approach for Simulating Multi-Level Auction Data](https://arxiv.org/abs/2207.12255) | econ.GN | 2022-07-25 | [abs](https://arxiv.org/abs/2207.12255) · [pdf](https://arxiv.org/pdf/2207.12255) |
| 6 | [Using Multi-Agent Reinforcement Learning in Auction Simulations](https://arxiv.org/abs/2004.02764) | cs.GT | 2020-04-06 | [abs](https://arxiv.org/abs/2004.02764) · [pdf](https://arxiv.org/pdf/2004.02764) |

## 摘要

### 1. AuctionNet: A Novel Benchmark for Decision-Making in Large-Scale Games

- 作者：Kefan Su, Yusen Huo, Zhilin Zhang, Shuai Dou, Chuan Yu, Jian Xu, Zongqing Lu, Bo Zheng
- 领域：`cs.AI`（全部：cs.AI, cs.LG）
- 发布：2024-12-14 · 更新：2024-12-28
- 链接：https://arxiv.org/abs/2412.10798 · PDF：https://arxiv.org/pdf/2412.10798
- 入库：2026-11-27T22:14:11+08:00

> Decision-making in large-scale games is an essential research area in artificial intelligence (AI) with significant real-world impact. However, the limited access to realistic large-scale game environments has hindered research progress in this area. In this paper, we present AuctionNet, a benchmark for bid decision-making in large-scale ad auctions derived from a real-world online advertising platform. AuctionNet is composed of three parts: an ad auction environment, a pre-generated dataset based on the environment, and performance evaluations of several baseline bid decision-making algorithms. More specifically, the environment effectively replicates the integrity and complexity of real-world ad auctions through the interaction of several modules: the ad opportunity generation module employs deep generative networks to bridge the gap between simulated and real-world data while mitigating the risk of sensitive data exposure; the bidding module implements diverse auto-bidding agents trained with different decision-making algorithms; and the auction module is anchored in the classic Generalized Second Price (GSP) auction but also allows for customization of auction mechanisms as needed. To facilitate research and provide insights into the environment, we have also pre-generated a substantial dataset based on the environment. The dataset contains 10 million ad opportunities, 48 diverse auto-bidding agents, and over 500 million auction records. Performance evaluations of baseline algorithms such as linear programming, reinforcement learning, and generative models for bid decision-making are also presented as a part of AuctionNet. We believe that AuctionNet is applicable not only to research on bid decision-making in ad auctions but also to the general area of decision-making in large-scale games.

### 2. DynamAuction: A Reinforcement Learning Environment for Repeated Auctions with Dynamic Value

- 作者：Eugénie Patard, Corentin Pla, Benjamin Heymann, Patrick Loiseau
- 领域：`stat.AP`（全部：stat.AP）
- 发布：2026-11-10 · 更新：2026-11-10
- 链接：https://arxiv.org/abs/2611.14000 · PDF：https://arxiv.org/pdf/2611.14000
- 入库：2026-11-27T22:14:11+08:00

> A buyer who repeatedly participates in auctions for related items often faces a dynamic value problem: what they win today changes what tomorrow's items are worth. Despite the empirical importance of such effects, especially in display advertising, the algorithmic literature on repeated auctions has largely focused on the learning problem, by treating each opportunity as a contextual bandit, while sidestepping the planning problem induced by the dependence of current value on past wins. We introduce DynamAuction, a synthetic environment for single-buyer sequential bidding. The reward from each win depends on the buyer's history of previous wins, summarized through a carry-over state. The environment supports first- and second-price auctions, non-homogeneous Poisson arrivals, delayed feedback, saturation, and recency effects. We also introduce a new class of Model Predictive Control (MPC) algorithms. On our benchmark scenario, these MPC policies outperform off-the-shelf deep RL baselines (PPO, SAC, TD3) as well as a tuned shading baseline. We release DynamAuction to support RL research on repeated auctions.

### 3. Put Your Money Where Your Mouth Is: Evaluating Strategic Planning and Execution of LLM Agents in an Auction Arena

- 作者：Jiangjie Chen, Siyu Yuan, Rong Ye, Bodhisattwa Prasad Majumder, Kyle Richardson
- 领域：`cs.CL`（全部：cs.CL, cs.AI）
- 发布：2023-10-09 · 更新：2024-08-25
- 链接：https://arxiv.org/abs/2310.05746 · PDF：https://arxiv.org/pdf/2310.05746
- 备注：Project page: https://auction-arena.github.io
- 入库：2026-11-27T22:14:11+08:00

> Recent advancements in Large Language Models (LLMs) showcase advanced reasoning, yet NLP evaluations often depend on static benchmarks. Evaluating this necessitates environments that test strategic reasoning in dynamic, competitive scenarios requiring long-term planning. We introduce AucArena, a novel evaluation suite that simulates auctions, a setting chosen for being highly unpredictable and involving many skills related to resource and risk management, while also being easy to evaluate. We conduct controlled experiments using state-of-the-art LLMs to power bidding agents to benchmark their planning and execution skills. Our research demonstrates that LLMs, such as GPT-4, possess key skills for auction participation, such as budget management and goal adherence, which improve with adaptive strategies. This highlights LLMs' potential in modeling complex social interactions in competitive contexts. However, variability in LLM performance and occasional outperformance by simpler methods indicate opportunities for further advancements in LLM design and the value of our simulation environment for ongoing testing and refinement.

### 4. LLM-Auction: Generative Auction towards LLM-Native Advertising

- 作者：Chujie Zhao, Qun Hu, Shiping Song, Dagui Chen, Han Zhu, Jian Xu, Bo Zheng
- 领域：`cs.GT`（全部：cs.GT, cs.AI, cs.LG）
- 发布：2025-12-11 · 更新：2026-10-22
- 链接：https://arxiv.org/abs/2512.10551 · PDF：https://arxiv.org/pdf/2512.10551
- 备注：NeurIPS 2026
- 入库：2026-11-27T22:14:11+08:00

> The commercialization of LLM applications is the next frontier in online advertising, with LLM-native advertising emerging as a promising paradigm by integrating ads into LLM-generated content. However, classic mechanisms are no longer applicable in this setting where the auction object is shifted from discrete ad slots to distributions over LLM outputs, and existing methods are impractical in industrial scenarios due to ignored externalities or high inference costs. To address these issues, we propose LLM-Auction, the first learning-based generative auction mechanism that integrates auction and generation. By formulating the allocation as preference alignment between LLM outputs and a mechanism objective that balances advertisers' value and user experience, we optimize the LLMs to inherently model allocation externalities without extra inference cost. Theoretically, we identify the allocation monotonicity and continuity of the optimal allocation rule of LLM-Auction, and prove that a simple first-price payment rule exhibits favorable incentive properties under this allocation rule. Furthermore, we build an LLM-as-a-judge simulation environment for quantitative evaluation, and experiments demonstrate that LLM-Auction achieves the state-of-the-art allocation efficiency while approximately satisfying key mechanism properties.

### 5. Implementing a Hierarchical Deep Learning Approach for Simulating Multi-Level Auction Data

- 作者：Igor Sadoune, Andrea Lodi, Marcelin Joanis
- 领域：`econ.GN`（全部：econ.GN）
- 发布：2022-07-25 · 更新：2024-02-15
- 链接：https://arxiv.org/abs/2207.12255 · PDF：https://arxiv.org/pdf/2207.12255
- 期刊/会议：Computational Economics, 2024
- DOI：10.1007/S10614-024-10622-4
- 入库：2026-11-27T22:14:11+08:00

> We present a deep learning solution to address the challenges of simulating realistic synthetic first-price sealed-bid auction data. The complexities encountered in this type of auction data include high-cardinality discrete feature spaces and a multilevel structure arising from multiple bids associated with a single auction instance. Our methodology combines deep generative modeling (DGM) with an artificial learner that predicts the conditional bid distribution based on auction characteristics, contributing to advancements in simulation-based research. This approach lays the groundwork for creating realistic auction environments suitable for agent-based learning and modeling applications. Our contribution is twofold: we introduce a comprehensive methodology for simulating multilevel discrete auction data, and we underscore the potential of DGM as a powerful instrument for refining simulation techniques and fostering the development of economic models grounded in generative AI.

### 6. Using Multi-Agent Reinforcement Learning in Auction Simulations

- 作者：Medet Kanmaz, Elif Surer
- 领域：`cs.GT`（全部：cs.GT, cs.MA）
- 发布：2020-04-06 · 更新：2020-04-06
- 链接：https://arxiv.org/abs/2004.02764 · PDF：https://arxiv.org/pdf/2004.02764
- 入库：2026-11-27T22:14:11+08:00

> Game theory has been developed by scientists as a theory of strategic interaction among players who are supposed to be perfectly rational. These strategic interactions might have been presented in an auction, a business negotiation, a chess game, or even in a political conflict aroused between different agents. In this study, the strategic (rational) agents created by reinforcement learning algorithms are supposed to be bidder agents in various types of auction mechanisms such as British Auction, Sealed Bid Auction, and Vickrey Auction designs. Next, the equilibrium points determined by the agents are compared with the outcomes of the Nash equilibrium points for these environments. The bidding strategy of the agents is analyzed in terms of individual rationality, truthfulness (strategy-proof), and computational efficiency. The results show that using a multi-agent reinforcement learning strategy improves the outcomes of the auction simulations.
