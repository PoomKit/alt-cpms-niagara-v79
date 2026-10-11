"""V7 scenario suite: headered pools, instrumentation diagnostics, air-side library (offline model, review aid).
usage: v7tests.py v7_fpt.bog v7.bog [out.csv]
  H-cases run on the FPT build (fast timers), A-cases (air side) run on the site build."""
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


def ft(tr, cond, after=0.0):
    for t, s in tr:
        if t >= after and cond(s): return t
    return None


def gap(tr, a, b):
    longest = cur = 0.0; prev = None
    for t, s in tr:
        if t < a or t > b: continue
        none = not (s['CH01StartSuccess'] or s['CH02StartSuccess'])
        if none and prev is not None: cur += t - prev
        elif not none: cur = 0.0
        longest = max(longest, cur); prev = t
    return longest


SAMPLE = ['CH01StartSuccess', 'CH02StartSuccess', 'CH01StartCmd', 'CH02StartCmd', 'CHP01StartCmd', 'CHP02StartCmd', 'CDP01StartCmd',
          'CDP02StartCmd', 'CT01StartCmd', 'CT02StartCmd', 'PlantRunRequest']


def sim(bog, events, dur, extra=(), every=1.0, base=True, ramps=False):
    m = faithful(Model6(bog, ramps=ramps))
    tr = m.run(dur, (BASE if base else []) + list(events), sample=SAMPLE + list(extra), every=every)
    return m, tr


def fire(name, ms=2000):
    def f(m): m.st[name]['rem'] = ms / 1000.0; m.out[name] = True
    return f


def setout(**kv):
    def f(m):
        for k, v in kv.items(): m.out[k] = v
    return f


o = lambda m, n: m.lv(n)
def setopt(mm):
    if 'Pump_StandbyValvesOpen' in mm.C: mm.force['Pump_StandbyValvesOpen'] = True     # V7.2: fast changeover option for P01/P02


# ------------------------------------------------------------------ H: headered pools (FPT timers)
# H01 the user's case: CDP01 and CHP02 failed -> CHP01 + CDP02 serve the plant
m, tr = sim(FPT, [(0.0, {'CDP01Fault': True, 'CHP02Fault': True})], 120)
ok = o(m, 'CH01StartSuccess') and o(m, 'CHP01StartCmd') and o(m, 'CDP02StartCmd') and not o(m, 'CDP01StartCmd') and not o(m, 'CHP02StartCmd')
row('H01', 'Pools', 'CDP01 + CHP02 failed (different "sets")', 'Plant runs on CHP01 + CDP02 (cross-set); V6.3 stopped the plant',
    ok, f"CH01 proven={o(m, 'CH01StartSuccess')} CHP01={o(m, 'CHP01StartCmd')} CDP02={o(m, 'CDP02StartCmd')} CDP01={o(m, 'CDP01StartCmd')} CHP02={o(m, 'CHP02StartCmd')} "
        f"CHP pool degraded alarm={o(m, 'CHP_PoolDegradedAlarm')}")
# H02 same faults while running: failure happens at 60 s
m, tr = sim(FPT, [(60.0, {'CDP01Fault': True, 'CHP02Fault': True})], 180)
row('H02', 'Pools', 'CDP01 + CHP02 fail while plant runs', 'Chiller keeps running (no loss of chiller); standby units take over',
    o(m, 'CH01StartSuccess') and o(m, 'CDP02StartCmd') and gap(tr, 60, 180) <= 10, f"longest gap without proven chiller {gap(tr, 60, 180):.0f} s; CDP02={o(m, 'CDP02StartCmd')}")
# H03 lead pump fails to prove (no run feedback): standby starts, unit latched, RESET clears
m, tr = sim(FPT, [(0.0, {'CHP01RunProof': False}), (100.0, {'CHP01RunProof': None}), (110.0, fire('CHP01ResetFire'))], 160, extra=['CHP01FailLatch'])
t_l = ft(tr, lambda s: s['CHP01FailLatch']); t_2 = ft(tr, lambda s: s['CHP02StartCmd'])
row('H03', 'Pools', 'CHP01 never proves', 'CHP01 latched after proof timeout, CHP02 starts, chiller proven; RESET clears latch',
    t_l is not None and t_2 is not None and ft(tr, lambda s: s['CH01StartSuccess'] or s['CH02StartSuccess']) is not None and not o(m, 'CHP01FailLatch'),
    f"CHP01 latched @{t_l}s CHP02 cmd @{t_2}s; after RESET @110 s latch={o(m, 'CHP01FailLatch')}")
