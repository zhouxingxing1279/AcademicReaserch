# 91. 同标签仿射策略下的凸化交换律

## 1. 合同

只考虑一个固定 source 标签 `q`、一条固定边 `ell:q->q'`。联合状态
`s=(eta,e)`，可见量 `d=D s=e-eta`。冻结 Run136 global residual 后，边动力学可写为

```math
F_\ell(s,u,\xi)=A_\ell s+B_\ell u+a_\ell+G_\ell\xi,
\qquad \xi\in\Xi_\ell,
```

其中 `Xi_ell` 是非空凸集，且不随 `u` 改变。在整个 source 标签上使用同一仿射可见策略

```math
u=\kappa_q(Ds)=K_qDs+c_q.
```

这不是按隐藏 `eta` 或 constituent-set index 选输入；运行时只读可见 `d`。

## 2. 交换引理

给定有限个非空集合 `S_i`，令 `S=conv(union_i S_i)`。定义固定边的闭环集合像

```math
\Phi_\ell(X)=
\{F_\ell(s,\kappa_q(Ds),\xi):s\in X,\xi\in\Xi_\ell\}.
```

则

```math
\Phi_\ell(S)
=\operatorname{conv}\!\left(\bigcup_i\Phi_\ell(S_i)\right).\tag{91.1}
```

同时

```math
\kappa_q(D S)
=\operatorname{conv}\!\left(\bigcup_i\kappa_q(D S_i)\right).\tag{91.2}
```

**证明。** 代入策略得到

```math
F_\ell(s,\kappa_q(Ds),\xi)
=(A_\ell+B_\ell K_qD)s+(B_\ell c_q+a_\ell)+G_\ell\xi,
```

即 `s` 与 `xi` 的仿射映射。仿射像与凸包交换。又因 `Xi_ell` 凸，
`conv(union_i (M S_i+b+G Xi)) = M conv(union_i S_i)+b+G Xi`：正向用
`xi=sum lambda_i xi_i in Xi`，反向可把同一 `xi` 复制给每个凸组合分量。式 (91.2) 同理。

## 3. 约束推论与仍需检查的义务

若输入集合 `U` 凸，且 `kappa_q(D S_i) subset U` 对所有 `i` 成立，则 (91.2) 直接给出
`kappa_q(D S) subset U`。若目标状态约束 `X` 凸，且所有 `Phi_ell(S_i) subset X`，则
(91.1) 给出 `Phi_ell(S) subset X`。所以 Run154 所说“凸化新增 fiber 必须重新逐点验证”可
收紧为：在本章合同成立时，无需枚举新增点；constituent-set 证书加交换引理已经覆盖它们。

但这**不是不变性证明**。仍必须逐项证明：

1. 同一 source 标签确实使用一张全域 affine-in-`d` 策略；
2. 每条允许 miss/success 边分别满足 constituent-set input/后继证书；
3. 每条边的像被相应 target 标签集合包含；
4. 初始化层的首次 return image 进入正确 recurrent 标签；
5. tube/MPC 终端、硬约束和移位递归可行性另行成立。

## 4. 失效边界

下列情形不能引用 (91.1)：

- 保留 `W(T)`，扰动集合随 `u` 改变；此时图像一般不是联合变量的仿射像；
- 不同 constituent sets 用不同 `K_i,c_i`，却未证明它们在重叠/新 fibers 上拼成一张因果策略；
- 策略饱和、切换或 nonlinear，且没有共同 convex graph 证书；
- `U` 或状态安全集非凸；
- 把不同 source edge dynamics 或不同离散标签先混合，再施加一个不存在的共同边映射。

## 5. 标签纪律与下一实例

Run148 的 `J4,J9,J14` 在 mode-only 表示中可取共同凸包；但在 Run153 的 60-state
`(current_age,last_return)` 自动机里，它们分别属于 `(0,5),(0,10),(0,15)`。跨这三个标签
凸化会把精化退回 mode-only 外包，不能用来证明 history-conditioned family 更不保守。

正确的第一次同标签测试是九条第二周期路径。对前一 return 标签
`r in {5,10,15}` 和下一 return length `r' in {5,10,15}` 传播各一条 exact image；然后仅按
共同 target `(0,r')` 分成三组，每组三个 constituent images。先为每个 source 标签冻结同一
affine policy，并逐边认证，再用 (91.1) 对 target 内凸化。该步骤仍只会产生一层 reachable
envelope；未达到 fixed point 前不得称 terminal RCI。

## 6. 证据等级

本章是 **exact algebraic implementation lemma + discrete-label correction**。证明不依赖浮点
样本，但属于仿射映射与凸包交换的直接推论，已包含在 Houska 式 extreme-set convex
interpolation 的一般框架中；不是新控制算法、RCI 证书或硕士课题创新。
