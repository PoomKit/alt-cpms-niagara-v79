"""V7.8 r11 cases (remaining SOO items), offline model. usage: v78r11tests.py <v78_fpt.bog> [out.csv]"""
import sys, csv, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim7 import Model6
from simstart import faithful
BOG = sys.argv[1]; rows = []
BASE = [(0.0, {'PlantEnable': True, 'PlantLoadPct': 70.0}), (1.0, {'BootQualified': True})]


def row(cid, title, ok, obs):
    rows.append({'id': cid, 'title': title, 'observed': obs, 'result': 'PASS' if ok else 'FINDING'})
    print(f"{cid:4} {'PASS' if ok else 'FINDING':8} {title}\n     {obs}", flush=True)


def sim(ev, dur, K, every=1.0):
    m = faithful(Model6(BOG)); return m.run(dur, BASE + ev, sample=K, every=every)


first = lambda tr, k, v, t0=0: next((t for t, s in tr if t >= t0 and s[k] == v), None)
at = lambda tr, t, k: next(s[k] for tt_, s in tr if tt_ >= t - 1e-6)
tr0 = sim([], 200.0, ['CH01RunProofSelected']); trun = first(tr0, 'CH01RunProofSelected', True) or 30
# F01 trip run-on
K = ['CH01_TripRunOnUse', 'CH01_SafetyTrip', 'CH01_SafetyTripIn']
tr = sim([(trun + 20, {'CH01_ChwSupplyTemp': 1.5})], trun + 90, K)
tt = first(tr, 'CH01_SafetyTrip', True) or trun; te = first(tr, 'CH01_SafetyTripIn', False, tt)
a, b = at(tr, te + 10, 'CH01_TripRunOnUse'), at(tr, te + 35, 'CH01_TripRunOnUse')
row('F01', 'after a freeze trip the water keeps flowing for the run-on time (test 20 s) after the trip signal ends', a and not b,
    f'trip {tt}, trip signal ended {te}; run-on 10 s later {a}, 35 s later {b}')
# F02 uncommanded run
K = ['CHP01_UncommandedRunAlarm', 'CHP01StartCmd']
tr = sim([(0.5, {'PlantEnable': False}), (30.0, {'CHP01RunProof': True})], 80.0, K)
row('F02', 'pump running without a command -> alarm', (not at(tr, 75, 'CHP01StartCmd')) and at(tr, 75, 'CHP01_UncommandedRunAlarm'),
    f"CHP01 cmd {at(tr, 75, 'CHP01StartCmd')}, alarm {at(tr, 75, 'CHP01_UncommandedRunAlarm')}")
# F03 AI message number
K = ['AI_SeqOk', 'AI_SeqOld', 'AI_SeqStale']
tr = sim([(1.0, {'AI_RequireSeq': True}), (5.0, {'AI_PayloadSeq': 10.0}), (30.0, {'AI_PayloadSeq': 5.0}), (40.0, {'AI_PayloadSeq': 11.0})], 130.0, K)
o1, ok2, st = at(tr, 35, 'AI_SeqOld'), at(tr, 45, 'AI_SeqOk'), at(tr, 125, 'AI_SeqStale')
row('F03', 'AI message number: going backwards = old payload rejected; not changing 60 s (test) = stale', o1 and ok2 and st,
    f'old after 10 -> 5: {o1}; ok after 11: {ok2}; stale 85 s later: {st}')
# F04 maintenance
K = ['CH01StartCmd', 'CH02StartCmd']
tr = sim([(0.5, {'CH01_Maintenance': True})], 150.0, K)
row('F04', 'CH01 in maintenance is never started; CH02 runs instead', not any(s['CH01StartCmd'] for t, s in tr) and any(s['CH02StartCmd'] for t, s in tr),
    f"CH01 started {any(s['CH01StartCmd'] for t, s in tr)}, CH02 started at {first(tr, 'CH02StartCmd', True)}")
# F05 condenser first
K = ['CH01ValveOpenCmd', 'CH01CDWFlowBridge', 'CH01CdwValveOpenCmd', 'CH01RunProofSelected']
tr = sim([(0.5, {'CH_CondenserFirst': True})], 200.0, K, every=0.5)
tv, tf, tc = first(tr, 'CH01ValveOpenCmd', True), first(tr, 'CH01CDWFlowBridge', True), first(tr, 'CH01CdwValveOpenCmd', True)
row('F05', 'condenser-first option: CHW valve opens only after condenser flow is proven, chiller still starts',
    None not in (tv, tf, tc) and tc <= tf <= tv and first(tr, 'CH01RunProofSelected', True) is not None,
    f'CDW valve {tc}, CDW flow proven {tf}, CHW valve {tv}, run {first(tr, "CH01RunProofSelected", True)}')
