# -*- coding: utf-8 -*-
"""V7.9: scalable equipment (user request 8 Oct 2026).
 * every chiller / CHW pump / CDW pump / cooling tower slot 01..06 and every spare sensor has <unit>_Installed
   (01-02 = existing units, Installed off = treated like maintenance; 03-06 = expansion units, built from one template)
 * Expansion/Supervisor adds expansion units when the base pair cannot carry the load or a base unit is missing:
     chillers  target = deficit (base units asked for but not available) + step-add (all running, CHWS high or load high)
     pumps/CT  target = chillers that need water - healthy base units  (one pump / tower per chiller, headered)
   first available slot is used (03 -> 06); a failed / maintenance / not-installed slot is skipped automatically
 * equipment register (Excel) -> Installed defaults, descriptions, protocols, sensor ranges; Field IO / point list / 3D map follow
"""
import json, os
import eqreg
import make_v6 as M6
import make_v7 as M7
import v77_fieldcx as FCX
import v78_improve as IMP
from make_v7 import AND, OR, NOT, DLY, SW, MATH, CMP, sealin, const, PULSE, ai, di, simlink

T, F = 'ConstantTrue', 'ConstantFalse'
tm, alarm = IMP.tm, IMP.alarm
REG = eqreg.default()        # replaced by make_v79 with eqreg.load(<ALT_V79_Equipment_Register.xlsx>)


def R():
    return REG
SLOTS = range(3, 7)
EX = 'Expansion'
SUP = f'{EX}/Supervisor'


def inst(slot, base):
    r = next((x for x in REG.get('Equipment', []) if x.get('Slot') == slot), None)
    return eqreg.installed(r) if r else base


def relink_consumers(S, old, new):
    """every link that reads `old` reads `new` instead (except the block that builds `new`)."""
    h_old, h_new = 'h:' + S.handle(old), 'h:' + S.handle(new)
    n = 0
    for name, el in S.comp.items():
        if name == new: continue
        for L in el:
            if L.get('t') == 'b:Link' and M6.child(L, 'sourceOrd').get('v') == h_old:
                M6.child(L, 'sourceOrd').set('v', h_new); n += 1
    S.log.append(('V7.9', 'RELINK', old, new, str(n), ''))


def count(S, f, name, bools):
    """number of true inputs (NumericSwitch 1/0 + Add tree)."""
    nums = []
    for b in bools:
        SW(S, f, f'{name}_{b}', b, 'One', 'Zero'); nums.append(f'{name}_{b}')
    return add_tree(S, f, name, nums)


def add_tree(S, f, name, nums):
    lvl, i = list(nums), 0
    while len(lvl) > 4:
        nxt = []
        for j in range(0, len(lvl), 4):
            i += 1; MATH(S, f, f'{name}_S{i}', 'Add', *lvl[j:j + 4]); nxt.append(f'{name}_S{i}')
        lvl = nxt
    MATH(S, f, name, 'Add', *lvl)
    return name


def common_unit(S, u, f, desc, base):
    S.bparam(f'{u}_Installed', inst(u, base), folder=f, t='Installed', f='Not installed',
             note=f'V7.9: {desc}. Off = unit does not exist / removed: never selected, alarms suppressed, hidden in 3D')
    S.bparam(f'{u}_Maintenance', False, folder=f, t='Maintenance (out of service)', f='In service', note='unit is not selected while in maintenance')
    PULSE(S, f, f'{u}_ResetFire', note='Px reset button')
    OR(S, f, f'{u}_ResetAny', f'{u}_ResetFire', F)   # inB = FO_Reset (plant reset), linked in post()


def proof_fail(S, f, u, cmd, fb, ms_site, ms_fpt, text):
    NOT(S, f, f'{u}_NoProof', fb)
    AND(S, f, f'{u}_ProofMissing', F, f'{u}_NoProof')   # inA = start command, linked in the logic step
    DLY(S, f, f'{u}_ProofFailDly', f'{u}_ProofMissing', tm(ms_site, ms_fpt))
    sealin(S, f, f'{u}_FailLatch', f'{u}_ProofFailDly', f'{u}_ResetAny')
    alarm(S, f, f'{u}_StartFailAlarm', f'{u}_FailLatch', 'Failed', 'Normal', 'Critical', text)


def avail(S, f, u):
    NOT(S, f, f'{u}_NotMaint', f'{u}_Maintenance'); NOT(S, f, f'{u}_NotFault', f'{u}Fault'); NOT(S, f, f'{u}_NotFailed', f'{u}_FailLatch')
    AND(S, f, f'{u}_Avail', f'{u}_Installed', f'{u}_NotMaint', f'{u}_NotFault', f'{u}_NotFailed')
    AND(S, f, f'{u}_FaultInst', f'{u}Fault', f'{u}_Installed')
    alarm(S, f, f'{u}_FaultAlarm', f'{u}_FaultInst', 'Fault', 'Normal', 'Critical', f'{u} fault (unit fault contact)')


def uncommanded(S, f, u, run, cmd):
    NOT(S, f, f'{u}_NoCmd', cmd); AND(S, f, f'{u}_RunNoCmd', run, f'{u}_NoCmd', f'{u}_Installed')
    DLY(S, f, f'{u}_RunNoCmdDly', f'{u}_RunNoCmd', tm(120000, 20000))
    alarm(S, f, f'{u}_UncommandedRunAlarm', f'{u}_RunNoCmdDly', 'Running', 'Normal', 'Warning', f'{u} is running without a command')


def pos(S, f, name, fb):
    SW(S, f, name + 'Calc', fb, 'HundredPct', 'Zero')
    S.npoint(f, name, name + 'Calc', 'pct', 0, note='3D: valve position')


