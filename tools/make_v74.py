"""Build ALT_CP_Ref_V7_4 = V7.3 (make_v73.py, imported unchanged) + V7.4 layer.

V7.4 (user request 29 Sep 2026 13:00):
  1. Coherent plant emulation (energy balance): the independent CHWS / CHWR / CHW flow / chiller-load ramps are replaced by ONE
     thermal-hydraulic model so that   sum(chiller RT) = plant RT   and   plant kW/RT >= chiller kW/RT.
       building flow  = air-side valves (AHU/OAU modulating, FCU on/off) + rest-of-building demand       -> CHWFlow (main FT)
       bypass flow    = min-flow valve feedback x Kv (+ manual bypass loop)                               -> evaporator flow
       evap flow      = building + bypass, split between the chillers on line (equal FCVs, optional bias)
       chiller LWT    = its own setpoint command (common SP + load-balance trim); EWT = building return mixed with bypass
       chiller RT     = flow x (EWT - LWT);  load % = RT / rated;  kW = rated x part-load curve x lift factor
       condenser      = CDR = CDS + (RT + kW) / CDW flow
  2. Equal loading: per-chiller LWT setpoint command = plant CHWST SP + load-balance trim (PI on load % vs average, +/-0.5 K)
     + imbalance alarm; FCVs on line are equal -> equal evaporator flow.
  3. Min-flow bypass valve opens slowly (rate limit) to keep sum of evaporator flows >= min flow x margin when the
     air-side valves close (emulation now closes the loop: valve -> bypass flow -> evaporator flow).
New station folder (does not touch V7 .. V7.3).  usage: make_v74.py c_v5.bog c_v5.tsv out.bog --regdir reg74 [--timing fpt]
"""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_v6 as M6
import make_v7 as M7
import make_v71 as M71
import make_v73 as M73
from make_v7 import AND, OR, NOT, DLY, SW, MATH, CMP, LIMIT, RATE, PID, const, ai, di, simlink, ramp, T, F, UNITS
from make_v73 import unlink, consumers

M6.STATION = M7.STATION = 'ALT_CP_Ref_V7_4'
M7.FOXS_PORT = '4922'
M6.TIMING['site'].update(ch_balance_alarm=600000)
M6.TIMING['fpt'].update(ch_balance_alarm=5000)

TH = 'Simulation/Thermal'
LB = 'ChwLoop/LoadBalance'


def relink_sim(S, target, src, note):
    """replace the emulation source (in10) of a measured point"""
    if any(M6.child(L, 'targetSlotName').get('v') == 'in10' for L in S.comp[target] if L.get('t') == 'b:Link'):
        unlink(S, target, 'in10')
    simlink(S, target, src, note)


def setprop(S, comp, prop, v):
    e = M6.child(S.comp[comp], prop)
    if e is None:
        import xml.etree.ElementTree as ET
        e = ET.SubElement(S.comp[comp], 'p', {'n': prop})
    e.set('v', v)


def drop_if_unused(S, *names):
    for n in names:
        if n in S.comp and not consumers(S, n):
            M6.remove_comp(S, n)


