# OIT / CZ / mRPI 验证原型

本目录实现 2026-11-05 研究验证；适用条件和研究判断见 [验证报告](D:/WorkSpace/AcademicReaserch/docs/research/proposal/OIT_MRPI_VALIDATION_REPORT.md) 与 [理论审计](D:/WorkSpace/AcademicReaserch/docs/research/proposal/OIT_MRPI_THEORY_AUDIT.md)。这是固定线性模型下的研究原型，不能直接当作任意系统的通用安全控制器。

## 接口

| 文件 | 主要内容 |
|---|---|
| `sets.py` | `LinearSystem`、`MPCConfig`、`ConstrainedZonotope(c,G,Aeq,beq)`、`HPolytope`、集合运算、包含充分证书、固定 CZ 模板比例综合 |
| `rpi.py` | 有限可达和、认证尾项、带正则化的 Raković 缩放、固定特征基迭代、固定生成方向 one-step LP |
| `estimation.py` | 量测交集、literal OIT、二维窗口消元、联合后验观测误差、固定偏置学习示例 |
| `control.py` | 双积分器、固定 K/L、联合 RPI 管、逐步遗忘历史的相容管束、终端集合和 QP |

`contains(outer, inner)` 返回含状态的字典；一般 CZ 使用 affine-lifting 充分 LP，`uncertified` 不等于“不包含”。`outer_reduce` 始终使用固定基盒外包，以满足证明所需的集合单调性；不是通用最小体积降阶器。`pontryagin_inner` 对 H 多面体约束逐行进行支持收紧。普通有限 CZ 不能直接表示无界量测条带。

配置结构是统一数据合同；本轮 `TubeMPC` 针对指定双积分器实例编写，并未实现接受任意 `MPCConfig` 的通用控制器工厂。窗口估计消元也针对二维位置观测的可观结构。

## 运行与数据

在 `D:\WorkSpace\AcademicReaserch` 使用本仓库 `.venv\Scripts\python.exe`：

```powershell
.\.venv\Scripts\python.exe -m experiments.oit_mrpi_verify --stage all
.\.venv\Scripts\python.exe -m experiments.oit_mrpi_audit
.\.venv\Scripts\python.exe -m experiments.oit_mrpi_plots
```

已有阶段不会重复计算；覆盖重算需 `--replace-stage`。数值代码变化后，应只重跑受影响阶段并重新审计。绘图命令读取保存结果，不重新模拟。测试入口为 `-m unittest tests.test_oit_mrpi -v`。

结果目录为 [oit_mrpi_20261105](D:/WorkSpace/AcademicReaserch/experiments/results/oit_mrpi_20261105)。

| 文件 | 数据口径 |
|---|---|
| `static.json` / `static_sets.csv` | 六种静态算法、统一字段、证书与系统；不可用指标为 null / 空列，并给原因 |
| `theory.json` / `reduction.csv` | A–D 的证书、反例和降阶比较 |
| `estimator.json` / `paper_observable.csv` | 模型复现、窗口 CZ 和 literal OIT；`snapshots` 保存 CZ 与 OIT 半空间 |
| `matched.json` / `matched_information.csv` | 同一创新记录下的集合比较；`runtime` 是整个查询任务耗时，不是单方向耗时 |
| `feasible.json` / `feasible_grid.csv` | 固定信息切片，31×25 个名义初始点；不等于一般闭环吸引域 |
| `closedloop.json` / `closedloop_detailed.csv` | 三控制器的配对轨迹；JSON 另保存各拍后验、预测管及固定模板引用 |
| `montecarlo.json` / `monte_carlo_10000.npz` | 10,000 条完整噪声轨迹、状态/输入/创新；集合按下述合同重构 |
| `controller.json` | 全精度 K/L、联合动力学、RPI 模板、终端集合、时域与窗口 |
| `audit.json` / `manifest.json` | 独立结果审计、强基线比较与源码/数据校验值 |
| `delivery_records.json` / `delivery_records.csv` | 任务书统一字段索引；源行号、缺失原因、单位和计时口径；由保存数据直接导出 |

各任务专用 CSV 使用不同列名；静态表完整覆盖任务书字段，动态表的系统常量位于 `controller.json`。例如 matched 的 `generators/equalities/runtime` 分别为生成系数数、等式数、完整集合查询耗时，不能直接当作 MPC 求解时间。未计算的高维 Hausdorff 与体积不得填 0。

统一字段索引可用 `.\.venv\Scripts\python.exe scripts/export_oit_mrpi_records.py` 从保存记录重新导出，不运行数值实验。其 `source_row_index` 是相应 JSON 的 `rows` 内从 0 开始的索引；聚合记录为 null。导出后运行审计更新结果校验值。

## 重构 Monte Carlo 的估计集和预测管

```python
from pathlib import Path
import numpy as np
from experiments.oit_mrpi_closedloop import reconstruct_mc_sets

archive = Path(r"D:\WorkSpace\AcademicReaserch\experiments\results\oit_mrpi_20261105\monte_carlo_10000.npz")
Xhat, tube = reconstruct_mc_sets(archive, trajectory=37, k=15)
with np.load(archive) as data:
    assert Xhat.point_contains(data["x_true"][37, 15])
```

轨迹索引为 0–9999，状态时刻为 0–30，控制时刻为 0–29。`Xhat` 为绝对状态估计集；`tube[i]` 为联合误差 `(epsilon, d)`，真实状态误差需用 `[I I]` 投影，输入误差需用 `[0 K]` 投影。重构使用保存的创新和已知 `hat_x-z` 历史及当前控制器合同；使用前检查 manifest，不能在改变 K/L、边界条件或窗口算法后声称重构的是旧实验。

大样本实验全部通过了无约束最优解的可行性验证，所以没有执行在线 QP；详细闭环记录才覆盖边界初值和实际受约束 QP。两者用途不同，不应混合计算控制器最坏延迟。

`window_estimate` 还调用既有 `src/outerloop/finite_memory.py` 的二维消元助手；该文件没有列入原阶段的源码哈希集合，属于复现追溯的已知边界。保留工作区版本；不能仅凭主包哈希断言所有传递依赖均已冻结。
