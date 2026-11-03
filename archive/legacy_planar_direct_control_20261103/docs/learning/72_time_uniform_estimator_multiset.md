# 15 模态 time-uniform 估计误差多集：存在性与控制接口否证

日期：2026-09-29。承接 [第 07 章](07_mode_radius_and_geometry.md) 与 [第 71 章](71_control_dependent_ancillary_contract.md)。

**结论：对冻结的六维线性估计误差 inclusion，15 个模式椭球组成的 time-uniform 不变多集存在，并已用有理数外包逐边核查；但最小 scalar/common-metric 半径下界在每个模式都使速度和角度 tightening 为空。因此它不能作为当前 MPC/ancillary 的 `E_eta^j`。这是否定证书类，不是否定 geometry-preserving SMF 多集。**

## 1. 信息时序与对象

沿用第 06--07 章的实际输入时序：以已执行 `u_k` 预测 `hat x_{k+1}^-`，随后按到达的 `y_{k+1}` 校正。模式 `j in {0,...,14}` 表示位置更新年龄；角度每 tick 直接更新。冻结线性 inclusion 为

```math
\eta^+=A_{ab}\eta+\bar G_{ab}\xi,qquad \|\xi\|_\infty\le1,qquad a\to b.
```

这里 `eta=x-hat x` 是状态估计误差，不是模型参数集合，也不是未来 process disturbance。17 条允许边、矩阵、噪声盒与 residual 边界均从 `check_mode_nestedness.py` 重算；不从旧 JSON 读入。

第 06 章已有模式度量 `P_j`，并逐边证明

```math
A_{ab}^T P_b A_{ab}\preceq (19/20)P_a.
```

令 `c=sqrt(19/20)`，以及

```math
q_{ab}=\max_{\|\xi\|_\infty\le1}
\xi^T\bar G_{ab}^T P_b\bar G_{ab}\xi,qquad d_{ab}=\sqrt{q_{ab}}.
```

则加权范数三角不等式给出 `||eta+||_{P_b} <= c||eta||_{P_a}+d_ab`。

## 2. Bellman 固定点与不变多集

在非负向量上定义

```math
[T(r)]_b=\max_{a\to b}(c r_a+d_{ab}).
```

`T` 对无穷范数是模数 `c<1` 的 contraction，故有唯一固定点 `r*`。从零开始的单调迭代收敛到它。若任一非负向量 `s` 满足 `T(s)<=s`，则 `T^n(0)<=s`，取极限得到 `r*<=s`；所以它是此 scalar/common-metric 类的最小不变半径。

定义

```math
E_eta^j={eta: eta^T P_j eta <= (r_j^*)^2}.
```

对任意边 `a->b`、`eta in E_eta^a` 和合法噪声，

```math
||eta+||_{P_b}<=c r_a^*+d_ab<=r_b^*,
```

故逐边包含成立。按 Athanasopoulos--Smpoukis--Jungers 的逐边判据，这构成冻结 inclusion 的 invariant multi-set。这里的 contraction 证明独立完成，不依赖该论文关于 full-dimensional C-set disturbance 的附加假设。

## 3. 有向舍入证书

验证器以 `10^-12` 网格包住所有平方根。下迭代使用 `c_lo,d_lo` 并向下舍入；上迭代使用 `c_hi,d_hi` 并向上舍入。若第 N 次上迭代为 `u_N`，残差

```math
delta=||T_hi(u_N)-u_N||_infty,
```

则

```math
u=u_N+delta/(1-c_hi) 1
```

满足 `T_hi(u)<=u`。脚本还独立检查 17 条边，而不是把迭代收敛当作包含证明。本实例在网格上 2048 次前已稳定，保存结果的 `delta=0`；上下界差仍保留平方根外包误差。

关键半径区间为：

| 模式 | `r_j` 下界 | `r_j` 上界 | 速度支持下界 |
|---:|---:|---:|---:|
| 0 | 7.365357238838 | 7.365357239200 | 7.365357238838 |
| 8（最小半径附近） | 7.014819479161 | 7.014819479523 | 8.612358074792 |
| 14 | 7.182172475658 | 7.182172476020 | 10.284675493963 |

完整分数和全部模式见 [结果 JSON](../../results/theory_mode_invariant_radius_20260929/exact_checks.json)。

## 4. 严格控制否证与物理范围

`P_j` 的角度块为单位阵，所以 `E_eta^j` 的角度支持就是 `r_j`；速度支持为 `r_j eta0^{-j/2}`。原状态区间的速度半宽为 3 m/s，角度半宽为 0.45 rad。验证器用**下界**证明：

- 15 个模式的速度支持全部大于 3 m/s；
- 15 个模式的角度支持全部大于 0.45 rad。

对任意中心，宽度大于原区间半宽的对称误差集不可能被平移进原状态区间。因此 nominal/estimate tightening 已为空；再加入 tracking tube 只会更差。这个结论不依赖 MPC 求解器或样本轨迹。

同时要严格限制“存在性”的语义：`d_ab` 来自已验证物理域内的 nonlinear residual 外包，而该椭球本身不能放入该域。因此本轮只证明**冻结线性 inclusion 的代数不变多集**，并没有得到一个自洽的全局非线性真值包含集。恰恰因为 domain closure 失败，它不能填入第 71 章的联合图。

失败源于 scalar/common-metric 几何：角度每 tick 测量误差实际只有 0.005 rad，但统一半径允许平移扰动能量全部分配到角度。第 07 章的同合同、保留生成元 25 步对照把角度保持在 0.005 rad，且所有坐标宽度低于原区间。这说明当前反例只否定椭球接口，不否定几何多集。

## 5. 文献边界与论文级判断

node-indexed invariant multi-set、minimal reachable multi-set 和有限外逼近已有 Athanasopoulos 等的直接理论；Hassaan 等又表明间歇数据 MPC 可使用 finite/periodic equalized-recovery error tubes，而不必要求 time-uniform invariant set。因此：

- Bellman 固定点是已知理论的直接特化；
- “15 模态不变椭球存在”不是创新；
- 本轮价值是严格关闭一个错误接口，并把剩余问题定位到 geometry-preserving、domain-valid 的 invariant outer multi-set。

## 6. 复现与下一唯一问题

```bash
PYTHONPATH=verification python -m unittest verification/test_mode_invariant_radius.py -v
PYTHONPATH=verification python verification/check_mode_invariant_radius.py --output /tmp/mode_invariant_radius.json
```

输出路径必须不存在。脚本只用 Python 标准库；`status=pass` 表示有理数算术、固定点外包和 17 条边检查通过，`control_gate=blocked_by_scalar_metric_geometry` 才是控制准入结论。它不证明 ancillary RCI、终端集合、递归可行性或闭环性能。

下一唯一问题：**在相同 15 模态、actual-input timing 与 residual domain 下，用 forward reachable sums 加 certified tail 构造 geometry-preserving 外不变多集，并判定其全部状态坐标支持能否闭合在物理域；若不能，给出最早严格阻断方向。** 只有该问题通过，才恢复第 71 章的联合 ancillary RCI。