# ============================================================ 2. equal loading (control)
def load_balance(S, prof):
    S.param('CH_BalanceEnable', 1.0, 'none', folder=LB, prec=0, lo=0, hi=1, note='1 = trim each chiller LWT SP to equalise % load')
    S.param('CH_BalanceMaxTrim', 0.5, 'none', folder=LB, prec=2, lo=0, hi=1.5, note='K: max LWT setpoint offset per chiller')
    S.param('CH_BalanceAlarmPct', 15.0, 'pct', folder=LB, lo=5, hi=50, note='alarm when % load differs more than this')
    const(S, 'Half', 0.5, 'none', 2)
    const(S, 'PctToFrac', 0.01, 'none', 3)
    AND(S, LB, 'CH_BothRunning', 'CH01RunProofSelected', 'CH02RunProofSelected')
    CMP(S, LB, 'CH_BalanceOn', 'GreaterThanEqual', 'CH_BalanceEnable', 'Half')
    AND(S, LB, 'CH_BalanceActive', 'CH_BothRunning', 'CH_BalanceOn')
    MATH(S, LB, 'CH_LoadSum', 'Add', 'CH01LoadPct', 'CH02LoadPct')
    MATH(S, LB, 'CH_LoadAvg', 'Multiply', 'CH_LoadSum', 'Half', note='2-chiller average (balancing set point, used only with both on line)')
    SW(S, LB, 'CH_Run01Num', 'CH01RunProofSelected', 'One', 'ZeroSpeed'); SW(S, LB, 'CH_Run02Num', 'CH02RunProofSelected', 'One', 'ZeroSpeed')
    MATH(S, LB, 'CH_RunNum', 'Add', 'CH_Run01Num', 'CH_Run02Num'); MATH(S, LB, 'CH_RunNumG', 'Maximum', 'CH_RunNum', 'One')
    MATH(S, LB, 'CH_LoadAvgOnLine', 'Divide', 'CH_LoadSum', 'CH_RunNumG')
    S.npoint(f'{LB}', 'CH_LoadAveragePct', 'CH_LoadAvgOnLine', 'pct', 1, note='average % load of the chillers on line')
    MATH(S, LB, 'CH_LoadDiff', 'Subtract', 'CH01LoadPct', 'CH02LoadPct')
    S.kc(LB, 'CH_LoadDiffAbs', 'AbsValue', {'inA': 'CH_LoadDiff'})
    S.npoint(LB, 'CH_LoadImbalancePct', 'CH_LoadDiffAbs', 'pct', 1, note='|CH01 % load - CH02 % load|')
    CMP(S, LB, 'CH_ImbalanceHigh', 'GreaterThan', 'CH_LoadDiffAbs', 'CH_BalanceAlarmPct')
    AND(S, LB, 'CH_ImbalanceLogic', 'CH_ImbalanceHigh', 'CH_BothRunning')
    DLY(S, 'Alarms', 'CH_ImbalanceDelay', 'CH_ImbalanceLogic', prof['ch_balance_alarm'])
    S.bpoint('Alarms', 'CH_LoadImbalanceAlarm', 'CH_ImbalanceDelay', 'Unequal', 'Normal')
    M6.COS['CH_LoadImbalanceAlarm'] = (True, 'Warning', 'Chillers on line not equally loaded (check FCV / flow / setpoint trim)')
    MATH(S, LB, 'CH_FlowSum', 'Add', 'CH01_ChwFlow', 'CH02_ChwFlow')
    MATH(S, LB, 'CH_FlowAvg', 'Multiply', 'CH_FlowSum', 'Half')
    for n in UNITS:
        c = f'CH{n}'
        # PI: load above average -> positive trim -> LWT setpoint raised -> this chiller sheds load
        S.kc(LB, f'{c}BalancePI', 'LoopPoint', {'controlledVariable': f'{c}LoadPct', 'setpoint': 'CH_LoadAvg', 'loopEnable': 'CH_BalanceActive'},
             props=[('loopAction', None, 'direct'), ('proportionalConstant', None, '0.8'), ('integralConstant', None, '2.0'), ('maximumOutput', None, '100.0'),
                    ('minimumOutput', None, '-100.0')], note='-100..+100 % of the max trim')
        MATH(S, LB, f'{c}BalanceTrimRaw', 'Multiply', f'{c}BalancePI', 'CH_BalanceMaxTrim', 'PctToFrac', note='trim K = PI % x max trim')
        SW(S, LB, f'{c}BalanceTrim', 'CH_BalanceActive', f'{c}BalanceTrimRaw', 'ZeroSpeed')
        S.npoint(LB, f'{c}_LwtTrim', f'{c}BalanceTrim', 'none', 2, note='K added to the plant CHWST SP for this chiller')
        MATH(S, LB, f'{c}ChwSpCalc', 'Add', 'CHW_LeavingTemperatureSetpoint_ACTIVE', f'{c}BalanceTrim')
        S.npoint(f'Chiller{n}/Points', f'{c}_ChwSetpointCmd', f'{c}ChwSpCalc', 'C', 2, kind='ao',
                 note='BACnet write to the chiller: leaving CHW setpoint = plant SP + load-balance trim')
        # equal evaporator flow: the chiller with MORE flow than the average throttles its outlet FCV (PI 0..60 %)
        S.kc(LB, f'{c}FlowBalancePI', 'LoopPoint', {'controlledVariable': f'{c}_ChwFlow', 'setpoint': 'CH_FlowAvg', 'loopEnable': 'CH_BalanceActive'},
             props=[('loopAction', None, 'direct'), ('proportionalConstant', None, '0.5'), ('integralConstant', None, '3.0'),
                    ('maximumOutput', None, '60.0'), ('minimumOutput', None, '0.0')], note='flow above average -> throttle % on the FCV')
        S.npoint(LB, f'{c}_FcvBalanceThrottle', f'{c}FlowBalancePI', 'pct', 1, note='FCV closing for equal evaporator flow')
        SW(S, LB, f'{c}FlowBalanceGate', 'CH_BalanceActive', f'{c}FlowBalancePI', 'ZeroSpeed', note='no throttle unless both chillers run')
        MATH(S, LB, f'{c}FcvLoopBal', 'Subtract', f'{c}FcvLoop', f'{c}FlowBalanceGate')
        S.rewire(f'{c}FcvAboveMin', 'inA', f'{c}FcvLoopBal', f'{c}FcvLoop')


