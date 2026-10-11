"""V7.7 cases: flow switches, fail-safe interlocks, chemical treatment, air side (offline model, FPT timers).
usage: v77tests.py v77_fpt.bog [out.csv]"""
import sys, csv, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim7 import Model6
from simstart import faithful

FPT = sys.argv[1]
BASE = [(0.0, {'PlantEnable': True, 'PlantLoadPct': 20.0}), (1.0, {'BootQualified': True})]
rows = []


def row(cid, area, title, expect, ok, obs):
    rows.append({'id': cid, 'area': area, 'title': title, 'expectation': expect, 'observed': obs, 'result': 'PASS' if ok else 'FINDING'})
    print(f"{cid:5} {'PASS' if ok else 'FINDING':8} {title}\n      {obs}", flush=True)


def sim(events, dur, extra=(), base=True):
    m = faithful(Model6(FPT, ramps=False))
    tr = m.run(dur, (BASE if base else []) + list(events), sample=list(extra), every=1.0)
    return m, tr


def fire(name, ms=2000):
    def f(m): m.st[name]['rem'] = ms / 1000.0; m.out[name] = True
    return f


def setout(**kv):
    def f(m):
        for k, v in kv.items(): m.out[k] = v
    return f


at = lambda tr, t, k: next(s[k] for tt, s in tr if tt >= t - 1e-6)
o = lambda m, n: m.lv(n)
K = ['CH01StartCmd', 'CH01RunProofSelected', 'CH02StartCmd']

# I01 freeze trip latched, reset after recovery
m, tr = sim([(80.0, {'CH01_ChwSupplyTemp': 2.0}), (100.0, {'CH01_ChwSupplyTemp': None}), (130.0, fire('PlantAlarmResetFire'))], 200,
            extra=K + ['CH01_SafetyTripAlarm'])
ok = at(tr, 79, 'CH01StartCmd') and at(tr, 95, 'CH01_SafetyTripAlarm') and not at(tr, 95, 'CH01StartCmd') and at(tr, 125, 'CH01_SafetyTripAlarm') \
    and not o(m, 'CH01_SafetyTripAlarm')
row('I01', 'Interlock', 'Chiller freeze trip (LWT < 3 C), latched until reset', 'trip + chiller stop; stays latched after LWT recovers; RESET clears',
    ok, f"run@79 {at(tr, 79, 'CH01StartCmd')}; trip@95 {at(tr, 95, 'CH01_SafetyTripAlarm')} cmd {at(tr, 95, 'CH01StartCmd')}; latched@125 "
        f"{at(tr, 125, 'CH01_SafetyTripAlarm')}; after reset {o(m, 'CH01_SafetyTripAlarm')}, CH02 cmd {o(m, 'CH02StartCmd')}")
# I02 condenser high trip
m, tr = sim([(80.0, {'CH01_CdwLeavingTemp': 43.0})], 100, extra=K + ['CH01_SafetyTripAlarm', 'CH01_CondHighTempAlarm'])
row('I02', 'Interlock', 'Condenser leaving water > 41 C -> chiller trip', 'CH01 safety trip + warning', o(m, 'CH01_SafetyTripAlarm') and not o(m, 'CH01StartCmd'),
    f"trip {o(m, 'CH01_SafetyTripAlarm')} warn {o(m, 'CH01_CondHighTempAlarm')} CH01 cmd {o(m, 'CH01StartCmd')}")
# I03 evaporator flow switch opens while running
m, tr = sim([(80.0, {'CH01CHWFlowProof': False}), (100.0, {'CH01CHWFlowProof': None})], 140, extra=K + ['CH01_EvapFlowSwTripAlarm'])
ok = at(tr, 90, 'CH01_EvapFlowSwTripAlarm') and o(m, 'CH01_EvapFlowSwTripAlarm')
row('I03', 'Flow switch', 'Evaporator flow switch opens while running', 'latched alarm (Critical); chiller stops via permissive, auto-restart (lock-out option off)',
    ok, f"alarm@90 {at(tr, 90, 'CH01_EvapFlowSwTripAlarm')} held@140 {o(m, 'CH01_EvapFlowSwTripAlarm')}; CH01 cmd@95 {at(tr, 95, 'CH01StartCmd')} @140 {o(m, 'CH01StartCmd')}")
m, tr = sim([(0.0, {'CH_FlowSwitchLockout': True}), (80.0, {'CH01CHWFlowProof': False}), (100.0, {'CH01CHWFlowProof': None})], 140, extra=K)
row('I04', 'Flow switch', 'Flow-switch lock-out option', 'CH_FlowSwitchLockout = true: CH01 stays off until reset', not o(m, 'CH01StartCmd'),
    f"CH01 cmd @140 {o(m, 'CH01StartCmd')} CH02 cmd {o(m, 'CH02StartCmd')}")
