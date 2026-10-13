# Run180：mode-0 miss lifted-cell 的 exact oracle

启动基线：远端 `main=1c49659`；Run179 本地 `ca2eb37`、远端 `aaef469`，共同 tree
`f275cb8`。本轮研究分支为 `research/run180-mode0-miss-lifted-cell`。

本轮从 Run179 检查点出发，只检查 `0->1 miss`。仓库审计确认该边属于冻结的 15-mode/17-edge
合同；竖直联合更新、Run136 estimator projections、名义/校正推力分配和 actual-thrust residual
公式已有可执行原语，因而无需另造模型。

全文重读 Hempel--Kominek--Werner §II、§III-A--C、Definitions 1--2、Theorem 1、式(3)--(14)
和 Algorithm 1。其 noisy-output fiber 共享输入与逐 facet 验证直接覆盖本轮方法思想，所以本轮
不作创新声明；实现价值仅在于检验 Run179 的 lifted graph 接口能否连接真实配置。

冻结 source cell：Run136 mode-0 的 `(eta_p,eta_v)` 精确投影乘可见 box
`|d_p|<=1/5, |d_v|<=1/4`，并令 `e=eta+d`。冻结仿射 fiber policy `deltaT=0`。检查器保留
`r_z=(1043/500+81T/800)rho_z`，在 actual thrust 区间上求可靠上界，并把同一 residual
realization 同时送入 `eta+` 和 `e+`。target 使用 mode-1 estimator 的 6 个固定 facets 与
tracking box 的 4 个 normals。

10 个 normal 全部闭合；estimator 的两个位置 facets 为精确零余量，tracking 位置/速度分别有
严格正余量。输入、当前 source domain、edge incidence 同时通过。该结果是
`exact_one_edge_target_normal_support_certificate`：不是 45-state terminal family、RCI、递归
可行性或六自由度保证。

失败尝试：最初生成 artifact 时文档尚未写入，hash-bound writer 按设计以缺文件失败；补齐准入卡、
学习章和日志后重跑。没有以删除 hash 依赖规避该失败。

论文级主线仍未闭合。下一唯一问题是 mode 4 的同一 source cell/同一 affine policy 同时覆盖
`4->5 miss` 与 `4->0 success` 的全部 target normals、共享 residual 和 success noise；这是第一处
真实 packet outcome 分叉。
