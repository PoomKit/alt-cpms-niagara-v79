# -*- coding: utf-8 -*-
"""V7.9 r4 tests of the office VAV / metering layer and the slot protections, run on the layer test station (layer_sim.py).
No source station is needed: base plant values are inputs set by the test (offline model, fast-test timing).
usage: python3 v79office_tests.py [out.csv]        exit code 1 on a finding"""
import csv, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import layer_sim
from sim7 import Model6
from simstart import faithful

BOG = os.path.join(tempfile.mkdtemp(prefix='v79office_'), 'layer.bog')
layer_sim.write(layer_sim.build('fpt'), BOG)
rows = []


def row(cid, title, ok, obs):
    rows.append({'id': cid, 'title': title, 'observed': obs, 'result': 'PASS' if ok else 'FINDING'})
    print(f"{cid:4} {'PASS' if ok else 'FINDING':8} {title}\n     {obs}", flush=True)


def sim(ev, dur, K, every=5.0):
    m = faithful(Model6(BOG, dt=1.0)); return m.run(dur, ev, sample=K, every=every)


at = lambda tr, t, k: next(s[k] for tt_, s in tr if tt_ >= t - 1e-6)
ever = lambda tr, k: any(s[k] for t, s in tr)
A = 'AHU_F02_'; V = 'VAV_F02_A_M1_'; R = 'RM_F02_A_M1_'
ON = (0.5, {'AirX_ManualOn': True})

# O01 floor 2 in automatic: duct static, SAT, rooms, ventilation
K = [A + x for x in ('SAT', 'SAT_SP', 'DuctSP', 'DuctSP_SP', 'FanSpeedCmd', 'OAFlow', 'OAFlowSP', 'ValveCmd')] + [R + 'T', 'RM_F02_B_EXEC_T', 'RM_F02_B_OPEN_T']
tr = sim([ON], 420.0, K)
s = dict(tr[-1][1]); rooms = [s[R + 'T'], s['RM_F02_B_EXEC_T'], s['RM_F02_B_OPEN_T']]
row('O01', 'floor 2 VAV AHU: SAT at its T&R setpoint, duct static at its T&R setpoint, rooms 22.5-25.5 C, OA >= 90 % of Vot (ASHRAE 62.1)',
    abs(s[A + 'SAT'] - s[A + 'SAT_SP']) < 1.5 and abs(s[A + 'DuctSP'] - s[A + 'DuctSP_SP']) < 30 and all(22.5 < x < 25.5 for x in rooms)
    and s[A + 'OAFlow'] >= 0.9 * s[A + 'OAFlowSP'] and 25 <= s[A + 'DuctSP_SP'] <= 250 and 30 <= s[A + 'FanSpeedCmd'] <= 100,
    f"SAT {s[A + 'SAT']:.1f}/{s[A + 'SAT_SP']:.1f} C, DSP {s[A + 'DuctSP']:.0f}/{s[A + 'DuctSP_SP']:.0f} Pa, fan {s[A + 'FanSpeedCmd']:.0f} %, "
    f"rooms {', '.join(f'{x:.1f}' for x in rooms)} C, OA {s[A + 'OAFlow']:.0f}/{s[A + 'OAFlowSP']:.0f} L/s")
vot_occ = s[A + 'OAFlowSP']

# O02 dehumidification: return RH high -> SAT setpoint capped
tr = sim([ON, (60.0, {A + 'RA_RH': 75.0})], 150.0, [A + 'SAT_SP'])
row('O02', 'return RH 75 % -> SAT setpoint not above 13 C (dehumidification, hot-humid climate)', at(tr, 145, A + 'SAT_SP') <= 13.0 + 1e-6,
    f"SAT setpoint {at(tr, 145, A + 'SAT_SP'):.1f} C")

