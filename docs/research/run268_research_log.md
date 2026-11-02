# Run268 — 第60拍全部合法包模式的测量条件化速度—姿态关联条带（2026-11-02）

## 1. 远端基准与唯一瓶颈

基准远端 main SHA `a531865b494e9658a66915156e6f13186fd12877`。本轮读取 `docs/research/CURRENT_CHECKPOINT.md`、唯一 `docs/literature/PAPER_READING_LOG.md`、`docs/research/model_selection/MODEL_SELECTION_EVIDENCE.md`、Run260/263/266/267研究日志、Run260/263验证源码及归档、真实 `configs/planar_baseline.json`。Run267证明第60/75拍可靠外包均通过三拍必要速度守卫，但没有保留速度、姿态、角速的测量关联。**唯一问题：在不枚举连续读数、不假设未来读数为零的情况下，能否给第60拍全部11条合法success/miss分支构造可计算且可靠的关联信息约束？**

本轮不开发新MPC控制器、不尝试15拍终端回返，不更改六状态物理首选。四状态冻结模型仅作数学基线。

## 2. 定义、精确运动学恒等式及新条带

冻结离散Euler真值：
`p[k+1]=p[k]+h*v[k]`，
`v[k+1]=v[k]+h*(-T*sin(phi[k])+r[k])`，
`phi[k+1]=phi[k]+h*omega[k]`，
`omega[k+1]=omega[k]+h*tau[k]/J`。
`h=J=1/50`、`T=981/100 N`、`|r|<=R=3246383/1600000`、位置量测 `y_k=p_k+e_k`, `|e_k|<=eps_p=1/50`。继承Run260真实共享输入 `tau[k]=0` 对全部 `k=35,...,59`，因此 `omega_i=omega_60` 且 `phi_i=phi_60-(60-i)h*omega_60` 对 `35<=i<=59` **精确成立**。Run260第60拍可靠外包对两类历史均给 `|phi_60|<=1/125`、`|omega_60|<=1/100`；不能把这些界扩展到任意初始历史。

取最近两个成功位置读数时刻 `s<t<=60`（合法间隔 `n=t-s in {5,10,15}`），令 `w_i=(i-s+1)/n`（`s<=i<t`）及 `w_i=1`（`t<=i<60`）。由Euler求和：
`v_60=(p_t-p_s)/(nh)+h*sum_{i=s}^{59} w_i[-T sin(phi_i)+r_i]`。

定义 `A=sum w_i`、`B=sum w_i(60-i)`、`D=(y_t-y_s)/(nh)`。利用全局 `|sin z-z|<=|z|^3/6`，获得对**全部非空有噪观测纤维**可靠的仿射条带：
```
|v_60 + h*T*A*phi_60 - h^2*T*B*omega_60 - D| <= E + Q,
E = 2*eps_p/(n*h) + h*R*((n+1)/2 + (60-t)),
Q = h*T*sum_i w_i*(1/125+(60-i)*h/100)^3/6.
```
系数与 `E,Q` 全用Python `Fraction` 精确计算；`Q` 是解析正弦Taylor余项的**可靠上界**，并非数值拟合。当前姿态/角速量测再以 `|phi_60-y_phi|<=0.005`、`|omega_60-y_omega|<=0.01` 与此条带及Run260可靠外包相交；读数 `y_s,y_t,y_phi,y_omega` 为任意一致实数，代码**未假设其为零**。

**量词与适用边界：** 对Run260固定第45拍SMM/MMS历史、未来11种合法位置包模式、全部非空一致有噪读数及全部合法扰动，真实 `(v_60,phi_60,omega_60)` 都落在相应观测条件化条带中。条带是后验的**外包约束**，不是精确SMF后验，也不是可生存终端集合。其可靠性依赖35–59拍零力矩和Run260第60拍可靠姿态盒；改变力矩策略时必须重新推导已知力矩历史项。

## 3. 分支数值证书与负面结果