# H04 pump running without dP (coupling) -> failover
m, tr = sim(FPT, [(40.0, {'CHP01_DischargePressure': 200.0, 'CHP01_SuctionPressure': 198.0})], 200, extra=['CHP01NoDPDelay', 'CHP01FailLatch'])
t_f = ft(tr, lambda s: s['CHP01FailLatch'])
row('H04', 'Pools', 'CHP01 runs but dP = 2 kPa (broken coupling)', 'No-dP detected 20 s -> CHP01 failed -> CHP02 runs, chiller keeps running',
    t_f is not None and 55 <= t_f <= 80 and o(m, 'CHP02StartCmd') and o(m, 'CH01StartSuccess'), f"CHP01 failed @{t_f}s; CHP02={o(m, 'CHP02StartCmd')} alarm={o(m, 'CHP01NoDeltaPAlarm')}")
# H05 VFD fault / HOA not in auto / CT vibration
m, tr = sim(FPT, [(40.0, {'CHP01VfdFault': True, 'CDP01InAuto': False, 'CT01VibrationAlarm': True})], 120)
row('H05', 'Pools', 'VFD fault CHP01, CDP01 HOA off-auto, CT01 vibration trip', 'Each pool skips the unit; plant keeps running on 02 units',
    o(m, 'CH01StartSuccess') and o(m, 'CHP02StartCmd') and o(m, 'CDP02StartCmd') and o(m, 'CT02StartCmd') and not o(m, 'CT01StartCmd'),
    f"CHP02={o(m, 'CHP02StartCmd')} CDP02={o(m, 'CDP02StartCmd')} CT02={o(m, 'CT02StartCmd')} CT01={o(m, 'CT01StartCmd')} NotInAuto alarm={o(m, 'CDP01NotInAutoAlarm')}")
# H06 CT isolation valve fails to open -> tower failed, other tower serves
m, tr = sim(FPT, [(0.0, {'CT_RunAllAvailable': False, 'CT01ValveOpenProof': False})], 120, extra=['CT01FailLatch'])
row('H06', 'Pools', 'CT01 isolation valve does not open', 'Valve stroke timeout -> CT01 failed -> CT02 (valve proven first) runs',
    o(m, 'CT01FailLatch') and o(m, 'CT02StartCmd') and o(m, 'CH01StartSuccess'), f"CT01 failed={o(m, 'CT01FailLatch')} CT02={o(m, 'CT02StartCmd')} chiller proven={o(m, 'CH01StartSuccess')}")
# H07 stage 2 needs 2 pumps: CHP02 unavailable -> stage 2 blocked + alarm, plant keeps 1 chiller
m, tr = sim(FPT, [(0.0, {'CHP02Available': False}), (10.0, {'PlantLoadPct': 90.0})], 150, extra=['Stage2Allowed'])
row('H07', 'Pools', 'Stage 2 requested with one CHW pump available', 'Stage 2 blocked (Stage2BlockedByPoolAlarm), lead chiller keeps running',
    o(m, 'CH01StartSuccess') and not o(m, 'CH02StartCmd') and o(m, 'Stage2BlockedByPoolAlarm'), f"CH02 cmd={o(m, 'CH02StartCmd')} blocked alarm={o(m, 'Stage2BlockedByPoolAlarm')}")
