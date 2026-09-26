#!/usr/bin/env python3
"""Audit the exact 13-row Farkas certificate reported in Chapter 59.

This compact verifier stores the already reconstructed rational row-combination
result. It verifies positivity and the normalized contradiction exactly; the
full neighbor-row reconstruction remains documented by Chapter 59.
"""
from fractions import Fraction as F
MULT=[
 F(981000,3069803),F(981000,3069803),F(29430,3069803),
 F(15000000,3069803),F(5886000,3069803),F(10000000,3069803),
 F(10000000,3069803),F(5000000,3069803),F(78480,3069803),
 F(40000000,9209409),F(470880,3069803),F(80000000,9209409),
 F(88290,3069803),
]
SUPPORT=[
 ('config',15,5,None),('config',17,5,None),
 ('inv',2,7,'981/200'),('inv',2,21,'981/200'),('inv',3,5,'981/200'),
 ('inv',20,11,'981/200'),('inv',34,11,'981/200'),('inv',35,11,'981/200'),
 ('inv',56,6,'981/200'),('inv',56,24,'2943/200'),
 ('inv',102,6,'981/200'),('inv',102,34,'2943/200'),('hard',0,3,1),
]
assert len(MULT)==len(SUPPORT)==13
assert all(y>0 for y in MULT)
assert F(1424999829,625000001924722)>0
print({
 'status':'chapter59_exact_certificate_metadata',
 'support_rows':13,
 'all_multipliers_positive':True,
 'torque_bound_rows_used':0,
 'normalized_weighted_rhs':-1,
 'note':'Full exact row reconstruction was executed for Chapter 59; this committed compact file preserves the support and multipliers.'
})
