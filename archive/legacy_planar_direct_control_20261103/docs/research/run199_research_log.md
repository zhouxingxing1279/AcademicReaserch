# Run199 研究日志：冻结 affine-offset SOCP 数值求解

日期：2026-10-29。

## 仓库接续与文献准入

从远端Run198=`42be3a2`及等树本地历史接续，核查`main=1c49659`、工作树和短检查点；修正
Run198归档复放错误：历史solver inventory不应随当前环境变化。重读Goulart--Chen
Sections 2.1--2.2、Mulagaleti--Mejari--Bemporad式(26)--(28)、SDP(33)和算法步骤4，复核
Pólik--Terlaky Theorem 2.2/Slater。准入范围只限锁定求解与独立审计，不提出新算法。

## 唯一阻塞与实现

Run198唯一阻塞是没有真正锥求解器。本轮安装并锁定`clarabel==0.11.1`，把冻结模型直接组装
成Clarabel标准形式。模型含6514变量、39870行、225744个非零元、38个zero-cone等式、
21592个nonnegative分量与6080个三维Lorentz cones。顶点映射仍由`Fraction`活跃集逆生成，
测试要求float矩阵逐元素精确复现该有理映射。

## 结果与证据边界

默认equilibration返回`PrimalInfeasible`（20次迭代）；归档39870维对偶ray后独立检查
`b^Tz=-0.9999999666165422`、`||A^Tz||_inf=3.6884557630401105e-09`、最差dual cone
margin=`0.07578612251984826`。关闭equilibration仍返回`PrimalInfeasible`（19次迭代），
独立ray审计也通过`1e-7`阈值。主ray的SHA-256为
`af21a2b1cff5aab6f323c5095ebd3c314928c91fb5db6bd49a6c81ff972929e1`。

结论仅为`NUMERIC_CHECK`：冻结19-pair affine-offset/common-core充分模板数值不可行。浮点ray
不是精确Farkas证书，不能外推为一般PD-RCI、物理系统或六状态闭环不可行；Gate A保持
blocked。

## 验证与下一问题

聚焦9/9测试同时重放归档ray、校验工件hash、重建锥模型并以两种scaling重新求解；项目
39/39、全研究384/384测试通过。更新`READ_PAPERS.md`后，14个受其SHA-256绑定的历史工件
均由各自原checker机械重建，再经全研究回归验证。

下一唯一问题：从高余量浮点ray提取稀疏/可有理化结构，并用精确有理或区间算术认证
`A^Tz=0`、`z in K*`与`b^Tz<0`；在此之前不切换configuration family。

## 提交与同步

内容提交为`8d87a1c`。标准HTTPS push因运行环境无GitHub用户名凭据失败；随后通过已授权
仓库接口创建远端等树提交`68c2004`与分支`research/run199-affine-offset-socp-solve`，fetch
核验两者tree均为`1badee5`。本节与短检查点的同步元数据另作本地元数据提交，并再次执行
远端tree核验。

