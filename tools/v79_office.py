# -*- coding: utf-8 -*-
"""V7.9 r4: rental office air side from the R9 coordinated design (graphics3d/data/office79.json).

Design (R9 OFFICE-B1-R9): floors 2-8 = one central chilled-water mixed-air VAV AHU per floor, no FCU; every conditioned room has
a pressure-independent cooling-only VAV box (integral motorized damper, airflow pickup, position feedback) and a room sensor
(temperature / RH / CO2 / occupancy). Floor 1 lobby / food court VAVs are served by AHU-01 / AHU-02 (V7.8 logic kept).
Floor chilled-water BTU meter + floor power meter, two tenant power sub-meters per office floor.

Sequences (basis, adapted to a hot-humid climate: cooling only, no air-side economizer, dehumidification by SAT):
  ASHRAE Guideline 36-2021  5.6 cooling-only VAV terminal (occupied / occupied-standby / unoccupied modes, cooling loop ->
                            airflow setpoint Vmin..Vcool-max, airflow loop -> damper, zone requests, zone alarms)
                            5.16 multi-zone VAV AHU (duct static pressure and SAT setpoint by Trim & Respond, minimum OA by
                            measured airflow, high duct static safety shutdown, alarms)
  ASHRAE 62.1 VRP           Vbz = Rp*Pz + Ra*Az per room (design data: 5 L/s/person + 0.6 L/s/m2), Vot = sum(Vbz) / Ev,
                            demand-controlled ventilation: the people part only when the room is occupied
  EIT (wor sor tor) / Thai fire code practice: AHU stops and its OA / relief dampers close on fire alarm (existing NotFireAlarm
                            permissive), smoke control is not part of this system
  Energy metering: Q[kW] = flow[m3/h] x 4.186 x dT / 3.6 (water, rho 1000), sub-meter reconciliation against the floor meter.
Every value here is a design-intent default (parameters in Workbench); TAB, commissioning and the engineer of record decide.
"""
import json, os, re
import make_v6 as M6
import make_v7 as M7
import v78_improve as IMP
import v79_scale as SC
import v79_air as AIRX
from make_v7 import AND, OR, NOT, DLY, SW, MATH, CMP, RATE, PID, PULSE, LIMIT, sealin, const, ai, di, simlink

AIR = M7.AIR
T, F = SC.T, SC.F
tm, alarm = IMP.tm, IMP.alarm
LS_PER_CFM = 0.471947
DATA = os.environ.get('V79_OFFICE', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'graphics3d', 'data', 'office79.json'))
# Niagara unit database names
M6.U.setdefault('Pa', 'units=u:pascal;Pa;(m-1)(kg)(s-2);;')
M6.U.setdefault('Ls', 'units=u:liters per second;l/s;(m3)(s-1);*0.001;')
M6.U.setdefault('ppm', 'units=u:parts per million;ppm;;;')
FLOOR_AHU_1 = {'G-LOB': 'AHU01', 'G-REC': 'AHU01', 'G-LOU': 'AHU02', 'G-FOOD': 'AHU02'}   # floor 1 VAVs on the V7.8 AHUs


def ramp(S, f, n, src, step, init, note='simulation: first-order response by rate limit'):
    """NumericDelay with a saved start value (no 0 C room at station start)"""
    return S.kc(f, n, 'NumericDelay', {'in': src}, props=[('maxStepSize', None, repr(float(step))), ('updateTime', 'b:RelTime', '1000'),
                                                        ('out', 'SN', init)], note=note)


def load(path=DATA):
    return json.load(open(path, encoding='utf-8'))


OD = None


def od():
    global OD
    if OD is None: OD = load()
    return OD


def nm(x):
    """design id -> station name part (VAV-F02-A-M1 -> F02_A_M1)"""
    return re.sub(r'[^A-Za-z0-9]+', '_', x).strip('_')


def ahu_of(fl):
    return f'AHU_F{fl:02d}'


def rooms_by_id():
    return {r['id']: r for r in od()['rooms']}


