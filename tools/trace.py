import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim6 import Model6
m=Model6(sys.argv[1], ramps=False)
def tr(n,d,ind=0,seen=set()):
    t=m.typ(n)
    ins={k:(v[0][0],v[1]) for k,v in m.inc[n].items()}
    print('  '*ind+f"{n} [{t}] "+', '.join(f"{k}<-{s}.{sl}" for k,(s,sl) in ins.items()))
    if d==0 or n in seen: return
    seen.add(n)
    for k,(s,sl) in ins.items():
        if s in m.C: tr(s,d-1,ind+1,seen)
for n in sys.argv[3:]: tr(n,int(sys.argv[2])); print()
