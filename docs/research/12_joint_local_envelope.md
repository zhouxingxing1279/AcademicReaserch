# 12 共享变量差函数界与局部包络查询

本轮在 [11](11_affine_enclosure_ablation.md) 的固定模型 A 上，实现离线联合差函数界、在线完整覆盖查询，并进行全局/局部配对重放。模型权重、物理输入、源轨迹、噪声及 60 个生成元预算保持不变。39 项测试通过。缺测场景仍未通过 20 秒可用性门。

## 1 联合界的公式与实现

离线计算七维变量 $`v=(s_1,\ldots,s_5,w_x,w_z)`$。在同一个叶子盒上以同一噪声向量表示真实加速度与网络：

```math
v=c+\operatorname{diag}(r)\xi,\quad |\xi|\leq\mathbf1,
\qquad a_\star(v)\in c_a+G_a\xi+[-e_a,e_a],
\qquad n_\theta(s)\in c_n+G_n\xi+[-e_n,e_n].
```

网络的最后两列生成元为零；其余五列使用第 11 章的仿射传播。先相减生成元，再取绝对值，得到：

```math
|a_\star(v)-n_\theta(s)|\leq
|c_a-c_n|+|G_a-G_n|\mathbf1+e_a+e_n.
```

这保留了真实模型和网络对共同输入变量的线性抵消。代码 `joint_envelope.py` 再将该界与原独立区间差界取逐分量最小值，确保数值回归检查中每个叶子不比旧界宽。

解析真值仅用于离线构建和验证产物；在线滤波不读取真实状态或真实风。此方法依赖本仓库明确给定的解析气动模型，尚不能直接转化为未知实机动力学的保证。

## 2 解析气动模型的仿射外包络

令两个标量仿射形式分别为 $`a=c_a+g_a\xi+\epsilon_a`$、$`b=c_b+g_b\xi+\epsilon_b`$，其中误差绝对值不超过 $`e_a,e_b`$，总半宽为 $`\rho_a=\|g_a\|_1+e_a`$、$`\rho_b=\|g_b\|_1+e_b`$。乘积满足：

```math
c_{ab}=c_ac_b,\quad g_{ab}=c_ag_b+c_bg_a,\quad
e_{ab}=|c_a|e_b+|c_b|e_a+\rho_a\rho_b.
```

对于二阶可导标量函数，若区间内 $`|f''|\leq M`$：

```math
c_f=f(c_a),\quad g_f=f'(c_a)g_a,\quad
e_f=|f'(c_a)|e_a+\frac{M}{2}\rho_a^2.
```

正弦与余弦采用 $`M=1`$。阻力函数 $`g(r)=r\sqrt{r^2+\varepsilon}`$，$`\varepsilon=0.04`$，有：

```math
g'(r)=\frac{2r^2+\varepsilon}{\sqrt{r^2+\varepsilon}},\qquad
g''(r)=\frac{r(2r^2+3\varepsilon)}{(r^2+\varepsilon)^{3/2}},\qquad |g''(r)|\leq2.
```

最后一个不等式可通过平方并展开验证：

```math
4(r^2+\varepsilon)^3-r^2(2r^2+3\varepsilon)^2
=3r^2\varepsilon^2+4\varepsilon^3\geq0.
```

将这些规则依次用于相对风速、阻力、交叉乘积、姿态正弦/余弦，即得到真实气动加速度的联合仿射形式。所有运算使用 float64 和工程裕量；未实现向外舍入，故仅保留条件解析推导及数值验证级别。

## 3 局部查询及覆盖依据

离线分区仍为七轴轮流二分、深度 14，共 16,384 个叶子。在线 `LocalEnvelope` 加载时，从配置域重新构造完整分区，逐元素核对上下界及顺序，核对模型、配置、表数据哈希和全局最大界。缺失、重排或修改叶子会被拒绝。

对当前状态集合外包盒构造归一化输入盒，控制量固定为实际执行值，风仍取完整允许区间。查询所有与该盒相交的闭叶子：

```math
\mathcal I_k=\{j:Q_j\cap Q_k\ne\varnothing\},\qquad
\bar e_k=\max_{j\in\mathcal I_k}\bar e_j.
```

