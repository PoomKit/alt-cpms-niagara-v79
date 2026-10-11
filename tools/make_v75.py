"""Build ALT_CP_Ref_V7_5 = V7.4 (make_v74.py, imported unchanged) + V7.5 layer.

V7.5 (user request 29 Sep 2026 16:25):
  1. CHW pumps keep controlling the END-OF-LOOP DP (water must reach the index circuit) + a second layer:
     LOW DELTA-T SYNDROME GUARD
       - plant delta-T (CHWR - CHWS) below the limit  ->  the DP setpoint is trimmed down slowly (max -30 %, never below DP min)
       - an air-side unit is starving (Trim & Respond requests above 'ignore')  ->  the guard is released (water to the end of
         the loop always wins over delta-T)
       - guard at its limit and delta-T still low for 30 min -> alarm 'check coil valves / 3-way valves / bypass'
     emulation: DP now comes from the pump speed and the building demand (pump + pipe curves) and the coil flow rises with the DP
     (pressure-dependent valves over-flow -> low delta-T), so the guard can be seen working.
     DP sensor validity no longer false-alarms while no CHW pump runs (a stopped loop has 0 kPa).
  2. AI HEARTBEAT, rebuilt as a simple stopwatch
       API arrives -> stopwatch reset to 0 (AI_HeartbeatAgeMin shows the minutes since the last API)
       the time between the last two APIs is measured (AI_HeartbeatIntervalMin) - nobody has to remember the 3rd-party period
       age >= Step 1 (min)  -> PRE-DISCONNECT (warning, AI still in control, last AI setpoints held)
       age >= Step 2 (min)  -> DISCONNECTED   (plant goes to LOCAL; beat counter cleared)
       APIs again           -> RECONNECTING   (needs HB_RequiredBeats new APIs) -> CONNECTED
       one state number AI_LinkState 0 Connected / 1 Pre-disconnect / 2 Disconnected / 3 Reconnecting
       smart checks: Step 2 is always >= Step 1 + 1 min; alarm when Step 1 is shorter than 1.2 x the measured API period
       (would give false pre-disconnects); alarm when the link dropped >= 3 times without 24 h of stable connection
     bumpless AI <-> LOCAL: the CHWST / DP / CDS setpoints glide to the new source at a set rate (no step to the chillers)
New station folder (does not touch V7 .. V7.4).  usage: make_v75.py c_v5.bog c_v5.tsv out.bog --regdir reg75 [--timing fpt]
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_v6 as M6
import make_v7 as M7
import make_v71 as M71
import make_v73 as M73
import make_v74 as M74
from make_v7 import AND, OR, NOT, DLY, SW, MATH, CMP, LIMIT, RATE, PID, PULSE, const, T, F
from make_v73 import unlink
from make_v74 import relink_sim, setprop, drop_if_unused

M6.STATION = M7.STATION = 'ALT_CP_Ref_V7_5'
M7.FOXS_PORT = '4923'
M6.U.setdefault('min', 'units=u:minute;min;(s);*60.0;')
M6.U.setdefault('s', 'units=u:second;s;(s);;')
M6.TIMING['site'].update(dtg_start=600000, dtg_starve_on=30000, dtg_starve_off=900000, dtg_alarm=1800000, dtg_release=0.1,
                         dp_valid_delay=30000, hb_stable=86400000, hb_short=1800000, hb_boot=5000, bl_chwst=0.005, bl_dp=0.25, bl_cds=0.008)
M6.TIMING['fpt'].update(dtg_start=5000, dtg_starve_on=1000, dtg_starve_off=20000, dtg_alarm=20000, dtg_release=2.0,
                        dp_valid_delay=3000, hb_stable=600000, hb_short=20000, hb_boot=5000, bl_chwst=1.0, bl_dp=30.0, bl_cds=1.0)

HY = 'Simulation/Hydraulic'
DG = 'ChwLoop/DeltaTGuard'
H = 'AI_Heartbeat'
MC = 'ModeControl'


# ============================================================ emulation: DP from the pumps + over-flow of the coils
def hydraulic(S, prof):
    S.param('Sim_PumpShutoffDP', 300.0, 'kPa', folder=HY, note='SIM: pump shut-off head at 100 % speed (as DP)')
    S.param('Sim_PumpLossRef', 316.0, 'kPa', folder=HY, note='SIM: head lost in ONE pump at the reference flow (pump curve droop)')
    S.param('Sim_PipeLossRef', 60.0, 'kPa', folder=HY, note='SIM: plant + mains friction to the DP sensor at the reference flow')
    S.param('Sim_FlowRef', 360.0, 'm3h', folder=HY, lo=10, note='SIM: reference (plant design) CHW flow')
    S.param('Sim_CoilDesignDP', 100.0, 'kPa', folder=HY, lo=10, note='SIM: DP at which the air-side valves pass exactly their demand')
    S.param('Sim_LowDtFactor', 1.0, 'none', folder=HY, prec=2, lo=0.3, hi=1.2,
            note='SIM fault injection: coil delta-T x this (0.6 = dirty coils / open 3-way valves -> low delta-T syndrome)')
    const(S, 'Half', 0.5, 'none', 2)
    S.param('Sim_DpLagAlpha', 0.3, 'none', folder=HY, prec=2, note='SIM: DP sensor / pipe first-order lag per second')
    # pump speed (fraction) and number of pumps running
    for n in ('01', '02'):
        MATH(S, HY, f'Sim_CHP{n}_SpeedOnFrac', 'Multiply', f'Sim_CHP{n}_SpeedFrac', f'Sim_CHP{n}_On')
    MATH(S, HY, 'Sim_PumpSpeedFrac', 'Maximum', 'Sim_CHP01_SpeedOnFrac', 'Sim_CHP02_SpeedOnFrac')
    MATH(S, HY, 'Sim_PumpsOn', 'Add', 'Sim_CHP01_On', 'Sim_CHP02_On')
    MATH(S, HY, 'Sim_PumpsOnG', 'Maximum', 'Sim_PumpsOn', 'One')
    MATH(S, HY, 'Sim_PumpsOnSq', 'Multiply', 'Sim_PumpsOnG', 'Sim_PumpsOnG')
    # system: DP = shutoff x s^2 / (1 + X),  X = (pump loss / N^2 + pipe loss) / coil DP x (demand / ref flow)^2
    MATH(S, HY, 'Sim_PumpLossN', 'Divide', 'Sim_PumpLossRef', 'Sim_PumpsOnSq')
    MATH(S, HY, 'Sim_LossRef', 'Add', 'Sim_PumpLossN', 'Sim_PipeLossRef')
    MATH(S, HY, 'Sim_LossRatio', 'Divide', 'Sim_LossRef', 'Sim_CoilDesignDP')
    MATH(S, HY, 'Sim_DemandRatio', 'Divide', 'Sim_BldgDemand', 'Sim_FlowRef')
    MATH(S, HY, 'Sim_SystemX', 'Multiply', 'Sim_LossRatio', 'Sim_DemandRatio', 'Sim_DemandRatio')
    MATH(S, HY, 'Sim_SystemDen', 'Add', 'One', 'Sim_SystemX')
    MATH(S, HY, 'Sim_DpHead', 'Multiply', 'Sim_PumpShutoffDP', 'Sim_PumpSpeedFrac', 'Sim_PumpSpeedFrac')
    MATH(S, HY, 'Sim_DpCalc', 'Divide', 'Sim_DpHead', 'Sim_SystemDen', note='end-of-loop DP (steady state)')
    # first-order lag  y = y_prev + alpha (x - y_prev)   (y_prev = 1 s unit delay)
    S.kc(HY, 'Sim_DpPrev', 'NumericDelay', props=[('maxStepSize', None, '100000.0'), ('updateTime', 'b:RelTime', '1000')])
    MATH(S, HY, 'Sim_DpErr', 'Subtract', 'Sim_DpCalc', 'Sim_DpPrev')
    MATH(S, HY, 'Sim_DpStep', 'Multiply', 'Sim_DpErr', 'Sim_DpLagAlpha')
    S.kc(HY, 'Sim_DpLag', 'Add', {'inA': 'Sim_DpPrev', 'inB': 'Sim_DpStep'})
    S.link(S.comp['Sim_DpPrev'], 'Sim_DpLag', 'in')
    relink_sim(S, 'CHWDP', 'Sim_DpLag', 'end-of-loop DP = pump curve vs system curve (speed, pumps running, building demand)')
    drop_if_unused(S, 'Ramp_CHWDP')
    # coil flow follows the DP (pressure-dependent valves): flow = demand x sqrt(DP / coil design DP)
    MATH(S, HY, 'Sim_DpPos', 'Maximum', 'CHWDP', 'ZeroSpeed')
    MATH(S, HY, 'Sim_DpRatio', 'Divide', 'Sim_DpPos', 'Sim_CoilDesignDP')
    S.kc(HY, 'Sim_OverflowRaw', 'SquareRoot', {'inA': 'Sim_DpRatio'})
    LIMIT(S, HY, 'Sim_Overflow', 'Sim_OverflowRaw', 0.0, 2.0)
    S.npoint(HY, 'Sim_CoilFlowRatio', 'Sim_Overflow', 'none', 2, kind='sim', note='coil flow / demand (>1 = over-flow -> low delta-T)')
    M6.NO_HISTORY.add('Sim_CoilFlowRatio')
    S.link(S.comp['Sim_BldgFlow'], 'Sim_Overflow', 'inC')
    # coil delta-T: over-flow -> dT / ratio (same heat, more water); starved -> dT / sqrt(ratio) (less heat, warmer return)
    S.kc(HY, 'Sim_OverflowSqrt', 'SquareRoot', {'inA': 'Sim_Overflow'})
    MATH(S, HY, 'Sim_DtDivRaw', 'Maximum', 'Sim_Overflow', 'Sim_OverflowSqrt')
    LIMIT(S, HY, 'Sim_DtDivLim', 'Sim_DtDivRaw', 0.3, 2.0)
    CMP(S, HY, 'Sim_LoopFlowing', 'GreaterThan', 'Sim_LoopOn', 'Half')
    SW(S, HY, 'Sim_DtDiv', 'Sim_LoopFlowing', 'Sim_DtDivLim', 'One', note='no loop flow: coil dT not scaled')
    MATH(S, HY, 'Sim_DtFlowFactor', 'Divide', 'Sim_LowDtFactor', 'Sim_DtDiv')
    S.link(S.comp['Sim_CoilDT'], 'Sim_DtFlowFactor', 'inC')
    # air side feels a starved coil: capacity x sqrt(flow ratio) below design flow -> the AHU valve opens further -> T&R request
    MATH(S, HY, 'Sim_CoilCapRaw', 'Minimum', 'Sim_OverflowSqrt', 'One')
    SW(S, HY, 'Sim_CoilCap', 'Sim_LoopFlowing', 'Sim_CoilCapRaw', 'One', note='no loop: legacy air-side emulation (capacity 1)')
    for u in ('AHU01', 'AHU02', 'OAU01'):
        S.link(S.comp[f'Sim_{u}_CoilDrop'], 'Sim_CoilCap', 'inD')
    # DP loop retune for the realistic emulation (was Ki 0.5 /min -> closed-loop time constant ~3 min; 2.0 /min -> ~40 s)
    setprop(S, 'CHWDP_PID', 'integralConstant', '2.0')
    S.log.append(('PROP', '', 'CHWDP_PID', 'integralConstant', '2.0', 'DP loop retuned (start-up value; commissioning tunes on site)'))
    # DP validity: a stopped loop reads ~0 kPa -> judge the sensor only after a CHW pump is proven
    DLY(S, 'PlantControl/SensorValidation', 'CHWDP_PumpProvenDelay', 'Byp_AnyPumpProven', prof['dp_valid_delay'])
    NOT(S, 'PlantControl/SensorValidation', 'CHWDP_NoPumpProven', 'CHWDP_PumpProvenDelay')
    OR(S, 'PlantControl/SensorValidation', 'CHWDP_LowOkOrStopped', 'CHWDPAboveMin', 'CHWDP_NoPumpProven',
       note='below the valid minimum counts as a fault only while a CHW pump is proven')
    S.rewire('CHWDPValid', 'inA', 'CHWDP_LowOkOrStopped', 'CHWDPAboveMin')
    # CHWR validity (the delta-T guard must not act on a failed return sensor): range + not colder than the supply
    SV = 'PlantControl/SensorValidation'
    S.param('CHWR_MinValid', 2.0, 'C', note='CHWR sensor valid range - low'); S.param('CHWR_MaxValid', 35.0, 'C', note='CHWR sensor valid range - high')
    S.param('CHWR_BelowChwsTol', 1.0, 'none', prec=1, note='K: CHWR may read this much below CHWS before it is judged failed')
    CMP(S, SV, 'CHWRAboveMin', 'GreaterThanEqual', 'CHWR', 'CHWR_MinValid')
    CMP(S, SV, 'CHWRBelowMax', 'LessThanEqual', 'CHWR', 'CHWR_MaxValid')
    MATH(S, SV, 'CHWR_LowestOk', 'Subtract', 'CHWS', 'CHWR_BelowChwsTol')
    CMP(S, SV, 'CHWRNotBelowChws', 'GreaterThanEqual', 'CHWR', 'CHWR_LowestOk')
    AND(S, SV, 'CHWRValid', 'CHWRAboveMin', 'CHWRBelowMax', 'CHWRNotBelowChws')
    NOT(S, 'Alarms', 'NotCHWRValid', 'CHWRValid')
    S.bpoint('Alarms', 'CHWR_SensorInvalidAlarm', 'NotCHWRValid', 'Invalid', 'Normal')
    M6.COS['CHWR_SensorInvalidAlarm'] = (True, 'Warning', 'CHWR sensor invalid (range, or colder than CHWS) - delta-T guard off')


# ============================================================ 1. low delta-T syndrome guard (second layer on the DP loop)
def dt_guard(S, prof):
    S.param('DTG_Enable', 1.0, 'none', folder=DG, prec=0, lo=0, hi=1, note='1 = trim the DP setpoint down when the plant delta-T is low')
    S.param('DTG_LowDeltaT', 4.0, 'none', folder=DG, prec=1, lo=1, hi=10, note='K: guard acts below this plant delta-T (design 5.5 K)')
    S.param('DTG_MaxReductionPct', 30.0, 'pct', folder=DG, lo=0, hi=60, note='largest DP setpoint cut (% of the active setpoint)')
    S.param('DTG_StarveRequests', 0.0, 'none', folder=DG, prec=0, note='air side starving when CHW requests are MORE than this (0 = any AHU asking)')
    S.param('DTG_ApplyInAI', 1.0, 'none', folder=DG, prec=0, lo=0, hi=1, note='1 = the guard also trims the AI DP setpoint in AI mode')
    MATH(S, DG, 'DTG_PlantDT', 'Subtract', 'CHWR', 'CHWS')
    S.npoint(DG, 'CHW_PlantDeltaT', 'DTG_PlantDT', 'none', 2, note='K: plant delta-T = CHWR - CHWS (low delta-T syndrome indicator)')
    # enable: plant running (after the start-up period), sensors valid, guard switched on
    CMP(S, DG, 'DTG_On', 'GreaterThanEqual', 'DTG_Enable', 'Half')
    DLY(S, DG, 'DTG_RunDelay', 'PlantPermissive', prof['dtg_start'], note='no guard during the start-up transient')
    CMP(S, DG, 'DTG_InAIOk', 'GreaterThanEqual', 'DTG_ApplyInAI', 'Half')
    OR(S, DG, 'DTG_ModeOk', 'NotOperationModeAI', 'DTG_InAIOk', note='LOCAL mode, or AI mode with DTG_ApplyInAI = 1')
    AND(S, DG, 'DTG_SensorsOk', 'CHWSValid', 'CHWRValid', 'CHWFlowValid')
    AND(S, DG, 'DTG_Ready', 'DTG_On', 'DTG_RunDelay', 'DTG_SensorsOk', 'DTG_ModeOk')
    # air side starving: Trim & Respond requests above 'ignore' -> water must reach the end of the loop first
    CMP(S, DG, 'DTG_StarveQ', 'GreaterThan', 'AirSide_ChwRequests', 'DTG_StarveRequests')
    DLY(S, DG, 'DTG_Starving', 'DTG_StarveQ', prof['dtg_starve_on'], prof['dtg_starve_off'], note='hold 15 min after the last request')
    NOT(S, DG, 'DTG_NotStarving', 'DTG_Starving')
    AND(S, DG, 'DTG_Allowed', 'DTG_Ready', 'DTG_NotStarving')
    # PI: delta-T below the limit -> output rises (0..100 % of the maximum cut)
    PID(S, DG, 'DTG_PI', 'DTG_PlantDT', 'DTG_LowDeltaT', 'DTG_Allowed', 'reverse', 20.0, 1.0, 0.0, 100.0,
        note='reverse: low delta-T -> more cut (20 % per K, integral 1 /min)')
    MATH(S, DG, 'DTG_CutRaw', 'Multiply', 'DTG_PI', 'DTG_MaxReductionPct', 'PctToFrac')
    RATE(S, DG, 'DTG_CutRamp', 'DTG_CutRaw', prof['dtg_release'], note='cut applied slowly (%/s) - no bump on the pumps')
    SW(S, DG, 'DTG_Cut', 'DTG_Starving', 'ZeroSpeed', 'DTG_CutRamp', note='AHU needs water -> the whole cut is removed at once')
    S.npoint(DG, 'CHW_DtGuardCutPct', 'DTG_Cut', 'pct', 1, note='% taken off the active DP setpoint by the delta-T guard')
    # effective DP setpoint = min(ACTIVE, max(ACTIVE x (1 - cut), DP_MinSetpoint))
    MATH(S, DG, 'DTG_CutFrac', 'Multiply', 'DTG_Cut', 'PctToFrac')
    MATH(S, DG, 'DTG_KeepFrac', 'Subtract', 'One', 'DTG_CutFrac')
    MATH(S, DG, 'DTG_SpCut', 'Multiply', 'CHWDP_Setpoint_ACTIVE', 'DTG_KeepFrac')
    MATH(S, DG, 'DTG_SpFloor', 'Maximum', 'DTG_SpCut', 'DP_MinSetpoint', note='never below the plant DP minimum')
    MATH(S, DG, 'DTG_SpEff', 'Minimum', 'CHWDP_Setpoint_ACTIVE', 'DTG_SpFloor')
    S.npoint(DG, 'CHWDP_Setpoint_EFFECTIVE', 'DTG_SpEff', 'kPa', 1, kind='sp', note='DP setpoint used by the CHW pumps (ACTIVE - delta-T guard cut)')
    S.rewire('CHWDP_PID', 'setpoint', 'CHWDP_Setpoint_EFFECTIVE', 'CHWDP_Setpoint_ACTIVE')
    # status for the operator
    S.param('DTG_ActiveBand', 0.5, 'kPa', folder=DG, note='guard shown active when EFFECTIVE is this far below ACTIVE')
    MATH(S, DG, 'DTG_SpBelow', 'Subtract', 'CHWDP_Setpoint_ACTIVE', 'DTG_SpEff')
    CMP(S, DG, 'DTG_Cutting', 'GreaterThan', 'DTG_SpBelow', 'DTG_ActiveBand', note='the DP setpoint really is lower than ACTIVE')
    S.bpoint(DG, 'CHW_DtGuardActive', 'DTG_Cutting', 'Reducing DP', 'Normal', note='the guard is holding the DP setpoint below ACTIVE')
    AND(S, DG, 'DTG_StarveShow', 'DTG_Ready', 'DTG_Starving')
    S.bpoint(DG, 'CHW_DtGuardHeld', 'DTG_StarveShow', 'Held - AHU needs water', 'Normal', note='air side starving: no DP cut allowed')
    CMP(S, DG, 'DTG_LowNow', 'LessThan', 'DTG_PlantDT', 'DTG_LowDeltaT')
    MATH(S, DG, 'DTG_CutLimit', 'Subtract', 'DTG_MaxReductionPct', 'Half')
    CMP(S, DG, 'DTG_AtMax', 'GreaterThanEqual', 'DTG_Cut', 'DTG_CutLimit')
    CMP(S, DG, 'DTG_AtFloor', 'LessThanEqual', 'DTG_SpCut', 'DP_MinSetpoint')
    OR(S, DG, 'DTG_NoMoreCut', 'DTG_AtMax', 'DTG_AtFloor')
    AND(S, DG, 'DTG_LimitLow', 'DTG_Allowed', 'DTG_Cutting', 'DTG_NoMoreCut', 'DTG_LowNow')
    DLY(S, 'Alarms', 'DTG_LimitDelay', 'DTG_LimitLow', prof['dtg_alarm'])
    S.bpoint('Alarms', 'CHW_LowDtPersistAlarm', 'DTG_LimitDelay', 'Alarm', 'Normal')
    M6.COS['CHW_LowDtPersistAlarm'] = (True, 'Warning', 'Low CHW delta-T persists with the DP setpoint already cut to its limit - check coil valves / 3-way valves / bypass / coil fouling')
    # state number for graphics: 0 off / 1 normal / 2 reducing / 3 held (starving)
    SW(S, DG, 'DTG_State1', 'DTG_Ready', 'One', 'ZeroSpeed')
    const(S, 'Two', 2.0, 'none', 0); const(S, 'Three', 3.0, 'none', 0)
    SW(S, DG, 'DTG_State2', 'DTG_Cutting', 'Two', 'DTG_State1')
    SW(S, DG, 'DTG_State3', 'DTG_StarveShow', 'Three', 'DTG_State2')
    S.npoint(DG, 'CHW_DtGuardState', 'DTG_State3', 'none', 0, note='0 off / 1 normal / 2 reducing DP / 3 held (AHU needs water)')
    M6.NO_HISTORY.discard('CHW_DtGuardState')


# ============================================================ 2. AI heartbeat = stopwatch with two steps
def heartbeat(S, prof):
    S.param('HB_Step1_PreDisconnectMin', 6.0, 'min', folder=H, prec=1, lo=1, hi=120, note='no API for this long -> PRE-DISCONNECT (warning, AI kept)')
    S.param('HB_Step2_DisconnectMin', 12.0, 'min', folder=H, prec=1, lo=2, hi=240, note='no API for this long -> DISCONNECTED (plant to LOCAL)')
    S.param('HB_UnstableDrops', 3.0, 'none', folder=H, prec=0, note='link drops without 24 h of stable connection -> unstable alarm')
    const(S, 'SecPerMin', 60.0, 'none', 0)
    const(S, 'HB_PeriodMargin', 1.2, 'none', 2)
    # change detection without a sampling clock: new value -> HB_Changed -> 1.5 s pulse -> at the END of the pulse the value is
    # latched (HB_Changed clears).  No API can be missed (the old 60 s sample clock lost an API that arrived on its edge).
    S.kc(H, 'HB_SecondClock', 'MultiVibrator', props=[('period', None, '1000'), ('dutyCycle', None, '50.0')])
    PULSE(S, H, 'HB_BeatPulse', 'HB_Changed', 1500, note='one pulse per API received')
    NOT(S, H, 'HB_BeatPulseEnd', 'HB_BeatPulse')
    S.rewire('HB_LastSample', 'clock', 'HB_BeatPulseEnd', 'HB_SampleClock')
    drop_if_unused(S, 'HB_SampleClock')
    # stopwatch: counts seconds, reset at the end of the pulse (the interval latch reads it at the start)
    S.kc(H, 'HB_AgeCounter', 'Counter', {'countUp': 'HB_SecondClock', 'clearIn': 'HB_BeatPulseEnd'}, note='seconds since the last API')
    const(S, 'HB_PulseSec', 1.5, 'none', 1, note='the stopwatch restarts 1.5 s after the API (end of the pulse)')
    MATH(S, H, 'HB_AgeSec', 'Add', 'HB_AgeCounter', 'HB_PulseSec', note='seconds since the last API')
    S.kc(H, 'HB_IntervalLatch', 'NumericLatch', {'in': 'HB_AgeSec', 'clock': 'HB_BeatPulse'}, note='seconds between the last two APIs')
    MATH(S, H, 'HB_AgeMinCalc', 'Divide', 'HB_AgeSec', 'SecPerMin')
    S.npoint(H, 'AI_HeartbeatAgeMin', 'HB_AgeMinCalc', 'min', 1, note='minutes since the last API from the AI (stopwatch)')
    MATH(S, H, 'HB_IntervalMinCalc', 'Divide', 'HB_IntervalLatch', 'SecPerMin')
    S.npoint(H, 'AI_HeartbeatIntervalMin', 'HB_IntervalMinCalc', 'min', 1, note='measured time between the last two APIs (3rd-party period)')
    # the two steps (seconds); Step 2 is always at least Step 1 + 1 min
    MATH(S, H, 'HB_Step1Sec', 'Multiply', 'HB_Step1_PreDisconnectMin', 'SecPerMin')
    MATH(S, H, 'HB_Step2SecSet', 'Multiply', 'HB_Step2_DisconnectMin', 'SecPerMin')
    MATH(S, H, 'HB_Step1Plus', 'Add', 'HB_Step1Sec', 'SecPerMin')
    MATH(S, H, 'HB_Step2Sec', 'Maximum', 'HB_Step2SecSet', 'HB_Step1Plus', note='Step 2 never shorter than Step 1 + 1 min')
    CMP(S, H, 'HB_Step1Reached', 'GreaterThanEqual', 'HB_AgeSec', 'HB_Step1Sec')
    CMP(S, H, 'HB_Step2Reached', 'GreaterThanEqual', 'HB_AgeSec', 'HB_Step2Sec')
    # beats needed to (re)connect: counter cleared when Step 2 is reached
    # station restart: forget the APIs counted before the restart -> AI only after HB_RequiredBeats FRESH APIs
    DLY(S, H, 'HB_BootDone', 'ConstantTrue', prof['hb_boot'], note='rising edge 5 s after the station starts')
    PULSE(S, H, 'HB_BootPulse', 'HB_BootDone', 2000, note='one pulse after the start (a level would mask the Step 2 edge)')
    OR(S, H, 'HB_BeatClear', 'HB_Step2Reached', 'HB_BootPulse', note='APIs counted again after a disconnect or a station restart')
    S.rewire('HB_BeatCounter', 'clearIn', 'HB_BeatClear', 'HB_DisconnectDelay')
    NOT(S, H, 'HB_NotStep2', 'HB_Step2Reached')
    AND(S, H, 'HB_Ok', 'HB_EnoughBeats', 'HB_NotStep2', note='AI usable: enough APIs since the last disconnect and not past Step 2')
    S.rewire('HeartbeatDetectorStatus', 'in16', 'HB_Ok', 'HB_OkLogic')
    S.rewire('HeartbeatPreDisconnect', 'in16', 'HB_Step1Reached', 'HB_NotRecent')
    S.rewire('AI_AvailableLogic', 'inA', 'HB_Ok', 'HB_OkLogic')
    for n in ('HB_OkLogic', 'HB_NotDisconnected', 'HB_DisconnectDelay', 'HB_NotRecent', 'HB_Recent'):
        drop_if_unused(S, n)
    # link states (one true at a time)
    NOT(S, H, 'HB_NotStep1', 'HB_Step1Reached')
    NOT(S, H, 'HB_NotOk', 'HB_Ok')
    AND(S, H, 'HB_StConnected', 'HB_Ok', 'HB_NotStep1')
    AND(S, H, 'HB_StPre', 'HB_Ok', 'HB_Step1Reached')
    AND(S, H, 'HB_StReconnecting', 'HB_NotOk', 'HB_NotStep2')
    S.bpoint(H, 'AI_Link_Connected', 'HB_StConnected', 'Connected', '-')
    S.bpoint(H, 'AI_Link_PreDisconnect', 'HB_StPre', 'Pre-disconnect', '-')
    S.bpoint(H, 'AI_Link_Disconnected', 'HB_Step2Reached', 'Disconnected', '-')
    S.bpoint(H, 'AI_Link_Reconnecting', 'HB_StReconnecting', 'Reconnecting', '-')
    const(S, 'Two', 2.0, 'none', 0); const(S, 'Three', 3.0, 'none', 0)
    SW(S, H, 'HB_State1', 'HB_StPre', 'One', 'ZeroSpeed')
    SW(S, H, 'HB_State2', 'HB_Step2Reached', 'Two', 'HB_State1')
    SW(S, H, 'HB_State3', 'HB_StReconnecting', 'Three', 'HB_State2')
    const(S, 'FiftyPct', 50.0, 'pct', 0)
    S.kc(H, 'HB_BarA', 'Reset', {'inA': 'HB_AgeSec', 'inputLowLimit': 'ZeroSpeed', 'inputHighLimit': 'HB_Step1Sec',
                                 'outputLowLimit': 'ZeroSpeed', 'outputHighLimit': 'FiftyPct'})
    S.kc(H, 'HB_BarB', 'Reset', {'inA': 'HB_AgeSec', 'inputLowLimit': 'HB_Step1Sec', 'inputHighLimit': 'HB_Step2Sec',
                                 'outputLowLimit': 'FiftyPct', 'outputHighLimit': 'HundredPct'})
    SW(S, H, 'HB_BarSel', 'HB_Step1Reached', 'HB_BarB', 'HB_BarA')
    S.npoint(H, 'AI_HeartbeatTimerPct', 'HB_BarSel', 'pct', 0, note='stopwatch bar: 50 % = Step 1 (pre-disconnect), 100 % = Step 2 (disconnect)')
    S.npoint(H, 'AI_LinkState', 'HB_State3', 'none', 0, note='0 Connected / 1 Pre-disconnect / 2 Disconnected / 3 Reconnecting')
    S.npoint(H, 'AI_HeartbeatBeats', 'HB_BeatCounter', 'none', 0, note='APIs received since the last disconnect')
    # smart check 1: Step 1 shorter than the real API period (x 1.2) -> false pre-disconnects
    MATH(S, H, 'HB_PeriodWithMargin', 'Multiply', 'HB_IntervalLatch', 'HB_PeriodMargin')
    const(S, 'HB_PeriodTolSec', 15.0, 'none', 0, note='tolerance: Step 1 = 6 min with a 5 min period is accepted')
    MATH(S, H, 'HB_Step1Tol', 'Add', 'HB_Step1Sec', 'HB_PeriodTolSec')
    CMP(S, H, 'HB_Step1TooShortQ', 'LessThan', 'HB_Step1Tol', 'HB_PeriodWithMargin')
    AND(S, H, 'HB_Step1TooShort', 'HB_Step1TooShortQ', 'HB_EnoughBeats')
    DLY(S, H, 'HB_Step1TooShortDelay', 'HB_Step1TooShort', prof['hb_short'], note='one late API does not alarm; a real period mismatch does')
    S.bpoint('Alarms', 'AI_HeartbeatStep1TooShortAlarm', 'HB_Step1TooShortDelay', 'Step 1 < API period', 'Normal')
    M6.COS['AI_HeartbeatStep1TooShortAlarm'] = (True, 'Warning', 'AI heartbeat Step 1 is shorter than 1.2 x the measured API period - raise HB_Step1_PreDisconnectMin')
    # smart check 2: link flapping (drops counted until 24 h of stable connection)
    DLY(S, H, 'HB_StableLong', 'HB_StConnected', prof['hb_stable'], note='24 h connected without a break')
    S.kc(H, 'HB_DropCounter', 'Counter', {'countUp': 'HB_Step2Reached', 'clearIn': 'HB_StableLong'}, note='disconnects since the last 24 h stable')
    S.npoint(H, 'AI_LinkDrops', 'HB_DropCounter', 'none', 0, note='AI link drops since the last 24 h of stable connection')
    CMP(S, H, 'HB_UnstableQ', 'GreaterThanEqual', 'HB_DropCounter', 'HB_UnstableDrops')
    S.bpoint('Alarms', 'AI_LinkUnstableAlarm', 'HB_UnstableQ', 'Unstable', 'Normal')
    M6.COS['AI_LinkUnstableAlarm'] = (True, 'Warning', 'AI link dropped repeatedly - check the 3rd-party API service / network')
    S.bpoint('Alarms', 'AI_HeartbeatPreDisconnectAlarm', 'HB_StPre', 'Pre-disconnect', 'Normal')
    M6.COS['AI_HeartbeatPreDisconnectAlarm'] = (True, 'Warning', 'AI heartbeat late (Step 1) - AI still in control, holding the last AI setpoints')


# ============================================================ bumpless AI <-> LOCAL
def bumpless(S, prof):
    """ACTIVE = anchor + rate-limited (selected - anchor): every change of the setpoint sent to the plant is gradual - AI <-> LOCAL
    transfer, AI steps, optimiser on/off, OA-sensor fallback.  Anchor = the safe (maximum) value -> after a restart the setpoint
    starts safe (warm CHWST, high DP, warm CDS) and glides to the selected value (soft start)."""
    for base, anchor, rate, note in (('Chwst', 'CHWST_MaxSetpoint', prof['bl_chwst'], 'K/s'), ('Dp', 'DP_MaxSetpoint', prof['bl_dp'], 'kPa/s'),
                                     ('Cds', 'CDW_MaxSetpoint', prof['bl_cds'], 'K/s')):
        MATH(S, MC, f'{base}XferDiff', 'Subtract', f'{base}ActiveSelect', anchor, note='selected source - safe anchor')
        RATE(S, MC, f'{base}XferGlide', f'{base}XferDiff', rate, note=f'setpoint slew limit {rate:g} {note}')
        MATH(S, MC, f'{base}XferOut', 'Add', anchor, f'{base}XferGlide')
        S.rewire(f'{base}ActiveClamp', 'inA', f'{base}XferOut', f'{base}ActiveSelect')


# ============================================================ graphics support
def gfx75(S, prof):
    GFL = 'Graphics/Flow'
    CMP(S, GFL, 'Gfx_AiLinkBad', 'GreaterThanEqual', 'AI_LinkState', 'One')
    S.bpoint(GFL, 'Gfx_AiLinkNotOk', 'Gfx_AiLinkBad', 'Check', 'OK')
    M6.NO_HISTORY.add('Gfx_AiLinkNotOk')


def v75(S, prof):
    M74._v73(S, prof)
    M74.load_balance(S, prof)
    M74.thermal(S, prof)
    M74.bypass_tune(S, prof)
    M74.valve_gfx(S, prof)
    M74.flow_gfx(S, prof)
    hydraulic(S, prof)
    dt_guard(S, prof)
    heartbeat(S, prof)
    bumpless(S, prof)
    gfx75(S, prof)
    if os.environ.get('UNITS_REPORT'):
        import units74, json
        q, rep = units74.report(S)
        with open(os.environ['UNITS_REPORT'], 'w') as f:
            json.dump({'q': q, 'boundary': rep}, f, indent=1)
    M74.units(S, prof)


M71.v71 = v75
_px = [n for _, n in M7.PX_PLANT]
M7.PX_PLANT.insert(_px.index('ALT_CP_Optimization') + 1 if 'ALT_CP_Optimization' in _px else len(_px), ('AiDtGuard', 'ALT_V75_AiDtGuard'))

# reproducible .bog: fixed zip entry time (review finding) - the file.xml content was already deterministic
import zipfile as _zf
_writestr = _zf.ZipFile.writestr


def _writestr_fixed(self, zinfo_or_arcname, data, *a, **kw):
    if isinstance(zinfo_or_arcname, str):
        zi = _zf.ZipInfo(zinfo_or_arcname, date_time=(2026, 9, 29, 0, 0, 0))
        zi.compress_type = self.compression
        return _writestr(self, zi, data, *a, **kw)
    return _writestr(self, zinfo_or_arcname, data, *a, **kw)


_zf.ZipFile.writestr = _writestr_fixed

if __name__ == '__main__':
    M7.main()
