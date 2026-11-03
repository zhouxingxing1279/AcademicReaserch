# 25 六状态 ancillary feedback：先审模型合同，再谈终端集

2026-09-23。接续 [24 真实 control-normal gate](24_control_normal_gate.md)。本轮按第24章要求尝试独立合成六状态 ancillary feedback，但得到的最重要结果不是一个可提交控制器，而是一个**必须保留的否证**：若把第12章“保留已知推力后”的较小水平余项，直接塞进固定 hover LTI 矩阵，就会得到一个看似满足全部硬约束的 LQR/RPI；但这个证书在模型语义上是错的。

## 1. 候选反馈

在 hover 点采用状态 `e=(px,pz-2,vx,vz,phi,omega)`，固定 LTI 中心

\[
e^+=Ae+B\delta u+w,\qquad \delta u=(T-g,\tau),
\]

其中 `vx+ = vx + h(-g phi + w_x)`。按 `planar_baseline.json` 的 Q/R 标度求离散 LQR，得到闭环谱半径

\[
\rho(A+BK)=0.9778088237<1.
\]

因此“稳定化增益不存在”不是当前障碍。

## 2. RPI 外包计算

对稳定闭环 \(A_K=A+BK\)，mRPI 为

\[
\mathcal S_\infty=\bigoplus_{i=0}^{\infty}A_K^i\mathcal W.
\]

实现计算前 1000 项的 zonotope support，并用离散 Lyapunov 范数给剩余尾项做外包：若

\[
\|A_Kx\|_P\le\rho_P\|x\|_P,
\]

且 \(d_P=\max_{w\in W}\|w\|_P\)，则完整 RPI 位于 P-范数半径 \(d_P/(1-\rho_P)\) 内；第1000项之后的尾部再乘 \(A_K^{1000}\) 得到各 state/input direction 的安全 support tail。

这是经典 tube MPC / mRPI 结构；Mayne–Seron–Rakovic (2005) 和 Rakovic et al. (2005) 已分别系统处理 bounded-disturbance robust MPC 与 mRPI 外逼近，因此这里不宣称算法创新。

## 3. 一致的全域 LTI 合同：失败

固定 `-g phi` 在中心动力学时，`(T-g)phi` 不能凭空消失。第12章已经给出全域独立盒水平半径

\[
d_x^{old}=4.3107340625.
\]

使用该**语义一致**扰动合同，RPI 外包 support 为：

|量|support|允许半宽|margin|
|---|---:|---:|---:|
|px|3.72647|5|+1.27353|
|pz-2|0.12467|1.5|+1.37533|
|vx|4.37810|3|**-1.37810**|
|vz|0.47712|3|+2.52288|
|phi|0.70752|0.45|**-0.25752**|
|omega|1.71061|2|+0.28939|
|T-g|4.48858|4.905|+0.41642|
|tau|0.16244|0.08|**-0.08244**|

所以这个标准 hover LQR **不能**给当前全域独立盒抽象提供满足硬约束的 RPI tube。失败方向正是 `vx / phi / tau`。

## 4. 一个危险的“假阳性”

若错误地把第12章较小的

\[
d_x(T)\le 2.1034840625
\]

当成固定 hover LTI 的 additive disturbance，再做完全相同计算，会得到：

- `vx` support 2.13636 < 3；
- `phi` support 0.34524 < 0.45；
- `tau` support 0.079264 < 0.08；
- 其余方向也全部有正 margin。

它看起来恰好“通过”全部约束，尤其 torque 只剩约 `7.36e-4` margin，很容易被误写成六状态 ancillary certificate。

但这是**无效证书**。较小余项成立的前提是中心动力学精确保留 `-T phi`：

\[
v_x^+=v_x+h[-T\phi+r_x].
\]

一旦仍使用固定 `-g phi` 的 A 矩阵，就必须把 `-(T-g)phi` 放回不确定项，退回旧半径。也就是说，不能同时享受“固定 LTI”与“保留输入—姿态相关性后的较小 W”。

这个假阳性非常重要：它说明后续自动合成若只看数值 margin，而不审计 set/model contract，会产生貌似漂亮但理论错误的 terminal certificate。

## 5. 对研究主线的影响

第24章提出“先合成真实 K，再决定 recenter 创新生死”。本轮把这一步进一步明确：

1. **旧独立盒 LTI**：已有第12章任意策略长期安全否证；本轮标准 LQR/RPI 又在 `vx/phi/tau` 上直接失败，不值得继续调 K 试图挽救一个结构上过保守的合同。
2. **较小 residual**：必须保留 `T*phi` 相关性，因此控制模型自然变成 bilinear / qLPV / joint-set 问题，而不是普通 additive-LTI tube。
3. 下一步真正应验证的是：在 `(e, delta T, phi, q=delta T*phi)` 联合约束下，用 McCormick/CZ 保留相关性后，是否能得到一个**合法**且明显小于独立盒 tube 的 robust invariant/finite-horizon tube。

这与当前“为什么 CZ 能降低保守性”的主问题重新汇合：潜在优势不是 CZ 这个名字，而是它能否保留输入—状态/估计相关性，避免把 `(T-g)phi` 独立 adversarial box 化。

## 6. 候选创新重新排序

### A. correlation-preserving joint tube — 提升优先级

核心问题：保留 `q=delta T*phi` 的联合可行关系，用 CZ/polytope/McCormick 表示，并证明相对独立盒 abstraction 的一步 reachable-set 包含更紧；再把该关系传播到 finite-horizon/tube tightening。

需要证明：包含性、固定复杂度外包、输入约束、递归可行性，以及相对 ellipsoid/zonotope/box baseline 的严格 support 改善条件。

### B. finite-control-normal recenter gate — 暂停

在合法六状态 ancillary controller 出现之前，不再扩展 recenter 实验。

### C. reduced residual + fixed LTI LQR — 否定

这是本轮代码主动发现并记录的 model-contract mismatch，不得再次作为控制证书使用。

## 7. 复现

实现：`verification/check_ancillary_lqr_rpi.py`；归档：`results/ancillary_lqr_rpi_20260923/checks.json`。

```bash
python verification/check_ancillary_lqr_rpi.py --output /tmp/ancillary_lqr_rpi.json
```

本轮实际运行环境 Python 3.13.5 / NumPy 2.3.5 / SciPy 1.17.0。数值 RPI 使用 1000 项有限和 + Lyapunov-norm 尾部外包；它是针对给定线性合同的数值证书审计，不是非线性四旋翼的闭环证明。

## 8. 下一轮

不再调 LQR 权重。直接构造一个最小二维/三维 `deltaT-phi-vx` 联合模型，对比：

1. 独立盒化 `(deltaT*phi)`；
2. McCormick polytope；
3. constrained-zonotope/joint latent representation。

要求在相同源域上严格验证 `exact/joint reachable ⊆ correlation-preserving outer ⊆ independent box outer`，并计算真实 MPC normals 上的 support tightening 差。如果第二个包含严格且计算量可控，再推进到六状态 finite-horizon tube；否则放弃这一创新候选。
