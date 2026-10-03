# Run 149：控制平移与推力相关余项的形状分离

日期：2026-10-03。分支 `research/run149-control-translation-split`。

## 1. 仓库接续与优先修复

刷新远端后，发现本地工作树已超过聊天检查点：Run146 远端完成 second sweep，Run147
远端完成 correlated seed，本地 Run148 `390f035` 完成三路径 convex template，但有一份
未提交的语义收紧测试。该测试稳定复现4项失败，显示旧 checker 把零修正 image 过强地
称为 policy-independent 必要 target，并把连续 perspective selector 含混地描述成保持路径
排他性。

先完成系统化修复并提交 `0f65ef3`：显式记录先行 correction 全零、二维 visible offset、
连续 selector 的分数混合 witness，并把证据降级为 fixed-zero-correction baseline。数值
支持、rank和约束包含均未改变。随后才建立本轮分支。

## 2. 文献准入与方向判断

本轮重读 Houska 2023 Sections 3.5、4.2--4.3、5.3--5.4、Theorem 1及证明、式(18)--(20)，
复核 Sections 6.5--6.7；重读 Hempel--Kominek--Werner 2011 Section III-A--C、Definition 2、
Theorem 1、式(3)--(12)；重读 Wehbeh--Kerrigan--Scaccia 2026 Introduction、Section II、
Assumption 1、Theorem 1/Remark 1、Section IV Assumption 2 与 Theorem 3。

准入结论：固定 `W` 下的 shape/translation separation 已由 Houska 一般证明覆盖；同一 fiber
共享控制由 Hempel 覆盖；control-dependent uncertainty 的 GSIP 建模由 Wehbeh 等覆盖。
本轮只准入当前冻结竖直合同的 exact interface certificate，不作算法或 RCI 创新声明。

## 3. TDD 与实现

先新增6项行为测试，使用手算有理数常量锁定：

- miss/success 两类边的独立 `eta,d,e` 更新与 `e+=eta++d+`；
- 固定绝对余项时，两个 correction 仅产生 `(0,h Delta deltaT)` 中心平移；
- scheduled residual 的共享联合生成元随实际推力严格变化，但在 `d=e-eta` 中抵消；
- Run136 global residual 列精确等于最大实际推力端点并覆盖完整区间；
- 证据边界与 hash-bound artifact。

RED 阶段6/6按预期失败，因为 checker 尚不存在。实现最小 exact-rational checker 后，5项
核心行为测试转绿；artifact 测试因第86章、日志和归档尚不存在保持预期失败。实现没有使用
浮点容差、采样成员检查或优化器成功作为证明。

## 4. 核心结果与证据等级

固定绝对余项 realization 时，miss/success 都满足

`Delta eta+=(0,0)`，`Delta e+=Delta d+=(0,h Delta deltaT)`。

因此使用 Run136 的固定 global envelope 时，correction 只改变中心；第85章 `C0` 的生成元
形状可作为 policy-independent 中心化代表，但 `C0` 的零中心本身不是必要 target。

保留 `r_z(T)` 时，实际推力从 `4.905 N` 到 `14.715 N` 使一步共享 residual 生成元从
`413221/8000000` 增至 `572143/8000000`，严格增加 `79461/4000000`。所以 scheduled
分支同时改变中心和联合形状，属于 decision-dependent robust containment；不能直接套用
固定 `W` intrinsic-separation 定理。

证据等级：**exact vertical control-translation and residual-shape split**。不是 RCI、一般
output-feedback 综合、完整六状态或 MPC recursive-feasibility 证明。

## 5. 验证、交付与下一问题

新增 checker、6项测试、第86章、文献准入卡、日志和 exact artifact；更新文献表、验证
索引、自动研究日志与短检查点。从仓库根目录运行 `python -m unittest discover -s
verification -v`，全量回归为 201/201 通过；`tests/` 为 39/39 通过；`python -m
compileall -q verification tests`、全部
`results/**/*.json` 的 `jq empty` 解析及 `git diff --check` 均返回零。文献表更新使 Run146--
Run148 三份旧 artifact 的单个文献表散列变化；去掉该散列字段后，新旧 JSON 无差异，故只
重生成散列而没有改写历史数值结论。最终提交前再次运行同一完整回归和静态检查。

一次从 `verification/` 子目录启动全量 discovery，因 Run122--129 的历史测试按仓库根目录
导入 `verification` 包而产生20项派生失败；改用上述仓库根入口后全部通过。本轮新 checker
另补了脚本入口与包入口双路径导入，定向两种入口均通过，未把错误启动方式计作数值失败。

下一轮唯一问题：采用固定 Run136 global envelope，把第85章的中心化形状改写成
`C0+c_0`，对 modes 4/9 的未知分叉和 mode14 return 做带可见中心变量的 exact shared-input
containment。若该 fixed-shape translation 类失败，只否定该类，再判断 scheduled GSIP 的
额外 tightening 是否值得其计算与证明成本。
