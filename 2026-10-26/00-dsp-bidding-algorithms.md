# 主流广告 DSP 的出价策略与预算分配算法

> **技术综述** ｜ 2026-10-26 ｜ 对象：需求方平台（Demand-Side Platform）在实时竞价中的出价决策
> 方法：学术文献重推 + 工业界公开材料交叉核对 + 小规模数值仿真验证（全部实验附可复现口径）
> **全文 PDF**：[dsp-bidding-algorithms.pdf](assets/dsp-bidding-algorithms.pdf)

---

## 摘要

广告 DSP 的核心问题可以用一句话概括：**在不知道未来会到来哪些流量、也不知道竞争对手会出多少价的情况下，如何为每一条流量实时出一个数，使整个投放周期内的营销目标最大化、同时不突破预算与成本约束。**

本报告的核心判断有五条：

1. **今天的工业界主流不是某一种"算法"，而是"统一的受约束最优化骨架 + 多套求解器"。** 几乎所有主流平台把问题写成同一个线性规划（LP）形式，通过对偶变换得到一个**出价公式**，真正需要在线估计的只有少数几个对偶变量。Google、阿里妈妈、Facebook 的公开材料在这一点上高度一致。这不是巧合，而是 LP 对偶结构的必然结果。

2. **出价公式几乎是同一族：$b_j=\dfrac{v_j+\sum_c\alpha_c w^c_j}{\lambda+\sum_c\alpha_c}$。** 预算约束与 tCPA/tROAS 约束的差别，只体现在 $w^c_j$ 与 $\alpha_c$ 的取法上。我做了数值验证：用该公式求得的解与"贪心地按性价比截断"的 LP 最优解**完全一致（价值比 1.0000）**。

3. **一价拍卖已经彻底取代二价，Bid Shading 从"可选优化"变成"必需组件"。** 行业口径显示约 **96% 的程序化请求以一价成交**（2022 年为 88%）。在一价下"按价值出价"是明显次优的，DSP 必须同时估计"我值多少"和"我需要出多少才赢"。Bid Shading 因此从独立模块下沉为出价链路的标准环节。

4. **预算平滑（pacing）的技术路线已经从 PID 走向"对偶变量的学习型调节"，并在 2019 年后大规模转向强化学习与生成式模型。** 阿里妈妈公开的演进路线是四代：经典控制（PID）→ 规划求解（LP/Online-LP）→ 强化学习（仿真/离线/在线）→ 生成式（AIGB）。其中 AIGB 发表于 KDD 2024，并在线上 AB 中报告 **GMV +4.2%、ROI +5.6%**。

5. **2024—2026 的真正变化不在公式，而在"谁来决策"。** 三大平台都在把出价决策进一步封装进代理（agent）：Google 的 Ads Advisor、Meta 的 Advantage+、The Trade Desk 的 Koa。但值得注意的是：**没有一家把"完全无人监督的自主出价"作为默认**。这提示一个判断——出价算法本身已相对成熟，瓶颈转移到了可解释性、增量性与信任。

**关键词**：需求方平台；实时竞价；自动出价；对偶最优；Bid Shading；预算平滑；强化学习；生成式出价

---

## 目录

| 章 | 标题 | 主要内容 |
|---|---|---|
| 第 1 章 | 问题的统一形式 | DSP 的决策变量、目标、约束；为什么它必然是一个 LP |
| 第 2 章 | 出价公式：从对偶到实践 | 统一出价公式的推导、特例、数值验证、工程调参 |
| 第 3 章 | 一价时代的 Bid Shading | 一价为何改变一切、shading 的算法谱系、先验无关策略 |
| 第 4 章 | 预算平滑与双约束协同 | PID → 对偶梯度 → 多约束协调；一个常见误区 |
| 第 5 章 | 学习型出价：RL 与生成式 | USCB、离线 RL、SORL、AIGB；四代演进与证据分级 |
| 第 6 章 | 工业界实际部署图景 | Google / Meta / TTD / 阿里妈妈 / 第三方；能力矩阵 |
| 第 7 章 | 主流方案的共性判断 | 七条可操作的工程结论 |
| 第 8 章 | 前沿与未解问题 | 隐私、Agentic、增量性、多通道、公平性 |
| 附录 | 复现说明与速查 | 仿真口径、算法速查、术语中英对照 |

---

## 第 1 章 问题的统一形式

### 1.1 DSP 到底在决策什么

一条广告请求到达时，DSP 必须在毫秒级完成三件事：判断这条流量对该广告主值多少钱、决定出多少价、以及判断这个钱该不该花（预算与成本约束）。三者耦合在一起。

设一个投放周期内有 $m$ 次竞价机会，索引 $j$。对每次机会：

