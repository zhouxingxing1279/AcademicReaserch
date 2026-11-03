# Run205：移动中心 SMF 外包的四拍精确鲁棒力矩准入与安全过滤器原型

日期：2026-10-30。基线 `main=bba2ea1419bfa86fdf1750605f91504304131914`（Run204）。唯一问题：在固定中心盒终端族被排除后，是否至少能对**移动中心的可靠后验外包**构造非零因果力矩的精确有限时域安全准入，并给出成功包/缺包的原始硬约束判定差异？

## 合同和量词

沿用 `configs/planar_baseline.json` 四状态 `(p,v,phi,omega)` Euler 模型，`h=J=1/50`，`T∈[981/200,2943/200]`，`|r|≤47/25+(243/16000)T`，`|tau|≤2/25`，状态约束 `(5,3,9/20,2)`。第10 tick位置包已观察到 success/miss 后，选择一个 `tau0`，未来三拍力矩固定为零；当前 `T0` 可见为高端点，未来 `T1,T2,T3` 每拍在全区间独立任意跳变，`r_k` 每拍独立。审计四拍中所有真实状态，**没有第15 tick位置包**；所以这还不是跨下一次成功/缺包分支的递归控制器。姿态观测可获得但不用于四拍内的反馈收紧。

初始集合为 `x0∈c+diag(q)[-1,1]^4`，中心 `c` 可移动，半宽 `q` 使用 Run202 10 tick 高推力 success/miss 的**严格有理区间外包**；未使用其浮点 CZ LP 投影。对于移位的 `c`，仅研究物理约束内的**假设信息盒**，未证明其可由冻结零初始集合及相应观测历史到达。任何真正的 SMF 后验只要被此盒包含，以下条件性安全结论成立；不得将假设盒的结果误写为实际成功/缺包统计。

## 四拍鲁棒准入定理（本冻结模型）

对固定未来推力端点序列和四拍固定 backup `tau1=tau2=tau3=0`，精确有理生成元传播给出每拍状态坐标

`x_{k,i}=a_{k,i}(T)+b_{k,i}(T)*tau0+sum_j G_{k,ij}(T)*xi_j`，`|xi_j|≤1`。

所以所有初始误差与残差均满足硬约束的**充要条件**为：

`|a_{k,i}(T)+b_{k,i}(T)*tau0|+sum_j |G_{k,ij}(T)| ≤ limit_i`，对 `k=1..4, i=1..4`。

对每个固定不确定性原语，冻结四状态动力学中每个未来推力分量分别仿射（横向残差半宽亦仿射），因此其多仿射插值位于未来推力顶点值的凸包；对正负坐标支持均只需检查 `2^3=8` 个推力端点组合。每个约束都给出 `tau0` 的闭区间，交集与执行器区间相交即为**精确有理数可接受力矩区间**，一共 `4×4×8=128` 条坐标准入检查。若区间非空，将建议力矩投影到该区间即可获得**仅未来四拍**的原始硬约束保证。若区间空，表示这一“单步非零、后三步零”的 backup 类不可行，**不排除其他因果控制策略**。

相对阶复核：`tau0` 首次影响 `omega1`、`phi2`、`v3`、`p4`；因此四拍首次可看到力矩对位置约束的影响，三拍审计无法看到该效应。证明范围仅为离散四状态合同、独立区间盒及该固定未来控制类。

## 结果与负面见证

在 `T0=Tmax`、10 tick 高推力的 Run202 区间半宽下，使用精确有理计算：

| 假设后验中心 `(p,v,phi,omega)` | 包结果 | 四拍可接受 `tau0` | `tau_proposed=0.04` 的过滤结果 |
|---|---|---|---|
| `(0,0,0,0)` | success/miss | `[-0.08,0.08]` | `0.04` |
| `(0,2.35,0,0)` | success | `[-0.08,0.08]` | `0.04` |
| `(0,2.35,0,0)` | miss | **空集** | 拒绝；不得假称有 backup |
| `(0,0,0.38,0.8)` | success/miss | `[-0.08,1/300]` | **裁剪为 `1/300≈0.003333`** |

速度移位案例中，成功包的速度半宽 `140632479/320000000≈0.43948`，缺包半宽 `8566589/16000000≈0.53541`；缺包盒即使初始仍满足 `|v|≤3`，在最大推力和每拍最大正扰动的合法顶点下，四拍后存在 `v>3` 的真实硬约束违反见证。由于控制相对阶限制，`|tau0|≤0.08` 无法用此 backup 消除违约。这是**控制相关的条件性信息差异**，而不是新增的终端安全证书。

姿态移位案例中，四拍姿态硬约束迫使 `tau0≤1/300`，故候选正力矩 `0.04` 被精确过滤；不是零力矩总能安全，也不是已实现无限时域 MPC。

## 文献复核与原创性边界

- Lorenzetti & Pavone (2020), *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*, ECC, DOI https://doi.org/10.23919/ECC51009.2020.9143979 ，作者版 https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf 。本轮核对摘要、固定截面管束与 RPI/终端条件的作用。其递归可行性保证不能用于本轮仅四拍的过滤器。
- Scott, Raimondo, Marseglia & Braatz (2016), *Constrained zonotopes: A new tool for set-based estimation and fault detection*, Automatica 69:126–136, DOI https://doi.org/10.1016/j.automatica.2016.02.036 ，作者全文 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。核对摘要、集合表示与精确交/投影能力；本轮只使用区间外包，未实现 CZ 相关性收紧，不能把盒准入说成新 CZ 算法。两篇均为历史84篇中的定向复核，不新增去重篇数。

## 复现与证据等级

`PYTHONPATH=verification python -m unittest verification.test_four_tick_affine_backup -v`

`python verification/check_four_tick_affine_backup.py --output results/four_tick_affine_backup_20261030/checks.json`

在 Python 3.13 标准库 `fractions.Fraction`、与远端配置和 Run202 行逐字段核对的本地最小镜像下：**14/14 新增测试通过**。测试覆盖初始/扰动极点枚举与生成元支持一致、任意推力内点、输入区间交、第四拍相对阶、成功/缺包差异和真实违约顶点。没有完整 Git checkout；未运行历史回归测试或 GitHub CI。上传前须核对源码 Blob SHA、远端依赖字段、结果文件；证据等级为 `EXACT_RATIONAL_CONDITIONAL_FOUR_TICK_ADMISSION`，而非 Gate A 安全证书。

**Gate A 仍 blocked。下一唯一优先任务：** 在真正可达的测量条件化 SMF/CZ 后验上实现滚动安全过滤器，使用控制后观测分支和未来推力的统一因果策略，并在候选 backup 失效时产生可复现反例；随后再尝试终端集合和递归可行性证明。不要把任意四拍成功当作长期安全。
