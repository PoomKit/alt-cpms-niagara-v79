"""V7.3 (= V7.2 cases, tower VSD per cell) + T-cases for V7.3: tower cells / SOO staging / low-low / make-up / treatment / bypass / zones.
V7.2 (= V7.1 cases + V7.2: pump valves follow the pump, settable staging).  V7.1 additions: CT entering TT / make-up / high-high, VFD details, VSD min/max, set selection and daily/weekly rotation.
usage: v73tests.py v73_fpt.bog v73.bog [out.csv]   (offline model, review aid — NOT native Niagara FPT)"""
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


o = lambda m, n: m.lv(n)
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
m, tr = sim(FPT, [(0.0, {'CT01_01_MinSpeed': 45.0, 'CT01_02_MaxSpeed': 15.0, 'CDP01_MaxSpeed': 60.0})], 200, extra=['CT01_01SpeedCmd', 'CDP01SpeedCmd', 'CT01StartCmd'])
ok = o(m, 'CT01_01StartCmd') and o(m, 'CT01_01SpeedCmd') >= 44.9 and o(m, 'CT01_02SpeedCmd') <= 20.01 and abs(o(m, 'CDP01SpeedCmd') - 60) < 0.5
row('N06', 'VSD', 'CT cell fan min / max, CDP max', 'CT-01/01 >= 45 % (its own min); CT-01/02 max 15 % below min 20 % -> 20 % (min wins); CDP01 capped at 60 %',
    ok, f"CT01/01 {o(m, 'CT01_01SpeedCmd'):.1f} % CT01/02 {o(m, 'CT01_02SpeedCmd'):.1f} %; CDP01 {o(m, 'CDP01SpeedCmd'):.1f} %")

# N07 AHU fan max, CPEF01 max ignored in fire
m, tr = sim(SITE, [(0.0, sch_on), (0.0, {'AHU01_MaxSpeed': 55.0, 'AHU01_DuctStatic': 50.0, 'CPEF01_MaxSpeed': 60.0, 'CPEF01_CO': 60.0}),
                   (200.0, {'FireAlarmSignal': True})], 320, extra=['AHU01_SpeedCmd', 'CPEF01_SpeedCmd'], every=5.0, base=False)
a, b = at(tr, 195, 'AHU01_SpeedCmd'), at(tr, 195, 'CPEF01_SpeedCmd')
row('N07', 'VSD', 'AHU01 max; CPEF01 max vs fire', 'AHU01 capped 55 %; CPEF01 capped 60 % normally but 100 % in fire (smoke clearance)',
    abs(a - 55) < 0.5 and abs(b - 60) < 0.5 and o(m, 'CPEF01_SpeedCmd') > 99, f"AHU01 {a:.1f} %; CPEF01 {b:.1f} % -> fire {o(m, 'CPEF01_SpeedCmd'):.1f} %")

# N08 VFD details: output V, temperature alarm, fault code
m, tr = sim(FPT, [(60.0, {'CHP01_VfdTemp': 80.0, 'CT01_01_VfdFaultCode': 12.0})], 80, extra=['CHP01_VfdOverTempAlarm'])
ok = abs(at(tr, 55, 'CHP01_VfdOverTempAlarm') - 0) < 1e-9 and o(m, 'CHP01_VfdOverTempAlarm') and o(m, 'CT01_01_VfdFaultCodeActive') and o(m, 'CHP01_VfdOutputV') > 100
row('N08', 'VFD', 'VFD detail points', 'output V ~ 4 V/% when running; heatsink 80 degC -> alarm; fault code 12 -> flag',
    ok, f"CHP01 {o(m, 'CHP01_VfdOutputV'):.0f} V DC {o(m, 'CHP01_VfdDcBusV'):.0f} V; over-temp {o(m, 'CHP01_VfdOverTempAlarm')}; CT01/01 code flag {o(m, 'CT01_01_VfdFaultCodeActive')}")