# ------------------------------------------------------------------ parameters
def common(S):
    C = f'{AIR}/Floors/Common'
    p = lambda n, v, u, note, prec=1: S.param(n, v, u, folder=C, prec=prec, note=note)
    # VAV terminal (G36 5.6)
    p('VAV_StandbyOffsetK', 1.0, 'C', 'occupied-standby: room cooling setpoint raised by this (G36 5.3.2)')
    p('VAV_UnoccCoolSP', 28.0, 'C', 'unoccupied cooling setpoint (setup)')
    p('VAV_ReqLoopPct', 95.0, 'pct', 'cooling loop above this -> 1 SAT request / damper above this -> 1 pressure request', 0)
    p('VAV_Req2K', 2.0, 'C', 'room above setpoint by this for 2 min -> 2 SAT requests (G36)')
    p('VAV_Req3K', 3.0, 'C', 'room above setpoint by this for 2 min -> 3 SAT requests (G36)')
    p('VAV_LowFlowPct', 70.0, 'pct', 'airflow below this % of setpoint for 5 min -> low airflow alarm (G36 level 3)', 0)
    p('VAV_VeryLowFlowPct', 50.0, 'pct', 'airflow below this % of setpoint -> 2 extra pressure requests and critical alarm (G36 level 2)', 0)
    p('VAV_DmpMismatchPct', 10.0, 'pct', 'damper command vs position feedback difference -> actuator fault', 0)
    p('VAV_TempHighK', 2.0, 'C', 'room above setpoint by this for 10 min -> zone temperature high alarm')
    p('VAV_CO2High', 1000.0, 'ppm', 'room CO2 above this for 15 min (occupied) -> alarm (ventilation check)', 0)
    p('VAV_RHHigh', 65.0, 'RH', 'room RH above this for 15 min -> alarm (ASHRAE 55 / mould risk in hot-humid climate)', 0)
    p('RM_TempValidLo', 5.0, 'C', 'room temperature below this = sensor fault'); p('RM_TempValidHi', 45.0, 'C', 'room temperature above this = sensor fault')
    # AHU (G36 5.16)
    p('AHU_DspInit', 120.0, 'Pa', 'duct static setpoint at fan start (T&R SP0)', 0); p('AHU_DspMin', 25.0, 'Pa', 'duct static setpoint minimum (SPmin)', 0)
    p('AHU_DspMax', 250.0, 'Pa', 'duct static setpoint maximum (SPmax, from TAB)', 0); p('AHU_DspTrim', -10.0, 'Pa', 'T&R trim per period', 0)
    p('AHU_DspResp', 15.0, 'Pa', 'T&R respond per request above the ignore count', 0); p('AHU_DspRespMax', 32.0, 'Pa', 'T&R maximum respond per period', 0)
    p('AHU_DspIgnore', 2.0, 'none', 'pressure requests ignored (I)', 0)
    p('AHU_SatInit', 14.0, 'C', 'SAT setpoint at fan start'); p('AHU_SatMin', 12.8, 'C', 'SAT setpoint minimum (coldest, design)')
    p('AHU_SatMax', 18.0, 'C', 'SAT setpoint maximum (warmest)'); p('AHU_SatTrim', 0.2, 'C', 'T&R trim per period (warmer)')
    p('AHU_SatResp', -0.3, 'C', 'T&R respond per request above the ignore count (colder)'); p('AHU_SatRespMax', -1.0, 'C', 'T&R maximum respond per period')
    p('AHU_SatIgnore', 2.0, 'none', 'SAT (cooling) requests ignored (I)', 0)
    p('AirX_SatDehumMax', 13.0, 'C', 'SAT setpoint not above this while return RH is high (dehumidification, hot-humid climate)')
    p('AHU_HighStaticTrip', 375.0, 'Pa', 'duct static above this -> fan shutdown, manual reset (G36 5.16.8, set from TAB)', 0)
    p('AHU_FilterDPMax', 250.0, 'Pa', 'filter differential pressure above this -> dirty filter alarm', 0)
    p('AHU_SatLowAlarm', 10.0, 'C', 'SAT below this for 5 min -> alarm')
    p('AHU_SatDevK', 2.0, 'C', 'SAT away from setpoint by this for 20 min -> alarm (G36 5.16.15)')
    p('AHU_VentEv', 0.8, 'none', 'system ventilation efficiency Ev (ASHRAE 62.1 VRP, set by the engineer)', 2)
    p('AHU_OAFlowLowPct', 90.0, 'pct', 'measured OA below this % of Vot for 10 min -> ventilation alarm', 0)
    p('AHU_FeedbackMismatchPct', 15.0, 'pct', 'command vs feedback (VSD, OA damper, PICV) difference -> alarm', 0)
    S.bparam('AirX_DCVEnable', True, folder=C, t='DCV on (people part of Vbz only when occupied)', f='DCV off (design Vbz always)',
             note='ASHRAE 62.1 6.2.7 demand-controlled ventilation')
    # r5: toilet / janitor exhaust dampers (R9 MD-EA-*)
    S.bparam('TE_ForceOpen', False, folder=C, t='Forced open', f='Schedule', note='toilet exhaust dampers open outside the schedule (cleaning / odour)')
    S.bparam('TE_CloseOnFire', True, folder=C, t='Close', f='Stay open', note='toilet exhaust dampers close on fire alarm (PROJECT fire strategy decides)')
    M = 'Metering/Floors/Common'
    S.param('MTR_LowDeltaTK', 3.0, 'C', folder=M, prec=1, note='floor CHW dT below this with flow -> low dT alarm (design 5.5 K)')
    S.param('MTR_ReconTolPct', 2.0, 'pct', folder=M, prec=1, note='tenant sub-meters sum above the floor meter by more than this -> alarm')
    S.bparam('EPMS_TenantThermalBilling', False, folder=M, t='Enabled', f='Disabled (shared AHU coil)',
             note='R9 billing basis: the shared floor AHU coil has no per-tenant water-side measurement - thermal tenant billing stays off')
    # trim & respond period clock (shared)
    S.kc(f'{AIR}/Floors/Common', 'AHU_TRClock', 'MultiVibrator', props=[('period', 'b:RelTime', str(tm(120000, 4000)))],
         note='T&R period: 2 min (G36), test 4 s')
    NOT(S, f'{AIR}/Floors/Common', 'AHU_TRClockN', 'AHU_TRClock')
    # simulation constants
    for n, v, note in (('AirX_SimLoadOcc', 0.75, 'room load fraction of design when occupied'), ('AirX_SimLoadUnocc', 0.3, 'room load fraction unoccupied'),
                       ('AirX_SimSupplyDT', 10.0, 'design room - supply air dT'), ('AirX_SimDspRef', 150.0, 'duct static giving design airflow at 100 % damper'),
                       ('AirX_SimDspDesign', 300.0, 'duct static at 100 % fan, average damper 50 %'), ('AirX_SimOAFrac', 0.23, 'OA fraction of supply'),
                       ('AirX_SimCO2Gen', 450.0, 'CO2 rise with design people and design OA'), ('AirX_SimFilterDP', 140.0, 'clean filter dP at 100 %'),
                       ('AirX_SimRHDry', 18.0, 'RH drop at design airflow'), ('AirX_SimChwDT', 5.0, 'floor CHW dT with flow'),
                       ('AirX_SimFanKW', 11.0, 'floor AHU fan kW at 100 %'), ('AirX_SimTenantKW', 35.0, 'tenant lighting + small power kW'),
                       ('AirX_KwPerM3hK', 1.16278, 'water: kW per (m3/h x K) = 4.186 / 3.6')):
        const(S, n, v, 'none', 5 if v < 2 else 1, note)


# ------------------------------------------------------------------ rooms (sensors) and VAV terminals
def room_sensor(S, fl, r, f):
    """dedicated room sensor RS-<room>: temperature / RH / CO2 / occupancy + validity"""
    k = f"RM_{nm(r['id'])}"
    ai(S, f, f'{k}_T', 25.0, 'C', 1, note=f"FIELD AI: room {r['id']} {r.get('name', '')} temperature")
    ai(S, f, f'{k}_RH', 58.0, 'RH', 0, note=f"FIELD AI: room {r['id']} humidity")
    ai(S, f, f'{k}_CO2', 600.0, 'ppm', 0, note=f"FIELD AI: room {r['id']} CO2")
    di(S, f, f'{k}_Occ', False, 'Occupied', 'Vacant', note=f"FIELD DI: room {r['id']} occupancy sensor")
    CMP(S, f, f'{k}_TAboveLo', 'GreaterThanEqual', f'{k}_T', 'RM_TempValidLo'); CMP(S, f, f'{k}_TBelowHi', 'LessThanEqual', f'{k}_T', 'RM_TempValidHi')
    AND(S, f, f'{k}_TValid', f'{k}_TAboveLo', f'{k}_TBelowHi'); NOT(S, f, f'{k}_TInvalid', f'{k}_TValid')
    DLY(S, f, f'{k}_TInvalidDly', f'{k}_TInvalid', tm(60000, 5000))
    alarm(S, f, f'{k}_SensorFaultAlarm', f'{k}_TInvalidDly', 'Sensor fault', 'Normal', 'Warning', f"Room {r['id']}: temperature outside the sensor range")
    return k


