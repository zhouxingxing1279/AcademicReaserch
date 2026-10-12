# Run170 研究日志：从抽象端点回到联合物理可达性

## 仓库审计

起点为本地Run169 `8a9d18d`、远端Run169 `02a2cea`，共同tree `8b5fbdd`；远端
`main=1c49659`。定向检查`planar_baseline.json`、cycle-lifted checker、Run169 checker与原始结果。

发现Run169把“抽象J14外包成员”写成“真实可达状态”。cycle checker仅对线性`A/G`与独立
逐边`rho_x,rho_z`传播；Run169 checker只验证坐标域和当前点的气动值，没有初态、控制/测量/
风历史或`plant.py`逐步重放。因此真实非线性benchmark可达性没有证明。

## 文献与纠错结果

精读Rego等§II--III：非线性reachability的正确义务是从`X0×W`递归包含`f(x,w)`；其factorable
lifted enclosure显式保留同一非线性计算图中的因子关系。它直接否定“外包成员就是plant可达”
这一逆向推理，但也给出下一步可实现基线。

Run169有理数事实仍有效：独立残差外包确实容许该J14组合，且该点气动下界超过目标。改变的是
结论范围：当前外包过宽，不能推出真实物理路线不可能。检查器现显式输出“无非线性轨迹证书”
与“联合物理可达路线仍开放”。

## 证据等级与未实现理由

- 已证明：当前独立残差外包不能满足Run168目标。
- 仓库审计事实：Run169没有真实非线性轨迹证书。
- 未决：联合物理可达外包是否排除极端组合、是否在固定预算下严格更紧。
- 未实现：文献门槛只允许先纠错；尚未冻结factorable plant graph、测量时序与降阶预算，直接写
  控制器会再次混淆外包、可达性和递归可行性。

下一唯一问题：为一个预测步写出`(state, wind, aerodynamic factors, residual)`的共享primitive
factorable CZ合同，并用包含证明及Run169点的可行性查询判断该极端组合是否仍被联合外包容许。
