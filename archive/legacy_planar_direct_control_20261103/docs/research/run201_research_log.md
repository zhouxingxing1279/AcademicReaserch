# Run201：四状态横向—姿态合同的丢测不可辨识位置宽度下界

日期：2026-10-30。接续已核实 main=`25aa83bfe2e0b06d7568a10751ebcb043701ad77`（Run200）。**本轮唯一问题**：标量 SMF-MPC 证明的“后验包含→移位→终端闭合”接口迁移到四状态降阶模型时，原有 5/10/15 tick 位置测量间隔究竟要求多大横向位置不确定性余量？

## 原合同及证明范围

读取 `configs/planar_baseline.json` 与 `verification/check_scheduling_visible_predecessor.py`：四状态 `(p_x,v_x,phi,omega)`，`h=1/50 s`，`J=1/50`，`T∈[981/200,2943/200] N`；`p^+=p+h v`、`v^+=v-hT phi+h r_x`、`phi^+=phi+h omega`、`omega^+=omega+(h/J)tau`，`|r_x|≤d(T)=47/25+(243/16000)T`。初始 prior 横向半宽 `p_0=1/50 m`、`v_0=1/10 m/s`，`phi/omega` 每 tick 有界观测，位置每 5 tick 有一次机会，最多连续丢两个位置包，允许的返回间隔为 5/10/15 tick。当前推力可见，未来推力不得假设有非平凡变化率。

**命题（冻结降阶不确定性合同下的必要宽度，DERIVED）：** 在时刻0的后验同时包含两条初始轨迹 `p=±p_0,v=±v_0,phi=omega=0`，且随后连续 `n` tick 不收到横向位置或速度信息时，对任意仅依据共同可见历史因果选取的 `T_k,tau_k`，存在两个具有相同可见姿态/角速率历史、相同控制历史且均满足冻结扰动包络的真实状态候选，其末端横向位置间隔至少为
`2 [p_0+n h v_0+h²∑_{i=0}^{n-1}(n-1-i)d(T_i)]`。
所以任何包含全部一致状态的 SMF 后验（及用于控制的可靠外包）在该共同历史下横向半宽不得小于括号内的量；由于 `d(T)` 随 `T` 单调增加，`T=T_min` 全程给出任意允许因果推力策略均不可突破的下界。

**证明：** 令两条候选的初始横向状态取正负端点，所有 `phi,omega` 与竖直状态相同；第0次位置观测可取 `y_{p_x}=0`，对应噪声分别为 `∓p_0`，均在 `±0.02m` 传感器界内。随后缺失位置包，持续可见的 `phi,omega` 在两条候选上完全相同。因控制律因果且可见历史相同，`T_k,tau_k` 相同；每 tick 独立扰动取 `r_{x,k}^{±}=±d(T_k)`。于是 `Δv_{k+1}=Δv_k+2h d(T_k)`、`Δp_{k+1}=Δp_k+hΔv_k`，且 `Δv_0=2v_0,Δp_0=2p_0`，逐步展开即得。此为**模型包络的最坏情况**，并不声称解析气动真值一定同时实现每个独立扰动端点。

## 可复现精确检查

新增 `verification/check_lateral_dropout_support_floor.py`、`verification/test_lateral_dropout_support_floor.py` 和 `results/lateral_dropout_support_floor_20261030/checks.json`。脚本从冻结配置读取常数、用 `fractions.Fraction` 推进两条不可辨识轨迹，并用线性像+独立扰动生成元计算固定推力序列下的**无测量先验**精确 zonotope 横向投影 support（后者是无观测外包，不等于有姿态观测后的最小后验）。覆盖 `n=5,10,15`、低/高/交替推力共9个合同。

| gap tick | 低推力不可辨识半宽 (m) | 高推力不可辨识半宽 (m) | 高推力无测量先验半宽 (m) |
|---|---:|---:|---:|
| 5 | 0.03781798 | 0.03841394 | 0.03872001 |
| 10 | 0.07518090 | 0.07786271 | 0.07932833 |
| 15 | 0.13208878 | 0.13834633 | 0.14197211 |

在最大15 tick缺测下，**至少约0.13209m** 的横向半宽是本冻结不确定性合同中任何仅依赖现有观测的因果控制器都无法通过改变 SMF 几何消除的部分；高推力固定序列下下界约0.13835m。此数值远小于全局 `|p_x|≤5m`，**不能**据此宣布硬约束不可行、终端集合不存在或控制器物理权限不足。若某候选 terminal/tightening 接口给出小于该下界的共同历史横向容许半宽，则该候选接口在这个可达历史上不能成立；还须检查其初始信息集合和终端中心是否匹配。

执行（Python 3.13.5）：
```bash
PYTHONPATH=verification python -m unittest verification.test_lateral_dropout_support_floor -v
python verification/check_lateral_dropout_support_floor.py --output /tmp/lateral_dropout_support_floor.json
```
本轮在隔离的配置字段镜像（与 GitHub 冻结配置逐项核对）上运行 **7/7** 测试通过；9组分数算术核查通过。远端代码会直接读取完整 `configs/planar_baseline.json`；本轮未在完整远端仓库上执行全部历史测试，不能虚报 CI 全绿。归档结果不构成 MPC 优化、闭环轨迹统计或 Gate A RCI 证书。

## 文献复核与创新边界

精读 Lorenzetti & Pavone，*A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*（arXiv:1911.07360v2，2020），Section II 的可观测性假设、Section IV-D 式(10)-(11)的终端闭合、Section IV-E/F 式(12)-(13)及 Proposition 1 的耦合误差 RPI/约束收紧：https://arxiv.org/pdf/1911.07360 。其证明说明：**可靠估计误差集合、稳定 ancillary feedback、终端条件及收紧约束缺一不可**。该论文是 LTI、固定截面 RPI 和持续测量条件；不能直接当作当前间歇位置/推力调度合同的充分证书。本轮的不可辨识下界是已知 reachability/support 原理在冻结模型上的审计应用，不宣称新集合算法或新控制理论。

## 对 Run200 三个接口的回答与下一步

- 后验包含：对本冻结合同可写出**必要**的横向支持半宽，并证明姿态/角速率测量不能辨别独立 `r_x` 的对称历史；但本轮未实现四状态条件化 SMF 的完整后验。
- 旧计划移位：缺少允许当前 `T` 可见、未来 `T` 任意跳变时的可行 backup policy，**未证明**。
- 终端后继不变：Run199 的 affine-offset SOCP 只有数值不可行证据；**仍 blocked**。
- 下一唯一任务：在保持15-tick合法返回图和实际 `W(T)` 下，构造**含姿态测量更新的四状态条件化 SMF 可复核后验外包**，逐个检验此必要宽度与候选 tightening/terminal 集的兼容性；再考虑控制合成，不把有限轨迹成功当作递归可行性。

证据级别：必要宽度为 `DERIVED`（在冻结降阶独立扰动模型与可达初始历史下）；9组测试为 `EXACT_CHECK`；原四状态/六状态安全及闭环 MPC 仍 `OPEN`。
