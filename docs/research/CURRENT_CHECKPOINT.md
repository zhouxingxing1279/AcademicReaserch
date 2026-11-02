**Run254研究增量（2026-11-01；PR/main CI与合并状态待独立核验）：** 起点远端main `fbaacacf0410acf8c76dbdd8736e73f0c00948cf`。在Run249四状态Euler、真实残差界和`SSSMMS`合法测量时序下，精确构造两条同初态、同零力矩、所有成功位置读数及每拍角度/角速读数均为0的真实安全轨迹；第30拍强制成功位置观测后仍同位置0，但隐藏速度为`±3246383/12800000m/s`，因此该特定合法后验速度直径必要下界`3246383/6400000≈0.50724734375m/s`。Run249区间SMF对同一历史给出可靠外包`v30∈[-1.346823505,1.346823505]`，故真实后验直径仅被夹在`[0.50724734375,2.69364701]`m/s，不能把区间宽度称为精确后验。精确Fraction逐拍检查与独立本地9项测试7通过、2因隔离目录缺完整配置/归档跳过；源码`verification/check_forced_success_velocity_alias.py`、测试、JSON、日志和CI工作流见`docs/research/run254_research_log.md`。本轮重读Qiu等(2020) §2–4，去重文献数保持101。Run253极端双路径可区分与Run254另构双路径不可区分并不矛盾。无终端RCI、无限时域递归可行或稳定性证书，Gate A仍blocked。**唯一下一步：** 对第30拍所有有噪成功观测分支构造完整信息后继及共享因果备份闭合条件。

---

**Run253完整checkout、PR/main CI及安全合并复核（2026-11-02 UTC）：** 研究PR #82 https://github.com/zhouxingxing1279/AcademicReaserch/pull/82 ，基准main `265a70c0bc9247d478b114e37c050aae808c794e`，合并前compare ahead=7/behind=0，7个预期文件，PR head `e6f5167128ad42bd2c6e31c8cc7a4b10baf0977a`，mergeable_state=clean。PR Actions https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41365844668 **completed/success**，读取完整checkout Python3.13.17 job日志确认Run249–253聚焦 **44/44通过、无跳过**，Run251/252和真实配置交叉核验、`py_compile`、精确JSON逐字比对及artifact上传成功。expected-head非强制squash合并至main `4a25e389f1ab4d7d2730dc308407b22bff21f6e3`，重新读取main SHA、PR merged和新增源码/证书/日志Blob核验落地。合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41365922605 **completed/success**，完整checkout再次**44/44通过、无跳过**，证书一致且artifact上传成功。此补记仅更新验证证据，不改变算法/数学证书；全仓库历史回归、整个SMF后验终端闭合、无限递归可行、六状态安全和20ms WCET仍未认证。Gate A仍blocked。

---

# 当前研究检查点 — Run253（2026-11-01；PR/CI/main合并状态待独立核验）

**基准远端main：** `265a70c0bc9247d478b114e37c050aae808c794e`（含Run252与模型背景PR #81）。**本轮严格正向有限证书：** 在Run251固定0–15拍零力矩共同观测历史和Run252的15–25拍双极端扰动轨迹上，所有15–29拍共享合法力矩与25–29拍任意合法独立残差均满足15–30拍硬约束；可执行非零共享桥接力矩`(+0.04,-0.04,-0.04,+0.04,0)Nm`。第30拍强制success位置测量之前，两路径位置差下界`236985959/800000000=0.29623244875m`，大于双测量噪声总宽`0.04m`，故这两条特定路径不可能继续具有相同成功位置读数。证明采用精确Fraction及`|sin(phi)|<=|phi|`安全外包。工件：`verification/check_forced_reobservation_bridge.py`、9项测试、`results/forced_reobservation_bridge_20261101/checks.json`、`docs/research/run253_research_log.md`、CI工作流。

**严格局限：** 双轨迹有限桥接并非覆盖所有SMF一致状态的安全控制律；第30拍两轨迹可区分不代表隐藏速度精确可测；未获得可移位终端信息集合、不变备份、无限时域递归可行、鲁棒稳定、六状态安全或20ms WCET。**Gate A仍blocked。**

**文献与测试：** Yang/Ozay (ADHS 2021, DOI 10.1016/j.ifacol.2021.08.481) §3–4分节重读，去重论文数保持100。隔离Linux/Python标准库本地9项中8通过、1项因缺完整仓库显式跳过，`py_compile`与Fraction JSON生成通过。PR完整checkout/Actions和main合并须等待真实核验。

**下一轮唯一优先任务：** 在第30拍强制success的互斥观测分支上，对**全部**SMF一致状态构造后验及可移位后继，尝试证明非空输出反馈终端信息集合闭合；不能将本轮有限双轨迹证书外推为一般递归安全。

---

**Run252完整checkout/CI与main合并复核（2026-11-01 UTC）：** 研究PR #79 https://github.com/zhouxingxing1279/AcademicReaserch/pull/79 ，起点main `2b7daf58ca5761e261fa12a2d9fff5a19661db44`，合并前compare ahead=11/behind=0、仅7个预期文件，PR head `689e5f0b6c9c9144ed5125e96385300c157e43c1`。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41361021188 **completed/success**；读取完整checkout Python3.13 job日志确认Run249–252聚焦 **35/35通过、无跳过**，Run249配置交叉项通过、py_compile、Fraction JSON逐字比对及artifact上传均成功。使用expected head非强制squash合并至main `46d7b3e1a171c385b3b5201dda27ee92e74fb53b`，重新读取main SHA及源码、证书、唯一论文阅读日志和检查点Blob确认落地。合并后main push CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41361070222 **completed/success**，job日志再次确认 **35/35通过、无跳过**，证书逐字比对及上传成功。本段仅补记验证证据，不修改算法/数学证书。全仓库历史回归、无限时域递归可行、六状态保证与20ms WCET仍未认证。Gate A仍blocked。

---

# 当前研究检查点 — Run252（2026-11-01；PR/CI及main合并状态待核验）

**起点远端main：** `2b7daf58ca5761e261fa12a2d9fff5a19661db44`。Run249的55拍SMF＋网格MPC＋零尾有限时域安全、Run250的零力矩67拍严格上限和Run251的15拍真实不可区分速度纤维仍有效，**Gate A仍blocked**。

**本轮新必要条件：** 对Run251的特定0–15拍零力矩前缀及三个成功位置包（5/10/15拍），随后20/25拍两次合法miss，任何共享因果合法力矩**后续序列**下，存在两个继续合法、逐拍满足全部硬约束、所有可用读数相同的真实扰动实现，其第20拍和25拍速度直径分别为 `0.9333351125` 和 `1.3391329875 m/s`。严格Fraction证书与所有后续力矩的安全外包见 `verification/check_dropout_velocity_fiber.py`、`results/dropout_velocity_fiber_20261101/checks.json` 和 `docs/research/run252_research_log.md`。这**不是**任意0–15拍控制历史的通用下界，也不是递归安全不可行性证明。

