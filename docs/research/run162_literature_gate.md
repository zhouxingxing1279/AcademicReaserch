# Run162 文献准入卡：方向宽度 gate 与 fallback 语义

## 最近邻核查

1. **Dey--Bhasin 2026（全文定向重读）**：Criterion 1、Algorithm 1、Theorem 2与Appendix IV；
   adaptive tube更新失败时保留旧参数/集合，backup仍由旧解移位与终端条件封闭。
2. **Lu--Cannon--Koksal-Rivet 2021（全文重读）**：Section 4.1 Proposition 1；递归可行性来自
   嵌套不确定集、移位候选与terminal set，不来自单个在线收缩指标。
3. **Lorenzen--Cannon--Allgöwer 2019（正文/作者稿既有精读，本轮定向复核）**：set-membership
   model update服务于robust constraints；稳定性与约束保证分别处理，不能用当前状态估计替代未来
   uncertainty contract。
4. **Dey--Dhar--Bhasin 2022（全文既有精读，本轮复核摘要与递归可行性结构）**：two-tube方案的
   fallback仍依赖不变estimation-error set和terminal闭合，不允许删除环境扰动分支。

## 差异、证明义务与可证伪条件

本轮不提出新fallback。项目特定问题是dropout长度由环境自动机选择，而不是MPC可控horizon。
要接受“短-dropout fallback”，必须证明通信调度能强制缩短语言，或短计划终端进入覆盖剩余miss的
不变backup family。任一证书存在即可推翻本轮阻塞；当前仓库两者都没有。

## 判断

**不通过在线切换器实现；通过语义纠正与停止规则记录。** Run161 gate暂时只能作为必要拒绝条件。

