#!/usr/bin/env python3
"""Independent finite checks on actual trained weights and saved envelope leaves."""
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from smf_mpc.neural_model import ResidualMLP
from smf_mpc.residual_envelope import envelope
from smf_mpc.plant import aerodynamic_acceleration
from smf_mpc.data import rng_for


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('training',type=Path);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    config=json.loads((ROOT/'configs/planar_baseline.json').read_text());model=ResidualMLP.from_dict(json.loads((args.training/'model.json').read_text()))
    saved=json.loads((args.training/'envelope.json').read_text());cert,lo,hi,bound=envelope(model,config,saved['depth'])
    leaves=np.load(args.training/'envelope_leaves.npz');same=(cert==saved and np.array_equal(lo,leaves['lower']) and np.array_equal(hi,leaves['upper']) and np.array_equal(bound,leaves['acceleration_halfwidth']))
    rng=rng_for(30000,'model_a_global_diagnostic');points=rng.uniform(cert['domain_lower'],cert['domain_upper'],(5000,7))
    actual=[]
    for q in points:
        x=np.array([0,2,3*q[0],3*q[1],.45*q[2],0]);u=np.array([9.81*(q[3]+1),.08*q[4]])
        actual.append(aerodynamic_acceleration(x,u,q[5:]))
    errors=np.abs(np.array(actual)-model.predict(points[:,:5]));sample_max=errors.max(axis=0)
    jac_error=0.;remainder_excess=0.
    for q in points[:100,:5]:
        eps=1e-6;fd=np.column_stack([(model.predict(q+eps*d)-model.predict(q-eps*d))/(2*eps) for d in np.eye(5)])
        jac_error=max(jac_error,float(np.max(np.abs(fd-model.jacobian(q)))))
        radius=np.array([.02,.02,.02,0,0]);second=.5*model.directional_second_bound(q-radius,q+radius,radius)
        for _ in range(10):
            delta=rng.uniform(-1,1,5)*radius
            residual=np.abs(model.predict(q+delta)-model.predict(q)-model.jacobian(q)@delta)
            remainder_excess=max(remainder_excess,float(np.max(residual-second)))
    result={'kind':'FINITE_ARTIFACT_CHECK_NOT_FORMAL_CERTIFICATION','weights_sha256':model.digest(),'diagnostic_seed':30000,
            'partition_regenerated_identically':same,'global_diagnostic_samples':5000,'global_sampled_max_error':sample_max.tolist(),
            'sample_envelope_excess':np.maximum(sample_max-np.array(cert['acceleration_halfwidth']),0).tolist(),
            'trained_jacobian_max_error':jac_error,'trained_remainder_sample_excess':max(remainder_excess,0),
            'all_passed':bool(same and np.all(sample_max<=cert['acceleration_halfwidth']) and jac_error<1e-7 and remainder_excess<1e-10),
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
    if not result['all_passed']:raise SystemExit(1)


if __name__=='__main__':main()
