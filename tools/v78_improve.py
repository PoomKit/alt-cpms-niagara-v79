# -*- coding: utf-8 -*-
"""V7.8 trial logic: the 'suggested improvements' of the trilingual SOO (JA/TH/EN, 6 Oct 2026), on top of V7.7 r9.
Every behaviour change has an ON/OFF switch in folder Improve78 (or next to the logic it changes) so it can be
turned off from the Px / property sheet without editing the wire sheet.  Status codes are plain numbers; their
meaning is in the 'note' of each point and in the SOO logic-control document.

 #  SOO   what                                                               switch (default)
 1  P-01  Plant_NotRunningReason: first reason the plant is not allowed to run  (status only)
 2  P-04  AI_NotUsedReason: why the AI setpoints are not used                 (status only)
 3  P-05  CHn_HandoverStuckAlarm: chiller change-over takes too long          (alarm only)
 4  P-06  stage-down also needs CHW supply temp close to setpoint            Stg_DownNeedsChwsOk (on)
 5  C-03  CHn_WaitingFor: what the chiller is waiting for before it can start (status only)
 6  C-05/W-04  second PI loop keeps the weakest running evaporator above its own minimum flow
                                                                          Byp_EvapLowFlowBoost (on)
 7  E-03  CDP speed goes to fixed (design) speed when measured CDW flow is below the chillers' minimum
                                                                          CDP_LowFlowBoost (on)
 8  W-03  CHW supply setpoint is not raised while an AHU is dehumidifying (LOCAL and AI); OAU optional
                                                                          Chwst_DehumHold (on), Chwst_DehumMaxSP
 9  T-03  basin level transmitter and level switch disagree -> alarm         (alarm only)
10  T-05  CHW manual chemical dose stops by itself after 30 min (delay block CHW_ChemManualTooLong)
11  S-03  plant first-out: the first protective trip is remembered            (status only, reset button)
12  A-06  hottest zone per AHU / FCU group (for the operator, and optional AHU SAT reset)
                                                                          AirSide_UseHottestZone (off)
13  X-05  RUN ALL stops at the first failed test                            CX_StopOnFail (off)
"""
import make_v6 as M6
import make_v7 as M7
import v77_fieldcx as FCX
from make_v7 import AND, OR, NOT, DLY, SW, MATH, CMP, sealin, const, PULSE

T, F = 'ConstantTrue', 'ConstantFalse'
IM = 'Improve78'
_fio = FCX.field_io


def tm(site, fpt):
    return site if FCX.PROF[0] is M6.TIMING['site'] else fpt


def alarm(S, folder, name, src, t, f, cls, text, note=''):
    S.bpoint(folder, name, src, t, f, note=note)
    M6.COS[name] = (True, cls, text)
    return name


def fold(S, n):
    return S.folder_of[n]


def code(S, n):
    return const(S, f'Code_{n}', float(n), 'none', 0, note=f'status code {n}')


def ladder(S, f, name, items, default='Zero', note=''):
    """items = [(condition, code), ...] in priority order (first true wins). Builds a chain of NumericSwitch."""
    nxt = default
    for i, (cond, n) in reversed(list(enumerate(items))):
        blk = f'{name}_S{i + 1:02d}'
        SW(S, f, blk, cond, code(S, n), nxt)
        nxt = blk
    return nxt


