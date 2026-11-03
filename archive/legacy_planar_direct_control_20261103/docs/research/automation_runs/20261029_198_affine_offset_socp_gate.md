# Run 198：affine-offset SOCP能力门

- 文献：Mulagaleti--Mejari--Bemporad 2025（LMI(28)、SDP(33)、算法/求解环境）；Fawzi 2019
  （`2 x 2` PSD/SOC同构）；Goulart--Chen 2026（Clarabel锥与解/不可行语义）。
- `DERIVED`：每个`2 x 2`区间LMI精确等价为一个三维Lorentz cone。
- 规模：6080个SOC，6514个原始标量变量，pair-offset等式消元后6476个。
- 当前环境无锥求解器；数值可行性`OPEN`，未用LP、网格或局部NLP替代。
- 验证：5项聚焦、39项项目、380项研究测试全部通过。
- Gate A：blocked。下一步只安装/锁定SOCP solver并独立审计候选。
