**Run249完整checkout与安全合并核验（2026-11-01 UTC）：** 研究PR #70 https://github.com/zhouxingxing1279/AcademicReaserch/pull/70 基于main `c00e7c70557159811bd09862ce9ef2d54354e2e3`，合并前compare ahead=7/behind=0、mergeable_state=clean，预期head=`60748cd92f41205c22c24e09fe85a351ce578397`。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41345024930 为**completed/success**，Python 3.13完整checkout Run224–249聚焦**233/233测试通过、无跳过**（64.267s），真实配置、归档JSON逐字核验与artifact上传成功。通过非强制squash合并至main `ce1ec02602270521963d00f408ccae873913bbd6`，重新读取main SHA、PR merged状态及新增源码/测试/证书Blob确认落地。合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41345183186 **completed/success**，完整checkout再次**233/233通过、无跳过**（84.508s），归档一致与artifact上传成功。该补记仅更新文档，未改变算法或验证证书；仍无无限时域输出反馈递归可行性、六状态安全或20ms最坏耗时认证。

---

# Run249 — 有限截止时域SMF后验驱动MPC与严格安全回退（2026-11-01）

**基准main：** `c00e7c70557159811bd09862ce9ef2d54354e2e3`，包含Run248控制研究与背景任务PR #69；**唯一瓶颈：** Run245固定+0.08力矩脉冲在某合法初始角点第14拍进入不可恢复区域（Run248），因此不再只寻找更早的必要反例，而是实现一个可运行、可验证的**后验驱动闭环**，同时诚实限定为有限截止时域安全。

## 1. 冻结模型、观测权限与算法

使用真实 `configs/planar_baseline.json` 的四状态横向—姿态显式Euler子系统 `x=(p,v,phi,omega)`，`h=J=0.02`，固定 `T=9.81 N`，`|tau|<=0.08 Nm`，每拍独立对抗 `|r|<=3246383/1600000=2.028989375 m/s²`；硬约束 `|p|<=5 m, |v|<=3 m/s, |phi|<=0.45 rad, |omega|<=2 rad/s`。初始盒 `|p|<=0.02, |v|<=0.1, |phi|<=0.005, |omega|<=0.01`。姿态与角速度每拍带有界噪声观测，位置每5拍一次成功机会，最多连续丢失2包，成功位置噪声 `<=0.02m`，速度不可测。**不是六状态垂向耦合模型，也没有推力调度。**

每拍控制器先以SMF后验区间 `S_k` 作为唯一信息状态；枚举3步离散力矩计划 `{-0.04,0,+0.04}^3`，使用中点的8步名义代价排序，且要求三步鲁棒状态可行。更重要的是对**实际将执行的第一拍** `a` 执行强制安全过滤：从整个 `S_k` 出发，验证 `a` 后接**至绝对第55拍全零力矩**的完整区间外包，每一步均满足硬约束；仅允许通过的首拍输入。随后真实plant更新，执行角/角速有噪SMF条带交，位置success时增加位置条带、miss时不增加；下一拍重新求解。算法并不读取隐藏真实速度、未来扰动或未来包状态。

所有集合预测用 `Fraction` 计算，`sin(phi)` 在 `[-0.45,0.45]` 上单调，正弦下/上界分别为 `phi-phi³/6` 与 `phi-phi³/6+phi⁵/120`（负角由奇对称获得），各状态端点每步向外取整至 `10^-10` 网格。区间相关性被保守丢弃，但真值包含保持；不把浮点replay当作数学证明。

## 2. 有限截止时域保证：证明量词与边界

1. **初始化非空：** 精确外包证明，对整个配置初始盒、全部合法逐拍扰动，连续55拍全零力矩满足所有四状态及输入硬约束。55拍零力矩包络最大绝对值：`|p|<=1.3849438439 m`、`|v|<=2.4441121266 m/s`、`|phi|<=0.016 rad`、`|omega|<=0.01 rad/s`。故初始时零动作被准入。
2. **归纳安全：** 若当前后验 `S_k` 真值包含且某个动作 `a` 通过首拍+零尾检验，执行该动作后的预测外包 `P(S_k,a)` 包含所有扰动下的真实下一状态。任何一致的success/miss测量后验 `S_(k+1)` 都是该外包的子集。Euler区间外包及向外取整对集合包含单调，因此 `S_(k+1)` 下从第`k+1`拍起执行全零力矩仍满足**剩余的同一个绝对截止时间**约束；下次至少零动作可选。对所有后验/噪声/包路径迭代，保证0–55拍安全、有限截止时间的可行性。
3. **严格边界：** 这不是固定长度55拍在每次滚动时无限延长的可行性，更不是无限时域RPI、MPC终端集合、渐近稳定性或Run248不可生存角点的无限恢复证书。第55拍之后无安全保证。当前名义MPC成本优化不构成全局最优性证明。所有合法丢包串的数学覆盖来自不使用未来包的归纳，不来自枚举所有串。