**文献：** 分节阅读Cosner等（IROS 2021, DOI 10.1109/IROS51168.2021.9636584）的测量鲁棒CBF/备份集Theorems 2–3与Segway实验；该文假设已知不变备份集，不能直接证明本仓库终端闭合。唯一论文阅读记录由99篇增至100篇去重条目。

**本地测试：** Run252独立8项中7通过、1项因隔离环境缺Run249模块显式跳过；标准库编译与有理数JSON生成成功。PR完整checkout、Actions和main合并**尚未核验，不能提前宣称通过或合并**。无限时域递归可行性、稳定性、六状态鲁棒安全和20ms最坏执行时间均未证明。

**下一轮唯一优先任务：** 从Run252第25拍 `SSSMM` 真实双速度纤维出发，构造覆盖第30拍下一次必成功位置包之前所有合法扰动的**非零共享因果备份及后继信息状态**，寻找非空可移位闭合证书。

---

**Run251完整checkout/安全合并核验（2026-11-01 UTC）：** PR #76 https://github.com/zhouxingxing1279/AcademicReaserch/pull/76 的CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41355983604 已completed/success；Python3.13完整checkout的Run249/250/251聚焦测试**27/27通过、无跳过**（读取job日志），源码编译、精确JSON归档逐字对比及artifact上传成功。合并前ahead=8/behind=0，expected head `d6d06582347e29f301743cc5fd57bf63869f780b`，非强制squash合并代码main SHA `913a79ff69a453245c4f6b90d030503925bb8283`；重新读取main及源码/归档/日志Blob确认落地。push触发的main Actions运行未独立读取，**不宣称main CI成功**。本补记仅修改文档，不改变数学证书。Gate A仍blocked。

---

# 当前研究检查点 — Run251（2026-11-01；CI/合并待独立核验）

**基准远端main：** `bf323f99a6b8dcd8a96d17dcd70de734e20ae972`，含Run250及背景第4轮。**本轮严格信息限制：** 对Run249冻结四状态Euler、固定T=9.81N、h=0.02s、|r|≤2.028989375m/s²，构造从同一真实初态(0,0,0,0)、共同零力矩出发的两条**真实可达且逐拍满足硬约束**的扰动轨迹。第5/10/15拍位置包即使全部成功，存在相同位置读数0（噪声半宽0.02m）及相同角度/角速读数；但第15拍真实速度分别为±0.26376861875m/s，相差**0.5275372375m/s**。所以这一合法共同观测历史的任何可靠SMF后验速度投影直径至少0.5275372375m/s。Fraction精确原始/对偶证书证明该差距在“成对反号扰动、精确相同终点位置”的受限LP中最优；**不是每个后验的统一宽度下界、不是安全不可行性证明**。5/10拍的对应必要半宽也已精确归档。

**本轮工件：** `verification/check_velocity_indistinguishability.py`、`verification/test_velocity_indistinguishability.py`、`results/velocity_indistinguishability_20261101/checks.json`、`.github/workflows/run251-velocity-indistinguishability.yml`、`docs/research/run251_research_log.md`。隔离Python3.13本地7项测试中6通过、1项因缺Run249完整源码跳过，语法编译和精确JSON生成通过；完整仓库集成与CI须实际验证。Yang/Ozay(2021)公开论文§3–4及Proposition 4/5重读，统一论文去重98篇不变。

**Gate A仍blocked：** Run249的55拍有限安全闭环、Run250零备份67拍最大安全时域不变。没有非空输出反馈终端信息状态受控不变核、无限递归可行/稳定性、六状态安全或20ms WCET。本轮证明必要信息宽度，不是新控制器。

**下一轮唯一优先任务：** 对15拍共同观测的两种隐藏速度构造共享因果非零控制和安全后继检验，先在一个非空信息状态上尝试后继闭合的正向证书；不把必要信息宽度或有限安全误写为无限保证。

---

**Run250完整checkout与main合并核验（2026-11-01 UTC）：** 研究PR #73 https://github.com/zhouxingxing1279/AcademicReaserch/pull/73 已在ahead=7/behind=0、mergeable_state=clean、expected head `879ee532e3fe1e5c876f81266d65a0f389b9077f` 条件下非强制squash合并，代码main SHA `5f410044071d629522bbe18a2edddf0927412119`，已重新读取main、PR merged及源码/归档Blob核验。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41350799741 与main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41350936591 均completed/success；Python3.13完整checkout Run224–250聚焦回归、真实配置/Run249交叉核验、精确归档JSON对比及工件上传均成功。沿用Run249的233项并新增9项理论上共242项，但未读取逐项unittest日志，故只以实际工作流成功为证据。全仓库历史回归、一般SMF＋MPC递归可行、六状态安全和20ms最坏时延仍未认证。此补记不改变控制算法或数学证书。

---

# 当前研究检查点 — Run250（2026-11-01；CI/合并状态须另行核验）

**基准远端main：** `f9348c2b5ff83a3f9713ad8058ea4b0f8eafb4cf`，含Run249完整四状态有限截止SMF＋网格MPC闭环及背景研究PR #72。**本轮唯一瓶颈：** Run249零力矩55拍备份能否作为可反复滚动的终端安全合同？**严格结论：不能直接重启同一个零力矩55拍备份。**对配置整个初始盒、所有独立有界扰动，精确Fraction区间外包认证零力矩至第67拍全部安全；一个合法真实初始角点 `(-0.02,-0.1,+0.005,+0.01)`、逐拍`r=-R`、零力矩下第68拍`v<=-3.0155175025m/s`，严格越界裕度至少0.0155175025m/s。故**固定零力矩策略**的全初始盒鲁棒安全最长67拍；这不排除其他可执行反馈、也不证明第55拍真实状态对任何未来控制不可生存。

**新增工件：** `verification/check_four_state_zero_backup_horizon.py`、`verification/test_four_state_zero_backup_horizon.py`（9项）、`results/four_state_zero_backup_horizon_20261101/checks.json`、`.github/workflows/run250-zero-backup-horizon.yml`、`docs/research/run250_research_log.md`。隔离Linux/Python3.13.5本地7通过/2因无完整checkout跳过，源码编译与JSON生成成功；完整checkout与GitHub Actions待实际核验。新增Wabersich/Zeilinger (2023) IEEE TAC预测CBF公开正文分节已读，统一论文去重96→97；不能套用其全状态终端CBF定理给当前有噪间歇SMF补造无限安全保证。

**Gate A仍blocked：** Run249有固定55拍SMF＋MPC真实滚动闭环及有限安全证明，但无非空输出反馈终端信息状态RCI、无限时域递归可行/稳定性、六状态安全、20ms最坏时延。**下一轮唯一优先任务：** 针对Run249第55拍真实可达的关联SMF后验，尝试非零共享因果备份与非空终端后继闭合的严格正向证书；不能只继续增加零备份截止时间。

---

