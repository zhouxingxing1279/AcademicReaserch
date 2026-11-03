# Run 127：539-generator Scott CZ 的终端 mRPI 反例审计

日期：2026-09-29。文献准入见 [run127_literature_gate.md](run127_literature_gate.md)。远端 `main` 为 1c49659c，研究起点为 `research/run126-scott-cz-baseline` c00d102（tree a215b46）。本轮不提出新算法，只核查 Run 126 的阶段准入结果是否满足递归可行性所需的固定终端条件。

## 1. 文献结论与问题边界

本轮定向精读 Köhler–Müller–Allgöwer 全文 pp. 5--6 的 set-membership 更新、pp. 9--10 的 Assumption 7、Theorem 4 与递归可行性证明。旧解移位的最后一步明确由 terminal ingredients 封闭，不能由有限个阶段 tightening 方向通过替代。Scott 2016 的外包降阶只保证原 posterior 包含于压缩集；它不保证压缩集仍位于另一个指定 mRPI 内。Dey–Bhasin 2026 的在线 tube/terminal 更新是强近邻，本轮只做冻结实现审计。Robbins 2026 正文仍不可得，首次性保持未知。

准入判断为：**通过既有实现的终端包含/分离审计，不通过新算法或创新声明。**

## 2. 终端问题的等价化

令 Run 126 的 539-generator CZ 为 (R)，一步扰动为 (W=D_0G[-1,1])，固定 mRPI 为

\[
S=\bigoplus_{i=0}^{\infty}F^iW.
\]

30 步终端误差集合为

\[
E_N(R)=F^NR\oplus\bigoplus_{i=0}^{N-1}F^iW.
\]

由支持函数可加性与 mRPI 的无限和分解，对任意 (q)，

\[
h_{E_N(R)}(q)-h_S(q)
=h_R(F^{N\mathsf T}q)-h_S(F^{N\mathsf T}q).
\]

冻结模型的 (F) 精确非奇异，所以 (r=F^{N\mathsf T}q) 遍历全部方向。因此

\[
E_N(R)\subseteq S\quad\Longleftrightarrow\quad R\subseteq S.
\]

这不是有限方向近似；它把终端包含完整地化成当前压缩集对固定 mRPI 的包含。

## 3. 反例证书

数值搜索只用于提出方向

\[
r=(-0.10057934443193688,-0.16340010131277027,
0.95599338253951383,0.22194786528659646).
\]

随后不再依赖浮点最优值作最终判断：

1. 将 Run 126 生成的 539-CZ 二进制浮点系数逐项解释为精确有理数；
2. HiGHS 只提出系数符号/基，索引 3、4、5 的三个自由变量由有理数线性方程重算；
3. 精确检查三条等式残差为零且全部 539 个系数位于 `[-1,1]`；
4. 以 900 个精确冲激项加 139 步 contractive block-tail，给出 intended rational mRPI 的支持上界；
5. 用精确 (F^{-N\mathsf T}r) 映射回终端方向，残差严格为零。

证书结果：

| 量 | 值 |
|---|---:|
| 539-CZ 可行点支持下界 | 0.029465947299252043 |
| mRPI 支持上界 | 0.029465855976498236 |
| 其中 900 项之后的安全尾界 | 2.2630790089128716e-9 |
| 严格支持差下界 | **9.132275380955128e-8** |
| 浮点 LP 等式残差（诊断） | 1.4224732503009818e-16 |

最终正差是有理数比较，不是“超过求解器容差即当作证明”。它严格否定冻结二进制浮点实现的 (R\subseteq S)，进而严格否定其 (E_N(R)\subseteq S)。

## 4. 结论、证据等级与限制

- **反例否定：** Run 126 的 539-generator CZ 虽在 `1e-8` 阶段准入阈值下通过 300 个查询，仍不满足固定 Run 121 terminal mRPI 包含，因而不能据此宣称完整递归可行。
- **实现级精确证书：** CZ 一侧是冻结 Scott 程序产生的 binary64 系数的精确有理数解释；mRPI 一侧使用 intended rational 模型。结论针对该实际实现。
- **不是一般定理：** 不否定所有 Scott 降阶、不证明 539 是一般下界，也不外推到六自由度非线性四旋翼。
- **方向纠正：** 不把该分离方向追加到阶段模板后继续局部修补。完整准入必须直接认证压缩集位于 terminal mRPI，或改用随在线集合更新且有备份集合证明的终端结构。

该结果关闭了“以 300 个阶段方向通过作为完整压缩准入”的路径。它是关键否证而非硕士课题创新；主线仍缺一个可实现、完整且同预算有优势的 terminal-aware 压缩/更新规则。

## 5. 复现文件与命令

- `verification/check_run127_terminal_cz_audit.py`
- `verification/test_run127_terminal_cz_audit.py`
- `results/controller_direction_closure_20260928/run127_terminal_cz_audit.json`

JSON 归档被审计 CZ 的全部 binary64 系数（`float.hex()`）、539 维 witness 的 box-sign 串和三个精确基变量，以及关键支持量/尾界/间隔的完整分数。`test_saved_exact_artifact_replays_without_linprog` 将 `linprog` 替换为报错函数后仍能重放证书，因而持久化结果不依赖再次求解 LP 或再次执行 QR 降阶。

```bash
python verification/check_run127_terminal_cz_audit.py
ACADEMIC_RESEARCH_NO_WRITE=1 python -m unittest verification.test_run127_terminal_cz_audit -v
ACADEMIC_RESEARCH_NO_WRITE=1 python -m unittest discover -s verification -p 'test_*.py' -q
```

完成前独立复验：Run 127 定向测试 5/5 通过（含 solver-free artifact replay）；Run 126 回归 8/8 通过；Run 120 精确有理数 mRPI 余量脚本通过；补强后全套 110 项测试于 109.710 s 内通过；`git diff --check` 无错误。

## 6. 下一轮唯一问题

构造并执行一个**全方向、方向正确的终端准入证书**：优先检验能否用有限内近似 (S_M\subset S) 与 AH/CZ 包含充分证书认证 (R_m\subseteq S_M)，并在同一 Scott 消去链上比较 (m=539,\ldots,605)。若只有未压缩的 605-generator 后验可证，则停止把普通 Scott 降阶当作完整控制基线；不得只追加本轮分离方向或继续随机扫描。