def vav(S, t, r, fl, ahu, sch, fan_on):
    """one pressure-independent cooling-only VAV terminal (ASHRAE G36 5.6) + its room sensor"""
    v = f"VAV_{nm(t['room'])}"; k = f"RM_{nm(r['id'])}"
    f = f'{AIR}/Floors/F{fl:02d}/VAV/{v}'
    vmax = round(t['design_CFM'] * LS_PER_CFM, 1)
    vmin_occ = round(min(t.get('minimumSA_CFM_concept') or t['design_CFM'] * 0.3, t['design_CFM']) * LS_PER_CFM, 1)
    vbz_occ = round(t.get('minimumVentilation_Ls_concept') or 0.0, 1)
    vbz_area = round(0.6 * r['area_m2'], 1)                                     # Ra x Az (people part off when vacant)
    oaf = max(0.05, vbz_occ / vmin_occ) if vmin_occ else 0.25
    vmin_stby = round(min(vmin_occ, vbz_area / oaf), 1)
    S.bparam(f'{v}_OOS', False, folder=f, t='Out of service', f='In service', note='no requests / alarms from this box (maintenance, TAB)')
    S.param(f'{k}_CoolSP', 24.0, 'C', folder=f, prec=1, note=f"room {r['id']} occupied cooling setpoint")
    S.param(f'{v}_Vmax', vmax, 'Ls', folder=f, prec=1, note=f"cooling maximum airflow (design {t['design_CFM']:.0f} CFM)")
    S.param(f'{v}_VminOcc', vmin_occ, 'Ls', folder=f, prec=1, note='occupied minimum airflow (Vbz / supply OA fraction)')
    S.param(f'{v}_VminStby', vmin_stby, 'Ls', folder=f, prec=1, note='occupied-standby minimum airflow (area ventilation only)')
    S.param(f'{v}_VbzOcc', vbz_occ, 'Ls', folder=f, prec=1, note=f"ASHRAE 62.1 Vbz = 5 x {r.get('people_assumed', 0)} + 0.6 x {r['area_m2']} m2")
    S.param(f'{v}_VbzArea', vbz_area, 'Ls', folder=f, prec=1, note='ASHRAE 62.1 area part Ra x Az')
    ai(S, f, f'{v}_Airflow', 0.0, 'Ls', 1, note='FIELD AI: VAV airflow (pickup / transducer)')
    ai(S, f, f'{v}_DmpFb', 0.0, 'pct', 0, note='FIELD AI: VAV damper position feedback')
    # modes: occupied (schedule) / occupied-standby (schedule, room vacant 5 min) / unoccupied
    NOT(S, f, f'{v}_Vacant', f'{k}_Occ'); DLY(S, f, f'{v}_VacantDly', f'{v}_Vacant', tm(300000, 5000))
    AND(S, f, f'{v}_Standby', sch, f'{v}_VacantDly'); NOT(S, f, f'{v}_Unocc', sch)
    MATH(S, f, f'{v}_StbySP', 'Add', f'{k}_CoolSP', 'VAV_StandbyOffsetK')
    SW(S, f, f'{v}_SPOcc', f'{v}_Standby', f'{v}_StbySP', f'{k}_CoolSP')
    SW(S, f, f'{v}_SPCalc', f'{v}_Unocc', 'VAV_UnoccCoolSP', f'{v}_SPOcc')
    S.npoint(f, f'{v}_CoolSPActive', f'{v}_SPCalc', 'C', 1, note='active room cooling setpoint (mode)')
    # cooling loop -> airflow setpoint
    AND(S, f, f'{v}_Enable', fan_on, f'{k}_TValid')
    PID(S, f, f'{v}_CoolLoop', f'{k}_T', f'{v}_CoolSPActive', f'{v}_Enable', 'direct', 25.0, 0.5, 0.0, 100.0, note='room above setpoint -> more air')
    SW(S, f, f'{v}_VminSel1', f'{v}_Standby', f'{v}_VminStby', f'{v}_VminOcc'); SW(S, f, f'{v}_Vmin', f'{v}_Unocc', 'Zero', f'{v}_VminSel1')
    MATH(S, f, f'{v}_Span', 'Subtract', f'{v}_Vmax', f'{v}_Vmin')
    MATH(S, f, f'{v}_SpanUse', 'Multiply', f'{v}_Span', f'{v}_CoolLoop', 'PctToFrac')
    MATH(S, f, f'{v}_FlowSPCalc', 'Add', f'{v}_Vmin', f'{v}_SpanUse')
    SW(S, f, f'{v}_FlowSPGate', fan_on, f'{v}_FlowSPCalc', 'Zero')
    S.npoint(f, f'{v}_AirflowSP', f'{v}_FlowSPGate', 'Ls', 1, note='VAV airflow setpoint')
    # airflow loop -> damper
    PID(S, f, f'{v}_FlowLoop', f'{v}_Airflow', f'{v}_AirflowSP', fan_on, 'reverse', round(50.0 / max(vmax, 1), 4), 3.0, 0.0, 100.0,
        note='pressure-independent airflow control')
    S.npoint(f, f'{v}_DmpCmd', f'{v}_FlowLoop', 'pct', 0, kind='ao', note='FIELD AO: VAV damper command')
    # requests to the AHU (G36 5.6.8)
    NOT(S, f, f'{v}_InSvc', f'{v}_OOS'); AND(S, f, f'{v}_Active', fan_on, f'{v}_InSvc')
    CMP(S, f, f'{v}_DmpHigh', 'GreaterThan', f'{v}_DmpCmd', 'VAV_ReqLoopPct'); AND(S, f, f'{v}_DmpHighA', f'{v}_DmpHigh', f'{v}_Active')
    DLY(S, f, f'{v}_DmpHighDly', f'{v}_DmpHighA', tm(60000, 3000))
    MATH(S, f, f'{v}_FlowSPDiv', 'Maximum', f'{v}_AirflowSP', 'One')
    MATH(S, f, f'{v}_FlowPct0', 'Divide', f'{v}_Airflow', f'{v}_FlowSPDiv'); MATH(S, f, f'{v}_FlowPct', 'Multiply', f'{v}_FlowPct0', 'HundredPct')
    CMP(S, f, f'{v}_FlowVeryLow', 'LessThan', f'{v}_FlowPct', 'VAV_VeryLowFlowPct'); CMP(S, f, f'{v}_FlowLow', 'LessThan', f'{v}_FlowPct', 'VAV_LowFlowPct')
    CMP(S, f, f'{v}_HasSP', 'GreaterThan', f'{v}_AirflowSP', 'One')
    AND(S, f, f'{v}_FlowVeryLowA', f'{v}_FlowVeryLow', f'{v}_Active', f'{v}_HasSP'); AND(S, f, f'{v}_FlowLowA', f'{v}_FlowLow', f'{v}_Active', f'{v}_HasSP')
    DLY(S, f, f'{v}_FlowVeryLowReqDly', f'{v}_FlowVeryLowA', tm(60000, 3000))
    SW(S, f, f'{v}_PReq1', f'{v}_DmpHighDly', 'One', 'Zero'); SW(S, f, f'{v}_PReq2', f'{v}_FlowVeryLowReqDly', 'Two', 'Zero')
    MATH(S, f, f'{v}_PressureReq', 'Add', f'{v}_PReq1', f'{v}_PReq2', note='duct static pressure requests')
    CMP(S, f, f'{v}_LoopHigh', 'GreaterThan', f'{v}_CoolLoop', 'VAV_ReqLoopPct'); AND(S, f, f'{v}_LoopHighA', f'{v}_LoopHigh', f'{v}_Active')
    MATH(S, f, f'{v}_TErr', 'Subtract', f'{k}_T', f'{v}_CoolSPActive')
    CMP(S, f, f'{v}_TErr2', 'GreaterThan', f'{v}_TErr', 'VAV_Req2K'); CMP(S, f, f'{v}_TErr3', 'GreaterThan', f'{v}_TErr', 'VAV_Req3K')
    AND(S, f, f'{v}_TErr2A', f'{v}_TErr2', f'{v}_Active'); AND(S, f, f'{v}_TErr3A', f'{v}_TErr3', f'{v}_Active')
    DLY(S, f, f'{v}_TErr2Dly', f'{v}_TErr2A', tm(120000, 3000)); DLY(S, f, f'{v}_TErr3Dly', f'{v}_TErr3A', tm(120000, 3000))
    SW(S, f, f'{v}_SReq1', f'{v}_LoopHighA', 'One', 'Zero'); SW(S, f, f'{v}_SReq2', f'{v}_TErr2Dly', 'One', 'Zero'); SW(S, f, f'{v}_SReq3', f'{v}_TErr3Dly', 'One', 'Zero')
    MATH(S, f, f'{v}_SatReq', 'Add', f'{v}_SReq1', f'{v}_SReq2', f'{v}_SReq3', note='cooling SAT requests (0-3)')
    # alarms (G36 5.6.6)
    DLY(S, f, f'{v}_FlowLowDly', f'{v}_FlowLowA', tm(300000, 20000))
    alarm(S, f, f'{v}_LowAirflowAlarm', f'{v}_FlowLowDly', 'Low', 'Normal', 'Warning', f"{v}: airflow below 70 % of setpoint for 5 min")
    DLY(S, f, f'{v}_FlowVeryLowDly', f'{v}_FlowVeryLowA', tm(300000, 20000))
    alarm(S, f, f'{v}_VeryLowAirflowAlarm', f'{v}_FlowVeryLowDly', 'Very low', 'Normal', 'Critical', f"{v}: airflow below 50 % of setpoint for 5 min")
    MATH(S, f, f'{v}_DmpDiff', 'Subtract', f'{v}_DmpCmd', f'{v}_DmpFb'); MATH(S, f, f'{v}_DmpDiffAbs', 'AbsValue', f'{v}_DmpDiff')
    CMP(S, f, f'{v}_DmpMis', 'GreaterThan', f'{v}_DmpDiffAbs', 'VAV_DmpMismatchPct'); AND(S, f, f'{v}_DmpMisA', f'{v}_DmpMis', f'{v}_Active')
    DLY(S, f, f'{v}_DmpMisDly', f'{v}_DmpMisA', tm(300000, 20000))
    alarm(S, f, f'{v}_DamperFaultAlarm', f'{v}_DmpMisDly', 'Fault', 'Normal', 'Warning', f"{v}: damper position does not follow the command (actuator / linkage)")
    CMP(S, f, f'{v}_THighK', 'GreaterThan', f'{v}_TErr', 'VAV_TempHighK'); AND(S, f, f'{v}_THighA', f'{v}_THighK', f'{v}_Active', sch)
    DLY(S, f, f'{v}_THighDly', f'{v}_THighA', tm(600000, 20000))
    alarm(S, f, f'{v}_TempHighAlarm', f'{v}_THighDly', 'High', 'Normal', 'Warning', f"Room {r['id']}: temperature above setpoint + 2 K for 10 min")
    CMP(S, f, f'{v}_CO2Hi', 'GreaterThan', f'{k}_CO2', 'VAV_CO2High'); AND(S, f, f'{v}_CO2HiA', f'{v}_CO2Hi', sch, f'{v}_InSvc')
    DLY(S, f, f'{v}_CO2HiDly', f'{v}_CO2HiA', tm(900000, 20000))
    alarm(S, f, f'{v}_CO2HighAlarm', f'{v}_CO2HiDly', 'High', 'Normal', 'Warning', f"Room {r['id']}: CO2 high - check ventilation (ASHRAE 62.1)")
    CMP(S, f, f'{v}_RHHi', 'GreaterThan', f'{k}_RH', 'VAV_RHHigh'); AND(S, f, f'{v}_RHHiA', f'{v}_RHHi', fan_on, f'{v}_InSvc')
    DLY(S, f, f'{v}_RHHiDly', f'{v}_RHHiA', tm(900000, 20000))
    alarm(S, f, f'{v}_RHHighAlarm', f'{v}_RHHiDly', 'High', 'Normal', 'Warning', f"Room {r['id']}: humidity high")
    # ventilation (VRP): Vbz for this zone now (DCV: people part only when occupied)
    AND(S, f, f'{v}_DCVVacant', 'AirX_DCVEnable', f'{v}_VacantDly')
    SW(S, f, f'{v}_VbzNow0', f'{v}_DCVVacant', f'{v}_VbzArea', f'{v}_VbzOcc'); SW(S, f, f'{v}_VbzNow', f'{v}_Unocc', 'Zero', f'{v}_VbzNow0')
    # 3D / Px: air flows to this room
    CMP(S, f, f'{v}_HasFlow', 'GreaterThan', f'{v}_Airflow', 'AirX_VavFlowShow'); S.bpoint(f, f'Gfx_{v}_Fwd', f'{v}_HasFlow', 'Flow', 'No flow', note='3D: supply air to the room')
    return v, k, vmax


