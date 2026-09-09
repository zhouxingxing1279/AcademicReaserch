#!/usr/bin/env python3
"""Regenerate every affine envelope cell and audit independent diagnostic points."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from smf_mpc.affine_model import AffineResidualMLP
from smf_mpc.residual_envelope import envelope,true_acceleration_interval

def main():
    folder=ROOT/'results/affine_model_a_20260909'
    m=AffineResidualMLP.from_dict(json.loads((folder/'model.json').read_text()))
    c=json.loads((ROOT/'configs/planar_baseline.json').read_text())
    cert,lo,hi,bound=envelope(m,c,14)
    saved=np.load(folder/'envelope_leaves.npz');old=np.load(ROOT/'results/model_a_20260909/envelope_leaves.npz')
    assert all(np.array_equal(saved[k],v) for k,v in [('lower',lo),('upper',hi),('acceleration_halfwidth',bound)])
    assert np.array_equal(old['lower'],lo) and np.array_equal(old['upper'],hi)
    assert np.all(bound<=old['acceleration_halfwidth']+1e-12)
    assert cert['acceleration_halfwidth']==json.loads((folder/'envelope.json').read_text())['acceleration_halfwidth']
    rng=np.random.default_rng(75003);count=10000;indices=rng.integers(0,len(lo),count)
    points=rng.uniform(lo[indices],hi[indices])
    tl,th=true_acceleration_interval(points,points)
    diff=np.abs(tl-m.predict(points[:,:5]))
    assert np.all(diff<=bound[indices]+1e-11)
    result={'all_passed':True,'cells_regenerated':len(lo),'all_cells_no_wider_than_legacy':True,
            'diagnostic_points':count,'seed':75003,'sample_max_abs_error':diff.max(axis=0).tolist(),
            'scope':'floating-point regression and diagnostics; not certification or formal test split',
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (folder/'artifact_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
