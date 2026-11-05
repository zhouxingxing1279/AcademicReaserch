"""Static set and finite-memory estimation benchmarks, with retained failures."""
import time
import numpy as np
from scipy.signal import place_poles
from scipy.spatial import ConvexHull
from src.oit_mrpi.sets import (ConstrainedZonotope as CZ, box, polygon, to_polytope,
    linear_map, minkowski_sum, outer_reduce, interval_hull)
from src.oit_mrpi.rpi import (finite_reach, invariant_tail, rakovic_scaled,
    iterative_rpi, one_step_rpi, rpi_direction_residual)
from src.oit_mrpi.control import double_integrator, lqr
from src.oit_mrpi.estimation import measure, window_estimate, literal_oit


def directions(n, rng, count=256):
    if n == 2:
        angle = np.arange(count)*2*np.pi/count
        Q = np.c_[np.cos(angle), np.sin(angle)]
    else:
        Q = rng.normal(size=(count, n)); Q /= np.linalg.norm(Q, axis=1)[:, None]
    return np.vstack([np.eye(n), -np.eye(n), Q])


def directed_polygon_distance(a, b):
    pb = to_polytope(CZ(np.zeros(2), np.eye(2))) if False else None
    hull = ConvexHull(b); H, h = hull.equations[:, :2], -hull.equations[:, 2]
    edges = np.roll(b, -1, axis=0)-b
    norm = (edges*edges).sum(axis=1)
    result = 0.
    for x in a:
        if max(H@x-h) <= 1e-11:
            continue
        t = np.clip(np.sum((x-b)*edges, axis=1)/norm, 0, 1)
        result = max(result, min(np.linalg.norm(x-b-t[:, None]*edges, axis=1)))
    return float(result)


def schema(system_id, n, rho, method):
    return dict(system_id=system_id, n=n, rho_F=rho, method=method,
                oit_window=None, generator_count=None, constraint_count=None,
                runtime_set=None, runtime_mpc=None, runtime_total=None,
                hausdorff_error=None, support_error=None, volume_ratio=None,
                max_constraint_violation=None, mpc_feasible=None,
                error_reason='MPC fields not applicable to static set computation')