def vav_sim(S, v, k, vmax, fl, sat, sch):
    f = f'{AIR}/Simulation/Floors/F{fl:02d}'
    if fl > 1: MATH(S, f, f'Sim_{v}_DspF', 'Divide', f'Sim_{ahu_of(fl)}_Dsp', 'AirX_SimDspRef')
    dsp = f'Sim_{v}_DspF' if fl > 1 else 'One'
    MATH(S, f, f'Sim_{v}_Flow0', 'Multiply', f'{v}_DmpCmd', f'{v}_Vmax', 'PctToFrac', dsp)
    MATH(S, f, f'Sim_{v}_Flow', 'Multiply', f'Sim_{v}_Flow0', 'AirX_SimFlowGain'); simlink(S, f'{v}_Airflow', f'Sim_{v}_Flow')
    simlink(S, f'{v}_DmpFb', f'{v}_DmpCmd')
    # room: steady state T = SAT + dT_design x load x Vmax / airflow (capped at the warm limit), first order by rate limit
    SW(S, f, f'Sim_{v}_Load', sch, 'AirX_SimLoadOcc', 'AirX_SimLoadUnocc')
    MATH(S, f, f'Sim_{v}_FlowMin', 'Multiply', f'{v}_Vmax', 'AirX_SimFlowFloor'); MATH(S, f, f'Sim_{v}_FlowDiv', 'Maximum', f'Sim_{v}_Flow', f'Sim_{v}_FlowMin')
    MATH(S, f, f'Sim_{v}_Ratio', 'Divide', f'{v}_Vmax', f'Sim_{v}_FlowDiv')
    MATH(S, f, f'Sim_{v}_Rise', 'Multiply', f'Sim_{v}_Ratio', f'Sim_{v}_Load', 'AirX_SimSupplyDT')
    MATH(S, f, f'Sim_{v}_TSS0', 'Add', sat, f'Sim_{v}_Rise'); MATH(S, f, f'Sim_{v}_TSS', 'Minimum', f'Sim_{v}_TSS0', 'AirX_SimWarm')
    ramp(S, f, f'Sim_{k}_T', f'Sim_{v}_TSS', tm(0.01, 0.15), 26.0); simlink(S, f'{k}_T', f'Sim_{k}_T')
    MATH(S, f, f'Sim_{v}_Frac', 'Divide', f'Sim_{v}_Flow', f'{v}_Vmax'); MATH(S, f, f'Sim_{v}_Dry', 'Multiply', f'Sim_{v}_Frac', 'AirX_SimRHDry')
    MATH(S, f, f'Sim_{k}_RH', 'Subtract', 'AirX_SimWetRH', f'Sim_{v}_Dry'); simlink(S, f'{k}_RH', f'Sim_{k}_RH')
    # CO2: rise = gen x Vbz / OA delivered (OA = airflow x OA fraction), occupied only
    MATH(S, f, f'Sim_{v}_OA0', 'Multiply', f'Sim_{v}_FlowDiv', 'AirX_SimOAFrac'); MATH(S, f, f'Sim_{v}_OARatio', 'Divide', f'{v}_VbzOcc', f'Sim_{v}_OA0')
    SW(S, f, f'Sim_{v}_Gen', f'{k}_Occ', 'AirX_SimCO2Gen', 'Zero')
    MATH(S, f, f'Sim_{v}_CO2Rise', 'Multiply', f'Sim_{v}_Gen', f'Sim_{v}_OARatio'); MATH(S, f, f'Sim_{v}_CO2Tgt', 'Add', 'AirX_SimCO2Out', f'Sim_{v}_CO2Rise')
    ramp(S, f, f'Sim_{k}_CO2', f'Sim_{v}_CO2Tgt', tm(2.0, 40.0), 600.0); simlink(S, f'{k}_CO2', f'Sim_{k}_CO2')
    simlink(S, f'{k}_Occ', sch)


def plain_room_sim(S, k, fl):
    f = f'{AIR}/Simulation/Floors/F{fl:02d}'
    simlink(S, f'{k}_T', 'AirX_SimPlainRoomT'); simlink(S, f'{k}_RH', 'AirX_SimWetRH'); simlink(S, f'{k}_CO2', 'AirX_SimCO2Out')


