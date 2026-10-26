# arXiv 论文记录

> 查询：conversion rate prediction · 共 2 篇 · 生成 2026-10-26T22:08:15+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [Modeling Cascaded Delay Feedback for Online Net Conversion Rate Prediction: Benchmark, Insights and Solutions](https://arxiv.org/abs/2601.19965) | cs.LG | 2026-01-27 | [abs](https://arxiv.org/abs/2601.19965) · [pdf](https://arxiv.org/pdf/2601.19965) |
| 2 | [Entire-Space Variational Information Exploitation for Post-Click Conversion Rate Prediction](https://arxiv.org/abs/2502.15687) | cs.IR | 2024-12-17 | [abs](https://arxiv.org/abs/2502.15687) · [pdf](https://arxiv.org/pdf/2502.15687) |

## 摘要

### 1. Modeling Cascaded Delay Feedback for Online Net Conversion Rate Prediction: Benchmark, Insights and Solutions

- 作者：Mingxuan Luo, Guipeng Xv, Sishuo Chen, Xinyu Li, Li Zhang, Zhangming Chan, Xiang-Rong Sheng, Han Zhu, Jian Xu, Bo Zheng, Chen Lin
- 领域：`cs.LG`（全部：cs.LG）
- 发布：2026-01-27 · 更新：2026-01-29
- 链接：https://arxiv.org/abs/2601.19965 · PDF：https://arxiv.org/pdf/2601.19965
- 备注：This paper has been accepted by the ACM Web Conference (WWW) 2026. This is the camera-ready version. Please refer to the published version for citation once available
- 入库：2026-10-26T22:08:15+08:00

> In industrial recommender systems, conversion rate (CVR) is widely used for traffic allocation, but it fails to fully reflect recommendation effectiveness because it ignores refund behavior. To better capture true user satisfaction and business value, net conversion rate (NetCVR), defined as the probability that a clicked item is purchased and not refunded, has been proposed.Unlike CVR, NetCVR prediction involves a more complex multi-stage cascaded delayed feedback process. The two cascaded delays from click to conversion and from conversion to refund have opposite effects, making traditional CVR modeling methods inapplicable. Moreover, the lack of open-source datasets and online continuous training schemes further hinders progress in this area.To address these challenges, we introduce CASCADE (Cascaded Sequences of Conversion and Delayed Refund), the first large-scale open dataset derived from the Taobao app for online continuous NetCVR prediction. Through an in-depth analysis of CASCADE, we identify three key insights: (1) NetCVR exhibits strong temporal dynamics, necessitating online continuous modeling; (2) cascaded modeling of CVR and refund rate outperforms direct NetCVR modeling; and (3) delay time, which correlates with both CVR and refund rate, is an important feature for NetCVR prediction.Based on these insights, we propose TESLA, a continuous NetCVR modeling framework featuring a CVR-refund-rate cascaded architecture, stage-wise debiasing, and a delay-time-aware ranking loss. Extensive experiments demonstrate that TESLA consistently outperforms state-of-the-art methods on CASCADE, achieving absolute improvements of 12.41 percent in RI-AUC and 14.94 percent in RI-PRAUC on NetCVR prediction. The code and dataset are publicly available at https://github.com/alimama-tech/NetCVR.

### 2. Entire-Space Variational Information Exploitation for Post-Click Conversion Rate Prediction

- 作者：Ke Fei, Xinyue Zhang, Jingjing Li
- 领域：`cs.IR`（全部：cs.IR, cs.LG）
- 发布：2024-12-17 · 更新：2024-12-17
- 链接：https://arxiv.org/abs/2502.15687 · PDF：https://arxiv.org/pdf/2502.15687
- 入库：2026-10-26T22:08:15+08:00

> In recommender systems, post-click conversion rate (CVR) estimation is an essential task to model user preferences for items and estimate the value of recommendations. Sample selection bias (SSB) and data sparsity (DS) are two persistent challenges for post-click conversion rate (CVR) estimation. Currently, entire-space approaches that exploit unclicked samples through knowledge distillation are promising to mitigate SSB and DS simultaneously. Existing methods use non-conversion, conversion, or adaptive conversion predictors to generate pseudo labels for unclicked samples. However, they fail to consider the unbiasedness and information limitations of these pseudo labels. Motivated by such analysis, we propose an entire-space variational information exploitation framework (EVI) for CVR prediction. First, EVI uses a conditional entire-space CVR teacher to generate unbiased pseudo labels. Then, it applies variational information exploitation and logit distillation to transfer non-click space information to the target CVR estimator. We conduct extensive offline experiments on six large-scale datasets. EVI demonstrated a 2.25\% average improvement compared to the state-of-the-art baselines.