def static_benchmarks(out, csv):
    rng = np.random.default_rng(20261105)
    sys = double_integrator(); K = lqr(sys.A, sys.B)
    weakK = -place_poles(sys.A, sys.B, [.9, .95]).gain_matrix
    systems = [('double_integrator_lqr', sys.A+sys.B@K, sys.B*.05),
               ('double_integrator_weak', sys.A+sys.B@weakK, sys.B*.05)]
    inventory = []
    for n in (4, 8, 16, 32):
        for rho in (.7, .95):
            P, _ = np.linalg.qr(rng.normal(size=(n, n)))
            F = P@np.diag(np.linspace(.3*rho, rho, n))@P.T
            m = (n+3)//4
            B = rng.normal(size=(n, m))/np.sqrt(n)
            Bw = rng.normal(size=(n, m))/np.sqrt(n)
            KK = rng.normal(size=(m, n))*.05/np.sqrt(n)
            C = rng.normal(size=(m, n))/np.sqrt(n)
            sid = f'random_n{n}_rho{rho}'
            systems.append((sid, F, Bw*.05))
            inventory.append(dict(system_id=sid, A=F-B@KK, B=B, Bw=Bw, C=C, K=KK,
                                  generation='orthogonal similarity of prescribed stable distinct real poles'))
    rows, saved, certificates = [], {}, {}
    for sid, F, D in systems:
        n = len(F); rho = float(max(abs(np.linalg.eigvals(F))))
        Q = directions(n, rng)
        ref, meta = invariant_tail(F, D, 1e-9)
        ref_finite = finite_reach(F, D, meta['horizon'])
        hs = ref_finite.support_many(Q)
        vr = polygon(ref_finite) if n == 2 else None
        functions = {
            'polytope_truncated_reference': lambda: (finite_reach(F, D, meta['horizon']),
                {'horizon': meta['horizon'], 'tail_bound_inf': meta['tail_bound_inf'], 'is_RPI': False}),
            'rakovic_scaled': lambda: rakovic_scaled(F, D),
            'zonotope_iterative_RPI': lambda: iterative_rpi(F, D),
            'zonotope_one_step_RPI': lambda: one_step_rpi(F, D),
            'CZ_batch_finite_12': lambda: (finite_reach(F, D, 12), {'horizon': 12, 'is_RPI': False}),
            'CZ_batch_plus_certified_tail': lambda: invariant_tail(F, D, 2e-4)}
        for method in rng.permutation(list(functions)):
            row = schema(sid, n, rho, method)
            start = time.perf_counter()
            try:
                Z, cert = functions[method]()
                vv = polygon(Z) if n == 2 else None
                if method == 'polytope_truncated_reference' and n == 2:
                    # Explicit V/H conversion included in the reference runtime.
                    PZ = to_polytope(Z)
                    np.testing.assert_allclose(PZ.support_many(Q), Z.support_many(Q), atol=1e-9)
                elapsed = time.perf_counter()-start
                errors = Z.support_many(Q)-hs
                row.update(generator_count=Z.g, constraint_count=len(Z.beq), runtime_set=elapsed,
                           runtime_total=elapsed, support_error=float(max(abs(errors))),
                           support_signed_min=float(min(errors)),
                           support_tolerance_pass=bool(max(abs(errors)) < 1e-3),
                           sampled_RPI_violation=float(max(rpi_direction_residual(F, D, Z, Q))),
                           certified_RPI=method not in ('CZ_batch_finite_12', 'polytope_truncated_reference'),
                           status='ok', reference_tail_bound_inf=meta['tail_bound_inf'])
                if n == 2:
                    row['volume_ratio'] = float(ConvexHull(vv).volume/ConvexHull(vr).volume)
                    row['hausdorff_error'] = max(directed_polygon_distance(vv, vr), directed_polygon_distance(vr, vv))
                    if row['certified_RPI']:
                        row['all_polygon_facets_RPI_violation'] = float(max(rpi_direction_residual(F, D, Z, to_polytope(Z).H)))
                    saved[sid+'__'+method] = vv
                else:
                    row['error_reason'] += '; volume/Hausdorff not evaluated; reference is implicit polytope support'
                certificates[sid+'__'+method] = cert
            except Exception as exc:
                row.update(status='failed', runtime_set=time.perf_counter()-start, error_reason=str(exc))
            rows.append(row)
        print('static', sid, flush=True)
    csv(out/'static_sets.csv', rows)
    np.savez_compressed(out/'set_polygons.npz', **saved)
    sweep = []
    P = np.array([[1., .5], [0., 1.]])
    for rho in (.5, .7, .9, .95, .98):
        F = P@np.diag([.8*rho, rho])@np.linalg.inv(P)
        start = time.perf_counter(); Z, cert = invariant_tail(F, .05*np.eye(2), 1e-5)
        sweep.append(dict(rho=rho, horizon=cert['horizon'], generators=Z.g,
                          tail_bound_inf=cert['tail_bound_inf'], runtime=time.perf_counter()-start))
    csv(out/'rho_horizon.csv', sweep)
    return {'rows': rows, 'certificates': certificates, 'systems': inventory, 'rho_sweep': sweep}