# H08 both chillers with full pools: 2 CHP + 2 CDP + 2 CT
m, tr = sim(FPT, [(10.0, {'PlantLoadPct': 90.0})], 150)
row('H08', 'Pools', 'Stage 2 with healthy pools', 'Two chillers, two CHP, two CDP, two CT', all(o(m, x) for x in ('CH01StartSuccess', 'CH02StartSuccess', 'CHP01StartCmd', 'CHP02StartCmd', 'CDP01StartCmd', 'CDP02StartCmd', 'CT01StartCmd', 'CT02StartCmd')),
    ' '.join(f"{x}={int(o(m, x))}" for x in ('CH02StartSuccess', 'CHP02StartCmd', 'CDP02StartCmd', 'CT02StartCmd')))
# H09 lead rotation by runtime (make-before-break)
def pre(mm):
    mm.extv[('CHP01RunProof', 'Runtime', 'elapsedActiveTimeNumeric')] = 30 * 3600 * 1000.0
    if 'Set_LinkPools' in mm.C: mm.force['Set_LinkPools'] = False     # V7.1: pools independent (runtime lead) for this case
m, tr = sim(FPT, [(60.0, pre)], 140, extra=['CHP_EffLead01', 'CHP01RunProof', 'CHP02RunProof'], every=0.5)
noflow = [t for t, s in tr if t > 60 and not (s['CHP01RunProof'] or s['CHP02RunProof'])]
row('H09', 'Pools', 'CHP01 30 h ahead in runtime', 'Lead moves to CHP02; CHP01 keeps running until CHP02 proven (no flow gap)',
    not o(m, 'CHP_EffLead01') and o(m, 'CHP02StartCmd') and not o(m, 'CHP01StartCmd') and not noflow, f"lead=CHP0{1 if o(m, 'CHP_EffLead01') else 2}; samples without any proven CHP after 60 s: {len(noflow)}")
# H10 whole pool lost -> Emergency alarm, auto-retry only as last resort
m, tr = sim(FPT, [(0.0, {'CHP01RunProof': False, 'CHP02RunProof': False}), (100.0, {'CHP01RunProof': None, 'CHP02RunProof': None})], 420,
            extra=['CHP_PoolUnavailableAlarm', 'CHP01FailLatch', 'CHP02FailLatch'], every=2.0)
t_e = ft(tr, lambda s: s['CHP_PoolUnavailableAlarm']); t_back = ft(tr, lambda s: s['CH01StartSuccess'] or s['CH02StartSuccess'], 100)
row('H10', 'Pools', 'Both CHW pumps fail to prove, repaired at 100 s', 'Emergency pool alarm; auto-retry (180 s) because no healthy unit left; plant restarts by itself',
    t_e is not None and t_back is not None, f"pool unavailable @{t_e}s; chiller proven again @{t_back}s (no operator)")
# ------------------------------------------------------------------ P: pool changeovers with SITE timers (independent-review cases)
STEADY = {'PlantLoadPct': 50.0, 'CHWFlow': 150.0, 'CHWS': 7.0, 'CHWR': 12.0, 'CHWDP': 120.0, 'CDS': 29.0, 'CDR': 34.0, 'CH01LoadPct': 50.0, 'OA_Temperature': 32.0, 'OA_Humidity': 65.0}
SB = [(0.0, STEADY), (10.0, {'BootQualified': True}), (15.0, {'PlantEnable': True})]
m, tr = sim(SITE, SB + [(0.0, setopt), (600.0, {'CHP01VfdFault': True})], 1000, base=False, every=1.0)
row('P01', 'Pools', 'Site timers: lead CHW pump VFD fault while running', 'Standby CHP02 starts inside the 30 s bridge; chiller never drops (no 180 s anti-recycle outage)',
    gap(tr, 600, 1000) == 0 and o(m, 'CHP02StartCmd') and o(m, 'CH01StartSuccess'), f"gap {gap(tr, 600, 1000):.0f} s; CHP02={o(m, 'CHP02StartCmd')}")
m, tr = sim(SITE, SB + [(0.0, setopt), (600.0, {'CHP01_DischargePressure': 185.0, 'CHP01_SuctionPressure': 183.0})], 1000, base=False, every=1.0)
row('P02', 'Pools', 'Site timers: lead CHW pump loses dP (coupling)', 'No-dP 20 s -> standby; chiller keeps running', gap(tr, 600, 1000) == 0 and o(m, 'CHP02StartCmd'),
    f"gap {gap(tr, 600, 1000):.0f} s; CHP01 failed={o(m, 'CHP01FailLatch')}")