# ------------------------------------------------------------------ unit templates (points first, logic after the supervisor)
def chiller_points(S, n):
    u = f'CH{n:02d}'; f = f'{EX}/{u}'
    common_unit(S, u, f, f'expansion chiller {u}', False)
    di(S, f, f'{u}RunProof', False, 'Running', 'Stopped', note='FIELD DI: compressor running (OEM status)')
    di(S, f, f'{u}Fault', False, 'Fault', 'Normal', note='FIELD DI: chiller general fault')
    di(S, f, f'{u}_ChwIsoFb', False, 'Open', 'Closed', note='FIELD DI: CHW isolation valve open limit')
    di(S, f, f'{u}_CdwIsoFb', False, 'Open', 'Closed', note='FIELD DI: CDW isolation valve open limit')
    di(S, f, f'{u}_ChwFlowSw', False, 'Flow', 'No flow', note='FIELD DI: evaporator flow switch')
    di(S, f, f'{u}_CdwFlowSw', False, 'Flow', 'No flow', note='FIELD DI: condenser flow switch')
    ai(S, f, f'{u}LoadPct', 0.0, 'pct', 0, note='FIELD AI: chiller load (OEM)')
    ai(S, f, f'{u}_ChwSupplyTemp', 12.0, 'C', 1, note='FIELD AI: chiller leaving CHW temperature')
    ai(S, f, f'{u}_kW', 0.0, 'kW', 1, note='FIELD AI: chiller power (meter)')
    proof_fail(S, f, u, f'{u}StartCmdLogic', f'{u}RunProof', 180000, 15000, f'{u} did not prove running after the start command')
    avail(S, f, u)
    AND(S, f, f'{u}_Running', f'{u}RunProof', f'{u}_Installed')
    SW(S, f, f'{u}_RunNum', f'{u}_Running', 'One', 'Zero')
    SW(S, f, f'{u}_LoadUse', f'{u}_Running', f'{u}LoadPct', 'Zero')
    SW(S, f, f'{u}_NeedNum', F, 'One', 'Zero')     # inSwitch = valve command (logic step)
    S.bpoint(f, f'{u}ValveOpenCmd', F, 'Open', 'Close', kind='do', note='FIELD DO (logic linked in post)')
    S.bpoint(f, f'{u}CdwValveOpenCmd', F, 'Open', 'Close', kind='do', note='FIELD DO (logic linked in post)')
    S.bpoint(f, f'{u}StartCmd', F, 'Start', 'Stop', kind='do', note='FIELD DO (logic linked in post)')
    sf = 'Simulation/Expansion'
    DLY(S, sf, f'Sim_{u}_RunFb', f'{u}StartCmd', 3000, 1000); simlink(S, f'{u}RunProof', f'Sim_{u}_RunFb')
    DLY(S, sf, f'Sim_{u}_ValveFb', f'{u}ValveOpenCmd', 2000, 2000)
    simlink(S, f'{u}_ChwIsoFb', f'Sim_{u}_ValveFb'); simlink(S, f'{u}_CdwIsoFb', f'Sim_{u}_ValveFb')
    AND(S, sf, f'Sim_{u}_ChwFlowFb', f'Sim_{u}_ValveFb', 'Sim_AnyCHP_RunFb'); simlink(S, f'{u}_ChwFlowSw', f'Sim_{u}_ChwFlowFb')
    AND(S, sf, f'Sim_{u}_CdwFlowFb', f'Sim_{u}_ValveFb', 'Sim_AnyCDP_RunFb'); simlink(S, f'{u}_CdwFlowSw', f'Sim_{u}_CdwFlowFb')
    SW(S, sf, f'Sim_{u}_Load', f'Sim_{u}_RunFb', 'CHX_SimLoadPct', 'Zero'); simlink(S, f'{u}LoadPct', f'Sim_{u}_Load')
    SW(S, sf, f'Sim_{u}_Lwt', f'Sim_{u}_RunFb', 'CHWS', 'CHWR'); simlink(S, f'{u}_ChwSupplyTemp', f'Sim_{u}_Lwt')
    MATH(S, sf, f'Sim_{u}_kWCalc', 'Multiply', f'Sim_{u}_Load', 'CHX_SimKwPerPct'); simlink(S, f'{u}_kW', f'Sim_{u}_kWCalc')
    chiller_detail(S, u, f, sf)


def pump_points(S, k, n):
    u = f'{k}{n:02d}'; f = f'{EX}/{u}'
    common_unit(S, u, f, f'expansion {"chilled" if k == "CHP" else "condenser"} water pump {u}', False)
    di(S, f, f'{u}RunProof', False, 'Running', 'Stopped', note='FIELD DI: VSD run status')
    di(S, f, f'{u}Fault', False, 'Fault', 'Normal', note='FIELD DI: VSD fault')
    di(S, f, f'{u}_MVFb', False, 'Open', 'Closed', note='FIELD DI: discharge valve open limit')
    proof_fail(S, f, u, f'{u}StartCmdLogic', f'{u}RunProof', 60000, 10000, f'{u} did not prove running after the start command')
    avail(S, f, u)
    S.bpoint(f, f'{u}_MVCmd', F, 'Open', 'Close', kind='do', note='FIELD DO (logic linked in post)')
    S.bpoint(f, f'{u}StartCmd', F, 'Start', 'Stop', kind='do', note='FIELD DO (logic linked in post)')
    S.npoint(f, f'{u}SpeedCmd', 'Zero', 'pct', 1, kind='ao', note='FIELD AO (logic linked in post)')
    sf = 'Simulation/Expansion'
    DLY(S, sf, f'Sim_{u}_RunFb', f'{u}StartCmd', 2000, 1000); simlink(S, f'{u}RunProof', f'Sim_{u}_RunFb')
    DLY(S, sf, f'Sim_{u}_MVFb', f'{u}_MVCmd', 2000, 2000); simlink(S, f'{u}_MVFb', f'Sim_{u}_MVFb')
    pump_detail(S, k, u, f, sf)


