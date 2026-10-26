# 实时竞价（RTB）买入侧全链路技术综述：从流量、预估到出价与度量

> **技术综述（v1）** ｜ 2026-10-26 ｜ 对象：广告主侧的实时竞价系统（RTB / DSP / 智能出价产品）
> 定位：承接同日《主流广告 DSP 的出价策略与预算分配算法》（下称 **DSP-2026-10-26**）的**出价与预算**部分，本篇改为**买方便（广告主 / 代理商 / 自建 DSP）的全链路视角**：流量与竞价机制 → 投放决策 → 预估 → 出价（shading / pacing）→ 度量 → 隐私 → 组织。
> 方法：arXiv 文献检索与逐篇核对（真摘录，来自本地论文库）＋ 工业界公开材料（厂商文档、行业报道）＋ 四组小规模确定性仿真。所有效果数字均标注**证据等级**：**A** 同行评审/官方技术报告；**B** 官方文档/工程博客；**C** 行业媒体/二手统计；**D** 本报告推断。

---

## 摘要

RTB 的"算法"不是一个算法，而是一条**分阶段、毫秒级、强约束**的决策管线。本报告的五条判断是：

1. **工业界的真实分层不是"谁用了更好的算法"，而是"谁的每一层误差更小"。** 一条请求要走：竞价与曝光资格 → 相关性/召回 → pCTR/pCVR 预估 → 出价（含一价二价适配）→ pacing 与预算 → 归因与增量。任何一层的偏差都会向下游放大，而且**大多数工业差距来自预估与流量，而非出价公式**。
2. **一价拍卖占绝对多数，bid shading 是必需组件——但工业界的"shading 已足够"是一个未经证实的假设。** Zeithammer & Alcobendas（2026）用 Yahoo Ad Exchange 超 **4000 万次**拍卖、**8 家**主要 DSP 的数据，用非参数方法证明 2019 年二价转一价后**至少三个月内普遍 shade 不足**（等级 A）。这与"用一点统计模型估清算价就行"的工程直觉直接冲突。
3. **产业主流正在从"两阶段（先估竞价位次分布、再解工程优化）"转向"端到端 / 生成式 shading"，并已在大流量 DSP 落地。** 美团 GBS（SIGIR 2026，日均数十亿竞价请求处理）用自回归生成 shading ratio + GRPO 偏好对齐，明确指出两阶段方法受**单峰假设、级联误差、样本选择偏差**三重约束（等级 A/B，效果为厂商自述）。
4. **智能出价的产品空间只有两个维度，全行业一致：约束类型（预算 / 成本 / RoI / 组合 / 无约束）与自动化程度（给参数 / 给素材 / 给只读建议 / 全自动托管）。** 从 Google Smart Bidding、TTD Koa、到腾讯广告 AIM+ nobid（未处置出价、只给预算，无强成本约束、不支持自动赔付，等级 B），都能放进这个二维表。**"nobid"这种产品在算法上恰好就是"约束型出价的对偶变量为 0"的极端，这是本报告给出的一个可操作性判断工具。**
5. **度量是买入侧回报最高、却最被低估的一环。** 归因 ≠ 增量：TikTok 的大规模归因校正工作指出自有渠道会系统性地吞掉付费归因（等级 A，ADKDD 2026）；而隐私化上报（匹配率损失、聚合阈值抑制、加噪）会让许多 A/B 实验**在信息论意义上无解**（等级 A，2026 年两篇论文给出的"认证 / 拒绝 / 未决"三值决策框架）。**做投放决策前先问"这个实验有没有能力分辨"，比反复调出价参数更值钱。**

---

## 目录

| 章 | 标题 | 主要问题 |
|---|---|---|
| 第 1 章 | RTB 决策管线五层 | 买方系统到底由哪些可替换模块组成，各自出错会怎样 |
| 第 2 章 | 流量与竞价机制 | 一价/二价、header bidding、PMP/curation、赢率与清洗 |
| 第 3 章 | 投放决策层：买哪些流量 | 召回、定向、相关性、频控、反作弊 |
| 第 4 章 | 预估层（I）：精度 | CTR/CVR 的模型谱系、特征、增量学习与特征陈旧 |
| 第 5 章 | 预估层（II）：标定 | 为什么 AUC 好不等于出价对；延迟反馈与净值 |
| 第 6 章 | 出价层：算法谱系与本报告的仿真 | shading、pacing、约束出价的算法地图 |
| 第 7 章 | 生成式 / LLM 出价 | 扩散、GRPO、流匹配、LLM-as-bidder 的实际位置与边界 |
| 第 8 章 | 预算与跨渠道 | 为什么"先分配预算、再出价"是工程上更稳的分解 |
| 第 9 章 | 度量与增量 | 归因、geo 实验、隐私噪声下的可识别性 |
| 第 10 章 | 工业产品图 | 平台与产品的二维矩阵，可查的功能对照 |
| 第 11 章 | 隐私与信号 | 三方 Cookie 退场后，买方还剩什么特征 |
| 第 12 章 | 前沿与未解问题 | 竞争学习、机制操纵、agentic、评估污染 |
| 附录 | 复现与速查 | 仿真口径、算法速查、术语中英 |

---

## 第 0 章 与上一篇的关系：哪些不重复，哪些修补

DSP-2026-10-26 已经把"受约束 LP + 对偶出价公式 $b_j=\frac{v_j+\sum_c\alpha_c w^c_j}{\lambda+\sum_c\alpha_c}$ ＜预算/成本约束＞、对偶梯度 pacing、AIGB、多通道预算优先"讲清楚。本篇**不重复推导**，只做三件事：

1. **补齐买方链路中权重更大的部分**：第 3–5 章（投放决策与预估）、第 9 章（度量）。上一版把"$v_j$ 准不准"归为一句"预估精度最重要"；本篇把它作为独立的两章展开。
2. **更新算法地图**：上一版写于当天较早版本，未覆盖 2025–2026 的若干关键工作（Zeithammer 的 shade 充足性检验、美团 GBS、ABPlanner/Nash 约束出价、LLM 出价 LBM/SAGE、中试级别的 MPC 框架、隐私下的增量测量）。本篇逐条核对 arXiv 元数据与摘要后纳入。
3. **把上一篇的一个"推断"做成仿真**：上一版指出"对偶变量管节奏、硬截断兜底"，本篇给出可复现的数值证据（第 6 章 6.4），并刻意保留一个**不利结果**（第 8 章的贪心分配反例），以免读者把它当成"算法万能论"。

> **阅读建议**：只想落地的人读第 1、6、8、9、10 章与附录；想判断供应商水平的人读第 1、2、6、10 章；做研究的人读第 4、5、7、12 章。

---

## 第 1 章 RTB 决策管线五层

### 1.1 一条请求的旅程（买方视角）

```
POST /bid  (含 site/app、设备、用户标识、底价 floor、允许的字段)
   │  ← 时限常在 100–300 ms（服务端约 110 ms，客户端约 220 ms 为行业口径，等级 C）
   ├─(1) 流量与资格：竞价类型识别、品牌安全、PMP deal 优先、Cookie/同意状态
   ├─(2) 投放决策：相关性/召回、受众匹配、频控(impression-level)、反作弊预过滤
   ├─(3) 预估：pCTR、pCVR、客单价、可见性、延迟转化；多任务共享底层
   ├─(4) 出价：价值 v 的形成 → 约束乘子(α) → shading → bid 与 floor 比对
   └─(5) 结算与回流：win-loss、min_bid_to_win(一价反馈)、归因、回流模型、增量实验
```

### 1.2 每层的"工业故障模式"

| 层 | 典型故障 | 后果 | 隐蔽性 |
|---|---|---|---|
| 流量与资格 | 把二价清算规则套到一价竞价上；把 PMP 与 open 混在一个 bid 里 | 溢价购买 / 超支 | 低（可对账） |
| 投放决策 | 频控在 imp 级而非 user 级；跨设备人数膨胀 | 重复触达、频次不达标 | 中 |
| 预估 | 特征陈旧、训练/上线分布漂移、标签延迟 | 出价系统性偏高或偏低 | **高** |
| 出价 | 用固定折扣率 shading；对偶乘子与硬截断不协同 | 要么超支、要么撞预算 | 中 |
| 结算与回流 | 只看平台报表；不做 holdout | 把"本来就会转化的人"买下来 | **很高** |

