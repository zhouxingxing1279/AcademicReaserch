# Run 130：终端 witness 约束降阶的文献否决与成功标准修正

日期：2026-09-29。文献准入见 [run130_literature_gate.md](run130_literature_gate.md)。本轮从未推送的 Run 129 提交 `1d5e9bc` 继续；远端 `main` 为 `1c49659`，远端最新研究分支仍为 Run 126 `c00d102`。结论仅针对冻结四状态合同、Run 123 的精确 posterior 与固定 `S_602` 终端 mRPI 前缀。

## 1. 文献结论：硬包含约束不是空白机制

本轮全文精读/定向重读三篇直接近邻：

- Sadraddini--Tedrake expanded arXiv:1903.05214 Section V-B、Proposition 6：直接把 reduced generator matrix 作为变量，在 outer containment 下优化 Hausdorff 上界；核心等式双线性，采用 projected sequential LP/交替求解。
- Kopetzki--Schürmann--Althoff 2017 Section III-D：在原 zonotope 被 reduced zonotope 包含的非线性约束下优化 reduced generators 与体积。
- Raghuraman--Koeln 2022 Section 5：用包含 encoding 做 zonotope/CZ inner-approximation order reduction；方向虽不适合 reliable posterior outer enclosure，但已覆盖“CZ reduction + containment constraint”的模块组合。

因此，把终端包含 witness 作为非-Scott reduction 的硬约束并不是新机制。当前严格差异只是把 CZ equality-aware outer inclusion 与另一个固定 target inclusion 串成

\[
R_{605}\subseteq R_{\mathrm{red}}\subseteq S_{602},
\]

属于既有包含模块的 sandwich 组合。其递归可行性价值仍须由完整 MPC/terminal 架构证明，不能从集合 sandwich 自行推出。

## 2. 退化解否定“删一列即成功”

精确 Run 123 posterior 的三条 measurement strips 是在 `S_602=Y[-1,1]^{602}` 的 latent box 内求交得到，故构造上已有 `R_605 subseteq S_602`。取 `R_red=S_602` 就从 605 generators、3 条 equality 变成 602 generators、0 条 equality，并满足两个包含关系。

这个解形式上一次删除三列，实际却丢弃全部测量信息并退化为固定 tube。因此 Run 129 提出的“实际删除至少一列”门槛过弱；generator count 下降不是控制保守性下降。

利用现有、未经修改的 Run 126 支持查询，在 10 阶预测、300 个冻结 controller-relevant queries 上比较 `S_602` 与精确 posterior：

| 诊断量 | 数值 |
|---|---:|
| 查询数 | 300 |
| `h_S602-h_R605 > 1e-10` | 300 / 300 |
| 最小支持损失 | 0.001958026923025623 |
| 中位支持损失 | 0.15964285349406954 |
| 平均支持损失 | 0.676475175763347 |
| 最大支持损失 | 2.341195601750166 |

最大损失出现在 stage 0 的负第一坐标方向：精确 posterior support 为 `0.006000000000000156`，固定 `S_602` support 为 `2.3471956017501663`。这些是冻结算例的数值观察，不是一般定理；但足以说明退化删列解在当前真实 tightening queries 上系统性丢失信息。

复现使用仓库现有 API（不写结果文件）：

```bash
python - <<'PY'
import numpy as np
from verification.check_run126_scott_cz_baseline import build_run123_posterior_cz, controller_directions, _scaled_source_constraints, _scaled_source_support
from verification.check_run122_run119_reproduction import F, HORIZON, _powers
source, _ = build_run123_posterior_cz(); powers = _powers(F, HORIZON + 1)
scaled = _scaled_source_constraints(source); loss = []
for k in range(HORIZON):
    for d in controller_directions():
        q = powers[k].T @ d
        loss.append(np.sum(np.abs(q @ source.generators)) - _scaled_source_support(source, q, scaled))
print(len(loss), sum(x > 1e-10 for x in loss), min(loss), np.median(loss), np.mean(loss), max(loss))
PY
```