# O03 occupied-standby + DCV
tr = sim([ON, (0.5, {R + 'Occ': False})], 60.0, [V + 'CoolSPActive', A + 'OAFlowSP', V + 'AirflowSP'])
row('O03', 'room vacant (occupancy sensor) -> occupied-standby: setpoint +1 K, Vot drops by Rp x Pz / Ev (DCV)',
    abs(at(tr, 55, V + 'CoolSPActive') - 25.0) < 1e-6 and abs((vot_occ - at(tr, 55, A + 'OAFlowSP')) - 60.0 / 0.8) < 1.0,
    f"setpoint {at(tr, 55, V + 'CoolSPActive')}, Vot {vot_occ:.1f} -> {at(tr, 55, A + 'OAFlowSP'):.1f} L/s")

# O04 unoccupied
tr = sim([(0.5, {'Sch_AHU': False})], 40.0, [A + 'StartCmd', V + 'AirflowSP', A + 'OADamperCmd', A + 'RADamperCmd'])
row('O04', 'outside the schedule: AHU off, VAV airflow setpoint 0, OA / RA dampers closed',
    not at(tr, 35, A + 'StartCmd') and at(tr, 35, V + 'AirflowSP') == 0 and at(tr, 35, A + 'OADamperCmd') == 0 and at(tr, 35, A + 'RADamperCmd') == 0,
    f"start {at(tr, 35, A + 'StartCmd')}, airflow SP {at(tr, 35, V + 'AirflowSP')}, OA {at(tr, 35, A + 'OADamperCmd')}, RA {at(tr, 35, A + 'RADamperCmd')}")

# O05 high duct static safety (G36 5.16.8): trip, manual reset, restart
tr = sim([ON, (30.0, {A + 'DuctSP': 450.0}), (45.0, {A + 'DuctSP': None}), (50.0, {'PlantAlarmResetFire': True}), (52.0, {'PlantAlarmResetFire': False})],
         80.0, [A + 'StartCmd', A + 'HighStaticAlarm'], every=1.0)
row('O05', 'duct static 450 Pa -> fan stops with a latched alarm, restarts only after the reset',
    at(tr, 40, A + 'HighStaticAlarm') and not at(tr, 40, A + 'StartCmd') and not at(tr, 48, A + 'StartCmd') and at(tr, 70, A + 'StartCmd'),
    f"alarm {at(tr, 40, A + 'HighStaticAlarm')}, start at 40 s {at(tr, 40, A + 'StartCmd')}, 48 s {at(tr, 48, A + 'StartCmd')}, after reset {at(tr, 70, A + 'StartCmd')}")

# O06 fire alarm
tr = sim([ON, (30.0, {'NotFireAlarm': False})], 50.0, [A + 'StartCmd', A + 'OADamperCmd', A + 'RelDamperCmd'])
row('O06', 'fire alarm -> floor AHU off, OA and relief dampers closed (EIT fire practice)',
    at(tr, 25, A + 'StartCmd') and not at(tr, 45, A + 'StartCmd') and at(tr, 45, A + 'OADamperCmd') == 0 and at(tr, 45, A + 'RelDamperCmd') == 0,
    f"before {at(tr, 25, A + 'StartCmd')}, after {at(tr, 45, A + 'StartCmd')}, OA {at(tr, 45, A + 'OADamperCmd')}, relief {at(tr, 45, A + 'RelDamperCmd')}")

# O07 / O08 VAV alarms
tr = sim([ON, (30.0, {V + 'Airflow': 0.0, 'VAV_F02_B_M1_DmpFb': 0.0})], 90.0, [V + 'VeryLowAirflowAlarm', V + 'PressureReq', 'VAV_F02_B_M1_DamperFaultAlarm', 'VAV_F02_B_M1_DmpCmd'])
row('O07', 'VAV airflow 0 with a setpoint -> very low airflow alarm, 2 extra pressure requests (G36)',
    at(tr, 85, V + 'VeryLowAirflowAlarm') and at(tr, 85, V + 'PressureReq') >= 2, f"alarm {at(tr, 85, V + 'VeryLowAirflowAlarm')}, requests {at(tr, 85, V + 'PressureReq')}")
