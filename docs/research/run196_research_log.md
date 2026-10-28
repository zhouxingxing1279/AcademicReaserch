# Run196 研究日志：参数相关 offset 的端点认证反例

日期：2026-10-29。

## 仓库接续

远端 `main=1c49659`；接续 Run195 远端 `0e1a757`，分支
`research/run196-pd-offset-contract`。启动工作树干净，先执行39项项目基线测试并全部通过。
只读取短检查点、Run195直接证据、19-pair checker及相关文献条目；未扩张历史
posterior/configuration 几何支线。

## 文献准入与方向纠正

精读 Mulagaleti--Mejari--Bemporad 的 PD-RCI 定义、仿射 offset/vertex control 与
式(26)--(28)，以及 Gupta--Mejari--Falcone--Piga 的 Definition 1、Lemma 3 与多项式/LMI
条件。两篇都要求覆盖未知未来调度；参数相关集合与 LPV 动力学结合后出现多项式条件，最近邻
分别用 S-procedure 或 Polya 松弛，而不是只查当前调度端点。因此本轮停止构造 endpoint LP，
只准入认证纠错。

## TDD 与精确结果

先写行为测试并运行，因 checker 尚不存在按预期 RED。随后实现纯标准库、纯 `Fraction` 的
闭区间二次最大值器与冻结反例。标量例子
`S(p)=[-(1+p),1+p]`、`x+=(1-p/2)x` 在任意未来 `p+ in [0,1]` 下的共同目标为 `[-1,1]`。
端点后继幅度均为1，但内部 `p=1/2` 为 `9/8`，精确超出 `1/8`。

证据等级为 `COUNTEREXAMPLE`，仅否定 affine-offset candidate 的 endpoint-only
certification。它不否定 PD-RCI 存在性、19-pair family、六状态安全或递归可行性。Gate A
仍 blocked。

## 复现与最终状态

- `python -m unittest verification.test_pd_offset_endpoint_counterexample -v`
- `python verification/check_pd_offset_endpoint_counterexample.py --root . --output <new-output>`
- `python -m unittest discover -s tests -v`
- `python -m unittest discover -s verification -p 'test_*.py' -v`
- `git diff --check`

最终项目测试39/39、研究验证366/366。新增论文条目改变`READ_PAPERS.md`的SHA-256，导致14个
历史工件的复现测试按预期失败；逐一运行原checker机械重建后，全部历史语义测试与哈希复现
恢复通过。自审未保留Critical、Important或Minor问题。

## 提交与同步

内容提交为本地`4c897f6`；标准HTTPS push因运行环境无GitHub用户名凭据失败。随后通过已授权
仓库连接器创建远端等树提交`6d2cd88`与分支`research/run196-pd-offset-contract`。重新fetch
核验本地与远端内容tree均为`ae465ae9792593a56165d8a4de0c871c03a295ac`；最终交付元数据
提交的远端head在本轮中文简报中报告。

## 下一唯一问题

为 19-pair affine-offset family 选择一个声音的全参数综合松弛（优先比较一维调度的精确
二次条件与 S-procedure/SDP），并规定任何返回候选必须通过本轮的独立全区间有理验证；未通过
前不声明 RCI 可行或安全。