def estimator_benchmarks(out, csv):
    rng = np.random.default_rng(20261106)
    s = double_integrator(); A, B, C = s.A, s.B, s.C
    x = np.array([2., 2.]); ys=[]; us=[]; rows=[]; states=[]; snapshots=[]
    exact = box([1, 1], [3, 3]); sequential = box([-4, -4], [4, 4])
    designers = {'Alice': box([0, 0], [4, 4]), 'Bob': box([-4, -4], [4, 4]),
                 'David': box([-2, -2], [2, 2])}
    for k in range(41):
        y = x[0]+rng.uniform(-1, 1); ys.append(y); states.append(x.copy())
        exact = measure(exact, C, [y], 1.)
        sequential = outer_reduce(measure(sequential, C, [y], 1.), 2)
        candidates = {'true_prior_full_history': exact, 'recursive_interval_reduction': sequential}
        for name, Z in list(designers.items()):
            if Z is not None:
                Z = measure(Z, C, [y], 1.)
                if not Z.lp(np.zeros(Z.g)).success:
                    Z = None
            designers[name] = Z
            if Z is not None:
                candidates[name] = Z
            else:
                rows.append(dict(k=k, method=name, window=None, width_p=None, width_v=None,
                                 g=None, q=None, contained=False, runtime=None, status='empty'))
        for delta in (2, 4, 8):
            if k >= delta:
                start = time.perf_counter()
                Z = window_estimate(A, B, C, ys[-delta-1:], us[-delta:], 1., 1.)
                runtime = time.perf_counter()-start
                candidates[f'OIT_CZ_window_{delta}'] = Z
                O = literal_oit(A, B, C, ys[-delta-1:], us[-delta:], 1., 1.)
                # Check every defining OIT facet, not only coordinate widths.
                assert max(Z.support_many(O.H)-O.h) < 2e-7
                assert min(Z.support_many(np.eye(2))-exact.support_many(np.eye(2))) > -2e-7
                snapshots.append(dict(k=k, delta=delta, CZ=Z.record(), OIT_H=O.H, OIT_h=O.h,
                                      runtime_reconstruction=runtime))
                vl = -np.array([O.support(-q) for q in np.eye(2)])
                vh = np.array([O.support(q) for q in np.eye(2)])
                rows.append(dict(k=k, method=f'literal_OIT_{delta}', window=delta,
                                 width_p=vh[0]-vl[0], width_v=vh[1]-vl[1], g=None,
                                 q=len(O.h), contained=bool(max(O.H@x-O.h)<2e-7), runtime=runtime, status='ok'))
        for name, Z in candidates.items():
            tic=time.perf_counter(); hull=interval_hull(Z)
            widths=2*np.diag(hull.G)
            rows.append(dict(k=k, method=name, window=int(name.rsplit('_', 1)[-1]) if name.startswith('OIT_CZ') else None,
                             width_p=widths[0], width_v=widths[1], g=Z.g, q=len(Z.beq),
                             contained=Z.point_contains(x), runtime=time.perf_counter()-tic, status='ok'))
        if k < 40:
            us.append(0.)
            x = A@x+B.ravel()*rng.uniform(-1, 1)
            W = CZ(np.zeros(2), B)
            exact = minkowski_sum(linear_map(A, exact), W)
            sequential = minkowski_sum(linear_map(A, sequential), W)
            for name, Z in designers.items():
                if Z is not None:
                    designers[name] = minkowski_sum(linear_map(A, Z), W)
    csv(out/'paper_observable.csv', rows)
    np.savez_compressed(out/'paper_data.npz', ys=ys, us=us, states=states)

    # Observability and window sweeps: identical underlying trajectory and unit noise draws.
    ys0 = np.array(ys[-13:]); truth = np.array(states[-13:])
    poor, windows = [], []
    for gain in (1., .3, .1, .03):
        scaled_y = truth[:, 0]+(ys0-truth[:, 0])/gain
        delta=4
        Z=window_estimate(A,B,C,scaled_y[-delta-1:],np.zeros(delta),1.,1/gain)
        hull=interval_hull(Z)
        Obs=np.vstack([gain*C,gain*C@A])
        poor.append(dict(gain=gain, gramian_min_eigenvalue=float(min(np.linalg.eigvalsh(Obs.T@Obs))),
                         width_p=2*hull.G[0,0],width_v=2*hull.G[1,1],
                         box_area=float(4*hull.G[0,0]*hull.G[1,1])))
    for delta in (1,2,3,4,6,8,12):
        tic=time.perf_counter(); Z=window_estimate(A,B,C,ys0[-delta-1:],np.zeros(delta),1.,1.)
        Q=directions(2,rng,128); sup=Z.support_many(Q)
        # Outer support polygon area, explicitly distinguished from exact CZ area.
        from src.oit_mrpi.sets import HPolytope
        pp=polygon(HPolytope(Q,sup))
        windows.append(dict(window=delta,outer_support_polygon_area=float(ConvexHull(pp).volume),
                            runtime=time.perf_counter()-tic,generators=Z.g,equalities=len(Z.beq)))
    csv(out/'poor_observability.csv',poor); csv(out/'window_area.csv',windows)
    return {'rows': rows, 'snapshots': snapshots, 'poor_observability': poor, 'window_sweep': windows,
            'reproduction_scope': 'Eq.(25) model and observable unrestricted-prior Algorithm 3 option; new seeded noise, not original figure records; no CORA speed comparison'}