row('O08', 'VAV damper feedback stuck at 0 while commanded open -> damper fault alarm', at(tr, 85, 'VAV_F02_B_M1_DamperFaultAlarm'),
    f"alarm {at(tr, 85, 'VAV_F02_B_M1_DamperFaultAlarm')}, damper command {at(tr, 85, 'VAV_F02_B_M1_DmpCmd'):.0f} %")

# O09 room sensors
tr = sim([ON, (10.0, {R + 'CO2': 1300.0, 'RM_F02_B_M2_T': 80.0})], 60.0, [V + 'CO2HighAlarm', 'RM_F02_B_M2_SensorFaultAlarm', 'VAV_F02_B_M2_CoolLoop'])
row('O09', 'room CO2 1300 ppm -> CO2 alarm; room sensor 80 C -> sensor fault, cooling loop disabled',
    at(tr, 55, V + 'CO2HighAlarm') and at(tr, 55, 'RM_F02_B_M2_SensorFaultAlarm') and at(tr, 55, 'VAV_F02_B_M2_CoolLoop') == 0,
    f"CO2 {at(tr, 55, V + 'CO2HighAlarm')}, sensor fault {at(tr, 55, 'RM_F02_B_M2_SensorFaultAlarm')}, loop {at(tr, 55, 'VAV_F02_B_M2_CoolLoop')}")

# O10-O13 metering
K = ['BTU_F03_kW', 'BTU_F03_LowDeltaTAlarm', 'BTU_F03_MeterFaultAlarm', 'PM_F02_ReconcileAlarm']
tr = sim([(0.5, {'FM_F03_Flow': 20.0, 'TT_S_F03': 7.0, 'TT_R_F03': 12.0}), (10.0, {'TT_R_F03': 8.5}), (50.0, {'TT_R_F03': 6.0}),
          (0.5, {'PM_F02_kW': 50.0})], 80.0, K)
row('O10', 'floor BTU meter: 20 m3/h x 5 K -> 116.3 kW', abs(at(tr, 5, 'BTU_F03_kW') - 116.28) < 0.1, f"{at(tr, 5, 'BTU_F03_kW'):.2f} kW")
row('O11', 'CHW dT 1.5 K with flow for the alarm time -> low dT alarm', at(tr, 45, 'BTU_F03_LowDeltaTAlarm'), f"{at(tr, 45, 'BTU_F03_LowDeltaTAlarm')}")
row('O12', 'negative dT with flow -> meter fault alarm, energy rate not negative', at(tr, 75, 'BTU_F03_MeterFaultAlarm') and at(tr, 75, 'BTU_F03_kW') == 0,
    f"fault {at(tr, 75, 'BTU_F03_MeterFaultAlarm')}, kW {at(tr, 75, 'BTU_F03_kW')}")
row('O13', 'tenant sub-meters 70 kW > floor meter 50 kW -> reconciliation alarm', at(tr, 45, 'PM_F02_ReconcileAlarm'), f"{at(tr, 45, 'PM_F02_ReconcileAlarm')}")

# O14 floor 1 VAV on AHU-01
tr = sim([(0.5, {'AHU01_Status': True})], 30.0, ['VAV_G_LOB_AirflowSP', 'VAV_G_LOB_DmpCmd'])
row('O14', 'floor 1 lobby VAV runs with AHU-01 (V7.8 AHU)', at(tr, 25, 'VAV_G_LOB_AirflowSP') > 0 and at(tr, 25, 'VAV_G_LOB_DmpCmd') > 0,
    f"airflow SP {at(tr, 25, 'VAV_G_LOB_AirflowSP'):.0f} L/s, damper {at(tr, 25, 'VAV_G_LOB_DmpCmd'):.0f} %")

# P01 / P02 expansion chiller protections, P03 basement flood
PL = {'PlantRunRequest': True, 'Stage2Request': True, 'PlantStage': 1.0, 'CH03_Installed': True, 'CH04_Installed': True, 'Sim_AnyCHP_RunFb': True,
      'Sim_AnyCDP_RunFb': True, 'CHWS': 7.0, 'CHWR': 12.0}