def improve(S):
    S.bparam('Improve78_Info', True, folder=IM, t='V7.8 trial logic loaded', f='-',
             note='V7.8 trial logic from the SOO improvement list. Each change has its own switch next to the logic.')
    # ---------------------------------------------------------------- 1  P-01 why the plant is not running
    f = fold(S, 'PlantEnableEffective')
    NOT(S, f, 'Why_PlantOff', 'PlantEnable'); NOT(S, f, 'Why_NoSchedule', 'ScheduleOk')
    NOT(S, f, 'Why_NoDemand', 'DemandOk'); NOT(S, f, 'Why_NotBooted', 'BootEpochQualifiedProbe')
    NOT(S, f, 'Why_CH01Unavail', 'CH01TrainHealthy'); NOT(S, f, 'Why_CH02Unavail', 'CH02TrainHealthy')
    AND(S, f, 'Why_NoChiller', 'Why_CH01Unavail', 'Why_CH02Unavail')
    r = ladder(S, f, 'Why_Plant', [('Why_PlantOff', 1), ('Plant_EmergencyStop', 2), ('Plant_PowerRestoreDelay', 3),
                                   ('Why_NoSchedule', 4), ('Why_NoDemand', 5), ('Why_NotBooted', 6), ('Why_NoChiller', 7)])
    S.npoint(f, 'Plant_NotRunningReason', r, 'none', 0,
             note='0 = allowed to run | 1 = plant switched off | 2 = emergency stop | 3 = waiting after power return | '
                  '4 = outside schedule | 5 = no cooling demand | 6 = controller start-up check | 7 = no chiller available')
    # ---------------------------------------------------------------- 2  P-04 why AI setpoints are not used
    f = fold(S, 'OperationModeAI')
    NOT(S, f, 'Why_AINotSelected', 'ModeCmd_UI'); NOT(S, f, 'Why_AINoHeartbeat', 'HB_Ok')
    NOT(S, f, 'Why_AIChwstLow', 'AI_ChwstAboveMin'); NOT(S, f, 'Why_AIChwstHigh', 'AI_ChwstBelowMax')
    NOT(S, f, 'Why_AIDpLow', 'AI_DpAboveMin'); NOT(S, f, 'Why_AIDpHigh', 'AI_DpBelowMax')
    NOT(S, f, 'Why_AICdsLow', 'AI_CdsAboveMin'); NOT(S, f, 'Why_AICdsHigh', 'AI_CdsBelowMax')
    OR(S, f, 'Why_AIChwstBad', 'Why_AIChwstLow', 'Why_AIChwstHigh')
    OR(S, f, 'Why_AIDpBad', 'Why_AIDpLow', 'Why_AIDpHigh')
    OR(S, f, 'Why_AICdsBad', 'Why_AICdsLow', 'Why_AICdsHigh')
    r = ladder(S, f, 'Why_AI', [('Why_AINotSelected', 1), ('Why_AINoHeartbeat', 2), ('Why_AIChwstBad', 3),
                                ('Why_AIDpBad', 4), ('Why_AICdsBad', 5)])
    S.npoint(f, 'AI_NotUsedReason', r, 'none', 0,
             note='0 = AI setpoints in use | 1 = operator selected LOCAL | 2 = AI heartbeat lost | '
                  '3 = AI CHW temp setpoint outside limits | 4 = AI pressure setpoint outside limits | 5 = AI condenser setpoint outside limits')
    # ---------------------------------------------------------------- 3  P-05 chiller change-over stuck
    for c in ('01', '02'):
        ch = f'CH{c}'; f = fold(S, f'{ch}HandoverHold')
        DLY(S, f, f'{ch}_HandoverLong', f'{ch}HandoverHold', tm(900000, 30000), note='site 15 min / test 30 s')
        alarm(S, f, f'{ch}_HandoverStuckAlarm', f'{ch}_HandoverLong', 'Stuck', 'Normal', 'Warning',
              f'{ch} change-over takes too long - the other chiller did not prove running')
    # ---------------------------------------------------------------- 4  P-06 stage down only when CHW supply is on target
    f = fold(S, 'LagNotNeeded')
    S.bparam('Stg_DownNeedsChwsOk', True, folder=f, t='Check CHW supply', f='Load only (V7.7)',
             note='V7.8: second chiller is released only when CHW supply temp is within Stg_DownChwsBand of setpoint')
    S.param('Stg_DownChwsBand', 1.0, 'none', folder=f, prec=1, note='K above the active CHW setpoint still counted as on target')
    MATH(S, f, 'Stg_DownChwsLimit', 'Add', 'CHW_LeavingTemperatureSetpoint_ACTIVE', 'Stg_DownChwsBand')
    CMP(S, f, 'Stg_DownChwsOnTarget', 'LessThanEqual', 'CHWS', 'Stg_DownChwsLimit')
    NOT(S, f, 'Stg_DownChwsCheckOff', 'Stg_DownNeedsChwsOk')
    OR(S, f, 'Stg_DownChwsOk', 'Stg_DownChwsOnTarget', 'Stg_DownChwsCheckOff', 'CHWS_SensorInvalidAlarm')
    AND(S, f, 'Stg_LagNotNeededOk', 'LagNotNeeded', 'Stg_DownChwsOk', note='V7.8: low load AND CHW supply on target')
    S.rewire('LagNotNeededDelay', 'in', 'Stg_LagNotNeededOk', 'LagNotNeeded')
    # ---------------------------------------------------------------- 5  C-03 what each chiller is waiting for
    for c in ('01', '02'):
        ch = f'CH{c}'; f = fold(S, f'{ch}StartPermissive')
        for nm, src in (('NoCHP', 'CHP_AnyProvenBridge'), ('NoCDP', 'CDP_AnyProvenBridge'), ('NoTower', 'CT_WaterPathBridge'),
                        ('NoChwValve', f'{ch}ValveOpenProof'), ('NoCdwValve', f'{ch}CdwValveOpenProof'),
                        ('NoChwFlow', f'{ch}CHWFlowBridge'), ('NoCdwFlow', f'{ch}CDWFlowBridge'),
                        ('AntiRecycle', f'{ch}MinOffPermit'), ('Interlock', f'{ch}_InterlockOK'), ('NotRunning', f'{ch}RunProofSelected')):
            NOT(S, f, f'{ch}_W_{nm}', src)
        AND(S, f, f'{ch}_W_Active', f'{ch}Request', f'{ch}_W_NotRunning', note='chiller asked to run but not yet proven running')
        r = ladder(S, f, f'{ch}_W', [(f'{ch}_W_Interlock', 1), (f'{ch}_W_NoCHP', 2), (f'{ch}_W_NoCDP', 3), (f'{ch}_W_NoTower', 4),
                                    (f'{ch}_W_NoChwValve', 5), (f'{ch}_W_NoCdwValve', 6), (f'{ch}_W_NoChwFlow', 7),
                                    (f'{ch}_W_NoCdwFlow', 8), (f'{ch}_W_AntiRecycle', 9), (f'{ch}StartCmd', 10)])
        SW(S, f, f'{ch}_W_Gate', f'{ch}_W_Active', r, 'Zero')
        S.npoint(f, f'{ch}_WaitingFor', f'{ch}_W_Gate', 'none', 0,
                 note='0 = not asked / running | 1 = safety trip or interlock | 2 = CHW pump | 3 = condenser pump | 4 = cooling tower water path | '
                      '5 = CHW valve | 6 = condenser valve | 7 = CHW flow switch | 8 = condenser flow switch | 9 = restart wait timer | 10 = compressor starting')
    # ---------------------------------------------------------------- 6  C-05 / W-04 one evaporator below its own minimum flow
    # second (per-evaporator) PI loop; bypass position = the larger of the plant-flow loop and this loop -> no on/off cycling
    from make_v7 import PID
    f = fold(S, 'Byp_Select')
    S.bparam('Byp_EvapLowFlowBoost', True, folder=f, t='Per-evaporator check', f='Plant total only (V7.7)',
             note='V7.8: bypass also opens when ONE running chiller has less than its own minimum CHW flow')
    S.param('Byp_EvapMinPct', 110.0, 'pct', folder=f, prec=0, note='keep each running evaporator above this % of its own minimum flow')
    const(S, 'Byp_EvapIdlePct', 999.0, 'none', 0, note='value used for a chiller that is not running (ignored by the minimum)')
    for c in ('01', '02'):
        ch = f'CH{c}'
        MATH(S, f, f'Byp_{ch}FlowRatio', 'Divide', f'{ch}_ChwFlow', f'{ch}_MinFlow')
        MATH(S, f, f'Byp_{ch}FlowPctRaw', 'Multiply', f'Byp_{ch}FlowRatio', 'HundredPct')
        SW(S, f, f'Byp_{ch}FlowPct', f'{ch}RunProofSelected', f'Byp_{ch}FlowPctRaw', 'Byp_EvapIdlePct', note='% of own minimum flow (999 = not running)')
    MATH(S, f, 'Byp_EvapFlowPctMin', 'Minimum', 'Byp_CH01FlowPct', 'Byp_CH02FlowPct', note='weakest running evaporator, % of its minimum')
    AND(S, f, 'Byp_EvapLoopEnable', 'Byp_Enable', 'Byp_EvapLowFlowBoost', 'Byp_EvapFlowValid')
    PID(S, f, 'Byp_EvapPID', 'Byp_EvapFlowPctMin', 'Byp_EvapMinPct', 'Byp_EvapLoopEnable', 'reverse', 0.5, 1.0, 0, 100,
        note='V7.8: weakest evaporator below its minimum -> open bypass')
    MATH(S, f, 'Byp_EvapMax', 'Maximum', 'Byp_FailSafeSelect', 'Byp_EvapPID')
    SW(S, f, 'Byp_EvapSel', 'Byp_EvapLoopEnable', 'Byp_EvapMax', 'Byp_FailSafeSelect', note='V7.8: larger of plant-flow loop and evaporator loop')
    S.rewire('Byp_Select', 'inTrue', 'Byp_EvapSel', 'Byp_FailSafeSelect')
    CMP(S, f, 'Byp_EvapLoopLeads', 'GreaterThan', 'Byp_EvapPID', 'Byp_FailSafeSelect')
    AND(S, f, 'Byp_EvapLowShow', 'Byp_EvapLoopLeads', 'Byp_EvapLoopEnable')
    S.bpoint(f, 'Byp_EvapLowFlowActive', 'Byp_EvapLowShow', 'Opening for one evaporator', 'Normal')
    # ---------------------------------------------------------------- 7  E-03 condenser flow measured below minimum
    f = fold(S, 'CDP_SpeedFinal')
    S.bparam('CDP_LowFlowBoost', True, folder=f, t='Boost to fixed speed', f='Off (V7.7)',
             note='V7.8: if measured CDW flow < running chillers minimum, CDP runs at the fixed (design) speed')
    CMP(S, f, 'CDP_FlowBelowMin', 'LessThan', 'CDW_Flow', 'Cdw_MinFlowSum')
    AND(S, f, 'CDP_FlowLowUse', 'CDP_FlowBelowMin', 'CDP_UseLoop', 'CDP_LowFlowBoost')
    DLY(S, f, 'CDP_FlowLowDly', 'CDP_FlowLowUse', tm(30000, 3000), tm(300000, 10000), note='on 30 s / off 5 min (site)')
    MATH(S, f, 'CDP_SpeedBoostMax', 'Maximum', 'CDP_SpeedRate', 'FixedCDPSpeedPct')
    SW(S, f, 'CDP_SpeedBoostSel', 'CDP_FlowLowDly', 'CDP_SpeedBoostMax', 'CDP_SpeedRate')
    S.rewire('CDP_SpeedFinal', 'inTrue', 'CDP_SpeedBoostSel', 'CDP_SpeedRate')
    S.bpoint(f, 'CDP_LowFlowBoostActive', 'CDP_FlowLowDly', 'Boost (low CDW flow)', 'Normal')
    # ---------------------------------------------------------------- 8  W-03 do not raise CHW setpoint while dehumidifying
    f = fold(S, 'ChwstActiveClamp')
    S.bparam('Chwst_DehumHold', True, folder=f, t='Hold low', f='Off (V7.7)',
             note='V7.8: while an AHU is dehumidifying (return air RH high), CHW setpoint (LOCAL or AI) is limited to Chwst_DehumMaxSP')
    S.param('Chwst_DehumMaxSP', 7.0, 'C', folder=f, prec=1, note='highest CHW supply setpoint allowed while dehumidifying')
    S.bparam('Chwst_DehumIncludeOAU', False, folder=f, t='AHU + OAU', f='AHU only',
             note='OAU (100 % outdoor air) dehumidifies almost all the time; include it only if its dew-point-high alarm should also hold CHWST')
    AND(S, f, 'Chwst_OauDehumUse', 'OAU01_DewPointHighAlarm', 'Chwst_DehumIncludeOAU', note='OAU counts only when its leaving dew point stayed high 30 min')
    OR(S, f, 'Chwst_AnyDehum', 'AHU01_DehumActive', 'AHU02_DehumActive', 'Chwst_OauDehumUse')
    AND(S, f, 'Chwst_DehumUse', 'Chwst_AnyDehum', 'Chwst_DehumHold')
    MATH(S, f, 'Chwst_DehumMin', 'Minimum', 'ChwstActiveClamp', 'Chwst_DehumMaxSP')
    SW(S, f, 'Chwst_DehumSel', 'Chwst_DehumUse', 'Chwst_DehumMin', 'ChwstActiveClamp')
    S.rewire('DL_ChwstSum', 'inA', 'Chwst_DehumSel', 'ChwstActiveClamp')
    S.bpoint(f, 'Chwst_DehumHoldActive', 'Chwst_DehumUse', 'Held for dehumidification', 'Normal')
    # ---------------------------------------------------------------- 9  T-03 level transmitter vs level switches
    for t in ('CT01', 'CT02'):
        f = fold(S, f'{t}LevelBelowLL')
        NOT(S, f, f'{t}_AnalogNotLow', f'{t}LevelBelowLow')
        AND(S, f, f'{t}_LLSwButAnalogOk', f'{t}_LowLowLevelSwitch', f'{t}_AnalogNotLow', f'{t}NotLevelSensorBad')
        NOT(S, f, f'{t}_LowSwNormal', f'{t}_LowLevelSwitch')
        AND(S, f, f'{t}_AnalogLLButSwOk', f'{t}LevelBelowLL', f'{t}_LowSwNormal', f'{t}NotLevelSensorBad')
        OR(S, f, f'{t}_LevelDisagree', f'{t}_LLSwButAnalogOk', f'{t}_AnalogLLButSwOk')
        DLY(S, f, f'{t}_LevelDisagreeDly', f'{t}_LevelDisagree', tm(120000, 5000))
        alarm(S, f, f'{t}_LevelDisagreeAlarm', f'{t}_LevelDisagreeDly', 'Disagree', 'Normal', 'Warning',
              f'{t} basin level transmitter and level switches disagree - check both')
    # ---------------------------------------------------------------- 10  T-05 CHW manual dose time limit
    f = fold(S, 'CHW_ChemDemand')
    DLY(S, f, 'CHW_ChemManualTooLong', 'CHW_ChemFeederOpen', tm(1800000, 20000), note='site 30 min / test 20 s')
    NOT(S, f, 'CHW_ChemManualInTime', 'CHW_ChemManualTooLong')
    AND(S, f, 'CHW_ChemManualOk', 'CHW_ChemFeederOpen', 'CHW_ChemManualInTime')
    S.rewire('CHW_ChemDemand', 'inB', 'CHW_ChemManualOk', 'CHW_ChemFeederOpen')
    S.rewire('CHW_ChemManualSel', 'inSwitch', 'CHW_ChemManualOk', 'CHW_ChemFeederOpen')
    alarm(S, f, 'CHW_ChemManualTimeoutAlarm', 'CHW_ChemManualTooLong', 'Timed out', 'Normal', 'Warning',
          'CHW manual chemical dose left on too long - pump stopped, set back to Auto')
    # ---------------------------------------------------------------- 11  S-03 first-out
    f = 'Alarms/Plant'
    PULSE(S, f, 'Plant_FirstOutResetFire', None, 2000, note='Px button: clear the first-out memory')
    OR(S, f, 'FO_Reset', 'Plant_FirstOutResetFire', 'PlantAlarmResetFire')
    src = [('Plant_EmergencyStop', 1), ('Plant_PowerRestoreDelay', 2), ('RL_StopChillers', 3), ('CH01_SafetyTrip', 4),
           ('CH02_SafetyTrip', 5), ('CH01_FlowTripAny', 6), ('CH02_FlowTripAny', 7)]
    lat = [f'FO_L{n}' for _, n in src]
    for L in lat:
        sealin(S, f, L, F, 'FO_Reset')
    OR(S, f, 'FO_AnyA', *lat[:4]); OR(S, f, 'FO_AnyB', *lat[4:])
    OR(S, f, 'FO_Any', 'FO_AnyA', 'FO_AnyB'); NOT(S, f, 'FO_None', 'FO_Any')
    for (s, n), L in zip(src, lat):
        AND(S, f, f'{L}_Set', s, 'FO_None', note='latched only if no other trip was remembered first')
        S.rewire(L, 'inA', f'{L}_Set', F)
    r = ladder(S, f, 'FO', [(L, n) for (_, n), L in zip(src, lat)])
    S.npoint(f, 'Plant_FirstOut', r, 'none', 0,
             note='first protective trip since the last reset: 0 = none | 1 = emergency stop | 2 = power / phase failure | 3 = refrigerant leak | '
                  '4 = CH01 freeze / condenser high | 5 = CH02 freeze / condenser high | 6 = CH01 flow switch | 7 = CH02 flow switch')
    # ---------------------------------------------------------------- 12  A-06 hottest zone
    A = M7.AIR; f = f'{A}/Zones/Averages'
    S.bparam('AirSide_UseHottestZone', False, folder=f'{A}/Common', t='Hottest zone', f='Zone average (V7.7)',
             note='V7.8 option: AHU SAT reset uses the hottest zone instead of the zone average')
    Z = {'AHU01': ['0101', '0102', '0103', '0104'], 'AHU02': ['0105', '0106', '0107', '0108'], 'FCU': ['0109', '0110']}
    for g, zs in Z.items():
        MATH(S, f, f'Zone_{g}_TMax', 'Maximum', *[f'ZoneTemperatureAvg_01_{z}' for z in zs])
        S.npoint(f, f'Zone_{g}_HottestTemp', f'Zone_{g}_TMax', 'C', 1, note=f'highest room temperature of the {g} zones')
    for u in ('AHU01', 'AHU02'):
        L = f'{A}/{u}/Safety'
        if f'Zone_{u}_HottestTemp' not in S.comp: continue
        SW(S, L, f'{u}_ZoneOrHot', 'AirSide_UseHottestZone', f'Zone_{u}_HottestTemp', f'Zone_{u}_AvgTemp')
        S.rewire(f'{u}_CtrlTempSel', 'inTrue', f'{u}_ZoneOrHot', f'Zone_{u}_AvgTemp')
    S.log.append(('V7.8', IM, 'SOO improvement trial logic', '13 items, see v78_improve.py', '', ''))


