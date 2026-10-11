# -*- coding: utf-8 -*-
"""V7.9 air side for the 8-storey building (user request 8 Oct 2026).
   Floor 1 keeps the V7.8 air side (AHU01 / AHU02 / OAU01 / FCU01-04, zones 01_0101..0112).
   Floors 2..8: one floor AHU each (AHU_Fnn) + 4 zones (AirPlug naming ZoneTemperatureAvg_nn_nn01..04), from the register.
   Per floor AHU: Installed -> start request (schedule Sch_AHU or AirX_ManualOn, no fire alarm, no fault, no start failure)
     -> fan start -> proof (fail latch + alarm) -> CHW valve PID on the floor average zone temperature (out-of-service zones
     excluded) with dehumidification minimum when return RH is high -> fan speed from the valve, OA damper from CO2.
   Zones: temperature / RH, out-of-service switch, floor average + hottest, high temperature / RH alarms (Zone_* limits)."""
import make_v6 as M6
import make_v7 as M7
import v77_fieldcx as FCX
import v78_improve as IMP
from make_v7 import AND, OR, NOT, DLY, SW, MATH, CMP, PULSE, RATE, di, ai, simlink, PID, RESET, const, sealin
import v79_scale as SC

AIR = M7.AIR
tm, alarm = IMP.tm, IMP.alarm
FLOORS = list(range(2, 9))
ZPF = 4
ZONE_NAMES = ['Office north', 'Office south', 'Meeting', 'Core / corridor']


def zcode(fl, z):
    return f'{fl:02d}_{fl:02d}{z:02d}'


