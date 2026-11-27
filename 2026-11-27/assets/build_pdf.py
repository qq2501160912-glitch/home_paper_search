#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建《广告竞价环境研究与出价优化》PDF（reportlab + STSong-Light CID 字体）。

依赖: reportlab（venv: /home/admin/.venv-pdf）
字体: 内建 CID 字体 STSong-Light（不嵌入字体文件，查看器自动替换，文本可提取/搜索/复制）
输出: 2026-11-27/bidding-environment-bid-optimization.pdf
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
OUT = os.path.join(BASE, "bidding-environment-bid-optimization.pdf")

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
    """页脚页码（第 X 页 / 共 N 页）+ 非首页页眉。"""

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
                                 "广告竞价环境研究与出价优化 · 研究内容整理（2026-11-27）")
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
S_CELL = style("cell", fontSize=9, leading=12.5, spaceAfter=0)
S_CELLB = style("cellb", fontSize=9, leading=12.5, textColor=BLUE, spaceAfter=0)
S_CELLH = style("cellh", fontSize=9.5, leading=13, textColor=NAVY, alignment=TA_CENTER,
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


def cmp_table(header_cells, rows):
    data = [[Paragraph(escape(c), S_CELLH) for c in header_cells]]
    for label, c1, c2 in rows:
        data.append([Paragraph(escape(label), S_CELLB),
                     Paragraph(escape(c1), S_CELL),
                     Paragraph(escape(c2), S_CELL)])
    t = Table(data, colWidths=[26 * mm, 71 * mm, 71 * mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f9fc")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 4 * mm))


# ============================ 封面标题 ============================
story.append(Paragraph("广告竞价环境研究与出价优化", S_TITLE))
story.append(Paragraph("研究内容整理：环境建模 · 数据集 · 竞价模拟 · 出价策略 · 研究计划", S_SUB))
small("基于 arXiv 检索批次（主题：bidding，共 10 篇，检索与整理时间 2026-11-27）"
      " · 报告原文见 2026-11-27/01-bidding.md")
story.append(Spacer(1, 3 * mm))

p("目标：作为出价方（广告主 / DSP），要对\"竞价环境\"进行研究并优化自身出价。"
  "\"竞价环境\"由拍卖规则、市场价分布、竞争对手行为与平台策略共同构成；"
  "可依据的材料主要有两类：广告平台（或第三方）公开的竞价日志数据集，"
  "以及自建或沿用论文方案的竞价模拟环境。"
  "本整理按\"环境研究的核心对象 - 数据路线 - 模拟路线 - 出价优化方法谱系 - 路线对比与选择 - "
  "研究计划\"展开，全部要点均对应到文末清单中的 10 篇论文（3 篇 2014-2019 年经典奠基文献 + 7 篇近两年工作），"
  "附录收录论文原文摘要与检索说明。")

# ============================ 1 环境研究的核心对象 ============================
h1("1. 竞价环境研究的核心对象")

h2("1.1 拍卖机制与规则")
bullet("二价拍卖与 GSP：历史上程序化广告的主流结算方式是二价（second-price）拍卖——"
       "竞得者支付次高价格。二价机制下研究者只能观测到成交价，低于成交价的市场价部分被截断（censorship），"
       "这是环境建模的核心难点之一 [P2]。")
bullet("一价（first-price）转型：一价拍卖近年成为行业主流（\"目前大多数广告机会的拍卖都是一价类型\" [P9]）。"
       "一价下\"出价即成交价\"，高估价值直接带来过度支付，因此需要出价矫正（bid shading）[P9]。")
bullet("保留价、排序与质量分：平台参数（保留价、广告质量得分等）会改变实际结算价格；"
       "平台可能\"无承诺\"（缺乏 commitment）——在观察到竞价者出价后重设规则（例如调整保留价），"
       "这反过来改变竞价者的最优策略选择 [P4]。")
bullet("auto-bidding 时代：广告主不再逐次手工出价，而是把高层约束（预算、tCPA/tROAS 目标）交给自动出价系统，"
       "由系统在每次竞价上决策 [P4][P7]。研究环境时既要研究对手，也要研究平台规则演化的动机。")

h2("1.2 市场价分布与出价景观（bid landscape）")
bullet("定义：对每个广告曝光机会，预测市场价（成交价 / 竞争者最高出价）的概率分布，"
       "即\"出多少价、有多大胜率\"的曲线 [P2][P9]。")
bullet("三种用途：(a) 二价下按真实价值出价的最优性论证依赖它；(b) 一价下 bid shading 需要"
       "\"竞争者最高出价分布\"（competitive landscape）来平衡胜率与支出 [P9]；"
       "(c) 平台直接向广告主展示 bid landscape，作为出价决策的输入 [P10]。")
bullet("深度建模方法：DLF（KDD 2019）用 RNN 学习条件胜出概率，再经概率链式法则推出完整市场价分布，"
       "不做分布形式的先验假设；并用生存分析处理二价截断问题 [P2]。")
bullet("鲁棒处理：当价值估计与竞争景观估计都噪声较大时，用 KL 模糊集上的 max-min "
       "双重分布鲁棒（Double DRO）优化来设计 bid shading 策略 [P9]。")

h2("1.3 竞争动力学与多智能体交互")
bullet("对手并非静止：所有广告主（智能体）都在预算与 KPI 约束下动态调整出价，共同构成竞争环境。"
       "图表示 + 规划式潜在扩散模型（latent graph diffusion）可用于对大规模竞价环境建模，"
       "并预测竞价结果 [P6]。")
bullet("竞争形态分类（PlatformBid 基准）：同质竞争（各家算法相同）、异质竞争（算法策略多样）、"
       "促销竞争（大促期间部分广告主预算激增）[P8]。")
bullet("战略层博弈：广告主对\"平台是否有承诺\"的信念会影响其选择 tCPA 还是 mCPA 出价模式；"
       "在 tCPA 模式下平台收入反而可能更高 [P4]。")

h2("1.4 观测数据的偏差与截断（研究环境必须处理的统计问题）")
bullet("二价截断：只观测到成交价（次高价），低于它的市场价密度缺失，需用生存分析 / 删失建模补齐 [P2]。")
bullet("胜者偏差与选择偏差：只能观测到自己赢得的曝光及其点击、转化；"
       "\"如果出别的价会怎样\"的反事实不可见，需要离线评估协议与模拟器补齐 [P1][P7]。")
bullet("竞价日志字段（以 iPinYou 为例）：竞拍、出价、曝光、点击、最终转化，"
       "构成从市场环境到用户反馈的完整链路 [P1]。")

# ============================ 2 数据路线 ============================
h1("2. 路线 A：基于平台竞价数据集的研究")

h2("2.1 公开数据集现状")
bullet("iPinYou（品友）：2013 年全球 RTB 算法竞赛公开的数据集，是首个公开的 RTB 展示广告数据集；"
       "包含竞拍日志、出价、曝光、点击与转化，可直接支持出价优化与 CTR 估计研究 [P1]。"
       "注意：该数据为二价时代、中国展示广告流量，直接复用于一价场景需要改造。")
bullet("工业内部数据：阿里巴巴（在线 A/B，GMV +2.81%、ROI +3.36% [P5]）、Yahoo DSP（一价真实数据 [P9]）、"
       "快手（在线实验，target cost 改善 +0.68% [P8]）——多数前沿工作在平台内部数据上验证，"
       "公开可复现性有限，需留意结论的外部有效性。")

h2("2.2 数据路线需要研究的内容")
bullet("竞价日志解析与特征工程：上下文特征、时段、预算余量、历史胜率等——RL 状态空间设计可参考 [P3]。")
bullet("市场价分布估计（bid landscape）[P2] 与价值估计（CTR/CVR 模型）。")
bullet("离线评估协议：如何用历史日志公平比较不同出价策略（iPinYou 论文给出简单而全面的评估协议 [P1]）。")
bullet("局限：日志只覆盖\"被记录策略\"到访过的状态空间，无法回答未探索出价的反事实问题，"
       "这是模拟路线存在的原因 [P7]。")

# ============================ 3 模拟路线 ============================
h1("3. 路线 B：基于竞价模拟的研究")

h2("3.1 三种模拟层次（由简到实）")
bullet("SRLB（Simulation-based RL Bidding）：规则化的离线模拟器。状态覆盖广、成本低，"
       "但模拟与真实的差距（sim2real gap）可能误导策略 [P7]。")
bullet("MRLB（Model-based RL Bidding）：从真实竞价数据学习环境模型，再用\"真实 + 模型生成\"数据训练策略，"
       "是前两者的折中。论文给出排列等变（permutation equivariant）模型架构与悲观鲁棒离线 Q-learning"
       "（PE-MORL 算法），真实实验优于 SOTA [P7]。")
bullet("环境级生成建模：用图表示 + 潜在扩散模型建模大规模竞价环境并预测竞价结果，"
       "在真实与合成竞价环境上均有效 [P6]。")

h2("3.2 平台视角的模拟基准")
p("PlatformBid 是首个\"统一广告平台\"视角的 auto-bidding 基准：把 SSP、DSP、Ad Exchange 一体化，"
  "优化目标同时包含广告主转化与平台收入；提供同质 / 异质 / 促销三种竞争设定，"
  "系统评估控制类、RL 类、生成式方法，并给出离线-在线一致性证据（快手在线 +0.68%）[P8]。")

h2("3.3 模拟路线需要研究的内容")
bullet("对手模型：其他竞价者的出价分布与策略学习 [P6][P8]。")
bullet("校准：用真实日志校准模拟器参数，量化 sim2real 差距 [P7]。")
bullet("评估可信度：模拟器上的提升能否迁移到在线（离线-在线一致性）[P8]。")

# ============================ 4 出价优化谱系 ============================
h1("4. 出价优化方法谱系")

h2("4.1 经典强化学习出价（2017 基线，WSDM 2017）")
p("把出价决策形式化为 MDP：状态 = 拍卖信息 + 预算等实时 campaign 参数；动作 = 出价；"
  "以拍卖竞争建模状态转移；用神经网络近似价值函数解决大规模问题 [P3]。"
  "这是后续绝大多数 RL 出价工作的框架起点。")

h2("4.2 生成式（扩散）出价（2024-2025 主线）")
bullet("AIGB / DiffBid：条件扩散直接建模\"回报 - 整条轨迹\"的相关性，规避 MDP 马尔可夫假设与长期误差传播；"
       "可在约束下生成最大化目标的轨迹；阿里在线 A/B：GMV +2.81%、ROI +3.36% [P5]。")
bullet("多智能体图扩散：规划式潜在扩散模型 + 图嵌入，reward alignment 微调后验，"
       "生成满足 KPI 约束的出价轨迹 [P6]。")

h2("4.3 一价拍卖的出价矫正（bid shading）")
p("一价下把估计价值直接当出价会显著过度支付。bid shading 在价值估计与竞争景观上做折价；"
  "双重分布鲁棒（Double DRO）max-min 策略在两类估计都存在 KL 模糊集误差时仍稳健，"
  "Yahoo DSP 真实数据上系统性优于非鲁棒对照 [P9]。")

h2("4.4 LLM 智能体出价（2026 前沿，工程陷阱多）")
bullet("设定：平台向推理模型展示 bid landscape（各候选出价的胜率曲线）并让其选价；"
       "论文在 eBay 成交价与 AuctionNet 模拟市场上评估 6 个 4B-14B 开源推理模型 [P10]。")
bullet("模型自身的两类失败：即使自己推理轨迹（trace）里已把最优项排第一，仍会跳过它；"
       "错误答案系统性偏向\"最高出价\"选项 [P10]。")
bullet("算子设置造成的损失：token 上限截断推理轨迹（允许自停时，5 个模型恢复计算器领先的 91-100%）；"
       "推理块未关闭就读答案会误读（关闭后最弱模型 eBay 上 42% -> 84%，AuctionNet 上 24% -> 81%）[P10]。")
bullet("审计兜底：把与轨迹数字不一致的出价覆盖为精确计算器的出价，"
       "768 强制 token 下恢复份额从 42-85% 提升到 84-100% [P10]。")
bullet("启示：若用 LLM 出价，应把\"精确计算器\"作为下限对照与审计器，而不是直接信任模型输出。")

h2("4.5 战略层：出价模式选择（tCPA vs mCPA）")
p("拍卖理论视角：平台无承诺时 tCPA 对广告主是更优选择（存在可信均衡，mCPA 不存在），"
  "且平台收入在 tCPA 下也可能更高；\"承诺能力\"本身具有可量化的价值 [P4]。"
  "这提示：环境研究不能只研究对手，还要研究平台规则演化的动机。")

# ============================ 5 路线对比 ============================
h1("5. 路线对比与选择")
cmp_table(
    ["维度", "平台竞价数据集", "竞价模拟"],
    [
        ("数据来源", "真实竞价日志（公开：iPinYou；工业内部：阿里 / Yahoo DSP / 快手等）",
         "规则化仿真，或从日志学习的生成式环境模型"),
        ("真实性", "高，但仅覆盖历史策略到访过的状态空间", "中-高；可合成任意状态，依赖模型质量"),
        ("反事实能力", "弱：未尝试过的出价无记录", "强：可任意探索（SRLB / MRLB）"),
        ("数据偏差", "二价截断、胜者偏差、策略相关性", "对手模型与市场价分布失真（sim2real gap）"),
        ("成本与门槛", "低（公开数据可直接开始）", "中（需构建 + 校准 + 可信度验证）"),
        ("代表工作", "[P1] [P2] [P9]", "[P6] [P7] [P8]"),
    ],
)
p("结论：推荐\"以数据为主、以模拟为辅\"——用真实数据估计价值与市场价分布，"
  "用 MRLB 方式从数据学习环境模型以扩展状态覆盖，用 PlatformBid 类基准做离线评估，"
  "最后以小流量在线 A/B 验证 [P1][P2][P7][P8]。")

# ============================ 6 研究计划 ============================
h1("6. 建议研究计划（分阶段）")
bullet("阶段 1 环境理解（1-2 周）：解析公开竞价日志（iPinYou 起步），实现市场价分布估计与 bid landscape "
       "可视化 [P1][P2]；明确目标平台的拍卖类型（一价 / 二价）与结算规则 [P4][P9]。")
bullet("阶段 2 模拟器构建（2-4 周）：先做规则化 SRLB 验证策略逻辑；再从日志学习环境模型"
       "（MRLB / PE-MORL 思路：排列等变结构 + 悲观惩罚控制模型误差）[P7]；"
       "参考 PlatformBid 构建同质 / 异质 / 促销竞争场景 [P8]。")
bullet("阶段 3 策略研发与离线评估（持续）：基线 = 经典 RL（MDP 框架 [P3]）+ 约束优化（预算 / CPA）；"
       "进阶 = 生成式出价（AIGB [P5]、图扩散 [P6]）；一价场景 = 分布鲁棒 bid shading [P9]；"
       "按离线协议对比，并做离线-在线一致性检查 [P1][P8]。")
bullet("阶段 4 在线验证（按条件）：小流量 A/B；若采用 LLM 出价，加\"计算器审计\"兜底 [P10]。")
bullet("产出建议：每阶段产出一份可复现脚本 + 评估报告；"
       "本库 2026-11-06 的《主流广告平台与竞价市场博弈综述（DSP/UAC）》及其 roi_bidding_sim.py "
       "五个确定性仿真可作为阶段 2 的起点。")

# ============================ 7 论文清单 ============================
h1("7. 论文清单（10 篇，标题与链接可点击）")
paper_block("1407.7073", "Real-Time Bidding Benchmarking with iPinYou Dataset",
            "cs.GT", "2014-07-25", "UCL Technical Report 2014",
            "首个公开 RTB 展示广告数据集（iPinYou 2013 竞赛）：竞拍 / 出价 / 曝光 / 点击 / 转化日志；"
            "给出统计分析与出价优化评估协议——数据路线的起点与评估方法参照。")
paper_block("1905.03028", "Deep Landscape Forecasting for Real-time Bidding Advertising",
            "cs.IR", "2019-05-07", "KDD 2019",
            "RNN + 生存分析处理二价截断，无分布假设地预测市场价概率分布（bid landscape），"
            "两个大规模真实数据集上超越既有方法——环境建模核心。")
paper_block("1701.02490", "Real-Time Bidding by Reinforcement Learning in Display Advertising",
            "cs.LG", "2017-01-10", "WSDM 2017",
            "出价决策形式化为 MDP（状态 = 拍卖信息 + 预算等；动作 = 出价），以拍卖竞争建模状态转移，"
            "神经网络近似价值函数——经典 RL 出价框架，后续工作的起点。")
paper_block("2301.07312", "Auctions without commitment in the auto-bidding world",
            "econ.TH", "2023-01-18", "",
            "拍卖理论视角：平台无承诺时 tCPA 对广告主更优且存在可信均衡，平台收入也可能更高——"
            "研究环境必须考虑平台规则演化的动机。")
paper_block("2405.16141", "AIGB: Generative Auto-bidding via Conditional Diffusion Modeling",
            "cs.LG", "2024-05-25", "KDD 2024",
            "DiffBid 条件扩散直接建模回报与整条轨迹的相关性，规避 MDP 假设与长期误差传播；"
            "阿里在线 A/B：GMV +2.81%、ROI +3.36%。")
paper_block("2503.05805", "Multi-agent Auto-Bidding with Latent Graph Diffusion Models",
            "cs.LG", "2025-03-04", "",
            "图表示 + 规划式潜在扩散模型对大规模竞价环境建模，生成满足 KPI 约束的出价轨迹并预测竞价结果——"
            "模拟路线的环境级建模方法。")
paper_block("2506.17919", "Permutation Equivariant Model-based Offline Reinforcement Learning for Auto-bidding",
            "cs.LG", "2025-06-22", "",
            "厘清 SRLB（模拟 RL）与 ORLB（离线 RL）的取舍：ORLB 状态覆盖有限、SRLB 有 sim2real 差距；"
            "提出从真实数据学环境模型的 MRLB / PE-MORL，真实实验优于 SOTA——\"数据 + 模拟结合\"的直接方案。")
paper_block("2607.27265", "PlatformBid: An Auto-Bidding Benchmark from a Unified Advertising Platform's Perspective",
            "cs.LG", "2026-07-29", "",
            "首个统一广告平台视角基准：SSP / DSP / Exchange 一体化，目标含平台收入；"
            "同质 / 异质 / 促销三种竞争设定；快手在线 +0.68% target cost，给出离线-在线一致性证据。")
paper_block("2410.14864", "Double Distributionally Robust Bid Shading for First Price Auctions",
            "cs.GT", "2024-10-18", "",
            "一价拍卖下对\"价值估计\"与\"竞争景观估计\"同时做 KL 模糊集 max-min 鲁棒 bid shading；"
            "Yahoo DSP 真实数据上系统性优于非鲁棒对照——一价环境的出价矫正模板。")
paper_block("2611.34068", "Budget, Readout or Reasoning? Where Small Reasoning Models Lose Value in Auction Bidding",
            "cs.AI", "2026-11-25", "代码与数据: github.com/DataismLab/bid-reasoning",
            "给 6 个 4B-14B 开源推理模型展示 bid landscape 让其选价：模型自身错误（跳过最优、偏向最高出价）"
            "与算子设置（token 上限、推理块未关闭）是主要损失来源；计算器审计可恢复大部分价值——"
            "LLM 出价必须带兜底。")

# ============================ 8 附录 ============================
story.append(PageBreak())
h1("附录 A：论文摘要（原文，英文）")
abs_block("1407.7073", "Real-Time Bidding Benchmarking with iPinYou Dataset",
          "Being an emerging paradigm for display advertising, Real-Time Bidding (RTB) drives the focus "
          "of the bidding strategy from context to users' interest by computing a bid for each impression "
          "in real time. The data mining work and particularly the bidding strategy development becomes "
          "crucial in this performance-driven business. However, researchers in computational advertising "
          "area have been suffering from lack of publicly available benchmark datasets, which are essential "
          "to compare different algorithms and systems. Fortunately, a leading Chinese advertising technology "
          "company iPinYou decided to release the dataset used in its global RTB algorithm competition in "
          "2013. The dataset includes logs of ad auctions, bids, impressions, clicks, and final conversions. "
          "These logs reflect the market environment as well as form a complete path of users' responses "
          "from advertisers' perspective. This dataset directly supports the experiments of some important "
          "research problems such as bid optimisation and CTR estimation. To the best of our knowledge, this "
          "is the first publicly available dataset on RTB display advertising. Thus, they are valuable for "
          "reproducible research and understanding the whole RTB ecosystem. In this paper, we first provide "
          "the detailed statistical analysis of this dataset. Then we introduce the research problem of bid "
          "optimisation in RTB and the simple yet comprehensive evaluation protocol. Besides, a series of "
          "benchmark experiments are also conducted, including both click-through rate (CTR) estimation and "
          "bid optimisation.")
abs_block("1905.03028", "Deep Landscape Forecasting for Real-time Bidding Advertising",
          "The emergence of real-time auction in online advertising has drawn huge attention of modeling the "
          "market competition, i.e., bid landscape forecasting. The problem is formulated as to forecast the "
          "probability distribution of market price for each ad auction. With the consideration of the "
          "censorship issue which is caused by the second-price auction mechanism, many researchers have "
          "devoted their efforts on bid landscape forecasting by incorporating survival analysis from medical "
          "research field. However, most existing solutions mainly focus on either counting-based statistics "
          "of the segmented sample clusters, or learning a parameterized model based on some heuristic "
          "assumptions of distribution forms. Moreover, they neither consider the sequential patterns of the "
          "feature over the price space. In order to capture more sophisticated yet flexible patterns at "
          "fine-grained level of the data, we propose a Deep Landscape Forecasting (DLF) model which combines "
          "deep learning for probability distribution forecasting and survival analysis for censorship "
          "handling. Specifically, we utilize a recurrent neural network to flexibly model the conditional "
          "winning probability w.r.t. each bid price. Then we conduct the bid landscape forecasting through "
          "probability chain rule with strict mathematical derivations. And, in an end-to-end manner, we "
          "optimize the model by minimizing two negative likelihood losses with comprehensive motivations. "
          "Without any specific assumption for the distribution form of bid landscape, our model shows great "
          "advantages over previous works on fitting various sophisticated market price distributions. In the "
          "experiments over two large-scale real-world datasets, our model significantly outperforms the "
          "state-of-the-art solutions under various metrics.")
abs_block("1701.02490", "Real-Time Bidding by Reinforcement Learning in Display Advertising",
          "The majority of online display ads are served through real-time bidding (RTB) --- each ad display "
          "impression is auctioned off in real-time when it is just being generated from a user visit. To "
          "place an ad automatically and optimally, it is critical for advertisers to devise a learning "
          "algorithm to cleverly bid an ad impression in real-time. Most previous works consider the bid "
          "decision as a static optimization problem of either treating the value of each impression "
          "independently or setting a bid price to each segment of ad volume. However, the bidding for a "
          "given ad campaign would repeatedly happen during its life span before the budget runs out. As "
          "such, each bid is strategically correlated by the constrained budget and the overall effectiveness "
          "of the campaign (e.g., the rewards from generated clicks), which is only observed after the "
          "campaign has completed. Thus, it is of great interest to devise an optimal bidding strategy "
          "sequentially so that the campaign budget can be dynamically allocated across all the available "
          "impressions on the basis of both the immediate and future rewards. In this paper, we formulate the "
          "bid decision process as a reinforcement learning problem, where the state space is represented by "
          "the auction information and the campaign's real-time parameters, while an action is the bid price "
          "to set. By modeling the state transition via auction competition, we build a Markov Decision "
          "Process framework for learning the optimal bidding policy to optimize the advertising performance "
          "in the dynamic real-time bidding environment. Furthermore, the scalability problem from the large "
          "real-world auction volume and campaign budget is well handled by state value approximation using "
          "neural networks.")
abs_block("2301.07312", "Auctions without commitment in the auto-bidding world",
          "Advertisers in online ad auctions are increasingly using auto-bidding mechanisms to bid into "
          "auctions instead of directly bidding their value manually. One prominent auto-bidding format is "
          "the target cost-per-acquisition (tCPA) which maximizes the volume of conversions subject to a "
          "return-of-investment constraint. From an auction theoretic perspective however, this trend seems "
          "to go against foundational results that postulate that for profit-maximizing bidders, it is "
          "optimal to use a classic bidding system like marginal CPA (mCPA) bidding rather than using "
          "strategies like tCPA. In this paper we rationalize the adoption of such seemingly sub-optimal "
          "bidding within the canonical quasi-linear framework. The crux of the argument lies in the notion "
          "of commitment. We consider a multi-stage game where first the auctioneer declares the auction "
          "rules; then bidders select either the tCPA or mCPA bidding format and then, if the auctioneer "
          "lacks commitment, it can revisit the rules of the auction (e.g., may readjust reserve prices "
          "depending on the observed bids). Our main result is that so long as a bidder believes that the "
          "auctioneer lacks commitment to follow the rule of the declared auction then the bidder will make "
          "a higher profit by choosing the tCPA format over the mCPA format. We then explore the commitment "
          "consequences for the auctioneer. In a simplified version of the model where there is only one "
          "bidder, we show that the tCPA subgame admits a credible equilibrium while the mCPA format does "
          "not. That is, when the bidder chooses the tCPA format the auctioneer can credibly implement the "
          "auction rules announced at the beginning of the game. We also show that, under some mild "
          "conditions, the auctioneer's revenue is larger when the bidder uses the tCPA format rather than "
          "mCPA. We further quantify the value for the auctioneer to be able to commit to the declared "
          "auction rules.")
abs_block("2405.16141", "AIGB: Generative Auto-bidding via Conditional Diffusion Modeling",
          "Auto-bidding plays a crucial role in facilitating online advertising by automatically providing "
          "bids for advertisers. Reinforcement learning (RL) has gained popularity for auto-bidding. However, "
          "most current RL auto-bidding methods are modeled through the Markovian Decision Process (MDP), "
          "which assumes the Markovian state transition. This assumption restricts the ability to perform in "
          "long horizon scenarios and makes the model unstable when dealing with highly random online "
          "advertising environments. To tackle this issue, this paper introduces AI-Generated Bidding (AIGB), "
          "a novel paradigm for auto-bidding through generative modeling. In this paradigm, we propose "
          "DiffBid, a conditional diffusion modeling approach for bid generation. DiffBid directly models the "
          "correlation between the return and the entire trajectory, effectively avoiding error propagation "
          "across time steps in long horizons. Additionally, DiffBid offers a versatile approach for "
          "generating trajectories that maximize given targets while adhering to specific constraints. "
          "Extensive experiments conducted on the real-world dataset and online A/B test on Alibaba "
          "advertising platform demonstrate the effectiveness of DiffBid, achieving 2.81% increase in GMV and "
          "3.36% increase in ROI.")
abs_block("2503.05805", "Multi-agent Auto-Bidding with Latent Graph Diffusion Models",
          "This paper proposes a diffusion-based auto-bidding framework that leverages graph representations "
          "to model large-scale auction environments. In such settings, agents must dynamically optimize "
          "bidding strategies under constraints defined by key performance indicator (KPI) metrics, all while "
          "operating in competitive environments characterized by uncertain, sparse, and stochastic "
          "variables. To address these challenges, we introduce a novel approach combining learnable "
          "graph-based embeddings with a planning-based latent diffusion model (LDM). By capturing patterns "
          "and nuances underlying the interdependence of impression opportunities and the multi-agent "
          "dynamics of the auction environment, the graph representation enable expressive computations "
          "regarding auto-bidding outcomes. With reward alignment techniques, the LDM's posterior is "
          "fine-tuned to generate auto-bidding trajectories that maximize KPI metrics while satisfying "
          "constraint thresholds. Empirical evaluations on both real-world and synthetic auction environments "
          "demonstrate significant improvements in auto-bidding performance across multiple common KPI "
          "metrics, as well as accuracy in forecasting auction outcomes.")
abs_block("2506.17919", "Permutation Equivariant Model-based Offline Reinforcement Learning for Auto-bidding",
          "Reinforcement learning (RL) for auto-bidding has shifted from using simplistic offline simulators "
          "(Simulation-based RL Bidding, SRLB) to offline RL on fixed real datasets (Offline RL Bidding, "
          "ORLB). However, ORLB policies are limited by the dataset's state space coverage, offering modest "
          "gains. While SRLB expands state coverage, its simulator-reality gap risks misleading policies. "
          "This paper introduces Model-based RL Bidding (MRLB), which learns an environment model from real "
          "data to bridge this gap. MRLB trains policies using both real and model-generated data, expanding "
          "state coverage beyond ORLB. To ensure model reliability, we propose: 1) A permutation equivariant "
          "model architecture for better generalization, and 2) A robust offline Q-learning method that "
          "pessimistically penalizes model errors. These form the Permutation Equivariant Model-based Offline "
          "RL (PE-MORL) algorithm. Real-world experiments show that PE-MORL outperforms state-of-the-art "
          "auto-bidding methods.")
abs_block("2607.27265", "PlatformBid: An Auto-Bidding Benchmark from a Unified Advertising Platform's Perspective",
          "Real-time bidding is central to computational advertising, comprising three elements: Supply Side "
          "Platform (SSP) selling ad impressions, Demand Side Platform (DSP) bidding for advertisers, and Ad "
          "Exchange conducting auctions between them. Traditional auto-bidding algorithms focus solely on the "
          "DSP side, maximizing advertiser conversions by adjusting bids against competitors. However, "
          "current big ad platforms, such as social media and e-commerce companies, now integrate SSP, DSP, "
          "and Ad Exchange functions internally. From such ad platforms' perspective, the goal of the "
          "auto-bidding algorithms is not only to maximize the advertisers' conversions, but also the total "
          "revenue of the platform. Given the lack of platform-centric evaluation frameworks and the pressing "
          "need to advance auto-bidding research, we propose PlatformBid - the first comprehensive benchmark "
          "designed from a unified ad platform's perspective. To accurately reflect the real-world "
          "auto-bidding scenarios, we define three representative settings: (1) homogeneous competition with "
          "identical algorithms across advertisers, (2) heterogeneous competition with diverse algorithmic "
          "strategies, and (3) promotional competition where some advertisers surge budgets for boosting sales "
          "during promotional events like Black Friday. We systematically evaluate a broad spectrum of "
          "existing auto-bidding methods across these settings, encompassing classical control methods, "
          "RL-based methods, and recent generative methods. Besides these methods, we further propose a novel "
          "auto-bidding method based on flow-matching, termed BidFlow, which leverages the flow-matching "
          "method's expressive policy representation to effectively handle dynamic competitive environments. "
          "Online experiments on Kuaishou further show a +0.68% improvement in target cost, providing "
          "deployment evidence for the offline-online consistency of PlatformBid.")
abs_block("2410.14864", "Double Distributionally Robust Bid Shading for First Price Auctions",
          "Bid shading has become a standard practice in the digital advertising industry, in which most "
          "auctions for advertising (ad) opportunities are now of first price type. Given an ad opportunity, "
          "performing bid shading requires estimating not only the value of the opportunity but also the "
          "distribution of the highest bid from competitors (i.e. the competitive landscape). Since these two "
          "estimates tend to be very noisy in practice, first-price auction participants need a bid shading "
          "policy that is robust against relatively significant estimation errors. In this work, we provide a "
          "max-min formulation in which we maximize the surplus against an adversary that chooses a "
          "distribution both for the value and the competitive landscape, each from a Kullback-Leibler-based "
          "ambiguity set. As we demonstrate, the two ambiguity sets are essential to adjusting the shape of "
          "the bid-shading policy in a principled way so as to effectively cope with uncertainty. Our "
          "distributionally robust bid shading policy is efficient to compute and systematically outperforms "
          "its non-robust counterpart on real datasets provided by Yahoo DSP.")
abs_block("2611.34068", "Budget, Readout or Reasoning? Where Small Reasoning Models Lose Value in Auction Bidding",
          "Ad platforms and marketplaces show bidders a bid landscape, the estimated chance of winning at "
          "each candidate bid, and increasingly let agents built on reasoning language models choose the "
          "bid. We give six open reasoning models of 4B to 14B parameters such landscapes, with win curves "
          "from eBay closing prices and from a simulated advertising market (AuctionNet), and score their "
          "bids on held-out auctions against an exact calculator. Because the agent is handed the estimates, "
          "the lost value can be split by cause. Two failures belong to the models. They pass over the best "
          "option even when the values written in their own trace already rank it first, and their wrong "
          "answers lean toward the highest bid on the menu. The lean is about the bid's size, not its place "
          "in the list, and it survives sampling. At 768 forced tokens on eBay, under pay-your-bid pricing, "
          "the wrong answers cost bidders 7-17% of the surplus the calculator's bids earn. Arithmetic errors "
          "are rare. Two further losses come from operator choices. A token cap cuts traces short: allowed to "
          "stop on their own within 4,096 tokens, five models recover 91-100% of the calculator's lead over a "
          "model that does no reasoning. Asking for the answer while the reasoning block is still open "
          "misreads it: closing the block first lifts the weakest model from 42% to 84% on eBay and from 24% "
          "to 81% on AuctionNet. Finally, an audit that flags bids disagreeing with the trace's own numbers, "
          "and overrides them with the calculator's bid, raises the share of the calculator's lead recovered "
          "at 768 forced tokens from 42-85% to 84-100% on eBay under nested cross-validation, and the same "
          "reader settings transfer from eBay to AuctionNet.")

h1("附录 B：检索与范围说明")
bullet("检索主题：bidding（单主题词，要求标题命中）；检索与入库时间 2026-11-27；"
       "检索词覆盖 real-time bidding / auto-bidding / bid landscape / auction simulator；"
       "共入库 10 篇，Markdown 报告：2026-11-27/01-bidding.md。")
bullet("范围说明：以近 3 年工作为主；3 篇 2014 / 2017 / 2019 年的论文（iPinYou 数据集、RL 出价框架、"
       "深度出价景观预测）作为数据集与 RL 框架的奠基文献保留。")
bullet("未纳入说明：AuctionGym（KDD 2023，Jeunen 等）经核实未收录于 arXiv，本批无法入库；"
       "AuctionNet（arXiv 2412.10798，大规模博弈决策基准，含广告竞价博弈）与本主题高度相关，"
       "但标题不含 bidding，未通过单主题词核对，列为延伸阅读。")
bullet_rich("延伸阅读：AuctionNet，" + link("https://arxiv.org/abs/2412.10798") + " ；DLF 代码与数据集，"
       + link("https://github.com/rk2900/DLF") + " （见 P2 备注）；P10 代码与数据，"
       + link("https://github.com/DataismLab/bid-reasoning") + " 。")
bullet("本库关联：2026-11-06 文件夹已有《主流广告平台与竞价市场博弈综述（DSP/UAC）》PDF "
       "与 roi_bidding_sim.py（五个确定性仿真，仅依赖 numpy），可作为阶段 2 模拟器构建的起点。")

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=18 * mm, rightMargin=18 * mm,
    topMargin=16 * mm, bottomMargin=18 * mm,
    title="广告竞价环境研究与出价优化：研究内容整理",
    author="Binks",
    subject="bidding / ad auction environment / bid optimization",
)
doc.build(story, canvasmaker=NumberedCanvas)
print(f"PDF written: {OUT}")