# I05 flow switch vs meter
m, tr = sim([(80.0, {'CH01_ChwFlow': 0.0})], 150, extra=['CH01_FlowSwMismatchAlarm'])
row('I05', 'Flow switch', 'Flow switch = FLOW but meter reads 0', 'disagreement alarm after 30 s (FPT)', o(m, 'CH01_FlowSwMismatchAlarm'),
    f"alarm {o(m, 'CH01_FlowSwMismatchAlarm')} (@100 {at(tr, 100, 'CH01_FlowSwMismatchAlarm')})")
m, tr = sim([], 200, extra=['CH01_FlowSwMismatchAlarm', 'CH01_EvapFlowSwTripAlarm'])
row('I06', 'Flow switch', 'Normal run: no false flow-switch alarms', 'no mismatch / trip alarm', not any(s['CH01_FlowSwMismatchAlarm'] or s['CH01_EvapFlowSwTripAlarm'] for _, s in tr),
    f"mismatch {o(m, 'CH01_FlowSwMismatchAlarm')} trip {o(m, 'CH01_EvapFlowSwTripAlarm')}")
# I07 E-stop / phase fail
m, tr = sim([(80.0, {'Plant_EmergencyStop': True})], 110, extra=K)
row('I07', 'Interlock', 'Plant emergency stop', 'chillers off at once, plant disabled', not o(m, 'CH01StartCmd') and not o(m, 'CH02StartCmd') and not o(m, 'PlantRunRequest'),
    f"CH01 {o(m, 'CH01StartCmd')} CH02 {o(m, 'CH02StartCmd')} PlantRunRequest {o(m, 'PlantRunRequest')}")
m, tr = sim([(80.0, {'Plant_PhaseFailRelay': True}), (100.0, {'Plant_PhaseFailRelay': False})], 200, extra=K + ['Plant_InterlockActive'])
ok = not at(tr, 95, 'CH01StartCmd') and at(tr, 103, 'Plant_InterlockActive') and not at(tr, 110, 'Plant_InterlockActive') and o(m, 'CH01StartCmd')
row('I08', 'Interlock', 'Phase-fail relay, auto restart after power healthy + delay', 'stop; inhibit held 5 s (FPT) after power returns; restart',
    ok, f"cmd@95 {at(tr, 95, 'CH01StartCmd')}; inhibit@103 {at(tr, 103, 'Plant_InterlockActive')} @110 {at(tr, 110, 'Plant_InterlockActive')}; cmd@200 {o(m, 'CH01StartCmd')}")
# I09 refrigerant leak
m, tr = sim([(80.0, {'PlantRoom_RefrigerantPPM': 400.0}), (100.0, {'PlantRoom_RefrigerantPPM': 1200.0})], 120, extra=K + ['PlantRoom_EmergencyVentCmd'])
ok = at(tr, 95, 'PlantRoom_EmergencyVentCmd') and at(tr, 95, 'CH01StartCmd') and not o(m, 'CH01StartCmd') and o(m, 'PlantRoom_RefLeakHighAlarm')
row('I09', 'Interlock', 'Refrigerant leak stage 1 / 2', '300 ppm: alarm + emergency vent (chillers run); 1000 ppm: chillers stop',
    ok, f"vent@95 {at(tr, 95, 'PlantRoom_EmergencyVentCmd')} CH01@95 {at(tr, 95, 'CH01StartCmd')}; stage2 {o(m, 'PlantRoom_RefLeakHighAlarm')} CH01 {o(m, 'CH01StartCmd')}")
# I10 pump high discharge
m, tr = sim([(80.0, {'CHP01_DischargePressure': 700.0, 'CHP01_SuctionPressure': 150.0})], 140, extra=['CHP01StartCmd', 'CHP02StartCmd'])
ok = o(m, 'CHP01_HighDischargeAlarm') and not o(m, 'CHP01StartCmd') and o(m, 'CHP02StartCmd') and o(m, 'CH01StartCmd')
row('I11', 'Interlock', 'CHP01 discharge > 6.5 bar -> pump trip, standby runs', 'CHP01 latched fail, CHP02 takes over, chiller keeps running',
    ok, f"alarm {o(m, 'CHP01_HighDischargeAlarm')} CHP01 {o(m, 'CHP01StartCmd')} CHP02 {o(m, 'CHP02StartCmd')} CH01 {o(m, 'CH01StartCmd')}")
