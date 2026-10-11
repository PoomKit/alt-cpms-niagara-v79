"""Build ALT_CP_Ref_V7_1 = V7 (make_v7.py, unchanged, imported) + V7.1 layer.

V7.1 layer (v71(S, prof), runs after the V7 air side):
  1. CT entering (inlet) TT per tower + range / approach calcs                   (item 6)
  2. CT make-up valve control + basin HIGH-HIGH (overflow) alarm                 (item 7)
  3. VFD detail points per drive: output V, DC bus V, drive temp, fault code,
     amps (air side), over-temperature alarm + emulation                          (item 8)
  4. VSD minimum / maximum speed per drive (writable, clamped 0-100 %)            (item 10)
  5. Chiller set selection (Set 1 / Set 2, pools linked to the set) and
     daily / weekly automatic rotation at 00:00 (TimeTrigger -> OneShot -> Counter -> Modulus)  (item 9)
  6. Power meter kVA / main meter demand calcs                                    (item 8)
REFERENCE SIMULATION – NOT PROJECT APPROVED.  Output is a NEW station file (does not touch V7).
usage: make_v71.py c_v5.bog c_v5.tsv out.bog --regdir reg71 [--timing fpt]
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_v6 as M6
import make_v7 as M7
from make_v7 import AND, OR, NOT, DLY, PULSE, SW, BSW, MATH, CMP, HYST, const, ai, di, simlink, T, F, AIR, UNITS, _f

M6.STATION = M7.STATION = 'ALT_CP_Ref_V7_1'
M7.FOXS_PORT = '4919'

PLANT_VSD = [('CHP01', 30.0), ('CHP02', 30.0), ('CDP01', 30.0), ('CDP02', 30.0), ('CT01', 20.0), ('CT02', 20.0)]
AIR_VSD = [('AHU01', 30.0), ('AHU02', 30.0), ('OAU01', 20.0), ('EF02', 20.0), ('EF03', 20.0), ('CPEF01', 30.0), ('LSF01', 30.0)]
SI = 'Simulation/Instruments'


def _src_of(S, target, slot):
    el = S.comp[target]
    L = [c for c in el if c.get('t') == 'b:Link' and M6.child(c, 'targetSlotName').get('v') == slot]
    assert len(L) == 1, (target, slot)
    h = M6.child(L[0], 'sourceOrd').get('v')[2:]
    return next(n for n, e in S.comp.items() if e.get('h') == h)


def ct_temps(S, prof):
    for n in UNITS:
        u = f'CT{n}'
        ai(S, f'{u}/Points', f'{u}_InletTemp', 35.0, 'C', note='TT tower entering (hot) water, downstream of the inlet valve')
        MATH(S, f'{u}/Logic', f'{u}RangeCalc', 'Subtract', f'{u}_InletTemp', f'{u}_OutletTemp')
        S.npoint(f'{u}/Monitor', f'{u}_Range', f'{u}RangeCalc', 'none', 1, note='tower range = entering - leaving')
        MATH(S, f'{u}/Logic', f'{u}ApproachCalc', 'Subtract', f'{u}_OutletTemp', 'OA_WetBulb')
        S.npoint(f'{u}/Monitor', f'{u}_Approach', f'{u}ApproachCalc', 'none', 1, note='tower approach = leaving - OA wet bulb')
        # emulation: entering = CDW return header while the inlet valve is open, basin temperature otherwise (stagnant)
        SW(S, SI, f'Sim_{u}_Inlet', f'Sim_{u}_ValveFb', 'CDR', f'{u}_BasinTemp')
        simlink(S, f'{u}_InletTemp', f'Sim_{u}_Inlet', 'entering = CDR when valve open')
    for n in UNITS:
        S.meta[f'CT{n}_Range']['hist'] = '5min'; S.meta[f'CT{n}_Approach']['hist'] = '5min'


def ct_level(S, prof):
    S.param('CT_LevelMakeupOpenPct', 70.0, 'pct', note='make-up valve opens below this basin level')
    S.param('CT_LevelMakeupClosePct', 80.0, 'pct', note='make-up valve closes above this basin level')
    S.param('CT_LevelHighHighPct', 98.0, 'pct', note='basin HIGH-HIGH (overflow) - make-up forced closed')
    for n in UNITS:
        u = f'CT{n}'
        L = f'{u}/Logic'
        CMP(S, L, f'{u}LevelBelowOpen', 'LessThan', f'{u}_BasinLevel', 'CT_LevelMakeupOpenPct')
        CMP(S, L, f'{u}LevelAboveClose', 'GreaterThan', f'{u}_BasinLevel', 'CT_LevelMakeupClosePct')
        # latch: open below 70 %, close above 80 % (order-independent seal-in)
        M7.sealin(S, L, f'{u}MakeupDemand', f'{u}LevelBelowOpen', f'{u}LevelAboveClose', note='fill 70 -> 80 %')
        CMP(S, 'Alarms', f'{u}LevelAboveHH', 'GreaterThan', f'{u}_BasinLevel', 'CT_LevelHighHighPct')
        OR(S, 'Alarms', f'{u}LevelHHLogic', f'{u}LevelAboveHH', f'{u}_HighLevelSwitch', note='analog HH or overflow float switch')
        DLY(S, 'Alarms', f'{u}LevelHHDelay', f'{u}LevelHHLogic', 10000, 5000)
        S.bpoint('Alarms', f'{u}BasinHighHighLevelAlarm', f'{u}LevelHHDelay', 'HIGH-HIGH', 'Normal')
        M6.COS[f'{u}BasinHighHighLevelAlarm'] = (True, 'Critical', f'{u} basin level HIGH-HIGH / overflow - make-up valve forced closed, check valve')
        # level transmitter out of range -> float control only (valve closed, alarm from the existing low/high switches)
        CMP(S, L, f'{u}LevelSensorLow', 'LessThan', f'{u}_BasinLevel', 'ZeroSpeed')
        CMP(S, L, f'{u}LevelSensorHigh', 'GreaterThan', f'{u}_BasinLevel', 'HundredPct')
        OR(S, L, f'{u}LevelSensorBad', f'{u}LevelSensorLow', f'{u}LevelSensorHigh')
        NOT(S, L, f'{u}NotLevelSensorBad', f'{u}LevelSensorBad')
        NOT(S, L, f'{u}NotLevelHH', f'{u}LevelHHLogic')
        AND(S, L, f'{u}MakeupPermit', f'{u}MakeupDemand', f'{u}NotLevelHH', f'{u}NotLevelSensorBad')
        S.bpoint(f'{u}/Points', f'{u}_MakeupValveCmd', f'{u}MakeupPermit', 'OPEN', 'CLOSE', kind='do', note='basin make-up solenoid valve')


def vfd_details(S, prof):
    S.param('VFD_TempHighC', 70.0, 'C', note='VFD heatsink over-temperature alarm')
    const(S, 'Sim_VPerPct', 4.0, note='SIM: 400 V at 100 %')
    const(S, 'Sim_DcBusV', 540.0, 'V', note='SIM: DC bus 400 V x 1.35')
    const(S, 'Sim_DriveTempBase', 32.0, 'C'); const(S, 'Sim_DriveTempPerPct', 0.25)
    const(S, 'Sim_AmpsPerKW', 1.8, note='SIM: 400 V 3-ph, PF 0.85')
    for u, _ in PLANT_VSD + AIR_VSD:
        air = u not in dict(PLANT_VSD)
        Pt, Mo = (_f(u, 'Points'), _f(u, 'Monitor')) if air else (f'{u}/Points', f'{u}/Monitor')
        L = _f(u, 'Logic') if air else f'{u}/Logic'
        SIM = f'{AIR}/Simulation' if air else SI
        cmd = f'{u}_SpeedCmd' if air else f'{u}SpeedCmd'
        run = f'Sim_{u}_StatusFb' if air else f'Sim_{u}_RunFb'
        ai(S, Pt, f'{u}_VfdOutputV', 0.0, 'V', note='VFD output voltage (BACnet/Modbus)', hist='5min')
        ai(S, Pt, f'{u}_VfdDcBusV', 540.0, 'V', note='VFD DC bus voltage', hist='5min')
        ai(S, Pt, f'{u}_VfdTemp', 32.0, 'C', note='VFD heatsink temperature', hist='5min')
        ai(S, Pt, f'{u}_VfdFaultCode', 0.0, 'none', prec=0, note='VFD last/active fault code (0 = none)', hist='5min')
        if air: ai(S, Pt, f'{u}_Amps', 0.0, 'A', note='VFD output current', hist='5min')
        CMP(S, L, f'{u}VfdTempHigh', 'GreaterThan', f'{u}_VfdTemp', 'VFD_TempHighC')
        DLY(S, L, f'{u}VfdTempHighDelay', f'{u}VfdTempHigh', 60000 if prof is M6.TIMING['site'] else 2000, 10000 if prof is M6.TIMING['site'] else 1000)
        S.bpoint(Mo, f'{u}_VfdOverTempAlarm', f'{u}VfdTempHighDelay', 'OVER TEMP', 'Normal')
        M6.COS[f'{u}_VfdOverTempAlarm'] = (True, 'Warning', f'{u} VFD heatsink over-temperature - check panel ventilation')
        CMP(S, L, f'{u}VfdFaultCodeActive', 'GreaterThan', f'{u}_VfdFaultCode', 'ZeroSpeed')
        S.bpoint(Mo, f'{u}_VfdFaultCodeActive', f'{u}VfdFaultCodeActive', 'FAULT CODE', 'None')
        # emulation
        SW(S, SIM, f'Sim_{u}_RunOne', run, 'One', 'ZeroSpeed')
        MATH(S, SIM, f'Sim_{u}_OutV', 'Multiply', cmd, 'Sim_VPerPct', f'Sim_{u}_RunOne'); simlink(S, f'{u}_VfdOutputV', f'Sim_{u}_OutV', 'V/Hz')
        simlink(S, f'{u}_VfdDcBusV', 'Sim_DcBusV', 'DC bus constant')
        simlink(S, f'{u}_VfdFaultCode', 'ZeroSpeed', 'no fault (override in8 to test)')
        MATH(S, SIM, f'Sim_{u}_TempRise', 'Multiply', cmd, 'Sim_DriveTempPerPct', f'Sim_{u}_RunOne')
        MATH(S, SIM, f'Sim_{u}_Temp', 'Add', 'Sim_DriveTempBase', f'Sim_{u}_TempRise'); simlink(S, f'{u}_VfdTemp', f'Sim_{u}_Temp', 'drive temperature')
        if air:
            MATH(S, SIM, f'Sim_{u}_A', 'Multiply', f'{u}_kW', 'Sim_AmpsPerKW'); simlink(S, f'{u}_Amps', f'Sim_{u}_A', 'kW x 1.8')
        M6.COS[f'{u}_VfdFaultCodeActive'] = (True, 'Warning', f'{u} VFD reports a fault / warning code')


def vsd_minmax(S, prof):
    """Per-drive min / max speed after the control output, before the start gate:
    speed = min( max(control, Min), max(Max, Min) ); fire duty (CPEF01) is not limited by Max."""
    for u, dmin in PLANT_VSD + AIR_VSD:
        air = u not in dict(PLANT_VSD)
        Pt = _f(u, 'Points') if air else f'{u}/Points'
        L = _f(u, 'Logic') if air else f'{u}/Logic'
        gate = f'{u}FixedSpeedGate' if u.startswith('CDP') else f'{u}SpeedGate'
        src = _src_of(S, gate, 'inTrue')
        S.param(f'{u}_MinSpeed', dmin, 'pct', folder=Pt, lo=0, hi=100, note='VSD minimum speed (commissioning)')
        S.param(f'{u}_MaxSpeed', 100.0, 'pct', folder=Pt, lo=0, hi=100, note='VSD maximum speed (commissioning)')
        MATH(S, L, f'{u}SpeedAboveMin', 'Maximum', src, f'{u}_MinSpeed')
        MATH(S, L, f'{u}SpeedMaxEff', 'Maximum', f'{u}_MaxSpeed', f'{u}_MinSpeed', note='max never below min')
        mx = f'{u}SpeedMaxEff'
        if u == 'CPEF01':
            SW(S, L, f'{u}SpeedMaxFire', 'FireAlarmSignal', 'HundredPct', f'{u}SpeedMaxEff', note='fire: smoke clearance 100 % not limited')
            mx = f'{u}SpeedMaxFire'
        MATH(S, L, f'{u}SpeedMinMax', 'Minimum', f'{u}SpeedAboveMin', mx)
        S.rewire(gate, 'inTrue', f'{u}SpeedMinMax', src)


def rotation(S, prof):
    """Set 1 / Set 2 selection + daily / weekly rotation (auto change-over at 00:00)."""
    LL = 'PlantControl/LeadLag'
    PT = 'PlantControl/Points'
    S.bparam('Set_LinkPools', True, folder=PT, t='Linked to set', f='Independent',
             note='Linked: CHP/CDP/CT lead follows the lead chiller set (Set 1 = CH01+CHP01+CDP01+CT01)')
    S.bparam('RotationMode_Daily', False, folder=PT, t='Daily', f='Off', note='swap the lead set every day at the rotation time')
    S.bparam('RotationMode_Weekly', False, folder=PT, t='Weekly', f='Off', note='swap the lead set every 7 days at the rotation time')
    S.add(LL, 'RotationTrigger', 'c:TimeTrigger', props=[('triggerMode', 'c:DailyTriggerMode', '00:00:00.000;7f;0')],
          note='daily 00:00 (edit triggerMode to change the change-over time) -> fire action link')
    PULSE(S, LL, 'RotationDayPulse', None, 2000, note='fired by RotationTrigger')
    S.link(S.comp['RotationDayPulse'], 'RotationTrigger.fireTrigger', 'fire')
    S.kc(LL, 'RotationDayCounter', 'Counter', {'countUp': 'RotationDayPulse'}, note='days since commissioning (clear action resets)')
    const(S, 'Two', 2.0); const(S, 'Fourteen', 14.0); const(S, 'Seven', 7.0); const(S, 'Half', 0.5)
    MATH(S, LL, 'RotationDayMod2', 'Modulus', 'RotationDayCounter', 'Two')
    CMP(S, LL, 'RotationDayOdd', 'GreaterThan', 'RotationDayMod2', 'Half')
    MATH(S, LL, 'RotationDayMod14', 'Modulus', 'RotationDayCounter', 'Fourteen')
    CMP(S, LL, 'RotationWeekOdd', 'GreaterThanEqual', 'RotationDayMod14', 'Seven')
    NOT(S, LL, 'NotRotationRuntime', 'RotationMode_Runtime')
    NOT(S, LL, 'NotRotationDaily', 'RotationMode_Daily')
    AND(S, LL, 'DailyRotationRequest', 'RotationMode_Daily', 'RotationDayOdd', 'NotRotationRuntime')
    AND(S, LL, 'WeeklyRotationRequest', 'RotationMode_Weekly', 'RotationWeekOdd', 'NotRotationRuntime', 'NotRotationDaily')
    S.rewire('RotationRequestFinal', 'inC', 'DailyRotationRequest')
    S.rewire('RotationRequestFinal', 'inD', 'WeeklyRotationRequest')
    S.npoint('PlantControl/Monitor', 'RotationDayCount', 'RotationDayCounter', 'none', 0, note='days counted by the rotation trigger')
    S.bpoint('PlantControl/Monitor', 'LeadSet', 'EffectiveLeadCH01', 'SET 1', 'SET 2', note='effective lead set (after rotation / availability)')
    M6.NO_HISTORY.update({'Two', 'Fourteen', 'Seven', 'Half'})
    # pools follow the chiller set when linked
    for eq in M7.POOLS:
        BSW(S, 'PlantControl/EquipmentPools', f'{eq}_LeadSelSet', 'Set_LinkPools', 'RotatedLeadCH01', f'{eq}_LeadSel01',
            note='linked: follow the lead chiller set; independent: runtime / manual per pool')
        S.rewire(f'{eq}_Lead01Healthy', 'inA', f'{eq}_LeadSelSet', f'{eq}_LeadSel01')


def meters(S, prof):
    const(S, 'PF_Min', 0.1, prec=2, note='guard: kVA = kW / max(PF, 0.1) (no divide-by-zero when the meter reads PF 0)')
    MATH(S, 'Metering/Power', 'PM_Main_PFSafe', 'Maximum', 'PM_Main_PF', 'PF_Min')
    MATH(S, 'Metering/Power', 'PM_Main_kVACalc', 'Divide', 'PM_Main_kW', 'PM_Main_PFSafe')
    S.npoint('Metering/Power', 'PM_Main_kVA', 'PM_Main_kVACalc', 'none', 1, note='apparent power kVA')
    for n in UNITS:
        MATH(S, f'Chiller{n}/Monitor', f'CH{n}_PFSafe', 'Maximum', f'CH{n}_PF', 'PF_Min')
        MATH(S, f'Chiller{n}/Monitor', f'CH{n}_kVACalc', 'Divide', f'CH{n}_kW', f'CH{n}_PFSafe')
        S.npoint(f'Chiller{n}/Monitor', f'CH{n}_kVA', f'CH{n}_kVACalc', 'none', 1, note='apparent power kVA')
    const(S, 'PM_Main_PctPerKW', 100.0 / 800.0, prec=4, note='100 / transformer-feeder rating 800 kW (PROJECT)')
    MATH(S, 'Metering/Power', 'PM_Main_LoadPctCalc', 'Multiply', 'PM_Main_kW', 'PM_Main_PctPerKW')
    S.npoint('Metering/Power', 'PM_Main_LoadPct', 'PM_Main_LoadPctCalc', 'pct', 1, note='feeder loading')


def _mv_onoff(S, P, L, SIM, tag, cmd_src, prof, note):
    """Two-position (on/off) motorised isolation valve: DO open/close + AI position feedback % (open >= 80 %, closed <= 20 %),
    command-failure alarm after the stroke timeout (reference: PUNN/Goldmarktech MV program, feedback% > 20 = status)."""
    S.bpoint(P, f'{tag}Cmd', cmd_src, 'OPEN', 'CLOSE', kind='do', note=note)
    ai(S, P, f'{tag}Fb', 0.0, 'pct', note='valve position feedback 0-100 % (actuator 2-10 V)', hist='5min')
    CMP(S, L, f'{tag}Open', 'GreaterThanEqual', f'{tag}Fb', 'MV_OpenPct')
    CMP(S, L, f'{tag}NotClosed', 'GreaterThan', f'{tag}Fb', 'MV_ClosedPct')
    NOT(S, L, f'{tag}NotOpen', f'{tag}Open'); NOT(S, L, f'{tag}CmdClose', f'{tag}Cmd')
    AND(S, L, f'{tag}FailOpen', f'{tag}Cmd', f'{tag}NotOpen'); AND(S, L, f'{tag}FailClose', f'{tag}CmdClose', f'{tag}NotClosed')
    OR(S, L, f'{tag}FailLogic', f'{tag}FailOpen', f'{tag}FailClose')
    DLY(S, L, f'{tag}FailDelay', f'{tag}FailLogic', prof['valve_timeout'], 5000 if prof['valve_timeout'] > 60000 else 1000)
    S.bpoint('Alarms', f'{tag}FailAlarm', f'{tag}FailDelay', 'Command failure', 'Normal')
    M6.COS[f'{tag}FailAlarm'] = (True, 'Warning', f'{tag.rstrip("_")} motorised valve did not reach the commanded position')
    DLY(S, SIM, f'Sim_{tag}Stroke', f'{tag}Cmd', prof['sim_valve'], prof['sim_valve'])
    SW(S, SIM, f'Sim_{tag}Pos', f'Sim_{tag}Stroke', 'HundredPct', 'ZeroSpeed'); simlink(S, f'{tag}Fb', f'Sim_{tag}Pos', 'on/off stroke')


def _mv_mod(S, P, L, SIM, tag, cmd_src, prof, note):
    """Modulating (0-100 %) motorised control valve: AO command + AI feedback, mismatch alarm |cmd - fb| > 10 %."""
    S.npoint(P, f'{tag}Cmd', cmd_src, 'pct', 1, kind='ao', note=note)
    ai(S, P, f'{tag}Fb', 0.0, 'pct', note='valve position feedback 0-100 %', hist='5min')
    MATH(S, L, f'{tag}Err', 'Subtract', f'{tag}Cmd', f'{tag}Fb'); MATH(S, L, f'{tag}ErrAbs', 'AbsValue', f'{tag}Err')
    CMP(S, L, f'{tag}ErrHigh', 'GreaterThan', f'{tag}ErrAbs', 'MV_MismatchPct')
    DLY(S, L, f'{tag}MismatchDelay', f'{tag}ErrHigh', prof['valve_timeout'], 5000 if prof['valve_timeout'] > 60000 else 1000)
    S.bpoint('Alarms', f'{tag}MismatchAlarm', f'{tag}MismatchDelay', 'Mismatch', 'Normal')
    M6.COS[f'{tag}MismatchAlarm'] = (True, 'Warning', f'{tag.rstrip("_")} control valve feedback does not follow the command')
    M7.RATE(S, SIM, f'Sim_{tag}Pos', f'{tag}Cmd', 100.0 / max(prof['sim_valve'] / 1000.0, 1.0)); simlink(S, f'{tag}Fb', f'Sim_{tag}Pos', 'actuator travel')


def valves(S, prof):
    """Motorised valves at the inlet / outlet of every item of plant (V7.1, user item 1).
    Type selection (on/off = isolation / sequencing, modulating = control of a process variable):
      chiller evaporator inlet  : on/off isolation (existing CHnValveOpenCmd + end switch)
      chiller evaporator outlet : MODULATING flow-limiting valve (FCV / energy-valve style, PID on barrel flow, min 20 %)
      chiller condenser inlet   : on/off isolation (existing CHnCdwValveOpenCmd + end switch)
      chiller condenser outlet  : MODULATING head-pressure valve (reset on entering CDW temp 15 -> 20 degC = 30 -> 100 %)
      pump suction / discharge  : on/off isolation, normally OPEN (auto-isolate a failed / out-of-service pump; start interlock)
      tower inlet / outlet      : on/off isolation (inlet existing; outlet new, opened with the inlet so an idle cell is fully isolated)
      CHW bypass, AHU/OAU coils : modulating (existing);  FCU coil : on/off (existing)"""
    S.param('MV_OpenPct', 80.0, 'pct', note='on/off valve: feedback >= this = OPEN')
    S.param('MV_ClosedPct', 20.0, 'pct', note='on/off valve: feedback <= this = CLOSED')
    S.param('MV_MismatchPct', 10.0, 'pct', note='modulating valve: |cmd - fb| alarm band')
    S.param('CH_ChwFlowLimit', 260.0, 'm3h', note='evaporator flow limit per chiller (FCV throttles above) - PROJECT')
    S.param('CH_FcvMinPos', 20.0, 'pct', note='FCV minimum position while the chiller is on line')
    S.param('CH_HpvTempLow', 15.0, 'C', note='entering CDW temp at which the head-pressure valve is at minimum')
    S.param('CH_HpvTempHigh', 20.0, 'C', note='entering CDW temp at which the head-pressure valve is fully open')
    S.param('CH_HpvMinPos', 30.0, 'pct', note='head-pressure valve minimum position')
    # ---- chillers: evaporator outlet FCV + condenser outlet head-pressure valve
    for n in UNITS:
        c = f'CH{n}'; P, L = f'Chiller{n}/Points', f'Chiller{n}/Monitor'
        M7.PID(S, L, f'{c}FcvThrottle', f'{c}_ChwFlow', 'CH_ChwFlowLimit', f'{c}ValveOpenCmd', 'direct', 0.2, 2.0, 0.0, 100.0,
               note='flow limiting: throttle 0 % below the limit (valve fully open), rises when the barrel is over-flowed')
        MATH(S, L, f'{c}FcvLoop', 'Subtract', 'HundredPct', f'{c}FcvThrottle')
        MATH(S, L, f'{c}FcvAboveMin', 'Maximum', f'{c}FcvLoop', 'CH_FcvMinPos')
        SW(S, L, f'{c}FcvGate', f'{c}ValveOpenCmd', f'{c}FcvAboveMin', 'ZeroSpeed', note='closed when the chiller is isolated')
        _mv_mod(S, P, L, SI, f'{c}_ChwFCV', f'{c}FcvGate', prof, 'evaporator outlet flow-control valve (modulating)')
        M7.RESET(S, L, f'{c}HpvReset', f'{c}_CdwEnteringTemp', 'CH_HpvTempLow', 'CH_HpvTempHigh', 'CH_HpvMinPos', 'HundredPct')
        SW(S, L, f'{c}HpvGate', f'{c}CdwValveOpenCmd', f'{c}HpvReset', 'ZeroSpeed')
        _mv_mod(S, P, L, SI, f'{c}_CdwHPV', f'{c}HpvGate', prof, 'condenser outlet head-pressure control valve (modulating)')
    # ---- pumps: suction + discharge isolation (normally open)
    for eq in ('CHP', 'CDP'):
        for n in UNITS:
            u = f'{eq}{n}'; P, L = f'{u}/Points', f'{u}/Logic'
            S.bparam(f'{u}_ServiceIsolate', False, folder=P, t='ISOLATED', f='In service',
                     note='maintenance: close both valves and take the pump out of the pool')
            NOT(S, L, f'{u}NotService', f'{u}_ServiceIsolate')
            OR(S, L, f'{u}MVKeepOpen', f'{u}NotFailLatched', f'{u}RunProof', note='a failed pump is isolated once stopped')
            AND(S, L, f'{u}MVOpenLogic', f'{u}NotService', f'{u}MVKeepOpen')
            _mv_onoff(S, P, L, SI, f'{u}_SuctionMV', f'{u}MVOpenLogic', prof, 'pump suction isolation valve (on/off, normally open)')
            _mv_onoff(S, P, L, SI, f'{u}_DischargeMV', f'{u}MVOpenLogic', prof, 'pump discharge isolation valve (on/off, normally open)')
            AND(S, L, f'{u}MVPathOpen', f'{u}_SuctionMVOpen', f'{u}_DischargeMVOpen')
            AND(S, L, f'{u}StartPermitMV', f'{u}StartPermit', f'{u}MVPathOpen', note='never start against a closed suction / discharge valve')
            S.rewire(f'{u}StartCmd', 'in16', f'{u}StartPermitMV', f'{u}StartPermit')
            OR(S, L, f'{u}MVFailAny', f'{u}_SuctionMVFailDelay', f'{u}_DischargeMVFailDelay')
            S.rewire(f'{u}FaultAny', 'inC', f'{u}MVFailAny', F)
            S.rewire(f'{u}FaultAny', 'inD', f'{u}_ServiceIsolate', F)
    # ---- towers: outlet isolation valve with the inlet valve; water path = both proven
    for n in UNITS:
        u = f'CT{n}'; P, L = f'{u}/Points', f'{u}/Logic'
        _mv_onoff(S, P, L, SI, f'{u}_OutletMV', f'{u}ValveDemand', prof, 'tower outlet (basin) isolation valve (on/off)')
        AND(S, L, f'{u}WaterPathProof', f'{u}ValveOpenProof', f'{u}_OutletMVOpen', note='inlet end switch AND outlet feedback >= 80 %')
        S.rewire(f'{u}StartPermit', 'inB', f'{u}WaterPathProof', f'{u}ValveOpenProof')
        S.rewire('CT_WaterPathProven', 'inA' if n == '01' else 'inB', f'{u}WaterPathProof', f'{u}ValveOpenProof')
        S.rewire(f'{u}FaultAny', 'inD', f'{u}_OutletMVFailDelay', F)


def v71(S, prof):
    valves(S, prof)
    ct_temps(S, prof)
    ct_level(S, prof)
    vfd_details(S, prof)
    vsd_minmax(S, prof)
    rotation(S, prof)
    meters(S, prof)


_air = M7.airside


def airside_and_v71(S, prof):
    _air(S, prof)
    v71(S, prof)


M7.airside = airside_and_v71
M7.PX_PLANT[:] = [('Plant', 'ALT_V7_Plant'), ('Plant3D', 'ALT_V71_Plant3D'), ('Chillers', 'ALT_V71_Chillers'), ('PlantDetail', 'ALT_V7_PlantDetail'),
                  ('Drives', 'ALT_V71_Drives'), ('Meters', 'ALT_V71_Meters'), ('Schedules', 'ALT_V71_Schedules'), ('Optimization', 'ALT_CP_Optimization'),
                  ('EnergyDashboard', 'ALT_CP_EnergyDashboard'), ('Energy', 'ALT_CP_Energy'), ('AlarmsHistory', 'ALT_CP_AlarmsHistory'),
                  ('Simulation', 'ALT_CP_Simulation')]

if __name__ == '__main__':
    M7.main()
