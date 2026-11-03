# Run 150：translated fixed-shape return 的精确宽度阻塞

日期：2026-10-03。分支 `research/run150-translated-template-obstruction`。

## 1. 仓库接续与独立复核

启动时只读取 `current_checkpoint.md`，随后刷新远端 `main` 与全部 `research/run*` refs。
实际本地工作树已推进到 Run149 `f333cdf`，晚于聊天中的 Run145；远端最新有效分支是
Run147 `18a2b61`，其 tree 与本地 Run147 一致。Run148 `0f65ef3`、Run149 `f333cdf`
尚未在远端出现。

先按仓库根文档入口复验 Run149：定向6/6；`verification/` 201/201；`tests/` 39/39；
`compileall`、全部 JSON 解析及 `git diff --check` 均通过。命令行 push 因 HTTPS remote
没有用户名/凭据失败，本轮结束时改用 GitHub 连接同步并逐 tree 核对。

## 2. 文献准入

本轮重新精读 Houska 2023 pp.14--17 的 Sections 4.1--4.3、Theorem 1及证明，pp.23--25
的式(18)--(19)/Theorem 2，以及 pp.29--32 的 extreme information polytopes、Theorem 3
及证明。其 fixed `W` intrinsic separation 和 translation functions 已覆盖一般思路；
extreme information set 的共享控制/连续插值也不是本项目创新。

同时复核 Hempel 2011 的 fiber shared-input 全文笔记、Wehbeh--Kerrigan--Scaccia 2026 的
decision-dependent uncertainty GSIP 全文笔记，以及 Rungger--Tabuada 2017 对有限
predecessor 层证据等级的边界。准入只允许当前15模态竖直合同的 exact实例否证，不允许
声称新集合算法、一般 RCI 或闭环定理。详见 `run150_literature_gate.md`。

## 3. TDD 与实现

先新增6项行为测试，手工锁定：

- Run148 三个 exact convex-hull 分量及逐 miss/success 的列数；
- `4->0`、`9->0`、`14->0` 三个 `e_p` support 半宽与严格超量；
- arbitrary centers/current correction 不改变 directional width；
- mode 4/9 的 success/miss 使用同一当前输入，且 success 单边失败；
- 证据边界与 hash-bound artifact。

RED 阶段最初出现5项FAIL和1项由测试直接索引空字典造成的派生ERROR；先把测试改为观测
缺失行为后，6/6均因 checker 不存在而按预期FAIL。实现最小 checker 后，5项核心行为转绿；
artifact 测试因第87章、日志和归档尚未存在保持预期红灯。实现只用 `Fraction`、完整生成
矩阵线性像、共享原语列和 convex-hull support `max_m h_{J_m}`，没有浮点容差、采样或求解器。

## 4. 核心结果与证据等级

令 `C_j` 为 Run148 `C0` 在固定 Run136 global envelope 下经 `j` 次 miss 的零中心 shape。
任意 correction 的联合平移为 `(0,0,0,h deltaT)`，故不能改变 `e_p` width。

目标 `C0` 的 `e_p` 半宽为 `23312147/48000000`。三条 return image 半宽/严格超量为：

- mode 4：`51293581/72000000`，超 `32650721/144000000`；
- mode 9：`14038717/14400000`，超 `70450729/144000000`；
- mode 14：`12222431/9600000`，超 `4725001/6000000`。

因此任意 source/target centers 和 current correction 都不能使三条 success image 包含于
`C0+c0`；最早阻塞在 mode 4。mode 4/9 的 miss shape 本身按定义精确映到 `C_{j+1}`，但
success 单边已失败，故同一个 current input 更不可能同时服务未知分叉。

证据等级仅为 **exact `e_p` width obstruction for the Run148 translated fixed-shape
family**。不否定 history-conditioned information ensemble、scheduled decision-dependent
shape、完整六状态 RCI、terminal 或 MPC recursive feasibility。

## 5. 验证、交付与下一问题

首次完整回归发现Run146--149共4项artifact测试失败。分别在临时目录重建4份JSON，删除
唯一变化的`source_sha256/docs/literature/READ_PAPERS.md`字段后与归档逐字段比较，4/4
完全一致；因此只更新文献表散列，没有改写历史数值、集合或结论。修复后回归为：

- Run150定向：6/6通过；
- `verification/`：207/207通过，88.726秒；
- `tests/`：39/39通过，1.165秒。

另用不调用本轮checker的闭式 support 递推独立复算：对每个Run148分量直接计算
`h(e_p+(j+1)h e_v)`，再加入历史 residual 三角和
`gamma*h*j(j+1)/2`；3/3精确复现本轮三项半宽与超量。冻结后再次执行完整测试、Python
编译、全部JSON解析、artifact源码散列及`git diff --check`，并在聊天简报报告最终结果。

下一轮唯一问题：构造最小 return-age/history-conditioned intrinsic shape family，不再强制
三条 success 返回同一 `C0`；先用 exact support 检查有限周期 fixed point。该骨架不存在前，
不启动 scheduled-residual GSIP，因为 current correction/center 无法改变本轮的 `e_p` 阻塞。