def pre_ct(mm):
    mm.extv[('CT01RunProof', 'Runtime', 'elapsedActiveTimeNumeric')] = 30 * 3600 * 1000.0
    if 'Set_LinkPools' in mm.C: mm.force['Set_LinkPools'] = False     # V7.1: pools independent (runtime lead) for this case
m, tr = sim(SITE, SB + [(0.0, {'CT_RunAllAvailable': False}), (600.0, pre_ct)], 1100, base=False, every=1.0, extra=['CT01RunProof', 'CT02RunProof', 'CT01ValveOpenProof'])
nof = [t for t, s in tr if t > 600 and not (s['CT01RunProof'] or s['CT02RunProof'])]
row('P03', 'Pools', 'Site timers: tower lead rotation with "match chillers"', 'CT02 valve strokes and fan proves before CT01 stops (make-before-break); chiller never drops',
    gap(tr, 600, 1100) == 0 and o(m, 'CT02RunProof') and not o(m, 'CT01StartCmd') and not nof, f"gap {gap(tr, 600, 1100):.0f} s; samples with no tower fan: {len(nof)}")
m, tr = sim(SITE, SB + [(0.0, setopt), (600.0, {'CT01VibrationAlarm': True, 'CT02VibrationAlarm': True})], 1000, base=False, every=1.0, extra=['CT01ValveOpenCmd', 'CT02ValveOpenCmd'])
row('P04', 'Pools', 'Site timers: both tower fans trip (vibration)', 'Chiller keeps running (plant never dark), tower valves stay open, CT pool Emergency alarm',
    gap(tr, 600, 1000) == 0 and o(m, 'CT01ValveOpenCmd') and o(m, 'CT02ValveOpenCmd') and o(m, 'CT_PoolUnavailableAlarm') and o(m, 'CDP01StartCmd'),
    f"gap {gap(tr, 600, 1000):.0f} s; valves {o(m, 'CT01ValveOpenCmd')}/{o(m, 'CT02ValveOpenCmd')} alarm={o(m, 'CT_PoolUnavailableAlarm')}")
m, tr = sim(SITE, SB, 400, base=False, every=1.0, extra=['CHP01RunProof', 'CH01ValveOpenProof'])
t_v = ft(tr, lambda s: s['CH01ValveOpenProof']); t_p = ft(tr, lambda s: s['CHP01StartCmd'])
row('P05', 'Pools', 'Pumps start only after a flow path is proven', 'CHP01 command after the evaporator valve end switch (no dead-heading)', t_v is not None and t_p is not None and t_p >= t_v,
    f"valve open @{t_v}s, CHP01 cmd @{t_p}s")
# ------------------------------------------------------------------ I: instrumentation
m, tr = sim(FPT, [(0.0, {'PlantLoadPct': 60.0, 'CH01LoadPct': 60.0, 'CHWS': 7.0, 'CHWR': 12.0, 'CHWFlow': 150.0})], 120, extra=['CoolingLoadSource'])
rt_b, rt_c = o(m, 'CoolingLoad_RT'), 150 * 5 * 1.1628 / 3.517
m2, tr2 = sim(FPT, [(0.0, {'PlantLoadPct': 60.0, 'CHWS': 7.0, 'CHWR': 12.0, 'CHWFlow': 150.0, 'BTU_CommOk': False})], 60)
row('I01', 'Meters', 'Cooling load source: BTU meter, fail-safe to flow x dT', 'BTU valid -> load from meter; BTU comm lost -> calculated load + alarm',
    abs(rt_b - rt_c) < 1.0 and o(m, 'CoolingLoadSource') and not o(m2, 'CoolingLoadSource') and o(m2, 'BTU_InvalidAlarm') and abs(o(m2, 'CoolingLoad_RT') - rt_c) < 0.5,
    f"BTU {rt_b:.1f} RT (source BTU={o(m, 'CoolingLoadSource')}); comm lost -> {o(m2, 'CoolingLoad_RT'):.1f} RT source BTU={o(m2, 'CoolingLoadSource')} alarm={o(m2, 'BTU_InvalidAlarm')}")
