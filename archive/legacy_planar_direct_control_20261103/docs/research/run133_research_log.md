# Run 133：ancillary tube 与 nominal terminal 证书分层纠正

日期：2026-09-29。文献准入见 [run133_literature_gate.md](run133_literature_gate.md)。本轮从本地 Run 132 提交 `d5a726c` 继续；远端 `main` 为 `1c49659`，远端最新研究分支仍为 Run 126 `c00d102`。

## 1. 本轮问题与停止条件

Run132 要求选择 certificate-based joint `K_f/X_f` synthesis，并按 Hassaan Assumption 2 实例化 common terminal baseline。本轮先核查：已有 joint controller/RPI 文献中的 feedback 与 invariant set，是否就是 Hassaan 终端假设中的 `K_f,X_f`。

停止条件为：若最近邻实际合成的是 disturbance-tracking inner controller，而 Hassaan 终端项作用于已收紧的 nominal dynamics，则必须先修正层次和符号；在 tracking tube 未知时，不得构造一个数值上无法定义 tightened constraints 的 terminal SDP。

## 2. 文献核查结果

Hassaan 2021 Section 3.1.2 与 Lemma 4 先设计 tracking controller，并由过程噪声与 estimation error 构造 control-error tube。Assumption 1 先要求这些 estimator/tracking tubes；Assumption 2 才要求一个对全部周期相位收紧约束有效的 nominal terminal gain/set。Theorem 6 的移位候选使用该 nominal terminal action。

Tahir 2010 则在 LTI additive-disturbance 系统上联合优化 feedback 与 RPI set；固定形状椭球用 S-procedure 给出充分 SDP，origin-centered axis-aligned box 用 Farkas 条件写成联合优化。Tahir--Jaimoukha 2012 把后者扩展到 norm-bounded model uncertainty与 additive disturbance。两者解决的是 ancillary/tracking RPI 层，不能直接替代 Hassaan 的 nominal terminal层。

2013 Tahir--Jaimoukha 论文的正式摘要也明确区分 inner RPI controller 与把状态导入 terminal set 的 outer MPC controller；本轮未取得全文，因此没有据此引用任何定理。Kothare 1996 本轮同样只核对正式页面与摘要，作为 constrained robust feedback synthesis 的经典背景。

## 3. 对仓库主线的实质纠正

此前把“合法 ancillary gain/不变域”和“terminal gain/common terminal domain”并列成一个缺失项不够精确。正确依赖关系是：

1. `K_c,S_c^j` 吸收过程扰动、estimation error 与重定心误差，并给出 phase-dependent correction-input 集；
2. 用全部 `S_c^j` 和 correction-input 集定义 common tightened `X_tight,U_tight`；
3. 再在无扰 nominal dynamics 上求 `K_f,X_f` 与 terminal decrease；
4. 用这个 common terminal action闭合旧名义计划移位。

所以当前阻塞仍在第1层，尚未到达 Run132 所写的 nominal `K_f/X_f` feasibility problem。当前配置的 `K`、`terminal_certificate`、`L_by_mode` 均为空，也与该判断一致。

## 4. certificate class 筛选

Tahir 2010/2012 的 origin-centered Cartesian hyperrectangle 不应实现。仓库第37章已经用精确一步反例证明该类在位置积分器与非零 residual 下不存在非空 RCI；重跑 SDP 不会增加证据。

固定形状椭球尚未被排除，但现有文献条件不直接覆盖本项目的 paired `(A(T),W(T))`：同一个推力 `T` 同时决定横向 LPV 矩阵和 residual 半径。若把 matrix uncertainty 与 global `W` 独立组合，就会丢失第35章修正的 vertex consistency。仓库对连续推力的 endpoint-exact 归约只证明于 polyhedral predecessor，不能自动套进 ellipsoidal S-procedure。

此外，当前没有完整六状态 estimator/recenter disturbance set 与 correction-input budget。故本轮没有足够数据构造 Hassaan tightened constraints，也没有一个与当前合同相符的最小 SDP 可写。

## 5. 命题与证据等级

- **文献事实：**Hassaan 的 tracking tube 与 nominal terminal set 是两个先后依赖的证书层；Tahir 2010/2012 联合综合的是前者所属的 disturbance-RPI 类型。
- **已证明的仓库事实：**origin-centered axis-aligned Cartesian RCI class 在当前积分链和非零 residual 下为空；不能把该类 infeasible 解释为执行器或所有 terminal sets 不可行。
- **条件性规范：**A 层必须保持同一 `T` 对应的 `(A(T),W(T))` 配对，并显式纳入 estimator/recenter 项；之后才可定义 B 层 common terminal feasibility problem。
- **未证明：**是否存在非轴对齐六状态 ancillary RPI/RCI；fixed-shape ellipsoid 是否可行；common nominal `X_f` 是否非空；mode-indexed family 是否有严格收益；完整非线性六自由度四旋翼保证。

## 6. 为什么不实现与验证边界

本轮不新增控制代码。实现 Tahir box SDP 会重复一个已严格否定的 certificate class；直接实现 ellipsoid SDP会把 LTI/独立 uncertainty 模型误当成当前 correlated LPV contract；直接实现 nominal terminal SDP则没有已定义的 tightened sets。三者都不能产生可审查的正结论或有意义的负结论。

仓库回归命令为：

```bash
ACADEMIC_RESEARCH_NO_WRITE=1 python -m unittest discover -s verification -p 'test_*.py' -q
```

通过回归只说明既有验证器未被文档更新破坏，不构成新控制命题证明。

## 7. 论文级主线与下一唯一问题

本轮不是继续局部法向或模板否证，而是修正递归可行性证明的依赖图。当前论文主线距离闭合仍有四项：六状态 A 层合同、非轴对齐 ancillary certificate、由其导出的 common terminal certificate、同预算 posterior-aware 优势及闭环验证。

下一轮唯一问题：**冻结六状态 ancillary/tracking error contract，并选择一个保持 correlated `(A(T),W(T))`、非轴对齐的有限证书类；构造可检查 feasibility problem并求得候选或给出该类明确反证。完成后才综合 nominal common `K_f,X_f`。**