def floor_ahu(S, fl):
    u = f'AHU_F{fl:02d}'; f = f'{AIR}/Floors/F{fl:02d}'
    reg = next((r for r in SC.R().get('AirSide', []) if r.get('Unit') == u), {})
    S.param(f'{u}_ZoneSP', 24.0, 'C', folder=f, note='floor zone temperature setpoint')
    S.bparam(f'{u}_Installed', SC.eqreg.installed(reg) if reg else True, folder=f, t='Installed', f='Not installed', note=f'V7.9: floor {fl} air handling unit exists')
    S.param(f'{u}_DehumRH', 65.0, 'RH', folder=f, prec=0, note='return RH above this -> supply-air temperature setpoint limited to AirX_SatDehumMax (dehumidification)')
    di(S, f, f'{u}_Status', False, 'Running', 'Stopped', note='FIELD DI: supply fan running')
    di(S, f, f'{u}_Fault', False, 'Fault', 'Normal', note='FIELD DI: VSD / fan fault')
    di(S, f, f'{u}_FilterDirty', False, 'Dirty', 'Clean', note='FIELD DI: filter differential pressure switch')
    ai(S, f, f'{u}_SAT', 18.0, 'C', note='FIELD AI: supply air temperature')
    ai(S, f, f'{u}_RA_RH', 60.0, 'RH', note='FIELD AI: return air humidity')
    ai(S, f, f'{u}_RA_CO2', 700.0, 'none', prec=0, note='FIELD AI: return air CO2 (ppm)')
    # zones
    zt = []
    for z in range(1, ZPF + 1):
        c = zcode(fl, z); zf = f'{AIR}/Floors/F{fl:02d}/Zones'
        t, h, oos = f'ZoneTemperatureAvg_{c}', f'ZoneHumidityAvg_{c}', f'ZoneOutOfService_{c}'
        ai(S, zf, t, 26.0, 'C', note=f'FIELD AI (AirPlug / Sense-T): floor {fl} {ZONE_NAMES[z - 1]}')
        ai(S, zf, h, 60.0, 'RH', note=f'FIELD AI: floor {fl} {ZONE_NAMES[z - 1]} humidity')
        S.bparam(oos, False, folder=zf, t='Out of service', f='In service', note='excluded from the floor average / hottest')
        NOT(S, zf, f'Z{c}_InSvc', oos)
        SW(S, zf, f'Z{c}_TUse', f'Z{c}_InSvc', t, 'Zero'); SW(S, zf, f'Z{c}_N', f'Z{c}_InSvc', 'One', 'Zero')
        SW(S, zf, f'Z{c}_TMaxIn', f'Z{c}_InSvc', t, 'Zero'); SW(S, zf, f'Z{c}_HUse', f'Z{c}_InSvc', h, 'Zero')
        CMP(S, zf, f'Z{c}_THigh', 'GreaterThan', t, 'Zone_TempAlarmHigh'); CMP(S, zf, f'Z{c}_RHHigh', 'GreaterThan', h, 'Zone_RHAlarmHigh')
        AND(S, zf, f'Z{c}_THighUse', f'Z{c}_THigh', f'Z{c}_InSvc'); AND(S, zf, f'Z{c}_RHHighUse', f'Z{c}_RHHigh', f'Z{c}_InSvc')
        DLY(S, zf, f'Z{c}_THighDly', f'Z{c}_THighUse', tm(900000, 10000)); DLY(S, zf, f'Z{c}_RHHighDly', f'Z{c}_RHHighUse', tm(900000, 10000))
        alarm(S, zf, f'Zone_{c}_TempHighAlarm', f'Z{c}_THighDly', 'High', 'Normal', 'Warning', f'Floor {fl} {ZONE_NAMES[z - 1]}: temperature high')
        alarm(S, zf, f'Zone_{c}_RHHighAlarm', f'Z{c}_RHHighDly', 'High', 'Normal', 'Warning', f'Floor {fl} {ZONE_NAMES[z - 1]}: humidity high')
        zt.append(c)
    fa = f'{AIR}/Floors/F{fl:02d}/Zones'
    MATH(S, fa, f'Zone_F{fl:02d}_TSum', 'Add', *[f'Z{c}_TUse' for c in zt]); MATH(S, fa, f'Zone_F{fl:02d}_NSum', 'Add', *[f'Z{c}_N' for c in zt])
    MATH(S, fa, f'Zone_F{fl:02d}_NDiv', 'Maximum', f'Zone_F{fl:02d}_NSum', 'One')
    MATH(S, fa, f'Zone_F{fl:02d}_TAvgCalc', 'Divide', f'Zone_F{fl:02d}_TSum', f'Zone_F{fl:02d}_NDiv')
    # every zone out of service: no measurement left -> hold the floor at its setpoint (valve PID neutral, no false 0 C) + alarm
    CMP(S, fa, f'Zone_F{fl:02d}_NoneInSvc', 'LessThan', f'Zone_F{fl:02d}_NSum', 'One')
    SW(S, fa, f'Zone_F{fl:02d}_TAvgSel', f'Zone_F{fl:02d}_NoneInSvc', f'{u}_ZoneSP', f'Zone_F{fl:02d}_TAvgCalc')
    S.npoint(fa, f'Zone_F{fl:02d}_AvgTemp', f'Zone_F{fl:02d}_TAvgSel', 'C', 1, note=f'floor {fl}: average of the zones in service (setpoint if none)')
    MATH(S, fa, f'Zone_F{fl:02d}_TMaxCalc', 'Maximum', *[f'Z{c}_TMaxIn' for c in zt])
    SW(S, fa, f'Zone_F{fl:02d}_TMaxSel', f'Zone_F{fl:02d}_NoneInSvc', f'{u}_ZoneSP', f'Zone_F{fl:02d}_TMaxCalc')
    S.npoint(fa, f'Zone_F{fl:02d}_HottestTemp', f'Zone_F{fl:02d}_TMaxSel', 'C', 1, note=f'floor {fl}: hottest zone in service (setpoint if none)')
    AND(S, fa, f'Zone_F{fl:02d}_NoneInSvcInst', f'Zone_F{fl:02d}_NoneInSvc', f'{u}_Installed')
    alarm(S, fa, f'Zone_F{fl:02d}_AllOutOfServiceAlarm', f'Zone_F{fl:02d}_NoneInSvcInst', 'All out of service', 'Normal', 'Warning',
          f'Floor {fl}: every zone is out of service - floor AHU controls to its setpoint without measurement')
    MATH(S, fa, f'Zone_F{fl:02d}_RHSum', 'Add', *[f'Z{c}_HUse' for c in zt])
    MATH(S, fa, f'Zone_F{fl:02d}_RHAvgCalc', 'Divide', f'Zone_F{fl:02d}_RHSum', f'Zone_F{fl:02d}_NDiv')
    S.npoint(fa, f'Zone_F{fl:02d}_AvgRH', f'Zone_F{fl:02d}_RHAvgCalc', 'RH', 0, note=f'floor {fl}: average humidity')
    # start / proof
    OR(S, f, f'{u}_SchOn', 'Sch_AHU', 'AirX_ManualOn')
    NOT(S, f, f'{u}_NotFault', f'{u}_Fault')
    PULSE(S, f, f'{u}_ResetFire', note='reset the start-failure latch')
    OR(S, f, f'{u}_ResetAny', f'{u}_ResetFire', 'PlantAlarmResetFire')
    sealin(S, f, f'{u}_FailLatch', SC.F, f'{u}_ResetAny', note='start failure latch (trip = proof timeout, linked below)')
    NOT(S, f, f'{u}_NotFail', f'{u}_FailLatch')
    AND(S, f, f'{u}_ReqLogic', f'{u}_Installed', f'{u}_SchOn', 'NotFireAlarm', f'{u}_NotFault')
    AND(S, f, f'{u}_StartLogic', f'{u}_ReqLogic', f'{u}_NotFail')
    S.bpoint(f, f'{u}_StartCmd', f'{u}_StartLogic', 'ON', 'OFF', kind='do')
    NOT(S, f, f'{u}_NoProof', f'{u}_Status'); AND(S, f, f'{u}_CmdNoProof', f'{u}_StartCmd', f'{u}_NoProof')
    DLY(S, f, f'{u}_ProofTimeout', f'{u}_CmdNoProof', tm(60000, 8000))
    S.rewire(f'{u}_FailLatch', 'inA', f'{u}_ProofTimeout', SC.F)
    alarm(S, f, f'{u}_FailAlarm', f'{u}_FailLatch', 'Failed', 'Normal', 'Critical', f'{u} (floor {fl}) fan did not prove running')
    AND(S, f, f'{u}_FaultInst', f'{u}_Fault', f'{u}_Installed')
    alarm(S, f, f'{u}_FaultAlarm', f'{u}_FaultInst', 'Fault', 'Normal', 'Critical', f'{u} (floor {fl}) fan / VSD fault')
    AND(S, f, f'{u}_FilterInst', f'{u}_FilterDirty', f'{u}_Installed')
    alarm(S, f, f'{u}_FilterAlarm', f'{u}_FilterInst', 'Dirty', 'Normal', 'Warning', f'{u} (floor {fl}) filter dirty - maintenance')
    # V7.9 r4: floor AHU = VAV AHU (R9 office design). Commands are created here and driven by v79_office.ahu_control():
    # PICV on supply-air temperature (T&R reset), fan VSD on duct static pressure (T&R reset), OA damper on measured OA airflow.
    S.npoint(f, f'{u}_ValveCmd', 'Zero', 'pct', 1, kind='ao', note='FIELD AO: CHW pressure-independent control valve (PICV)')
    S.npoint(f, f'{u}_FanSpeedCmd', 'Zero', 'pct', 1, kind='ao', note='FIELD AO: supply fan VSD')
    S.npoint(f, f'{u}_OADamperCmd', 'Zero', 'pct', 0, kind='ao', note='FIELD AO: outdoor air damper (measured minimum OA, DCV)')
    CMP(S, f, f'{u}_ValveOpen', 'GreaterThan', f'{u}_ValveCmd', 'AirX_ValveFlowPct')
    AND(S, f, f'Gfx_{u}_FwdLogic', f'{u}_ValveOpen', 'Gfx_ChwMain_Fwd')
    S.bpoint(f, f'Gfx_{u}_Fwd', f'Gfx_{u}_FwdLogic', 'Flow', 'No flow', note='3D: chilled water flows to this floor AHU')
    return u, zt


