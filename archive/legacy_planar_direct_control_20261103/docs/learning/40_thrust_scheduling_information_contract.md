# 40 推力 scheduling 信息合同：当前模型只能认证任意跳变

日期：2026-09-24。承接第39章。仓库起点：`29449306f60c32e1d4999fa604e1b96b36cb4c90`。

## 1. 本轮唯一问题

第39章指出，是否允许使用 bounded-rate parameter-dependent RCI，取决于仓库是否真正拥有可证明的推力变化率信息。本轮只回答：**当前 frozen planar benchmark 是否支持一个非平凡的 `|T_{k+1}-T_k|<=rho` 合同？**

结论是否定的，而且不需要数值优化。

## 2. 仓库模型语义

`configs/planar_baseline.json` 把 `T` 直接列为输入，逐点约束

\[
T_k\in[4.905,14.715]\;\mathrm N.
\]

状态只有 `px,pz,vx,vz,phi,omega`，没有实际推力状态。`docs/research/01_model_and_bounds.md` 也明确写明：若执行器动态重要，应显式增加 `T_act` 并采用例如

\[
\dot T_{act}=(T_{cmd}-T_{act})/t_m,
\]

然后重新推导约束；不能默认 command 等于 actual thrust。

因此当前定义离散 benchmark 的 admissible input sequence 是点态笛卡尔积

\[
\mathcal U^{\mathbb N},\qquad
\mathcal U_T=[T_L,T_U],
\]

并没有跨时刻耦合约束。

## 3. 命题：任何非平凡 thrust-rate bound 都不由当前模型推出

**命题 40.1.** 在当前输入合同下，若希望

\[
|T_{k+1}-T_k|\le\rho
\]

对所有 admissible input sequences 成立，则必要且充分条件是

\[
\rho\ge T_U-T_L=9.81\;\mathrm{N/tick}.
\]

**证明。**

充分性：任意两个区间元素的距离不超过区间直径 `T_U-T_L`。

必要性：序列允许相邻两步取 `T_k=T_L`、`T_{k+1}=T_U`，二者都逐点满足输入约束，但

\[
|T_{k+1}-T_k|=T_U-T_L=9.81.
\]

故任何 `rho<9.81` 都被这个合法两步序列反例否定。证毕。

按 `h=0.02 s` 换算，区间直径对应 `490.5 N/s` 的离散斜率，但这里不把它解释为物理 actuator slew rate；它只是“任意两个合法离散输入端点可相邻出现”的数值换算。

## 4. 对 PD-RCI 的直接后果

Mulagaleti、Mejari、Bemporad 的 PD-RCI 框架考虑实时可测 scheduling parameter，并显式假设其变化量属于给定集合；该信息用于缩小当前参数 `p` 下可能的下一参数集合。

对本仓库，唯一无新增假设即可认证的 `rho` 是整个区间宽度 9.81。此时对任意当前 `T_k in [T_L,T_U]`，下一步可达 scheduling set 仍然是整个 `[T_L,T_U]`。所以这个“rate bound”**没有任何 transition-set reduction**，不能获得 bounded-rate PD-RCI 的保守性收益。

因此当前强 baseline 必须按：

> `T_k` 在求解/施加时已知，但未来 `T_{k+1},T_{k+2},...` 在区间内可任意跳变。

若以后希望采用 `rho<9.81`，必须修改物理/控制合同，例如增加 `T_act` actuator state、command slew constraint 或经过验证的 motor dynamics，并重新推导 residual、状态/输入约束和 RCI/MPC 证明。不能为了得到更大的 invariant set 事后添加 rate assumption。

## 5. 与文献的关系及创新边界

### Mulagaleti, Mejari, Bemporad (2025)

*Parameter-Dependent Robust Control Invariant Sets for LPV Systems With Bounded Parameter-Variation Rate*, IEEE TAC 70(2):1259–1266, DOI `10.1109/TAC.2024.3454528`, preprint `arXiv:2309.02384`。

论文系统为 `x+=A(p)x+B(p)u+w`，实时测量 scheduling parameter，并利用 bounded parameter variation 合成 parameter-dependent RCI 与 parameter-dependent vertex controller。其 configuration-constrained polytope 允许 facets/vertices 联合参数化。

可复用：如果未来四旋翼模型确实加入并认证 thrust-rate/actuator dynamics，该类 PD-RCI 是直接 baseline。

不可直接复用的假设：当前仓库没有非平凡 `Delta T` bound。因此不能把论文中的 bounded-rate transition set 直接套入当前 benchmark。

创新边界：`T`-dependent RCI、bounded-rate PD-RCI、configuration-constrained polytope 都已有直接近邻，不作为本项目创新点。

## 6. repeated predecessor 的含义

第39章已经证明 repeated predecessor 会产生 deeper-chain normals。现在信息合同闭合后，下一轮可以合法地采用 arbitrary-jump robust predecessor：每个未来步的 `T_i` 都独立属于 `[T_L,T_U]`。

这也给出一个重要方法边界：如果下一轮为了控制 normal growth 只枚举一个平滑 thrust trajectory，那不是当前 robust contract 的证明。必须覆盖所有允许 scheduling sequences，或者证明连续区间 worst case 可精确归约到有限 vertex sequences。

## 7. 可重复验证

新增：

- `verification/check_thrust_scheduling_contract.py`
- `results/thrust_scheduling_contract_20260924/checks.json`

运行：

```bash
python verification/check_thrust_scheduling_contract.py \
  --output /tmp/thrust_scheduling_contract.json
```

脚本直接读取 frozen config，并使用 `Decimal` 精确十进制运算。得到：

- `T_U-T_L = 9.810 N/tick`；
- 等价离散斜率 `490.5 N/s`；
- 当前状态中不存在 `T_act`；
- `rho<9.81` 被 endpoint alternation 反例否定；
- `rho=9.81` 不缩小下一 scheduling set。

这不是仿真观察，而是对当前仓库模型定义的直接逻辑核查。

## 8. 命题状态

### 已证明

1. 当前 benchmark 不蕴含任何 `rho<9.81 N/tick` 的 thrust-rate bound；
2. `rho=9.81` 与纯 pointwise interval contract 在下一参数集合上等价，因此不提供 PD-RCI transition reduction；
3. 当前合法 baseline 是 measured-current / arbitrary-future-jump scheduling。

### 被否定

> “可在不改变当前模型的情况下直接假设一个较小 thrust-rate bound，并利用 bounded-rate PD-RCI 减少保守性。”

该命题错误。

### 尚未证明

- arbitrary-jump scheduling 下 repeated-predecessor 是否可精确归约为 endpoint vertex sequences；
- endpoint sequence normal family 的增长速度以及是否存在有限 redundancy closure；
- 在该强合同下是否存在满足全部 hard constraints 的 nonempty correlated RCI。

## 9. 下一轮唯一优先问题

> **证明或反驳：在当前 arbitrary-jump thrust contract 下，有限深度 robust predecessor 对连续 `T_i in [T_L,T_U]` 的最坏约束是否可以精确归约到 endpoint sequences `T_i in {T_L,T_U}`；若可以，计算 normal family 随深度的增长与冗余。**

只有把连续 scheduling uncertainty 精确有限化，才能开始可信的 correlated-RCI certificate synthesis；不能用 thrust 网格代替证明，也暂不恢复 CZ 几何收益讨论。
