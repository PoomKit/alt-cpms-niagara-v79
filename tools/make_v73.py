"""Build ALT_CP_Ref_V7_3 = V7.2 (make_v72.py -> make_v71.py -> make_v7.py, imported unchanged) + V7.3 layer.

V7.3 (user request 29 Sep 2026):
  1. Cooling tower SOO (Kittipoom S., 'SOO for Cooling Tower' - add / reduce operation) + tower CELLS:
     every tower = 2 fan cells, each with its own VSD (CT01/01, CT01/02, CT02/01, CT02/02 -> CT01_01 ... CT02_02).
       * plant enable: >= 1 chiller request, CDP running, CDW circulating (flow / chiller flow switch), tower healthy
       * 1 chiller: lead tower only (lowest runtime) -> isolation valves proven -> fans start at the initial speed -> PID (direct)
         stage LAG tower when CDS > SP + 1.0 K AND tower speed >= 90 % for 10 min; DE-STAGE when 1 chiller AND CDS < SP - 0.5 K
         AND speed <= low threshold for 30 min; lag then locked off for the minimum stop time
       * 2 chillers: both towers (reduction locked out unless single-tower hydraulics is verified)
       * extra (better than the SOO): CDS sensor invalid -> all towers at fail-safe speed; lead tower lost a cell -> lag staged
         at once; failed start permissive -> alarm; cell failure = other cell keeps running
  2. CHW bypass: bypass flow meter removed; modulating min-flow valve on the sum of evaporator flows; manual bypass loop
     (normally closed, position switch alarm) around the valve for maintenance
  4. Basin LOW-LOW (float + transmitter) -> that tower's fans stop and the tower is isolated; both towers dry -> CDPs stop
  5. Make-up water: per-basin make-up valves (emergency fill on low-low) + CHW loop fill line (expansion tank pressure,
     water meter, fill-timeout leak lock-out)
  6. Water treatment: CHW bypass (pot) chemical feeder + CDW bleed-off (conductivity) + dosing pump + tank low level
  11. Zone temperature / humidity points ready for AETERLINK Sense-T / AirPlug (BACnet names ZoneTemperatureAvg_FF_ZZZZ)
New station folder (does not touch V7 / V7.1 / V7.2).  usage: make_v73.py c_v5.bog c_v5.tsv out.bog --regdir reg73 [--timing fpt]
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_v6 as M6
import make_v7 as M7
import make_v71 as M71
import make_v72 as M72
from make_v7 import AND, OR, NOT, DLY, PULSE, SW, MATH, CMP, const, ai, di, simlink, ramp, T, F, UNITS, AIR

M6.STATION = M7.STATION = 'ALT_CP_Ref_V7_3'
M7.FOXS_PORT = '4921'
M6.TIMING['site'].update(ct_stage_up=600000, ct_stage_down=1800000, ct_min_stop=600000, ct_init=60000, ct_ll=5000,
                         ct_permit_alarm=120000, chw_fill_max=1800000, zone_alarm=900000)
M6.TIMING['fpt'].update(ct_stage_up=5000, ct_stage_down=8000, ct_min_stop=6000, ct_init=2000, ct_ll=1000,
                        ct_permit_alarm=5000, chw_fill_max=20000, zone_alarm=5000)

CELLS = [(f'CT{n}', f'CT{n}_{k}') for n in UNITS for k in UNITS]          # (tower, cell)
CELL_NAME = {c: f'CT-{c[2:4]}/{c[5:]}' for _, c in CELLS}                 # display 'CT-01/01'
# plant drives: CHP / CDP + the 4 tower cells (tower-level VSD removed - every cell has its own drive)
M71.PLANT_VSD[:] = [x for x in M71.PLANT_VSD if not x[0].startswith('CT')] + [(c, 20.0) for _, c in CELLS]
SI = 'Simulation/Instruments'
TS = 'CdwLoop/TowerStaging'
ZF = f'{AIR}/Zones'
ZONES = [  # (code, room name, served by)  - AirPlug naming ZoneTemperatureAvg_<floor>_<zone>
    ('01_0101', 'Lobby', 'AHU01'), ('01_0102', 'Reception', 'AHU01'), ('01_0103', 'Open office A', 'AHU01'),
    ('01_0104', 'Open office B', 'AHU01'), ('01_0105', 'Meeting 1', 'AHU02'), ('01_0106', 'Meeting 2', 'AHU02'),
    ('01_0107', 'Training', 'AHU02'), ('01_0108', 'Executive', 'AHU02'), ('01_0109', 'Server room', 'FCU'),
    ('01_0110', 'Pantry', 'FCU'), ('01_0111', 'Storage', 'OAU01'), ('01_0112', 'Corridor', 'OAU01')]


def unlink(S, target, slot):
    el = S.comp[target]
    L = [c for c in el if c.get('t') == 'b:Link' and M6.child(c, 'targetSlotName').get('v') == slot]
    assert len(L) == 1, (target, slot, len(L))
    el.remove(L[0])
    S.log.append(('UNLINK', '', target, slot, '', ''))


def consumers(S, name):
    h = S.handle(name)
    return [(n, M6.child(L, 'targetSlotName').get('v')) for n, e in S.comp.items() for L in e
            if L.get('t') == 'b:Link' and M6.child(L, 'sourceOrd').get('v') == 'h:' + h]


# ============================================================ 1a. tower cells (runs BEFORE the V7.1 layer: VFD details / min-max)
def ct_cells(S, prof):
    const(S, 'CT_CellRatedKW', 5.5, 'kW', 1, note='SIM: fan motor per cell (2 cells = 11 kW tower)')
    S.param('CT_InitialSpeed', 40.0, 'pct', folder=TS, lo=0, hi=100, note='SOO: fan ramps to this speed after start, then PID')
    S.npoint('CdwLoop/TowerControl', 'CT_CommonSpeed', 'CDS_RateLimit', 'pct', 1,
             note='CDS PID output (direct acting) after rate limit / fail-safe = common cell speed request')
    for tw, c in CELLS:
        P, L = f'{c}/Points', f'{c}/Logic'
        nm = CELL_NAME[c]
        di(S, P, f'{c}InAuto', True, 'Auto', 'Hand/Off', note=f'{nm} VFD / MCC HOA in AUTO')
        di(S, P, f'{c}VfdFault', False, 'Fault', 'Normal', note=f'{nm} VFD fault')
        di(S, P, f'{c}VibrationAlarm', False, 'Trip', 'Normal', note=f'{nm} fan vibration switch')
        di(S, P, f'{c}Fault', False, 'Fault', 'Normal', note=f'{nm} motor overload / local isolator open')
        S.bparam(f'{c}_ServiceIsolate', False, folder=P, t='OUT OF SERVICE', f='In service',
                 note='maintenance: take this cell out of service (other cell keeps running)')
        di(S, P, f'{c}RunProof', False, 'Run', 'Stop', note=f'{nm} VFD run status')
        add_ext = M6.add_ext
        add_ext(S, f'{c}RunProof', 'Runtime', 'c:DiscreteTotalizerExt')
        S.bpoint(P, f'{c}StartCmd', F, 'START', 'STOP', kind='do', note=f'{nm} VFD start')
        OR(S, L, f'{c}FaultAny', f'{c}Fault', f'{c}VfdFault', f'{c}VibrationAlarm', f'{c}_ServiceIsolate')
        NOT(S, L, f'{c}NotFaultAny', f'{c}FaultAny')
        NOT(S, L, f'{c}NotRunProof', f'{c}RunProof')
        AND(S, L, f'{c}NoProofWhileCmd', f'{c}StartCmd', f'{c}NotRunProof')
        DLY(S, L, f'{c}ProofFailDelay', f'{c}NoProofWhileCmd', prof['fan_proof'], note='run status not proven -> cell failed')
        PULSE(S, L, f'{c}ResetFire', note=f'Px RESET {nm} -> action fire')
        OR(S, L, f'{c}ResetAny', f'{c}ResetFire', 'PlantAlarmResetFire', f'{tw}ResetFire')
        M7.sealin(S, L, f'{c}FailLatch', f'{c}ProofFailDelay', f'{c}ResetAny', note='latched until RESET (cell / tower / plant)')
        NOT(S, L, f'{c}NotFailLatched', f'{c}FailLatch')
        AND(S, L, f'{c}Healthy', f'{c}NotFaultAny', f'{c}NotFailLatched', f'{c}InAuto')
        AND(S, L, f'{c}StartLogic', f'{tw}StartCmd', f'{c}Healthy', note='cell runs with its tower (both cells share the load)')
        S.rewire(f'{c}StartCmd', 'in16', f'{c}StartLogic', F)
        DLY(S, L, f'{c}InitDone', f'{c}RunProof', prof['ct_init'], note='SOO: hold the initial speed after the start')
        SW(S, L, f'{c}SpeedSel', f'{c}InitDone', 'CT_CommonSpeed', 'CT_InitialSpeed')
        SW(S, L, f'{c}SpeedGate', f'{c}StartCmd', f'{c}SpeedSel', 'ZeroSpeed')
        S.npoint(P, f'{c}SpeedCmd', f'{c}SpeedGate', 'pct', 1, kind='ao', note=f'{nm} VFD speed command')
        S.bpoint('Alarms', f'{c}_FailAlarm', f'{c}FailLatch', 'Failed', 'Normal')
        S.bpoint(f'{c}/Monitor', f'{c}_FaultSts', f'{c}FaultAny', 'FAULT', 'OK', note='any cell fault / trip / out of service (graphics)')
        NOT(S, 'Alarms', f'{c}NotInAutoLogic', f'{c}InAuto')
        S.bpoint('Alarms', f'{c}_NotInAutoAlarm', f'{c}NotInAutoLogic', 'Not auto', 'Normal')
        M6.COS.update({f'{c}_FailAlarm': (True, 'Critical', f'{nm} fan failed to prove - cell locked out, press RESET'),
                       f'{c}_NotInAutoAlarm': (True, 'Warning', f'{nm} HOA not in AUTO'),
                       f'{c}VfdFault': (True, 'Warning', f'{nm} VFD fault'),
                       f'{c}VibrationAlarm': (True, 'Critical', f'{nm} fan vibration trip'),
                       f'{c}Fault': (True, 'Warning', f'{nm} motor overload / isolator')})
        M6.CMD_FAIL[f'{c}StartCmd'] = (f'{c}RunProof', 'Critical', 30000)
        # field analogs (VFD via BACnet / Modbus)
        ai(S, P, f'{c}_FanSpeedHz', 0.0, 'Hz', note='VFD output frequency', hist='5min')
        ai(S, P, f'{c}_Amps', 0.0, 'A', note='VFD motor current', hist='5min')
        ai(S, P, f'{c}_kW', 0.0, 'kW', note='VFD output power', hist='5min')
        add_ext(S, f'{c}_kW', 'Energy', 'c:NumericTotalizerExt', [('totalizationInterval', None, 'hourly')])
        S.npoint(f'{c}/Monitor', f'{c}_kWh', f'{c}_kW:Energy.total', 'kWh', 1)
        S.kc(f'{c}/Monitor', f'{c}RuntimeHoursCalc', 'Divide', {'inA': f'{c}RunProof:Runtime.elapsedActiveTimeNumeric', 'inB': 'MsPerHour'})
        S.npoint(f'{c}/Monitor', f'{c}_RuntimeHours', f'{c}RuntimeHoursCalc', 'hr', 1)
        # emulation
        DLY(S, SI, f'Sim_{c}_RunFb', f'{c}StartCmd', prof['fan_proof'] // 3, 1000, note='emulated VFD run status')
        simlink(S, f'{c}RunProof', f'Sim_{c}_RunFb')
        SW(S, SI, f'Sim_{c}_On', f'Sim_{c}_RunFb', 'One', 'ZeroSpeed')
        MATH(S, SI, f'Sim_{c}_Frac', 'Divide', f'{c}SpeedCmd', 'PlantReset_Full')
        MATH(S, SI, f'Sim_{c}_kWc', 'Multiply', f'Sim_{c}_Frac', f'Sim_{c}_Frac', f'Sim_{c}_Frac', 'CT_CellRatedKW')
        MATH(S, SI, f'Sim_{c}_kWr', 'Multiply', f'Sim_{c}_kWc', f'Sim_{c}_On'); simlink(S, f'{c}_kW', f'Sim_{c}_kWr', 'affinity law')
        MATH(S, SI, f'Sim_{c}_Hz', 'Multiply', f'{c}SpeedCmd', 'HzPerPct', f'Sim_{c}_On'); simlink(S, f'{c}_FanSpeedHz', f'Sim_{c}_Hz')
        MATH(S, SI, f'Sim_{c}_A', 'Multiply', f'{c}_kW', 'Amps_per_kW'); simlink(S, f'{c}_Amps', f'Sim_{c}_A')


# ============================================================ 1b. tower = sum of its cells
def ct_towers(S, prof):
    for n in UNITS:
        tw = f'CT{n}'; L = f'{tw}/Logic'
        c1, c2 = f'{tw}_01', f'{tw}_02'
        OR(S, L, f'{tw}CellsAnyRun', f'{c1}RunProof', f'{c2}RunProof', note='tower proven = any cell proven')
        unlink(S, f'{tw}RunProof', 'in10'); S.link(S.comp[f'{tw}RunProof'], f'{tw}CellsAnyRun', 'in16')
        S.meta.setdefault(f'{tw}RunProof', {})['kind'] = 'calc'
        OR(S, L, f'{tw}CellsAnyHealthy', f'{c1}Healthy', f'{c2}Healthy')
        NOT(S, L, f'{tw}CellsAllFailed', f'{tw}CellsAnyHealthy')
        AND(S, L, f'{tw}CellsBoth', f'{c1}Healthy', f'{c2}Healthy')
        NOT(S, L, f'{tw}CellsNotBoth', f'{tw}CellsBoth')
        AND(S, L, f'{tw}CellsVfdAll', f'{c1}VfdFault', f'{c2}VfdFault')
        S.link(S.comp[f'{tw}VfdFault'], f'{tw}CellsVfdAll', 'in16'); S.meta.setdefault(f'{tw}VfdFault', {})['kind'] = 'calc'
        AND(S, L, f'{tw}CellsVibAll', f'{c1}VibrationAlarm', f'{c2}VibrationAlarm')
        S.link(S.comp[f'{tw}VibrationAlarm'], f'{tw}CellsVibAll', 'in16'); S.meta.setdefault(f'{tw}VibrationAlarm', {})['kind'] = 'calc'
        # tower meters = sum / max of the cells
        MATH(S, L, f'{tw}CellsKW', 'Add', f'{c1}_kW', f'{c2}_kW')
        S.rewire(f'{tw}_kW', 'in16', f'{tw}CellsKW')
        MATH(S, L, f'{tw}CellsHz', 'Maximum', f'{c1}_FanSpeedHz', f'{c2}_FanSpeedHz')
        S.rewire(f'{tw}_FanSpeedHz', 'in10', f'{tw}CellsHz')
        MATH(S, L, f'{tw}CellsAmps', 'Add', f'{c1}_Amps', f'{c2}_Amps')
        S.rewire(f'{tw}_Amps', 'in10', f'{tw}CellsAmps')
        MATH(S, L, f'{tw}CellsSpeed', 'Maximum', f'{c1}SpeedCmd', f'{c2}SpeedCmd')
        S.npoint(f'{tw}/Monitor', f'{tw}_CellSpeed', f'{tw}CellsSpeed', 'pct', 1, note='highest cell speed of the tower')
        S.bpoint(f'{tw}/Monitor', f'{tw}_CellsHealthy', f'{tw}CellsBoth', 'Both cells', 'Cell lost')


# ============================================================ 1c. SOO: add / reduce tower operation
def ct_soo(S, prof):
    S.param('CT_StageUpDeltaK', 1.0, 'none', folder=TS, lo=0.2, hi=5, note='SOO A: CDS above SP + this (K) ...')
    S.param('CT_StageUpSpeedPct', 90.0, 'pct', folder=TS, lo=50, hi=100, note='SOO B: ... and lead tower fans >= this % of available output')
    S.param('CT_StageDownDeltaK', 0.5, 'none', folder=TS, lo=0.1, hi=5, note='SOO reduce B: CDS below SP - this (K)')
    S.param('CT_LowSpeedPct', 35.0, 'pct', folder=TS, lo=0, hi=90, note='SOO reduce C: all running fans at / below this low-speed threshold')
    S.param('CT_CdwMinFlow', 30.0, 'm3h', folder=TS, note='SOO enable 3: condenser water circulating (header flow)')
    S.bparam('CT_SingleTowerVerified', False, folder=TS, t='Verified', f='Not verified',
             note='SOO: with 2 chillers both towers run; reduction allowed only when single-tower hydraulics is formally verified')
    S.bparam('CT_StageOnCellFail', True, folder=TS, t='Stage lag', f='Off', note='lead tower lost a fan cell -> stage the lag tower at once')
    S.set_fallback('CT_RunAllAvailable', False)      # SOO: towers follow chillers + staging (option 'All towers' kept)
    # --- SOO step 1: plant enable for the tower fans
    CMP(S, TS, 'CT_CdwFlowOK', 'GreaterThanEqual', 'CDW_Flow', 'CT_CdwMinFlow')
    OR(S, TS, 'CT_CdwCirculating', 'CT_CdwFlowOK', 'CH01CDWFlowProof', 'CH02CDWFlowProof', note='header flow OR a chiller condenser flow switch')
    AND(S, TS, 'CT_FanEnable', 'CDP_AnyProven', 'CT_CdwCirculating', note='SOO: associated CDP running AND condenser water circulating')
    for n in UNITS:
        S.rewire(f'CT{n}StartPermit', 'inD', 'CT_FanEnable', T)
    OR(S, TS, 'CT_AnyRequest', 'CT01Request', 'CT02Request')
    NOT(S, TS, 'CT_NotFanEnable', 'CT_FanEnable')
    AND(S, TS, 'CT_InhibitLogic', 'CT_AnyRequest', 'CT_NotFanEnable')
    DLY(S, TS, 'CT_InhibitDelay', 'CT_InhibitLogic', prof['ct_permit_alarm'])
    S.bpoint('Alarms', 'CT_StartInhibitedAlarm', 'CT_InhibitDelay', 'Inhibited', 'Normal')
    M6.COS['CT_StartInhibitedAlarm'] = (True, 'Warning', 'Cooling tower start inhibited - CDP not proven / no condenser water flow')
    # --- mode: one chiller (staging allowed) / two chillers (both towers)
    NOT(S, TS, 'CT_NotPoolNeed2', 'Pool_Need2')
    OR(S, TS, 'CT_OneChillerOrVerified', 'CT_NotPoolNeed2', 'CT_SingleTowerVerified')
    AND(S, TS, 'CT_OneChillerMode', 'Pool_Need1', 'CT_OneChillerOrVerified')
    NOT(S, TS, 'CT_NotSingleVerified', 'CT_SingleTowerVerified')
    AND(S, TS, 'CT_TwoChillerNeed', 'Pool_Need2', 'CT_NotSingleVerified', note='2 chillers -> 2 towers (reduction locked out)')
    # --- stage-up conditions A (CDS > SP + 1.0) AND B (speed >= 90 %) for 10 min
    MATH(S, TS, 'CT_CdsStageUpLimit', 'Add', 'CDS_Setpoint_ACTIVE', 'CT_StageUpDeltaK')
    CMP(S, TS, 'CT_CdsAboveStageUp', 'GreaterThan', 'CDS', 'CT_CdsStageUpLimit')
    CMP(S, TS, 'CT_SpeedHigh', 'GreaterThanEqual', 'CT_CommonSpeed', 'CT_StageUpSpeedPct')
    AND(S, TS, 'CT_StageUpCond', 'CT_OneChillerMode', 'CT_CdsAboveStageUp', 'CT_SpeedHigh', T, note='inD: lag minimum-stop timer')
    DLY(S, TS, 'CT_StageUpTimer', 'CT_StageUpCond', prof['ct_stage_up'], note='SOO staging delay 10 min (resets if a condition drops)')
    # --- reduce conditions A (1 chiller) B (CDS < SP - 0.5) C (speed <= low) for 30 min
    MATH(S, TS, 'CT_CdsStageDownLimit', 'Subtract', 'CDS_Setpoint_ACTIVE', 'CT_StageDownDeltaK')
    CMP(S, TS, 'CT_CdsBelowStageDown', 'LessThan', 'CDS', 'CT_CdsStageDownLimit')
    CMP(S, TS, 'CT_SpeedLow', 'LessThanEqual', 'CT_CommonSpeed', 'CT_LowSpeedPct')
    AND(S, TS, 'CT_StageDownCond', 'CT_OneChillerMode', 'CT_CdsBelowStageDown', 'CT_SpeedLow', 'CDSValid')
    DLY(S, TS, 'CT_StageDownTimer', 'CT_StageDownCond', prof['ct_stage_down'], note='SOO de-staging delay 30 min')
    NOT(S, TS, 'CT_NoChiller', 'Pool_Need1')
    OR(S, TS, 'CT_LagReset', 'CT_StageDownTimer', 'CT_NoChiller')
    OR(S, TS, 'CT_LagSet', 'CT_StageUpTimer', 'CT_TwoChillerNeed', note='2 chillers also latch 2 towers -> reduction after 30 min on 1 chiller')
    M7.sealin(S, TS, 'CT_LagStaged', 'CT_LagSet', 'CT_LagReset', note='LAG tower staged ON until the reduction conditions hold 30 min')
    DLY(S, TS, 'CT_LagStopTimer', 'CT_LagStaged', 0, prof['ct_min_stop'])
    NOT(S, TS, 'CT_NotLagStaged', 'CT_LagStaged')
    AND(S, TS, 'CT_LagMinStop', 'CT_LagStopTimer', 'CT_NotLagStaged', note='SOO: lag available again after the minimum stop period')
    NOT(S, TS, 'CT_NotLagMinStop', 'CT_LagMinStop')
    S.rewire('CT_StageUpCond', 'inD', 'CT_NotLagMinStop', T)
    # --- extras: CDS invalid -> all towers (fail-safe speed); lead tower lost a cell -> lag at once
    NOT(S, TS, 'CT_CdsInvalid', 'CDSValid')
    AND(S, TS, 'CT_CdsInvalidAll', 'Pool_Need1', 'CT_CdsInvalid')
    for n in UNITS:
        AND(S, TS, f'CT_Lead{n}Degraded', f'CT_EffLead{n}', f'CT{n}CellsNotBoth', 'CT_StageOnCellFail', 'Pool_Need1')
    OR(S, TS, 'CT_Need2Extra', 'CT_CdsInvalidAll', 'CT_Lead01Degraded', 'CT_Lead02Degraded')
    # --- water-path fail-safe: lead tower valves not proven while a chiller needs condenser water -> open every healthy
    #     tower's valves (a stuck lead valve must not lock the chiller out; the lead is failed by its own valve timeout)
    for n in UNITS:
        tw = f'CT{n}'
        # outlet valve command failure LATCHED (as the V7.2 pumps): otherwise a stuck valve 'recovers' when commanded closed
        # and the tower is re-selected as lead every cycle
        M7.sealin(S, f'{tw}/Logic', f'{tw}MVFailLatch', f'{tw}_OutletMVFailDelay', f'{tw}ManualReset', note='latched until RESET')
        S.rewire(f'{tw}FaultAny', 'inD', f'{tw}MVFailLatch', f'{tw}_OutletMVFailDelay')
        S.bpoint('Alarms', f'{tw}_MVFailLatchedAlarm', f'{tw}MVFailLatch', 'Valve failed', 'Normal')
        M6.COS[f'{tw}_MVFailLatchedAlarm'] = (True, 'Critical', f'{tw} outlet valve failed - tower locked out, press RESET')
    for n in UNITS:
        AND(S, TS, f'CT_Lead{n}PathOK', f'CT_EffLead{n}', f'CT{n}WaterPathProof')
    OR(S, TS, 'CT_LeadPathOK', 'CT_Lead01PathOK', 'CT_Lead02PathOK')
    NOT(S, TS, 'CT_LeadPathNotOK', 'CT_LeadPathOK')
    AND(S, TS, 'CT_PathMissing', 'Pool_Need1', 'CT_LeadPathNotOK')
    DLY(S, TS, 'CT_PathMissingDelay', 'CT_PathMissing', prof['pool_bridge'], note='lead tower valves should prove within the stroke time')
    OR(S, TS, 'CT_PathFailSafeReset', 'CT_NoChiller', 'CT_LeadPathOK')
    M7.sealin(S, TS, 'CT_PathFailSafe', 'CT_PathMissingDelay', 'CT_PathFailSafeReset', note='all tower valves open until the lead tower path proves')
    OR(S, TS, 'CT_ValvesAllOpenLogic', 'CT_NoneLogic', 'CT_PathFailSafe')
    S.rewire('CT_ValvesFailSafe', 'inB', 'CT_ValvesAllOpenLogic', 'CT_NoneLogic')
    S.rewire('CT_Need2', 'inA', 'CT_TwoChillerNeed', 'Pool_Need2')
    S.rewire('CT_Need2', 'inC', 'CT_LagStaged', F)
    S.rewire('CT_Need2', 'inD', 'CT_Need2Extra', F)
    # --- monitor points (graphics / history)
    Mo = 'CdwLoop/Monitor'
    S.bpoint(Mo, 'CT_Mode2Towers', 'CT_Need2', '2 TOWERS', '1 TOWER', note='towers requested')
    S.bpoint(Mo, 'CT_LagStagedSts', 'CT_LagStaged', 'Lag staged', 'Lead only')
    S.bpoint(Mo, 'CT_StageUpCondSts', 'CT_StageUpCond', 'Timing (10 min)', 'Not met')
    S.bpoint(Mo, 'CT_StageDownCondSts', 'CT_StageDownCond', 'Timing (30 min)', 'Not met')
    S.bpoint(Mo, 'CT_LagMinStopSts', 'CT_LagMinStop', 'Min stop', 'Available')
    S.bpoint(Mo, 'CT_FanEnableSts', 'CT_FanEnable', 'Enabled', 'Inhibited')
    S.bpoint(Mo, 'CT_OneChillerModeSts', 'CT_OneChillerMode', '1 chiller', '2 chillers / off')
    S.npoint(Mo, 'CT_CdsStageUpSP', 'CT_CdsStageUpLimit', 'C', 1)
    S.npoint(Mo, 'CT_CdsStageDownSP', 'CT_CdsStageDownLimit', 'C', 1)


# ============================================================ 4. basin LOW-LOW interlock
def ct_lowlow(S, prof):
    S.param('CT_LevelLowLowPct', 15.0, 'pct', folder=TS, note='basin LOW-LOW (dry-run) trip level')
    S.param('CT_LevelLowLowResetPct', 30.0, 'pct', folder=TS, note='LOW-LOW clears when the level recovers above this')
    for n in UNITS:
        tw = f'CT{n}'; L = f'{tw}/Logic'; P = f'{tw}/Points'
        di(S, P, f'{tw}_LowLowLevelSwitch', False, 'LOW-LOW', 'Normal', note='LSLL basin low-low float (dry-run protection)')
        CMP(S, L, f'{tw}LevelBelowLL', 'LessThan', f'{tw}_BasinLevel', 'CT_LevelLowLowPct')
        AND(S, L, f'{tw}LevelLLAnalog', f'{tw}LevelBelowLL', f'{tw}NotLevelSensorBad', note='transmitter only when in range')
        OR(S, L, f'{tw}LevelLLLogic', f'{tw}LevelLLAnalog', f'{tw}_LowLowLevelSwitch')
        DLY(S, L, f'{tw}LevelLLDelay', f'{tw}LevelLLLogic', prof['ct_ll'])
        CMP(S, L, f'{tw}LevelAboveLLReset', 'GreaterThan', f'{tw}_BasinLevel', 'CT_LevelLowLowResetPct')
        NOT(S, L, f'{tw}NotLLSwitch', f'{tw}_LowLowLevelSwitch')
        AND(S, L, f'{tw}LLRecovered', f'{tw}LevelAboveLLReset', f'{tw}NotLLSwitch')
        M7.sealin(S, L, f'{tw}BasinLL', f'{tw}LevelLLDelay', f'{tw}LLRecovered', note='held until the basin refills')
        S.bpoint('Alarms', f'{tw}BasinLowLowLevelAlarm', f'{tw}BasinLL', 'LOW-LOW', 'Normal')
        M6.COS[f'{tw}BasinLowLowLevelAlarm'] = (True, 'Critical', f'{tw} basin LOW-LOW - tower fans stopped, tower isolated, emergency make-up open')
        # interlock: tower out of the pool (fans stop), valves closed (CDP no longer draws from a dry basin)
        OR(S, L, f'{tw}TowerFault', f'{tw}Fault', f'{tw}BasinLL', f'{tw}CellsAllFailed', note='tower unavailable')
        S.rewire(f'{tw}FaultAny', 'inA', f'{tw}TowerFault', f'{tw}Fault')
        NOT(S, L, f'{tw}NotBasinLL', f'{tw}BasinLL')
        AND(S, L, f'{tw}ValveDemandLL', f'{tw}ValveDemand', f'{tw}NotBasinLL', note='a dry basin is isolated even in valve fail-safe')
        S.rewire(f'{tw}ValveOpenCmd', 'in16', f'{tw}ValveDemandLL', f'{tw}ValveDemand')
        S.rewire(f'{tw}_OutletMVCmd', 'in16', f'{tw}ValveDemandLL', f'{tw}ValveDemand')
        # emergency make-up on low-low (float) even with a failed transmitter; never against HIGH-HIGH
        AND(S, L, f'{tw}MakeupEmergency', f'{tw}BasinLL', f'{tw}NotLevelHH')
        OR(S, L, f'{tw}MakeupCmdLogic', f'{tw}MakeupPermit', f'{tw}MakeupEmergency')
        S.rewire(f'{tw}_MakeupValveCmd', 'in16', f'{tw}MakeupCmdLogic', f'{tw}MakeupPermit')
    AND(S, TS, 'CT_AllBasinsLL', 'CT01BasinLL', 'CT02BasinLL')
    NOT(S, TS, 'CT_BasinWaterOK', 'CT_AllBasinsLL')
    for n in UNITS:
        S.rewire(f'CDP{n}StartPermitMV', 'inC', 'CT_BasinWaterOK', T)
    AND(S, 'Alarms', 'CT_AllBasinsDryLogic', 'CT_AllBasinsLL', 'Pool_Need1')
    S.bpoint('Alarms', 'CT_AllBasinsDryAlarm', 'CT_AllBasinsDryLogic', 'No water', 'Normal')
    M6.COS['CT_AllBasinsDryAlarm'] = (True, 'Emergency', 'Both tower basins LOW-LOW - condenser pumps stopped (dry-run protection), heat rejection lost')


# ============================================================ 5. make-up water: basins + CHW loop fill
def makeup(S, prof):
    MU = 'MakeupWater'
    ai(S, f'{MU}/Points', 'MU_SupplyPressure', 250.0, 'kPa', note='PT make-up water header (from the water tank / booster set)', hist='5min')
    S.param('MU_SupplyLowKPa', 100.0, 'kPa', folder=f'{MU}/Points', note='make-up header pressure low alarm')
    CMP(S, 'Alarms', 'MU_SupplyLow', 'LessThan', 'MU_SupplyPressure', 'MU_SupplyLowKPa')
    DLY(S, 'Alarms', 'MU_SupplyLowDelay', 'MU_SupplyLow', 60000 if prof is M6.TIMING['site'] else 2000)
    S.bpoint('Alarms', 'MU_SupplyLowAlarm', 'MU_SupplyLowDelay', 'Low', 'Normal')
    M6.COS['MU_SupplyLowAlarm'] = (True, 'Warning', 'Make-up water header pressure low - basins / CHW loop cannot be filled')
    ramp(S, 'Sim_MU_Supply', 'SineWave', 2400000, 15.0, 250.0, 'kPa', target='MU_SupplyPressure')
    # CHW loop fill (closed loop top-up) at the expansion tank: RPZ + PRV + meter + solenoid valve
    S.param('CHW_FillOnKPa', 180.0, 'kPa', folder=f'{MU}/Points', note='open the CHW fill valve below this expansion-tank pressure')
    S.param('CHW_FillOffKPa', 200.0, 'kPa', folder=f'{MU}/Points', note='close the CHW fill valve above this pressure')
    L = f'{MU}/Logic'
    CMP(S, L, 'CHW_FillBelowOn', 'LessThan', 'CHW_ExpansionTankPressure', 'CHW_FillOnKPa')
    CMP(S, L, 'CHW_FillAboveOff', 'GreaterThan', 'CHW_ExpansionTankPressure', 'CHW_FillOffKPa')
    M7.sealin(S, L, 'CHW_FillDemand', 'CHW_FillBelowOn', 'CHW_FillAboveOff', note='fill 180 -> 200 kPa')
    DLY(S, L, 'CHW_FillTooLong', 'CHW_FillDemand', prof['chw_fill_max'], note='continuous fill = leak / burst pipe')
    PULSE(S, L, 'CHW_FillResetFire', note='Px RESET fill lock-out')
    OR(S, L, 'CHW_FillResetAny', 'CHW_FillResetFire', 'PlantAlarmResetFire')
    M7.sealin(S, L, 'CHW_FillLockout', 'CHW_FillTooLong', 'CHW_FillResetAny', note='fill valve locked closed until RESET (flood protection)')
    NOT(S, L, 'CHW_FillNotLocked', 'CHW_FillLockout')
    AND(S, L, 'CHW_FillPermit', 'CHW_FillDemand', 'CHW_FillNotLocked')
    S.bpoint(f'{MU}/Points', 'CHW_FillValveCmd', 'CHW_FillPermit', 'OPEN', 'CLOSE', kind='do', note='CHW loop make-up (fill) solenoid valve')
    ai(S, f'{MU}/Points', 'CHW_FillFlow', 0.0, 'm3h', note='FM CHW fill water meter (pulse)', hist='5min')
    M6.add_ext(S, 'CHW_FillFlow', 'Volume', 'c:NumericTotalizerExt', [('totalizationInterval', None, 'hourly')])
    S.npoint(f'{MU}/Monitor', 'CHW_FillVolume', 'CHW_FillFlow:Volume.total', 'm3', 2, note='water added to the closed CHW loop')
    S.bpoint('Alarms', 'CHW_FillLockoutAlarm', 'CHW_FillLockout', 'Locked out', 'Normal')
    M6.COS['CHW_FillLockoutAlarm'] = (True, 'Critical', 'CHW loop fill ran too long - possible leak, fill valve locked closed (RESET)')
    const(S, 'Sim_FillFlowOpen', 1.2, 'm3h')
    SW(S, SI, 'Sim_CHW_FillFlow', 'CHW_FillValveCmd', 'Sim_FillFlowOpen', 'ZeroSpeed'); simlink(S, 'CHW_FillFlow', 'Sim_CHW_FillFlow')
    OR(S, L, 'MU_BasinFillLogic', 'CT01_MakeupValveCmd', 'CT02_MakeupValveCmd')
    S.bpoint(f'{MU}/Monitor', 'MU_BasinFilling', 'MU_BasinFillLogic', 'Filling', 'Idle')


# ============================================================ 6. water treatment
def treatment(S, prof):
    WT = 'CdwLoop/WaterTreatment'
    S.param('CT_BleedOnUs', 2000.0, 'none', folder=WT, prec=0, note='bleed-off opens above this conductivity (uS/cm) - water treatment contractor')
    S.param('CT_BleedOffUs', 1800.0, 'none', folder=WT, prec=0, note='bleed-off closes below this conductivity')
    CMP(S, WT, 'CT_CondAboveBleed', 'GreaterThan', 'CT_Conductivity', 'CT_BleedOnUs')
    CMP(S, WT, 'CT_CondBelowBleed', 'LessThan', 'CT_Conductivity', 'CT_BleedOffUs')
    M7.sealin(S, WT, 'CT_BleedDemand', 'CT_CondAboveBleed', 'CT_CondBelowBleed')
    AND(S, WT, 'CT_BleedPermit', 'CT_BleedDemand', 'CT_CdwCirculating', note='only with condenser water circulating')
    S.bpoint(WT, 'CT_BleedValveCmd', 'CT_BleedPermit', 'OPEN', 'CLOSE', kind='do', note='CDW bleed-off (blow-down) solenoid valve')
    AND(S, WT, 'CT_DosingLogic', 'CT_CdwCirculating', 'MU_BasinFillLogic', note='dose with make-up water (proportional feed)')
    S.bpoint(WT, 'CT_ChemDosingPumpCmd', 'CT_DosingLogic', 'RUN', 'STOP', kind='do', note='inhibitor / biocide dosing pump (CDW)')
    di(S, WT, 'CT_ChemTankLowLevel', False, 'Low', 'Normal', note='chemical tank low level switch')
    M6.COS['CT_ChemTankLowLevel'] = (True, 'Warning', 'Water treatment chemical tank low - refill')
    di(S, 'ChwLoop/Points', 'CHW_ChemFeederOpen', False, 'Feeding', 'Isolated',
       note='CHW bypass (pot) chemical feeder - inlet / outlet valve position switch (manual dosing across the CHP headers)')


# ============================================================ 2. bypass: min-flow valve on evaporator flow, no bypass flow meter
def bypass(S, prof):
    for n in ('Sim_BypassFlow', 'CHW_BypassFlow', 'BypassFlowPerPct'):
        # remove the bypass flow meter (and its emulation); verify nothing else reads it
        users = [u for u in consumers(S, n) if u[0] not in ('CHW_BypassFlow', 'Sim_BypassFlow')]
        assert not users, (n, users)
    M6.remove_comp(S, 'CHW_BypassFlow'); M6.remove_comp(S, 'Sim_BypassFlow')
    if not consumers(S, 'BypassFlowPerPct'): M6.remove_comp(S, 'BypassFlowPerPct')
    S.param('Byp_MinFlowMargin', 1.10, 'none', folder='ChwLoop/Bypass', prec=2, note='bypass holds evaporator flow >= min flow x this margin')
    MATH(S, 'ChwLoop/Bypass', 'Byp_EvapFlowSum', 'Add', 'CH01_ChwFlow', 'CH02_ChwFlow', note='PV = sum of evaporator flows (per-chiller FT)')
    MATH(S, 'ChwLoop/Bypass', 'Byp_MinFlowTarget', 'Multiply', 'Byp_MinFlowSum', 'Byp_MinFlowMargin')
    S.rewire('Byp_PID', 'controlledVariable', 'Byp_EvapFlowSum', 'CHWFlow')
    S.rewire('Byp_PID', 'setpoint', 'Byp_MinFlowTarget', 'Byp_MinFlowSum')
    S.npoint('ChwLoop/Monitor', 'CHW_EvapFlowTotal', 'Byp_EvapFlowSum', 'm3h', 1, note='total evaporator flow (bypass PV)')
    S.npoint('ChwLoop/Monitor', 'CHW_BypassMinFlowSP', 'Byp_MinFlowTarget', 'm3h', 1, note='bypass setpoint = sum of min flows of valves open')
    di(S, 'ChwLoop/Points', 'CHW_BypassManualOpen', False, 'OPEN', 'Closed',
       note='manual bypass loop around the min-flow valve (maintenance) - position switch, normally closed')
    S.bpoint('Alarms', 'CHW_BypassManualOpenAlarm', 'CHW_BypassManualOpen', 'Manual bypass open', 'Normal')
    M6.COS['CHW_BypassManualOpenAlarm'] = (True, 'Warning', 'CHW manual bypass valve open - min-flow control valve bypassed (maintenance)')


# ============================================================ 11. zone T / RH (Sense-T / AirPlug ready)
def zones(S, prof):
    Z = ZF
    S.param('Zone_TempLow', 23.0, 'C', folder=f'{Z}/Settings', note='comfort band low (graphic colour)')
    S.param('Zone_TempHigh', 26.0, 'C', folder=f'{Z}/Settings', note='comfort band high (graphic colour)')
    S.param('Zone_TempAlarmHigh', 28.0, 'C', folder=f'{Z}/Settings', note='zone over-temperature alarm')
    S.param('Zone_RHAlarmHigh', 70.0, 'pct', folder=f'{Z}/Settings', note='zone high humidity alarm')
    di(S, f'{Z}/Gateway', 'AirPlug_GatewayOnline', True, 'Online', 'Offline',
       note='AETERLINK AirPlug gateway DeviceInformation_0001-systemStatus (BACnet)')
    NOT(S, 'Alarms', 'AirPlug_OfflineLogic', 'AirPlug_GatewayOnline')
    S.bpoint('Alarms', 'AirPlug_GatewayOfflineAlarm', 'AirPlug_OfflineLogic', 'Offline', 'Normal')
    M6.COS['AirPlug_GatewayOfflineAlarm'] = (True, 'Warning', 'AirPlug (Sense-T) gateway offline - zone temperature / humidity not updating')
    by = {}
    for i, (code, room, srv) in enumerate(ZONES):
        P, L = f'{Z}/Z{code}', f'{Z}/Z{code}/Logic'
        t, h, oos = f'ZoneTemperatureAvg_{code}', f'ZoneHumidityAvg_{code}', f'ZoneOutOfService_{code}'
        ai(S, P, t, 24.5, 'C', note=f'{room} - Sense-T average temperature (AirPlug BACnet AV {t})', hist='5min')
        ai(S, P, h, 55.0, 'pct', note=f'{room} - Sense-T average humidity (AirPlug BACnet AV {h})', hist='5min')
        di(S, P, oos, False, 'Out of service', 'In service', note=f'{room} - AirPlug {t}-outOfService')
        CMP(S, L, f'Z{code}_TempHigh', 'GreaterThan', t, 'Zone_TempAlarmHigh')
        NOT(S, L, f'Z{code}_InService', oos)
        AND(S, L, f'Z{code}_TempHighOK', f'Z{code}_TempHigh', f'Z{code}_InService', 'AirPlug_GatewayOnline')
        DLY(S, L, f'Z{code}_TempHighDelay', f'Z{code}_TempHighOK', prof['zone_alarm'])
        S.bpoint('Alarms', f'Zone_{code}_TempHighAlarm', f'Z{code}_TempHighDelay', 'Hot', 'Normal')
        CMP(S, L, f'Z{code}_RHHigh', 'GreaterThan', h, 'Zone_RHAlarmHigh')
        AND(S, L, f'Z{code}_RHHighOK', f'Z{code}_RHHigh', f'Z{code}_InService', 'AirPlug_GatewayOnline')
        DLY(S, L, f'Z{code}_RHHighDelay', f'Z{code}_RHHighOK', prof['zone_alarm'] * 2)
        S.bpoint('Alarms', f'Zone_{code}_RHHighAlarm', f'Z{code}_RHHighDelay', 'Humid', 'Normal')
        M6.COS[f'Zone_{code}_TempHighAlarm'] = (True, 'Warning', f'{room} ({code}) temperature high')
        M6.COS[f'Zone_{code}_RHHighAlarm'] = (True, 'Warning', f'{room} ({code}) humidity high')
        ramp(S, f'Sim_Z{code}_T', 'SineWave', 1500000 + i * 137000, 1.4 + (i % 3) * 0.4, 24.2 + (i % 4) * 0.5, 'C', target=t)
        ramp(S, f'Sim_Z{code}_H', 'SineWave', 1900000 + i * 151000, 6.0, 55.0 + (i % 3) * 3.0, 'pct', target=h)
        by.setdefault(srv, []).append(code)
    # averages per serving unit (for display; future: AHU return-air replacement / zone reset)
    const(S, 'Quarter', 0.25, prec=2); const(S, 'HalfC', 0.5, prec=2)
    for srv, codes in by.items():
        MATH(S, f'{Z}/Averages', f'Zone_{srv}_TSum', 'Add', *[f'ZoneTemperatureAvg_{c}' for c in codes])
        MATH(S, f'{Z}/Averages', f'Zone_{srv}_TAvgCalc', 'Multiply', f'Zone_{srv}_TSum', 'Quarter' if len(codes) == 4 else 'HalfC')
        S.npoint(f'{Z}/Averages', f'Zone_{srv}_AvgTemp', f'Zone_{srv}_TAvgCalc', 'C', 1, note=f'average of the zones served by {srv}')
        MATH(S, f'{Z}/Averages', f'Zone_{srv}_HSum', 'Add', *[f'ZoneHumidityAvg_{c}' for c in codes])
        MATH(S, f'{Z}/Averages', f'Zone_{srv}_HAvgCalc', 'Multiply', f'Zone_{srv}_HSum', 'Quarter' if len(codes) == 4 else 'HalfC')
        S.npoint(f'{Z}/Averages', f'Zone_{srv}_AvgRH', f'Zone_{srv}_HAvgCalc', 'pct', 1, note=f'average humidity, zones served by {srv}')
    M6.NO_HISTORY.update({'Quarter', 'HalfC'})


# ============================================================ independent-review fixes (V7.3 review 29 Sep)
def review_fixes(S, prof):
    # 1. staging uses the ACTUAL lead-tower fan speed (not the PID request); PID only runs with a tower proven (no wind-up)
    SW(S, TS, 'CT_LeadCellSpeed', 'CT_EffLead01', 'CT01CellsSpeed', 'CT02CellsSpeed', note='lead tower: highest cell speed command')
    for n in UNITS:
        AND(S, TS, f'CT_Lead{n}Run', f'CT_EffLead{n}', f'CT{n}RunProof')
    OR(S, TS, 'CT_LeadRunning', 'CT_Lead01Run', 'CT_Lead02Run')
    S.rewire('CT_SpeedHigh', 'inA', 'CT_LeadCellSpeed', 'CT_CommonSpeed')
    AND(S, TS, 'CT_SpeedHighRun', 'CT_SpeedHigh', 'CT_LeadRunning', note='SOO B: lead tower RUNNING at >= 90 %')
    S.rewire('CT_StageUpCond', 'inC', 'CT_SpeedHighRun', 'CT_SpeedHigh')
    MATH(S, TS, 'CT_MaxCellSpeed', 'Maximum', 'CT01CellsSpeed', 'CT02CellsSpeed', note='SOO reduce C: all running fans')
    S.rewire('CT_SpeedLow', 'inA', 'CT_MaxCellSpeed', 'CT_CommonSpeed')
    OR(S, TS, 'CT_AnyTowerProven', 'CT01RunProof', 'CT02RunProof')
    AND(S, 'CdwLoop/TowerControl', 'CDS_PIDEnable', 'PlantPermissive', 'CT_AnyTowerProven', note='no integrator wind-up with the fans off')
    S.rewire('CDS_PID', 'loopEnable', 'CDS_PIDEnable', 'PlantPermissive')
    S.npoint('CdwLoop/Monitor', 'CT_LeadSpeed', 'CT_LeadCellSpeed', 'pct', 1, note='lead tower fan speed (staging condition B)')
    # 2. lead tower by accumulated runtime (SOO) even when the pumps follow the chiller set
    S.bparam('CT_LeadByRuntime', True, folder=TS, t='Runtime (SOO)', f='Follow set', note='SOO: lead tower = fewer operating hours')
    NOT(S, TS, 'CT_NotLeadByRuntime', 'CT_LeadByRuntime')
    AND(S, TS, 'CT_LinkToSet', 'Set_LinkPools', 'CT_NotLeadByRuntime')
    S.rewire('CT_LeadSelSet', 'inSwitch', 'CT_LinkToSet', 'Set_LinkPools')
    # 3. lead lost a cell -> lag staged through the latch (debounced; held while degraded - no chatter)
    OR(S, TS, 'CT_LeadDegradedAny', 'CT_Lead01Degraded', 'CT_Lead02Degraded')
    DLY(S, TS, 'CT_LeadDegradedDelay', 'CT_LeadDegradedAny', prof['pool_bridge'])
    S.rewire('CT_LagSet', 'inC', 'CT_LeadDegradedDelay', F)
    S.rewire('CT_Need2Extra', 'inB', F, 'CT_Lead01Degraded'); S.rewire('CT_Need2Extra', 'inC', F, 'CT_Lead02Degraded')
    # 4. condenser pump permit rides through a tower valve changeover (e.g. dry basin isolated, other tower opening)
    S.rewire('CDW_PathOpen', 'inB', 'CT_WaterPathBridge', 'CT_WaterPathProven')
    # 5. bypass PV (evaporator flows) validity -> bypass fail-safe position
    S.param('Byp_EvapFlowMaxValid', 600.0, 'm3h', folder='ChwLoop/Bypass', note='evaporator flow meter valid range 0..max')
    for n in UNITS:
        CMP(S, 'ChwLoop/Bypass', f'Byp_CH{n}FlowAboveMin', 'GreaterThanEqual', f'CH{n}_ChwFlow', 'ZeroSpeed')
        CMP(S, 'ChwLoop/Bypass', f'Byp_CH{n}FlowBelowMax', 'LessThanEqual', f'CH{n}_ChwFlow', 'Byp_EvapFlowMaxValid')
    AND(S, 'ChwLoop/Bypass', 'Byp_EvapFlowValid', 'Byp_CH01FlowAboveMin', 'Byp_CH01FlowBelowMax', 'Byp_CH02FlowAboveMin', 'Byp_CH02FlowBelowMax')
    AND(S, 'ChwLoop/Bypass', 'Byp_PVValid', 'CHWFlowValid', 'Byp_EvapFlowValid')
    S.rewire('Byp_FailSafeSelect', 'inSwitch', 'Byp_PVValid', 'CHWFlowValid')
    NOT(S, 'Alarms', 'Byp_EvapFlowInvalidLogic', 'Byp_EvapFlowValid')
    DLY(S, 'Alarms', 'Byp_EvapFlowInvalidDelay', 'Byp_EvapFlowInvalidLogic', 60000 if prof is M6.TIMING['site'] else 2000)
    S.bpoint('Alarms', 'Byp_EvapFlowInvalidAlarm', 'Byp_EvapFlowInvalidDelay', 'Invalid', 'Normal')
    M6.COS['Byp_EvapFlowInvalidAlarm'] = (True, 'Warning', 'Evaporator flow meter out of range - bypass valve at fail-safe position')
    # 6. "2 chillers" = BOTH chillers RUN feedback (SOO), not requests incl. post-run (no false lag latch on failover)
    AND(S, TS, 'CT_TwoChRunRaw', 'CH01RunProofSelected', 'CH02RunProofSelected')
    DLY(S, TS, 'CT_TwoChRunning', 'CT_TwoChRunRaw', prof['handover_ok'], note='both chillers proven running')
    S.rewire('CT_NotPoolNeed2', 'in', 'CT_TwoChRunning', 'Pool_Need2')
    S.rewire('CT_TwoChillerNeed', 'inA', 'CT_TwoChRunning', 'Pool_Need2')
    # 7. OA wet bulb invalid -> fixed CDS setpoint (SOO), not default WB + approach
    AND(S, 'CdwLoop/TowerControl', 'CdsOptUsable', 'OptimizationEnable', 'OA_ValidLogic', note='WB reset only with a valid OA sensor')
    S.rewire('CdsLocalSelect', 'inSwitch', 'CdsOptUsable', 'OptimizationEnable')
    # 8. both basins dry: alarm while the plant is requested (not only while a chiller is)
    S.rewire('CT_AllBasinsDryLogic', 'inB', 'PlantRunRequest', 'Pool_Need1')


def remap_cell_folders(S):
    for name, fol in list(S.folder_of.items()):
        for _, c in CELLS:
            if fol == c or fol.startswith(c + '/'):
                S.folder_of[name] = f'{c[:4]}/Cell{c[5:]}' + fol[len(c):]


_v72 = M71.v71        # = make_v72.v72 (wraps the original V7.1 layer)


def kpi_fix(S, prof):
    """V7.3 fix: emulated chiller kW follows the measured cooling load (flow x dT) so Plant kW/RT is physically consistent
    (was: independent ramps -> kW/RT ~0.06, below the 0.4 floor of the dial). Part-load curve: kW = rated x (fixed + (1-fixed) x PLR)."""
    SI = 'Simulation/Feedback'
    S.param('CH_PartLoadFixedFrac', 0.15, 'none', prec=2, note='SIM: fixed share of rated kW at zero load (part-load curve)')
    S.param('CH_PartLoadVarFrac', 0.85, 'none', prec=2, note='SIM: 1 - fixed share')
    SW(S, SI, 'Sim_CH01_RunNum', 'CH01RunProofSelected', 'One', 'ZeroSpeed')
    SW(S, SI, 'Sim_CH02_RunNum', 'CH02RunProofSelected', 'One', 'ZeroSpeed')
    MATH(S, SI, 'Sim_CH_RunCount', 'Add', 'Sim_CH01_RunNum', 'Sim_CH02_RunNum')
    MATH(S, SI, 'Sim_CH_RunGuard', 'Maximum', 'Sim_CH_RunCount', 'One')
    MATH(S, SI, 'Sim_CH_ShareRT', 'Divide', 'CoolingLoad_RT', 'Sim_CH_RunGuard', note='cooling load shared by running chillers')
    MATH(S, SI, 'Sim_CH_PLRraw', 'Divide', 'Sim_CH_ShareRT', 'CH_RatedRT')
    S.kc(SI, 'Sim_CH_PLR', 'Limiter', {'inA': 'Sim_CH_PLRraw'}, props=[('inMin', None, '0.0'), ('inMax', None, '1.1')])
    MATH(S, SI, 'Sim_CH_PLRvar', 'Multiply', 'Sim_CH_PLR', 'CH_PartLoadVarFrac')
    MATH(S, SI, 'Sim_CH_kWFrac', 'Add', 'CH_PartLoadFixedFrac', 'Sim_CH_PLRvar', note='part-load kW fraction')
    for n in ('01', '02'):
        S.rewire(f'Sim_CH{n}_kWRunning', 'inA', 'Sim_CH_kWFrac', f'Sim_CH{n}_LoadFrac')


def v73(S, prof):
    ct_cells(S, prof)            # before V7.1: VFD details + min/max are generated per cell
    _v72(S, prof)
    ct_towers(S, prof)
    ct_soo(S, prof)
    ct_lowlow(S, prof)
    makeup(S, prof)
    treatment(S, prof)
    bypass(S, prof)
    zones(S, prof)
    review_fixes(S, prof)
    kpi_fix(S, prof)
    remap_cell_folders(S)


M71.v71 = v73
for key, px in (('ChillerPlant', 'ALT_V73_ChillerPlant'), ('CTPlant', 'ALT_V73_CTPlant')):
    M7.PX_PLANT.insert(1 if key == 'ChillerPlant' else 2, (key, px))
M7.PX_AIR.append(('Zones', 'ALT_V73_Zones'))

if __name__ == '__main__':
    M7.main()