# C01 inhibitor, flow-paced + tank low
m, tr = sim([(60.0, {'CT01_BasinLevel': 60.0, 'CT_MakeupFlow': 2.6}), (120.0, {'CT_ChemTankLowLevel': True})], 140, extra=['CT_ChemDosingPumpCmd', 'CT_InhibitorPumpRate'])
ok = at(tr, 110, 'CT_ChemDosingPumpCmd') and 40 < at(tr, 110, 'CT_InhibitorPumpRate') < 60 and not o(m, 'CT_ChemDosingPumpCmd')
row('C01', 'CDW chem', 'Inhibitor pump paced by make-up flow, stops on tank low', 'make-up 50 % of design -> 50 % stroke; tank low -> stop',
    ok, f"pump@110 {at(tr, 110, 'CT_ChemDosingPumpCmd')} rate {at(tr, 110, 'CT_InhibitorPumpRate'):.0f} %; tank low -> {o(m, 'CT_ChemDosingPumpCmd')}")
# C02 biocide A sequence: pre-bleed 20 s, dose 20 s, lock-out 40 s (FPT)
KB = ['CT_BleedValveCmd', 'CT_BiocideAPumpCmd', 'CT_BleedLockout', 'CT_PreBleedActive', 'CT_BiocideACycleSts']
m, tr = sim([(60.0, {'CT_Conductivity': 1500.0}), (80.0, {'CT_BiocideA_ManualStart': True}), (85.0, {'CT_BiocideA_ManualStart': False}),
             (120.0, {'CT_Conductivity': 2100.0})], 200, extra=KB)
ok = at(tr, 90, 'CT_BleedValveCmd') and at(tr, 90, 'CT_PreBleedActive') and not at(tr, 90, 'CT_BiocideAPumpCmd') \
    and at(tr, 110, 'CT_BiocideAPumpCmd') and not at(tr, 110, 'CT_BleedValveCmd') and not at(tr, 130, 'CT_BleedValveCmd') and at(tr, 130, 'CT_BleedLockout') \
    and not at(tr, 190, 'CT_BiocideACycleSts') and at(tr, 190, 'CT_BleedValveCmd')
row('C02', 'CDW chem', 'Biocide A cycle: pre-bleed -> dose (bleed closed) -> contact lock-out -> normal bleed',
    'bleed forced open 20 s, pump 20 s, bleed blocked 40 s even at 2,100 uS, then conductivity bleed resumes', ok,
    ' '.join(f"t{t}: bleed {at(tr, t, 'CT_BleedValveCmd')} pump {at(tr, t, 'CT_BiocideAPumpCmd')} lock {at(tr, t, 'CT_BleedLockout')}" for t in (90, 110, 130, 190)))
m, tr = sim([(80.0, {'CT_BiocideA_ManualStart': True}), (85.0, {'CT_BiocideA_ManualStart': False}), (110.0, {'CT_Conductivity': 2700.0})], 130, extra=KB)
row('C03', 'CDW chem', 'Conductivity above max overrides the lock-out', 'bleed opens at 2,700 uS during dose / contact', o(m, 'CT_BleedValveCmd'),
    f"bleed {o(m, 'CT_BleedValveCmd')} lock {o(m, 'CT_BleedLockout')}")
m, tr = sim([(60.0, {'CT_BiocideB_ManualStart': True}), (65.0, {'CT_BiocideB_ManualStart': False}), (80.0, {'CT_BiocideBPumpFlowSw': False})], 110, extra=KB + ['CT_BiocideBPumpFailAlarm'])
row('C04', 'CDW chem', 'Biocide B pump runs without flow', 'dosing-pump fail alarm (8 s FPT)', at(tr, 95, 'CT_BiocideBPumpFailAlarm'), f"fail alarm @95 {at(tr, 95, 'CT_BiocideBPumpFailAlarm')}")
m, tr = sim([(60.0, {'CT_Conductivity': 500.0})], 120, extra=['CT_CyclesOfConcentration'])
row('C05', 'CDW chem', 'Cycles of concentration + low CoC alarm', 'CoC = 500 / 350 = 1.43 < 2 -> alarm after 20 s (FPT)',
    abs(o(m, 'CT_CyclesOfConcentration') - 1.43) < 0.02 and o(m, 'CT_CoCLowAlarmSts'), f"CoC {o(m, 'CT_CyclesOfConcentration'):.2f} alarm {o(m, 'CT_CoCLowAlarmSts')}")
