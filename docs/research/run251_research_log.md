**Run251完整checkout/CI/合并核验（2026-11-01 UTC）：** 研究PR #76 https://github.com/zhouxingxing1279/AcademicReaserch/pull/76 基于main `bf323f99a6b8dcd8a96d17dcd70de734e20ae972`；合并前compare ahead=8/behind=0，7个预期文件。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41355983604 **completed/success**，Python3.13完整checkout Run249/250/251聚焦**27/27测试通过、无跳过**（0.952s），源码编译、精确JSON逐字对比、artifact `run251-exact-certificate` 上传均成功；已读取job日志核对实际测试数。通过expected head `d6d06582347e29f301743cc5fd57bf63869f780b` 非强制squash合并到main `913a79ff69a453245c4f6b90d030503925bb8283`，重新读取main SHA及源码/证书/日志Blob确认落地。**本轮未能独立读取push触发的main Actions运行状态**，不能宣称main CI成功；上述PR CI已在完整checkout验证代码。此补记仅更新文档，不修改算法或数学证书；全仓库历史回归、无限递归可行、六状态安全及20ms WCET均未认证。

---

# Run251 — 有噪位置测量下不可区分扰动导致的速度后验宽度下界（2026-11-01）

**基准远端main：** `bf323f99a6b8dcd8a96d17dcd70de734e20ae972`（已含Run250和背景任务第4轮）。**唯一研究问题：** Run249已有55拍有界SMF＋网格MPC＋安全过滤闭环，但尚未得到无限时域终端信息状态。首先检查一个更基础的必要条件：在每5拍都有成功位置包的有利情况下，是否仍存在合法、观测不可区分但真实速度相差显著的扰动历史？若存在，终端信息集合不能假定速度已被精确识别。

## 1. 冻结动力学和精确构造

使用Run249冻结四状态显式Euler模型 `x=(p,v,phi,omega)`，`h=1/50 s`、固定 `T=981/100 N`、`|r_k|<=R=3246383/1600000 m/s²`、`|tau|<=2/25 Nm`；`p+=h*v`、`v+=h*(-T*sin(phi)+r)`、`phi+=h*omega`、`omega+=h/J*tau`。约束 `|p|<=5,|v|<=3,|phi|<=0.45,|omega|<=2`；每拍有噪姿态/角速度观测，位置每5拍一次成功机会且噪声半宽 `1/50=0.02m`。

选**同一个合法精确初态** `x0=(0,0,0,0)`、同一合法控制 `tau_k=0`，令两个合法扰动历史 `r_k^+=R*d_(14-k)`、`r_k^-=-R*d_(14-k)`。下标 `w=14-k` 是该扰动对第15拍位置的Euler权重；`d_w=1`（w=0..9）、`d_10=1/2`、`d_w=-1`（w=11..14）。于是：

- `sum_(w=0)^14 w*d_w = 0`，故两条轨迹第15拍位置**精确相同**，且同为0。
- `sum d_w = 13/2`，故第15拍速度差 `v15^+-v15^- = 2*h*R*(13/2) = 42202979/80000000 = 0.5275372375 m/s`；两条速度分别为 `±42202979/160000000 = ±0.26376861875 m/s`。
- 两条轨迹在第5/10/15拍的位置分别为 `±3246383/400000000`、`±22724681/1600000000`、`0`，绝对值分别约0.008116、0.014203、0，均小于位置噪声半宽0.02。因此即使**全部三个位置包成功**，也能取共同读数 `y_p=0`，两条真实轨迹均与该读数一致。姿态/角速度都为0，逐拍观测也完全相同。全部中间真实状态均满足硬约束。
- 结论：对这一**真实可发生的观测历史**，任何保证真值包含的SMF后验 `S15` 都必须同时包含这两个速度值，故其速度投影直径至少 `0.5275372375m/s`、半宽至少 `0.26376861875m/s`。这不是对每一个后验的统一下界，更不是任何安全控制策略不可能存在的证明。

