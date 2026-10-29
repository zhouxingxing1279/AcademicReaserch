# Run 199：冻结 affine-offset SOCP 数值求解

- 文献：Goulart--Chen 2026（Sections 2.1--2.2）；Mulagaleti--Mejari--Bemporad 2025
  （式(26)--(28)、SDP(33)、算法步骤4）；Pólik--Terlaky 2007（Theorem 2.2/Slater）。
- 求解：锁定`clarabel==0.11.1`；6514变量、39870行、225744非零元、6080个SOC。
- `NUMERIC_CHECK`：默认与关闭equilibration均返回`PrimalInfeasible`；两条对偶ray均通过
  独立`1e-7`审计，主ray SHA-256=`af21a2b1...29e1`。
- 边界：没有精确有理/区间证书，不能否定一般PD-RCI、六状态安全或递归可行性。
- 验证：聚焦9/9、项目39/39、全研究384/384测试通过。
- Gate A：blocked。下一步只提取并认证精确conic infeasibility certificate。