# ============================================================ 1 / 3. coherent thermal-hydraulic emulation
def thermal(S, prof):
    # --- design / emulation constants (PROJECT values replace these on a real site; they only drive the emulation)
    S.param('Sim_AhuDesignFlow', 45.0, 'm3h', folder=TH, note='SIM: AHU CHW coil design flow at 100 % valve')
    S.param('Sim_OauDesignFlow', 30.0, 'm3h', folder=TH, note='SIM: OAU CHW coil design flow at 100 % valve')
    S.param('Sim_FcuDesignFlow', 2.5, 'm3h', folder=TH, note='SIM: FCU CHW flow (on/off valve)')
    S.param('Sim_BypFlowPerPct', 1.6, 'm3h', folder=TH, note='SIM: min-flow bypass valve flow per % open')
    S.param('Sim_ManualBypFlow', 60.0, 'm3h', folder=TH, note='SIM: flow through the manual bypass loop when open')
    S.param('Sim_ChFlowBias', 0.0, 'none', folder=TH, prec=2, lo=-0.3, hi=0.3,
            note='SIM: evaporator flow imbalance (+0.1 = CH01 gets 10 % more flow) - test the load balancing')
    S.param('Sim_ChwIdleTemp', 14.0, 'C', folder=TH, note='SIM: CHW temperature with no chiller running')
    S.param('Sim_CH_PLFixed', 0.12, 'none', folder=TH, prec=2, note='SIM: chiller kW at zero load / rated kW')
    S.param('Sim_CH_PLVar', 0.88, 'none', folder=TH, prec=2, note='SIM: 1 - fixed share')
    S.param('Sim_CH_DesignLift', 22.0, 'none', folder=TH, note='SIM: K (CDS - LWT) at rated efficiency')
    S.param('Sim_CH_LiftCoef', 0.02, 'none', folder=TH, prec=3, note='SIM: kW change per K of lift above design')
    const(S, 'Tiny', 0.001, 'none', 3)
    ramp(S, 'Sim_OtherBldgFlow', 'Ramp', 3600000, 80.0, 100.0, 'm3h')            # rest of the building 20..180 m3/h / 60 min
    ramp(S, 'Sim_BldgDeltaT', 'SineWave', 2400000, 0.7, 5.3, 'none')              # coil delta-T 4.6..6.0 K
    # --- building (air side) flow
    MATH(S, TH, 'Sim_AhuFlowPct', 'Add', 'AHU01_ValveFeedback', 'AHU02_ValveFeedback')
    MATH(S, TH, 'Sim_AhuFlow', 'Multiply', 'Sim_AhuFlowPct', 'Sim_AhuDesignFlow', 'PctToFrac')
    MATH(S, TH, 'Sim_OauFlow', 'Multiply', 'OAU01_ValveFeedback', 'Sim_OauDesignFlow', 'PctToFrac')
    MATH(S, TH, 'Sim_FcuOnCount', 'Add', 'Sim_FCU01_ValveOn', 'Sim_FCU02_ValveOn', 'Sim_FCU03_ValveOn', 'Sim_FCU04_ValveOn')
    MATH(S, TH, 'Sim_FcuFlow', 'Multiply', 'Sim_FcuOnCount', 'Sim_FcuDesignFlow')
    MATH(S, TH, 'Sim_BldgDemand', 'Add', 'Sim_AhuFlow', 'Sim_OauFlow', 'Sim_FcuFlow', 'Sim_OtherBldgFlow')
    # a path exists only with a CHW pump running and at least one chiller isolation path open
    MATH(S, TH, 'Sim_ChwPumpOn', 'Maximum', 'Sim_CHP01_On', 'Sim_CHP02_On')
    MATH(S, TH, 'Sim_ChwPathOn', 'Maximum', 'Sim_CH01_ChwOn', 'Sim_CH02_ChwOn')
    MATH(S, TH, 'Sim_LoopOn', 'Multiply', 'Sim_ChwPumpOn', 'Sim_ChwPathOn')
    MATH(S, TH, 'Sim_BldgFlow', 'Multiply', 'Sim_BldgDemand', 'Sim_LoopOn')
    relink_sim(S, 'CHWFlow', 'Sim_BldgFlow', 'building flow = air-side valves + rest of building')
    # --- bypass + evaporator flow (uses the MEASURED main flow so FPT overrides of CHWFlow still drive the plant)
    MATH(S, TH, 'Sim_BypModFlow', 'Multiply', 'CHW_BypassValveFeedback', 'Sim_BypFlowPerPct')
    SW(S, TH, 'Sim_BypManFlow', 'CHW_BypassManualOpen', 'Sim_ManualBypFlow', 'ZeroSpeed')
    MATH(S, TH, 'Sim_BypFlowRaw', 'Add', 'Sim_BypModFlow', 'Sim_BypManFlow')
    MATH(S, TH, 'Sim_BypFlow', 'Multiply', 'Sim_BypFlowRaw', 'Sim_LoopOn')
    S.npoint(TH, 'Sim_BypassFlowCalc', 'Sim_BypFlow', 'm3h', 1, kind='sim', note='emulated bypass flow (no meter on site)')
    M6.NO_HISTORY.add('Sim_BypassFlowCalc')
    MATH(S, TH, 'Sim_MainFlowOn', 'Multiply', 'CHWFlow', 'Sim_LoopOn')
    MATH(S, TH, 'Sim_EvapFlow', 'Add', 'Sim_MainFlowOn', 'Sim_BypFlow')
    MATH(S, TH, 'Sim_EvapFlowGuard', 'Maximum', 'Sim_EvapFlow', 'Tiny')
    # split between the chillers whose isolation path is open (equal FCVs; optional bias)
    MATH(S, TH, 'Sim_BiasPos', 'Add', 'One', 'Sim_ChFlowBias')
    MATH(S, TH, 'Sim_BiasNeg', 'Subtract', 'One', 'Sim_ChFlowBias')
    MATH(S, TH, 'Sim_CH01_W', 'Multiply', 'Sim_CH01_ChwOn', 'Sim_BiasPos', 'CH01_ChwFCVFb', 'PctToFrac')
    MATH(S, TH, 'Sim_CH02_W', 'Multiply', 'Sim_CH02_ChwOn', 'Sim_BiasNeg', 'CH02_ChwFCVFb', 'PctToFrac')
    MATH(S, TH, 'Sim_CH_WSum', 'Add', 'Sim_CH01_W', 'Sim_CH02_W')
    MATH(S, TH, 'Sim_CH_WGuard', 'Maximum', 'Sim_CH_WSum', 'Tiny')
    for n in UNITS:
        c = f'CH{n}'
        MATH(S, TH, f'Sim_{c}_FlowFrac', 'Divide', f'Sim_{c}_W', 'Sim_CH_WGuard')
        MATH(S, TH, f'Sim_{c}_EvapFlowT', 'Multiply', 'Sim_EvapFlow', f'Sim_{c}_FlowFrac')
        S.rewire(f'Sim_{c}_ChwFlow', 'inA', f'Sim_{c}_EvapFlowT', 'Sim_ChwFlowShare')
        S.rewire(f'Sim_{c}_ChwFlow', 'inB', 'One', f'Sim_{c}_ChwOn')
    # --- temperatures.  CHWS (header) lags the chiller outlets 0.1 K/s (breaks the algebraic loop, like pipe transport)
    SW(S, TH, 'Sim_ChwsForReturn', 'Sim_LoopOn', 'CHWS', 'Sim_ChwIdleTemp')
    # coil heat transfer falls as the chilled water warms: dT = design dT x (air - CHWS) / (air - design CHWS)  (stable, no runaway)
    S.param('Sim_CoilAirTemp', 24.0, 'C', folder=TH, note='SIM: average coil entering-air temperature')
    S.param('Sim_CoilDesignChws', 7.0, 'C', folder=TH, note='SIM: CHWS at which the coil delta-T equals the design value')
    MATH(S, TH, 'Sim_CoilDrive', 'Subtract', 'Sim_CoilAirTemp', 'Sim_ChwsForReturn')
    MATH(S, TH, 'Sim_CoilDriveDesign', 'Subtract', 'Sim_CoilAirTemp', 'Sim_CoilDesignChws')
    MATH(S, TH, 'Sim_CoilFactorRaw', 'Divide', 'Sim_CoilDrive', 'Sim_CoilDriveDesign')
    LIMIT(S, TH, 'Sim_CoilFactor', 'Sim_CoilFactorRaw', 0, 1.5)
    MATH(S, TH, 'Sim_CoilDT', 'Multiply', 'Sim_BldgDeltaT', 'Sim_CoilFactor')
    MATH(S, TH, 'Sim_CHWRCalc', 'Add', 'Sim_ChwsForReturn', 'Sim_CoilDT', note='building return = supply + coil delta-T')
    relink_sim(S, 'CHWR', 'Sim_CHWRCalc', 'building return (before bypass mixing)')
    # EWT = (main x CHWR + bypass x CHWS) / evap  (uses measured CHWS / CHWR -> FPT overrides stay effective)
    MATH(S, TH, 'Sim_EwtMainHeat', 'Multiply', 'Sim_MainFlowOn', 'CHWR')
    MATH(S, TH, 'Sim_EwtBypHeat', 'Multiply', 'Sim_BypFlow', 'CHWS')
    MATH(S, TH, 'Sim_EwtHeat', 'Add', 'Sim_EwtMainHeat', 'Sim_EwtBypHeat')
    MATH(S, TH, 'Sim_EwtMix', 'Divide', 'Sim_EwtHeat', 'Sim_EvapFlowGuard')
    CMP(S, TH, 'Sim_EvapFlowing', 'GreaterThan', 'Sim_EvapFlow', 'One')
    S.kc(TH, 'Sim_EWT', 'NumericSwitch', {'inSwitch': 'Sim_EvapFlowing', 'inTrue': 'Sim_EwtMix', 'inFalse': 'CHWR'})
    S.npoint(TH, 'Sim_EvapEnteringTemp', 'Sim_EWT', 'C', 2, kind='sim', note='emulated chiller entering temperature (after bypass)')
    M6.NO_HISTORY.add('Sim_EvapEnteringTemp')
    S.param('Sim_CH_MaxCapPct', 105.0, 'pct', folder=TH, note='SIM: chiller maximum capacity % of rated')
    MATH(S, TH, 'Sim_CH_CapRT', 'Multiply', 'CH_RatedRT', 'Sim_CH_MaxCapPct', 'PctToFrac')
    MATH(S, TH, 'Sim_CH_CapKW', 'Multiply', 'Sim_CH_CapRT', 'kW_per_RT')
    heat_terms = []
    for n in UNITS:
        c = f'CH{n}'
        # LWT = own setpoint command while running (capacity limited to 105 %: above that the leaving temperature rises)
        SW(S, TH, f'Sim_{c}_LwtSp', f'{c}RunProofSelected', f'{c}_ChwSetpointCmd', 'Sim_EWT')
        MATH(S, TH, f'Sim_{c}_EvapDTSp', 'Subtract', 'Sim_EWT', f'Sim_{c}_LwtSp')
        LIMIT(S, TH, f'Sim_{c}_EvapDTPos', f'Sim_{c}_EvapDTSp', 0, 20)
        MATH(S, TH, f'Sim_{c}_QK', 'Multiply', f'Sim_{c}_EvapFlowT', 'Water_kW_Factor', note='kW per K through this evaporator')
        MATH(S, TH, f'Sim_{c}_LoadKWDem', 'Multiply', f'Sim_{c}_QK', f'Sim_{c}_EvapDTPos')
        MATH(S, TH, f'Sim_{c}_LoadKW', 'Minimum', f'Sim_{c}_LoadKWDem', 'Sim_CH_CapKW')
        MATH(S, TH, f'Sim_{c}_QKGuard', 'Maximum', f'Sim_{c}_QK', 'Tiny')
        MATH(S, TH, f'Sim_{c}_EvapDTAct', 'Divide', f'Sim_{c}_LoadKW', f'Sim_{c}_QKGuard')
        MATH(S, TH, f'Sim_{c}_LWT', 'Subtract', 'Sim_EWT', f'Sim_{c}_EvapDTAct')
        relink_sim(S, f'{c}_ChwSupplyTemp', f'Sim_{c}_LWT', 'chiller leaving = own setpoint command while running (capacity limited)')
        relink_sim(S, f'{c}_ChwReturnTemp', 'Sim_EWT', 'chiller entering = building return mixed with bypass')
        MATH(S, TH, f'Sim_{c}_LoadRT', 'Divide', f'Sim_{c}_LoadKW', 'kW_per_RT')
        MATH(S, TH, f'Sim_{c}_PLR', 'Divide', f'Sim_{c}_LoadRT', 'CH_RatedRT')
        MATH(S, TH, f'Sim_{c}_LoadPctT', 'Multiply', f'Sim_{c}_PLR', 'HundredPct')
        relink_sim(S, f'{c}LoadPct', f'Sim_{c}_LoadPctT', 'chiller % load = RT / rated (BACnet from chiller)')
        # kW = rated x (fixed + var x PLR) x (1 + coef x (lift - design)),  lift = CDS - LWT
        MATH(S, TH, f'Sim_{c}_PLRVar', 'Multiply', f'Sim_{c}_PLR', 'Sim_CH_PLVar')
        MATH(S, TH, f'Sim_{c}_PLCurve', 'Add', 'Sim_CH_PLFixed', f'Sim_{c}_PLRVar')
        MATH(S, TH, f'Sim_{c}_Lift', 'Subtract', 'CDS', f'Sim_{c}_LWT')
        MATH(S, TH, f'Sim_{c}_LiftExcess', 'Subtract', f'Sim_{c}_Lift', 'Sim_CH_DesignLift')
        MATH(S, TH, f'Sim_{c}_LiftAdj', 'Multiply', f'Sim_{c}_LiftExcess', 'Sim_CH_LiftCoef')
        MATH(S, TH, f'Sim_{c}_LiftFactor', 'Add', 'One', f'Sim_{c}_LiftAdj')
        LIMIT(S, TH, f'Sim_{c}_LiftFactorLim', f'Sim_{c}_LiftFactor', 0.7, 1.5)
        MATH(S, TH, f'Sim_{c}_kWModel', 'Multiply', f'CH{n}_RatedKW', f'Sim_{c}_PLCurve', f'Sim_{c}_LiftFactorLim')
        S.rewire(f'Sim_{c}_kWCalc', 'inTrue', f'Sim_{c}_kWModel', f'Sim_{c}_kWRunning')
        # heat rejected to the condenser = cooling + compressor power (only while running)
        MATH(S, TH, f'Sim_{c}_RejectRun', 'Add', f'Sim_{c}_LoadKW', f'CH{n}_kW')
        SW(S, TH, f'Sim_{c}_Reject', f'{c}RunProofSelected', f'Sim_{c}_RejectRun', 'ZeroSpeed')
        heat_terms.append(f'Sim_{c}_Reject')
    # header CHWS = flow-weighted mix of the chiller outlets, lagged
    for n in UNITS:
        MATH(S, TH, f'Sim_CH{n}_OutHeat', 'Multiply', f'Sim_CH{n}_EvapFlowT', f'Sim_CH{n}_LWT')
    MATH(S, TH, 'Sim_OutHeat', 'Add', 'Sim_CH01_OutHeat', 'Sim_CH02_OutHeat')
    MATH(S, TH, 'Sim_ChwsMix', 'Divide', 'Sim_OutHeat', 'Sim_EvapFlowGuard')
    S.kc(TH, 'Sim_ChwsSel', 'NumericSwitch', {'inSwitch': 'Sim_EvapFlowing', 'inTrue': 'Sim_ChwsMix', 'inFalse': 'Sim_ChwIdleTemp'})
    MATH(S, TH, 'Sim_ChwsDev', 'Subtract', 'Sim_ChwsSel', 'Sim_ChwIdleTemp')
    RATE(S, TH, 'Sim_ChwsDevLag', 'Sim_ChwsDev', 0.1, note='header transport lag 0.1 K/s (deviation form: starts at the idle temperature)')
    MATH(S, TH, 'Sim_ChwsLag', 'Add', 'Sim_ChwIdleTemp', 'Sim_ChwsDevLag')
    relink_sim(S, 'CHWS', 'Sim_ChwsLag', 'header supply = mix of chiller outlets')
    # condenser return
    MATH(S, TH, 'Sim_RejectKW', 'Add', *heat_terms)
    MATH(S, TH, 'Sim_CdwFlowGuard', 'Maximum', 'Sim_CdwPlantFlow', 'One')
    MATH(S, TH, 'Sim_CdwDTRaw', 'Divide', 'Sim_RejectKW', 'Sim_CdwFlowGuard')
    MATH(S, TH, 'Sim_CdwDT', 'Divide', 'Sim_CdwDTRaw', 'Water_kW_Factor')
    LIMIT(S, TH, 'Sim_CdwDTLim', 'Sim_CdwDT', 0, 15)
    MATH(S, TH, 'Sim_CDRCalc', 'Add', 'CDS', 'Sim_CdwDTLim')
    relink_sim(S, 'CDR', 'Sim_CDRCalc', 'condenser return = CDS + heat rejected / CDW flow')
    # plant load % (of one chiller) now follows the measured cooling load (in16 calc) - drop the ramp
    if any(M6.child(L, 'targetSlotName').get('v') == 'in10' for L in S.comp['PlantLoadPct'] if L.get('t') == 'b:Link'):
        unlink(S, 'PlantLoadPct', 'in10')
    # remove the superseded ramps / V7.3 kpi_fix emulation
    for r in ('Ramp_CHWS', 'Ramp_CHWR', 'Ramp_CHWFlow', 'Ramp_CDR', 'Ramp_CH01LoadPct', 'Ramp_CH02LoadPct', 'Ramp_PlantLoadPct'):
        drop_if_unused(S, r)
    for n in UNITS:
        drop_if_unused(S, f'Sim_CH{n}_kWRunning', f'Sim_CH{n}_LoadFrac', f'Sim_CH{n}_RunNum')
    drop_if_unused(S, 'Sim_CH_kWFrac', 'Sim_CH_PLRvar', 'Sim_CH_PLR', 'Sim_CH_PLRraw', 'Sim_CH_ShareRT', 'Sim_CH_RunGuard',
                   'Sim_CH_RunCount', 'Sim_CH01_RunNum', 'Sim_CH02_RunNum', 'Sim_ChwFlowShare')
    drop_if_unused(S, 'CH_PartLoadFixedFrac', 'CH_PartLoadVarFrac', 'Sim_CH01_ChwSupply', 'Sim_CH02_ChwSupply', 'Sim_ChwOnGuard', 'Sim_ChwOnCount')