def simulation(S, fl, u, zt):
    f = f'{AIR}/Simulation/Floors'
    DLY(S, f, f'Sim_{u}_RunFb', f'{u}_StartCmd', 3000, 1000); simlink(S, f'{u}_Status', f'Sim_{u}_RunFb')
    # first-order-ish zone response: target temperature from the valve, rate-limited
    if 'AirX_SimClock' not in S.comp:
        S.kc(f, 'AirX_SimClock', 'MultiVibrator', props=[('period', 'b:RelTime', '2000')], note='sample clock of the floor model')
        NOT(S, f, 'AirX_SimClockN', 'AirX_SimClock')
    S.kc(f, f'Sim_{u}_ValveA', 'NumericLatch', {'in': f'{u}_ValveCmd', 'clock': 'AirX_SimClock'})
    S.kc(f, f'Sim_{u}_ValveB', 'NumericLatch', {'in': f'Sim_{u}_ValveA', 'clock': 'AirX_SimClockN'}, note='two latches: no loop inside one scan')
    MATH(S, f, f'Sim_{u}_Cool', 'Multiply', f'Sim_{u}_ValveB', 'AirX_SimKPerPct')
    MATH(S, f, f'Sim_{u}_Dry', 'Multiply', f'Sim_{u}_ValveB', 'AirX_SimRHPerPct')
    for i, c in enumerate(zt):
        const(S, f'AirX_SimZoneOff{i}', [0.0, 0.6, -0.4, 0.9][i], 'C', 1)
        MATH(S, f, f'Sim_{c}_TTgt0', 'Subtract', 'AirX_SimWarm', f'Sim_{u}_Cool')
        MATH(S, f, f'Sim_{c}_TTgt', 'Add', f'Sim_{c}_TTgt0', f'AirX_SimZoneOff{i}')
        S.kc(f, f'Sim_{c}_T', 'NumericDelay', {'in': f'Sim_{c}_TTgt'}, props=[('maxStepSize', None, '0.3'), ('updateTime', 'b:RelTime', '1000')])
        simlink(S, f'ZoneTemperatureAvg_{c}', f'Sim_{c}_T')
        MATH(S, f, f'Sim_{c}_RH', 'Subtract', 'AirX_SimWetRH', f'Sim_{u}_Dry'); simlink(S, f'ZoneHumidityAvg_{c}', f'Sim_{c}_RH')
    MATH(S, f, f'Sim_{u}_SATc', 'Multiply', f'Sim_{u}_ValveB', 'AirX_SimSatPerPct')
    MATH(S, f, f'Sim_{u}_SAT', 'Subtract', 'AirX_SimWarm', f'Sim_{u}_SATc'); simlink(S, f'{u}_SAT', f'Sim_{u}_SAT')
    MATH(S, f, f'Sim_{u}_RH', 'Subtract', 'AirX_SimWetRH', f'Sim_{u}_Dry'); simlink(S, f'{u}_RA_RH', f'Sim_{u}_RH')


