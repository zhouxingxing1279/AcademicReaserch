# Run165 文献准入卡：极端可见fiber的15-tick安全性

## 最近邻核查

| 工作 | 本轮阅读范围 | 与本轮问题的关系 |
|---|---|---|
| Yang & Ozay, *Safety Control Synthesis for Systems with Missing Measurements* (2021) | **全文重读** Sections 3--4、Definition 3、Propositions 2--5 | 缺测串开始前的因果控制承诺必须覆盖允许串的每个扰动和中间状态；极端可见fiber也不能因概率小而删除。 |
| Hempel, Kominek, Werner, *Output-feedback controlled-invariant sets…* (2011) | 重读既有全文记录的 Section III-A--C、Definition 2、Theorem 1 | 同一输出fiber共享一个可见输出相关输入，并覆盖fiber全部隐藏状态；本轮允许更乐观的全状态反馈，故反例更强。 |
| Houska, Müller, Villanueva, *Polyhedral Control Design* (2025) | 重读既有全文记录的 Sections 3.5--3.6、3.10 | 多面体RCI、robust tube与vertex control已有完整基线；单个可达fiber反例不构成集合综合创新。 |
| Scott et al., *Constrained zonotopes* (2016) | 复核Run164精读的 Sections 2.2、3.1--3.2 | 精确等式切片已知；本轮只使用极端support face退化后的实例结构。 |

## 差异、最强基线与推翻条件

本轮检查Run164留下的完整安全问题，不再使用“整体J14宽度”。最强比较允许控制器知道完整真实状态
和过去扰动，并每拍选择任意满足盒约束的输入。若连此乐观权限都能保证极端fiber的14次miss路径，
才值得继续做实际output-feedback综合。

反例会被以下任一事实推翻：极端 `d_p` 不可由J14生成元盒达到；该fiber初始方向support不超过1；
未来正残差小于当前global bound；或物理输入权限大于配置盒。检查器必须分别给出这些量的精确证书。

## 判断

**通过项目特定的可达fiber反例；不通过控制器实现。** 这是对Run164“宽度门槛通过”的必要补充：
半宽缩小不代表绝对中心可补偿。若极端fiber在乐观控制权限下仍失败，则当前15-tick合同应停止继续
调gain，转向可证明改变seed中心范围、future residual或执行器权限的合同设计。
