# 研究短检查点（2026-09-28，Run 125）

主命题：可靠 SMF 集合进入输出反馈 tube MPC 的收紧、终端、递归可行性与同预算优势；学习暂停。仓库：`main` 1c49659c；本轮基于 `research/run124-recenter-compression` c2f6188。

本轮精读 Sadraddini–Tedrake 2019 Sections III–IV（AH/zonotope 包含充分编码及非必要反例）和 Kouramas–Raković 等 2005 Sections II–V（外 RPI 近似；要求满维 C-set，不能直接用于秩一 `W`）。对 Run-124 实际非零 `d0` 找到方向 `r` 和 posterior 可行 witness；浮点仅提议，三条测量约束、602 个 box 变量、前600项及139步无限尾均用 `Fraction` 复核。证明 `h_C(r)-r^Td0-h_S(r)>0.0023726854`。因精确 `det(F)=0.6999615978!=0`，对应终端方向满足 `h_EN-h_S>0`，故该候选 **严格不包含于固定 mRPI**，不是仅缺证明。

结论：停止 Run-124 非零重定心支线；300行模板只保留为安全压缩基线。下一唯一问题：取得并精读 Robbins et al. ACC 2026 全文，按相同信息/硬约束/在线预算复现其 zonotope 外包收紧强基线；仍不可得则用 Scott 2016 外包作替代并标未知。