# ------------------------------------------------------------------ floor VAV AHU (G36 5.16)
def trim_respond(S, f, name, reqs, init, lo, hi, trim, resp, resp_max, ignore, run, note, negative=False):
    """setpoint register updated once per T&R period: SP += trim when requests <= ignore, else respond x (R - I) (limited);
    reset to the initial value while the fan has not run for the start delay. Two latches = one update per period."""
    MATH(S, f, f'{name}_RExcess', 'Subtract', reqs, ignore)
    CMP(S, f, f'{name}_Respond', 'GreaterThan', f'{name}_RExcess', 'Zero')
    MATH(S, f, f'{name}_RespRaw', 'Multiply', f'{name}_RExcess', resp)
    MATH(S, f, f'{name}_RespUp', 'Maximum' if negative else 'Minimum', f'{name}_RespRaw', resp_max, note='respond limited to the maximum')
    SW(S, f, f'{name}_Delta', f'{name}_Respond', f'{name}_RespUp', trim)
    S.kc(f, f'{name}_Prev', 'NumericLatch', {'in': init, 'clock': 'AHU_TRClockN'}, note='copy of the register (other clock edge)')
    MATH(S, f, f'{name}_Next0', 'Add', f'{name}_Prev', f'{name}_Delta')
    MATH(S, f, f'{name}_NextHi', 'Minimum', f'{name}_Next0', hi); MATH(S, f, f'{name}_Next', 'Maximum', f'{name}_NextHi', lo)
    SW(S, f, f'{name}_In', run, f'{name}_Next', init)
    S.kc(f, f'{name}_Reg', 'NumericLatch', {'in': f'{name}_In', 'clock': 'AHU_TRClock'}, note=note)
    S.rewire(f'{name}_Prev', 'in', f'{name}_Reg', init)
    return f'{name}_Reg'


def ahu_control(S, fl, vavs):
    u = ahu_of(fl); f = f'{AIR}/Floors/F{fl:02d}'
    sch = next(x for x in od()['ahuSchedules'] if x['id'] == f'AHU-F{fl:02d}')
    oa_des = round(sch['OA_Ls_concept'], 1)
    S.param(f'{u}_OADesignLs', oa_des, 'Ls', folder=f, prec=0, note='design minimum OA (R9 concept)')
    # field points (R9 ahuAirDevices)
    ai(S, f, f'{u}_SpeedFb', 0.0, 'pct', 1, note='FIELD AI: supply fan VSD speed feedback')
    ai(S, f, f'{u}_RAT', 25.0, 'C', 1, note='FIELD AI: return air temperature'); ai(S, f, f'{u}_MAT', 26.0, 'C', 1, note='FIELD AI: mixed air temperature')
    ai(S, f, f'{u}_OAFlow', 0.0, 'Ls', 0, note='FIELD AI: outdoor airflow measuring station')
    ai(S, f, f'{u}_FilterDP', 80.0, 'Pa', 0, note='FIELD AI: filter differential pressure')
    ai(S, f, f'{u}_DuctSP', 0.0, 'Pa', 0, note='FIELD AI: supply duct static pressure (2/3 down the main)')
    ai(S, f, f'{u}_OADmpFb', 0.0, 'pct', 0, note='FIELD AI: OA damper position'); ai(S, f, f'{u}_RADmpFb', 0.0, 'pct', 0, note='FIELD AI: RA damper position')
    ai(S, f, f'{u}_RelDmpFb', 0.0, 'pct', 0, note='FIELD AI: relief damper position'); ai(S, f, f'{u}_PICVFb', 0.0, 'pct', 0, note='FIELD AI: PICV position feedback')
    run = f'{u}_Status'
    DLY(S, f, f'{u}_RunStable', run, tm(600000, 6000), 0, note='T&R starts after the fan has run for this time (G36 td)')
    # high duct static safety (G36 5.16.8): latch, manual reset; added to the start permissive
    CMP(S, f, f'{u}_StaticHi', 'GreaterThan', f'{u}_DuctSP', 'AHU_HighStaticTrip'); DLY(S, f, f'{u}_StaticHiDly', f'{u}_StaticHi', tm(5000, 2000))
    sealin(S, f, f'{u}_HighStaticLatch', f'{u}_StaticHiDly', f'{u}_ResetAny', note='high static trip')
    NOT(S, f, f'{u}_NoHighStatic', f'{u}_HighStaticLatch'); S.rewire(f'{u}_StartLogic', 'inC', f'{u}_NoHighStatic', T)
    alarm(S, f, f'{u}_HighStaticAlarm', f'{u}_HighStaticLatch', 'Tripped', 'Normal', 'Critical', f'{u}: duct static above the safety limit - fan stopped, reset required')
    # requests from the VAVs
    SC.add_tree(S, f, f'{u}_PressureReqs', [f'{v}_PressureReq' for v in vavs])
    SC.add_tree(S, f, f'{u}_SatReqs', [f'{v}_SatReq' for v in vavs])
    S.npoint(f, f'{u}_PressureRequests', f'{u}_PressureReqs', 'none', 0, note='VAV duct pressure requests (sum)')
    S.npoint(f, f'{u}_CoolingRequests', f'{u}_SatReqs', 'none', 0, note='VAV cooling (SAT) requests (sum)')
    # duct static: T&R setpoint, fan PID
    reg = trim_respond(S, f, f'{u}_Dsp', f'{u}_PressureRequests', 'AHU_DspInit', 'AHU_DspMin', 'AHU_DspMax', 'AHU_DspTrim', 'AHU_DspResp',
                       'AHU_DspRespMax', 'AHU_DspIgnore', f'{u}_RunStable', 'duct static setpoint (T&R)')
    S.npoint(f, f'{u}_DuctSP_SP', reg, 'Pa', 0, note='duct static pressure setpoint (G36 T&R)')
    PID(S, f, f'{u}_FanLoop', f'{u}_DuctSP', f'{u}_DuctSP_SP', run, 'reverse', 0.3, 1.0, 0.0, 100.0, note='duct static below setpoint -> faster')
    MATH(S, f, f'{u}_FanMin', 'Maximum', f'{u}_FanLoop', 'AirX_FanMinPct')
    SW(S, f, f'{u}_FanGate2', f'{u}_StartCmd', f'{u}_FanMin', 'Zero'); S.rewire(f'{u}_FanSpeedCmd', 'in16', f'{u}_FanGate2', 'Zero')
    # SAT: T&R setpoint, dehumidification cap, PICV PID
    reg = trim_respond(S, f, f'{u}_Sat', f'{u}_CoolingRequests', 'AHU_SatInit', 'AHU_SatMin', 'AHU_SatMax', 'AHU_SatTrim', 'AHU_SatResp',
                       'AHU_SatRespMax', 'AHU_SatIgnore', f'{u}_RunStable', 'SAT setpoint (T&R)', negative=True)
    CMP(S, f, f'{u}_RHHigh', 'GreaterThan', f'{u}_RA_RH', f'{u}_DehumRH')
    MATH(S, f, f'{u}_SatDehum', 'Minimum', reg, 'AirX_SatDehumMax')
    SW(S, f, f'{u}_SatSPSel', f'{u}_RHHigh', f'{u}_SatDehum', reg)
    S.npoint(f, f'{u}_SAT_SP', f'{u}_SatSPSel', 'C', 1, note='supply-air temperature setpoint (T&R, dehumidification limit)')
    PID(S, f, f'{u}_SatLoop', f'{u}_SAT', f'{u}_SAT_SP', run, 'direct', 6.0, 1.0, 0.0, 100.0, note='SAT above setpoint -> open the PICV')
    SW(S, f, f'{u}_ValveGate2', run, f'{u}_SatLoop', 'Zero'); S.rewire(f'{u}_ValveCmd', 'in16', f'{u}_ValveGate2', 'Zero')
    # minimum OA (62.1 VRP + DCV): Vot = sum(Vbz) / Ev, OA damper PID on measured OA
    SC.add_tree(S, f, f'{u}_VouSum', [f'{v}_VbzNow' for v in vavs])
    MATH(S, f, f'{u}_VotCalc', 'Divide', f'{u}_VouSum', 'AHU_VentEv')
    S.npoint(f, f'{u}_OAFlowSP', f'{u}_VotCalc', 'Ls', 0, note='outdoor air intake setpoint Vot (ASHRAE 62.1 VRP, DCV)')
    PID(S, f, f'{u}_OALoop', f'{u}_OAFlow', f'{u}_OAFlowSP', run, 'reverse', round(50.0 / max(oa_des, 1), 4), 2.0, 0.0, 100.0, note='OA below Vot -> open')
    SW(S, f, f'{u}_OAGate2', f'{u}_StartCmd', f'{u}_OALoop', 'Zero'); S.rewire(f'{u}_OADamperCmd', 'in16', f'{u}_OAGate2', 'Zero')
    SW(S, f, f'{u}_RAGate', f'{u}_StartCmd', 'HundredPct', 'Zero')
    S.npoint(f, f'{u}_RADamperCmd', f'{u}_RAGate', 'pct', 0, kind='ao', note='FIELD AO: return air damper (open with the fan, no economizer)')
    S.npoint(f, f'{u}_RelDamperCmd', f'{u}_OAGate2', 'pct', 0, kind='ao', note='FIELD AO: relief damper (tracks the OA damper)')
    # alarms
    CMP(S, f, f'{u}_FilterHi', 'GreaterThan', f'{u}_FilterDP', 'AHU_FilterDPMax'); AND(S, f, f'{u}_FilterHiA', f'{u}_FilterHi', run)
    DLY(S, f, f'{u}_FilterHiDly', f'{u}_FilterHiA', tm(600000, 10000))
    alarm(S, f, f'{u}_FilterDPAlarm', f'{u}_FilterHiDly', 'Dirty', 'Normal', 'Warning', f'{u}: filter differential pressure high - replace filter')
    CMP(S, f, f'{u}_SatLow', 'LessThan', f'{u}_SAT', 'AHU_SatLowAlarm'); AND(S, f, f'{u}_SatLowA', f'{u}_SatLow', run)
    DLY(S, f, f'{u}_SatLowDly', f'{u}_SatLowA', tm(300000, 10000))
    alarm(S, f, f'{u}_SatLowAlarm', f'{u}_SatLowDly', 'Low', 'Normal', 'Warning', f'{u}: supply air too cold (condensation on diffusers)')
    MATH(S, f, f'{u}_SatDev', 'Subtract', f'{u}_SAT', f'{u}_SAT_SP'); MATH(S, f, f'{u}_SatDevAbs', 'AbsValue', f'{u}_SatDev')
    CMP(S, f, f'{u}_SatDevHi', 'GreaterThan', f'{u}_SatDevAbs', 'AHU_SatDevK'); AND(S, f, f'{u}_SatDevA', f'{u}_SatDevHi', f'{u}_RunStable')
    DLY(S, f, f'{u}_SatDevDly', f'{u}_SatDevA', tm(1200000, 30000))
    alarm(S, f, f'{u}_SatNotTrackingAlarm', f'{u}_SatDevDly', 'Deviation', 'Normal', 'Warning', f'{u}: supply-air temperature not at setpoint for 20 min (CHW / PICV)')
    MATH(S, f, f'{u}_OALim', 'Multiply', f'{u}_OAFlowSP', 'AHU_OAFlowLowPct', 'PctToFrac')
    CMP(S, f, f'{u}_OALow', 'LessThan', f'{u}_OAFlow', f'{u}_OALim'); AND(S, f, f'{u}_OALowA', f'{u}_OALow', f'{u}_RunStable')
    DLY(S, f, f'{u}_OALowDly', f'{u}_OALowA', tm(600000, 20000))
    alarm(S, f, f'{u}_VentilationLowAlarm', f'{u}_OALowDly', 'Low', 'Normal', 'Warning', f'{u}: outdoor air below the ASHRAE 62.1 minimum for 10 min')
    for nmx, cmd, fb in (('Fan', f'{u}_FanSpeedCmd', f'{u}_SpeedFb'), ('OADmp', f'{u}_OADamperCmd', f'{u}_OADmpFb'), ('PICV', f'{u}_ValveCmd', f'{u}_PICVFb')):
        MATH(S, f, f'{u}_{nmx}Diff', 'Subtract', cmd, fb); MATH(S, f, f'{u}_{nmx}DiffAbs', 'AbsValue', f'{u}_{nmx}Diff')
        CMP(S, f, f'{u}_{nmx}Mis', 'GreaterThan', f'{u}_{nmx}DiffAbs', 'AHU_FeedbackMismatchPct'); AND(S, f, f'{u}_{nmx}MisA', f'{u}_{nmx}Mis', run)
        DLY(S, f, f'{u}_{nmx}MisDly', f'{u}_{nmx}MisA', tm(300000, 20000))
        alarm(S, f, f'{u}_{nmx}MismatchAlarm', f'{u}_{nmx}MisDly', 'Mismatch', 'Normal', 'Warning', f'{u}: {nmx} feedback does not follow the command')
    return u