## 3. 实验、基线、负面结果

本地隔离 `Linux / Python 3.13.5`，标准库 `fractions`，未连接仓库完整checkout；执行：

```bash
PYTHONPATH=. python -m unittest -v test_four_state_shielded_smf_mpc
python -m py_compile check_four_state_shielded_smf_mpc.py test_four_state_shielded_smf_mpc.py
python check_four_state_shielded_smf_mpc.py --output checks.json
```

11项本地测试：**9通过、2项因缺完整checkout真实配置/归档跳过**；源码编译成功。完整checkout CI负责再次运行并验证 `--root .`、归档JSON完全一致。真实配置及全仓库历史回归尚不能用本地隔离测试代替。

确定性数值重放：3种合法success/miss字串 × 2种初始真实状态 × 2种符号交替扰动 × (MPC/零力矩) = **24条55拍轨迹、1320拍**；全部4维后验真值包含检查5280次、采样硬约束违约0。MPC共执行94次非零力矩，12条MPC轨迹平均位置RMSE `0.0920326m`，对应12条零力矩 `0.0970092m`，**仅是所选有限样本约5.13%的数值改善**，不是统计显著性、全扰动性能或稳定性结论。最坏采样速度幅值约0.478272m/s。一次本地完整验证约24–27秒，MPC单步平均墙钟约31.65ms（Python解释器与主机依赖、非WCET），**未达到20ms工程目标，保留为负面结果**；时间值不写入需逐字复现的归档JSON。

对比Run245：前者是30拍开环倾角脉冲，Run248给出第14拍不可生存角点；本轮55拍共享因果后验闭环在固定截止时间内严格安全，**不能因此宣称长期恢复了可生存性**。

## 4. 文献分节复核（去重95篇不变）

**Quanwei Qiu, Fuwen Yang, Yong Zhu, Eman Mousavinejad (2020)**，*Output feedback model predictive control based on set-membership state estimation*，*IET Control Theory & Applications* 14(4):558–567，DOI https://doi.org/10.1049/iet-cta.2019.0881 ，开放正文 https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/iet-cta.2019.0881 。本轮实际阅读§2、§3.1–3.2（Theorem 1与MPC公式(19)）和§4（终端RPI条件）及§6。论文将有界噪声线性时变系统的椭球SMF与LMI形式的输出反馈MPC连接，在附加终端不变条件下讨论稳定/可行；不是四旋翼位置丢包模型。**本轮的55拍零尾合同没有其§4的无限时域终端条件，不能引用该文为无限保证。** 本文历史已读，不新增去重计数；对照Mayne等(2006)已有输出反馈Tube MPC阅读记录，不重复计数。

## 5. 可行性、创新性、难度与下一轮唯一优先任务

- **可行性：** 四状态`状态→扰动→观测SMF→网格MPC→安全过滤→执行`已接成可运行闭环，严格保证仅至固定第55拍；比继续累积开环负面证书更接近硕士算法实现。
- **创新性：** 有限截止时域SMF＋安全过滤属于已知思想的工程组合，不是新理论；下一步需检验非保守信息状态终端合同与测量条件化的实际收益。
- **难度：** 55拍后备策略不闭合；粗区间丢失关联、在线计算约31.65ms平均超过20ms，六状态模型与推力调度均未认证。Gate A仍blocked。
- **下一轮唯一优先任务：** 将固定绝对第55拍的零尾合同替换为一个**非空、可重复闭合的输出反馈终端信息状态/备份律**；首先以Run249末端关联SMF及Run248负面角点检查候选，若无法证明则明确改用有条件的有限时域安全问题作为硕士范围，不继续将截止时间无限延长。

**工件：** `verification/check_four_state_shielded_smf_mpc.py`、`verification/test_four_state_shielded_smf_mpc.py`、`results/four_state_shielded_smf_mpc_20261101/checks.json`、`.github/workflows/run249-shielded-smf-mpc.yml`。
