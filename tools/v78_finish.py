# -*- coding: utf-8 -*-
"""V7.8 r11: the remaining SOO improvement items (after v78_improve.py).  Options that change behaviour have a switch;
items that cannot be decided in logic (vendor addresses, fire matrix, OEM data) are listed in the SOO document.

 #  SOO   what                                                                switch (default)
 1  P-01  freeze / condenser trip keeps the pumps and valves on 10 min after the cause clears   CH_TripRunOn (on)
 2  P-02  equipment running without a command (Hand / stuck contactor / state after power return) -> alarm
 3  P-04  AI payload sequence number: reject old (lower) and stale (not changing 12 min) payloads   AI_RequireSeq (off)
 4  P-05  maintenance switch per chiller / pump / tower: unit is taken out of selection   xx_Maintenance (off)
 5  C-01  full condenser-first order: CHW valve opens only after condenser flow is proven  CH_CondenserFirst (off)
 6  C-03  first start-failure cause latched (CHn_StartFailCause) + retries left
 7  C-06  HPV can be switched off (valve fully open with the CDW valve)     CH_HpvEnable (on)
 8  E-01  pump / tower change-over stuck -> alarm
 9  W-02  trim & respond: no request is ignored when fewer than 3 air-side units run     TR_AutoIgnore (on)
10  T-02  tower fail-safe 'open all valves' skips a tower that is dry (LL) or has both cells isolated   CT_FailSafeSkipDry (on)
11  T-05  CHW fill water totaliser + high-fill alarm, reset button
12  S-01  E-stop / refrigerant-leak stop need a reset before restart       Plant_EstopNeedsReset / RL_NeedsReset (off)
13  A-03  FCU fan speed relays: break-before-make 1 s
14  A-06  number of valid zone sensors + alarm when too few
15  X-05  RUN ALL run number (CX_RunId) for archiving results
"""
import make_v6 as M6
import make_v7 as M7
import v77_fieldcx as FCX
import v78_improve as IMP
from make_v7 import AND, OR, NOT, DLY, SW, MATH, CMP, sealin, const, PULSE

T, F = 'ConstantTrue', 'ConstantFalse'
tm, alarm, fold, code = IMP.tm, IMP.alarm, IMP.fold, IMP.code
_fio = FCX.field_io
_cx = FCX.commissioning