def bypass_tune(S, prof):
    """3. min-flow valve: open gradually (rate limit) - evaporator flow is now closed-loop through the emulation"""
    setprop(S, 'Byp_RateLimit', 'maxStepSize', '1.0' if prof is M6.TIMING['site'] else '5.0')
    S.log.append(('PROP', '', 'Byp_RateLimit', 'maxStepSize', '1.0 %/s site', 'gradual min-flow valve opening'))


# ============================================================ 4 / 7. graphics support: valve travel + pipe flow direction
GF = 'Graphics/Valves'
GFL = 'Graphics/Flow'
VALVE_ANIM = [  # (graphic tag, command, 'b' on/off | 'p' modulating %, position feedback % or None -> estimated travel)
    ('CH01_ChwIso', 'CH01ValveOpenCmd', 'b', None), ('CH01_ChwFCV', 'CH01_ChwFCVCmd', 'p', 'CH01_ChwFCVFb'),
    ('CH01_CdwIso', 'CH01CdwValveOpenCmd', 'b', None), ('CH01_CdwHPV', 'CH01_CdwHPVCmd', 'p', 'CH01_CdwHPVFb'),
    ('CH02_ChwIso', 'CH02ValveOpenCmd', 'b', None), ('CH02_ChwFCV', 'CH02_ChwFCVCmd', 'p', 'CH02_ChwFCVFb'),
    ('CH02_CdwIso', 'CH02CdwValveOpenCmd', 'b', None), ('CH02_CdwHPV', 'CH02_CdwHPVCmd', 'p', 'CH02_CdwHPVFb')] + \
    [(f'{u}_{sd}MV', f'{u}_{sd}MVCmd', 'b', f'{u}_{sd}MVFb') for u in ('CHP01', 'CHP02', 'CDP01', 'CDP02') for sd in ('Suction', 'Discharge')] + \
    [(f'CT{n}_InletMV', f'CT{n}ValveOpenCmd', 'b', None) for n in UNITS] + \
    [(f'CT{n}_OutletMV', f'CT{n}_OutletMVCmd', 'b', f'CT{n}_OutletMVFb') for n in UNITS] + \
    [('CHW_BypassMV', 'CHW_BypassValveCmd', 'p', 'CHW_BypassValveFeedback')]


