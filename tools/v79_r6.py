# -*- coding: utf-8 -*-
"""V7.9 r6: sequences the R9 building needs that the station did not have yet (all on top of the V7.9 r4/r5 layers).

  1 OAU-01 (roof DOAS feeding the OA riser): airflow setpoint follows the ventilation demand of the floors (sum of the AHU Vot
    setpoints + design OA of the running ground-floor AHUs, x margin) instead of a fixed design airflow (ASHRAE 62.1 DCV cascade)
  2 AHU-01 / AHU-02 (ground floor, V7.8 logic kept): R9 devices added - measured OA airflow, mixed-air temperature, RA damper
    (complement of the OA damper), relief damper (tracks OA), OA airflow low alarm (ASHRAE 62.1)
  3 TEF (roof toilet exhaust fan): runs while any toilet-exhaust damper is commanded open, stops on fire alarm with the dampers
    (TE_CloseOnFire), proof / fail alarm
  4 KEF (roof kitchen exhaust) + MAU (roof kitchen make-up air unit, CHW coil): hood switches / kitchen schedule start the KEF;
    the MAU only runs while the KEF is proven (kitchen kept negative, make-up = MAU_MakeupPct of the exhaust), MAU leaving-air
    temperature by PICV; hood fire-suppression release -> MAU stops, gas shut-off, KEF per fire strategy (NFPA 96 / EIT practice:
    KEF_RunOnFire); fire alarm -> MAU stops
  5 Relief fan RF (roof): building static pressure control (G36 5.16.10 relief-fan control), enabled while any AHU runs
  6 B1 plant room ventilation PAF / PEF: emergency ventilation from the V7.7 refrigerant detection (ASHRAE 15 / EN 378) and the purge
    switch at 100 %, heat ventilation by room temperature, normal ventilation while the plant runs
  9 plant link: floors 2-8 AHU cooling calls / CHW reset requests (G36 5.16.14) / running units added to the plant demand mode,
    T&R CHWST reset and dT guard; expansion slots 03-06 power added to Plant_kW
  7 Corridor sensors (R9, 30): temperature / RH / CO2 monitoring + sensor fault alarm
  8 EPMS export (tenant billing data): per tenant power register, period-start reading latched at the billing close, period
    energy, meter reset / rollover detection (billing hold), airflow-weighted thermal allocation of the floor BTU meter
    (informative; billable only with EPMS_TenantThermalBilling = Enabled by contract)
Every value is a parameter (design intent); commissioning and the engineer of record decide."""
import re
import make_v6 as M6
import make_v7 as M7
import v78_improve as IMP
import v79_scale as SC
import v79_office as OF
from make_v7 import AND, OR, NOT, DLY, SW, MATH, CMP, PID, PULSE, sealin, const, ai, di, simlink

AIR = M7.AIR
T, F = SC.T, SC.F
tm, alarm = IMP.tm, IMP.alarm
nm = OF.nm


def p(S, folder, n, v, u, note, prec=1):
    return S.param(n, v, u, folder=folder, prec=prec, note=note)


def fan(S, f, u, start_src, note):
    """start command + run proof + start failure alarm (proof missing 60 s) for a new fan"""
    S.bpoint(f, f'{u}_StartCmd', start_src, 'Start', 'Stop', kind='do', note=f'FIELD DO: {note} start')
    di(S, f, f'{u}_Status', False, 'Running', 'Stopped', note=f'FIELD DI: {note} run status (current switch)')
    NOT(S, f, f'{u}_NoProof', f'{u}_Status'); AND(S, f, f'{u}_CmdNoProof', f'{u}_StartCmd', f'{u}_NoProof')
    DLY(S, f, f'{u}_FailDly', f'{u}_CmdNoProof', tm(60000, 3000))
    alarm(S, f, f'{u}_FailAlarm', f'{u}_FailDly', 'Fail', 'Normal', 'Critical', f'{u}: commanded on, no run proof')
    sf = f'{AIR}/Simulation/Roof'
    DLY(S, sf, f'Sim_{u}_Run', f'{u}_StartCmd', tm(8000, 1000), tm(5000, 1000), note='simulation: motor start / stop time'); simlink(S, f'{u}_Status', f'Sim_{u}_Run')


