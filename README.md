# home_paper_search

个人 arXiv 论文阅读记录库，由本地 `arxiv-paper-log` skill 自动生成并同步。

## 目录结构

```
home_paper_search/
  2026-10-23/
    01-diffusion-policy.md    # <两位序号>-<主题>.md
    02-world-model.md
```

每个文件是一次检索/保存的批次报告，包含论文表格与完整摘要。

## 专题综述

- 2026-10-25：[强化学习：从试错学习到推理智能](2026-10-25/00-reinforcement-learning-survey.md)（[PDF 全文](2026-10-25/assets/reinforcement-learning-survey.pdf)，116 页，79 条参考文献）

## 同步方式

在本机 DSH 会话中说出「更新github论文库」，会自动把新增的 Markdown 文件提交并推送到本仓库。

## 说明

- 内容只包含论文元数据与公开摘要，不含个人隐私。
- 源数据保存在本地 `papers/papers.jsonl`，本仓库只是发布副本。
