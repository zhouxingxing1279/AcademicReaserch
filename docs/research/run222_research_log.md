# Run222 — 四状态终端不变集的严格推力/扰动阻塞证书（2026-10-31）

**基准main：** `5632a93296983955606dc42822f4de5dfeb824f9`。**唯一瓶颈：** Run221仅在孤立姿态通道证明终端不变性。审计其姿态终端管是否能作为四状态横向—姿态系统的终端集合，而不继续增加未经验证的SMF条带。

## 冻结模型与量词

根据 `configs/planar_baseline.json`、`docs/research/01_model_and_bounds.md`及Run208/210横向代理合同，四状态 `(p_x,v_x,phi,omega)` 的Euler横向更新为 `p_x^+=p_x+h v_x`、`v_x^+=v_x+h(-T sin(phi)+r_x)`，其中 `h=1/50`、`T∈[981/200,2943/200]`、`|v_x|≤3`，且允许每拍独立的 `r_x∈[-R(T),R(T)]`，`R(T)=47/25+(243/16000)T`。注意 `plant.external_process_halfwidth=0` 与此经Run208定义的**横向模型残差不确定性**不是同一量；本轮的结论以Run208/210残差包络为条件。

Run221名义终端 `|z_phi|≤1/20` 和误差RPI `|e_phi|≤1/100` 若被强制保持，则实际姿态 `|phi|≤3/50`。本轮检验所有非空集合 `C⊆{|phi|≤3/50,|v_x|≤3}` 是否可能对上述**全扰动集合**受控不变。控制允许任意因果策略和全部合法推力/力矩；反例无需指定控制律或依赖传感器数据。

## 严格阻塞证明

对任意控制选择 `T_k`，扰动对手选择每拍合法的 `r_{x,k}=+R(T_k)`。由 `sin(phi)≤|phi|≤3/50` 和 `T>0`：

```
v_x(k+1)-v_x(k)
 = h[-T_k sin(phi_k)+47/25+(243/16000)T_k]
 >= h[47/25+(243/16000-3/50)T_max]
 = 3905869/160000000 > 0.
```

因此，**只要策略保持姿态在Run221终端管内**，对手即可使 `v_x(k)≥v_x(0)+k·3905869/160000000`。即使从 `v_x(0)=-3` 开始，246拍后 `v_x≥240421887/80000000≈3.005274>3`；从零速度开始123拍后 `v_x≥480421887/160000000≈3.002637>3`。若策略先让姿态越出 `|phi|≤3/50`，则同样已经离开假定终端集合。因此**不存在非空的、完全包含于该姿态条带与横向速度硬界内的鲁棒受控不变终端集合**，不仅仅是独立矩形集合失败。

必要的持续抗正向扰动倾角下界（由 `sin(phi)≤phi` 得到）为 `phi≥47/(25T_max)+243/16000=6731149/47088000≈0.142948>0.06`。这只是消除单步正漂移的必要条件，不是新终端集合的充分条件；更大倾角还要考虑姿态动态、输入限制、反向扰动和位置边界。

**证据边界：** 严格结论适用于Run208/210的每拍独立有界残差模型，不等于证明真实气动残差可以长期取该上界，也不否定放宽姿态终端范围、改变扰动包络或重新设计四状态联合终端集合的可能性。没有新建四状态SMF/MPC闭环或证明六状态安全。Gate A保持blocked。

## 论文阅读与关联

- **Mayne, Raković, Findeisen, Allgöwer（2006）**，*Robust output feedback model predictive control of constrained linear systems*，*Automatica* 42(7):1217–1222，DOI https://doi.org/10.1016/j.automatica.2006.03.005 。本轮依据已读§2–4终端/RPI记录和公开摘要定向复核，**非重新全文精读**。关键假设包括有界扰动、误差不变集、非空终端条件；这些不能从孤立姿态证明自动转移至四状态。
- **Blanchini（1999）**，*Set invariance in control*，*Automatica* 35(11):1747–1767，DOI https://doi.org/10.1016/S0005-1098(99)00113-2 。本轮仅核验DBLP书目，**尚未阅读正文**；作为待阅读不变集基础文献，不加入已读计数。

上述漂移阻塞是对仓库冻结模型的自行推导，不是上述论文中的定理。统一论文日志仍为87篇去重已核验历史记录。

## 实现、测试与可复现性

新增 `verification/check_four_state_terminal_obstruction.py`、`verification/test_four_state_terminal_obstruction.py`、`results/four_state_terminal_obstruction_20261031/checks.json` 和专用CI。Linux/Python 3.13.5、仅标准库：

```bash
PYTHONPATH=verification python -m unittest -v verification.test_four_state_terminal_obstruction
python -m py_compile verification/check_four_state_terminal_obstruction.py verification/test_four_state_terminal_obstruction.py
python verification/check_four_state_terminal_obstruction.py --root . --output /tmp/run222_checks.json
diff -u results/four_state_terminal_obstruction_20261031/checks.json /tmp/run222_checks.json
```

本地无完整checkout，6项测试**5通过、1项配置合同跳过**，编译通过、精确结果生成成功。CI应在完整checkout中执行全部6项和归档逐字比较；若CI未成功，不宣称完成完整仓库验证。测试包含正漂移严格分数、123/246拍越界、放宽姿态/收紧残差的反事实检查及证据边界。

## 课题收敛与唯一后续任务

**可行性：** 姿态两状态终端闭环正向可行，但直接将其小角度终端管用于全残差四状态系统被严格否定。**创新性：** 该否定证书是问题设定的必要清理，不作为新控制算法创新。**难度：** 四状态终端必须同时考虑扰动抗衡所需倾角、角速率可达性、推力调度和位置边界，且不能无根据缩小残差界。

**下一轮唯一优先任务：** 在不改变硬约束和残差包络的条件下，检验放宽姿态终端倾角后的四状态联合终端可生存核是否非空；先用全扰动、全推力的可达/不变性必要条件筛除不可能候选，再考虑MPC和SMF的闭环集成。若核为空，保留严格负面证书并评估缩小硕士课题范围。
