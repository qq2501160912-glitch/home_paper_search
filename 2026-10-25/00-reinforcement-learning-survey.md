# 强化学习：从试错学习到推理智能

> **专题研究综述** ｜ 2026-10-25 ｜ 全文 116 页 ｜ 79 条参考文献  
> **全文 PDF**：[reinforcement-learning-survey.pdf](assets/reinforcement-learning-survey.pdf)

---

## 摘要

强化学习（reinforcement learning, RL）研究的是：一个处于未知环境中的决策者，如何仅凭交互所得的经验信号，逐步改进行为，使长期累积回报最大化。它既是最优控制与动态规划在统计学习条件下的延续，也是心理学中“试错—强化”思想的可计算化，更是当代大语言模型推理能力与智能体行为的核心训练范式。

本报告以“问题—数学—算法—应用—边界”为主线，给出了一份兼顾历史纵深、推导严谨性与工程证据的强化学习全景研究。全文的五个核心判断是：

1. **诞生是三条思想源流的交汇**：Bellman 的动态规划提供了“延迟回报的递归数学”，Thorndike 的效果律与多巴胺奖励预测误差提供了“行为由后果塑造”的生物学原型，Samuel 与 Minsky 的早期程序提供了“机器可以通过经验改善行为”的工程信念。MDP 把三者压缩为一个可分析的对象。
2. **算法史是五次范式转移**：表格型 TD/Q-learning → 函数逼近与策略梯度 → 深度 RL → 模型基/离线/RLHF → 偏好与可验证奖励。每一次转移都保留了 Bellman/策略梯度的骨架，只替换“表示、数据、更新、目标”中的一个组件。
3. **数学主线可以被完整串起**：贝尔曼算子的压缩性 → 值迭代收敛 → 策略梯度定理 → 信任域下界 → KL 正则 RLHF → DPO 闭式消元 → GRPO 组内优势。全文对这些结论给出了从假设到结论的推导，而不是罗列公式。
4. **应用效果必须分层评估**：在规则完备、仿真廉价、奖励可验证的领域（围棋、Atari、芯片布局、矩阵乘法、数据中心冷却、托卡马克控制），RL 已产生可复核的超人类或数量级效果；在奖励延迟、反事实不可观测的领域（推荐、金融、医疗），RL 更多以离线、约束、人机协同的方式产生增量价值。
5. **当前瓶颈是基础设施，不是公式**：可交互环境、可验证奖励、可信评估，将决定下一波突破的速度与方向。奖励劫持、分布偏移、样本效率、长程信用分配与评估污染，是 2026 年最需要正视的问题。

**关键词**：强化学习；马尔可夫决策过程；贝尔曼方程；策略梯度；深度强化学习；RLHF；RLVR；大语言模型；智能体

---

## 目录

| 章 | 标题 | 主要内容 |
|---|---|---|
| 第 1 章 | 强化学习诞生的背景 | 最优控制、心理学、早期 AI 三条源流；为什么是 MDP |
| 第 2 章 | 数学基础 | MDP、贝尔曼方程、压缩映射、策略迭代/值迭代、死亡三角、POMDP |
| 第 3 章 | 发展历程 | 五次范式转移、关键算法、里程碑年表、算法进步的五个机制 |
| 第 4 章 | 值函数方法 | TD(0)、TD(λ)、SARSA、Q-learning、Double Q、DQN、分布型 RL |
| 第 5 章 | 策略优化方法 | 策略梯度定理、REINFORCE、GAE、TRPO、PPO、DPG/DDPG、SAC、TD3 |
| 第 6 章 | 模型基、搜索与离线 RL | Dyna、Dreamer、MuZero、UCT、AlphaZero、BCQ/CQL/IQL、Decision Transformer |
| 第 7 章 | LLM 时代的强化学习 | RLHF、Bradley–Terry、PPO-RLHF、DPO、GRPO、RLVR、DeepSeek-R1、Agentic RL |
| 第 8 章 | 应用版图与效果评估 | 游戏、机器人、LLM、推荐、芯片/系统、能源/交通/医疗/科学、工业/金融 |
| 第 9 章 | 挑战与未来方向 | 样本效率、奖励劫持、分布偏移、长程信用分配、安全、评估危机、RL Scaling |
| 附录 A/B | 符号表 / 算法速查 | 常用恒等式、算法更新式、复现清单、术语中英对照 |

---

## 一条数学主线

