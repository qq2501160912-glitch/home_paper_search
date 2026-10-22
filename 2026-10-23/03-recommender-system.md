# arXiv 论文记录

> 查询：recommender system · 共 5 篇 · 生成 2026-10-23T01:53:13+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [GenRec: Large Language Model for Generative Recommendation](https://arxiv.org/abs/2307.00457) | cs.IR | 2023-07-02 | [abs](https://arxiv.org/abs/2307.00457) · [pdf](https://arxiv.org/pdf/2307.00457) |
| 2 | [XRec: Large Language Models for Explainable Recommendation](https://arxiv.org/abs/2406.02377) | cs.IR | 2024-06-04 | [abs](https://arxiv.org/abs/2406.02377) · [pdf](https://arxiv.org/pdf/2406.02377) |
| 3 | [Large Language Models Make Sample-Efficient Recommender Systems](https://arxiv.org/abs/2406.02368) | cs.IR | 2024-06-04 | [abs](https://arxiv.org/abs/2406.02368) · [pdf](https://arxiv.org/pdf/2406.02368) |
| 4 | [Understanding and Mitigating Training Instability in Large-Scale Recommender Systems: A Cascade Perspective](https://arxiv.org/abs/2610.14394) | cs.IR | 2026-10-09 | [abs](https://arxiv.org/abs/2610.14394) · [pdf](https://arxiv.org/pdf/2610.14394) |
| 5 | [LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation](https://arxiv.org/abs/2002.02126) | cs.IR | 2020-02-06 | [abs](https://arxiv.org/abs/2002.02126) · [pdf](https://arxiv.org/pdf/2002.02126) |

## 摘要

### 1. GenRec: Large Language Model for Generative Recommendation

- 作者：Jianchao Ji, Zelong Li, Shuyuan Xu, Wenyue Hua, Yingqiang Ge, Juntao Tan, Yongfeng Zhang
- 领域：`cs.IR`（全部：cs.IR, cs.AI, cs.CL, cs.LG）
- 发布：2023-07-02 · 更新：2023-07-04
- 链接：https://arxiv.org/abs/2307.00457 · PDF：https://arxiv.org/pdf/2307.00457
- 入库：-

> In recent years, large language models (LLM) have emerged as powerful tools for diverse natural language processing tasks. However, their potential for recommender systems under the generative recommendation paradigm remains relatively unexplored. This paper presents an innovative approach to recommendation systems using large language models (LLMs) based on text data. In this paper, we present a novel LLM for generative recommendation (GenRec) that utilized the expressive power of LLM to directly generate the target item to recommend, rather than calculating ranking score for each candidate item one by one as in traditional discriminative recommendation. GenRec uses LLM's understanding ability to interpret context, learn user preferences, and generate relevant recommendation. Our proposed approach leverages the vast knowledge encoded in large language models to accomplish recommendation tasks. We first we formulate specialized prompts to enhance the ability of LLM to comprehend recommendation tasks. Subsequently, we use these prompts to fine-tune the LLaMA backbone LLM on a dataset of user-item interactions, represented by textual data, to capture user preferences and item characteristics. Our research underscores the potential of LLM-based generative recommendation in revolutionizing the domain of recommendation systems and offers a foundational framework for future explorations in this field. We conduct extensive experiments on benchmark datasets, and the experiments shows that our GenRec has significant better results on large dataset.

### 2. XRec: Large Language Models for Explainable Recommendation

- 作者：Qiyao Ma, Xubin Ren, Chao Huang
- 领域：`cs.IR`（全部：cs.IR, cs.AI, cs.CL）
- 发布：2024-06-04 · 更新：2024-09-22
- 链接：https://arxiv.org/abs/2406.02377 · PDF：https://arxiv.org/pdf/2406.02377
- 备注：Accepted to EMNLP 2024 Findings
- 入库：-

> Recommender systems help users navigate information overload by providing personalized recommendations aligned with their preferences. Collaborative Filtering (CF) is a widely adopted approach, but while advanced techniques like graph neural networks (GNNs) and self-supervised learning (SSL) have enhanced CF models for better user representations, they often lack the ability to provide explanations for the recommended items. Explainable recommendations aim to address this gap by offering transparency and insights into the recommendation decision-making process, enhancing users' understanding. This work leverages the language capabilities of Large Language Models (LLMs) to push the boundaries of explainable recommender systems. We introduce a model-agnostic framework called XRec, which enables LLMs to provide comprehensive explanations for user behaviors in recommender systems. By integrating collaborative signals and designing a lightweight collaborative adaptor, the framework empowers LLMs to understand complex patterns in user-item interactions and gain a deeper understanding of user preferences. Our extensive experiments demonstrate the effectiveness of XRec, showcasing its ability to generate comprehensive and meaningful explanations that outperform baseline approaches in explainable recommender systems. We open-source our model implementation at https://github.com/HKUDS/XRec.

### 3. Large Language Models Make Sample-Efficient Recommender Systems

- 作者：Jianghao Lin, Xinyi Dai, Rong Shan, Bo Chen, Ruiming Tang, Yong Yu, Weinan Zhang
- 领域：`cs.IR`（全部：cs.IR, cs.CL）
- 发布：2024-06-04 · 更新：2024-06-04
- 链接：https://arxiv.org/abs/2406.02368 · PDF：https://arxiv.org/pdf/2406.02368
- 备注：Accepted by Frontier of Computer Science
- 入库：-

> Large language models (LLMs) have achieved remarkable progress in the field of natural language processing (NLP), demonstrating remarkable abilities in producing text that resembles human language for various tasks. This opens up new opportunities for employing them in recommender systems (RSs). In this paper, we specifically examine the sample efficiency of LLM-enhanced recommender systems, which pertains to the model's capacity to attain superior performance with a limited quantity of training data. Conventional recommendation models (CRMs) often need a large amount of training data because of the sparsity of features and interactions. Hence, we propose and verify our core viewpoint: Large Language Models Make Sample-Efficient Recommender Systems. We propose a simple yet effective framework (i.e., Laser) to validate the viewpoint from two aspects: (1) LLMs themselves are sample-efficient recommenders; and (2) LLMs, as feature generators and encoders, make CRMs more sample-efficient. Extensive experiments on two public datasets show that Laser requires only a small fraction of training samples to match or even surpass CRMs that are trained on the entire training set, demonstrating superior sample efficiency.

### 4. Understanding and Mitigating Training Instability in Large-Scale Recommender Systems: A Cascade Perspective

- 作者：Yuening Li, Zeyu Wang, Zhen Zhang, Jiayi Liu, Zhimeng Jiang, Yuji Roh, Weikai Xu, Mingyan Gao, Onkar Dalal, Chuan He, Liang Liu
- 领域：`cs.IR`（全部：cs.IR, cs.LG）
- 发布：2026-10-09 · 更新：2026-10-09
- 链接：https://arxiv.org/abs/2610.14394 · PDF：https://arxiv.org/pdf/2610.14394
- 入库：-

> Training large-scale recommender systems on dynamic industrial platforms, such as Short-Form Video (SFV) services with billions of daily interactions, faces critical stability challenges. Rapid distribution shifts in user data and increasing model complexity frequently trigger a divergence cascade, typically initiating with gradient explosion, propagating to weight explosion, and culminating in loss explosion. This G-W-L cascade severely impedes model convergence and performance. This paper provides a systematic analysis of this G-W-L cascade within an industrial SFV recommender context. We then propose and evaluate a structured mitigation framework where interventions are explicitly mapped to counteract specific stages of the cascade: gradient (G) control, weight/activation (W) stabilization, and loss (L) shaping. Our contribution provides a structured framework for understanding and tackling training divergence, offering practical insights for deploying robust, continuously updated recommenders in large-scale, non-stationary settings. We empirically validate the effectiveness of these strategies on a major industrial SFV recommendation system.

### 5. LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation

- 作者：Xiangnan He, Kuan Deng, Xiang Wang, Yan Li, Yongdong Zhang, Meng Wang
- 领域：`cs.IR`（全部：cs.IR, cs.LG）
- 发布：2020-02-06 · 更新：2020-07-07
- 链接：https://arxiv.org/abs/2002.02126 · PDF：https://arxiv.org/pdf/2002.02126
- 备注：Accepted by SIGIR
- 入库：-

> Graph Convolution Network (GCN) has become new state-of-the-art for collaborative filtering. Nevertheless, the reasons of its effectiveness for recommendation are not well understood. Existing work that adapts GCN to recommendation lacks thorough ablation analyses on GCN, which is originally designed for graph classification tasks and equipped with many neural network operations. However, we empirically find that the two most common designs in GCNs -- feature transformation and nonlinear activation -- contribute little to the performance of collaborative filtering. Even worse, including them adds to the difficulty of training and degrades recommendation performance. In this work, we aim to simplify the design of GCN to make it more concise and appropriate for recommendation. We propose a new model named LightGCN, including only the most essential component in GCN -- neighborhood aggregation -- for collaborative filtering. Specifically, LightGCN learns user and item embeddings by linearly propagating them on the user-item interaction graph, and uses the weighted sum of the embeddings learned at all layers as the final embedding. Such simple, linear, and neat model is much easier to implement and train, exhibiting substantial improvements (about 16.0\% relative improvement on average) over Neural Graph Collaborative Filtering (NGCF) -- a state-of-the-art GCN-based recommender model -- under exactly the same experimental setting. Further analyses are provided towards the rationality of the simple LightGCN from both analytical and empirical perspectives.