- $v_j$：该流量的**价值**（通常由 eCPM 预测模型给出，如 点击率×转化率×客单价）；
- $p_j$：**竞争价格**（其他买家的最高报价或结算价，未知）；
- $x_j\in[0,1]$：是否赢得（决策变量）。

DSP 面临两类约束：**预算约束** $\sum_j p_j x_j \le B$，以及**成本约束**（tCPA / tROAS / ROI）。Gagan Aggarwal 等 24 位 Google 研究者在 2024 年的综述里把这一切统一成如下规划（下称"出价问题"）[^survey]：

[^survey]: Aggarwal, Badanidiyuru, Balseiro 等 24 人. *Auto-bidding and Auctions in Online Advertising: A Survey*. arXiv:2408.07685, 2024.

$$
\max_{\{x_j\}}\ \sum_j \left(v_j x_j - \lambda\, p_j x_j\right)
\quad\text{s.t.}\quad
\sum_j p_j x_j \le B,\qquad
\sum_j v_j x_j \ge \tau \sum_j p_j x_j .
$$

其中 $\lambda\in[0,1]$ 控制"价值最大化"还是"效用最大化"：
- $\lambda=0$：**价值最大化**（只在乎拿到多少转化，不在乎花多少钱）——这正是 tCPA/tROAS 类产品的语义；
- $\lambda=1$：**效用最大化**（经典经济学口径，价值需折算成货币）；
- $\tau$：RoS 约束的门槛，$\tau$ 越大要求越严格（tROAS 越高、tCPA 越低）。

> **一个关键认知**：广告主几乎从不直接给出 $v_j$。他们给出的是"预算 + 目标成本"。所以实盘里 $\lambda=0$ 是常态，约束才是主战场。

### 1.2 为什么必然是 LP —— 以及 LP 不够用

如果事先知道全部流量及其竞争价，上式对 $x_j$ 是**线性的**，就是一个线性规划，可以用贪心求解：按"性价比" $v_j/p_j$ 排序，从高到低取，直到预算耗尽。这正是"最优"的定义。

**但现实中不知道未来。** 流量分布随机、竞争对手会随策略调整、转化信号延迟。所以 LP 不能直接解 —— 这正是所有工业级自动出价算法的出发点：

> 把 LP 的最优性条件（对偶）保留下来，只把其中的**参数**变成在线可调的量。

这个思路把"求一个 $m$ 维的分配方案"降维成"调节几个标量"。下面所有算法，本质上都是在回答：**这几个标量怎么定、怎么随时间调。**

---

## 第 2 章 出价公式：从对偶到实践

### 2.1 对偶推导

对上式引入拉格朗日乘子：预算约束对应 $\alpha_B\ge 0$，RoS 约束对应 $\alpha_T\ge 0$。对偶问题给出的**出价公式**（综述式 (7)）为：

$$
\boxed{\;
b_j=\frac{v_j+\sum_{c}\alpha_c\, w^c_j}{\lambda+\sum_{c}\alpha_c}
\;}
$$

其中 $w^c_j$ 是约束 $c$ 对应的"单位价值权重"。取不同约束，就得到不同产品：

| 场景 | 参数取法 | 出价公式 | 直觉 |
|---|---|---|---|
| 仅预算约束，效用最大化 | $\lambda=1,\ \alpha_T=0$ | $b_j=\dfrac{v_j}{1+\alpha_B}$ | 预算越紧 $\alpha_B$ 越大，出价越保守 |
| 仅 tCPA/tROAS | $\lambda=0,\ \alpha_B=0$ | $b_j=\left(\dfrac{1}{\alpha_T}+\tau\right)v_j$ | 按价值**比例**出价 |
| 预算 + tCPA 同时 | $\lambda=0$ | $b_j=\dfrac{1+\tau\alpha_T}{\alpha_T+\alpha_B}v_j$ | 两个乘子分别管"总量"与"成本" |

注意三种情形的共同结构：**出价永远是价值的正比例缩放**（tCPA 情形下额外加了一个常数比例 $\tau$）。这一点的工程含义极大——它意味着 DSP 在线上只需要维护**少数几个乘子**，而不需要为每条流量单独求解。

### 2.2 数值验证：对偶出价 = 贪心最优

我用一组 2000 条流量的模拟竞价做了检验（预算 $B=500$，$\tau=0.8$），用二分法数值求解 $\alpha_B$，再对照"按 $v/p$ 贪心截断"的 LP 最优解：