def simulation_co2(S, fl, u, zt):
    """V7.9 r3: zone CO2 follows occupancy and the OA damper; return air CO2 = average of the floor zones.
    OA damper -> CO2 -> damper is a loop: sampled through two latches (same as the valve) and rate limited."""
    f = f'{AIR}/Simulation/Floors'
    S.kc(f, f'Sim_{u}_OAA', 'NumericLatch', {'in': f'{u}_OADamperCmd', 'clock': 'AirX_SimClock'})
    S.kc(f, f'Sim_{u}_OAB', 'NumericLatch', {'in': f'Sim_{u}_OAA', 'clock': 'AirX_SimClockN'}, note='two latches: no loop inside one scan')
    SW(S, f, f'Sim_{u}_CO2Gen', f'{u}_SchOn', 'AirX_SimCO2Occ', 'AirX_SimCO2Unocc')
    MATH(S, f, f'Sim_{u}_CO2Purge', 'Multiply', f'Sim_{u}_OAB', 'AirX_SimCO2PerPct')
    co2 = []
    for i, c in enumerate(zt):
        const(S, f'AirX_SimCO2Off{i}', [0.0, 40.0, -30.0, 60.0][i], 'none', 0)
        MATH(S, f, f'Sim_{c}_CO2Tgt0', 'Subtract', f'Sim_{u}_CO2Gen', f'Sim_{u}_CO2Purge')
        MATH(S, f, f'Sim_{c}_CO2Tgt1', 'Add', f'Sim_{c}_CO2Tgt0', f'AirX_SimCO2Off{i}')
        MATH(S, f, f'Sim_{c}_CO2Tgt', 'Maximum', f'Sim_{c}_CO2Tgt1', 'AirX_SimCO2Unocc')
        RATE(S, f, f'Sim_{c}_CO2', f'Sim_{c}_CO2Tgt', 15.0, 1000)
        simlink(S, f'ZoneCO2_{c}', f'Sim_{c}_CO2'); co2.append(f'Sim_{c}_CO2')
    MATH(S, f, f'Sim_{u}_RACO2Sum', 'Add', *co2)
    MATH(S, f, f'Sim_{u}_RACO2', 'Divide', f'Sim_{u}_RACO2Sum', 'AirX_ZonesPerFloor'); simlink(S, f'{u}_RA_CO2', f'Sim_{u}_RACO2')


