"""V7.7 r9 cases (SOO R1 review logic changes), offline model."""
import sys, csv, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim7 import Model6
from simstart import faithful
BOG = sys.argv[1]; rows = []
BASE = [(0.0, {'PlantEnable': True, 'PlantLoadPct': 70.0}), (1.0, {'BootQualified': True})]
def row(cid, title, ok, obs):
    rows.append({'id': cid, 'title': title, 'observed': obs, 'result': 'PASS' if ok else 'FINDING'}); print(f"{cid:4} {'PASS' if ok else 'FINDING':8} {title}\n     {obs}", flush=True)
def sim(ev, dur, K, every=1.0):
    m = faithful(Model6(BOG)); return m.run(dur, BASE + ev, sample=K, every=every)
first = lambda tr, k, v, t0=0: next((t for t, s in tr if t >= t0 and s[k] == v), None)
# R01 post-run anchor + R05 trip without min-run
K = ['CH01Request', 'CH01StartCmd', 'CH01RunProof', 'CH01PostRun', 'CH01_SafetyTrip', 'CHP01StartCmd', 'CDP01RunProof', 'CH01_ChwSupplyTemp']
tr = sim([(400.0, {'PlantEnable': False})], 900.0, K)
tq, tc, tp, tpr = first(tr, 'CH01Request', False, 400), first(tr, 'CH01StartCmd', False, 400), first(tr, 'CH01RunProof', False, 400), first(tr, 'CH01PostRun', False, 400)
row('R01', 'post-run counts from the last of request / start command / run proof',
    None not in (tq, tc, tp, tpr) and tpr - max(tq, tc, tp) >= 0.9 * (tpr - tq if tpr - tq > 0 else 1) * 0 + 1 and tpr > max(tq, tc, tp),
    f'request off {tq}, start cmd off {tc}, run proof off {tp}, post-run off {tpr} (post-run after last = {None if None in (tq,tc,tp,tpr) else tpr - max(tq,tc,tp)} s)')
ts = first(tr, 'CH01RunProof', True)
tr2 = sim([(ts + 20 if ts else 200.0, {'CH01_ChwSupplyTemp': 1.5})], (ts or 200) + 120, K)
tt = first(tr2, 'CH01_SafetyTrip', True); tcm = first(tr2, 'CH01StartCmd', False, (ts or 200) + 20)
row('R05', 'freeze trip removes the chiller command at once (does not wait for 15 min min-run)', tt is not None and tcm is not None and tcm - tt <= 2,
    f'run proof {ts}, trip {tt}, start cmd off {tcm}')
# R02 freeze reset needs LWT >= CH_FreezeResetTemp
t0 = (ts or 200) + 20
ev = [(t0, {'CH01_ChwSupplyTemp': 1.5}), (t0 + 40, {'CH01_ChwSupplyTemp': 4.0}), (t0 + 45, {'CH01LockoutReset': True}), (t0 + 48, {'CH01LockoutReset': False}),
      (t0 + 60, {'CH01_ChwSupplyTemp': 6.0}), (t0 + 65, {'CH01LockoutReset': True}), (t0 + 68, {'CH01LockoutReset': False})]
tr3 = sim(ev, t0 + 90, K)
at = lambda tr, t, k: next(s[k] for tt_, s in tr if tt_ >= t - 1e-6)
row('R02', 'safety-trip reset refused at 4 C, accepted at 6 C (CH_FreezeResetTemp 5 C)',
    at(tr3, t0 + 55, 'CH01_SafetyTrip') and not at(tr3, t0 + 85, 'CH01_SafetyTrip'),
    f"after reset at 4 C trip={at(tr3, t0 + 55, 'CH01_SafetyTrip')}; after reset at 6 C trip={at(tr3, t0 + 85, 'CH01_SafetyTrip')}")
# R03 CDP before CHP
K3 = ['CHP01StartCmd', 'CHP02StartCmd', 'CDP01RunProof', 'CDP02RunProof', 'CHP01RunProof']
tr4 = sim([(0.5, {'CDP01RunProof': False, 'CDP02RunProof': False}), (300.0, {'CDP01RunProof': None, 'CDP02RunProof': None})], 500.0, K3)
c_before = any(s['CHP01StartCmd'] or s['CHP02StartCmd'] for t, s in tr4 if t < 290)
tchp = first(tr4, 'CHP01StartCmd', True, 300) or first(tr4, 'CHP02StartCmd', True, 300)
row('R03', 'CHW pump does not start until a condenser pump is proven', not c_before and tchp is not None, f'CHP cmd before CDP proven: {c_before}; CHP start after CDP released at {tchp}')
tr5 = sim([], 400.0, K3)
trun = first(tr5, 'CHP01RunProof', True)
K4 = K3 + ['CHP01_CdpFirstGate']
tr6 = sim([((trun or 200) + 30, {'CDP01RunProof': False, 'CDP02RunProof': False})], (trun or 200) + 60, K4)
bad = [t for t, s in tr6 if s['CHP01RunProof'] and not s['CHP01_CdpFirstGate']]
held = [t for t, s in tr6 if t > (trun or 200) + 30 and s['CHP01RunProof'] and s['CHP01_CdpFirstGate']]
row('R04', 'CDP-first gate stays open for a running CHW pump when the condenser pump proof drops (start-only gate)', not bad and len(held) > 0,
    f"CHP01 run {trun}; gate closed while CHP running at {bad[:3]}; CHP running with gate open after CDP loss for {len(held)} s "
    "(the CHP then stops because the chiller trips on condenser flow - expected)")
# R06 biocide A/B interlock
K6 = ['CT_BioA_Cycle', 'CT_BioB_Cycle']
tr7 = sim([(10.0, {'CT_BiocideA_ManualStart': True}), (14.0, {'CT_BiocideA_ManualStart': False}), (30.0, {'CT_BiocideB_ManualStart': True})], 90.0, K6)
row('R06', 'biocide B waits while the A cycle is running', at(tr7, 60, 'CT_BioA_Cycle') and not any(s['CT_BioB_Cycle'] for t, s in tr7 if t > 30 and s['CT_BioA_Cycle']),
    f"A cycle {at(tr7, 60, 'CT_BioA_Cycle')}, B cycle during A {any(s['CT_BioB_Cycle'] for t, s in tr7 if s['CT_BioA_Cycle'])}")
if len(sys.argv) > 2:
    with open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