def tower_points(S, n):
    u = f'CT{n:02d}'; f = f'{EX}/{u}'
    common_unit(S, u, f, f'expansion cooling tower {u} (1 cell, VSD fan)', False)
    di(S, f, f'{u}RunProof', False, 'Running', 'Stopped', note='FIELD DI: fan VSD run status')
    di(S, f, f'{u}Fault', False, 'Fault', 'Normal', note='FIELD DI: fan VSD fault / vibration')
    di(S, f, f'{u}_ValveFb', False, 'Open', 'Closed', note='FIELD DI: inlet + outlet valves open limits (series)')
    proof_fail(S, f, u, f'{u}StartCmdLogic', f'{u}RunProof', 60000, 10000, f'{u} fan did not prove running after the start command')
    avail(S, f, u)
    S.bpoint(f, f'{u}_ValveCmd', F, 'Open', 'Close', kind='do', note='FIELD DO (logic linked in post)')
    S.bpoint(f, f'{u}StartCmd', F, 'Start', 'Stop', kind='do', note='FIELD DO (logic linked in post)')
    S.npoint(f, f'{u}SpeedCmd', 'Zero', 'pct', 1, kind='ao', note='FIELD AO (logic linked in post)')
    sf = 'Simulation/Expansion'
    DLY(S, sf, f'Sim_{u}_RunFb', f'{u}StartCmd', 2000, 1000); simlink(S, f'{u}RunProof', f'Sim_{u}_RunFb')
    DLY(S, sf, f'Sim_{u}_ValveFb', f'{u}_ValveCmd', 2000, 2000); simlink(S, f'{u}_ValveFb', f'Sim_{u}_ValveFb')
    tower_detail(S, u, f, sf)


# ------------------------------------------------------------------ V7.9 r2: full field detail for slots 03-06 (same names as slots 01-02)
def _k(S):
    const(S, 'X_HzPerPct', 0.5, 'none', 2, 'VSD output Hz per % speed (50 Hz at 100 %)')
    const(S, 'CHX_SimRtPerPct', 3.34, 'none', 2, 'simulated RT per % load (334 TR chiller)')
    const(S, 'CHX_SimChwFlow', 480.0, 'none', 0, 'simulated evaporator flow gpm')
    const(S, 'CHX_SimCdwFlow', 560.0, 'none', 0, 'simulated condenser flow gpm')
    for k, kw, dp, suc in (('CHP', 1.85e-5, 3.3e-4, 1.96), ('CDP', 2.2e-5, 3.1e-4, 0.60)):
        const(S, f'{k}X_SimKwK', kw, 'none', 7, f'{k} kW = k x speed^3')
        const(S, f'{k}X_SimDpK', dp, 'none', 6, f'{k} dP bar = k x speed^2')
        const(S, f'{k}X_SimSuction', suc, 'none', 2, f'{k} suction pressure bar')
    const(S, 'CTX_SimKwK', 5.5e-6, 'none', 7, 'CT fan kW = k x speed^3')
    const(S, 'CTX_SimBasin', 68.0, 'none', 0, 'simulated basin level %')


def chiller_detail(S, u, f, sf):
    _k(S)
    di(S, f, f'{u}InAuto', True, 'Remote', 'Local', note='FIELD DI: chiller in remote / auto (OEM)')
    ai(S, f, f'{u}_ChwReturnTemp', 12.0, 'C', 1, note='FIELD AI: chiller entering CHW temperature')
    ai(S, f, f'{u}_CdwEnteringTemp', 30.0, 'C', 1, note='FIELD AI: condenser entering water temperature')
    ai(S, f, f'{u}_CdwLeavingTemp', 30.0, 'C', 1, note='FIELD AI: condenser leaving water temperature')
    ai(S, f, f'{u}_ChwFlow', 0.0, 'none', 0, note='FIELD AI: evaporator flow gpm')
    ai(S, f, f'{u}_CdwFlow', 0.0, 'none', 0, note='FIELD AI: condenser flow gpm')
    simlink(S, f'{u}_ChwReturnTemp', 'CHWR'); simlink(S, f'{u}_CdwEnteringTemp', 'CDS')
    SW(S, sf, f'Sim_{u}_Cdl', f'Sim_{u}_RunFb', 'CDR', 'CDS'); simlink(S, f'{u}_CdwLeavingTemp', f'Sim_{u}_Cdl')
    SW(S, sf, f'Sim_{u}_ChwFlowV', f'Sim_{u}_ChwFlowFb', 'CHX_SimChwFlow', 'Zero'); simlink(S, f'{u}_ChwFlow', f'Sim_{u}_ChwFlowV')
    SW(S, sf, f'Sim_{u}_CdwFlowV', f'Sim_{u}_CdwFlowFb', 'CHX_SimCdwFlow', 'Zero'); simlink(S, f'{u}_CdwFlow', f'Sim_{u}_CdwFlowV')
    MATH(S, f, f'{u}RTCalc', 'Multiply', f'{u}LoadPct', 'CHX_SimRtPerPct'); S.npoint(f, f'{u}_RT', f'{u}RTCalc', 'none', 1, note='chiller RT (calc)')
    MATH(S, f, f'{u}KwPerRTDiv', 'Divide', f'{u}_kW', f'{u}_RT'); SW(S, f, f'{u}KwPerRTCalc', f'{u}RunProof', f'{u}KwPerRTDiv', 'Zero')
    S.npoint(f, f'{u}_kW_per_RT', f'{u}KwPerRTCalc', 'none', 3, note='chiller kW/RT (calc)')
    MATH(S, f, f'{u}LiftCalc', 'Subtract', f'{u}_CdwLeavingTemp', f'{u}_ChwSupplyTemp'); S.npoint(f, f'{u}_Lift', f'{u}LiftCalc', 'C', 1, note='lift (calc)')


