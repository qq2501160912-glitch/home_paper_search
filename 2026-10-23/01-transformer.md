# arXiv 论文记录

> 查询：transformer · 共 5 篇 · 生成 2026-10-23T02:20:32+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [Multiscale Vision Transformers](https://arxiv.org/abs/2104.11227) | cs.CV | 2021-04-22 | [abs](https://arxiv.org/abs/2104.11227) · [pdf](https://arxiv.org/pdf/2104.11227) |
| 2 | [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805) | cs.CL | 2018-10-11 | [abs](https://arxiv.org/abs/1810.04805) · [pdf](https://arxiv.org/pdf/1810.04805) |
| 3 | [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929) | cs.CV | 2020-10-22 | [abs](https://arxiv.org/abs/2010.11929) · [pdf](https://arxiv.org/pdf/2010.11929) |
| 4 | [Swin Transformer: Hierarchical Vision Transformer using Shifted Windows](https://arxiv.org/abs/2103.14030) | cs.CV | 2021-03-25 | [abs](https://arxiv.org/abs/2103.14030) · [pdf](https://arxiv.org/pdf/2103.14030) |
| 5 | [Deformable DETR: Deformable Transformers for End-to-End Object Detection](https://arxiv.org/abs/2010.04159) | cs.CV | 2020-10-08 | [abs](https://arxiv.org/abs/2010.04159) · [pdf](https://arxiv.org/pdf/2010.04159) |

## 摘要

### 1. Multiscale Vision Transformers

- 作者：Haoqi Fan, Bo Xiong, Karttikeya Mangalam, Yanghao Li, Zhicheng Yan, Jitendra Malik, Christoph Feichtenhofer
- 领域：`cs.CV`（全部：cs.CV, cs.AI, cs.LG）
- 发布：2021-04-22 · 更新：2021-04-22
- 链接：https://arxiv.org/abs/2104.11227 · PDF：https://arxiv.org/pdf/2104.11227
- 备注：Technical report
- 入库：2026-10-23T02:20:18+08:00

> We present Multiscale Vision Transformers (MViT) for video and image recognition, by connecting the seminal idea of multiscale feature hierarchies with transformer models. Multiscale Transformers have several channel-resolution scale stages. Starting from the input resolution and a small channel dimension, the stages hierarchically expand the channel capacity while reducing the spatial resolution. This creates a multiscale pyramid of features with early layers operating at high spatial resolution to model simple low-level visual information, and deeper layers at spatially coarse, but complex, high-dimensional features. We evaluate this fundamental architectural prior for modeling the dense nature of visual signals for a variety of video recognition tasks where it outperforms concurrent vision transformers that rely on large scale external pre-training and are 5-10x more costly in computation and parameters. We further remove the temporal dimension and apply our model for image classification where it outperforms prior work on vision transformers. Code is available at: https://github.com/facebookresearch/SlowFast

### 2. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding

- 作者：Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova
- 领域：`cs.CL`（全部：cs.CL）
- 发布：2018-10-11 · 更新：2019-05-24
- 链接：https://arxiv.org/abs/1810.04805 · PDF：https://arxiv.org/pdf/1810.04805
- 入库：2026-10-23T02:11:27+08:00

> We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context in all layers. As a result, the pre-trained BERT model can be fine-tuned with just one additional output layer to create state-of-the-art models for a wide range of tasks, such as question answering and language inference, without substantial task-specific architecture modifications. BERT is conceptually simple and empirically powerful. It obtains new state-of-the-art results on eleven natural language processing tasks, including pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1 (5.1 point absolute improvement).

### 3. An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale

- 作者：Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, Neil Houlsby
- 领域：`cs.CV`（全部：cs.CV, cs.AI, cs.LG）
- 发布：2020-10-22 · 更新：2021-06-03
- 链接：https://arxiv.org/abs/2010.11929 · PDF：https://arxiv.org/pdf/2010.11929
- 备注：Fine-tuning code and pre-trained models are available at https://github.com/google-research/vision_transformer. ICLR camera-ready version with 2 small modifications: 1) Added a discussion of CLS vs GAP classifier in the appendix, 2) Fixed an error in exaFLOPs computation in Figure 5 and Table 6 (relative performance of models is basically not affected)
- 入库：2026-10-23T02:11:27+08:00

> While the Transformer architecture has become the de-facto standard for natural language processing tasks, its applications to computer vision remain limited. In vision, attention is either applied in conjunction with convolutional networks, or used to replace certain components of convolutional networks while keeping their overall structure in place. We show that this reliance on CNNs is not necessary and a pure transformer applied directly to sequences of image patches can perform very well on image classification tasks. When pre-trained on large amounts of data and transferred to multiple mid-sized or small image recognition benchmarks (ImageNet, CIFAR-100, VTAB, etc.), Vision Transformer (ViT) attains excellent results compared to state-of-the-art convolutional networks while requiring substantially fewer computational resources to train.

### 4. Swin Transformer: Hierarchical Vision Transformer using Shifted Windows

- 作者：Ze Liu, Yutong Lin, Yue Cao, Han Hu, Yixuan Wei, Zheng Zhang, Stephen Lin, Baining Guo
- 领域：`cs.CV`（全部：cs.CV, cs.LG）
- 发布：2021-03-25 · 更新：2021-08-17
- 链接：https://arxiv.org/abs/2103.14030 · PDF：https://arxiv.org/pdf/2103.14030
- 入库：2026-10-23T02:11:27+08:00

> This paper presents a new vision Transformer, called Swin Transformer, that capably serves as a general-purpose backbone for computer vision. Challenges in adapting Transformer from language to vision arise from differences between the two domains, such as large variations in the scale of visual entities and the high resolution of pixels in images compared to words in text. To address these differences, we propose a hierarchical Transformer whose representation is computed with \textbf{S}hifted \textbf{win}dows. The shifted windowing scheme brings greater efficiency by limiting self-attention computation to non-overlapping local windows while also allowing for cross-window connection. This hierarchical architecture has the flexibility to model at various scales and has linear computational complexity with respect to image size. These qualities of Swin Transformer make it compatible with a broad range of vision tasks, including image classification (87.3 top-1 accuracy on ImageNet-1K) and dense prediction tasks such as object detection (58.7 box AP and 51.1 mask AP on COCO test-dev) and semantic segmentation (53.5 mIoU on ADE20K val). Its performance surpasses the previous state-of-the-art by a large margin of +2.7 box AP and +2.6 mask AP on COCO, and +3.2 mIoU on ADE20K, demonstrating the potential of Transformer-based models as vision backbones. The hierarchical design and the shifted window approach also prove beneficial for all-MLP architectures. The code and models are publicly available at~\url{https://github.com/microsoft/Swin-Transformer}.

### 5. Deformable DETR: Deformable Transformers for End-to-End Object Detection

- 作者：Xizhou Zhu, Weijie Su, Lewei Lu, Bin Li, Xiaogang Wang, Jifeng Dai
- 领域：`cs.CV`（全部：cs.CV）
- 发布：2020-10-08 · 更新：2021-03-18
- 链接：https://arxiv.org/abs/2010.04159 · PDF：https://arxiv.org/pdf/2010.04159
- 备注：ICLR 2021 Oral
- 入库：2026-10-23T02:11:27+08:00

> DETR has been recently proposed to eliminate the need for many hand-designed components in object detection while demonstrating good performance. However, it suffers from slow convergence and limited feature spatial resolution, due to the limitation of Transformer attention modules in processing image feature maps. To mitigate these issues, we proposed Deformable DETR, whose attention modules only attend to a small set of key sampling points around a reference. Deformable DETR can achieve better performance than DETR (especially on small objects) with 10 times less training epochs. Extensive experiments on the COCO benchmark demonstrate the effectiveness of our approach. Code is released at https://github.com/fundamentalvision/Deformable-DETR.
