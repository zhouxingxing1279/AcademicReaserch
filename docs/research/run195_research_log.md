# Run195 研究日志：调度可见 19-pair 配置锥的精确复核

日期：2026-10-28。

## 仓库接续

远端`main=1c49659`；接续Run194远端`5565959`，分支
`research/run195-scheduling-visible-19pair-farkas`。启动工作树干净，先执行39项基线测试并
全部通过。定向读取Run194检查点、第44--51章及相应checker后发现：“独立offset CC综合”
历史上已经完成，但旧19-pair实现采用每个顶点一个共享力矩，仍是`exists tau forall T`量词。
因此本轮没有重复综合，而是复核正确的当前推力可见量词。

## 文献准入与唯一问题

精读Mulagaleti--Mejari--Bemporad的PD-RCI定义、Proposition 2及PD vertex law；其调度参数在
控制前可测，控制为`u(x,p)`。重读Mejari--Mulagaleti--Bemporad的Lemma 3及CC-RCI综合；其
非PD基线给每个集合顶点一个共享输入。两者共同确认旧LP是更保守基线，而非当前合同的完整
权限。Abbas等仅核查可得问题设置和递归可行性材料，未计入全文精读。准入仅允许审计同一
19-pair锥，不做首次性或一般不可行声明。

## TDD、数值审计与精确证书

先写7项行为测试，首次运行因新checker不存在而RED。实现后6项通过，归档复现因结果文件尚未
生成而RED；生成结果后7项全GREEN。整分支自审又发现冻结合同未绑定下侧状态/力矩界；新增
漂移反例先RED，再补断言并重建工件，最终专项8项GREEN。

修正LP使用38个offset与每个160状态顶点的低/高推力独立力矩，共358变量、19520不等式。
有界与无界力矩版本均由HiGHS报告不可行（`NUMERIC_CHECK`）。随后用纯`Fraction`重建24行
Farkas电路：秩23，全部乘子严格为正，358个加权左端系数（含320个端点力矩列）精确为零，
右端为`-3069803/88290`。证书未用力矩限幅、offset等式或非负边界，故对冻结候选给出
`COUNTEREXAMPLE`，并说明失败不是执行器限幅导致。

## 限制与下一问题

该证书只否定第48章固定19-pair、参数无关offset的configuration cone；它不否定不同法向、
parameter-dependent offsets、一般PD-RCI、六状态安全或递归可行性。Gate A仍blocked。
下一轮唯一问题是定义严格包含该候选的最小parameter-dependent-offset CC/RCI类，并在编码前
冻结独立可核查的可行证书/否证接口。

## 复现命令

- `python -m unittest verification/test_scheduling_visible_19pair_farkas.py -v`
- `python verification/check_scheduling_visible_19pair_farkas.py --root . --output <new-output>`
- `python -m unittest discover -s tests -v`
- `python -m unittest discover -s verification -p 'test_*.py' -v`
- `git diff --check`

最终验证：项目测试39/39，研究验证357/357；文献索引变更导致的14个历史工件均由各自原
checker重建后通过复现。自审未保留Critical/Important/Minor问题。