def finish(S):
    # 1 P-01 trip run-on
    f0 = fold(S, 'CH01PostRunSrc')
    S.bparam('CH_TripRunOn', True, folder=f0, t='Keep water flowing 10 min', f='Normal post-run only',
             note='r11: after a freeze / condenser-high trip the valves and pumps stay on 10 min after the cause clears')
    for c in ('01', '02'):
        ch = f'CH{c}'; f = fold(S, f'{ch}PostRunSrc')
        DLY(S, f, f'{ch}_TripRunOnDly', f'{ch}_SafetyTripIn', 0, tm(600000, 20000), note='off-delay 10 min (site)')
        AND(S, f, f'{ch}_TripRunOnUse', f'{ch}_TripRunOnDly', 'CH_TripRunOn', 'PlantPermissive')
        S.rewire(f'{ch}PostRunSrc', 'inD', f'{ch}_TripRunOnUse', F)
    # 2 P-02 running without command
    for u in ('CH01', 'CH02', 'CHP01', 'CHP02', 'CDP01', 'CDP02'):
        f = fold(S, f'{u}StartCmd')
        NOT(S, f, f'{u}_NoCmd', f'{u}StartCmd')
        AND(S, f, f'{u}_RunNoCmd', f'{u}RunProof', f'{u}_NoCmd')
        DLY(S, f, f'{u}_RunNoCmdDly', f'{u}_RunNoCmd', tm(120000, 20000))
        alarm(S, f, f'{u}_UncommandedRunAlarm', f'{u}_RunNoCmdDly', 'Running', 'Normal', 'Warning',
              f'{u} is running without a command (Hand / local / stuck contactor / state after power return)')
    # 3 P-04 AI payload sequence
    f = 'AI_Cloud'
    S.param('AI_PayloadSeq', 0.0, 'none', folder=f, prec=0, note='r11: AI writes an increasing message number with every payload (tag melco:pointNameString)')
    S.bparam('AI_RequireSeq', False, folder=f, t='Check message number', f='Not checked',
             note='r11: when on, AI values are used only while AI_PayloadSeq keeps increasing')
    S.kc(f, 'AI_SeqClock', 'MultiVibrator', props=[('period', 'b:RelTime', str(tm(60000, 5000)))], note='sample the message number')
    MATH(S, f, 'AI_SeqMaxIn', 'Maximum', 'AI_PayloadSeq', 'AI_PayloadSeq')
    S.kc(f, 'AI_SeqMaxSeen', 'NumericLatch', {'in': 'AI_SeqMaxIn', 'clock': 'AI_SeqClock'}, note='highest message number seen')
    S.rewire('AI_SeqMaxIn', 'inB', 'AI_SeqMaxSeen', 'AI_PayloadSeq')
    CMP(S, f, 'AI_SeqOld', 'LessThan', 'AI_PayloadSeq', 'AI_SeqMaxSeen', note='number went backwards = old / replayed payload')
    S.kc(f, 'AI_SeqPrev', 'NumericLatch', {'in': 'AI_PayloadSeq', 'clock': 'AI_SeqClock'})
    CMP(S, f, 'AI_SeqSame', 'LessThanEqual', 'AI_PayloadSeq', 'AI_SeqPrev')
    DLY(S, f, 'AI_SeqStale', 'AI_SeqSame', tm(720000, 60000), note='no new message for 12 min (site)')
    OR(S, f, 'AI_SeqBad', 'AI_SeqOld', 'AI_SeqStale')
    NOT(S, f, 'AI_SeqCheckOff', 'AI_RequireSeq'); NOT(S, f, 'AI_SeqGood', 'AI_SeqBad')
    OR(S, f, 'AI_SeqOk', 'AI_SeqGood', 'AI_SeqCheckOff')
    S.rewire('AI_AvailableLogic', 'inC', 'AI_SeqOk', T)
    NOT(S, f, 'Why_AISeqBad', 'AI_SeqOk')
    SW(S, fold(S, 'Why_AI_S05'), 'Why_AI_S06', 'Why_AISeqBad', code(S, 6), 'Zero')
    S.rewire('Why_AI_S05', 'inFalse', 'Why_AI_S06', 'Zero')
    # 4 P-05 maintenance
    for u in ('CH01', 'CH02', 'CHP01', 'CHP02', 'CDP01', 'CDP02', 'CT01', 'CT02'):
        f = fold(S, f'{u}Healthy')
        S.bparam(f'{u}_Maintenance', False, folder=f, t='Maintenance (out of service)', f='In service',
                 note='r11: unit is not selected and not started while in maintenance')
        NOT(S, f, f'{u}_NotMaint', f'{u}_Maintenance')
        AND(S, f, f'{u}_AvailNotMaint', f'{u}Available', f'{u}_NotMaint')
        S.rewire(f'{u}Healthy', 'inA', f'{u}_AvailNotMaint', f'{u}Available')
    # 5 C-01 condenser first + 7 C-06 HPV switch
    f0 = fold(S, 'CH01Healthy')
    S.bparam('CH_CondenserFirst', False, folder=f0, t='Condenser side first', f='Both sides together (V7.7)',
             note='r11: CHW valve (and so the CHW pump) waits until condenser water flow is proven - confirm with the chiller OEM')
    S.bparam('CH_HpvEnable', True, folder=f0, t='HPV modulates', f='HPV fully open',
             note='r11: switch off if the OEM says the head-pressure valve is not needed')
    NOT(S, f0, 'CH_CondFirstOff', 'CH_CondenserFirst')
    for c in ('01', '02'):
        ch = f'CH{c}'; f = fold(S, f'{ch}PostRun')
        OR(S, f, f'{ch}_ChwValveGateOk', 'CH_CondFirstOff', f'{ch}CDWFlowBridge', f'{ch}RunProofSelected')
        AND(S, f, f'{ch}_ChwValveCmdLogic', f'{ch}PostRun', f'{ch}_ChwValveGateOk', note='r11: CHW valve after condenser flow (option)')
        S.rewire(f'{ch}ValveOpenCmd', 'in16', f'{ch}_ChwValveCmdLogic', f'{ch}PostRun')
        f = fold(S, f'{ch}HpvGate')
        SW(S, f, f'{ch}_HpvSel', 'CH_HpvEnable', f'{ch}HpvReset', 'HundredPct')
        S.rewire(f'{ch}HpvGate', 'inTrue', f'{ch}_HpvSel', f'{ch}HpvReset')
    # 6 C-03 first failure cause
    for c in ('01', '02'):
        ch = f'CH{c}'; f = fold(S, f'{ch}RetryCounter')
        if 'CH_WaitHoldClock' not in S.comp:
            S.kc(f, 'CH_WaitHoldClock', 'MultiVibrator', props=[('period', 'b:RelTime', '1000')], note='1 s sample of the waiting-for code')
        SW(S, f, f'{ch}_WaitHoldIn', f'{ch}_W_Active', f'{ch}_WaitingFor', f'{ch}_WaitingFor')
        S.kc(f, f'{ch}_WaitHold', 'NumericLatch', {'in': f'{ch}_WaitHoldIn', 'clock': 'CH_WaitHoldClock'},
             note='last waiting-for code while the chiller was asked to run (held when not asked)')
        S.rewire(f'{ch}_WaitHoldIn', 'inFalse', f'{ch}_WaitHold', f'{ch}_WaitingFor')
        S.kc(f, f'{ch}_StartFailLatch', 'NumericLatch', {'in': f'{ch}_WaitHold', 'clock': f'{ch}StartTimeoutDelay'},
             note='r11: waiting-for code at the moment the start timed out')
        S.npoint(f, f'{ch}_StartFailCause', f'{ch}_StartFailLatch', 'none', 0,
                 note='last start failure: same codes as CHn_WaitingFor (0 = none yet)')
        MATH(S, f, f'{ch}_RetriesLeftCalc', 'Subtract', 'CH_MaxAutoRetries', f'{ch}RetryCounter')
        S.npoint(f, f'{ch}_RetriesLeftNum', f'{ch}_RetriesLeftCalc', 'none', 0, note='automatic retries left')
    # 8 E-01 change-over stuck
    for u in ('CHP01', 'CHP02', 'CDP01', 'CDP02', 'CT01', 'CT02'):
        f = fold(S, f'{u}HandoverHold')
        DLY(S, f, f'{u}_HandoverLong', f'{u}HandoverHold', tm(300000, 30000), note='site 5 min / test 30 s')
        alarm(S, f, f'{u}_HandoverStuckAlarm', f'{u}_HandoverLong', 'Stuck', 'Normal', 'Warning',
              f'{u} change-over takes too long - the other unit did not prove running')
    # 9 W-02 no ignored request with few air-side units
    f = fold(S, 'TR_Loop')
    S.bparam('TR_AutoIgnore', True, folder=f, t='Ignore 0 when < 3 units run', f='Always TR_IgnoreRequests',
             note='r11: with only 1-2 air-side units running, a single request is not ignored')
    units = ['AHU01_Status', 'AHU02_Status', 'OAU01_Status', 'FCU01_Status', 'FCU02_Status', 'FCU03_Status', 'FCU04_Status']
    for s in units:
        SW(S, f, f'TR_Cnt_{s}', s, 'One', 'Zero')
    MATH(S, f, 'TR_CntA', 'Add', *[f'TR_Cnt_{s}' for s in units[:4]])
    MATH(S, f, 'TR_CntB', 'Add', *[f'TR_Cnt_{s}' for s in units[4:]])
    MATH(S, f, 'TR_UnitsRunning', 'Add', 'TR_CntA', 'TR_CntB')
    const(S, 'TR_FewUnits', 3.0, 'none', 0, note='fewer running air-side units than this = do not ignore requests')
    CMP(S, f, 'TR_Few', 'LessThan', 'TR_UnitsRunning', 'TR_FewUnits')
    AND(S, f, 'TR_IgnoreZeroUse', 'TR_Few', 'TR_AutoIgnore')
    SW(S, f, 'TR_IgnoreSel', 'TR_IgnoreZeroUse', 'Zero', 'TR_IgnoreRequests')
    S.rewire('TR_Loop', 'setpoint', 'TR_IgnoreSel', 'TR_IgnoreRequests')
    # 10 T-02 fail-safe valves skip dry / isolated towers
    f0 = fold(S, 'CT_ValvesFailSafe')
    S.bparam('CT_FailSafeSkipDry', True, folder=f0, t='Skip dry / isolated tower', f='Open all (V7.7)',
             note='r11: fail-safe open-all-valves does not open a tower whose basin is low-low or whose cells are both isolated')
    NOT(S, f0, 'CT_FailSafeAll', 'CT_FailSafeSkipDry')
    for t in ('CT01', 'CT02'):
        f = fold(S, f'{t}ValveDemand')
        AND(S, f, f'{t}_BothIsolated', f'{t}_01_ServiceIsolate', f'{t}_02_ServiceIsolate')
        NOT(S, f, f'{t}_NotIsolated', f'{t}_BothIsolated')
        AND(S, f, f'{t}_WetAndInService', f'{t}NotBasinLL', f'{t}_NotIsolated')
        OR(S, f, f'{t}_FailSafeAllowed', f'{t}_WetAndInService', 'CT_FailSafeAll')
        AND(S, f, f'{t}_FailSafeOpen', 'CT_ValvesFailSafe', f'{t}_FailSafeAllowed')
        S.rewire(f'{t}ValveDemand', 'inB', f'{t}_FailSafeOpen', 'CT_ValvesFailSafe')
    # 11 T-05 fill totaliser
    f = fold(S, 'CHW_ChemDemand')
    S.kc(f, 'CHW_FillClock', 'MultiVibrator', props=[('period', 'b:RelTime', '60000')], note='1 min')
    const(S, 'Sixty', 60.0, 'none', 0)
    MATH(S, f, 'CHW_FillPerMin', 'Multiply', 'CHW_FillFlow', 'One', note='gpm x 1 min = gallons added this minute')
    MATH(S, f, 'CHW_FillSum', 'Add', 'CHW_FillPerMin', 'CHW_FillPerMin')
    PULSE(S, f, 'CHW_FillTotalResetFire', None, 2000, note='Px button: reset the fill total')
    SW(S, f, 'CHW_FillNext', 'CHW_FillTotalResetFire', 'Zero', 'CHW_FillSum')
    S.kc(f, 'CHW_FillTotalLatch', 'NumericLatch', {'in': 'CHW_FillNext', 'clock': 'CHW_FillClock'})
    NOT(S, f, 'CHW_FillClockN', 'CHW_FillClock')
    S.kc(f, 'CHW_FillTotalPrev', 'NumericLatch', {'in': 'CHW_FillTotalLatch', 'clock': 'CHW_FillClockN'},
         note='second latch (other clock edge) so the running total has no loop inside one scan')
    S.rewire('CHW_FillSum', 'inB', 'CHW_FillTotalPrev', 'CHW_FillPerMin')
    S.npoint(f, 'CHW_FillTotal', 'CHW_FillTotalLatch', 'none', 0, note='r11: water added to the CHW loop since the last reset (gallons)')
    S.param('CHW_FillTotalAlarmLimit', 500.0, 'none', folder=f, prec=0, note='fill total (gallons, about 1.9 m3) above this since the last reset -> possible leak')
    CMP(S, f, 'CHW_FillTotalHigh', 'GreaterThan', 'CHW_FillTotal', 'CHW_FillTotalAlarmLimit')
    alarm(S, f, 'CHW_FillTotalHighAlarm', 'CHW_FillTotalHigh', 'High', 'Normal', 'Warning', 'CHW loop has taken a lot of make-up water - check for leaks')
    # 12 S-01 restart needs reset
    f = fold(S, 'Plant_HardInhibit')
    S.bparam('Plant_EstopNeedsReset', False, folder=f, t='Reset needed after E-stop', f='Restart when released (V7.7)',
             note='r11: after an E-stop the plant stays off until Plant reset / first-out reset')
    S.bparam('RL_NeedsReset', False, folder=f, t='Reset needed after leak stop', f='Restart when gas clears (V7.7)',
             note='r11: after a refrigerant-leak chiller stop the chillers stay off until reset')
    sealin(S, f, 'Plant_EstopLatch', 'Plant_EmergencyStop', 'FO_Reset')
    AND(S, f, 'Plant_EstopLatchUse', 'Plant_EstopLatch', 'Plant_EstopNeedsReset')
    S.rewire('Plant_HardInhibit', 'inC', 'Plant_EstopLatchUse', F)
    sealin(S, f, 'RL_StopLatch', 'RL_StopChillers', 'FO_Reset')
    AND(S, f, 'RL_StopLatchUse', 'RL_StopLatch', 'RL_NeedsReset')
    S.rewire('Plant_ChillerInhibit', 'inC', 'RL_StopLatchUse', F)
    # 13 A-03 break-before-make
    for n in ('01', '02', '03', '04'):
        u = f'FCU{n}'
        for sp in ('High', 'Med', 'Low'):
            f = fold(S, f'{u}{sp}Logic')
            DLY(S, f, f'{u}_{sp}Make', f'{u}{sp}Logic', 1000, 0, note='r11: relay closes 1 s after the previous speed opened')
            S.rewire(f'{u}_Fan{sp}Cmd', 'in16', f'{u}_{sp}Make', f'{u}{sp}Logic')
    # 14 A-06 valid zone sensors
    f = f'{M7.AIR}/Zones/Averages'
    zs = [f'ZoneTemperatureAvg_01_{i:04d}' for i in range(101, 113)]
    zs = [z for z in zs if z in S.comp]
    const(S, 'Zone_ValidLo', 5.0, 'C', 1); const(S, 'Zone_ValidHi', 45.0, 'C', 1)
    for z in zs:
        CMP(S, f, f'{z}_AboveLo', 'GreaterThan', z, 'Zone_ValidLo'); CMP(S, f, f'{z}_BelowHi', 'LessThan', z, 'Zone_ValidHi')
        AND(S, f, f'{z}_Ok', f'{z}_AboveLo', f'{z}_BelowHi')
        SW(S, f, f'{z}_OkN', f'{z}_Ok', 'One', 'Zero')
    parts = []
    for i in range(0, len(zs), 4):
        MATH(S, f, f'Zone_ValidSum{i // 4}', 'Add', *[f'{z}_OkN' for z in zs[i:i + 4]]); parts.append(f'Zone_ValidSum{i // 4}')
    MATH(S, f, 'Zone_ValidCountCalc', 'Add', *parts)
    S.npoint(f, 'Zone_ValidCount', 'Zone_ValidCountCalc', 'none', 0, note=f'r11: room sensors giving a believable value (of {len(zs)})')
    S.param('Zone_MinValid', 6.0, 'none', folder=f, prec=0, note='fewer valid room sensors than this -> alarm')
    CMP(S, f, 'Zone_FewValid', 'LessThan', 'Zone_ValidCount', 'Zone_MinValid')
    AND(S, f, 'Zone_FewValidOnline', 'Zone_FewValid', 'AirPlug_GatewayOnline')
    DLY(S, f, 'Zone_FewValidDly', 'Zone_FewValidOnline', tm(600000, 10000))
    alarm(S, f, 'Zone_FewSensorsAlarm', 'Zone_FewValidDly', 'Few sensors', 'Normal', 'Warning', 'Too few room sensors give valid values - zone averages are not reliable')
    # 16 W-01 drive speed does not follow the command
    const(S, 'VFD_BaseHz', 50.0, 'none', 0, note='drive frequency at 100 % speed')
    S.param('VFD_SpeedDevLimit', 10.0, 'pct', folder=fold(S, 'CHP01SpeedCmd'), prec=0, note='r11: command vs drive feedback difference -> alarm (%)')
    for u, fb in (('CHP01', 'CHP01_SpeedFeedbackHz'), ('CHP02', 'CHP02_SpeedFeedbackHz'), ('CDP01', 'CDP01_SpeedFeedbackHz'), ('CDP02', 'CDP02_SpeedFeedbackHz')):
        if fb not in S.comp: continue
        f = fold(S, f'{u}SpeedCmd')
        MATH(S, f, f'{u}_FbRatio', 'Divide', fb, 'VFD_BaseHz'); MATH(S, f, f'{u}_FbPct', 'Multiply', f'{u}_FbRatio', 'HundredPct')
        MATH(S, f, f'{u}_SpdDev', 'Subtract', f'{u}SpeedCmd', f'{u}_FbPct'); S.kc(f, f'{u}_SpdDevAbs', 'AbsValue', {'inA': f'{u}_SpdDev'})
        CMP(S, f, f'{u}_SpdDevHigh', 'GreaterThan', f'{u}_SpdDevAbs', 'VFD_SpeedDevLimit')
        AND(S, f, f'{u}_SpdDevRun', f'{u}_SpdDevHigh', f'{u}RunProof')
        DLY(S, f, f'{u}_SpdDevDly', f'{u}_SpdDevRun', tm(120000, 15000))
        alarm(S, f, f'{u}_SpeedNotFollowingAlarm', f'{u}_SpdDevDly', 'Deviation', 'Normal', 'Warning',
              f'{u} drive speed does not follow the command (check drive local / limit / feedback)')
    # 17 X-01 data source changed while the plant runs
    if 'IO_AnyFieldSts' in S.comp:
        f = fold(S, 'IO_AnyFieldSts')
        DLY(S, f, 'IO_SrcDelayed', 'IO_AnyFieldSts', 3000, 3000)
        NOT(S, f, 'IO_SrcNow0', 'IO_AnyFieldSts'); NOT(S, f, 'IO_SrcDly0', 'IO_SrcDelayed')
        AND(S, f, 'IO_SrcUp', 'IO_AnyFieldSts', 'IO_SrcDly0'); AND(S, f, 'IO_SrcDown', 'IO_SrcNow0', 'IO_SrcDelayed')
        OR(S, f, 'IO_SrcChanged', 'IO_SrcUp', 'IO_SrcDown')
        AND(S, f, 'IO_SrcChangedRun', 'IO_SrcChanged', 'PlantRunRequest')
        sealin(S, f, 'IO_SrcChangedLatch', 'IO_SrcChangedRun', 'FO_Reset')
        alarm(S, f, 'IO_SourceChangedWhileRunningAlarm', 'IO_SrcChangedLatch', 'Changed', 'Normal', 'Warning',
              'SIM / FIELD source changed while the plant was running - check for value jumps; switch with the plant stopped')
    S.log.append(('V7.8r11', 'Improve78', 'remaining SOO items', 'see v78_finish.py', '', ''))


def cx(S):
    f = 'Commissioning/FunctionalTest/RunAll'
    S.kc(f, 'CX_RunCounter', 'Counter', {'countUp': 'CX_RunAllFire'}, note='r11: +1 every RUN ALL')
    S.npoint(f, 'CX_RunId', 'CX_RunCounter', 'none', 0, note='RUN ALL number - write it on the exported report to keep results apart')


def field_io(S):
    r = _fio(S)
    finish(S)
    return r


def commissioning(S):
    r = _cx(S)
    cx(S)
    return r


FCX.field_io = field_io
FCX.commissioning = commissioning