def oau_cascade(S):
    f = f'{AIR}/OAU01/Ventilation'
    S.bparam('OAU_DemandReset', True, folder=f, t='Demand (sum of floors)', f='Fixed design airflow',
             note='OAU airflow setpoint follows the floors ventilation demand (ASHRAE 62.1 DCV cascade)')
    p(S, f, 'OAU_DemandMarginPct', 10.0, 'pct', 'margin on the summed OA demand (duct leakage, riser balance)', 0)
    p(S, f, 'OAU_MinAirflow', 2000.0, 'm3h_air', 'minimum OAU airflow while running (fan / coil stability)', 0)
    p(S, f, 'OAU_FixedAirflow', 6000.0, 'm3h_air', 'design airflow used when the demand reset is off', 0)
    flo = [f'AHU_F{fl:02d}_OAFlowSP' for fl in range(2, 9)]
    for u in ('AHU01', 'AHU02'):
        SW(S, f, f'OAU_{u}_Dem', f'{u}_Status', f'{u}_OADesignLs', 'Zero'); flo.append(f'OAU_{u}_Dem')
    SC.add_tree(S, f, 'OAU_DemandLs', flo)
    const(S, 'LsToM3h', 3.6, 'none', 1, 'L/s -> m3/h')
    MATH(S, f, 'OAU_DemandM3h0', 'Multiply', 'OAU_DemandLs', 'LsToM3h')
    MATH(S, f, 'OAU_MarginF', 'Multiply', 'OAU_DemandMarginPct', 'PctToFrac'); MATH(S, f, 'OAU_MarginF1', 'Add', 'OAU_MarginF', 'One')
    MATH(S, f, 'OAU_DemandM3h1', 'Multiply', 'OAU_DemandM3h0', 'OAU_MarginF1'); MATH(S, f, 'OAU_DemandM3h', 'Maximum', 'OAU_DemandM3h1', 'OAU_MinAirflow')
    SW(S, f, 'OAU_AirflowSPSel', 'OAU_DemandReset', 'OAU_DemandM3h', 'OAU_FixedAirflow')
    S.link(S.comp['OAU01_Airflow_SP'], 'OAU_AirflowSPSel', 'in16')
    S.log.append(('V7.9 r6', 'OAU01_Airflow_SP', 'in16 <- OAU_AirflowSPSel', 'demand cascade', '', ''))


def fahu(S, u, sid):
    """ground-floor AHU-01 / AHU-02: R9 devices on the V7.8 unit"""
    f = f'{AIR}/{u}/R9'
    sch = next(x for x in OF.od()['ahuSchedules'] if x['id'] == sid)
    p(S, f, f'{u}_OADesignLs', round(sch['OA_Ls_concept'], 1), 'Ls', 'design minimum OA (R9 concept, ASHRAE 62.1 VRP)', 0)
    ai(S, f, f'{u}_OAFlow', 0.0, 'Ls', 0, note=f'FIELD AI: {u} outdoor airflow measuring station')
    ai(S, f, f'{u}_MAT', 26.0, 'C', 1, note=f'FIELD AI: {u} mixed-air temperature (averaging)')
    MATH(S, f, f'{u}_RACalc', 'Subtract', 'HundredPct', f'{u}_OADamperCmd')
    SW(S, f, f'{u}_RAGate', f'{u}_Status', f'{u}_RACalc', 'Zero')
    S.npoint(f, f'{u}_RADamperCmd', f'{u}_RAGate', 'pct', 0, kind='ao', note=f'FIELD AO: {u} return-air damper (complement of OA)')
    SW(S, f, f'{u}_RelGate', f'{u}_Status', f'{u}_OADamperCmd', 'Zero')
    S.npoint(f, f'{u}_RelDamperCmd', f'{u}_RelGate', 'pct', 0, kind='ao', note=f'FIELD AO: {u} relief damper (tracks OA)')
    ai(S, f, f'{u}_RADmpFb', 0.0, 'pct', 0, note=f'FIELD AI: {u} RA damper position'); ai(S, f, f'{u}_RelDmpFb', 0.0, 'pct', 0, note=f'FIELD AI: {u} relief damper position')
    MATH(S, f, f'{u}_OALim', 'Multiply', f'{u}_OADesignLs', 'AHU_OAFlowLowPct', 'PctToFrac')
    CMP(S, f, f'{u}_OALow', 'LessThan', f'{u}_OAFlow', f'{u}_OALim'); AND(S, f, f'{u}_OALowA', f'{u}_OALow', f'{u}_Status')
    DLY(S, f, f'{u}_OALowDly', f'{u}_OALowA', tm(600000, 20000))
    alarm(S, f, f'{u}_VentilationLowAlarm', f'{u}_OALowDly', 'Low', 'Normal', 'Warning', f'{u}: outdoor airflow below 90 % of design minimum for 10 min (ASHRAE 62.1)')
    sf = f'{AIR}/Simulation/R9'
    MATH(S, sf, f'Sim_{u}_OAF', 'Multiply', f'{u}_OADesignLs', f'{u}_OADamperCmd', 'PctToFrac'); SW(S, sf, f'Sim_{u}_OAFl', f'{u}_Status', f'Sim_{u}_OAF', 'Zero')
    MATH(S, sf, f'Sim_{u}_OAFl2', 'Multiply', f'Sim_{u}_OAFl', 'Two'); simlink(S, f'{u}_OAFlow', f'Sim_{u}_OAFl2')    # OA damper ~50 % at design OA
    simlink(S, f'{u}_RADmpFb', f'{u}_RADamperCmd'); simlink(S, f'{u}_RelDmpFb', f'{u}_RelDamperCmd')


def tef(S, te):
    f = f'{AIR}/Roof/TEF'
    lv = [f'{n}_CmdLogic' for n in te]
    while len(lv) > 4:
        nxt = []
        for j in range(0, len(lv), 4):
            n = f'TE_Any_{len(nxt)}_{len(lv)}'; OR(S, f, n, *lv[j:j + 4]); nxt.append(n)
        lv = nxt
    OR(S, f, 'TE_AnyOpen', *lv)
    fan(S, f, 'TEF', 'TE_AnyOpen', 'toilet exhaust fan TEF (roof)')