def pump_detail(S, k, u, f, sf):
    _k(S)
    di(S, f, f'{u}InAuto', True, 'Auto', 'Hand', note='FIELD DI: VSD in auto')
    ai(S, f, f'{u}_SpeedFeedbackHz', 0.0, 'none', 1, note='FIELD AI: VSD output Hz')
    ai(S, f, f'{u}_kW', 0.0, 'kW', 1, note='FIELD AI: VSD power')
    ai(S, f, f'{u}_SuctionPressure', 0.0, 'none', 2, note='FIELD AI: suction pressure bar')
    ai(S, f, f'{u}_DischargePressure', 0.0, 'none', 2, note='FIELD AI: discharge pressure bar')
    MATH(S, sf, f'Sim_{u}_Hz', 'Multiply', f'{u}SpeedCmd', 'X_HzPerPct'); simlink(S, f'{u}_SpeedFeedbackHz', f'Sim_{u}_Hz')
    MATH(S, sf, f'Sim_{u}_kWv', 'Multiply', f'{u}SpeedCmd', f'{u}SpeedCmd', f'{u}SpeedCmd', f'{k}X_SimKwK'); simlink(S, f'{u}_kW', f'Sim_{u}_kWv')
    simlink(S, f'{u}_SuctionPressure', f'{k}X_SimSuction')
    MATH(S, sf, f'Sim_{u}_Dp', 'Multiply', f'{u}SpeedCmd', f'{u}SpeedCmd', f'{k}X_SimDpK')
    MATH(S, sf, f'Sim_{u}_Dis', 'Add', f'{k}X_SimSuction', f'Sim_{u}_Dp'); simlink(S, f'{u}_DischargePressure', f'Sim_{u}_Dis')
    MATH(S, f, f'{u}DPCalc', 'Subtract', f'{u}_DischargePressure', f'{u}_SuctionPressure'); S.npoint(f, f'{u}_DiffPressure', f'{u}DPCalc', 'none', 2, note='pump dP bar (calc)')


def tower_detail(S, u, f, sf):
    _k(S)
    di(S, f, f'{u}InAuto', True, 'Auto', 'Hand', note='FIELD DI: fan VSD in auto')
    ai(S, f, f'{u}_FanSpeedHz', 0.0, 'none', 1, note='FIELD AI: fan VSD output Hz')
    ai(S, f, f'{u}_kW', 0.0, 'kW', 1, note='FIELD AI: fan VSD power')
    ai(S, f, f'{u}_InletTemp', 30.0, 'C', 1, note='FIELD AI: tower water in')
    ai(S, f, f'{u}_OutletTemp', 30.0, 'C', 1, note='FIELD AI: tower water out')
    ai(S, f, f'{u}_BasinLevel', 68.0, 'pct', 0, note='FIELD AI: basin level')
    MATH(S, sf, f'Sim_{u}_Hz', 'Multiply', f'{u}SpeedCmd', 'X_HzPerPct'); simlink(S, f'{u}_FanSpeedHz', f'Sim_{u}_Hz')
    MATH(S, sf, f'Sim_{u}_kWv', 'Multiply', f'{u}SpeedCmd', f'{u}SpeedCmd', f'{u}SpeedCmd', 'CTX_SimKwK'); simlink(S, f'{u}_kW', f'Sim_{u}_kWv')
    SW(S, sf, f'Sim_{u}_In', f'Sim_{u}_ValveFb', 'CDR', 'CDS'); simlink(S, f'{u}_InletTemp', f'Sim_{u}_In')
    simlink(S, f'{u}_OutletTemp', 'CDS'); simlink(S, f'{u}_BasinLevel', 'CTX_SimBasin')


def chiller_logic(S, n):
    u = f'CH{n:02d}'; f = f'{EX}/{u}'; req = f'CHX_Req{n:02d}'
    DLY(S, f, f'{u}_ReqHold', req, 0, tm(600000, 10000), note='minimum run 10 min (site)')
    NOT(S, f, f'{u}_NotInhibit', 'Plant_ChillerInhibit')
    AND(S, f, f'{u}_RunReq', f'{u}_ReqHold', f'{u}_Avail', 'PlantPermissive', f'{u}_NotInhibit')
    DLY(S, f, f'{u}_ValveLogic', f'{u}_RunReq', 0, tm(300000, 10000), note='valves stay open for the post-run time')
    S.rewire(f'{u}ValveOpenCmd', 'in16', f'{u}_ValveLogic', F)
    S.rewire(f'{u}CdwValveOpenCmd', 'in16', f'{u}_ValveLogic', F)
    AND(S, f, f'{u}_ValvesOpen', f'{u}_ChwIsoFb', f'{u}_CdwIsoFb')
    AND(S, f, f'{u}StartCmdLogic', f'{u}_RunReq', f'{u}_ValvesOpen', f'{u}_ChwFlowSw', f'{u}_CdwFlowSw')
    for side in ('Chw', 'Cdw'):
        NOT(S, f, f'{u}_No{side}Flow', f'{u}_{side}FlowSw'); AND(S, f, f'{u}_{side}FlowMissing', f'{u}_ValvesOpen', f'{u}_No{side}Flow', f'{u}_RunReq')
        DLY(S, f, f'{u}_{side}FlowMissingDly', f'{u}_{side}FlowMissing', tm(60000, 10000))
        alarm(S, f, f'{u}_{side}FailAlarm', f'{u}_{side}FlowMissingDly', 'No flow', 'Normal', 'Critical',
              f'{u}: no {"chilled" if side == "Chw" else "condenser"} water flow with the valve open - chiller not started')
    S.rewire(f'{u}StartCmd', 'in16', f'{u}StartCmdLogic', F)
    S.rewire(f'{u}_ProofMissing', 'inA', f'{u}StartCmdLogic', F)
    uncommanded(S, f, u, f'{u}RunProof', f'{u}StartCmd')
    S.rewire(f'{u}_NeedNum', 'inSwitch', f'{u}_ValveLogic', F)
    pos(S, f, f'Gfx_{u}_ChwIso_Pos', f'{u}_ChwIsoFb'); pos(S, f, f'Gfx_{u}_CdwIso_Pos', f'{u}_CdwIsoFb')
    AND(S, f, f'Gfx_{u}EvapLogic', f'{u}_ChwIsoFb', 'Gfx_ChwMain_Fwd'); S.bpoint(f, f'Gfx_{u}Evap_Fwd', f'Gfx_{u}EvapLogic', 'Flow', 'No flow')
    AND(S, f, f'Gfx_{u}CondLogic', f'{u}_CdwIsoFb', 'Gfx_CdwTotal_Fwd'); S.bpoint(f, f'Gfx_{u}Cond_Fwd', f'Gfx_{u}CondLogic', 'Flow', 'No flow')
    # simulation


