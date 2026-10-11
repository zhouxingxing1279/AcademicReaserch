# 94. Run157 救援后的 mode-9 共享分叉见证

## 1. 非平凡检查对象

Run157 在 edge `8->9` 上把 `J_14` 路径的真实速度半宽压回硬约束。到达扩展标签
`(9,15)` 后，当前 packet outcome 尚未知；控制器必须先基于同一个可见 `d=e-eta` 选择输入，
再同时覆盖

```math
(9,15)\xrightarrow{miss}(10,15),\qquad
(9,15)\xrightarrow{success}(0,10).
```

这才是 Hempel 式 output-fiber 量词在当前自动机中的第一次真实分叉，而不是 Run157 的
`8->9` 救援边。

## 2. exact shared policy

Run157 首次救援后的 mode-9 set 具有可见速度半宽

```math
h_{d_v}=\frac{70527869}{32000000}.
```

选取同一 centered affine policy

```math
\delta T=K_vd_v,\qquad K_p=0,qquad
K_v=-\frac{114428600}{70527869}.
```

则 robust input support 恰为 correction 上界

```math
h_u=\frac{572143}{160000}.
```

success 与 miss 对真实 tracking error 使用同一动力学和同一物理 residual，只在 estimator
更新及 measurement-noise primitive 上不同。因此两支的真实误差半宽完全相同：

```math
h_{e_p^+}=\frac{85072353058880561}{87379729200000000}
\approx0.973594<1,
```

```math
h_{e_v^+}=\frac{4751967529055069}{1747594584000000}
\approx2.719148<\frac{11}{4}.
```

estimator 部分不受 correction 影响；既有 full mode-9 envelope 的精确 facet certificate 已分别
证明 miss 像包含于 `E_10`、success 像包含于 `E_0`。当前 rescued set 是该 full envelope 的
子集，故两支 estimator target containment 继承成立。

## 3. 结论边界与方向纠正

本轮证明的是 **one-step shared success/miss state-input safety**：同一当前 affine policy 对
两种 packet outcome 都可执行且安全。它没有证明两支完整联合集合落入某个已冻结的 recurrent
target family；更没有证明后续所有历史使用一张一致策略。

因此“先建立 `(14,10)`、`(9,15)` 共同外包”并不是充分的下一步：在每个第二周期标签只有
单一 constituent 时，取凸包是平凡的。真正剩余的非平凡义务是把 success 后的集合分别并入
`(0,15)`、`(0,10)` 的多历史 target families，并证明后续逐边闭合。