# F06 start failure cause
K = ['CH01_StartFailCause', 'CH01StartCmd']
tr = sim([(0.5, {'CH01RunProof': False})], 120.0, K)
c = at(tr, 115, 'CH01_StartFailCause')
row('F06', 'start failure (no run proof) is remembered as cause 10 = compressor did not start', c == 10, f'CH01_StartFailCause {c}')
# F07 HPV off
K = ['CH01_CdwHPVCmd', 'CH01CdwValveOpenCmd']
tr = sim([(0.5, {'CH_HpvEnable': False})], 60.0, K)
row('F07', 'HPV switched off -> valve 100 % while the condenser valve is open', at(tr, 55, 'CH01CdwValveOpenCmd') and at(tr, 55, 'CH01_CdwHPVCmd') >= 99,
    f"HPV {at(tr, 55, 'CH01_CdwHPVCmd'):.0f} %")
# F08 trim & respond ignore
K = ['TR_UnitsRunning', 'TR_IgnoreSel', 'TR_IgnoreRequests']
tr = sim([], 60.0, K); n, sel, ig = at(tr, 55, 'TR_UnitsRunning'), at(tr, 55, 'TR_IgnoreSel'), at(tr, 55, 'TR_IgnoreRequests')
row('F08', 'requests ignored only when 3 or more air-side units run', (sel == 0) if n < 3 else (sel == ig), f'units running {n:.0f}, ignore used {sel:.0f} (setting {ig:.0f})')
# F09 fill total
K = ['CHW_FillTotal', 'CHW_FillTotalHighAlarm']
tr = sim([(1.0, {'CHW_FillFlow': 60.0})], 200.0, K)
tot = at(tr, 195, 'CHW_FillTotal')
row('F09', 'fill water totaliser adds gpm x 1 min every minute (60 m3/h = 264 gpm) and alarms above 500 gal', 500 <= tot <= 1100 and at(tr, 195, 'CHW_FillTotalHighAlarm'),
    f'total after ~3 min {tot:.0f} gal, alarm {at(tr, 195, "CHW_FillTotalHighAlarm")}')
# F10 E-stop needs reset
K = ['Plant_HardInhibit']
tr = sim([(0.5, {'Plant_EstopNeedsReset': True}), (30.0, {'Plant_EmergencyStop': True}), (60.0, {'Plant_EmergencyStop': False})], 100.0, K)
tr2 = sim([(30.0, {'Plant_EmergencyStop': True}), (60.0, {'Plant_EmergencyStop': False})], 100.0, K)
row('F10', 'option on: plant stays inhibited after E-stop release until reset; option off: restarts', at(tr, 95, 'Plant_HardInhibit') and not at(tr2, 95, 'Plant_HardInhibit'),
    f"option on {at(tr, 95, 'Plant_HardInhibit')}, option off {at(tr2, 95, 'Plant_HardInhibit')}")
# F11 FCU break-before-make + zone count
K = ['FCU01_FanHighCmd', 'FCU01_FanMedCmd', 'FCU01_FanLowCmd', 'Zone_ValidCount']
tr = sim([], 300.0, K, every=0.5)
two = [t for t, s in tr if sum(bool(s[k]) for k in K[:3]) > 1]
row('F11', 'FCU fan relays never two at once; valid room sensors counted', not two and at(tr, 295, 'Zone_ValidCount') >= 10,
    f'overlap times {two[:3]}, valid sensors {at(tr, 295, "Zone_ValidCount"):.0f}')
# F12 drive speed vs command
K = ['CHP01_SpeedNotFollowingAlarm', 'CHP01RunProof', 'CHP01SpeedCmd', 'CHP01_SpeedFeedbackHz']
tr = sim([], 120.0, K); tr2 = sim([(60.0, {'CHP01_SpeedFeedbackHz': 10.0})], 120.0, K)
row('F12', 'CHW pump drive speed not following the command -> alarm (none in normal running)',
    not any(s['CHP01_SpeedNotFollowingAlarm'] for t, s in tr) and at(tr2, 115, 'CHP01_SpeedNotFollowingAlarm'),
    f"normal: cmd {at(tr, 115, 'CHP01SpeedCmd'):.0f} % fb {at(tr, 115, 'CHP01_SpeedFeedbackHz'):.1f} Hz alarm {at(tr, 115, 'CHP01_SpeedNotFollowingAlarm')}; fb forced 10 Hz -> {at(tr2, 115, 'CHP01_SpeedNotFollowingAlarm')}")
# F13 SIM / FIELD changed while running
K = ['IO_SourceChangedWhileRunningAlarm', 'PlantRunRequest']
tr = sim([(100.0, {'IO_AnyFieldSts': True})], 130.0, K)
row('F13', 'data source switched while the plant runs -> alarm (stays until reset)', not at(tr, 95, 'IO_SourceChangedWhileRunningAlarm') and at(tr, 125, 'IO_SourceChangedWhileRunningAlarm'),
    f"before {at(tr, 95, 'IO_SourceChangedWhileRunningAlarm')}, after {at(tr, 125, 'IO_SourceChangedWhileRunningAlarm')}")
if len(sys.argv) > 2:
    with open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
