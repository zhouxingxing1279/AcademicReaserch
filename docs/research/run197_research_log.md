# Run197 研究日志：标量区间精确 SDP 合同

日期：2026-10-29。

## 仓库接续

核查远端 `main=1c49659`、远端 Run196=`d98ddcd` 与短检查点；本地 Run196 与远端因连接器
提交历史不同而各自 ahead/behind 3，但内容 tree 一致且工作树干净。接续后创建
`research/run197-affine-offset-exact-sdp`。启动39项项目测试全部通过。

## 文献准入

精读 Pólik--Terlaky 的 S-lemma/Slater 条件，重读 Mulagaleti--Mejari--Bemporad 式
(26)--(28)、Remarks 4--5和SDP(33)，并复核 Gupta 等的参数多项式/Polya LMI。结论是：
最近邻的一般多维 S-procedure 是充分条件且可能有间隙；当前一个标量区间可用单二次约束的
S-lemma 得到精确 `2 x 2` LMI。该特化是已有定理直接推论，不作创新声明。

## TDD 与结果

先写9项行为测试并运行，因 checker 尚不存在按预期 RED。随后实现纯标准库、纯 `Fraction`
证书核查器；首轮8项通过，仅归档结果尚不存在而失败。生成机器可读结果后9/9通过。检查器
精确核查系数恒等式、非负乘子、PSD对角元与 determinant；正例 `1-s^2`、`1+s` 通过，
Run196 归一化负例 `(s^2-1)/8` 被拒绝。

固定19-pair cone共有38 facets、160 vertices，故下一综合器需要6080条区间 LMI；
configuration/state/torque 的 affine 条件仍可精确查端点。未来调度任意跳变以共同 core
offset 给出可靠但可能保守的 successor target。整体状态仍为 `OPEN`，Gate A blocked。

## 实现边界

运行环境未安装 CVXPY 或其他仓库声明的 SDP 接口，本轮不临时引入未经锁定的新依赖，也不
报告任何19-pair solver feasibility。该暂停符合先冻结证书合同、再数值综合、最后独立精确
复核的证据顺序。

## 复现

- `python -m unittest verification.test_scalar_interval_slemma -v`
- `python verification/check_scalar_interval_slemma.py --root . --output <new-output>`
- `python -m unittest discover -s tests -v`
- `python -m unittest discover -s verification -p 'test_*.py' -v`
- `git diff --check`

最终聚焦测试9/9、项目测试39/39、全研究验证375/375。文献总表更新触发14个历史工件的
依赖哈希变化；全部由原checker机械重建，逐份diff确认仅`READ_PAPERS.md`哈希变化，旧数值
与证据结论未改变。归档JSON重新生成与独立临时输出逐字一致，`git diff --check`通过。

## 下一唯一问题

在可复现 SDP 环境中求解固定 cone 的19-pair affine-offset 候选；返回候选必须逐条通过
6080条全区间二次独立核查，再讨论可行/不可行或扩大 configuration family。