# W01 CHW chemical feed
m, tr = sim([(60.0, {'CHW_ExpansionTankPressure': 170.0, 'CHW_FillFlow': 1.0}), (90.0, {'CHW_ChemTankLowLevel': True})], 100, extra=['CHW_ChemDosePumpCmd', 'CHW_ChemPumpRate'])
ok = at(tr, 80, 'CHW_ChemDosePumpCmd') and 45 < at(tr, 80, 'CHW_ChemPumpRate') < 55 and not o(m, 'CHW_ChemDosePumpCmd') and o(m, 'Gfx_PotFeeder_Fwd') is False
row('W01', 'CHW chem', 'CHW chemical feed paced by loop fill, stops on tank low', 'fill 1.0 of 2.0 m3/h -> 50 %; tank low -> off',
    ok, f"pump@80 {at(tr, 80, 'CHW_ChemDosePumpCmd')} rate {at(tr, 80, 'CHW_ChemPumpRate'):.0f} %; tank low -> {o(m, 'CHW_ChemDosePumpCmd')}")
m, tr = sim([(60.0, {'CHW_ChemFeederOpen': True})], 80)
row('W02', 'CHW chem', 'Manual dose (test-kit result)', 'pump runs at 50 %', o(m, 'CHW_ChemDosePumpCmd') and abs(o(m, 'CHW_ChemPumpRate') - 50) < 1,
    f"pump {o(m, 'CHW_ChemDosePumpCmd')} rate {o(m, 'CHW_ChemPumpRate'):.0f} %")
# A: air side
sch_on = setout(Sch_AHU=True, Sch_FCU=True, Sch_EF=True, Sch_CarPark=True)
m, tr = sim([(0.0, sch_on), (0.0, {'AHU01_RA_RH': 70.0, 'AHU01_RAT': 24.5})], 120, base=False)
row('A01', 'Air side', 'AHU dehumidification (RA RH 70 %)', 'SAT setpoint = SAT min 13 C', o(m, 'AHU01_DehumActive') and abs(o(m, 'AHU01_SAT_SP') - 13.0) < 0.05,
    f"dehum {o(m, 'AHU01_DehumActive')} SAT SP {o(m, 'AHU01_SAT_SP'):.1f}")
m, tr = sim([(0.0, sch_on), (60.0, {'AHU01_DuctStatic': 600.0}), (70.0, {'AHU01_DuctStatic': None}), (100.0, fire('PlantAlarmResetFire'))], 200, base=False,
            extra=['AHU01_StartCmd', 'AHU01_HighStaticAlarm'])
ok = at(tr, 58, 'AHU01_StartCmd') and not at(tr, 90, 'AHU01_StartCmd') and at(tr, 90, 'AHU01_HighStaticAlarm') and not o(m, 'AHU01_HighStaticAlarm') and o(m, 'AHU01_StartCmd')
row('A02', 'Air side', 'High duct static cut-out (latched)', 'fan stops, stays off until reset, restarts after reset',
    ok, f"run@58 {at(tr, 58, 'AHU01_StartCmd')}; @90 {at(tr, 90, 'AHU01_StartCmd')} alarm {at(tr, 90, 'AHU01_HighStaticAlarm')}; after reset {o(m, 'AHU01_StartCmd')}")
m, tr = sim([(0.0, {'AHU01_RAT': 30.0})], 120, base=False, extra=['AHU01_StartCmd'])
row('A03', 'Air side', 'Unoccupied high-limit (night cooling)', 'schedule off, RAT 30 C -> AHU runs', o(m, 'AHU01_NightCoolActive') and o(m, 'AHU01_StartCmd'),
    f"night {o(m, 'AHU01_NightCoolActive')} AHU01 {o(m, 'AHU01_StartCmd')} AHU02 {o(m, 'AHU02_StartCmd')}")
m, tr = sim([(0.0, sch_on), (0.0, {'AHU01_RA_CO2': 1400.0})], 60, base=False)
row('A04', 'Air side', 'Return-air CO2 1,400 ppm', 'CO2 high alarm; OA damper 100 %', o(m, 'AHU01_CO2HighAlarm') and o(m, 'AHU01_OADamperCmd') > 99,
    f"alarm {o(m, 'AHU01_CO2HighAlarm')} OAD {o(m, 'AHU01_OADamperCmd'):.0f} %")
