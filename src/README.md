# 活动源码

当前活动源码包含通用数值集合工具、[精确一步共同输入门](outerloop/startup_gate.py)、[有限记忆时间戳CZ](outerloop/finite_memory.py)与[Tube MPC数学原型](outerloop/tube_mpc.py)。新增模块只覆盖声明的ZOH双积分合同；具体飞控接口、一般外环模型和12状态物理覆盖未完成。旧平面直接控制实现位于历史归档。

新增原型依赖根目录requirements-research.txt中的NumPy、SciPy和OSQP。LP/QP为float64；精确Fraction证书独立于求解器，不代表全部软件被形式化认证。详见[课题方案](../docs/research/proposal/RESEARCH_PROPOSAL.md)。

活动的 numerical_sets.py 从旧 src/smf_mpc/sets.py 复制，只提供 float64 Box/Zonotope 运算；不是 Constrained Zonotope，没有可靠向外舍入，不提供形式化集合包含证书，不可直接用于确定性安全证明。新模块应按已冻结的 MODEL_CONTRACT 建立。
