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
```

每个 `.md` 是一次检索/保存的批次报告，包含论文表格与完整摘要；
`NN-<主题>.md` 中的专题综述另附 `assets/` 下的 PDF 全文。

## 专题综述

| 日期 | 标题 | 材料 |
|---|---|---|
| 2026-10-25 | 强化学习：从试错学习到推理智能 | [摘要](2026-10-25/00-reinforcement-learning-survey.md) · [PDF 全文](2026-10-25/assets/reinforcement-learning-survey.pdf)（116 页，79 条参考文献）· [勘误](2026-10-25/errata.md) |

## 同步方式

在本机 DSH 会话中说出「更新github论文库」，会自动把新增的 Markdown 文件提交并推送到本仓库。

## 说明

- 内容只包含论文元数据、公开摘要与自撰综述，不含个人隐私。
- 源数据保存在本地 `papers/papers.jsonl`，本仓库只是发布副本。
- 综述中的效应量均标注证据等级；勘误文件记录历次审读发现的问题与更正。