def pump_logic(S, k, n):
    u = f'{k}{n:02d}'; f = f'{EX}/{u}'; req = f'{k}X_Req{n:02d}'
    AND(S, f, f'{u}_RunReq', req, f'{u}_Avail', 'PlantPermissive')
    DLY(S, f, f'{u}_MVLogic', f'{u}_RunReq', 0, tm(30000, 3000), note='valve closes after the pump stops')
    S.rewire(f'{u}_MVCmd', 'in16', f'{u}_MVLogic', F)
    AND(S, f, f'{u}StartCmdLogic', f'{u}_RunReq', f'{u}_MVFb')
    S.rewire(f'{u}StartCmd', 'in16', f'{u}StartCmdLogic', F)
    S.rewire(f'{u}_ProofMissing', 'inA', f'{u}StartCmdLogic', F)
    SW(S, f, f'{u}_SpeedSel', f'{u}StartCmd', f'{k}X_Speed', 'Zero')
    S.rewire(f'{u}SpeedCmd', 'in16', f'{u}_SpeedSel', 'Zero')
    uncommanded(S, f, u, f'{u}RunProof', f'{u}StartCmd')
    AND(S, f, f'{u}_Running', f'{u}RunProof', f'{u}_Installed')
    pos(S, f, f'Gfx_{u}_MV_Pos', f'{u}_MVFb')
    AND(S, f, f'Gfx_{u}_FwdLogic', f'{u}_Running', f'{u}_MVFb'); S.bpoint(f, f'Gfx_{u}_Fwd', f'Gfx_{u}_FwdLogic', 'Flow', 'No flow')


def tower_logic(S, n):
    u = f'CT{n:02d}'; f = f'{EX}/{u}'; req = f'CTX_Req{n:02d}'
    AND(S, f, f'{u}_RunReq', req, f'{u}_Avail', 'PlantPermissive')
    DLY(S, f, f'{u}_ValveLogic', f'{u}_RunReq', 0, tm(300000, 10000))
    S.rewire(f'{u}_ValveCmd', 'in16', f'{u}_ValveLogic', F)
    AND(S, f, f'{u}StartCmdLogic', f'{u}_RunReq', f'{u}_ValveFb')
    S.rewire(f'{u}StartCmd', 'in16', f'{u}StartCmdLogic', F)
    S.rewire(f'{u}_ProofMissing', 'inA', f'{u}StartCmdLogic', F)
    SW(S, f, f'{u}_SpeedSel', f'{u}StartCmd', 'CT_LeadSpeed', 'Zero')
    S.rewire(f'{u}SpeedCmd', 'in16', f'{u}_SpeedSel', 'Zero')
    uncommanded(S, f, u, f'{u}RunProof', f'{u}StartCmd')
    pos(S, f, f'Gfx_{u}_Valve_Pos', f'{u}_ValveFb')
    AND(S, f, f'Gfx_{u}_FwdLogic', f'{u}_ValveFb', 'Gfx_CdwTotal_Fwd'); S.bpoint(f, f'Gfx_{u}_Fwd', f'Gfx_{u}_FwdLogic', 'Flow', 'No flow')