**Run249完整checkout与安全合并核验（2026-11-01 UTC）：** 研究PR #70 https://github.com/zhouxingxing1279/AcademicReaserch/pull/70 基于main `c00e7c70557159811bd09862ce9ef2d54354e2e3`，合并前compare ahead=7/behind=0、mergeable_state=clean，预期head=`60748cd92f41205c22c24e09fe85a351ce578397`。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41345024930 为**completed/success**，Python 3.13完整checkout Run224–249聚焦**233/233测试通过、无跳过**（64.267s），真实配置、归档JSON逐字核验与artifact上传成功。通过非强制squash合并至main `ce1ec02602270521963d00f408ccae873913bbd6`，重新读取main SHA、PR merged状态及新增源码/测试/证书Blob确认落地。合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41345183186 **completed/success**，完整checkout再次**233/233通过、无跳过**（84.508s），归档一致与artifact上传成功。该补记仅更新文档，未改变算法或验证证书；仍无无限时域输出反馈递归可行性、六状态安全或20ms最坏耗时认证。

---

# 当前研究检查点 — Run249（2026-11-01；CI与合并须另行核验）

**基准main：** `c00e7c70557159811bd09862ce9ef2d54354e2e3`，含Run248与模型选型PR #69。**新增真实闭环：** 四状态固定T=9.81的冻结Euler子系统，55拍（1.1秒）固定绝对截止时域的SMF后验→三步网格MPC→首拍+全零尾鲁棒安全过滤→plant→有噪位置success/miss及每拍姿态测量更新。控制不读取隐藏速度/未来包；全区间用Fraction、正弦Taylor包络与向外网格舍入。精确全初始盒零力矩55拍安全（|p|<=1.3849438439m、|v|<=2.4441121266m/s）；首拍通过零尾检验后，任何合法测量后验都包含于预测集合，零尾剩余时域仍可行，因此证明**仅至绝对第55拍的因果硬约束满足和有限截止时间可行性**，不是无限递归可行/终端不变/稳定。

**数值重放：** 24条55拍轨迹（12 MPC＋12零力矩），1320拍，5280个四维分量包含检查、0采样约束违约；MPC 94次非零力矩，选定样本平均位置RMSE 0.09203m vs 零力矩0.09701m，不能推广为普遍优势。隔离Python3.13.5测试11项中9通过、2项因无完整checkout跳过，`py_compile`与归档生成成功；本地平均单步求解约31.65ms，**超过20ms目标**，非WCET。PR完整checkout CI及真实配置断言待验证，不能提前宣称成功。

**严格边界：** Run248固定脉冲第14拍不可生存反例仍成立；Run249不是对该前缀的无限修复。仅四状态、固定推力、粗区间SMF和有限截止55拍；无非空输出反馈终端RCI、一般SMF/CZ＋Tube MPC无限递归可行、六状态安全、推力调度或20ms最坏时延。Gate A仍blocked。Qiu等(2020)期刊开放正文§2–4分节重读，统一去重论文数保持95篇。

**工件：** `verification/check_four_state_shielded_smf_mpc.py`、`verification/test_four_state_shielded_smf_mpc.py`、`results/four_state_shielded_smf_mpc_20261101/checks.json`、`.github/workflows/run249-shielded-smf-mpc.yml`、`docs/research/run249_research_log.md`。

**下一轮唯一优先任务：** 尝试构造非空、可重复闭合的输出反馈终端信息状态与共享因果备份律，先检查Run249第55拍后验族及Run248不可生存反例；若不能给出严格正向证书，明确将硕士目标调整为条件性有限时域安全过滤而非无止境扩大截止时间。

---

**Run248完整checkout与合并核验（2026-11-01）：** PR #67 https://github.com/zhouxingxing1279/AcademicReaserch/pull/67 已安全squash合并，代码main SHA 671c7a5a878524fc522d17c4ccd8de3daa601016；PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41340127964 与main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41340319892 均completed/success，Python 3.13.17完整checkout Run224–248聚焦测试**222/222通过、无跳过**，真实配置、精确Fraction归档与artifact上传均成功。已重新读取main SHA、PR merged、源码与证书Blob。此补记只修改文档，不改变数学证明或算法；全仓库历史回归及SMF+MPC递归可行性、六状态安全、20ms最坏时延仍未认证。

---

**Run248阶段检查点（2026-11-01；合并/CI须独立核验）：** 基于main 72724f81ef10046eeb41f0ed6398695ab6533e05，发现Run245固定前缀另一合法真实初始角点(p,v,phi,omega)=(-0.02,-0.1,+0.005,+0.01)、持续r=-R下，**第14拍已严格不可生存**：phi14=0.1502、omega14=0.81，任何后续合法力矩（甚至全状态/非因果）在持续r=-R下最迟第44拍有v44<=-3.002033058421m/s，严格越界裕度>0.002033m/s；Run247原角点第26拍拒绝仍正确但不是最坏初始盒角点。数学证书 verification/check_four_state_corner_viability.py、11项测试、results/four_state_corner_viability_20261101/checks.json、日志 docs/research/run248_research_log.md。隔离Python 9通过/2缺完整仓库跳过；PR/main CI需按真实结果另行确认。Yang/Ozay(2021)§3–4重读，统一论文去重94篇不增加。**证据范围：** 只反证Run245指定前缀，有限guard首次拒绝不等于真实最早失效；无SMF后验、MPC优化、递归可行、六状态安全或20ms WCET，Gate A仍blocked。**下一轮唯一优先任务：** 把共享因果控制与关联SMF决策前移至第10拍success/miss机会，覆盖双向扰动及真实丢包自动机，先验证非空安全前缀，不能再仅在第25拍补救。

---

**Run247完整checkout与安全合并核验（2026-11-01）：** 研究PR #64 https://github.com/zhouxingxing1279/AcademicReaserch/pull/64 基于main `8b7b22c757749fcc6290d7bdbd7fc494a64e86b6`，合并前compare ahead=7/behind=0、mergeable_state=clean，head=`8271e2e5e1042b2bda9595f3b1a5863bc10d4111`。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41335351537 **completed/success**；Python 3.13.17完整checkout Run224–247聚焦测试**211/211通过、无跳过**（74.114s），真实配置、Run246轨迹逐项比较、Fraction精确证书、归档JSON对比与artifact上传成功。PR非强制squash合并至main `193d4cd99e7f48ff56b43f8289336ff75c492cc5`，已重新读取main、PR merged及源码/归档/阅读记录Blob确认落地。合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41335523410 **completed/success**，Python 3.13.17完整checkout再次**211/211通过、无跳过**（56.300s），证书一致性与artifact上传成功。此证据补记仅更新文档，未改变算法；全仓库历史回归、SMF＋MPC递归可行、六状态安全和20ms最坏求解时延仍未认证。

---

# 当前研究检查点 — Run247（2026-11-01）

**main基准：** `8b7b22c757749fcc6290d7bdbd7fc494a64e86b6`。主方向仍为四旋翼MPC＋SMF输出反馈闭环，允许背景任务比较低维/平面/高维模型，但不得把四状态必要guard误称一般模型的充分控制律。

