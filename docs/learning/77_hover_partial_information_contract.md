# 77. Hover 邻域 partial-information ancillary 合同

日期：2026-10-02。承接第 76 章的六项合同门槛。本章只把问题实例化到可执行状态，
不综合控制器或不变集。

**结论：真实配置现已显式冻结 15 模态/17 边的因果量词、可见信息、hover nominal
box、actual-thrust residual graph、共享物理/测量原语和 `S_0 x {0}` 初始化；contract
gate 从 `blocked` 变为 `ready`。该状态只表示后续 synthesis 回答的是一个确定问题，绝不
表示 RCI 存在。**

## 1. 信息与量词

令

```math
\eta=x-\hat x,\qquad d=\hat x-z,\qquad e=x-z=\eta+d.
```

在当前模式 `j`、可见 `d,z,bar u` 下，控制器先选择

```math
\delta u=\kappa_j(d,z,\bar u),
```

然后自然才实现下一 packet outcome、隐藏 `eta`、物理余项及下一测量噪声。冻结量词为

```math
\forall(j,d,z,\bar u)\ \exists\delta u=\kappa_j(d,z,\bar u)\
\forall\eta\in Q_j(d)\ \forall(j,j^+)\in E(j)\ \forall\xi.
\tag{77.1}
```

待综合 policy class 是 mode-indexed observation-piecewise-affine。它必须对同一
observation fiber 使用同一输入；`eta`、真实状态、已实现 residual、下一边和未来测量均
不是 policy 输入。该有限类是 Hempel--Kominek--Werner output-feedback CI 的保守实例，
不等价于 Baras--Patel 的一般信息状态反馈。

## 2. 冻结 hover nominal 域

名义中心为 `z_h=(0,2,0,0,0,0)`，existence-probe box 为

```math
Z_h=[-1/2,1/2]\times[3/2,5/2]\times[-1/4,1/4]^2
\times[-1/20,1/20]\times[-1/4,1/4].
\tag{77.2}
```

hover 严格位于各坐标内点。该盒只局部化第 71 章中的 `delta T z_phi` 并给后续求解一个
确定域；它不是最终 maneuvering set，也不证明 `x=z+eta+d` 留在物理源域。候选 RCI
仍须显式满足该 source-domain 约束。

## 3. 同一原语生成三条后继

给定一个当前样本，先由关系

```math
x=z+d+\eta,\qquad \hat x=z+d,
```

恢复真值与估计中心。实际输入为

```math
T=\bar T+\delta T,\qquad \tau=\bar\tau+\delta\tau.
```

物理后继使用第 71 章模型：

```math
\begin{aligned}
p_x^+&=p_x+h v_x,&p_z^+&=p_z+h v_z,\\
v_x^+&=v_x-hT\phi+h r_x,&
v_z^+&=v_z+h(T-g)+h r_z,\\
\phi^+&=\phi+h\omega,&
\omega^+&=\omega+h\tau/J.
\end{aligned}
\tag{77.3}
```

其中单个共享归一化原语向量

```math
\xi=(\rho_x,\rho_z,\nu_{px},\nu_{pz},\nu_\phi,\nu_\omega)\in[-1,1]^6
```

按边标签只实例化一次；同一实际推力决定

```math
r_x=[47/25+(243/16000)T]\rho_x,\qquad
r_z=[1043/500+(81/800)T]\rho_z.
\tag{77.4}
```

名义后继把 `(T,tau,r)` 换为 `(bar T,bar tau,0)`。observer prediction 使用已执行的
actual input；水平速度预测保持 Run 136 的 `-hg hat phi`，垂向用 `h(T-g)`。每 tick
直接以带界噪声的下一 `phi,omega` 测量重置相应估计；在 success 边上另取

```math
\hat p_i^+=y_i^+,
\qquad
\hat v_x^+=\hat v_x^-+5(y_x^+-\hat p_x^-),
\qquad
\hat v_z^+=\hat v_z^-+\frac92(y_z^+-\hat p_z^-).
\tag{77.5}
```

miss 边不作位置修正。最后只定义一次

```math
\eta^+=x^+-\hat x^+,
\qquad d^+=\hat x^+-z^+.
\tag{77.6}
```

所以物理余项及下一测量噪声只有一个 realization，自动满足

```math
\eta^++d^+=x^+-z^+=e^+.
\tag{77.7}
```

这比把 `eta+`、`d+` 各放一份独立 residual box 更强且语义正确。成功边中的位置测量
与物理余项通过同一个 `x+` 进入 observer；不能为两条误差坐标重新采样。

## 4. 模式与初始化

模式表示距最近成功位置包的年龄。冻结 14 条 miss 边 `j->j+1`，以及
`4,9,14 -> 0` 三条 success 边。模式 4 和 9 的输入在未知 success/miss 分叉前选择；
mode 14 受 bounded-dropout 合同强制 success。初始化要求 mode 0 候选包含

```math
S_0\times\{d=0\},
```

其中 `S_0` 来自 Run 136 的通过 artifact。它只证明 nonempty initialization slice，
不保证该切片属于尚未综合的 joint RCI。

## 5. 精确核查与证据等级

`check_hover_partial_information_contract.py` 使用 `Fraction` 从物理、observer 和 nominal
三条后继独立重建 `eta+`，再与 Run 136 边映射逐式比较。关键变换为

```math
w_x=r_x+(g-T)\phi,
```

并在 `T in {4.905,14.715}`、`phi in {-0.45,0.45}` 与 residual 归一化端点上验证
`|w_x|<=13794349/3200000`、`|w_z|<=572143/160000`。全部 17 条边同时检查该独立
oracle、共享分裂恒等式和 Run 136 扰动界。

contract gate 失效封闭地拒绝：隐藏信息进入 policy、错误 policy class、同一 observation
fiber 使用不同输入、控制晚于未知下一边、共享向量或 miss/success 边级 incidence 被改写、
余项与 actual thrust 脱钩、source/input/Run136 投影约束关闭、或 nominal-plus-correction
超出 actuator box。常数 oracle 还会在 `h,g,J`、域或测量噪声与配置漂移时失败。

- **已证明的代数事实：**冻结 successor construction 对全部输入满足式 (77.7)，且其
  `eta+` 与独立恢复的 Run 136 success/miss 方程一致；源域角度/推力端点满足认证扰动界。
- **已核查配置事实：**七项义务齐全、17 条边与 Run 136 初始化 artifact 存在，hover
  严格在 probe box 内。
- **未证明：**存在任何 causal policy/RCI、候选 source-domain closure、最终 nominal
  input 内点、terminal/shift、recursive feasibility 或闭环性能。

下一唯一问题：在 vertical projection
`(eta_pz,eta_vz,d_pz,d_vz)` 上，用同一 15-mode graph、Run 136 投影、实际推力余项与
correction box，求解 observation-fiber PWA RCI feasibility；同时以允许读取 `eta` 的
full-state vertex RCI 作非因果上界。若两者分离，记录因果性代价；若 causal 类失败，只
否定该 policy/certificate class，不升级为完整六状态不存在。
