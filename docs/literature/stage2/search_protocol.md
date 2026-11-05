# 阶段 2 检索协议 v1 · 2026-11-05

问题取自[已验收的问题表](../../research/research_questions.md)。用户指定项目工作仅以本地仓库为据，学术论文可在线阅读。本轮是可更新的结构化范围调研。以下时间分层、页深与筛选规则是本轮执行选择。

**来源与时间。** 以阶段 1 的 21 个 DOI 为已纳入种子。取 Crossref 与 OpenAlex 的题录检索结果，对关键作者稿、会议正文、作者机构与出版社记录再定位。收录截至 2026-11-05，经典及可迁移工作不设起始年，前沿层按 2024–2026 单独检索。检索用英文，以本地已有中英文资料补查。项目云端记录不参与。

| 层 | 英文检索式（每一行独立检索） |
|---|---|
| 应用 | quadrotor model predictive control outer loop position velocity trajectory |
| 应用 | multirotor robust tube model predictive control bounded disturbances |
| 基础 | robust output feedback model predictive control constraint tightening recursive feasibility terminal set |
| 基础 | set membership state estimation constrained zonotopes bounded noise |
| 方法迁移 | set valued moving horizon estimation output feedback predictive control |
| 方法迁移 | equalized recovery missing delayed observations output feedback predictive control |
| 方法迁移 | set membership state estimation sparse delayed measurements |
| 前沿 | constrained zonotope tube model predictive control constraint tightening |
| 前沿 | bounded error state estimation intermittent delayed measurements zonotope |

**筛选单位与深度。** 每式每库取相关性排序首 10 条；按 DOI 去重，未配 DOI 的按题名与作者检查。预印本与同一正式论文共用记录。两项种子锚点 M1 与 M2 作引文扩展，向后取所列文献、向前优先查可取得的引文索引。已知项召回按关键词自然命中和另行定向核验分别统计。来源失败则记录请求及影响，并用学术网页定向检索补足。

**纳入。** 主库包含 21 项种子，以及题名/摘要筛选后能直接解释至少一个目标连接的代表作。新增代表作优先级依次为：同篇覆盖时间戳/失测及确定性包含或可行性，集员估计到输出反馈 MPC 或收紧，直接四旋翼外环 Tube，最后是未被种子覆盖的集合或终端基础。按上述优先级在各连接取具有可定位原文或权威摘要的工作。同类重复实现及仅有泛主题相似的条目保留在筛选表。排除与状态估计/控制无关、仅网络通信、仅能量管理等记录。只有摘要的纳入项保留缺失字段。

**停止与复现。** 本轮完成固定检索页、引文扩展尝试、种子真实性核对和逐篇提取后交付。报告分别列出返回、去重、纳入和保留待查的数目，保存返回快照与筛选理由。此截止按页深与本轮范围决定，不据此宣称检索饱和。长期更新时沿用 DOI 与 citekey，补录来源、版本与勘误。
