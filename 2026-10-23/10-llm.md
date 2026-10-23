# arXiv 论文记录

> 查询：LLM · 共 3 篇 · 生成 2026-10-23T20:37:10+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [EpiSEM-Bench: Evaluating Safety and Evidence Recovery in LLM Agents under Missing Evidence](https://arxiv.org/abs/2610.31650) | cs.AI | 2026-10-22 | [abs](https://arxiv.org/abs/2610.31650) · [pdf](https://arxiv.org/pdf/2610.31650) |
| 2 | [Who Is Sycophantic to Whom? Confident LLMs, Human Deference, and the Collapse of Trust Calibration](https://arxiv.org/abs/2610.31579) | cs.AI | 2026-10-22 | [abs](https://arxiv.org/abs/2610.31579) · [pdf](https://arxiv.org/pdf/2610.31579) |
| 3 | [VERA: A Responsible AI Dashboard for Assessing LLM Deployments in Light of the EU AI Act](https://arxiv.org/abs/2610.31588) | cs.SE | 2026-10-22 | [abs](https://arxiv.org/abs/2610.31588) · [pdf](https://arxiv.org/pdf/2610.31588) |

## 摘要

### 1. EpiSEM-Bench: Evaluating Safety and Evidence Recovery in LLM Agents under Missing Evidence

- 作者：Qijin Zhang, Hanzhen Wang, Yuehan Zhao, Haoyu Dai, Yao Shu, Zhongxiang Dai, Shuang Qiu
- 领域：`cs.AI`（全部：cs.AI, cs.LG）
- 发布：2026-10-22 · 更新：2026-10-22
- 链接：https://arxiv.org/abs/2610.31650 · PDF：https://arxiv.org/pdf/2610.31650
- 入库：2026-10-23T20:37:10+08:00

> Tool-using language model agents rely on environmental facts to decide whether an action is permitted. When a tool response omits a safety-relevant fact, an agent may carry out a prohibited action even though the user request is benign and every returned statement is true. We introduce \bench{}, an executable benchmark for evaluating unsafe execution, safety boundaries, and evidence recovery in LLM agents under missing evidence. It contains 300 matched unsafe/safe task pairs across six domains. By systematically suppressing critical facts, the benchmark measures unsafe execution under critical evidence omission and determines the minimum observed failure cardinality, including failures with full evidence and cases with no observed failure after exhaustive testing. An independent audit tool tests whether agents seek missing facts and then withhold prohibited actions while completing permissible tasks. The benchmark reveals substantial variation across the ten models in omission robustness, evidence acquisition, and appropriate action. Resistance to missing evidence does not necessarily translate into useful recovery. Recovery access reduces unsafe execution for all ten models, but agents differ in whether they actively obtain the missing facts and use them to act appropriately in both worlds.

### 2. Who Is Sycophantic to Whom? Confident LLMs, Human Deference, and the Collapse of Trust Calibration

- 作者：Deepthika S, Pawni Yadav, B. Sankar
- 领域：`cs.AI`（全部：cs.AI, cs.HC）
- 发布：2026-10-22 · 更新：2026-10-22
- 链接：https://arxiv.org/abs/2610.31579 · PDF：https://arxiv.org/pdf/2610.31579
- 备注：49 pages; 32 figures; 7 tables
- 入库：2026-10-23T20:37:10+08:00

> Research on sycophancy asks whether large language models (LLMs) bend towards what their users want to hear. We ask the reverse question: when an LLM is confident, consistent, and wrong, do users bend towards it? In a within-subjects experiment, 32 participants learned up to five science topics by chatting with five assistants built on the same model (GPT-5-mini). Unknown to participants, each assistant's briefing had 0, 25, 50, 75, or 100% of its facts replaced by plausible falsehoods, and every assistant spoke with full confidence. A surprise quiz after each topic offered the correct fact, the planted falsehood, and two distractors, with a confidence rating for every answer. Across 104 quizzes and 1,040 answers, scores fell from 7.4 to 2.9 out of 10, and the planted option was chosen on 60% of falsified items against 11% of correctly taught ones (odds ratio 12.5). Transcript coding showed that whenever the assistant stated a falsehood, it was adopted about 65% of the time at every falsification level. Absorbed falsehoods were held with high confidence (8.4/10), the modeled confidence advantage of right over wrong answers vanished, and the discrimination of confidence for correctness fell from an AUROC of 0.70 to chance, while post-task trust ratings barely moved. Participants tended to return to the chat more when the assistant was worse, but returning went with more absorption, not less, and 30% of all turns pasted quiz questions back to the source being checked. The assistant itself was almost never sycophantic and never conceded under pushback. We introduce a baseline-corrected Human Deference Index to quantify this human-side sycophancy and argue that trustworthiness is a property of the human-AI pair, that sycophancy evaluations should measure both directions, and that learning interfaces must make reliability legible claim by claim.

### 3. VERA: A Responsible AI Dashboard for Assessing LLM Deployments in Light of the EU AI Act

- 作者：Robin Quériaux, Solveig Bachellery, Léa Déléris, Saurabhsingh Rajput, Mariam Barry, Tushar Sharma, Jérôme Lebecq
- 领域：`cs.SE`（全部：cs.SE, cs.AI, cs.CY）
- 发布：2026-10-22 · 更新：2026-10-22
- 链接：https://arxiv.org/abs/2610.31588 · PDF：https://arxiv.org/pdf/2610.31588
- 备注：Accepted at the 33rd Asia-Pacific Software Engineering Conference (APSEC 2026), Software Engineering in Practice track, Bali, Indonesia, 7-10 December 2026. 11 pages, 3 figures
- 入库：2026-10-23T20:37:10+08:00

> Institutions that deploy large language models in regulated settings often need technical evidence of responsible AI practices before approving a deployment. COMPL-AI provides a technical interpretation of the EU AI Act that organises this evidence under six principle groups and eighteen technical requirements, twelve of which current benchmarks can measure. The benchmark suites that produce this evidence are typically operated from a command line, while the staff who approve deployments are non-engineers. We present VERA, an open-source self-hosted dashboard deployed to facilitate responsible AI processes within a large European bank. A reviewer selects a model and runs public benchmarks against it. VERA scores the twelve requirements that current benchmarks can measure and instruments the energy consumed by each evaluation, adding run-level evidence for environmental impact. We run four served open-weight models through the requirement pipeline, and the dashboard displays a score for each measurable requirement. A within-subject study then compares how participants read these benchmark results: from the raw output files in one condition, and through the VERA dashboard in the other. The dashboard reduced the time needed to perform the responsible AI assessment, reducing the time required from 56 seconds using raw files to 30 seconds using our dashboard, on average. Our dashboard scored highly (4.36 out of 5) on usefulness in the survey conducted within the organization. The dashboard and the study material are released publicly to promote replicability and reproducibility in different organisational contexts.
