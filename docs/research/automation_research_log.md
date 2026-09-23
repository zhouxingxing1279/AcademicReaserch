# 自动研究日志

## 2026-09-23 — 任意多等式 CZ 支持查询认证

### 本轮问题

第 20 章固定后验实验只能对“3 潜变量 + 1 等式”的 CZ 重建原始顶点。连续 SMF 历史会产生多条等式，因此当前性能证书不能直接进入滚动 CZ 后验。本轮目标是补齐一般 \(A\xi=b\) 的可信支持查询接口，并核对它是否与现有文献创新边界冲突。

### 查阅/核对文献

1. Scott et al., *Automatica* 2016 — CZ 定义、精确集合运算与复杂度约减。
2. Le et al., CDC-ECC 2011 — zonotopic SMF 与 tube MPC 已有组合先例。
3. Rego et al., *Automatica* 2020 — nonlinear set-valued estimation 的 CZ guaranteed propagation/update。
4. Cong, Wang, Zhou, *Automatica* 2025 — SMF 初值稳定性与快速 CZ-SMF。
5. Qiu et al., IET CTA 2020 — ellipsoidal set-membership output-feedback MPC。

完整摘要见 \`docs/literature/READ_PAPERS.md\`。

### 理论推进

对

\[
\mathcal Z=\{c+G\xi:A\xi=b,\|\xi\|_\infty\le1\}
\]

和方向 \(p\)，任意乘子 \(\lambda\) 给支持上界

\[
U=p^\top c+\lambda^\top b+\|p^\top G-\lambda^\top A\|_1.
\]

任意经精确核验的成员 \(\xi^f\) 给下界

\[
L=p^\top(c+G\xi^f).
\]

因此原始/对偶证书可以解耦：数值 LP 只负责产生提案；有理数验证决定是否接受。原始重建失败不影响安全上界。

新增通用成员重建：选择满秩列基 \(B\)，非基变量有理化，精确求解

\[
\xi_B=A_B^{-1}(b-A_N\xi_N),
\]

再严格检查等式与盒约束。它是 validator，不是任意病态 LP 提案都成功的定理。

### 代码实验

运行：

\`\`\`bash
python verification/check_generic_cz_support_certificate.py \
  --output /tmp/generic_cz_support.json \
  --seed 20260923 --cases 600
\`\`\`

本地实际结果：

- 600 个随机有理数、满行秩、多等式 CZ；
- 600/600 重建出精确成员；
- 600/600 通过独立数值最优值审计 \(L\le h^\star\le U\)；
- 该批样例 600/600 得到 \(L=U\)；
- 最大认证 gap = 0。

单元测试：

\`\`\`bash
python -m unittest verification/test_generic_cz_support_certificate.py -v
\`\`\`

3 项通过：多等式成员重建、任意非最优乘子的上界安全性、固定种子压力子集。

### 不能据此声称的结论

- 600/600 不是对任意 CZ 重建成功率的理论保证；
- 本批矩阵不是病态对抗样例；
- 不能把“通用 CZ 支持 LP”或“SMF + Tube MPC”作为创新；
- 尚未证明滚动闭环下证书优先查询在总时间上优于全查询；
- 尚未进入部分观测四旋翼，也没有新的 ISS 结论。

### 保留候选创新

保留“可行性与性能双证书驱动的控制相关集合计算”。本轮贡献只是把它从单等式特例推进到一般历史 CZ 可用的 primal/dual 认证接口。

### 被否定/收缩的说法

- “CZ 与 Tube MPC 的结合本身有创新性”：否定，已有直接近邻。
- “固定后验中 LP 查询减少即可说明在线更快”：否定，QP 重解和历史 CZ 处理成本可能抵消。
- “数值 LP 成功就能把原始点当成员”：否定，必须精确等式/盒核验。

### 下一轮最关键任务

把本轮认证器接入 \`check_constrained_zonotope.py\` 的连续 \`predict/observe\` 历史 CZ，然后在约束活跃的滚动任务上比较 0-query / full-query / fixed-order / certificate-priority 四种策略。重点搜索“LP 数减少但总墙钟更差”的反例，并禁止跨后验直接复用旧原始成员点。
