# Run183：Houska竖直强基线适配合同

启动只读取Run182短检查点、Houska终端ensemble相关章节、当前15-mode合同与竖直共享原语
检查器。远端续接点为Run182 `1685b980`，远端main为`1c49659`。

本轮重新精读Houska §4.2、§5.5、§6.1--6.7、式(24)--(31)和Theorem 3证明；阅读全文
Villanueva--Müller--Houska 2022的pp.1--9（摘要、Introduction、§2.1--2.3、§3.1--3.4）。
文献准入只允许实现固定包络适配合同：一般configuration-constrained geometry、extreme-set
control和terminal ensemble均已有覆盖。

设计比较了直接代入原`W(T)`、忽略packet mode、以及固定全域包络并保留edge measurement三种
路径。前两者分别违反固定`W`假设和传感信息合同，故选择第三种。按TDD先写4项测试；checker
不存在时4项均按预期失败。最小实现从配置精确导出二维`A/B/C`、全域residual、状态/输入margin、
15 modes/17 edges、miss/success measurement和mode 4/9共享控制义务；4/4 targeted tests通过。

精确结果：连续residual半宽`572143/160000`，离散速度扰动半宽`572143/8000000`；安全tracking
error盒为`(1,11/4)`，修正推力半宽`572143/160000`。这只把式(29)图扩展的问题数据冻结为可执行
合同，没有合成`Y/G/Lambda`、`Z/H/Omega`或invariant terminal ensemble。

下一唯一问题：二维box information template的configuration/vertex maps加15-source/17-edge
式(29)可行性问题，要求mode 4/9共享控制并保存原始/对偶证书。