原始输出：`300 300 0.001958026923025623 0.15964285349406954 0.676475175763347 2.341195601750166`。

## 3. 在线规模止损

对最直接的 604-generator map 参数化 `G_red=YB`，`B` 有 `602*604=363,608` 个条目；605→604 outer-inclusion map 有 `604*605=365,420` 个条目。尚未加入 equality 调整、绝对值线性化、dual variables 或双线性迭代，就至少有 `729,028` 个连续 map/generator entries。

该计数是直接参数化的保守规模下界，不是完整 CZ 非凸问题的精确变量数。但结合 Sadraddini--Tedrake 的双线性 projected sequential LP 和 Kopetzki 的 constrained nonlinear optimization，已足以否定“可作为便宜在线单步规则”的当前主张。Run 128 的一般 AH/CZ 证书规模问题并未被解决，只是换了参数化。

## 4. 证据等级与不实现决定

- **文献已覆盖：** ordinary zonotope 的 containment-constrained outer reduction；CZ containment-constrained reduction 也已有明确近邻，尽管 Raghuraman--Koeln 的 Section 5 是 inner approximation。
- **构造性已证明：** `R_red=S_602` 是满足本轮 sandwich 且删除三列的退化解；因此“删至少一列”不能作为有效贡献标准。
- **数值观察：** 当前 300 个控制查询上，退化解相对精确 posterior 全部严格更松，数值范围如上。
- **规模估计：** 直接 604-generator map 参数化在加入完整 CZ 约束前已至少 729,028 个条目。
- **未证明：** 不存在任何稀疏、结构化、终端安全并保留 posterior 收益的 reduction；不存在完整 backup/adaptive terminal 架构；完整六自由度四旋翼保证。

文献准入的创新/实现门不通过，因此本轮没有新增 optimizer、solver 依赖或测试。继续实现只会复现已有非凸 containment-constrained reduction，或以退化固定 tube 解制造“成功删除”的假阳性。

文档更新后的完整回归命令为：

```bash
ACADEMIC_RESEARCH_NO_WRITE=1 python -m unittest discover -s verification -p 'test_*.py' -q
```

结果：115 项测试全部通过，运行时间 77.292 s；`git diff --check` 通过。

## 5. 课题级方向纠正

Run 127--130 已形成连贯止损链：有限 stage directions 不能替代 terminal containment；通用 AH/CZ certificate 过大；carried Scott witness 首步失败；任意“删列”又可由丢弃测量信息的固定集完成。因此关闭 post-hoc generator-reduction 主线，不再扫描 604→539，也不再把局部列删除作为论文贡献。

完整课题仍未闭合。后续评价固定复杂度模块时，最低成功标准改为：可靠 outer containment；终端/backup 可接纳；与固定 `S_602`/固定 tube 在相同信息和计算预算下，全部实际硬约束 normals 不劣且至少一个控制指标严格改善；并有跨时刻 shifted-feasibility 证明。

## 6. 下一轮唯一问题

文献先行回答：能否构造一个两层 output-feedback tube 架构，使精确或按需查询的 SMF posterior 只负责 finite-horizon stage tightening，而独立的 backup/adaptive terminal tube 在 measurement dropout、posterior recenter 和旧计划移位时保证 recursive feasibility，且不要求每个 post-hoc compressed posterior 都落入固定 Run 121 mRPI？

必须先精读 Dey--Bhasin 2026、Köhler 等 adaptive robust MPC 以及 Ping 的 output-feedback/scaled-terminal 基线，明确哪些是已有 acceptance/backup 或 adaptive-terminal 结论。若两层机制本身已覆盖，只保留“间歇测量 + 固定查询预算 + 四旋翼执行器约束”中尚未解决的严格证明义务，不预先声明创新。