**严格数学增量：** 在Run245/246冻结四状态Euler、固定T=9.81N、`|tau|<=0.08Nm`、`|r|<=2.028989375m/s²`和角度/速度硬界下，推导任意当前真实`(v,phi,omega)`、未来N拍的**双向必要可生存速度区间**。通过Euler因果索引`j(j-1)/2`、安全角度剪裁和精确有理数sin上下界，分别固定合法`r=-R`和`r=+R`；即使允许任意未来全状态/非因果力矩，区间外状态也不可能满足全部安全约束。它是**必要条件**，不提供控制器、充分性、终端不变性或递归可行性。

**Run245合法角点真实轨迹：** 前26拍安全，但第26拍`phi=0.2202rad`、`omega=-0.01rad/s`、`v<=-1.70139869449m/s`；未来20拍的必要下界为`v>=-1.69261511798m/s`，严格差距`0.00878357651m/s`。因此即使从第26拍起完全知晓状态并任意选择合法力矩，合法持续负向扰动使`v46<=-3.00878357651m/s`，最迟第46拍越界。Run246第30拍才检测到的不可恢复性，本轮提前至第26拍。对第0至25拍的1–30拍必要guard扫描未拒绝，**不证明那些状态可生存**。实际位置包第25拍可success/miss，不能预设一定获得新位置测量。

**验证与文献：** `verification/check_four_state_early_viability_guard.py`、11项测试、精确JSON、Run247 CI工作流、`docs/research/run247_research_log.md`。隔离Python测试9通过、2项因缺完整checkout跳过；完整GitHub PR CI和远端合并状态需单独核验。新分节已读Breeden/Zaccarian/Panagou (2024) arXiv:2403.03663v3（定时量测/误差界/robust timed CBF，卫星算例，不直接覆盖四旋翼有噪位置SMF），统一去重已读92→93篇。**Gate A仍blocked**：无四状态SMF＋MPC递归可行、六状态安全或20ms最坏求解时延认证。

**下一轮唯一优先任务：** 在真实第25拍success/miss分支上结合Run240关联SMF后验，寻找能避开第26拍不可生存区域的共享因果可执行控制，并严格认证至少一个非空后继分支；不要把必要筛选通过写成充分安全。

---

**Run239完整checkout及合并核验（2026-11-01）：** PR #47 https://github.com/zhouxingxing1279/AcademicReaserch/pull/47 已安全Squash合并，代码main SHA 60905d7f00c0da013e1d8995fa0da64af47fe8eb，重新读取main及源码、测试、JSON和论文日志Blob核验。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41296087821 与main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41296187607 均success；Python 3.13.17完整checkout聚焦测试121/121通过、无跳过，真实配置、Fraction证书、JSON逐字比对、artifact上传成功。未执行全仓库历史回归、递归可行性或20ms最坏时间认证。该补记不改变算法。

---

## Run239 当前检查点（2026-11-01）

**基准main：** f40c17e4833f6186c4e44b67b552c1a1e70f9e5e。Run238指定两状态纤维15拍可达zonotope与本轮配置核验一致。本轮在15拍成功有噪位置观测y_px=0、|n_px|≤0.02m条件下，按初始速度正负两分支建立精确CZ测量交，使用Fraction原始/对偶支持证书得到速度后验半宽353411321/960000000≈0.36813679m/s，相对先验0.6522563875m/s收紧约43.56%；若y=先验最大位置，速度上界不收缩，故**无统一观测收缩率**。该条件后验下再零力矩15拍的严格安全盒为|p|≤0.215659m、|v|≤0.976834m/s；**不是终端不变集、全先验SMF或MPC递归可行证明**。源码、10项测试、JSON、CI及日志见Run239研究记录；CI及远端合并状态须单独核验。Gate A仍blocked。

**下一轮唯一任务：** 对所有可达位置观测和5/10/15拍模式建立统一SMF后验及共享控制可行性判据，首先审计最坏观测分支。

---

**Run237完整checkout CI与合并核验（2026-11-01）：** PR #43 https://github.com/zhouxingxing1279/AcademicReaserch/pull/43 已非强制Squash合并到main `12213e80725935931c1fb5578b19450bb01ef270`，重新读取main及验证器Blob核验。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41283529172 和main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41283612955 均success。Python 3.13.17完整checkout Run224–237聚焦测试**102/102通过、无跳过**，真实配置、精确支持证书、JSON归档比对及artifact上传成功。文档补记不改变算法，未单独触发CI；全仓库历史回归、SMF-MPC闭环和20ms最坏时间仍未认证。

---

## Run237 当前检查点（2026-11-01）

**基准main：** a51a657de081c7b49884569fd02b87326c93126d。Run235固定推力全状态反馈有限4000生成元F仍严格RPI，但Run237以精确Fraction计算F的支持函数，找到方向l=(13939/100000,55667/100000,-252917/100000,-1)；对Run236相同观测的x±=(0,±hD,0,0)，分别选合法r=±R，若两个实际后继都属于F，前者要求共享tau>0.0181 Nm，后者要求tau< -0.0181 Nm。严格矛盾，证明**指定两状态SMF后验纤维对原F不存在共享一步终端力矩**，强于Run236的“原K不可测”结论；不排除其他输出反馈终端集合/动态策略。

**工件：** verification/check_four_state_shared_successor.py、8项测试、results/four_state_shared_successor_20261101/checks.json、.github/workflows/run237-shared-successor.yml、docs/research/run237_research_log.md。隔离最小镜像7/8通过、1项缺完整checkout跳过，GitHub CI待核实。Qiu等(2020)公开原文§2–4分节阅读，去重91篇不变。**Gate A=blocked**，尚无四状态SMF+MPC递归可行、稳定、六状态安全或20ms最坏时延保证。

**下一轮唯一任务：** 构造允许估计误差/观测历史进入终端状态的共享因果备份律及终端集合，首先对Run236两状态纤维给出严格一步可行见证，再追求递归闭合。

---

**Run236合并与完整checkout验证（2026-11-01）：** PR #41 https://github.com/zhouxingxing1279/AcademicReaserch/pull/41 已安全Squash合并到main 7afc3a60e663fd7640fc7e6eb60bb7d8c4643744；PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41279295891 和main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41279361402 均success。Python 3.13.17完整checkout Run224–236共94/94项聚焦测试通过、无跳过，真实配置、编译、精确有理数及归档JSON逐字比对成功；新增源码/测试/JSON Blob已重新读取核验。**证据补记不改变算法，未单独触发CI；未执行全仓库历史回归，Gate A仍blocked。**

---

## Run236 当前检查点（2026-11-01）

