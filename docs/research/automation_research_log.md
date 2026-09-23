# 自动研究日志

## 2026-09-23 — 任意多等式 CZ 支持查询认证
第 20 章固定后验实验只能对单等式 CZ 重建原始顶点。本轮补齐一般历史 CZ 的 primal/dual 认证接口。固定 seed=20260923 的 600 个随机多等式有理数 CZ 全部通过上下界审计；详见第21章。

---
## 2026-09-23 — 后验收缩与 observer/nominal center 漂移
精确一维反例否定“posterior shrinkage 自动推出 recentered tube shrinkage”。详见第22章。

---
## 2026-09-23 — 六状态 rolling CZ 与 posterior-member recenter LP
62 个压力方向中 coordinate-midpoint recenter 出现 mixed-direction violations；posterior-member budget LP 消除数值违反。但随机 mixed directions 并非真实 MPC normals。详见第23章。

---
## 2026-09-23 — 真实 control normals 门：recenter 候选降级
18个真实法向重跑 rolling posterior 零违反；更新前 feasibility gate 已有近邻。详见第24章。

---
## 2026-09-23 — 六状态 ancillary LQR/RPI：模型合同假阳性
固定 hover LTI 上 LQR 稳定，但语义一致的全域扰动下 mRPI 在 vx/phi/tau 三个硬约束方向失败；错误使用 reduced residual 则产生假正 margin。详见第25章。

---
## 2026-09-24 — 单乘积相关性：McCormick 已 support-exact
单矩形域上线性 support 的 McCormick relaxation 已是 exact convex hull；普通 CZ 改写不会进一步缩紧。详见第26章。

---
## 2026-09-24 — 控制决策语义闭合
`deltaT` 保持 MPC decision，SMF 只认证 `phi`；给定 `phi` interval 后 robust support 是两个关于 `deltaT` 的仿射函数最大值，可精确 epigraph。详见第27章。

---
## 2026-09-24 — Exact rolling CZ 的 shift-nesting 自动成立；缺口转向 fixed-complexity reduction

### 研究问题
第27章要求验证 horizon-wise `phi` intervals 是否满足 `[ell_i|k+1,u_i|k+1] subset [ell_i+1|k,u_i+1|k]`。本轮先从集合算子本身推导，而不是把该关系当经验假设。

### 理论结论
固定预测算子 `P(S)=F S (+) W`、合法 measurement update `X_{k+1} subset P(X_k)` 下，线性映射和 Minkowski 和的集合单调性直接给出

`P^i(X_{k+1}) subset P^(i+1)(X_k)`。

因此所有线性 support 都 non-expanding，特别是 `phi` projection interval 自动 shift-nested。对第27章 decision-conditioned support，只要 shifted candidate 沿用上一 horizon 的对应 thrust decision，前 `N-1` stages 的新 tightening 不会比旧 tightening 更差。

这不是完整 recursive-feasibility theorem：terminal append、decision-dependent map change、adaptive W/model contract、以及 fixed-complexity reduction 仍未闭合。

### 代码验证
新增 `verification/check_shift_nested_scheduling_tube.py`，复用六状态 affine outer model、CZ predict/observe 和非零 truth-consistent measurements。horizon=8、26 ticks，实际审计 200 个 shifted interval inclusions：0 violations；400 个 endpoints 中 200 个严格收缩；平均 endpoint reduction `2.744e-4 rad`，最大 `5.60e-4 rad`。归档于 `results/shift_nested_scheduling_20260924/checks.json`。

数值实验只是 theorem audit；包含关系证明不依赖样例。

### 文献边界
Köhler et al. 2021 已明确给 set-membership update 与 tube/set RAMPC 的 monotonic/non-increasing 条件来保证 recursive feasibility/constraint satisfaction；Hanema et al. 2021 已用 state/scheduling relation 构造 future scheduling tube 并证明 recursive feasibility/stability。因此“nested future uncertainty 帮助递归可行”不是创新。

### 本轮最重要的方向收缩
exact CZ history 下，前 `N-1` stages 的 shift nesting 不需要额外 feasibility gate。真正工程必需且尚未闭合的是**固定复杂度压缩**：若每一步独立 outer-reduce CZ，虽然 `X subset R(X)`，却不自动推出对嵌套 `A subset B` 有 `R(A) subset R(B)`。因此 naive reduction 可能破坏刚刚证明的 shift compatibility。

### 候选创新排序
1. **certificate-preserving fixed-complexity CZ reduction**：主候选。要求 outer inclusion + bounded complexity + control-normal/集合层面的 shift compatibility。
2. **certified SMF-to-scheduling-tube interface**：保留为系统接口，但 exact-CZ nesting 本身不是创新。
3. **exact-CZ update feasibility gate**：降级；固定 prediction contract 下前 N-1 stages 冗余。

### 下一轮关键任务
主动构造 `A subset B` 但独立 reduction 后某真实 control normal 上 `h_R(A)(p)>h_R(B)(p)` 的反例。若存在，再设计 ancestor-capped support reduction 或共享-template nested reduction，并验证固定复杂度、outer inclusion 和 recursive-feasibility compatibility 能否同时成立。