def sensor(S, r):
    u = r['Slot']; f = f'{EX}/Sensors/{u}'
    kind = r.get('Kind') or 'Generic'; dflt = eqreg.SENSOR_KINDS.get(kind, eqreg.SENSOR_KINDS['Generic'])
    num = lambda k, d: float(r[k]) if r.get(k) not in (None, '') else d
    unit = dflt[0]; vlo, vhi, alo, ahi, sim = num('ValidLo', dflt[1]), num('ValidHi', dflt[2]), num('AlarmLo', dflt[3]), num('AlarmHi', dflt[4]), num('SimValue', dflt[5])
    r = dict(r, desc=f"{r.get('Tag') or u} {r.get('Description') or ''}".strip())
    S.bparam(f'{u}_Installed', eqreg.installed(r), folder=f, t='Installed', f='Spare',
             note=f'V7.9 sensor slot: {r["desc"]} ({kind}) - switch on when the sensor is wired')
    ai(S, f, f'{u}_Value', sim, unit, 1, note=f'FIELD AI: {r.get("desc", "spare sensor")}')
    S.param(f'{u}_SimValue', sim, unit, folder='Simulation/Expansion', prec=1, note='simulated value')
    simlink(S, f'{u}_Value', f'{u}_SimValue')
    for nm, v in (('ValidLo', vlo), ('ValidHi', vhi), ('AlarmLo', alo), ('AlarmHi', ahi)):
        S.param(f'{u}_{nm}', v, unit, folder=f, prec=1, note={'ValidLo': 'below = sensor fault', 'ValidHi': 'above = sensor fault',
                                                              'AlarmLo': 'low alarm', 'AlarmHi': 'high alarm'}[nm])
    CMP(S, f, f'{u}_AboveVLo', 'GreaterThanEqual', f'{u}_Value', f'{u}_ValidLo'); CMP(S, f, f'{u}_BelowVHi', 'LessThanEqual', f'{u}_Value', f'{u}_ValidHi')
    AND(S, f, f'{u}_Valid', f'{u}_AboveVLo', f'{u}_BelowVHi', f'{u}_Installed')
    NOT(S, f, f'{u}_NotValid', f'{u}_Valid'); AND(S, f, f'{u}_BadInst', f'{u}_NotValid', f'{u}_Installed')
    DLY(S, f, f'{u}_BadDly', f'{u}_BadInst', tm(60000, 5000))
    alarm(S, f, f'{u}_SensorFaultAlarm', f'{u}_BadDly', 'Sensor fault', 'Normal', 'Warning', f'{u} {r.get("desc", "")}: value outside the sensor range (open / short / not wired)')
    CMP(S, f, f'{u}_Hi', 'GreaterThan', f'{u}_Value', f'{u}_AlarmHi'); AND(S, f, f'{u}_HiV', f'{u}_Hi', f'{u}_Valid')
    DLY(S, f, f'{u}_HiDly', f'{u}_HiV', tm(300000, 5000))
    alarm(S, f, f'{u}_HighAlarm', f'{u}_HiDly', 'High', 'Normal', 'Warning', f'{u} {r.get("desc", "")}: high')
    CMP(S, f, f'{u}_Lo', 'LessThan', f'{u}_Value', f'{u}_AlarmLo'); AND(S, f, f'{u}_LoV', f'{u}_Lo', f'{u}_Valid')
    DLY(S, f, f'{u}_LoDly', f'{u}_LoV', tm(300000, 5000))
    alarm(S, f, f'{u}_LowAlarm', f'{u}_LoDly', 'Low', 'Normal', 'Warning', f'{u} {r.get("desc", "")}: low')


# ------------------------------------------------------------------ supervisor
def ranks(S, k, target, units):
    """slot request: available AND (number of available slots up to this one) <= target."""
    prev = None
    for n in SLOTS:
        u = f'{units}{n:02d}'
        SW(S, SUP, f'{k}X_Av{n:02d}', f'{u}_Avail', 'One', 'Zero')
        rk = f'{k}X_Rank{n:02d}'
        if prev: MATH(S, SUP, rk, 'Add', prev, f'{k}X_Av{n:02d}')
        else: MATH(S, SUP, rk, 'Add', f'{k}X_Av{n:02d}')
        CMP(S, SUP, f'{k}X_InTarget{n:02d}', 'LessThanEqual', rk, target)
        AND(S, SUP, f'{k}X_Req{n:02d}', f'{u}_Avail', f'{k}X_InTarget{n:02d}', 'PlantPermissive', 'CHX_Enable')
        prev = rk
    return prev


