# Run244 — 重复阻尼脉冲的严格扰动权限反例（2026-11-01）

**基准远端main：** a8009179dc0b9491735f0dc1fd5123f0445824c2。已读取main ref、Run243源码/日志、配置及近期分支。**本轮瓶颈：** Run243的20/25/30拍固定宏周期仅在无扰、无噪、局部不饱和时Schur稳定。本轮检查它是否可能在全部合法量测和扰动下保证安全。

## 1. 严格反例

冻结四状态Euler (p,v,phi,omega)，h=1/50s，J=1/50，固定推力T=981/100N，横向逐拍独立残差r∈[-R,R]，R=47/25+(243/16000)T=3246383/1600000m/s²；|v|≤3m/s，|tau|≤2/25Nm。取合法初始x=(0,0,0,0)，每拍r=+R、测量噪声0、**每5拍位置包均成功**。连续缺包0≤2；控制器可主动忽略中间成功包，选用每20/25/30拍的成功包。这些是选中使用的包间隔，不是实际连续成功包间隔。

考察Run243固定15拍脉冲形状s=(+1×3,-1×6,+1×3,0×3)，随后n=5/10/15拍零力矩。每宏周期幅值u允许任意依赖历史，甚至允许完整状态或预知未来，只要求|u|≤0.08。单位幅值的15拍起始姿态系数a_j≥0，sum a_j=27/25，max a_j=9/50；脉冲末端phi=omega=0。利用|sin z|≤|z|，单个脉冲可抵消的速度变化至多：

\[
hT|u|\sum_{j=0}^{14}|a_j|\le26487/1562500\approx0.01695168\ {\rm m/s}.
\]

因此每个N=15+n拍宏周期的真实速度增量：

\[
v_{k+N}-v_k=hNR-hT\sum_j\sin(u a_j)
\ge hNR-26487/1562500.
\]

| 自由段n | 选用成功包间隔N | 速度增长下界(m/s/周期) | 认证最晚越界拍数 | 末端速度严格下界(m/s) |
|---:|---:|---:|---:|---:|
| 5 | 20 | 0.79464407 | 80 | 3.17857628 |
| 10 | 25 | 0.9975430075 | 100 | 3.99017203 |
| 15 | 30 | 1.200441945 | 90 | 3.601325835 |

全部比较使用Fraction精确分数。若其他状态约束更早违约，则安全更早失败；否则假设直到末端都安全，必与速度约束矛盾。一条合法all-success历史足以否定“对所有合法模式均安全”。**反例覆盖所有同形状、同自由段且满足执行器限幅的脉冲幅值选择，强于仅否定Run243特定PD增益。**

**范围：** 不否定一般输出反馈、非零稳态倾角/持续姿态控制、SMF-MPC或Run234/235全状态RCI。Run243无扰局部Schur证书仍然正确，但不能推广为鲁棒安全。

## 2. 验证工件与证据等级

新增verification/check_four_state_pulse_authority.py（精确证书、真实配置核验、数值sanity），verification/test_four_state_pulse_authority.py（11项测试），results/four_state_pulse_authority_20261101/checks.json及.github/workflows/run244-pulse-authority.yml。隔离Linux Python环境执行11项测试：**10通过、1项因缺完整仓库配置跳过**；py_compile和JSON生成通过。完整仓库CI、归档一致性及main合并需独立核验，不能预先报成功。

数值Euler sanity在恒定u=+0.08、r=+R下，n=5/10/15模式分别在80/100/90拍得v≈3.178578/3.990174/3.601327m/s，均在第76拍首次超过3m/s。数值轨迹不是证明；严格结论来自不等式及Fraction。未执行全仓库历史回归、MPC优化或20ms最坏时延认证。

## 3. 文献与课题判断

**Johannes Köhler; Matthias A. Müller; Frank Allgöwer (2021)**，Robust output feedback model predictive control using online estimation bounds，arXiv:2105.03427，https://arxiv.org/html/2105.03427v1 。本轮实际核对§II-A Assumption 1、§III开头的当前估计误差、未来估计误差、估计器偏差三项条件及§IV Tube MPC接口。其10状态四旋翼算例及在线误差界有借鉴价值，但相关稳定性/递归可行条件不能由本轮脉冲Schur结果推出。历史已读，不重复计数。

**Liren Yang; Necmiye Ozay (2021)**，Safety Control Synthesis for Systems with Missing Measurements，IFAC-PapersOnLine 54(5):97–102，DOI https://doi.org/10.1016/j.ifacol.2021.08.481 。本轮对照已有Run240–242分节笔记，未重新阅读全文。其丢包自动机和因果控制综合可复用，但成功包无噪全状态假设与本项目有噪位置不同。唯一论文日志去重仍91篇。

**可行性：** 排除一条低权限终端路线，其他输出反馈控制仍可研究。**创新性：** 反例重要但不足单独成题。**难度：** 必须设计可持续抵消横向残差的姿态权限并与SMF/CZ、模式自动机闭合。**Gate A=blocked**：一般四状态SMF＋MPC闭环、递归可行性、六状态安全、20ms最坏求解时间均未证明。

## 4. 下一轮唯一优先任务

构造**允许非零稳态倾角、跨5拍量测机会保留姿态**的共享因果备份律，先检查固定推力四状态模型对恒定极端扰动的控制权限，再对每条success/miss边做SMF集合传播和硬约束认证。不要继续把15拍强制复位脉冲当作可重复安全终端策略。


## 5. 完整checkout CI与远端main核验（2026-11-01）

研究PR #58 https://github.com/zhouxingxing1279/AcademicReaserch/pull/58 基于main a8009179dc0b9491735f0dc1fd5123f0445824c2，合并前compare ahead=7/behind=0、mergeable=true。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41320036916 completed/success，Python 3.13.17完整checkout执行Run224–244聚焦测试**178/178通过、无跳过**，真实配置、精确证书与归档JSON（浮点sanity容差1e-10）、artifact上传均通过。PR以非强制squash安全合并，代码main SHA 0be31388bdb49a859c7c882d6c90edd1b625f92f；已重新读取main、源码Blob及归档JSON确认落地。合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41320133837 completed/success，完整checkout **178/178通过、无跳过**（32.558s），归档校验和artifact上传成功。**未执行全仓库历史回归、一般SMF-MPC递归可行或20ms最坏时延认证。** 此补记只增加证据记录，不修改算法。