# N09 set selection: Set 2 runs CH02 + CHP02 + CDP02 + CT02 (linked)
K = ['CH02StartSuccess', 'CHP02StartCmd', 'CDP02StartCmd', 'CT02StartCmd', 'CHP01StartCmd']
m, tr = sim(FPT, [(0.0, {'LeadCH01': False, 'CT_LeadByRuntime': False})], 150, extra=K)
ok = o(m, 'CH02StartSuccess') and o(m, 'CHP02StartCmd') and o(m, 'CDP02StartCmd') and o(m, 'CT02StartCmd') and not o(m, 'CHP01StartCmd') and not o(m, 'LeadSet')
row('N09', 'Set', 'Lead set 2 selected (pools linked)', 'CH02 + CHP02 + CDP02 + CT02 run; set-1 pumps off (towers follow the set when CT_LeadByRuntime = Follow set)',
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
ok = o(m, 'CT01_MVFailLatchedAlarm') and not o(m, 'CT01StartCmd') and o(m, 'CT02StartCmd') and o(m, 'CH01StartSuccess')
row('N17', 'Valves', 'CT01 outlet valve stuck closed', 'command failure latched (Critical, RESET), CT01 out of the pool; tower valves fail-safe open until CT02 path proves; chiller runs',
    ok, f"latched alarm={o(m, 'CT01_MVFailLatchedAlarm')} CT01={o(m, 'CT01StartCmd')} CT02={o(m, 'CT02StartCmd')} CH01={o(m, 'CH01StartSuccess')}")

# N18 modulating valves: evaporator FCV (flow limit) and condenser head-pressure valve
m, tr = sim(FPT, [(0.0, {'CH01_ChwFlow': 120.0, 'CH01_CdwEnteringTemp': 28.0}), (120.0, {'CH01_ChwFlow': 200.0, 'CH01_CdwEnteringTemp': 16.0})], 240,   # V7.6: limit 720 gpm = 163.5 m3/h
            extra=['CH01_ChwFCVCmd', 'CH01_CdwHPVCmd'])
a, b = at(tr, 115, 'CH01_ChwFCVCmd'), at(tr, 115, 'CH01_CdwHPVCmd')
c_, d_ = o(m, 'CH01_ChwFCVCmd'), o(m, 'CH01_CdwHPVCmd')
row('N18', 'Valves', 'Modulating FCV + head-pressure valve', 'flow 120 < limit -> FCV 100 %; flow 200 > limit -> FCV throttles (>= 20 %); ECWT 28 -> HPV 100 %; ECWT 16 -> HPV 44 %',
    abs(a - 100) < 0.5 and 20 <= c_ < 90 and abs(b - 100) < 0.5 and abs(d_ - 44) < 1, f"FCV {a:.0f} -> {c_:.0f} %; HPV {b:.0f} -> {d_:.0f} %")

# N19 settable staging: start the next chiller at X % (default 90); 75 % load -> no stage 2; X = 70 -> stage 2
m, tr = sim(FPT, [(0.0, {'PlantLoadPct': 50.0, 'Stage_UpLoadPct': 90.0}), (10.0, {'PlantLoadPct': 75.0})], 150, extra=['Stage2Request', 'CH02StartCmd'])
a = o(m, 'Stage2Request')
m2, tr2 = sim(FPT, [(0.0, {'PlantLoadPct': 50.0, 'Stage_UpLoadPct': 70.0}), (10.0, {'PlantLoadPct': 75.0})], 150, extra=['Stage2Request', 'CH02StartCmd'])
row('N19', 'Staging', 'Start next chiller at settable load %', 'load 75 % with setting 90 % -> 1 chiller; setting 70 % -> stage 2, CH02 started',
    not a and o(m2, 'Stage2Request') and o(m2, 'CH02StartCmd'), f"setting 90: stage2={a}; setting 70: stage2={o(m2, 'Stage2Request')} CH02 cmd={o(m2, 'CH02StartCmd')}")

# N20 (V7.6: load falls -> flow falls too, below the VPF flow-hold) settable stage-down
m, tr = sim(FPT, [(0.0, {'PlantLoadPct': 95.0}), (100.0, {'PlantLoadPct': 55.0, 'Stage_DownLoadPct': 50.0, 'CHWFlow': 100.0}), (200.0, {'Stage_DownLoadPct': 60.0})], 320,
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


# ======================================================================= V7.3 T-cases
SP = 'CDS_Setpoint_ACTIVE'
CELLK = ['CT01_01StartCmd', 'CT01_02StartCmd', 'CT02_01StartCmd', 'CT02_02StartCmd', 'CT01StartCmd', 'CT02StartCmd', 'CT_LagStaged',
         'CT_CommonSpeed', 'CT01_01SpeedCmd']


def cds_rel(dk):
    """force CDS to the ACTIVE setpoint + dk (evaluated at event time)"""
    def f(m): m.force['CDS'] = m.out[SP] + dk
    return f


def fire(name, ms=2000):
    def f(m): m.st[name]['rem'] = ms / 1000.0; m.out[name] = True
    return f


# T01 one chiller: lead tower, both of its cells run, lag tower off
m, tr = sim(FPT, [], 150, extra=CELLK)
ok = o(m, 'CH01StartSuccess') and o(m, 'CT01_01StartCmd') and o(m, 'CT01_02StartCmd') and not o(m, 'CT02_01StartCmd') and not o(m, 'CT02StartCmd') \
    and abs(o(m, 'CT01_kW') - (o(m, 'CT01_01_kW') + o(m, 'CT01_02_kW'))) < 1e-6 and o(m, 'CT01RunProof')
row('T01', 'CT SOO', '1 chiller -> lead tower, both fan cells', 'CT-01/01 + CT-01/02 run (own VSD), CT-02 cells off; tower kW = sum of cells; tower proven = any cell',
    ok, ' '.join(f"{k}={int(o(m, k))}" for k in CELLK[:6]) + f" CT01 kW {o(m, 'CT01_kW'):.2f}")

# T02 initial speed after start, then PID
m, tr = sim(FPT, [(0.0, cds_rel(3.0))], 150, extra=['CT01_01SpeedCmd', 'CT01_01RunProof', 'CT_CommonSpeed'], every=0.5)
t_run = next((t for t, s_ in tr if s_['CT01_01RunProof']), None)
early = at(tr, t_run + 0.5, 'CT01_01SpeedCmd') if t_run else -1
row('T02', 'CT SOO', 'Fan start at initial speed, then PID', 'right after run proof speed = CT_InitialSpeed 40 %; after the hold it follows the CDS PID (CDS 3 K high -> ramps up)',
    t_run is not None and abs(early - 40) < 0.5 and o(m, 'CT01_01SpeedCmd') > 60, f"run @{t_run}s speed {early:.1f} % -> end {o(m, 'CT01_01SpeedCmd'):.1f} % (common {o(m, 'CT_CommonSpeed'):.1f} %)")

# T03 permissive: CDP running but no condenser water flow -> fans inhibited + alarm (valves open)
K = ['CT01StartCmd', 'CT01_01StartCmd', 'CT01ValveOpenCmd', 'CT_StartInhibitedAlarm', 'CDP01RunProof']
m, tr = sim(FPT, [(0.0, {'CDW_Flow': 0.0, 'CH01CDWFlowProof': False, 'CH02CDWFlowProof': False})], 30, extra=K)
s20 = {k: at(tr, 20, k) for k in K}
ok = s20['CDP01RunProof'] and s20['CT01ValveOpenCmd'] and not s20['CT01StartCmd'] and not s20['CT01_01StartCmd'] and s20['CT_StartInhibitedAlarm']
row('T03', 'CT SOO', 'Plant enable not satisfied (no condenser water flow)', 'CDP running + tower valves open, but no CDW flow -> fans inhibited; "CT start inhibited" alarm',
    ok, ' '.join(f"{k}={int(v)}" for k, v in s20.items()) + ' @20 s')

# T04 stage-up needs A (CDS > SP + 1) AND B (speed >= 90 %) for the delay
m, tr = sim(FPT, [(0.0, {'CT_CommonSpeed': 95.0}), (10.0, cds_rel(0.5)), (60.0, cds_rel(2.0))], 120, extra=CELLK, every=0.5)   # V7.5: SP soft start settles first
a = at(tr, 58, 'CT_LagStaged')
t_st = next((t for t, s_ in tr if s_['CT_LagStaged']), None)
ok = not a and t_st is not None and 64 <= t_st <= 67 and o(m, 'CT02_01StartCmd') and o(m, 'CT02_02StartCmd') and o(m, 'CT01_01StartCmd')
row('T04', 'CT SOO', 'Stage LAG tower: CDS > SP+1.0 K AND speed >= 90 % for the delay', 'speed 95 % but CDS SP+0.5 -> no; CDS SP+2 -> lag after the staging delay (FPT 5 s), all 4 cells run',
    ok, f"@58s staged={a}; staged @{t_st}s (A true @60s); CT02 cells {o(m, 'CT02_01StartCmd')}/{o(m, 'CT02_02StartCmd')}")

# T05 de-stage: 1 chiller AND CDS < SP - 0.5 AND speed <= low for the delay; then minimum stop
m, tr = sim(FPT, [(0.0, {'CT_CommonSpeed': 95.0}), (0.0, cds_rel(2.0)), (60.0, {'CT_CommonSpeed': 30.0}), (60.0, cds_rel(-1.0)),
                  (70.0, {'CT_CommonSpeed': 95.0}), (70.0, cds_rel(2.0))], 110, extra=CELLK, every=0.5)
t_off = next((t for t, s_ in tr if t > 60 and not s_['CT_LagStaged']), None)
t_on = next((t for t, s_ in tr if t_off and t > t_off and s_['CT_LagStaged']), None)
ok = at(tr, 59, 'CT_LagStaged') and t_off is not None and 67 <= t_off <= 70 and not at(tr, t_off + 1, 'CT02_01StartCmd') and at(tr, t_off + 1, 'CT01_01StartCmd') \
    and t_on is not None and t_on - t_off >= 10.5
row('T05', 'CT SOO', 'De-stage LAG tower + minimum stop', 'CDS SP-1 and speed 30 % -> lag off after the de-staging delay (FPT 8 s), lead stays; lag cannot restart before its minimum stop (FPT 6 s) even if staging is met at once',
    ok, f"lag off @{t_off}s (cond @60s), lead on {at(tr, (t_off or 0) + 1, 'CT01_01StartCmd')}; lag re-staged @{t_on}s (cond again @70s -> waits min-stop 6 s + delay 5 s)")

# T06 two chillers -> both towers; reduction locked out
m, tr = sim(FPT, [(0.0, {'PlantLoadPct': 150.0}), (150.0, {'CT_CommonSpeed': 20.0}), (150.0, cds_rel(-2.0))], 260, extra=CELLK)
ok = o(m, 'CH02StartSuccess') and o(m, 'CT01StartCmd') and o(m, 'CT02StartCmd') and o(m, 'CT_LagStaged') and all(o(m, c) for c in CELLK[:4])
row('T06', 'CT SOO', '2 chillers -> both towers, no reduction', 'stage 2: CT01 + CT02 (4 cells) and the reduction conditions are ignored while 2 chillers run',
    ok, f"CH02={o(m, 'CH02StartSuccess')} CT01={o(m, 'CT01StartCmd')} CT02={o(m, 'CT02StartCmd')} cells={[int(o(m, c)) for c in CELLK[:4]]}")

# T07 back to 1 chiller: lag stays until the reduction conditions hold (SOO dual -> reduce loop)
m, tr = sim(FPT, [(0.0, {'PlantLoadPct': 150.0}), (150.0, {'PlantLoadPct': 40.0, 'CHWFlow': 70.0}), (150.0, {'CT_CommonSpeed': 60.0}), (150.0, cds_rel(0.0)),
                  (400.0, {'CT_CommonSpeed': 20.0}), (400.0, cds_rel(-1.5))], 440, extra=CELLK + ['Pool_Need2'])
t1 = next((t for t, s_ in tr if t > 150 and not s_['Pool_Need2']), None)
ok = t1 is not None and at(tr, 395, 'CT_LagStaged') and at(tr, 395, 'CT02StartCmd') and not o(m, 'CT_LagStaged') and not o(m, 'CT02StartCmd')
row('T07', 'CT SOO', '2 -> 1 chiller: lag tower kept until reduction conditions', 'after CH02 stops both towers keep running (CDS at SP, speed 60 %); CDS SP-1.5 + speed 20 % -> lag off after the delay',
    ok, f"1 chiller @{t1}s; @395s lag={at(tr, 395, 'CT_LagStaged')} CT02={at(tr, 395, 'CT02StartCmd')}; end lag={o(m, 'CT_LagStaged')} CT02={o(m, 'CT02StartCmd')}")

# T08 one cell VFD fault: other cell continues; lead tower degraded -> lag staged at once
m, tr = sim(FPT, [(100.0, {'CT01_01VfdFault': True})], 160, extra=CELLK)
ok = at(tr, 95, 'CT01_01StartCmd') and not o(m, 'CT01_01StartCmd') and o(m, 'CT01_02StartCmd') and o(m, 'CT01StartCmd') and o(m, 'CT02_01StartCmd') \
    and not at(tr, 95, 'CT02StartCmd')
row('T08', 'Cells', 'CT-01/01 VFD fault', 'CT-01/01 stops, CT-01/02 keeps running (tower stays on); lead lost a cell -> CT-02 staged at once',
    ok, f"CT01/01 {o(m, 'CT01_01StartCmd')} CT01/02 {o(m, 'CT01_02StartCmd')} CT02 {at(tr, 95, 'CT02StartCmd')} -> {o(m, 'CT02StartCmd')} cells healthy sts {o(m, 'CT01_CellsHealthy')}")

# T09 cell fails to prove -> latched alarm -> RESET
m, tr = sim(FPT, [(60.0, {'CT01_01RunProof': False}), (120.0, {'CT01_01RunProof': None}), (130.0, fire('CT01_01ResetFire'))], 170, extra=['CT01_01_FailAlarm', 'CT01_01StartCmd'])
ok = at(tr, 125, 'CT01_01_FailAlarm') and not at(tr, 125, 'CT01_01StartCmd') and not o(m, 'CT01_01_FailAlarm') and o(m, 'CT01_01StartCmd')
row('T09', 'Cells', 'Cell fails to prove -> latched -> RESET', 'no run status 5 s (FPT) -> cell failed + alarm (held after the fault clears); RESET -> cell back in service',
    ok, f"@125s alarm {at(tr, 125, 'CT01_01_FailAlarm')} cmd {at(tr, 125, 'CT01_01StartCmd')}; after RESET alarm {o(m, 'CT01_01_FailAlarm')} cmd {o(m, 'CT01_01StartCmd')}")

# T10 both cells of the lead tower out -> tower unavailable -> CT02 leads
m, tr = sim(FPT, [(0.0, {'CT01_01InAuto': False, 'CT01_02_ServiceIsolate': True})], 150, extra=CELLK)
ok = not o(m, 'CT01StartCmd') and o(m, 'CT02StartCmd') and o(m, 'CT02_01StartCmd') and not o(m, 'CT01Healthy') and o(m, 'CT_Lead') is False
row('T10', 'Cells', 'Both cells of CT-01 unavailable', 'CT-01 unhealthy (no fan cell) -> CT-02 becomes lead; CT-01/01 not-in-auto alarm',
    ok, f"CT01 healthy {o(m, 'CT01Healthy')} cmd {o(m, 'CT01StartCmd')}; CT02 {o(m, 'CT02StartCmd')}; lead {'CT01' if o(m, 'CT_Lead') else 'CT02'}; alarm {o(m, 'CT01_01_NotInAutoAlarm')}")

# T11 basin LOW-LOW on the lead tower
K = ['CT01StartCmd', 'CT02StartCmd', 'CT01ValveOpenCmd', 'CT01_OutletMVCmd', 'CT01_MakeupValveCmd', 'CT01BasinLowLowLevelAlarm']
m, tr = sim(FPT, [(100.0, {'CT01_LowLowLevelSwitch': True, 'CT01_BasinLevel': 10.0}), (180.0, {'CT01_LowLowLevelSwitch': False, 'CT01_BasinLevel': 40.0})], 260, extra=K + ['CH01StartSuccess'])
s1 = {k: at(tr, 170, k) for k in K}
ok = s1['CT01BasinLowLowLevelAlarm'] and not s1['CT01StartCmd'] and not s1['CT01ValveOpenCmd'] and not s1['CT01_OutletMVCmd'] and s1['CT01_MakeupValveCmd'] \
    and s1['CT02StartCmd'] and at(tr, 170, 'CH01StartSuccess') and not o(m, 'CT01BasinLowLowLevelAlarm')
row('T11', 'Basin', 'CT-01 basin LOW-LOW', 'CT-01 fans stop, inlet + outlet valves close, emergency make-up opens, Critical alarm; CT-02 takes over; chiller stays on; clears when refilled',
    ok, ' '.join(f"{k}={int(v)}" for k, v in s1.items()) + f" CH01={at(tr, 170, 'CH01StartSuccess')}; end alarm {o(m, 'CT01BasinLowLowLevelAlarm')}")

# T12 both basins dry -> condenser pumps stop (dry-run protection)
m, tr = sim(FPT, [(100.0, {'CT01_LowLowLevelSwitch': True, 'CT02_LowLowLevelSwitch': True})], 160, extra=['CDP01StartCmd'])
ok = at(tr, 95, 'CDP01StartCmd') and not o(m, 'CDP01StartCmd') and not o(m, 'CDP02StartCmd') and o(m, 'CT_AllBasinsDryAlarm')
row('T12', 'Basin', 'Both basins LOW-LOW', 'CDPs stopped (no water to pump), Emergency alarm', ok,
    f"CDP01 {at(tr, 95, 'CDP01StartCmd')} -> {o(m, 'CDP01StartCmd')} CDP02 {o(m, 'CDP02StartCmd')} alarm {o(m, 'CT_AllBasinsDryAlarm')}")

# T13 CDS sensor invalid -> all towers (fail-safe speed)
m, tr = sim(FPT, [(100.0, {'CDSSensorHealthy': False})], 180, extra=CELLK)
ok = o(m, 'CT02StartCmd') and o(m, 'CT01StartCmd') and abs(o(m, 'CT01_01SpeedCmd') - o(m, 'CT_FailSafeSpeed')) < 1.0 and not at(tr, 95, 'CT02StartCmd')
row('T13', 'CT SOO', 'CDS sensor invalid', 'both towers run at the fail-safe speed (heat rejection first)', ok,
    f"CT02 {at(tr, 95, 'CT02StartCmd')} -> {o(m, 'CT02StartCmd')}; cell speed {o(m, 'CT01_01SpeedCmd'):.1f} % (fail-safe {o(m, 'CT_FailSafeSpeed'):.0f})")

# T14 CHW loop fill: 180 -> 200 kPa, leak lock-out, RESET
K = ['CHW_FillValveCmd', 'CHW_FillLockoutAlarm']
m, tr = sim(FPT, [(10.0, {'CHW_ExpansionTankPressure': 170.0}), (18.0, {'CHW_ExpansionTankPressure': 190.0}), (25.0, {'CHW_ExpansionTankPressure': 205.0}),
                  (40.0, {'CHW_ExpansionTankPressure': 170.0}), (90.0, {'CHW_ExpansionTankPressure': 205.0}), (95.0, fire('CHW_FillResetFire'))], 110, extra=K)
seq = [at(tr, t, 'CHW_FillValveCmd') for t in (8, 15, 22, 35, 55, 85)]
ok = seq == [False, True, True, False, True, False] and at(tr, 85, 'CHW_FillLockoutAlarm') and not o(m, 'CHW_FillLockoutAlarm') and o(m, 'CHW_FillVolume') > 0
row('T14', 'Make-up', 'CHW loop fill + leak lock-out', 'open < 180 kPa, stays open to 200 kPa; filling > 20 s (FPT) -> valve locked closed + Critical alarm; RESET clears',
    ok, f"valve @8/15/22/35/55/85 s = {seq}; lockout @85s {at(tr, 85, 'CHW_FillLockoutAlarm')} after RESET {o(m, 'CHW_FillLockoutAlarm')}; fill {o(m, 'CHW_FillVolume'):.3f} m3")

# T15 bleed-off + dosing
m, tr = sim(FPT, [(0.0, {'CT01_BasinLevel': 75.0, 'CT02_BasinLevel': 75.0}), (60.0, {'CT_Conductivity': 2100.0}), (90.0, {'CT_Conductivity': 1900.0}), (120.0, {'CT_Conductivity': 1700.0}),
                  (130.0, {'CT01_BasinLevel': 60.0})], 150, extra=['CT_BleedValveCmd', 'CT_ChemDosingPumpCmd'])
seq = [at(tr, t, 'CT_BleedValveCmd') for t in (55, 85, 115, 145)]
ok = seq == [False, True, True, False] and o(m, 'CT_ChemDosingPumpCmd') and not at(tr, 125, 'CT_ChemDosingPumpCmd')
row('T15', 'Treatment', 'Bleed-off (conductivity) + dosing', 'bleed opens > 2000 uS/cm, holds to 1800; dosing pump runs with make-up water',
    ok, f"bleed @55/85/115/145 s = {seq}; dosing {at(tr, 125, 'CT_ChemDosingPumpCmd')} -> {o(m, 'CT_ChemDosingPumpCmd')} (make-up opened @130s)")

# T16 bypass: min-flow valve on evaporator flow, bypass flow meter removed, manual bypass alarm
m, tr = sim(FPT, [(0.0, {'CH01_ChwFlow': 120.0}), (80.0, {'CH01_ChwFlow': 45.0}), (200.0, {'CHW_BypassManualOpen': True})], 220, extra=['CHW_BypassValveCmd'])
ok = at(tr, 75, 'CHW_BypassValveCmd') < 1 and o(m, 'CHW_BypassValveCmd') > 5 and o(m, 'CHW_BypassManualOpenAlarm') and 'CHW_BypassFlow' not in m.C
row('T16', 'Bypass', 'Min-flow bypass valve (modulating)', 'evaporator flow 200 > 66 m3/h -> closed; 45 m3/h -> opens; no bypass flow meter; manual bypass open -> alarm',
    ok, f"valve {at(tr, 75, 'CHW_BypassValveCmd'):.1f} -> {o(m, 'CHW_BypassValveCmd'):.1f} % (SP {o(m, 'CHW_BypassMinFlowSP'):.0f} m3/h); manual alarm {o(m, 'CHW_BypassManualOpenAlarm')}; FT removed {'CHW_BypassFlow' not in m.C}")

# T17 zones (Sense-T / AirPlug)
z = '01_0103'
m, tr = sim(FPT, [(0.0, {f'ZoneTemperatureAvg_{z}': 29.0, 'ZoneTemperatureAvg_01_0104': 29.0, 'ZoneOutOfService_01_0104': True}),
                  (20.0, {'AirPlug_GatewayOnline': False})], 30, extra=[f'Zone_{z}_TempHighAlarm', 'Zone_01_0104_TempHighAlarm'])
ts = [o(m, f'ZoneTemperatureAvg_01_010{i}') for i in (1, 2, 3, 4)]
ok = at(tr, 15, f'Zone_{z}_TempHighAlarm') and not at(tr, 15, 'Zone_01_0104_TempHighAlarm') and o(m, 'AirPlug_GatewayOfflineAlarm') \
    and abs(o(m, 'Zone_AHU01_AvgTemp') - sum(ts) / 4) < 0.05
row('T17', 'Zones', 'Zone T / RH (Sense-T / AirPlug)', '29 degC -> over-temperature alarm after the delay; zone out of service -> no alarm; gateway offline alarm; AHU01 average of its 4 zones',
    ok, f"alarm {z} {at(tr, 15, f'Zone_{z}_TempHighAlarm')} OOS zone {at(tr, 15, 'Zone_01_0104_TempHighAlarm')}; gateway alarm {o(m, 'AirPlug_GatewayOfflineAlarm')}; AHU01 avg {o(m, 'Zone_AHU01_AvgTemp'):.2f}")

# T18 site timers: staging delay 10 min, de-staging 30 min  (one chiller: its load is pinned so the V7.4 coherent model does not stage CH02)
STEADY = {'PlantLoadPct': 50.0, 'CHWFlow': 150.0, 'ModeCmd_UI': False, 'CH01LoadPct': 50.0, 'CH02LoadPct': 0.0}
SB = [(0.0, STEADY), (10.0, {'BootQualified': True}), (15.0, {'PlantEnable': True})]
m, tr = sim(SITE, SB + [(400.0, {'CT_CommonSpeed': 95.0}), (400.0, cds_rel(2.0)), (1200.0, {'CT_CommonSpeed': 20.0}), (1200.0, cds_rel(-1.0))], 3100,
            extra=['CT_LagStaged', 'CT02_01RunProof'], every=5.0, base=False)
t_up = next((t for t, s_ in tr if s_['CT_LagStaged']), None)
t_dn = next((t for t, s_ in tr if t_up and t > t_up and not s_['CT_LagStaged']), None)
ok = t_up is not None and 995 <= t_up <= 1010 and t_dn is not None and 2995 <= t_dn <= 3010
row('T18', 'CT SOO', 'Site timers: 10 min staging / 30 min de-staging', 'conditions from 400 s -> lag staged ~1000 s; reduce conditions from 1200 s -> lag off ~3000 s',
    ok, f"staged @{t_up}s, de-staged @{t_dn}s; CT02/01 proven {o(m, 'CT02_01RunProof')}")


# ---- cases added after the independent review
# T19 staging needs the lead tower RUNNING at >= 90 % (not a wound-up PID request with the fans off)
m, tr = sim(FPT, [(0.0, {'CDW_Flow': 0.0, 'CH01CDWFlowProof': False, 'CH02CDWFlowProof': False}), (0.0, cds_rel(3.0))], 60, extra=['CT_LagStaged'])
row('T19', 'CT SOO', 'No staging while the lead fans are not running', 'fans inhibited (no CDW flow) + CDS SP+3 -> lag NOT staged, PID not wound up',
    not any(s_['CT_LagStaged'] for _, s_ in tr) and o(m, 'CT_CommonSpeed') < 25, f"lag staged ever={any(s_['CT_LagStaged'] for _, s_ in tr)} PID request {o(m, 'CT_CommonSpeed'):.1f} %")


def pre_ct100(mm):
    mm.extv[('CT01RunProof', 'Runtime', 'elapsedActiveTimeNumeric')] = 100 * 3600 * 1000.0


# T20 lead tower = fewer operating hours (SOO), also with pumps linked to the chiller set
m, tr = sim(FPT, [(0.0, pre_ct100)], 120, extra=['CT02StartCmd'])
row('T20', 'CT SOO', 'Lead tower by accumulated runtime', 'CT01 100 h ahead -> CT02 is lead (CT_LeadByRuntime default, Set_LinkPools linked)',
    o(m, 'CT02StartCmd') and not o(m, 'CT01StartCmd') and not o(m, 'CT_Lead'), f"lead={'CT01' if o(m, 'CT_Lead') else 'CT02'} CT01={o(m, 'CT01StartCmd')} CT02={o(m, 'CT02StartCmd')}")

# T21 flapping lead-cell fault -> lag staged once and held (no start/stop chatter)
ev = [(60.0 + 4 * k, {'CT01_01VfdFault': k % 2 == 0}) for k in range(10)]
m, tr = sim(FPT, ev, 110, extra=['CT02StartCmd'], every=0.5)
starts = sum(1 for (a, b) in zip(tr, tr[1:]) if b[1]['CT02StartCmd'] and not a[1]['CT02StartCmd'])
row('T21', 'Cells', 'Lead cell fault flapping', 'VFD fault toggling every 4 s -> lag tower staged once and held (latched), no cycling',
    starts == 1 and o(m, 'CT02StartCmd'), f"CT02 starts = {starts}, CT02 at end {o(m, 'CT02StartCmd')}")

# T22 bypass PV invalid (evaporator flow meter) -> fail-safe position + alarm
m, tr = sim(FPT, [(60.0, {'CH01_ChwFlow': -10.0})], 120, extra=['CHW_BypassValveCmd'])
row('T22', 'Bypass', 'Evaporator flow meter invalid', 'bypass valve goes to its fail-safe position (not 100 %), invalid alarm',
    abs(o(m, 'CHW_BypassValveCmd') - o(m, 'Byp_FailSafePosition')) < 0.5 and o(m, 'Byp_EvapFlowInvalidAlarm'),
    f"valve {o(m, 'CHW_BypassValveCmd'):.1f} % (fail-safe {o(m, 'Byp_FailSafePosition'):.0f}) alarm {o(m, 'Byp_EvapFlowInvalidAlarm')}")

# T23 OA wet bulb invalid -> fixed CDS setpoint (SOO)
m, tr = sim(FPT, [(30.0, {'OA_SensorFault': True})], 60, extra=['CDS_Setpoint_ACTIVE'])
row('T23', 'CT SOO', 'OA sensor invalid -> fixed CDS setpoint', 'CDS SP = OA WB + approach while valid; fixed CDSSetpoint when invalid',
    abs(o(m, 'CDS_Setpoint_ACTIVE') - o(m, 'CDSSetpoint')) < 0.01 and abs(at(tr, 25, 'CDS_Setpoint_ACTIVE') - o(m, 'CDSSetpoint')) > 0.1,
    f"SP {at(tr, 25, 'CDS_Setpoint_ACTIVE'):.2f} -> {o(m, 'CDS_Setpoint_ACTIVE'):.2f} (fixed {o(m, 'CDSSetpoint'):.1f})")

if len(sys.argv) > 3:
    with open(sys.argv[3], 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"{sum(r['result'] == 'PASS' for r in rows)}/{len(rows)} PASS")