def valve_gfx(S, prof):
    S.param('Gfx_MV_MovingBand', 3.0, 'pct', folder=GF, note='graphic shows the actuator running while |target - position| > this')
    step = 100.0 / max(prof['sim_valve'] / 1000.0, 1.0)
    for tag, cmd, kind, fb in VALVE_ANIM:
        tgt = cmd
        if kind == 'b':
            tgt = f'Gfx_{tag}_Target'; SW(S, GF, tgt, cmd, 'HundredPct', 'ZeroSpeed')
        if fb:
            pos = fb
        else:
            RATE(S, GF, f'Gfx_{tag}_Travel', tgt, step, note='estimated travel from the stroke time (end switches only on this valve)')
            pos = f'Gfx_{tag}_Travel'
        S.npoint(GF, f'Gfx_{tag}_Pos', pos, 'pct', 0, note='valve position for the graphic (feedback, or estimated travel)')
        MATH(S, GF, f'Gfx_{tag}_Err', 'Subtract', tgt, pos)
        S.kc(GF, f'Gfx_{tag}_ErrAbs', 'AbsValue', {'inA': f'Gfx_{tag}_Err'})
        CMP(S, GF, f'Gfx_{tag}_MovingCmp', 'GreaterThan', f'Gfx_{tag}_ErrAbs', 'Gfx_MV_MovingBand')
        S.bpoint(GF, f'Gfx_{tag}_Moving', f'Gfx_{tag}_MovingCmp', 'Moving', 'Stopped')
        M6.NO_HISTORY.update({f'Gfx_{tag}_Pos', f'Gfx_{tag}_Moving'})


