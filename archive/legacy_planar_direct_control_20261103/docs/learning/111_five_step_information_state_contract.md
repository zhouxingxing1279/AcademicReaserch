# 111. 五步非线性 information-state 前驱的正确合同

> **Run178 纠正。** 本章的 `T_0/T_1` 只标记 tick 5 的一对局部 success/miss 后继，不能作为
> 无限时域 terminal family。仓库第 88、89 章与 Run154 已给出 60-state 扩展及 45-state
> recurrent family；可靠定义与排重见[第112章](112_terminal_information_family_dedup.md)。

本轮把 Run176 的“配置初始 posterior”拆成了可执行前必须回答的数学对象。结论是：配置并没有给出
单个初始 posterior，而只给出 prior、测量半宽和 tick-0 更新规则。若 tick-0 位置读数为
`y0`，初始信息集应写成

\[
I_0(y_0)=X_0\cap\{x:|C_px-y_{0,x}|\le 0.02,
                         |C_pz-y_{0,z}|\le 0.02,\ldots\},
\]

且 `y0` 本身遍历所有与 `X0` 及噪声界相容的值。因此“从配置初始 posterior 出发”必须解释为
对全部可行 `y0` 的 posterior **族**取全称量词；除非另行固定一条归档测量，否则不能选一个中心读数
代表全族。

## 时序与 Bellman 对象

仓库 `BoxSMF.advance(u, observation)` 先用 `u_k` 从 tick `k` 预测到 `k+1`，再用 tick `k+1`
观测求交。因此五步策略的时序为

\[
u_k=\pi_k(h_k),\quad x_{k+1}=f(x_k,u_k,w_k),\quad
y_{k+1}=C_{\gamma_{k+1}}x_{k+1}+v_{k+1},
\]

其中 `h_k` 只含截至 tick `k` 已到达的观测。tick 1--4 没有位置包；tick 5 才分成
`success`/`miss`，所以 tick-5 的位置值不能影响 `u_4`。令 `Post(I,u,γ,y)` 表示真实非线性像与
测量条带的求交，则有限时域回返域应递归定义为

\[
P_0^m=\mathcal T_m,\qquad
P_{j+1}^m=\{I:\exists u\in U,\ \forall(\gamma,y)\in Obs(m,I,u),
Post(I,u,\gamma,y)\in P_j^{m^+(\gamma)}\}.
\]

这正是“同一观测 history/fiber 共用输入”的量词，不是逐状态选择输入，也不是传播一个区间盒后
检查端点。Baras--Patel 1998 的 Section IV-A、Lemma 4、Remarks 8--10 和 Theorems 9--11
说明了为什么完整历史诱导的信息状态才是输出反馈动态博弈的充分状态，并且有限时域控制可以写成
该信息状态上的动态规划。

## 两个会改变结论的边界

1. **当前两条后继必须保留 mode，但终端族不能只保留两个 mode。** tick 5 成功后 miss age 为
   0，失败后为 1；二者不是同一个信息状态。局部可记为 `T_0/T_1`，但无限时域证书必须使用
   60-state 扩展中的 45 个 recurrent 标签并覆盖全部循环边。仅证五步物理状态回到 `X0` 也
   不等价于 posterior 回返。
2. **竖直切片只可作构造性子问题。** 在 `px=vx=phi=omega=0, wind_x=0, tau=0` 时真实 plant
   约化为
   `pz+=h*vz`, `vz+=h*(T-g-0.15*(vz-wz)*sqrt((vz-wz)^2+0.04))`。
   但 `tau=0` 是控制器选择，不是对任意六维控制器成立的扰动约束。因此竖直切片可用于构造一个
   竖直策略或发现该受限策略失败，不能单独证明完整六维输出反馈策略不存在。

## 准入结论

当前不应实现“单个 initial box 到单个 terminal box”的五步检查器：它会漏掉 tick-0 posterior
族、tick-5 两个 mode 后继以及 observation-fiber 共享输入，得到的数值结果不能作为递归可行性
证据。下一步应先给出 mode-indexed terminal information-family 的有限表示及包含判据；若该表示
不能可靠外包，则回退到完整 history tree，而不是把测量成功当作物理 reset。Run178 排重确认
该 mode-indexed family 的一般充分合同已在第 88 章给出；真正下一步是冻结固定复杂度表示
`Gamma` 与可靠 source-to-target 包含 oracle。

证据等级：`timing_and_quantifier_contract_from_source_plus_primary_full_text`。这不是可行性、不可能性、
终端不变性或硕士课题创新证明。