def ahu_sim(S, fl, vavs, rooms):
    u = ahu_of(fl); f = f'{AIR}/Simulation/Floors/F{fl:02d}'
    SC.add_tree(S, f, f'Sim_{u}_DmpSum', [f'{v}_DmpCmd' for v in vavs]); const(S, f'AirX_VavCount{fl:02d}', float(len(vavs)), 'none', 0)
    MATH(S, f, f'Sim_{u}_DmpAvg', 'Divide', f'Sim_{u}_DmpSum', f'AirX_VavCount{fl:02d}')
    MATH(S, f, f'Sim_{u}_Spd2', 'Multiply', f'{u}_FanSpeedCmd', f'{u}_FanSpeedCmd', 'PctToFrac', 'PctToFrac')
    MATH(S, f, f'Sim_{u}_DmpTerm0', 'Multiply', f'Sim_{u}_DmpAvg', 'AirX_SimDmpK'); MATH(S, f, f'Sim_{u}_DmpTerm', 'Subtract', 'AirX_SimDmpBase', f'Sim_{u}_DmpTerm0')
    MATH(S, f, f'Sim_{u}_Dsp', 'Multiply', 'AirX_SimDspDesign', f'Sim_{u}_Spd2', f'Sim_{u}_DmpTerm'); simlink(S, f'{u}_DuctSP', f'Sim_{u}_Dsp')
    simlink(S, f'{u}_SpeedFb', f'{u}_FanSpeedCmd'); simlink(S, f'{u}_OADmpFb', f'{u}_OADamperCmd'); simlink(S, f'{u}_RADmpFb', f'{u}_RADamperCmd')
    simlink(S, f'{u}_RelDmpFb', f'{u}_RelDamperCmd'); simlink(S, f'{u}_PICVFb', f'{u}_ValveCmd')
    MATH(S, f, f'Sim_{u}_OAF', 'Multiply', f'{u}_OADesignLs', f'{u}_OADamperCmd', f'{u}_FanSpeedCmd', 'PctToFrac')
    MATH(S, f, f'Sim_{u}_OAFlow', 'Multiply', f'Sim_{u}_OAF', 'PctToFrac', 'AirX_SimOAGain'); simlink(S, f'{u}_OAFlow', f'Sim_{u}_OAFlow')
    MATH(S, f, f'Sim_{u}_Filter', 'Multiply', 'AirX_SimFilterDP', f'Sim_{u}_Spd2'); simlink(S, f'{u}_FilterDP', f'Sim_{u}_Filter')
    SC.add_tree(S, f, f'Sim_{u}_RATSum', [f'{k}_T' for k in rooms]); const(S, f'AirX_RoomCount{fl:02d}', float(len(rooms)), 'none', 0)
    MATH(S, f, f'Sim_{u}_RAT', 'Divide', f'Sim_{u}_RATSum', f'AirX_RoomCount{fl:02d}'); simlink(S, f'{u}_RAT', f'Sim_{u}_RAT')
    MATH(S, f, f'Sim_{u}_OAdiff', 'Subtract', 'OA_Temperature', f'Sim_{u}_RAT'); MATH(S, f, f'Sim_{u}_OAmix', 'Multiply', f'Sim_{u}_OAdiff', 'AirX_SimOAFrac')
    MATH(S, f, f'Sim_{u}_MAT', 'Add', f'Sim_{u}_RAT', f'Sim_{u}_OAmix'); simlink(S, f'{u}_MAT', f'Sim_{u}_MAT')
    S.rewire(f'Sim_{u}_SAT', 'inA', f'Sim_{u}_MAT', 'AirX_SimWarm')                    # coil leaving air = mixed air - coil dT
    ramp(S, f, f'Sim_{u}_SATr', f'Sim_{u}_SAT', tm(0.05, 0.4), 14.0, note='coil thermal lag')
    S.rewire(f'{u}_SAT', 'in10', f'Sim_{u}_SATr', f'Sim_{u}_SAT')
    # the 4 legacy AirPlug zone points (V7.9 r2) are aggregates now: their simulated temperature follows the floor rooms
    for z in range(1, AIRX.ZPF + 1):
        c = AIRX.zcode(fl, z)
        S.rewire(f'Sim_{c}_TTgt0', 'inA', f'Sim_{u}_RAT', 'AirX_SimWarm'); S.rewire(f'Sim_{c}_TTgt0', 'inB', 'Zero', f'Sim_{u}_Cool')


