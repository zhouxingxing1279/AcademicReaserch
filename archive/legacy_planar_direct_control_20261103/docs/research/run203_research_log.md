# Run203：15-mode 成功/缺包后验的三拍鲁棒控制准入与非不变性见证

日期：2026-10-30。起点 `main=e019946758481aa82f62294f8c81dedaabb7e0df`（Run202）。唯一问题：Run202 的条件化速度严格外包能否在**当前推力可见、未来推力任意跳变、位置包成功/缺失分支**的真实硬约束下，给出可复核的控制准入，而不是仅比较滤波器宽度？

## 合同、时序和量词

使用 `configs/planar_baseline.json` 四状态 `(p,v,phi,omega)` 横向—姿态 Euler 模型：`h=1/50 s`、`J=1/50 kg m²`，`p+=p+h v`、`v+=v-h T phi+h r`、`phi+=phi+h omega`、`omega+=omega+h tau/J`，`|r|<=47/25+243T/16000`。真实硬约束：`|p|<=5m`、`|v|<=3m/s`、`|phi|<=0.45rad`、`|omega|<=2rad/s`、`|tau|<=0.08N m`。历史推力固定为低/高端点，当前 `T0` 可见；未来 `T1,T2` 可在 `[4.905,14.715]N` 中任意选择，不假设缓变。选择当前 `tau0` 后，接下来两拍设 `tau1=tau2=0`，每拍独立横向 residual。

位置包决策来自冻结的15-mode图：在5 tick，`mode4 -> mode0(success)/mode5(miss)`；在10 tick，`mode9 -> mode0(success)/mode10(miss)`；在15 tick，**只能** `mode14 -> mode0(success)`，不得伪造第15拍的缺包边。所检查的3拍内均无新的位置包；姿态/角速度虽然每拍观测，本轮保守地不利用其后验收缩。控制选择发生在**已知本次包结果之后**；这不是前一拍控制必须对所有后继边相同的完整因果策略证明。

使用 Run202 归档的精确有理可靠外包：成功包时 `|p|<=sigma_p=0.02` 且 `|v|<=min(返包消元上界,先验区间上界)`；缺包时使用前向区间可靠外包；两类均取 `|phi|<=0.005`、`|omega|<=0.01`。**后验的真实 CZ 相关性被丢弃**，因此这里的区间是可靠但保守的控制输入集合。未使用 Run202 的浮点 CZ LP 支持值。

## 精确三拍可达外包与证明范围

给定当前盒 `B0` 和候选力矩 `tau0`，以有理数生成元递推 `x+ = A(T)x+B tau+E r`，每拍增加独立 residual 生成元。固定推力序列的各坐标最大绝对值精确等于 `|center_i|+sum_j |G_ij|`。在该冻结模型下，姿态/角速度不依赖推力，`p,v` 的中心和各生成元对未来 `T1,T2` 分别仿射，残差半宽也对 `T` 仿射。因此每个坐标支持函数是推力矩形上的凸函数，其最大值在四个端点组合之一达到；枚举 `(Tmin/Tmax)^2` 即覆盖**所有连续未来推力**，不是只采样四种未来。

对对称盒，第三拍速度支持具有可独立核查的闭式：

`R_v3 = r_v + h[(T0+T1+T2)r_phi + h(T1+2T2)r_omega + d(T0)+d(T1)+d(T2)] + (h³/J)T2|tau0|`。

初始力矩 `tau0` 对 `v1,v2` **没有作用**，到 `v3` 才出现；对 `p1,p2,p3` 均没有作用。该相对阶限制解释了为什么三拍硬约束检查不能替代稳定化控制器设计。

## 结果（零力矩三拍，全部使用严格有理外包）

| 包时刻 | 历史推力 | 分支 | 第3拍位置最大绝对值(m) | 第3拍速度最大绝对值(m/s) | 原硬约束 | 假设速度阈值0.65 |
|---|---|---|---:|---:|---|---|
| 10 | 低 | success | 0.04752 | 0.54453 | PASS | PASS |
| 10 | 低 | miss | 0.10783 | 0.62264 | PASS | PASS |
| 10 | 高 | success | 0.04898 | **0.57028** | PASS | PASS |
| 10 | 高 | miss | 0.11393 | **0.66621** | PASS | FAIL |
| 15 | 低 | success | 0.04945 | 0.57682 | PASS | PASS |
| 15 | 高 | success | 0.05151 | 0.61246 | PASS | PASS |