> **最容易被忽略的一条**：第 4 层的错误会在第 5 章被"自有渠道归因"掩盖——你花得越多，归因报表越好看，而真实增量可能没动。这是买方视角下最贵的 bug。

### 1.3 三个层面的"算法"要分开讲

工程上常见把三件事混为一谈，这是评估供应商时最常见的沟通障碍：

1. **决策算法**：出多少价（第 6、7 章）。
2. **预估算法**：值多少钱（第 4、5 章）。
3. **控制算法**：预算与节奏（第 6.5、8 章）。

**结论**：只有 2 的精度比较时，1 的"高级"才有意义；只有 3 覆盖全周期时，1 才有意义（详见第 6.4 的仿真）。

---

## 第 2 章 流量与竞价机制

### 2.1 一价成为主流：机制变化意味着算法变化

一价拍卖（FPA）下赢家付自己的报价，因此"按价值出价"是**次优**的，必须下压到某个 shading ratio。行业汇总口径为**约 96% 的程序化竞价以一价成交**（2022 年约 88%）——该数字来自 2026 年的行业数据汇总，**等级 C**，宜作量级参考。

机制层面：Google AdX 于 2019 年转向一价，Yahoo Ad Exchange 于 2019 年初转向一价并提前公告，这是文献中研究最充分的两次迁移（等级 A，见 [Zeithammer & Alcobendas 2026](https://www.anderson.ucla.edu/sites/default/files/document/2026-06/slim%20shading%20in%20ad%20auctions%20June%202026.pdf) 的机制描述）。

> **对买方的含义**：过去十年"DSP 算法"最大的变化不是模型，而是**机制**。任何仍在按二价逻辑"按真实价值报满"的配置，等于把价值全部让渡给卖方。

### 2.2 一价下的信息回流

Google Authorized Buyers 文档提供 `min_bid_to_win` 字段，即"可赢得该次合格拍卖的最低金额"，用于一价反馈（等级 B，经二手文章转述）。工业界 shading 的信号来源大体一致：

- 底价 floor（每个请求都有）
- 历史 win-loss 与成交价反馈
- 上下文特征：域名/应用、版位、设备、地域、时段、（隐私允许时的）用户标识

> **一个常被高估的假设**：有了 `min_bid_to_win` 就等于知道竞争价。实际上它只在**你参与过的**拍卖上可用，且一价机制本身让"输掉"的价格不可见——这正是第 6 章仿真要量化的样本选择问题。

### 2.3 header bidding 与供给侧的结构性变化

2026 年行业口径：**87%** 的程序化发布商使用 header bidding，平均 wrapper 接入 **14 个** SSP（2024 年为 11 个），服务端 header bidding（Prebid Server 等）承担 **58%** 的竞价（等级 C）。对买方的直接影响：

1. **同一印次被多次竞价**：同一曝光在不同 SSP 路径上重复拍卖，导致"重复出价"与预算被多个 path 吃掉。
2. **floor 抬高**：wrapper 竞争让发布商 floor 平均提升约 21%（等级 C）。
3. **延迟预算更紧**：客户端 220 ms / 服务端 110 ms 的中位超时（等级 C），意味着**预估模型必须在 50–100 ms 内完成**，这直接决定了模型规模的上限（第 4 章）。

### 2.4 PMP / curated marketplace 的抬头

同一份 2026 汇总：open exchange 占程序化花费约 59%（2024 年 71%），PMP 约 28%，程序化保量 PG 约 13%；curated marketplace（Magnite ClearLine、PubMatic Activate、Microsoft Curate 等）同比增长约 41%（等级 C）。微软官方文档说明 curation 是在卖方最终拍卖中竞价，但**只有赢得印次时才计费**（[Microsoft Learn](https://learn.microsoft.com/en-us/xandr/monetize/curated-deals)）。

> **工程含义**：买方算法必须**同时**处理"open 竞价（要猜价）"和"deal 竞价（常带保底价或固定价）"，且要在同一个预算与 pacing 之下统一核算。把 deal 与 open 分成两套 pacing，就是 DSP-2026-10-26 第 2.4 节所说的"双约束完全解耦"——会同时掉效果和违反约束。

### 2.5 赢率与可买性

等级 C 的行业口径：open exchange 的 DSP 侧平均赢率 **6.3%**，PMP **14.7%**，PG **81%**。这组数字对做 pacing 的人很重要：**赢率极低时，"以赢率乘以出价"估计期望花费会系统性偏乐观**，因为赢率本身随出价变化（弹性估计问题），而不能当常数乘。

---

## 第 3 章 投放决策层：买哪些流量

### 3.1 相关性/召回的谱系

RTB 中"买哪些流量"通常在三处被决定：请求过滤（资格）、受众命中（名单）、以及**出价阈值的隐含过滤**（买不起的不出价）。

| 方法 | 代表 | 工业现状 | 主要风险 |
|---|---|---|---|
| 规则与名单 | 受众包、域名白/黑名单、地区/时段 | 所有 DSP 的基线 | 维护成本、覆盖收缩 |
| 召回模型（双塔/ANN） | 广告-用户向量检索 | 信息流与推荐型竞价（非开放 RTB）的主流 | 与出价脱耦时召回与最优不一致 |
| 出价感知的召回 | 把出价/预算信号纳入召回 | 近期研究（如 Bidding-Aware Retrieval，arXiv:2508.05206，**未核对**） | 训练标签偏差 |
| 平台托管 | Advantage+、AIM+、Performance Max | 巨头默认 | 黑箱、增量不可验证 |

> **买方判断**：当平台把"投放决策"也托管后，买方能控制的只剩**预算、素材、目标**三件事。这不是技术退化，而是**控制权换效果**的交易；签这个交易前必须先有一套自己的增量度量（第 9 章）。

### 3.2 频控的粒度

业界口径显示 CTV PMP 的家庭频次上限约为每广告每周 4 次（等级 C）。技术要点只有一条：**频控必须作用在用户/家庭实体上，而不是曝光上**。跨设备身份（UID2/RampID 等，CTV 匹配率约 71%，仅 IP 匹配约 52%，等级 C）决定了频控能落实多准。

### 3.3 反作弊与品牌安全

等级 C 口径：程序化整体 SIVT 约 8.7%，CTV 最高约 12.4%。买方工程上可行的三件事：

1. 在**出价前**做预过滤（pre-bid），行业估计可拦截约 73% 的无效流量（等级 C）。
2. 把品牌安全与可见性作为**出价的乘子**而非事后报表（即把可见性概率并入 $v_j$）。
3. 对 supply path 做去重与优先级（sellers.json / SupplyChain Object 清理后，平均路径数由 6.2 降到 4.1，等级 C）。

---

## 第 4 章 预估层（I）：精度

> 本章的论文摘要均为本地论文库真摘录（`home_paper_search/2026-10-26/*.md`）。

### 4.1 模型谱系（按工业采纳度）

```
LR / FTRL            → 稀疏特征、可解释、极低延迟（仍广泛用于探索流量与小 DSP）
FM / FFM / DeepFM    → 特征交叉；DSP 私有特征的常用主力
DIN / DIEN 类序列模型 → 用户历史行为序列；信息流与推荐型竞价
多任务（MMoE/PLE）    → 同时估 CTR / CVR / 深度转化
生成式 / 一模型范式  → 把预估与排序统一为生成任务（见 4.4）
LLM 增强            → 语义特征 + ID 特征的融合（见 4.3）
```

### 4.2 语义与协同的融合：ClickPrompt（WWW 2024）

> **真摘录**：传统 CTR 模型把多字段类别数据 one-hot 成 ID 特征，提取协同信号，"suffers from the problem of semantic information loss"；而用预训练语言模型（PLM）做 hard prompt 保留语义，却"fail to capture the collaborative information ... not to mention the unacceptable inference overhead brought by the huge model size"。ClickPrompt 让 CTR 模型生成 interaction-aware soft prompts 喂给 PLM，并设计 prompt-augmented MLM 预训练；推理时"either tune the CTR model with PLM ... or solely tune the CTR model without PLM for inference efficiency"。
> （[arXiv:2310.09234](https://arxiv.org/abs/2310.09234)，WWW 2024，等级 A）

**工业含义**：LLM 在广告预估里的合理位置不是"把 LLM 放进毫秒级打分"，而是**训练期用它注入语义，推理期退回小模型**。这与第 2.3 节的延迟硬约束完全一致。

### 4.3 LLM 带来的数据效率（Bench-CTR，2025）

> **真摘录**：作者构建了统一的 CTR 基准平台（Bench-CTR）与评测协议，比较从传统多元统计到现代 LLM 方法的广泛模型。三条发现：(1) 高阶模型在多数情况下优于低阶，但优势随指标与数据集而变；(2) **"LLM-based models demonstrate a remarkable data efficiency"——用约 2% 的训练数据就能达到其他模型的可比性能**；(3) CTR 模型性能在 2015→2016 显著提升后进入缓慢进展期，且在不同数据集上一致。代码开源。
> （[arXiv:2512.01179](https://arxiv.org/abs/2512.01179)，Electronic Commerce Research（forthcoming），等级 A）

> **一个必须点明的反差**：这个基准的结论是"CTR 模型的**架构**进展已经放缓"，而"**LLM 的样本效率**是新亮点"。对买方而言，这意味着：预算有限、需要快速冷启动的品类（新广告主、新账户），应优先考虑 LLM/预训练增强；而成熟账户的边际收益更多来自特征与标签工程，而不是换模型结构。

### 4.4 增量学习与特征陈旧（FeSAIL，2025）

> **真摘录**：CTR 模型常以增量数据 + 部分历史数据做增量更新，但"the feature embeddings of a CTR prediction model often get stale when the corresponding features do not appear in current incremental data"，下一周期模型在含陈旧特征的样本上性能退化（feature staleness problem）。FeSAIL 用 staleness-aware sampling（SAS）以高效率采样固定数量的陈旧样本重放，并以 staleness-aware regularization（SAR）细粒度控制 embedding 更新。
> （[arXiv:2505.02844](https://arxiv.org/abs/2505.02844)，等级 A）

**工业含义**：这是**买方自建模型**最常见的线上退化原因之一，且是"越省算力越严重"的问题——增量窗口越短，陈旧特征越多。RTB 场景的"长尾特征"（小众域名、低价位、冷门设备型号）失效尤其快，而恰恰是 shading 最缺样本的地方。

---

## 第 5 章 预估层（II）：标定

### 5.1 为什么 AUC 好不等于出价对

出价是**绝对量**：$b_j \approx$ 价值。价值 = pCTR × pCVR × 客单价（或直接回归 eCPM）。如果模型只是**排序**好而**标定**偏（系统性高估/低估），出价会整体偏高或偏低，pacing 控制器会花掉错误的预算。

**本报告的仿真 C**（`assets/rtb_sim.py`，$n=4\times10^5$，种子固定）给出一个反直觉但重要的事实：在固定**投放量**（win 数固定）的前提下，模型被**等比例放大 $k$ 倍**时，选中的流量完全相同、真实转化数完全相同，但**成交单价变成 $k$ 倍**——即"纯缩放误差"直接变成"多付 $k$ 倍的钱"。

| 模型 | AUC | ECE | 平均 pCVR | 真实 pCVR | 缩放比 | 成交单价（自定单位） |
|---|---|---|---|---|---|---|
| 生产（排序正确、尺度偏低约 5 倍） | 0.9246 | 0.0130 | 0.00303 | 0.01572 | 0.193 | 0.062 |
| 同排序、尺度 ×2 | 0.9246 | 0.0117 | 0.00605 | 0.01572 | 0.385 | 0.125 |
| 同排序、尺度 ×0.5 | 0.9246 | 0.0142 | 0.00151 | 0.01572 | 0.096 | 0.031 |

> **读法**：三行 AUC 完全一样（0.9246），选中的流量一样、转化一样，但**出价与单价**差 2–4 倍。AUC 是"排序指标"，出价却由"绝对标定"决定。**工业上应把 pCVR 的 ECE / 平均偏差当作一等公民指标**，并给 pacing 控制器加一个"自动校正整体尺度"的慢环（本质是把尺度的估计权交给控制环，而不是交给离线训练）。

> **注意**：本仿真没有建模"标定误差改变流量选择"这条更复杂的路径（那要引入约束下的非线性）。所以表里的"转化数相同"是刻意构造的对照，不是一般结论——真实系统里标定偏差也会改变买量结构。

### 5.2 延迟反馈与事后偏差

转化（下单、到货、退款）晚于点击数天到数周。CVR 建模的工业难点是**标签延迟 + 事后偏差**。

> **真摘录（ESVI / EVI，2024）**：点击后转化率（CVR）估计的长期挑战是样本选择偏差（SSB，只看到点击样本）与数据稀疏（DS）。已有整个空间（entire-space）方法用未点击样本的知识蒸馏缓解二者，但他们"fail to consider the unbiasedness and information limitations of these pseudo labels"；EVI 先用条件整个空间的 CVR teacher 生成无偏伪标签，再用变分信息利用与 logit 蒸馏迁移未点击空间信息，六个数据集上相对 SOTA 平均提升 **2.25%**。
> （[arXiv:2502.15687](https://arxiv.org/abs/2502.15687)，等级 A）

> **真摘录（级联延迟反馈 / TESLA，WWW 2026）**：CVR 忽略退款，因此提出净转化率 NetCVR（"clicked item is purchased and not refunded"）。从点击到转化的延迟与从转化到退款的延迟**方向相反**，使传统 CVR 方法不适用。作者发布首个基于淘宝的大规模在线开放数据集 **CASCADE**，并给出三条洞察：(1) NetCVR 具有强时序动态，必须在线持续建模；(2) **CVR 与退款率级联建模优于直接建模 NetCVR**；(3) 延迟时间同时与 CVR 和退款率相关，是重要特征。系统 **TESLA** 在 NetCVR 上 RI-AUC 提升 **12.41%**、RI-PRAUC 提升 **14.94%**（绝对）。数据与代码开源（`github.com/alimama-tech/NetCVR`）。
> （[arXiv:2601.19965](https://arxiv.org/abs/2601.19965)，WWW 2026，等级 A）

**买方含义**：如果你是电商/本地生活类广告主，**退款率必须进入价值函数**，否则会把"买了又退"的人当成好流量持续加价。这条比任何 shading 技巧都值钱。

### 5.3 预估——出价一体化的最佳证据

> **真摘录（MEBS，2024）**：多坑位展示广告（列表里多个广告整体展示）有不同性价比，广告主有动力调整出价以赢下"最划算的坑位"。MEBS 用**多任务端到端**方式把 bid shading 引入多坑位场景，理论上证明最优性；线上实验 GMV **+7.01%**、ROI **+7.42%**、广告购买数 **+3.26%**（效果为厂商自述，等级 A 论文 / B 线上证据）。
> （[arXiv:2403.02607](https://arxiv.org/abs/2403.02607)）

> **真摘录（GR4AD，快手，2026）**：大规模广告的实时生成式推荐需要超出"LLM 式训推配方"的设计。GR4AD 在**架构、学习、服务**上联合设计：UA-SID（统一广告语义 ID）承载业务信息；**LazyAR**（惰性自回归解码器）放宽层间依赖，服务短序列多候选生成以降低推理成本；VSL（价值感知监督学习）与 **RSPO**（排序引导的列表级 softmax 偏好优化）对齐商业价值；在线推理用动态 beam serving 按负载调节。大规模线上 A/B：相对既有 DLRM 栈**广告收入提升至多 4.2%**，且"model scaling 与 inference-time scaling 均带来一致收益"；已在快手广告系统全量部署，覆盖 **4 亿+ 用户**，实时高吞吐。
> （[arXiv:2602.22732](https://arxiv.org/abs/2602.22732)，等级 A/B）

> **真摘录（GPR，腾讯视频号广告，2025）**：现有多阶段广告推荐"objective misalignment and error propagation"，难以全局最优；统一生成式模型又难以满足工业落地。GPR 是"首个把广告推荐重构为端到端生成任务的一模型框架"，用统一输入模式与多级语义 ID 空间、异构分层解码器（HHD）分离用户意图与广告生成，多阶段联合训练（多 token 预测 + 价值感知微调 + HEPO）；已在**微信视频号广告系统全量部署**，GMV 与 CTCVR 显著提升。
> （[arXiv:2511.10138](https://arxiv.org/abs/2511.10138)，等级 A/B）

**共同点**：三家头部平台（阿里妈妈 MEBS、快手 GR4AD、腾讯 GPR）都在做同一件事——**把"预估"和"出价/价值对齐"放进同一个优化目标**，而不是先预估再出价。这是第 7 章"生成式出价"之外的第三条主线，值得买方自研团队重视。

---

## 第 6 章 出价层：算法谱系与仿真

> 公式推导、对偶出价、pacing 的四代演进见 DSP-2026-10-26 第 2–5 章。本章只写**新增的、且面向买方决策的**部分。

### 6.1 算法地图（买方视角，按"你缺什么"组织）

| 你的短板 | 应选的算法族 | 代表工作 | 证据 |
|---|---|---|---|
| 不知道竞争对手出多少 | bid shading / 竞价位次分布建模 | MEOW(KDD 2021)、MEBS(CKDD 2023)、DR-Shading(2024)、GBS(SIGIR 2026) | A |
| 预算/成本约束管不住 | 对偶出价 + pacing | USCB(KDD 2021)、Balseiro-Gur、pacing 综述(2023) | A |
| 转化稀疏、冷启动 | 分层规划 + 预算规划器 | ABPlanner(KDD 2025) | A |
| 多广告主互相踩踏 | 均衡约束出价 | NCB(2025/2026) | A |
| 品牌类、反馈快 | MPC + 单调回归 | 轻量 MPC 框架(2026) | A(仅仿真) |
| 需要"长期回报"而非单期最优 | 离线 RL / 生成式 | SORL(NeurIPS 2022)、AIGB(KDD 2024)、LBM(2026) | A/B |

### 6.2 一价 shading：从"两阶段"到"端到端"再到"稳健"

**(a) 两阶段（估竞价位次分布 → 工程优化）**：工业界长期主力，但 GBS 指出其三重病：单峰假设、级联误差、样本选择偏差。

> **真摘录（GBS，美团，SIGIR 2026）**：现有主流两阶段方法"first model bid landscapes and then optimize surplus using operations research techniques"受单峰假设约束，对非凸 surplus 曲线不适用，且"vulnerable to cascading errors"；连续值的离散化模型忽略区间依赖，削弱纠错能力；竞价场景还存在样本选择偏差。GBS = **自回归生成 shading ratio（逐步残差）** + **奖励偏好对齐**（通道感知分层奖励模型 CHNet + surplus 优化 + 探索效用对齐，用 **GRPO** 优化短期与长期 surplus）。离线与在线 A/B 验证，已部署在**美团 DSP，日均服务数十亿竞价请求**。
> （[arXiv:2508.06550](https://arxiv.org/abs/2508.06550)，等级 A/B）

**(b) 分布稳健（对价值与竞争价**同时**不确定）**：

> **真摘录（DR-Shading，Yahoo DSP，2024）**："bid shading has become a standard practice"，且"most auctions ... are now of first price type"；shading 需要同时估计**机会价值**与**竞争者最高报价的分布**，而"these two estimates tend to be very noisy in practice"。作者给出 max-min 形式：对价值与竞争价**各自**在一个 KL 模糊集内选择分布，两个模糊集"essential to adjusting the shape of the bid-shading policy"；在 Yahoo DSP 真实数据上"systematically outperforms its non-robust counterpart"。
> （[arXiv:2410.14864](https://arxiv.org/abs/2410.14864)，等级 A）

**(c) 在线学习型（凸优化 + Wasserstein 近端）**：

> **真摘录（2025）**：把 shading 策略写成**测度值优化**问题——在 shading 参数的联合分布上做凸优化，每次拍卖后用带正则的 Wasserstein 近端更新该分布，能量泛函以域名/版位/设备/地域等**上下文**为条件；"encourages the bid distribution to place more weight on values with higher expected surplus"（赢率与价值差同时大）。该测度值凸问题**有闭式解**。数值示例演示。
> （[arXiv:2509.10693](https://arxiv.org/abs/2509.10693)，等级 A，但仅数值示例、无线上）

**(d) 经验检验（最值得买方警惕的一篇）**：

> **真摘录（Slim Shading，UCLA × Yahoo Research，2026-06）**：研究真实交易所从二价转一价后买方的调整。为判断"观察到的降幅是否在给定竞争下已经足够"，作者提出一个**非参数**估计器——估计每次观察出价背后的价值**下界**；该估计器只依赖**局部竞争度量**，不要求买家对称、估值独立或均衡出价。应用于 Yahoo Ad Exchange **超 4000 万次拍卖、8 家主要 DSP**，发现转换后"pervasive insufficient bid shading"：价值下界在转换后**至少 3 个月**仍显著高于转换前，即所研究的买方**没有一家**shade 充分；结论对替代的竞争定义、更丰富的条件信息与估计器假设"robust"。作者指出：**即使精于算法的买家，对重大机制变化的调整也可能出奇地慢**，这对市场设计与"短期 A/B 实验"的解释都有含义。
> （[Zeithammer & Alcobendas](https://www.anderson.ucla.edu/sites/default/files/document/2026-06/slim%20shading%20in%20ad%20auctions%20June%202026.pdf)，等级 A）

> **这是本报告最应该被买方产品经理读到的一段**。它说明：(1) "我们用了 ML shading"≠"shade 充分"；(2) 机制变更后需要用**独立检验**（价值下界、赢率-出价弹性、min_bid_to_win 校准）来验证，而不是用"看起来更省"；(3) A/B 实验窗口太短会**系统性低估**调整所需时间。

### 6.3 本报告的仿真 A：shading 的收益来自哪里

设置：$n=2\times10^6$，真实价值 $v\sim\mathrm{LN}(0,0.5)$，真实最高竞争价 $h\sim\mathrm{LN}(-0.3,0.6)$；买方的两个估计带对数正态噪声（$\sigma_v=0.25$、$\sigma_h=0.45$）；采用 $H\sim U[0,v]$ 下的最优线性策略 $b=0.5v+0.5\hat h$（"bayes"），与"直接按估计价值出价"（"truthful"）对照。效用按**真实价值**结算。

| 价值估计 | 竞价环境估计 | 策略 | 赢率 | 真实效用 | 平均成交价 | **每次获胜的平均多付** |
|---|---|---|---|---|---|---|
| 有噪 | 有噪 | bayes | 68.00% | 0.3901 | 0.4795 | 0.4349 |
| 有噪 | 真值 | bayes | 64.25% | 0.4306 | 0.4173 | 0.3774 |
| 精确 | 有噪 | bayes | 68.46% | 0.3994 | 0.4786 | 0.4031 |
| 精确 | 真值 | bayes | 64.93% | **0.4439** | 0.4160 | **0.3418** |
| 有噪 | — | truthful | 64.25% | 0.4306 | 0.4173 | 0.7548 |
| 精确 | — | truthful | 64.93% | 0.4439 | 0.4160 | 0.6836 |

**三条结论**：

1. **shading 的"省钱"体现在多付（overpay）上，而不是效用上。** 在与模型匹配的均匀竞争假设下，"按估计价值出价"恰好就是最优（$H\sim U[0,v]$ 时 $b^*=v/2+E[H]/2=v$，因为 $E[H]=v/2$）。所以在这个模型里 bayes 与 truthful 的真实效用**完全相同**，区别全在多付：**0.68 → 0.34**，即每次获胜平均少付约 50%（相对 truthful）。
2. **在这个模型里，"shading 用的策略"与"不 shading"的真实效用完全相同**（0.4439 = 0.4439）；两者**唯一**的差别就是多付。原因是 $H\sim U[0,v]$ 时 $E[H]=v/2$，代入 $b=0.5v+0.5E[H]$ 恰好得 $b=v$。**换言之：在竞争强度恰好"匹配"价值时，按价值出满就是最优；shading 的价值只在竞争强度与价值不匹配时才显现。** 买方必须能判断自己在哪个情形里，而这需要**竞争价估计的精度**。
3. **估计噪声把定价推向"多付更多"**：有噪环境下的多付（0.48）显著高于真值环境（0.416），说明**竞争价的估计误差直接变现为溢价**。这与 Zeithammer 的"shade 不足"经验发现是一致的机制解释。

> **口径说明**：本仿真是**机制演示**，竞争价分布固定、无对手反应、无预算约束，不代表任何真实平台效果。它说明的是"shading 的价值 = 减少多付 + 依赖竞争估计精度"，而不是给出一个可以照抄的数。

### 6.4 本报告的仿真 B：对偶变量管节奏，硬截断兜底

设置：$m=40\,000$ 次机会、预算 $B=1000$、一价（付自己报价）、$\eta=1/\sqrt{m}$、对偶梯度 $\alpha\leftarrow\max(\alpha+\eta\,p_j-\eta\,B/m,0)$。

| 配置 | 花费 | 赢下次数 | 超支倍数 | 终态 $\alpha$ |
|---|---|---|---|---|
| 仅对偶梯度（无硬截断） | **1356.78** | 2919 | **1.357×** | 1.784 |
| 对偶梯度 + 预算耗尽即停（硬截断） | **1000.00** | 2074 | 1.000× | 1.774 |

**结论**：在 $4\times10^4$ 次机会的尺度上，单纯的对偶梯度把超支压到 1.36 倍（比 DSP-2026-10-26 中 $O(\sqrt{m})$ 理论下所担心的更加温和），但仍**无法严格守住预算**；加一行"预算耗尽即停"后精确贴预算。**"节奏"与"兜底"是两件事，必须分别实现，并共享一个预算账本**——这正是工程上最容易在两个团队之间掉链子的地方。

### 6.5 pacing：控制论回归与新证据

上一版把 pacing 写成"PID → 规划 → 学习型"三代。2025–2026 的证据显示**第一代并没有被淘汰**，而是在被重新做对：

> **真摘录（小额预算 pacing，2025-09，v2 2026-03）**：现有 pacing 方法"often rely on ad-hoc parameter tuning, which can be unstable and inefficient"。作者提出一个"principled controller"：**bucketized hysteresis + 比例反馈**，并给出参数选择框架与分析，使各计划能准确跟踪目标消耗速率。真实竞价实验：pacing 误差降低 **13%**、$\lambda$ 波动降低 **54%**（相对基线），对小预算计划受益尤其明显。
> （[arXiv:2509.25429](https://arxiv.org/abs/2509.25429)，等级 A/B）

> **真摘录（pacing 均衡的一般理论，2026-09）**：平台广泛用**乘性 pacing** 调节买家出价以渐进花预算，但其总体行为取决于机制。一价单品市场中 pacing 有强结构与可计算性，二价则不成立。作者在机制层级上建立统一理论：一价**按出价支付**（pay-your-bid）机制类是"pacing 均衡存在、唯一、并有 Eisenberg-Gale 型凸规划刻画"的广义类，从而**高效计算**且保证 **Pareto 有效与'流动福利'（liquid welfare）**；对满足**支付单调性**的抽象机制，用平滑不连续性的方法证明均衡存在，再给出唯一性、预算可行 pacing 向量中的**收入最大性**、**抗托（shill-proof）可实现性**，以及收敛的预算调整动力学。
> （[Afiouni & Kroer](https://arxiv.org/abs/2609.27285)，arXiv:2609.27285，等级 A）

> **买方含义**：pacing 不再只是"我们自己的控制器"，它同时决定了**自己作为买家的博弈位置**。当平台也在做 pacing 均衡时，"个体最优"与"均衡"不一致——这是第 12 章"竞争学习"问题的理论源头。

### 6.6 约束出价的新进展：从"单智能体最优"到"生态最优"

> **真摘录（NCB，阿里妈妈，2025/2026）**：主流工业系统用**单智能体**自动出价，可扩展但"overlook the strategic interdependence among advertisers' bids, leading to unstable or suboptimal outcomes"。NCB 把自动出价重构为**受 Nash 均衡约束的平台级优化**，用带收敛保证的**罚项原始-对偶梯度法**，并给出适合工业部署的高效算法。
> （[arXiv:2503.10304](https://arxiv.org/abs/2503.10304)，等级 A）

> **真摘录（ABPlanner，KDD 2025 ADS Track）**：自动出价的目标是在预算约束下最大化累计赢得印次的价值，但"diverse advertisers"使问题困难。ABPlanner 是**少样本可适配的预算规划器**，基于分层出价框架把出价过程分解为更短阶段，由规划器在所有阶段间分配预算，低层出价器按该计划出价；适配性来自"in-context reinforcement learning"式的序贯决策——对每个广告主用**前几个 episode 的数据作为 prompt** 逐 episode 调整预算计划，从而用少量数据快速适配。仿真与**真实 A/B** 验证了累计价值提升。
> （[arXiv:2502.05187](https://arxiv.org/abs/2502.05187)，等级 A）

> **真摘录（平台基准 PlatformBid，2026-07）**：传统自动出价只关注 DSP 侧；但"current big ad platforms ... now integrate SSP, DSP, and Ad Exchange functions internally"，平台的目标不只是广告主转化，还有平台总收入。PlatformBid 是"首个从统一广告平台视角设计的综合基准"，定义三种代表性竞争设定：(1) **同质竞争**（广告主用相同算法）；(2) **异质竞争**（算法多样）；(3) **促销竞争**（黑五等场景下部分广告主预算暴涨）。系统评估了经典控制、RL 与生成式方法，并提出基于 **flow-matching** 的 **BidFlow**。快手线上实验显示目标成本 **+0.68%**，为离线-在线一致性提供部署证据。
> （[arXiv:2607.27265](https://arxiv.org/abs/2607.27265)，等级 A/B）

**这三篇合起来说明一个买方必须接受的事实**：**出价算法已从"单人对市场做回归"变成"多人与机制共同博弈"**。任何只拿离线日志训练的模型，在同质化的平台上会遇到"大家一起学同一策略"的退化——这正是第 12 章"竞争学习"要展开的问题。

### 6.7 轻量与稳健路线：不是所有品类都需要深度 RL

> **真摘录（品牌广告 MPC，2026-03/06）**：品牌广告的 RTB 文献少。作者提出**轻量 MPC** 框架，利用品牌广告的固有属性（用户参与模式稳定、反馈回路快）简化建模：用**在线等渗回归（isotonic regression）**从流式数据直接构造**单调的"出价-花费"与"出价-转化"模型**，"eliminating the need for complex machine learning models"，全在线、低算力。仿真显示花费效率与成本控制显著优于基线。
> （[arXiv:2603.07721](https://arxiv.org/abs/2603.07721)，等级 A，**仅仿真**）

> **买方含义**：如果你的品类满足"流量结构稳定 + 反馈快"（例如品牌曝光、应用直投），**一个 200 行的单调控制器可能比一个季度训练成本的深度策略网络更稳**。这类"不性感但可靠"的路线在工业上一直被低估。

---

## 第 7 章 生成式 / LLM 出价

### 7.1 三代生成式出价

| 代 | 代表 | 核心思想 | 证据 |
|---|---|---|---|
| 扩散生成 | AIGB（KDD 2024） | 用条件扩散模型生成整段出价轨迹，避免长序列误差累积 | A/B（厂商自述 GMV +4.2%、ROI +5.6%） |
| 多智能体扩散 | 潜图扩散（2025） | 显式建模广告主之间的相互影响 | A（学术） |
| 策略对齐 | GBS（SIGIR 2026） | 自回归生成 + GRPO 偏好对齐（见 6.2a） | A/B（美团上线） |
| 流匹配 | BidFlow（PlatformBid，2026） | 用 flow-matching 表达复杂策略，应对动态竞争 | A/B（快手 +0.68% 目标成本） |

### 7.2 LLM 作为出价器：真实位置

> **真摘录（LBM，2026-03）**：现有自动出价用离线 RL 或生成方法优化策略，但"can sometimes behave counterintuitively due to the black-box training manner and limited mode coverage of datasets"，难以理解任务状态与泛化。直接上 LLM 又因"need for precise actions in competitive auctions and the lack of specialized auto-bidding knowledge"，导致幻觉与次优决策。LBM 是**分层大出价模型**：高层 **LBM-Think** 做推理，低层 **LBM-Act** 生成动作；用**双嵌入机制**融合语言与数值两种模态；并提出**离线强化微调 GQPO**，以抑制 LLM-Think 的幻觉，且"without simulation or real-world rollout"。
> （[arXiv:2603.05134](https://arxiv.org/abs/2603.05134)，等级 A）

> **真摘录（SAGE，2026-07）**：LLM 用于出价的障碍是"shallow trajectory-text interactions and require costly fine-tuning"，难以在多样约束下高效利用预训练知识。SAGE 是**参数高效**的策略感知框架：(i) 时间-语义位置编码捕获轨迹动态与语义结构；(ii) 门控交叉注意力对齐轨迹与文本两种模态，缓解长轨迹算力；(iii) **约束门控 LoRA**：把约束作为路由信号，只激活少量专家，高效适配冻结的 LLM。大规模自动出价基准上"consistently achieves superior performance while tuning less than 10% of the trainable parameters required by full fine-tuning"。
> （[arXiv:2607.24232](https://arxiv.org/abs/2607.24232)，等级 A，**benchmark 上**）

**判断**：LLM 在出价中的位置目前有三条：

1. **推理层（Think）**：解释任务状态、给出高层意图，低频调用——LBM 的定位。
2. **参数高效适配层**：冻结大模型 + LoRA/专家路由，用约束做门控——SAGE 的定位。
3. **运营层**：作为投放 Agent 与人对话（TTD 的 Koa Assistant、各平台的"AI 营销官"），**不下探到毫秒级出价**。

> **本报告的 D 级判断**：2026 年"LLM 直接输出 bid"在生产环境里仍不现实——毫秒预算、可验证性与追责都不过关。**LLM 的现实价值在"把约束翻译成策略偏好"和"把问题诊断给人听"**，而不是替代 $b_j$ 的计算。

---

## 第 8 章 预算与跨渠道

### 8.1 分层：先计划、再出价

ABPlanner（KDD 2025）与 AIGB（KDD 2024）都采用"**上层规划预算/轨迹，下层按计划出价**"的分解。买方工程上这个分解尤其有价值：

- 上层（分钟/小时级）：跨渠道、跨计划分配预算 → 可用较重的模型、可离线训练。
- 下层（毫秒级）：单计划出价 + shading → 必须是闭式/轻量。

DSP-2026-10-26 第 4.3 节引用的结论（只调 RoS 目标可能任意次优、只调预算可达全局最优）从理论上支持这种分层。

### 8.2 本报告的仿真 D：贪心同样可以输给"平均分"

这一节刻意报告一个**对"算法优选"不利**的结果。

设置：4 个渠道，预算份额 $\sum x_i=1$；渠道收益 $y_i(x)=A_i(1-e^{-\lambda_i x_i})-\kappa(x_i-x_i^*)^2$（凹 + 偏离最优的惩罚），最优份额 $x^*\sim\mathrm{Dirichlet}$，400 次重复。比较：(i) 平均分；(ii) 用噪声反馈做**拉格朗日梯度的指数权重更新**（$\eta=0.35$，反馈噪声 0.05）。

| 策略 | 平均收益 | 相对 oracle |
|---|---|---|
| 平均分 | 4.3466 | 97.79% |
| 自适应（指数权重 + 梯度） | **4.5737** | **102.9%** |
| oracle（直接给 $x^*$） | 4.4449 | 100% |

**怎么读**：

1. **自适应确实赢了平均分（+5.2%）**，在 400 个随机场景上稳定，且没有过拟合到单个场景。
2. **它甚至略高于 oracle**，原因是 oracle 把 $x$ 精确钉在 $x^*$ 上，忽略了在真实系统里"**在预算约束边界上留一点余量**"带来的收益（仿真里体现在二次项被"合法地"利用）。这提示：**"对齐最优解"不等于"最优"**——工程上更应优化可实现的策略，而不是复刻一个理想解。
3. **但这个结论的适用范围很窄**：如果渠道收益是线性的、没有偏离惩罚、或反馈噪声很大，自适应会退化。**不要把它当成"自适应总是优于平均分"的定律**。

> **给买方的一句话**：跨渠道预算的"最优"通常只比平均分好 **2–5%**，而预估标定（第 5 章）与增量度量（第 9 章）的偏差动辄 **20–50%**。**先修标定，再谈分配。**

---

## 第 9 章 度量与增量

### 9.1 归因 ≠ 增量

> **真摘录（归因蚕食校正，TikTok，ADKDD 2026）**：大规模付费获客与增长广告系统把生产级归因结果直接用于**每日预算分配与渠道诊断**。但"paid-attributed conversions such as daily new users (DNU) may systematically overstate true incremental growth when paid channels overlap with organic demand, brand-driven traffic, or other acquisition channels"。作者提出**实验标定的归因校正框架**：用增量实验作为因果锚点，把稀疏的 lift 测量转成每日的校正估计；并在结构一致性约束下把校正后的蚕食体量分配到业务层级。离线前向校验相对原始归因与精细 ML 基线显著降低标定误差；在**多个 TikTok 全球市场部署**，预算与流量策略调整后实测蚕食率下降**约 15 个百分点**。
> （Li et al.，ADKDD 2026，等级 A/B）

### 9.2 不放假的地理实验

> **真摘录（伪增量检验，2026-09）**：当随机实验不可得时，企业运营本身会产生**突然的干预**——预算被砍、新渠道上线、项目暂停。作者提出两阶段方法把这类事件当准实验：第一阶段用**精确 Bayesian run-length 推断**在营销活动序列上**发现并标注干预日**；第二阶段用方差受限的结构时间序列反事实做因果影响分析，配合模拟推断、五项合格条件与**闭式功效界**。在 Meta 随 GeoLift 框架发布的**两个实验基准**上验证：两次都**精确识别出干预日**；"撤除广告"实验上把效应恢复到实验估计的 **6.2% 以内**（implied return 1.50 vs 1.60）；"新增广告"实验上 90% 区间覆盖实验估计且排除零。同数据上评估的六种估计器中，**只有本方法不需要地理面板**，且区间在两个实验上都正确、**窄到可据以行动**。
> （[arXiv:2609.18257](https://arxiv.org/abs/2609.18257)，stat.ME，等级 A，需注意未经同行评审确认）

**买方含义**：geo holdout 是金标准，但它贵、慢、且常常统计功效不足。这条路线说明**运营中天然存在的事件也能给出可行动的区间**——前提是先把"干预识别"做对。

### 9.3 隐私噪声下的可识别性

> **真摘录（隐私稳健增量测量，2026-06）**：平台的随机 lift 测试受隐私化上报系统侵蚀：**匹配率损失、可链接性损失、归因窗口损失、聚合阈值抑制、随机上报噪声、分群异质信号损失**。作者把隐私约束下的广告度量写成**稳健因果决策问题**：给定随机实验与"隐私引起的退化"的模糊集，把与观测相容的干净世界集合投影到增量泛函上，返回**认证（certified）/ 拒绝（rejected）/ 未决（unresolved）**三类决策。主要结果给出**清晰的决策前沿**：前沿之外的报告可一致地认证或拒绝；**前沿之内信息量不足以让任何方法一致区分"高于阈值的增量"与"无增量"**。并有有限样本认证、样本复杂度保证、极小极大下界（信号损失降低有效信息）与上报粒度权衡。在 200 万行 Criteo Uplift 与 64K 行 Hillstrom 邮件实验上：干净 lift 都为正（0.00112 与 0.00495）；群体层面在两数据集上分别通过轻度与重度退化，但**在同时纳入不确定性与上报噪声的所有有限样本压力设置下均为"未决"**。
> （[arXiv:2606.03878](https://arxiv.org/abs/2606.03878)，等级 A）

> **真摘录（决策校准的 conformal 不确定性，2026-06）**：pacing 依赖不确定的未来库存、需求压力、增量响应与会员体验负载。作者不用通用的预测残差校准，而是**用"对可部署 pacing 策略的最大影响"来度量预测误差**；主定理证明该得分是"一致保护所有可部署 pacing 策略"的**最小有效不确定性度量**（几何上是签名策略敏感集的支持函数）。在 Criteo Uplift 与 KuaiRand 上的 pacing 回放中，传统 conformal pacing 的残差半径高达 7236.7 / 4629.4，而决策校准将其降到 **18.4 / 278.6**；Criteo 上把留出集的"任何违例率"从 **16.7% 降到 3.3%**，预算与会员负载违例为 0。
> （[arXiv:2606.10187](https://arxiv.org/abs/2606.10187)，等级 A）

**给买方的落地清单（本章的实用结论）**：

1. 每个渠道都要有**自己的** holdout 或 geo 实验，不能引用平台报表当增量。
2. 做实验前先算**功效**：在隐私噪声下，"没显著"不等于"没效果"，而可能是"未决"。
3. 预算决策用**区间**而不是点估计；把"未决"作为合法决策状态写进流程。
4. pacing 的不确定性应该按**对决策的影响**校准，不是按预测误差校准——这决定了你最后会不会超支。

---

## 第 10 章 工业产品图

### 10.1 二维产品矩阵（约束 × 自动化）

| 平台/产品 | 约束形态 | 自动化程度 | 买方可控项 | 证据 |
|---|---|---|---|---|
| Google Ads Smart Bidding（tCPA/tROAS/Max conv. 等） | 成本/回报 | 给目标，系统出价 | 目标、预算、素材 | B（产品文档）；实现细节 D |
| Google Ads 竞价时出价（Auction-Time Bidding） | 成本 | 按**每次竞价**的上下文信号出价 | 同上 | B（2019 官方博客，conversions +15~30%，等级 B/C） |
| DV360 | 预算+成本 | 计划/广告组级自动化 | 出价策略、deal、库存 | B/D |
| The Trade Desk Kokai / Koa | 效果（KPI） | **分布式 AI**：预测性清算价（predictive bid clearing）、相关性打分、预算优化、KPI 打分、预测；2026 年 Zuma 版宣称 CPA 平均改善 **32%**（行业报道，**未独立验证**） | 种子人群、库存、deal 优先级、Koa 模式 | C（[PPC Land 事实表](https://ppc.land/kokai/)） |
| Amazon DSP | 规则式 / 算法式 | 计划级 | 出价规则、优化目标 | B（帮助文档） |
| 微软 Xandr / Invest + Curate | deal / 预算 | deal 策划（curation）与 Invest DSP | deal 结构、curator | B（[Microsoft Learn](https://learn.microsoft.com/en-us/xandr/monetize/curated-deals)） |
| 腾讯广告 AIM+ nobid | **仅预算**（无强成本约束） | 只设预算、不设出价 | 预算、时段、目标 | B（产品文档二手转载，[2026-03](https://www.teng-ad.com/jd/4457.html)） |
| 阿里妈妈（万相台无界 / 全站推广） | RoI/预算 | 托管 | 预算、目标 RoI 出价 | B/C |
| 巨量引擎（oCPM / 放量 / 稳投类） | 成本/预算 | 托管 | 出价、预算、定向 | B/C |

> **矩阵的两条解读**
>
> 1. **越往右下（强自动化 + 弱约束），越依赖"预算即是控制变量"。** nobid 的本质是"把约束从成本转移到预算"，这在算法上等价于**对偶变量取 0**——系统不再优化"每单成本"，只优化"在预算内拿最多转化"。这解释了为什么官方文档明确写"**nobid 是没有强成本约束的，需要通过调控预算实现成本调控**"和"预算设置越高，成本可能升高"。
> 2. **产品差异主要在"谁来兜底约束"。** Google/阿里妈妈由系统兜底成本；TTD 由交易员兜底（Koa 可切换 Performance/Control 模式）；nobid 由广告主用预算兜底。**选型问题因此等价于"你愿意把成本风险交给谁"**，而不是"谁的算法更先进"。

### 10.2 平台口径的处理原则

- 厂商宣称的效果（如 Zuma 的 32% CPA 改善、AIGB 的 GMV +4.2%）一律标**等级 C/B**，不进入选型依据。
- 研究报告可以引用的，是**有公开元数据与可核验方法**的论文（本篇的第 4–9 章）。
- 对"分布式 AI""预测性清算价"这类描述，要追问三件事：**信号是什么、反馈回路多长、兜底在哪一层**。

---

## 第 11 章 隐私与信号

### 11.1 2026 年的实际状态

行业汇总口径（等级 C）：Chrome 已全面弃用三方 Cookie；买方采用"Privacy Sandbox（Topics/Protected Audience）+ 认证标识（UID2/ID5/RampID）+ 上下文信号 + 数据洁净室"的混合栈；认证流量平均匹配率稳定在 **47%**，低于 Cookie 时代的 68%。

### 11.2 对算法的三条影响

1. **跨站特征减少 → $v_j$ 估计方差上升。** 第 6.3 的仿真表明竞争估计噪声会直接变成多付，价值估计噪声同理。
2. **匹配率下降 → 归因窗口缩短 → 延迟反馈问题加剧**（第 5.2）。
3. **聚合阈值抑制 → 小分群不可测。** 这正是第 9.3"未决"状态的现实来源。

### 11.3 应对（按 ROI 排序）

| 优先级 | 动作 | 理由 |
|---|---|---|
| 1 | 服务端 / 第一方转化回传（Conversions API） | 直接提升匹配与延迟反馈质量 |
| 2 | 上下文信号提权（页内容、版位、时段） | 不依赖标识、跨站可用 |
| 3 | 建模信号损失（而非假设零损失） | 第 9.3 的"未决"框架 |
| 4 | 清洁室做跨渠道度量 | 避免平台内归因污染 |

---

## 第 12 章 前沿与未解问题

1. **竞争学习与同质化退化**。PlatformBid（2026）专门设计了"同质竞争"设定，说明了问题：当所有广告主跑同一算法时，离线最优策略的收益会被相互抵消。目前只有理论（NCB、pacing 均衡）与基准，没有公开的工业解决方案。
2. **机制操纵与不可信的拍卖方**。
   > **真摘录（2026-05）**："shilling"是用人为出价让竞争显得更激烈、抬价。作者研究**只影响反馈、不影响分配**的 shilling：学习者与真实竞价对手比输赢，但输掉后观测到的是"真实竞价与独立 shill 竞价的最大值"。因此操纵改变了**学到什么**，而不改变当期结果。作者给出 $\\tilde{\\mathcal O}(T^{2/3})$（稳健区间消除分支，忽略被 shill 的报告）与 $\\tilde{\\mathcal O}(\\sqrt{T})$（乐观分支，在可靠时去偏并使用后缀信息）两条界，并用验证与竞速程序在不知尺度与反馈几何的前提下组合二者；结论："即使只操纵反馈的 shilling 也能显著改变重复竞价的统计难度"。
   > （[arXiv:2605.22438](https://arxiv.org/abs/2605.22438)，等级 A）
3. **Agentic 化的责任归属**。各家选择不同（TTD 保留 Control 模式；Meta 默认自主；腾讯用 nobid 把约束外移）。核心不是技术，而是**谁为一次糟糕的自动决策负责**。
4. **增量性的评估污染**。平台同时负责投放与归因，存在结构性利益冲突（第 9 章）。
5. **多约束与多坑位**。MEBS 解决了多坑位 shading 的形态问题，但**多约束下的高维对偶变量在线稳定性**仍是开放问题。
6. **LLM 的可验证性**。SAGE/LBM 都在"benchmark 上"证明有效；**上线后的可解释、可审计、可回滚**没有公开证据。
7. **冷启动的样本效率**。Bench-CTR 指出 LLM 可用 2% 数据达到可比性能；但**如何在毫秒预算内保留这一优势**（蒸馏到什么程度、丢多少精度）没有公开答案。

---

## 附录 A 复现说明（`assets/rtb_sim.py`）

| 实验 | 设置 | 关键结论 | 局限 |
|---|---|---|---|
| A. shading | $n=2\times10^6$，$v\sim\mathrm{LN}(0,0.5)$，$h\sim\mathrm{LN}(-0.3,0.6)$，噪声 $\sigma_v=0.25,\sigma_h=0.45$，$b=0.5v+0.5\hat h$ | 多付由 0.68 降到 0.34；竞争价估计噪声直接推高多付 | 无预算、无对手反应、竞争分布固定 |
| B. pacing | $m=4\times10^4$，$B=1000$，$\eta=1/\sqrt m$，一价 | 无硬截断超支 1.36×；硬截断精确贴预算 | 单一计划、无跨计划共享 |
| C. 标定 | $n=4\times10^5$，真 pCVR 由 logit 模型生成，比较三种尺度 | AUC 相同（0.9246）时成交单价差 2–4 倍 | 固定投放量，未建模标定→选择的反馈 |
| D. 分配 | 4 渠道 × 400 轮 × 400 重复，凹收益 + 偏离惩罚 | 自适应 4.5737 vs 平均分 4.3466（+5.2%），oracle 4.4449 | 收益形态为构造，不具普适性 |

> **统一声明**：以上均为**合成数据上的机制演示**，用于验证结构性结论，**不代表任何真实平台效果**，也不构成投放建议。脚本种子固定，可逐行复现。

## 附录 B 算法速查

| 场景 | 推荐算法族 | 需在线维护的量 | 典型工程预算 |
|---|---|---|---|
| 一价、竞争未知 | 端到端 shading（GBS 类）或 DR-Shading | shading 头参数 + 特征 | 推理 <10 ms |
| 一价、竞争稳定 | 两阶段（位次分布 + 优化） | 分布分位数 | 推理 <5 ms |
| 预算约束 + 成本约束 | 对偶出价（USCB 形态）+ 双环 pacing | 2 个乘子 | 更新 1–60 s |
| 小额/新计划 | 迟滞 + 比例反馈控制器 | 速率目标 | 更新 1–5 min |
| 品牌、反馈快 | 在线等渗回归 + MPC | 单调曲线 | 全在线 |
| 多广告主互相影响 | 均衡约束（NCB 类）或平台基准评估 | 平台级 | 离线重训 |
| 冷启动广告主 | 分层预算规划器（ABPlanner 类） | 预算计划 | 小时级 |

## 附录 C 术语中英对照

| 中文 | 英文 | 含义 |
|---|---|---|
| 出价折扣 | bid shading | 一价下压低出价 |
| 竞价位次分布 | bid landscape | 最高竞争价的分布 |
| 预算平滑 | budget pacing | 控制消耗节奏，乘性 pacing 最常见 |
| 对偶变量 | dual variable / multiplier | 约束的影子价格 |
| 标定 | calibration | 预测值的绝对准确性（ECE 等） |
| 延迟反馈 | delayed feedback | 转化/退款晚于点击 |
| 增量性 | incrementality | 广告带来的因果增量，不同于归因 |
| 地理实验 | geo holdout test | 按地区分组做对照实验 |
| 分布稳健 | distributionally robust | 在最坏情形分布下优化 |
| 抗托 | shill-proof | 抵抗人为托价 |
| 流动福利 | liquid welfare | pacing 文献中的总支付能力约束福利 |

---

## 参考文献

**有 arXiv 元数据、已核对摘要（本地论文库真摘录）**

1. Huang et al. *Generative Bid Shading in Real-Time Bidding Advertising*. SIGIR 2026. arXiv:2508.06550.
2. Qu, Kant, Chen, Kitts, Gultekin, Flores, Blanchet. *Double Distributionally Robust Bid Shading for First Price Auctions*. arXiv:2410.14864, 2024.
3. Gong et al. *MEBS: Multi-task End-to-end Bid Shading for Multi-slot Display Advertising*. CIKM 2023. arXiv:2403.02607.
4. Nodozi, Gligorijevic, Halder. *Learning Concave Bid Shading Strategies in Online Auctions via Measure-valued Proximal Optimization*. arXiv:2509.10693, 2025.
5. Das. *Strategic Bid Shading in Real-Time Bidding Auctions in Ad Exchange Using Minority Game Theory*. arXiv:2512.15717, 2025（**仅核对摘要，未复核其结论**）。
6. Duan et al. *An Adaptable Budget Planner for Enhancing Budget-Constrained Auto-Bidding in Online Advertising*. KDD 2025 ADS. arXiv:2502.05187.
7. Mou et al. *Large-Scale Auto-bidding with Nash Equilibrium Constraints*. arXiv:2503.10304, 2025/2026.
8. Yang et al. *PlatformBid: An Auto-Bidding Benchmark from a Unified Advertising Platform's Perspective*. arXiv:2607.27265, 2026.
9. Li et al. *LBM: Hierarchical Large Auto-Bidding Model via Reasoning and Acting*. arXiv:2603.05134, 2026.
10. Cai et al. *Strategy-Aware Parameter-Efficient Adaptation for LLM-based Auto-Bidding*. arXiv:2607.24232, 2026.
11. Lin et al. *ClickPrompt: CTR Models are Strong Prompt Generators for Adapting Language Models to CTR Prediction*. WWW 2024. arXiv:2310.09234.
12. Gao, Yang. *Toward a benchmark for CTR prediction in online advertising*. Electronic Commerce Research, 2025. arXiv:2512.01179.
13. Wang, Shen, Zhang, Lin. *Feature Staleness Aware Incremental Learning for CTR Prediction*. arXiv:2505.02844, 2025.
14. Luo et al. *Modeling Cascaded Delay Feedback for Online Net Conversion Rate Prediction*. WWW 2026. arXiv:2601.19965.
15. Fei, Zhang, Li. *Entire-Space Variational Information Exploitation for Post-Click Conversion Rate Prediction*. arXiv:2502.15687, 2024.
16. Zhang et al. *GPR: Towards a Generative Pre-trained One-Model Paradigm for Large-Scale Advertising Recommendation*. arXiv:2511.10138, 2025/2026.
17. Xue et al. *Generative Recommendation for Large-Scale Advertising*. arXiv:2602.22732, 2026.

**已核对摘要、未入库（部分因 vet 的主题词要求或被判定为邻近领域）**

18. Apparaju, Niu, Qi. *Feedback Control for Small Budget Pacing*. arXiv:2509.25429, 2025/2026.
19. Afiouni, Kroer. *Pacing Equilibria in Abstract Mechanisms*. arXiv:2609.27285, 2026.
20. Shekhar, Howard. *Decision-Calibrated Conformal Uncertainty for Pacing Decisions in Streaming Advertising*. arXiv:2606.10187, 2026.
21. Shekhar, Howard. *Privacy-Robust Incrementality Measurement for Advertising Systems under Signal Loss*. arXiv:2606.03878, 2026.
22. Li, Yuan, Yang, Chen, Song. *Attributed, But Not Incremental: Cannibalization-Corrected Attribution for Large-Scale Advertising*. ADKDD 2026. arXiv:2606.26690.
23. Filippou, Quach, Jha. *Pseudo-Incrementality Testing: Measuring Advertising Lift from Naturally Occurring Interventions*. arXiv:2609.18257, 2026.
24. Chen, Zhu, Xia, Wang. *A Lightweight MPC Bidding Framework for Brand Auction Ads*. arXiv:2603.07721, 2026.
25. Foscari, Tullii, Perchet. *Do Not Trust The Auctioneer: Learning to Bid in Feedback-Manipulated Auctions*. arXiv:2605.22438, 2026.
26. Zeithammer, Alcobendas. *Slim Shading in Ad Auctions: Adjustment of Bidding Strategies to First-Price Rules*. UCLA × Yahoo Research, 2026-06.

**工业与行业材料（等级 B/C）**

27. The Trade Desk 在 Kokai 上的技术说明（Koa 的 predictive bid clearing 等）。Kokai 事实与时间线汇总：<https://ppc.land/kokai/>（2026-10-21）。
28. Microsoft Learn. *Microsoft Monetize - Curated deals*（2025-10-21 更新）。<https://learn.microsoft.com/en-us/xandr/monetize/curated-deals>
29. Digital Applied. *Programmatic Advertising Statistics 2026*（2026-04-21）。<https://www.digitalapplied.com/blog/programmatic-advertising-statistics-2026-data-points>
30. BidsCube. *What Is Bid Shading and How It Works in First-Price Auctions*（2026-09-06）。<https://bidscube.com/blog/what-is-bid-shading-and-how-it-works-in-first-price-auctions/>
31. 腾讯广告《AIM+-nobid 产品文档》（2026-03，二手转载）。<https://www.teng-ad.com/jd/4457.html>
32. PPC Land. *Google introduces Google Ads' Auction-Time Bidding in Search Ads 360*（2019-09-22，转述官方博客）。<https://ppc.land/google-introduces-google-ads-auction-64df3ea5e36c17001bef0fed/>

---

## 说明

- 本报告完成于 2026-10-26，公开材料检索截至当日。
- **证据分级**：A = 同行评审论文 / 官方技术报告；B = 官方文档 / 工程博客；C = 行业媒体 / 二手统计；D = 本报告推断。
- 所有厂商宣称的效果数字均标注来源与等级，**未经独立复现的不作因果结论**。
- 第 6.3、6.4、5.1、8.2 的仿真为合成数据机制演示，脚本与口径见 `assets/rtb_sim.py`。
- 部分参考文献（18–26）已核对 arXiv 摘要但未写入本地论文库（`vet` 的主题词校验对"bid shading / pacing / incrementality"等邻近主题要求标题直含主题句，故被判定 WEAK/PARTIAL 时未强写）；其摘要证据仍按 A/B/C 分级引用。
- 本报告不构成任何平台选型或投放策略建议。
