# arXiv 论文记录

> 查询：incrementality · 共 2 篇 · 生成 2026-11-08T14:43:24+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [Privacy-Robust Incrementality Measurement for Advertising Systems under Signal Loss](https://arxiv.org/abs/2606.03878) | stat.ML | 2026-06-02 | [abs](https://arxiv.org/abs/2606.03878) · [pdf](https://arxiv.org/pdf/2606.03878) |
| 2 | [Attributed, But Not Incremental: Cannibalization-Corrected Attribution for Large-Scale Advertising](https://arxiv.org/abs/2606.26690) | cs.IR | 2026-06-25 | [abs](https://arxiv.org/abs/2606.26690) · [pdf](https://arxiv.org/pdf/2606.26690) |

## 摘要

### 1. Privacy-Robust Incrementality Measurement for Advertising Systems under Signal Loss

- 作者：Prashant Shekhar, Caroline Howard
- 领域：`stat.ML`（全部：stat.ML, cs.LG）
- 发布：2026-06-02 · 更新：2026-06-02
- 链接：https://arxiv.org/abs/2606.03878 · PDF：https://arxiv.org/pdf/2606.03878
- 入库：2026-11-08T14:43:24+08:00

> Advertising platforms use randomized lift tests to measure incrementality, but privacy-preserving reporting systems degrade the observed signal through match-rate loss, linkability loss, attribution-window loss, aggregation-threshold suppression, randomized reporting noise, and segment-heterogeneous signal loss. This paper formulates privacy-constrained advertising measurement as a robust causal decision problem under the mentioned signal losses. Given a randomized experiment and an ambiguity set for privacy-induced degradation, the framework projects the observation-compatible fiber of clean/unfiltered experimental worlds onto the incrementality functional and returns certified, rejected, and unresolved decisions. The main result gives a sharp decision frontier. Reports outside the frontier support uniformly valid certification or rejection, whereas reports inside it contain too little information for any method to uniformly distinguish above-threshold incrementality from non-incrementality. Supporting results give finite-sample certification, sample-complexity guarantees, a minimax lower bound showing that signal loss reduces effective information, and a reporting-granularity tradeoff. On 2.0M Criteo Uplift rows and the 64K-row Hillstrom email experiment, clean conversion lift is positive in both datasets, with lifts 0.00112 and 0.00495, respectively. Population certification survives mild degradation in Criteo and severe degradation in Hillstrom, while all considered finite-sample stress settings in both datasets remain unresolved after simultaneous uncertainty and reporting noise are included. Overall, the research contributes a decision-theoretic layer for privacy-aware incrementality measurement whose output is the strongest causal-claim justified by degraded ads signals.

### 2. Attributed, But Not Incremental: Cannibalization-Corrected Attribution for Large-Scale Advertising

- 作者：Donghui Li, Bowen Yuan, Zili Yang, Qinxin Chen, Lijing Song
- 领域：`cs.IR`（全部：cs.IR, cs.LG）
- 发布：2026-06-25 · 更新：2026-06-25
- 链接：https://arxiv.org/abs/2606.26690 · PDF：https://arxiv.org/pdf/2606.26690
- 备注：6 pages, 3 figures. Accepted at ADKDD 2026
- 入库：2026-11-08T14:43:24+08:00

> In large-scale paid acquisition and growth advertising systems, production attribution outputs are widely used for daily budget allocation and channel diagnosis. However, paid-attributed conversions such as daily new users (DNU) may systematically overstate true incremental growth when paid channels overlap with organic demand, brand-driven traffic, or other acquisition channels. This attribution-cannibalization mismatch can distort incremental ROI measurement and budget decisions at scale. We propose an experiment-calibrated attribution correction framework that uses incrementality experiments as causal anchors to convert sparse lift measurements into daily correction estimates. To make the corrected signal actionable at production granularity, we further allocate calibrated cannibalization volume across business hierarchies under structural consistency constraints. Offline forward-in-time validation against channel-level incrementality experiment readouts shows that the proposed framework substantially reduces calibration error relative to raw attribution and fine-grained ML baselines. Deployed across multiple global TikTok markets, the system supported budget and traffic strategy adjustments that were followed by an approximately 15-percentage-point reduction in the measured cannibalization rate.
