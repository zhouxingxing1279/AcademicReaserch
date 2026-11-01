# Run250 — Run249零力矩备份的严格最大安全时域（2026-11-01）

**远端基准main：** `f9348c2b5ff83a3f9713ad8058ea4b0f8eafb4cf`（已包含背景研究PR #72和Run249）。**唯一瓶颈：** Run249已证明55拍有限截止时间SMF＋网格MPC＋零力矩尾备份的鲁棒安全，但尚无可反复移位的输出反馈终端合同。先对现有零备份计算**精确最大鲁棒安全时域**，检验能否直接重新启动55拍保证，避免把有限时域归纳误用成递归可行。

## 1. 模型、精确证书与量词

继承真实 `configs/planar_baseline.json` 的冻结四状态显式Euler子系统：`x=(p,v,phi,omega)`，`h=J=1/50`，固定 `T=981/100`，`|tau|<=2/25`，逐拍独立 `|r|<=3246383/1600000`；硬约束 `|p|<=5,|v|<=3,|phi|<=0.45,|omega|<=2`。配置初始盒 `p∈[-.02,.02],v∈[-.1,.1],phi∈[-.005,.005],omega∈[-.01,.01]`。

对**固定控制 `tau_k=0`**，精确Fraction端点、交错Taylor正弦界及每步向外 `10^-10` 网格舍入，严格外包全部初态与全部合法扰动词。得到：

| 时刻 | 全初态/全扰动速度可靠外包（m/s） | 硬约束 |
|---|---:|---|
| 55 | [-2.4441121266,+2.4441121266] | 通过 |
| 67 | [-2.9713278455,+2.9713278455] | 通过 |
| 68 | [-3.0155175093,+3.0155175093] | 外包不能认证 |

**关键不是单纯外包超界：** 构造一个真实可达的配置角点 `(-0.02,-0.1,+0.005,+0.01)`，取`tau=0`和每拍合法`r=-R`，姿态与角速度精确递推，速度用sin有理数上下界严格包络。第0–67拍均由全盒证书认证安全；第68拍有
`v_68 <= -1206207001/400000000 = -3.0155175025 m/s`，**真实严格越界裕度至少0.0155175025m/s**。因此**固定零力矩策略**对整个初始盒的鲁棒安全最长为**67拍**（1.34s），第68拍（1.36s）有真实反例。

这证明Run249第55拍**不能仅靠重启相同零力矩55拍备份**取得长期保证。它**不**证明第55拍角点对任意其他力矩不可恢复，也**不**证明SMF＋MPC递归可行不可能；没有把区间伪角点误写为真实轨迹。Run249的55拍安全及采样性能数据仍成立，且本轮不修改其控制算法。

## 2. 文献分节阅读与理论接口

新增实际阅读 **Kim P. Wabersich、Melanie N. Zeilinger (2023)**，*Predictive Control Barrier Functions: Enhanced Safety Mechanisms for Learning-Based Control*，*IEEE Transactions on Automatic Control* **68(5):2638–2651**，DOI https://doi.org/10.1109/TAC.2022.3175628 ，公开arXiv预印本 https://arxiv.org/abs/2105.10241 （2021首发、2022更新）。阅读公开正文§1、§2.1、§3.1–3.3、§4中的终端设计，尤其(5f)、(13a,b)、Assumption 1及Theorem 3.4/3.6的条件；未逐式核验IEEE排版终版，登记**分节已读**。

论文的预测安全过滤要求预测末态落在存在安全控制律的终端集合；旧解移位与终端不变性是递归可行的关键。其软约束/预测CBF用于**可行域恢复**，并不自动保证处于原硬约束集合外时仍满足原硬约束；该文名义全状态确定性系统和本仓库有噪间歇SMF的量词不同。**不得用论文定理给Run249零尾补造无限时域保证**。统一去重阅读记录增加1篇，既有Didier等(2021)的参数SMF/备份论文不重复计数。

## 3. 工件与测试

- `verification/check_four_state_zero_backup_horizon.py`：独立Fraction区间外包＋真实角点负扰动反例；完整checkout还逐点与Run249零备份代码比对。
- `verification/test_four_state_zero_backup_horizon.py`：9项，包含Taylor符号、向外舍入、55/67/68边界、真实角点、保证范围、真实配置/归档。
- `results/four_state_zero_backup_horizon_20261101/checks.json`：可逐字复现的有理数证书。
- `.github/workflows/run250-zero-backup-horizon.yml`：Python3.13完整checkout，Run224–250聚焦回归、真实配置与Run249交叉核验、归档对比、工件上传。

本地隔离环境 `Linux / Python 3.13.5`，命令：
```bash
PYTHONPATH=. python -m unittest -v test_four_state_zero_backup_horizon
python -m py_compile check_four_state_zero_backup_horizon.py test_four_state_zero_backup_horizon.py
python check_four_state_zero_backup_horizon.py --output checks.json
```
**9项中7通过、2项因隔离环境无完整checkout而显式跳过**；源码编译及JSON生成成功。不能将其称为完整仓库9/9通过，PR CI及main CI须实际检查结果。未运行全仓库历史回归；未测20ms WCET。

## 4. 可行性、创新性、难度与下一轮唯一任务

**Gate A仍blocked。** 本轮是严格边界/负面结果，不是新控制器。Run249已有可运行四状态有限截止SMF＋MPC闭环，但没有无限时域终端集合。固定零备份的鲁棒时域上限67拍，继续单纯增加55拍截止时间无法解决递归闭合。文献中的PSF/PCBF已成熟，不能把简单安全过滤包装成新理论。

**下一轮唯一优先任务：** 对Run249第55拍**真实可达的关联后验族**，构造一个可执行的**非零共享因果备份**及其终端信息状态后继闭合条件；先在一个明确的非空后验子域上给出严格正向证书，并明确能否覆盖初始盒。若连续尝试失败，及时将硕士课题收敛为**带明确适用域的有限时域SMF安全过滤与保守性改进**，而不是无限延长固定截止时间。

**合并状态：** 本文创建时为待PR/CI验证，后续应根据实际GitHub结果更新，不能预填成功。
