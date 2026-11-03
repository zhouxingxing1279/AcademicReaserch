# Run168 文献准入卡：15-tick future residual 物理分解

## 最近邻核查

| 工作 | 本轮阅读层级 | 已解决内容与边界 |
|---|---|---|
| Do, Prodan, *Tube MPC via flatness for multicopter trajectory tracking* (ECC 2024) | **开放全文精读** §§II-A、III-A--B，式(18)--(25) | 把多旋翼跟踪误差写成有界加性扰动系统，以 `W` 构造 mRPI 集 `Z` 并作状态/输入收紧；明确要求 `W` 足够可控，使收紧后约束非空。`W` 是先验固定集合，未给出由在线信息集缩小气动余项的证明。 |
| Hu, Bujarbaruah, Zhang, Borrelli, *Real-Time Tube MPC Applied to a 10-State Quadrotor Model* (ACC 2018) | **开放全文精读** Theorem 1、式(8)、Lemma 1 | 在当前椭球tube的全部状态与扰动上用 `Omega_n(q,Q)` 外包非线性余项，并由RFIT条件保证tube包含。这是本轮最强同条件方法基线：局部界必须覆盖整个预测tube，不能只用当前后验样本。 |
| Lu, Cannon, Koksal-Rivet, *Robust adaptive MPC: Performance and parameter estimation* (2021) | 复核Run166全文精读记录 | 可靠集合更新与旧解移位/递归可行是分开的义务；当前后验收缩不能直接充当未来扰动收缩。 |

## 严格差异、基线与推翻条件

本轮不提出新tube算法，只审计仓库冻结合同中的竖直余项来源。强基线是Hu等的tube-dependent
nonlinearity bounder：任何局部气动缩放都必须对15个未来tick、全部信息一致状态/风/控制成立，
并与旧计划移位兼容。Do--Prodan的固定`W`是当前全局包络的直接基线。

命题若满足任一条件即被推翻：(i) benchmark真值含未计入的积分余项；(ii) 外部过程半宽非零；
(iii) 当前`r_z`不是`1043/500+(81/800)T`；(iv) 即使保留`1043/500`，删除全部姿态--推力项
已能达到Run166的绝对阈值。

## 判断

**通过合同分解与路线否证；不通过新控制算法声明。** 本轮允许实现精确审计器，判断仅否定
“只缩小姿态--推力线性化项”的路线。局部未来气动tube界仍未决，且在得到全预测期包含证书前
不得声称递归可行或降低保守性。
