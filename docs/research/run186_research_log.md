# Run186：六 facet measurement-support 基线

从远端 Run185 `302600a5` 开始，基线测试为项目39/39、研究验证301/301。精读 Villanueva--Müller--Houska §3.4--3.5/Theorems 1--2/Corollary 4，Houska §6.2--6.5/Theorem 3，以及 Badalamenti 等2025 §3.1--3.2、§4.1/Algorithm 1。后者已系统覆盖增加 facets 与 template refinement，故本轮不作模板创新声明。

按 `+p,+v,-q,-p,-v,+q` 构造六个相邻 vertex maps 与24行 configuration cone。初始 RED 因 checker 不存在而5项失败；实现后5/5 GREEN，项目39/39、研究306/306。随后增加 artifact replay 测试，先因 CLI/归档缺失 RED，再生成哈希绑定 artifact 后6/6 GREEN。

独立代码复核另外以216组对称支持和729组一般 offsets 检查代数，确认 vertex/configuration/support 结果；同时发现 `run()` 虽记录非法先验却仍可能发出正结论。新增非法先验回归测试先 RED，随后令 gate 对先验与 canonical posterior 的 configuration-cone 失配直接拒绝，7/7 GREEN；重建 artifact 后全量项目39/39、研究验证308/308。未扩展所有支持分支与退化边界测试，也未改写文档中“checker 枚举”的简写（实际独立枚举位于测试），两项记为非阻塞 minor。

核心精确结果：对 `|p|<=a, |v|<=r_v, |p-kappa v|<=r_q`，紧 slant 支持是 `min(r_q,a+kappa*r_v)`。在 `(r_p,r_v,r_q)=(1,11/4,1)`、`a=1/50` 下，raw success offsets 不在六边形 configuration cone，而 canonical offsets 的 `r_q=59/200`，严格收缩 `141/200` 并位于 cone 边界。这纠正 Run185 在恢复 velocity facets 后仍默认 success 保留 `q` 的潜在误用。

证据仅为 `exact_six_facet_measurement_support_map`；没有 graph/meta ensemble、center、control、terminal 或递归可行性结论。下一步只构造连续 measurement-center 的六-facet `Z/H/Omega` 和15-mode/17-edge因果LP，不再把局部支持收缩本身包装成课题贡献。
