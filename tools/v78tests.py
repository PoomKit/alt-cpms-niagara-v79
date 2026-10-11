"""V7.8 trial logic cases (SOO improvement list), offline model. usage: v78tests.py <v78_fpt.bog> [out.csv]"""
import sys, csv, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim7 import Model6
from simstart import faithful
BOG = sys.argv[1]; rows = []
BASE = [(0.0, {'PlantEnable': True, 'PlantLoadPct': 70.0}), (1.0, {'BootQualified': True})]


def row(cid, title, ok, obs):
    rows.append({'id': cid, 'title': title, 'observed': obs, 'result': 'PASS' if ok else 'FINDING'})
    print(f"{cid:4} {'PASS' if ok else 'FINDING':8} {title}\n     {obs}", flush=True)


def sim(ev, dur, K, every=1.0, base=BASE):
    m = faithful(Model6(BOG)); return m.run(dur, base + ev, sample=K, every=every)


first = lambda tr, k, v, t0=0: next((t for t, s in tr if t >= t0 and s[k] == v), None)
at = lambda tr, t, k: next(s[k] for tt_, s in tr if tt_ >= t - 1e-6)

# N01 plant reason
K = ['Plant_NotRunningReason', 'PlantPermissive', 'CH01RunProofSelected']
tr = sim([(0.0, {'PlantEnable': False}), (60.0, {'PlantEnable': True}), (200.0, {'Plant_EmergencyStop': True}), (240.0, {'Plant_EmergencyStop': None})], 300.0, K)
v_off, v_on, v_es = at(tr, 50, 'Plant_NotRunningReason'), at(tr, 190, 'Plant_NotRunningReason'), at(tr, 230, 'Plant_NotRunningReason')
row('N01', 'plant reason: switched off = 1, running = 0, emergency stop = 2', (v_off, v_on, v_es) == (1, 0, 2),
    f'off {v_off}, running {v_on} (permissive {at(tr, 190, "PlantPermissive")}), E-stop {v_es}')
# N02 AI reason
K = ['AI_NotUsedReason', 'OperationModeAI']
tr = sim([(30.0, {'ModeCmd_UI': True})], 60.0, K)
a0, a1 = at(tr, 20, 'AI_NotUsedReason'), at(tr, 55, 'AI_NotUsedReason')
row('N02', 'AI reason: LOCAL selected = 1, AI selected without heartbeat = 2', (a0, a1) == (1, 2), f'LOCAL {a0}, AI requested {a1}, AI in use {at(tr, 55, "OperationModeAI")}')
# N03 chiller waiting-for codes
K = ['CH01_WaitingFor', 'CH01Request', 'CH01RunProofSelected']
tr = sim([], 400.0, K)
codes = []
for t, s in tr:
    if s['CH01_WaitingFor'] not in codes: codes.append(s['CH01_WaitingFor'])
trun = first(tr, 'CH01RunProofSelected', True)
row('N03', 'CH01 waiting-for code steps through the start sequence and returns to 0 when running',
    trun is not None and len(codes) >= 3 and at(tr, trun + 5, 'CH01_WaitingFor') == 0 and all(0 <= c <= 10 for c in codes),
    f'codes seen in order {codes}; run proof at {trun}')
# N04 stage-down needs CHW supply on target
K = ['LagNotNeeded', 'Stg_LagNotNeededOk', 'CHWS', 'CHW_LeavingTemperatureSetpoint_ACTIVE']
tr = sim([(150.0, {'PlantLoadPct': 20.0}), (250.0, {'CHWS': 12.0}), (300.0, {'Stg_DownNeedsChwsOk': False})], 330.0, K)
l1, ok1 = at(tr, 245, 'LagNotNeeded'), at(tr, 245, 'Stg_LagNotNeededOk')
l2, ok2 = at(tr, 295, 'LagNotNeeded'), at(tr, 295, 'Stg_LagNotNeededOk')
ok3 = at(tr, 325, 'Stg_LagNotNeededOk')
row('N04', 'second chiller released only when CHW supply is on target (switch off = V7.7 behaviour)',
    l1 and ok1 and l2 and not ok2 and ok3, f'low load + CHWS ok -> release {ok1}; CHWS 12 C -> release {ok2}; check switched off -> release {ok3}')
# N05 bypass opens for one evaporator short of flow
K = ['Byp_EvapLowFlowActive', 'CHW_BypassValveCmd', 'CH01RunProofSelected', 'CH01_ChwFlow']
tr = sim([], 400.0, K); trun = first(tr, 'CH01RunProofSelected', True) or 250
tr = sim([(trun + 30, {'CH01_ChwFlow': 30.0})], trun + 120, K)
b0, b1, act = at(tr, trun + 25, 'CHW_BypassValveCmd'), at(tr, trun + 115, 'CHW_BypassValveCmd'), at(tr, trun + 115, 'Byp_EvapLowFlowActive')
row('N05', 'CH01 evaporator below its own minimum flow -> bypass valve driven open', act and b1 > 50,
    f'bypass before {b0:.1f} %, after {b1:.1f} %, boost active {act}')