**基准main：** 9442a873d89c270204fa32b4562334e1d0a07d1b。Run235有限4000生成元F仍为严格固定推力全状态反馈RCI；Run236证明F内且属于初始先验的两个状态 x±=(0,±1742383/40000000,0,0)，在初始成功位置包下具有相同(p,phi,omega)观测，但Run235反馈需要相反力矩±430368601/20000000000 Nm。任何共享观测力矩至少对一个状态偏离原全状态律0.02151843005 Nm；角速度下一拍相对该全状态律误差同值。100项精确有理数支持函数证明sup_F|Kx|>0.06 Nm，故朴素全局三角收紧0.06+0.02151843005>0.08 Nm无法认证。**不证明没有其他共享力矩，也不证明F在共享控制下必然不变性失败。**

**证据：** verification/check_four_state_shared_torque.py、8项测试、results/four_state_shared_torque_20261101/checks.json。Python 3.13本地最小模块镜像7/8通过、1项缺完整checkout跳过；GitHub Actions真实配置和Run224–236聚焦回归待验证。首次缺Run235模块的ModuleNotFoundError已修复并重测。文献日志纠正Lucia等2023期刊DOI及卷号，已读仍91篇。**Gate A仍blocked**：没有共享因果终端律、SMF+Tube MPC递归可行、六状态安全或20ms最坏时延证明。

**下一轮唯一任务：** 对同一后验纤维建立真正的exists shared torque / forall hidden states and disturbances的一步F后继包含判定；不可把Run236特定K不具备观测可实现性误写成所有共享控制不可能。

---

**Run229完整仓库CI与合并核验（2026-10-31）：** 研究PR #27 https://github.com/zhouxingxing1279/AcademicReaserch/pull/27 已通过非强制Squash合并，代码main SHA `4964ff795a4dd8a4e1398ef77a2c1b740b436fae`。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41251472104 与合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41251521934 均为success；Python 3.13，完整checkout Run224–229共40/40聚焦测试通过，无跳过，真实配置、编译、有理数摘要断言和完整JSON artifact上传成功。已重新读取main SHA及新增源码/测试Blob。**未执行全仓库历史回归；无非空终端RCI、输出反馈SMF＋MPC递归可行、稳定性、六状态安全或20ms最坏耗时证明。** 本补记是文档更新，不改变控制算法。

---

## Run229 当前检查点（2026-10-31）

**基准main：** `20bf13cdfb1de57ffddacae58ecda5b11ded69cb`。针对Run228中央桥速度分叉，构造种子小盒与正负速度分支，使用Run228精确Fraction外包和并集覆盖取得3条经认证的有向边：种子→正负速度两盒，各分支→各自第二拍位置—速度关联盒。固定 `T=981/200`、`tau=0`；所有后继均满足冻结四状态安全盒。第一拍速度半宽为 `17675197493460000327/400000000000000000000≈0.044188` m/s，中心点两侧对抗速度幅值至少 `6254383/160000000≈0.039089894` m/s。此图为**两拍无环DAG**，无自环、无非空RCI、无SMF输出反馈递归可行性或稳定性证明。验证器正向回归价值明确，但研究创新性仍未建立。

**测试：** Python 3.13本地等公式隔离镜像6项中5通过、1项因无完整checkout跳过；语法编译与JSON生成成功。新增GitHub Actions完整仓库Run224–229回归及配置/有理数断言，CI成功之前不宣称通过。统一论文日志定向复核Li/Liu(2018)原文Proposition 2等，去重已读仍89篇。

**Gate A=blocked。下一轮唯一任务：** 寻找并严格认证一个非空闭合循环单元终端集合（含正负扰动分叉），或提供严谨阻塞证书；不将有限DAG当作MPC终端集合。

---

**Run228合并与CI核验补记（2026-10-31）：** PR #25已非强制Squash合并至main `57f749a884588247b846d251103a2c745f444b6b`。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41246301443 与main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41246344516 均success；Python 3.13.17，完整checkout Run224–228聚焦测试34/34通过、真实配置/编译/精确摘要核验及JSON artifact上传成功。无全仓库历史回归、四状态RCI、输出反馈MPC安全或20ms最坏耗时保证。

---

## Run228 当前检查点（2026-10-31）

基准main `2d25c3736bc987edf2b4b3d53e0dc155e9263810`。冻结Run224四状态Euler/Run208–210逐拍独立对抗残差，针对Run227必须穿越的小倾角桥构造三个闭盒的策略图候选。严格证明若中心 `(0,0,0,0)` 被包含且其他单元排除 `phi=0`，中央桥 `|v|<=0.03` 则非RCI：任意控制下合法 `r=+R(T)` 使 `v+>=6254383/160000000=0.03908989375`，越界严格裕度 `1454383/160000000`。扩大至 `|v|<=0.05` 后此反例失效，但不意味着RCI成立。

新增精确Fraction区间后继、闭盒并集覆盖、9输入/单元的保守图扫描；两种候选均未找到经认证的单元控制边，**仅表示当前菜单与外包无法认证**，不是连续控制不可行证明。7/8本地测试通过，1项真实配置检查缺checkout跳过；新增CI用于完整仓库复核。统一论文日志新增Li/Liu(2018)正式期刊版分节复核，与2016预印本去重，仍89篇。

**Gate A=blocked**：无四状态非空RCI、SMF输出反馈MPC递归可行、稳定性、六状态安全及20ms最坏时间证明。**下一轮唯一任务：** 扩大桥速度宽度并加入位置—速度相关邻接单元，尝试认证至少一条可靠单元后继边。

---

## Run227 合并与CI核验补记（2026-10-31）

PR #22已非强制Squash合并到main首个SHA `5efed49fd0c477cc591b4d91ee16c5ce138aab01`；PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41242517572 和合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41242569200 均success，完整checkout Run224–227聚焦测试26/26通过、配置/编译/归档逐字核验通过。新增源码、测试、结果Blob SHA与研究分支一致。仍未完成全仓库回归、四状态RCI、SMF输出反馈Tube MPC递归可行性、六状态安全或20ms最坏耗时。

---

## Run227 当前研究检查点（2026-10-31）

**基准main：** 4817403c2ac4dae7c1abe348f0096b3e21bcf5ff。冻结Run224–226四状态Euler及Run208/210逐拍独立残差。提出非空位置—速度—倾角耦合双模式终端候选 C_switch，严格证明它不是RCI：x=(0,0,0.15,0)在r=-R(T)下对任何控制后继phi*v<0。更一般地，任何非空RCI都必须包含至少一个|phi|<=0.02 rad的状态；任何完全落在|phi|>=0.15两倾角带的集合均非RCI，最迟112拍有严格对抗速度越界证书。任何非空轴对齐四状态笛卡尔积盒也不可能为RCI。以上是严格必要几何/负面结果，**没有构造非空RCI**。

**本地验证：** Python 3.13.5，7项中6通过、1项缺完整checkout跳过，语法编译和JSON生成成功。随后完整checkout GitHub Actions已执行Run224–227聚焦测试26/26通过、真实配置及归档核验成功；详见本文件顶部合并补记。

**文献：** 新增Li与Liu(2016) arXiv:1608.08683原文分节阅读，统一去重已读88→89。区间分区思想可借鉴，但论文有限模式不直接适用本项目连续控制和对抗扰动。