def kitchen(S):
    f = f'{AIR}/Roof/Kitchen'
    S.bparam('KEF_RunOnFire', True, folder=f, t='Keep running', f='Stop', note='kitchen exhaust on fire alarm / suppression (PROJECT fire strategy, NFPA 96)')
    S.bparam('Kitchen_Schedule', False, folder=f, t='Kitchen open', f='Closed', note='food-court operating hours (or linked schedule)')
    p(S, f, 'MAU_MakeupPct', 85.0, 'pct', 'make-up air as % of exhaust (kitchen kept negative)', 0)
    p(S, f, 'MAU_SAT_SP', 16.0, 'C', 'make-up air leaving temperature setpoint (cooled / dehumidified OA)')
    hoods = []
    for i in range(1, 7):
        di(S, f, f'HOOD{i}_On', False, 'On', 'Off', note=f'FIELD DI: food stall {i} hood switch'); hoods.append(f'HOOD{i}_On')
    di(S, f, 'Hood_SuppressionReleased', False, 'Released', 'Normal', note='FIELD DI: hood wet-chemical suppression system released')
    OR(S, f, 'HoodAny0', *hoods[:4]); OR(S, f, 'HoodAny1', *hoods[4:]); OR(S, f, 'KEF_Req', 'HoodAny0', 'HoodAny1', 'Kitchen_Schedule')
    OR(S, f, 'KEF_FireOK', 'NotFireAlarm', 'KEF_RunOnFire')
    NOT(S, f, 'NoSuppression', 'Hood_SuppressionReleased'); OR(S, f, 'KEF_SupprOK', 'NoSuppression', 'KEF_RunOnFire')
    AND(S, f, 'KEF_StartLogic', 'KEF_Req', 'KEF_FireOK', 'KEF_SupprOK')
    fan(S, f, 'KEF', 'KEF_StartLogic', 'kitchen exhaust fan KEF (roof)')
    AND(S, f, 'MAU_StartLogic', 'KEF_Status', 'NotFireAlarm', 'NoSuppression')
    fan(S, f, 'MAU', 'MAU_StartLogic', 'kitchen make-up air unit MAU (roof)')
    SW(S, f, 'MAU_SpeedSel', 'MAU_StartCmd', 'MAU_MakeupPct', 'Zero')
    S.npoint(f, 'MAU_SpeedCmd', 'MAU_SpeedSel', 'pct', 0, kind='ao', note='FIELD AO: MAU fan speed (make-up % of exhaust)')
    ai(S, f, 'MAU_SAT', 20.0, 'C', 1, note='FIELD AI: MAU leaving-air temperature')
    PID(S, f, 'MAU_SatLoop', 'MAU_SAT', 'MAU_SAT_SP', 'MAU_Status', 'direct', 8.0, 1.0, 0.0, 100.0, note='MAU PICV: warmer than setpoint -> open')
    S.npoint(f, 'MAU_ValveCmd', 'MAU_SatLoop', 'pct', 0, kind='ao', note='FIELD AO: MAU PICV command')
    S.bpoint(f, 'Kitchen_GasShutoff', 'Hood_SuppressionReleased', 'Shut off', 'Normal', kind='do', note='FIELD DO: kitchen gas valve shut-off (suppression release)')
    alarm(S, f, 'Hood_SuppressionAlarm', 'Hood_SuppressionReleased', 'Released', 'Normal', 'Critical', 'Food court hood suppression released - MAU stopped, gas shut off')
    p(S, f, 'MAU_SatHiLim', 22.0, 'C', 'MAU leaving air above this for 15 min -> alarm'); CMP(S, f, 'MAU_SatHi', 'GreaterThan', 'MAU_SAT', 'MAU_SatHiLim')
    AND(S, f, 'MAU_SatHiA', 'MAU_SatHi', 'MAU_Status'); DLY(S, f, 'MAU_SatHiDly', 'MAU_SatHiA', tm(900000, 20000))
    alarm(S, f, 'MAU_SatHighAlarm', 'MAU_SatHiDly', 'High', 'Normal', 'Warning', 'MAU: leaving-air temperature high for 15 min (coil / PICV / CHW)')
    sf = f'{AIR}/Simulation/Roof'
    MATH(S, sf, 'Sim_MAU_Cool', 'Multiply', 'MAU_ValveCmd', 'PctToFrac', 'AirX_SimSupplyDT', 'Two'); MATH(S, sf, 'Sim_MAU_T0', 'Subtract', 'OA_Temperature', 'Sim_MAU_Cool')
    OF.ramp(S, sf, 'Sim_MAU_SAT', 'Sim_MAU_T0', tm(0.02, 0.5), 30.0); simlink(S, 'MAU_SAT', 'Sim_MAU_SAT')