最大值逐分量计算。完整分区覆盖全域，故任何查询点必属于一个被选中的叶子，其误差由该叶子的界控制。边界相交使用非严格不等式，避免漏掉分界上的叶子；越域、非有限输入或空覆盖显式拒绝。没有按最近中心选叶子，没有使用真实风缩小查询范围。

`local_filter.py` 使用局部加速度误差替代全域误差；神经仿射余项、物理余项、测量修正、约简及超域检查沿用上一轮。这种查询取的是整个相交叶子的界，仍然可能远宽于查询盒实际所需界。

## 4 结果与限制

| 全域加速度半宽（m/s²） | x | z |
|---|---:|---:|
| 原 IBP 模型 A | 6.593940 | 5.697553 |
| 第 11 章仿射区间交集 | 3.748999 | 2.850717 |
| 本轮共享变量差函数界 | 3.123067 | 2.724711 |

本轮局部查询的三个种子：S0 全部完成 20 秒；S1 分别在 3.56、3.18、2.98 秒超域，S2 全部在 1.58 秒超域。相比第 11 章 S1 的 1.32–1.38 秒及 S2 的 1.02–1.04 秒，前缀延长，但仍不满足可用性门。物理 zonotope 基线在相同源轨迹上仍全部完成 20 秒，不能声称当前学习滤波优于物理基线。

本轮另运行同一联合包络的全域最大值版本，作为局部查询的配对对照；其具体结果及本轮计时汇总见下方自动生成表。所有结果仅为三个种子的 pilot；有限成员检查、训练点预测精度和提前终止时间均不能证明闭环稳定性。

## 5 复现与验证

```bash
OPENBLAS_NUM_THREADS=1 python scripts/build_joint_envelope.py --output results/my_joint
OPENBLAS_NUM_THREADS=1 python scripts/evaluate_joint_model_a.py results/my_joint --propagation local --output results/my_local
OPENBLAS_NUM_THREADS=1 python scripts/evaluate_joint_model_a.py results/my_joint --propagation global --output results/my_global
OPENBLAS_NUM_THREADS=1 python -m unittest discover -s tests -v
```

输出目录须为空；运行依赖 NumPy、SciPy/HiGHS，沿用 `verification/requirements.txt`。默认测试核查归档产物。新增四项测试覆盖：全部叶子重生成及不劣于旧界；5,000 点真实模型仿射与联合界诊断；缺叶/篡改/配置不匹配拒绝；分区边界查询、100 点独立动力学预测 LP 成员检查及域外输入拒绝。有限点检查用于发现实现错误，不构成全域证明。

- [包络产物](../../results/joint_model_a_20260909/envelope.json)
- [39 项测试日志](../../results/joint_model_a_20260909/tests.txt)
- [局部查询重放](../../results/joint_local_20260909/summary.json)
- [全域最大值重放](../../results/joint_global_20260909/summary.json)

## 6 下一步及停止条件

下一轮先诊断“完整相交叶子取界”引入的量化冗余：固定模型，在离线加密速度/风维分区，比较查询界、缺测集合半宽和查询耗时。不能通过减少风范围、放大有效域或删除失败轨迹获得通过结果。若分区加密收益饱和，应比较直接对总动力学的共享仿射传播与当前“学习预测加独立误差”的表示冗余，而不是无限增大分区。

只有全部 S0/S1/S2 完成 20 秒且无数值成员检查失败，才进入更大种子集验证及 B/C/D 训练目标比较；实时预算需单独在固定环境测量。MPC 的可行性、约束收紧和稳定性证明仍为后续任务，不能由本轮结果替代。

## 7 本轮配对汇总

| 查询方式 | S0 秒 | S1 秒 | S2 秒 | 成员失败数 | 超过 20 ms 次数 | 最大调用 ms |
|---|---:|---:|---:|---:|---:|---:|
| global | 20.00–20.00 | 1.36–1.38 | 1.04–1.06 | 0 | 1 | 22.83 |
| local | 20.00–20.00 | 2.98–3.56 | 1.58–1.58 | 0 | 0 | 12.63 |

重放进程按顺序运行；局部版本运行期间另有短暂测试进程，计时仍受调度影响，不能作为严格实时基准。两个版本都保留超域终止，因此各自耗时样本长度不同。
