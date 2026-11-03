# Run209：Run208 第96拍拒绝的物理可行性根因（2026-10-30）

基线 main：f712f41f9eac2269c380497c3098b353497eb64d（Run208）。本轮唯一问题：在第96拍允许下一次观测值条件化的任意因果力矩，能否修复 Run208 拒绝？

## 1. 严格负面结果：不是单纯的测量策略保守

冻结四状态 Euler 模型的姿态子系统：

    phi_{k+1}=phi_k+h*omega_k
    omega_{k+1}=omega_k+(h/J)*tau_k

其中 h=J=1/50，|tau|<=2/25 N·m，|phi|<=9/20 rad。姿态子系统不含推力 T 或横向残差 r_x。对任意 n>=1 和任何满足输入界的任意因果策略，精确展开得：

    phi_{k+n}=phi_k+n*h*omega_k+(h*h/J)*sum_{j=0}^{n-2}(n-1-j)*tau_{k+j}
    phi_{k+n}>=phi_k+n*h*omega_k-(h*h/J)*UMAX*n*(n-1)/2.

每个力矩系数非负，最小值由所有有关力矩取 -UMAX 达到；下界对未来任意测量、推力、控制反馈甚至完整状态反馈均成立。它是必要物理可行性条件，不是四拍 backup 模板的特例。

在 Run208 的 alternating_high 合法历史中，前95拍均被两层过滤器准入。第96拍开始时，精确后验和真实状态满足 phi≈0.29924394150001254 rad、omega≈1.944450731249843 rad/s；后验 phi、omega 均为精确单点，真实状态尚未违反硬约束。

所有未来力矩都取最强反向制动时，未来姿态最小值：

| 再过 n tick | min phi（展示近似值，决策使用 Fraction） | 必然超出 +0.45 rad？ |
|---|---:|---|
| 1 | 0.338132956125 | 否 |
| 2 | 0.375421970750 | 否 |
| 3 | 0.411110985375 | 否 |
| 4 | 0.445200000000 | 否 |
| 5 | **0.477689014625** | **是，至少超出 0.027689014625 rad** |

n=5 的严格分数差值见结果 JSON；另外枚举 2^5=32 条输入端点序列，验证闭式最小值等于全负力矩序列。由于目标值对连续力矩序列是仿射函数，端点极小值覆盖整个连续输入盒。从这个特定实际可达状态出发，任何满足力矩界的控制策略都不能保持未来五拍内全部姿态硬约束，即使未来观测完全准确也不行。

这是一个具体实际可达状态的严格有限时间 nonviability 见证，不是所有四旋翼状态或所有 SMF–MPC 方案的不可行性证明。Run208 上一拍仅保证四拍有限备份，第五拍必然违约与该保证相容。

## 2. 观测条件化为何无法修复此拒绝

第96拍的 phi、omega 后验是单点；第97拍没有位置测量，且姿态预测在给定当前力矩后仍是单点。对所有与模型/噪声一致的下一姿态测量，集合交不会收紧物理状态盒。故第97拍基于下一测量值选择 u1 不会增加可用物理状态信息。即使假设未来可获得完整无噪状态，上一节的制动下界仍然证明五拍姿态必然越界。

不再把更复杂的观测条件化 u1 当作第96拍的修复方案；应在更早时刻加入物理可行域/制动距离预警。

## 3. 文献与创新边界

1. Ian M. Mitchell、Jacob Budzis、Andriy Bolyachevets（2019），Invariant, Viability and Discriminating Kernel Under-Approximation via Zonotope Scaling，https://arxiv.org/abs/1901.01006 。本轮阅读 arXiv 正文 Sections 3.2、5.3、6（Proposition 6.2、Section 6.1 六维四旋翼）及 8。文中用 zonotope 缩放与凸规划构造有限时域 viability/discriminating kernel 的内近似；其六维四旋翼算例采用线性化和有界误差包络，未覆盖本仓库间歇测量信息状态。它是强竞争基线；viability kernel 和制动距离不是本项目原创。
2. Jean-Pierre Aubin（1990），A Survey of Viability Theory，SIAM J. Control Optim. 28(4):749–788，https://doi.org/10.1137/0328044 。仅核对出版社摘要和书目，不标为全文精读。

统一阅读记录新增 Mitchell 等一篇，85→86篇去重；Aubin 作为待进一步阅读的参考文献，不计入已读总数。

## 4. 复现与证据级别

新增 verification/check_attitude_viability_obstruction.py、verification/test_attitude_viability_obstruction.py、结果摘要 JSON 和本日志。运行：

    PYTHONPATH=verification python -m unittest -v verification.test_attitude_viability_obstruction
    PYTHONPATH=verification python verification/check_attitude_viability_obstruction.py --output /tmp/run209_full.json

本地 Python 3 标准库 Fraction、与远端 Run206/208 关键函数逐式核对的最小镜像上 9/9 测试通过；Run208 第95拍区间独立重放为 [-0.08,-0.05554926875015705...]，第96拍拒绝与仓库结果一致。检查涵盖精确动力学闭式、32端点枚举、单点后验、下一测量无增益、Run208拒绝及输出一致性。尚未取得完整仓库 checkout；未运行完整历史回归测试或 GitHub CI。

## 5. 课题收敛与下一轮唯一任务

Gate A = blocked。即使局部四拍安全过滤器每次成功准入，也可能把系统带入五拍内无法避免违约的物理状态；仅改进 SMF 表示或后继测量反馈不能修复控制权不足。

下一轮唯一优先任务：把姿态双积分器的精确有限时域 viability 必要条件加入提前准入/预警，在 Run208 同一可达场景下比较首个预警与控制拒绝时刻，并尝试设计不进入非生存域的因果反馈基线。必要条件不得冒充终端 RCI 或递归可行性充分证明。

硕士课题保底定位仍为 SMF 辅助的有限时域鲁棒安全过滤与失败诊断；六维四旋翼及无限时域安全须另行验证。