def supervisor(S):
    P = 'Parameters/Expansion'
    S.param('CHX_UpLoadPct', 90.0, 'pct', folder=P, prec=0, note='V7.9: add an expansion chiller when the average load of the running chillers is above this')
    S.param('CHX_DownLoadPct', 75.0, 'pct', folder=P, prec=0, note='remove one when the others could carry the load below this average')
    S.param('CDPX_MinSpeed', 60.0, 'pct', folder=P, prec=0, note='expansion CDP speed when no base CDP runs')
    S.bparam('CHX_Enable', True, folder=P, t='Expansion slots in use', f='Off (V7.8 behaviour)', note='V7.9 master switch: off = slots 03-06 never run')
    # ---- chillers
    count(S, SUP, 'CHX_BaseAvail', ['CH01TrainHealthy', 'CH02TrainHealthy'])
    MATH(S, SUP, 'CHX_DeficitRaw', 'Subtract', 'PlantStage', 'CHX_BaseAvail')
    MATH(S, SUP, 'CHX_Deficit', 'Maximum', 'CHX_DeficitRaw', 'Zero')
    add_tree(S, SUP, 'CHX_RunCount', [f'CH{n:02d}_RunNum' for n in SLOTS])
    add_tree(S, SUP, 'CHX_LoadSum', [f'CH{n:02d}_LoadUse' for n in SLOTS])
    count(S, SUP, 'CHX_AvailCount', [f'CH{n:02d}_Avail' for n in SLOTS])
    MATH(S, SUP, 'CHX_TotalRun', 'Add', 'CH_RunNum', 'CHX_RunCount')
    MATH(S, SUP, 'CHX_TotalLoad', 'Add', 'ChillerLoadSum', 'CHX_LoadSum')
    MATH(S, SUP, 'CHX_RunDiv', 'Maximum', 'CHX_TotalRun', 'One')
    MATH(S, SUP, 'CHX_AvgLoad', 'Divide', 'CHX_TotalLoad', 'CHX_RunDiv')
    S.npoint(SUP, 'CHX_AverageLoad', 'CHX_AvgLoad', 'pct', 1, note='average load of all running chillers')
    MATH(S, SUP, 'CHX_RunLess1', 'Subtract', 'CHX_TotalRun', 'One'); MATH(S, SUP, 'CHX_RunLess1Div', 'Maximum', 'CHX_RunLess1', 'One')
    MATH(S, SUP, 'CHX_LoadIfOneLess', 'Divide', 'CHX_TotalLoad', 'CHX_RunLess1Div')
    # step register: latch samples next value on any step event
    S.kc(SUP, 'CHX_StepLatch', 'NumericLatch', {'in': 'Zero', 'clock': F}, note='extra chillers added for load (in / clock linked below)')
    S.npoint(SUP, 'CHX_StageAdd', 'CHX_StepLatch', 'none', 0, note='expansion chillers added for load (0-4)')
    MATH(S, SUP, 'CHX_Target', 'Add', 'CHX_Deficit', 'CHX_StageAdd')
    CMP(S, SUP, 'CHX_AllRunning', 'GreaterThanEqual', 'CHX_RunCount', 'CHX_Target')
    CMP(S, SUP, 'CHX_LoadHigh', 'GreaterThanEqual', 'CHX_AvgLoad', 'CHX_UpLoadPct')
    OR(S, SUP, 'CHX_NeedMore', 'CHX_LoadHigh', 'ChwsAboveStageUpLimit')
    CMP(S, SUP, 'CHX_RoomToAdd', 'LessThan', 'CHX_Target', 'CHX_AvailCount')
    AND(S, SUP, 'CHX_UpCond', 'PlantRunRequest', 'Stage2Request', 'CHX_AllRunning', 'CHX_NeedMore')
    AND(S, SUP, 'CHX_UpCond2', 'CHX_UpCond', 'CHX_RoomToAdd')
    DLY(S, SUP, 'CHX_UpDly', 'CHX_UpCond2', tm(600000, 15000), note='site 10 min / test 15 s')
    CMP(S, SUP, 'CHX_HasStep', 'GreaterThanEqual', 'CHX_StageAdd', 'One')
    CMP(S, SUP, 'CHX_LightLoad', 'LessThan', 'CHX_LoadIfOneLess', 'CHX_DownLoadPct')
    CMP(S, SUP, 'CHX_NotOver', 'LessThanEqual', 'CHX_RunCount', 'CHX_Target')
    AND(S, SUP, 'CHX_DownCond', 'CHX_HasStep', 'CHX_LightLoad', 'Stg_DownChwsOk', 'CHX_NotOver')
    DLY(S, SUP, 'CHX_DownDly', 'CHX_DownCond', tm(900000, 20000), note='site 15 min / test 20 s')
    NOT(S, SUP, 'CHX_PlantOff', 'PlantRunRequest')
    SW(S, SUP, 'CHX_UpN', 'CHX_UpDly', 'One', 'Zero'); SW(S, SUP, 'CHX_DownN', 'CHX_DownDly', 'One', 'Zero')
    MATH(S, SUP, 'CHX_StepPlus', 'Add', 'CHX_StageAdd', 'CHX_UpN')
    MATH(S, SUP, 'CHX_StepCalc', 'Subtract', 'CHX_StepPlus', 'CHX_DownN')
    S.kc(SUP, 'CHX_StepLim', 'Limiter', {'inA': 'CHX_StepCalc'}, props=[('inMin', None, '0.0'), ('inMax', None, '4.0')])
    SW(S, SUP, 'CHX_StepIn', 'CHX_PlantOff', 'Zero', 'CHX_StepLim')
    OR(S, SUP, 'CHX_StepClock', 'CHX_UpDly', 'CHX_DownDly', 'CHX_PlantOff')
    S.rewire('CHX_StepLatch', 'in', 'CHX_StepIn', 'Zero'); S.rewire('CHX_StepLatch', 'clock', 'CHX_StepClock', F)
    NOT(S, SUP, 'CHX_StepClockN', 'CHX_StepClock')
    S.kc(SUP, 'CHX_StepPrev', 'NumericLatch', {'in': 'CHX_StepLatch', 'clock': 'CHX_StepClockN'},
         note='copy taken on the other clock edge: one step per event, no loop inside a scan')
    S.rewire('CHX_StepPlus', 'inA', 'CHX_StepPrev', 'CHX_StageAdd')
    S.npoint(SUP, 'CHX_TargetNum', 'CHX_Target', 'none', 0, note='expansion chillers wanted = missing base units + added for load')
    ranks(S, 'CH', 'CHX_Target', 'CH')
    # ---- water: chillers that need water (base post-run + expansion valve open)
    count(S, SUP, 'CHX_BaseNeed', ['CH01PostRun', 'CH02PostRun'])
    add_tree(S, SUP, 'CHX_ExpNeed', [f'CH{n:02d}_NeedNum' for n in SLOTS])
    MATH(S, SUP, 'CHX_NeedNow', 'Add', 'CHX_BaseNeed', 'CHX_ExpNeed')
    count(S, SUP, 'CHX_ExpReqCount', [f'CHX_Req{n:02d}' for n in SLOTS])
    MATH(S, SUP, 'CHX_BaseAsked', 'Minimum', 'PlantStage', 'CHX_BaseAvail')
    MATH(S, SUP, 'CHX_Asked', 'Add', 'CHX_BaseAsked', 'CHX_ExpReqCount')
    MATH(S, SUP, 'CHX_TotalNeed', 'Add', 'CHX_NeedNow', 'Zero', note='chillers in post-run / valves open (base pool demand)')
    MATH(S, SUP, 'CHX_WaterDemand', 'Maximum', 'CHX_NeedNow', 'CHX_Asked', note='chillers asked for (water first) or in post-run')
    S.npoint(SUP, 'CHX_ChillersNeedingWater', 'CHX_TotalNeed', 'none', 0, note='chillers that need CHW / CDW flow now')
    CMP(S, SUP, 'CHX_Need1', 'GreaterThanEqual', 'CHX_TotalNeed', 'One')
    CMP(S, SUP, 'CHX_Need2', 'GreaterThanEqual', 'CHX_TotalNeed', 'Two')
    for k, base in (('CHP', ('CHP01Healthy', 'CHP02Healthy')), ('CDP', ('CDP01Healthy', 'CDP02Healthy')), ('CT', ('CT01Healthy', 'CT02Healthy'))):
        count(S, SUP, f'{k}X_BaseAvail', list(base))
        MATH(S, SUP, f'{k}X_TargetRaw', 'Subtract', 'CHX_WaterDemand', f'{k}X_BaseAvail')
        MATH(S, SUP, f'{k}X_Target', 'Maximum', f'{k}X_TargetRaw', 'Zero')
        ranks(S, k, f'{k}X_Target', k)
    MATH(S, SUP, 'CHPX_Speed', 'Maximum', 'CHP01SpeedMinMax', 'CHP02SpeedMinMax')
    MATH(S, SUP, 'CDPX_Speed', 'Maximum', 'CDP01SpeedCmd', 'CDP02SpeedCmd', 'CDPX_MinSpeed')


