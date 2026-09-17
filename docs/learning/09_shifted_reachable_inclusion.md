# C2-G/S：跨时刻可达集包含与固定模板接口

日期：2026-09-17。承接 [08 约束 zonotope 接口](08_constrained_zonotope_interface.md)。

**本轮闭合了一个受限但关键的义务：在绝对状态坐标中，若新后验包含于旧时刻对实际后继的一步预测、沿用旧 MPC 解的移位控制尾部，并且逐级扰动集合嵌套，则新移位候选的仿射可达集包含于旧预测的对应层。中心改变已包含在绝对集合比较中，位置缺测分支定义为恒等更新。该结果支持继承非终端收紧约束；完整 MPC 递归可行性仍因控制侧 tube、终端鲁棒不变集和末端追加控制律缺失而阻断。**

本轮不训练 RL，不声称新优化器解与旧最优解嵌套，也不从近期扰动样本推断未来扰动集合缩小。

## 1. 为什么必须比较绝对集合

估计器通常保存 $X=c+E$。若旧预测为 $X^o=c_o+E_o$，新后验为 $X^n=c_n+E_n$，半径或生成元缩小并不足以推出包含。准确条件是

```math
X^n\subseteq X^o
\quad\Longleftrightarrow\quad
d^\top(c_n-c_o)+h_{E_n}(d)\le h_{E_o}(d),\quad\forall d.
```

对轴对齐盒，第 $r$ 个坐标的准确包含余量为

```math
m_r=r^o_r-|c^n_r-c^o_r|-r^n_r.
```

全部 $m_r\ge0$ 才有包含。验证脚本中的一维反例取旧集合 $[-1,1]$、新集合 $[1/2,3/2]$；新半径 $1/2<1$，但中心位移为 1，包含余量为 $-1/2$。因此 `radius contraction` 与 `absolute-set contraction` 必须是两个接口。

CZ 的 `recenter` 只改变误差坐标：若 $E=X-\hat x$ 且观测器中心改变 $\Delta$，则 $E^+=X-(\hat x+\Delta)=E-\Delta$。它不改变绝对集合 $X$，也不能凭此制造绝对集合收缩。

## 2. 测量与缺测合同

设旧时刻对实际后继模式的一步预测为 $P^o_{1|k-1}$。位置包到达时，可靠测量集合为 $M_k$，后验为

```math
X_{k|k}=P^o_{1|k-1}\cap M_k\subseteq P^o_{1|k-1}.
```

位置包未到达时，$X_{k|k}=P^o_{1|k-1}$：缺测是恒等更新，不是假设性的收缩。若有限窗口重算出另一个可靠外包 $B_k$，控制接口应采用

```math
X_{k|k}=B_k\cap P^o_{1|k-1},
```

或保留两者为独立证明约束。只采用可能更宽的 $B_k$ 会失去跨时刻包含，即使 $B_k$ 本身仍可靠。

## 3. 定理：固定移位尾部下的可达集单调性

考虑阶段相关仿射集合模型

```math
x^+=F_jx+B_ju+W_j.
```

旧时刻已经生成实际后继之后的参考集合 $P^o_{1|k-1}$，以及控制尾部 $u^o_{1|k-1},u^o_{2|k-1},\ldots$。新时刻不使用重新优化后的输入作包含证明，而定义参考候选

```math
u^s_{j|k}=u^o_{j+1|k-1}.
```

### 定理 1（移位可达集包含）

对 $i=0,\ldots,N-1$，假设：

1. $X_{k|k}\subseteq P^o_{1|k-1}$；
2. 新旧比较采用相同的移位控制尾部；
3. $W^n_{j|k}\subseteq W^o_{j+1|k-1}$；
4. 两次计算使用相同的 $F_j,B_j$，或已证明新映射的集合值像包含于旧映射的对应外包。

则

```math
\boxed{R^s_{i|k}\subseteq P^o_{i+1|k-1}}.
```

**证明。** $i=0$ 即假设 1。若结论对 $i$ 成立，由仿射映射保持集合包含、相同输入只产生相同平移、Minkowski 和的单调性，以及假设 3，

```math
\begin{aligned}
R^s_{i+1|k}
&=F_iR^s_{i|k}\oplus\{B_iu^s_{i|k}\}\oplus W^n_{i|k}\\
&\subseteq F_iP^o_{i+1|k-1}
\oplus\{B_iu^o_{i+1|k-1}\}\oplus W^o_{i+1|k-1}\\
&=P^o_{i+2|k-1}.
\end{aligned}
```

归纳完成。这里比较绝对状态集合，所以估计中心变化已由假设 1 处理。□

### 3.1 间歇模式扩展

若未来映射依赖观测模式边，每条从新模式出发的允许路径都可在前面补上已经发生的实际边，成为旧时刻的一条允许路径。对每对匹配路径应用定理 1，再对路径取并，得到

```math
\bigcup_{\pi\in\Pi_i(j_k)}R^s_{i|k}(\pi)
\subseteq
\bigcup_{\bar\pi\in\Pi_{i+1}(j_{k-1})}P^o_{i+1|k-1}(\bar\pi).
```