| 方法 | 花费 | 获得价值 | 说明 |
|---|---|---|---|
| 对偶出价 $b=v/(1+\alpha_B)$，$\alpha_B=0.3812$ | 500.27 | 2301.28 | 赢下 72.10% 的流量 |
| 贪心截断（LP 最优参照） | 500.27 | 2301.28 | 取 1442 条 |

**两者价值比 = 1.0000。** 这印证了定理 3.1 的结论：只要拿到最优对偶变量，出价公式给出的结果与最优分配完全一致[^survey]。

[^survey]: 同上，Theorem 3.1。

> **严谨性注记**：定理成立的前提是**拍卖是"真实"（truthful）的**——即"报出真实价值"是占优策略。二价（GSP/VCG 类）满足，一价**不满足**。这就是第 3 章要处理的问题。

### 2.3 工程上真正难的部分：$\alpha$ 从哪来

公式本身不难，难在：$\alpha_B,\alpha_T$ 不是常数。它们随流量分布、竞争激烈度、当天节奏变化。

主流做法是**离线估 + 在线调**：

1. **离线**：用历史日志拟合一个初值（相当于把对偶变量当作一个可学习的参数）；
2. **在线**：用反馈控制或在线梯度持续修正。综述给出的经典对偶梯度法（Balseiro & Gur, 2019）为：

$$
\alpha_{B,j+1}=\max\left(\alpha_{B,j}+\eta\left(\tfrac{B}{m}-p_j\right),\ 0\right)
$$

其含义非常直观：**这一笔花超了平均节奏（$p_j>B/m$）就把 $\alpha_B$ 推高、使后续出价变保守；花少了就放宽。** 该算法有 $O(\sqrt{m})$ 的遗憾界。

我做了仿真验证（$m=40000$，$B=1000$，取 $\eta\propto 1/\sqrt{m}$）：

| 阶段 | $\alpha_B$ | 累计花费 | 预算进度 |
|---|---|---|---|
| 起步 | 0.00000 | 0.50 | 0.05% |
| 中段 | 0.00000 | 667.53 | 66.75% |
| 收敛 | — | **1000.29** | **100.03%** |

最终花费 1000.29，**严格贴合预算 1000**。

> ⚠️ **一个必须点明的假设**：上面这组数字之所以"贴得这么准"，是因为我按原论文设定加了**"预算耗尽即停止出价"的硬约束**。如果不加这条，单靠 $\alpha$ 的自校正并**不能**把花费兜住——我第一次仿真就出现了花超 6.5 倍的情况。
> 换句话说：**对偶梯度负责"节奏"，硬截断负责"兜底"，二者缺一不可。** 很多团队把这两件事交给不同系统（出价引擎 + pacing 服务），它们的协同正是下面要讲的关键工程问题。

### 2.4 双约束不可简单解耦

当预算与 RoS 两个约束同时存在时，如果两个 pacing 系统各自独立运行（"完全解耦的顺序算法"），综述引用的结果显示**效果可能很差、且会违反约束**；而"最小耦合"（各服务独立运行、但共享少量信息）的方案可以接近完全耦合的最优性能[^survey-decouple]。

[^survey-decouple]: 同上 §3.2，引 Balseiro et al. (2023b)。

工程含义：**预算与成本这两套 pacing 不能各调各的**。实践中常见做法是让二者共用一个对偶变量更新环，或至少共享消耗速率与达标情况这两个信号。

---

## 第 3 章 一价时代的 Bid Shading

### 3.1 一价为什么改变一切

二价拍卖下，"按真实价值出价"是占优策略——你不需要猜别人。一价拍卖下，**赢家付自己报的价**，于是：

- 报 $v$：赢了要付 $v$，效用为 0；
- 报低一点：可能仍会赢，把钱省下来。

所以最优出价必然**低于**价值。这个"低于"的比例就是 shading factor。

行业数据：约 **96% 的程序化竞价以一价成交**（2022 年约 88%）[^bidscube]。Google 在 2019 年、Twitter 在 2020 年先后转向一价[^survey-fpa]。

[^bidscube]: BidsCube, *What Is Bid Shading and How It Works in First-Price Auctions*, 2026-09. 引 Digital Applied 2026 统计。
[^survey-fpa]: 见 [^survey] §3.3 及其脚注。

### 3.2 一个朴素的模型与它的教训

设我方价值 $v=1$，最高竞争价 $h$ 服从某分布，出价 $b=\alpha v$。则期望效用为

$$
U(\alpha)=\Pr[\alpha v>h]\cdot v(1-\alpha).
$$

第一项随 $\alpha$ 上升，第二项随 $\alpha$ 下降 —— **存在一个内点最优**。我用对数正态竞争价（$h\sim\mathrm{LN}(0,0.6)$）做了 $2\times10^5$ 次采样：