- SMM起始：4种未来合法分支；MMS起始：7种；共11种。每支都存在最近两次成功位置包 `s,t`，脚本按观测自动机逐项输出 `A,B,E,Q`。
- `SMM -> SMM`：`s=35,t=50,A=18,B=541/3,E=103652341/120000000≈0.8637695083m/s`，`Q≈6.1505e-7m/s`。
- `MMS -> SMM`：`s=45,t=50,A=13,B=92,E=74202979/80000000≈0.9275372375m/s`，`Q≈3.6204e-7m/s`。
- `MMS -> SMS`：`s=50,t=60,A=11/2,B=22,E=67710213/160000000≈0.4231888313m/s`，`Q≈1.2371e-7m/s`。
- 全11支 `E<1m/s`、`Q<1e-5m/s`。这些是**以测量差为中心、条件化于姿态的条带半宽**，不能直接当作最终速度投影半宽、平均后验宽度或安全裕量。
- 对零位置读数的说明性纤维，SMM/SMM的条带可剔除Run260无条件速度盒的某些角点；这只是外包几何收紧，不证明完整后验体积减少、信息终端回返或MPC性能改善。

**负面结论：** 现有Run267必要守卫通过，仍无法由此条带证明15拍共享因果回返；条带只使用最近两次成功位置读数，未综合全部姿态读数、较早成功位置条带、扰动时序相关性和完整SMF/CZ预测更新，因此不宣称精确后验。

## 4. 新论文正文阅读与技术边界

Alesi A. de Paula, Davide M. Raimondo, Guilherme V. Raffo, Bruno O. S. Teixeira, *Set-based state estimation for discrete-time constrained nonlinear systems: An approach based on constrained zonotopes and DC programming*, **Automatica 159 (2024), 111401**, DOI https://doi.org/10.1016/j.automatica.2023.111401；作者公开预印本 arXiv:2211.05912v1 https://arxiv.org/pdf/2211.05912 。2026-11-02实际阅读预印本PDF pp.1–7的§2–5（Theorems 1–2、Corollary 1、Algorithm 1、Table 1及两数值案例）与p.8 §6；未逐页比对期刊终版，**正文分节已读，不是独立复现**。

论文研究带有界过程/量测噪声、状态线性不等式及非线性等式约束的离散非线性系统，提出CZDC：非线性预测、量测交集、可行域交集、非线性一致性和降阶；以DC规划界定线性化余项并与CZ表示结合。Theorem 1/2分别给预测和量测更新的外包包含，**不是MPC稳定性/递归可行性定理**。§5.1为两状态非线性过程仿真；§5.2为四元数飞行机器人**姿态估计仿真**，不是四旋翼MPC实飞，且未涉及位置失测自动机。Table 3报告姿态案例平均每步CZDC 3.58s、CZFO 39.8s、CZMV 1.76s（作者MATLAB/旧CPU环境），**不能作为20ms实时控制器**。可复用预测—量测—约束—降阶的分层结构及CZ广义交集；本轮解析仿射条带可作为其量测一致性约束的低维接口，但尚未实现CZDC。

## 5. 工件、实际测试与证据等级

新增 `verification/check_run268_observation_fiber_strip.py`、`verification/test_run268_observation_fiber_strip.py`、`results/run268_observation_fiber_strip_20261102/checks.json`、`.github/workflows/run268-observation-fiber-strip.yml`。本地Linux Python 3.13.5执行：
`PYTHONPATH=. python -m unittest -v test_run268_observation_fiber_strip.py`：**6/6通过**；`python -m py_compile *.py`：通过；`python check_run268_observation_fiber_strip.py --output checks.json`：生成11支精确有理数JSON。6项测试包括Euler恒等式的有理数精确验证、线性化版本的有理数残差、解析余项界、11包模式及非线性随机示例（示例仅为统计/浮点交叉检查，不代替解析证明）。本地DNS不能访问github.com，完整仓库Run26x回归及真实配置核验以PR CI实际结果为准；CI另检查归档JSON逐字一致。

**证据等级：** 在冻结离散Euler真值下，测量条件化仿射条带的解析可靠包含 + 精确系数数值证书；没有完整SMF/CZ后验、MPC优化、15拍反馈终端RCI、无限递归可行、鲁棒稳定、六状态物理安全或20ms WCET。**Gate A=blocked**。六状态平面物理首选仍为条件性，四状态数学基线不变。

## 6. 下一轮唯一优先任务

将本轮11支观测条件化 `(v,phi,omega)` 条带与Run260第60拍可靠状态盒、Run266三拍必要守卫相交，针对**同一观测纤维**构造可计算的15拍共享因果安全回返**充分条件或明确反例**。不得把必要条件通过、条带变窄或有限开环安全误写成终端信息RCI。
