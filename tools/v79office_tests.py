# -*- coding: utf-8 -*-
"""V7.9 r4-r6 tests of the office VAV / metering layer, the r6 sequences and the slot protections, run on the layer test station (layer_sim.py).
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

# R01-R08: r6 sequences (v79_r6.py)
K = ['OAU01_Airflow_SP', 'OAU_DemandLs'] + [f'AHU_F{f:02d}_OAFlowSP' for f in range(2, 9)]
tr = sim([ON, (0.5, {'AHU01_Status': True, 'AHU02_Status': False})], 60.0, K)
s = dict(tr[-1][1]); dem = sum(s[f'AHU_F{f:02d}_OAFlowSP'] for f in range(2, 9)) + 939.4
row('R01', 'OAU-01 airflow setpoint = (sum of floor Vot + running ground-floor AHU design OA) x 3.6 x 1.1 (DCV cascade)',
    abs(s['OAU01_Airflow_SP'] - max(2000.0, dem * 3.6 * 1.1)) < 5.0, f"demand {s['OAU_DemandLs']:.0f} L/s -> OAU setpoint {s['OAU01_Airflow_SP']:.0f} m3/h")
tr = sim([(0.5, {'AHU01_Status': True, 'AHU01_OADamperCmd': 40.0})], 40.0, ['AHU01_RADamperCmd', 'AHU01_RelDamperCmd', 'AHU01_OAFlow', 'AHU01_VentilationLowAlarm'])
row('R02', 'AHU-01: RA damper = 100 - OA, relief tracks OA, OA airflow 80 % of design -> ventilation low alarm',
    at(tr, 35, 'AHU01_RADamperCmd') == 60.0 and at(tr, 35, 'AHU01_RelDamperCmd') == 40.0 and at(tr, 35, 'AHU01_VentilationLowAlarm'),
    f"RA {at(tr, 35, 'AHU01_RADamperCmd')}, relief {at(tr, 35, 'AHU01_RelDamperCmd')}, OA {at(tr, 35, 'AHU01_OAFlow'):.0f} L/s, alarm {at(tr, 35, 'AHU01_VentilationLowAlarm')}")
tr = sim([(0.5, {'Sch_AHU': True}), (20.0, {'NotFireAlarm': False})], 30.0, ['TEF_StartCmd', 'TEF_Status', 'TEF_FailAlarm'], every=1.0)
row('R03', 'toilet exhaust fan runs with the toilet dampers (schedule), proven, stops on fire alarm',
    at(tr, 10, 'TEF_StartCmd') and at(tr, 10, 'TEF_Status') and not at(tr, 25, 'TEF_StartCmd') and not ever(tr, 'TEF_FailAlarm'),
    f"run {at(tr, 10, 'TEF_Status')}, after fire cmd {at(tr, 25, 'TEF_StartCmd')}")
tr = sim([(0.5, {'HOOD1_On': True}), (20.0, {'Hood_SuppressionReleased': True})], 30.0,
         ['KEF_StartCmd', 'KEF_Status', 'MAU_StartCmd', 'MAU_SpeedCmd', 'Kitchen_GasShutoff', 'Hood_SuppressionAlarm'], every=1.0)
row('R04', 'hood on -> KEF, MAU only after KEF proof at 85 %; suppression release -> MAU stops, gas shut off, KEF keeps running (strategy)',
    at(tr, 15, 'KEF_Status') and at(tr, 15, 'MAU_StartCmd') and at(tr, 15, 'MAU_SpeedCmd') == 85.0 and not at(tr, 0.5, 'MAU_StartCmd')
    and not at(tr, 25, 'MAU_StartCmd') and at(tr, 25, 'KEF_StartCmd') and at(tr, 25, 'Kitchen_GasShutoff') and at(tr, 25, 'Hood_SuppressionAlarm'),
    f"MAU {at(tr, 15, 'MAU_StartCmd')} {at(tr, 15, 'MAU_SpeedCmd')} %, after release MAU {at(tr, 25, 'MAU_StartCmd')} KEF {at(tr, 25, 'KEF_StartCmd')} gas {at(tr, 25, 'Kitchen_GasShutoff')}")
tr = sim([ON], 240.0, ['RF_StartCmd', 'RF_SpeedCmd', 'BLDG_DP'])
row('R05', 'relief fan holds the building static pressure near +12 Pa while the AHUs run (G36 5.16.10)',
    at(tr, 235, 'RF_StartCmd') and 6.0 <= at(tr, 235, 'BLDG_DP') <= 18.0, f"RF {at(tr, 235, 'RF_SpeedCmd'):.0f} %, building {at(tr, 235, 'BLDG_DP'):.1f} Pa")
tr = sim([(1.0, {'PlantRoom_EmergencyVentCmd': True}), (20.0, {'PlantRoom_EmergencyVentCmd': False, 'PR_Temp': 35.0}), (40.0, {'PR_Temp': 27.0})], 60.0,
         ['PAF_StartCmd', 'PEF_SpeedCmd', 'PAF_Status'], every=1.0)
row('R06', 'B1 emergency ventilation (V7.7 refrigerant detection) -> PAF / PEF at 100 %; room 35 C -> heat ventilation at normal speed; 27 C -> off',
    at(tr, 15, 'PAF_StartCmd') and at(tr, 15, 'PEF_SpeedCmd') == 100.0 and at(tr, 15, 'PAF_Status') and at(tr, 35, 'PEF_SpeedCmd') == 50.0 and not at(tr, 58, 'PAF_StartCmd'),
    f"emergency {at(tr, 15, 'PEF_SpeedCmd')} %, heat {at(tr, 35, 'PEF_SpeedCmd')} %, cool room {at(tr, 58, 'PAF_StartCmd')}")
tr = sim([ON], 200.0, ['PLANT_TotalCalls', 'PLANT_TotalRunning', 'PLANT_TotalReqs', 'AHU_F02_ValveCmd'])
row('R11', 'floors 2-8 AHUs count in the plant demand / T&R totals (cooling calls, running units)',
    at(tr, 195, 'PLANT_TotalRunning') >= 7 and at(tr, 195, 'PLANT_TotalCalls') >= 1,
    f"running {at(tr, 195, 'PLANT_TotalRunning')}, calls {at(tr, 195, 'PLANT_TotalCalls')}, requests {at(tr, 195, 'PLANT_TotalReqs')}")
E = 'EPMS_F02_A_'
tr = sim([(0.5, {'PM_F02_A_kWh': 1000.0}), (2.0, {'EPMS_PeriodClose': True}), (4.0, {'EPMS_PeriodClose': False}), (10.0, {'PM_F02_A_kWh': 1250.0}),
          (20.0, {'PM_F02_A_kWh': 900.0})], 25.0, [E + 'PeriodStart_kWh', E + 'Period_kWh', E + 'QualityOK', E + 'MeterResetAlarm'], every=1.0)
row('R07', 'EPMS: period close latches the register (1000 kWh), period energy 250 kWh good; register 900 kWh -> reset alarm, billing hold',
    at(tr, 15, E + 'PeriodStart_kWh') == 1000.0 and abs(at(tr, 15, E + 'Period_kWh') - 250.0) < 1e-6 and at(tr, 15, E + 'QualityOK')
    and at(tr, 24, E + 'MeterResetAlarm') and not at(tr, 24, E + 'QualityOK'),
    f"start {at(tr, 15, E + 'PeriodStart_kWh')}, period {at(tr, 15, E + 'Period_kWh')}, after 900: reset {at(tr, 24, E + 'MeterResetAlarm')} quality {at(tr, 24, E + 'QualityOK')}")
tr = sim([(0.5, {'CS_F02_PUBLIC_T': 60.0})], 15.0, ['CS_F02_PUBLIC_SensorFaultAlarm'], every=1.0)
row('R08', 'corridor sensor reading 60 C -> sensor fault alarm', at(tr, 14, 'CS_F02_PUBLIC_SensorFaultAlarm'), f"{at(tr, 14, 'CS_F02_PUBLIC_SensorFaultAlarm')}")

tr = sim([(0.5, {'BTU_F02_kW': 120.0, 'VAV_F02_A_M1_Airflow': 300.0})], 40.0, ['EPMS_F02_A_AirShare', 'EPMS_F02_A_Thermal_kW', 'EPMS_F02_A_Thermal_kWh'], every=2.0)
s = dict(tr[-1][1])
row('R10', 'tenant thermal allocation = floor BTU x tenant airflow share; register integrates every minute (test 2 s)',
    s['EPMS_F02_A_AirShare'] > 0 and abs(s['EPMS_F02_A_Thermal_kW'] - 120.0 * s['EPMS_F02_A_AirShare']) < .01 and at(tr, 39, 'EPMS_F02_A_Thermal_kWh') > at(tr, 11, 'EPMS_F02_A_Thermal_kWh') > 0,
    f"share {s['EPMS_F02_A_AirShare']:.3f}, {s['EPMS_F02_A_Thermal_kW']:.1f} kW_th, register {at(tr, 11, 'EPMS_F02_A_Thermal_kWh'):.2f} -> {at(tr, 39, 'EPMS_F02_A_Thermal_kWh'):.2f} kWh_th")
C = 'COIL_AHU_F03_'
tr = sim([ON, (60.0, {C + 'CHR_T': 8.0}), (61.0, {'ISO_AHU_F03_CHS_Fb': False})], 100.0, [C + 'DeltaT', C + 'LowDeltaTAlarm', 'ISO_AHU_F03_CHS_Cmd', 'ISO_AHU_F03_CHS_FailAlarm', 'AHU_F03_ValveCmd'])
row('R09', 'coil dT from the coil TT pair; dT 1 K with the PICV open -> coil low dT alarm; isolation valve commanded open without end switch -> alarm',
    at(tr, 55, C + 'DeltaT') > 3.0 and at(tr, 98, C + 'LowDeltaTAlarm') and at(tr, 98, 'ISO_AHU_F03_CHS_Cmd') and at(tr, 98, 'ISO_AHU_F03_CHS_FailAlarm'),
    f"dT {at(tr, 55, C + 'DeltaT'):.1f} K (valve {at(tr, 55, 'AHU_F03_ValveCmd'):.0f} %) -> low dT {at(tr, 98, C + 'LowDeltaTAlarm')}, valve alarm {at(tr, 98, 'ISO_AHU_F03_CHS_FailAlarm')}")

if len(sys.argv) > 1:
    with open(sys.argv[1], 'w', newline='', encoding='utf-8') as fo:
        w = csv.DictWriter(fo, fieldnames=['id', 'title', 'observed', 'result']); w.writeheader(); w.writerows(rows)
print(f"{sum(r['result'] == 'PASS' for r in rows)}/{len(rows)} PASS")
sys.exit(0 if all(r['result'] == 'PASS' for r in rows) else 1)
