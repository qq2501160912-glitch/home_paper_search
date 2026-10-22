# arXiv 论文记录

> 查询：conversion-rate · 共 5 篇 · 生成 2026-10-23T02:47:10+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [On the Practice of Scaling Search Conversion Rate Prediction](https://arxiv.org/abs/2605.29232) | cs.IR | 2026-05-28 | [abs](https://arxiv.org/abs/2605.29232) · [pdf](https://arxiv.org/pdf/2605.29232) |
| 2 | [ChoirRec: Semantic User Grouping via LLMs for Conversion Rate Prediction of Low-Activity Users](https://arxiv.org/abs/2510.09393) | cs.IR | 2025-10-10 | [abs](https://arxiv.org/abs/2510.09393) · [pdf](https://arxiv.org/pdf/2510.09393) |
| 3 | [Masked Multi-Domain Network: Multi-Type and Multi-Scenario Conversion Rate Prediction with a Single Model](https://arxiv.org/abs/2403.17425) | cs.IR | 2024-03-26 | [abs](https://arxiv.org/abs/2403.17425) · [pdf](https://arxiv.org/pdf/2403.17425) |
| 4 | [See Beyond a Single View: Multi-Attribution Learning Leads to Better Conversion Rate Prediction](https://arxiv.org/abs/2508.15217) | cs.LG | 2025-08-21 | [abs](https://arxiv.org/abs/2508.15217) · [pdf](https://arxiv.org/pdf/2508.15217) |
| 5 | [Entire Space Cascade Delayed Feedback Modeling for Effective Conversion Rate Prediction](https://arxiv.org/abs/2308.04768) | cs.IR | 2023-08-09 | [abs](https://arxiv.org/abs/2308.04768) · [pdf](https://arxiv.org/pdf/2308.04768) |

## 摘要

### 1. On the Practice of Scaling Search Conversion Rate Prediction

- 作者：James Pak, Jyun-Yu Jiang, Fan Zhang, Sen Wang, Taekmin Kim, Henry Tsai, Vijay Rajaram, Juexin Lin, Mohitdeep Singh, Alessandro Magnani, Johnny Chen, Qian Zhao, Rao Fu, Zhirong Liang, Jordan Gilliland, Winter Jiao
- 领域：`cs.IR`（全部：cs.IR）
- 发布：2026-05-28 · 更新：2026-05-28
- 链接：https://arxiv.org/abs/2605.29232 · PDF：https://arxiv.org/pdf/2605.29232
- 入库：2026-10-23T02:47:10+08:00

> Scaling a Search Conversion Rate (CVR) prediction model, especially in high-traffic environments, presents a challenge: superior model quality needs to be balanced with strict constraints on training cost and serving latency. This paper details an effective approach for scaling modern search CVR prediction models. We begin with an empirical study to understand the scaling performance of search CVR models, analyzing how quality improves as we scale three key factors of model backbone computation, the size of embedding parameters, and the volume of training data. We use a large-scale production dataset, comprising over a year of customer interaction logs from a high-traffic e-commerce platform, to evaluate the scalability of several state-of-the-art architectures and their ensembles. Our key findings are: (1) selecting the right backbone and scaling factors is crucial; (2) the impact of scaling backbone, embedding, and data is largely independent and additive, which has implications for more efficient scaling exploration; (3) a streamlined warmstart strategy can accelerate training iterations while simplifying new updates; (4) inference optimization strategies such as decoupled graph execution and dynamic batching can enable low-latency GPU serving even for high-capacity models. Compared to a baseline of a pre-scaling production model, we ultimately deployed a model trained on 2.5x larger training data with 8x more inference compute while having minimal latency impact. Online A/B tests also demonstrate that our launches achieved a combined +2.6% gain in a key metric of search conversion rate.

### 2. ChoirRec: Semantic User Grouping via LLMs for Conversion Rate Prediction of Low-Activity Users

- 作者：Dakai Zhai, Jiong Gao, Boya Du, Junwei Xu, Qijie Shen, Jialin Zhu, Yuning Jiang
- 领域：`cs.IR`（全部：cs.IR, cs.AI）
- 发布：2025-10-10 · 更新：2025-10-13
- 链接：https://arxiv.org/abs/2510.09393 · PDF：https://arxiv.org/pdf/2510.09393
- 入库：2026-10-23T02:47:10+08:00

> Accurately predicting conversion rates (CVR) for low-activity users remains a fundamental challenge in large-scale e-commerce recommender systems. Existing approaches face three critical limitations: (i) reliance on noisy and unreliable behavioral signals; (ii) insufficient user-level information due to the lack of diverse interaction data; and (iii) a systemic training bias toward high-activity users that overshadows the needs of low-activity users. To address these challenges, we propose ChoirRec, a novel framework that leverages the semantic capabilities of Large Language Models (LLMs) to construct semantic user groups and enhance CVR prediction for low-activity users. With a dual-channel architecture designed for robust cross-user knowledge transfer, ChoirRec comprises three components: (i) a Semantic Group Generation module that utilizes LLMs to form reliable, cross-activity user clusters, thereby filtering out noisy signals; (ii) a Group-aware Hierarchical Representation module that enriches sparse user embeddings with informative group-level priors to mitigate data insufficiency; and (iii) a Group-aware Multi-granularity Modual that employs a dual-channel architecture and adaptive fusion mechanism to ensure effective learning and utilization of group knowledge. We conduct extensive offline and online experiments on Taobao, a leading industrial-scale e-commerce platform. ChoirRec improves GAUC by 1.16\% in offline evaluations, while online A/B testing reveals a 7.24\% increase in order volume, highlighting its substantial practical value in real-world applications.

### 3. Masked Multi-Domain Network: Multi-Type and Multi-Scenario Conversion Rate Prediction with a Single Model

- 作者：Wentao Ouyang, Xiuwu Zhang, Chaofeng Guo, Shukui Ren, Yupei Sui, Kun Zhang, Jinmei Luo, Yunfeng Chen, Dongbo Xu, Xiangzheng Liu, Yanlong Du
- 领域：`cs.IR`（全部：cs.IR, cs.LG）
- 发布：2024-03-26 · 更新：2024-03-26
- 链接：https://arxiv.org/abs/2403.17425 · PDF：https://arxiv.org/pdf/2403.17425
- 备注：CIKM 2023 (larger figures)
- DOI：10.1145/3583780.3614697
- 入库：2026-10-23T02:47:10+08:00

> In real-world advertising systems, conversions have different types in nature and ads can be shown in different display scenarios, both of which highly impact the actual conversion rate (CVR). This results in the multi-type and multi-scenario CVR prediction problem. A desired model for this problem should satisfy the following requirements: 1) Accuracy: the model should achieve fine-grained accuracy with respect to any conversion type in any display scenario. 2) Scalability: the model parameter size should be affordable. 3) Convenience: the model should not require a large amount of effort in data partitioning, subset processing and separate storage. Existing approaches cannot simultaneously satisfy these requirements. For example, building a separate model for each (conversion type, display scenario) pair is neither scalable nor convenient. Building a unified model trained on all the data with conversion type and display scenario included as two features is not accurate enough. In this paper, we propose the Masked Multi-domain Network (MMN) to solve this problem. To achieve the accuracy requirement, we model domain-specific parameters and propose a dynamically weighted loss to account for the loss scale imbalance issue within each mini-batch. To achieve the scalability requirement, we propose a parameter sharing and composition strategy to reduce model parameters from a product space to a sum space. To achieve the convenience requirement, we propose an auto-masking strategy which can take mixed data from all the domains as input. It avoids the overhead caused by data partitioning, individual processing and separate storage. Both offline and online experimental results validate the superiority of MMN for multi-type and multi-scenario CVR prediction. MMN is now the serving model for real-time CVR prediction in UC Toutiao.

### 4. See Beyond a Single View: Multi-Attribution Learning Leads to Better Conversion Rate Prediction

- 作者：Sishuo Chen, Zhangming Chan, Xiang-Rong Sheng, Lei Zhang, Sheng Chen, Chenghuan Hou, Han Zhu, Jian Xu, Bo Zheng
- 领域：`cs.LG`（全部：cs.LG, cs.IR）
- 发布：2025-08-21 · 更新：2025-08-21
- 链接：https://arxiv.org/abs/2508.15217 · PDF：https://arxiv.org/pdf/2508.15217
- 备注：Accepted at CIKM 2025
- 入库：2026-10-23T02:47:10+08:00

> Conversion rate (CVR) prediction is a core component of online advertising systems, where the attribution mechanisms-rules for allocating conversion credit across user touchpoints-fundamentally determine label generation and model optimization. While many industrial platforms support diverse attribution mechanisms (e.g., First-Click, Last-Click, Linear, and Data-Driven Multi-Touch Attribution), conventional approaches restrict model training to labels from a single production-critical attribution mechanism, discarding complementary signals in alternative attribution perspectives. To address this limitation, we propose a novel Multi-Attribution Learning (MAL) framework for CVR prediction that integrates signals from multiple attribution perspectives to better capture the underlying patterns driving user conversions. Specifically, MAL is a joint learning framework consisting of two core components: the Attribution Knowledge Aggregator (AKA) and the Primary Target Predictor (PTP). AKA is implemented as a multi-task learner that integrates knowledge extracted from diverse attribution labels. PTP, in contrast, focuses on the task of generating well-calibrated conversion probabilities that align with the system-optimized attribution metric (e.g., CVR under the Last-Click attribution), ensuring direct compatibility with industrial deployment requirements. Additionally, we propose CAT, a novel training strategy that leverages the Cartesian product of all attribution label combinations to generate enriched supervision signals. This design substantially enhances the performance of the attribution knowledge aggregator. Empirical evaluations demonstrate the superiority of MAL over single-attribution learning baselines, achieving +0.51% GAUC improvement on offline metrics. Online experiments demonstrate that MAL achieved a +2.6% increase in ROI (Return on Investment).

### 5. Entire Space Cascade Delayed Feedback Modeling for Effective Conversion Rate Prediction

- 作者：Yunfeng Zhao, Xu Yan, Xiaoqiang Gui, Shuguang Han, Xiang-Rong Sheng, Guoxian Yu, Jufeng Chen, Zhao Xu, Bo Zheng
- 领域：`cs.IR`（全部：cs.IR）
- 发布：2023-08-09 · 更新：2023-08-09
- 链接：https://arxiv.org/abs/2308.04768 · PDF：https://arxiv.org/pdf/2308.04768
- 备注：Accepted to CIKM'23
- 入库：2026-10-23T02:47:10+08:00

> Conversion rate (CVR) prediction is an essential task for large-scale e-commerce platforms. However, refund behaviors frequently occur after conversion in online shopping systems, which drives us to pay attention to effective conversion for building healthier shopping services. This paper defines the probability of item purchasing without any subsequent refund as an effective conversion rate (ECVR). A simple paradigm for ECVR prediction is to decompose it into two sub-tasks: CVR prediction and post-conversion refund rate (RFR) prediction. However, RFR prediction suffers from data sparsity (DS) and sample selection bias (SSB) issues, as the refund behaviors are only available after user purchase. Furthermore, there is delayed feedback in both conversion and refund events and they are sequentially dependent, named cascade delayed feedback (CDF), which significantly harms data freshness for model training. Previous studies mainly focus on tackling DS and SSB or delayed feedback for a single event. To jointly tackle these issues in ECVR prediction, we propose an Entire space CAscade Delayed feedback modeling (ECAD) method. Specifically, ECAD deals with DS and SSB by constructing two tasks including CVR prediction and conversion \& refund rate (CVRFR) prediction using the entire space modeling framework. In addition, it carefully schedules auxiliary tasks to leverage both conversion and refund time within data to alleviate CDF. Experimental results on the offline industrial dataset and online A/B testing demonstrate the effectiveness of ECAD. In addition, ECAD has been deployed in one of the recommender systems in Alibaba, contributing to a significant improvement of ECVR.
