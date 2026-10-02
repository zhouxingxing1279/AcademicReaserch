# Run 142 文献准入卡：竖直 causal product-fiber predecessor

日期：2026-10-02。仓库起点为 Run 141 本地提交 `2b02af0`，其 tree 与远端
`research/run141-vertical-causality-gap` 的 `cf2234c` 一致；远端 `main` 为 `1c49659`。
本轮问题是：固定 Run 136 的 15 个估计误差 zonotope 后，能否在可观的竖直中心误差
`d=(d_pz,d_vz)` 上构造非轴对齐、模态相关的因果 RCI 多集，并强制 mode 4、9 的
miss/success 分叉共享同一个当前推力修正。

## 1. 最近邻与本轮实际阅读

| 文献 | 本轮阅读范围 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Hempel, Kominek, Werner, *Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix*, CDC-ECC 2011, DOI `10.1109/CDC.2011.6160901`, [公开全文](https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1283.pdf) | **全文定向重读 Section III-A--C，Definition 2、Theorem 1、式 (3)--(10)，并复核 Section V 的限制** | 对每个 noisy output 与当前可测 scheduling 只选择一次输入；Theorem 1 用 Farkas 条件验证给定多面体，Section III-C 在线求满足 robustified constraints 的输入。论文明确没有直接计算 OFCI 多面体的算法。 | 同一 observation fiber 和未知后继分支必须共享输入；验证/在线输入计算已有理论，不是创新。其 scheduling 外生可测，不能直接替代本项目的 packet graph 和控制相关实际推力。 |
| Rungger, Tabuada, *Computing Robust Controlled Invariant Sets of Linear Systems*, IEEE TAC 2017, DOI `10.1109/TAC.2017.2672859`, [arXiv:1601.00416](https://arxiv.org/pdf/1601.00416) | **全文精读 pp.1--7：定义、式 (4)--(10)、Lemma 1、Theorem 1、Section 4 的 Pontryagin difference 与 projection 实例** | 以 `pre(R)={x: exists u, Ax+Bu+W subset R}` 做递减迭代；有限停机不一般成立；给出带约束放松的外近似和带 disturbance inflation 的内近似。 | predecessor 迭代本身已有；其状态反馈量词假定 `x` 可见。本轮只能把它用于可见 `d`，隐藏 `eta` 必须先在 fiber 上统一 robustify。 |
| Houska, Müller, Villanueva, *Polyhedral Control Design: Theory and Methods*, 2024, [arXiv:2412.13082](https://arxiv.org/pdf/2412.13082) | **全文定向阅读 Sections 3.3--3.6 与 Section 3.10 的 output-feedback 路由，重点 pp.12--16** | 总结 controllable/control-invariant/robust-control-tube 的 vertex/projection 与固定复杂度参数化；指出 output-feedback set dynamics 是独立文献线。 | 非轴对齐多面体、vertex input interpolation 和固定模板都不是贡献；本轮应报告证书类和保守化步骤。 |
| Artstein, Rakovic, *Set invariance under output feedback: a set-dynamics approach*, IJSS 2011, DOI `10.1080/00207720903513331` | **沿用 Run 140 对信息状态量词的全文精读，本轮仅复核其在 Houska 综述中的定位** | 一般历史输出反馈以 set-valued information state 为控制状态。 | 本轮固定 `E_eta^j x D_j` 是更保守的有限类；失败不能否定一般 history-dependent controller。 |

检索覆盖 `output-feedback controlled invariant polyhedra`、`information-state invariance`、
`robust predecessor iteration` 和 `polyhedral RCI synthesis`。至少两篇原始全文在本轮按
定义、定理、证明/算法与限制实际核查；不以摘要判断首次性。

## 2. 候选类、严格差异与强基线

冻结 product-fiber 候选

```math
S_j=E_\eta^j\times D_j,
```

其中 `E_eta^j` 是 Run 136 已认证的六维 zonotope，`D_j` 是本轮待求的二维凸多面体。
控制器完整观察 `d` 和 mode，不能观察 `eta`。竖直更新为

```math
\begin{aligned}
d^+&=A_d d+B\delta T &&\text{miss},\\
d^+&=A_d d+B\delta T+[1,L]^\top(q+n) &&\text{success},\\
q&=\eta_{p_z}+h\eta_{v_z},\quad n\in[-1/50,1/50].
\end{aligned}
```

对 success 边，用 Run 136 zonotope 的精确 support robustify `q+n`；对 mode 4、9 的两条
边，Fourier--Motzkin projection 必须消去同一个 `delta T`。源集合还要满足全部
`z` 和 `eta` 下的真值位置/速度域，输入满足 Run 138 correction box。

最强同条件基线有两个：

1. **因果 product-fiber predecessor：**共享 `delta T(d,j)`，是本轮可认证对象；
2. **隐藏状态乐观上界：**允许 `delta T(d,eta,j)`，仅用于量化因果代价和 Run 141
   negative control，不可作为控制器证书。

与文献的严格差异仅是当前四旋翼合同的实例化：15-mode packet graph、分叉前输入、
Run 136 zonotope support 与实际 correction box。predecessor、投影和 OFCI 量词均已有。

## 3. 证据义务与推翻条件

通过实现前必须满足：

- 所有数值由当前 config 和 Run 136 生成元以有理数重建；
- 当前 mode 的所有后继边共用一个投影变量；
- 每个迭代集合由精确有理数半空间交与投影得到，并删去冗余约束但不放大集合；
- 若有限达到固定点，逐边重新验证 robust image inclusion、source domain 和输入非空；
- 若只迭代有限步而未固定，则结果只是 outer predecessor sequence，不是 RCI；
- 若 product-fiber 类变空，只否定该类；不得升级为一般 output-feedback RCI 不存在。

候选被以下任一结果推翻：初始化切片 `d=0` 被删除；任一 mode 为空；mode 4/9 只有
分边不同输入才可行；集合不满足真值源域；或迭代未固定却被误报为 invariant。

## 4. 课题作用与准入结论

该问题直接决定 Run 136 估计证书能否进入 ancillary input/state tightening。若得到非空
固定点，下一步才有资格反推具有严格内点的 nominal input domain；若 product-fiber 类
为空，则必须转向保持 `eta-d` 相关性的 joint information-set 表示，而不是继续调多面体
法向。

**准入：通过“因果 product-fiber 基线与证书类判定”；不通过算法创新、完整六状态 RCI、
终端/递归可行性或降低保守性声明。**