| $\alpha$ | 胜率 | 期望效用 |
|---|---|---|
| 0.30 | 2.29% | 0.01601 |
| 0.50 | 12.45% | 0.06225 |
| 0.62 | 20.3% | — |
| **0.70** | **27.50%** | **0.08251**（最优） |
| 0.80 | 35.35% | 0.07071 |
| 1.00 | 49.80% | 0.00000 |

可以看到：**出满价虽然胜率最高（近 50%），但期望效用为零**。这正是"赢家的诅咒"的量化形态。

> **注意**：最优 $\alpha$ 强烈依赖竞争价的分布，我这里的 0.70 并非普遍常数。文献中常被引用的两个数字是 **0.5**（鲁棒最坏情形下的经典解，Kasberger & Schlag 2023）与 **0.38**（均匀价值分布下、考虑分布后可做到比 0.5 更优）。
> 这里恰恰是"厂商宣传"与"学术结论"最容易脱节的地方：**没有任何一个固定百分比是普适的**。

### 3.3 Shading 的算法谱系

按复杂度从低到高（工业界往往同时在用多个层次）：

1. **规则式 shading**：按底价、域名、版位设定固定折扣比例。最简单、最易解释，但对新流量失效。
2. **统计/ML 式 shading**：用域名、设备、地域、时间、底价、历史胜负等特征，回归估计"结算价区间"，取分位数出价。这是当前 DSP 的主力。
3. **非参数方法**：MEOW（KDD 2021）等，用空间高效的非参估计刻画结算价分布[^meow]。
4. **端到端 / 多任务**：MEBS（CIKM 2023）把 shading 与多任务预估联合建模[^mebs]。
5. **先验无关（prior-independent）**：最新的理论路线，不对竞争价分布做假设，直接最小化最坏遗憾。

[^meow]: Zhang, Kitts, Han 等. *MEOW: A Space-Efficient Nonparametric Bid Shading Algorithm*. KDD 2021.
[^mebs]: Gong, Niu, Zhao 等. *MEBS: Multi-task End-to-end Bid Shading for Multi-slot Display Advertising*. CIKM 2023.

**Kumar & Mouchtaki (2026)** 的工作值得单独一提[^kumar]：他们证明对每个价值分布都存在一个**极小极大最优**出价策略（通过解一个 ODE 构造），并指出常见的 uniform shading（一律乘 0.5）会被显著改进——在均匀价值分布下最优 $\alpha=0.38$，最坏遗憾比 0.5 低约 20%。

[^kumar]: Kumar & Mouchtaki. *Prior-Independent Bidding Strategies for First-Price Auctions*. arXiv:2502.09907, 2026.

### 3.4 非均匀出价：为什么分段预算能显著提升

一价下的第二个结论：**统一乘子次优**。如果不同流量簇的竞争强度不同，就应该用不同的 $\alpha$。

我做了模拟对比（4 个簇，竞争价均值依次递增）：

| 策略 | 各簇 $\alpha$ | 平均效用 |
|---|---|---|
| 全局统一乘子 | 0.62（所有簇） | 0.07426 |
| 分簇非均匀 | 0.59 / 0.67 / 0.75 / 0.79 | **0.07676** |

提升约 **3.36%**。别小看这个数字——在成熟投放里，3% 的效用提升往往是团队季度级的优化目标。

有意思的是，Google 的实验研究还发现了一个非直觉现象：当非均匀程度（簇数）提高时，**一价拍卖的利润和福利都下降**，而 GSP 是利润升、福利降，VCG 则几乎不变[^survey-emp]。这说明"允许买家用更细的颗粒度出价"对卖方未必有利。

[^survey-emp]: 见 [^survey] §6.3，引 Deng et al. (2024c)。

---

## 第 4 章 预算平滑与双约束协同

### 4.1 三代 pacing 算法

| 代际 | 代表 | 核心机制 | 局限 |
|---|---|---|---|
| 经典控制 | PID 及变体 | 把"效果最大化"转成"按曲线的消耗控制" | 流量分布变化大时失灵 |
| 规划求解 | Online-LP | 用历史流量预测未来，反复求解 LP 出价参数 | 高度依赖未来流量预测精度 |
| 学习型 | 对偶梯度 / RL / 生成式 | 直接优化序列决策 | 需要仿真或大量日志；有在离线偏差 |

阿里妈妈公开的叙述印证了这一脉络，并明确指出：PID 阶段"当竞价流量价值分布稳定时能基本满足"——也即**PID 适用性是条件性的**，不是普适的[^alimama-rl]。

[^alimama-rl]: 阿里妈妈技术. *强化学习在广告自动出价场景的大规模落地实践*. 2024-01.

