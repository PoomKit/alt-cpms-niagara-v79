"""V7.5 cases: AI heartbeat stopwatch (H) + low delta-T syndrome guard / DP emulation (D).
usage: v75tests.py v75_fpt.bog v75.bog [out.csv]   (offline model, review aid - NOT native Niagara FPT)"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim7 import Model6
from simstart import faithful

FPT, SITE = sys.argv[1], sys.argv[2]
BASE = [(0.0, {'PlantEnable': True, 'PlantLoadPct': 20.0, 'CHWFlow': 150.0}), (1.0, {'BootQualified': True})]
BASE_FREE = [(0.0, {'PlantEnable': True, 'PlantLoadPct': 20.0}), (1.0, {'BootQualified': True})]     # flows from the emulation
rows = []


def row(cid, area, title, expect, ok, obs):
    rows.append({'id': cid, 'area': area, 'title': title, 'expectation': expect, 'observed': obs, 'result': 'PASS' if ok else 'FINDING'})
    print(f"{cid:5} {'PASS' if ok else 'FINDING':8} {title}\n      {obs}", flush=True)


def sim(bog, events, dur, extra=(), every=1.0, base=BASE):
    m = faithful(Model6(bog, ramps=False))
    tr = m.run(dur, list(base) + list(events), sample=list(extra), every=every)
    return m, tr


def at(tr, t, k):
    return next(s[k] for tt, s in tr if tt >= t - 1e-6)


def first(tr, cond, after=0.0):
    return next((t for t, s in tr if t >= after and cond(s)), None)


o = lambda m, n: m.lv(n)
HB = ['AI_LinkState', 'AI_HeartbeatAgeMin', 'AI_HeartbeatIntervalMin', 'AI_HeartbeatBeats', 'OperationMode', 'HeartbeatPreDisconnect',
      'HeartbeatDetectorStatus', 'AI_LinkDrops', 'AI_LinkUnstableAlarm', 'AI_HeartbeatStep1TooShortAlarm', 'AI_HeartbeatTimerPct']


def beats(*ts, k0=100):
    return [(t, {'HeartbeatTimestampSetpoint': float(k0 + i)}) for i, t in enumerate(ts)]


AI_ON = [(0.0, {'ModeCmd_UI': True, 'Sim_AiHeartbeatEnable': False})]

# H01 connected: measured API period, stopwatch
m, tr = sim(FPT, AI_ON + beats(10, 310, 610), 640, extra=HB)
ok = at(tr, 640, 'AI_LinkState') == 0 and abs(o(m, 'AI_HeartbeatIntervalMin') - 5.0) < 0.05 and 0.3 < o(m, 'AI_HeartbeatAgeMin') < 0.6 \
    and o(m, 'OperationMode') and at(tr, 300, 'AI_HeartbeatAgeMin') > 4.75 and at(tr, 305, 'AI_LinkState') == 3
row('H01', 'AI link', 'API every 5 min -> CONNECTED, period measured', 'after 2 APIs: state 0, AI mode; interval = 5.0 min; stopwatch resets on every API',
    ok, f"state@305 {at(tr, 305, 'AI_LinkState'):.0f} (1 API) -> @640 {o(m, 'AI_LinkState'):.0f}; interval {o(m, 'AI_HeartbeatIntervalMin'):.2f} min; "
        f"age before API {at(tr, 300, 'AI_HeartbeatAgeMin'):.2f} -> {o(m, 'AI_HeartbeatAgeMin'):.2f} min; mode {'AI' if o(m, 'OperationMode') else 'Local'}")

# H02 + H03 API stops -> Step 1 pre-disconnect (AI kept) -> Step 2 disconnect (Local) -> 1 API reconnecting -> 2 APIs connected
m, tr = sim(FPT, AI_ON + beats(10, 310, 610, 1500, 1800), 1850, extra=HB)
t_pre = first(tr, lambda s: s['AI_LinkState'] == 1, 610); t_dis = first(tr, lambda s: s['AI_LinkState'] == 2, 610)
t_loc = first(tr, lambda s: not s['OperationMode'], 610)
ok = t_pre is not None and 965 <= t_pre <= 975 and at(tr, 1200, 'OperationMode') and at(tr, 1200, 'HeartbeatPreDisconnect') \
    and t_dis is not None and 1325 <= t_dis <= 1335 and t_loc is not None and abs(t_loc - t_dis) <= 1 and at(tr, 1400, 'AI_HeartbeatBeats') == 0 \
    and at(tr, 1400, 'AI_LinkDrops') == 1
row('H02', 'AI link', 'No API: Step 1 = 6 min pre-disconnect, Step 2 = 12 min disconnect', 'last API @610 s: state 1 @~970 s (AI kept, warning); state 2 + LOCAL @~1330 s; beats cleared; drops = 1',
    ok, f"pre-disconnect @{t_pre}s (AI kept: {at(tr, 1200, 'OperationMode')}); disconnect @{t_dis}s, Local @{t_loc}s; beats {at(tr, 1400, 'AI_HeartbeatBeats'):.0f}; drops {at(tr, 1400, 'AI_LinkDrops'):.0f}; "
        f"timer bar @Step1 {at(tr, 975, 'AI_HeartbeatTimerPct'):.0f} % @Step2 {at(tr, 1335, 'AI_HeartbeatTimerPct'):.0f} %")
ok = at(tr, 1510, 'AI_LinkState') == 3 and not at(tr, 1510, 'OperationMode') and at(tr, 1840, 'AI_LinkState') == 0 and o(m, 'OperationMode')
row('H03', 'AI link', 'API back: RECONNECTING until 2 APIs, then CONNECTED + AI', '1st API: state 3, still Local; 2nd API: state 0, AI mode',
    ok, f"@1510 state {at(tr, 1510, 'AI_LinkState'):.0f} mode {'AI' if at(tr, 1510, 'OperationMode') else 'Local'}; @1840 state {o(m, 'AI_LinkState'):.0f} mode {'AI' if o(m, 'OperationMode') else 'Local'}")

# H04 Step 1 shorter than the real API period -> advisory alarm (after the persistence delay); pre-disconnect every cycle
m, tr = sim(FPT, AI_ON + [(0.0, {'HB_Step1_PreDisconnectMin': 4.0})] + beats(10, 310, 610, 910), 940, extra=HB)
t_al = first(tr, lambda s: s['AI_HeartbeatStep1TooShortAlarm'])
ok = t_al is not None and 330 <= t_al <= 345 and at(tr, 600, 'AI_LinkState') == 1 and o(m, 'OperationMode')
row('H04', 'AI link', 'Smart check: Step 1 (4 min) < 1.2 x measured period (5 min)', 'AI_HeartbeatStep1TooShortAlarm ~20 s (FPT) after the period is known; state 1 before each API',
    ok, f"alarm @{t_al}s; state before API @600 s = {at(tr, 600, 'AI_LinkState'):.0f}; mode {'AI' if o(m, 'OperationMode') else 'Local'}")

# H05 Step 2 set below Step 1 -> Step 2 = Step 1 + 1 min
m, tr = sim(FPT, AI_ON + [(0.0, {'HB_Step1_PreDisconnectMin': 2.0, 'HB_Step2_DisconnectMin': 1.0})] + beats(5, 10), 260, extra=HB)
t_pre = first(tr, lambda s: s['AI_LinkState'] == 1, 12); t_dis = first(tr, lambda s: s['AI_LinkState'] == 2, 12)
row('H05', 'AI link', 'Smart check: Step 2 never shorter than Step 1 + 1 min', 'Step1 2 min / Step2 set 1 min -> pre @~2 min, disconnect @~3 min after the last API',
    t_pre is not None and 128 <= t_pre <= 136 and t_dis is not None and 188 <= t_dis <= 196, f"last API @10 s: pre-disconnect @{t_pre}s, disconnect @{t_dis}s")

# H06 flapping link -> unstable alarm; cleared after a stable period (FPT 10 min instead of 24 h)
ev = AI_ON + [(0.0, {'HB_Step1_PreDisconnectMin': 1.0, 'HB_Step2_DisconnectMin': 2.0})] + beats(10, 20, 200, 210, 400, 410, *range(600, 1400, 50))
m, tr = sim(FPT, ev, 1400, extra=HB, every=2.0)
t_al = first(tr, lambda s: s['AI_LinkUnstableAlarm']); t_clr = first(tr, lambda s: not s['AI_LinkUnstableAlarm'], (t_al or 0) + 1)
ok = t_al is not None and 525 <= t_al <= 540 and t_clr is not None and 1245 <= t_clr <= 1260 and o(m, 'AI_LinkDrops') == 0
row('H06', 'AI link', 'Smart check: link dropped 3 times -> unstable alarm; cleared after a stable period', '3rd disconnect @~530 s -> alarm; 10 min (site 24 h) connected (from the 2nd API @650 s) -> drops 0, alarm clears @~1250 s',
    ok, f"alarm @{t_al}s (drops {at(tr, 540, 'AI_LinkDrops'):.0f}); cleared @{t_clr}s")

# H07 bumpless AI -> LOCAL (site rates): CHWST glides 0.3 K/min
K = ['CHW_LeavingTemperatureSetpoint_ACTIVE', 'OperationMode', 'ChwstLocalSelect', 'CHW_LeavingTemperatureSetpoint_AI', 'CHWDP_Setpoint_ACTIVE']
m, tr = sim(SITE, [(0.0, {'ModeCmd_UI': True}), (1300.0, {'ModeCmd_UI': False})], 1960, extra=K, every=5.0)
a900, a960, loc = at(tr, 1295, 'CHW_LeavingTemperatureSetpoint_ACTIVE'), at(tr, 1360, 'CHW_LeavingTemperatureSetpoint_ACTIVE'), o(m, 'ChwstLocalSelect')
ok = abs(a900 - o(m, 'CHW_LeavingTemperatureSetpoint_AI')) < 0.01 and not at(tr, 1305, 'OperationMode') and abs(a960 - (a900 + 0.3)) < 0.05 \
    and abs(o(m, 'CHW_LeavingTemperatureSetpoint_ACTIVE') - loc) < 0.01
row('H07', 'Mode', 'Bumpless AI -> LOCAL: setpoint glides, mode changes at once', 'user Local @1300 s: mode Local immediately; CHWST SP 7 -> 10 °C at 0.3 K/min (no step to the chillers)',
    ok, f"SP {a900:.2f} -> {a960:.2f} after 60 s -> {o(m, 'CHW_LeavingTemperatureSetpoint_ACTIVE'):.2f} (LOCAL {loc:.2f}); mode @1305 {'AI' if at(tr, 1305, 'OperationMode') else 'Local'}")

# H08 review finding: API period exactly 5 min (and 5 min 1 s) with the default Step 1 = 6 min must NOT raise the period alarm
res = []
for per in (300, 301):
    m, tr = sim(FPT, AI_ON + beats(*range(10, 1300, per)), 1300, extra=HB, every=5.0)
    res.append((per, o(m, 'AI_HeartbeatIntervalMin'), any(s['AI_HeartbeatStep1TooShortAlarm'] for t, s in tr), o(m, 'AI_LinkState')))
row('H08', 'AI link', 'Default Step 1 = 6 min with a 5 min API period: no false period alarm', 'period 300 s and 301 s: no Step-1-too-short alarm, state connected',
    all(not a and st == 0 for _, _, a, st in res), '; '.join(f"period {p} s: measured {iv:.2f} min alarm {a} state {st:.0f}" for p, iv, a, st in res))

# H09 station restart: APIs counted before the restart are forgotten -> AI only after 2 fresh APIs
m, tr = sim(FPT, AI_ON + beats(2, 4, 300), 330, extra=HB)
ok = at(tr, 200, 'AI_LinkState') == 3 and not at(tr, 200, 'OperationMode') and at(tr, 320, 'AI_LinkState') == 3
m2, tr2 = sim(FPT, AI_ON + beats(2, 10, 310), 330, extra=HB)
ok = ok and at(tr2, 200, 'AI_LinkState') == 3 and o(m2, 'AI_LinkState') == 0 and o(m2, 'OperationMode')
row('H09', 'AI link', 'Station restart: AI only after 2 fresh APIs', 'APIs inside the first 5 s after start-up are not counted; 2 APIs after that -> CONNECTED / AI',
    ok, f"APIs @2,4,300 s: state @200 {at(tr, 200, 'AI_LinkState'):.0f} @320 {at(tr, 320, 'AI_LinkState'):.0f}; APIs @2,10,310 s: @200 {at(tr2, 200, 'AI_LinkState'):.0f} -> {o(m2, 'AI_LinkState'):.0f} mode {'AI' if o(m2, 'OperationMode') else 'Local'}")

# H10 review finding: in AI mode a LOCAL-side change (optimiser off, LOCAL SP edited) must not move the ACTIVE setpoint
K = ['CHW_LeavingTemperatureSetpoint_ACTIVE', 'OperationMode', 'CHW_LeavingTemperatureSetpoint_AI']
m, tr = sim(SITE, [(0.0, {'ModeCmd_UI': True}), (1500.0, {'OptimizationEnable': False, 'CHW_LeavingTemperatureSetpoint_LOCAL': 12.0})], 1800, extra=K, every=5.0)
a0 = at(tr, 1495, 'CHW_LeavingTemperatureSetpoint_ACTIVE'); mx = max(abs(s['CHW_LeavingTemperatureSetpoint_ACTIVE'] - a0) for t, s in tr if t >= 1495)
row('H10', 'Mode', 'AI mode: a LOCAL-side change does not reach the plant', 'optimiser off + LOCAL SP 12 °C while in AI: ACTIVE stays at the AI setpoint',
    at(tr, 1495, 'OperationMode') and o(m, 'OperationMode') and mx < 0.01 and abs(a0 - o(m, 'CHW_LeavingTemperatureSetpoint_AI')) < 0.01,
    f"ACTIVE {a0:.2f} -> max deviation {mx:.3f} K after the LOCAL change (AI {o(m, 'CHW_LeavingTemperatureSetpoint_AI'):.2f})")

# ------------------------------------------------------------ delta-T guard
D = ['CHW_PlantDeltaT', 'CHW_DtGuardCutPct', 'CHW_DtGuardState', 'CHW_DtGuardActive', 'CHW_DtGuardHeld', 'CHWDP_Setpoint_EFFECTIVE', 'CHWDP_Setpoint_ACTIVE',
     'CHW_LowDtPersistAlarm', 'CHWDP', 'CHP01SpeedCmd', 'CHWDP_SensorInvalidAlarm', 'CHWFlow', 'Sim_CoilFlowRatio']
LOWDT = [(0.0, {'CHWS': 7.0, 'CHWR': 9.0, 'CHWDP_Setpoint_ACTIVE': 150.0})]
m, tr = sim(FPT, LOWDT + [(200.0, {'AirSide_ChwRequests': 3.0})], 260, extra=D)
ok = abs(at(tr, 190, 'CHW_DtGuardCutPct') - 30) < 0.5 and abs(at(tr, 190, 'CHWDP_Setpoint_EFFECTIVE') - 105) < 0.5 and at(tr, 190, 'CHW_DtGuardState') == 2 \
    and at(tr, 60, 'CHW_DtGuardCutPct') < at(tr, 120, 'CHW_DtGuardCutPct')
row('D01', 'dT guard', 'Low plant delta-T (2 K < 4 K) -> DP setpoint trimmed down gradually', 'cut rises to the 30 % maximum; EFFECTIVE = 150 x 0.7 = 105 kPa; state 2 (reducing)',
    ok, f"cut @60/120/190 s = {at(tr, 60, 'CHW_DtGuardCutPct'):.1f}/{at(tr, 120, 'CHW_DtGuardCutPct'):.1f}/{at(tr, 190, 'CHW_DtGuardCutPct'):.1f} %; "
        f"EFFECTIVE {at(tr, 190, 'CHWDP_Setpoint_EFFECTIVE'):.1f} kPa (ACTIVE 150); state {at(tr, 190, 'CHW_DtGuardState'):.0f}")
ok = at(tr, 203, 'CHW_DtGuardState') == 3 and at(tr, 203, 'CHW_DtGuardCutPct') < 0.01 and abs(at(tr, 203, 'CHWDP_Setpoint_EFFECTIVE') - 150) < 0.1 \
    and o(m, 'CHW_DtGuardState') == 3
row('D02', 'dT guard', 'Air side starving (AHU CHW requests) -> the whole cut removed at once', 'state 3 (held - AHU needs water); cut 0 within the 1 s (FPT) confirmation; EFFECTIVE = ACTIVE 150 kPa',
    ok, f"@199 s cut {at(tr, 199, 'CHW_DtGuardCutPct'):.1f} % -> @203 s state {at(tr, 203, 'CHW_DtGuardState'):.0f} cut {at(tr, 203, 'CHW_DtGuardCutPct'):.1f} % EFFECTIVE {at(tr, 203, 'CHWDP_Setpoint_EFFECTIVE'):.1f} kPa")

m, tr = sim(FPT, [(0.0, {'CHWS': 7.0, 'CHWR': 9.0, 'CHWDP_Setpoint_ACTIVE': 80.0})], 200, extra=D)
t_al = first(tr, lambda s: s['CHW_LowDtPersistAlarm'])
ok = abs(o(m, 'CHWDP_Setpoint_EFFECTIVE') - 60) < 0.1 and t_al is not None
row('D03', 'dT guard', 'Floor + persistent low delta-T alarm', 'ACTIVE 80 kPa: cut stops at DP minimum 60 kPa; low delta-T still there -> CHW_LowDtPersistAlarm (FPT 20 s; site 30 min)',
    ok, f"EFFECTIVE {o(m, 'CHWDP_Setpoint_EFFECTIVE'):.1f} kPa (floor 60); alarm @{t_al}s")

m, tr = sim(FPT, [(0.0, {'CHWS': 7.0, 'CHWR': 12.5, 'CHWDP_Setpoint_ACTIVE': 150.0})], 150, extra=D)
m2, tr2 = sim(FPT, LOWDT + [(0.0, {'DTG_Enable': 0.0})], 150, extra=D)
ok = o(m, 'CHW_DtGuardCutPct') == 0 and o(m, 'CHW_DtGuardState') == 1 and abs(o(m, 'CHWDP_Setpoint_EFFECTIVE') - 150) < 0.01 \
    and o(m2, 'CHW_DtGuardCutPct') == 0 and o(m2, 'CHW_DtGuardState') == 0
row('D04', 'dT guard', 'Normal delta-T / guard disabled -> no change', 'dT 5.5 K: state 1, cut 0, EFFECTIVE = ACTIVE; DTG_Enable = 0: state 0, cut 0',
    ok, f"dT {o(m, 'CHW_PlantDeltaT'):.1f} K: state {o(m, 'CHW_DtGuardState'):.0f} cut {o(m, 'CHW_DtGuardCutPct'):.1f} %; disabled: state {o(m2, 'CHW_DtGuardState'):.0f} cut {o(m2, 'CHW_DtGuardCutPct'):.1f} %")

# D07 review findings: failed CHWR sensor -> guard off + alarm; ACTIVE already at the DP minimum -> no 'persists' alarm (nothing was cut)
m, tr = sim(FPT, [(0.0, {'CHWS': 7.0, 'CHWR': 5.0, 'CHWDP_Setpoint_ACTIVE': 150.0})], 120, extra=D + ['CHWR_SensorInvalidAlarm'])
m2, tr2 = sim(FPT, [(0.0, {'CHWS': 7.0, 'CHWR': 9.0, 'CHWDP_Setpoint_ACTIVE': 60.0})], 200, extra=D)
ok = o(m, 'CHWR_SensorInvalidAlarm') and o(m, 'CHW_DtGuardState') == 0 and o(m, 'CHW_DtGuardCutPct') == 0 \
    and not any(s['CHW_LowDtPersistAlarm'] for t, s in tr2) and not o(m2, 'CHW_DtGuardActive') and abs(o(m2, 'CHWDP_Setpoint_EFFECTIVE') - 60) < 0.01
row('D07', 'dT guard', 'Bad CHWR sensor / nothing to cut', 'CHWR 5 °C < CHWS 7 °C: CHWR invalid alarm, guard off (state 0, cut 0); ACTIVE = DP min 60 kPa with low dT: no persists alarm, not shown as reducing',
    ok, f"CHWR alarm {o(m, 'CHWR_SensorInvalidAlarm')} state {o(m, 'CHW_DtGuardState'):.0f} cut {o(m, 'CHW_DtGuardCutPct'):.1f} %; "
        f"ACTIVE 60: EFFECTIVE {o(m2, 'CHWDP_Setpoint_EFFECTIVE'):.1f} active {o(m2, 'CHW_DtGuardActive')} persists alarm {any(s['CHW_LowDtPersistAlarm'] for t, s in tr2)}")

# D05 DP emulation + sensor validity
m, tr = sim(FPT, [(300.0, {'CHWDP': 0.0})], 330, extra=D)
inv_before = any(s['CHWDP_SensorInvalidAlarm'] for t, s in tr if t < 300)
dev = abs(at(tr, 295, 'CHWDP') - at(tr, 295, 'CHWDP_Setpoint_EFFECTIVE'))
ok = not inv_before and dev < 5 and o(m, 'CHWDP_SensorInvalidAlarm') and abs(o(m, 'CHP01SpeedCmd') - 80) < 0.5 and at(tr, 0.5, 'CHWDP') < 1
row('D05', 'DP loop', 'DP from the pump curve; sensor judged only with a pump proven', 'DP = 0 before the pump runs (no false invalid alarm); pump holds DP at the EFFECTIVE SP; DP forced 0 while running -> invalid alarm + 80 % fail-safe speed',
    ok, f"DP start {at(tr, 0.5, 'CHWDP'):.1f} kPa, invalid alarm before 300 s: {inv_before}; @295 s DP {at(tr, 295, 'CHWDP'):.1f} vs SP {at(tr, 295, 'CHWDP_Setpoint_EFFECTIVE'):.1f} kPa "
        f"(speed {at(tr, 295, 'CHP01SpeedCmd'):.1f} %); DP 0 -> alarm {o(m, 'CHWDP_SensorInvalidAlarm')} speed {o(m, 'CHP01SpeedCmd'):.1f} %")

# D06 closed loop: dirty coils / over-flow (low delta-T syndrome) with vs without the guard
res = {}
for en in (1.0, 0.0):
    m, tr = sim(FPT, [(0.0, {'Sim_LowDtFactor': 0.6, 'CHWDP_Setpoint_ACTIVE': 150.0, 'DTG_Enable': en})], 900, extra=D, every=10.0, base=BASE_FREE)
    avg = lambda k: sum(s[k] for t, s in tr if t >= 600) / len([1 for t, s in tr if t >= 600])
    res[en] = (avg('CHW_PlantDeltaT'), avg('CHWDP'), avg('CHWFlow'), avg('CHP01SpeedCmd'), avg('CHW_DtGuardCutPct'))
(dt1, dp1, q1, s1, c1), (dt0, dp0, q0, s0, c0) = res[1.0], res[0.0]
row('D06', 'dT guard', 'Low delta-T syndrome (coil dT x 0.6), guard ON vs OFF (emulation, 10-15 min)', 'guard ON: DP lower, less flow, lower pump speed, higher plant delta-T than OFF',
    c1 > 5 and dp1 < dp0 - 10 and q1 < q0 and s1 < s0 and dt1 > dt0,
    f"ON: dT {dt1:.2f} K, DP {dp1:.0f} kPa, flow {q1:.0f} m3/h, speed {s1:.1f} %, cut {c1:.1f} % | OFF: dT {dt0:.2f} K, DP {dp0:.0f} kPa, flow {q0:.0f} m3/h, speed {s0:.1f} %")

if len(sys.argv) > 3:
    with open(sys.argv[3], 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"{sum(r['result'] == 'PASS' for r in rows)}/{len(rows)} PASS")
