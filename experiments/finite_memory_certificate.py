"""Standard-library exact-rational checks, independent of float LP/QP runs."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sys


def mm(a, b):
    return [[sum((x*y for x, y in zip(row, col)), F(0)) for col in zip(*b)] for row in a]


def tr(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[x+y for x, y in zip(r, s)] for r, s in zip(a, b)]


def check():
    T, a, nu = F(1, 2), F(1, 50), F(1, 200)
    M, L, Q = 1, 1, 4
    r0 = [F(1, 200), F(1, 100)]
    cases, candidates = [], []
    vertex_count = 0
    for h in range(M+L+1):
        for d in range(1, Q-h+1):
            beta = 2*nu/(d*T)+d*T*a/2
            radius = [nu+h*T*beta+(h*T)**2*a/2, beta+h*T*a]
            maxima = [F(0), F(0)]
            n = d+h
            for signs in product([-1, 1], repeat=n+2):
                p, v = F(2, 9), -F(1, 13)
                initial_p = p
                controls = [F((-1)**j, 7) for j in range(n)]
                history = [(p, v)]
                for j in range(n):
                    q = controls[j]+signs[j]*a
                    p, v = p+T*v+T*T*q/2, v+T*q
                    history.append((p, v))
                ys = initial_p+signs[-2]*nu
                yt = history[d][0]+signs[-1]*nu
                vs = (yt-ys-sum(T*T*(d-j-F(1, 2))*controls[j] for j in range(d)))/(d*T)
                vt = vs+sum(T*controls[j] for j in range(d))
                vp = vt+sum(T*controls[j] for j in range(d, n))
                pp = yt+h*T*vt+sum(T*T*(n-j-F(1, 2))*controls[j] for j in range(d, n))
                error = [abs(p-pp), abs(v-vp)]
                assert all(e <= r for e, r in zip(error, radius))
                maxima = [max(e, m) for e, m in zip(error, maxima)]
                vertex_count += 1
            assert maxima == radius
            candidates.append([2*r for r in radius])
            cases.append(dict(d=d, h=h, radius=radius, exact_vertex_maxima=maxima))
    for k in range(Q):
        candidates.append([r0[0]+k*T*r0[1]+(k*T)**2*a/2, r0[1]+k*T*a])
    E = [max(r[i] for r in candidates) for i in range(2)]
    A, B, K = [[F(1), T], [F(0), F(1)]], [[T*T/2], [T]], [[-1/(T*T), -F(3, 2)/T]]
    closed = add(A, mm(B, K))
    assert mm(closed, closed) == [[0, 0], [0, 0]]
    delta = a+sum(abs(k)*e for k, e in zip(K[0], E))
    FB = mm(closed, B)
    S = [[delta*b[0], delta*f[0]] for b, f in zip(B, FB)]
    state_margin = [sum(abs(q) for q in row) for row in S]
    input_margin = sum(abs(q) for q in mm(K, S)[0])+sum(abs(k)*e for k, e in zip(K[0], E))
    tight = [F(3)-state_margin[0], F(2)-state_margin[1]]
    input_tight = F(4)-input_margin
    base = [[1, 0], [0, 1], [-1, 0], [0, -1], K[0], [-v for v in K[0]]]
    budget = tight+tight+[input_tight, input_tight]
    H = base+mm(base, closed)
    hf = budget+budget
    assert mm(H, closed) == mm(base, closed)+[[0, 0] for _ in base]
    inscribed = min(b/sum(abs(v) for v in row) for b, row in zip(hf, H) if any(row))
    stage = add([[F(4), F(0)], [F(0), F(1)]], [[F(1, 5)*v for v in row] for row in mm(tr(K), K)])
    P = add(stage, mm(mm(tr(closed), stage), closed))
    assert add(mm(mm(tr(closed), P), closed), stage) == P
    admission = r0[0]/(T*T*delta)+r0[1]/(2*T*delta)
    assert admission <= 1 and inscribed > 0
    return dict(arithmetic='fractions.Fraction, exact rational', pair_cases=cases,
                pair_vertices=vertex_count, E=E, K=K, F=closed, delta=delta,
                tube_generators=S, state_margin=state_margin, input_margin=input_margin,
                nominal_state=tight, nominal_input=input_tight, terminal_H=H, terminal_h=hf,
                terminal_inscribed_box_radius=inscribed, P=P,
                initial_tube_coefficient_bound=admission,
                identities=['F^2=0', 'F S + B[-delta,delta] = S',
                            'H_f F = [H_base F;0]', 'F^T P F + Q + K^T R K = P'],
                scope='Algebra/endpoint certificate only; no float LP/QP or physical certification')


if __name__ == '__main__':
    result = check()
    target = Path('experiments/results/finite_memory_tube/exact_certificate.json')
    target.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(result, default=str, indent=2)
    if '--check' in sys.argv:
        assert json.loads(target.read_text(encoding='utf-8')) == json.loads(encoded)
    else:
        target.write_text(encoded, encoding='utf-8')
    print(json.dumps({k: result[k] for k in ['pair_vertices', 'E', 'state_margin', 'input_margin',
                                          'terminal_inscribed_box_radius']}, default=str))