def relief(S):
    f = f'{AIR}/Roof/Relief'
    p(S, f, 'BLDG_DP_SP', 12.0, 'Pa', 'building static pressure setpoint (positive vs outdoors, G36 5.16.10)', 0)
    p(S, f, 'BLDG_DP_HiLim', 40.0, 'Pa', 'building static above this for 5 min -> alarm (doors / relief)', 0)
    ai(S, f, 'BLDG_DP', 10.0, 'Pa', 1, note='FIELD AI: building static pressure (lobby level vs outdoors)')
    OR(S, f, 'AnyAHU0', 'AHU_F02_Status', 'AHU_F03_Status', 'AHU_F04_Status', 'AHU_F05_Status')
    OR(S, f, 'AnyAHU1', 'AHU_F06_Status', 'AHU_F07_Status', 'AHU_F08_Status', 'AHU01_Status'); OR(S, f, 'RF_Enable', 'AnyAHU0', 'AnyAHU1', 'AHU02_Status')
    fan(S, f, 'RF', 'RF_Enable', 'relief fan RF (roof)')
    PID(S, f, 'RF_DpLoop', 'BLDG_DP', 'BLDG_DP_SP', 'RF_Status', 'direct', 4.0, 0.5, 0.0, 100.0, note='building pressure above setpoint -> more relief')
    S.npoint(f, 'RF_SpeedCmd', 'RF_DpLoop', 'pct', 0, kind='ao', note='FIELD AO: relief fan speed')
    CMP(S, f, 'BLDG_DP_Hi', 'GreaterThan', 'BLDG_DP', 'BLDG_DP_HiLim'); DLY(S, f, 'BLDG_DP_HiDly', 'BLDG_DP_Hi', tm(300000, 20000))
    alarm(S, f, 'BLDG_DP_HighAlarm', 'BLDG_DP_HiDly', 'High', 'Normal', 'Warning', 'Building static pressure high for 5 min (relief / doors)')
    sf = f'{AIR}/Simulation/Roof'
    const(S, 'Sim_BDP_K', 30.0, 'none', 1, 'simulation: Pa per 100 % relief'); const(S, 'Sim_BDP_Hi', 35.0, 'none', 1, 'simulation: building pressure with AHUs on, no relief')
    MATH(S, sf, 'Sim_BDP_Relief', 'Multiply', 'RF_SpeedCmd', 'PctToFrac', 'Sim_BDP_K')
    SW(S, sf, 'Sim_BDP_Src', 'RF_Enable', 'Sim_BDP_Hi', 'Zero')
    MATH(S, sf, 'Sim_BDP0', 'Subtract', 'Sim_BDP_Src', 'Sim_BDP_Relief'); OF.ramp(S, sf, 'Sim_BLDG_DP', 'Sim_BDP0', tm(0.5, 5.0), 5.0)
    simlink(S, 'BLDG_DP', 'Sim_BLDG_DP')


def plant_room(S):
    """B1 plant room ventilation fans PAF / PEF (R9 B1 supply / exhaust risers). The refrigerant detection is the V7.7 base logic
    (PlantRoom_RefrigerantPPM -> RL alarms, PlantRoom_EmergencyVentCmd, chiller inhibit): its emergency ventilation command and the purge
    switch run both fans at 100 %; heat ventilation by room temperature and normal ventilation while the plant runs at PR_NormalSpeed."""
    f = 'Alarms/PlantRoom/Ventilation'
    p(S, f, 'PR_VentOnTemp', 32.0, 'C', 'plant room temperature above this -> ventilation fans on (heat rejection)')
    p(S, f, 'PR_VentOffTemp', 29.0, 'C', 'plant room temperature below this -> heat ventilation off')
    p(S, f, 'PR_NormalSpeed', 50.0, 'pct', 'normal ventilation fan speed', 0)
    ai(S, f, 'PR_Temp', 30.0, 'C', 1, note='FIELD AI: B1 plant room temperature')
    di(S, f, 'PR_PurgeSw', False, 'Purge', 'Auto', note='FIELD DI: emergency purge switch at the plant room door')
    CMP(S, f, 'PR_HotOn', 'GreaterThan', 'PR_Temp', 'PR_VentOnTemp'); CMP(S, f, 'PR_HotOff', 'LessThan', 'PR_Temp', 'PR_VentOffTemp')
    sealin(S, f, 'PR_HeatVent', 'PR_HotOn', 'PR_HotOff', note='heat ventilation with hysteresis')
    OR(S, f, 'PR_Emergency', 'PlantRoom_EmergencyVentCmd', 'PR_PurgeSw', note='base refrigerant-leak emergency ventilation (V7.7) or purge')
    OR(S, f, 'PR_VentReq', 'PR_Emergency', 'PR_HeatVent', 'PlantRunRequest')
    fan(S, f, 'PAF', 'PR_VentReq', 'B1 plant room supply fan PAF')
    fan(S, f, 'PEF', 'PR_VentReq', 'B1 plant room exhaust fan PEF')
    SW(S, f, 'PR_Speed1', 'PR_Emergency', 'HundredPct', 'PR_NormalSpeed'); SW(S, f, 'PR_Speed', 'PR_VentReq', 'PR_Speed1', 'Zero')
    S.npoint(f, 'PAF_SpeedCmd', 'PR_Speed', 'pct', 0, kind='ao', note='FIELD AO: PAF speed (100 % emergency)')
    S.npoint(f, 'PEF_SpeedCmd', 'PR_Speed', 'pct', 0, kind='ao', note='FIELD AO: PEF speed (100 % emergency)')


