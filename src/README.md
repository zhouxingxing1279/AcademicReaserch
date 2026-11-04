# 活动源码

当前活动源码包含通用数值集合工具，以及 [startup_gate.py](outerloop/startup_gate.py)：支持函数与精确有理数顶点枚举构造一步共同输入集合。它是小规模离线研究验证器，超过预算明确拒绝，不是在线SMF或Tube MPC。完整外环闭环、飞控接口、时间戳CZ估计器尚未实现；旧平面直接控制实现已移入历史归档。

活动的 numerical_sets.py 从旧 src/smf_mpc/sets.py 复制，只提供 float64 Box/Zonotope 运算；不是 Constrained Zonotope，没有可靠向外舍入，不提供形式化集合包含证书，不可直接用于确定性安全证明。新模块应按已冻结的 MODEL_CONTRACT 建立。