def _flow_flags(S, name, flow, note='', proof='Gfx_AnyPumpRun'):
    """<name>_Fwd / _Rev booleans (graphics only): water is shown moving only when the pumps are PROVEN (run feedback) AND the
    flow meter confirms the flow (double check after the pump starts)"""
    CMP(S, GFL, f'{name}FwdQ', 'GreaterThan', flow, 'Gfx_FlowMin')
    CMP(S, GFL, f'{name}RevQ', 'LessThan', flow, 'Gfx_FlowMinNeg')
    AND(S, GFL, f'{name}Fwd', f'{name}FwdQ', proof)
    AND(S, GFL, f'{name}Rev', f'{name}RevQ', proof)
    S.bpoint(GFL, f'{name}_Fwd', f'{name}Fwd', 'Flow', 'No flow', note=note)
    S.bpoint(GFL, f'{name}_Rev', f'{name}Rev', 'Flow', 'No flow', note=note)
    M6.NO_HISTORY.update({f'{name}_Fwd', f'{name}_Rev'})


def _header(S, name, taps, proof='Gfx_AnyPumpRun'):
    """cumulative flow along a header: taps = [(component, +1 source / -1 sink)] in drawing order; segment k carries the sum of
    taps[0..k] in the drawing direction -> Gfx_<name>_S<k>_Fwd / _Rev"""
    acc = None
    for k, (src, sg) in enumerate(taps[:-1]):
        if acc is None:
            acc = src if sg > 0 else None
            if acc is None:
                MATH(S, GFL, f'Gfx_{name}_C{k}', 'Subtract', 'ZeroSpeed', src); acc = f'Gfx_{name}_C{k}'
        else:
            MATH(S, GFL, f'Gfx_{name}_C{k}', 'Add' if sg > 0 else 'Subtract', acc, src); acc = f'Gfx_{name}_C{k}'
        _flow_flags(S, f'Gfx_{name}_S{k}', acc, f'{name} segment {k}', proof)


