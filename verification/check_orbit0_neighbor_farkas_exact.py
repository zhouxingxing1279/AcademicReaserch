#!/usr/bin/env python3
from fractions import Fraction as F
import argparse,json
SUPPORT=[("config",17,5,None),("inv",20,11,"981/200"),("inv",34,3,"981/200"),("inv",35,3,"981/200"),("inv",49,6,"981/200"),("inv",49,34,"2943/200"),("inv",57,6,"981/200"),("inv",57,24,"2943/200"),("inv",65,6,"981/200"),("inv",65,18,"981/200"),("inv",76,6,"981/200"),("inv",76,20,"981/200"),("hard",0,3,"1"),("hard",5,3,"-1")]
MULT=[F(x) for x in ["94176000/391546301","1440000000/391546301","1120000000/391546301","320000000/391546301","69219360/391546301","3920000000/391546301","12713760/391546301","2160000000/391546301","470880/391546301","240000000/391546301","4237920/391546301","2160000000/391546301","33903360/391546301","1412640/391546301"]]
ROWS=[
({2:F(-1),3:F(1,25),9:F(10000,981),16:F(-10000,981)},F(0)),
({3:F(2943,250000),5:F(-1),12:F(7,3),17:F(-4,3)},F(-6254383,160000000)),
({1:F(-1),10:F(3,2),11:F(1),12:F(-3,2)},F(-6254383,160000000)),
({1:F(-1),10:F(3,2),11:F(-7,2),16:F(3)},F(-6254383,160000000)),
({68:F(1)},F(0)),
({2:F(2943,10000),3:F(-8829,500000),68:F(-8829,500000)},F(-6731149,160000000)),
({76:F(1)},F(0)),
({12:F(-1),17:F(1),76:F(-2943,500000)},F(-6731149,160000000)),
({3:F(-2),84:F(1)},F(0)),
({3:F(2943,250000),9:F(-1),12:F(2),17:F(-1),84:F(-981,500000)},F(-6254383,160000000)),
({3:F(-2),95:F(1)},F(0)),
({1:F(1),2:F(-981,2000),3:F(981,100000),10:F(-1),95:F(-981,500000)},F(-6254383,160000000)),
({3:F(1)},F(2)),
({1:F(-500000,981),5:F(1000000,981),9:F(-500000,981)},F(2))]
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--output",required=True);a=ap.parse_args()
 assert len(ROWS)==len(MULT)==14 and all(y>0 for y in MULT)
 combo={}
 for y,(row,b) in zip(MULT,ROWS):
  for j,x in row.items():combo[j]=combo.get(j,F(0))+y*x
 rhs=sum(y*b for y,(row,b) in zip(MULT,ROWS))
 assert all(v==0 for v in combo.values()) and rhs==F(-1)
 out={"status":"exact_orbit0_farkas_identity","support_rows":14,"weighted_lhs_zero_exact":True,"weighted_rhs_exact":"-1","torque_bound_rows_used":0,"support":[{"row":list(m),"multiplier":str(y)} for m,y in zip(SUPPORT,MULT)],"scope":"Exact for the frozen rational primal rows after 19-pair elimination; H/V incidence discovery remains numerical."}
 open(a.output,"w").write(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
if __name__=="__main__":main()
