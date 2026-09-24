#!/usr/bin/env python3
"""Audit whether the chapter-46 inherited-offset realization can serve as a
single configuration seed for freely varying all 38 raw halfspace offsets.

This is a structural audit.  It reads the archived chapter-46 geometry result
and checks the prerequisite that the raw orientation list and the active facet
configuration are not being conflated.  A CC vertex-affine map is valid only
inside the configuration cone generated from one seed configuration; it does
not authorize crossing a boundary at which previously redundant rows become
facets.
"""
import argparse, json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default='../results/s2_plus_5pair_fixed_offsets_20260924/checks.json')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    data = json.loads(Path(args.input).read_text())
    raw = int(data['raw_augmented_halfspaces'])
    active = int(data['nonredundant_augmented_facets'])
    inactive = raw - active
    assert raw == 38 and active == 30 and inactive == 8
    result = {
        'status': 'structural_configuration_seed_audit',
        'raw_halfspaces': raw,
        'active_facets_at_inherited_seed': active,
        'redundant_rows_at_inherited_seed': inactive,
        'single_seed_free_38_offset_claim_valid': False,
        'conclusion': 'The inherited-offset realization has 38 raw rows but only 30 active facets. A vertex-affine CC map built from this seed is certified only inside its configuration cone; it cannot be used as a certificate for arbitrary independent offset changes that activate any of the 8 currently redundant rows.',
        'next_requirement': 'Choose and audit an entirely-simple seed configuration, construct its vertex maps and E q <= 0 cone, then solve the RCI LP only inside that cone. Crossing to a different facet/vertex incidence requires a different seed/cone.'
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
