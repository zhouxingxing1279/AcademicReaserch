# Run198 研究日志：fixed-cone affine-offset SOCP 能力门

日期：2026-10-29。

## 仓库接续

核查远端`main=1c49659`、远端Run197=`5c6c424`与短检查点。本地Run197=`513a5c1`因连接器
提交历史不同而与远端各自ahead/behind，但两者内容tree均为`e6c6382`且工作树干净；随后创建
`research/run198-affine-offset-socp-gate`。本轮只读取Run197合同、19-pair计数源码及直接文献。

## 文献准入与唯一阻塞

重读Mulagaleti--Mejari--Bemporad的LMI(28)、SDP(33)、算法步骤4与Section IV求解环境；
精读Fawzi的Introduction式(1)和Theorem 1；定向精读Goulart--Chen Sections 2.1--2.2。
最近邻确认`2 x 2` PSD可精确改写为SOCP，但一般更高阶PSD不能。当前唯一阻塞不是理论
不可行，而是运行环境没有真正的conic solver，无法执行Run197冻结的6080条件综合。

## 推导、代码与证据

对`Q=[[q00,q01],[q01,q11]]`，证明
`Q>=0 iff ||(2q01,q00-q11)||_2<=q00+q11`，并以`Fraction`精确检查
`(q00+q11)^2-[4q01^2+(q00-q11)^2]=4det(Q)`。证据等级为`DERIVED`。

冻结原始SOCP包含6080个三维cone、6514个标量变量；38个pair-offset coefficient等式消元
后为6476个。另有12160条configuration端点、2560条硬状态端点、640条力矩端点、76条
common-core端点及76条offset非负端点约束。计数不对common core强加pair symmetry，也未
删冗余行。

模块、可执行文件和pip cache核查均未发现Clarabel、SCS、CVXPY、CVXOPT、ECOS或商业锥
solver。故不以HiGHS LP、有限网格或局部NLP替代。`numerical_feasibility=OPEN`；不能推出
四状态RCI、六状态安全或递归可行性。

## 验证

- `python -m unittest verification.test_affine_offset_socp_gate -v`：5/5通过；
- `python -m unittest discover -s tests -v`：39/39通过；
- `PYTHONPATH=verification python -m unittest discover -s verification -p 'test_*.py' -v`：
  380/380通过；
- `git diff --check`：通过。

更新`READ_PAPERS.md`使14个历史hash-bound工件按预期失配；均用原checker机械重建，确认仅
文献总表SHA-256变化，第二次全研究回归全部通过。

## 提交与下一问题

内容提交=`5ca99b7`，tree=`a1e0265`。下一唯一问题：提供锁定版本SOCP solver，求解冻结
affine-offset模型；无论solver状态如何，返回候选必须逐条通过6080个全区间二次条件与全部
端点线性约束的独立审计。