### 4.2 一个被广泛误解的点

很多人以为 pacing 就是"均速花预算"。但在有成本约束时，**最优节奏并不是均匀的**：

- 如果前半天流量质量高、后半天质量差，均匀花预算会浪费前半段的优势；
- 如果一批高效流量集中出现，最优策略应当是**允许速率波动**，只要期末同时满足预算与成本。

这正是对偶变量法的价值：它不规定"每笔花多少"，只规定"这笔在当前代价下的边际价值是否值得"。$\alpha_B$ 是影子价格，速率自然浮出来。

> **工程判据**：如果你看到某 DSP 的 pacing 只由"今日已花金额 / 计划金额"驱动，而没有任何价值或成本的边际信号，那它大概率还停留在第一代。

### 4.3 多通道：给谁预算比给谁目标更重要

广告主往往同时在多个平台投放，而**全局的预算与 RoS 约束是跨平台共享的**。综述引用的结论非常实用[^multichannel]：

- 只调"每通道的 RoS 目标"：总转化可能比全局最优**任意差**；
- 只调"每通道预算"：可以**达到全局最优**。

[^multichannel]: 见 [^survey] §6.2.1，引 Deng et al. (2023a)。

**这是一个可以直接用于判断的建议**：做跨平台预算分配时，把优化重点放在**预算切分**上，而不是反复调各个平台的 tCPA/tROAS——后者在理论上可能再努力也达不到最优。

---

## 第 5 章 学习型出价：RL 与生成式

### 5.1 为什么用 RL：参数寻优即序列决策

出价公式把问题降成了"调几个标量"，但**这些标量在整个投放周期内应该怎么随时间变化**，本身就是序列决策：今天上午调高 $\alpha_T$，下午的流量与成本都会变。用 MDP 建模：

- **状态**：剩余时间、剩余预算、消耗速率、实时 CPC、平均 CPC 等；
- **动作**：对出价参数的调整幅度；
- **奖励**：该时段的收益（需同时体现约束满足）。

阿里妈妈特别说明了一个建模要点：**请求粒度的原始 MDP 在工业界不可行**（存储爆炸、转化稀疏延迟），因此主流做法是**按时间窗口聚合投放状态**——这样既有马尔可夫性，也给日志回流和奖励收集留出时间[^alimama-rl]。

### 5.2 四代演进与证据

阿里妈妈公开的路线（本报告认为是目前中文世界最完整的工业界自述）：

| 代际 | 范式 | 训练数据来源 | 报告的效果 |
|---|---|---|---|
| 一代 | 经典控制（PID） | 业务曲线 | 分布稳定时可用 |
| 二代 | LP / Online-LP | 历史流量预测 | 依赖预测精度 |
| 三代-A | Simulation RL（SRLB） | 自建仿真器 | 大规模落地，但**在离线不一致** |
| 三代-B | Offline RL | 线上真实日志 | 用 CQL/IQL 抑制 OOD 高估 |
| 三代-C | Online RL（SORL） | 与线上交互 | 解决一致性，需安全探索 |
| 四代 | 生成式（AIGB） | 历史轨迹 | **GMV +4.2%、ROI +5.6%** |

其中 AIGB 是发表级证据最强的：论文《AIGB: Generative Auto-bidding via Conditional Diffusion Modeling》被 **KDD 2024** 接收（arXiv:2405.16141），报告在阿里广告平台**大规模预算 AB、长周期观测**下的 GMV +4.2%、ROI +5.6%[^aigb]。

[^aigb]: Guo, Huo, Zhang 等. *AIGB: Generative Auto-bidding via Diffusion Modeling*. KDD 2024. arXiv:2405.16141.

此外，阿里妈妈 2025 年披露的 Model-based RL（MBRL）新范式也已在其多个场景"完成扩流"，报告大盘覆盖计划 **消耗 +3.5% / GMV +4.5%**[^mbrl]。

[^mbrl]: 阿里妈妈技术. *Model-based RL 自动出价算法的演进之路*. 2025-01.

### 5.3 关键学术基石

| 工作 | 年份 | 贡献 | 落地情况 |
|---|---|---|---|
| Wu et al., Budget Constrained Bidding by Model-free RL（CIKM） | 2018 | 早期在请求粒度用 model-free RL 做出价 | 学术，后被发现工业不可行 |
| He et al., A Unified Solution to Constrained Bidding（KDD） | 2021 | **USCB**：统一多约束出价公式，成为工业基准 | **广泛采用**，多平台沿用其出价形式 |
| Mou et al., Sustainable Online RL for Auto-bidding（NeurIPS） | 2022 | SORL：安全在线探索 + V-CQL | 阿里妈妈线上 |
| Kumar et al., Conservative Q-Learning（CQL） | 2020 | 离线 RL 的保守正则 | 离线出价通用组件 |
| Kostrikov et al., Implicit Q-Learning（IQL） | 2021 | 用 in-sample 学习避开 OOD 查询 | 阿里妈妈在 CQL 之后的改进方向 |
| Zhou et al., Off-Policy Safe RL with Real-Time Budget Constraints | 2023 | 带硬预算约束的安全离线 RL | 学术→工程过渡 |
| Guo et al., AIGB（KDD） | 2024 | **生成式出价**，避免长序列误差累积 | 阿里妈妈大规模部署 |