**Gate A=blocked。** 未完成四状态RCI、SMF输出反馈Tube MPC递归可行、稳定性、六状态安全及20ms最坏时间。

**工件：** verification/check_four_state_terminal_bridge.py；verification/test_four_state_terminal_bridge.py；results/terminal_bridge_20261031/checks.json；docs/research/run227_research_log.md；.github/workflows/run227-terminal-bridge.yml。

**下一轮唯一优先任务：** 构造包含|phi|<=0.02过渡桥的相关四状态有限单元策略图，并严格验证每个单元的exists u forall r后继闭合。

---

## Run226合并与CI核验补记（2026-10-31）

PR #20 https://github.com/zhouxingxing1279/AcademicReaserch/pull/20 已通过非强制Squash安全合并，落地main提交 `8caa45710f9c3255c602274613a60d36ad3c0adf`。完整checkout PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41237414093 和合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41237460322 均为 `success`；Python 3.13.17，Run224/225/226聚焦测试19/19通过，源码编译、真实配置合同、归档JSON逐字比较成功。合并后重新读取main SHA，新增源码/测试/结果Blob分别为 `d120e52789f258adfbc6d455f7fc92702ecc3741`、`9d96e671bd6f33e3d804622cb3b6ebdcb98e5184`、`202c434afd1cf30912b236d5cdb586922f5f557e`，与本地验证一致。**未执行全仓库历史回归；未证明四状态RCI、完整SMF＋MPC递归可行性或20ms最坏耗时。**

---

## Run226 当前研究检查点（2026-10-31）

**基准远端main：** `5ddca85294ecfd5a1693410c9cc9b0e0e70ef2bc`。唯一主方向：无人机MPC＋SMF鲁棒输出反馈闭环，子问题允许证据驱动调整。

**严格新增：** 冻结四状态Euler及Run208/210逐拍独立横向残差下，三步正确因果前驱Pre³(X)有正负两个严格可行见证 `(0,±3,±0.15,0)`，固定三拍TMAX、tau=0；而 `(0,±3,±0.15,∓0.4)` 严格属于Pre²(X)但不属于Pre³(X)。所有合法因果控制在三拍对抗残差下的速度越界下界为 `31023794855816198031/39062500000000000000000≈0.0007942091483m/s>0`。这是一项有限时域严格证书，**不是**非空RCI核、四状态输出反馈安全或递归可行性证明。

**测试：** Python 3.13.5本地兼容镜像7项聚焦测试6通过1项完整checkout配置跳过，语法编译、归档JSON通过。新增CI用于完整checkout Run224/225/226测试、真实配置和归档逐字比对；未取得CI成功前不宣称成功。无全仓库回归和20ms最坏耗时保证。

**文献：** Liu等（2021）arXiv:2109.12378，新增原文§II–IV-A分节阅读，核对可见/不可见扰动量词、Theorems 1–2；去重已读87→88，非全文精读。唯一论文日志已更新，历史READ_PAPERS不改。

**Gate A=blocked。** 二维姿态SMF＋MPC局部递归可行性（Run221限定假设）仍成立；四状态RCI终端、完整SMF输出反馈Tube MPC、稳定性和六状态安全未建立。不要把有限步全状态反馈证书当作鲁棒安全控制器。

**工件：** `verification/check_four_state_three_step_predecessor.py`、`verification/test_four_state_three_step_predecessor.py`、`results/three_step_predecessor_20261031/checks.json`、`docs/research/run226_research_log.md`、`.github/workflows/run226-three-step-predecessor.yml`。

**下一轮唯一优先任务：** 不再机械增加Pre步数；构造具有双侧倾角切换的四状态联合终端候选并验证真正鲁棒受控不变性，失败则保留阻塞证书并收敛课题范围。

---

## Run225 合并与 CI 实测补记（2026-10-31）

PR #18 https://github.com/zhouxingxing1279/AcademicReaserch/pull/18 已通过非强制 Squash 安全合并，首个 main 落地 SHA 为 6c1a574c6c742c1335bd5b3592eea486b2d2171b；重新读取远端 main 和新增源码/测试/结果文件 Blob SHA 确认落地。PR 完整 checkout CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41232818700 为 success；合并后 main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41232866432 为 success。两者均执行旧 Run224 和新 Run225 聚焦测试、Python 语法编译、真实配置合同检查、归档 JSON 逐字比对。**未执行全仓库历史回归，亦无四状态终端不变性/20ms 最坏执行时间保证。**

# 当前研究检查点 — Run225（2026-10-31）

**基准 main：** b4b8d6beeaabf0e25d53fef4dad9289a2e822716。唯一主方向为无人机 MPC＋SMF 鲁棒输出反馈闭环；不锁死历史子题。

**严格增量：** 在冻结四状态 Euler 模型及 Run208/210 每拍独立横向残差合同下，二步正确量词 Pre²(X)=Pre(Pre(X))：exists u0 forall r0 exists u1(x1) forall r1。以 Fraction 和 sin 的严格 Taylor 上下界证明 (0,±3,±3/20,0) 属于 Pre²(X)（固定两拍 TMAX、tau=0）；而 (0,±3,±3/20,∓2) 属于 Pre(X) 但不属于 Pre²(X)。对抗速度越界的精确下界为 15703932131047/2000000000000000 m/s，任意合法因果推力/力矩均不能避免；严格排除不等于真实物理气动必然如此。

**证据边界：** 两步前驱非空，不是鲁棒受控不变终端核；全状态反馈不等于部分观测SMF；没有四状态 MPC 递归可行性、Lyapunov 稳定性、六状态安全或20ms最坏耗时。**Gate A=blocked。**

**测试：** 本地源码兼容镜像 Python 3.13：6项中5通过，1项因缺完整 checkout 跳过；py_compile、JSON生成通过。新增 GitHub Actions 将在完整仓库检查旧新测试、配置与归档JSON逐字一致；成功前不宣称 CI 通过。

**文献：** Kolmanovsky & Gilbert (1998), DOI https://doi.org/10.1155/S1024123X98000866，出版商摘要及书目复核；未读正文，不新增已读篇数；唯一阅读日志去重87篇不变。

**工件：** verification/check_four_state_two_step_predecessor.py；verification/test_four_state_two_step_predecessor.py；results/two_step_predecessor_20261031/checks.json；docs/research/run225_research_log.md；.github/workflows/run225-two-step-predecessor.yml。

**下一轮唯一优先任务：** 计算第三轮鲁棒前驱的严格局部内外证书，检验二步正见证是否继续安全，不把有限步见证误称为终端不变性。

---

**Run224验证后补记（2026-10-31）：** PR #16（https://github.com/zhouxingxing1279/AcademicReaserch/pull/16）已通过非强制Squash合并至main提交 1defcf77b9776c40e7febb835b2fe6db2d9a7fdb。完整checkout GitHub Actions运行 https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41227640954 状态success；verify job含Python语法编译、6项测试、真实配置断言与归档JSON逐字比对，均成功。新增源码、测试、归档及CI工作流的Git Blob SHA与本地已测文件逐项一致。**这是聚焦测试，不是全仓库回归或完整闭环证明。**

