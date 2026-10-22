# arXiv 论文记录

> 查询：diffusion policy · 共 5 篇 · 生成 2026-10-23T01:39:22+08:00

| # | 标题 | 领域 | 发布时间 | 链接 |
|---|---|---|---|---|
| 1 | [One-Step Diffusion Policy: Fast Visuomotor Policies via Diffusion Distillation](https://arxiv.org/abs/2410.21257) | cs.RO | 2024-10-28 | [abs](https://arxiv.org/abs/2410.21257) · [pdf](https://arxiv.org/pdf/2410.21257) |
| 2 | [Diffusion Policy Policy Optimization](https://arxiv.org/abs/2409.00588) | cs.RO | 2024-09-01 | [abs](https://arxiv.org/abs/2409.00588) · [pdf](https://arxiv.org/pdf/2409.00588) |
| 3 | [Equivariant Diffusion Policy](https://arxiv.org/abs/2407.01812) | cs.RO | 2024-07-01 | [abs](https://arxiv.org/abs/2407.01812) · [pdf](https://arxiv.org/pdf/2407.01812) |
| 4 | [Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](https://arxiv.org/abs/2303.04137) | cs.RO | 2023-03-07 | [abs](https://arxiv.org/abs/2303.04137) · [pdf](https://arxiv.org/pdf/2303.04137) |
| 5 | [Diffusion Policies as an Expressive Policy Class for Offline Reinforcement Learning](https://arxiv.org/abs/2208.06193) | cs.LG | 2022-08-12 | [abs](https://arxiv.org/abs/2208.06193) · [pdf](https://arxiv.org/pdf/2208.06193) |

## 摘要

### 1. One-Step Diffusion Policy: Fast Visuomotor Policies via Diffusion Distillation

- 作者：Zhendong Wang, Zhaoshuo Li, Ajay Mandlekar, Zhenjia Xu, Jiaojiao Fan, Yashraj Narang, Linxi Fan, Yuke Zhu, Yogesh Balaji, Mingyuan Zhou, Ming-Yu Liu, Yu Zeng
- 领域：`cs.RO`（全部：cs.RO, cs.LG）
- 发布：2024-10-28 · 更新：2024-10-28
- 链接：https://arxiv.org/abs/2410.21257 · PDF：https://arxiv.org/pdf/2410.21257
- 入库：2026-10-23T01:30:15+08:00

> Diffusion models, praised for their success in generative tasks, are increasingly being applied to robotics, demonstrating exceptional performance in behavior cloning. However, their slow generation process stemming from iterative denoising steps poses a challenge for real-time applications in resource-constrained robotics setups and dynamically changing environments. In this paper, we introduce the One-Step Diffusion Policy (OneDP), a novel approach that distills knowledge from pre-trained diffusion policies into a single-step action generator, significantly accelerating response times for robotic control tasks. We ensure the distilled generator closely aligns with the original policy distribution by minimizing the Kullback-Leibler (KL) divergence along the diffusion chain, requiring only $2\%$-$10\%$ additional pre-training cost for convergence. We evaluated OneDP on 6 challenging simulation tasks as well as 4 self-designed real-world tasks using the Franka robot. The results demonstrate that OneDP not only achieves state-of-the-art success rates but also delivers an order-of-magnitude improvement in inference speed, boosting action prediction frequency from 1.5 Hz to 62 Hz, establishing its potential for dynamic and computationally constrained robotic applications. We share the project page at https://research.nvidia.com/labs/dir/onedp/.

### 2. Diffusion Policy Policy Optimization

- 作者：Allen Z. Ren, Justin Lidard, Lars L. Ankile, Anthony Simeonov, Pulkit Agrawal, Anirudha Majumdar, Benjamin Burchfiel, Hongkai Dai, Max Simchowitz
- 领域：`cs.RO`（全部：cs.RO, cs.LG）
- 发布：2024-09-01 · 更新：2024-12-09
- 链接：https://arxiv.org/abs/2409.00588 · PDF：https://arxiv.org/pdf/2409.00588
- 备注：Website: diffusion-ppo.github.io
- 入库：2026-10-23T01:30:15+08:00

> We introduce Diffusion Policy Policy Optimization, DPPO, an algorithmic framework including best practices for fine-tuning diffusion-based policies (e.g. Diffusion Policy) in continuous control and robot learning tasks using the policy gradient (PG) method from reinforcement learning (RL). PG methods are ubiquitous in training RL policies with other policy parameterizations; nevertheless, they had been conjectured to be less efficient for diffusion-based policies. Surprisingly, we show that DPPO achieves the strongest overall performance and efficiency for fine-tuning in common benchmarks compared to other RL methods for diffusion-based policies and also compared to PG fine-tuning of other policy parameterizations. Through experimental investigation, we find that DPPO takes advantage of unique synergies between RL fine-tuning and the diffusion parameterization, leading to structured and on-manifold exploration, stable training, and strong policy robustness. We further demonstrate the strengths of DPPO in a range of realistic settings, including simulated robotic tasks with pixel observations, and via zero-shot deployment of simulation-trained policies on robot hardware in a long-horizon, multi-stage manipulation task. Website with code: diffusion-ppo.github.io

### 3. Equivariant Diffusion Policy

- 作者：Dian Wang, Stephen Hart, David Surovik, Tarik Kelestemur, Haojie Huang, Haibo Zhao, Mark Yeatman, Jiuguang Wang, Robin Walters, Robert Platt
- 领域：`cs.RO`（全部：cs.RO, cs.LG）
- 发布：2024-07-01 · 更新：2024-10-15
- 链接：https://arxiv.org/abs/2407.01812 · PDF：https://arxiv.org/pdf/2407.01812
- 备注：Conference on Robot Learning 2024, Oral Presentation
- 入库：2026-10-23T01:30:15+08:00

> Recent work has shown diffusion models are an effective approach to learning the multimodal distributions arising from demonstration data in behavior cloning. However, a drawback of this approach is the need to learn a denoising function, which is significantly more complex than learning an explicit policy. In this work, we propose Equivariant Diffusion Policy, a novel diffusion policy learning method that leverages domain symmetries to obtain better sample efficiency and generalization in the denoising function. We theoretically analyze the $\mathrm{SO}(2)$ symmetry of full 6-DoF control and characterize when a diffusion model is $\mathrm{SO}(2)$-equivariant. We furthermore evaluate the method empirically on a set of 12 simulation tasks in MimicGen, and show that it obtains a success rate that is, on average, 21.9% higher than the baseline Diffusion Policy. We also evaluate the method on a real-world system to show that effective policies can be learned with relatively few training samples, whereas the baseline Diffusion Policy cannot.

### 4. Diffusion Policy: Visuomotor Policy Learning via Action Diffusion

- 作者：Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, Shuran Song
- 领域：`cs.RO`（全部：cs.RO）
- 发布：2023-03-07 · 更新：2024-03-14
- 链接：https://arxiv.org/abs/2303.04137 · PDF：https://arxiv.org/pdf/2303.04137
- 备注：An extended journal version of the original RSS2023 paper
- 入库：2026-10-23T01:30:15+08:00

> This paper introduces Diffusion Policy, a new way of generating robot behavior by representing a robot's visuomotor policy as a conditional denoising diffusion process. We benchmark Diffusion Policy across 12 different tasks from 4 different robot manipulation benchmarks and find that it consistently outperforms existing state-of-the-art robot learning methods with an average improvement of 46.9%. Diffusion Policy learns the gradient of the action-distribution score function and iteratively optimizes with respect to this gradient field during inference via a series of stochastic Langevin dynamics steps. We find that the diffusion formulation yields powerful advantages when used for robot policies, including gracefully handling multimodal action distributions, being suitable for high-dimensional action spaces, and exhibiting impressive training stability. To fully unlock the potential of diffusion models for visuomotor policy learning on physical robots, this paper presents a set of key technical contributions including the incorporation of receding horizon control, visual conditioning, and the time-series diffusion transformer. We hope this work will help motivate a new generation of policy learning techniques that are able to leverage the powerful generative modeling capabilities of diffusion models. Code, data, and training details is publicly available diffusion-policy.cs.columbia.edu

### 5. Diffusion Policies as an Expressive Policy Class for Offline Reinforcement Learning

- 作者：Zhendong Wang, Jonathan J Hunt, Mingyuan Zhou
- 领域：`cs.LG`（全部：cs.LG, stat.ML）
- 发布：2022-08-12 · 更新：2023-08-25
- 链接：https://arxiv.org/abs/2208.06193 · PDF：https://arxiv.org/pdf/2208.06193
- 备注：ICLR 2023
- 入库：2026-10-23T01:30:15+08:00

> Offline reinforcement learning (RL), which aims to learn an optimal policy using a previously collected static dataset, is an important paradigm of RL. Standard RL methods often perform poorly in this regime due to the function approximation errors on out-of-distribution actions. While a variety of regularization methods have been proposed to mitigate this issue, they are often constrained by policy classes with limited expressiveness that can lead to highly suboptimal solutions. In this paper, we propose representing the policy as a diffusion model, a recent class of highly-expressive deep generative models. We introduce Diffusion Q-learning (Diffusion-QL) that utilizes a conditional diffusion model to represent the policy. In our approach, we learn an action-value function and we add a term maximizing action-values into the training loss of the conditional diffusion model, which results in a loss that seeks optimal actions that are near the behavior policy. We show the expressiveness of the diffusion model-based policy, and the coupling of the behavior cloning and policy improvement under the diffusion model both contribute to the outstanding performance of Diffusion-QL. We illustrate the superiority of our method compared to prior works in a simple 2D bandit example with a multimodal behavior policy. We then show that our method can achieve state-of-the-art performance on the majority of the D4RL benchmark tasks.