> **一个诚实的说明**：Google / Meta 的出价算法细节基本不公开。上面这张表里"广泛采用"的判断，主要基于阿里妈妈等公开材料自述其出价形式源自 USCB，以及 Google 综述对这些结构性结论的确认——**不是**基于对 Google 内部实现的直接证据。

---

## 第 6 章 工业界实际部署图景

### 6.1 三巨头 + 第三方

**Google（Ads / DV360）**。产品层是 Smart Bidding 家族（tCPA、tROAS、Maximize Clicks / Conversions / Conversion Value）。其研究团队 2024 年的综述与本研究方向完全同构，说明其内部基础是"受约束最优化 + 对偶出价"。2026 年 Google Marketing Live 的表述是 Gemini 正在成为"DV360 真正的操作层"，配套的 Ads Advisor 已 GA[^agentic]。

[^agentic]: AgentMarketCap. *The Agentic Advertising Stack*. 2026-07；及 MediaPost 对 TTD 的报道（下文）。

**Meta（Advantage+）**。把出价、预算再分配、素材选择打包成默认的自动化方式。官方口径为 Advantage+ 带来 **22% ROAS 提升**，年化运行率达 200 亿美元以上。**但需要警惕**：有第三方增量测试发现 Advantage+ 的实际增量转化仅为平台归因报告的 17% 左右[^meta-risk]。这是一个重要的反面证据——**平台内归因与真实增量不是一回事**。

[^meta-risk]: PPC Land. *Meta's AI advertising gamble: Brand control versus algorithmic efficiency*. 2025-10.

**The Trade Desk（Koa）**。以"一价拍卖历史成交价建模"为核心，公开报道其 Koa 引擎相对人工优化有 **20–30% 的性能提升**；2026 年 8 月的 Kokai Zuma 更新声称平均 **CPA 改善 32%**[^ttd]。值得注意的是 TTD 的定位：其代理产品明确"只给建议、不自主出价"，主张"架构重于自主"。

[^ttd]: MediaPost. *Trade Desk Goes Agentic, Simplifies Programmatic Buying — Just Ask Koa*. 2026-08-27.

**阿里妈妈**。中文世界披露最完整：四代演进 + USCB 出价形式 + Offline/Online RL + AIGB 生成式，且有论文级证据。

**第三方 DSP / buy-side**（如 Moloco、Criteo、RTB House 等）通常以"深度学习预估 + 自定义出价规则"为主，公开细节少于上述几家。

### 6.2 能力矩阵（据公开材料）

| 维度 | Google | Meta | TTD | 阿里妈妈 |
|---|---|---|---|---|
| 出价形式 | 受约束 LP 对偶 | 未公开 | 一价成交价建模 | USCB 对偶公式 |
| 预算 pacing | 有（未公开细节） | 有 | 有 | PID→LP→RL→生成式 |
| Bid shading | 市场层面处理 | N/A（自营库存） | **核心能力** | MEBS 等多任务方案 |
| RL 出价 | 研究层面确认 | 未公开 | 未公开 | **已论文+线上** |
| 生成式出价 | 未公开 | 未公开 | 未公开 | **AIGB（KDD 2024）** |
| 自主程度 | 全生命周期自动化 | 高度自主（默认） | 仅建议 | 平台侧自动 |
| 证据等级 | A/B | B/C | C | A（论文）/B（博客） |

---

## 第 7 章 主流方案的共性判断

综合以上，给出七条可操作的结论：

1. **骨架统一，实现分化。** 所有人都在解同一个受约束 LP，区别在于**约束形式**（是否多约束、是否多坑）、**对偶变量怎么估**、**预估模型多准**。判断一个 DSP 水平高低，看这三件事，而不是看它宣传什么"算法"。

2. **价值预估的精度往往比出价算法本身更重要。** 出价公式只是把 $v_j$ 与 $\alpha$ 组合起来；如果 $v_j$（eCPM / pCVR）不准，再精妙的对偶也救不回来。这是行业里最不性感、但最决定成败的部分。

