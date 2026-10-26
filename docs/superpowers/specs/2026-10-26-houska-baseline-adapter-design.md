# Houska 基线适配合同设计

## 目的

把 Houska 式 (29) 的固定线性、固定扰动 information-ensemble 基线可靠地接到当前竖直
15-mode 合同上；本轮只冻结可执行问题数据，不声称已求得 invariant terminal ensemble。

## 设计选择

考虑过三种路径：(1) 直接把当前 `(eta,d)` 非线性图塞入式 (29)，但其 decision-dependent
residual 违反论文固定 `W` 假设；(2) 忽略 packet mode 使用单一每步测量算子，会改变传感信息；
(3) 对真实竖直 tracking error `e_z=(e_pz,e_vz)` 使用全执行器域 residual 外包，并保留
15-mode edge-indexed measurement operator。选择 (3)，因为它是同一物理合同的可靠、保守强基线。

冻结数据为

```math
A=\begin{bmatrix}1&1/50\\0&1\end{bmatrix},\quad
B=\begin{bmatrix}0\\1/50\end{bmatrix},\quad C=[1\ 0].
```

实际推力位于 `[981/200,2943/200]`，所以竖直 residual 的固定最大半宽为
`572143/160000`，离散速度扰动半宽为 `572143/8000000`。success 边使用位置噪声
半宽 `1/50`；miss 边不作测量求交。状态误差安全盒从 nominal probe box 与真实 source
domain 的逐坐标余量推出：`|e_pz|<=1`、`|e_vz|<=11/4`。修正推力盒为
`|delta T|<=572143/160000`。

三处分叉 mode 4、9 的所有外出边必须对同一 source extreme information set 复用同一当前
控制；mode 14 只有 success 边。后续式 (29) 的图扩展须逐 source mode 建 ensemble，并在每条
边施加 successor inclusion。

## 非目标与停止条件

- 不选择 `Y,G,Lambda,Z,H,Omega` 模板；不运行终端优化器。
- 不宣称 terminal invariance、MPC recursive feasibility、六自由度保证或创新性。
- 若检查器不能从仓库冻结配置精确重建上述数据，禁止进入模板综合。
