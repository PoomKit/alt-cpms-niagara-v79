"""V7.2 (= V7.1 cases + V7.2: pump valves follow the pump, settable staging).  V7.1 additions: CT entering TT / make-up / high-high, VFD details, VSD min/max, set selection and daily/weekly rotation.
usage: v71tests.py v71_fpt.bog v71.bog [out.csv]   (offline model, review aid — NOT native Niagara FPT)"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim7 import Model6
from simstart import faithful

FPT, SITE = sys.argv[1], sys.argv[2]
BASE = [(0.0, {'PlantEnable': True, 'PlantLoadPct': 20.0, 'CHWFlow': 150.0}), (1.0, {'BootQualified': True})]
rows = []


def row(cid, area, title, expect, ok, obs):
    rows.append({'id': cid, 'area': area, 'title': title, 'expectation': expect, 'observed': obs, 'result': 'PASS' if ok else 'FINDING'})
    print(f"{cid:5} {'PASS' if ok else 'FINDING':8} {title}\n      {obs}", flush=True)


def sim(bog, events, dur, extra=(), every=1.0, base=True):
    m = faithful(Model6(bog, ramps=False))
    tr = m.run(dur, (BASE if base else []) + list(events), sample=list(extra), every=every)
    return m, tr


def setout(**kv):
    def f(m):
        for k, v in kv.items(): m.out[k] = v
    return f


def at(tr, t, k):
    return next(s[k] for tt, s in tr if tt >= t - 1e-6)


o = lambda m, n: m.out[n]
sch_on = setout(Sch_AHU=True, Sch_FCU=True, Sch_EF=True, Sch_CarPark=True)

# N01 CT entering / leaving TT, range, approach
m, tr = sim(FPT, [], 120)
ok = abs(o(m, 'CT01_InletTemp') - o(m, 'CDR')) < 0.01 and abs(o(m, 'CT01_Range') - (o(m, 'CT01_InletTemp') - o(m, 'CT01_OutletTemp'))) < 0.01 \
    and abs(o(m, 'CT01_Approach') - (o(m, 'CT01_OutletTemp') - o(m, 'OA_WetBulb'))) < 0.01
row('N01', 'CT', 'CT entering + leaving TT, range and approach', 'CT01 inlet = CDW return while valve open; range = in - out; approach = out - OA WB',
    ok, f"CT01 in {o(m, 'CT01_InletTemp'):.2f} out {o(m, 'CT01_OutletTemp'):.2f} range {o(m, 'CT01_Range'):.2f} approach {o(m, 'CT01_Approach'):.2f} (CDR {o(m, 'CDR'):.2f})")

# N02 make-up valve 70 -> 80 % with latch
K = ['CT01_MakeupValveCmd', 'CT01_BasinLevel']
m, tr = sim(FPT, [(0.0, {'CT01_BasinLevel': 75.0}), (10.0, {'CT01_BasinLevel': 65.0}), (20.0, {'CT01_BasinLevel': 75.0}), (30.0, {'CT01_BasinLevel': 85.0}),
                  (40.0, {'CT01_BasinLevel': 75.0})], 50, extra=K)
seq = [at(tr, t, 'CT01_MakeupValveCmd') for t in (8, 18, 28, 38, 48)]
row('N02', 'CT', 'Basin make-up valve (open < 70 %, close > 80 %)', 'level 75 closed, 65 open, 75 stays open (latched), 85 closed, 75 stays closed',
    seq == [False, True, True, False, False], f"valve at 75/65/75/85/75 % = {seq}")

# N03 high-high (overflow float) closes make-up and raises a critical alarm
m, tr = sim(FPT, [(0.0, {'CT01_BasinLevel': 60.0}), (20.0, {'CT01_HighLevelSwitch': True})], 50, extra=K + ['CT01BasinHighHighLevelAlarm', 'CT01BasinHighLevelAlarm'])
ok = at(tr, 18, 'CT01_MakeupValveCmd') and not o(m, 'CT01_MakeupValveCmd') and o(m, 'CT01BasinHighHighLevelAlarm') and not at(tr, 25, 'CT01BasinHighHighLevelAlarm')
row('N03', 'CT', 'Basin HIGH-HIGH / overflow switch', 'make-up forced closed immediately; HH alarm after 10 s (Critical); high alarm too',
    ok, f"valve before {at(tr, 18, 'CT01_MakeupValveCmd')} after {o(m, 'CT01_MakeupValveCmd')}; HH@25s {at(tr, 25, 'CT01BasinHighHighLevelAlarm')} HH@50s {o(m, 'CT01BasinHighHighLevelAlarm')} high {o(m, 'CT01BasinHighLevelAlarm')}")

# N04 level transmitter failure -> make-up closed (float switches remain)
m, tr = sim(FPT, [(0.0, {'CT01_BasinLevel': -5.0})], 20, extra=K)
row('N04', 'CT', 'Level transmitter out of range', 'make-up valve not driven by a failed transmitter (closed)', not o(m, 'CT01_MakeupValveCmd'), f"valve {o(m, 'CT01_MakeupValveCmd')}")

# N05 VSD max / min on the CHW pump
K = ['CHP01SpeedCmd', 'CHP01StartCmd']
m, tr = sim(FPT, [(0.0, {'CHWDP': 20.0}), (100.0, {'CHP01_MaxSpeed': 50.0}), (200.0, {'CHP01_MinSpeed': 60.0})], 300, extra=K)
a, b, c = at(tr, 95, 'CHP01SpeedCmd'), at(tr, 195, 'CHP01SpeedCmd'), o(m, 'CHP01SpeedCmd')
row('N05', 'VSD', 'CHP01 min / max speed', 'low DP drives speed up; max 50 % caps it; min 60 % above max -> 60 % (min wins)',
    a > 55 and abs(b - 50) < 0.5 and abs(c - 60) < 0.5, f"speed {a:.1f} % -> max 50: {b:.1f} % -> min 60: {c:.1f} %")

# N06 CT fan and CDP min / max
m, tr = sim(FPT, [(0.0, {'CT01_MinSpeed': 45.0, 'CDP01_MaxSpeed': 60.0})], 200, extra=['CT01SpeedCmd', 'CDP01SpeedCmd', 'CT01StartCmd'])
ok = (not o(m, 'CT01StartCmd') or o(m, 'CT01SpeedCmd') >= 44.9) and abs(o(m, 'CDP01SpeedCmd') - 60) < 0.5
row('N06', 'VSD', 'CT fan min / CDP max', 'CT01 >= 45 % when running (0 when stopped); CDP01 fixed 75 % capped at 60 %',
    ok, f"CT01 run={o(m, 'CT01StartCmd')} {o(m, 'CT01SpeedCmd'):.1f} %; CDP01 {o(m, 'CDP01SpeedCmd'):.1f} %")

# N07 AHU fan max, CPEF01 max ignored in fire
m, tr = sim(SITE, [(0.0, sch_on), (0.0, {'AHU01_MaxSpeed': 55.0, 'AHU01_DuctStatic': 50.0, 'CPEF01_MaxSpeed': 60.0, 'CPEF01_CO': 60.0}),
                   (200.0, {'FireAlarmSignal': True})], 320, extra=['AHU01_SpeedCmd', 'CPEF01_SpeedCmd'], every=5.0, base=False)
a, b = at(tr, 195, 'AHU01_SpeedCmd'), at(tr, 195, 'CPEF01_SpeedCmd')
row('N07', 'VSD', 'AHU01 max; CPEF01 max vs fire', 'AHU01 capped 55 %; CPEF01 capped 60 % normally but 100 % in fire (smoke clearance)',
    abs(a - 55) < 0.5 and abs(b - 60) < 0.5 and o(m, 'CPEF01_SpeedCmd') > 99, f"AHU01 {a:.1f} %; CPEF01 {b:.1f} % -> fire {o(m, 'CPEF01_SpeedCmd'):.1f} %")

# N08 VFD details: output V, temperature alarm, fault code
m, tr = sim(FPT, [(60.0, {'CHP01_VfdTemp': 80.0, 'CT01_VfdFaultCode': 12.0})], 80, extra=['CHP01_VfdOverTempAlarm'])
ok = abs(at(tr, 55, 'CHP01_VfdOverTempAlarm') - 0) < 1e-9 and o(m, 'CHP01_VfdOverTempAlarm') and o(m, 'CT01_VfdFaultCodeActive') and o(m, 'CHP01_VfdOutputV') > 100
row('N08', 'VFD', 'VFD detail points', 'output V ~ 4 V/% when running; heatsink 80 degC -> alarm; fault code 12 -> flag',
    ok, f"CHP01 {o(m, 'CHP01_VfdOutputV'):.0f} V DC {o(m, 'CHP01_VfdDcBusV'):.0f} V; over-temp {o(m, 'CHP01_VfdOverTempAlarm')}; CT01 code flag {o(m, 'CT01_VfdFaultCodeActive')}")

# N09 set selection: Set 2 runs CH02 + CHP02 + CDP02 + CT02 (linked)
K = ['CH02StartSuccess', 'CHP02StartCmd', 'CDP02StartCmd', 'CT02StartCmd', 'CHP01StartCmd']
m, tr = sim(FPT, [(0.0, {'LeadCH01': False})], 150, extra=K)
ok = o(m, 'CH02StartSuccess') and o(m, 'CHP02StartCmd') and o(m, 'CDP02StartCmd') and o(m, 'CT02StartCmd') and not o(m, 'CHP01StartCmd') and not o(m, 'LeadSet')
row('N09', 'Set', 'Lead set 2 selected (pools linked)', 'CH02 + CHP02 + CDP02 + CT02 run; set-1 pumps off',
    ok, ' '.join(f"{k}={int(o(m, k))}" for k in K) + f" LeadSet={o(m, 'LeadSet')}")

# N10 independent pools keep their own lead (runtime / manual) with set 2
m, tr = sim(FPT, [(0.0, {'LeadCH01': False, 'Set_LinkPools': False})], 150, extra=K)
ok = o(m, 'CH02StartSuccess') and o(m, 'CHP01StartCmd') and not o(m, 'CHP02StartCmd')
row('N10', 'Set', 'Set 2, pools independent', 'CH02 runs, pools keep their own lead (01 by runtime)', ok, ' '.join(f"{k}={int(o(m, k))}" for k in K))

# N11 daily rotation: day counter odd -> set 2 leads (plant stays up during change-over)
K = ['CH01StartSuccess', 'CH02StartSuccess', 'CHP02StartCmd', 'LeadSet']
m, tr = sim(FPT, [(0.0, {'RotationMode_Daily': True, 'RotationMode_Runtime': False}), (150.0, setout(RotationDayCounter=1.0))], 450, extra=K)
before, after = at(tr, 145, 'LeadSet'), o(m, 'LeadSet')
ok = before and not after and o(m, 'CH02StartSuccess') and o(m, 'CHP02StartCmd')
row('N11', 'Rotation', 'Daily rotation at 00:00', 'day 0 -> set 1; day 1 -> set 2 (CH02 + CHP02)', ok,
    f"LeadSet day0={before} day1={after} CH02={o(m, 'CH02StartSuccess')} CHP02={o(m, 'CHP02StartCmd')}")

# N12 weekly rotation: day 1..6 set 1, day 7 set 2, day 14 set 1
m, tr = sim(FPT, [(0.0, {'RotationMode_Weekly': True, 'RotationMode_Runtime': False}), (20.0, setout(RotationDayCounter=1.0)),
                  (40.0, setout(RotationDayCounter=7.0)), (60.0, setout(RotationDayCounter=14.0))], 80, extra=['LeadSet'])
seq = [at(tr, t, 'LeadSet') for t in (18, 38, 58, 78)]
row('N12', 'Rotation', 'Weekly rotation', 'day 0/1 set 1, day 7 set 2, day 14 set 1', seq == [True, True, False, True], f"LeadSet day 0/1/7/14 = {seq}")

# N13 runtime mode has priority over daily (no double swap)
m, tr = sim(FPT, [(0.0, {'RotationMode_Daily': True, 'RotationMode_Runtime': True}), (20.0, setout(RotationDayCounter=1.0))], 40, extra=['LeadSet'])
row('N13', 'Rotation', 'Runtime mode + daily both on', 'daily request suppressed while runtime rotation is selected', not o(m, 'DailyRotationRequest'),
    f"DailyRotationRequest={o(m, 'DailyRotationRequest')}")

# N14 pump valves follow the pump: lead pump valves open before start, standby pump valves stay closed
K = ['CHP01_SuctionMVFb', 'CHP01_DischargeMVFb', 'CHP01StartCmd', 'CHP02_SuctionMVFb', 'CHP02_DischargeMVFb', 'CHP02StartCmd']
m, tr = sim(FPT, [], 90, extra=K, every=0.5)
t_open = next((t for t, s_ in tr if s_['CHP01_SuctionMVFb'] >= 80 and s_['CHP01_DischargeMVFb'] >= 80), None)
t_start = next((t for t, s_ in tr if s_['CHP01StartCmd']), None)
ok = t_open is not None and t_start is not None and t_start >= t_open and o(m, 'CHP02_SuctionMVFb') < 1 and not o(m, 'CHP02StartCmd') \
    and not o(m, 'CDP02_SuctionMVCmd') and o(m, 'CDP01_SuctionMVCmd')
row('N14', 'Valves', 'Pump valves follow the pump (on/off)', 'lead pump: valves open -> proven -> start; standby pumps: valves CLOSED',
    ok, f"CHP01 valves open @{t_open}s start @{t_start}s; CHP02 fb {o(m, 'CHP02_SuctionMVFb'):.0f} %; CDP01 cmd {o(m, 'CDP01_SuctionMVCmd')} CDP02 cmd {o(m, 'CDP02_SuctionMVCmd')}")

# N14b pump stops -> valves close after the close delay
m, tr = sim(FPT, [(60.0, {'PlantEnable': False})], 300, extra=['CHP01RunProof', 'CHP01_SuctionMVCmd'], every=0.5)
t_stop = next((t for t, s_ in tr if t > 60 and not s_['CHP01RunProof']), None)
t_close = next((t for t, s_ in tr if t > 60 and not s_['CHP01_SuctionMVCmd']), None)
row('N14b', 'Valves', 'Pump stop -> valves close', 'valves close after the pump stopped (+ close delay), never before',
    t_stop is not None and t_close is not None and t_close >= t_stop and o(m, 'CHP01_SuctionMVFb') < 1, f"pump stopped @{t_stop}s, valve close cmd @{t_close}s, fb {o(m, 'CHP01_SuctionMVFb'):.0f} %")

# N15 CHP01 suction valve stuck closed -> command failure -> pool uses CHP02, chiller keeps running
m, tr = sim(FPT, [(0.0, {'CHP01_SuctionMVFb': 0.0})], 150, extra=['CHP01StartCmd', 'CHP02StartCmd', 'CH01StartSuccess'])
ok = o(m, 'CHP01_MVFailLatchedAlarm') and o(m, 'CHP02StartCmd') and not o(m, 'CHP01StartCmd') and o(m, 'CH01StartSuccess')
row('N15', 'Valves', 'CHP01 suction valve stuck closed', 'valve command-failure alarm; CHP01 treated as faulted; CHP02 runs; chiller runs',
    ok, f"latched alarm={o(m, 'CHP01_MVFailLatchedAlarm')} CHP01={o(m, 'CHP01StartCmd')} CHP02={o(m, 'CHP02StartCmd')} CH01={o(m, 'CH01StartSuccess')}")

# N16 service isolation of the standby pump
m, tr = sim(FPT, [(0.0, {'CHP02_ServiceIsolate': True})], 120, extra=['CHP02_SuctionMVCmd'])
ok = not o(m, 'CHP02_SuctionMVCmd') and not o(m, 'CHP02_DischargeMVCmd') and o(m, 'CHP02_SuctionMVFb') < 1 and o(m, 'CHP01StartCmd') and o(m, 'CHP_PoolDegradedAlarm')
row('N16', 'Valves', 'CHP02 isolated for service', 'both CHP02 valves closed, CHP02 out of pool (standby-lost alarm), CHP01 runs',
    ok, f"CHP02 valves cmd {o(m, 'CHP02_SuctionMVCmd')}/{o(m, 'CHP02_DischargeMVCmd')} fb {o(m, 'CHP02_SuctionMVFb'):.0f} %; degraded={o(m, 'CHP_PoolDegradedAlarm')}")

# N17 tower outlet valve stuck closed
m, tr = sim(FPT, [(0.0, {'CT01_OutletMVFb': 0.0})], 150, extra=['CT01StartCmd', 'CT02StartCmd'])
ok = o(m, 'CT01_OutletMVFailAlarm') and not o(m, 'CT01StartCmd') and o(m, 'CT02StartCmd') and o(m, 'CH01StartSuccess')
row('N17', 'Valves', 'CT01 outlet valve stuck closed', 'CT01 fan not started (no water path), alarm; CT02 carries the load; chiller runs',
    ok, f"alarm={o(m, 'CT01_OutletMVFailAlarm')} CT01={o(m, 'CT01StartCmd')} CT02={o(m, 'CT02StartCmd')} CH01={o(m, 'CH01StartSuccess')}")

# N18 modulating valves: evaporator FCV (flow limit) and condenser head-pressure valve
m, tr = sim(FPT, [(0.0, {'CH01_ChwFlow': 200.0, 'CH01_CdwEnteringTemp': 28.0}), (120.0, {'CH01_ChwFlow': 320.0, 'CH01_CdwEnteringTemp': 16.0})], 240,
            extra=['CH01_ChwFCVCmd', 'CH01_CdwHPVCmd'])
a, b = at(tr, 115, 'CH01_ChwFCVCmd'), at(tr, 115, 'CH01_CdwHPVCmd')
c_, d_ = o(m, 'CH01_ChwFCVCmd'), o(m, 'CH01_CdwHPVCmd')
row('N18', 'Valves', 'Modulating FCV + head-pressure valve', 'flow 200 < 260 -> FCV 100 %; flow 320 -> FCV throttles (>= 20 %); ECWT 28 -> HPV 100 %; ECWT 16 -> HPV 44 %',
    abs(a - 100) < 0.5 and 20 <= c_ < 90 and abs(b - 100) < 0.5 and abs(d_ - 44) < 1, f"FCV {a:.0f} -> {c_:.0f} %; HPV {b:.0f} -> {d_:.0f} %")

# N19 settable staging: start the next chiller at X % (default 90); 75 % load -> no stage 2; X = 70 -> stage 2
m, tr = sim(FPT, [(0.0, {'PlantLoadPct': 50.0, 'Stage_UpLoadPct': 90.0}), (10.0, {'PlantLoadPct': 75.0})], 150, extra=['Stage2Request', 'CH02StartCmd'])
a = o(m, 'Stage2Request')
m2, tr2 = sim(FPT, [(0.0, {'PlantLoadPct': 50.0, 'Stage_UpLoadPct': 70.0}), (10.0, {'PlantLoadPct': 75.0})], 150, extra=['Stage2Request', 'CH02StartCmd'])
row('N19', 'Staging', 'Start next chiller at settable load %', 'load 75 % with setting 90 % -> 1 chiller; setting 70 % -> stage 2, CH02 started',
    not a and o(m2, 'Stage2Request') and o(m2, 'CH02StartCmd'), f"setting 90: stage2={a}; setting 70: stage2={o(m2, 'Stage2Request')} CH02 cmd={o(m2, 'CH02StartCmd')}")

# N20 settable stage-down
m, tr = sim(FPT, [(0.0, {'PlantLoadPct': 95.0}), (100.0, {'PlantLoadPct': 55.0, 'Stage_DownLoadPct': 50.0}), (200.0, {'Stage_DownLoadPct': 60.0})], 320,
            extra=['Stage2Request'])
row('N20', 'Staging', 'Stop lag chiller at settable load %', 'stage 2 at 95 %; 55 % with stop setting 50 % -> stays; setting 60 % -> stage 1',
    at(tr, 95, 'Stage2Request') and at(tr, 195, 'Stage2Request') and not o(m, 'Stage2Request'),
    f"@95s {at(tr, 95, 'Stage2Request')} @195s {at(tr, 195, 'Stage2Request')} @320s {o(m, 'Stage2Request')}")

# N21 site timers, valves follow pump: lead CHW pump trips while running -> standby valves stroke, standby starts, plant recovers by itself
STEADY = {'PlantLoadPct': 50.0, 'CHWFlow': 150.0, 'ModeCmd_UI': False}
SB = [(0.0, STEADY), (10.0, {'BootQualified': True}), (15.0, {'PlantEnable': True})]
m, tr = sim(SITE, SB + [(600.0, {'CHP01VfdFault': True})], 1200, extra=['CH01StartSuccess', 'CH02StartSuccess', 'CHP02StartCmd', 'CHP02_SuctionMVFb'], every=1.0, base=False)
t_v = next((t for t, s_ in tr if t > 600 and s_['CHP02_SuctionMVFb'] >= 80), None)
t_p = next((t for t, s_ in tr if t > 600 and s_['CHP02StartCmd']), None)
back = o(m, 'CH01StartSuccess') or o(m, 'CH02StartSuccess')
row('N21', 'Valves', 'Site timers: lead CHP trips, valves follow pump', 'standby valves open (stroke) -> CHP02 starts -> plant recovers automatically (a chiller flow trip is possible)',
    t_v is not None and t_p is not None and t_p >= t_v and back and o(m, 'CHP02StartCmd'), f"CHP02 valves open @{t_v}s, CHP02 start @{t_p}s, chiller running at end={back}")

if len(sys.argv) > 3:
    with open(sys.argv[3], 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"{sum(r['result'] == 'PASS' for r in rows)}/{len(rows)} PASS")
