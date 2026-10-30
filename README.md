# home_paper_search

个人 arXiv 论文阅读记录与专题研究综述库，由本地 `arxiv-paper-log` skill 生成并同步。

## 目录结构

```
home_paper_search/
  2026-10-23/
    01-diffusion-policy.md          # <两位序号>-<主题>.md
    08-large-language-model.md      # 一次检索/保存批次的论文表 + 摘要
    ...                             # 同目录下另有 transformer、推荐、MIMO 等批次
  2026-10-25/
    00-reinforcement-learning-survey.md   # 专题综述（Markdown 摘要）
    errata.md                             # 该综述的审读勘误
    assets/
      reinforcement-learning-survey.pdf   # 全文 PDF
  2026-10-26/
    00-dsp-bidding-algorithms.md          # 广告 DSP 出价算法综述
    01-bid-shading.md                     # 论文批次：一价下出价折扣
    02-auto-bidding.md                    # 论文批次：自动出价
    03-conversion-rate-prediction.md      # 论文批次：CVR 预估
    04-ctr-prediction.md                  # 论文批次：CTR 预估
    05-rtb-buy-side-survey.md             # 实时竞价（RTB）买入侧全链路综述
    assets/
      dsp-bidding-algorithms.pdf
      rtb-buy-side-survey.pdf|.docx       # 买入侧综述全文（Markdown 版另附）
      rtb_sim.py                          # 该综述的四组仿真脚本
  2026-10-30/
    00-dsp-bidding-response-strategy.md   # DSP 竞价应对策略：反馈调整、控制闭环与落地路径
    assets/
      bid_strategy_toolkit.py             # 该报告的完整可运行实现（删失估计/折价/控制器 + 五个实验）
      make_figures.py                     # 图表生成脚本
      fig1..fig5-*.png                    # 报告引用的五张图
```

每个 `.md` 是一次检索/保存的批次报告，包含论文表格与完整摘要；
`NN-<主题>.md` 中的专题综述另附 `assets/` 下的 PDF 全文。

## 专题综述

| 日期 | 标题 | 材料 |
|---|---|---|
| 2026-10-25 | 强化学习：从试错学习到推理智能 | [摘要](2026-10-25/00-reinforcement-learning-survey.md) · [PDF 全文](2026-10-25/assets/reinforcement-learning-survey.pdf)（116 页，79 条参考文献）· [勘误](2026-10-25/errata.md) |
| 2026-10-26 | 主流广告 DSP 的出价策略与预算分配算法 | [正文](2026-10-26/00-dsp-bidding-algorithms.md) · [PDF 全文](2026-10-26/assets/dsp-bidding-algorithms.pdf)（17 页，20 条核心参考文献） |
| 2026-10-26 | 实时竞价（RTB）买入侧全链路技术综述：从流量、预估到出价与度量 | [正文](2026-10-26/05-rtb-buy-side-survey.md) · [PDF 全文](2026-10-26/assets/rtb-buy-side-survey.pdf)（19 页，32 条参考文献，含 4 组仿真） |
| 2026-10-30 | DSP 竞价应对策略调研：算法方向、工业实践与落地路径 | [正文](2026-10-30/00-dsp-bidding-response-strategy.md) · [配套代码](2026-10-30/assets/bid_strategy_toolkit.py)（删失估计 / 折价 / 控制器，5 组仿真，仅依赖 numpy） |

## 同步方式

在本机 DSH 会话中说出「更新github论文库」，会自动把新增的 Markdown 文件提交并推送到本仓库。

## 说明

- 内容只包含论文元数据、公开摘要与自撰综述，不含个人隐私。
- 源数据保存在本地 `papers/papers.jsonl`，本仓库只是发布副本。
- 综述中的效应量均标注证据等级；勘误文件记录历次审读发现的问题与更正。
