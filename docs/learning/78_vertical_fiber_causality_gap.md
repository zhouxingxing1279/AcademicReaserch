# 78. 竖直 observation-fiber 的一步因果性差距

日期：2026-10-02。本章只构造 Run 140 合同的一个精确有理数 negative control，目的
是防止后续 RCI 求解器把隐藏估计误差当作可观状态。它不是不变集，也不证明 causal
vertical RCI 不存在。

## 1. 同一 observation fiber

取 mode 4、hover 名义状态、`d_pz=d_vz=0`。令采样周期 `h=1/50`、竖直位置
observer 增益 `L=9/2`，并定义

```math
q=\eta_{p_z}+h\eta_{v_z}.
```

从 Run 136 的 mode-4 zonotope 直接计算方向 `(0,1,0,h,0,0)` 的精确支持：

```math
q\in[-q_4,q_4],\qquad q_4=\frac{1004143}{7200000}.
\tag{78.1}
```

该支持由 zonotope 生成元符号精确取得，不是采样极值。逐坐标支持进一步验证整个
mode-4 fiber 在 hover 真值源域内；最小上下界余量均严格为正。

## 2. 两条未知后继边

当前输入必须在 mode 4 的 `miss:4->5` 与 `success:4->0` 实现之前选定。由第 77 章
共享 successor 可得

```math
\begin{aligned}
d_{p_z}^{+}&=0,&
d_{v_z}^{+}&=h\delta T &&\text{(miss)},\\
d_{p_z}^{+}&=q+n,&
d_{v_z}^{+}&=h\delta T+L(q+n) &&\text{(success)},
\end{aligned}
\tag{78.2}
```

其中 `n in [-1/50,1/50]`。取 successor slice

```math
\begin{aligned}
\text{miss: }&d_{p_z}^{+}=0,\quad |d_{v_z}^{+}|\le 7/100,\\
\text{success: }&|d_{p_z}^{+}|\le q_4+1/50,\quad
|d_{v_z}^{+}|\le 13/20.
\end{aligned}
\tag{78.3}
```

这些 target 只定义一步 predecessor 比较，不是声称已经找到 mode-indexed RCI。

## 3. 允许读取隐藏状态时可行

success 边在零控制下的最坏速度半径为

```math
L(q_4+1/50)=\frac{1148143}{1600000}.
```

令

```math
r=\frac{L(q_4+1/50)-13/20}{h}=\frac{108143}{32000},
\qquad
\delta T(q)=-\frac{r}{q_4}q.
\tag{78.4}
```

则 success 的四个 `(q,n)` 顶点满足式 (78.3)，miss 的两个 `q` 顶点满足

```math
|h\delta T|=\frac{108143}{1600000}<\frac7{100}.
```

所需 `r=3.37946875 N` 小于 Run 138 correction 权限
`572143/160000=3.57589375 N`；实际推力端点为
`205777/32000` 与 `422063/32000 N`，均严格位于执行器盒内。由于映射对 `q,n`
仿射，六个顶点的精确检查覆盖整个区间乘积。

该 policy 读取真实 `q`，因此对实际 output-feedback 控制器是故意非因果的，只能作为
乐观 full-state 上界。

## 4. 同一可见信息下 causal 控制严格不可行

真实 policy 在该 fiber 上只能选同一个常数 `delta T`. 对
`(q,n)=(q_4,1/50)`，success target 要求

```math
\delta T\le-r.
```

对 `(q,n)=(-q_4,-1/50)`，则要求

```math
\delta T\ge r.
```

因 `r>0`，可行区间 `[r,-r]` 严格为空；加入 miss target 和 correction box 不可能恢复
交集。这是一个 observation-fiber predecessor 的严格分离，而非有限样本观察。

## 5. 证据等级与用途

- **精确证明：**Run 136 mode-4 整个 fiber 在源域内；非因果 policy 对两个未知边的六个
  顶点满足 target/input；任一共享 causal 输入在同一 fiber 上不满足 success target。
- **类特定负对照：**任何后续 solver 若在固定该 source/target slice 时报告一个读取
  `eta` 的 vertex control 为“causal feasible”，其量词或变量共享实现错误。
- **未证明：**causal vertical RCI 不存在、完整六状态 RCI 不存在、terminal/shift、递归
  可行性、保守性优势或闭环性能。

下一步不应继续制造相似的一步反例，而应实现非轴对齐 vertical mode-indexed
observation-fiber predecessor/RCI 求解；以本章反例作为必要回归测试，再报告认证候选或
明确的 policy/certificate-class 反证。
