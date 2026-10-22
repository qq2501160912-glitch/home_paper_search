# arXiv 论文记录

> 查询：transformer · 共 1 篇 · 生成 2026-10-23T02:17:22+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [Music Transformer](https://arxiv.org/abs/1809.04281) | cs.LG | 2018-09-12 | [abs](https://arxiv.org/abs/1809.04281) · [pdf](https://arxiv.org/pdf/1809.04281) |

## 摘要

### 1. Music Transformer

- 作者：Cheng-Zhi Anna Huang, Ashish Vaswani, Jakob Uszkoreit, Noam Shazeer, Ian Simon, Curtis Hawthorne, Andrew M. Dai, Matthew D. Hoffman, Monica Dinculescu, Douglas Eck
- 领域：`cs.LG`（全部：cs.LG, cs.SD, eess.AS, stat.ML）
- 发布：2018-09-12 · 更新：2018-12-12
- 链接：https://arxiv.org/abs/1809.04281 · PDF：https://arxiv.org/pdf/1809.04281
- 备注：Improved skewing section and accompanying figures. Previous titles are "An Improved Relative Self-Attention Mechanism for Transformer with Application to Music Generation" and "Music Transformer"
- 入库：2026-10-23T02:17:22+08:00

> Music relies heavily on repetition to build structure and meaning. Self-reference occurs on multiple timescales, from motifs to phrases to reusing of entire sections of music, such as in pieces with ABA structure. The Transformer (Vaswani et al., 2017), a sequence model based on self-attention, has achieved compelling results in many generation tasks that require maintaining long-range coherence. This suggests that self-attention might also be well-suited to modeling music. In musical composition and performance, however, relative timing is critically important. Existing approaches for representing relative positional information in the Transformer modulate attention based on pairwise distance (Shaw et al., 2018). This is impractical for long sequences such as musical compositions since their memory complexity for intermediate relative information is quadratic in the sequence length. We propose an algorithm that reduces their intermediate memory requirement to linear in the sequence length. This enables us to demonstrate that a Transformer with our modified relative attention mechanism can generate minute-long compositions (thousands of steps, four times the length modeled in Oore et al., 2018) with compelling structure, generate continuations that coherently elaborate on a given motif, and in a seq2seq setup generate accompaniments conditioned on melodies. We evaluate the Transformer with our relative attention mechanism on two datasets, JSB Chorales and Piano-e-Competition, and obtain state-of-the-art results on the latter.