# N06 CDP boost on low measured condenser flow
K = ['CDP_LowFlowBoostActive', 'CDP_SpeedDemand', 'CDP_UseLoop', 'CDW_Flow']
tr = sim([], 700.0, K)
tu = first(tr, 'CDP_UseLoop', True) or 600
tr = sim([(tu + 30, {'CDW_Flow': 10.0})], tu + 80, K)
s0, s1, act = at(tr, tu + 25, 'CDP_SpeedDemand'), at(tr, tu + 75, 'CDP_SpeedDemand'), at(tr, tu + 75, 'CDP_LowFlowBoostActive')
row('N06', 'condenser flow measured below minimum -> CDP to fixed (design) speed', act and s1 >= 99.0,
    f'CDP loop from {tu}; speed before {s0:.1f} %, after {s1:.1f} %, boost {act}')
# N07 CHW setpoint held during dehumidification
K = ['CHW_LeavingTemperatureSetpoint_ACTIVE', 'Chwst_DehumHoldActive']
NODH = {'AHU01_DehumActive': False, 'AHU02_DehumActive': False}
tr = sim([(1.0, dict(NODH, OptimizationEnable=False, CHW_LeavingTemperatureSetpoint_LOCAL=9.0)), (120.0, {'AHU01_DehumActive': True})], 240.0, K)
c0, c1 = at(tr, 115, 'CHW_LeavingTemperatureSetpoint_ACTIVE'), at(tr, 235, 'CHW_LeavingTemperatureSetpoint_ACTIVE')
row('N07', 'CHW setpoint 9 C is limited to 7 C while an AHU dehumidifies', abs(c0 - 9.0) < 0.3 and abs(c1 - 7.0) < 0.3,
    f'setpoint before {c0:.2f} C, during dehumidification {c1:.2f} C (hold {at(tr, 235, "Chwst_DehumHoldActive")})')
# N08 basin level disagreement
K = ['CT01_LevelDisagreeAlarm', 'CT01_BasinLevel']
tr = sim([(20.0, {'CT01_LowLowLevelSwitch': True})], 60.0, K)
row('N08', 'low-low switch made while the level transmitter reads normal -> disagreement alarm',
    not at(tr, 18, 'CT01_LevelDisagreeAlarm') and at(tr, 55, 'CT01_LevelDisagreeAlarm'), f'level {at(tr, 55, "CT01_BasinLevel"):.0f} %, alarm {at(tr, 55, "CT01_LevelDisagreeAlarm")}')
# N09 manual CHW dose time limit
K = ['CHW_ChemDosePumpCmd', 'CHW_ChemManualTimeoutAlarm', 'CHP_AnyProven']
tr = sim([(200.0, {'CHW_ChemFeederOpen': True})], 260.0, K)
p1, p2, al = at(tr, 210, 'CHW_ChemDosePumpCmd'), at(tr, 250, 'CHW_ChemDosePumpCmd'), at(tr, 250, 'CHW_ChemManualTimeoutAlarm')
row('N09', 'manual CHW dose stops by itself after the time limit (test timing 20 s)', p1 and not p2 and al,
    f'pump 10 s after manual {p1}, after 50 s {p2}, alarm {al}')
# N10 first-out
K = ['Plant_FirstOut', 'CH01_SafetyTrip', 'CH01RunProofSelected']
tr = sim([], 400.0, K); trun = first(tr, 'CH01RunProofSelected', True) or 250
tr = sim([(trun + 20, {'CH01_ChwSupplyTemp': 1.5}), (trun + 60, {'Plant_EmergencyStop': True})], trun + 90, K)
f1, f2 = at(tr, trun + 50, 'Plant_FirstOut'), at(tr, trun + 85, 'Plant_FirstOut')
row('N10', 'first-out keeps the first trip (CH01 freeze = 4) when an emergency stop follows', f1 == 4 and f2 == 4, f'after freeze {f1}, after E-stop {f2}')
# N11 hottest zone
K = ['Zone_AHU01_HottestTemp', 'Zone_AHU01_AvgTemp']
tr = sim([], 30.0, K)
h, a = at(tr, 25, 'Zone_AHU01_HottestTemp'), at(tr, 25, 'Zone_AHU01_AvgTemp')
row('N11', 'hottest zone temperature is shown and is not below the average', h is not None and h >= a - 0.01, f'hottest {h:.2f} C, average {a:.2f} C')
if len(sys.argv) > 2:
    with open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
