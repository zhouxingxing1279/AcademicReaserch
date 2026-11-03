#!/usr/bin/env python3
"""Exact circuit audit of the chapter-49 25-row Farkas witness.

Rebuilds the selected inequalities with rational arithmetic, verifies the
positive Farkas relation, proves the 25 coefficient rows have rank 24, and
enumerates the nondegenerate one-boundary active-set flips for the four
configuration rows used by the certificate.
"""
from fractions import Fraction as F
import argparse, json
import sympy as sp
import check_19pair_cc_seed_cone as cc
import check_19pair_cc_exact_farkas as cert


def sf(x): return F(int(x.p), int(x.q))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output', required=True); args=ap.parse_args()
    S2=cc.build_s2(); reps=cc.orientation_reps(S2); H=cc.seed_H(reps)
    _,_,V,acts=cc.enumerate_vertices(H)
    assert len(H)==38 and len(V)==160 and all(len(a)==4 for a in acts)
    Ce=[[F(v) for v in a] for a,_ in H]; nq=38; nv=160; nvar=nq+nv

    def Linv(i):
        ids=acts[i]
        M=sp.Matrix([[sp.Rational(v.numerator,v.denominator) for v in Ce[k]] for k in ids])
        return ids,M.inv()

    def row(meta):
        typ,i,j,z=meta; ids,L=Linv(i); out=[F(0)]*nvar
        if typ=='config':
            for k in range(4):
                for t,col in enumerate(ids): out[col]+=Ce[j][k]*sf(L[k,t])
            out[j]-=1; rhs=F(0)
        elif typ=='inv':
            T=F(z); ra=cc.base.mm(Ce[j],cc.base.A(T))
            for k in range(4):
                for t,col in enumerate(ids): out[col]+=ra[k]*sf(L[k,t])
            out[j]-=1
            out[nq+i]=sum(Ce[j][k]*cc.base.B[k] for k in range(4))
            rhs=-abs(sum(Ce[j][k]*cc.base.E[k] for k in range(4)))*(cc.base.d0+cc.base.c*T)
        else:
            k=j; sg=F(z)
            for t,col in enumerate(ids): out[col]+=sg*sf(L[k,t])
            rhs=[F(5),F(3),F('0.45'),F(2)][k]
        return out,rhs

    rows=[]; rhs=[]
    for meta in cert.SUPPORT:
        r,b=row(meta); rows.append(r); rhs.append(b)
    M=sp.Matrix([[sp.Rational(v.numerator,v.denominator) for v in r] for r in rows])
    rank=M.rank()
    combo=[sum(cert.MULT[k]*rows[k][j] for k in range(len(rows))) for j in range(nvar)]
    bsum=sum(cert.MULT[k]*rhs[k] for k in range(len(rows)))
    assert rank==24 and len(rows)==25
    assert all(y>0 for y in cert.MULT) and all(v==0 for v in combo)
    assert bsum==F(-3069803,88290)

    # Since nullity of M^T is one and the known null vector has no zero entry,
    # no proper subset of the 25 rows is linearly dependent: this is a circuit.
    flips=[]
    for typ,i,j,z in cert.SUPPORT:
        if typ!='config': continue
        old=acts[i]; union=old+[j]; candidates=[]
        for drop in old:
            new=sorted(k for k in union if k!=drop)
            N=sp.Matrix([[sp.Rational(v.numerator,v.denominator) for v in Ce[k]] for k in new])
            if N.det()!=0: candidates.append({'drop':drop,'new_active_set':new})
        flips.append({'vertex':i,'old_active_set':old,'entering_facet':j,
                      'nondegenerate_flip_candidates':candidates})
    assert len(flips)==4 and all(len(x['nondegenerate_flip_candidates'])==3 for x in flips)

    result={
      'status':'exact_positive_circuit_and_boundary_reduction',
      'support_rows':25,'coefficient_rank_exact':rank,'left_nullity':1,
      'all_farkas_multipliers_strictly_positive':True,
      'weighted_lhs_zero_exact':True,'weighted_rhs':str(bsum),
      'support_is_linear_circuit':True,
      'configuration_rows_in_circuit':4,
      'critical_configuration_boundaries':flips,
      'nondegenerate_single_boundary_flip_candidates':sum(len(x['nondegenerate_flip_candidates']) for x in flips),
      'conclusion':'The chapter-49 witness is a support-minimal positive linear circuit. Every one of its 25 inequalities is essential to this specific Farkas contradiction. Hence any adjacent-cone search capable of invalidating this certificate must cross at least one of the four configuration inequalities appearing in the circuit; auditing unrelated configuration boundaries cannot remove this exact obstruction.',
      'limitation':'Circuit minimality is exact for this Farkas witness, not a proof that other Farkas certificates cannot survive after a critical boundary crossing. The 12 active-set replacements are nondegenerate local flip candidates; a valid neighboring configuration cone must still be constructed and checked globally.'
    }
    open(args.output,'w').write(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))

if __name__=='__main__': main()
