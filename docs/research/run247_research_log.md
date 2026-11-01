**Run247完整checkout与安全合并核验（2026-11-01）：** 研究PR #64 https://github.com/zhouxingxing1279/AcademicReaserch/pull/64 基于main `8b7b22c757749fcc6290d7bdbd7fc494a64e86b6`，合并前compare ahead=7/behind=0、mergeable_state=clean，head=`8271e2e5e1042b2bda9595f3b1a5863bc10d4111`。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41335351537 **completed/success**；Python 3.13.17完整checkout Run224–247聚焦测试**211/211通过、无跳过**（74.114s），真实配置、Run246轨迹逐项比较、Fraction精确证书、归档JSON对比与artifact上传成功。PR非强制squash合并至main `193d4cd99e7f48ff56b43f8289336ff75c492cc5`，已重新读取main、PR merged及源码/归档/阅读记录Blob确认落地。合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41335523410 **completed/success**，Python 3.13.17完整checkout再次**211/211通过、无跳过**（56.300s），证书一致性与artifact上传成功。此证据补记仅更新文档，未改变算法；全仓库历史回归、SMF＋MPC递归可行、六状态安全和20ms最坏求解时延仍未认证。

---

# Run247 — 双向速度可生存必要条件与Run245更早不可恢复时刻（2026-11-01）

**远端main基准：** `8b7b22c757749fcc6290d7bdbd7fc494a64e86b6`。读取Run245/246研究日志、源码、精确证书、`configs/planar_baseline.json`、唯一论文阅读记录和历史检查点。**唯一瓶颈：** Run246只在第30拍终点证明不可恢复；要让SMF/MPC的安全前驱在终端之前拒绝危险分支，需要一个能在任意当前状态计算、且对未来所有合法控制有效的必要筛选条件。

## 1. 可计算的双向鲁棒可生存必要条件

沿用冻结四状态显式Euler模型：
\[
p_{k+1}=p_k+h v_k,\quad v_{k+1}=v_k+h(-T\sin\phi_k+r_k),\quad
\phi_{k+1}=\phi_k+h\omega_k,\quad\omega_{k+1}=\omega_k+(h/J)\tau_k.
\]
其中 `h=J=1/50`、`T=981/100`、`R=3246383/1600000`、`|r_k|<=R`、`|\tau_k|<=U=2/25`、`|\phi|<=0.45`、`|v|<=3`。对任何当前真实 `(v,phi,omega)`，任意未来合法控制（甚至允许完整状态、预知未来），角度Euler可达外包为
\[
\phi_{k+j}\in[\phi+jh\omega-c_j,\ \phi+jh\omega+c_j],\quad
c_j=h(h/J)Uj(j-1)/2.
\]
安全轨迹还必须与 `[-0.45,0.45]` 相交。令剪裁后端点为 `L_j,H_j`，使用 `sin_L(x)<=sin(x)<=sin_U(x)` 的有理数Taylor外包和 `sin` 在该区间的单调性，定义
\[
\underline v_N=-3+h\sum_{j=0}^{N-1}[R+T\sin_L(L_j)],\qquad
\overline v_N=3-h\sum_{j=0}^{N-1}[R-T\sin_U(H_j)].
\]
**必要条件：** 若当前真实状态对未来所有合法扰动具有至少N拍安全的控制策略，则必有 `underline_v_N <= v <= overline_v_N`。证明：分别固定合法对抗扰动 `r=-R`、`r=+R`，前者给出任意未来力矩下的速度**上界**，后者给出速度**下界**。即使这些最有利界都越过 `-3/+3`，控制器必然失败。两侧分别用有理数精确验证；这是**必要而非充分**条件，不是构造反馈、RCI或MPC。

## 2. Run245真实可达角点的更早不可恢复证书

保持Run246合法真实初始角点 `(-0.02,-0.1,-0.005,-0.01)`、每拍 `r=-R` 和Run245固定前30拍力矩（`+0.08*12,-0.08*12,0*6`）。本轮在**第26拍**已认证：
- `phi26=1101/5000=0.2202 rad`、`omega26=-1/100=-0.01 rad/s`（精确）；
- `v26<=-1.701398694489753 m/s`（逐拍真实角度与Taylor外包）；
- 对未来20拍全部合法力矩、全部满足角度硬界的轨迹，必要条件为 `v26>=-1.692615117977474 m/s`；
- 严格差距 `0.008783576512279 m/s>0`，故即使从第26拍起获知真实状态、允许任意甚至非因果力矩，合法持续 `r=-R` 仍使 `v46<=-3.008783576512279 m/s<-3`，最迟第46拍违约（若先发生角度违约，则同样不安全）。

