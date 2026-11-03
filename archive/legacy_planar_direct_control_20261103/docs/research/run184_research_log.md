# Run184：box information-ensemble 图 LP 与不可行证书

从远端Run183 `893046dc`的等价本地树续接。重新精读Houska §6.1--6.7、式(25)--(30)、
Theorem 3及证明，并定向重读CCTMPC §2.1--2.3、§3.1--3.4。文献准入只允许复现既有
configuration/extreme-set machinery；不允许把box模板或图LP称为创新。

首先纠正时序：Houska原式先测量后控制，而当前配置明确current control先于success/miss
后继揭示。因此每个source只配置4个extreme-set controls和一个predicted ensemble，之后才走
edge-specific measurement；mode 4/9没有branch-specific current control。

按TDD先写box/meta maps测试，模块不存在时4项按预期失败。最小实现得到4-facet/4-vertex box、
6-parameter meta-template、16个meta vertices和4个maximal-radius extreme sets。初始测试曾错误
把具体`Zy`等同meta上界`z`，已按手算signed coordinate纠正并记录。

完整LP有498变量、2772不等式。原计划期望恢复exact feasible primal，但HiGHS稳定报告不可行。
逐类删除诊断表明miss-only、success-only均可行，任一return edge与其前置miss cycle组合即
不可行。根因是axis-aligned position measurement不收缩velocity radius。随后先写失败测试，再
实现21行exact Farkas聚合：最短`0->1->2->3->4->0`环上全部变量系数为零，右端为
`-572143/800000<0`。因此数值不可行已升级为模板级数学否证。

整分支独立复审发现初版success外包只缩小position radius却保留center bounds，会漏掉预测盒
边缘的合法小集合。按精确反例先增加失败测试，再改为保持左右position endpoints的耦合约束；
修复后LP规模及21行velocity-radius Farkas聚合不变。复审同时发现artifact claim误写成primal
certificate及SciPy marginal stationarity符号错误，均以RED--GREEN测试修正。

该结果终止纯axis-aligned box terminal baseline，不终止Houska/CZ路线。下一轮只研究最小
position--velocity相关facet模板是否打破速度半径环；仍保持相同信息、扰动、约束和control
权限，避免用放宽合同掩盖不可行。
