# Run 136：成功周期提升的 zonotope 估计误差不变多集

日期：2026-09-29。文献准入见 [run136_literature_gate.md](run136_literature_gate.md)，推导与证书边界见 [第 73 章](../learning/73_cycle_lifted_zonotope_multiset.md)。本轮从本地 Run 135 提交 `7ff1100` 继续；远端 `main` 为 `1c49659`，远端最新研究分支仍为 Run 126 `c00d102`。

## 1. 文献与准入

精读 Athanasopoulos--Smpoukis--Jungers 2017 的 forward reachable multi-set、outer approximation、逐边不变性和 T-product lift；重读 Kouramas--Raković--Kerrigan--Allwright--Mayne 2005 的 finite-sum scaling 外 RPI。两者都要求 full-dimensional C-set disturbance 才能直接使用对应缩放定理，而当前逐拍扰动 zonotope 秩亏。因此本轮准入直接的周期提升逐边证书，不套用不满足假设的尾公式；该构造属于现有理论的特化，不作创新声明。

## 2. 核心结果与证据等级

15-mode 丢包图的成功返回周期只有 5、10、15 tick。对每个周期精确合成 signed lifted matrix 和 disturbance zonotope，在 mode 0 求三个 lifted image 的最小分量外包盒，再沿 miss edges 保留生成元传播。

- **条件性解析证明：**三个周期 image 均包含于 mode-0 盒；14 条 miss edge 是生成元等式，3 条 success edge 是对应周期包含，故得到 time-uniform invariant multi-set。
- **精确算术核查：**3/3 周期、17/17 原图边通过；所有接受判定均为有理数。
- **状态域准入：**最坏 mode 14 支持为 `[0.608088,0.444613,2.754283,2.052858,0.005,0.01]`，逐坐标低于 `[5,1.5,3,3,0.45,2]`，估计误差 tightening 非空。
- **负对照：**15-tick x 速度真实 signed gain 为 `1/2`，逐拍绝对值 boxing 伪造为 `23/10>1`；因此停止使用逐拍 box 发散作否证。
- **未证明：**center/tracking/input 的联合 residual-domain closure、ancillary RCI、terminal、递归可行性与闭环性能。

## 3. 实现与验证

按 red-green 新增 `test_cycle_lifted_zonotope.py`：先观察缺少实现的两项预期失败，再新增 `check_cycle_lifted_zonotope.py`。测试覆盖周期闭合、17 边不变性、状态域余量和逐拍 boxing 负对照。归档 JSON 在 `results/theory_cycle_lifted_zonotope_20260929/exact_checks.json`，包含源码 SHA-256。

定向命令：

```bash
PYTHONPATH=verification python -m unittest verification/test_cycle_lifted_zonotope.py -v
PYTHONPATH=verification python verification/check_cycle_lifted_zonotope.py --output /tmp/cycle_lifted_zonotope.json
```

2026-10-01 独立复核：定向 2/2 测试通过；重新生成的精确 JSON 通过 3/3 成功周期、17/17 原图边检查，15 个模式的全部状态域余量为严格正数。mode 14 有 104 个生成元，最小速度余量为 `39314657/160000000`（x 速度）。完整命令 `PYTHONPATH=verification python -m unittest discover -s verification -p 'test_*.py'` 的结果为 **120/120 通过，131.667 s**。归档文件由这次重新生成的 JSON 复制；其 `source_sha256` 记录输入、验证器和第 73 章文档哈希。优化器成功或样本成员检查均未被当作证明。

本次重新查看 Athanasopoulos--Smpoukis--Jungers 原文 Sections 2.1--2.2、3.2、6.1：Proposition 1 给逐边可达包含判据；Assumption 2 要求每个扰动集为含原点内点的 C-set；Theorem 2 的缩放外包依赖 Assumptions 2--4。故本轮不把该缩放定理直接套到秩亏逐拍扰动上。原文：https://arxiv.org/html/1702.00598v1 。

## 4. 主线判断与停止规则

Run 135 的失败来自共同 scalar/metric 几何，不是估计问题本身不可闭合。本轮已把“可靠估计集合存在且 state tightening 非空”提升到 time-uniform 精确证书，因此停止继续优化估计集合。结果仍只是传统主线的必要接口，离硕士课题级完整方法尚缺 control-dependent joint ancillary RCI、输入硬约束、terminal/shift、同预算比较和四旋翼闭环。

## 5. 下一唯一问题

把 15 个 zonotope 的 exact support oracle 接入第 71 章实际推力相关联合 `(e,eta)` 图，在相同 state/input/residual 合同下构造或否定非空 mode-indexed ancillary RCI；若只能证明单方向余量或有限时域可行，则停止，不进入 terminal/controller 数值实验。
