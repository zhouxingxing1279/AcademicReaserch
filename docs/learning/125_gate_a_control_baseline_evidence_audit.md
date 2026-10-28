# 125 Gate A 控制基线证据审计：现有负结果尚未构成 RCI 基线

日期：2026-10-27。范围严格限于四状态横向—姿态局部基准，不外推到六状态平面四旋翼。

## 1. 唯一问题与冻结合同

本轮不再扩张测量 posterior 或配置锥邻接，而只问：仓库是否已经存在一个充分的
ancillary feedback/RCI 证书，覆盖

\[
T_k\in[4.905,14.715],\qquad
|d_k|\le 1.880+T_k\frac{0.45^3}{6},
\]

全部状态硬约束和 `|tau|<=0.08`？当前 `T_k` 在施加时已知，但 frozen benchmark
没有推力状态或 slew constraint，故未来推力必须允许区间内任意跳变。对当前仿射
`A(T)` 与仿射扰动 support，连续区间 robustification 可精确归约到两个端点。

## 2. 可执行审计结果

新增审计器读取既有归档、核对关键结论，并为每个证据记录生成它的 checker
SHA-256；审计器自身、测试、冻结配置与八份直接结果依赖也全部绑定，且生成结果与归档
逐次比较。结果如下。

| 证据 | 等级 | 能推出 | 不能推出 |
|---|---|---|---|
| fixed `K` common-`P` | DERIVED | 无扰动 LPV 家族严格稳定 | RCI、扰动包含、硬约束、终端闭合 |
| fixed `K` torque support | COUNTEREXAMPLE | 该 `K` 在允许高推力路径下不能满足 RPI torque support | 其他 `K`、vertex/PWA policy、plant 不可行 |
| 30,000 static-`K` 搜索 | NUMERIC_CHECK | 冻结搜索盒内无样本通过全部有限必要检查 | static-`K` 不存在性 |
| 执行器权限 LP | NUMERIC_CHECK | 更宽策略类存在满足硬约束的有限轨迹；`W(T)` 显著优于全域盒 | 因果反馈、RCI、递归可行性 |
| axis-aligned RCI box | COUNTEREXAMPLE | 该集合类因积分器相关性严格不可能 | 相关多面体、椭球、CZ、参数相关集合 |
| 一个 19-pair cone | COUNTEREXAMPLE | 该单一 configuration cone 有 exact Farkas 不可行证书 | 其他 cone、orientation family 或其他 RCI 类 |

审计归档：`results/gate_a_control_baseline_audit_20261027/checks.json`。

## 3. 核心结论

**Gate A 仍为 blocked。** 仓库拥有名义稳定证书和若干候选/集合类/单一配置锥的
严格反例，但没有一个充分证书同时量化全部允许推力端点、扰动、状态限制和力矩限制。
因此以下升级均不合法：

- fixed-`K` 失败 -> 系统物理不可行；
- 随机搜索失败 -> static feedback 不存在；
- axis-aligned box 失败 -> correlated RCI 不存在；
- 单一 configuration cone 失败 -> 整个 orientation family 不可行；
- 有限轨迹可行 -> RCI 或 rolling recursive feasibility 已证明。

## 4. 文献准入与方向纠正

Mejari 等已经给出 configuration-constrained LPV RCI 与 vertex control 综合；
Mulagaleti 等已经给出带**已知参数变化集合**的 PD-RCI；Köhler 等的 nonlinear
tube MPC 又明确要求 incremental feedback、tube tightening、terminal ingredients 与
shift proof 一起成立才有递归可行性。故“固定法向 + vertex control”“调度相关集合”或
“状态/输入相关扰动”本身都不是本项目创新。

当前模型没有非平凡推力变化率，不能通过套用 bounded-rate PD-RCI 获得虚假的过渡集收缩。
同时，Run49--51 的局部 configuration-cone 邻接路线已经连续产出类特定否证，不能直接
解除控制闭环阻塞；本轮主动停止继续枚举。

## 5. 下一唯一问题

构造一个**充分**的 correlated controller/RCI 证书：保留 `W(T)`、未来推力任意跳变、
全部状态与 torque constraints，并用独立 support/reachable 检查反向攻击。若综合不可行，
结论只能限定到所选 controller/set class；除非取得 class-wide dual certificate，不能升级。

该四状态证书通过后仍只完成 Gate A 的降阶子问题；下一步必须写出与六状态模型中
`p_z,v_z,T` 通道、推力分配及非线性余项的接口，不能直接宣称六状态安全。

## 6. 复现

```bash
python -m unittest verification/test_gate_a_control_baseline_audit.py
python verification/check_gate_a_control_baseline_audit.py \
  --output /tmp/gate_a_control_baseline_audit.json
```

