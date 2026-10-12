# Run167 文献准入卡：测量相交不能保证全局可见范围阈值

## 最近邻核查

| 工作 | 本轮阅读层级 | 已解决内容与边界 |
|---|---|---|
| Scott, Raimondo, Marseglia, Braatz, *Constrained zonotopes: A new tool for set-based estimation and fault detection* (2016), DOI `10.1016/j.automatica.2016.02.036` | **开放全文精读** §2 Definition 2，§3.1 Proposition 1及证明，§5式(31)--(33) | bounded-error状态集是预测集与给定观测逆像的generalized intersection；CZ可精确做该相交，降阶只能取保守外包。它不保证所有允许观测对应的创新都落入任意预设小区间。 |
| Alamo, Bravo, Camacho, *Guaranteed state estimation by zonotopes* (2005), DOI `10.1016/j.automatica.2004.12.008` | 正式摘要、问题设定及既有可访问正文片段复核；**非本轮全文精读** | 用zonotope外包含真值的测量一致状态集；不能为满足控制阈值而删除合法真值。 |
| Lu, Cannon, Koksal-Rivet, *Robust adaptive MPC: Performance and parameter estimation* (2021), DOI `10.1002/rnc.5175` | 复核Run166已精读的集合包含/旧解移位记录 | 集合更新的可靠性和控制递归可行是不同证明义务；当前状态后验不能充当未来扰动保证。 |

## 差异、基线与推翻条件

本轮不是提出SMF更新，而是审计项目特定的Run166必要阈值。强基线是Scott等的精确generalized
intersection：允许保留全部测量相关性。命题若满足以下任一条件即被推翻：(i) 强制return并非
`d_p^+=q+n_p`；(ii) `J14`的`q`支持小于等于阈值；(iii) `q`极值或`n_p=0`不在允许集合中。

## 判断

**通过精确反例与方向终止；不通过新算法声明。** 即使用精确CZ相交和零测量噪声，合法真值仍可
产生超过阈值的可见偏差。因此不实现measurement-only gate，停止seed/measurement支线；后续只
研究改变`J14`形成机制或未来物理余项合同的可认证方案。
