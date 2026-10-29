# 132 固定 affine-offset SOCP 的数值不可行证书

日期：2026-10-29。证据等级：`NUMERIC_CHECK`。

## 问题与适用范围

本轮只求解Run197--198冻结的四状态横向—姿态降阶基准：38个固定facets、160个
configuration vertices、当前归一化推力`s in [-1,1]`可见、未来推力可任意跳变，并使用
仿射offset、仿射vertex torque与一个parameter-independent common successor core。它是
Mulagaleti--Mejari--Bemporad参数相关RCI充分模板的受限实例，不是六状态四旋翼结论。

每个facet/vertex的区间二次条件经单约束S-lemma得到一个`2 x 2` PSD条件，再按

`Q >= 0 iff ||(2 q01, q00-q11)||_2 <= q00+q11`

精确改写为三维Lorentz cone。最终标准锥形式有6514个变量、39870行、225744个非零元、
6080个SOC；另含38个zero-cone等式和21592个nonnegative-cone分量。

## 数值结果

锁定`clarabel==0.11.1`后，默认equilibration求解20次迭代返回`PrimalInfeasible`；关闭
equilibration的独立稳健性运行19次迭代仍返回同一状态。主运行保存完整39870维归一化对偶
ray，其独立重放得到：

- `b^T z = -0.9999999666165422`；
- `||A^T z||_inf = 3.6884557630401105e-09`；
- 最差dual-cone margin为`0.07578612251984826`；
- 非负锥与全部6080个SOC均在`1e-7`审计容差内。

关闭equilibration的ray给出`b^T z=-0.999999993388883`、stationarity infinity norm
`1.430303697702584e-08`及最差dual-cone margin `0.08018399542180811`。两条证据来自不同
numerical scaling，但都只构成浮点不可行证书。

## 能推出与不能推出什么

可以推出：在归档矩阵、锥顺序和`1e-7`审计容差下，冻结充分SOCP有一条可重放的强数值
不可行ray；因此不应继续把同一模板当作即将得到RCI的候选。

不能推出：该SOCP精确数学不可行、所有parameter-dependent RCI都不可行、执行器物理权限
不足、六状态模型不安全，或Tube MPC不能递归可行。fixed normals、19-pair configuration、
affine dependence及common core均是额外保守性来源。升级为`COUNTEREXAMPLE`前，必须获得
精确有理或区间认证的conic Farkas证书。

## 可复现入口

- 生成/求解：`python verification/check_affine_offset_socp_solve.py --output ... --dual-output ...`
- 独立回放：`PYTHONPATH=verification python -m unittest verification.test_affine_offset_socp_solve -v`
- 原始工件：`results/affine_offset_socp_solve_20261029/checks.json`与`dual_ray.npy`。

