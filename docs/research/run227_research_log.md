# Run227 — 双倾角终端候选严格失败证书与切换桥必要条件（2026-10-31）

**基准main：** 4817403c2ac4dae7c1abe348f0096b3e21bcf5ff。本轮唯一瓶颈：提出四状态联合终端候选并检验真正的 forall x exists u forall r 后继闭合，而非继续扩展有限步前驱。

## 模型与候选
沿用Run224–226冻结四状态Euler：x=(p,v,phi,omega)，p+=p+h*v，v+=v+h*(-T*sin(phi)+r)，phi+=phi+h*omega，omega+=omega+h*tau/J；h=1/50，T∈[981/200,2943/200]，|tau|<=2/25，J=1/50；|p|<=5，|v|<=3，|phi|<=9/20，|omega|<=2；每拍独立 |r|<=R(T)=47/25+(243/16000)T。当前控制先于对抗r；姿态过程扰动为零。全状态反馈，不是输出反馈SMF。

构造非空双模式联合候选 C_switch={x∈X: |p+v/2|<=5, |phi|>=3/20, phi*v>=0}，包含(0,±3,±3/20,0)。它同时耦合位置—速度与速度—倾角，但**不声称不变**。

## 严格负面证书
**一步反例：** C_switch包含x=(0,0,3/20,0)。任意合法T,tau下下一倾角仍3/20；合法对手选r=-R(T)，下一速度 <= -385278383943217/7168000000000000 <0（使用s7正弦下界），故phi*v<0，后继不属于C_switch。C_switch严格不是RCI。

**全类切换桥必要条件：** 若a>h*omega_max/2=1/50=0.02 rad，则任何非空C⊂X∩{|phi|>=a}均不可能RCI。理由：|phi+-phi|<=1/25<2a，不能从正倾角带一步跳至负倾角带；若永不进入缺口，符号不变。正倾角下对手逐拍选r=-R(T)，v每拍至少下降hR0=47/1250；从任意v<=3出发160拍内必越过-3；负倾角同理。故**任意非空四状态RCI必须包含至少一个|phi|<=0.02的状态**。这与Run223两侧倾角必须超过±0.1434的必要条件结合，要求显式中间倾角过渡，但不证明该过渡可安全实现。

对a=3/20，严格s7(a)使对抗速度漂移幅度每拍至少385278383943217/7168000000000000≈0.05374977455 m/s，最迟第112拍严格越界，保守越界裕度1278383943217/64000000000000≈0.01997475 m/s。这个上限是反证假定一直处于候选带内时的上限，不是实际闭环安全时长。

**全维轴对齐盒失败：** 对任何非空C=P×V×Phi×Omega⊂X，p+=p+hv在P两端要求max V<=0<=min V，故V={0}。但相同控制下r=±R(T)造成下一速度至少6254383/80000000的间隔，不能都保持V={0}。因此全维笛卡尔积盒不能作为RCI终端集合；不否定相关多面体/CZ或非凸终端集合。

## 文献、验证与评价
新增原文分节阅读：Yinan Li、Jun Liu（2016），Invariance Control Synthesis for Switched Systems: An Interval Analysis Approach，arXiv:1608.08683，https://arxiv.org/pdf/1608.08683 。核对§I–III、§IV Algorithm 2/3和Theorems 1/2、§V Theorem 4/Proposition 8。论文有限切换模式下的区间内外近似与分区控制器为下一轮提供方法，但不直接覆盖本项目连续推力、控制依赖对抗扰动、部分观测。唯一论文日志去重已读88→89（分节阅读，非全文）。本轮证书均为独立推导。

本地Python 3.13.5，标准库Fraction和与远端Run224一致的常数/正弦函数镜像：7项聚焦测试6通过、1项因容器无法clone完整仓库而跳过；语法编译、JSON生成通过。完整checkout的真实配置和Run224–227回归由新增GitHub Actions执行；CI成功前不宣称通过。复现：
    PYTHONPATH=verification python -m unittest -v verification.test_four_state_terminal_bridge
    python -m py_compile verification/check_four_state_terminal_bridge.py verification/test_four_state_terminal_bridge.py
    PYTHONPATH=verification python verification/check_four_state_terminal_bridge.py --output results/terminal_bridge_20261031/checks.json

**Gate A=blocked。** 四状态RCI、完整SMF输出反馈Tube MPC、递归可行性、稳定性、六状态安全和20ms最坏耗时均未建立。可行性：需要带中间倾角桥的相关集合；创新性：这是已知不变性理论下模型特定的严格负面筛选，不作为独立创新；难度：高。

**下一轮唯一优先任务：** 构造包含|phi|<=0.02过渡区、位置—速度—姿态—角速度耦合的有限单元终端策略图，利用区间外包与exists u forall r验证所有单元后继闭合；若失败，保留反例并收敛课题范围。

## Run227 合并与完整仓库CI核验补记（2026-10-31）

PR #22 https://github.com/zhouxingxing1279/AcademicReaserch/pull/22 已经通过非强制Squash安全合并，首个main落地SHA为 `5efed49fd0c477cc591b4d91ee16c5ce138aab01`。完整checkout PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41242517572 与合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41242569200 均为success；Run224–227合计26/26项聚焦测试通过（无跳过），真实配置合同、Python编译和归档JSON逐字比较通过。重新读取远端main确认SHA与新增源码/测试/归档Blob SHA分别为 `2078adf8af6ea0c26d2fa90d1cab69d5522a3384`、`8b3cac1861228f4d792d9306d19bf8e260581cb4`、`0ebc83cc6bb64742b0ca2ef5b942a832eea79c19`。**未执行全仓库历史回归；没有四状态RCI、输出反馈MPC递归可行或20ms最坏时间保证。** 此补记为文档更新，若另行合并不会单独触发聚焦CI。
