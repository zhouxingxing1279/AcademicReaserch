**Run254 PR完整checkout CI复核（2026-11-02 UTC）：** PR #85 https://github.com/zhouxingxing1279/AcademicReaserch/pull/85 。首次PR workflow https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41370808916 **failure**：53/53单元测试全部通过，但精确JSON逐字比较在第22行失败，原因是JavaScript写入归档时整数样式键按数值排序，而Python `sort_keys=True`按字符串排序；不是数学证书失败。已将归档键顺序修正，不改变数值或算法。修复后PR workflow https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41370855348 **completed/success**；读取完整Python3.13.17 job日志确认Run249–254 **53/53通过、无跳过**，源码编译、真实配置交叉核验、精确JSON逐字比较及artifact上传均成功。全仓库历史回归未执行；该CI成功不代表递归安全/稳定性证明。main合并与合并后CI仍待独立核验。

---

# Run254 — 强制成功位置测量后的隐藏速度仍不可区分（2026-11-01）

## 基线与唯一瓶颈

起点远端main `fbaacacf0410acf8c76dbdd8736e73f0c00948cf`，包含Run249–253及模型背景PR #84。已核对`docs/research/CURRENT_CHECKPOINT.md`、唯一论文阅读记录、Run249/251/252/253源码和配置。Run253只证明**特定极端双轨迹**在第30拍成功测量后可以区分，尚未证明对所有真实一致状态都能消除速度歧义。本轮只研究这一量词缺口；不并行开发另一控制器。

## 新的精确反例：恢复位置测量并不必然识别隐藏速度

使用Run249冻结四状态离散Euler：`p+=h v; v+=h(-T sin(phi)+r); phi+=h omega; omega+=h/J tau`，`h=J=1/50`、`T=981/100`、`R=3246383/1600000`、`|r|<=R`、`|tau|<=2/25`。两条真实路径同从`(p,v,phi,omega)=(0,0,0,0)`出发，施加相同合法`tau=0`。0–14拍`r=0`；15–19拍路径A取`r=-3R/4`，20–29拍取`r=+R`；路径B取A的逐拍相反残差。位置包时序5/10/15/20/25/30为`SSSMMS`，即20、25两次合法miss，第30拍被强制success。所有成功位置读数均为0；角度/角速每拍均读0，取合法零噪声。

以第15拍为局部0时刻，末端位置扰动加权和为
`sum_{i=0}^{14}(14-i)r_i/R = -(3/4)(14+13+12+11+10)+(9+...+0)=-(3/4)*60+45=0`。
末端速度差由
`v30(A)=h R[-5*(3/4)+10]=R/8=3246383/12800000≈0.253623671875m/s`，
`v30(B)=-R/8`。
因此两条路径在第30拍**同位置、同姿态、同角速、同全部可用测量历史**，却具有
`diam(proj_v S30 | y5=y10=y15=y30=0, word=SSSMMS) >= R/4 = 3246383/6400000≈0.50724734375m/s`。
这个下界仅对所构造的合法信息历史成立，非所有后验的统一下界，也不是完整后验直径的精确解。

用Python `fractions.Fraction` 对每拍真实状态、残差合法性、全部硬约束与传感器一致性做了精确断言。两个路径的最大位置绝对值为`107130639/8000000000≈0.013391329875m`，最大速度绝对值为`3246383/12800000≈0.253623671875m/s`，姿态和角速均为0；均满足`|p|<=5,|v|<=3,|phi|<=0.45,|omega|<=2`。

再用Run249原始`step`（正弦Taylor包络、向外网格舍入）和`strip`（有噪量测交集）沿相同观测历史递推**完整初始盒的可靠区间外包**，第30拍得到`p∈[-0.02,0.02]`、`v∈[-1.346823505,1.346823505]`。故对该历史的真实后验速度直径，当前证据仅给出**严格夹界**
`0.50724734375 <= true diameter <= 2.69364701 m/s`。
后者是区间外包的上界，不能称为真实后验宽度或CZ必然优于区间盒的定量倍数。两条真实路径逐拍落在该外包内。

**与Run253并不矛盾：** Run253的特定双路径在第30拍位置分离>噪声容差，故必然可区分；Run254另造了合法的不同双路径，在第30拍位置重新相遇，故仍不可区分。不能把两条特定轨迹的区分结果提升为全体后验的可观测性定理。

## 文献核验

Quanwei Qiu、Fuwen Yang、Yong Zhu、Eman Mousavinejad (2020), *Output feedback model predictive control based on set-membership state estimation*, *IET Control Theory & Applications* 14(4):558–567, DOI https://doi.org/10.1049/iet-cta.2019.0881，开放正文 https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/iet-cta.2019.0881 。2026-11-01本轮重新阅读§2 Assumptions 1–2、§3.1 Theorem 1、§3.2 minimax与§4终端RPI条件。该文的椭球SMF提供条件性真实状态包含；§4的终端鲁棒正不变性是额外假设/构造，不由有限时域后验交集自动得到。论文是线性时变/多面体不确定模型，未处理本仓库正弦Euler四状态与有界连续失测自动机。既有已读条目，本轮不增加去重数（保持101）。

## 工件、验证与下一步

- `verification/check_forced_success_velocity_alias.py`：构造双路径、精确Fraction逐拍检查、调用Run249原始SMF可靠外包及可选真实配置核验。
- `verification/test_forced_success_velocity_alias.py`：9项聚焦测试。
- `results/forced_success_velocity_alias_20261101/checks.json`：精确有理数可重放证书。
- `.github/workflows/run254-forced-success-alias.yml`：完整checkout运行Run249–254回归、真实配置核验、证书逐字比较与工件上传。

隔离Linux/Python 3.13运行`cd verification && python -m unittest -v test_forced_success_velocity_alias`：7通过，2因隔离目录缺真实仓库配置/归档显式跳过；`python -m py_compile`与JSON生成成功。完整checkout PR/main CI与安全合并结果以实际GitHub记录为准，不预先宣称通过。

**可行性/创新性/难度：** 本轮是信息状态不可区分性的严格必要条件，提示应在终端安全游戏中保留速度纤维和历史关联；尚无非空终端不变集合或递归可行证明。四状态有限安全闭环已实现，六状态物理扩展仍为条件性后续。**Gate A继续blocked。**

**下一轮唯一优先任务：** 在`SSSMMS`强制success后的**全部**有噪SMF后验上，检验一个显式共享因果备份律的后继闭合条件（含位置读数分支），而不是继续只比较两条证人轨迹。