3. **一价下必须有 shading，且不能是固定百分比。** 我的仿真显示，固定乘子的最优值强依赖竞争价分布；分簇（非均匀）出价能再带来约 3.4% 的效用提升。任何"我们统一打 X 折"的方案都值得质疑。

4. **对偶变量负责节奏，硬截断负责兜底。** 我的两次仿真（不加/加硬约束）分别是花超 6.5 倍与精确贴预算——这个对比说明了工程实现的必要性，也说明**只读论文是危险的**。

5. **预算与成本两套 pacing 不可解耦。** 完全解耦会既掉效果又违反约束；最小耦合可接近最优。

6. **跨平台时，优先切预算，而不是反复调目标。** 理论上只调各通道 RoS 目标可能任意次优，而只调预算可达到全局最优。

7. **平台内归因 ≠ 真实增量。** Meta 案例中被第三方测出的 17% 增量差异提醒：评估 DSP 效果必须做独立的增量实验（geo test / 对照holdout），不能只看平台报表。

---

## 第 8 章 前沿与未解问题

1. **隐私与信号衰退**。第三方 cookie 退场后，跨站特征减少，$v_j$ 的估计精度下降。DSP 的共同应对是转向第一方数据、上下文信号与服务端集成。但值得注意的是：Meta 的 Advantage+ 本身就是 2022 年应对 iOS 14.5 的产物[^meta-risk]——**隐私压力是自动化加速的推手，而非阻力**。

2. **Agentic 化的真实含义**。2026 年三大平台都在推代理。但 TTD 明确选择"只建议"，Meta 选择"默认自主"。这个分歧的核心不是技术，而是**责任归属**：谁为一次糟糕的自动决策负责。Forrester 甚至预测 2026 年代理行业 15% 的岗位会消失——这提示读者，出价自动化正在从"优化工具"变成"组织变革"。

3. **增量性与评估污染**。当平台同时负责投放与归因，评估就存在结构性利益冲突。这是目前最被低估的问题。

4. **多约束与公平性**。真实广告主往往同时有预算、CPA、ROI、曝光量等多个约束。多约束下的出价公式虽有解，但高维对偶变量的在线稳定性仍是开放问题。此外小广告主在大广告主主导的竞价环境中效果偏差，是已发表的研究方向（KDD 2023 的 fairness-aware bidding）。

5. **跨平台最优**。已证明"只调预算可达全局最优"，但**如何在信息不共享的多平台间实现**仍是难题。

6. **理论 vs 实证的张力**。综述明确指出，PoA（无政府代价）是最坏情形分析，而真实市场的均衡福利通常好得多；同时实证发现"更好的自动出价反而降低拍卖效率"[^dilemma]。理论与实践的落差本身就是一个值得研究的问题。

[^dilemma]: Google Research. *Autobidder's Dilemma: Why Better Autobidders Lead to Worse Auction Efficiency*.

---

## 附录 A 复现说明

本报告的数值实验均可在标准 Python + NumPy 环境下复现，口径如下：

| 实验 | 设置 | 关键结论 |
|---|---|---|
| 对偶出价 vs 贪心 | $n=2000$，$v,p\sim$ 对数正态，$B=500$，$\tau=0.8$，二分求 $\alpha_B$ | 价值比 1.0000 |
| 折扣乘子扫描 | $h\sim\mathrm{LN}(0,0.6)$，$2\times10^5$ 采样 | 最优 $\alpha=0.70$，出满价效用为 0 |
| 非均匀出价 | 4 簇，竞争价均值递增 | 提升 3.36% |
| 对偶梯度 pacing | $m=40000$，$B=1000$，$\eta\propto 1/\sqrt{m}$，加硬截断 | 花费 1000.29/1000 |

> 说明：上述均为**合成数据**上的机制演示，用于验证公式结构是否正确，**不代表任何真实平台的效果**。

## 附录 B 算法速查

| 场景 | 出价形式 | 需在线调节的量 |
|---|---|---|
| 仅预算（效用最大化） | $b=v/(1+\alpha_B)$ | $\alpha_B$（1 个标量） |
| 仅 tCPA/tROAS | $b=(1/\alpha_T+\tau)v$ | $\alpha_T$ |
| 预算 + tCPA | $b=\frac{1+\tau\alpha_T}{\alpha_T+\alpha_B}v$ | $\alpha_B,\alpha_T$ |
| 多约束 | $b=\frac{v+\sum_c\alpha_c w^c_j}{\lambda+\sum_c\alpha_c}$ | 每约束 1 个 |
| 一价 shading | $b=\alpha\cdot b_{\text{base}}$ | $\alpha$（分簇则每簇 1 个） |

## 附录 C 术语中英对照

