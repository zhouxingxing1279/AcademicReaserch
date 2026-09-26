# 55 Terminal support gate

For a polyhedral terminal error set X_f={e:H_f e<=h_f} and terminal error dynamics e+=F_f e+w, w in W, the exact terminal append condition is finite-direction:

h_E(F_f^T H_f[j]^T)+h_W(H_f[j]^T)<=h_f[j] for every terminal facet j.

This follows directly from h_{F_f E+W}(a)=h_E(F_f^T a)+h_W(a) and the H-representation containment test. Therefore full compressed-set inclusion is sufficient but not necessary. Chapter 54's nonterminal support ledger must be augmented by the terminal pullback directions F_f^T H_f; stage-only support domination does not imply recursive feasibility.

Exact 2-D counterexample used in this run: old box [-1,1]^2 and a candidate box [-1/2,1/2]x[-3,3] have improved support in the stage direction +/-e1, but with F_f=diag(1/2,1/4), W=[-1/10,1/10]^2 and X_f={|e1|<=1,|e2|<=1/2}, the terminal +e2 row gives 3/4+1/10=17/20>1/2. Thus the stage-only finite-direction claim is false.

Scope: this closes only the terminal set-containment interface. A recursive-feasibility theorem still also needs the nominal terminal controller/set invariance, input admissibility, and the shifted nominal tail. It does not prove those ingredients for the current quadrotor model.

Literature boundary: Mayne, Seron, Rakovic, Automatica 41(2), 219-224, DOI 10.1016/j.automatica.2004.08.019, is the classical robust MPC baseline; this support-function restatement is not claimed as a new MPC theorem.

Next priority: instantiate H_f and F_f for the repository's actual ancillary/terminal candidate and test whether the augmented finite-direction ledger is nonempty under the current disturbance contract.