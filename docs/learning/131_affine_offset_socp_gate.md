# 131 固定 affine-offset 综合的精确 SOCP 门

## 1. 小LMI并不需要一般SDP接口

Run197的每条区间证书只有一个`2 x 2`对称矩阵
`Q=[[q00,q01],[q01,q11]]`。它PSD当且仅当

`||(2 q01, q00-q11)||_2 <= q00+q11`。

平方后两边之差恰为`4 det(Q)`；Lorentz cone还显式要求右端非负。因此该转换与PSD主子式
条件精确等价，不是近似，也不依赖浮点采样。这个结论只适用于`2 x 2`；一般更高阶PSD不能
据此改写。

## 2. 冻结原始形式的规模

对38 facets、160 vertices，综合包含6080个三维Lorentz cones。若保留未消元变量：

- affine facet offsets：76个系数；
- affine scalar vertex torques：320个系数；
- common-core offsets：38个；
- S-lemma multipliers：6080个；
- 合计6514个标量变量；38个相反facet的系数等式消元后有效6476个。

精确端点线性条件包括12160条configuration inequalities、2560条硬状态约束、640条力矩
约束、76条common-core包含及76条offset非负条件。该计数不对common core强加pair symmetry，
也未删除冗余行，因而是可复现的原始建模规模，不是solver presolve后的规模。

## 3. 求解器能力是证据链的一部分

当前运行环境只有NumPy/SciPy；没有Clarabel、SCS、CVXPY、CVXOPT、ECOS，也没有相应命令行
程序或缓存wheel。`scipy.optimize.linprog`/HiGHS只处理polyhedral LP，Lorentz cone非多面体，
不能用有限线性行精确替代。SLSQP等局部非线性优化即使返回success，也不是凸锥可行性或
不可行性证书。

所以本轮的可靠结论是：**综合可精确表为SOCP，但当前环境不能求解它。** 这不是理论不可行，
更不是四旋翼物理不可行。下一步应锁定一个锥求解器及版本，保存原始solver状态/残差；若得到
候选，还必须用Run196/197的独立全区间检查器逐条验证，solver的`optimal`不能替代证书。
