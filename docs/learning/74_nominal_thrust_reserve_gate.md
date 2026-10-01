# 联合 ancillary RCI 前的名义推力预留门槛

日期：2026-10-01。承接第 71 章的 control-dependent ancillary contract 与第 73 章的 15-mode estimator-error zonotope multi-set。

**结论：当前配置只声明实际推力硬区间，没有单独名义推力区间。若 nominal MPC 直接复用完整 `[4.905,14.715]` N，则任何非空紧致 vertical ancillary RCI（包括有限 mode-indexed family）都不存在。对当前 residual，名义推力的必要预留区间为 `[7.48763125,11.13910625]` N。该区间只是一项必要条件，不是 RCI 存在证书。**

## 1. 冻结垂向合同

第 71 章给出

\[
e_{v_z}^{+}=e_{v_z}+h(\delta T+r_z),\qquad
T=\bar T+\delta T\in[T_{\min},T_{\max}],
\]

且

\[
|r_z|\le d_z(T)=c+\alpha T,
\quad c=2.086,
\quad \alpha=\frac{0.45^2}{2}=\frac{81}{800}.
\]

配置中的实际推力端点为

\[
T_{\min}=4.905=\frac{981}{200},\qquad
T_{\max}=14.715=\frac{2943}{200}.
\]

这里不假定 static linear feedback；`delta T` 可以由任意 causal policy 产生。允许更强的 full-state policy 也不能绕过下述输入权限必要条件，因此结论同样约束 output-feedback policy。

## 2. 必要预留定理

**命题 74.1。** 若一个固定名义推力 `bar T` 要允许某个非空紧致 tracking-error RCI，且 residual 可在每步独立选择 `[-d_z(T),d_z(T)]` 中任意值，则必须满足

\[
\boxed{
T_{\min}+d_z(T_{\min})\le \bar T
\le T_{\max}-d_z(T_{\max}).
}
\tag{74.1}
\]

**证明。** 设紧致候选中 `e_vz` 的最大值为 `M`。在该边界取合法扰动 `r_z=d_z(T)`，不向外漂移要求存在合法 `delta T` 使

\[
\delta T+d_z(\bar T+\delta T)\le0.
\]

左端对 `delta T` 的斜率为 `1+alpha>0`，故在实际推力下界对应的最小合法修正 `delta T=T_min-bar T` 处最小。可行性要求

\[
T_{\min}-\bar T+d_z(T_{\min})\le0,
\]

得到式 (74.1) 左侧。对候选中 `e_vz` 的最小值取 `r_z=-d_z(T)`；不向外漂移要求 `delta T-d_z(T)>=0`。该式对 `delta T` 的斜率为 `1-alpha>0`，在最大合法修正 `T_max-bar T` 处最大，从而得到式 (74.1) 右侧。证毕。

若允许有限个 dropout-mode 集合，同一结论仍适用于允许持续出现的 constant nominal-thrust path：`bar T` 低于左界时，取持续正 residual 后每步 `e_vz` 至少增加 `h[T_min-bar T+d_z(T_min)]>0`；高于右界时存在对称的持续负漂移。有限个紧致集合的并仍有全局最大/最小值，故 mode indexing 不能消除该阻塞。

## 3. 当前精确数值

\[
d_z(T_{\min})=\frac{413221}{160000}=2.58263125,
\]

\[
d_z(T_{\max})=\frac{572143}{160000}=3.57589375.
\]

因此

\[
\boxed{
\bar T\in
\left[\frac{1198021}{160000},\frac{1782257}{160000}\right]
=[7.48763125,11.13910625]\ {\rm N}.
}
\tag{74.2}
\]

hover 值 `9.81 N` 严格位于其中，所以该必要条件没有否定 hover-neighborhood ancillary RCI。它否定的是把完整 actual input set 同时交给 nominal MPC，并仍假定 ancillary 有双向 thrust authority。

## 4. 证据等级与控制接口

- **已证明：**完整 nominal thrust range 中包含两条严格 endpoint nonexistence witness；式 (74.2) 是任何固定 `bar T` 紧致 vertical RCI 的必要条件。
- **配置事实：**`planar_baseline.json` 只有 actual `input_lower/input_upper`，没有独立 `nominal_input_lower/upper`；`K` 与 terminal certificate 仍为空。
- **未证明：**式 (74.2) 内存在联合 `(e,eta)` RCI；horizontal bilinear coupling、torque reserve、state/residual source-domain closure、terminal 与 shift 均未闭合。

下一步必须先冻结 nominal input allocation。建议把 nominal thrust 初始 baseline 限制在 hover 附近、并把实际输入余量完整留给 ancillary；只有该配置通过 exact reserve gate 后，才实现 Lorenzetti--Pavone 风格的 augmented-error RCI 强基线，并将 Run 136 的 mode zonotope 作为 estimator-error 输入，而不是把它独立 boxing。

复现：

```bash
PYTHONPATH=verification python -m unittest verification/test_nominal_thrust_reserve.py -v
PYTHONPATH=verification python verification/check_nominal_thrust_reserve.py --output /tmp/nominal_thrust_reserve.json
```