# 当前研究检查点 — Run224（2026-10-31）

**基准main：** 372fdc669e58ec8a3987e544f401e077813f6eed。**主方向：** 四旋翼MPC＋SMF鲁棒输出反馈闭环，证据驱动收敛。

**严格增量：** 对冻结四状态安全盒X，定义正确因果前驱Pre(X)：存在当前状态反馈控制(T,tau)，使对所有合法Run208/210横向残差，下一状态仍属于X。以Fraction和sin的s7/s5 Taylor上下界证明x=(0,±3,±3/20,0)在T=2943/200、tau=0时属于Pre(X)，而x=(0,±3,±717/5000,0)在任何合法推力下都被对抗残差严格排除。**仅一步前驱，不是终端鲁棒受控不变核，也不是SMF输出反馈可行性。**

**验证：** 本地Python 6项测试5通过、1项因缺完整checkout跳过；py_compile及归档JSON生成通过。新增GitHub Actions工作流负责完整checkout配置核验、6项测试和结果逐字比对，需实际成功后才可宣称CI通过。

**文献：** Kolmanovsky与Gilbert（1998），DOI https://doi.org/10.1155/S1024123X98000866，出版商摘要/书目核验，非正文精读；唯一论文日志去重已读仍87篇。

**Gate A=blocked：** Run221二维姿态局部递归可行性仍成立（限定假设）；四状态终端RCI、部分观测Tube MPC递归可行性、稳定性、六状态鲁棒安全、20ms最坏耗时均未证明。不能由Pre(X)非空推出无限时域安全。

**工件：** verification/check_four_state_one_step_predecessor.py、verification/test_four_state_one_step_predecessor.py、results/one_step_predecessor_20261031/checks.json、docs/research/run224_research_log.md、.github/workflows/run224-one-step-predecessor.yml。

**下一轮唯一优先任务：** 计算第二轮正确因果前驱Pre(Pre(X))，严格检查双侧边界见证是否可持续；不在单步非空基础上虚报终端不变性。

---

# 当前研究检查点 — Run223（2026-10-31）

**基准main：** f72155bf15c782ca32d51d0cd873524060d1372e。**主方向：** 无人机MPC＋SMF鲁棒输出反馈闭环，保持单课题收敛。

**本轮严格必要条件：** 在Run208/210允许每拍独立选择|r_x|≤47/25+(243/16000)T、T∈[981/200,2943/200]、h=1/50、|vx|≤3的冻结横向Euler模型下，使用Taylor有理数上界证明：任何非空鲁棒受控不变四状态集合C必须满足sup_C(phi)>717/5000=0.1434和inf_C(phi)<-717/5000。任意完全落在phi≤0.1434或phi≥-0.1434的候选终端集合都会被合法持续对抗残差强制违反速度约束。r=0.14的严格有限越界上限为5988拍；r=0.1434为519396拍。若轨迹需要从+0.1434转到-0.1434，姿态速率界给出至少8拍的运动学下界，不是可达性证明。

**证据边界：** 必要条件，不是非空终端核构造。对r=0.15漂移下界为负，不能断言可行。未完成四状态SMF/MPC递归可行、稳定、六状态安全。Run221二维姿态闭环保证不变；Gate A仍blocked。该极端扰动合同不等同真实持续气动扰动。

**测试：** 本地Python 3标准库Fraction，5项测试4通过、1项因无完整checkout跳过，py_compile成功；新增CI将核对真实配置、全部5项测试及归档JSON。未见成功CI前不得宣称已通过。

**文献：** Kolmanovsky与Gilbert（1998），DOI https://doi.org/10.1155/S1024123X98000866，出版商摘要核验；Blanchini（1999），DOI https://doi.org/10.1016/S0005-1098(99)00113-2，书目核验。均未新增正文精读计数；统一论文阅读记录87篇不变。

**工件：** verification/check_two_sided_terminal_necessity.py、verification/test_two_sided_terminal_necessity.py、results/two_sided_terminal_20261031/checks.json、docs/research/run223_research_log.md、.github/workflows/run223-two-sided-terminal.yml。

**下一轮唯一优先任务：** 对允许|phi|>0.1434的四状态联合终端候选，计算一轮正确因果量词的鲁棒前驱，给出非空内核见证或严格进一步阻塞；之后再谈SMF＋Tube MPC集成。

---

# 当前研究检查点 — Run222（2026-10-31）

**主方向：** 无人机MPC＋SMF输出反馈闭环；保持证据驱动单一课题收敛。基准main `5632a93296983955606dc42822f4de5dfeb824f9`。

**严格负面增量：** Run221名义姿态终端 `|z_phi|≤1/20` 与误差RPI `|e_phi|≤1/100` 蕴含真实 `|phi|≤3/50`。在Run208/210冻结四状态Euler横向残差包络 `|r_x|≤47/25+(243/16000)T`、`T∈[981/200,2943/200]` 下，扰动选择 `r_x=+R(T)` 使所有保持该姿态条带的控制策略都满足 `v_x^+-v_x≥3905869/160000000≈0.02441168m/s`。从任意 `|v_x|≤3` 初态出发最多246拍严格越过 `v_x≤3`，故**不存在非空、完全位于该姿态条带及速度硬界内的四状态鲁棒受控不变集合**。这否定了直接扩展Run221姿态终端管的路线，不否定允许更大倾角的其他终端集合。

**验证：** Python 3.13.5 Fraction，6项聚焦测试本地5通过、1项完整checkout配置检查跳过；语法编译通过；新增GitHub Actions完整checkout配置/归档结果核验工作流。CI结果见本轮PR（在完成前不宣称成功）。

**边界：** 上述残差可由不确定性集合中的对手逐拍选择，未证明实际物理气动能持续取极值；与`external_process_halfwidth=0`不矛盾。无四状态闭环MPC、递归可行性、终端Lyapunov或六状态安全证明。**Gate A=blocked。**

**文献：** Mayne等（2006）DOI https://doi.org/10.1016/j.automatica.2006.03.005（已读章节定向复核）；Blanchini（1999）DOI https://doi.org/10.1016/S0005-1098(99)00113-2（仅书目核验，未读正文）。唯一论文阅读记录维持87篇已读历史去重计数。

**本轮工件：** `verification/check_four_state_terminal_obstruction.py`、`verification/test_four_state_terminal_obstruction.py`、`results/four_state_terminal_obstruction_20261031/checks.json`、`docs/research/run222_research_log.md`、`.github/workflows/run222-four-state-obstruction.yml`。

**下一轮唯一优先任务：** 审计允许更大姿态倾角的四状态联合终端可生存核，在全扰动/全推力/硬约束下检验非空性；优先精确必要条件和反例，再进行优化器集成。

---

# 当前研究检查点 — Run221（2026-10-31）