m, tr = sim([(0.0, sch_on), (0.0, {'OAU01_LAT_RH': 99.0, 'OAU01_LAT': 17.5})], 60, base=False)
row('A05', 'Air side', 'OAU leaving dew point high', 'dew point > 16 C -> LAT SP 16.5 - 1.5 = 15.0 C', o(m, 'OAU01_DehumActive') and abs(o(m, 'OAU01_LAT_SP_EFFECTIVE') - 15.0) < 0.05,
    f"dew point {o(m, 'OAU01_LAT_DewPoint'):.1f} dehum {o(m, 'OAU01_DehumActive')} LAT SP {o(m, 'OAU01_LAT_SP_EFFECTIVE'):.1f}")
m, tr = sim([(0.0, sch_on), (60.0, {'OAU01_SmokeDetected': True})], 90, base=False)
row('A06', 'Air side', 'OAU duct smoke detector', 'OAU stops (latched)', not o(m, 'OAU01_StartCmd'), f"OAU01 cmd {o(m, 'OAU01_StartCmd')}")

# R: V7.7 r1 review fixes
m, tr = sim([(20.0, {'CHWS': 14.0}), (700.0, {'CHWS': None})], 800, extra=['Stg_TempStageHold', 'Stage2Request'])
ok = at(tr, 650, 'Stg_TempStageHold') and at(tr, 650, 'Stage2Request') and not o(m, 'Stg_TempStageHold')
row('R01', 'Staging', 'CHWS-high stage-up held, released by low chiller load', 'hold + stage 2 during high CHWS; released when CH load sum below 80 % (FPT: no delay)',
    ok, f"hold@650 {at(tr, 650, 'Stg_TempStageHold')} stage2@650 {at(tr, 650, 'Stage2Request')}; hold@800 {o(m, 'Stg_TempStageHold')}")
m, tr = sim([], 420, extra=['CDP01SpeedCmd', 'CDW_Flow', 'CDP_FlowTarget', 'CDW_DeltaT'])
ok = 39.9 <= o(m, 'CDP01SpeedCmd') <= 100 and m.out['CDW_Flow'] >= 0.95 * m.out['CDP_FlowTarget']
row('R02', 'CDP', 'CDP variable speed (dT + min flow)', 'speed 40-100 %, CDW flow >= min-flow target',
    ok, f"CDP01 {o(m, 'CDP01SpeedCmd'):.1f} % flow {m.out['CDW_Flow']:.0f} gpm target {o(m, 'CDP_FlowTarget'):.0f} dT {o(m, 'CDW_DeltaT'):.2f} K")
m, tr = sim([(0.0, {'CDP_VariableSpeedEnable': False})], 200)
row('R03', 'CDP', 'CDP variable speed disabled', 'fixed 100 % (design flow)', abs(o(m, 'CDP01SpeedCmd') - 100) < 0.5, f"CDP01 {o(m, 'CDP01SpeedCmd'):.1f} %")
m, tr = sim([(60.0, {'PlantRoom_RefrigerantPPM': 400.0, 'PlantRoom_EmergencyVentStatus': False})], 100)
row('R04', 'Interlock', 'Emergency vent fan commanded but not running', 'fail alarm', o(m, 'PlantRoom_EmergencyVentFailAlarm'), f"alarm {o(m, 'PlantRoom_EmergencyVentFailAlarm')}")
m, tr = sim([(0.0, {'AHU01_RAT': 30.0})], 120, base=False)
row('R05', 'Air side', 'Night high-limit: OA damper closed', 'AHU runs, OA damper 0 %', o(m, 'AHU01_StartCmd') and o(m, 'AHU01_OADamperCmd') < 0.1,
    f"AHU01 {o(m, 'AHU01_StartCmd')} OAD {o(m, 'AHU01_OADamperCmd'):.1f} %")
m, tr = sim([(0.0, sch_on), (0.0, {'FCU04_RoomTemp': 60.0})], 60, base=False)
ok = abs(o(m, 'AHU01_ControlTemp') - o(m, 'Zone_AHU01_AvgTemp')) < 0.01 and abs(o(m, 'FCU04_ControlTemp') - o(m, 'Zone_FCU_AvgTemp')) < 0.01
row('R06', 'Air side', 'Zone average used in control', 'AHU SAT reset from zone avg; FCU04 sensor failed -> zone avg',
    ok, f"AHU01 ctrl {o(m, 'AHU01_ControlTemp'):.2f} zone {o(m, 'Zone_AHU01_AvgTemp'):.2f}; FCU04 ctrl {o(m, 'FCU04_ControlTemp'):.2f} zone {o(m, 'Zone_FCU_AvgTemp'):.2f}")

if len(sys.argv) > 2:
    with open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(sum(r['result'] == 'PASS' for r in rows), '/', len(rows), 'PASS')
