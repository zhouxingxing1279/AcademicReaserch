# Run175 文献准入卡：受控回返量词纠错

## 最近邻与判断

| 工作 | 本轮阅读 | 关键边界 |
|---|---|---|
| Hassaan–Shen–Yong 2021 | 开放全文重读 Problem 1、§3、Theorems 3.2/3.4 | 固定长度缺测语言下联合合成path-dependent控制器/估计器，保证有限时域equalized recovery。 |
| Wintenberg–Ozay 2020 | 开放全文核查 Definition 2.1及N-step recurrence | 回返命题要求存在控制器，对全部扰动/模式实现N步回返。 |
| Scott等 2016 | 复核§3.1 generalized intersection | 测量相交不改变plant；但不决定控制器能否主动回返。 |

Run174使用最大推力轨迹，只证明存在一个允许输入会离开初始盒。受控回返的正确量词是存在因果
策略，使所有允许扰动和缺测路径满足约束并回到目标集；控制输入不能和风/噪声一起作全称量化。

**准入通过证据等级纠错，不通过新的反例或算法声明。** 在写周期tube代码前，必须先冻结可实现
的output-feedback策略参数化及共享观测fiber控制量词。
