# Run166 文献准入卡：中心范围三因素合同

## 最近邻核查

| 工作 | 本轮阅读层级 | 已解决内容与边界 |
|---|---|---|
| Lu, Cannon, Koksal-Rivet, *Robust adaptive MPC: Performance and parameter estimation* (2021), DOI `10.1002/rnc.5175` | **开放全文精读** §§3.1--3.2、Lemma 1、§4.1 Proposition 1及证明，复核§6.1比较 | 固定复杂度参数集保持真值包含/嵌套，tube对全参数集与扰动鲁棒化；递归可行性还依赖旧解移位和终端条件。其对象是参数集，不允许把状态posterior缩小当作未来扰动缩小。 |
| Köhler et al., *A robust adaptive MPC framework for nonlinear uncertain systems* (2021), DOI `10.1002/rnc.5147` | 正文摘要与既有全文记录的monotonicity/non-increasing条件复核 | 给出在线参数界与tube更新相容的一般框架；本轮只建立冻结路径必要合同，不覆盖其完整RAMPC。 |
| Mayne et al., *Robust output feedback MPC of constrained linear systems* (2006), DOI `10.1016/j.automatica.2006.03.005` | 摘要与既有全文记录复核 | 固定估计误差不变集、tube收紧及终端闭合是强基线；未提供当前按可见fiber参数化的合同阈值。 |
| Houska, *Intrinsic separation principles* (2026), DOI `10.1016/j.automatica.2025.112661` | 复核既有全文§§4.2--4.3、6.4--6.5/Theorem 3记录 | 一般information-set feedback和极端信息集控制已覆盖；单条支持LP及其对偶不是方法创新。 |

## 差异、最强基线与推翻条件

本轮严格区分当前状态可见范围`r`、未来过程余项尺度`beta`和物理输入权限`gamma`。最强比较仍
允许全状态因果反馈；目标只是给Run165反例的最小合同边界，不声称递归可行。若支持LP在所需阈值
附近不是所写仿射支、原始与对偶不相等，或任一单因素边界代回不能达到1，则命题被推翻。

## 判断

**通过项目特定的精确合同接口；不通过算法创新或控制器实现声明。** 式(102.1)改变可初始化性、
扰动保证或执行器物理权限，能直接决定是否值得恢复终端/移位综合；但它仍只是必要条件。