def base_installed(S):
    for u in ('CH01', 'CH02', 'CHP01', 'CHP02', 'CDP01', 'CDP02', 'CT01', 'CT02'):
        f = S.folder_of[f'{u}_Maintenance']
        S.bparam(f'{u}_Installed', inst(u, True), folder=f, t='Installed', f='Not installed',
                 note='V7.9: off = unit removed / not built - never selected (same as maintenance)')
        S.rewire(f'{u}_AvailNotMaint', 'inC', f'{u}_Installed', T)


def sim_hooks(S):
    OR(S, 'Simulation/Expansion', 'Sim_CHPX_AnyRunFb', *[f'Sim_CHP{n:02d}_RunFb' for n in SLOTS])
    OR(S, 'Simulation/Expansion', 'Sim_CDPX_AnyRunFb', *[f'Sim_CDP{n:02d}_RunFb' for n in SLOTS])
    S.rewire('Sim_AnyCHP_RunFb', 'inC', 'Sim_CHPX_AnyRunFb', F)
    S.rewire('Sim_AnyCDP_RunFb', 'inC', 'Sim_CDPX_AnyRunFb', F)
    count(S, 'Simulation/Expansion', 'Sim_CDPX_OnCount', [f'Sim_CDP{n:02d}_RunFb' for n in SLOTS])
    S.link(S.comp['Sim_CdpOnCount'], 'Sim_CDPX_OnCount', 'inC')
    MATH(S, 'Simulation/Expansion', 'Sim_CDPX_SpeedMax', 'Maximum', *[f'CDP{n:02d}SpeedCmd' for n in SLOTS])
    S.link(S.comp['Sim_CdpSpeedMax'], 'Sim_CDPX_SpeedMax', 'inC')


def scale(S):
    build(S)


def build(S):
    const(S, 'Two', 2.0, 'none', 0)
    S.param('CHX_SimLoadPct', 60.0, 'pct', folder='Simulation/Expansion', prec=0, note='simulated load of a running expansion chiller')
    S.param('CHX_SimKwPerPct', 2.05, 'none', folder='Simulation/Expansion', prec=2, note='334 TR x 0.614 kW/TR / 100 %')
    for n in SLOTS:
        chiller_points(S, n); pump_points(S, 'CHP', n); pump_points(S, 'CDP', n); tower_points(S, n)
    sens = REG['Sensors']; nsens = len(sens)
    for r in sens: sensor(S, r)
    sim_hooks(S)
    S.log.append(('V7.9', EX, 'scalable equipment', f'{len(SLOTS)} expansion slots x 4 types, {nsens} sensor slots', '', ''))


# ------------------------------------------------------------------ field IO: expansion groups = one group per unit, numbered after the base groups
_group_of = FCX.group_of


def group_of(S, n):
    f = S.folder_of[n].split('/')
    if f[0] == EX and len(f) > 1:
        g = f[1]                                     # CH03 ... CT06, Sensors
        return g, f'FieldIO/{g}'
    if f[0] == M7.AIR and len(f) > 2 and f[1] == 'Floors':
        return f[2], f'{M7.AIR}/FieldIO/{f[2]}'
    return _group_of(S, n)


FCX.group_of = group_of
_prev_field_io = FCX.field_io


def post(S):
    for n in SLOTS:
        for k in ('CH', 'CHP', 'CDP', 'CT'): S.rewire(f'{k}{n:02d}_ResetAny', 'inB', 'FO_Reset', F)
    supervisor(S)
    for n in SLOTS:
        chiller_logic(S, n); pump_logic(S, 'CHP', n); pump_logic(S, 'CDP', n); tower_logic(S, n)
    base_installed(S)
    S.rewire('Pool_Need1', 'inC', 'CHX_Need1', F)
    OR(S, SUP, 'CHX_PoolNeed2', 'Pool_Need2', 'CHX_Need2'); relink_consumers(S, 'Pool_Need2', 'CHX_PoolNeed2')
    OR(S, SUP, 'CHX_CTNeed2', 'CT_Need2', 'CHX_Need2'); relink_consumers(S, 'CT_Need2', 'CHX_CTNeed2')


def field_io(S):
    scale(S)                                         # module global: v79_air wraps it
    r = _prev_field_io(S)
    post(S)
    # keep the base groups' device numbers as in V7.8; expansion groups follow
    io = FCX.REG['io']
    exp = {f'{k}{n:02d}' for n in SLOTS for k in ('CH', 'CHP', 'CDP', 'CT')} | {'Sensors'} | {f'F{i:02d}' for i in range(2, 9)}
    base = sorted({x['Group'] for x in io} - exp); extra = sorted(exp & {x['Group'] for x in io})
    idx = {g: i for i, g in enumerate(base + extra, 1)}
    eq = {r['Slot']: r for r in REG.get('Equipment', [])}
    for x in io:
        gi = idx[x['Group']]; x['BACnet_Device'] = 7700 + gi; x['Modbus_Unit'] = gi
        reg = eq.get(x['Group'])
        if reg and reg.get('Protocol'):
            x['Protocol'] = int(reg['Protocol']); x['Protocol_Name'] = FCX.PROTO[int(reg['Protocol'])]
    for g, reg in eq.items():
        if reg.get('Protocol') and f'IO_{g}_Protocol' in S.comp: S.set_fallback(f'IO_{g}_Protocol', float(reg['Protocol']))
    return r


FCX.field_io = field_io
