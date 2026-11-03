# Run187：连续测量中心的六 facet sensor-ensemble 门槛

远端核查：`main=1c49659`，最新实质分支Run186为`2047ee6`；本地从同树
`7215ef45`建立隔离分支。基线项目39/39、研究验证308/308。

本轮重读Houska §4.1--4.2、§6.2--6.5、式(7)、(25)--(27)与Theorem 3证明，并复核CCTMPC
§3.4--3.5。关键纠正是：Houska sensor ensemble已用存在同一`eta`的集合量词覆盖连续测量
中心；未来中心不需要枚举，非凸`min`也已有式(25)的安全凸外包。因此准入“六facet
measurement row精确复现”，不准入新算法或完整meta-template声明。

TDD先因checker缺失得到5项RED；实现后5/5 GREEN。对configuration内`P(y)`，vertex maps
精确给出`max p=y_0`、`min p=-y_3`，从而存在兼容测量中心当且仅当
`(y_0+y_3)/2<=a`。平移边界见证以`a=1/50`得到唯一中心`eta=1/3`。非法configuration会在
发出结论前被拒绝。artifact replay测试先因归档缺失RED，生成哈希绑定工件后6/6 GREEN。

更新阅读表后，25份既有理论工件的`READ_PAPERS.md`源哈希同步重绑；随后完整项目测试
39/39、研究验证314/314通过。一次未设置`PYTHONPATH=verification`的聚焦命令因模块导入失败，
按仓库规定环境复跑6/6通过；该失败属于调用环境，不作为实现缺陷或数学证据。

独立审查未发现代数反例，但指出已提交测试尚未落实规格中的一般有理offset枚举。修复轮先令
结构化`assumptions`断言RED，再加入不复用checker vertex maps的facet-pair枚举：扫描625个
configuration内形状（其中540个非中心对称）及每个形状的窄/边界/宽三种halfwidth，共1875个
精确案例；同时把`G y<=0`、非空性和位置输出写入artifact。修复后聚焦7/7 GREEN。
最终完整项目测试39/39、研究验证315/315通过。

证据等级仅为`exact_six_facet_sensor_ensemble_measurement_row`；未选择剩余`Z_2/H/Omega`，
也未构造15-mode/17-edge LP、控制、终端或递归可行性证明。下一轮唯一问题是比较direct
facet-offset bounds与center/radius/support bounds两种`Z_2`，只保留能以有限固定
configuration给出exact `H/Omega`和可审计extreme-set预算的方案，再进入图LP。
