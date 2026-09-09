#!/usr/bin/env python3
"""Rebound fixed model A, retaining every partition cell and original envelope."""
import argparse, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from smf_mpc.affine_model import AffineResidualMLP
from smf_mpc.residual_envelope import envelope

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists() and any(a.output.iterdir()):p.error('output must be empty')
    a.output.mkdir(parents=True,exist_ok=True)
    original=ROOT/'results/model_a_20260909/model.json'
    model=AffineResidualMLP.from_dict(json.loads(original.read_text()))
    config=json.loads((ROOT/'configs/planar_baseline.json').read_text())
    cert,lo,hi,bound=envelope(model,config,14)
    cert['algorithm']='balanced_midpoint_cycle_7_axes_affine_ibp_intersection_v1'
    (a.output/'model.json').write_bytes(original.read_bytes())
    (a.output/'envelope.json').write_text(json.dumps(cert,indent=2)+'\n')
    np.savez_compressed(a.output/'envelope_leaves.npz',lower=lo,upper=hi,acceleration_halfwidth=bound)
    sources=[ROOT/'src/smf_mpc/affine_model.py',ROOT/'src/smf_mpc/neural_model.py',ROOT/'src/smf_mpc/residual_envelope.py',Path(__file__)]
    manifest={'model_unchanged':True,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'artifact_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in a.output.iterdir() if p.is_file()}}
    (a.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(cert))
if __name__=='__main__':main()