这比Run246第30拍才发现不可恢复**提前4拍**；对这一特定路径，若希望避免进入该不可生存状态，控制必须在进入第26拍前改变。每5拍的位置包机会中第25拍可能success或miss，不能假设该包必成功；角度/角速度每拍可见，但隐藏速度的SMF后验尚未与此必要条件集成。

扫描Run245该角点的第0至30拍前缀、每个前缀未来1至30拍的上述必要条件，**首次严格拒绝发生在第26拍、未来20拍**。第0至25拍未被**这个有限、保守必要筛选器**拒绝，绝不意味着它们可生存、可被某个共享因果控制恢复，或该扫描找到真正最早不可恢复时刻。全部0–30拍仍满足Run245硬约束。

## 3. 新论文分节阅读及与本课题的区别

**Joseph Breeden, Luca Zaccarian, Dimitra Panagou (2024)**，*Robust Safety-Critical Control for Systems with Sporadic Measurements and Dwell Time Constraints*，arXiv:2403.03663v3，https://arxiv.org/html/2403.03663v3 ，https://arxiv.org/abs/2403.03663 （2024-06-04修订）。本轮实际阅读原文§II-C Rule 4、Lemma 1/Assumption 2（有界估计误差与测量重置）、§III Theorem 1、§IV Lemma 3/Definition 2/Theorem 2（连续执行器的timed CBF）及§V案例说明。其连续/混合动力学、误差半径预测与定时CBF提供“未来可见测量时间之前必须保持安全”的接口；实例是卫星交会与轨道保持，**不是四旋翼**，且其量测含带界状态估计、定时模型不同于本仓库有噪位置SMF和success/miss自动机。不可直接宣称本轮已经满足论文的CBF存在性或递归可行假设。唯一论文阅读记录新增一篇分节已读，去重92→93（若并发更新需重新核验）。

## 4. 工件、测试与证据级别

- `verification/check_four_state_early_viability_guard.py`：独立Fraction两侧必要条件、真实Run245角点逐拍外包、有限前缀扫描；`--root .`还核对仓库真实配置并与Run246真实轨迹逐项比较。
- `verification/test_four_state_early_viability_guard.py`：11项回归（Euler因果索引、Taylor外包、初始角点、双向必要条件、早期严格反例、范围声明、配置与归档）。
- `results/four_state_early_viability_guard_20261101/checks.json`：精确有理数证书；`.github/workflows/run247-early-viability-guard.yml`：Python 3.13完整checkout Run224–247聚焦回归及归档一致性。
- 本地容器无GitHub DNS，无法git clone。独立Python 3环境执行 `PYTHONPATH=/mnt/data/run247 python -m unittest -v test_four_state_early_viability_guard`：**11项中9通过、2项因隔离环境无仓库配置/归档而跳过**；`python -m py_compile`通过；`python check_four_state_early_viability_guard.py --output checks.json`生成成功。完整仓库PR CI和合并状态以实际GitHub结果为准，未执行全仓库历史回归。
- **严格数学结论**：指定模型与角点、合法持续扰动、全部未来控制量词下，第26拍已处于不可生存状态。**非证明**：有限前缀扫描的无拒绝、hover附近必要区间、浮点正弦sanity；无一般SMF后验可行性、共享因果终端控制、MPC优化、递归可行性或20ms最坏时延证书。

**Gate A仍blocked。** 可行性：增加了可直接用于候选终端筛选的低成本必要判据；创新性：必要guard与既有viability/CBF思想一致，尚非独立创新；研究难度：将精确关联后验、可观测信息和共享控制的存在量词与success/miss逐边前驱结合。

## 5. 下一轮唯一优先任务

**在真实第25拍success/miss分支上，使用Run240关联SMF后验，检验是否存在一个满足执行器界、能够避开本轮第26拍必要不可生存区域的共享因果控制选择；先建立一个可严格验证的非空后继分支，不把必要筛选通过误写成递归可行。**
