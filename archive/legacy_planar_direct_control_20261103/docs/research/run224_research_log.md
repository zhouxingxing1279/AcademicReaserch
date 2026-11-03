# Run224 — 四状态一步鲁棒前驱：严格边界见证与排除（2026-10-31）

**基准main：** 372fdc669e58ec8a3987e544f401e077813f6eed。**唯一问题：** Run223证明非空四状态鲁棒不变集需要双侧足够大的姿态投影，但尚无前驱集合或充分见证。本轮只计算完整四状态安全盒 X 的第一轮鲁棒前驱 Pre(X) 的两个包含见证和两个严格排除点。

## 冻结模型与量词

状态 x=(p,v,phi,omega)，h=1/50，惯量 I=1/50；推力 T∈[981/200,2943/200]，力矩 tau∈[-2/25,2/25]；安全盒 |p|≤5，|v|≤3，|phi|≤9/20，|omega|≤2。更新式为 p+=p+hv，v+=v+h(-T sin(phi)+r)，phi+=phi+h omega，omega+=omega+h tau/I。Run208/210残差合同为 |r|≤R(T)=47/25+(243/16000)T，允许每拍独立选择。

**正确因果量词：** Pre(X)={x∈X: 存在当前状态决定的合法(T,tau)，使对所有 r∈[-R(T),R(T)]，下一状态F(x,u,r)∈X}。控制先选，扰动后选；这是完整状态反馈，不是输出反馈SMF可行性。

对0≤a≤0.45，交错Taylor给出 s7=a-a³/6+a⁵/120-a⁷/5040≤sin(a)≤s5=a-a³/6+a⁵/120；负角使用奇对称。代码以Fraction精确构造下一步状态外包，全部坐标位于X内构成严格充分证书。

**严格正见证：** x+=(0,3,3/20,0)及x-=(0,-3,-3/20,0)，各取T=2943/200、tau=0。对所有合法残差，位置下一拍±3/50，角度保持±3/20，角速度0，速度严格在[-3,3]内。结果JSON保留有理数界，故Pre(X)非空。

**严格负见证：** 在x=(0,3,717/5000,0)，任意T下，取对抗r=+R(T)，由s5(717/5000)<243/16000+(47/25)/(2943/200)可知v+>3；负速度/负角度对称。因此这两个边界点不属于Pre(X)。

**不能推广：** Pre(X)非空不意味着无限时域不变核非空；也没有证明这两个见证下一步仍在Pre(X)。角速度切换、位置长时安全、输出反馈信息纤维、终端Lyapunov下降和六状态安全仍未知。

## 测试与可复现性

Python标准库Fraction；本地命令：
- PYTHONPATH=verification python -m unittest -v verification.test_four_state_one_step_predecessor
- python -m py_compile verification/check_four_state_one_step_predecessor.py verification/test_four_state_one_step_predecessor.py
- python verification/check_four_state_one_step_predecessor.py --output results/one_step_predecessor_20261031/checks.json

本地6项测试5通过，1项因缺完整仓库checkout跳过；语法编译通过。91个正负角度浮点sin交叉检查仅为sanity check，严格性来自Taylor余项与有理数不等式。新增GitHub Actions工作流在完整checkout中检查真实配置、6项测试和结果JSON逐字相等；未见成功运行前不宣称CI成功。没有全仓库回归、20ms最坏执行时间或多拍闭环实验。

## 文献、课题评价及下一轮

Kolmanovsky与Gilbert（1998），Theory and computation of disturbance invariant sets for discrete-time linear systems，Mathematical Problems in Engineering 4(4):317–367，DOI https://doi.org/10.1155/S1024123X98000866 。本轮核对出版商摘要与书目；其Pontryagin差、最大不变集算法是概念参考，未阅读全文及定理编号，不能直接迁移到非线性模型。唯一论文日志已读去重87篇不变。

可行性：第一轮前驱有非空证据，但无终端核；创新性：前驱运算是成熟控制理论，当前只是可复现基线；难度：高，须处理多轮集合和部分观测。Gate A仍blocked。

**下一轮唯一优先任务：** 计算第二轮正确量词前驱 Pre(Pre(X))，检验双侧边界见证是否能持续，提供严格内外逼近或有限步排除，而不将单步可行误称为递归可行。

## 合并后证据补记（2026-10-31）

PR #16 https://github.com/zhouxingxing1279/AcademicReaserch/pull/16 已通过非强制Squash合并；main首次落地SHA 1defcf77b9776c40e7febb835b2fe6db2d9a7fdb，重新读取远端main及核心Git Blob SHA确认落地。完整checkout聚焦CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41227640954 为success；verify job的配置合同、6项测试、语法编译和归档JSON逐字比对均成功。没有执行完整仓库历史回归、20ms最坏耗时审计或四状态多拍闭环；Gate A仍blocked。
