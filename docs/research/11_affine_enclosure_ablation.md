# 11 固定模型 A 的仿射包络改进与配对消融

本轮承接 [10](10_model_a_training_and_envelope.md)，不重新训练模型，不改变物理系统、传感器噪声、输入或生成元预算。结果是部分改善：正常测量 S0 完成 20 秒；S1/S2 缺测场景仍超域。尚未实现 MPC，也没有证明闭环稳定性或严格浮点包含性。

## 1 实际改动与研究边界

新增 `affine_model.py`：保留输入扰动的线性相关性，以标量 tanh 切线余项包住非线性；输出区间与原 IBP 取交集。新增 `affine_filter.py`：用该仿射余项代替旧逐层二阶导数绝对值界。原实现和历史日志完整保留。

这是包络实现的改进与消融证据，不是已确立的论文创新。当前仍分别外包真实残差和网络输出；尚未实现二者共享变量的差函数联合传播。训练权重 SHA-256 保持为 `98b084b43cb6286a6849424d63ace5fd85ab50440cdddb05aff19c9350900ce9`，点预测误差因此不变。

## 2 仿射传播推导

对归一化输入盒，令中心为 c、半宽为 r。每层用一个共享输入噪声向量和附加区间误差表示：

```math
s=c+\operatorname{diag}(r)\xi,\quad |\xi|\leq\mathbf1,
\qquad h\in c_h+G_h\xi+[-e_h,e_h].
```

初始为 $`G_h=\operatorname{diag}(r), e_h=0`$。线性层保留带符号生成元：

```math
c_z=Wc_h+b,\qquad G_z=WG_h,\qquad e_z=|W|e_h,
\qquad \rho_z=|G_z|\mathbf1+e_z.
```

因此第 j 个预激活属于 $`[c_{z,j}-\rho_{z,j},c_{z,j}+\rho_{z,j}]`$。在其中心作切线：

```math
d_j=1-\tanh^2(c_{z,j}),\qquad
q_j(z)=\tanh(z)-\tanh(c_{z,j})-d_j(z-c_{z,j}).
```

导数零点满足：

```math
q'_j(z)=\operatorname{sech}^2(z)-\operatorname{sech}^2(c_{z,j})=0
\quad\Longrightarrow\quad z\in\{-|c_{z,j}|,|c_{z,j}|\}.
```

在实数算术下，只需检查区间两端及落在区间内的这两个驻点，即得到 $`\eta_j=\max |q_j(z)|`$。于是激活层更新为：

```math
c_h^+=\tanh(c_z),\qquad
G_h^+=\operatorname{diag}(d)G_z,\qquad
e_h^+=d\odot e_z+\eta.
```

归纳可得每层集合包含关系。网络末层为线性层，因此最终中心是 $`n_\theta(c)`$，线性项是精确链式 Jacobian：

```math
G_{\rm out}=J_\theta(c)\operatorname{diag}(r),\qquad
|n_\theta(c+\delta)-n_\theta(c)-J_\theta(c)\delta|
\leq e_{\rm out},\quad |\delta|\leq r.
```

这一步保留生成元乘法中的符号抵消，但附加误差仍以盒表示，仍会丢失部分相关性。代码末尾增加工程数值裕量；没有使用向外舍入，故上述实数推导不构成实现的严格浮点证书。

## 3 误差包络与滤波接入

网络输出盒为：

```math
I_{\rm aff}=[c_{\rm out}-|G_{\rm out}|\mathbf1-e_{\rm out},
             c_{\rm out}+|G_{\rm out}|\mathbf1+e_{\rm out}],
\qquad I_n=I_{\rm aff}\cap I_{\rm IBP}.
```

在同一 16,384 个分区上，保留 [10](10_model_a_training_and_envelope.md) 的真实残差区间，重新计算真实残差减网络输出的区间差。所有叶子均保留，未用采样最大误差代替全域界。

| 加速度半宽（m/s²） | x 方向 | z 方向 |
|---|---:|---:|
| 原模型 A 包络 | 6.593940 | 5.697553 |
| 仿射与 IBP 交集包络 | 3.748999 | 2.850717 |
| 物理模型原包络 | 1.879898 | 2.085498 |

新包络仍大于物理模型基线。对滤波当前状态盒，仅将其速度、姿态半宽映射到网络输入；实际控制量已知，其输入半宽为零。网络状态 Jacobian 加入预测矩阵，$`h e_{\rm out}`$ 加入速度行余项，新的模型误差包络替代旧模型误差项。外部过程扰动和物理动力学余项分别保留，不重复叠加旧模型误差。

## 4 配对消融结果