tr = sim([(0.5, PL), (60.0, {'CHWS': 2.0})], 90.0, ['CH03RunProof', 'CH03_FreezeTripAlarm', 'CH03StartCmd'], every=1.0)
row('P01', 'expansion chiller CH03 leaving water 2 C while running -> freeze trip (latched alarm), compressor stops',
    at(tr, 55, 'CH03RunProof') and at(tr, 85, 'CH03_FreezeTripAlarm') and not at(tr, 85, 'CH03StartCmd'),
    f"running {at(tr, 55, 'CH03RunProof')}, trip {at(tr, 85, 'CH03_FreezeTripAlarm')}, start at 85 s {at(tr, 85, 'CH03StartCmd')}")
tr = sim([(0.5, dict(PL, EXP_RotateByRuntime=False)), (60.0, {'CHX_Enable': False}), (75.0, {'CHX_Enable': True})], 110.0, ['CH03StartCmd'], every=1.0)
off = next((t for t, s in tr if t > 60 and not s['CH03StartCmd']), None); back = next((t for t, s in tr if off and t > off and s['CH03StartCmd']), None)
row('P02', 'CH03 stopped then asked again (rotation off) -> no restart before the anti-recycle time (test 15 s)',
    off is not None and back is not None and back - off >= 15.0 - 1e-6, f"stopped {off} s, restarted {back} s")
tr = sim([(5.0, {'PlantRoom_FloodSw': True})], 20.0, ['PlantRoom_FloodAlarm', 'PR_FloodStop'], every=1.0)
row('P03', 'B1 plant room flood switch -> emergency alarm and chiller stop signal', at(tr, 15, 'PlantRoom_FloodAlarm') and at(tr, 15, 'PR_FloodStop'),
    f"alarm {at(tr, 15, 'PlantRoom_FloodAlarm')}, stop {at(tr, 15, 'PR_FloodStop')}")

# O15 / O16 toilet exhaust dampers (r5, R9 MD-EA): schedule, fire close, end-switch proof
E = 'TE_F02_A_WC_'
tr = sim([(0.5, {'Sch_AHU': True}), (20.0, {'NotFireAlarm': False})], 30.0, [E + 'DmpCmd', E + 'DmpFb', E + 'DamperFaultAlarm', 'TE_F03_B_JAN_DmpCmd'], every=1.0)
row('O15', 'toilet exhaust damper opens on the schedule (end switch proves open), closes on fire alarm (TE_CloseOnFire)',
    at(tr, 15, E + 'DmpCmd') and at(tr, 15, E + 'DmpFb') and at(tr, 15, 'TE_F03_B_JAN_DmpCmd') and not at(tr, 25, E + 'DmpCmd') and not ever(tr, E + 'DamperFaultAlarm'),
    f"cmd {at(tr, 15, E + 'DmpCmd')} fb {at(tr, 15, E + 'DmpFb')} -> fire: cmd {at(tr, 25, E + 'DmpCmd')}, fault {ever(tr, E + 'DamperFaultAlarm')}")
tr = sim([(0.5, {'Sch_AHU': True}), (1.0, {E + 'DmpFb': False})], 20.0, [E + 'DmpCmd', E + 'DamperFaultAlarm'], every=1.0)
row('O16', 'exhaust damper commanded open, end switch stays closed -> damper fault alarm (test 4 s)',
    at(tr, 15, E + 'DmpCmd') and at(tr, 15, E + 'DamperFaultAlarm'), f"cmd {at(tr, 15, E + 'DmpCmd')}, fault {at(tr, 15, E + 'DamperFaultAlarm')}")

if len(sys.argv) > 1:
    with open(sys.argv[1], 'w', newline='', encoding='utf-8') as fo:
        w = csv.DictWriter(fo, fieldnames=['id', 'title', 'observed', 'result']); w.writeheader(); w.writerows(rows)
print(f"{sum(r['result'] == 'PASS' for r in rows)}/{len(rows)} PASS")
sys.exit(0 if all(r['result'] == 'PASS' for r in rows) else 1)
