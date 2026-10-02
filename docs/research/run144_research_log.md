# Run 144：竖直 joint `(eta,e)` 三个关键一步 predecessor 非空

日期：2026-10-02。分支 `research/run144-vertical-joint-predecessor`。

## 仓库与基线

启动时读取 `docs/research/current_checkpoint.md` 及 Run 143 直接证书。刷新远端后确认最新
有效分支为 `origin/research/run143-joint-information-semantics=3fcaeab`，本地 Run 143
提交为 `bb48593`，两者 tree 同为 `3893f404fc78ba81993bb37c9c4ed9dd2b14348c`；
`origin/main=1c49659`。linked worktree 干净。实现前基线回归为 `verification/` 162/162、
`tests/` 39/39，合计 201/201。

## 文献与准入

精读 Houska 2023 *Intrinsic Separation Principles* Sections 4.4、6.1--6.7，尤其
Definition 4、Lemma 2、Theorem 3 与 Problems (24)/(27)/(29)：information ensemble、
extreme information-set control 及其 configuration-constrained polytope 凸近似已经覆盖
一般方法。重读 Hempel 等 2011 Section III-A--C 的 fiber 共享输入量词。另精读 2026
Kumar--Kothyari Sections 2.3--3、Definition 4、Theorem 5：其 zonotope-LP 同时求静态
output gain 与 state RCI，但系统只有 `y=Cx`、加性过程扰动，没有 measurement noise、
packet graph、observer split 或 actual-input dependent residual。

因此准入只允许把现有 output-feedback information-set 理论实例化到当前冻结合同，核查
三处关键一步 predecessor；不允许把 joint set、zonotope/LP 或 extreme-fiber control 声明
为创新，也不启动固定点求解。详见 `run144_literature_gate.md`。

## TDD 与实现

先新增7项测试。首次运行 7/7 因 `check_vertical_joint_predecessor` 缺失按预期失败；随后
实现最小 checker，7/7 GREEN。为避免把零维切片误报为正体积，又先新增 config-derived
tracking limits、精确 eta 投影面积和 joint dimension 断言；该测试先因字段缺失 RED，
再补实现后 7/7 GREEN。

检查器直接复用 Run 136 zonotope 生成元，但独立构造二维 exact H-polytope、逐 facet 支持
包含和 tracking-error 解析余量。候选为 `S_j=E_j x B_e`，不独立约束 `d=e-eta`；Run 143
违反旧 product `d` 限幅的 success 见证被显式验证仍属于 `S_0`。

## 核心结果

对 modes 4、9、14，集合

`C_j={eta in E_j, |d_p|<=1/5, |d_v|<=1/4, e=eta+d}`

均为四维正体积 convex set。统一策略 `deltaT=0` 对整个 observation box 有效，并在
nominal thrust 全区间 `[8.48089375,11.13910625] N` 上把 actual thrust 保持在同一区间。
由同一 actual thrust 导出的最大 residual 半宽为
`411370817/128000000`，同时用于 eta/e 后继。

逐边 exact support 证书通过 `4->5 miss`、`4->0 success`、`9->10 miss`、
`9->0 success`、`14->0 success`。mode 4/9 的两个未知后继在计算前共享同一个零输入。
最紧的 tracking target 余量出现在 mode 14，位置为 `14847853/48000000`，速度为
`22053067447/57600000000`，均严格正。

证据等级：**exact positive-volume inner certificate for three critical one-step
predecessors**。这不是 RCI、固定点、全六状态或 MPC recursive-feasibility 证书。

## 交付与验证

新增：

- `docs/learning/81_vertical_joint_one_step_predecessor.md`
- `docs/research/run144_literature_gate.md`
- `docs/research/run144_research_log.md`
- `verification/check_vertical_joint_predecessor.py`
- `verification/test_vertical_joint_predecessor.py`
- `results/theory_vertical_joint_predecessor_20261002/exact_checks.json`

独立代码复核没有发现 support 数学错误，但指出两项 Important 缺口：原测试只核对
residual 元数据、未锁定 eta facet support；artifact 也漏列三个间接执行依赖。修复采用
residual-sensitive facet 的精确余量断言（mode 14 为 `471323459/320`），并把
`check_mode_nestedness.py`、`check_mode_radius.py`、`check_intermittent_metric.py` 纳入逐文件
SHA-256；修复测试先有2项 RED，随后7/7 GREEN。

最终验证命令为：

- `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s verification -v`：169/169；
- `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v`：39/39；
- `python -m py_compile`（本轮 checker/test）、`python -m json.tool`、逐源文件 SHA-256
  重算及 `git diff --check`：全部通过。

合计 208/208。远端同步在最终提交后以目标 branch 的 SHA/tree 另行核验并在本轮简报报告；
本段不作自指式 commit hash 声明。

## 下一唯一问题

把当前 exact fiber robustification 扩展到全部15个 mode，执行 **一次** joint
descending predecessor sweep；输出每个 mode 保留的 observation projection、正体积内集
或空集证书。仅当全模态一步非空时，才启动固定点迭代。