def build_air(S):
    C = f'{AIR}/Floors/Common'
    S.bparam('AirX_ManualOn', False, folder=C, t='Run (manual)', f='By schedule Sch_AHU', note='floor AHUs run regardless of the schedule')
    S.param('AirX_FanMinPct', 30.0, 'pct', folder=C, prec=0, note='supply fan VSD minimum speed (motor cooling / minimum airflow)')
    S.param('AirX_ValveFlowPct', 2.0, 'pct', folder=C, prec=0, note='3D: valve above this = water shown flowing')
    const(S, 'AirX_ZonesPerFloor', float(ZPF), 'none', 0)
    const(S, 'AirX_SimWarm', 29.0, 'C', 1); const(S, 'AirX_SimKPerPct', 0.06, 'none', 2)
    const(S, 'AirX_SimWetRH', 72.0, 'RH', 0); const(S, 'AirX_SimRHPerPct', 0.15, 'none', 2); const(S, 'AirX_SimSatPerPct', 0.17, 'none', 2)
    const(S, 'AirX_SimCO2Occ', 1150.0, 'none', 0, 'simulated zone CO2 (ppm) with occupants and the OA damper closed')
    const(S, 'AirX_SimCO2Unocc', 450.0, 'none', 0, 'simulated zone CO2 (ppm) outside the AHU schedule')
    const(S, 'AirX_SimCO2PerPct', 6.0, 'none', 1, 'simulated CO2 drop (ppm) per % OA damper')
    out = []
    for fl in FLOORS:
        u, zt = floor_ahu(S, fl); out.append((fl, u, zt))
    for fl, u, zt in out: simulation(S, fl, u, zt)
    zone_co2(S)
    for fl, u, zt in out: simulation_co2(S, fl, u, zt)
    S.log.append(('V7.9', 'AirSide/Floors', f'{len(FLOORS)} floor AHUs, {len(FLOORS) * ZPF} zones', 'see v79_air.py', '', ''))
    return out


def zone_co2(S):
    """V7.9 digital twin: CO2 per zone (every floor, floor 1 AirPlug zones included) + high CO2 alarm."""
    import re
    S.param('Zone_CO2AlarmHigh', 1000.0, 'none', folder=f'{AIR}/Common', prec=0, note='zone CO2 above this (ppm) for 15 min -> alarm')
    zs = sorted(n[len('ZoneTemperatureAvg_'):] for n in list(S.comp) if re.match(r'^ZoneTemperatureAvg_\d\d_\d{4}$', n))
    for i, c in enumerate(zs):
        zf = S.folder_of[f'ZoneTemperatureAvg_{c}']; co2 = f'ZoneCO2_{c}'
        ai(S, zf, co2, 600.0 + (i % 7) * 35, 'none', prec=0, note=f'FIELD AI: zone {c} CO2 (ppm)')
        CMP(S, zf, f'Z{c}_CO2High', 'GreaterThan', co2, 'Zone_CO2AlarmHigh')
        DLY(S, zf, f'Z{c}_CO2HighDly', f'Z{c}_CO2High', tm(900000, 10000))
        alarm(S, zf, f'Zone_{c}_CO2HighAlarm', f'Z{c}_CO2HighDly', 'High', 'Normal', 'Warning', f'Zone {c}: CO2 high - check outdoor air')
    S.log.append(('V7.9', 'AirSide', f'{len(zs)} zone CO2 points', 'digital twin', '', ''))


# Field IO: floor groups -> AirSide/FieldIO/Fnn  (hooked into v79_scale.field_io_exp through the folder test)
_scale = SC.scale


def scale(S):
    _scale(S)
    build_air(S)


SC.scale = scale