def flow_gfx(S, prof):
    S.param('Gfx_FlowMin', 2.0, 'm3h', folder=GFL, note='graphic animates a pipe when its flow is above this')
    S.kc(GFL, 'Gfx_FlowMinNeg', 'Subtract', {'inA': 'ZeroSpeed', 'inB': 'Gfx_FlowMin'})
    # equal-share estimates for unmetered branches (pumps, towers); bypass = evaporator total - main
    for eq, tot in (('CHP', 'Byp_EvapFlowSum'), ('CDP', 'CDW_Flow')):
        SW(S, GFL, f'Gfx_{eq}01_On', f'{eq}01RunProof', 'One', 'ZeroSpeed'); SW(S, GFL, f'Gfx_{eq}02_On', f'{eq}02RunProof', 'One', 'ZeroSpeed')
        MATH(S, GFL, f'Gfx_{eq}_N', 'Add', f'Gfx_{eq}01_On', f'Gfx_{eq}02_On'); MATH(S, GFL, f'Gfx_{eq}_NG', 'Maximum', f'Gfx_{eq}_N', 'One')
        MATH(S, GFL, f'Gfx_{eq}_Each', 'Divide', tot, f'Gfx_{eq}_NG')
        for n in UNITS: MATH(S, GFL, f'Gfx_Q_{eq}{n}', 'Multiply', f'Gfx_{eq}_Each', f'Gfx_{eq}{n}_On')
    for n in UNITS: SW(S, GFL, f'Gfx_CT{n}_Open', f'CT{n}ValveOpenProof', 'One', 'ZeroSpeed')
    MATH(S, GFL, 'Gfx_CT_N', 'Add', 'Gfx_CT01_Open', 'Gfx_CT02_Open'); MATH(S, GFL, 'Gfx_CT_NG', 'Maximum', 'Gfx_CT_N', 'One')
    MATH(S, GFL, 'Gfx_CT_Each', 'Divide', 'CDW_Flow', 'Gfx_CT_NG')
    for n in UNITS: MATH(S, GFL, f'Gfx_Q_CT{n}', 'Multiply', 'Gfx_CT_Each', f'Gfx_CT{n}_Open')
    MATH(S, GFL, 'Gfx_Q_BypRaw', 'Subtract', 'Byp_EvapFlowSum', 'CHWFlow')
    MATH(S, GFL, 'Gfx_Q_Byp', 'Maximum', 'Gfx_Q_BypRaw', 'ZeroSpeed')
    # proofs: CHW side = a CHW pump proven, CDW side = a CDW pump proven (flow meter + run feedback both required)
    OR(S, GFL, 'Gfx_AnyPumpRun', 'CHP01RunProof', 'CHP02RunProof')
    OR(S, GFL, 'Gfx_CdpAnyRun', 'CDP01RunProof', 'CDP02RunProof')
    # single-direction branches
    for nm, q, pr in (('ChwMain', 'CHWFlow', 'Gfx_AnyPumpRun'), ('Bypass', 'Gfx_Q_Byp', 'Gfx_AnyPumpRun'), ('EvapTotal', 'Byp_EvapFlowSum', 'Gfx_AnyPumpRun'),
                      ('CdwTotal', 'CDW_Flow', 'Gfx_CdpAnyRun'), ('CH01Evap', 'CH01_ChwFlow', 'Gfx_AnyPumpRun'), ('CH02Evap', 'CH02_ChwFlow', 'Gfx_AnyPumpRun'),
                      ('CH01Cond', 'CH01_CdwFlow', 'Gfx_CdpAnyRun'), ('CH02Cond', 'CH02_CdwFlow', 'Gfx_CdpAnyRun'),
                      ('CHP01', 'Gfx_Q_CHP01', 'CHP01RunProof'), ('CHP02', 'Gfx_Q_CHP02', 'CHP02RunProof'),
                      ('CDP01', 'Gfx_Q_CDP01', 'CDP01RunProof'), ('CDP02', 'Gfx_Q_CDP02', 'CDP02RunProof'),
                      ('CT01', 'Gfx_Q_CT01', 'Gfx_CdpAnyRun'), ('CT02', 'Gfx_Q_CT02', 'Gfx_CdpAnyRun')):
        _flow_flags(S, f'Gfx_{nm}', q, f'{nm} flow (graphic: pump proven AND flow meter)', pr)
    # headers with flows joining from both ends (drawing order = the order in gen_px74)
    _header(S, 'ChpDis', [('Gfx_Q_CHP01', 1), ('CH01_ChwFlow', -1), ('Gfx_Q_CHP02', 1), ('CH02_ChwFlow', -1)], 'Gfx_AnyPumpRun')   # X_DIS top -> bottom
    _header(S, 'CdpDis', [('CH01_CdwFlow', -1), ('Gfx_Q_CDP01', 1), ('CH02_CdwFlow', -1), ('Gfx_Q_CDP02', 1)], 'Gfx_CdpAnyRun')    # X_CDS top -> bottom
    # pump running but the flow meter shows no flow -> graphic warning (water NOT drawn moving)
    NOT(S, GFL, 'Gfx_ChwNoFlowQ', 'Gfx_EvapTotalFwdQ')
    AND(S, GFL, 'Gfx_ChwNoFlowLogic', 'Gfx_AnyPumpRun', 'Gfx_ChwNoFlowQ')
    S.bpoint(GFL, 'Gfx_ChwPumpNoFlow', 'Gfx_ChwNoFlowLogic', 'PUMP ON - NO FLOW', 'OK', note='CHW pump proven but evaporator flow meters read no flow')
    NOT(S, GFL, 'Gfx_CdwNoFlowQ', 'Gfx_CdwTotalFwdQ')
    AND(S, GFL, 'Gfx_CdwNoFlowLogic', 'Gfx_CdpAnyRun', 'Gfx_CdwNoFlowQ')
    S.bpoint(GFL, 'Gfx_CdwPumpNoFlow', 'Gfx_CdwNoFlowLogic', 'PUMP ON - NO FLOW', 'OK', note='CDW pump proven but the CDW flow meter reads no flow')
    CMP(S, GFL, 'Gfx_BypModOpen', 'GreaterThan', 'CHW_BypassValveFeedback', 'Gfx_MV_MovingBand')
    AND(S, GFL, 'Gfx_BypModLogic', 'Gfx_BypModOpen', 'Gfx_BypassFwd')
    S.bpoint(GFL, 'Gfx_BypMod_Fwd', 'Gfx_BypModLogic', 'Flow', 'No flow', note='flow through the modulating min-flow valve')
    M6.NO_HISTORY.add('Gfx_BypMod_Fwd')
    AND(S, GFL, 'Gfx_PotFeedLogic', 'CHW_ChemFeederOpen', 'Byp_AnyPumpProven')
    S.bpoint(GFL, 'Gfx_PotFeeder_Fwd', 'Gfx_PotFeedLogic', 'Flow', 'No flow')
    AND(S, GFL, 'Gfx_ManBypLogic', 'CHW_BypassManualOpen', 'Byp_AnyPumpProven')
    S.bpoint(GFL, 'Gfx_ManBypass_Fwd', 'Gfx_ManBypLogic', 'Flow', 'No flow')
    OR(S, GFL, 'Gfx_MuTowersLogic', 'CT01_MakeupValveCmd', 'CT02_MakeupValveCmd')
    S.bpoint(GFL, 'Gfx_MuTowers_Fwd', 'Gfx_MuTowersLogic', 'Flow', 'No flow')
    M6.NO_HISTORY.update({'Gfx_PotFeeder_Fwd', 'Gfx_ManBypass_Fwd', 'Gfx_MuTowers_Fwd'})