def plant_link(S):
    """floors 2-8 VAV AHUs -> chiller plant: cooling calls (plant demand mode), CHW reset requests (G36 5.16.14, plant T&R) and running
    units, added to the V7.8 air-side totals; expansion slots 03-06 power added to Plant_kW"""
    f = 'PlantControl/AirSideDemand'
    const(S, 'AirX_CallValvePct', 10.0, 'none', 0, 'PICV above this = cooling call'); const(S, 'AirX_ReqValvePct', 95.0, 'none', 0, 'PICV above this for 5 min = 1 request')
    const(S, 'AirX_ReqSat2K', 2.0, 'none', 1, 'SAT above setpoint by this for 5 min = 1 more request'); const(S, 'AirX_ReqSat3K', 3.0, 'none', 1, 'and by this = 1 more')
    calls, reqs, runs = [], [], []
    for fl in range(2, 9):
        u = f'AHU_F{fl:02d}'
        CMP(S, f, f'{u}_ChwCallV', 'GreaterThan', f'{u}_ValveCmd', 'AirX_CallValvePct'); AND(S, f, f'{u}_ChwCall', f'{u}_ChwCallV', f'{u}_Status')
        CMP(S, f, f'{u}_ReqV', 'GreaterThan', f'{u}_ValveCmd', 'AirX_ReqValvePct')
        MATH(S, f, f'{u}_SatErr', 'Subtract', f'{u}_SAT', f'{u}_SAT_SP')
        CMP(S, f, f'{u}_ReqS2', 'GreaterThan', f'{u}_SatErr', 'AirX_ReqSat2K'); CMP(S, f, f'{u}_ReqS3', 'GreaterThan', f'{u}_SatErr', 'AirX_ReqSat3K')
        for k in ('V', 'S2', 'S3'):
            AND(S, f, f'{u}_Req{k}A', f'{u}_Req{k}', f'{u}_RunStable'); DLY(S, f, f'{u}_Req{k}Dly', f'{u}_Req{k}A', tm(300000, 3000))
            SW(S, f, f'{u}_Req{k}N', f'{u}_Req{k}Dly', 'One', 'Zero')
        MATH(S, f, f'{u}_ChwReqCalc', 'Add', f'{u}_ReqVN', f'{u}_ReqS2N', f'{u}_ReqS3N')
        S.npoint(f, f'{u}_ChwRequests', f'{u}_ChwReqCalc', 'none', 0, note=f'{u}: chilled-water reset requests to the plant (G36 5.16.14)')
        SW(S, f, f'{u}_CallN', f'{u}_ChwCall', 'One', 'Zero'); SW(S, f, f'{u}_RunN', f'{u}_Status', 'One', 'Zero')
        calls.append(f'{u}_CallN'); reqs.append(f'{u}_ChwRequests'); runs.append(f'{u}_RunN')
    for n, lst, base, note in (('PLANT_TotalCalls', calls, 'AirSide_CoolingCalls', 'cooling calls, all air units'),
                               ('PLANT_TotalReqs', reqs, 'AirSide_ChwRequests', 'CHW reset requests, all air units'),
                               ('PLANT_TotalRunning', runs, 'AirSide_UnitsRunning', 'air units running')):
        SC.add_tree(S, f, f'{n}_F', lst); MATH(S, f, f'{n}_Calc', 'Add', f'{n}_F', base)
        S.npoint(f, n, f'{n}_Calc', 'none', 0, note=note + ' (V7.8 units + floors 2-8)')
    S.rewire('AirSideCallsEnough', 'inA', 'PLANT_TotalCalls', 'AirSide_CoolingCalls')
    S.rewire('AirSideOnline', 'inA', 'PLANT_TotalRunning', 'AirSide_UnitsRunning')
    S.rewire('TR_Loop', 'controlledVariable', 'PLANT_TotalReqs', 'AirSide_ChwRequests')
    S.rewire('DTG_StarveQ', 'inA', 'PLANT_TotalReqs', 'AirSide_ChwRequests')
    for n in range(3, 7):                                  # expansion chillers get the plant CHW supply setpoint (CH01 / CH02 have CHnn_ChwSetpointCmd)
        S.npoint(f'Expansion/CH{n:02d}', f'CH{n:02d}_ChwSetpointCmd', 'CHW_LeavingTemperatureSetpoint_ACTIVE', 'C', 1, kind='ao',
                 note=f'FIELD AO / BMS write: CH{n:02d} leaving CHW temperature setpoint (plant ACTIVE setpoint)')
    e = 'Energy'
    kws = [f'{t}{n:02d}_kW' for n in range(3, 7) for t in ('CH', 'CHP', 'CDP', 'CT')]
    SC.add_tree(S, e, 'EXP_kWSum0', kws); S.npoint(e, 'EXP_kW', 'EXP_kWSum0', 'kW', 1, note='expansion slots 03-06 power (chillers, pumps, towers)')
    S.link(S.comp['PlantKWSum'], 'EXP_kW', 'inD')
    S.log.append(('V7.9 r6', 'PlantKWSum', 'inD <- EXP_kW', 'expansion power in Plant_kW', '', ''))


