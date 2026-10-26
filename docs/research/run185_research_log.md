# Run185：固定单斜向 parallelogram 形状门槛与复审纠错

从远端 Run184 `5f2e1415` 的等价本地树续接。重新精读 CCTMPC §3.4--4.2，并针对 Run184 重读 Houska §6.3--6.7；Scott 2016 与 Robbins 2026 只作 CZ 强基线和摘要级排重。准入允许精确检查最小相关形状，不允许把加法向或线性集合运算称为创新。

本轮先选择固定 `q=p-(1/10)v` 的 `(p,q)` parallelogram 外包作为进入完整六 facet LP 前的廉价 gate。初版实现错误地把 transformed `p` 行首系数从 `1+h/kappa=6/5` 写成 `1-h/kappa=4/5`，并由同一错误矩阵生成测试期望，造成伪周期证书。整分支独立复审用第一 miss 顶点反例识别该问题。

按唯一修复轮新增独立 signed transform 回归，再从坐标恒等式纠正半径矩阵为 `[[6/5,1/5],[1/5,4/5]]`。其15步 `q->q` 增益为 `187604137722/30517578125>1`；由于 success 只重置 `r_p` 而保留 `r_q`，任意非负 return radius 都有 `r_q^15>R`。10步边也失败，只有5步系数小于1。初版候选第一 miss 欠包 `1/125`，第5步即不能回返且派生速度半径超过 `11/4`。

可靠结论改为 `exact_fixed_slant_parallelogram_shape_obstruction`。它不否定保留 active velocity facets 的六边形、旋转模板、CZ或一般 information ensemble。下一唯一问题是构造完整六 facet configuration/vertex/measurement outer map，检查 velocity facets 能否打破该放大；不再用舍弃原速度 facets 的 parallelogram 代替“box加一对法向”。
