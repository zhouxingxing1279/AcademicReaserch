# Run202：四状态条件化 SMF 的精确 CZ 递推与返包后速度信息收益

日期：2026-10-30。起点 `main=93f0638f3ab65e683b12ce60daf543744748e8ba`（Run201）。唯一问题：在四状态横向—姿态合同中，持续姿态观测与最长15 tick位置丢包下，**位置返包究竟能否严格收紧未直接测量的速度后验**？是否需要先开发新的集合算法？

## 合同和可复现实现

读取 `configs/planar_baseline.json`，状态 `(px,vx,phi,omega)`，`h=1/50 s`、`J=1/50`，`px+=px+h vx`、`vx+=vx-h T phi+h r_x`、`phi+=phi+h omega`、`omega+=omega+h tau/J`，`|r_x|<=47/25+(243/16000)T`；`T=4.905` 或 `14.715N` 固定可见、`tau=0`。初始位置/速度半宽为 `0.02m/0.1m/s`；每 tick 接收有界噪声姿态和角速率，tick0与tick5/10/15的返包时刻收到位置观测（其余 tick 缺包）。这仅覆盖**固定推力的合法观测历史**，没有未来任意推力、反馈力矩或六状态结论。

新增 `verification/check_four_state_conditional_smf.py`，以 `fractions.Fraction` 精确表示 CZ `(c,G,A,b)`。线性预测精确传播所有生成元并增加独立 `r_x` 生成元；每次测量添加零状态生成元 `nu` 及等式 `e_i'(c+G xi)+sigma nu=y`、`|nu|<=1`，**精确表示测量一致集合交**。同时实现独立的轴对齐区间外包；对 CZ 用 SciPy/HiGHS 浮点 LP 求投影支持，仅作 `NUMERIC_CHECK`，不将浮点最优值宣称为严格安全界。真实状态和生成元见证使用分数精确重放；另外测试非零初态、扰动、噪声。

## 新的严格推导：返包后的速度界

设固定推力 `T`、`a_i=-T phi_i+r_i`，在位置观测 `y_p(0)=y_p(n)=0`、每 tick 姿态观测 `y_phi(i)=0` 下，`|p_0|,|p_n|<=sigma_p=0.02`、`|phi_i|<=sigma_phi=0.005`。由状态递推消去未知 `v_0`：

`v_n=(p_n-p_0)/(n h)+(h/n) sum_{i=0}^{n-1}(i+1)a_i`。

因此，对**所有**与该观测历史及独立扰动合同一致的轨迹，有精确有理上界：

`|v_n| <= 2 sigma_p/(n h)+h(n+1)/2 * [T sigma_phi + d(T)]`。

与条件化区间传播的可靠上界取最小，仍是严格外包。它依赖返包的实际值、固定已知推力、每 tick 的姿态观测与初始一致性，不是无条件终端不变集。Run201的不可辨识对给出返包**之前**速度半宽必要下界 `v_0+n h d(T)`，位置半宽必要下界 `p_0+n h v_0+h² n(n-1)d(T)/2`；返包之后不可继续套用该无位置测量下界。

| 连续丢测间隔 | 推力 | 返包前速度必要半宽 m/s | 返包前区间可靠上界 m/s | 返包后严格上界 m/s | 严格收紧比例 |
|---|---|---:|---:|---:|---:|
| 5 | 低 | 0.29545 | 0.29790 | 0.29790 | 0.0% |
| 5 | 高 | 0.31035 | 0.31771 | 0.31771 | 0.0% |
| 10 | 低 | 0.49090 | 0.49580 | 0.41769 | 15.8% |
| 10 | 高 | 0.52070 | 0.53541 | 0.43948 | 17.9% |
| 15 | 低 | 0.68635 | 0.69371 | **0.44998** | **35.1%** |
| 15 | 高 | 0.73105 | 0.75312 | **0.48166** | **36.0%** |

精确 CZ 浮点 LP 在15 tick返包后的速度支持分别约为 `±0.44685` 与 `±0.47656 m/s`，与上述**独立严格上界**一致，但其差额不是已认证的保守性改进。返包前位置必要半宽 `0.13209/0.13835m`，可靠区间外包 `0.13312/0.14144m`；该特定历史中扰动主导位置宽度，单纯更换集合表示的空间有限。返包后速度相关性收益更显著，值得在控制准入中评估。

注意 `configs` 中 nominal `vx∈[-0.25,0.25]` 是**名义状态域**，不能当作已经认证的估计误差 tube 预算。即使返包前速度信息必要半宽大于0.25m/s，也**不能**推断原控制约束不可行；实际硬约束是 `|vx|<=3m/s`，本轮未证明其违反。

## 论文依据及创新边界

Scott、Raimondo、Marseglia、Braatz（2016），*Constrained zonotopes: A new tool for set-based estimation and fault detection*，*Automatica* 69:126–136，DOI `10.1016/j.automatica.2016.02.036`，原文 Definition 2/3、Section 3.1 的 generalized intersection 和 CG-rep。精确 CZ 交运算**属于已知方法**，本轮只是冻结合同的可靠实现。Lorenzetti & Pavone（2020），*A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*，ECC，DOI `10.23919/ECC51009.2020.9143979`，Section II/IV 关于误差 RPI、约束收紧、终端闭合：估计集合的精确性不等于 MPC 递归可行性。

## 验证与局限

本地 Python 3.13.5，`numpy==2.3.5`、`scipy==1.17.0`，在与远端关键字段核对的最小配置镜像中运行：

```bash
PYTHONPATH=verification python -m unittest verification.test_four_state_conditional_smf -v
python verification/check_four_state_conditional_smf.py --output results/four_state_conditional_smf_20261030/checks.json
```

7/7新增测试通过；6组合法返包历史，包含非零初始状态、噪声和扰动的精确 CZ witness 测试。运行环境使用**字段镜像**而非完整远端 checkout，故还需要在真实仓库运行回归/CI。`NUMERIC_CHECK` 的 LP 不承担严格保证；严格结论仅为有理代数、独立扰动见证和上式条件化外包。

**Gate A仍 blocked：** 未合成四状态控制器、受控 RCI/终端集合、旧计划移位证明，六状态闭环也未完成。

**下一唯一优先任务：** 将本轮“返包后速度严格收紧”嵌入 mode-indexed 控制可行性检查，特别是对成功/缺包两类后继和未来任意推力都成立的 backup/terminal 条件；比较使用 CZ 相关性与仅区间收紧时的可行性和计算成本，失败保留反例。