def corridor(S):
    for s in OF.od()['corridorSensors']:
        k = f"CS_{nm(s['id'].replace('CS-', ''))}"; f = f"{AIR}/Floors/F{s['floor']:02d}/Corridor"
        ai(S, f, f'{k}_T', 25.0, 'C', 1, note=f"FIELD AI: corridor sensor {s['id']} temperature")
        ai(S, f, f'{k}_RH', 58.0, 'RH', 0, note=f"FIELD AI: corridor sensor {s['id']} humidity")
        ai(S, f, f'{k}_CO2', 550.0, 'ppm', 0, note=f"FIELD AI: corridor sensor {s['id']} CO2")
        CMP(S, f, f'{k}_TLo', 'LessThan', f'{k}_T', 'RM_TempValidLo'); CMP(S, f, f'{k}_THi', 'GreaterThan', f'{k}_T', 'RM_TempValidHi')
        OR(S, f, f'{k}_Bad', f'{k}_TLo', f'{k}_THi'); DLY(S, f, f'{k}_BadDly', f'{k}_Bad', tm(60000, 5000))
        alarm(S, f, f'{k}_SensorFaultAlarm', f'{k}_BadDly', 'Sensor fault', 'Normal', 'Warning', f"Corridor sensor {s['id']}: temperature outside the sensor range")


def epms(S):
    """tenant billing data for the EPMS (ALT_EPMS_DC01): one folder per tenant under Metering/EPMS"""
    C = 'Metering/EPMS/Common'
    S.bparam('EPMS_PeriodClose', False, folder=C, t='Close period', f='Normal', note='billing period close (EPMS / operator pulse): latches the period-start readings')
    PULSE(S, C, 'EPMS_CloseEdge', 'EPMS_PeriodClose', tm(3000, 2000), note='one latch per close command')
    p(S, C, 'EPMS_ResetTolKWh', 1.0, 'kWh', 'register lower than the period start by more than this = meter reset / rollover (billing hold)', 1)
    S.kc(C, 'EPMS_MinuteClock', 'MultiVibrator', props=[('period', 'b:RelTime', str(tm(60000, 2000)))], note='thermal energy integration clock (1 min)')
    const(S, 'EPMS_KWhPerKWMin', 1.0 / 60.0, 'none', 5, 'kWh per kW per minute')
    D = OF.od(); vav_rooms = {t['room'] for t in D['airTerminals']}
    by_floor = {}
    for t in D['tenancies']: by_floor.setdefault(t['floor'], []).append(t)
    for fl, ts in sorted(by_floor.items()):
        fv = [f"VAV_{nm(r)}_Airflow" for r in sorted(vav_rooms) if r.startswith(f'F{fl:02d}-')]
        F_ = f'Metering/EPMS/F{fl:02d}'
        SC.add_tree(S, F_, f'EPMS_F{fl:02d}_AirSum', fv) if len(fv) > 1 else None
        MATH(S, F_, f'EPMS_F{fl:02d}_AirDiv', 'Maximum', f'EPMS_F{fl:02d}_AirSum', 'One')
        for t in ts:
            q = nm(t['id']); f = f'Metering/EPMS/{q}'; reg = f'PM_{q}_kWh'
            S.kc(f, f'EPMS_{q}_StartLatch', 'NumericLatch', {'in': reg, 'clock': 'EPMS_CloseEdge'}, note='period-start register (latched at close)')
            S.npoint(f, f'EPMS_{q}_PeriodStart_kWh', f'EPMS_{q}_StartLatch', 'kWh', 1, note='register at the start of the billing period')
            MATH(S, f, f'EPMS_{q}_Delta', 'Subtract', reg, f'EPMS_{q}_PeriodStart_kWh')
            MATH(S, f, f'EPMS_{q}_DeltaPos', 'Maximum', f'EPMS_{q}_Delta', 'Zero')
            S.npoint(f, f'EPMS_{q}_Period_kWh', f'EPMS_{q}_DeltaPos', 'kWh', 1, note='energy this billing period (electric)')
            MATH(S, f, f'EPMS_{q}_NegLim', 'Subtract', 'Zero', 'EPMS_ResetTolKWh')
            CMP(S, f, f'EPMS_{q}_Reset', 'LessThan', f'EPMS_{q}_Delta', f'EPMS_{q}_NegLim')
            alarm(S, f, f'EPMS_{q}_MeterResetAlarm', f'EPMS_{q}_Reset', 'Reset', 'Normal', 'Critical', f"{t['id']}: energy register below the period start - meter reset / rollover, billing hold")
            NOT(S, f, f'EPMS_{q}_NoReset', f'EPMS_{q}_Reset')
            S.bpoint(f, f'EPMS_{q}_QualityOK', f'EPMS_{q}_NoReset', 'Good', 'Hold', note='EPMS quality flag (billing allowed)')
            rv = [f"VAV_{nm(r)}_Airflow" for r in t['rooms'] if r in vav_rooms]
            if len(rv) > 1: SC.add_tree(S, f, f'EPMS_{q}_AirSum', rv)
            src = f'EPMS_{q}_AirSum' if len(rv) > 1 else (rv[0] if rv else 'Zero')
            MATH(S, f, f'EPMS_{q}_AirShare0', 'Divide', src, f'EPMS_F{fl:02d}_AirDiv')
            S.npoint(f, f'EPMS_{q}_AirShare', f'EPMS_{q}_AirShare0', 'none', 3, note='tenant share of the floor VAV airflow (0-1)')
            MATH(S, f, f'EPMS_{q}_Thermal0', 'Multiply', f'BTU_F{fl:02d}_kW', f'EPMS_{q}_AirShare')
            S.npoint(f, f'EPMS_{q}_Thermal_kW', f'EPMS_{q}_Thermal0', 'kW', 1, note='airflow-weighted share of the floor BTU meter (informative)')
            # thermal energy register: kitControl integrator (latch + add feedback, one step per minute) -> period energy like the power meter
            S.kc(f, f'EPMS_{q}_ThInt', 'NumericLatch', {'clock': 'EPMS_MinuteClock'}, note='thermal energy register (integrated each minute)')
            MATH(S, f, f'EPMS_{q}_ThInc', 'Multiply', f'EPMS_{q}_Thermal_kW', 'EPMS_KWhPerKWMin')
            MATH(S, f, f'EPMS_{q}_ThSum', 'Add', f'EPMS_{q}_ThInt', f'EPMS_{q}_ThInc'); S.link(S.comp[f'EPMS_{q}_ThInt'], f'EPMS_{q}_ThSum', 'in')
            S.npoint(f, f'EPMS_{q}_Thermal_kWh', f'EPMS_{q}_ThInt', 'kWh', 1, note='allocated thermal energy register (kWh_th, cumulative)')
            S.kc(f, f'EPMS_{q}_ThStartLatch', 'NumericLatch', {'in': f'EPMS_{q}_Thermal_kWh', 'clock': 'EPMS_CloseEdge'}, note='period-start thermal register')
            MATH(S, f, f'EPMS_{q}_ThDelta', 'Subtract', f'EPMS_{q}_Thermal_kWh', f'EPMS_{q}_ThStartLatch'); MATH(S, f, f'EPMS_{q}_ThDeltaPos', 'Maximum', f'EPMS_{q}_ThDelta', 'Zero')
            S.npoint(f, f'EPMS_{q}_PeriodThermal_kWh', f'EPMS_{q}_ThDeltaPos', 'kWh', 1, note='allocated thermal energy this billing period (kWh_th)')
            AND(S, f, f'EPMS_{q}_ThermalBillable0', 'EPMS_TenantThermalBilling', f'EPMS_{q}_NoReset')
            S.bpoint(f, f'EPMS_{q}_ThermalBillable', f'EPMS_{q}_ThermalBillable0', 'Billable', 'Not billable',
                     note='thermal billing only when enabled by contract (EPMS_TenantThermalBilling)')
            S.meta[f'EPMS_{q}_Period_kWh']['epms'] = t['id']


