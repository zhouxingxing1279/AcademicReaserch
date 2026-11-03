# Run181：mode-4 未知分叉的 exact lifted-cell oracle

启动基线：远端 `main=1c49659`；最新实际成果分支
`research/run180-mode0-miss-lifted-cell@9f8d46a`。本轮从后者创建
`research/run181-mode4-unknown-branch-lifted-cell`，没有从落后的 `main` 重做历史工作。

仓库短检查点把唯一问题定为：冻结 mode-4 的同一 source cell 与同一仿射 fiber policy，同时
认证 `4->5 miss` 和 `4->0 success`。定向核查 Run136 cycle-lifted zonotope、Run144 joint
predecessor、配置的 17-edge graph 及 Run180 checker 后，确认已有代码只给出三种关键 mode 的
内前驱存在性，没有留下两支联合 `(eta,e)` 全部 target-normal 的逐行 artifact。

本轮重新下载并精读 Hempel--Kominek--Werner 2011 的 §III-A--C、Definition 2、Theorem 1、
式(3)--(14)和 Algorithm 1。其 noisy-output fiber 共用输入与逐 facet 验证已经覆盖方法思想；
Robbins 2026 的 CZ 在线收紧只能取得正式摘要，未用来作定理或首次性判断。准入结论因此是：
允许补齐可靠证书，不允许声称新算法。

按测试先行加入五组回归。RED 阶段因 checker/module 不存在得到 5 个预期失败；实现后发现
mode-5 estimator 并非 Run180 的 6 facets，而是 14 facets，修正了测试中错误的 10-row 预期，
没有删减实际法向。最终 checker 对 miss 的 18 行与 success 的 8 行逐项解析求支持，并显式
记录：单一 `deltaT=0` 在 edge label 前选择；actual-thrust residual law 对两支相同且在每支内
共享到 `eta/e`；success 噪声进入 estimator、在 tracking error 中抵消。

结果为 26/26 target normals 闭合。两支最小总余量均为零，来源是 estimator 的精确位置边界；
tracking 位置/速度余量分别至少为 `4719857/7200000` 和
`63247363447/57600000000`。source domain 与输入盒亦通过。证据等级限定为
`exact_two_edge_unknown_label_target_normal_support_certificate`：不是 RCI、terminal family、
递归可行性或六自由度保证。

失败/纠正记录：第一版测试沿用 Run180 的 10-row 直觉，把 mode-5 target 错计为 6 个 estimator
facets；真实固定投影有 14 facets。检查器返回 18 行后，回看 exact polygon 的不同生成元方向，
将测试修正为 18，而不是压缩/删除 facets 以迎合预期。

独立代码审阅随后指出初版把“共享 residual / noise 抵消”和“source 正体积”写成了弱断言。
先新增失败回归，再把 estimator/tracking 支持统一改由同一组联合 `(eta^+,e^+)` primitive columns
计算；逐列验证 `rho_z` 在 `eta/e` 的系数相同、success `n` 在 `e` 的系数为零。另计算 mode-4
estimator 投影精确面积 `41105550110953/240000000000000`，并与两个 `d` 半宽共同纳入 pass 条件。

下一唯一问题：固定在线 cell/normal 预算，尝试把 mode-0 与 mode-4 局部证书扩成覆盖初始化可达
observation domain 的有限 cell family，并证明重叠处策略选择单值、输入可行且逐边闭合；若需要
随 history 无界增长的细分，则停止 lifted-cell 表示路线。