# ============================================================ 12. units: kPa -> bar, m3/h (water) -> US gpm
GPM = 4.402867539
DEADBAND = {}
_alarm_ext = M6.alarm_ext


def _alarm_ext_units(S, point, kind, *a, **kw):
    r = _alarm_ext(S, point, kind, *a, **kw)
    if kind == 'oor' and point in DEADBAND:
        for p in S.comp[point].iter('p'):
            if p.get('n') == 'deadband': p.set('v', repr(DEADBAND[point]))
    return r


M6.alarm_ext = _alarm_ext_units
def units(S, prof):
    import units74
    M6.U['bar'] = units74.NEWU['P']
    M6.U['gpm'] = units74.NEWU['Q']
    # volumes stay m3: totalizer of a gpm flow = gpm.h -> x 0.2271247 = m3
    const(S, 'GpmHrToM3', 0.2271247, 'none', 7, note='1 gpm for 1 h = 60 US gal = 0.2271247 m3')
    for pt, flow, folder in (('CT_MakeupVolume', 'CT_MakeupFlow', 'CdwLoop/Monitor'), ('CHW_FillVolume', 'CHW_FillFlow', 'MakeupWater/Monitor')):
        blk = f'{pt}Calc'
        MATH(S, folder, blk, 'Multiply', f'{flow}:Volume.total', 'GpmHrToM3', note='gpm.h -> m3')
        unlink(S, pt, 'in16')
        S.link(S.comp[pt], blk, 'in16')
    manual = [('Water_kW_Factor', 'fallback', 1.0 / GPM),                  # kW per (m3/h . K) -> per (gpm . K)
              ('Sim_EvapDPk', 'fallback', 0.01 / GPM ** 2), ('Sim_CondDPk', 'fallback', 0.01 / GPM ** 2),   # dP = k x Q^2
              ('MakeupPerRT', 'fallback', GPM)]                                # make-up m3/h per RT -> gpm per RT
    q, done = units74.convert(S, manual)
    # out-of-range alarm limits are applied after this layer: convert the table + scale the deadband
    for pt, (lo, hi, cls, dly, inh) in list(M6.OOR.items()):
        if q.get(pt):
            k = units74.FACT[q[pt]]
            M6.OOR[pt] = (round(lo * k, 4), round(hi * k, 4), cls, dly, inh)
            DEADBAND[pt] = 0.5 * k
    for n, qq in q.items():
        S.meta.setdefault(n, {})['unit'] = 'bar' if qq == 'P' else 'gpm'
        r = S.meta[n].get('ramp')
        if isinstance(r, str):                                   # emulation note: 'SineWave 80..160 / 15 min' -> bar / gpm
            k = units74.FACT[qq]
            S.meta[n]['ramp'] = re.sub(r'(-?[\d.]+)\.\.(-?[\d.]+)', lambda m: f'{float(m.group(1)) * k:.3g}..{float(m.group(2)) * k:.3g}', r, count=1)
    import re as _re
    for n in ('Sim_EvapDPk', 'Sim_CondDPk'):
        f = M6.child(S.comp[n], 'facets')
        if f is not None: f.set('v', _re.sub(r'precision=i:\d+', 'precision=i:9', f.get('v')))
    S.log.append(('UNITS', '', f'{len(q)} components', 'kPa->bar / m3h->gpm', f'{len(done)} stored values scaled', ''))
    if os.environ.get('UNITS_LOG'):
        with open(os.environ['UNITS_LOG'], 'w') as f:
            for n, slot in done: f.write(f'{n}\t{slot}\n')


_v73 = M73.v73


def v74(S, prof):
    _v73(S, prof)
    load_balance(S, prof)
    thermal(S, prof)
    bypass_tune(S, prof)
    valve_gfx(S, prof)
    flow_gfx(S, prof)
    if os.environ.get('UNITS_REPORT'):
        import units74, json
        q, rep = units74.report(S)
        with open(os.environ['UNITS_REPORT'], 'w') as f:
            json.dump({'q': q, 'boundary': rep}, f, indent=1)
    units(S, prof)


M71.v71 = v74

if __name__ == '__main__':
    M7.main()
