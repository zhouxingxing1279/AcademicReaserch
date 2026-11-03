# Run190 研究日志：测量条件化 extreme family

日期：2026-10-27。

## 仓库与文献

远端 `main=1c49659`；最新成果为 Run189 `c24ae0a8`，tree `0a94d51b`，启动时无 Run190 远端分支。基线项目 39/39、研究验证 325/325。

重读 Houska §3.1--3.2、§6.1--6.5、Definition 7、式(56)--(57)与 Theorem 3 证明接口；重读 Villanueva--Müller--Houska §3.4--3.5、Lemma 1、Definition 7 与 Theorem 2。Valero 等 2020 阅读 Introduction、§1.1及其固定复杂度多面体估计表示；Artstein--Rakovic 2011 仅取得作者摘要，未据此引用定理或判断首次性。

准入通过“实际位置测量生成的单-mode extreme family”复现，不通过新算法、有限两个真正 extreme sets、regular `H/Omega` 或控制结论。

## 精确结果

对 `X=[-1,1]x[-11/4,11/4]` 和位置噪声半宽 `a=1/50`，全部非空测量中心为 `[-51/50,51/50]`。中心区间 `[-49/50,49/50]` 生成 maximal rectangles `R(c)=[c-a,c+a]x[-11/4,11/4]`；边界截断 posterior 由端点矩形覆盖。

不同 `R(c)` 等宽，故包含成立当且仅当中心相同；真正 extreme boundary 是连续族。其六 offset 向量关于 `c` 仿射，参数域是一条仅有两个顶点的线段。端点 sets 互不包含，局部门槛通过，但不能把两个参数顶点误报为整个 extreme boundary。

## 实现、验证与边界

TDD RED 为 checker/CLI 缺失导致 6/6 明确失败；GREEN 聚焦 6/6。最终项目 39/39、研究验证 331/331；25份依赖阅读索引的历史工件由各自主checker重放并更新哈希。检查器保存边界 posterior、端点 offsets、configured vertices、连续边界语义和所有否定声明，并以源码哈希绑定。

该 family 保留完整速度半宽，斜 facets 在 maximal rectangles 上冗余，未移除 Run184 的 velocity-radius 环。证据等级为 `exact_measurement_conditioned_extreme_information_family`；未证明 graph invariance、输入/终端约束、递归可行性或六状态保证。

独立整分支复审另以401个测量中心、301个offset中心及全部`G/Lambda`恒等式核查，未发现Critical或Important问题。保留两项非阻塞审计缺口：正文尚未显式写出由紧致center区间抽取收敛子列的Hausdorff闭性论证；artifact中的端点凸包等于物理盒字段尚缺独立回归断言。这两项不改变当前精确几何结论，但后续复用前应补齐。

下一唯一问题：从速度与斜 facets 真正活跃的相关 source polytope 构造全连续 measurement posterior family，检查是否存在有限、固定、非退化 meta configuration；闭合前不进入完整 mode graph。
