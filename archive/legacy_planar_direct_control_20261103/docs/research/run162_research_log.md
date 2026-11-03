# Run162：短-dropout fallback 的权限反例

日期：2026-10-12；从Run161本地`ea90783`、远端`13ac69f`同tree `b255bf0d`接续；远端
`main=1c49659`。重读Dey--Bhasin adaptive update兼容条件、Lu等递归可行性移位证明，并复核
Lorenzen等recursive model update与Dey--Dhar--Bhasin two-tube结构。

核心纠正：测量到达串是环境选择，控制器不能在Run161 gate失败后把15-tick合同自行降级为
5/10-tick合同。短计划只有在终端进入覆盖剩余miss语言的robust invariant backup时才是fallback；
否则只是把未处理风险移出时域。当前仓库没有这种backup，且Run160已否定当前J14/global
residual/correction合同下15-tick full-state放松问题。因此本轮文献门槛不通过实现，只保留
`semantic_counterexample_to_short_dropout_fallback_under_uncontrolled_measurement_arrivals`。

下一唯一问题：二选一核查可交付性——通信层能否被控制器调用并认证“最多10次连续miss”；若不能，
则构造覆盖原15-tick语言的backup family，且必须使用改变后的seed/residual/authority合同。

验证：基础测试39/39、verification 226/226、compileall、135份JSON及`git diff --check`通过；
文献表哈希更新后的10份历史artifact删除`source_sha256`后载荷10/10不变。本轮未新增控制代码。

