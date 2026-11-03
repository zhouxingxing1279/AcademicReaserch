# Run161 文献准入卡：`k=14` 合同三因素权衡与信息接口

## 最近邻正文核查

1. **Lu--Cannon--Koksal-Rivet 2021（开放全文，本轮新增精读）**：Sections 3.1--3.2、
   Lemma 1、Section 4.1 Proposition 1、Section 5.2 Theorem 3。论文把状态/输入硬约束下的
   fixed-complexity parameter-set update、预测 tube 与旧解移位闭合；在线不确定集变小可减少
   conservatism，但对象是常参数集合，不是当前状态后验或未来逐拍 residual。
2. **Köhler--Müller--Allgöwer 2021（全文定向重读）**：Section III-C、Section IV-B、
   Assumption 7、Theorem 4。online estimation-error bounds 可进入 finite-horizon tightening，
   但 augmented terminal ingredients 仍负责 shift/recursive feasibility；“当前估计更紧”不能
   单独替代尾端兼容性。
3. **Dey--Bhasin 2025/2026（全文定向重读）**：Sections IV-A--F、Criterion 1、Theorem 2、
   Appendix IV。更新后的 tube/terminal ingredients 必须通过 consecutive compatibility gate，
   否则保持旧参数/集合。因此 realized posterior contraction 与 uniform recurrent guarantee 是
   不同量词。
4. **Robbins--Glunt--Thompson--Pangborn 2026（仅正式摘要与书目信息）**：覆盖 nonlinear error
   reachability、online tightening 与 CZ-to-zonotope 外包；正文仍不可得，不能据摘要判断其
   terminal/recursive-feasibility 条件或 claim novelty。

## 差异、最强基线和证明义务

本轮不提出新的 adaptive MPC。最强基线是上述 online-bound/adaptive-tube 方法；项目特定问题只
是把 Run160 的 `k=14` necessary bound 写成三个可审计参数的精确半空间：seed 在唯一控制方向的
半直径缩放、未来 residual 缩放与 correction authority 缩放。一般后验须用两侧支持
`[h_X(a)+h_X(-a)]/2`，不能沿用中心对称 seed 的单侧支持。必须明确：state posterior、model
parameter set、future disturbance set 是三个不同对象；只有第一项可能由当前 SMF 测量更新直接
收缩，且仅对 realized information set 有效。

## 推动作用与可证伪条件

若精确权衡显示任何单因素修改都不现实，则应删除15-tick dropout constituent，而不是继续调
gain。若 current SMF 能在同一 disturbance guarantee 下认证所需方向半直径，并有 backup/compatibility
机制，则该阈值可成为在线准入规则的必要门槛。算术关系、`k=14` 时序、`g_r=hU` 或集合对象分类
任一错误都会推翻本轮结论。

## 判断

**通过项目特定的 exact contract trade-off 与 information-interface audit；不通过算法创新、
充分可行性、递归可行性、RCI或六自由度保证声明。**