5 tick成功/缺包共4个附加工况亦通过。10种合法分支历史的所有中间拍均满足原硬约束；枚举的5个 `tau0 ∈ {-0.08,-0.04,0,0.04,0.08}` 都通过原硬约束。**0.65m/s只是为了观察信息收益而定义的诊断阈值，不是配置中的硬约束、终端集或已证明的tube预算**；它显示10 tick高推力返包会改变该诊断的准入判定，但不能据此宣称实际 MPC 可行域增大。

### 必须保留的反例

零力矩并非不变 backup。取真实初态 `(0,0,0,0)`、恒定高推力 `T=14.715N`、`tau=0`、每拍合法最大正 residual `r=2.1034840625m/s²`，姿态观测恒为零、位置包可如实报告非零位置。第72拍真实 `v=3.02901705m/s > 3m/s`，当时 `p=2.1506021055m < 5m`。这是**对永久零力矩安全性的明确反例**，不否定存在其他反馈策略或模式相关终端集合。三拍的局部准入不能当作递归可行性证明。

## 文献依据、创新边界与研究收敛

1. Lorenzetti & Pavone (2020), *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*, ECC, DOI https://doi.org/10.23919/ECC51009.2020.9143979，作者版 https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf 。本轮定向核对 Section IV-C/D/E 的式(9)–(13)及 Proposition 1：有限时域收紧需要终端不变控制和误差RPI才能推出递归可行与鲁棒约束保证。本轮仅有3拍外包，尚不满足其充分条件。
2. Athanasopoulos, Smpoukis & Jungers (2017), *Invariance in Constrained Switching*, arXiv https://arxiv.org/abs/1702.00598 ；本轮核对摘要、Introduction 的图约束切换和不变多集合概念，并对照仓库历史Run135/136的更深阅读记录。其图索引不变多集合启发下一轮的模式相关终端候选；不能不核查稳定性、扰动集合假设就直接引用外逼近定理。

本轮精确生成元递推、端点枚举和三拍准入均为已知线性集合传播的合同化审计，**不主张算法原创**。课题可行性方面已建立一个可用的硬约束有限时域入口，但尚未找到稳定化 backup、15-mode controlled invariant family 或 shifted-plan 递归可行性证书。创新点应落在**观测条件化的控制相关收紧与可认证的模式相关闭环策略**，而不是 CZ 的定义或简单枚举。

## 可复现性、测试与提交

新增 `verification/check_mode_indexed_backup_admission.py`、`verification/test_mode_indexed_backup_admission.py`、`results/mode_indexed_backup_admission_20261030/checks.json`。运行：

```bash
PYTHONPATH=verification python -m unittest verification.test_mode_indexed_backup_admission -v
python verification/check_mode_indexed_backup_admission.py --output results/mode_indexed_backup_admission_20261030/checks.json
```

本地 Python 3.13.5 标准库 `fractions.Fraction`，以远端配置关键字段和 Run202 精确结果镜像运行，**9/9新增测试通过**，包括分支合法性、生成元与128个极点见证一致、任意推力内点检查、闭式公式、信息分支差异及72拍反例。首次测试有1项失败，仅因测试期望的分支排序与实现排序相反；修正测试后9/9通过。未获取完整仓库checkout，故尚未执行完整历史回归/CI；严格结论限于冻结四状态合同与镜像字段一致性。

**Gate A仍blocked。下一唯一任务：** 从3拍局部准入转向可控模式相关终端候选：构造至少一个非零、基于可见姿态/角速率及条件化SMF的因果反馈力矩，并检验所有成功/缺包后继和任意推力下的一步集合包含；若失败，保留最小反例并判断是否应改用有限时域安全过滤器作为硕士课题切入点。
