# Run 147：初始化路径的 correlated return seed

日期：2026-10-03。分支 `research/run147-vertical-correlated-return-seed`。

## 1. 仓库接续与独立复核

启动时刷新远端，发现 Run 146 已先完成 Run 145 指定的 second sweep；因此没有重复实现。
从远端 Run 146 `160952c` / tree `5f039e1` 接续，`origin/main=1c49659`。Run 146 checker
重新生成的 JSON 与归档逐字节一致；按声明的 discovery 入口重跑 `verification/` 为
182/182、`tests/` 为39/39，`compileall` 退出0。

曾用 `python -m unittest verification/test_vertical_joint_second_sweep.py` 从仓库根直接运行，
因历史测试采用 `verification/` 顶层 import 而出现5项 `ModuleNotFoundError` 派生失败。
系统化复核表明 README/Run146 明确使用 discovery 或 `PYTHONPATH=verification`；按该入口
定向6/6通过。这不是 validator 结论失败，也没有为未声明的 package API 做无关重构。

## 2. 文献准入与方向纠正

本轮精读 Houska 2023 全文 HTML Sections 4.4、6.2、6.4--6.5、Lemma 2、Definition 7、
Theorem 3 及证明；重读 Hempel 2011 Sections III-A--C、Definition 2、Theorem 1、
式 (3)--(11)；复核 Kumar--Kothyari 2026 与 Baras--Patel 1998 的已读全文记录。
information ensemble、extreme-set control、OFCI fiber 量词与 zonotopic output-feedback LP
均有直接近邻，因此不作算法创新声明。

排重发现 Run 146 的下一问题“把 mode-14 `q|d` 压至 product 门槛以下并保留初始化
miss-chain”已被 Run 143 精确否定。初始化 `d=0` 经14条 miss 后仍是同一 visible offset，
必须保留完整 `E_14` fiber；重复做条件纤维压缩既不会改变可行性，也违反停止规则。
本轮改为构造强制 `14->0 success` 的完整 correlated return image。详见准入卡。

## 3. TDD 与实现

先写6项行为测试，锁定：初始化 miss-chain 的完整可达性；共享 residual/measurement
primitive；精确 affine-hull 秩；完整联合像的 estimator/true-error 支持；相对 Run146
product `D_0^0` 的严格分离；结论边界与 hash-bound artifact。RED 阶段6/6因 checker
缺失按预期失败。

实现 exact-rational checker 后，5项核心行为测试通过；artifact 测试先因理论文档未生成
而失败，符合交付依赖。checker 从 Run136 的 mode-14 104列 zonotope 直接映射式 (84.1)，
再只增加一列共享 residual 与一列共享位置噪声；没有采样、浮点判定或独立装箱。

抛弃式代数探针原先假设 return image 可能四维，精确秩检查给出3。准入卡随即改为“确定
并正确标注 affine-hull 维数”；生产测试锁定 `rank=3` 及所有生成元的
`d_v^+=(9/2)d_p^+` 关系，避免把低维必达集合冒充正体积 RCI。

本轮 rulings：

- **Ruling：**Run146 的下一问题与 Run143 的初始化可达性结论冲突，改做完整 correlated
  return image；若判断错误，代价是过早放弃一种条件模板，但14条 miss 的 exact reachable
  equality 和固定 `d=0` 直接排除了所要求的压缩。
- **Ruling：**接受 rank-three reachable seed，不为满足原设想而外加虚假厚度；若判断
  错误，代价是低估后续模板维数，但 exact Gaussian rank 和逐生成元线性恒等式独立支持它。

## 4. 核心结果与证据等级

14条 miss 从合同初始化精确到达 Run136 mode-14 zonotope，`q` 半宽仍为
`23312147/48000000`。强制 success 的完整 vertical return seed：

- 106个相关生成元，affine-hull rank为3；
- `eta` 支持为 `(1/50, 7329131969/7200000000)`，包含于 mode-0 vertical box；
- `e` 支持为 `(23312147/48000000, 152955031/72000000)`，严格满足
  `|e_p|<=1, |e_v|<=11/4`；
- `d_v` 支持 `72816441/32000000` 超出 Run146 product target
  `94125081847/57600000000`，严格超量 `36944511953/57600000000`。

因此 Run146 的 mode-14 塌缩来自独立 `d` 限幅；完整初始化 return image 本身在当前竖直
真实约束内。证据等级仅为 **exact rank-three correlated return seed for the required
initialization path**，不是 RCI、全六状态、输入/终端/移位或递归可行性证明。

## 5. 验证、交付与下一问题

第一次全仓回归发现 Run146 artifact 因本轮更新 `READ_PAPERS.md` 而只剩该文件的历史
SHA-256 失配。重新生成并逐字段比较确认：数值、集合、结论和其他散列完全不变，只有
`READ_PAPERS.md` 散列更新；Run146 定向6/6恢复通过。修复后的回归为：

- `verification/`：188/188，通过，90.766秒；
- `tests/`：39/39，通过，1.320秒；
- 合计227/227；
- 新 checker 定向6/6通过；
- `compileall`、JSON 解析和 `git diff --check` 进入最终冻结复核。

按无子代理约束执行最终作者自审：逐项核对共享原语、坐标变换、支持函数、秩、证据等级、
历史 artifact 更新和测试入口，未发现 Critical/Important 问题；作者自审弱于独立审稿，
因此结论仍严格限制为必要 seed。

新增 checker、测试、第84章、准入卡、日志和 exact JSON artifact；更新文献表与短检查点。

下一轮唯一问题：对初始化可发生的5/10/15 tick 三种 success return 构造同语义的相关
seed，并判断是否存在一个满足真实约束、保留三者共享原语的单一 mode-0 模板；该门槛通过
后才准入 controlled predecessor synthesis。
