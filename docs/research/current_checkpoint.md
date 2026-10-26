# 研究短检查点（2026-10-26，Run185）

主线：传统SMF/鲁棒输出反馈MPC；学习暂停。远端`main=1c49659`；Run184远端`5f2e1415`。

Run185检查固定`q=p-(1/10)v`的`(p,q)` parallelogram shape gate。独立复审纠正坐标变换：半径矩阵应为`[[6/5,1/5],[1/5,4/5]]`，不是初版的`[[4/5,1/5],[1/5,4/5]]`；错误候选第一miss欠包`1/125`。正确矩阵15步`q->q`增益`187604137722/30517578125>1`，success只重置`r_p`而保留`r_q`，故不存在非负周期return radius。证据等级：`exact_fixed_slant_parallelogram_shape_obstruction`。只否定该固定parallelogram外包，不否定保留active velocity facets的六边形/CZ，也未认证center、input或MPC递归可行。

下一唯一问题：保留`+/-p,+/-v`并加入`+/-(p-(1/10)v)`，构造完整六facet configuration/vertex及measurement outer map；检查active velocity facets能否阻断`q`半径放大，再求exact primal或Farkas证书。
