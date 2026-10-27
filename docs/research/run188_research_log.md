# Run188 研究日志：六 facet meta 坐标选择

日期：2026-10-27。

## 仓库接续

- 远端 `main=1c49659c762dcb96dadeb8fe7a6216570951b774`。
- 最新成果分支 `research/run187-six-facet-meta-gate`，远端提交 `d33c98516894d8110ee413bb46f64eca055d08bc`。
- 本轮基于同一 tree `c4bbf0f228643188a2e3df8bfdeb5808082f0b0a`；基线项目测试39/39、研究验证315/315。

## 文献准入

重读 Houska §6.1--6.5、式(25)--(27)、Definition 7、Theorem 3及证明；重读
Villanueva--Müller--Houska §3.4--3.5、Definition 6、Lemma 1、Theorem 1；精读
Raghuraman--Koeln §2、§3开头、式(1)--(3)及Theorem 4相关表示讨论。Robbins 2026仍仅有摘要。
准入通过“坐标自由度与measurement closure方向纠正”，不通过“center/radius减少预算是创新”
或“已构造 `H/Omega`”。

## 候选与精确结果

1. direct six offsets：完整保留configuration参数自由度，选作后续参考；
2. five center/radius coordinates：隐含 `delta=c_q-c_p+(1/10)c_v=0`，被实际测量反例否定；
3. six center/radius/skew coordinates：与direct offsets可逆，仅为换元。

反例从 `y_i=3/200` 出发，使用实际测量半宽 `1/50` 与中心 `-23/4000`；紧posterior为
`(57/4000,3/200,...,3/200)`，六facets活跃且configuration最大margin为`-3/4000`，但skew
从0变为`3/8000`。同一参数多面体经可逆换元后极点一一对应，故不能仅凭坐标减少预算。

## 实现、证据与剩余缺口

按TDD先写5项测试；checker和artifact缺失时5项均失败，随后实现精确有理数求交、可逆映射、
configuration margin和哈希绑定，聚焦测试5/5通过。阶段性全套为项目39/39、研究验证320/320；
最终提交前重新全量复验。证据等级为
`exact_six_facet_meta_coordinate_nonclosure_certificate`，不是控制、终端或递归可行性结论。

独立只读复审确认代数、测量见证、六facet活跃性、25份历史哈希变更与证据边界均无
Critical/Important问题。两项非阻塞Minor建议（测试中显式固定六个posterior vertices、断言manifest
必需成员）留待后续测试维护，不影响本轮精确结论。

下一轮唯一问题：选择受物理bounds限制的有界direct-offset meta polytope，精确枚举configuration
与真正extreme information sets；预算不可接受则转向CZ固定复杂度可靠外包。