ok = (o(m, 'CH01_ChwFlow') > 100 and abs(o(m, 'CH01_DeltaT') - (o(m, 'CH01_ChwReturnTemp') - o(m, 'CH01_ChwSupplyTemp'))) < 0.02
      and o(m, 'CH01_DeltaT') > 1.0 and o(m, 'CH01_RT') > 50 and o(m, 'CH01_Amps') > 0 and o(m, 'CHP01_DiffPressure') > 10
      and o(m, 'CHP01_SpeedFeedbackHz') > 0 and o(m, 'CT01_FanSpeedHz') >= 0 and o(m, 'CH01_EvapDP') > 5 and o(m, 'CT_MakeupFlow') > 0)
row('I02', 'Meters', 'Per-equipment instruments populated', 'Chiller flow/dT/RT/amps, pump dP/Hz, evap dP, tower Hz, make-up flow all live',
    ok, f"CH01 flow {o(m, 'CH01_ChwFlow'):.0f} m3/h dT {o(m, 'CH01_DeltaT'):.1f} K {o(m, 'CH01_RT'):.0f} RT {o(m, 'CH01_Amps'):.0f} A kW/RT {o(m, 'CH01_kW_per_RT'):.3f}; "
        f"CHP01 dP {o(m, 'CHP01_DiffPressure'):.0f} kPa {o(m, 'CHP01_SpeedFeedbackHz'):.1f} Hz; evap dP {o(m, 'CH01_EvapDP'):.1f} kPa; make-up {o(m, 'CT_MakeupFlow'):.2f} m3/h")
m, tr = sim(FPT, [(0.0, {'CT01_BasinLevel': 20.0}), (0.0, {'CT02_HighLevelSwitch': True})], 400)
row('I03', 'Meters', 'Tower basin level low / high', 'Low level alarm (Critical) after 60 s, high level alarm (Warning) after 5 min; plant keeps running',
    o(m, 'CT01BasinLowLevelAlarm') and o(m, 'CT02BasinHighLevelAlarm') and o(m, 'CH01StartSuccess'), f"low={o(m, 'CT01BasinLowLevelAlarm')} high={o(m, 'CT02BasinHighLevelAlarm')}")
# ------------------------------------------------------------------ A: air side (site timers)
AIR = ['AHU01_StartCmd', 'AHU01_Status', 'AHU01_ValveCmd', 'AHU01_SAT', 'AHU01_SAT_SP', 'AHU01_SpeedCmd', 'AHU01_DuctStatic', 'AHU01_OADamperCmd']
sch_on = setout(Sch_AHU=True, Sch_FCU=True, Sch_EF=True, Sch_CarPark=True)
m, tr = sim(SITE, [(0.0, sch_on), (0.0, {'AHU01_RAT': 24.5, 'AHU01_RA_CO2': 950.0})], 1200, extra=AIR, every=10.0, base=False)
ok = (o(m, 'AHU01_Status') and abs(o(m, 'AHU01_SAT') - o(m, 'AHU01_SAT_SP')) < 0.6 and abs(o(m, 'AHU01_DuctStatic') - 250) < 15
      and abs(o(m, 'AHU01_SAT_SP') - 14.25) < 0.1 and 55 < o(m, 'AHU01_OADamperCmd') < 65)
row('A01', 'AHU', 'AHU start, SAT reset, valve PID, static PID, CO2 DCV', 'RAT 24.5 (SP 24) -> SAT SP 14.25; SAT tracks; static 250 Pa; CO2 950 -> OA damper 60 %',
    ok, f"SAT {o(m, 'AHU01_SAT'):.2f}/{o(m, 'AHU01_SAT_SP'):.2f} valve {o(m, 'AHU01_ValveCmd'):.0f} %; static {o(m, 'AHU01_DuctStatic'):.0f} Pa @ {o(m, 'AHU01_SpeedCmd'):.0f} %; OAD {o(m, 'AHU01_OADamperCmd'):.0f} %")