### 1. 贝尔曼期望方程

对策略 $\pi$，值函数满足

$$
V^{\pi}(s)=\sum_{a\in\mathcal{A}}\pi(a\mid s)\left[r(s,a)+\gamma\sum_{s'\in\mathcal{S}}P(s'\mid s,a)V^{\pi}(s')\right].
$$

贝尔曼算子 $\mathcal{T}^{\pi}$ 在无穷范数下是 $\gamma$-压缩映射：

$$
\|\mathcal{T}^{\pi}V_1-\mathcal{T}^{\pi}V_2\|_{\infty}\le\gamma\|V_1-V_2\|_{\infty}.
$$

由 Banach 不动点定理，$V^{\pi}$ 唯一，值迭代以 $\gamma^k$ 几何收敛。最优算子 $\mathcal{T}^{*}$ 把期望换成逐状态最大化，得到

$$
V^{*}(s)=\max_{a\in\mathcal{A}}\left[r(s,a)+\gamma\sum_{s'\in\mathcal{S}}P(s'\mid s,a)V^{*}(s')\right].
$$

### 2. 策略梯度定理

令 $J(\theta)=\mathbb{E}_{\tau\sim p_\theta}\left[\sum_{t=0}^{\infty}\gamma^{t}R_{t+1}\right]$，则

$$
\nabla_{\theta}J(\theta)
=\mathbb{E}_{\tau\sim p_{\theta}}\left[\sum_{t=0}^{\infty}\gamma^{t}\,\nabla_{\theta}\log\pi_{\theta}(A_t\mid S_t)\,G_t\right].
$$

证明只依赖两个事实：轨迹似然比 $\nabla_{\theta}p_{\theta}(\tau)=p_{\theta}(\tau)\sum_t\nabla_{\theta}\log\pi_{\theta}(A_t\mid S_t)$，以及得分函数的条件期望为零。它不要求环境可微，这是 RL 能用于黑箱系统的根本原因。

### 3. KL 正则 RLHF 与 DPO

RLHF 的目标是

$$
\max_{\theta}\ \mathbb{E}_{x,y\sim\pi_{\theta}}\left[r_{\phi}(x,y)\right]
-\beta\,\mathbb{E}_{x}\left[D_{\mathrm{KL}}\left(\pi_{\theta}(\cdot\mid x)\,\|\,\pi_{\mathrm{ref}}(\cdot\mid x)\right)\right].
$$

其闭式最优策略为

$$
\pi^{*}(y\mid x)=\frac{1}{Z(x)}\,\pi_{\mathrm{ref}}(y\mid x)\exp\left(\frac{r(x,y)}{\beta}\right),
$$

反解奖励得 $r(x,y)=\beta\log\frac{\pi^{*}(y\mid x)}{\pi_{\mathrm{ref}}(y\mid x)}+\beta\log Z(x)$。把它代入 Bradley–Terry 偏好模型，配分函数 $Z(x)$ 消掉，得到 DPO 损失：

$$
\mathcal{L}_{\mathrm{DPO}}(\theta)
=-\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\left[
\log\sigma\left(
\beta\log\frac{\pi_{\theta}(y_w\mid x)}{\pi_{\mathrm{ref}}(y_w\mid x)}
-\beta\log\frac{\pi_{\theta}(y_l\mid x)}{\pi_{\mathrm{ref}}(y_l\mid x)}
\right)
\right].
$$

DPO 的梯度为

$$
\nabla_{\theta}\mathcal{L}_{\mathrm{DPO}}
=-\beta\,\sigma(-u)\left(\nabla_{\theta}\log\pi_{\theta}(y_w\mid x)-\nabla_{\theta}\log\pi_{\theta}(y_l\mid x)\right),
$$

其中 $u$ 是括号内的隐式奖励差。它提高获胜回答的似然、降低失败回答的似然，权重随“已经分对的程度”自适应衰减。

### 4. GRPO 的组内优势

GRPO 对同一问题采样 $G$ 个回答，用组内相对奖励替代 critic：

$$
\hat{A}_{i}=\frac{r_i-\operatorname{mean}(r_1,\dots,r_G)}{\operatorname{std}(r_1,\dots,r_G)}.
$$

目标函数为

$$
\mathcal{J}_{\mathrm{GRPO}}(\theta)
=\mathbb{E}_{q,\{o_i\}\sim\pi_{\theta_{\mathrm{old}}}}\left[
\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_i|}\sum_{t=1}^{|o_i|}
\min\left(\rho_{i,t}\hat{A}_i,\ \operatorname{clip}\left(\rho_{i,t},1-\epsilon,1+\epsilon\right)\hat{A}_i\right)
-\beta D_{\mathrm{KL}}\left(\pi_{\theta}\,\|\,\pi_{\mathrm{ref}}\right)
\right].
$$

它把“价值网络”换成了“同一问题下多个回答的相对好坏”，显存开销约为 PPO-RLHF 的一半，适合数学、代码、STEM 等可验证任务。

---

## 发展时间线（节选）

| 年份 | 节点 | 关键创新 | 局限/后续 |
|---|---|---|---|
| 1957 | 动态规划 / MDP | 最优性原理、Bellman 方程、值迭代/策略迭代 | 需要已知模型 |
| 1959 | Samuel 跳棋 | 自我对弈、线性评估、rote learning | 依赖人工特征 |
| 1988 | TD(0) | 用自举目标在线估计值函数 | 仅策略评估 |
| 1989 | Q-learning | 离策略、直接逼近最优动作价值 | 最大化偏差；函数逼近下发散 |
| 1992 | REINFORCE | 似然比策略梯度，无需环境模型 | 方差极大 |
| 1992/1995 | TD-Gammon | 非线性函数逼近 + 自博弈 + TD(λ) | 难以推广到围棋 |
| 2013/2015 | DQN | 经验回放、目标网络、端到端像素输入 | 样本效率低 |
| 2015 | TRPO / GAE | KL 信赖域、指数加权优势 | 实现复杂 |
| 2016 | AlphaGo | 策略/价值网络 + MCTS + 自我对弈 | 依赖人类棋谱 |
| 2017 | PPO / AlphaZero | 裁剪目标；无人类数据的自我对弈 | 非单调保证；算力昂贵 |
| 2017 | RLHF（Christiano） | 人类偏好训练奖励模型 | 奖励劫持 |
| 2018 | SAC / TD3 | 最大熵、双 critic、延迟更新 | 以连续控制为主 |
| 2019/2020 | BCQ / CQL / IQL | 离线 RL 的保守正则与 OOD 抑制 | 数据覆盖敏感 |
| 2020 | MuZero | 学习隐式模型 + 树搜索 | 模型偏差 |
| 2022 | InstructGPT / ChatGPT | RLHF 规模化；1.3B 优于 175B GPT-3 | 偏好昂贵；对齐税 |
| 2023 | DPO | 闭式消去奖励模型 | 离线数据；缺少探索 |
| 2024 | GRPO / o1 | 组内相对优势；长思维链 + RL | 信用分配粗；推理成本高 |
| 2025 | DeepSeek-R1 | 纯 RL 激励推理，RLVR 范式 | 开放任务泛化有限 |
| 2025/2026 | Agentic RL | POMDP、工具调用、长程信用分配 | 环境/奖励基础设施不成熟 |

---

## 应用效果（节选）

| 领域 | 代表工作 | 报告效果 | 证据 |
|---|---|---|---|
| 围棋 | AlphaGo / AlphaZero | 4:1 击败李世石；超人类 | A |
| 星际争霸 II | AlphaStar | Grandmaster，前 99.8% | A |
| Dota 2 | OpenAI Five | 2:0 击败世界冠军 OG | B |
| 赛车 | Gran Turismo Sophy | 击败顶级车手并创赛道纪录 | A |
| 矩阵乘法 | AlphaTensor | $4\times4$ 模 2：47 次（此前 49） | A |
| 排序 | AlphaDev | 短序列最高快 70%，长序列约 1.7% | A |
| 芯片布局 | AlphaChip | 用于三代 TPU | A/B |
| 数据中心冷却 | DeepMind / Google | 冷却能耗约 −40%，PUE 约 −15% | B |
| 视频流 | Pensieve | QoE +12% 至 +25% | A |
| 机器人 | ANYmal / Rudin et al. | 复杂地形鲁棒行走；分钟级训练 | A |
| LLM 对齐 | InstructGPT | 1.3B 模型在人类偏好上优于 175B GPT-3 | A |
| LLM 推理 | DeepSeek-R1 | AIME 2024 79.8%，MATH-500 97.3% | A |
| LLM 推理 | o3 | ARC-AGI 87.5%（高算力预算） | B |
| 推荐 | SlateQ / Page-wise / Top-K | CTR/留存离线或小流量提升 | A/B |
| 核聚变 | DeepMind / EPFL | 托卡马克等离子体多构型稳定控制 | A |
| 医疗 | AI Clinician | 离线估计生存率提升（非临床验证） | A（离线） |
| 数学 | AlphaProof / AlphaGeometry 2 | IMO 28/42，银牌水平 | A |
| 数学 | Gemini Deep Think | IMO 35/42，金牌水平 | B |

> **证据分级**：A = 同行评审论文/官方技术报告，可复核；B = 权威机构博客/官方文档，数据具体但缺独立复现；C = 产业案例/媒体报道，方向可信、效应量需谨慎；D = 本报告的推断与评论。

**效应量的四个陷阱**：选择偏差、基线选择、评估污染、成本外溢。一个“提升 2%”的结论，若不报告算力、样本量与推理成本，就无法判断是否值得部署。

---

## 为什么这份报告强调“推导”

强化学习的算法很容易被记成“损失函数 + 调参技巧”，但真正决定一个方法能否成立的，是三个数学事实：

1. **贝尔曼算子的压缩性**：它保证值函数唯一、值迭代几何收敛；一旦函数逼近破坏压缩性，算法就可能发散（死亡三角）。
2. **策略梯度的似然比结构**：它把“对轨迹分布求导”化为“对动作对数概率求导”，使黑箱环境下的优化成为可能；基线、优势、GAE 都是围绕方差削减展开的。
3. **KL 正则的闭式解**：它把“奖励—策略对数比”绑定在一起，使 DPO 可以消去奖励模型；同样的结构也解释了 RLHF 中 KL 惩罚的作用。

报告对上述结论给出了完整的证明或证明思路，包括：Banach 不动点定理、策略改进定理、值迭代近似界、策略梯度定理、性能差引理、TRPO 下界、PPO 裁剪梯度、DPG 定理、SAC 软策略迭代、DPO 闭式推导、GRPO 组内优势性质。所有公式均按标准数学排版，下标、上标、期望与算子均保持语义一致。

---

## 如何阅读全文

- **只想看结论**：读摘要、第 8 章应用表、第 9 章“三个核心判断”。
- **想补数学**：第 2 章（MDP/贝尔曼/压缩映射）→ 第 5 章（策略梯度/TRPO/PPO/SAC）→ 第 7 章（RLHF/DPO/GRPO）。
- **想做工程**：第 3 章时间线 → 第 4/5 章算法推导 → 第 6 章模型基/离线 → 第 8 章场景与证据分级 → 附录 B 复现清单。
- **想追前沿**：第 7 章 RLVR/Agentic RL → 第 9 章 RL Scaling/评估危机。

**全文 PDF**：[reinforcement-learning-survey.pdf](assets/reinforcement-learning-survey.pdf)

---

## 参考文献（节选）

1. R. Bellman. *A Markovian Decision Process*. Journal of Mathematics and Mechanics, 1957.
2. R. S. Sutton, A. G. Barto. *Reinforcement Learning: An Introduction*. 2nd ed. MIT Press, 2018.
3. C. J. C. H. Watkins, P. Dayan. *Q-learning*. Machine Learning, 1992.
4. V. Mnih, et al. *Human-level control through deep reinforcement learning*. Nature, 2015.
5. D. Silver, et al. *Mastering the game of Go with deep neural networks and tree search*. Nature, 2016.
6. J. Schulman, et al. *Proximal Policy Optimization Algorithms*. arXiv:1707.06347, 2017.
7. L. Ouyang, et al. *Training language models to follow instructions with human feedback*. NeurIPS, 2022.
8. R. Rafailov, et al. *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. NeurIPS, 2023.
9. DeepSeek-AI. *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning*. arXiv:2501.12948, 2025; Nature 645, 633–638, 2025.
10. G. Zhang, et al. *The Landscape of Agentic Reinforcement Learning for LLMs: A Survey*. arXiv:2509.02547, 2025.

完整 79 条参考文献、脚注与实验口径见 PDF 末章。

---

## 说明

- 本报告完成于 2026 年 10 月，文献检索截止于 2026 年 10 月中旬。
- 产业数据均标注原始口径与证据等级；未独立复现的效应量不作因果结论。
- 报告为研究综述，不构成医疗、金融、工业控制等高风险场景的部署建议。
- 反馈与勘误：欢迎在仓库 Issue 中提出。
