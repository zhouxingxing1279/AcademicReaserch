# Run214：滚动历史支持界诊断第193拍拒绝（2026-10-31）

**基准 main：** `6debbe5282fed27ee5478381f495951d30bc95dc`（Run213）。**唯一瓶颈：** 第192拍历史速度收紧恢复准入后，第193拍为什么仍拒绝？能否用因果滚动的有限历史线性约束消除该拒绝？

## 1. 模型、方法与严格证据

继承冻结四状态 Euler 模型、15拍位置成功返包、连续姿态/角速度观测、已知当前推力、推力相关残差上界及 Run208/210 控制过滤器。用第192拍前的 Run213 历史界恢复一次合法力矩，精确重放到第193拍控制前。第193拍仅使用此前已收到的6个位置包（105、120、135、150、165、180）及截至191拍的姿态观测与实际推力，**不使用未来量测**。

对任意三个成功位置包 `a<b<c`，选取系数 `c_a+c_b+c_c=0`、`H[(b-a)c_b+(c-a)c_c]=1`，有精确 Euler 恒等式：

`v_k = c_a p_a + c_b p_b + c_c p_c + sum_{i=a}^{k-1} w_i a_i`

其中 `w_i=H-c_b H² max(b-1-i,0)-c_c H² max(c-1-i,0)`，`a_i=-T_i phi_i+r_i`。将 `p`、`phi` 的有界量测误差及 `r_i` 的有界残差分别外包，得到可靠的速度支持区间。令 `q=c_c`，上下支持是关于 `q` 的分段仿射凹/凸函数；枚举全部系数和 `w_i` 的零点，可用 **Fraction 精确求出这一个参数族的最佳上下界**。交集保留真实状态，但**不是精确 CZ 后验**；独立残差放松会丢失历史动态相关性。

## 2. 可达历史的实验结果（第193拍控制前）

| 估计方法 | 速度下界 m/s | 速度上界 m/s | Run208/210 两层 Backup |
|---|---:|---:|---|
| Run213 一次收紧后再传播的独立盒 | -2.5355587595 | -0.6005811657 | 拒绝 |
| 最近3包、优化支持系数 | -2.5355587595 | -0.6562115824 | 拒绝 |
| 最近6包、20个三包组合交集 | **-2.4955466060** | **-0.6674724157** | **仍拒绝** |

- 6包方法相对独立盒的速度下界严格收紧 `57617501/1440000000 ≈ 0.04001215347 m/s`；最佳下界来自包105、165、180，`q=50/9`。
- 实际速度约 `-0.7633444991 m/s`，在所有精确支持界内；已执行前192拍状态包含与硬约束检查均通过。
- 对新独立外包盒的危险联合角点，固定合法高推力、最不利负残差，即使连续5拍使用最大反向力矩，得到 `v_{k+5}≈-3.0358494888 m/s < -3 m/s`。这是**外包盒的有限步不可认证见证**；该联合角点未证实符合完整历史，不能宣称真实状态不可生存。
- 补充数值诊断：用 SciPy HiGHS 求解截至180拍全部位置返包约束、但独立放松姿态/残差的历史 LP，速度上下界约为 `[-2.4955466060,-0.6674724157]`，与精确三包支持界在浮点精度内一致。**LP 的全局最优性仅为数值证据，未给出精确对偶证书。**
- 本地 20 个三包组合的精确支持计算约 `0.75 s`，大于模型 `H=0.02 s` 控制周期；这套直接枚举实现**尚不满足在线实时预算**。与 Run213 的约 `0.013 s` 单次 Backup 计时不是同一工作负载，不能据此计算严格加速比。

**负面结果保留：** 即使使用更早位置历史并对单参数支持函数精确优化，193拍两层因果 Backup 仍为空；这说明只优化一维速度外包不足以恢复准入，不能把拒绝归咎于求解器数值误差。

## 3. 复现、测试、证据级别

- 新源码：`verification/check_rolling_history_support.py`；5项测试：`verification/test_rolling_history_support.py`；结果：`results/rolling_history_support_20261031/checks.json`。
- 指令：`PYTHONPATH=verification python -m unittest -v verification.test_rolling_history_support`；`python -m py_compile verification/check_rolling_history_support.py verification/test_rolling_history_support.py`；`PYTHONPATH=verification python verification/check_rolling_history_support.py --output results/rolling_history_support_20261031/checks.json`。
- Python 3.13.5，Linux x86_64。**5/5测试通过**，包含精确系数恒等式、因果历史、Run213可达前缀、20个三包支持的真值包含、193拍拒绝和五拍盒角点见证。新源码与测试文件的远端 Git Blob SHA 分别应为 `392563cc6146a9a30a824f641cf5cfd142dff8c5`、`f4bbe6c8841e76ce8713680e2730d5756edb318c`。
- 本地测试依赖与远端函数逐式核对的轻量镜像，**不是完整仓库 checkout**；未完成仓库全量回归和 GitHub CI。所有数学判定使用精确分数；性能和 LP 诊断使用浮点，不参与安全证明。

## 4. 文献与硕士课题收敛

- Scott、Raimondo、Marseglia、Braatz（2016），*Constrained zonotopes: A new tool for set-based estimation and fault detection*，*Automatica* 69:126–136，DOI https://doi.org/10.1016/j.automatica.2016.02.036。复核公开正文引言与集合表示/交运算的相关论述；CZ 能表示联合约束，不能将本文一维支持交集冒称 CZ。
- Rego、Raffo、Scott、Raimondo（2020），*Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems*，*Automatica* 111:108614，arXiv https://arxiv.org/abs/1908.09950。本轮仅核对摘要/书目信息；仓库Run179已有分章节全文精读记录，本轮不重复声称精读，也不增加去重计数；非线性 CZ 传播方法可作为后续候选，当前四状态模型先采用线性精确传播。
- 统一论文阅读记录仍为87篇已计数文献，按证据级别更新本轮复核，不将摘要核验标为已读全文。

**Gate A = blocked。** 现有成果：四状态 SMF 数值闭环、有限时域因果 Backup、历史一致一维支持的严格局部准入恢复及其后续负面界。缺口：联合 `(p,v,phi,omega)` 历史相关性、可在线计算的 CZ/线性约束表示、完整 MPC、终端不变性、递归可行性、稳定性与六状态安全证明。

**下一轮唯一优先任务：** 构造**保留位置—速度与姿态—角速度动力学耦合的有限窗口联合 CZ/线性约束后验**，用可验证的支持函数或精确对偶证书检查第193拍危险联合角点是否历史一致；优先给出计算预算内的约束压缩，而不是继续增加独立速度支持组合。
