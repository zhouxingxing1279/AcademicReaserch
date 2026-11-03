# Run179：`Gamma` 的 information-family 类型纠正

本轮只从Run178短检查点接续，并定向核对第88、90、112章、已有CZ接口、真实`plant.py`和
`filter.py`。仓库已有单个CZ的预测、测量交、支持证书和降阶反例，但没有把连续可见量`d`上的
全部posterior与output-feedback policy作为一张固定复杂度图表示。

全文精读Rego等§2、§3.1、§§4.1--4.5及主要定理。论文严格覆盖给定输入、给定测量下的单CZ
prediction/update，并说明迭代复杂度增长后可作外包order reduction；其比较实验也固定生成元和
约束数。但论文问题式(1)--(3)中的输入是已知值，不承担“同一visible fiber共享输入、不同fiber
允许不同输入”的terminal synthesis量词。

因此Run178的`Gamma`若仅选CZ/SPZ reduction，存在类型错误。当前终端对象是集合值映射
`d -> K_q(d)`或lifted graph `(d,s)`；合并全部`d`会削弱控制权限，连续逐fiber保存又不是固定
复杂度。本轮将候选下推为固定cell、固定normal、cell内仿射fiber policy的lifted polyhedral
graph；非线性source-to-target oracle必须对每条边和每个target normal做全量词支持证明。

本轮不写代码：尚未冻结第一条source cell、target normals和可靠非线性支持计算，单CZ checker
即使通过也不回答terminal-family问题。证据等级为
`information_family_type_obstruction_from_source_and_primary_full_text`，不是可行性、RCI、递归
可行性或创新证明。

论文级主线仍未闭合。下一唯一问题：在mode 0的一条miss边上冻结一个lifted `(d,s)` source
cell、仿射fiber policy和target fixed normals，用真实非线性plant构造可复算的逐normal上界；
若该最小cell不能在输入、状态和source-domain约束内闭合，则停止固定复杂度terminal-family支线。