m, tr = sim(SITE, [(0.0, sch_on), (300.0, {'FireAlarmSignal': True})], 420, extra=AIR + ['LSF01_StartCmd', 'SEF01_StartCmd', 'CPEF01_SpeedCmd', 'FCU01_StartCmd', 'LSF01_StairDP'], every=5.0, base=False)
ok = (not o(m, 'AHU01_StartCmd') and not o(m, 'FCU01_StartCmd') and o(m, 'LSF01_StartCmd') and o(m, 'SEF01_StartCmd') and o(m, 'CPEF01_SpeedCmd') > 99
      and abs(o(m, 'LSF01_StairDP') - 45) < 5 and o(m, 'AHU01_ValveCmd') == 0)
row('A02', 'Fire', 'Fire alarm', 'AHU/FCU stop, valves close; stair pressurisation + smoke exhaust start; car-park fan 100 %; stair dP controlled to 45 Pa',
    ok, f"AHU01={o(m, 'AHU01_StartCmd')} FCU01={o(m, 'FCU01_StartCmd')} LSF01={o(m, 'LSF01_StartCmd')} dP {o(m, 'LSF01_StairDP'):.0f} Pa SEF01={o(m, 'SEF01_StartCmd')} CPEF01 {o(m, 'CPEF01_SpeedCmd'):.0f} %")
m, tr = sim(SITE, [(0.0, sch_on), (0.0, {'FCU01_RoomTemp': 26.0, 'FCU02_RoomTemp': 24.9, 'FCU03_RoomTemp': 23.0, 'FCU04_RoomTemp': 60.0})], 200,
            extra=['FCU01_FanHighCmd', 'FCU02_FanMedCmd', 'FCU03_FanLowCmd', 'FCU03_ValveCmd', 'FCU04_FanMedCmd', 'FCU04_ValveCmd'], every=5.0, base=False)
ok = (o(m, 'FCU01_FanHighCmd') and o(m, 'FCU01_ValveCmd') and o(m, 'FCU02_FanMedCmd') and o(m, 'FCU03_FanLowCmd') and not o(m, 'FCU03_ValveCmd')
      and abs(o(m, 'FCU04_ControlTemp') - o(m, 'Zone_FCU_AvgTemp')) < 0.01 and o(m, 'FCU04_RoomTemp_SensorAlarm'))
row('A03', 'FCU', 'FCU 3-speed bands and fail-safe', 'SP+2 -> HIGH + valve; SP+0.9 -> MED; SP-1 -> LOW, valve closed; sensor 60 degC invalid -> alarm + control from zone average (V7.7 r1)',
    ok, ' '.join(f"{k}={int(o(m, k))}" for k in ('FCU01_FanHighCmd', 'FCU02_FanMedCmd', 'FCU03_FanLowCmd', 'FCU03_ValveCmd', 'FCU04_FanMedCmd', 'FCU04_ValveCmd')) + f" FCU04 ctrl {o(m, 'FCU04_ControlTemp'):.2f} zone {o(m, 'Zone_FCU_AvgTemp'):.2f}")
m, tr = sim(SITE, [(0.0, sch_on), (0.0, {'AHU01_SAT': 99.0, 'AHU01_DuctStatic': -50.0, 'AHU01_Overload': False})], 300, extra=AIR, every=5.0, base=False)
row('A04', 'AHU', 'AHU sensor failures', 'SAT invalid -> valve 60 %; static invalid -> fan 80 %; alarms', o(m, 'AHU01_ValveCmd') == 60.0 and abs(o(m, 'AHU01_SpeedCmd') - 80) < 0.5 and o(m, 'AHU01_SAT_SensorAlarm'),
    f"valve {o(m, 'AHU01_ValveCmd'):.0f} % speed {o(m, 'AHU01_SpeedCmd'):.0f} % alarm={o(m, 'AHU01_SAT_SensorAlarm')}")
