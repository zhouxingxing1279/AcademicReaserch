# Run177 文献准入卡：五步 information-state 合同

| 工作 | 本轮实际阅读 | 已解决内容 | 与本轮严格边界 |
|---|---|---|---|
| Baras--Patel, *Robust Control of Set-Valued Discrete-Time Dynamical Systems*, IEEE TAC 43(1), 1998, DOI `10.1109/9.654887`，[作者全文](https://user.eng.umd.edu/~baras/publications/journals/1998_Baras_Robust_Control.pdf) | **全文重读 §IV-A，尤其 Lemma 4、Remarks 8--10、Theorems 9--11、Corollary 4** | observation/control history 诱导的信息状态递归；输出反馈鲁棒博弈等价为 information-state 全信息博弈；有限时域动态规划给出必要/充分条件。 | 不提供本仓库非线性四旋翼的有限维集合外包、丢包 mode 终端族或数值证书。 |
| Ghaemi--Del Vecchio, *Control for Safety Specifications of Systems With Imperfect Information on a Partial Order*, IEEE TAC 59(4), 2014, DOI `10.1109/TAC.2014.2301563` | 复核作者稿 §II Problems 1--2、§III Theorem 1、§IV Theorem 4（Run176 已全文精读） | 用 information set 定义因果安全控制，并在 order-preserving 假设下构造控制映射。 | 当前六维 plant 未证明 order-preserving；不能用极端输入定理替代真实非线性前驱。 |
| Yang--Ozay, *Safety Control Synthesis for Systems with Missing Measurements*, IFAC-PapersOnLine 54(5), 2021 | 复核 Run153 对 §§4.1--4.4、Algorithm 1、Propositions 2--5 的全文记录 | 丢包 string/product 模式与中间安全义务。 | mode graph 已是仓库基线；连续有界噪声信息集仍须传播。 |

最强概念基线是 Baras--Patel 的完整信息状态动态规划；最强仓库基线是 Run142 的精确
product-fiber 前驱。当前严格不同处不是“发明 information state”，而是配置初始 posterior **族**、
真实非线性 vertical plant、tick-5 success/miss 两个 mode 后继与将来 terminal family 的可靠有限表示。

**准入判断：新算法/检查器不通过；问题合同纠正通过。** 原因是目标集合尚未按 mode 分层，直接实现
单盒回返会回答错误问题。对照基线应保持同一 plant、输入/风界、测量时序与 observation-fiber 权限。
推翻本判断的证据是：仓库已有一个从全部可行 tick-0 测量出发、同时验证 tick-5 success/miss 后继
进入 mode-indexed terminal information-family 的真实非线性证书；定向检索未发现该对象。

课题推进：明确了递归可行性前必须补齐的接口。反例条件：若任何合法初始 posterior 或任一 tick-5
后继无法进入相应 `T_0/T_1`，候选五步回返族失败；但竖直 `tau=0` 子问题失败不能升级为完整六维
控制策略不存在。