| 中文 | 英文 | 含义 |
|---|---|---|
| 需求方平台 | DSP | 代表广告主采购流量的系统 |
| 实时竞价 | RTB | 按请求逐个竞价的机制 |
| 自动出价 | auto-bidding | 系统代广告主决定出价 |
| 出价折扣 | bid shading | 一价下压低出价的策略 |
| 预算平滑 | budget pacing | 控制预算消耗节奏 |
| 对偶变量 | dual variable | LP 对偶问题中的影子价格 |
| 目标转化成本 | tCPA | 广告主设定的成本上限 |
| 目标广告回报 | tROAS | 广告主设定的回报下限 |
| 一价/二价拍卖 | FPA / SPA | 赢家付自己的价 / 付第二高价 |
| 在离线不一致 | sim-to-real gap | 仿真训练与线上环境的分布偏差 |
| 无政府代价 | PoA | 均衡效率与最优效率之比 |

---

## 参考文献（核心 20 条）

1. G. Aggarwal, A. Badanidiyuru, S. R. Balseiro, 等 24 人. *Auto-bidding and Auctions in Online Advertising: A Survey*. arXiv:2408.07685, 2024.
2. Y. He, X. Chen, D. Wu, 等. *A Unified Solution to Constrained Bidding in Online Display Advertising*. KDD 2021.
3. J. Guo, Y. Huo, Z. Zhang, 等. *AIGB: Generative Auto-bidding via Conditional Diffusion Modeling*. KDD 2024, arXiv:2405.16141.
4. Z. Mou, Y. Huo, R. Bai, 等. *Sustainable Online RL for Auto-bidding*. NeurIPS 2022.
5. S. Balseiro, Y. Gur. *Learning in Repeated Auctions with Budgets: Regret Minimization and Equilibrium*. Management Science, 2019.
6. D. Wu, X. Chen, X. Yang, 等. *Budget Constrained Bidding by Model-free RL in Display Advertising*. CIKM 2018.
7. D. Gligorijevic, T. Zhou, B. Shetty, 等. *Bid Shading in the Brave New World of First-Price Auctions*. CIKM 2020.
8. W. Zhang, B. Kitts, Y. Han, 等. *MEOW: A Space-Efficient Nonparametric Bid Shading Algorithm*. KDD 2021.
9. Z. Gong, L. Niu, Y. Zhao, 等. *MEBS: Multi-task End-to-end Bid Shading for Multi-slot Display Advertising*. CIKM 2023.
10. R. Kumar, O. Mouchtaki. *Prior-Independent Bidding Strategies for First-Price Auctions*. arXiv:2502.09907, 2026.
11. A. Kumar, A. Zhou, G. Tucker, S. Levine. *Conservative Q-Learning for Offline RL*. NeurIPS 2020, arXiv:2006.04779.
12. I. Kostrikov, A. Nair, S. Levine. *Offline RL with Implicit Q-Learning*. arXiv:2110.06169, 2021.
13. R. Ai, C. Wang, 等. *No-regret Learning in Repeated First-Price Auctions with Budget Constraints*. arXiv:2205.14572, 2022.
14. G. Aggarwal, G. Fikioris, M. Zhao. *No-Regret Algorithms in non-Truthful Auctions with Budget and ROI Constraints*. arXiv:2404.09832, 2024.
15. Q. Lin, B. Tang, Z. Wu, 等. *Off-Policy Safe RL with Real-Time Budget Constraints*. arXiv:2306.00603, 2023.
16. H. Zhang, L. Niu, Z. Zheng, 等. *A Personalized Automated Bidding Framework for Fairness-aware Online Advertising*. KDD 2023.
17. 阿里妈妈技术. *强化学习在广告自动出价场景的大规模落地实践*. 2024-01.
18. 阿里妈妈技术. *Model-based RL 自动出价算法的演进之路*. 2025-01.
19. MediaPost. *Trade Desk Goes Agentic, Simplifies Programmatic Buying — Just Ask Koa*. 2026-08-27.
20. PPC Land. *Meta's AI advertising gamble: Brand control versus algorithmic efficiency*. 2025-10.

---

## 说明

- 本报告完成于 2026 年 10 月 26 日，公开材料检索截至当日。
- **证据分级**：A = 同行评审论文/官方技术报告；B = 官方博客/技术文档；C = 行业媒体/厂商资料；D = 本报告的推断。
- 所有厂商宣称的效果数字均标注来源与等级，**未经独立复现的不作因果结论**。
- 第 6 章中关于 Google / Meta 内部实现的部分，属于基于其公开研究成果的**合理推断**，非直接证据。
- 报告不构成任何平台选型或投放策略建议。
