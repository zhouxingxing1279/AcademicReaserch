# Run 132：间歇数据 terminal 近邻审计与阻塞重定位

日期：2026-09-29。文献准入见 [run132_literature_gate.md](run132_literature_gate.md)。本轮从未推送的 Run 131 提交 `27d7de1` 继续；远端 `main` 为 `1c49659`，远端最新研究分支仍为 Run 126 `c00d102`。

## 1. 本轮问题与判退规则

Run 131 把唯一优先问题定为“为 15-mode bounded-dropout automaton 构造或反驳 mode-indexed backup terminal family”。本轮先核查这个问题是否已经被 missing-data/path-dependent MPC 近邻覆盖，以及仓库是否具备实例化条件。

判退规则是：若已有工作用相同的有限数据语言、时变误差 tube 和 terminal shift 闭合递归可行性，则不能把 mode indexing 本身称作创新；若当前六状态合同没有合法 terminal feedback，也不得写只会通过所选数值样例的 set iteration。

## 2. 文献核查后的关键纠正

Hassaan--Pati--Shen--Yong 2021 是比 Run 131 文献更直接的近邻。它把 delayed/missing pattern 表成周期有限长度语言，使用 path/time-varying estimator 与 control tubes，并在 Assumption 2 中要求一个 common nominal terminal set `X_f`：该集合对 terminal feedback 不变，同时位于所有周期相位的 state-tightened constraints 中，反馈像位于所有 phase-dependent input-tightened constraints 中。Theorem 6 直接用旧 nominal sequence 移位与 terminal action 证明递归可行。

这改变了 Run 131 的优先级判断：**15-mode terminal family 不是先验必要骨架。** 更强且更简单的第一基线是一个对全部 dropout phases 有效的 common `K_f,X_f`。只有它为空或在同预算下过度缩小认证可行域，mode-indexed family 才可能有实际价值。

Rutledge--Yong--Ozay 2020 已用 missing-data language 表达连续丢包上界并在约束下合成 prefix feedback；其 Remark 3 还指出 zonotope template 可适配。Hassaan--Shen--Yong 2021 已进一步合成 path-dependent controller/estimator 和 reduced event language。Wildhagen 等 2022 则从 bounded packet loss 的 min-max MPC 方向证明递归可行、约束满足和收敛。故 `finite dropout automaton + indexed controller/set + terminal proof` 的各组件和主要组合已有充分近邻。

## 3. 仓库原始证据复核

- [05_intermittent_error_interface.md](../learning/05_intermittent_error_interface.md) 的 15 modes、17 edges、最大 15 tick 间隔，以及逐边 quadratic multinorm contraction，只认证 estimation-error homogeneous dynamics。
- [06_mode_dependent_nestedness.md](../learning/06_mode_dependent_nestedness.md) 已给出 reachable-mode envelope 的 shift inclusion，但明确 terminal/control ingredients 未实例化；统一 Young recursion 甚至在 `e_0=0` 时就会因过度保守而触碰原速度约束。
- `configs/planar_baseline.json` 中 `K`、`terminal_certificate`、`L_by_mode` 全为 `null`。
- 第33章以有限 reachable support 严格否定旧 hover-DARE `K` 的 torque 约束；第34--35章的 static-`K` 搜索无成功样本不是不存在证明；第36章给出更一般控制序列可行的数值证据，否定“执行器本身绝对不可能”的过度结论。

因此，本轮不能可信地构造 common 或 indexed terminal set。直接套用冻结四状态 Run 121 的 gain 会混用模型、扰动和执行器合同；把 estimator posterior 当作未来 disturbance 也会违反信息语义。

## 4. 命题与证据等级

- **文献事实：**有限 missing/delayed-data language、path-dependent controller/estimator、time-varying tubes、common terminal set 与旧解移位的组合已由 2020--2022 近邻覆盖。
- **条件性理论判断：**对全部 dropout phases 的 common `X_f` 是当前必须先复现的强基线；mode-indexed family 只有在 common baseline 被证伪或表现出实质保守性时才可能准入。
- **仓库事实：**当前六状态配置缺少 terminal/ancillary gain 与 certificate，旧候选已在当前 residual/torque contract 下被否定。
- **未证明：**common `X_f` 是否非空；是否存在合法 joint `K_f/X_f`；mode-indexed family 是否恢复更大认证可行域；CZ posterior support query 能否在 handoff 中提供同预算严格收益；完整六自由度四旋翼保证。

本轮没有新增控制代码或数值结果。文献门槛已经把问题前移到 certificate-based terminal feedback/invariant-set synthesis；现在实现 mode-indexed set iteration会跳过决定性前提。

## 5. 论文主线总审视

Run 127--130 已关闭 post-hoc CZ reduction；Run 131 排除了宽泛 two-layer tube 的首次性；本轮又排除了“先做 15-mode terminal family”的默认顺序。当前论文级主线仍未闭合，但阻塞已更精确：先在语义一致六状态/LPV/执行器合同上获得一个可独立检查的 terminal feedback 与 common terminal domain，再检验 posterior-aware tightening 是否能以相同预算扩大 domain 或改善闭环指标。

这不是回到第34--35章的随机 `K` 搜索。下一轮必须先精读并选择一类 certificate-based joint gain/invariant-set synthesis 方法，明确其 uncertainty class 是否覆盖 arbitrary thrust switching 与 local residual；不覆盖时只报告假设缺口，不能把数值 solver success 升级为闭环保证。

## 6. 验证与下一唯一问题

本轮基线与最终回归命令均为：

```bash
ACADEMIC_RESEARCH_NO_WRITE=1 python -m unittest discover -s verification -p 'test_*.py' -q
```

测试通过只说明仓库既有验证器未被文档更新破坏，不构成 terminal 命题证明。

下一轮唯一问题：**文献先行选择一类与 thrust-scheduled 六状态局部合同相容的、certificate-based joint `K_f/X_f` synthesis；以 Hassaan 2021 Assumption 2 为规格，形成 common terminal set 的有限可检查 feasibility problem，并给出已认证候选或 certificate-class 明确的不可行结论。** common baseline 未闭合前，不准入 mode-indexed family 或 posterior stage-tightening controller。
