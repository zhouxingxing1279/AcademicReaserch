# 31 保留推力语义的 LPV ancillary 候选：真实输入法向首次显示 CZ 收益

日期：2026-09-24。承接第25章的“固定 hover LTI + reduced residual 是假证书”和第30章“现有 terminal normal 不消费 CZ 相关性”。本轮不再人为挑 mixed normal，而从**保留已知推力的真实动力学**合成一个 ancillary 候选，再检查由该反馈自然产生的输入约束法向是否消费 rolling CZ 的相关性。

## 1. 语义一致的横向—姿态 LPV 家族

取误差状态

\[
e=[p_x,v_x,\phi,\omega]^\top,
\]

并把 MPC 已知/决策推力 `T` 保留在系统矩阵中：

\[
e^+=A(T)e+B\tau,
\]

\[
A(T)=\begin{bmatrix}
1&h&0&0\\0&1&-hT&0\\0&0&1&h\\0&0&0&1
\end{bmatrix},\qquad
B=\begin{bmatrix}0&0&0&h/J\end{bmatrix}^\top .
\]

这与第12/25章的模型合同一致：`-(T-g)phi` 不再被错误地塞进独立扰动。非线性 `sin(phi)` remainder 和 aero disturbance 仍应进入 tube disturbance；本轮**没有**声称它们已被 RPI 闭合。

## 2. Hover DARE 只作为候选生成器

按 `planar_baseline.json` 的归一化 Q/R，在 `T=g` 处求离散 DARE，得到

\[
K=[0.1425749515,\ 0.2006738212,\ -1.1714620252,\ -0.2286054551].
\]

这里使用 `tau=K e` 的符号约定。三个 frozen thrust 点的闭环谱半径为

| T | rho(A(T)+BK) |
|---:|---:|
| 4.905 | 0.9915812083 |
| 9.81 | 0.9778088237 |
| 14.715 | 0.9781403290 |

因此该 K 至少不是第25章那种模型合同错误产生的“稳定假象”。进一步枚举两个端点矩阵长度 1–12 的全部切换乘积，最大的归一化谱半径为 `0.99158120835 < 1`。

**但这仍不是任意 switching 稳定性证明。** 有限乘积搜索只是主动反例搜索；在得到 common Lyapunov / periodically contractive terminal certificate 前，配置中的 `K` 必须继续保持 `null`。

## 3. 真正重要的新观察：输入法向消费了 CZ 相关性

输入硬约束 `|tau|<=0.08` 对误差 tube 需要支持

\[
h_E(\pm K).
\]

把 K 嵌入六状态顺序 `(px,pz,vx,vz,phi,omega)` 得

\[
p_K=(0.142575,0,0.200674,0,-1.171462,-0.228605).
\]

这不是人为诊断方向，而是由语义一致的 ancillary 候选和真实 torque constraint 自动产生的 normal。

在第30章相同 rolling CZ benchmark（26 ticks、horizon 8）上，共检查正负方向 468 次。比较 exact CZ support 与最小 coordinate-box outer support：

- 331 / 468 次出现严格 gap；
- 平均 gap `3.1982541e-5`；
- 最大 gap `1.8127720e-4`。

因此第30章“当前 terminal normal `±(4,1)` 没有 CZ tightening 收益”不能推广到未来真实输入法向。**一旦反馈律产生跨 `(px,vx,phi,omega)` 的 mixed input normal，rolling CZ 的相关性确实可能转化为更小的 input tightening。**

这只是数值观察，不是当前控制器可行性结论：最大 gap 相对 `0.08` torque limit 很小，而且 K 尚未获得 robust LPV terminal/tube certificate。

## 4. 候选创新重新排序

### 候选 A：SMF-CZ 对真实 ancillary input normals 的 certified tightening

核心机制不是“CZ 几何更紧”，而是

\[
h_{X_k}(K(T)^\top q_u)
<
h_{B(X_k)}(K(T)^\top q_u)
\]

在真实输入约束法向上严格成立，并且该差异足以扩大 nominal input margin / feasible set。第31章首次给出真实反馈候选生成的正证据，但尚未达到“足以改善可行域”的量级证明。

证明义务：先得到合法 LPV ancillary/terminal certificate；再证明或认证这些法向上的 support gap；最后把 gap 转成 nominal constraint inclusion 或 domain-of-attraction 改善。

### 候选 B：CZ-SMF scheduling bounds + LPV terminal family

第27–28章已经证明 exact posterior 的 scheduling interval 可 shift-nest；Hanema–Lazar–Tóth 的 LPV tube MPC 已有 terminal/periodic contractive set 理论，因此“LPV terminal family”本身不是创新。可研究的接口只能是 measurement-conditioned CZ-SMF 如何给出可认证且跨时刻兼容的 scheduling/support bounds。

### 被否定的捷径

- frozen vertices 都 Schur **不能**推出任意 scheduling switching 稳定；
- 长度 12 的 endpoint product 搜索通过 **不能**代替 common Lyapunov/contractive-set proof；
- 当前 input-normal support gap **不能**证明 torque tube 可行，因为 additive remainder/RPI 尚未闭合；
- 不允许为了填 `K` 而把这个候选写进正式 config。

## 5. 文献边界

Hanema, Lazar, Tóth, *Automatica* 2017 已系统给出 LPV tube MPC 的 stabilizing terminal set/cost，并使用 periodically contractive terminal sets；因此本项目不能把“LPV tube + terminal certificate”作为新贡献。Ping et al., IEEE TCYB 2022 又已经给出 LPV output-feedback robust MPC、nested RPI/RCI estimation/control error sets 与 scaled terminal sets。现阶段的新颖性若存在，只能更具体地落在 **CZ-SMF measurement posterior 的相关性如何在真实 LPV input normals 上形成 certified tightening，并与 shift-compatible support computation 联动**。

## 6. 复现

```bash
python verification/check_candidate_lpv_input_normal.py \
  --output /tmp/candidate_lpv_input_normal.json --horizon 8
```

归档：`results/candidate_lpv_input_normal_20260924/checks.json`。

环境：Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0。

## 7. 下一步

下一轮优先解决“候选 K 能否升级为合法 ancillary controller”，而不是继续寻找 support gap：

1. 对 `A(T)+BK, T in [4.905,14.715]` 搜索 common quadratic / polytopic contractive certificate；由于 `A(T)` 对 T 仿射，可利用端点/凸性结构，但必须严格核对所用 LMI 的充分性。
2. 若 common quadratic certificate 不存在，转向 Hanema 的 periodically contractive / heterogeneous tube parameterization，而不是调参硬凑。
3. 在稳定证书成立后加入语义一致的 `r_x(T)` remainder，计算 robust control invariant tube，并检查 `|tau|<=0.08`；若仍失败，则当前 K 只能作为诊断法向，不能进入 MPC。
4. 只有硬输入 tube 通过后，才比较 exact CZ、coordinate box、ellipsoid 在真实 `K^T q_u` 上的 feasible-margin 改善。
