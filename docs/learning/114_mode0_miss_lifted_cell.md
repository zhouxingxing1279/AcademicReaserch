# 114. mode 0 miss 边的最小 lifted-cell oracle

日期：2026-10-13。本章只实例化 Run179 要求的第一条 source-to-target 检查，不把一步闭合
升级成 terminal family 或 RCI。

## 冻结对象与时序

取竖直联合坐标 `s=(eta_p,eta_v,e_p,e_v)`、可见量 `d=e-eta`。source cell 用等价的
`(eta,d)` 表示：`eta` 属于 Run136 mode-0 精确二维投影，且
`|d_p|<=1/5, |d_v|<=1/4`。这给出正四维体积 cell，并保证当前 tracking-error 仍在
`|e_p|<=1, |e_v|<=11/4` 内；两项精确余量为 `39/50` 与
`52142137/36000000`。

冻结合法边 `0->1 miss`，并采用可见量上的仿射策略

```math
\delta T=0d_p+0d_v+0.
```

它不读隐藏 `eta`。名义推力区间也是实际推力区间
`[1356943/160000,1782257/160000]`，严格位于物理执行器区间内。

## 保留 actual-thrust residual graph

没有把估计误差当未来扰动。对同一个 `rho_z in [-1,1]` 使用

```math
r_z(T,\rho_z)=\left(\frac{1043}{500}+\frac{81}{800}T\right)\rho_z,
```

并让这一 realization 同时进入 `eta_v^+` 与 `e_v^+`。在本 cell 的零修正策略下，最坏
半宽于实际推力上端取得：`411370817/128000000`。miss 更新为

```math
\eta_p^+=\eta_p+h\eta_v,\quad
\eta_v^+=\eta_v+h r_z,\quad
e_p^+=e_p+h e_v,\quad
e_v^+=e_v+h r_z.
```

这保留了认证非线性 plant 余项对实际推力的依赖，但仍只是冻结的竖直 residual graph，
不是精确六自由度动力学。

## 逐 target-normal 证书

target 的 estimator 部分取 Run136 mode-1 精确投影的 6 个固定 facet normals；tracking
部分取 `B_e` 的 4 个有符号坐标 normals。检查器对 source cell、推力区间和共享 `rho_z`
解析求每个 normal 的支持上界。10 行均不超过 target bound：tracking 位置与速度的最小
严格余量分别为 `1357142137/1800000000` 和
`79725081847/57600000000`。estimator 有两个位置 facet 为零余量，这是 Run136 reachable
set 构造的精确边界相等，不是浮点容差。

因此该固定 lifted cell 在 `0->1 miss` 上闭合。它证明了 Run179 所需 oracle 在至少一个
非退化 cell 上可复算，且没有把全部 `d` 合并为单一输入。但零策略、单边和已有 reachable
投影使其只是实现引理；Hempel--Kominek--Werner 的 noisy-output fiber 条件已经覆盖这类
共享输入/逐 facet 验证思想。

## 证据边界与下一步

- **已证明：**一个固定正体积 source cell、一个仿射 fiber policy、10 个固定 target
  normals 在真实配置的 mode-0 miss 边上满足输入、source-domain 与后继包含。
- **未证明：**其他 16 条边、cells 的覆盖/重叠一致性、45-state terminal family、RCI、
  MPC shift/递归可行性、水平姿态耦合或六自由度保证。
- **准入结论：**允许继续到第一个未知分叉；本结果本身不是创新或论文级贡献。

下一唯一问题：冻结 mode 4 的同一类 lifted source cell 和**同一张**仿射 fiber policy，分别
对 `4->5 miss` 与 `4->0 success` 的全部 target normals 做共享输入、共享 actual-thrust
residual 与 success measurement-noise 证书；任一分支失败则停止扩展该 cell。
