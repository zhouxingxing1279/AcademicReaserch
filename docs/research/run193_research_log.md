# Run193 研究日志：当前调度可见 predecessor 合同纠正

日期：2026-10-28。

## 仓库接续与唯一阻塞

起点为远端 Run192 `69c3266`，远端 `main=1c49659`，启动工作树干净。Run192 的最高优先
阻塞仍是：冻结 `W(T)`、任意未来推力跳变、状态与 `|tau|<=0.08` 下缺少充分 correlated
controller/RCI。本轮没有继续 posterior/CZ 或 configuration-cone 几何，而先审查 predecessor
是否尊重“当前 `T` 已知”的控制信息时序。

## 文献准入

重读 Mulagaleti--Mejari--Bemporad 的 PD-RCI 定义、Sections 3.1--3.2及式(12)--(25)；
重读 Mejari--Mulagaleti--Bemporad Section III-C、Lemma 3证明、Problem 1与 Sections IV--V；
核查 Mejari--Gupta--Piga 的 gain-scheduled RCI 问题陈述。Hanema--Tóth--Lazar 仅核对机构页
摘要，不据此引用定理。准入只允许量词纠正与有限 predecessor 审计，不允许创新或 RCI 声明。

## TDD、调试与结果

先新增6项测试并观察缺模块 RED；最小 checker 实现后发现旧工件候选数未逐项复现。按系统
调试追溯到旧 checker 的 `canon`：硬盒单位法向含 Python `int`，`int/int` 产生 `float`，使
其声称的 Fraction-only 行构造从第一层起失效。新增回归测试先因缺审计字段 RED，再加入可
执行 legacy witness 与全保留行 Fraction 类型检查后 GREEN。

新 checker 对两种量词分别做 exact-rational 行生成与标量输入投影；HiGHS只用于冗余及双向
包含。共同力矩/调度可见路径在深度1--4的候选数分别为
`(17,31,99,903)` / `(17,31,85,489)`，非冗余 facets 都为 `(16,28,52,102)`；双向包含最大
violation `4.44e-16`，故只记为 `NUMERIC_CHECK` 的四层相同。该结果不是 RCI 或收敛证明。
旧归档的面数一致性不是手写断言：checker读取并哈希绑定Run152归档，逐层比较旧归档与修正
共同力矩路径的非冗余面数。候选数变化说明浮点泄漏确实改变了中间行表示，不能恢复旧版的
“精确投影”证据等级。

## 命题等级

- COUNTEREXAMPLE：旧 projected-predecessor checker 未保持其声称的全 Fraction 算术。
- DERIVED：真实信息时序是 `forall measured T exists tau(x,T)`；当前仿射合同下端点控制仿射
  插值覆盖内部推力。
- NUMERIC_CHECK：修正算术后两种量词的前四层保留多面体相同。
- OPEN：充分 scheduling-visible correlated RCI；六状态接口；terminal/shift与递归可行性。

## 下一唯一问题

不继续增加 predecessor 深度或局部 cone。选择一个能直接返回充分证书的调度可见 correlated
controller/RCI 综合，并独立核查全部顶点、推力端点、`W(T)`、state与torque constraints；若
失败，只否定该策略/集合类别。

## 复现命令

- `python -m unittest discover -s tests -v`
- `python -m unittest verification.test_scheduling_visible_predecessor -v`
- `python -m unittest discover -s verification -p 'test_*.py'`
- `git diff --check`

最终执行结果在提交前重新生成并核对；具体通过数写入本轮提交信息与中文简报，避免文档中的
静态数字因随后新增回归测试而失真。
