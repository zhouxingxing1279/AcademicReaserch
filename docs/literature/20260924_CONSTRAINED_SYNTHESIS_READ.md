# 2026-09-24 约束感知反馈合成文献核对

> 本轮新增核对记录。后续整理 `READ_PAPERS.md` 时应查重并合并；本文件保留本轮直接使用的原始来源细节。

## Kothare, Balakrishnan, Morari — Robust constrained model predictive control using linear matrix inequalities
- 年份/出处：1996, *Automatica*, 32(10):1361–1379。
- DOI：https://doi.org/10.1016/0005-1098(96)00063-5
- 稳定来源：https://authors.library.caltech.edu/records/t7km1-0q967
- 研究问题：在显式模型不确定性下，把 worst-case performance、输入约束和输出约束统一进 robust MPC/state-feedback synthesis。
- 方法概要：以 worst-case infinite-horizon objective 为目标，利用 LMI 把性能上界与约束处理转为凸优化，并给出对所考虑 uncertain plants 的 robust stabilization 结论。
- 与本项目关系：第34章之后需要的“直接考虑约束来合成 K”已有经典成熟基线，不能作为创新；可作为 common-quadratic/ellipsoidal constrained synthesis 起点。
- 局限：不是 rolling CZ-SMF posterior，也不回答 posterior correlation 如何降低真实 MPC support tightening。
- 本项目状态：作为下一轮约束感知 ancillary baseline。

## Pluymers, Kothare, Suykens, De Moor — Robust synthesis of constrained linear state feedback using LMIs and polyhedral invariant sets
- 年份/出处：2006, *American Control Conference*, pp. 881–886。
- 原文：https://ftp.esat.kuleuven.be/pub/SISTA/pluymers/reports/ACC06_Synthesis_using_Polyhedral_Sets.pdf
- 研究问题：对 polytopic uncertain discrete-time systems 合成满足约束的线性反馈，并降低 ellipsoidal invariant-set constraint handling 的保守性。
- 方法概要：扩展 Kothare 类 LMI synthesis 以处理 mixed state/input constraints 与 cost cross-terms，并引入 polyhedral invariant sets；论文报告相对 ellipsoidal handling 更优的 feedback/feasible-region 结果。
- 与本项目关系：说明“联合优化 feedback + invariant set + state/input constraints”已有直接先例。若本项目继续，只能把它作为 baseline，再研究 CZ-SMF posterior 的在线 support tightening 是否带来额外、可证明的 feasible-set 改善。
- 局限：不处理 set-membership measurement posterior、CZ complexity、shift nesting 或 adaptive support ledger。
- 本项目状态：作为下一轮 polyhedral constrained synthesis 强基线。