# ------------------------------------------------------------------ floor energy metering
def metering(S, m, fl_valves):
    fl = m['floor']; f = f'Metering/Floors/F{fl:02d}'; p = f'F{fl:02d}'
    ai(S, f, f'FM_{p}_Flow', 0.0, 'm3h', 1, note=f"FIELD AI: floor {fl} CHW flow ({m['flowMeter']})")
    ai(S, f, f'TT_S_{p}', 7.0, 'C', 2, note=f"FIELD AI: floor {fl} CHW supply temperature ({m['ttSupply']})")
    ai(S, f, f'TT_R_{p}', 12.0, 'C', 2, note=f"FIELD AI: floor {fl} CHW return temperature ({m['ttReturn']})")
    MATH(S, f, f'BTU_{p}_DTCalc', 'Subtract', f'TT_R_{p}', f'TT_S_{p}'); S.npoint(f, f'BTU_{p}_DeltaT', f'BTU_{p}_DTCalc', 'C', 2, note='floor CHW dT')
    MATH(S, f, f'BTU_{p}_kW0', 'Multiply', f'FM_{p}_Flow', f'BTU_{p}_DeltaT', 'AirX_KwPerM3hK')
    MATH(S, f, f'BTU_{p}_kWPos', 'Maximum', f'BTU_{p}_kW0', 'Zero')
    S.npoint(f, f'BTU_{p}_kW', f'BTU_{p}_kWPos', 'kW', 1, note=f"{m['btuMeter']}: floor cooling energy rate")
    M6.add_ext(S, f'BTU_{p}_kW', 'Energy', 'c:NumericTotalizerExt')
    # meter quality: negative dT or flow -> fault; low dT with real flow -> low dT syndrome alarm
    const(S, 'MTR_DTNegLimit', -0.5, 'C', 1, 'dT below this = sensor swap / fault'); const(S, 'MTR_FlowMinShow', 2.0, 'm3h', 1, 'flow above this = flowing')
    CMP(S, f, f'BTU_{p}_DTNeg', 'LessThan', f'BTU_{p}_DeltaT', 'MTR_DTNegLimit'); CMP(S, f, f'BTU_{p}_Flowing', 'GreaterThan', f'FM_{p}_Flow', 'MTR_FlowMinShow')
    AND(S, f, f'BTU_{p}_BadA', f'BTU_{p}_DTNeg', f'BTU_{p}_Flowing'); DLY(S, f, f'BTU_{p}_BadDly', f'BTU_{p}_BadA', tm(300000, 10000))
    alarm(S, f, f'BTU_{p}_MeterFaultAlarm', f'BTU_{p}_BadDly', 'Fault', 'Normal', 'Warning', f"{m['btuMeter']}: negative dT with flow - check sensor pair / installation")
    CMP(S, f, f'BTU_{p}_DTLow', 'LessThan', f'BTU_{p}_DeltaT', 'MTR_LowDeltaTK'); AND(S, f, f'BTU_{p}_DTLowA', f'BTU_{p}_DTLow', f'BTU_{p}_Flowing')
    DLY(S, f, f'BTU_{p}_DTLowDly', f'BTU_{p}_DTLowA', tm(1800000, 20000))
    alarm(S, f, f'BTU_{p}_LowDeltaTAlarm', f'BTU_{p}_DTLowDly', 'Low dT', 'Normal', 'Warning', f'Floor {fl}: CHW dT low for 30 min (low dT syndrome - coil / PICV / control)')
    # power: floor feeder meter and (floors 2-8) two tenant sub-meters
    ai(S, f, f'PM_{p}_kW', 0.0, 'kW', 1, note=f"FIELD AI: floor {fl} feeder power ({m['powerMeter']})")
    ai(S, f, f'PM_{p}_kWh', 0.0, 'kWh', 0, note=f"FIELD AI: floor {fl} feeder energy register ({m['powerMeter']})", hist='5min')
    tenants = [t for t in od()['tenantMetering'] if t['floor'] == fl]
    tk = []
    for t in tenants:
        q = f"PM_{nm(t['tenantId'])}"
        ai(S, f, f'{q}_kW', 0.0, 'kW', 1, note=f"FIELD AI: tenant {t['tenantId']} power ({t['powerMeterId']}, sub-meter of {t['parentPowerMeterId']})")
        ai(S, f, f'{q}_kWh', 0.0, 'kWh', 0, note=f"FIELD AI: tenant {t['tenantId']} energy register (billing, revenue-grade meter)", hist='5min')
        tk.append(q)
    if tk:
        MATH(S, f, f'PM_{p}_TenantSum', 'Add', *[f'{q}_kW' for q in tk])
        MATH(S, f, f'PM_{p}_ReconLim0', 'Multiply', f'PM_{p}_kW', 'MTR_ReconTolPct', 'PctToFrac'); MATH(S, f, f'PM_{p}_ReconLim', 'Add', f'PM_{p}_kW', f'PM_{p}_ReconLim0', 'One')
        CMP(S, f, f'PM_{p}_ReconBad', 'GreaterThan', f'PM_{p}_TenantSum', f'PM_{p}_ReconLim'); DLY(S, f, f'PM_{p}_ReconDly', f'PM_{p}_ReconBad', tm(900000, 20000))
        alarm(S, f, f'PM_{p}_ReconcileAlarm', f'PM_{p}_ReconDly', 'Mismatch', 'Normal', 'Warning', f'Floor {fl}: tenant sub-meters exceed the floor meter (CT / wiring / meter)')
    # simulation
    sf = 'Simulation/Metering'
    if len(fl_valves) > 1: MATH(S, sf, f'Sim_{p}_ValveSum', 'Add', *fl_valves)
    vs = f'Sim_{p}_ValveSum' if len(fl_valves) > 1 else fl_valves[0]
    S.param(f'Sim_{p}_DesignFlow', 30.0 if fl > 1 else 45.0, 'm3h', folder=sf, prec=1, note='floor design CHW flow (simulation)')
    MATH(S, sf, f'Sim_{p}_Flow', 'Multiply', vs, 'PctToFrac', f'Sim_{p}_DesignFlow'); simlink(S, f'FM_{p}_Flow', f'Sim_{p}_Flow')
    simlink(S, f'TT_S_{p}', 'CHWS'); CMP(S, sf, f'Sim_{p}_Fl', 'GreaterThan', f'Sim_{p}_Flow', 'MTR_FlowMinShow')
    SW(S, sf, f'Sim_{p}_DT', f'Sim_{p}_Fl', 'AirX_SimChwDT', 'Zero'); MATH(S, sf, f'Sim_{p}_TR', 'Add', 'CHWS', f'Sim_{p}_DT'); simlink(S, f'TT_R_{p}', f'Sim_{p}_TR')
    for q in tk: simlink(S, f'{q}_kW', 'AirX_SimTenantKW')
    fan = f'{ahu_of(fl)}_FanSpeedCmd' if fl > 1 else 'Zero'
    MATH(S, sf, f'Sim_{p}_Fan3', 'Multiply', fan, fan, fan, 'PctToFrac'); MATH(S, sf, f'Sim_{p}_FanKW', 'Multiply', f'Sim_{p}_Fan3', 'PctToFrac', 'PctToFrac', 'AirX_SimFanKW')
    MATH(S, sf, f'Sim_{p}_kW', 'Add', f'Sim_{p}_FanKW', *([f'{q}_kW' for q in tk] or ['AirX_SimTenantKW']))
    simlink(S, f'PM_{p}_kW', f'Sim_{p}_kW')


