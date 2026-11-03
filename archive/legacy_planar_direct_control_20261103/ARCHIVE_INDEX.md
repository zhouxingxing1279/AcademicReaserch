# 历史归档索引 — legacy planar/direct-control research

归档日期：2026-11-03。来源 main：eb18e857090b0babe531c13c61aea944793af428。

## 原则
旧平面/底层直接控制工件只移动、不删除，按原始相对路径保留。归档不表示历史证明错误，而是说明其模型、输入权限和假设不再是当前外环研究的活动合同。本次从活动路径移动 **1,164 个文件**；旧 README 另行复制；原始 docs/research 检查点与 Run 日志完整保留在归档的 docs/research 子树中；通用数值集合工具另复制到活动源码目录。

## 原路径映射
| 原路径 | 归档子路径 | 内容 |
|---|---|---|
| README.md | README_legacy_20261103.md | 旧项目导航及过时检查点 |
| docs/research/**（model_selection 除外） | docs/research/** | 旧研究合同、Run 日志、automation_runs 与旧检查点 |
| docs/learning/** | docs/learning/** | 旧 SMF/CZ/Tube/信息状态推导 |
| docs/theory/** | docs/theory/** | 旧平面姿态、推力/力矩、终端与可行性理论 |
| docs/superpowers/** | docs/superpowers/** | 一次性设计计划与规格 |
| docs/research_framework.md | docs/research_framework.md | 旧研究框架 |
| docs/课题中期报告.md | docs/课题中期报告.md | 旧阶段报告 |
| configs/planar_baseline.json | configs/planar_baseline.json | 旧平面直接控制模型配置 |
| src/smf_mpc/** | src/smf_mpc/** | 旧 plant、观测器、滤波器与模型专用代码 |
| scripts/** | scripts/** | 旧训练、仿真和绘图脚本 |
| tests/** | tests/** | 旧单元测试与 fixtures |
| verification/** | verification/** | 旧精确证书检查器与回归测试 |
| results/** | results/** | 旧实验/理论计算结果与 JSON/SVG |
| .github/workflows/** | .github/workflows/** | Run220–278 专用历史 CI 工作流 |

## 值得复用的历史资产
- **Run246**：旧四状态固定推力模型下的可生存性反例；只说明特定初始点/扰动下的终端不可生存。
- **Run260/261**：旧四状态合同下的条件化桥接/终端安全证据；量词、测量历史和控制权限需重新映射。
- **Run278**：旧四状态冻结 Euler 后验受限切片与共享开环障碍；不是完整 SMF 后验，也不是因果反馈不可能性。
- **docs/learning/08、15–21、27–29、36、76–99、120–132**：CZ 接口、输出反馈 Tube、支持函数、测量条件化、信息状态和递归可行性探索；可作为数学工具/反例库，但物理假设须重新核对。
- **docs/theory/01–09**：旧模型下的解析证明/反例，不可直接移植到新三维平移闭环模型。
- **results/** 与 **verification/**：保留精确有理数 JSON、脚本和历史测试。
- 旧 src/smf_mpc/sets.py 已复制为活动 src/common/numerical_sets.py；它只是 float64 Box/Zonotope 数值工具，不是 CZ 或形式化向外舍入证书。

## 活动目录保留
- docs/literature/PAPER_READING_LOG.md：唯一论文总账，未移动、未重建。
- docs/research/model_selection/**：全部背景文献审计与模型矩阵保留，作为可追溯证据库；`MODEL_SELECTION_EVIDENCE.md` 顶部是唯一当前决策摘要，其下旧矩阵/逐轮日志已显式标为历史记录，里面曾经出现的“平面六状态直接推力/力矩首选”及旧“下一步”不再生效。
- docs/research/CURRENT_CHECKPOINT.md：新外环检查点。
- docs/research/MODEL_CONTRACT.md：临时接口/模型合同。
- src/common/numerical_sets.py：可复用但仅数值性的集合工具。

归档中的代码与 CI 是旧模型历史实现，移动后不再由活动工作流自动运行。复现时应在独立工作树/分支恢复相应文件。不得把旧 Run 的通过记录称为当前外环模型测试通过。
