# Run210：姿态制动必要条件前移与可达反馈基线（2026-10-30）

**基线 main：** 4c3096f4e8fb845400976a5a2811a5517da8acd4（Run209）。唯一问题：能否提前识别 Run208 第96拍五拍内必然越界的风险，并通过更早的因果反馈避免该特定危险历史？

## 1. 精确必要条件与适用边界

冻结离散姿态模型：phi_{k+1}=phi_k+h*omega_k，omega_{k+1}=omega_k+(h/J)*tau_k；h=J=1/50，|tau|<=2/25，|phi|<=9/20。

从当前时刻起，第 n 拍的姿态最小/最大可达值分别为

    phi + n*h*omega ± (h*h/J)*UMAX*n*(n-1)/2.

对于当前控制 u0 已固定、后续控制允许任意合法因果选择，n>=2 时：

    phi_{k+n} = phi_k+n*h*omega_k + (h*h/J)*(n-1)*u0
                + (h*h/J)*sum_{j=1}^{n-2}(n-1-j)*u_{k+j}.

以最强制动/最强反向加速界定后续极值，得到对每个 n=2..H 的当前力矩上下界；取所有 n 交集形成 guard_interval。n=1 的姿态不依赖当前力矩，单独检查。

**逻辑级别：** 这是 H 拍可生存性的必要条件。不同 n 的极端控制序列可能不一致，交集非空不能推出存在一个可持续安全策略。对于不精确的后验盒，坐标端点还可能不可同时达到，导致保守拒绝。它既不是 RCI 集，也不是终端充分条件。

## 2. 实际可达轨迹与负面结果

严格复用 Run206 的 Fraction 动力学、间歇测量、两包速度收紧与 Run208 的两层推力条件化 backup。当前推力可见，后继推力任意端点；每拍先审计再施加力矩。

- **原 Run208 交变高推力轨迹：** 第96拍首次拒绝。H=8 的后继状态制动预警在第93拍首次触发（拟执行动作使下一状态出现到第100拍必然越界的姿态），当前状态预警在第94拍首次触发。此历史的姿态/角速度后验为单点，故不是独立盒端点伪见证。
- **只加必要条件、不改建议反馈：** 第94拍就拒绝，仅执行93拍。说明早期检测本身并不能挽救控制；更严格的必要条件可能提前停止。
- **提前反馈基线：** 在原建议力矩上加 -omega/5（使用后验中点），再投影到 Run208 两层 backup 区间与 H=8 必要制动区间的交集。相同确定性场景，交变高推力执行200/200拍，持续正扰动高推力执行191拍后第192拍仍拒绝，切换推力正扰动执行200/200拍。对照原 Run208 分别为95、113、121拍。每个已执行动作均经过原四拍 backup 审计及本轮必要条件检查；真实状态在重放中保持在 SMF 后验和原硬约束内。
- **负面结果保留：** 正扰动高推力在第192拍再次拒绝；200拍内未拒绝不等于无限时域可行。反馈轨迹不同，结果不能解释为同一状态的严格配对性能提升，也不能推广为所有噪声、扰动和推力历史的安全保证。

## 3. 文献核验及创新边界

Alexandre Didier, Kim P. Wabersich, Melanie N. Zeilinger (2021), *Adaptive Model Predictive Safety Certification for Learning-based Control -- Extended Version*, arXiv:2109.13033, https://arxiv.org/abs/2109.13033 。本轮核对 arXiv HTML 正文 Sections II-A/II-B、III-A，Assumptions 1–2、Definition 1、Algorithm 1、Theorem 1。论文要求模型参数集合真实包含与嵌套、终端 safe set 和 backup 控制策略，才能形成递归安全证书；其 parameter-SMF 与本仓库 state-SMF 不能混同。故 Run210 的制动条件和有限四拍 backup 不能借用其 Theorem 1。已有的 predictive safety filtering 和提前制动思想均非本课题原创。

## 4. 测试、环境、限制

本地 Python 3.13.5，标准库 Fraction。以远端 Run206/Run208 源码逐式核对的最小镜像运行；新增 verification/test_attitude_viability_guard.py **8/8 测试通过**，涵盖全力矩端点、必要区间、可达第93/94拍预警、guard-only 负面结果、提前制动150拍、持续正扰动第192拍拒绝及模型合同。运行：

    PYTHONPATH=verification python -m unittest -v verification.test_attitude_viability_guard
    PYTHONPATH=verification python verification/check_attitude_viability_guard.py --output /tmp/run210_full.json

摘要见 results/attitude_viability_guard_20261030/checks.json；完整重放可按第二条指令再生。**未取得完整仓库 checkout，未执行历史全量回归和 GitHub CI；不能把本地镜像测试写成完整仓库验证。** 失败/拒绝不删除。

## 5. 课题成熟度与唯一下一步

Gate A = **blocked**。四状态已形成可靠 SMF 包含检查、局部四拍鲁棒 backup、物理必要条件早期预警与更有前瞻性的因果反馈实验；仍无终端 RCI、完整 MPC 优化、递归可行性/稳定性或六状态四旋翼安全证明。

可行性：**有限时域闭环仿真可行**，无限时域保证未知；创新性：**中低且待论证**，需在信息状态/保守性/可计算性比较中寻找增量；硕士工作量：若聚焦 SMF＋有限时域安全过滤及失败诊断则适中，若同时要求六状态全局证明则过大。

**下一轮唯一优先任务：** 针对正扰动高推力第192拍的拒绝，构造与姿态制动兼容的有限步控制策略优化（非仅修改反馈增益），检验是否能在相同信息和预算下扩大可达准入域；若不能，应明确保留有限时域安全过滤器为课题边界。