# ------------------------------------------------------------------ toilet / janitor exhaust dampers (r5)
def exhaust_damper(S, d):
    """R9 MD-EA-<room>: two-position exhaust damper on the toilet exhaust riser branch. Open while the building is occupied
    (ASHRAE 62.1 Table 6-4: toilet exhaust whenever the space is occupied; R9 control note: exhaust schedule / interlock, no shutdown
    from CO2), forced open by TE_ForceOpen, closed on fire alarm when TE_CloseOnFire (fire strategy). End-switch proof -> fault alarm."""
    fl, n = d['floor'], f"TE_{nm(d['room'])}"; f = f'{AIR}/Floors/F{fl:02d}/Exhaust'
    di(S, f, f'{n}_DmpFb', False, 'Open', 'Closed', note=f"FIELD DI: {d['id']} damper end switch (open)")
    OR(S, f, f'{n}_Req', 'Sch_AHU', 'TE_ForceOpen')
    OR(S, f, f'{n}_FireOK', 'NotFireAlarm', 'TE_FireStay')
    AND(S, f, f'{n}_CmdLogic', f'{n}_Req', f'{n}_FireOK')
    S.bpoint(f, f'{n}_DmpCmd', f'{n}_CmdLogic', 'Open', 'Closed', kind='do', note=f"FIELD DO: {d['id']} damper open command")
    NOT(S, f, f'{n}_FbN', f'{n}_DmpFb'); NOT(S, f, f'{n}_CmdN', f'{n}_DmpCmd')
    AND(S, f, f'{n}_NotOpened', f'{n}_DmpCmd', f'{n}_FbN'); AND(S, f, f'{n}_NotClosed', f'{n}_CmdN', f'{n}_DmpFb')
    OR(S, f, f'{n}_Mismatch', f'{n}_NotOpened', f'{n}_NotClosed'); DLY(S, f, f'{n}_MismatchDly', f'{n}_Mismatch', tm(120000, 4000))
    alarm(S, f, f'{n}_DamperFaultAlarm', f'{n}_MismatchDly', 'Fault', 'Normal', 'Warning', f"{d['id']}: exhaust damper does not follow its command (end switch)")
    sf = f'{AIR}/Simulation/Floors/F{fl:02d}'
    DLY(S, sf, f'Sim_{n}_Fb', f'{n}_DmpCmd', tm(15000, 1500), tm(15000, 1500), note='simulation: actuator stroke time')
    simlink(S, f'{n}_DmpFb', f'Sim_{n}_Fb')
    return n


# ------------------------------------------------------------------ build
def build_office(S):
    common(S)
    const(S, 'PctToFrac', 0.01, 'none', 2, '% -> fraction'); const(S, 'Two', 2.0, 'none', 0)
    const(S, 'AirX_VavFlowShow', 10.0, 'none', 0, '3D: VAV airflow above this L/s = air shown flowing')
    for n, v in (('AirX_SimFlowGain', 1.1), ('AirX_SimFlowFloor', 0.05), ('AirX_SimDmpK', 0.008), ('AirX_SimDmpBase', 1.4), ('AirX_SimOAGain', 1.1),
                 ('AirX_SimCO2Out', 420.0), ('AirX_SimPlainRoomT', 27.0)):
        const(S, n, v, 'none', 3, 'simulation')
    R = rooms_by_id(); vt = od()['airTerminals']; vav_rooms = {t['room'] for t in vt}
    out = {}
    for fl in range(1, 9):
        rooms_fl = [r for r in od()['rooms'] if r['floor'] == fl]
        sch = 'Sch_AHU'
        vavs, rk, vk = [], [], []
        for r in rooms_fl:
            f = f'{AIR}/Floors/F{fl:02d}/Rooms/{nm(r["id"])}'
            k = room_sensor(S, fl, r, f)
            if r['id'] not in vav_rooms: plain_room_sim(S, k, fl)
        for t in [x for x in vt if x['floor'] == fl]:
            r = R[t['room']]
            ahu = ahu_of(fl) if fl > 1 else FLOOR_AHU_1.get(t['room'], 'AHU01')
            v, k, vmax = vav(S, t, r, fl, ahu, sch, f'{ahu}_Status')
            vavs.append(v); rk.append(k); vk.append((v, k, vmax, ahu))
        out[fl] = (vavs, rk, vk)
        if fl > 1: ahu_control(S, fl, vavs)
    # simulation (after every floor exists: the floor model reads the AHU)
    for fl, (vavs, rk, vk) in out.items():
        if fl > 1: ahu_sim(S, fl, vavs, rk)
        for v, k, vmax, ahu in vk: vav_sim(S, v, k, vmax, fl, f'{ahu}_SAT', 'Sch_AHU')
    NOT(S, f'{AIR}/Floors/Common', 'TE_FireStay', 'TE_CloseOnFire')
    te = [exhaust_damper(S, d) for d in od()['motorizedDampers'] if not d.get('integralVAV')]
    for m in od()['floorMeters']:
        fl = m['floor']
        metering(S, m, [f'{ahu_of(fl)}_ValveCmd'] if fl > 1 else ['AHU01_ValveCmd', 'AHU02_ValveCmd'])
    S.log.append(('V7.9 r4', 'AirSide/Floors', f"{len(vt)} VAV terminals, {len(od()['rooms'])} room sensors, {len(od()['floorMeters'])} floor meters",
                  'v79_office.py (R9 design)', '', ''))
    S.log.append(('V7.9 r5', 'AirSide/Floors/Fnn/Exhaust', f'{len(te)} toilet / janitor exhaust dampers (schedule, fire close, end-switch proof)',
                  'v79_office.py (R9 MD-EA)', '', ''))


_scale = SC.scale


def scale(S):
    _scale(S)
    build_office(S)


SC.scale = scale