**主方向：** 四旋翼/无人机 MPC＋SMF 输出反馈闭环；单一课题、允许证据驱动收敛。基准main `df66453b7dc0565905c3d366c77f1ee0f27f2141`。

**严格正向增量（限定范围）：** 在真实冻结Euler姿态子通道 `(phi,omega)`，用每拍有界姿态/角速度测量、区间SMF中点、`K=(-8/25,-4/25)`、误差RPI `E={|e_phi|<=1/100,|e_omega+4e_phi|<=1/25}`、名义终端不变集 `Zf={|z_phi|<=1/20,|z_omega+4z_phi|<=1/5}`，完成可执行的有限网格名义MPC与移位尾计划。精确证明姿态通道误差不变、硬约束收紧与递归可行；没有终端Lyapunov下降/目标收敛证明。现有 `check_terminal_polytope.py` 已有同K的角度RPI理论，本轮不宣称创新。

**有限闭环证据：** Python 3.13.5 本地6项测试中5项通过、1项因缺完整checkout跳过；GitHub Actions完整checkout（Python 3.13.17）6/6通过、源码编译和归档结果逐字比对通过；32条48拍确定性轨迹合计1536拍，SMF包含检查全通过、硬约束违约0。相同SMF和K下，MPC平均角度跟踪RMSE约0.01329536 rad，终端律对照约0.04001874 rad；624拍选择非原尾计划。单点优化本地中位5.49ms、p95约6.70ms，非20ms最坏耗时保证。新增GitHub Actions全仓库配置断言与归档结果逐字比对。

**证据边界：** 姿态测量每拍成功、姿态过程扰动为零、初始姿态误差属于E；横向/垂向残差、位置缺测、推力任意跳变、完整四/六状态安全与递归可行均**未证明**。Gate A仍为blocked。当前没有证据表明独立盒/CZ的控制性能优劣在全系统成立。

**文献：** Mayne等(2006), DOI https://doi.org/10.1016/j.automatica.2006.03.005；Lorenzetti与Pavone(2020), DOI https://doi.org/10.23919/ECC51009.2020.9143979。两篇本轮核对原文终端/收紧相关章节，统一论文日志去重87篇不变。

**本轮工件：** `verification/check_attitude_terminal_smf_mpc.py`、`verification/test_attitude_terminal_smf_mpc.py`、`results/attitude_terminal_smf_mpc_20261031/checks.json`、`docs/research/run221_research_log.md`、`.github/workflows/run221-attitude-terminal.yml`。

**下一轮唯一优先任务：** 审计是否存在将本轮姿态终端集合与四状态横向位置/速度约束组合的充分因果受控不变终端集合；如无，则给出精确阻塞证书，绝不把姿态局部保证推广到四状态。

---

# 当前研究检查点 — Run220（2026-10-31）

**主方向：** 无人机MPC＋SMF输出反馈闭环；以可复现的安全基线与真实控制收益为目标。

**Run220新增：** 实现1–2条共享扰动历史半空间的双乘子支持对偶上界；浮点HiGHS只生成候选，最终Fraction精确核验，保证上界可靠。合成方盒例中每条单独约束支持为1，双约束精确支持上界为0，证明联合收益可被识别。本地4项聚焦测试通过、1项真实集成跳过；GitHub Actions完整checkout中4项聚焦及1项真实第193拍集成全部通过。

**重要证据边界：** Run219真实第193拍单条约束支持改善0.01158303778、五拍速度裕度仍-0.02473733。Run220在完整checkout测试12个候选第二半空间，**额外可认证支持改善为0**；可认证速度裕度下界仍约-0.02473733，负下界不能判定真实联合后验不可行。双乘子返回的是支持上界，故推得安全裕度下界；负下界不能证明不可行。GitHub Actions run 41208687506成功；没有全仓库回归或20ms在线预算证明。

**Gate A=blocked：** 未实现完整Tube MPC、终端受控不变集、递归可行性、稳定性或六状态安全证明。

**下一轮唯一优先任务：** 停止无目标增加同类三包约束；优先形成可检验的终端安全/递归可行闭环基线，并在固定预算下再比较历史相关性收益。

**本轮工件：** `verification/check_two_shared_rows.py`、`verification/test_two_shared_rows.py`、`docs/research/run220_research_log.md`、`results/two_shared_rows_20261031/checks.json`。

---

# 当前研究检查点 — Run219（2026-10-31）

**主方向：** 四旋翼/无人机MPC＋SMF输出反馈闭环。允许围绕可验证瓶颈收敛具体科学问题，不预设子题与安全定理成立。

**Run219关键严格进展：** 第193拍Run218旧关键支持方向 `q=(0,-1,2943/2000,2943/50000)` 的整个支持极大面，被位置包135、165、180的**共享扰动**线性组合 `lambda=(1,-6,5)` 排除。精确排除裕度 `5212367/500000000=0.010424734>0`；单条有效历史半空间将关键支持上界收紧 `5212367/450000000≈0.01158303778`。旧两块联合外包的六条分别放松扰动条带增益为0（Run218），新证书证实历史相关性确有可计算控制相关增益。

**重要负面结果：** 一条共享扰动半空间收紧后，第193拍五步速度下界的最有利控制裕度仍约 `-0.02473733102<0`。因此**该外包上的有限备份证书仍拒绝**，不证明完整历史后验不可行、真实状态不可生存或递归可行性。第135拍姿态观测另可严格排除旧支持极大点（残差0.0064>0.005），但单独的姿态历史支持改善亦不足以解除阻塞。

**测试与证据：** Python 3.13.5 Fraction，4项聚焦测试通过、1项完整checkout集成测试显式跳过；语法编译通过。源码兼容独立镜像重放192拍，复现Run214/216/218关键数值并严格核验支持改善。**容器DNS无法git clone；没有完整仓库回归或GitHub CI。** 单半空间裁剪约12.38ms，不含历史构造与控制优化；20ms在线预算未证实。

**文献：** Scott等(2016)原文摘要/集合估计定位定向核对，DOI https://doi.org/10.1016/j.automatica.2016.02.036；唯一 `docs/literature/PAPER_READING_LOG.md` 去重仍87篇，不虚增已读。

**Gate A=blocked：** 现有冻结四状态SMF有限闭环和局部Backup，不具备真正鲁棒Tube MPC优化、终端受控不变集、递归可行性、稳定性或六状态四旋翼鲁棒安全证明。

**下一轮唯一优先任务：** 对第193拍选择并联合验证少量独立共享扰动组合约束，判断是否能在计算预算内消除剩余约0.02473733的五拍速度证书阻塞；保留失败案例。

**工件：** `docs/research/run219_research_log.md`、`verification/check_shared_disturbance_support.py`、`verification/test_shared_disturbance_support.py`、`results/shared_disturbance_support_20261031/checks.json`。

---
**上一检查点：** Run218严格证明六条分别放松扰动的跨块历史条带对同一支持方向增益精确为0，见 `docs/research/run218_research_log.md`。
