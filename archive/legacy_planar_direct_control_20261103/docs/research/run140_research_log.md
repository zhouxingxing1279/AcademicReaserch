# Run 140：冻结 hover partial-information ancillary 合同

日期：2026-10-02。分支 `research/run140-hover-partial-information-contract`。

## 仓库与基线

只读取 Run 139 短检查点、Run 139 gate/log、第 71、73--76 章、当前配置、Run 136
artifact 及对应验证器。远端刷新后确认 `origin/main=1c49659`；Run 139 本地
`8116839` 与远端 `50f3da1` tree 同为 `d2e010f`。隔离 worktree 起点干净。修改前
`verification` 131/131、`tests` 39/39，共 170/170 通过。

聊天摘要曾给出“先做二维因果反例”，但仓库权威检查点的唯一问题是先让真实 15-mode
合同 ready；本轮按仓库纠正，不用小反例替代合同。

## 文献与准入

全文精读 Hempel--Kominek--Werner 2011 Sections II--III、Definitions 1--2、Theorem 1
及控制计算：其 output-feedback CI 对同一噪声输出一致的全部状态选择同一个输入。全文
定向精读 Baras--Patel 1998 Section IV-A--B、Lemma 4、Theorems 9--11、15--16：一般
output-feedback robust game 的充分统计量是 observation history 诱导的信息状态。另核查
Yang--Ozay 2020/2021 与 Ning 2026 摘要；前两份作者 PDF 正文抽取失败，未引用定理。

准入结论：量词/automaton 不是创新；允许把当前物理与估计模型实例化为保守有限合同，
不允许综合 RCI 或作首次性声明。详见 `run140_literature_gate.md`。

## 核心合同

冻结 policy 观察量 `(d,mode,z,nominal_input)`，隐藏 `eta`；控制先于未知下一边和原语。
nominal probe box 以 `(0,2,0,0,0,0)` 为内点，半宽为
`(1/2,1/2,1/4,1/4,1/20,1/4)`。模式图为 14 条 miss 与三条 success 边。

同一实际推力 `T=bar T+delta T` 进入物理后继与余项半宽。实现从同一当前
`x=z+d+eta`、`hat x=z+d` 及同一 `(r_x,r_z,n_next)` 生成 `x+`,`hat x+`,`z+`，再取
`eta+=x+-hat x+`,`d+=hat x+-z+`。因此没有独立复制过程/测量原语，且
`eta++d+=e+` 精确成立。

## TDD 与验证

RED 阶段出现五项预期失败：真实配置仍 blocked；独立 `d+` 扰动副本未被拒绝；新
checker 缺失导致 success、miss 和 17-edge 三项失败。第二轮 RED 证明把 actual-thrust
余项公式替换为全局常数不会被旧 gate 发现。最小实现后 11/11 定向测试通过。

新增 checker/测试及 artifact 只证明问题合同可执行。没有 policy 系数、RCI 或 solver
结果，不把 17 条数值 edge probe 冒充集合不变性证明。

完整回归第一次运行时，`verification` 136/136 通过，但 `tests` 的 affine/joint envelope
载入稳定复现两项 `INVALID_MODEL_OR_CONFIG_HASH`。根因是新增纯控制合同改变了整份配置
digest；用仓库原始 build scripts 在临时目录重建后逐字段比较，两个 envelope 都只有
`config_sha256` 变化，model 与 compressed leaves 的文件 SHA 及数组逐元素完全相同。
据此更新两个 envelope 的配置哈希及 manifest 中对应 artifact SHA；目标测试 5/5 通过。

首版全仓回归：`verification` 136/136（98.556 s），`tests` 39/39（1.940 s），合计
175/175。Python 编译、JSON 解析、Run 140 artifact 源码哈希及 `git diff --check` 均通过。

## 独立审查后的补强

独立代码审查未发现 successor 公式或因果时序错误，但指出首版 gate 对 observation-fiber
布尔量、安全约束与原语 incidence 没有 fail closed，首版 exact checker 的 17 边测试也
主要是按定义的分裂恒等式。随后先新增 mutation/boundary 测试并观察预期 RED，再完成：

1. 只接受冻结 policy class 且强制同一 observation fiber 使用同一输入；
2. 验证 `x=z+eta+d`、source-domain、actual-input、actuator-box 与 Run136 投影约束，并
   精确检查 nominal/correction Minkowski 分配不越界，且三组输入区间有限、有序；
3. 用单个 `xi_next_shared_once` 归一化向量和 miss/success edge incidence 取代两组同名
   primitive IDs；
4. 独立恢复 `w_x=r_x+(g-T)phi` 与 Run136 `eta+` 方程，在推力、姿态及余项端点验证
   Run136 半宽；同时校验 checker 常数与配置一致。

这次配置语义补强再次只改变旧 affine/joint envelope 的 canonical config digest；用原始
脚本临时重建确认 model、leaves 数组逐元素不变，仅更新 digest 及 manifest artifact hash。
审查修复后的最终全仓回归为 `verification` 143/143（104.022 s）、`tests` 39/39
（1.967 s），合计 182/182；定向 18/18、Python 编译、JSON 解析、Run140 source hash、
两个 envelope manifest hash 及 `git diff --check` 全部通过。

## 主线总审视

Run 136 已闭合 frozen observer inclusion 的估计误差 multi-set；Run 137--138 给出输入
权限必要门槛；Run 139--140 现已把 partial-information 控制问题从语义缺口推进到 ready。
论文级主线仍缺 causal ancillary RCI、严格内点 nominal allocation、terminal/shift、同预算
优势和四旋翼闭环。下一轮应先做 vertical projection 的 causal/full-state 强比较，避免直接
进入难以解释的 12 维非凸搜索。

## 下一唯一问题

对 vertical `(eta_pz,eta_vz,d_pz,d_vz)` 投影，在 15-mode graph 和当前 actual-thrust
residual/correction 权限下比较 observation-fiber PWA RCI 与可读取 `eta` 的 full-state
vertex RCI；给出认证可行候选或 policy/certificate-class 特定反证。
