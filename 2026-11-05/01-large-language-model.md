# arXiv 论文记录

> 查询：large language model · 共 5 篇 · 生成 2026-11-05T00:53:04+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [Reinforcement Learning Meets Large Language Models: A Survey of Advancements and Applications Across the LLM Lifecycle](https://arxiv.org/abs/2509.16679) | cs.CL | 2025-09-20 | [abs](https://arxiv.org/abs/2509.16679) · [pdf](https://arxiv.org/pdf/2509.16679) |
| 2 | [CROP: Token-Efficient Reasoning in Large Language Models via Regularized Prompt Optimization](https://arxiv.org/abs/2604.14214) | cs.CL | 2026-04-08 | [abs](https://arxiv.org/abs/2604.14214) · [pdf](https://arxiv.org/pdf/2604.14214) |
| 3 | [Behavioral and Representational Evidence of Binomial Ordering Preferences in Large Language Models](https://arxiv.org/abs/2606.21645) | cs.CL | 2026-06-19 | [abs](https://arxiv.org/abs/2606.21645) · [pdf](https://arxiv.org/pdf/2606.21645) |
| 4 | [A Survey of AIOps in the Era of Large Language Models](https://arxiv.org/abs/2507.12472) | cs.SE | 2025-06-23 | [abs](https://arxiv.org/abs/2507.12472) · [pdf](https://arxiv.org/pdf/2507.12472) |
| 5 | [Reranking Answers of Large Language Models with Knowledge Graphs](https://arxiv.org/abs/2610.25185) | cs.CL | 2026-10-18 | [abs](https://arxiv.org/abs/2610.25185) · [pdf](https://arxiv.org/pdf/2610.25185) |

## 摘要

### 1. Reinforcement Learning Meets Large Language Models: A Survey of Advancements and Applications Across the LLM Lifecycle

- 作者：Keliang Liu, Dingkang Yang, Ziyun Qian, Weijie Yin, Yuchi Wang, Hongsheng Li, Jun Liu, Peng Zhai, Yang Liu, Lihua Zhang
- 领域：`cs.CL`（全部：cs.CL）
- 发布：2025-09-20 · 更新：2025-09-20
- 链接：https://arxiv.org/abs/2509.16679 · PDF：https://arxiv.org/pdf/2509.16679
- 备注：A Survey of Reinforcement Learning for Large Language Models
- 入库：2026-11-05T00:52:29+08:00

> In recent years, training methods centered on Reinforcement Learning (RL) have markedly enhanced the reasoning and alignment performance of Large Language Models (LLMs), particularly in understanding human intents, following user instructions, and bolstering inferential strength. Although existing surveys offer overviews of RL augmented LLMs, their scope is often limited, failing to provide a comprehensive summary of how RL operates across the full lifecycle of LLMs. We systematically review the theoretical and practical advancements whereby RL empowers LLMs, especially Reinforcement Learning with Verifiable Rewards (RLVR). First, we briefly introduce the basic theory of RL. Second, we thoroughly detail application strategies for RL across various phases of the LLM lifecycle, including pre-training, alignment fine-tuning, and reinforced reasoning. In particular, we emphasize that RL methods in the reinforced reasoning phase serve as a pivotal driving force for advancing model reasoning to its limits. Next, we collate existing datasets and evaluation benchmarks currently used for RL fine-tuning, spanning human-annotated datasets, AI-assisted preference data, and program-verification-style corpora. Subsequently, we review the mainstream open-source tools and training frameworks available, providing clear practical references for subsequent research. Finally, we analyse the future challenges and trends in the field of RL-enhanced LLMs. This survey aims to present researchers and practitioners with the latest developments and frontier trends at the intersection of RL and LLMs, with the goal of fostering the evolution of LLMs that are more intelligent, generalizable, and secure.

### 2. CROP: Token-Efficient Reasoning in Large Language Models via Regularized Prompt Optimization

- 作者：Deep Shah, Sanket Badhe, Nehal Kathrotia, Priyanka Tiwari
- 领域：`cs.CL`（全部：cs.CL, cs.AI）
- 发布：2026-04-08 · 更新：2026-04-08
- 链接：https://arxiv.org/abs/2604.14214 · PDF：https://arxiv.org/pdf/2604.14214
- 备注：Accepted at ICLR 2026 Workshop on Logical Reasoning of Large Language Models
- 入库：2026-11-05T00:52:29+08:00

> Large Language Models utilizing reasoning techniques improve task performance but incur significant latency and token costs due to verbose generation. Existing automatic prompt optimization(APO) frameworks target task accuracy exclusively at the expense of generating long reasoning traces. We propose Cost-Regularized Optimization of Prompts (CROP), an APO method that introduces regularization on response length by generating textual feedback in addition to standard accuracy feedback. This forces the optimization process to produce prompts that elicit concise responses containing only critical information and reasoning. We evaluate our approach on complex reasoning datasets, specifically GSM8K, LogiQA and BIG-Bench Hard. We achieved an 80.6\% reduction in token consumption while maintaining competitive accuracy, seeing only a nominal decline in performance. This presents a pragmatic solution for deploying token-efficient and cost-effective agentic AI systems in production pipelines.

### 3. Behavioral and Representational Evidence of Binomial Ordering Preferences in Large Language Models

- 作者：Zhiqing Yang, Yilun Liu, Yunpu Ma, Volker Tresp, Hinrich Schütze
- 领域：`cs.CL`（全部：cs.CL, cs.LG）
- 发布：2026-06-19 · 更新：2026-06-19
- 链接：https://arxiv.org/abs/2606.21645 · PDF：https://arxiv.org/pdf/2606.21645
- 备注：Code and data are publicly available at https://github.com/Zhi-qing-Yang/Linguistic-Binomials-in-Large-Language-Models
- 入库：2026-11-05T00:52:29+08:00

> Large language models (LLMs) can readily reproduce conventional expressions, yet their ability to model gradient frequency distributions remains underexplored. We investigate this using linguistic binomials, such as men and women, where both word permutations are grammatically valid but exhibit distinct, cross-linguistic variations in conventionality. We formalize binomial ordering as a distributional alignment problem, and construct a multilingual dataset of 600 binomial pairs across 8 languages. With categorical and distributional metrics, we measure and compare the corpus-derived preferences with model-induced ordering probabilities of 6 open-weight LLMs. While models often behaviorally recover the dominant corpus-preferred order, particularly for strongly conventionalized pairs, they align less well with the exact corpus preference distributions. This suggests that apparent directional order overstates how faithfully LLMs capture the statistical nuances of language use. Sparse probing verifies that the concept of preference strength is partially encoded among middle-to-late layers, and steering along probe-derived directions alters model-induced ordering distributions, demonstrating that the statistical behavioral preference of LLMs can be mechanistically measured and manipulated via internal representations.

### 4. A Survey of AIOps in the Era of Large Language Models

- 作者：Lingzhe Zhang, Tong Jia, Mengxi Jia, Yifan Wu, Aiwei Liu, Yong Yang, Zhonghai Wu, Xuming Hu, Philip S. Yu, Ying Li
- 领域：`cs.SE`（全部：cs.SE, cs.CL）
- 发布：2025-06-23 · 更新：2025-06-23
- 链接：https://arxiv.org/abs/2507.12472 · PDF：https://arxiv.org/pdf/2507.12472
- 备注：Accepted By CSUR, an extended version of "A Survey of AIOps for Failure Management in the Era of Large Language Models" [arXiv:2406.11213]
- 入库：2026-11-05T00:52:29+08:00

> As large language models (LLMs) grow increasingly sophisticated and pervasive, their application to various Artificial Intelligence for IT Operations (AIOps) tasks has garnered significant attention. However, a comprehensive understanding of the impact, potential, and limitations of LLMs in AIOps remains in its infancy. To address this gap, we conducted a detailed survey of LLM4AIOps, focusing on how LLMs can optimize processes and improve outcomes in this domain. We analyzed 183 research papers published between January 2020 and December 2024 to answer four key research questions (RQs). In RQ1, we examine the diverse failure data sources utilized, including advanced LLM-based processing techniques for legacy data and the incorporation of new data sources enabled by LLMs. RQ2 explores the evolution of AIOps tasks, highlighting the emergence of novel tasks and the publication trends across these tasks. RQ3 investigates the various LLM-based methods applied to address AIOps challenges. Finally, RQ4 reviews evaluation methodologies tailored to assess LLM-integrated AIOps approaches. Based on our findings, we discuss the state-of-the-art advancements and trends, identify gaps in existing research, and propose promising directions for future exploration.

### 5. Reranking Answers of Large Language Models with Knowledge Graphs

- 作者：Mikhail Salnikov, Hai Le, Olga Tsymboi, Ivan Lazichny, Dmitrii Iarosh, Egor Cheremiskin, Andrey Savchenko, Dmitry Simakov, Alexander Panchenko
- 领域：`cs.CL`（全部：cs.CL, cs.AI）
- 发布：2026-10-18 · 更新：2026-10-18
- 链接：https://arxiv.org/abs/2610.25185 · PDF：https://arxiv.org/pdf/2610.25185
- 备注：37 pages. Accepted for the Semantic Web journal (tracking no. 4075-5289); not published. https://www.semantic-web-journal.net/content/reranking-answers-large-language-models-knowledge-graphs-1
- 入库：2026-11-05T00:52:29+08:00

> Answering natural language questions over knowledge graph data is challenging due to the vast number of facts, which can be difficult to process and navigate. One potential solution for this issue is to use mined subgraphs related to the query, although this process still requires extracting these subgraphs. This research presents a solution for extracting subgraphs related to entity candidates from a question-and-answer set, which can be obtained by inferring a large language model by calculating the shortest paths between entities. The proposed approaches detail various features that can be extracted from the subgraphs and reranking models to select the most probable answers from a list of candidates. Experiments were conducted on Wikidata to evaluate the effectiveness of the proposed approaches. This involved enumerating all the main feature types that can be extracted from mined subgraphs and a detailed analysis of the proposed features and reranking method combinations. In addition, a public web application that provides a useful web tool for studying the graph space between question and answer entities has been developed to work with subgraphs. This includes visualization of the extracted subgraph and automatic generation of natural language text to describe it.
