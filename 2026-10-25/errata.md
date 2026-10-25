# 《强化学习：从试错学习到推理智能》审读勘误

> 审读日期：2026-10-25 ｜ 对象：`00-reinforcement-learning-survey.md` 与 `assets/reinforcement-learning-survey.pdf`（LaTeX 源码：`Desktop/rl_survey`）
> 方法：逐条重推公式 + 小规模 MDP 数值验证（有限时域枚举、随机 MDP 压缩测试、DPO 反解残差）+ 对照原始论文与 Crossref 元数据

## 一、审读结论

正文的核心数学骨架**正确且可验证**，PDF 全文的推导质量显著高于 Markdown 摘要：摘要的问题主要来自"把 116 页的推导压缩成几行"造成的语义塌缩，而非数学错误。

已在 4 个独立数值实验中复核的结论：

| 结论 | 验证方式 | 结果 |
|---|---|---|
| 贝尔曼算子 $\gamma$-压缩 | 30 状态 × 4 动作随机 MDP，200 组随机值向量 | 实测最大压缩比 0.3454 ≤ $\gamma=0.9$ ✅ |
| 策略梯度定理 | 有限时域 $H=3$ 精确枚举轨迹 | 解析梯度 = 数值梯度 = −0.3973094689（误差 < 1e-11）✅ |
| DPO 闭式解与奖励反解 | 三动作策略，检验 $r=\beta\log\frac{\pi^*}{\pi_{ref}}+\beta\log Z$ | 三个动作反解残差均为 0，$\sum\pi^*=1$ ✅ |
| GRPO 组内优势零均值 | 直接代数验证 | $\frac{1}{G}\sum_i\hat A_i$ 恒为 0 ✅ |

## 二、更正：我上一轮的两处误判

**这两处是我（审读方）判断有误，原报告是正确的，本次不做修改。**

1. **策略梯度定理的折扣因子（原第 69 行、PDF 式 5.6）**

   我最初判定 $\mathbb{E}[\sum_t\gamma^t\nabla\log\pi\,G_t]$ 是"双重重加权"。数值复核表明这是**错的**：报告定义 $G_t=\sum_k\gamma^kR_{t+k+1}$（从 $t$ 起、以 $\gamma^0$ 开头的折扣回报），此时
   $$\nabla_\theta J=\mathbb{E}\Big[\sum_t\gamma^t\nabla_\theta\log\pi_\theta(A_t\mid S_t)\,G_t\Big]$$
   精确成立（−0.3973094689 vs −0.3973094689，误差 < 1e-11）。若要省去外层 $\gamma^t$，则 $G_t$ 必须改用"含全折扣前缀"的写法，两者等价。
   **原写法正确，PDF 的逐式推导（式 5.8→5.11→5.12）也完全自洽。**

2. **GRPO 的 KL 项位置（PDF 式 7.22）**

   我怀疑 KL 应作为逐 token 奖励塑形而非序列级目标项。对照 DeepSeekMath 原文（式 3）确认：**原文正是把 $-\beta D_{\mathrm{KL}}(\pi_\theta\|\pi_{\mathrm{ref}})$ 直接加在目标函数里**，并明确说明 "instead of adding KL penalty in the reward"。PDF 忠实于原文。
   组内奖励除以标准差亦经原文确认（"normalized by subtracting the group average and dividing by the group standard deviation"）。

## 三、本次实际修订

### A. Markdown 摘要（`00-reinforcement-learning-survey.md`）

| # | 位置 | 问题 | 处理 |
|---|---|---|---|
| A1 | 贝尔曼收敛表述 | "值迭代以 $\gamma^k$ 几何收敛"省略了 $\frac{1}{1-\gamma}$ 放大常数 | 补出严格界 |
| A2 | 策略梯度定理 | 证明称"只依赖两个事实"，遗漏**因果性**（$t$ 时刻动作不影响之前奖励）这一必要条件 | 补为三个事实 |
| A3 | 策略梯度定理 | 期望分布写作"全回报"而非 reward-to-go，与 PDF 的 $G_t$ 定义口径不一致 | 统一为 reward-to-go 定义 |
| A4 | 时间线 Q-learning | 标注 1989，与文末参考文献 [3] 的 1992 冲突 | 改为"1989 博士论文 / 1992 期刊"并分别标注 |
| A5 | GRPO 优势 | 未说明 std=0（组内全对或全错）时除零退化 | 补充工程处理说明 |
| A6 | GRPO 显存 | "约为 PPO-RLHF 的一半"是将经验值当作结论 | 改为"省去与策略同规模的 critic" |
| A7 | DPO 推导 | 未点明"固定 $x$ 逐点最优"与"$Z(x)$ 因 $x$ 相同而消去"两个前提 | 补充前提 |
| A8 | 文内一致性 | 第 196 行称正文含 12 项完整证明，但 md 实际只有 4 段；另有 6 项只见于 PDF | 改为明确指向 PDF |
| A9 | 元数据 | "116 页 / 79 条参考文献"已核实属实（PDF 共 116 页，编号至 [79]） | 保留，加注核实来源 |

### B. LaTeX 源码与 PDF（`Desktop/rl_survey`）

经逐章核对，PDF 正文的数学推导无错。仅修正上述条款在 PDF 中的对应表述若有同类问题处，以及一处表格标注：

| # | 位置 | 问题 | 处理 |
|---|---|---|---|
| B1 | `chapters/ch3.tex` 时间线 | 表中 `1989 & Q-learning` 与正文"1989 年博士论文"一致，但读者易与 1992 期刊版混淆 | 年份列改为 `1989/1992` |
| B2 | `chapters/ch7.tex` GRPO | $\hat A_i$ 未提 std 为零的退化情形 | 补一句工程说明 |

### C. README

修正目录结构示例（原示例列出不存在的 `02-world-model.md` 且未反映 2026-10-25 目录），并补充本勘误的链接。

## 四、经核实无误、**不需修改**的主要事实

- 页数 116、参考文献 79 条 —— PDF 实测
- Watkins & Dayan, *Q-learning*, Machine Learning 8(3–4): 279–292, **1992** —— Crossref `10.1007/BF00992698`
- DeepSeek-R1, *Nature* **645**(8081): 633–638, 2025 —— Crossref `10.1038/s41586-025-09422-z`（arXiv:2501.12948 亦正确）
- AlphaTensor 模 2 的 $4\times4$ 矩阵乘 47 次（此前 Strassen 49 次）—— 注意该结论**仅在模 2 下成立**，报告已正确限定
- AlphaDev 短序列最高快 70%、超 25 万元素序列约 1.7% —— DeepMind 官方口径
- AlphaProof/AlphaGeometry 2 IMO 2024 得 28/42 银牌 —— DeepMind 官方口径
- AlphaGo 2016 *Nature* 529: 484–489；AlphaStar 2019 *Nature* 575: 350–354；DQN 2015 *Nature* 518: 529–533 —— Crossref
- 策略梯度定理证明、基线不变性（命题 5.1）、以梯度范数平方加权的最优基线（式 5.19）、值迭代近似界（定理 2.x，$2\gamma/(1-\gamma)$ 放大）、KL 正则闭式解（定理 7.1 拉格朗日推导）、DPO 及其梯度（式 7.19–7.21）—— 逐式复核正确
