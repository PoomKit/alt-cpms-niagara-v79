"""Build ALT_CP_Ref_V7_7 = V7.6 (make_v76.py, imported unchanged) + V7.7 (user request 30 Sep 2026 10:03):
  1/2  TT at CT / chiller in-out and PT at CHP / CDP suction-discharge: the field points already exist (V7.1-V7.3); V7.7 adds
       the missing CT outlet / inlet instrument tags on the Plant page (gen_px77.py)
  3    chiller evaporator / condenser FLOW SWITCHES (CHnCHWFlowProof / CHnCDWFlowProof): flow-loss trip while running (latched
       alarm, optional lock-out), flow switch vs flow meter disagreement alarm
  4    air side completed: AHU dehumidification (RA RH -> SAT reset to min), CO2 high alarm, high duct static safety cut-out
       (latched), unoccupied night high-limit cooling; OAU leaving dew-point control + smoke detector + low airflow alarm
  5    fail-safe interlocks: chiller freeze + condenser high-temperature trips (latched, manual reset), plant emergency stop,
       phase-fail relay (auto restart after a delay), refrigerant leak monitor (2 stages: emergency ventilation, chillers off),
       pump high discharge-pressure trip (-> standby pump)
  6    condenser water chemical treatment: flow-paced inhibitor, biocide A / B slug dosing with pre-bleed + bleed lock-out,
       cycles of concentration, tank low levels, dosing-pump flow-fail alarms
  7    CHW 'pot feeder' -> CHW CHEMICAL FEED (tank + metering pump, flow-paced on the loop fill water)
usage: make_v77.py c_v5.bog c_v5.tsv out.bog --regdir reg77 [--timing fpt]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_v6 as M6
import make_v7 as M7
import make_v74 as M74
import make_v76 as M76                                   # noqa: F401  (installs the V7.6 layer)
import v77_fieldcx as FCX                                # r2: field interface, commissioning, history fixes
import v77_smart as SMART                                # r5: readable folders, PM, predictive FDD, health, TOU demand limit
import v77_cloud as CLOUD                                # r7: AI from cloud (tag mapping), not BACnet
import v77_r9 as R9                                      # r9: SOO R1 review logic changes
from make_v7 import AND, OR, NOT, DLY, PULSE, SW, MATH, CMP, LIMIT, HYST, const, sealin, di, ai, simlink

M6.STATION = M7.STATION = 'ALT_CP_Ref_V7_7'
M7.FOXS_PORT = '4925'
T, F = 'ConstantTrue', 'ConstantFalse'
_units = M74.units


def tm(prof, site_ms, fpt_ms):
    return site_ms if prof is M6.TIMING['site'] else fpt_ms


def alarm(S, folder, name, src, t, f, cls, text, note=''):
    S.bpoint(folder, name, src, t, f, note=note)
    M6.COS[name] = (True, cls, text)
    return name


# ------------------------------------------------------------------ 3 + 5  chiller flow switches and safety interlocks
def interlocks(S, prof):
    IL = 'PlantControl/Interlocks'
    S.param('CH_FreezeTripTemp', 3.0, 'C', folder=IL, note='evaporator LWT low limit -> chiller trip (latched)')
    S.param('CH_FreezeResetTemp', 5.0, 'C', folder=IL, note='freeze trip can be reset above this')
    S.param('CH_CondHighAlarmTemp', 38.0, 'C', folder=IL, note='condenser LWT high warning')
    S.param('CH_CondHighTripTemp', 41.0, 'C', folder=IL, note='condenser LWT high limit (high head pressure) -> chiller trip (latched)')
    S.bparam('CH_FlowSwitchLockout', False, folder=IL, t='Lock-out', f='Auto restart',
             note='true = flow-switch trip locks the chiller out until reset (default: chiller stops, restarts when flow is proven)')
    S.param('CH_FlowSwMismatchRatio', 0.5, 'none', folder=IL, prec=2, note='meter < ratio x min flow while switch = FLOW -> disagreement')
    # plant level
    di(S, IL, 'Plant_EmergencyStop', False, 'E-STOP', 'Normal', note='plant room emergency stop push-button (NC loop, volt-free)')
    di(S, IL, 'Plant_PhaseFailRelay', False, 'Phase fail', 'Normal', note='phase-failure / under-voltage relay of the chiller MCC')
    M6.COS['Plant_EmergencyStop'] = (True, 'Emergency', 'PLANT EMERGENCY STOP - chillers and plant stopped')
    M6.COS['Plant_PhaseFailRelay'] = (True, 'Critical', 'Power phase failure - chillers inhibited (auto restart after power is healthy)')
    DLY(S, IL, 'Plant_PowerRestoreDelay', 'Plant_PhaseFailRelay', 0, tm(prof, 120000, 5000), note='hold 2 min after power returns (site)')
    OR(S, IL, 'Plant_HardInhibit', 'Plant_EmergencyStop', 'Plant_PowerRestoreDelay')
    NOT(S, IL, 'Plant_NotInhibited', 'Plant_HardInhibit')
    S.rewire('PlantEnableEffective', 'inD', 'Plant_NotInhibited', T)
    S.bpoint(IL, 'Plant_InterlockActive', 'Plant_HardInhibit', 'Inhibited', 'Normal', note='E-stop or power fail')
    # refrigerant leak (plant room)
    ai(S, IL, 'PlantRoom_RefrigerantPPM', 0.0, 'none', prec=0, note='refrigerant leak detector (R-134a / R-513A) ppm, 4-20 mA')
    S.param('RL_AlarmPPM', 300.0, 'none', folder=IL, prec=0, note='stage 1: alarm + emergency ventilation')
    S.param('RL_HighPPM', 1000.0, 'none', folder=IL, prec=0, note='stage 2 (TLV / RCL region): critical alarm, chillers off if enabled')
    S.bparam('CH_StopOnRefLeak', True, folder=IL, t='Stop chillers', f='Alarm only', note='stage-2 leak stops the chillers (PROJECT decision)')
    CMP(S, IL, 'RL_AboveAlarm', 'GreaterThanEqual', 'PlantRoom_RefrigerantPPM', 'RL_AlarmPPM')
    CMP(S, IL, 'RL_AboveHigh', 'GreaterThanEqual', 'PlantRoom_RefrigerantPPM', 'RL_HighPPM')
    DLY(S, IL, 'RL_AlarmDelay', 'RL_AboveAlarm', tm(prof, 10000, 1000))
    DLY(S, IL, 'RL_HighDelay', 'RL_AboveHigh', tm(prof, 10000, 1000))
    alarm(S, IL, 'PlantRoom_RefLeakAlarm', 'RL_AlarmDelay', 'Leak', 'Normal', 'Critical', 'Refrigerant leak stage 1 - plant room emergency ventilation ON')
    alarm(S, IL, 'PlantRoom_RefLeakHighAlarm', 'RL_HighDelay', 'Leak HIGH', 'Normal', 'Emergency', 'Refrigerant leak stage 2 - evacuate plant room')
    S.bparam('PlantRoom_EmergencyVentManual', False, folder=IL, t='Manual ON', f='Auto')
    DLY(S, IL, 'RL_VentRunOn', 'RL_AlarmDelay', 0, tm(prof, 900000, 5000), note='ventilation runs on 15 min after the leak clears')
    OR(S, IL, 'RL_VentLogic', 'RL_VentRunOn', 'PlantRoom_EmergencyVentManual')
    S.bpoint(IL, 'PlantRoom_EmergencyVentCmd', 'RL_VentLogic', 'ON', 'OFF', note='plant room emergency exhaust fan (leak / manual)')
    AND(S, IL, 'RL_StopChillers', 'RL_HighDelay', 'CH_StopOnRefLeak')
    OR(S, IL, 'Plant_ChillerInhibit', 'Plant_HardInhibit', 'RL_StopChillers')
    for n in ('01', '02'):
        c = f'CH{n}'
        # freeze + condenser high: latched, reset by the chiller / plant reset
        CMP(S, IL, f'{c}_FreezeLow', 'LessThan', f'{c}_ChwSupplyTemp', 'CH_FreezeTripTemp')
        AND(S, IL, f'{c}_FreezeRun', f'{c}_FreezeLow', f'{c}RunProofSelected')
        DLY(S, IL, f'{c}_FreezeDelay', f'{c}_FreezeRun', tm(prof, 10000, 1000))
        CMP(S, IL, f'{c}_CondHigh', 'GreaterThan', f'{c}_CdwLeavingTemp', 'CH_CondHighTripTemp')
        AND(S, IL, f'{c}_CondHighRun', f'{c}_CondHigh', f'{c}RunProofSelected', f'{c}CDWFlowProof')   # no flow = flow-switch trip, not HP
        DLY(S, IL, f'{c}_CondHighDelay', f'{c}_CondHighRun', tm(prof, 10000, 1000))
        CMP(S, IL, f'{c}_CondWarm', 'GreaterThan', f'{c}_CdwLeavingTemp', 'CH_CondHighAlarmTemp')
        AND(S, IL, f'{c}_CondWarmRun', f'{c}_CondWarm', f'{c}RunProofSelected')
        DLY(S, IL, f'{c}_CondWarmDelay', f'{c}_CondWarmRun', tm(prof, 300000, 5000))
        alarm(S, IL, f'{c}_CondHighTempAlarm', f'{c}_CondWarmDelay', 'High', 'Normal', 'Warning', f'{c} condenser leaving water high (tower / CDW)')
        # flow switches: loss while running
        NOT(S, IL, f'{c}_EvapNoFlow', f'{c}CHWFlowProof')
        NOT(S, IL, f'{c}_CondNoFlow', f'{c}CDWFlowProof')
        AND(S, IL, f'{c}_EvapFlowLossRun', f'{c}_EvapNoFlow', f'{c}RunProofSelected')
        AND(S, IL, f'{c}_CondFlowLossRun', f'{c}_CondNoFlow', f'{c}RunProofSelected')
        DLY(S, IL, f'{c}_EvapFlowLossDly', f'{c}_EvapFlowLossRun', tm(prof, 3000, 1000))
        DLY(S, IL, f'{c}_CondFlowLossDly', f'{c}_CondFlowLossRun', tm(prof, 3000, 1000))
        sealin(S, IL, f'{c}_EvapFlowTrip', f'{c}_EvapFlowLossDly', f'{c}ManualReset', note='evaporator flow switch opened while running')
        sealin(S, IL, f'{c}_CondFlowTrip', f'{c}_CondFlowLossDly', f'{c}ManualReset', note='condenser flow switch opened while running')
        alarm(S, IL, f'{c}_EvapFlowSwTripAlarm', f'{c}_EvapFlowTrip', 'Tripped', 'Normal', 'Critical', f'{c} evaporator flow switch - flow lost while running')
        alarm(S, IL, f'{c}_CondFlowSwTripAlarm', f'{c}_CondFlowTrip', 'Tripped', 'Normal', 'Critical', f'{c} condenser flow switch - flow lost while running')
        OR(S, IL, f'{c}_FlowTripAny', f'{c}_EvapFlowTrip', f'{c}_CondFlowTrip')
        AND(S, IL, f'{c}_FlowTripLock', f'{c}_FlowTripAny', 'CH_FlowSwitchLockout')
        # flow switch vs flow meter
        MATH(S, IL, f'{c}_EvapMeterLowLim', 'Multiply', f'{c}_MinFlow', 'CH_FlowSwMismatchRatio')
        CMP(S, IL, f'{c}_EvapMeterLow', 'LessThan', f'{c}_ChwFlow', f'{c}_EvapMeterLowLim')
        CMP(S, IL, f'{c}_EvapMeterHigh', 'GreaterThan', f'{c}_ChwFlow', f'{c}_MinFlow')
        AND(S, IL, f'{c}_EvapSwOnMeterLow', f'{c}CHWFlowProof', f'{c}_EvapMeterLow')
        AND(S, IL, f'{c}_EvapSwOffMeterHigh', f'{c}_EvapNoFlow', f'{c}_EvapMeterHigh')
        MATH(S, IL, f'{c}_CondMeterLowLim', 'Multiply', 'CH_CdwMinFlow', 'CH_FlowSwMismatchRatio')
        CMP(S, IL, f'{c}_CondMeterLow', 'LessThan', f'{c}_CdwFlow', f'{c}_CondMeterLowLim')
        CMP(S, IL, f'{c}_CondMeterHigh', 'GreaterThan', f'{c}_CdwFlow', 'CH_CdwMinFlow')
        AND(S, IL, f'{c}_CondSwOnMeterLow', f'{c}CDWFlowProof', f'{c}_CondMeterLow')
        AND(S, IL, f'{c}_CondSwOffMeterHigh', f'{c}_CondNoFlow', f'{c}_CondMeterHigh')
        OR(S, IL, f'{c}_FlowSwMismatch', f'{c}_EvapSwOnMeterLow', f'{c}_EvapSwOffMeterHigh', f'{c}_CondSwOnMeterLow', f'{c}_CondSwOffMeterHigh')
        DLY(S, IL, f'{c}_FlowSwMismatchDly', f'{c}_FlowSwMismatch', tm(prof, 120000, 30000))
        alarm(S, IL, f'{c}_FlowSwMismatchAlarm', f'{c}_FlowSwMismatchDly', 'Disagree', 'Normal', 'Warning',
              f'{c} flow switch and flow meter disagree (check switch / meter)')
        # latched safety trip -> start permit inC
        OR(S, IL, f'{c}_SafetyTripIn', f'{c}_FreezeDelay', f'{c}_CondHighDelay')
        sealin(S, IL, f'{c}_SafetyTrip', f'{c}_SafetyTripIn', f'{c}ManualReset', note='freeze / condenser high - manual reset')
        alarm(S, IL, f'{c}_SafetyTripAlarm', f'{c}_SafetyTrip', 'TRIP', 'Normal', 'Critical', f'{c} safety trip (freeze / condenser high) - reset required')
        OR(S, IL, f'{c}_InterlockAny', f'{c}_SafetyTrip', f'{c}_FlowTripLock', 'Plant_ChillerInhibit')
        NOT(S, IL, f'{c}_InterlockOK', f'{c}_InterlockAny')
        S.rewire(f'{c}StartFinalPermit', 'inC', f'{c}_InterlockOK', T)
        S.bpoint(IL, f'{c}_InterlockOKSts', f'{c}_InterlockOK', 'OK', 'Interlocked')
    # pumps: high discharge pressure -> existing fail latch (standby pump takes over, reset = pump / plant reset)
    S.param('CHP_DischargeHiTrip', 650.0, 'kPa', folder=IL, note='CHP discharge high limit (closed valve / dead head) -> pump trip')
    S.param('CDP_DischargeHiTrip', 550.0, 'kPa', folder=IL, note='CDP discharge high limit -> pump trip')
    for u in ('CHP01', 'CHP02', 'CDP01', 'CDP02'):
        CMP(S, IL, f'{u}_DischHigh', 'GreaterThan', f'{u}_DischargePressure', f'{u[:3]}_DischargeHiTrip')
        AND(S, IL, f'{u}_DischHighRun', f'{u}_DischHigh', f'{u}RunProof')
        DLY(S, IL, f'{u}_DischHighDly', f'{u}_DischHighRun', tm(prof, 10000, 1000))
        S.rewire(f'{u}FailTripLogic', 'inC', f'{u}_DischHighDly', F)
        sealin(S, IL, f'{u}_DischHighLatch', f'{u}_DischHighDly', f'{u}ResetAny', note='held until the pump is reset')
        alarm(S, IL, f'{u}_HighDischargeAlarm', f'{u}_DischHighLatch', 'High', 'Normal', 'Critical', f'{u} discharge pressure high - pump tripped')
    S.log.append(('V7.7', IL, 'interlocks', 'flow switch / freeze / cond high / E-stop / phase / refrigerant / pump HP', '', ''))


# ------------------------------------------------------------------ 6  condenser water chemical treatment
def dose_pump(S, f, pump, cmd, prof):
    """dosing pump flow (stroke) sensor: emulated = command after 2 s; fault injection = override the DI to 'No flow'"""
    di(S, f, f'{pump}FlowSw', False, 'Flow', 'No flow', note='dosing pump flow / stroke sensor')
    DLY(S, 'Simulation/Chemical', f'Sim_{pump}FlowSw', cmd, 2000, 0)
    simlink(S, f'{pump}FlowSw', f'Sim_{pump}FlowSw', 'follows the pump command')
    NOT(S, f, f'{pump}NoFlow', f'{pump}FlowSw')
    AND(S, f, f'{pump}FailLogic', cmd, f'{pump}NoFlow')
    DLY(S, f, f'{pump}FailDelay', f'{pump}FailLogic', tm(prof, 60000, 8000))
    return alarm(S, f, f'{pump}FailAlarm', f'{pump}FailDelay', 'FAIL', 'Normal', 'Warning', f'{pump} dosing pump running but no flow')


def weekly_one_day(S, name, window, day):
    """sch:BooleanSchedule true only on `day` (0 = Sunday) in `window`."""
    el = M6.schedule_el(S, name, weekly=window)
    wk = next(c for c in next(c for c in el if c.get('n') == 'schedule') if c.get('n') == 'week')
    for i, d in enumerate(c for c in wk if c.get('t') == 'sch:DailySchedule'):
        if i != day:
            dy = next(c for c in d if c.get('n') == 'day')
            for c in list(dy): dy.remove(c)
    return el


def cdw_chem(S, prof):
    CH = 'CdwLoop/ChemTreatment'
    # cycles of concentration
    S.param('CT_MakeupConductivity', 350.0, 'none', folder=CH, prec=0, note='make-up (city) water conductivity uS/cm (lab value)')
    MATH(S, CH, 'CT_CoCCalc', 'Divide', 'CT_Conductivity', 'CT_MakeupConductivity')
    S.npoint(CH, 'CT_CyclesOfConcentration', 'CT_CoCCalc', 'none', 2, note='CoC = tower water / make-up conductivity')
    S.param('CT_CoCLowAlarm', 2.0, 'none', folder=CH, prec=1, note='CoC below this for 1 h while circulating = bleed stuck open / water waste')
    CMP(S, CH, 'CT_CoCLow', 'LessThan', 'CT_CyclesOfConcentration', 'CT_CoCLowAlarm')
    AND(S, CH, 'CT_CoCLowRun', 'CT_CoCLow', 'CT_CdwCirculating')
    DLY(S, CH, 'CT_CoCLowDly', 'CT_CoCLowRun', tm(prof, 3600000, 20000))
    alarm(S, CH, 'CT_CoCLowAlarmSts', 'CT_CoCLowDly', 'Low', 'Normal', 'Warning', 'Cooling tower cycles of concentration low (bleed valve stuck open?)')
    # inhibitor: flow-paced on make-up water, stops on tank low
    M6.COS['CT_ChemTankLowLevel'] = (True, 'Warning', 'CDW inhibitor tank low level - refill')
    NOT(S, CH, 'CT_InhibitorTankOK', 'CT_ChemTankLowLevel')
    S.rewire('CT_DosingLogic', 'inC', 'CT_InhibitorTankOK', T)
    S.param('CT_MakeupFlowDesign', 5.2, 'm3h', folder=CH, prec=1, note='design make-up (evaporation + bleed, 2 x 300 RT, CoC 4) = 100 % pump rate')
    MATH(S, CH, 'CT_InhibitorRatio', 'Divide', 'CT_MakeupFlow', 'CT_MakeupFlowDesign')
    MATH(S, CH, 'CT_InhibitorRatePctRaw', 'Multiply', 'CT_InhibitorRatio', 'HundredPct')
    LIMIT(S, CH, 'CT_InhibitorRateLim', 'CT_InhibitorRatePctRaw', 10, 100)
    SW(S, CH, 'CT_InhibitorRateSel', 'CT_ChemDosingPumpCmd', 'CT_InhibitorRateLim', 'Zero')
    S.npoint(CH, 'CT_InhibitorPumpRate', 'CT_InhibitorRateSel', 'pct', 0, note='metering pump stroke rate, paced by make-up flow')
    dose_pump(S, CH, 'CT_InhibitorPump', 'CT_ChemDosingPumpCmd', prof)
    # biocide A (oxidising) Mon 02:00 / B (non-oxidising) Thu 02:00: pre-bleed -> dose (bleed closed) -> contact lock-out
    for x, day in (('A', 1), ('B', 4)):
        sch = f'Sch_Biocide{x}'
        S.comp[sch] = weekly_one_day(S, sch, ('02:00:00.000', '02:10:00.000'), day); S.folder_of[sch] = CH
        S.log.append(('ADD', CH, sch, 'sch:BooleanSchedule', f"{'Mon' if day == 1 else 'Thu'} 02:00", 'edit in Workbench Scheduler view'))
        S.bparam(f'CT_Biocide{x}_ManualStart', False, folder=CH, t='Start', f='-', note='operator: start one biocide cycle now')
        di(S, CH, f'CT_Biocide{x}_TankLow', False, 'LOW', 'Normal', note=f'biocide {x} tank low-level switch')
        M6.COS[f'CT_Biocide{x}_TankLow'] = (True, 'Warning', f'CDW biocide {x} tank low level - refill')
        OR(S, CH, f'CT_Bio{x}_Req', sch, f'CT_Biocide{x}_ManualStart')
        PULSE(S, CH, f'CT_Bio{x}_Edge', f'CT_Bio{x}_Req', 2000)
        pre, dose, lock = tm(prof, 1800000, 20000), tm(prof, 1200000, 20000), tm(prof, 14400000, 40000)
        sealin(S, CH, f'CT_Bio{x}_Cycle', f'CT_Bio{x}_Edge', F)                 # reset wired below (cycle done)
        DLY(S, CH, f'CT_Bio{x}_PreDone', f'CT_Bio{x}_Cycle', pre, note='pre-bleed 30 min (site)')
        DLY(S, CH, f'CT_Bio{x}_DoseDone', f'CT_Bio{x}_Cycle', pre + dose, note='dose 20 min (site)')
        DLY(S, CH, f'CT_Bio{x}_Done', f'CT_Bio{x}_Cycle', pre + dose + lock, note='bleed lock-out 4 h contact time (site)')
        S.rewire(f'CT_Bio{x}_CycleNotReset', 'in', f'CT_Bio{x}_Done', F)
        NOT(S, CH, f'CT_Bio{x}_NotPreDone', f'CT_Bio{x}_PreDone')
        NOT(S, CH, f'CT_Bio{x}_NotDoseDone', f'CT_Bio{x}_DoseDone')
        AND(S, CH, f'CT_Bio{x}_PreBleed', f'CT_Bio{x}_Cycle', f'CT_Bio{x}_NotPreDone')
        AND(S, CH, f'CT_Bio{x}_Dosing', f'CT_Bio{x}_PreDone', f'CT_Bio{x}_NotDoseDone', f'CT_Bio{x}_Cycle')
        AND(S, CH, f'CT_Bio{x}_Lockout', f'CT_Bio{x}_Cycle', f'CT_Bio{x}_PreDone')
        NOT(S, CH, f'CT_Bio{x}_TankOK', f'CT_Biocide{x}_TankLow')
        AND(S, CH, f'CT_Bio{x}_PumpLogic', f'CT_Bio{x}_Dosing', 'CT_CdwCirculating', f'CT_Bio{x}_TankOK')
        S.bpoint(CH, f'CT_Biocide{x}PumpCmd', f'CT_Bio{x}_PumpLogic', 'Dosing', 'Off', note=f'biocide {x} slug-dose pump')
        S.bpoint(CH, f'CT_Biocide{x}CycleSts', f'CT_Bio{x}_Cycle', 'Cycle', 'Idle')
        dose_pump(S, CH, f'CT_Biocide{x}Pump', f'CT_Biocide{x}PumpCmd', prof)
    # bleed: normal (conductivity hysteresis, existing) blocked during dose / contact time, forced during pre-bleed,
    # high-high conductivity overrides the lock-out
    OR(S, CH, 'CT_BleedLockoutAny', 'CT_BioA_Lockout', 'CT_BioB_Lockout')
    OR(S, CH, 'CT_PreBleedAny', 'CT_BioA_PreBleed', 'CT_BioB_PreBleed')
    NOT(S, CH, 'CT_BleedNotLocked', 'CT_BleedLockoutAny')
    AND(S, CH, 'CT_BleedNormal', 'CT_BleedPermit', 'CT_BleedNotLocked')
    AND(S, CH, 'CT_BleedOverride', 'CT_BleedPermit', 'CT_ConductivityHigh')
    AND(S, CH, 'CT_BleedPre', 'CT_PreBleedAny', 'CT_CdwCirculating')
    OR(S, CH, 'CT_BleedFinal', 'CT_BleedNormal', 'CT_BleedOverride', 'CT_BleedPre')
    S.rewire('CT_BleedValveCmd', 'in16', 'CT_BleedFinal', 'CT_BleedPermit')
    S.bpoint(CH, 'CT_BleedLockout', 'CT_BleedLockoutAny', 'Locked (biocide)', 'Normal')
    S.bpoint(CH, 'CT_PreBleedActive', 'CT_PreBleedAny', 'Pre-bleed', '-')
    S.log.append(('V7.7', CH, 'CDW chemical treatment', 'inhibitor flow-paced, biocide A/B, pre-bleed, lock-out, CoC', '', ''))


# ------------------------------------------------------------------ 7  CHW chemical feed (replaces the pot feeder)
def chw_chem(S, prof):
    CF = 'MakeupWater/ChemFeed'
    S.set_prop('CHW_ChemFeederOpen', 'facets', 'trueText=s:Manual dose|falseText=s:Auto')
    di(S, CF, 'CHW_ChemTankLowLevel', False, 'LOW', 'Normal', note='CHW inhibitor (nitrite / molybdate) tank low-level switch')
    M6.COS['CHW_ChemTankLowLevel'] = (True, 'Warning', 'CHW chemical feed tank low level - refill')
    S.param('CHW_FillFlowDesign', 2.0, 'm3h', folder=CF, prec=1, note='loop fill flow = 100 % metering pump rate')
    S.param('CHW_ChemManualRate', 50.0, 'pct', folder=CF, prec=0, note='pump rate for a manual (test-kit) dose')
    OR(S, CF, 'CHW_ChemDemand', 'CHW_FillValveCmd', 'CHW_ChemFeederOpen')
    NOT(S, CF, 'CHW_ChemTankOK', 'CHW_ChemTankLowLevel')
    AND(S, CF, 'CHW_ChemPumpLogic', 'CHW_ChemDemand', 'CHP_AnyProven', 'CHW_ChemTankOK')
    S.bpoint(CF, 'CHW_ChemDosePumpCmd', 'CHW_ChemPumpLogic', 'Dosing', 'Off', note='CHW metering pump: paced by loop fill water (+ manual dose)')
    MATH(S, CF, 'CHW_ChemRatio', 'Divide', 'CHW_FillFlow', 'CHW_FillFlowDesign')
    MATH(S, CF, 'CHW_ChemRatePctRaw', 'Multiply', 'CHW_ChemRatio', 'HundredPct')
    LIMIT(S, CF, 'CHW_ChemRateLim', 'CHW_ChemRatePctRaw', 0, 100)
    SW(S, CF, 'CHW_ChemManualSel', 'CHW_ChemFeederOpen', 'CHW_ChemManualRate', 'Zero')
    MATH(S, CF, 'CHW_ChemRateMax', 'Maximum', 'CHW_ChemRateLim', 'CHW_ChemManualSel')
    SW(S, CF, 'CHW_ChemRateSel', 'CHW_ChemDosePumpCmd', 'CHW_ChemRateMax', 'Zero')
    S.npoint(CF, 'CHW_ChemPumpRate', 'CHW_ChemRateSel', 'pct', 0, note='CHW metering pump stroke rate')
    dose_pump(S, CF, 'CHW_ChemPump', 'CHW_ChemDosePumpCmd', prof)
    S.rewire('Gfx_PotFeedLogic', 'inA', 'CHW_ChemDosePumpCmd', 'CHW_ChemFeederOpen')   # graphic chemical line = pump running
    S.log.append(('V7.7', CF, 'CHW chemical feed', 'pot feeder -> tank + metering pump, fill-paced', '', ''))


# ------------------------------------------------------------------ 4  air side
def airside77(S, prof):
    A = M7.AIR
    C = f'{A}/Common'
    S.param('AHU_CO2AlarmPPM', 1200.0, 'none', folder=C, prec=0, note='return-air CO2 high alarm')
    S.param('AHU_StaticHiLimit', 500.0, 'none', folder=C, prec=0, note='duct static high limit Pa -> fan trip (latched)')
    S.bparam('AirSide_NightCoolEnable', True, folder=C, t='Enabled', f='Disabled', note='unoccupied high-limit: AHU runs if RAT > 29 C until < 27 C')
    NOT(S, C, 'Sch_AHU_Unocc', 'Sch_AHU')
    for u in ('AHU01', 'AHU02'):
        L = f'{A}/{u}/Safety'
        # dehumidification: RH hysteresis 60 / 65 %
        HYST(S, L, f'{u}_DehumHyst', f'{u}_RA_RH', 60, 65)
        AND(S, L, f'{u}_DehumLogic', f'{u}_DehumHyst', f'{u}_RA_RHValid' if f'{u}_RA_RHValid' in S.comp else T)
        S.bpoint(L, f'{u}_DehumActive', f'{u}_DehumLogic', 'Dehumidify', 'Normal', note='SAT reset overridden to SAT min')
        SW(S, L, f'{u}SatSpDehum', f'{u}_DehumActive', f'{u}_SAT_Min', f'{u}SatSpSelect')
        S.rewire(f'{u}_SAT_SP', 'in16', f'{u}SatSpDehum', f'{u}SatSpSelect')
        # CO2 high
        CMP(S, L, f'{u}_CO2High', 'GreaterThan', f'{u}_RA_CO2', 'AHU_CO2AlarmPPM')
        AND(S, L, f'{u}_CO2HighRun', f'{u}_CO2High', f'{u}_Status')
        DLY(S, L, f'{u}_CO2HighDly', f'{u}_CO2HighRun', tm(prof, 600000, 10000))
        alarm(S, L, f'{u}_CO2HighAlarm', f'{u}_CO2HighDly', 'High', 'Normal', 'Warning', f'{u} return-air CO2 high (OA damper / ventilation)')
        # high duct static safety (latched)
        CMP(S, L, f'{u}_StaticHigh', 'GreaterThan', f'{u}_DuctStatic', 'AHU_StaticHiLimit')
        DLY(S, L, f'{u}_StaticHighDly', f'{u}_StaticHigh', tm(prof, 5000, 1000))
        sealin(S, L, f'{u}_HighStaticTrip', f'{u}_StaticHighDly', 'PlantAlarmResetFire', note='fire / smoke damper closed - reset required')
        alarm(S, L, f'{u}_HighStaticAlarm', f'{u}_HighStaticTrip', 'TRIP', 'Normal', 'Critical', f'{u} duct static high limit - fan stopped (reset required)')
        NOT(S, L, f'{u}_StaticOK', f'{u}_HighStaticTrip')
        S.rewire(f'{u}StartLogic', 'inC', f'{u}_StaticOK', T)
        # unoccupied high-limit (night cooling)
        HYST(S, L, f'{u}_NightHyst', f'{u}_RAT', 27, 29)
        AND(S, L, f'{u}_NightCool', 'Sch_AHU_Unocc', f'{u}_NightHyst', 'AirSide_NightCoolEnable', f'{u}_ModeAuto')
        S.rewire(f'{u}RunRequest', 'inC', f'{u}_NightCool', F)
        S.bpoint(L, f'{u}_NightCoolActive', f'{u}_NightCool', 'Night cool', '-')
    # OAU: dew-point control, smoke detector, low airflow
    u, L = 'OAU01', f'{A}/OAU01/Safety'
    S.param('OAU_DewPointMax', 16.0, 'C', folder=C, note='OAU leaving dew point above -> LAT setpoint reset down')
    S.param('OAU_DehumOffsetK', 1.5, 'none', folder=C, note='LAT setpoint reduction while dew point high (K)')
    HYST(S, L, f'{u}_DewHyst', f'{u}_LAT_DewPoint', 15.0, 16.0)
    S.bpoint(L, f'{u}_DehumActive', f'{u}_DewHyst', 'Dehumidify', 'Normal')
    MATH(S, L, f'{u}_LatSpLow', 'Subtract', f'{u}_LAT_SP', 'OAU_DehumOffsetK')
    SW(S, L, f'{u}_LatSpSel', f'{u}_DehumActive', f'{u}_LatSpLow', f'{u}_LAT_SP')
    S.npoint(L, f'{u}_LAT_SP_EFFECTIVE', f'{u}_LatSpSel', 'C', 1, note='LAT setpoint incl. dew-point reset')
    S.rewire(f'{u}ValvePID', 'setpoint', f'{u}_LAT_SP_EFFECTIVE', f'{u}_LAT_SP')
    CMP(S, L, f'{u}_DewHigh', 'GreaterThan', f'{u}_LAT_DewPoint', 'OAU_DewPointMax')
    AND(S, L, f'{u}_DewHighRun', f'{u}_DewHigh', f'{u}_Status')
    DLY(S, L, f'{u}_DewHighDly', f'{u}_DewHighRun', tm(prof, 1800000, 20000))
    alarm(S, L, f'{u}_DewPointHighAlarm', f'{u}_DewHighDly', 'High', 'Normal', 'Warning', f'{u} leaving air dew point high for 30 min (humid air to building)')
    di(S, L, f'{u}_SmokeDetected', False, 'SMOKE', 'Normal', note='OAU supply duct smoke detector')
    M6.COS[f'{u}_SmokeDetected'] = (True, 'Emergency', f'{u} duct smoke detected - unit stopped')
    sealin(S, L, f'{u}_SmokeLatch', f'{u}_SmokeDetected', 'PlantAlarmResetFire')
    NOT(S, L, f'{u}_NoSmoke', f'{u}_SmokeLatch')
    S.rewire(f'{u}Permissive', 'inD', f'{u}_NoSmoke', T)
    S.param('OAU_AirflowLowPct', 70.0, 'pct', folder=C, note='airflow below % of setpoint while running -> alarm')
    MATH(S, L, f'{u}_AirflowRatio', 'Divide', f'{u}_Airflow', f'{u}_Airflow_SP')
    MATH(S, L, f'{u}_AirflowPct', 'Multiply', f'{u}_AirflowRatio', 'HundredPct')
    CMP(S, L, f'{u}_AirflowLow', 'LessThan', f'{u}_AirflowPct', 'OAU_AirflowLowPct')
    AND(S, L, f'{u}_AirflowLowRun', f'{u}_AirflowLow', f'{u}_Status')
    DLY(S, L, f'{u}_AirflowLowDly', f'{u}_AirflowLowRun', tm(prof, 300000, 20000))
    alarm(S, L, f'{u}_AirflowLowAlarm', f'{u}_AirflowLowDly', 'Low', 'Normal', 'Warning', f'{u} fresh-air flow low (filter / damper / fan)')
    S.log.append(('V7.7', A, 'air side', 'dehum, CO2, high static, night cool, OAU dew point / smoke / airflow', '', ''))


# ------------------------------------------------------------------ V7.7 r1: gaps found in the SOO review (30 Sep 11:31)
def review_fixes(S, prof):
    """runs after the V7.6 layer and the unit conversion (only unit-less / K / % parameters here)"""
    from make_v7 import PID
    from make_v74 import relink_sim
    ST, IL, CD = 'PlantControl/Staging', 'PlantControl/Interlocks', 'CdwLoop/CdpControl'
    # (1) P-06: CHWS-deviation stage-up is held until the lag chiller is no longer needed (no stage cycling)
    NOT(S, ST, 'Stg_NotPlantRun', 'PlantRunRequest')
    OR(S, ST, 'Stg_TempRelease', 'LagNotNeededDelay', 'Stg_NotPlantRun')
    sealin(S, ST, 'Stg_TempStageHold', 'ChwsDeviationStageUp', 'Stg_TempRelease',
           note='CHWS high stage-up held until CH01 + CH02 load below StageDownChillerSumPct for 15 min')
    S.rewire('Stage2LoadOrTemp', 'inB', 'Stg_TempStageHold', 'ChwsDeviationStageUp')
    # (2) P-06: flow-limited staging (VPF) is not blocked by the low plant delta-T rule
    S.rewire('Stage2NoLowDTOrRunning', 'inC', 'Stg_FlowStageUp', F)
    # (3) E-02: CDP variable speed = max(condenser delta-T loop, condenser min-flow loop); fixed speed on sensor failure
    S.bparam('CDP_VariableSpeedEnable', True, folder=CD, t='Variable (dT / min flow)', f='Fixed speed', note='false = FixedCDPSpeedPct (V7.6 behaviour)')
    S.set_fallback('FixedCDPSpeedPct', 100.0)   # CDP sized 900 gpm @ 80 ft at full speed: fixed / fail-safe speed = design flow
    S.param('CDP_DeltaTSetpoint', 5.3, 'none', folder=CD, prec=1, note='condenser water range at design (K)')
    S.param('CDP_MinFlowMargin', 1.1, 'none', folder=CD, prec=2, note='CDW flow kept above running chillers min flow x margin')
    S.param('CDP_MinSpeedPct', 40.0, 'pct', folder=CD, prec=0, note='CDP minimum speed (tower distribution / NPSH)')
    MATH(S, CD, 'CDP_CdwDT', 'Subtract', 'CDR', 'CDS')
    S.npoint(CD, 'CDW_DeltaT', 'CDP_CdwDT', 'none', 2, note='CDR - CDS (K)')
    CMP(S, CD, 'CDP_CdrAboveMin', 'GreaterThanEqual', 'CDR', 'CDSMinValid')
    CMP(S, CD, 'CDP_CdrBelowMax', 'LessThanEqual', 'CDR', 'CDSMaxValid')
    AND(S, CD, 'CDP_DTValid', 'CDSValid', 'CDP_CdrAboveMin', 'CDP_CdrBelowMax')
    AND(S, CD, 'CDP_LoopEnable', 'PlantPermissive', 'CDP_AnyProven', 'CDP_VariableSpeedEnable')
    MATH(S, CD, 'CDP_CH01CondDT', 'Subtract', 'CH01_CdwLeavingTemp', 'CH01_CdwEnteringTemp')
    MATH(S, CD, 'CDP_CH02CondDT', 'Subtract', 'CH02_CdwLeavingTemp', 'CH02_CdwEnteringTemp')
    MATH(S, CD, 'CDP_CondDTMax', 'Maximum', 'CDP_CH01CondDT', 'CDP_CH02CondDT', note='highest running-chiller condenser range')
    MATH(S, CD, 'CDP_DTRatio', 'Divide', 'CDP_CondDTMax', 'CDP_DeltaTSetpoint')
    MATH(S, CD, 'CDP_DTPI', 'Multiply', 'CDP_DTRatio', 'FixedCDPSpeedPct', note='speed for design range = present speed x range / setpoint')
    MATH(S, CD, 'CDP_FlowTarget', 'Multiply', 'Cdw_MinFlowSum', 'CDP_MinFlowMargin')
    SW(S, CD, 'CDP_Run01', 'CDP01RunProof', 'One', 'ZeroSpeed')
    SW(S, CD, 'CDP_Run02', 'CDP02RunProof', 'One', 'ZeroSpeed')
    MATH(S, CD, 'CDP_RunCount', 'Add', 'CDP_Run01', 'CDP_Run02')
    MATH(S, CD, 'CDP_RunCountG', 'Maximum', 'CDP_RunCount', 'One')
    MATH(S, CD, 'CDP_DesignTotal', 'Multiply', 'CDP_DesignFlow', 'CDP_RunCountG')
    MATH(S, CD, 'CDP_FlowRatio', 'Divide', 'CDP_FlowTarget', 'CDP_DesignTotal')
    MATH(S, CD, 'CDP_FlowPI', 'Multiply', 'CDP_FlowRatio', 'HundredPct', note='min-flow speed (affinity: flow ~ speed)')
    MATH(S, CD, 'CDP_SpeedMaxRaw', 'Maximum', 'CDP_DTPI', 'CDP_FlowPI', 'CDP_MinSpeedPct')
    LIMIT(S, CD, 'CDP_SpeedMax', 'CDP_SpeedMaxRaw', 0, 100)
    OR(S, CD, 'CDP_AnyChillerRun', 'CH01RunProofSelected', 'CH02RunProofSelected')
    DLY(S, CD, 'CDP_ChillerStable', 'CDP_AnyChillerRun', tm(prof, 300000, 240000), note='fixed speed until a chiller has run 5 min (start transient)')
    AND(S, CD, 'CDP_UseLoop', 'CDP_LoopEnable', 'CDP_DTValid', 'CDP_ChillerStable')
    SW(S, CD, 'CDP_SpeedSel', 'CDP_UseLoop', 'CDP_SpeedMax', 'FixedCDPSpeedPct')
    S.kc(CD, 'CDP_SpeedRate', 'NumericDelay', {'in': 'CDP_SpeedSel'}, props=[('maxStepSize', None, '0.5'), ('updateTime', 'b:RelTime', '1000')])
    S.rewire('CDP_DTPI', 'inB', 'CDP_SpeedRate', 'FixedCDPSpeedPct')
    SW(S, CD, 'CDP_SpeedFinal', 'CDP_UseLoop', 'CDP_SpeedRate', 'FixedCDPSpeedPct')
    S.npoint(CD, 'CDP_SpeedDemand', 'CDP_SpeedFinal', 'pct', 1, note='common CDP speed demand')
    for u in ('CDP01', 'CDP02'):
        S.rewire(f'{u}SpeedAboveMin', 'inA', 'CDP_SpeedFinal', 'FixedCDPSpeedPct')
    # emulation: condenser flow follows CDP speed (affinity)
    MATH(S, 'Simulation/Hydraulic', 'Sim_CdpSpeedMax', 'Maximum', 'CDP01SpeedCmd', 'CDP02SpeedCmd')
    MATH(S, 'Simulation/Hydraulic', 'Sim_CdpSpeedFrac', 'Multiply', 'Sim_CdpSpeedMax', 'PctToFrac')
    MATH(S, 'Simulation/Hydraulic', 'Sim_CdwPlantFlowV', 'Multiply', 'Sim_CdwPlantFlow', 'Sim_CdpSpeedFrac')
    relink_sim(S, 'CDW_Flow', 'Sim_CdwPlantFlowV', 'CDP count x design flow x speed')
    const(S, 'Sim_FlowSwitchGpm', 100.0, 'none', 0, note='SIM: emulated flow switch opens below this flow')
    for n in ('01', '02'):   # emulated flow switch follows the real condenser flow (pump stopping -> switch opens)
        CMP(S, 'Simulation/Hydraulic', f'Sim_CH{n}_CdwFlowOk', 'GreaterThanEqual', 'Sim_CdwPlantFlowV', 'Sim_FlowSwitchGpm')
        S.rewire(f'Sim_CH{n}_CdwFlowFb', 'inC', f'Sim_CH{n}_CdwFlowOk', T)
    S.rewire('Sim_CdwFlowShare', 'inA', 'Sim_CdwPlantFlowV', 'Sim_CdwPlantFlow')
    S.rewire('Sim_CdwFlowGuard', 'inA', 'Sim_CdwPlantFlowV', 'Sim_CdwPlantFlow')
    # (4) S-01: emergency ventilation fan status + fail alarm
    di(S, IL, 'PlantRoom_EmergencyVentStatus', False, 'Running', 'Stopped', note='emergency exhaust fan run status (CT / aux contact)')
    DLY(S, 'Simulation/Chemical', 'Sim_EmergencyVentFb', 'PlantRoom_EmergencyVentCmd', 5000, 5000)
    simlink(S, 'PlantRoom_EmergencyVentStatus', 'Sim_EmergencyVentFb', 'follows the fan command')
    NOT(S, IL, 'RL_VentNoStatus', 'PlantRoom_EmergencyVentStatus')
    AND(S, IL, 'RL_VentFailLogic', 'PlantRoom_EmergencyVentCmd', 'RL_VentNoStatus')
    DLY(S, IL, 'RL_VentFailDly', 'RL_VentFailLogic', tm(prof, 30000, 8000))
    alarm(S, IL, 'PlantRoom_EmergencyVentFailAlarm', 'RL_VentFailDly', 'FAIL', 'Normal', 'Critical', 'Plant room emergency ventilation fan commanded but not running')
    # (5) A-01: OA damper closed (full recirculation) during unoccupied night high-limit cooling
    # (6) A-06: zone average temperature used in control (AHU SAT reset; FCU fallback when its own sensor fails)
    A = M7.AIR
    C = f'{A}/Common'
    S.bparam('AirSide_UseZoneTemp', True, folder=C, t='Zone average', f='Return air', note='AHU SAT reset from the zone average when the gateway is online')
    for u, zt in (('AHU01', 'Zone_AHU01_AvgTemp'), ('AHU02', 'Zone_AHU02_AvgTemp')):
        L = f'{A}/{u}/Safety'
        SW(S, L, f'{u}_OadNight', f'{u}_NightCoolActive', 'ZeroSpeed', f'{u}OadSafe')
        S.rewire(f'{u}OadGate', 'inTrue', f'{u}_OadNight', f'{u}OadSafe')
        CMP(S, L, f'{u}_ZoneAbove', 'GreaterThanEqual', zt, f'Valid_{u}_RAT_Lo')
        CMP(S, L, f'{u}_ZoneBelow', 'LessThanEqual', zt, f'Valid_{u}_RAT_Hi')
        AND(S, L, f'{u}_UseZone', 'AirSide_UseZoneTemp', 'AirPlug_GatewayOnline', f'{u}_ZoneAbove', f'{u}_ZoneBelow')
        SW(S, L, f'{u}_CtrlTempSel', f'{u}_UseZone', zt, f'{u}_RAT')
        S.npoint(L, f'{u}_ControlTemp', f'{u}_CtrlTempSel', 'C', 1, note='temperature used for SAT reset (zone average or RAT)')
        S.rewire(f'{u}SatReset', 'inA', f'{u}_ControlTemp', f'{u}_RAT')
        OR(S, L, f'{u}_CtrlTempValid', f'{u}_UseZone', f'{u}_RATValid')
        S.rewire(f'{u}SatSpSelect', 'inSwitch', f'{u}_CtrlTempValid', f'{u}_RATValid')
    for n in ('01', '02', '03', '04'):
        u, L = f'FCU{n}', f'{A}/FCU{n}/Logic'
        CMP(S, L, f'{u}_ZoneAbove', 'GreaterThanEqual', 'Zone_FCU_AvgTemp', f'Valid_{u}_RoomTemp_Lo')
        CMP(S, L, f'{u}_ZoneBelow', 'LessThanEqual', 'Zone_FCU_AvgTemp', f'Valid_{u}_RoomTemp_Hi')
        AND(S, L, f'{u}_ZoneOk', 'AirPlug_GatewayOnline', f'{u}_ZoneAbove', f'{u}_ZoneBelow')
        SW(S, L, f'{u}_CtrlTempSel', f'{u}_RoomTempValid', f'{u}_RoomTemp', 'Zone_FCU_AvgTemp')
        S.npoint(L, f'{u}_ControlTemp', f'{u}_CtrlTempSel', 'C', 1, note='own room sensor; zone average when the sensor fails')
        OR(S, L, f'{u}_CtrlValid', f'{u}_RoomTempValid', f'{u}_ZoneOk')
        S.rewire(f'{u}Error', 'inA', f'{u}_ControlTemp', f'{u}_RoomTemp')
        S.rewire(f'{u}Invalid', 'in', f'{u}_CtrlValid', f'{u}_RoomTempValid')
        S.rewire(f'{u}HighLogic', 'inC', f'{u}_CtrlValid', f'{u}_RoomTempValid')
    S.log.append(('V7.7r1', '', 'SOO review fixes', 'stage hold, VPF vs low dT, CDP VSD, vent status, night OAD, zone temp', '', ''))


def units77(S, prof):
    FCX.PROF[0] = prof
    interlocks(S, prof)
    cdw_chem(S, prof)
    chw_chem(S, prof)
    airside77(S, prof)
    M76.units76(S, prof)       # V7.6 hydraulics + staging + sizing, then kPa -> bar / m3h -> gpm
    review_fixes(S, prof)


M74.units = units77
_px = [n for _, n in M7.PX_PLANT]
M7.PX_PLANT.insert(_px.index('ALT_V76_Design') + 1, ('Safety', 'ALT_V77_Safety'))
M7.PX_PLANT.insert(_px.index('ALT_V76_Design') + 2, ('Commissioning', 'ALT_V77_Commissioning'))
M7.PX_PLANT.insert(_px.index('ALT_V76_Design') + 3, ('FieldIO', 'ALT_V77_FieldIO'))
M7.PX_PLANT.insert(_px.index('ALT_V76_Design') + 4, ('AssetHealth', 'ALT_V77_Health'))

if __name__ == '__main__':
    M7.main()
