"""Normalize saved verification records without running any numerical experiment."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'experiments/results/oit_mrpi_20261105'
FIELDS = [
    'system_id', 'n', 'rho_F', 'method', 'oit_window', 'generator_count',
    'constraint_count', 'runtime_set', 'runtime_mpc', 'runtime_total',
    'hausdorff_error', 'support_error', 'volume_ratio',
    'max_constraint_violation', 'mpc_feasible',
    'stage', 'source_file', 'source_row_index', 'recorded_runtime', 'scope_note',
]


def main():
    records = []
    inputs = {}
    def load(name):
        path = OUT / (name + '.json')
        inputs[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        return json.loads(path.read_text(encoding='utf-8'))

    static = load('static')
    rho = next(r['rho_F'] for r in static['rows']
               if r['system_id'] == 'double_integrator_lqr')
    def add(stage, index, original, *, system='double_integrator_lqr',
            dimension=2, radius=rho, note='', **values):
        record = dict.fromkeys(FIELDS)
        record.update(system_id=system, n=dimension, rho_F=radius,
                      method=original.get('method'), stage=stage,
                      source_file=stage+'.json', source_row_index=index,
                      scope_note=note)
        record.update(values)
        records.append(record)

    for i, r in enumerate(static['rows']):
        values = {k: r.get(k) for k in FIELDS[:15]}
        # Already uses the requested schema, including nulls with a reason.
        add('static', i, r, note=r.get('error_reason', ''), **values)

    estimator = load('estimator')
    for i, r in enumerate(estimator['rows']):
        add('estimator', i, r, system='paper_eq25_observable', radius=None,
            oit_window=r['window'], generator_count=r['g'],
            constraint_count=r['q'], recorded_runtime=r['runtime'],
            note='Estimation only; no closed-loop rho_F. Original runtime scopes differ: '
                 'CZ rows time hull queries; literal OIT rows reuse window reconstruction '
                 'time. Do not interpret as comparable total estimator latency. '
                 'Containment and status remain in the source row.')

    matched = load('matched')
    for i, r in enumerate(matched['rows']):
        add('matched', i, r, oit_window=r['window'],
            generator_count=r['generators'], constraint_count=r['equalities'],
            runtime_set=r['runtime'], runtime_total=r['runtime'],
            note='Full set-and-support-query workload repeated across horizons/directions; '
                 'deduplicate by (k,window,method) for timing. No MPC solve. '
                 'Raw halfwidth excludes common future noise.')

    feasible = load('feasible')
    for i, r in enumerate(feasible['rows']):
        add('feasible', i, r, oit_window=3 if r['method'] in
            ('ordinary_zonotope', 'OIT_CZ_compatible') else 0,
            runtime_mpc=r['runtime_mpc'], mpc_feasible=r['feasible'],
            note='Frozen zero-innovation information slice; nominal grid point in source. '
                 'Set construction not timed per row; total latency unavailable. '
                 'QP residual is not a realized physical constraint violation.')

    closed = load('closedloop')
    for i, r in enumerate(closed['rows']):
        add('closedloop', i, r, oit_window=3 if r['method']=='OIT_CZ_compatible' else 0,
            runtime_set=r['runtime_set'], runtime_mpc=r['runtime_mpc'],
            runtime_total=r['runtime_total'],
            max_constraint_violation=r['max_constraint_violation'],
            mpc_feasible=True,
            note='One logged step with an available feasible plan; aborted runs, if any, '
                 'are separately retained in source failures. Timing excludes instrumentation '
                 'and serialization; seed/k and full state in source.')

    mc = load('montecarlo')
    add('montecarlo', None, {'method':'OIT_CZ_compatible'}, oit_window=3,
        max_constraint_violation=mc['max_constraint_violation'],
        recorded_runtime=mc['runtime'],
        note='Aggregate of 10000 trajectories x 30 steps; batch runtime is not per-step '
             'latency. All 300000 applied plans used verified unconstrained optima, '
             'zero online QP solves, one distinct adaptive tube construction. '
             'Per-plan feasibility is in source, not inferred from physical violations.')

    for i, failure in enumerate(closed['failures']):
        add('closedloop', None, {'method':str(failure.get('adaptive'))},
            note=f'Failure record index {i} in closedloop.json failures: '
                 + json.dumps(failure, ensure_ascii=False))

    helper = ROOT / 'src/outerloop/finite_memory.py'
    result = dict(
        purpose='Field-normalized index derived entirely from saved outputs; no rerun.',
        time_unit='seconds', null_policy='Unavailable or inapplicable; never substituted with zero.',
        source_row_index='Zero-based index in source JSON rows; null means aggregate/failure.',
        source_hashes=inputs,
        exporter_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        transitive_dependency=dict(path=str(helper),
            sha256_at_export=hashlib.sha256(helper.read_bytes()).hexdigest(),
            scope='Current dependency recorded at delivery; not a retroactive run-time hash.'),
        fields=FIELDS, rows=records,
    )
    (OUT/'delivery_records.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    with (OUT/'delivery_records.csv').open('w', newline='', encoding='utf-8') as f:
        writer=csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(records)
    print(json.dumps({'exported_records':len(records),
          'stages':{stage:sum(r['stage']==stage for r in records)
                    for stage in sorted({r['stage'] for r in records})}}))


if __name__ == '__main__':
    main()