这要求旧预测保留所有允许后继，或其外包覆盖这些路径；不能只保留“最可能收到位置包”的分支。当前合同位置机会每 5 tick 一次、最多连续缺失 2 次。本轮数值核查分别覆盖实际位置成功和实际位置缺失两个后继；一般路径前缀关系来自上述解析证明，不来自 25 步枚举。

## 4. 三个必要反例

1. **重新优化控制：**一维 $x^+=x+u$，初始集合均为 $\{0\}$，旧移位输入为 0，新优化输入为 2。新后继 $\{2\}$ 不包含于旧后继 $\{0\}$。递归可行性应证明旧解的 shifted candidate，而非任意新 optimum 的 tube 嵌套。
2. **扰动扩大：**一维 $x^+=x+w$，旧扰动 $[-1,1]$，新扰动 $[-2,2]$。即使初始集合和控制相同，新后继也不包含于旧后继。逐时 adversarial 扰动不能依据近期样本安全缩小；固定未知参数的可行参数集或另有覆盖保证的验证器才可提供嵌套。
3. **忽略中心：**第 1 节反例中半径从 1 降至 $1/2$，集合仍越出旧预测。包含测试必须使用绝对集合支持或等价的“中心位移 + 误差支持”。

## 5. 与固定模板和 CZ 的连接

取固定方向矩阵 $H$，定义 $P_H(b)=\{x:Hx\le b\}$。设定理 1 已证明真实新可达集 $R\subseteq P_H(b^o)$；独立验证器给出

```math
\beta_r\ge h_R(H_r^\top),\qquad b^n_r=\min\{\beta_r,b^o_r\}.
```

因为真实支持同时不超过两个上界，

```math
\boxed{R\subseteq P_H(b^n)\subseteq P_H(b^o)}.
```

`min` 安全的前提是 $R$ 同时包含于验证器上界和旧预测模板；若定理 1 未成立，直接取 `min` 可能裁掉真实状态。

该结果没有证明任意 CZ 降阶保持旧预测包含。安全接口可让 CZ 负责精确预测、测量求交和支持证书，让固定模板负责 MPC 可见的有限方向上界。如何把模板多面体转换成固定大小 CZ、同时保持双侧包含和 20 ms 预算，仍是表示层任务。

## 6. 六维有理数核查

验证器：[check_shifted_reachable_inclusion.py](../../verification/check_shifted_reachable_inclusion.py)；测试：[test_shifted_reachable_inclusion.py](../../verification/test_shifted_reachable_inclusion.py)；结果：[exact_checks.json](../../results/theory_shifted_reachable_20260917/exact_checks.json)。

核查冻结 `planar_baseline.json` 的状态次序、$h=1/50$、$g=981/100$、$I=1/50$、horizon 25、位置机会周期 5、最多连续缺失 2 次，以及 08 的全域仿射余项 $D_x,D_z$。仿射输入坐标使用 $(t,\tau)$，其中 $t=T-g$。

| 实际后继 | 核查层数（含初值） | 最小坐标包含余量 | 结果 |
|---|---:|---:|---|
| 位置成功 | 26 | $1/200$ | 通过 |
| 位置缺失 | 26 | $0$ | 通过（等号允许） |

全部判定使用 `Fraction`；没有以浮点容差决定包含。三个反例分别确认改变控制、扩大扰动和忽略中心位移会使合同失败。该试验不是一般 CZ 包含算法或非线性闭环证明；它只机械核对定理在当前六维仿射外包参数下的一个非零中心实例。

复现：

```bash
python -m unittest discover -s verification -p test_shifted_reachable_inclusion.py -v
python verification/check_shifted_reachable_inclusion.py \
  --output /tmp/shifted_reachable_exact_checks.json
```

输出路径须不存在。

## 7. 对递归可行性的准确结论

定理 1 加固定模板夹逼足以说明：对旧解的 shifted candidate，若某个非终端 tightened constraint 对旧预测集合成立，则在其余 nominal 量不变时，新集合不会使该约束更难满足。

完整递归可行性还需要：合格的 ancillary feedback 和控制侧误差 tube；状态/输入收紧读取的方向及注入界；非线性余项源域的逐步有效性；horizon 末端追加控制律；对全部允许观测模式闭合且对不确定界向下闭合的终端鲁棒不变集；以及初始 MPC 可行性。

仓库配置中的 `mpc.K`、`mpc.L_by_mode` 和 `mpc.terminal_certificate` 仍为空。因此当前门状态是：

```math
\boxed{\text{shifted reachable-set gate: PASS}}
```

```math
\boxed{\text{full recursive-feasibility gate: BLOCKED}}
```

下一步不训练 RL。先从状态/输入约束和候选反馈传播中导出控制器实际读取的 $H$，检查固定模板在整个 horizon 内是否给出非空收紧；随后才可能构造终端集合并完成条件 Theorem D。
