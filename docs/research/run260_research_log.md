# Run260 — 第45拍两类不利后验的15拍共享开环安全桥（2026-11-02 UTC）

## 研究问题与冻结基准
基准main `f73def4339a94a6f652c3cb32a1d256929022304`；读取`CURRENT_CHECKPOINT.md`、Run255–259日志/验证源码、`configs/planar_baseline.json`及唯一论文记录。Run259已认证固定零读数历史中第45拍SMM、MMS的可靠外包，但未证明后续所有测量分支安全。本轮唯一问题：**在第45拍两个不利可靠外包上，是否存在同一合法控制序列，覆盖未来15拍全部有界扰动与任意合法后续观测？**

冻结四状态离散Euler真值`x=(p,v,phi,omega)`，`h=J=1/50`、实际固定推力`T=981/100 N`、`|r|<=3246383/1600000 m/s²`，`|tau|<=0.08 Nm`；硬盒`|p|<=5,|v|<=3,|phi|<=0.45,|omega|<=2`。第30拍来自Run254`SSSMMS`零读数可靠外包；30–34拍继承Run255非零共享脉冲；35–44拍零力矩，35–45拍每拍姿态与角速零读数，位置35/40/45按SMM或MMS，成功读数为零。该前缀是**特定观测历史**，不是所有历史。

## 新增数学证书
从Run259滚动位置锚点重算`S45^{SMM}`和`S45^{MMS}`，与其`roll(pattern)`的第45拍速度区间逐项精确一致。对两个可靠盒施加**相同**控制`u_k=(T=9.81N,tau=0)`，`k=45,...,59`；使用Run255 `Fraction`、sin Taylor保守包络、1e-10向外舍入的`step`逐拍计算16个外包。所有外包严格位于硬约束内部：

| 第45拍历史 | 第60拍p可靠区间(m) | 第60拍v可靠区间(m/s) | 15拍最小速度裕量(m/s) |
|---|---|---|---|
| SMM | [-0.5323297832,0.5321100428] | [-1.5683557186,1.5679162373] | 1.4316442814 |
| MMS | [-0.2474339699,0.2473900217] | [-1.0935293635,1.0933828698] | 1.9064706365 |

证书直接**忽略第46–60拍全部测量更新**。因为控制不依赖未来读数，任意合法success/miss、任意有界噪声的非空后验都包含在未条件化前向外包内；故这是从上述两个固定可靠盒出发、对所有后续扰动/测量历史成立的**有限15拍共享开环安全前缀**。它不要求未来位置读数为零，也不需要枚举未来测量树。15拍对应0.3s；两个起始模式下最多连续2次miss的合同分别要求下一成功不晚于50或60拍，但本证书甚至不依赖该未来成功是否被利用。

**量词边界**：`forall x45 in S45, exists common tau_45:59=0, forall r_45:59 and admissible measurement branches, x46:60 in X`。这不是`S60 in terminal invariant family`，不是任意第45拍读数或所有先验历史的结论，也不证明闭环MPC优化、无限时域递归可行、稳定性、六状态垂向安全或20ms WCET。对更宽泛信息状态的前驱仍须检查success/miss后验与可移位终端族。

## 真实文献阅读及创新边界
Abraham P. Vinod, Avishai Weiss, Stefano Di Cairano (2025), *Projection-free computation of robust controllable sets with constrained zonotopes*, *Automatica* **175**, 112211, DOI https://doi.org/10.1016/j.automatica.2025.112211；作者正式公开稿 https://www.merl.com/publications/docs/TR2025-023.pdf （19 PDF页）。本轮实际阅读PDF pp.3–5（§1–2.3、Definition 2、式(13)–(14)）、pp.9–11（§4.4–5、复杂度）、pp.12–14（§6数值实验）。论文针对**全状态线性离散系统**`x+=Ax+Bu+Fw`、对称紧凸加性扰动、状态/输入约束、目标集合，使用CZ近似Pontryagin差与有限步robust controllable sets。它不提供间歇有噪位置SMF后验或部分观测信息状态不变核，也不控制四旋翼；其Def.2的状态反馈可控集不能直接替换本项目的同一观测纤维共享控制量词。可借鉴CZ安全前驱的**内近似**（而非把外近似当作安全集合）；表示复杂度随时域增长，需固定预算/降阶。

## 代码、测试与证据等级
新增`verification/check_run260_conditional_shared_bridge.py`、`verification/test_run260_conditional_shared_bridge.py`、`results/run260_conditional_shared_bridge_20261102/checks.json`及专用GitHub Actions workflow。隔离Python Fraction同公式独立重算两分支16个外包及端点，结果一致；真实完整checkout的Run249–260回归、配置交叉核验、源码编译及归档JSON逐字对比以PR CI真实状态为准。该数值证书的有效性依赖仓库冻结离散Euler真值、既定残差界及保守三角函数包络；不能扩展为连续时间物理无人机保证。

## 研究成熟度与唯一下一步
四状态有限时域SMF＋MPC基线不变；本轮仅添加条件性共享安全前缀，不添加新控制算法。**Gate A仍blocked**。下一轮唯一优先问题：在SMM/MMS到达下一强制成功后，检查**更新后的所有非空有噪位置后验是否落入同一可移位信息状态终端族**；如不成立，记录可复核反例并考虑以有限时域安全为硕士课题主保证。