def cx78(S):
    # ---------------------------------------------------------------- 13  X-05 RUN ALL stops at the first failure
    f = 'Commissioning/FunctionalTest/RunAll'
    S.bparam('CX_StopOnFail', False, folder=f, t='Stop at first FAIL', f='Run all (V7.7)',
             note='V7.8 option: automatic test sequence stops when a test fails, so the fault can be looked at')
    fails = [f'CX_FT{i:02d}_Fail' for i in range(1, 11) if f'CX_FT{i:02d}_Fail' in S.comp]
    OR(S, f, 'CX_FailOr0', *fails[:4]); OR(S, f, 'CX_FailOr1', *fails[4:8]); OR(S, f, 'CX_FailOr2', *fails[8:])
    OR(S, f, 'CX_AnyFail', 'CX_FailOr0', 'CX_FailOr1', 'CX_FailOr2')
    AND(S, f, 'CX_StopNow', 'CX_AnyFail', 'CX_StopOnFail')
    S.rewire('CX_AutoSeqReset', 'inC', 'CX_StopNow', F)


def field_io(S):
    r = _fio(S)
    improve(S)
    return r


FCX.field_io = field_io
_cx = FCX.commissioning


def commissioning(S):
    r = _cx(S)
    cx78(S)
    return r


FCX.commissioning = commissioning
