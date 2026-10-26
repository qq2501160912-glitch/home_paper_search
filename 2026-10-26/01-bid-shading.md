# arXiv 论文记录

> 查询：bid shading · 共 5 篇 · 生成 2026-10-26T22:07:18+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [Generative Bid Shading in Real-Time Bidding Advertising](https://arxiv.org/abs/2508.06550) | cs.GT | 2025-08-06 | [abs](https://arxiv.org/abs/2508.06550) · [pdf](https://arxiv.org/pdf/2508.06550) |
| 2 | [Double Distributionally Robust Bid Shading for First Price Auctions](https://arxiv.org/abs/2410.14864) | cs.GT | 2024-10-18 | [abs](https://arxiv.org/abs/2410.14864) · [pdf](https://arxiv.org/pdf/2410.14864) |
| 3 | [MEBS: Multi-task End-to-end Bid Shading for Multi-slot Display Advertising](https://arxiv.org/abs/2403.02607) | cs.GT | 2024-03-05 | [abs](https://arxiv.org/abs/2403.02607) · [pdf](https://arxiv.org/pdf/2403.02607) |
| 4 | [Learning Concave Bid Shading Strategies in Online Auctions via Measure-valued Proximal Optimization](https://arxiv.org/abs/2509.10693) | cs.LG | 2025-09-12 | [abs](https://arxiv.org/abs/2509.10693) · [pdf](https://arxiv.org/pdf/2509.10693) |
| 5 | [Strategic Bid Shading in Real-Time Bidding Auctions in Ad Exchange Using Minority Game Theory](https://arxiv.org/abs/2512.15717) | econ.TH | 2025-12-02 | [abs](https://arxiv.org/abs/2512.15717) · [pdf](https://arxiv.org/pdf/2512.15717) |

## 摘要

### 1. Generative Bid Shading in Real-Time Bidding Advertising

- 作者：Yinqiu Huang, Hao Ma, Wenshuai Chen, Zongwei Wang, Shuli Wang, Yongqiang Zhang, Xue Wei, Yinhua Zhu, Haitao Wang, Xingxing Wang
- 领域：`cs.GT`（全部：cs.GT, cs.LG）
- 发布：2025-08-06 · 更新：2026-04-29
- 链接：https://arxiv.org/abs/2508.06550 · PDF：https://arxiv.org/pdf/2508.06550
- 备注：SIGIR 2026
- 入库：2026-10-26T22:07:18+08:00

> Bid shading plays a crucial role in Real-Time Bidding (RTB) by adaptively adjusting the bid to avoid advertisers overspending. Existing mainstream two-stage methods, which first model bid landscapes and then optimize surplus using operations research techniques, are constrained by unimodal assumptions that fail to adapt for non-convex surplus curves and are vulnerable to cascading errors in sequential workflows. Additionally, existing discretization models of continuous values ignore the dependence between discrete intervals, reducing the model's error correction ability, while sample selection bias in bidding scenarios presents further challenges for prediction. To address these issues, this paper introduces Generative Bid Shading (GBS), which comprises two primary components: 1) an end-to-end generative model that utilizes an autoregressive approach to generate shading ratios by stepwise residuals, capturing complex value dependencies without relying on predefined priors; and 2) a reward preference alignment system, which incorporates a channel-aware hierarchical dynamic network (CHNet) as the reward model to extract fine-grained features, along with modules for surplus optimization and exploration utility reward alignment, ultimately optimizing both short-term and long-term surplus using group relative policy optimization (GRPO). Extensive experiments on both offline and online A/B tests validate GBS's effectiveness. Moreover, GBS has been deployed on the Meituan DSP platform, serving billions of bid requests daily.

### 2. Double Distributionally Robust Bid Shading for First Price Auctions

- 作者：Yanlin Qu, Ravi Kant, Yan Chen, Brendan Kitts, San Gultekin, Aaron Flores, Jose Blanchet
- 领域：`cs.GT`（全部：cs.GT, math.OC）
- 发布：2024-10-18 · 更新：2024-10-18
- 链接：https://arxiv.org/abs/2410.14864 · PDF：https://arxiv.org/pdf/2410.14864
- 入库：2026-10-26T22:07:18+08:00

> Bid shading has become a standard practice in the digital advertising industry, in which most auctions for advertising (ad) opportunities are now of first price type. Given an ad opportunity, performing bid shading requires estimating not only the value of the opportunity but also the distribution of the highest bid from competitors (i.e. the competitive landscape). Since these two estimates tend to be very noisy in practice, first-price auction participants need a bid shading policy that is robust against relatively significant estimation errors. In this work, we provide a max-min formulation in which we maximize the surplus against an adversary that chooses a distribution both for the value and the competitive landscape, each from a Kullback-Leibler-based ambiguity set. As we demonstrate, the two ambiguity sets are essential to adjusting the shape of the bid-shading policy in a principled way so as to effectively cope with uncertainty. Our distributionally robust bid shading policy is efficient to compute and systematically outperforms its non-robust counterpart on real datasets provided by Yahoo DSP.

### 3. MEBS: Multi-task End-to-end Bid Shading for Multi-slot Display Advertising

- 作者：Zhen Gong, Lvyin Niu, Yang Zhao, Miao Xu, Zhenzhe Zheng, Haoqi Zhang, Zhilin Zhang, Fan Wu, Rongquan Bai, Chuan Yu, Jian Xu, Bo Zheng
- 领域：`cs.GT`（全部：cs.GT, cs.AI）
- 发布：2024-03-05 · 更新：2024-03-05
- 链接：https://arxiv.org/abs/2403.02607 · PDF：https://arxiv.org/pdf/2403.02607
- 入库：2026-10-26T22:07:18+08:00

> Online bidding and auction are crucial aspects of the online advertising industry. Conventionally, there is only one slot for ad display and most current studies focus on it. Nowadays, multi-slot display advertising is gradually becoming popular where many ads could be displayed in a list and shown as a whole to users. However, multi-slot display advertising leads to different cost-effectiveness. Advertisers have the incentive to adjust bid prices so as to win the most economical ad positions. In this study, we introduce bid shading into multi-slot display advertising for bid price adjustment with a Multi-task End-to-end Bid Shading(MEBS) method. We prove the optimality of our method theoretically and examine its performance experimentally. Through extensive offline and online experiments, we demonstrate the effectiveness and efficiency of our method, and we obtain a 7.01% lift in Gross Merchandise Volume, a 7.42% lift in Return on Investment, and a 3.26% lift in ad buy count.

### 4. Learning Concave Bid Shading Strategies in Online Auctions via Measure-valued Proximal Optimization

- 作者：Iman Nodozi, Djordje Gligorijevic, Abhishek Halder
- 领域：`cs.LG`（全部：cs.LG, cs.AI, math.OC, stat.ML）
- 发布：2025-09-12 · 更新：2025-09-12
- 链接：https://arxiv.org/abs/2509.10693 · PDF：https://arxiv.org/pdf/2509.10693
- 入库：2026-10-26T22:07:18+08:00

> This work proposes a bid shading strategy for first-price auctions as a measure-valued optimization problem. We consider a standard parametric form for bid shading and formulate the problem as convex optimization over the joint distribution of shading parameters. After each auction, the shading parameter distribution is adapted via a regularized Wasserstein-proximal update with a data-driven energy functional. This energy functional is conditional on the context, i.e., on publisher/user attributes such as domain, ad slot type, device, or location. The proposed algorithm encourages the bid distribution to place more weight on values with higher expected surplus, i.e., where the win probability and the value gap are both large. We show that the resulting measure-valued convex optimization problem admits a closed form solution. A numerical example illustrates the proposed method.

### 5. Strategic Bid Shading in Real-Time Bidding Auctions in Ad Exchange Using Minority Game Theory

- 作者：Dipankar Das
- 领域：`econ.TH`（全部：econ.TH, cs.GT）
- 发布：2025-12-02 · 更新：2025-12-02
- 链接：https://arxiv.org/abs/2512.15717 · PDF：https://arxiv.org/pdf/2512.15717
- 入库：2026-10-26T22:07:18+08:00

> Traditional auction theory posits that bid value exhibits a positive correlation with the probability of securing the auctioned object in ascending auctions. However, under uncertainty and incomplete information, as is characteristic in real-time advertising markets, truthful bidding may not always represent a dominant strategy or yield a Pure Strategy Nash Equilibrium. Real-Time Bidding (RTB) platforms operationalize impression-level auctions via programmatic interfaces, where advertisers compete in first-price auction settings and often resort to bid shading, i.e., strategically submitting bids below their private valuations to optimize payoff. This paper empirically investigates bid shading behaviors and strategic adaptation using large-scale RTB auction data from the Yahoo Webscope dataset. Integrating Minority Game Theory with clustering algorithms and variance-scaling diagnostics, we analyze equilibrium bidding behavior across temporally segmented impression markets. Our results reveal the emergence of minority-based bidding strategies, wherein agents partition hourly ad slots into submarkets and place bids strategically where they anticipate being in the numerical minority. This strategic heterogeneity facilitates reduced expenditure while enhancing win probability, functioning as an endogenous bid shading mechanism. The analysis highlights the computational and economic implications of minority strategies in shaping bidder dynamics and pricing outcomes in decentralized, high-frequency auction environments.
