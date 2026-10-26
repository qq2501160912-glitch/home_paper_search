# arXiv 论文记录

> 查询：auto bidding · 共 1 篇 · 生成 2026-10-26T22:12:20+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [Strategy-Aware Parameter-Efficient Adaptation for LLM-based Auto-Bidding](https://arxiv.org/abs/2607.24232) | cs.IR | 2026-07-27 | [abs](https://arxiv.org/abs/2607.24232) · [pdf](https://arxiv.org/pdf/2607.24232) |

## 摘要

### 1. Strategy-Aware Parameter-Efficient Adaptation for LLM-based Auto-Bidding

- 作者：Songyue Cai, Lianyu Wang, Shan Gu, Ziru Xu, Jian Xu, Xiaofeng Zhu, Bo Zheng
- 领域：`cs.IR`（全部：cs.IR）
- 发布：2026-07-27 · 更新：2026-08-27
- 链接：https://arxiv.org/abs/2607.24232 · PDF：https://arxiv.org/pdf/2607.24232
- 入库：2026-10-26T22:12:20+08:00

> Advertising bidding has evolved from manual strategies to auto-bidding systems better adapted for large-scale, dynamic auction environments. While recent advances in Large Language Models (LLMs) offer strong reasoning for auto-bidding, existing methods suffer from shallow trajectory-text interactions and require costly fine-tuning, hindering the efficient use of pretrained knowledge under diverse constraints. To address these challenges, we propose SAGE, a novel Strategy-aware Auto-bidding framework Guided by LLMs for Efficient bidding. SAGE introduces a parameter-efficient multi-modal alignment framework for constrained auto-bidding with LLMs. Specifically, SAGE comprises three key components: (i) the position augmentation module adopts temporal-semantic positional embeddings to effectively capture the intrinsic dynamics and semantic structures; (ii) the text alignment module leverages gated cross-attention to align the embedding spaces of trajectory and text modalities, enabling effective multi-modal fusion while alleviating the computational overhead caused by long trajectories; (iii) the constraint-gated LoRA module employs constraints as routing signals, activating only a small subset of experts to adapt the behavior of a frozen LLM efficiently. Extensive experiments on large-scale auto-bidding benchmark demonstrate that SAGE consistently achieves superior performance while tuning less than 10% of the trainable parameters required by full fine-tuning. Ablation studies further validate the critical contribution of each component to the framework's overall performance.
