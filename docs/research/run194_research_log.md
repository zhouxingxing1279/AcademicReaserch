# Run194 研究日志：同心 `S4` 的精确 RCI 否证

日期：2026-10-28。

## 仓库接续

远端`main=1c49659`；接续Run193远端`aae3a53`，新分支
`research/run194-self-predecessor-rci-gate`。启动工作树干净。只读取Run193短检查点、checker、
工件和本轮相关文献记录，没有继续posterior/configuration图扩张。

## 唯一问题与准入

检查Run193最强有限层形状能否通过同心缩放升级为真正RCI。Rungger--Tabuada说明有限下降层
一般不具不变性；Mejari等的configuration-constrained和PD-RCI vertex control是直接强基线。
准入只允许否定`alpha*S4`，不允许一般RCI或六状态结论。详见`run194_literature_gate.md`。

## 探索、TDD与精确结果

一次性探索脚本先定位可能的低推力顶点矛盾，未保留为产品代码。随后按TDD新增5项测试：首次
运行因checker不存在而RED；实现最小checker后4项通过、归档复现因工件尚未生成而RED；生成
哈希绑定工件后5项全部GREEN。

checker重建Run193的16/28/52/102-facet层。S4行选择沿用HiGHS，故模板选择仍为
`NUMERIC_CHECK`。冻结后，精确验证一个5-facet活跃、法向秩4的有理顶点。低推力端点两条
后继facet给出

`tau_lower-tau_upper=(5626543/1569600) alpha + 6254383/174400 > 0`

对全部`alpha>0`成立，且不使用`|tau|<=0.08`。证据等级为针对冻结homothetic模板类的
`COUNTEREXAMPLE`。

## 限制与下一问题

不排除不同法向、独立offset、非同心、PWA、gain-scheduled或PD-RCI集合/控制器。Gate A仍
blocked。下一轮唯一问题是实施一个独立offset的configuration-constrained vertex-control
综合，并对返回候选做独立精确/容差审计；失败只否定该模板与综合合同。

## 复现命令

- `python -m unittest verification.test_homothetic_s4_rci_gate -v`
- `python -m unittest discover -s tests -v`
- `python -m unittest discover -s verification -p 'test_*.py' -v`
- `git diff --check`
