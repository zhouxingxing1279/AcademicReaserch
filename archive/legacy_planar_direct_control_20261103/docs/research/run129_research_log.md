# Run 129：携证 Scott 消元首步的精确行预算障碍

日期：2026-09-29。文献准入见 [run129_literature_gate.md](run129_literature_gate.md)。本轮从未推送的 Run 128 提交 `c1dd18f`（tree `3709943`）继续；远端最新研究分支仍为 Run 126 `c00d102`。结论仅针对冻结四状态、605-generator 后验和 Run 126 的确定性 Scott 实现。

## 1. 文献准入与问题收缩

本轮全文定向重读 Scott 2016 Appendix (A.9)--(A.10)，精读 Kopetzki 等 2017 的 zonotope order-reduction 方法与评价，并重读 Sadraddini--Tedrake 2019 的生成元映射证书。另精读 Diaconescu 等 2026 Sections 3.1、3.4：预计算/携带 inclusion matrix 和行范数条件已有直接 MPC 近邻，不能作为创新。

因此本轮只审计一个可推翻的实现命题：从未压缩后验 `R_605 subseteq S_602=Y[-1,1]^602` 的显式映射出发，沿现有 Scott 列替换同步传播 `G_m=Y C_m`，再用 CZ equality 自由度修复行预算；是否至少能完成 605 到 604 的第一次非平凡消元？若失败即停止当前普通 Scott 路线，不扫描 603--539，也不退回通用巨型 LP。

## 2. 等式修正的逐行充分证书

当前 CZ 写成

\[
R_m=\{G_m\xi:\|\xi\|_\infty\le1,\ A_m\xi=b_m\},
\qquad G_m=YC_m.
\]

对任意矩阵 `Q`，在 equality slice 上

\[
C_m\xi=(C_m+QA_m)\xi-Qb_m.
\]

故若对每个目标系数行 `c_j` 都存在 `q_j` 满足

\[
\|c_j+q_j^\top A_m\|_1+|q_j^\top b_m|\le1,
\]

则 `R_m subseteq S_602`。每行仅有三个自由变量 `q_j`；绝对值线性化后是一个小 LP。该条件是已知 affine-generator containment witness 的直接特化，只是把 CZ equality 的零作用方向显式用于修正，不是新的集合包含定理。

其对偶为

\[
\max_{z,u}\;c_j^\top z
\quad\text{s.t.}\quad A_mz+b_mu=0,
\quad\|z\|_\infty\le1,\ |u|\le1.
\]

任一对偶可行点目标值大于 1，即可严格否定该行 witness，而不依赖 primal solver 的“不可行”状态。

## 3. 首步结果与精确复核

验证器首先复现 Run 126 的 maximum-volume basis 和 Scott 删除顺序，同时对基列放大同步更新 `C`，对未删除 residual columns 保持原谱系。604-generator 输出与原实现逐元素一致到 `2e-13` 相对容差；`Y C_604` 与实际状态生成元的最大 binary64 重构残差为 `6.938893903907228e-18`。

第一次消元后，602 个目标行中只有 4 行的朴素预算大于 1：

| 目标行 | 朴素行预算 | 等式修正最优值 | 精确对偶下界减 1 |
|---:|---:|---:|---:|
| 4 | 1.0000000650085386 | 1.0000000650085386 | 6.500853855229138e-8 |
| 27 | 1.0000000437770518 | 1.0000000437770518 | 4.377705176139557e-8 |
| 78 | 1.0000000787984658 | 1.0000000787984658 | 7.879846575242766e-8 |
| 601 | 1.0000000128686530 | 1.0000000128686530 | 1.2868653032072075e-8 |

四个 primal LP 都取 `q=0`。为排除 HiGHS 约 `1e-8` 级等式残差造成的假结论，验证器把 LP 给出的 dual proposal 解释为 binary64 精确有理数，并只在三个**零目标系数、严格位于盒内**的变量上重解 3x3 有理线性系统。归档的四个 witness 均满足：

- `A z+b u=0` 的精确残差为 `0/1`；
- 最大盒超限为 `0/1`；
- 精确对偶目标严格大于 1，最小严格间隔为 `1.2868653032072075e-8`；
- `q=0` 同时给出相同 primal 上界，故上述四行的最优值等于朴素预算。

因此，**对冻结 binary64 系数的精确有理数解释，当前 carried-map + equality-adjustment 充分证书在第一次 605→604 Scott 消元后已经不可行。** 这是对该证书类和该确定性消元的严格否定，不是 `R_604 not subseteq S_602` 的证明：Sadraddini--Tedrake 型生成元映射一般不必要，另一谱系、另一包含证书或真实集合包含仍可能存在。

## 4. 实现与测试

新增：

- `verification/check_run129_certificate_carrying_scott.py`：谱系传播、逐行 equality-adjusted primal、小型 dual、精确有理数 witness 修复与 JSON 报告；
- `verification/test_run129_certificate_carrying_scott.py`：覆盖 equality 修正确有作用的手算例、604 谱系重构、首步四行精确 dual 障碍和直接脚本入口；
- `results/controller_direction_closure_20260928/run129_certificate_carrying_scott.json`：原始预算、精确分数间隔、修复基和证据边界。

测试按 red--green 顺序建立：模块缺失、谱系 API 缺失、首步审计 API 缺失和 JSON 精确间隔字段缺失均先产生预期失败，再补最小实现。定稿前的完整验证命令与结果记录在本轮提交中。

完整回归命令：

```bash
ACADEMIC_RESEARCH_NO_WRITE=1 python -m unittest discover -s verification -p 'test_*.py' -q
```

结果：最终提交前 115 项测试全部通过，运行时间 79.507 s。

## 5. 证据等级与方向纠正

- **已证明（实现级）：** 冻结 Scott 链的第一次消元无法保留本轮 equality-adjusted carried row-`l1` witness；四个 exact-rational dual witness 给出严格下界。
- **已验证（数值实现一致性）：** 604 输出重放与 Run 126 实现一致，谱系状态重构残差为 `6.94e-18`。
- **未证明：** 604-CZ 真实不包含于 `S_602`；所有可能生成元映射都失败；任意 Scott basis/删除选择都失败；完整六自由度四旋翼保证。
- **停止项：** 不再沿当前普通 Scott 删除顺序扫描 603--539，不再以更多有限方向或百万变量通用 LP 补救。
- **课题总审视：** 这次结果关闭了一个便宜终端证书候选，但本身只是方向纠正，不是硕士课题创新。主线仍缺 terminal-compatible 固定复杂度算子、递归可行性闭环以及同预算四旋翼收益。

## 6. 下一轮唯一问题

先做文献门槛，再回答：能否把终端包含 witness 作为**删除算子的硬约束**，设计一个不使用 Scott `T(I+diag|r|)` 放大的单步替换，并在相同 605 后验上实际删除至少一列？比较对象必须包括 Kopetzki 的 constrained optimization reduction、Sadraddini--Tedrake/Diaconescu 的包含映射以及不压缩 605 基线。若只能得到通用模块拼接、巨型 LP，或不能删除任何列，则停止 post-hoc generator reduction，转向完整 terminal/tube 架构而非继续局部模板否证。
