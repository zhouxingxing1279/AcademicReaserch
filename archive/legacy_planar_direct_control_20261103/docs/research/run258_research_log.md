**Run258 PR/main CI及安全合并复核（2026-11-02 UTC）：** 研究PR #97 https://github.com/zhouxingxing1279/AcademicReaserch/pull/97 基于main 357ad7de2fb46be8941fc6b00f25ca6864327242，合并前compare ahead=7/behind=0，仅7个预期文件，mergeable_state=clean，expected head 8a84e4a75e64483b9e9f9b51386f2da5da5d4f6c。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41392632341 **completed/success**；读取Python3.13完整job日志确认Run249–258聚焦**87/87通过、无跳过**，源码编译、真实配置交叉核验、精确JSON逐字比较和artifact上传均成功。使用expected-head非强制squash合并至main 2e85c52fe2103e1d15b27b270929d41c6a82654e；重新读取main SHA、PR merged及7个文件Blob核验落地。合并后main push CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41392685927 **completed/success**，读取完整job日志再次**87/87通过、无跳过**、配置交叉核验和JSON逐字比较成功。**全仓库历史回归未执行**；该CI仅核验特定历史延迟位置锚点证书，不是完整CZ递推、终端RCI、无限时域递归可行性或稳定性证明。Gate A仍blocked。本补记仅更新验证状态，不修改算法、证书或论文去重数。

---

# Run258 — 失测后跨10拍位置锚点恢复隐藏速度的严格外包（2026-11-02 UTC）

## 基准与瓶颈

远端main基准：357ad7de2fb46be8941fc6b00f25ca6864327242。已核对CURRENT_CHECKPOINT、唯一论文总账、Run255–257日志与验证源码、planar_baseline配置及模型选型背景结论。Run257证明第35拍成功位置读数的速度投影宽度≤1.04999253m/s；第35拍失测仍为3.11003963m/s独立盒。**本轮唯一问题：第35拍miss后，第40拍合法success能否利用第30拍历史位置恢复速度信息？** 不开发新MPC或六状态控制器。

四状态定义的离散Euler真值：x=(p,v,phi,omega)，h=0.02s，固定T=9.81N，J=0.02kg·m²，|r|≤3246383/1600000m/s²，位置噪声±0.02m，姿态/角速噪声±0.005rad/±0.01rad/s。第30拍Run254 SSSMMS全零读数历史可靠盒；30–34拍沿用Run255合法共享力矩(+0.04,-0.04,-0.04,+0.04,0)Nm，35–39拍零力矩。第35–40拍姿态与角速读数固定零；位置在第35、40拍按success零读数或miss构成SS/SM/MS/MM四种合法分支。

## 数学推导及认证结果

对任意n步Euler真实路径，a_i=-T sin(phi_i)+r_i，有精确运动学消元：

\[
p_{k+n}=p_k+nhv_k+h^2\sum_{i=0}^{n-1}(n-1-i)a_i,\quad
v_{k+n}=v_k+h\sum_{i=0}^{n-1}a_i,
\]
\[
v_{k+n}=\frac{p_{k+n}-p_k}{nh}
+h\sum_{i=0}^{n-1}\frac{i+1}{n}a_i.
\]

保留第30拍p30∈[-0.02,0.02]m历史锚点，使用Run255/257相同Fraction、正弦Taylor可靠包络和1e-10向外网格传播10个加速度区间。第40拍若位置成功读数为任意y40，其位置条带p40∈[y40−0.02,y40+0.02]。对**所有非空成功读数分支**，速度可靠投影宽度上界：

\[
W_{40}^{success}\leq\frac{0.04+0.04}{10h}
+h\sum_{i=0}^{9}\frac{i+1}{10}(a_i^U-a_i^L)
=\frac{107185316574375443426493}{125000000000000000000000}
\approx0.8574825325950035\ \mathrm{m/s}.
\]

这个上界即使第35拍miss也成立，因为第30拍位置锚点未被丢弃。它是可靠外包的宽度上界，**不是精确真实后验直径**；与其他可靠区间相交只会进一步缩小。

| 35/40位置包 | 第40拍认证速度宽度m/s | 解释 |
|---|---:|---|
| SS | 0.857482532595 | 两次成功零读数 |
| SM | 1.4656003655 | 第35拍成功，第40拍失测 |
| MS | 0.857482532595 | 第35拍失测，第40拍成功，延迟锚点恢复 |
| MM | 3.5256474675 | 两次失测，无新位置条带 |

四个零读数分支均非空：p30=v30=phi30=omega30=0、r=0，执行脉冲后phi35=omega35=0，之后零力矩；精确正弦Taylor区间证明p35、p40均落在±0.02m位置测量条带。四个分支外包逐拍满足四状态硬约束。第35/40两次miss在第30拍成功后合法，第45拍将强制success，但本轮尚未验证第45拍。

**边界：** 这是保留历史位置的两点条带投影，不是完整H-rep/CZ生成元滤波器，不是任意观测历史下的最小后验，不是终端不变集合或MPC升级。MM速度宽度仍增长；不能从特定读数树的有限安全推广无限时域递归可行性。

## 论文分节阅读（唯一总账已有条目，不增加去重数）

Joseph K. Scott, Davide M. Raimondo, Giuseppe Roberto Marseglia, Richard D. Braatz (2016), *Constrained zonotopes: A new tool for set-based estimation and fault detection*, *Automatica* 69:126–136，DOI https://doi.org/10.1016/j.automatica.2016.02.036 ，公开PDF https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。2026-11-02实际阅读PDF印刷pp.126–130：§2 Definitions 1–2，§3 Definition 3、Propositions 1–3、Theorem 1，§4开头。论文针对**线性离散系统有界噪声的状态SMF及故障检测**，不是参数估计、四旋翼、MPC或位置丢包控制；Proposition 1式(11)–(13)给出CZ线性映射、Minkowski和广义测量交集精确运算，Proposition 2的非空/成员检查需LP，§4讨论保包含降阶。没有四旋翼物理输入/状态硬约束、无人机实飞或本项目20ms WCET证据。可复用关联信息表示和成功包广义交集，但不能直接替代本轮非线性真值外包与终端安全证明。

## 测试、证据级别及下一步

隔离Linux/Python标准库Fraction等价原型本地9/9单元测试通过，py_compile通过；命令：在verification目录运行 python -m unittest -v test_run258_delayed_anchor，及 python check_run258_delayed_anchor.py --root .. --output /tmp/run258_checks.json 后逐字比较归档。隔离测试使用与Run255/256/257相同的动力学等价函数；**完整checkout真实配置交叉核验、Run249–258聚焦回归和归档逐字比较必须由PR CI独立确认**。工件：verification/check_run258_delayed_anchor.py、verification/test_run258_delayed_anchor.py、results/run258_delayed_anchor_20261102/checks.json、.github/workflows/run258-delayed-anchor.yml。本日志写入时PR/CI/main合并尚待核验。

可行性：一次失测后成功位置仍能恢复可靠速度界，支持关联SMF路线。创新性：该有限投影属于已有集合估计原理的具体实例，不单独声称方法创新。难度：全观测树、固定复杂度、共享因果终端信息状态、20ms预算仍高。**Gate A blocked**；未证明无限时域递归可行性、稳定性或六状态安全。

**下一轮唯一优先问题：** 对SS/SM/MS/MM以及第45拍强制success的合法观测树，构造固定复杂度、可移位的历史锚点H-rep/CZ信息状态更新，核验丢弃旧锚点是否仍可靠包含并能支持共享终端前驱。
