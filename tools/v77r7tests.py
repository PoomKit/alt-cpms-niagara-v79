"""V7.7 r7 cases: AI from cloud (writes at in10 / force), simulation released in CLOUD mode, heartbeat loss -> LOCAL.  (DP values in legacy kPa at the test boundary)"""
import sys, csv, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim7 import Model6
from simstart import faithful
BOG = sys.argv[1]; rows = []
BASE = [(0.0, {'PlantEnable': True, 'PlantLoadPct': 70.0, 'ModeCmd_UI': True}), (1.0, {'BootQualified': True})]
def row(cid, title, ok, obs):
    rows.append({'id': cid, 'title': title, 'observed': obs, 'result': 'PASS' if ok else 'FINDING'}); print(f"{cid:4} {'PASS' if ok else 'FINDING':8} {title}\n     {obs}", flush=True)
at = lambda tr, t, k: next(s[k] for tt, s in tr if tt >= t - 1e-6)
K = ['AI_Available', 'OperationMode', 'HeartbeatDetectorStatus', 'AI_LinkState', 'CHW_LeavingTemperatureSetpoint_AI', 'CHW_LeavingTemperatureSetpoint_ACTIVE',
     'CHW_LeavingTemperatureSetpoint_LOCAL', 'HeartbeatTimestampSetpoint', 'ChwstLocalSelect']
beats = [(float(t), {'HeartbeatTimestampSetpoint': 1.7e9 + t}) for t in range(30, 1500, 60)]
ev = [(2.0, {'AI_SourceCloud': True, 'CHW_LeavingTemperatureSetpoint_AI': 8.5, 'CHWDP_Setpoint_AI': 120.0, 'CDS_Setpoint_AI': 29.0})] + beats
m = faithful(Model6(BOG)); tr = m.run(2400.0, BASE + ev, sample=K, every=30.0)
row('C01', 'CLOUD mode: AI heartbeat + setpoint written by cloud -> AI mode, CHWST active = AI value',
    at(tr, 1400, 'OperationMode') and abs(at(tr, 1400, 'CHW_LeavingTemperatureSetpoint_ACTIVE') - 8.5) < 0.3,
    f"t1400 mode {at(tr, 1400, 'OperationMode')} link {at(tr, 1400, 'AI_LinkState')} CHWST_AI {at(tr, 1400, 'CHW_LeavingTemperatureSetpoint_AI')} active {at(tr, 1400, 'CHW_LeavingTemperatureSetpoint_ACTIVE'):.2f}")
row('C02', 'heartbeat stops at 1470 s -> disconnect (12 min) -> LOCAL path (LOCAL SP + reset) drives CHWST',
    not at(tr, 2370, 'OperationMode') and at(tr, 2370, 'AI_LinkState') == 2 and abs(at(tr, 2370, 'CHW_LeavingTemperatureSetpoint_ACTIVE') - at(tr, 2370, 'ChwstLocalSelect')) < 0.3,
    f"t2370 mode {at(tr, 2370, 'OperationMode')} link {at(tr, 2370, 'AI_LinkState')} active {at(tr, 2370, 'CHW_LeavingTemperatureSetpoint_ACTIVE'):.2f} local path {at(tr, 2370, 'ChwstLocalSelect'):.2f} (LOCAL SP {at(tr, 2370, 'CHW_LeavingTemperatureSetpoint_LOCAL'):.2f})")
m = faithful(Model6(BOG)); tr = m.run(900.0, BASE + [(2.0, {'AI_SourceCloud': True})], sample=K, every=30.0)
row('C03', 'CLOUD mode, nothing written by cloud: simulation ramps / beats released, no AI mode',
    not at(tr, 890, 'AI_Available') and not at(tr, 890, 'OperationMode'),
    f"t890 AI_Available {at(tr, 890, 'AI_Available')} HB {at(tr, 890, 'HeartbeatTimestampSetpoint')} CHWST_AI {at(tr, 890, 'CHW_LeavingTemperatureSetpoint_AI')}")
if len(sys.argv) > 2:
    with open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