m, tr = sim(SITE, [(0.0, sch_on), (0.0, {'AHU01_Status': False})], 200, extra=AIR, every=5.0, base=False)
row('A05', 'AHU', 'Fan fails to prove', 'Fan-fail alarm after 30 s; valve and OA damper stay closed', o(m, 'AHU01_FanFailAlarm') and o(m, 'AHU01_ValveCmd') == 0 and o(m, 'AHU01_OADamperCmd') == 0,
    f"FanFail={o(m, 'AHU01_FanFailAlarm')} valve {o(m, 'AHU01_ValveCmd')} OAD {o(m, 'AHU01_OADamperCmd')}")
m, tr = sim(SITE, [(0.0, sch_on), (0.0, {'CPEF01_CO': 37.5, 'EF02_Overload': True})], 200, extra=['CPEF01_SpeedCmd', 'EF02_StartCmd'], every=5.0, base=False)
row('A06', 'Fans', 'Car-park CO ramp; exhaust fan overload', 'CO 37.5 ppm -> 65 %; EF02 overload -> not started + alarm', abs(o(m, 'CPEF01_SpeedCmd') - 65) < 1 and not o(m, 'EF02_StartCmd'),
    f"CPEF01 {o(m, 'CPEF01_SpeedCmd'):.1f} %; EF02 cmd={o(m, 'EF02_StartCmd')}")
m, tr = sim(SITE, [(0.0, sch_on), (0.0, {'PlantDemandMode': True, 'AHU01_RAT': 27.0, 'AHU02_RAT': 27.0, 'PlantEnable': True, 'BootQualified': True})], 2400,
            extra=['AirSide_CoolingCalls', 'AirSide_ChwRequests', 'PlantRunRequest', 'PlantResetPct', 'TR_Use'], every=10.0, base=False)
t_run = ft(tr, lambda s: s['PlantRunRequest'])
row('A07', 'Plant I/F', 'Plant demand mode + Trim & Respond from AHU valve requests',
    'Calls >= 1 for 5 min -> plant enabled; AHUs at 100 % valve -> requests -> plant reset request rises (T&R)',
    o(m, 'PlantRunRequest') and o(m, 'TR_Use') and o(m, 'PlantResetPct') > 10 and o(m, 'AirSide_ChwRequests') >= 1,
    f"plant run @{t_run}s; calls {o(m, 'AirSide_CoolingCalls'):.0f} requests {o(m, 'AirSide_ChwRequests'):.0f}; T&R active={o(m, 'TR_Use')} reset {o(m, 'PlantResetPct'):.0f} %")
m, tr = sim(SITE, [(0.0, sch_on), (0.0, {'LSF01_InAuto': False}), (100.0, {'FireAlarmSignal': True})], 200, extra=['LSF01_StartCmd'], every=5.0, base=False)
row('A08', 'Fire', 'Life-safety fan in HAND/OFF when fire alarm occurs', 'Emergency fire-fail alarm raised even though the fan was never commanded',
    o(m, 'LSF01_FireFailAlarm') and o(m, 'SEF01_StartCmd'), f"LSF01 fire-fail={o(m, 'LSF01_FireFailAlarm')} SEF01 cmd={o(m, 'SEF01_StartCmd')}")
m, tr = sim(SITE, [(0.0, sch_on), (300.0, {'AHU01_SmokeDetected': True}), (360.0, {'AHU01_SmokeDetected': False}), (420.0, fire('AHU01SmokeResetFire'))], 560,
            extra=['AHU01_StartCmd'], every=5.0, base=False)
t_off = ft(tr, lambda s: not s['AHU01_StartCmd'], 300); t_on = ft(tr, lambda s: s['AHU01_StartCmd'], 305)
row('A09', 'AHU', 'Duct smoke shutdown latched until RESET', 'Stops at smoke, stays off after detector clears, restarts only after RESET',
    t_off is not None and t_off <= 306 and t_on is not None and t_on >= 420, f"off @{t_off}s, restart @{t_on}s (RESET @420 s)")
print('PASS', sum(r['result'] == 'PASS' for r in rows), '/', len(rows))
if len(sys.argv) > 3:
    with open(sys.argv[3], 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
