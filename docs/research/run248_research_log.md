**Run248 PR/main完整checkout核验（2026-11-01）：** PR #67 https://github.com/zhouxingxing1279/AcademicReaserch/pull/67 基于main 72724f81ef10046eeb41f0ed6398695ab6533e05，合并前compare ahead=7/behind=0，mergeable_state=clean，head=3b371d37a8c1bf44c31a2742041fae378232466a。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41340127964 **completed/success**；Python 3.13.17完整checkout Run224–248聚焦**222/222通过、无跳过**（82.072s），真实配置、Fraction证书与归档JSON一致、artifact上传成功。PR非强制squash合并到main 671c7a5a878524fc522d17c4ccd8de3daa601016，重新读取main SHA、PR merged和源码/归档Blob确认落地。合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41340319892 **completed/success**，Python 3.13.17完整checkout再次**222/222通过、无跳过**（82.089s），归档证书一致与artifact上传成功。此证据补记仅更新文档，未改变算法；全仓库历史回归、SMF＋MPC递归可行性、六状态安全与20ms最坏求解时延仍未认证。

---

# Run248 — 合法初始角点在第14拍已不可生存（2026-11-01）

**基准远端main：** 72724f81ef10046eeb41f0ed6398695ab6533e05（包含背景任务PR #66）。主方向为四旋翼MPC＋状态SMF/CZ鲁棒输出反馈闭环；本轮不重复模型选型任务的Sasfi 2023综述。

## 1. 关键问题与严格数学结果

Run247在Run245一个合法角点发现第26拍的必要guard拒绝，但Run245前30拍开环控制必须覆盖整个初始盒。改用另一真实合法角点：

\[
(p_0,v_0,\phi_0,\omega_0)=(-1/50,-1/10,+1/200,+1/100)
\]

持续选择合法横向扰动 r=-R=-3246383/1600000 m/s²，并保持Run245前缀力矩：第0–11拍+0.08、第12–23拍-0.08、第24–29拍0。精确Euler姿态递推和Fraction正弦Taylor外包证明前0–30拍该真实角点满足全部冻结四状态硬约束。**但第14拍已经不可生存：**

- 第14拍精确姿态 phi=751/5000=0.1502rad、omega=81/100=0.81rad/s，速度真实上界约-0.799504639366m/s。
- 对未来任意合法力矩（甚至全状态、知道未来的非因果控制），Euler时序给出第14+j拍最小可能角度：
  \[
  \phi_{14+j}\ge\phi_{14}+jh\omega_{14}-h(h/J)Uj(j-1)/2,\quad j=0,\ldots,29.
  \]
  该极小角序列严格在[-0.0296,0.2404]rad内。对于所有保持角度硬界的真实轨迹，sin在[-0.45,0.45]单调，用sin的有理数Taylor下包络可逐拍得到最大可能速度上界。
- 即使采用最有利角度下界，持续合法r=-R也有：
  \[
  v_{44}\le-\frac{1876270661513130313664589}{625000000000000000000000}
  \approx -3.002033058421\ \mathrm{m/s}<-3.
  \]
  严格越界裕度约0.002033058421m/s（精确分数见归档）。

**结论：** Run245固定前14拍控制在合法初始盒中已经产生一个真实可达、未来即使全状态控制也无法再保持30拍安全的状态。第15拍或第25拍成功位置包无法在第14拍之后挽救此角点。比Run247的第26拍角点反例更早，且不依赖SMF外包误差。

**量词与限制：** 只反证Run245特定前缀、指定合法角点与冻结四状态模型；不反证其他提前反馈策略、不证明整个初始盒都不可生存、不证明第14拍是实际最早不可恢复时刻。有限扫描k=0..30、N<=30的本必要guard首次拒绝为(k,N)=(14,30)；更早未拒绝不等于可生存。若某未来控制先违反角度或其他硬界，则同样不安全。

## 2. 文献复核

重读Liren Yang与Necmiye Ozay (2021), *Safety Control Synthesis for Systems with Missing Measurements*, IFAC-PapersOnLine 54(5):97–102, DOI https://doi.org/10.1016/j.ifacol.2021.08.481 ，作者PDF https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。实际核对§3 Assumption 1/Problem 1、§4.1–4.4的string automaton、因果控制承诺、Proposition 4–5。论文成功包提供无噪完整状态，不直接覆盖本仓库有噪位置SMF；但其因果约束强调控制不能预知下一次成功包。该论文历史已读，本轮是**分节重读，去重篇数不增加**。Kaynama等(2015) DOI https://doi.org/10.1109/TAC.2015.2411872仅对照历史分节记录，不冒充本轮重新全文阅读。

## 3. 工件、测试与证据级别

- verification/check_four_state_corner_viability.py：复用Run247有理数正弦外包与必要guard，独立重算另一真实角点及未来任意力矩的速度上界。
- verification/test_four_state_corner_viability.py：11项回归（配置、Euler因果延迟、真实前缀安全、角度极值、直接求和与必要guard一致性、证据范围、归档）。
- results/four_state_corner_viability_20261101/checks.json：精确Fraction证书。
- .github/workflows/run248-corner-viability.yml：完整checkout聚焦Run224–248回归、真实配置与归档逐字核对。
- 本地隔离Python 3标准库执行：PYTHONPATH=/mnt/data/run248 python -m unittest -v test_four_state_corner_viability；**9通过、2因隔离环境缺完整仓库配置/归档跳过**。隔离Run247依赖为同公式最小镜像；完整仓库PR/main CI需要单独核验。已执行独立Fraction四个姿态/角速角点的辅助扫描，其他角点分别于第25、25、26拍被有限guard拒绝；这不是连续初始盒或所有观测的枚举。
- **严格数学证明：** 指定真实角点、合法持续负扰动及任意未来力矩下的速度必越界。**未完成：** 状态SMF后验、MPC优化、共享因果控制器、无限时域递归可行性、六状态安全和20ms最坏求解时延。Gate A仍blocked。

## 4. 研究判断及唯一下一任务

可行性：应把控制干预点从第25拍前进一步提前到**第14拍前**；创新性：必要viability反例属于安全核已有思想，不是独立硕士创新；难度：必须用真实量测历史覆盖双向扰动及初始不确定性。

**下一轮唯一优先任务：** 在第10拍success/miss测量机会之前或当时，结合Run240关联SMF与5拍测量/最多两次丢包自动机，检验是否存在覆盖双向初始角点与扰动的共享因果安全前缀；不能再只在第25拍修补Run245。