UNIT = {'MAU-DESIGN': 'MAU'}


def unit_of(eq):
    """R9 equipment id -> station prefix (AHU-F02 -> AHU_F02, AHU-01 -> AHU01, OAU-01 -> OAU01, MAU-DESIGN -> MAU)"""
    if eq in UNIT: return UNIT[eq]
    m = re.match(r'AHU-F(\d\d)$', eq)
    return f'AHU_F{m.group(1)}' if m else eq.replace('-', '')


def instruments(S):
    """R9 instrument schedule completed in the station: coil TT pair + dT / low-dT alarm, coil dP, motorised isolation valves
    (command with the unit, end-switch proof), expansion-chiller evaporator / condenser dP"""
    D = OF.od(); f0 = 'Metering/Coils'
    p(S, f0, 'COIL_LowDTK', 3.0, 'C', 'coil CHW dT below this with the valve > 20 % for 30 min -> low dT alarm (coil / PICV)')
    const(S, 'COIL_ValveMin', 20.0, 'none', 0, 'valve open above this = coil in duty')
    S.bparam('ISO_FloorValvesOpen', True, folder=f0, t='Open', f='Closed (maintenance)', note='motorised floor isolation valves (S / R)')
    coils = {}
    for i in D['instruments']:
        eq = i.get('equipment') or ''
        m = re.match(r'(TT|PT|MBFV)-(AHU-F\d\d|AHU-\d\d|OAU-\d\d|MAU-DESIGN)(?:-(CHS|CHR))?$', i['id'])
        if m:
            k, e, svc = m.groups(); u = unit_of(e); f = f'Metering/Coils/{u}'; coils.setdefault(u, set())
            if k == 'TT':
                ai(S, f, f'COIL_{u}_{svc}_T', 7.0 if svc == 'CHS' else 12.0, 'C', 2, note=f"FIELD AI: {i['id']} coil {svc} temperature"); coils[u].add(svc)
            elif k == 'PT':
                ai(S, f, f'COIL_{u}_DP', 40.0, 'kPa', 1, note=f"FIELD AI: {i['id']} coil / PICV differential pressure")
            else:
                n = f'ISO_{u}_{svc}'
                S.bpoint(f, f'{n}_Cmd', f'{u}_StartCmd' if u != 'MAU' else 'MAU_StartCmd', 'Open', 'Closed', kind='do', note=f"FIELD DO: {i['id']} open (with the unit)")
                di(S, f, f'{n}_Fb', False, 'Open', 'Closed', note=f"FIELD DI: {i['id']} open end switch")
                NOT(S, f, f'{n}_FbN', f'{n}_Fb'); AND(S, f, f'{n}_Bad', f'{n}_Cmd', f'{n}_FbN'); DLY(S, f, f'{n}_BadDly', f'{n}_Bad', tm(90000, 4000))
                alarm(S, f, f'{n}_FailAlarm', f'{n}_BadDly', 'Not open', 'Normal', 'Warning', f"{i['id']}: commanded open, end switch not made")
                DLY(S, f'{AIR}/Simulation/R9', f'Sim_{n}', f'{n}_Cmd', tm(30000, 1500), tm(30000, 1500)); simlink(S, f'{n}_Fb', f'Sim_{n}')
            continue
        m = re.match(r'MBFV-([SR])-F(\d\d)$', i['id'])
        if m:
            n = f'ISO_F{m.group(2)}_{"CHS" if m.group(1) == "S" else "CHR"}'; f = f'Metering/Floors/F{m.group(2)}'
            S.bpoint(f, f'{n}_Cmd', 'ISO_FloorValvesOpen', 'Open', 'Closed', kind='do', note=f"FIELD DO: {i['id']} floor isolation")
            di(S, f, f'{n}_Fb', True, 'Open', 'Closed', note=f"FIELD DI: {i['id']} open end switch")
            NOT(S, f, f'{n}_FbN', f'{n}_Fb'); AND(S, f, f'{n}_Bad', f'{n}_Cmd', f'{n}_FbN'); DLY(S, f, f'{n}_BadDly', f'{n}_Bad', tm(90000, 4000))
            alarm(S, f, f'{n}_FailAlarm', f'{n}_BadDly', 'Not open', 'Normal', 'Warning', f"{i['id']}: floor isolation valve not open")
            simlink(S, f'{n}_Fb', f'{n}_Cmd')
            continue
        m = re.match(r'PT-CH-(0[3-6])-(CHS|CDS)$', i['id'])
        if m:
            c = f'CH{m.group(1)}'; x = 'EvapDP' if m.group(2) == 'CHS' else 'CondDP'
            ai(S, f'Expansion/{c}', f'{c}_{x}', 60.0, 'kPa', 1, note=f"FIELD AI: {c} {'evaporator' if x == 'EvapDP' else 'condenser'} water pressure drop")
    for u, svcs in coils.items():
        if svcs != {'CHS', 'CHR'}: continue
        f = f'Metering/Coils/{u}'; vc = f'{u}_ValveCmd'
        MATH(S, f, f'COIL_{u}_DTCalc', 'Subtract', f'COIL_{u}_CHR_T', f'COIL_{u}_CHS_T')
        S.npoint(f, f'COIL_{u}_DeltaT', f'COIL_{u}_DTCalc', 'C', 2, note='coil chilled-water dT')
        CMP(S, f, f'COIL_{u}_Duty', 'GreaterThan', vc, 'COIL_ValveMin'); CMP(S, f, f'COIL_{u}_DTLow', 'LessThan', f'COIL_{u}_DeltaT', 'COIL_LowDTK')
        AND(S, f, f'COIL_{u}_DTLowA', f'COIL_{u}_Duty', f'COIL_{u}_DTLow'); DLY(S, f, f'COIL_{u}_DTLowDly', f'COIL_{u}_DTLowA', tm(1800000, 20000))
        alarm(S, f, f'COIL_{u}_LowDeltaTAlarm', f'COIL_{u}_DTLowDly', 'Low dT', 'Normal', 'Warning', f'{u}: coil CHW dT low for 30 min (coil fouling / PICV setting / airflow)')
        sf = f'{AIR}/Simulation/R9'
        simlink(S, f'COIL_{u}_CHS_T', 'CHWS'); MATH(S, sf, f'Sim_COIL_{u}_DT', 'Multiply', vc, 'PctToFrac', 'AirX_SimChwDT', 'Two')
        MATH(S, sf, f'Sim_COIL_{u}_DT2', 'Minimum', f'Sim_COIL_{u}_DT', 'Sim_COIL_DTMax'); MATH(S, sf, f'Sim_COIL_{u}_R', 'Add', 'CHWS', f'Sim_COIL_{u}_DT2')
        simlink(S, f'COIL_{u}_CHR_T', f'Sim_COIL_{u}_R')


def build_r6(S):
    for u, sid in (('AHU01', 'AHU-01'), ('AHU02', 'AHU-02')): fahu(S, u, sid)
    oau_cascade(S)
    te = [f"TE_{nm(d['room'])}" for d in OF.od()['motorizedDampers'] if not d.get('integralVAV')]
    tef(S, te)
    kitchen(S); relief(S); plant_room(S); corridor(S); epms(S); plant_link(S)
    const(S, 'Sim_COIL_DTMax', 6.0, 'none', 1, 'simulation: coil dT at full load'); instruments(S)
    S.log.append(('V7.9 r6', 'AirSide / Metering', 'OAU demand cascade, FAHU R9 devices, TEF, KEF/MAU, relief fan, B1 ventilation / refrigerant, '
                  'corridor sensors, EPMS tenant export', 'v79_r6.py', '', ''))


_scale = SC.scale


def scale(S):
    _scale(S)
    build_r6(S)


SC.scale = scale