3 个种子 70001–70003，S0/S1/S2 三类传感器时序，60 个生成元；每条源轨迹哈希与归档物理对照相同。本轮新增三组、共 27 次运行，旧组合直接使用归档结果。表中为三个种子的终止时间范围；20 秒表示完整结束，其他时间均为 OutOfDomain。

| 全局包络 | 在线余项 | S0（秒） | S1（秒） | S2（秒） |
|---|---|---:|---:|---:|
| 原包络 | 原二阶界（归档） | 0.36 | 0.30 | 0.26 |
| 新包络 | 原二阶界 | 0.68 | 0.48 | 0.44 |
| 原包络 | 新仿射余项 | 20.00 | 0.58–0.76 | 0.48–0.50 |
| 新包络 | 新仿射余项 | 20.00 | 1.32–1.38 | 1.02–1.04 |
| 物理 zonotope（归档） | 物理余项 | 20.00 | 20.00 | 20.00 |

该消融支持一个局部结论：在固定模型、数据和预算下，原余项传播是 S0 提前失败的重要来源；收紧包络进一步改善缺测前缀，但不足以通过缺测场景。不能据此声称学习模型优于物理模型，不能把通过的 S0 作为所有场景的成功率。

有效前缀数值 LP 成员检查没有失败；超域终止时不记录旧集合为新时刻有效结果。两项改进同时启用的运行中有 25 次滤波调用超过 20 ms，最大约 180.59 ms。实验进程存在并发与环境调度影响，计时仅作原始运行诊断，不能用于实时性能排序或实时保证。

## 5 验证工具与可复现产物

NumPy 完成网络仿射运算，SciPy/HiGHS 完成 zonotope 成员 LP；`unittest` 共 35 项通过。新增检查包括训练后网络在 80 个盒、每盒 30 个点的余项与区间诊断、批量与单盒一致性、零半宽退化、100 个独立动力学预测成员检查。

`verification/check_affine_artifact.py` 重新生成全部 16,384 个叶子，与 NPZ 逐项一致；每个叶子的界均不宽于归档旧界。另以种子 75003 检查 10,000 个诊断点。这些有限样本不能证明全域包含，也不属于正式测试集结论。

- [新包络与检查](../../results/affine_model_a_20260909/envelope.json)
- [两项改进同时启用](../../results/affine_both_20260909/summary.json)
- [仅改包络](../../results/affine_envelope_only_20260909/summary.json)
- [仅改传播](../../results/affine_propagation_only_20260909/summary.json)
- [测试日志](../../results/affine_model_a_20260909/tests.txt)

在仓库根目录，依赖沿用 `verification/requirements.txt`，使用空输出目录：

```bash
OPENBLAS_NUM_THREADS=1 python scripts/build_affine_envelope.py --output results/my_affine
OPENBLAS_NUM_THREADS=1 python scripts/evaluate_affine_model_a.py results/my_affine --output results/my_both
OPENBLAS_NUM_THREADS=1 python scripts/evaluate_affine_model_a.py results/my_affine --propagation legacy --output results/my_envelope_only
OPENBLAS_NUM_THREADS=1 python scripts/evaluate_affine_model_a.py results/model_a_20260909 --output results/my_propagation_only
python -m unittest discover -s tests -v
OPENBLAS_NUM_THREADS=1 python verification/check_affine_artifact.py
```

最后一条命令核查固定归档目录并重写该目录的诊断 JSON。训练权重直接复制原产物，未重新拟合。原训练与重放源码不修改，以保留历史 manifest 的可核对性。

## 6 下一步任务与验收条件

1. **共享变量差函数界**：实现 $`a_\star(s,w)-n_\theta(s)`$ 的联合仿射或均值形式，在相同变量上保留抵消；先与现有每叶界取交集。该接口只能在离线分析模块访问解析真值，在线滤波只加载与模型和配置绑定的产物。检查分区完整性、导数、叶子界和模型哈希后再重放。
2. **局部包络查询**：若全域最大值仍主导膨胀，查询所有与当前状态盒及已知控制相交的预验证叶子，取覆盖并集的最大界；风维必须覆盖全部允许区间。没有覆盖、域外或哈希不匹配时显式拒绝，不能用最近叶子替代覆盖。所有闭区间边界需正确处理。
3. **可用性门**：保留同一 3×3 pilot 配对矩阵，要求 S0/S1/S2 均完成 20 秒、无成员检查失败、无静默丢弃困难样本；再扩展正式种子与模型 B/C/D。仅改善终止时间不算通过。
4. **计算成本门**：对稳定通过的实现单进程测量滤波/查询/LP/约简耗时，固定硬件与线程；未达预算则先优化，再讨论 MPC 闭环集成。

现阶段最值得继续验证的研究问题是：包络算法的保守性是否掩盖了训练目标对集合估计的影响。必须先排除这一混杂因素，才能将模型间差异解释为训练方法的贡献。
