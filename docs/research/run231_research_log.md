# Run231 — 四状态正体积终端单元的25拍严格排除（2026-10-31）

**基准远端main：** `b6ab233a2188a138f9ef64d76418827a52fb37f4`。**唯一瓶颈：** Run229的中央分叉图仍是有限两拍DAG而非闭合RCI；Run230只排除零速度、零姿态、零角速度的低维切片。本轮检验能否对真实四维体积的候选终端单元作正确全控制量词的严格剪枝，以避免把不安全单元接入终端策略图。

## 严格有限时域证书

冻结Euler模型 `(p,v,phi,omega)`，`h=1/50`，`p+=p+h*v`，`v+=v+h*(-T*sin(phi)+r)`，`phi+=phi+h*omega`，`omega+=omega+h*tau/I`，`I=1/50`，`T in [981/200,2943/200]`，`|tau|<=2/25`，`|r|<=47/25+(243/16000)*T`，`|p|<=5`，`|phi|<=9/20`。对于**任意**因果控制序列，扰动对手每拍在控制后选择 `r=+R(T)`。

对初始盒 `B`，用其 `p_lower,v_lower,phi_upper,omega_upper`，由力矩上界得到 `phi_k <= phi_upper + k*h*omega_upper + h^2*(tau_max/I)*k*(k-1)/2`。在尚未发生约束违约的轨迹上，若该上界处于 `[-0.45,0.45]`，正弦单调性与有理数Taylor上界给出 `sin(phi_k)<=s5_upper(phi_upper_k)`。因此对任意合法推力 `v_(k+1)-v_k >= h*[R0+min_{T=Tmin,Tmax}T*(RT-s5_upper)]`。以盒下界初始化并逐拍积分，可严格下界**每一个初始状态、每一种合法因果控制**在同一合法对抗扰动策略下的位置。若第25拍位置下界严格超过5，则所有盒内状态都在25拍内被迫违反硬约束。

具体正体积四维盒：
- `p0 in [4.9,4.91]` m；
- `v0,phi0,omega0 in [-1/200,1/200]`（各自SI单位）。

Python `Fraction` 精确给出 `p25 >= 5 + 461731712952866342887537/25000000000000000000000000 = 5.018469268518114...` m。严格裕度 `0.0184692685...` m。通过 `(p,v,phi,omega)->(-p,-v,-phi,-omega)` 及扰动/力矩符号镜像，负位置盒 `p0 in [-4.91,-4.9]` 同样严格排除。盒在四维上均有正宽度。这是**有限25拍全控制量词的整个初始盒排除证书**，不是非空RCI构造，更不是整个安全域RCI为空的证明。中央零状态未被本证书排除，也不能因此称其安全。

**对终端图的用途：** 候选终端单元若整体落入上述已排除盒，必须从无限时域RCI候选中删除；部分交叠需进一步细分，不能直接删除整格。Run229中央两拍分叉图没有获得新的闭合循环，本轮没有虚构成功的RCI。

## 文献与适用边界

定向复核Yinan Li、Jun Liu (2018), *Invariance Control Synthesis for Switched Nonlinear Systems: An Interval Analysis Approach*, IEEE TAC 63(7):2206–2211, DOI https://doi.org/10.1109/TAC.2017.2760106，作者原文 https://www.math.uwaterloo.ca/~j49liu/papers/2018/li2018invariance.pdf ，重点§II–III、Proposition 2及Theorem 1。该文说明闭合前驱判据及内近似的鲁棒裕度前提；论文的有限切换模式无外部对抗残差模型，不能直接证明本项目非线性控制依赖扰动下的RCI。本轮属于已读论文复核，**统一去重已读数维持90篇**。

## 实现、测试、缺口

新增 `verification/check_four_state_cell_position_guard.py`、`verification/test_four_state_cell_position_guard.py`、`.github/workflows/run231-cell-position-guard.yml` 及归档结果。复现命令：
```bash
PYTHONPATH=verification python -m unittest -v verification.test_four_state_cell_position_guard
PYTHONPATH=verification python verification/check_four_state_cell_position_guard.py --root . --output /tmp/run231_checks.json
```
本地Python标准库Fraction：7项测试中6通过、1项因无完整checkout配置跳过；`py_compile`和精确JSON生成通过。完整checkout CI结果须待GitHub Actions实际执行后再记录，不预先宣称通过。

**Gate A=blocked。** 二维姿态SMF+MPC限定假设下的闭环不变；四状态非空终端RCI、输出反馈Tube MPC递归可行、稳定性、六状态安全、20ms最坏耗时和全仓库历史回归均未完成。可行性：增加可计算的正体积单元严格剪枝，但中央区域是否有闭合终端核仍未知；创新性：此剪枝本身低；难度：仍高。

**下一轮唯一优先任务：** 在远离已排除边界的中央位置区域，设计含位置—速度—姿态—角速度关联及控制标记的有限候选终端图，并尝试严格认证**至少一个非空闭合循环**；若失败，保留失败证书并审慎缩小硕士课题保证范围。
