# Run 128：通用 AH/CZ 终端包含证书的在线预算止损

日期：2026-09-29。文献准入见 [run128_literature_gate.md](run128_literature_gate.md)。本轮先核查远端和所有未合并研究分支：远端最新有效成果仍为 Run 126 `c00d102`；本地 Run 126 替代提交 `65aeaa7` 与它具有相同 tree `a215b46`，没有额外内容；Run 127 的严格终端反例只存在于本地提交 `df98eee`，此前推送因 HTTPS 无凭据失败。本轮从该本地提交继续，不重复生成反例。

## 1. 阻塞问题

Run 127 已严格证明 539-generator Scott CZ 不位于固定 mRPI `S` 内；下一问题原定为对同一 Scott 链 `m=539,...,605` 使用有限内近似 `S_M subset S` 与 sound AH/CZ certificate 做全方向准入。本轮先回答更基础且会决定是否值得编码的问题：Sadraddini--Tedrake 的通用证书能否在当前规模下成为在线机制？

## 2. 文献核查后的证明边界

Sadraddini--Tedrake Theorem 1 和 Theorem 3 都是可靠的充分包含编码，但一般不必要。故存在三条不能越过的边界：

- 证书可行可证明包含；
- 证书不可行不能证明不包含；
- CZ equality slice 不是满维 primitive，必须先作 nullspace 参数化，或独立对约束 box 的支持函数作对偶化，不能直接套公式。

Hellwig 等进一步说明，浮点 LP 成功仍须归档 witness，并用精确有理数或残差—裕量条件复核。Kulmburg 等只在本轮取得摘要，不据此作正文结论。Froese 等的固定维数 zonotope 算法不直接覆盖 CZ，但说明 exact containment 的一般计算负担不能被忽略。

## 3. 正确证书与规模推导

目标取 `S_602=Y[-1,1]^602 subset S`。对 `m` 个生成元、3 条等式的 CZ，nullspace 后 primitive 维数为 `m-3`、facet 数为 `2m`；目标 box 维数为 602、facet 数为 1204。Theorem 1 的主要变量为

\[
\Gamma\in\mathbb R^{602\times(m-3)},\quad
\beta\in\mathbb R^{602},\quad
\Lambda\in\mathbb R_+^{1204\times 2m}.
\]

因此 `m=539` 时共有 1,621,186 个连续变量，`m=605` 时共有 1,819,846 个；等式分别为 647,492 和 727,220 条，另有 1,204 条主不等式。避免 nullspace、直接对 `|xi|<=1,Axi=b` 的每个目标系数行做正负支持对偶，会得到约 1.63--1.83 百万变量，并未改变数量级。

Theorem 3 若把 CZ equality 全部丢掉，只认证其 zonotope 外壳，可降到约 65--73 万变量，但这是更强且不必要的条件；失败仍无否定意义。以上为精确维数计数，不是未经运行的速度主张。

## 4. 为什么本轮不实现

未压缩 `m=605` 候选已经由构造得到 `R_605 subseteq S_602`：602 个扰动变量生成 `S_602`，三个测量噪声变量只通过等式实施 strip intersection，不增加状态生成元。为重证该事实而解百万变量 LP 没有研究价值。

对 `m<605` 批量求这些 LP 也不满足本轮证据目标：

1. 可行只给某些点的冻结离线证书，不能自动给跨时刻在线算法；
2. 不可行既不能关闭候选，也不能定位真正终端违例；
3. 当前阶段基线按 67 候选、300 支持方向计时，通用证书的变量规模已不符合“同在线预算”入口；
4. 若只得到 605 可行，结论本已由构造知道，不应以大量计算伪装成新增证据。

因此文献门槛在实现前判为不通过。本轮没有新增验证器，也没有把有限方向或优化器状态当证明。

## 5. 证据等级与课题总审视

- **已证明：** Run 127 的 539-CZ 严格终端反例仍成立；605-CZ 由 measurement intersection 构造包含于 `S_602`。
- **条件性证明工具：** 通用 AH/CZ LP 可行时可证 `R_m subseteq S_602`；浮点结果还需 witness 可靠复核。
- **已核查复杂度事实：** 正确通用编码在本实例为约 160--180 万变量；zonotope 外壳版本约 65--73 万变量。
- **未决：** 是否存在某个 `m in {540,...,604}` 真包含于 `S_602`；通用充分证书不可行不能回答它。
- **方向纠正：** 不继续“局部分离方向 + 通用巨型 LP”循环。论文级主线需要把 terminal certificate 作为压缩算子的组成部分，而非压缩后的昂贵补救。

这使课题更接近一个完整方法问题：设计固定复杂度、certificate-carrying 的在线 CZ reduction，使真值外包、控制支持预算和 terminal inner-containment witness 同步传播；随后才能讨论同预算可行域/闭环优势。目前尚未形成第二个硕士课题方向，也没有创新性结论。

## 6. 仓库核查与验证

基线命令：

```bash
ACADEMIC_RESEARCH_NO_WRITE=1 python -m unittest discover -s verification -p 'test_*.py' -q
```

启动基线为 110 项全部通过（79.521 s）。文档定稿后再次执行相同全套命令，110 项全部通过（80.737 s）；`git diff --cached --check` 无错误。本轮没有代码变更。

## 7. 下一轮唯一问题

推导并审计一个 **certificate-carrying Scott elimination**：从 `R_605 subseteq S_602` 的显式稀疏系数映射出发，每次消去同时更新到 `Y` 的系数 witness，并检查目标 box 的逐行 `l1` 预算。先回答是否存在至少一次非平凡消去仍保留可靠 witness；若没有，给出可复现的首步结构反例并停止普通 Scott 压缩。不得退回百万变量通用 LP 或追加有限分离方向。
