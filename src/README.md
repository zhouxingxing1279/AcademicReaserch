# 活动源码

当前活动源码只包含可复用的数值集合几何工具。外环 plant、飞控接口适配、SMF/CZ 估计器和 Tube MPC 控制器尚未实现；旧平面直接控制实现已移入历史归档。

活动的 numerical_sets.py 从旧 src/smf_mpc/sets.py 复制，只提供 float64 Box/Zonotope 运算；不是 Constrained Zonotope，没有可靠向外舍入，不提供形式化集合包含证书，不可直接用于确定性安全证明。新模块应按已冻结的 MODEL_CONTRACT 建立。
