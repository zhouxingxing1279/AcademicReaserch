# 75. 增广 ancillary RCI 前的显式输入预算探针

日期：2026-10-02。承接第 74 章。本章只冻结一个用于回答“最有利输入权限下增广 RCI 是否存在”的预算合同，不把它误称为最终 nominal MPC 输入域。

## 1. 文献边界

Lorenzetti--Pavone 的 coupled-error RPI 以

\[
\bar{\mathcal U}=\mathcal U\ominus[0\ K]\mathcal R
\]

直接从已认证 correction support 得到 nominal input tightening。Köhler--Müller--Allgöwer 则在 tube constraint 中对所有允许 estimation/tracking error 联合检查真实反馈输入。两者都说明最终 nominal/correction 权限应由反馈与误差管共同决定；预先切一个任意固定比例不是新算法，也不是最终证明。

当前仓库仍需先排除“求解器暗中使用全部实际输入”的语义错误。因此这里冻结一个可复现、对 ancillary 最有利的 existence probe，之后仍须由 RCI 的真实 input support 恢复有严格内点的 nominal 域。

## 2. 推力预算的精确构造

实际推力区间为

\[
U_T=[T_{\min},T_{\max}]=[4.905,14.715],\quad g=9.81,
\]

垂向余项半宽为

\[
d_z(T)=c+\alpha T,\qquad c=2.086,\quad \alpha=0.45^2/2=81/800.
\]

取 correction 半径为全域最大余项

\[
b_T=d_z(T_{\max})=\frac{572143}{160000}=3.57589375.
\]

在要求 nominal 区间关于 hover 对称且
`nominal interval + correction interval` 不越过实际输入盒时，最大 nominal 半径为

\[
a_T=\frac{T_{\max}-T_{\min}}2-b_T
=\frac{212657}{160000}=1.32910625.
\]

因此冻结

\[
\bar U_T=[g-a_T,g+a_T]
=[8.48089375,11.13910625],
\]

\[
\Delta U_T=[-3.57589375,3.57589375].
\]

两者的 Minkowski 和恰好等于实际推力区间。这个“最宽”结论只在上述**对称 nominal + 对称固定 correction + 使用完整实际推力盒**的证书类内成立。

## 3. 边界权限与零余量

在 `e_vz` 最大边界，为抵抗正余项，令 `delta T<0` 并解

\[
\delta T+d_z(\bar T+\delta T)=0.
\]

当 `bar T=8.48089375` 时，精确解为

\[
\delta T=-\frac{376920383}{140960000}\approx-2.673953,
\]

位于 correction 区间内。对 `e_vz` 最小边界，解

\[
\delta T-d_z(\bar T+\delta T)=0.
\]

当 `bar T=11.13910625` 时，精确解恰为 `3.57589375`，实际推力达到 `14.715`。所以该探针在上边界的 certified authority margin 为 **0**。

这些等式只是输入幅值 witness。控制器在施加当前输入时不知道随后实现的 `r_z`，不能把等式解释为同拍 disturbance cancellation，更不能由此推出 RCI。

## 4. 力矩预算为何只能是 existence probe

当前 benchmark 没有冻结未知力矩扰动数值界，也没有已认证 ancillary gain/support，无法从物理合同唯一推出 correction torque 的最小半径。为了让第一轮 RCI existence test 对 ancillary 最有利，暂取

\[
\bar U_\tau=\{0\},\qquad \Delta U_\tau=[-0.08,0.08].
\]

这保留全部力矩给 tracking correction，但 nominal torque 没有内点，不能表示一般机动轨迹，也不足以构造最终 terminal controller。若该最有利探针下仍不存在满足状态/余项域的增广 RCI，当前 residual/actuator 合同应被优先重审；若存在，则必须从认证的 correction input support 计算 `U ominus U_c`，证明所得 nominal thrust/torque 均有严格内点后才能进入 terminal MPC。

## 5. 证据等级与停止点

- **精确配置事实：**显式 nominal/correction 盒的 Minkowski 和不越过实际执行器盒。
- **类内解析最优：**推力 nominal 区间是在固定对称 correction 半径 `d_z(Tmax)` 下最大的 hover 对称区间。
- **精确边界证书：**两侧 vertical boundary balance 等式成立，但上侧余量为零。
- **已否定的升级：**该探针不是最终 nominal MPC 域；nominal torque 无内点，且尚无 causal feedback/RPI/terminal/shift 证明。

复现：

```bash
PYTHONPATH=verification python -m unittest verification/test_ancillary_allocation_probe.py -v
PYTHONPATH=verification python verification/check_ancillary_allocation_probe.py --output /tmp/ancillary_allocation_probe.json
```

下一唯一问题：在这个对 ancillary 最有利、但不具最终 MPC 可用性的预算下，保持 Run 136 的共享噪声生成元与 actual-thrust residual graph，构造或严格否定 15-mode augmented `(eta,d=hat x-z)` RCI；若存在，立即用其真实 correction support 反推严格内点 nominal input set。