**限定最优性证明：** 在固定共同初态、成对反号扰动、精确相同终点位置的受限LP `max sum d_w`，约束 `sum w*d_w=0, |d_w|<=1` 下，取对偶乘子 `lambda=1/10`，有 `sum d_w = sum (1-w/10)*d_w <= sum |1-w/10| = 13/2`。上述有理数构造达到等号，故在**这个受限LP**中原始/对偶最优；不能宣称是有噪位置SMF全局最小宽度或所有控制律的性能极限。相同方法得到5拍和10拍的必要半宽分别为 `22724681/240000000≈0.09468617` 与 `14376839/80000000≈0.17971049m/s`。

**因果性备注：** 横向残差不进入姿态/角速度动力学；在两个观测历史相同的情况下任何因果控制器必然给出相同力矩，公共 `-T sin(phi)` 对速度和位置差分相消。上述明确验证的物理安全见证使用 `tau=0`，不据此声称任意控制律在两条路径上都保持安全。

## 2. 文献分节复核（唯一日志去重98篇不变）

Liren Yang, Necmiye Ozay (2021), *Safety Control Synthesis for Systems with Missing Measurements*, 7th IFAC Conference on Analysis and Design of Hybrid Systems (ADHS), *IFAC-PapersOnLine*, pp.97–102, DOI https://doi.org/10.1016/j.ifacol.2021.08.481 ，作者公开正文 https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。本轮实际重读§3式(3)–(7)的丢包自动机/因果控制、§4.2–4.4的string automaton、Proposition 4/5的产品系统不变性与安全合成。其成功包给**完整无噪状态** `y=x`，丢包时 `y=∅`；没有本仓库的每拍姿态有噪、位置每5拍有噪、速度永不直接测量的SMF。论文说明控制不得预知未来包，支持本轮使用共享观测历史的因果不可区分论证，但本轮数值下界为**独立推导**，不是该文定理或论文原始结论。历史Run248已分节读此文，本轮重读不新增去重数。

## 3. 代码、测试和可复现证据

- `verification/check_velocity_indistinguishability.py`：标准库Fraction精确计算5/10/15拍的扰动原始/对偶证书、真实双轨迹和所有位置读数噪声一致性。
- `verification/test_velocity_indistinguishability.py`：7项单测，包括原始/对偶相等、精确速度间隔、各中间状态约束、全包成功不可区分、真实Run249区间SMF集成检查。
- `results/velocity_indistinguishability_20261101/checks.json`：有理数证书归档。
- `.github/workflows/run251-velocity-indistinguishability.yml`：完整checkout下执行Run249/250/251聚焦测试、编译和JSON逐字对比。

本地隔离Linux/Python3.13执行 `PYTHONPATH=. python -m unittest -v test_velocity_indistinguishability`：**6通过、1项因隔离环境缺Run249源码显式跳过**；`python -m py_compile`通过；`python check_velocity_indistinguishability.py --output checks.json`生成归档。完整checkout下的Run249集成测试和GitHub Actions结果须独立核验后再记录；不将本地隔离测试冒充全仓库回归。

## 4. 课题判断与唯一下一步

**正向价值：** 首次在本冻结四状态配置上用精确可达轨迹及对偶证书量化“即使所有位置包成功也无法精确识别速度”的必要不确定性，给候选SMF/CZ终端信息状态提供可检验的下界。其科学性质是部分观测信息限制，而非新的SMF算法或安全控制律；不能单独作为硕士创新性。

**仍未完成：** Run249固定55拍安全与Run250零备份67拍上限不变；没有非空后继闭合的终端信息状态、无限时域输出反馈递归可行性/稳定性、六状态保证或20ms WCET。Gate A继续blocked。

**下一轮唯一优先任务：** 将本轮15拍共同观测的双轨迹速度纤维纳入候选终端信息状态的**共享因果前驱检验**，尝试构造一个对这两种隐藏速度都合法且后继安全的非零控制与测量分支闭合证书；若无正向证书，记录明确反例而非继续扩大固定截止时间。
