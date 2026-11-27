#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建《竞价强化学习系统深度调研》PDF（reportlab + STSong-Light CID 字体）。

依赖: reportlab（venv: /home/admin/.venv-pdf）
输出: 2026-11-27/rl-bidding-systems-deep-dive.pdf
"""
import os
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import (PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)
from reportlab.pdfgen import canvas as canvas_module

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "rl-bidding-systems-deep-dive.pdf")

NAVY = colors.HexColor("#1a4a7a")
BLUE = colors.HexColor("#23609e")
GRAY = colors.HexColor("#6e6e6e")
LIGHT = colors.HexColor("#ebf0f6")
INK = colors.HexColor("#1e1e1e")
BORDER = colors.HexColor("#c9d6e4")

pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
registerFontFamily("STSong-Light", normal="STSong-Light", bold="STSong-Light",
                   italic="STSong-Light", boldItalic="STSong-Light")


class NumberedCanvas(canvas_module.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_footer(total)
            super().showPage()
        super().save()

    def _draw_footer(self, total):
        self.saveState()
        self.setFont("STSong-Light", 8)
        self.setFillColor(GRAY)
        self.drawCentredString(A4[0] / 2, 10 * mm, f"第 {self._pageNumber} 页 / 共 {total} 页")
        if self._pageNumber > 1:
            self.drawRightString(A4[0] - 18 * mm, A4[1] - 9 * mm,
                                 "竞价强化学习系统深度调研（2026-11-27）")
        self.restoreState()


def style(name, **kw):
    defaults = dict(fontName="STSong-Light", fontSize=10, leading=15.5,
                    textColor=INK, spaceBefore=0, spaceAfter=0)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)


S_TITLE = style("title", fontSize=17, leading=24, textColor=NAVY, spaceAfter=4)
S_SUB = style("sub", fontSize=10.5, leading=16, textColor=GRAY, spaceAfter=2)
S_SMALL = style("small", fontSize=8.5, leading=12, textColor=GRAY, spaceAfter=2)
S_H1 = style("h1", fontSize=13.5, leading=18, textColor=NAVY, spaceBefore=10,
             spaceAfter=5, backColor=LIGHT, borderPadding=(2, 4, 3, 4))
S_H2 = style("h2", fontSize=11, leading=15, textColor=BLUE, spaceBefore=7, spaceAfter=2.5)
S_BODY = style("body", spaceAfter=4)
S_BULLET = style("bullet", spaceAfter=2.5, leftIndent=10, bulletIndent=2)
S_PTITLE = style("ptitle", fontSize=10.5, leading=15, textColor=NAVY, spaceAfter=1)
S_PMETA = style("pmeta", fontSize=8.5, leading=12, textColor=GRAY, spaceAfter=1.5)
S_TAKE = style("take", fontSize=9.5, leading=14, spaceAfter=6)
S_ABS = style("abs", fontSize=8.5, leading=12, textColor=GRAY, spaceAfter=4)
S_ABS_T = style("abst", fontSize=9.5, leading=13.5, textColor=NAVY, spaceBefore=3, spaceAfter=1)
S_CELL = style("cell", fontSize=8, leading=11, spaceAfter=0)
S_CELLB = style("cellb", fontSize=8, leading=11, textColor=BLUE, spaceAfter=0)
S_CELLH = style("cellh", fontSize=8.5, leading=11.5, textColor=NAVY, alignment=TA_CENTER,
                spaceAfter=0)

story = []


def h1(text):
    story.append(Paragraph(escape(text), S_H1))


def h2(text):
    story.append(Paragraph(escape(text), S_H2))


def p(text):
    story.append(Paragraph(escape(text), S_BODY))


def bullet(text):
    story.append(Paragraph(escape(text), S_BULLET, bulletText="-"))


def bullet_rich(text):
    story.append(Paragraph(text, S_BULLET, bulletText="-"))


def small(text):
    story.append(Paragraph(escape(text), S_SMALL))


def link(url, label=None):
    return f'<link href="{url}">{escape(label or url)}</link>'


def paper_block(pid, title, cat, date, note, takeaway):
    story.append(Paragraph(f'<link href="https://arxiv.org/abs/{pid}">[{pid}] {escape(title)}</link>', S_PTITLE))
    meta = f"{cat} · {date}"
    if note:
        meta += f" · {note}"
    meta += f" · abs: {link(f'https://arxiv.org/abs/{pid}')} · pdf: {link(f'https://arxiv.org/pdf/{pid}')}"
    story.append(Paragraph(meta, S_PMETA))
    story.append(Paragraph("要点：" + escape(takeaway), S_TAKE))


def abs_block(pid, title, text):
    story.append(Paragraph(f'<link href="https://arxiv.org/abs/{pid}">[{pid}] {escape(title)}</link>', S_ABS_T))
    story.append(Paragraph(escape(text), S_ABS))


def table(header_cells, rows, widths_mm, cell_style=S_CELL):
    data = [[Paragraph(escape(c), S_CELLH) for c in header_cells]]
    for row in rows:
        data.append([Paragraph(escape(c), S_CELLB if i == 0 else cell_style)
                     for i, c in enumerate(row)])
    t = Table(data, colWidths=[w * mm for w in widths_mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f9fc")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t)
    story.append(Spacer(1, 4 * mm))


# ============================ 封面标题 ============================
story.append(Paragraph("竞价强化学习系统深度调研", S_TITLE))
story.append(Paragraph("可用的竞价数据与虚拟竞价环境 + 基于其设计的强化学习系统", S_SUB))
small("基于 arXiv 检索批次（主题 bidding 12 篇 + auction 6 篇，共 18 篇，2026-11-27 入库）"
      " · 与上一批 10 篇（01-bidding.md）配合阅读 · 含开源仓库盘点")
story.append(Spacer(1, 3 * mm))

p("问题：有没有\"包含我能用的竞价数据或虚拟竞价环境、并基于该环境设计的强化学习系统\"？"
  "答案是肯定的，且分三类：")
bullet("开源环境 / 基准（可直接下载运行）：AuctionNet（阿里妈妈，含环境+数据集+基线评估）、"
       "AuctionGym（Amazon）、RTBGym / SCOPE-RL、DynamAuction、AucArena、LLM-Auction 仿真环境；")
bullet("工业级 RL 竞价系统论文（给出完整系统设计，不可直接下载）：HiBid（美团部署）、SORL、MAAB、TEE、"
       "HALO、LBM、ABPlanner、NCB、经典预算约束竞价 RL；")
bullet("有理论保证的一价 + 预算出价学习算法：Dual-LTE 等（可结合自有日志落地）。")
p("本调研按\"环境与数据盘点 - 系统逐类拆解 - 对比表 - 三条可复现路线 - 论文清单\"组织；"
  "18 篇论文全部要点对应文末清单（编号 D1-D18），上一批的 10 篇以 arXiv 编号直接引用。")

# ============================ 1 环境与数据 ============================
h1("1. 可直接使用的竞价数据与虚拟环境（重点）")

h2("1.1 开源虚拟竞价环境 / 基准")
bullet("AuctionNet [D1]（2024，阿里）：来自真实广告平台的大规模广告竞价决策基准，由三部分组成："
       "广告竞价环境 + 基于环境的预生成数据集 + 多个基线出价算法的评估。环境通过模块交互复刻真实竞价："
       "机会生成模块用深度生成网络弥合模拟与真实数据的差距、同时规避敏感数据泄露；"
       "竞价模块实现多种以不同决策算法训练的 auto-bidding 智能体；"
       "拍卖模块锚定经典 GSP 拍卖、可自定义机制。官方仓库已公开（alimama-tech/AuctionNet）。"
       "这是\"虚拟竞价环境 + 强化学习\"最直接的起点。")
bullet("AuctionGym（KDD 2023，未收录 arXiv，仓库 amzn/auction-gym）：Gymnasium 风格的在线广告竞价环境，"
       "用于评估 bandit / RL 出价算法，内置预算约束与竞价格式切换。")
bullet("RTBGym / SCOPE-RL（仓库 hakuhodo-technologies/scope-rl）：RTB 合成仿真器（含拍卖与出价日志生成）"
       "→ 收集合成数据集 → 离线 RL 训练 + 离线策略评估（OPE）一套打通，适合先离线验证再上线。")
bullet("DynamAuction [D2]（2026-11）：单买家序贯竞价合成环境，专门刻画\"今天赢到的曝光改变明天物品价值\""
       "的动态价值问题（展示广告常见）。支持一价/二价、非齐次泊松到达、延迟反馈、饱和与近因效应"
       "（carry-over 状态概括历史赢得情况）；附带 MPC 基线（基准场景下优于 PPO/SAC/TD3 与调参 shading）；"
       "已开源发布。")
bullet("AucArena [D3]（2023）：面向 LLM 智能体的拍卖竞技场评估套件，模拟不可预测的拍卖场景，"
       "考察预算管理与目标遵循能力（GPT-4 类模型具备基本技能，但表现波动、简单方法有时更优）。")
bullet("LLM-Auction [D4]（2025）：LLM 原生广告下的生成式拍卖：拍卖对象从离散广告位变为 LLM 输出的分布，"
       "用偏好对齐把分配与机制目标一体化，并内置 LLM-as-a-judge 仿真环境做定量评估。")

h2("1.2 公开竞价数据与数据生成")
bullet("iPinYou（1407.7073，上一批）：首个公开 RTB 展示广告日志（竞拍/出价/曝光/点击/转化），"
       "做预算约束 RL 出价（如 [D7]）的经典数据源。")
bullet("AuctionNet 预生成数据集、RTBGym 合成数据集：随环境提供，开箱即用。")
bullet("拍卖数据生成方法 [D5]（2207.12255）：层级深度生成模型 + 人工学习者预测条件出价分布，"
       "模拟真实的一价密封拍卖数据（高基数特征 + 多级结构），为 agent-based 学习环境提供数据基础。")
bullet("多智能体拍卖仿真 [D6]（2004.02764）：用 MARL 训练竞价智能体参与英式/密封/Vickrey 拍卖，"
       "并与纳什均衡结果对比，验证 MARL 改善拍卖仿真结果。")

# ============================ 2 系统拆解 ============================
h1("2. RL 竞价系统逐类拆解（系统设计范式）")

h2("2.1 模拟器训练 vs 在线训练：VAS-RAS 差距与解决")
bullet("SORL [D8]（2210.07006，阿里，2022）：指出\"基于历史数据构建的离线虚拟广告系统（VAS）与真实系统（RAS）"
       "之间存在显著差距\"，正式定义线上/线下不一致问题（IBOO）并分析成因；提出可持续在线 RL 框架，"
       "基于 Q 函数 Lipschitz 平滑性设计安全高效的在线探索（SER）策略，直接在真实系统中持续训练。")
bullet("TEE [D11]（2402.15102，阿里，2024）：迭代离线 RL 框架——并行部署多个出价智能体收集交互数据，"
       "离线 RL 训练新策略后再部署；指出瓶颈来自离线 RL 的固有保守性导致的无效探索/利用，"
       "提出轨迹级探索与利用（TEE）方法打破瓶颈。")

h2("2.2 离线 RL 系统（基于历史日志）")
bullet("预算约束竞价 RL [D7]（1802.08365，阿里，2018）：把预算约束竞价形式化为 MDP，提出 model-free RL 框架；"
       "关键洞察是\"资源约束下环境的即时奖励具有误导性\"，据此设计面向约束 RL 的奖励函数学习方法；"
       "相比 model-based 方案可扩展、易于大规模部署。")
bullet("HiBid [D9]（2312.17503，美团，2023）：跨渠道约束竞价系统 = 高层规划器（带辅助损失的非竞争性预算分配）"
       "+ 数据增强的低层执行器（按预算自适应出价）+ CPC 引导的动作选择；在美团大规模日志与在线 A/B 上"
       "优于 6 个基线（点击量、CPC 达标率、ROI），已部署。")
bullet("HALO [D12]（2508.03267，2025）：面向广告主异构性（预算与 ROI 目标跨数量级）的多约束竞价（MCB）；"
       "用理论支撑的 hindsight 机制把失败的探索轨迹重定向为任意约束配置的训练数据，解决样本低效；"
       "并用 B-spline 建模约束与出价系数的物理关系，提升约束迁移泛化。")

h2("2.3 多智能体系统（竞争环境建模）")
bullet("MAAB [D10]（2106.06224，阿里，2021）：分布式多智能体出价框架；温度正则化信用分配建立"
       "\"合作-竞争\"混合范式，在个体效用与社会福利之间达到均衡；引入 bar agents 设置个性化出价下限，"
       "防止合作带来的串谋压价。")
bullet("NCB [D15]（2503.10304，阿里，2025）：把自动出价重铸为\"纳什均衡约束下的平台级优化\"，"
       "刻画广告主之间的策略性相互依赖；罚函数原始对偶梯度法有严格收敛保证，工业可部署。")

h2("2.4 LLM 出价系统")
bullet("LBM [D13]（2603.05134，2026）：层级大模型出价——高层推理（LBM-Think）与低层行动分层，"
       "利用 LLM 的先验知识与推理能力解决黑盒离线 RL/生成式方法的反直觉行为、数据集模式覆盖有限与幻觉问题。"
       "（工程提醒：LLM 出价必须加\"精确计算器\"审计兜底，见上一批 2611.34068。）")

h2("2.5 预算与一价拍卖的出价学习（理论保证）")
bullet("ABPlanner [D14]（2502.05187，2025）：few-shot 自适应预算规划器；层级框架把竞价分解为短阶段并逐阶段"
       "分配预算；以 in-context RL 的思路按 episode 用历史数据作为 prompt 快速适应新广告主。")
bullet("[D16]（2304.13477，2023）：对偶算法在重复一价拍卖中做预算管理；全信息反馈与\"仅赢家出价可见\""
       "的单边反馈下均达到 O(√T) 量级 regret，附数值实验验证。")
bullet("[D17]（2604.03103，2026）：对偶梯度下降出价策略应对一价转型与非平稳环境；"
       "无信息设定下 regret = O(√T) + Wasserstein 变差项（刻画非平稳，阶最优）；"
       "有预算分配预测时变差项可被消去。")
bullet("Dual-LTE [D18]（2605.09448，2026）：同时学习\"广告曝光的因果增量价值\"与\"赢得曝光所需的最强竞争出价 HoB\""
       "两个潜变量（共享上下文线性处理效应结构）；置信度引导探索协调价值估计、HoB 估计与预算/RoS 控制；"
       "全信息反馈 O(√T)、二元胜负反馈 O(T^{2/3}) 保证；用真实拍卖协变量做半合成实验。")

# ============================ 3 对比表 ============================
h1("3. 系统要素对比")
h2("3.1 环境 / 基准（可直接运行）")
table(
    ["名称", "形态", "拍卖机制", "数据 / 环境内容", "状态"],
    [
        ("AuctionNet [D1]", "基准 + 环境 + 数据集", "GSP（可自定义）",
         "深度生成的机会生成 + 多算法出价智能体 + 基线评估", "arXiv + 官方仓库"),
        ("AuctionGym", "Gymnasium 环境", "二价/一价可切换", "广告竞价 + 预算约束", "KDD'23，仓库开源"),
        ("RTBGym / SCOPE-RL", "仿真器 + 离线 RL 工具链", "RTB（GSP）", "合成 RTB 数据集 + OPE", "仓库开源"),
        ("DynamAuction [D2]", "合成环境", "一价 / 二价", "动态价值、泊松到达、延迟反馈", "已开源发布"),
        ("AucArena [D3]", "LLM 评估竞技场", "通用拍卖", "预算 / 风险管理技能评测", "arXiv"),
        ("LLM-Auction [D4]", "生成式拍卖 + 仿真", "一价（生成分配）", "LLM-as-a-judge 仿真环境", "arXiv"),
    ],
    [30, 32, 28, 56, 28],
)
h2("3.2 RL 竞价系统 / 算法")
table(
    ["系统", "数据 / 环境", "训练范式", "约束", "评估"],
    [
        ("预算约束竞价 RL [D7]", "iPinYou 等日志", "离线 model-free RL + 奖励学习", "预算", "大规模实验"),
        ("SORL [D8]", "真实系统 RAS（在线）", "在线 RL + 安全探索 SER", "预算/多约束", "在线"),
        ("HiBid [D9]", "美团日志", "层级离线 DRL", "总预算 + CPC", "日志 + 在线 A/B（已部署）"),
        ("MAAB [D10]", "多智能体环境", "合作-竞争 MARL", "个体目标 + 社会福利", "仿真"),
        ("TEE [D11]", "并行部署收集数据", "迭代离线 RL", "预算", "工业场景"),
        ("HALO [D12]", "历史探索轨迹", "在线 + hindsight 重定向", "预算 + ROI（MCB）", "多约束场景"),
        ("LBM [D13]", "离线数据 + LLM 知识", "层级 LLM 推理 + 行动", "目标 + 约束", "动态环境"),
        ("ABPlanner [D14]", "历史 episode 数据", "in-context RL 规划", "预算（分层分配）", "多广告主"),
        ("NCB [D15]", "平台级竞价环境", "纳什均衡约束优化", "预算 + KPI", "理论收敛 + 仿真"),
        ("[D16]", "重复一价拍卖", "对偶在线学习", "预算", "regret 理论 + 数值"),
        ("[D17]", "一价拍卖（非平稳）", "对偶梯度下降", "预算", "regret 理论"),
        ("Dual-LTE [D18]", "真实协变量（半合成）", "置信度引导在线学习", "预算 + RoS", "regret + 约束违背"),
    ],
    [34, 34, 36, 34, 36],
)

# ============================ 4 复现路线 ============================
h1("4. 三条可复现路线（怎么用起来）")

h2("路线 A：无日志，直接用开源环境（最快）")
bullet("下载 AuctionNet 仓库，用预生成数据集 + 内置环境训练 RL 出价智能体，与内置基线（不同决策算法训练的 "
       "auto-bidding 智能体）对比；需要 GSP 之外的机制时利用其可自定义拍卖模块 [D1]。")
bullet("用 AuctionGym 做 Gymnasium 风格的 bandit / RL 快速实验；用 RTBGym 生成合成 RTB 数据并跑离线 RL + OPE。")
bullet("关注动态价值（赢得曝光影响后续价值）问题时直接用 DynamAuction，其 MPC 基线是很好的对照 [D2]。")

h2("路线 B：有历史竞价日志，做离线 RL 系统")
bullet("复现 [D7] 的预算约束竞价 MDP（含约束奖励学习）作为基线；有跨渠道与 CPC 约束时参考 HiBid 的"
       "分层结构（预算规划器 + 出价执行器 + CPC 引导）[D9]。")
bullet("策略迭代用 TEE 思路：并行部署收集数据 → 离线 RL → 再部署，解决保守性瓶颈 [D11]。")
bullet("多约束 / 预算-ROI 组合多样时用 hindsight 重定向（HALO）提升样本效率 [D12]；"
       "预算分配用 ABPlanner 的 few-shot 分层规划 [D14]。")
bullet("评估：离线策略评估（OPE，可用 SCOPE-RL），再小流量 A/B（参照 HiBid 的日志 + 在线验证方式 [D9]）。")

h2("路线 C：无日志也无现成环境，先造环境")
bullet("用深度生成模型生成仿真竞价数据（[D5] 的一价拍卖数据模拟方法）或 RTBGym 合成器造环境，再走路线 A/B。")
bullet("一价场景的出价矫正参照上一批 2410.14864 的双重分布鲁棒 bid shading；"
       "有理论要求时采用 [D16][D17][D18] 的对偶类算法（预算 + RoS 约束、非平稳、O(√T) 保证）。")

h2("已知陷阱（来自这批论文自己的发现）")
bullet("VAS-RAS 差距：只靠历史数据建的模拟器训练，上线不一致（IBOO）——用在线安全探索 SORL 或迭代离线 RL 缓解 [D8][D11]。")
bullet("离线 RL 保守性：状态覆盖与探索受限，需要轨迹级探索利用与悲观惩罚的平衡 [D11]（上一批 2506.17919 的 "
       "PE-MORL 用环境模型 + 悲观 Q 学习是同一问题的解法）。")
bullet("约束异构与样本低效：不同广告主预算/ROI 跨数量级，失败探索无迁移价值 [D12]。")
bullet("非平稳与一价转型：对手与市场分布漂移使历史最优失效，需要自适应对偶策略与变差刻画 [D17]；"
       "二价数据直接用于一价会高估支付 [D16]。")
bullet("LLM 出价幻觉与反直觉决策：需层级推理 + 计算器审计兜底 [D13] + 2611.34068。")

# ============================ 5 论文清单 ============================
h1("5. 论文清单（本批 18 篇，链接可点击）")
paper_block("2412.10798", "AuctionNet: A Novel Benchmark for Decision-Making in Large-Scale Games",
            "cs.AI", "2024-12-14", "官方仓库: github.com/alimama-tech/AuctionNet",
            "[D1] 环境：来自真实广告平台的大规模广告竞价基准 = 深度生成机会模块 + 多算法出价智能体 + 可自定义 GSP "
            "拍卖模块 + 预生成数据集 + 基线评估。")
paper_block("2611.14000", "DynamAuction: A Reinforcement Learning Environment for Repeated Auctions with Dynamic Value",
            "stat.AP", "2026-11-10", "已开源发布",
            "[D2] 环境：动态价值（carry-over 状态）的重复拍卖 RL 环境；一价/二价、泊松到达、延迟反馈、饱和与近因效应；"
            "MPC 基线优于 PPO/SAC/TD3。")
paper_block("2310.05746", "Put Your Money Where Your Mouth Is: Evaluating Strategic Planning and Execution of LLM Agents in an Auction Arena",
            "cs.CL", "2023-10-09", "",
            "[D3] 环境：AucArena 拍卖竞技场，评估 LLM 智能体的策略规划与执行（预算管理、目标遵循）。")
paper_block("2512.10551", "LLM-Auction: Generative Auction towards LLM-Native Advertising",
            "cs.GT", "2025-12-11", "",
            "[D4] 环境+机制：LLM 原生广告的生成式拍卖；拍卖对象从广告位变为 LLM 输出分布；偏好对齐一体化分配与机制；"
            "LLM-as-a-judge 仿真环境。")
paper_block("2207.12255", "Implementing a Hierarchical Deep Learning Approach for Simulating Multi-Level Auction Data",
            "econ.GN", "2022-07-25", "",
            "[D5] 数据生成：层级深度生成模型 + 条件出价分布预测，模拟真实一价密封拍卖数据，"
            "为 agent-based 学习环境打数据基础。")
paper_block("2004.02764", "Using Multi-Agent Reinforcement Learning in Auction Simulations",
            "cs.GT", "2020-04-06", "",
            "[D6] 仿真：MARL 训练竞价智能体参与英式/密封/Vickrey 拍卖，结果优于纳什均衡对照。")
paper_block("1802.08365", "Budget Constrained Bidding by Model-free Reinforcement Learning in Display Advertising",
            "cs.AI", "2018-02-23", "",
            "[D7] 系统：预算约束竞价 MDP + model-free RL；指出约束下即时奖励的误导性，设计约束 RL 的奖励学习方法；"
            "大规模可部署。")
paper_block("2210.07006", "Sustainable Online Reinforcement Learning for Auto-bidding",
            "cs.LG", "2022-10-13", "",
            "[D8] 系统：定义线上/线下不一致（IBOO），提出可持续在线 RL（SORL）与安全高效在线探索（SER），"
            "直接在真实系统中训练。")
paper_block("2312.17503", "HiBid: A Cross-Channel Constrained Bidding System with Budget Allocation by Hierarchical Offline Deep Reinforcement Learning",
            "cs.LG", "2023-12-29", "美团部署",
            "[D9] 系统：跨渠道约束竞价 = 高层预算规划器 + 数据增强低层执行器 + CPC 引导动作选择；"
            "日志 + 在线 A/B 优于 6 基线。")
paper_block("2106.06224", "A Cooperative-Competitive Multi-Agent Framework for Auto-bidding in Online Advertising",
            "cs.MA", "2021-06-11", "",
            "[D10] 系统：MAAB 合作-竞争多智能体出价；温度正则化信用分配达均衡（个体效用 + 社会福利）；"
            "bar agents 防串谋压价。")
paper_block("2402.15102", "Trajectory-wise Iterative Reinforcement Learning Framework for Auto-bidding",
            "cs.LG", "2024-02-23", "",
            "[D11] 系统：迭代离线 RL（部署-收集-离线训练循环）；轨迹级探索与利用（TEE）解决离线 RL 保守性瓶颈。")
paper_block("2508.03267", "HALO: Hindsight-Augmented Learning for Online Auto-Bidding",
            "cs.LG", "2025-08-05", "",
            "[D12] 系统：多约束竞价（MCB）；hindsight 机制把失败探索重定向为任意约束配置的训练数据；"
            "B-spline 建模约束-出价系数关系。")
paper_block("2603.05134", "LBM: Hierarchical Large Auto-Bidding Model via Reasoning and Acting",
            "cs.CL", "2026-03-05", "",
            "[D13] 系统：层级大模型出价（高层推理 + 低层行动），以 LLM 先验知识与推理缓解黑盒反直觉决策与幻觉。")
paper_block("2502.05187", "An Adaptable Budget Planner for Enhancing Budget-Constrained Auto-Bidding in Online Advertising",
            "cs.GT", "2025-01-26", "",
            "[D14] 系统：ABPlanner few-shot 自适应预算规划器；分层分阶段预算分配 + in-context RL 思路快速适应新广告主。")
paper_block("2503.10304", "Large-Scale Auto-bidding with Nash Equilibrium Constraints",
            "cs.LG", "2025-03-13", "",
            "[D15] 系统：NCB 纳什均衡约束的平台级自动出价；罚函数原始对偶梯度法，收敛保证 + 工业可部署。")
paper_block("2304.13477", "Learning to Bid in Repeated First-Price Auctions with Budgets",
            "cs.GT", "2023-04-26", "",
            "[D16] 算法：重复一价拍卖预算管理的对偶算法；全信息与单边反馈均 O(√T) regret。")
paper_block("2604.03103", "Adaptive Bidding Policies for First-Price Auctions with Budget Constraints under Non-stationarity",
            "cs.GT", "2026-04-03", "",
            "[D17] 算法：一价 + 预算 + 非平稳的自适应对偶梯度出价；regret = O(√T) + Wasserstein 变差项（阶最优），"
            "有预测时可消去变差项。")
paper_block("2605.09448", "Learning to Bid with Unknown Private Values in Budget-Constrained First-Price Auctions",
            "cs.LG", "2026-05-10", "",
            "[D18] 算法：Dual-LTE 同时学习因果增量价值与最强竞争出价（HoB）；置信度引导探索协调价值/HoB/预算/RoS；"
            "O(√T) / O(T^{2/3}) 保证；真实拍卖协变量半合成实验。")

# ============================ 6 附录 ============================
story.append(PageBreak())
h1("附录 A：论文摘要（原文，英文）")
abs_block("2412.10798", "AuctionNet: A Novel Benchmark for Decision-Making in Large-Scale Games",
          "Decision-making in large-scale games is an essential research area in artificial intelligence (AI) "
          "with significant real-world impact. However, the limited access to realistic large-scale game "
          "environments has hindered research progress in this area. In this paper, we present AuctionNet, a "
          "benchmark for bid decision-making in large-scale ad auctions derived from a real-world online "
          "advertising platform. AuctionNet is composed of three parts: an ad auction environment, a "
          "pre-generated dataset based on the environment, and performance evaluations of several baseline "
          "bid decision-making algorithms. More specifically, the environment effectively replicates the "
          "integrity and complexity of real-world ad auctions through the interaction of several modules: "
          "the ad opportunity generation module employs deep generative networks to bridge the gap between "
          "simulated and real-world data while mitigating the risk of sensitive data exposure; the bidding "
          "module implements diverse auto-bidding agents trained with different decision-making algorithms; "
          "and the auction module is anchored in the classic Generalized Second Price (GSP) auction but also "
          "allows for customization of auction mechanisms as needed. We evaluate the performance of a broad "
          "spectrum of state-of-the-art decision-making methods on AuctionNet, including behavior cloning, "
          "offline reinforcement learning, and online reinforcement learning.")
abs_block("2611.14000", "DynamAuction: A Reinforcement Learning Environment for Repeated Auctions with Dynamic Value",
          "A buyer who repeatedly participates in auctions for related items often faces a dynamic value "
          "problem: what they win today changes what tomorrow's items are worth. Despite the empirical "
          "importance of such effects, especially in display advertising, the algorithmic literature on "
          "repeated auctions has largely focused on the learning problem, by treating each opportunity as a "
          "contextual bandit, while sidestepping the planning problem induced by the dependence of current "
          "value on past wins. We introduce DynamAuction, a synthetic environment for single-buyer sequential "
          "bidding. The reward from each win depends on the buyer's history of previous wins, summarized "
          "through a carry-over state. The environment supports first- and second-price auctions, "
          "non-homogeneous Poisson arrivals, delayed feedback, saturation, and recency effects. We also "
          "introduce a new class of Model Predictive Control (MPC) algorithms. On our benchmark scenario, "
          "these MPC policies outperform off-the-shelf deep RL baselines (PPO, SAC, TD3) as well as a tuned "
          "shading baseline. We release DynamAuction to support RL research on repeated auctions.")
abs_block("2310.05746", "Put Your Money Where Your Mouth Is: Evaluating Strategic Planning and Execution of LLM Agents in an Auction Arena",
          "Recent advancements in Large Language Models (LLMs) showcase advanced reasoning, yet NLP "
          "evaluations often depend on static benchmarks. Evaluating this necessitates environments that test "
          "strategic reasoning in dynamic, competitive scenarios requiring long-term planning. We introduce "
          "AucArena, a novel evaluation suite that simulates auctions, a setting chosen for being highly "
          "unpredictable and involving many skills related to resource and risk management, while also being "
          "easy to evaluate. We conduct controlled experiments using state-of-the-art LLMs to power bidding "
          "agents to benchmark their planning and execution skills. Our research demonstrates that LLMs, such "
          "as GPT-4, possess key skills for auction participation, such as budget management and goal "
          "adherence, which improve with adaptive strategies. This highlights LLMs' potential in modeling "
          "complex social interactions in competitive contexts. However, variability in LLM performance and "
          "occasional outperformance by simpler methods indicate opportunities for further advancements in "
          "LLM design and the value of our simulation environment for ongoing testing and refinement.")
abs_block("2512.10551", "LLM-Auction: Generative Auction towards LLM-Native Advertising",
          "The commercialization of LLM applications is the next frontier in online advertising, with "
          "LLM-native advertising emerging as a promising paradigm by integrating ads into LLM-generated "
          "content. However, classic mechanisms are no longer applicable in this setting where the auction "
          "object is shifted from discrete ad slots to distributions over LLM outputs, and existing methods "
          "are impractical in industrial scenarios due to ignored externalities or high inference costs. To "
          "address these issues, we propose LLM-Auction, the first learning-based generative auction "
          "mechanism that integrates auction and generation. By formulating the allocation as preference "
          "alignment between LLM outputs and a mechanism objective that balances advertisers' value and user "
          "experience, we optimize the LLMs to inherently model allocation externalities without extra "
          "inference cost. Theoretically, we identify the allocation monotonicity and continuity of the "
          "optimal allocation rule of LLM-Auction, and prove that a simple first-price payment rule exhibits "
          "favorable incentive properties under this allocation rule. Furthermore, we build an LLM-as-a-judge "
          "simulation environment for quantitative evaluation.")
abs_block("2207.12255", "Implementing a Hierarchical Deep Learning Approach for Simulating Multi-Level Auction Data",
          "We present a deep learning solution to address the challenges of simulating realistic synthetic "
          "first-price sealed-bid auction data. The complexities encountered in this type of auction data "
          "include high-cardinality discrete feature spaces and a multilevel structure arising from multiple "
          "bids associated with a single auction instance. Our methodology combines deep generative modeling "
          "(DGM) with an artificial learner that predicts the conditional bid distribution based on auction "
          "characteristics, contributing to advancements in simulation-based research. This approach lays the "
          "groundwork for creating realistic auction environments suitable for agent-based learning and "
          "modeling applications. Our contribution is twofold: we introduce a comprehensive methodology for "
          "simulating multilevel discrete auction data, and we underscore the potential of DGM as a powerful "
          "instrument for refining simulation techniques and fostering the development of economic models "
          "grounded in generative AI.")
abs_block("2004.02764", "Using Multi-Agent Reinforcement Learning in Auction Simulations",
          "Game theory has been developed by scientists as a theory of strategic interaction among players "
          "who are supposed to be perfectly rational. These strategic interactions might have been presented "
          "in an auction, a business negotiation, a chess game, or even in a political conflict aroused "
          "between different agents. In this study, the strategic (rational) agents created by reinforcement "
          "learning algorithms are supposed to be bidder agents in various types of auction mechanisms such "
          "as British Auction, Sealed Bid Auction, and Vickrey Auction designs. Next, the equilibrium points "
          "determined by the agents are compared with the outcomes of the Nash equilibrium points for these "
          "environments. The bidding strategy of the agents is analyzed in terms of individual rationality, "
          "truthfulness (strategy-proof), and computational efficiency. The results show that using a "
          "multi-agent reinforcement learning strategy improves the outcomes of the auction simulations.")
abs_block("1802.08365", "Budget Constrained Bidding by Model-free Reinforcement Learning in Display Advertising",
          "Real-time bidding (RTB) is an important mechanism in online display advertising, where a proper "
          "bid for each page view plays an essential role for good marketing results. Budget constrained "
          "bidding is a typical scenario in RTB where the advertisers hope to maximize the total value of the "
          "winning impressions under a pre-set budget constraint. However, the optimal bidding strategy is "
          "hard to be derived due to the complexity and volatility of the auction environment. To address "
          "these challenges, in this paper, we formulate budget constrained bidding as a Markov Decision "
          "Process and propose a model-free reinforcement learning framework to resolve the optimization "
          "problem. Our analysis shows that the immediate reward from environment is misleading under a "
          "critical resource constraint. Therefore, we innovate a reward function design methodology for the "
          "reinforcement learning problems with constraints. Based on the new reward design, we employ a deep "
          "neural network to learn the appropriate reward so that the optimal policy can be learned "
          "effectively. Different from the prior model-based work, which suffers from the scalability problem, "
          "our framework is easy to be deployed in large-scale industrial scenarios.")
abs_block("2210.07006", "Sustainable Online Reinforcement Learning for Auto-bidding",
          "Recently, auto-bidding technique has become an essential tool to increase the revenue of "
          "advertisers. Facing the complex and ever-changing bidding environments in the real-world "
          "advertising system (RAS), state-of-the-art auto-bidding policies usually leverage reinforcement "
          "learning (RL) algorithms to generate real-time bids on behalf of the advertisers. Due to safety "
          "concerns, it was believed that the RL training process can only be carried out in an offline "
          "virtual advertising system (VAS) that is built based on the historical data generated in the RAS. "
          "In this paper, we argue that there exists significant gaps between the VAS and RAS, making the RL "
          "training process suffer from the problem of inconsistency between online and offline (IBOO). "
          "Firstly, we formally define the IBOO and systematically analyze its causes and influences. Then, "
          "to avoid the IBOO, we propose a sustainable online RL (SORL) framework that trains the "
          "auto-bidding policy by directly interacting with the RAS, instead of learning in the VAS. "
          "Specifically, based on our proof of the Lipschitz smooth property of the Q function, we design a "
          "safe and efficient online exploration (SER) policy for continuously collecting high-quality "
          "interaction data. Experiments on a virtual bidding environment and real industry bidding "
          "environment demonstrate the effectiveness of the SORL framework.")
abs_block("2312.17503", "HiBid: A Cross-Channel Constrained Bidding System with Budget Allocation by Hierarchical Offline Deep Reinforcement Learning",
          "Online display advertising platforms service numerous advertisers by providing real-time bidding "
          "(RTB) for the scale of billions of ad requests every day. The bidding strategy handles ad requests "
          "cross multiple channels to maximize the number of clicks under the set financial constraints, "
          "i.e., total budget and cost-per-click (CPC), etc. Different from existing works mainly focusing on "
          "single channel bidding, we explicitly consider cross-channel constrained bidding with budget "
          "allocation. Specifically, we propose a hierarchical offline deep reinforcement learning (DRL) "
          "framework called HiBid, consisted of a high-level planner equipped with auxiliary loss for "
          "non-competitive budget allocation, and a data augmentation enhanced low-level executor for "
          "adaptive bidding strategy in response to allocated budgets. Additionally, a CPC-guided action "
          "selection mechanism is introduced to satisfy the cross-channel CPC constraint. Through extensive "
          "experiments on both the large-scale log data and online A/B testing, we confirm that HiBid "
          "outperforms six baselines in terms of the number of clicks, CPC satisfactory ratio, and "
          "return-on-investment (ROI). We also deploy HiBid on Meituan advertising platform.")
abs_block("2106.06224", "A Cooperative-Competitive Multi-Agent Framework for Auto-bidding in Online Advertising",
          "In online advertising, auto-bidding has become an essential tool for advertisers to optimize their "
          "preferred ad performance metrics by simply expressing high-level campaign objectives and "
          "constraints. Previous works designed auto-bidding tools from the view of single-agent, without "
          "modeling the mutual influence between agents. In this paper, we instead consider this problem from "
          "a distributed multi-agent perspective, and propose a general Multi-Agent reinforcement learning "
          "framework for Auto-Bidding, namely MAAB, to learn the auto-bidding strategies. First, we "
          "investigate the competition and cooperation relation among auto-bidding agents, and propose a "
          "temperature-regularized credit assignment to establish a mixed cooperative-competitive paradigm. "
          "By carefully making a competition and cooperation trade-off among agents, we can reach an "
          "equilibrium state that guarantees not only individual advertiser's utility but also the system "
          "performance (i.e., social welfare). Second, to avoid the potential collusion behaviors of bidding "
          "low prices underlying the cooperation, we further propose bar agents to set a personalized bidding "
          "bar for each advertiser.")
abs_block("2402.15102", "Trajectory-wise Iterative Reinforcement Learning Framework for Auto-bidding",
          "In online advertising, advertisers participate in ad auctions to acquire ad opportunities, often "
          "by utilizing auto-bidding tools provided by demand-side platforms (DSPs). The current auto-bidding "
          "algorithms typically employ reinforcement learning (RL). However, due to safety concerns, most "
          "RL-based auto-bidding policies are trained in simulation, leading to a performance degradation "
          "when deployed in online environments. To narrow this gap, we can deploy multiple auto-bidding "
          "agents in parallel to collect a large interaction dataset. Offline RL algorithms can then be "
          "utilized to train a new policy. The trained policy can subsequently be deployed for further data "
          "collection, resulting in an iterative training framework, which we refer to as iterative offline "
          "RL. In this work, we identify the performance bottleneck of this iterative offline RL framework, "
          "which originates from the ineffective exploration and exploitation caused by the inherent "
          "conservatism of offline RL algorithms. To overcome this bottleneck, we propose Trajectory-wise "
          "Exploration and Exploitation (TEE), which introduces a novel data collecting and data utilization "
          "method for iterative offline RL from a trajectory perspective.")
abs_block("2508.03267", "HALO: Hindsight-Augmented Learning for Online Auto-Bidding",
          "Digital advertising platforms operate millisecond-level auctions through Real-Time Bidding (RTB) "
          "systems, where advertisers compete for ad impressions through algorithmic bids. This dynamic "
          "mechanism enables precise audience targeting but introduces profound operational complexity due "
          "to advertiser heterogeneity: budgets and ROI targets span orders of magnitude across advertisers, "
          "from individual merchants to multinational brands. This diversity creates a demanding adaptation "
          "landscape for Multi-Constraint Bidding (MCB). Traditional auto-bidding solutions fail in this "
          "environment due to two critical flaws: 1) severe sample inefficiency, where failed explorations "
          "under specific constraints yield no transferable knowledge for new budget-ROI combinations, and "
          "2) limited generalization under constraint shifts, as they ignore physical relationships between "
          "constraints and bidding coefficients. To address this, we propose HALO: Hindsight-Augmented "
          "Learning for Online Auto-Bidding. HALO introduces a theoretically grounded hindsight mechanism "
          "that repurposes all explorations into training data for arbitrary constraint configuration via "
          "trajectory reorientation. Further, it employs B-spline curves to encode physical relationships "
          "between constraint parameters and bidding coefficients.")
abs_block("2603.05134", "LBM: Hierarchical Large Auto-Bidding Model via Reasoning and Acting",
          "The growing scale of ad auctions on online advertising platforms has intensified competition, "
          "making manual bidding impractical and necessitating auto-bidding to help advertisers achieve "
          "their economic goals. Current auto-bidding methods have evolved to use offline reinforcement "
          "learning or generative methods to optimize bidding strategies, but they can sometimes behave "
          "counterintuitively due to the black-box training manner and limited mode coverage of datasets, "
          "leading to challenges in understanding task status and generalization in dynamic ad environments. "
          "Large language models (LLMs) offer a promising solution by leveraging prior human knowledge and "
          "reasoning abilities to improve auto-bidding performance. However, directly applying LLMs to "
          "auto-bidding faces difficulties due to the need for precise actions in competitive auctions and "
          "the lack of specialized auto-bidding knowledge, which can lead to hallucinations and suboptimal "
          "decisions. To address these challenges, we propose a hierarchical Large autoBidding Model (LBM) "
          "to leverage the reasoning capabilities of LLMs for developing a superior auto-bidding strategy. "
          "This includes a high-level LBM-Think model for reasoning and a low-level LBM-Act model for "
          "action-taking.")
abs_block("2502.05187", "An Adaptable Budget Planner for Enhancing Budget-Constrained Auto-Bidding in Online Advertising",
          "In online advertising, advertisers commonly utilize auto-bidding services to bid for impression "
          "opportunities. A typical objective of the auto-bidder is to optimize the advertiser's cumulative "
          "value of winning impressions within specified budget constraints. However, such a problem is "
          "challenging due to the complex bidding environment faced by diverse advertisers. To address this "
          "challenge, we introduce ABPlanner, a few-shot adaptable budget planner designed to improve "
          "budget-constrained auto-bidding. ABPlanner is based on a hierarchical bidding framework that "
          "decomposes the bidding process into shorter, manageable stages. Within this framework, ABPlanner "
          "allocates the budget across all stages, allowing a low-level auto-bidder to bids based on the "
          "budget allocation plan. The adaptability of ABPlanner is achieved through a sequential "
          "decision-making approach, inspired by in-context reinforcement learning. For each advertiser, "
          "ABPlanner adjusts the budget allocation plan episode by episode, using data from previous episodes "
          "as prompt for current decisions. This enables ABPlanner to quickly adapt to different advertisers "
          "with few-shot data, providing a sample-efficient solution.")
abs_block("2503.10304", "Large-Scale Auto-bidding with Nash Equilibrium Constraints",
          "Auto-bidding has become a cornerstone of modern online advertising platforms, enabling many "
          "advertisers to automate bidding at scale and optimize campaign performance. However, prevailing "
          "industrial systems rely on single-agent auto-bidding methods that are scalable but overlook the "
          "strategic interdependence among advertisers' bids, leading to unstable or suboptimal outcomes. "
          "While recent works recognize the game-theoretic nature of auto-bidding, existing approaches remain "
          "either computationally intractable at scale or lack a principled equilibrium-selection that aligns "
          "with platform-wide objectives. In this paper, we bridge this gap by introducing Nash "
          "Equilibrium-Constrained Bidding (NCB), a principled and scalable auto-bidding framework that "
          "recasts auto-bidding as a platform-wide optimization problem subject to Nash equilibrium "
          "constraints. This approach accounts for fine-grained strategic interdependencies among "
          "advertisers, ensuring both agent-level stability and ecosystem-level optimality. Notably, we "
          "develop a theoretically sound penalty-based primal-dual gradient method with rigorous convergence "
          "guarantees, supported by an efficient algorithm suitable for industrial deployment.")
abs_block("2304.13477", "Learning to Bid in Repeated First-Price Auctions with Budgets",
          "Budget management strategies in repeated auctions have received growing attention in online "
          "advertising markets. However, previous work on budget management in online bidding mainly focused "
          "on second-price auctions. The rapid shift from second-price auctions to first-price auctions for "
          "online ads in recent years has motivated the challenging question of how to bid in repeated "
          "first-price auctions while controlling budgets. In this work, we study the problem of learning in "
          "repeated first-price auctions with budgets. We design a dual-based algorithm that can achieve a "
          "near-optimal O(sqrt(T)) regret with full information feedback where the maximum competing bid is "
          "always revealed after each auction. We further consider the setting with one-sided information "
          "feedback where only the winning bid is revealed after each auction. We show that our modified "
          "algorithm can still achieve an O(sqrt(T)) regret with mild assumptions on the bidder's value "
          "distribution. Finally, we complement the theoretical results with numerical experiments to "
          "confirm the effectiveness of our budget management policy.")
abs_block("2604.03103", "Adaptive Bidding Policies for First-Price Auctions with Budget Constraints under Non-stationarity",
          "In this paper, we study how a budget-constrained bidder should learn to bid adaptively in repeated "
          "first-price auctions to maximize cumulative payoff. This problem arises from the recent "
          "industry-wide shift from second-price auctions to first-price auctions in display advertising, "
          "which renders truthful bidding suboptimal. We propose a simple dual-gradient-descent-based bidding "
          "policy that maintains a dual variable for the budget constraint as the bidder consumes the budget. "
          "We analyze two settings based on the bidder's knowledge of future private values: (i) an "
          "uninformative setting where all distributional knowledge (potentially non-stationary) is entirely "
          "unknown, and (ii) an informative setting where a prediction of budget allocation is available in "
          "advance. We characterize the performance loss (regret) relative to an optimal policy with complete "
          "information. For uninformative setting, we show that the regret is O(sqrt(T)) plus a "
          "Wasserstein-based variation term capturing non-stationarity, which is order-optimal. In the "
          "informative setting, the variation term can be eliminated using predictions, yielding a regret of "
          "O(sqrt(T)) plus the prediction error. Furthermore, we go beyond the existing literature by "
          "extending our analysis to a non-stationary setting.")
abs_block("2605.09448", "Learning to Bid with Unknown Private Values in Budget-Constrained First-Price Auctions",
          "We study the operational problem of automated bidding in repeated first-price auctions under "
          "budget and return-on-spend (RoS) constraints. In this setting, an auto-bidder must translate "
          "advertiser goals and constraints into real-time bids while learning two latent objects: the causal "
          "uplift value of each ad impression and the highest competing bid (HoB) needed to win it. We model "
          "uplift values and HoBs through a shared-context Linear Treatment Effect (LTE) structure and "
          "analyze both full-information and binary HoB feedback. We develop Dual-LTE, a dual-aware online "
          "learning framework that coordinates value estimation, HoB estimation, and budget/RoS control "
          "through confidence-guided exploration. We prove regret and constraint-violation guarantees that "
          "scale as O(sqrt(T)) under full-information HoB feedback and O(T^{2/3}) under binary win/loss "
          "feedback, where O(.) hides problem-dependent and logarithmic factors. Semi-synthetic experiments "
          "using real auction covariates show that Dual-LTE achieves lower regret than the baselines across "
          "budget and RoS settings, while illustrating the tradeoff between regret and constraint violation.")

h1("附录 B：检索与范围说明")
bullet("本批入库 18 篇（主题 bidding 12 篇 + auction 6 篇），检索与入库时间 2026-11-27；"
       "报告：2026-11-27/01-bidding.md（22 篇，含上一批 10 篇）与 2026-11-27/02-auction.md（6 篇）。")
bullet("与上一批的关系：上一批 PDF《广告竞价环境研究与出价优化》（bidding-environment-bid-optimization.pdf）"
       "覆盖环境研究的总体框架（机制、bid landscape、数据 vs 模拟、方法谱系）；本批聚焦\"强化学习系统\"："
       "可运行环境、系统级设计与理论保证算法，两篇文档互为补充。")
bullet("范围说明：以 2018-2026 的系统与算法工作为主；2004/2020 两篇（MARL 拍卖仿真、拍卖数据模拟）"
       "作为仿真方法奠基文献保留。")
bullet("开源仓库（非 arXiv 资源）：AuctionNet 官方仓库 https://github.com/alimama-tech/AuctionNet ；"
       "AuctionGym https://github.com/amzn/auction-gym （KDD 2023，未收录 arXiv）；"
       "SCOPE-RL（含 RTBGym）https://github.com/hakuhodo-technologies/scope-rl 。")
bullet("与论文库的对应：01-bidding.md 收录 bidding 主题 22 篇（上一批 10 篇 + 本批 12 篇），"
       "02-auction.md 收录 auction 主题 6 篇；两份报告的 Markdown 与 PDF 均随本仓库推送 GitHub。")

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=18 * mm, rightMargin=18 * mm,
    topMargin=16 * mm, bottomMargin=18 * mm,
    title="竞价强化学习系统深度调研",
    author="Binks",
    subject="RL bidding systems / auction environments / auto-bidding",
)
doc.build(story, canvasmaker=NumberedCanvas)
print(f"PDF written: {OUT}")
