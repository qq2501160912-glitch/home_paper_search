# arXiv 论文记录

> 查询：conversion rate prediction · 共 5 篇 · 生成 2026-10-23T02:06:08+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [Entire Space Cascade Delayed Feedback Modeling for Effective Conversion Rate Prediction](https://arxiv.org/abs/2308.04768) | cs.IR | 2023-08-09 | [abs](https://arxiv.org/abs/2308.04768) · [pdf](https://arxiv.org/pdf/2308.04768) |
| 2 | [Contrastive Learning for Conversion Rate Prediction](https://arxiv.org/abs/2307.05974) | cs.IR | 2023-07-12 | [abs](https://arxiv.org/abs/2307.05974) · [pdf](https://arxiv.org/pdf/2307.05974) |
| 3 | [On the Practice of Deep Hierarchical Ensemble Network for Ad Conversion Rate Prediction](https://arxiv.org/abs/2504.08169) | cs.LG | 2025-04-10 | [abs](https://arxiv.org/abs/2504.08169) · [pdf](https://arxiv.org/pdf/2504.08169) |
| 4 | [Modeling Cascaded Delay Feedback for Online Net Conversion Rate Prediction: Benchmark, Insights and Solutions](https://arxiv.org/abs/2601.19965) | cs.LG | 2026-01-27 | [abs](https://arxiv.org/abs/2601.19965) · [pdf](https://arxiv.org/pdf/2601.19965) |
| 5 | [Conversion rate prediction in online advertising: modeling techniques, performance evaluation and future directions](https://arxiv.org/abs/2512.01171) | cs.IR | 2025-12-01 | [abs](https://arxiv.org/abs/2512.01171) · [pdf](https://arxiv.org/pdf/2512.01171) |

## 摘要

### 1. Entire Space Cascade Delayed Feedback Modeling for Effective Conversion Rate Prediction

- 作者：Yunfeng Zhao, Xu Yan, Xiaoqiang Gui, Shuguang Han, Xiang-Rong Sheng, Guoxian Yu, Jufeng Chen, Zhao Xu, Bo Zheng
- 领域：`cs.IR`（全部：cs.IR）
- 发布：2023-08-09 · 更新：2023-08-09
- 链接：https://arxiv.org/abs/2308.04768 · PDF：https://arxiv.org/pdf/2308.04768
- 备注：Accepted to CIKM'23
- 入库：2026-10-23T02:06:08+08:00

> Conversion rate (CVR) prediction is an essential task for large-scale e-commerce platforms. However, refund behaviors frequently occur after conversion in online shopping systems, which drives us to pay attention to effective conversion for building healthier shopping services. This paper defines the probability of item purchasing without any subsequent refund as an effective conversion rate (ECVR). A simple paradigm for ECVR prediction is to decompose it into two sub-tasks: CVR prediction and post-conversion refund rate (RFR) prediction. However, RFR prediction suffers from data sparsity (DS) and sample selection bias (SSB) issues, as the refund behaviors are only available after user purchase. Furthermore, there is delayed feedback in both conversion and refund events and they are sequentially dependent, named cascade delayed feedback (CDF), which significantly harms data freshness for model training. Previous studies mainly focus on tackling DS and SSB or delayed feedback for a single event. To jointly tackle these issues in ECVR prediction, we propose an Entire space CAscade Delayed feedback modeling (ECAD) method. Specifically, ECAD deals with DS and SSB by constructing two tasks including CVR prediction and conversion \& refund rate (CVRFR) prediction using the entire space modeling framework. In addition, it carefully schedules auxiliary tasks to leverage both conversion and refund time within data to alleviate CDF. Experimental results on the offline industrial dataset and online A/B testing demonstrate the effectiveness of ECAD. In addition, ECAD has been deployed in one of the recommender systems in Alibaba, contributing to a significant improvement of ECVR.

### 2. Contrastive Learning for Conversion Rate Prediction

- 作者：Wentao Ouyang, Rui Dong, Xiuwu Zhang, Chaofeng Guo, Jinmei Luo, Xiangzheng Liu, Yanlong Du
- 领域：`cs.IR`（全部：cs.IR, cs.LG）
- 发布：2023-07-12 · 更新：2023-07-12
- 链接：https://arxiv.org/abs/2307.05974 · PDF：https://arxiv.org/pdf/2307.05974
- 备注：SIGIR 2023
- DOI：10.1145/3539618.3591968
- 入库：2026-10-23T02:06:08+08:00

> Conversion rate (CVR) prediction plays an important role in advertising systems. Recently, supervised deep neural network-based models have shown promising performance in CVR prediction. However, they are data hungry and require an enormous amount of training data. In online advertising systems, although there are millions to billions of ads, users tend to click only a small set of them and to convert on an even smaller set. This data sparsity issue restricts the power of these deep models. In this paper, we propose the Contrastive Learning for CVR prediction (CL4CVR) framework. It associates the supervised CVR prediction task with a contrastive learning task, which can learn better data representations exploiting abundant unlabeled data and improve the CVR prediction performance. To tailor the contrastive learning task to the CVR prediction problem, we propose embedding masking (EM), rather than feature masking, to create two views of augmented samples. We also propose a false negative elimination (FNE) component to eliminate samples with the same feature as the anchor sample, to account for the natural property in user behavior data. We further propose a supervised positive inclusion (SPI) component to include additional positive samples for each anchor sample, in order to make full use of sparse but precious user conversion events. Experimental results on two real-world conversion datasets demonstrate the superior performance of CL4CVR. The source code is available at https://github.com/DongRuiHust/CL4CVR.

### 3. On the Practice of Deep Hierarchical Ensemble Network for Ad Conversion Rate Prediction

- 作者：Jinfeng Zhuang, Yinrui Li, Runze Su, Ke Xu, Zhixuan Shao, Kungang Li, Ling Leng, Han Sun, Meng Qi, Yixiong Meng, Yang Tang, Zhifang Liu, Qifei Shen, Aayush Mudgal, Caleb Lu, Jie Liu, Hongda Shen
- 领域：`cs.LG`（全部：cs.LG, cs.AI, stat.AP, stat.ML）
- 发布：2025-04-10 · 更新：2025-04-23
- 链接：https://arxiv.org/abs/2504.08169 · PDF：https://arxiv.org/pdf/2504.08169
- 备注：Accepted by WWW 2025
- 入库：2026-10-23T02:06:08+08:00

> The predictions of click through rate (CTR) and conversion rate (CVR) play a crucial role in the success of ad-recommendation systems. A Deep Hierarchical Ensemble Network (DHEN) has been proposed to integrate multiple feature crossing modules and has achieved great success in CTR prediction. However, its performance for CVR prediction is unclear in the conversion ads setting, where an ad bids for the probability of a user's off-site actions on a third party website or app, including purchase, add to cart, sign up, etc. A few challenges in DHEN: 1) What feature-crossing modules (MLP, DCN, Transformer, to name a few) should be included in DHEN? 2) How deep and wide should DHEN be to achieve the best trade-off between efficiency and efficacy? 3) What hyper-parameters to choose in each feature-crossing module? Orthogonal to the model architecture, the input personalization features also significantly impact model performance with a high degree of freedom. In this paper, we attack this problem and present our contributions biased to the applied data science side, including: First, we propose a multitask learning framework with DHEN as the single backbone model architecture to predict all CVR tasks, with a detailed study on how to make DHEN work effectively in practice; Second, we build both on-site real-time user behavior sequences and off-site conversion event sequences for CVR prediction purposes, and conduct ablation study on its importance; Last but not least, we propose a self-supervised auxiliary loss to predict future actions in the input sequence, to help resolve the label sparseness issue in CVR prediction. Our method achieves state-of-the-art performance compared to previous single feature crossing modules with pre-trained user personalization features.

### 4. Modeling Cascaded Delay Feedback for Online Net Conversion Rate Prediction: Benchmark, Insights and Solutions

- 作者：Mingxuan Luo, Guipeng Xv, Sishuo Chen, Xinyu Li, Li Zhang, Zhangming Chan, Xiang-Rong Sheng, Han Zhu, Jian Xu, Bo Zheng, Chen Lin
- 领域：`cs.LG`（全部：cs.LG）
- 发布：2026-01-27 · 更新：2026-01-29
- 链接：https://arxiv.org/abs/2601.19965 · PDF：https://arxiv.org/pdf/2601.19965
- 备注：This paper has been accepted by the ACM Web Conference (WWW) 2026. This is the camera-ready version. Please refer to the published version for citation once available
- 入库：2026-10-23T02:06:08+08:00

> In industrial recommender systems, conversion rate (CVR) is widely used for traffic allocation, but it fails to fully reflect recommendation effectiveness because it ignores refund behavior. To better capture true user satisfaction and business value, net conversion rate (NetCVR), defined as the probability that a clicked item is purchased and not refunded, has been proposed.Unlike CVR, NetCVR prediction involves a more complex multi-stage cascaded delayed feedback process. The two cascaded delays from click to conversion and from conversion to refund have opposite effects, making traditional CVR modeling methods inapplicable. Moreover, the lack of open-source datasets and online continuous training schemes further hinders progress in this area.To address these challenges, we introduce CASCADE (Cascaded Sequences of Conversion and Delayed Refund), the first large-scale open dataset derived from the Taobao app for online continuous NetCVR prediction. Through an in-depth analysis of CASCADE, we identify three key insights: (1) NetCVR exhibits strong temporal dynamics, necessitating online continuous modeling; (2) cascaded modeling of CVR and refund rate outperforms direct NetCVR modeling; and (3) delay time, which correlates with both CVR and refund rate, is an important feature for NetCVR prediction.Based on these insights, we propose TESLA, a continuous NetCVR modeling framework featuring a CVR-refund-rate cascaded architecture, stage-wise debiasing, and a delay-time-aware ranking loss. Extensive experiments demonstrate that TESLA consistently outperforms state-of-the-art methods on CASCADE, achieving absolute improvements of 12.41 percent in RI-AUC and 14.94 percent in RI-PRAUC on NetCVR prediction. The code and dataset are publicly available at https://github.com/alimama-tech/NetCVR.

### 5. Conversion rate prediction in online advertising: modeling techniques, performance evaluation and future directions

- 作者：Tao Xue, Yanwu Yang, Panyu Zhai
- 领域：`cs.IR`（全部：cs.IR, cs.AI, cs.LG）
- 发布：2025-12-01 · 更新：2025-12-01
- 链接：https://arxiv.org/abs/2512.01171 · PDF：https://arxiv.org/pdf/2512.01171
- 备注：99 pages, 15 figures, 7 tables
- 期刊/会议：Information Processing & Management, 63(2), 104450 (2026)
- DOI：10.1016/j.ipm.2025.104450.
- 入库：2026-10-23T02:06:08+08:00

> Conversion and conversion rate (CVR) prediction play a critical role in efficient advertising decision-making. In past decades, although researchers have developed plenty of models for CVR prediction, the methodological evolution and relationships between different techniques have been precluded. In this paper, we conduct a comprehensive literature review on CVR prediction in online advertising, and classify state-of-the-art CVR prediction models into six categories with respect to the underlying techniques and elaborate on connections between these techniques. For each category of models, we present the framework of underlying techniques, their advantages and disadvantages, and discuss how they are utilized for CVR prediction. Moreover, we summarize the performance of various CVR prediction models on public and proprietary datasets. Finally, we identify research trends, major challenges, and promising future directions. We observe that results of performance evaluation reported in prior studies are not unanimous; semantics-enriched, attribution-enhanced, debiased CVR prediction and jointly modeling CTR and CVR prediction would be promising directions to explore in the future. This review is expected to provide valuable references and insights for future researchers and practitioners in this area.
