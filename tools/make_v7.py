"""Build ALT_CP_Ref_V7 — standard chiller plant + air-side logic library (reference).

V7 = V6.3 (make_v6.py, unchanged, imported) + four layers:
  1. headered(S)        CHP / CDP / CT are independent POOLS: any healthy pump or tower serves any chiller
                        (fixes: CDP01 + CHP02 failed -> plant stopped; now CHP01 + CDP02 run)
  2. instrumentation(S) BTU / flow / pressure / level / temperature transmitters, current (CT) and power meters
                        per equipment + validation, diagnostics, alarms, emulation
  3. airside(S)         AHU / FCU / OAU / exhaust & ventilation fans / car-park CO fan / stair pressurisation /
                        smoke exhaust templates + fire-alarm interface + plant demand and Trim & Respond
  4. graphics           gen_px7.py (kitPxGraphics images, separate script)
Sources: References/Sequence of Operation (AHU, FCU-2, OAU, FAN-1/3/4/5, LSF-1, CT, ETS, Chiller Manager),
MasterRFQ 208/212/301, Forestias ALC programs (chiller manager, CT manager, bypass, AHU/OAU/FCU/EF).
REFERENCE SIMULATION – NOT PROJECT APPROVED.  Output is a NEW station file.
"""
import sys, os, re, csv, zipfile, hashlib, argparse, math
import xml.etree.ElementTree as ET
from collections import OrderedDict, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_v6 as M6
from make_v6 import P, child, add_ext, U

M6.STATION = 'ALT_CP_Ref_V7'
FOXS_PORT = '4918'
STATION = M6.STATION
T, F = 'ConstantTrue', 'ConstantFalse'
U.update({'Pa': 'units=u:pascal;Pa;(m-1)(kg)(s-2);;', 'A': 'units=u:ampere;A;(A);;', 'V': 'units=u:volt;V;(m2)(kg)(s-3)(A-1);;',
          'Hz': 'units=u:hertz;Hz;(s-1);;', 'ppm': 'units=u:parts per million;ppm;;;', 'm3': 'units=u:cubic meter;m³;(m3);;',
          'RTh': 'units=u:null;RTh;;;', 'm3h_air': 'units=u:cubic meters per hour;m³/hr;(m3)(s-1);*2.777777777777778E-4;'})

# extra timer entries for the pools (site = commissioning values, fpt = compressed regression values)
M6.TIMING['site'].update(pool_bridge=30000, flow_bridge=15000, handover_ok=10000, valve_timeout=120000, pump_proof=30000, pump_retry=180000, aux_timeout=180000, fan_proof=30000, fan_min_off=60000)
M6.TIMING['fpt'].update(pool_bridge=3000, flow_bridge=2000, handover_ok=1000, valve_timeout=5000, pump_proof=3000, pump_retry=180000, aux_timeout=20000, fan_proof=5000, fan_min_off=2000)

POOLS = ('CHP', 'CDP', 'CT')
UNITS = ('01', '02')


# ============================================================ small builders
def AND(S, f, n, *i, note=''):
    i = list(i) + [T] * (4 - len(i)); return S.kc(f, n, 'And', dict(zip(('inA', 'inB', 'inC', 'inD'), i)), note=note)


def OR(S, f, n, *i, note=''):
    i = list(i) + [F] * (4 - len(i)); return S.kc(f, n, 'Or', dict(zip(('inA', 'inB', 'inC', 'inD'), i)), note=note)


def NOT(S, f, n, src, note=''):
    return S.kc(f, n, 'Not', {'in': src}, note=note)


def DLY(S, f, n, src, on, off=0, note=''):
    return S.kc(f, n, 'BooleanDelay', {'in': src}, props=[('onDelay', 'b:RelTime', str(int(on))), ('offDelay', 'b:RelTime', str(int(off)))], note=note)


def PULSE(S, f, n, src=None, ms=2000, note=''):
    return S.kc(f, n, 'OneShot', {'in': src} if src else None, props=[('time', 'b:RelTime', str(ms))], note=note)


def SW(S, f, n, sw, t, fl, note=''):
    return S.kc(f, n, 'NumericSwitch', {'inSwitch': sw, 'inTrue': t, 'inFalse': fl}, note=note)


def BSW(S, f, n, sw, t, fl, note=''):
    return S.kc(f, n, 'BooleanSwitch', {'inSwitch': sw, 'inTrue': t, 'inFalse': fl}, note=note)


def MATH(S, f, n, typ, *i, note=''):
    return S.kc(f, n, typ, dict(zip(('inA', 'inB', 'inC', 'inD'), i)), note=note)


def CMP(S, f, n, typ, a, b, note=''):
    return S.kc(f, n, typ, {'inA': a, 'inB': b}, note=note)


def LIMIT(S, f, n, src, lo, hi, note=''):
    return S.kc(f, n, 'Limiter', {'inA': src}, props=[('inMin', None, repr(float(lo))), ('inMax', None, repr(float(hi)))], note=note)


def HYST(S, f, n, src, lo, hi, note=''):
    return S.kc(f, n, 'Hysteresis', {'in': src}, props=[('inLow', None, repr(float(lo))), ('inHigh', None, repr(float(hi)))], note=note)


def RATE(S, f, n, src, step, upd=1000, note=''):
    return S.kc(f, n, 'NumericDelay', {'in': src}, props=[('maxStepSize', None, repr(float(step))), ('updateTime', 'b:RelTime', str(upd))], note=note)


def PID(S, f, n, cv, sp, en, action, kp, ki, lo, hi, note=''):
    return S.kc(f, n, 'LoopPoint', {'controlledVariable': cv, 'setpoint': sp, 'loopEnable': en},
                props=[('loopAction', None, action), ('proportionalConstant', None, repr(float(kp))), ('integralConstant', None, repr(float(ki))),
                       ('maximumOutput', None, repr(float(hi))), ('minimumOutput', None, repr(float(lo)))], note=note)


def RESET(S, f, n, src, il, ih, ol, oh, note=''):
    return S.kc(f, n, 'Reset', {'inA': src, 'inputLowLimit': il, 'inputHighLimit': ih, 'outputLowLimit': ol, 'outputHighLimit': oh}, note=note)


def const(S, name, v, unit='none', prec=1, note=''):
    if name not in S.comp:
        S.param(name, v, unit, prec=prec, note=note or 'constant')
        M6.NO_HISTORY.add(name)
    return name


def ai(S, folder, name, v, unit, prec=1, note='', hist='1min', lo=None, hi=None):
    """Field analog input (transmitter / meter register). Emulated at in10 by the Simulation folder."""
    S.param(name, v, unit, folder=folder, prec=prec, note=note or 'FIELD INPUT (emulated)', lo=lo, hi=hi)
    S.meta[name].update(kind='ai', hist=hist)
    return name


def di(S, folder, name, v, t, f, note=''):
    S.bparam(name, v, folder=folder, t=t, f=f, note=note or 'FIELD INPUT (manual fault injection / emulated)')
    S.meta[name]['kind'] = 'di'
    return name


def simlink(S, target, src, note='emulated'):
    S.link(S.comp[target], src, 'in10')
    S.log.append(('SIMLINK', '', target, 'in10', src, note))
    S.meta.setdefault(target, {})['ramp'] = note


def ramp(S, name, typ, per, amp, off, unit='none', target=None):
    props = [('period', None, str(per)), ('amplitude', None, repr(float(amp))), ('offset', None, repr(float(off)))]
    if typ == 'Ramp': props.append(('waveform', None, 'triangle'))
    props.append(('facets', 'b:Facets', U[unit] + '|precision=i:1|min=d:-inf|max=d:+inf'))
    S.kc('Simulation/Ramps', name, typ, props=props, note=f'{off - amp:g}..{off + amp:g} / {per / 60000:g} min')
    if target: simlink(S, target, name, f'{typ} {off - amp:g}..{off + amp:g} / {per / 60000:g} min')
    return name


def sealin(S, f, name, trip, reset, note=''):
    """name = trip OR (name AND NOT reset): order-independent latch (V6.2 pattern)."""
    NOT(S, f, name + 'NotReset', reset)
    S.kc(f, name, 'Or', {'inA': trip, 'inC': F, 'inD': F}, note=note)
    AND(S, f, name + 'Hold', name, name + 'NotReset')
    S.link(S.comp[name], name + 'Hold', 'inB')
    return name


# ============================================================ 1. headered pools
def headered(S, prof):
    """CHP / CDP / CT pools independent of the chillers (Forestias CT manager + filtering-pump manager pattern,
    SOO 'request next unit on failure', RFQ rotation 'failure skip').  Rules:
      * a chiller may run when its own permissives are met and each pool has >= 1 healthy unit
      * the number of pumps/towers requested = number of chillers requested (post-run included)
      * lead unit per pool by runtime (hysteresis) or manual; failed/Hand/fault units are skipped
      * proof failure latches the UNIT (not the chiller) -> standby starts; manual RESET or auto-reset
        (only when no other unit of the pool is healthy - last resort, never cycles a healthy standby)
      * make-before-break on lead change (old unit runs until the new one is proven)
      * stage 2 needs 2 healthy CHP and 2 healthy CDP; CT: 1 healthy tower is enough (alarm)"""
    PP = 'PlantControl/EquipmentPools'
    for n in UNITS:
        S.set_prop(f'CH{n}AuxProofTimeout', 'onDelay', str(prof['aux_timeout']))
    S.bparam('CT_RunAllAvailable', True, folder='PlantControl/Points', t='All towers', f='Match chillers',
             note='Energy: all healthy towers share the load at lower fan speed (affinity law) while any chiller runs')
    OR(S, PP, 'Pool_Need1', 'CH01PostRun', 'CH02PostRun', note='>= 1 chiller requested (incl. post-run)')
    AND(S, PP, 'Pool_Need2', 'CH01PostRun', 'CH02PostRun', note='2 chillers requested')
    AND(S, PP, 'CT_Need2All', 'Pool_Need1', 'CT_RunAllAvailable')
    OR(S, PP, 'CT_Need2', 'Pool_Need2', 'CT_Need2All')
    # tower isolation valves: open with the tower request, fan waits for the valve end switch
    for n in UNITS:
        u = f'CT{n}'
        S.bpoint(f'{u}/Points', f'{u}ValveOpenCmd', f'{u}Request', 'OPEN', 'CLOSE', kind='do')
        di(S, f'{u}/Points', f'{u}ValveOpenProof', False, 'Open', 'Closed', note='Tower inlet isolation valve end switch')
        NOT(S, f'{u}/Logic', f'{u}NotLowTempCutout', 'CdsLowCutout')
        AND(S, f'{u}/Logic', f'{u}StartPermit', f'{u}Request', f'{u}ValveOpenProof', f'{u}NotLowTempCutout',
            note='fan starts after valve proven open; fan OFF (not 0 %) during low-temperature cut-out')
        S.rewire(f'{u}StartCmd', 'in16', f'{u}StartPermit', f'{u}Request')
    for eq in POOLS:
        need2 = 'CT_Need2' if eq == 'CT' else 'Pool_Need2'
        S.bparam(f'{eq}_RotationMode_Runtime', True, folder='PlantControl/Points', t='Runtime', f='Manual',
                 note=f'{eq} lead by lowest runtime (24 h hysteresis) or manual selection')
        S.bparam(f'{eq}_Lead01Manual', True, folder='PlantControl/Points', t=f'{eq}01 lead', f=f'{eq}02 lead')
        for n in UNITS:
            u = f'{eq}{n}'
            di(S, f'{u}/Points', f'{u}InAuto', True, 'Auto', 'Hand/Off', note='HOA selector in AUTO (field DI)')
            di(S, f'{u}/Points', f'{u}VfdFault', False, 'Fault', 'Normal', note='VFD fault (field DI / BACnet)')
            if eq == 'CT':
                di(S, f'{u}/Points', f'{u}VibrationAlarm', False, 'Trip', 'Normal', note='Fan vibration switch')
                OR(S, f'{u}/Logic', f'{u}FaultAny', f'{u}Fault', f'{u}VfdFault', f'{u}VibrationAlarm')
            else:
                OR(S, f'{u}/Logic', f'{u}FaultAny', f'{u}Fault', f'{u}VfdFault')
            S.rewire(f'Not{u}Fault', 'in', f'{u}FaultAny', f'{u}Fault')
            S.kc(f'{u}/Logic', f'{u}RuntimeHoursCalc', 'Divide', {'inA': f'{u}RunProof:Runtime.elapsedActiveTimeNumeric', 'inB': 'MsPerHour'})
            S.npoint(f'{u}/Monitor', f'{u}_RuntimeHours', f'{u}RuntimeHoursCalc', 'hr', 1)
        # lead selection (runtime hysteresis or manual)
        S.kc(PP, f'{eq}_RuntimeDiff', 'Subtract', {'inA': f'{eq}01RuntimeHoursCalc', 'inB': f'{eq}02RuntimeHoursCalc'})
        HYST(S, PP, f'{eq}_01MoreRuntime', f'{eq}_RuntimeDiff', -24.0, 24.0, note='+24 h -> unit 02 leads, -24 h -> unit 01 leads')
        NOT(S, PP, f'{eq}_AutoLead01', f'{eq}_01MoreRuntime')
        BSW(S, PP, f'{eq}_LeadSel01', f'{eq}_RotationMode_Runtime', f'{eq}_AutoLead01', f'{eq}_Lead01Manual')
        AND(S, PP, f'{eq}_Lead01Healthy', f'{eq}_LeadSel01', f'{eq}01Healthy')
        NOT(S, PP, f'{eq}_Not02Healthy', f'{eq}02Healthy')
        NOT(S, PP, f'{eq}_Not01Healthy', f'{eq}01Healthy')
        OR(S, PP, f'{eq}_EffLead01', f'{eq}_Lead01Healthy', f'{eq}_Not02Healthy', note='selected lead if healthy, else the other unit')
        NOT(S, PP, f'{eq}_EffLead02', f'{eq}_EffLead01')
        S.bpoint(f'PlantControl/Monitor', f'{eq}_Lead', f'{eq}_EffLead01', f'{eq}01', f'{eq}02')
        OR(S, PP, f'{eq}_PoolAny', f'{eq}01Healthy', f'{eq}02Healthy', note=f'>= 1 healthy {eq}')
        AND(S, PP, f'{eq}_PoolBoth', f'{eq}01Healthy', f'{eq}02Healthy')
        OR(S, PP, f'{eq}_AnyProven', f'{eq}01RunProof', f'{eq}02RunProof')
        for n in UNITS:
            u = f'{eq}{n}'
            AND(S, f'{u}/Logic', f'{u}ProvenGood', f'{u}RunProof', note='inB: pump dP OK (instrumentation layer)')
            DLY(S, f'{u}/Logic', f'{u}ProvenStable', f'{u}ProvenGood', prof['handover_ok'], note='proven (and dP OK) for 10 s')
        for n, o in (('01', '02'), ('02', '01')):
            u, other = f'{eq}{n}', f'{eq}{o}'
            L = f'{u}/Logic'
            # make-before-break: keep running until the new unit (requested) is proven stable
            NOT(S, L, f'{u}OtherNotProven', f'{other}ProvenStable')
            AND(S, L, f'{u}HandoverHold', f'{u}RunProof', f'{other}Request', f'{u}OtherNotProven')
            OR(S, L, f'{u}LeadOrHandover', f'{eq}_EffLead{n}', f'{u}HandoverHold')
            AND(S, L, f'{u}NeedOne', 'Pool_Need1', f'{u}LeadOrHandover')
            OR(S, L, f'{u}Demand', need2, f'{u}NeedOne', note=f'{u} runs as lead, as 2nd unit, or during handover')
            S.rewire(f'{u}Request', 'inA', f'{u}Demand', f'CH{n}PostRun')
            # proof failure -> unit latch (standby takes over); CT also trips on isolation valve failure
            NOT(S, L, f'{u}NotRunProof', f'{u}RunProof')
            AND(S, L, f'{u}NoProofWhileCmd', f'{u}StartCmd', f'{u}NotRunProof')
            DLY(S, L, f'{u}ProofFailDelay', f'{u}NoProofWhileCmd', prof['pump_proof'], note='run proof timeout -> unit failed')
            if eq == 'CT':
                NOT(S, L, f'{u}NotValveProof', f'{u}ValveOpenProof')
                AND(S, L, f'{u}ValveNotOpen', f'{u}ValveOpenCmd', f'{u}NotValveProof')
                DLY(S, L, f'{u}ValveFailDelay', f'{u}ValveNotOpen', prof['valve_timeout'], note='isolation valve stroke timeout -> tower failed')
                OR(S, L, f'{u}FailTripLogic', f'{u}ProofFailDelay', f'{u}ValveFailDelay')
            else:
                OR(S, L, f'{u}FailTripLogic', f'{u}ProofFailDelay', note='inB: no-dP detection (instrumentation layer)')
            PULSE(S, L, f'{u}ResetFire', note=f'Px RESET {u} -> action fire')
            S.kc(L, f'{u}AutoResetArm', 'And', {'inB': f'{eq}_Not{o}Healthy', 'inC': 'CH_AutoRetryEnable', 'inD': T},
                 note='auto-retry ONLY when no other unit of the pool is healthy (never cycles a running standby)')
            DLY(S, L, f'{u}AutoResetDelay', f'{u}AutoResetArm', prof['pump_retry'])
            PULSE(S, L, f'{u}AutoResetPulse', f'{u}AutoResetDelay')
            OR(S, L, f'{u}ResetAny', f'{u}ResetFire', 'PlantAlarmResetFire', f'{u}AutoResetPulse')
            sealin(S, L, f'{u}FailLatch', f'{u}FailTripLogic', f'{u}ResetAny', note='seal-in: set by unit failure, reset by RESET/auto')
            S.link(S.comp[f'{u}AutoResetArm'], f'{u}FailLatch', 'inA')
            DLY(S, L, f'{u}RunStable30', f'{u}ProvenStable', 1800000)
            OR(S, L, f'{u}ManualReset', f'{u}ResetFire', 'PlantAlarmResetFire')
            OR(S, L, f'{u}RetryClear', f'{u}RunStable30', f'{u}ManualReset')
            S.kc(L, f'{u}RetryCounter', 'Counter', {'countUp': f'{u}AutoResetPulse', 'clearIn': f'{u}RetryClear'})
            CMP(S, L, f'{u}RetriesLeft', 'LessThan', f'{u}RetryCounter', 'CH_MaxAutoRetries')
            S.rewire(f'{u}AutoResetArm', 'inD', f'{u}RetriesLeft', T)
            NOT(S, L, f'{u}NoRetriesLeft', f'{u}RetriesLeft')
            AND(S, L, f'{u}HardFailLogic', f'{u}FailLatch', f'{u}NoRetriesLeft')
            S.bpoint('Alarms', f'{u}HardFailAlarm', f'{u}HardFailLogic', 'Manual reset', 'Normal')
            NOT(S, L, f'{u}NotFailLatched', f'{u}FailLatch')
            S.rewire(f'{u}Healthy', 'inC', f'{u}NotFailLatched', T)
            S.rewire(f'{u}Healthy', 'inD', f'{u}InAuto', T)
            S.bpoint('Alarms', f'{u}ProofFailAlarm', f'{u}FailLatch', 'Failed', 'Normal')
            NOT(S, 'Alarms', f'{u}NotInAutoLogic', f'{u}InAuto')
            S.bpoint('Alarms', f'{u}NotInAutoAlarm', f'{u}NotInAutoLogic', 'Not auto', 'Normal')
        NOT(S, 'Alarms', f'{eq}_NotBothLogic', f'{eq}_PoolBoth')
        AND(S, 'Alarms', f'{eq}_PoolDegradedLogic', 'PlantRunRequest', f'{eq}_PoolAny', f'{eq}_NotBothLogic')
        S.bpoint('Alarms', f'{eq}_PoolDegradedAlarm', f'{eq}_PoolDegradedLogic', 'Standby lost', 'Normal')
        NOT(S, 'Alarms', f'{eq}_NoneLogic', f'{eq}_PoolAny')
        AND(S, 'Alarms', f'{eq}_PoolUnavailableLogic', 'PlantRunRequest', f'{eq}_NoneLogic')
        S.bpoint('Alarms', f'{eq}_PoolUnavailableAlarm', f'{eq}_PoolUnavailableLogic', 'No unit', 'Normal')
    AND(S, PP, 'PoolSupportsStage2', 'CHP_PoolBoth', 'CDP_PoolBoth', note='2 chillers need 2 CHW + 2 CDW pumps (towers: alarm only)')
    # pool proof bridges: a pump / tower changeover must not drop a running chiller (standby proves within the bridge)
    OR(S, PP, 'CT_WaterPathProven', 'CT01ValveOpenProof', 'CT02ValveOpenProof', note='condenser water path through >= 1 tower cell')
    for n_, src in (('CHP_AnyProvenBridge', 'CHP_AnyProven'), ('CDP_AnyProvenBridge', 'CDP_AnyProven'), ('CT_WaterPathBridge', 'CT_WaterPathProven')):
        DLY(S, PP, n_, src, 0, prof['pool_bridge'], note='off-delay bridge for changeover')
    # flow path before pumps start (no dead-heading)
    for n in UNITS:   # condenser isolation valve per chiller (a headered condenser side needs one)
        S.bpoint(f'Chiller{n}/Points', f'CH{n}CdwValveOpenCmd', f'CH{n}PostRun', 'OPEN', 'CLOSE', kind='do')
        di(S, f'Chiller{n}/Points', f'CH{n}CdwValveOpenProof', False, 'Open', 'Closed', note='CDW isolation valve end switch')
    OR(S, PP, 'CHW_PathOpen', 'CH01ValveOpenProof', 'CH02ValveOpenProof')
    OR(S, PP, 'CDW_CondValveOpen', 'CH01CdwValveOpenProof', 'CH02CdwValveOpenProof')
    AND(S, PP, 'CDW_PathOpen', 'CDW_CondValveOpen', 'CT_WaterPathProven')
    for n in UNITS:
        AND(S, f'CHP{n}/Logic', f'CHP{n}StartPermit', f'CHP{n}Request', 'CHW_PathOpen', note='start after an evaporator valve is proven open')
        S.rewire(f'CHP{n}StartCmd', 'in16', f'CHP{n}StartPermit', f'CHP{n}Request')
        AND(S, f'CDP{n}/Logic', f'CDP{n}StartPermit', f'CDP{n}Request', 'CDW_PathOpen', note='start after condenser + tower valves are proven open')
        S.rewire(f'CDP{n}StartCmd', 'in16', f'CDP{n}StartPermit', f'CDP{n}Request')
        # tower isolation valves follow DEMAND (not fan health); all valves open if no healthy fan
        pass
    AND(S, PP, 'CT_ValvesFailSafe', 'Pool_Need1', 'CT_NoneLogic', note='no healthy tower fan: keep every tower valve open (water path)')
    for n in UNITS:
        OR(S, f'CT{n}/Logic', f'CT{n}ValveDemand', f'CT{n}Demand', 'CT_ValvesFailSafe')
        S.rewire(f'CT{n}ValveOpenCmd', 'in16', f'CT{n}ValveDemand', f'CT{n}Request')
    # lag chiller min-run hold only while the pools can carry two chillers
    for n, o in (('01', '02'), ('02', '01')):
        NOT(S, f'Chiller{n}/Request', f'CH{n}OtherNotRunning', f'CH{o}RunProofSelected')
        OR(S, f'Chiller{n}/Request', f'CH{n}MinRunPoolOk', 'PoolSupportsStage2', f'CH{n}OtherNotRunning')
        AND(S, f'Chiller{n}/Request', f'CH{n}MinRunHoldPool', f'CH{n}MinRunHold', f'CH{n}MinRunPoolOk')
        S.rewire(f'CH{n}DemandWithMinRun', 'inB', f'CH{n}MinRunHoldPool', f'CH{n}MinRunHold')
    # chiller side: pool availability replaces the dedicated train
    for n in UNITS:
        S.rewire(f'CH{n}AncillaryHealthy', 'inA', 'CHP_PoolAny', f'CHP{n}Healthy')
        S.rewire(f'CH{n}AncillaryHealthy', 'inB', 'CDP_PoolAny', f'CDP{n}Healthy')
        S.rewire(f'CH{n}AncillaryHealthy', 'inC', T, f'CT{n}Healthy')          # tower fans never block a chiller (alarm only)
        S.rewire(f'CH{n}WaterProofA', 'inA', 'CHP_AnyProvenBridge', f'CHP{n}RunProof')
        S.rewire(f'CH{n}WaterProofA', 'inB', 'CDP_AnyProvenBridge', f'CDP{n}RunProof')
        S.rewire(f'CH{n}WaterProofA', 'inC', 'CT_WaterPathBridge', f'CT{n}RunProof')
        for fl in ('CHW', 'CDW'):
            DLY(S, f'Chiller{n}/Permissive', f'CH{n}{fl}FlowBridge', f'CH{n}{fl}FlowProof', 0, prof['flow_bridge'], note='rides through a pump changeover')
        S.rewire(f'CH{n}WaterProofB', 'inA', f'CH{n}CHWFlowBridge', f'CH{n}CHWFlowProof')
        S.rewire(f'CH{n}WaterProofB', 'inB', f'CH{n}CDWFlowBridge', f'CH{n}CDWFlowProof')
        # condenser isolation valve per chiller (headered condenser side needs one)
        S.rewire(f'CH{n}WaterProofB', 'inC', f'CH{n}CdwValveOpenProof', T)
        di(S, f'Chiller{n}/Points', f'CH{n}InAuto', True, 'Remote', 'Local', note='Chiller local/remote (BACnet)')
        S.rewire(f'CH{n}Healthy', 'inC', f'CH{n}InAuto', T)
        NOT(S, 'Alarms', f'CH{n}NotInAutoLogic', f'CH{n}InAuto')
        S.bpoint('Alarms', f'CH{n}NotInAutoAlarm', f'CH{n}NotInAutoLogic', 'Local', 'Normal')
    S.param('CHP_PostRunSpeed', 30.0, 'pct', note='CHW pump speed during post-run / plant disabled (V6 gave 0 % while the pump was still commanded)')
    S.rewire('CHWDP_SafeSelect', 'inFalse', 'CHP_PostRunSpeed', 'ZeroSpeed')
    S.rewire('Stage2Allowed', 'inC', 'PoolSupportsStage2', T)
    S.kc('Alarms', 'NotPoolSupportsStage2', 'Not', {'in': 'PoolSupportsStage2'})
    AND(S, 'Alarms', 'Stage2BlockedLogic', 'Stage2Selected', 'NotPoolSupportsStage2')
    DLY(S, 'Alarms', 'Stage2BlockedDelay', 'Stage2BlockedLogic', 60000)
    S.bpoint('Alarms', 'Stage2BlockedByPoolAlarm', 'Stage2BlockedDelay', 'Blocked', 'Normal')
    # simulation: flow through a chiller = its valve open AND any pump of the pool running
    SF = 'Simulation/Feedback'
    OR(S, SF, 'Sim_AnyCHP_RunFb', 'Sim_CHP01_RunFb', 'Sim_CHP02_RunFb')
    OR(S, SF, 'Sim_AnyCDP_RunFb', 'Sim_CDP01_RunFb', 'Sim_CDP02_RunFb')
    for n in UNITS:
        DLY(S, SF, f'Sim_CH{n}_CdwValveFb', f'CH{n}CdwValveOpenCmd', prof['sim_valve'], prof['sim_valve'])
        simlink(S, f'CH{n}CdwValveOpenProof', f'Sim_CH{n}_CdwValveFb', 'emulated end switch')
        S.rewire(f'Sim_CH{n}_ChwFlowFb', 'inB', 'Sim_AnyCHP_RunFb', f'Sim_CHP{n}_RunFb')
        S.rewire(f'Sim_CH{n}_CdwFlowFb', 'inA', f'Sim_CH{n}_CdwValveFb', f'Sim_CH{n}_ValveFb')
        S.rewire(f'Sim_CH{n}_CdwFlowFb', 'inB', 'Sim_AnyCDP_RunFb', f'Sim_CDP{n}_RunFb')
        DLY(S, SF, f'Sim_CT{n}_ValveFb', f'CT{n}ValveOpenCmd', prof['sim_valve'], prof['sim_valve'])
        simlink(S, f'CT{n}ValveOpenProof', f'Sim_CT{n}_ValveFb', 'emulated end switch')
    for pt, v in {**{f'{e}{n}ProofFailAlarm': (True, 'Critical', f'{e}{n} failed to prove - standby unit started, press RESET after repair') for e in POOLS for n in UNITS},
                  **{f'{e}{n}NotInAutoAlarm': (True, 'Warning', f'{e}{n} HOA not in AUTO - skipped by pool') for e in POOLS for n in UNITS},
                  **{f'CH{n}NotInAutoAlarm': (True, 'Warning', f'Chiller {n} in LOCAL - skipped by staging') for n in UNITS},
                  **{f'{e}_PoolDegradedAlarm': (True, 'Warning', f'{e} pool: only one healthy unit (no standby)') for e in POOLS},
                  **{f'{e}_PoolUnavailableAlarm': (True, 'Emergency', f'{e} pool: no healthy unit' + (' - heat rejection lost, valves held open' if e == 'CT' else ' - plant cannot run')) for e in POOLS},
                  **{f'{e}{n}HardFailAlarm': (True, 'Critical', f'{e}{n} auto-retries used - repair and press RESET') for e in POOLS for n in UNITS},
                  'Stage2BlockedByPoolAlarm': (True, 'Warning', 'Stage 2 requested but pump pool cannot support 2 chillers'),
                  **{f'{e}{n}VfdFault': (True, 'Critical', f'{e}{n} VFD fault') for e in POOLS for n in UNITS},
                  **{f'CT{n}VibrationAlarm': (True, 'Critical', f'CT{n} fan vibration trip') for n in UNITS}}.items():
        M6.COS[pt] = v
    for n in UNITS:
        M6.CMD_FAIL[f'CH{n}CdwValveOpenCmd'] = (f'CH{n}CdwValveOpenProof', 'Warning', 60000)
        M6.CMD_FAIL[f'CT{n}ValveOpenCmd'] = (f'CT{n}ValveOpenProof', 'Warning', 150000)


# ============================================================ 2. instrumentation (transmitters, meters, diagnostics)
def instrumentation(S, prof):
    SI = 'Simulation/Instruments'
    const(S, 'Pct_to_Frac', 0.01, prec=2)
    const(S, 'Amps_per_kW', 1.604, prec=3, note='3-phase 400 V, PF 0.9: A = kW x 1000 / (1.732 x 400 x 0.9)')
    const(S, 'HzPerPct', 0.5, prec=2, note='50 Hz at 100 % speed')
    const(S, 'MinusOne', -1.0)
    S.param('Pump_MinDP', 10.0, 'kPa', note='Pump running with dP below this for 60 s = no flow (coupling/air lock) -> failover (below min-speed head)')
    S.bparam('Pump_DpFailoverEnable', True, t='Enabled', f='Disabled', note='Use pump dP transmitters to fail over a running pump')
    S.param('Pump_MinSuction', 30.0, 'kPa', note='Low suction pressure alarm (cavitation / system pressure)')
    S.param('Press_MinValid', 0.0, 'kPa'); S.param('Press_MaxValid', 1000.0, 'kPa')
    S.param('CH_EvapApproachMax', 3.0, 'none', note='Evaporator approach alarm (K) - fouling / low refrigerant (OEM)')
    S.param('CH_CondApproachMax', 4.0, 'none', note='Condenser approach alarm (K) - tube fouling -> brush / water treatment (OEM)')
    S.param('CT_LevelLowPct', 30.0, 'pct', note='Basin level low alarm'); S.param('CT_LevelHighPct', 95.0, 'pct', note='Basin level high (make-up valve)')
    S.param('CT_ConductivityMax', 2500.0, 'none', prec=0, note='uS/cm - bleed-off / water treatment alarm')
    S.param('BTU_MaxValidRT', 3000.0, 'tR'); S.param('Meter_DeviationPct', 15.0, 'pct', note='Meter vs calculation cross-check')
    S.bparam('LoadSource_BTU', True, t='BTU meter', f='Flow x dT', note='Cooling load from BTU meter when valid, else calculated (fail-safe)')
    const(S, 'MakeupPerRT', 0.009, prec=4, note='SIM: evaporation + blow-down m3/h per RT (~3 USgpm/100 RT)')
    const(S, 'CDP_DesignFlow', 180.0, 'm3h', note='SIM: condenser pump design flow')
    for n_, v_ in (('CHP_StaticSuction', 180.0), ('CDP_StaticSuction', 60.0), ('CHP_DesignHead', 280.0), ('CDP_DesignHead', 220.0)):
        const(S, n_, v_, 'kPa', note='SIM: pump pressures')
    const(S, 'Sim_EvapSatOffset', -1.2); const(S, 'Sim_CondSatOffset', 1.5); const(S, 'Sim_EvapDPk', 0.0006, prec=5); const(S, 'Sim_CondDPk', 0.0005, prec=5)
    const(S, 'BypassFlowPerPct', 1.5, 'm3h'); const(S, 'KpiMinRT', 5.0, 'tR'); const(S, 'MeterFixed_kW', 3.0, 'kW')
    const(S, 'MeterFactor', 1.02, prec=3)
    ramp(S, 'Sim_GridVolts', 'SineWave', 600000, 4.0, 400.0, 'V')
    ramp(S, 'Sim_PowerFactor', 'SineWave', 900000, 0.02, 0.91)
    ramp(S, 'Sim_GridHz', 'SineWave', 420000, 0.05, 50.0, 'Hz')
    ramp(S, 'Sim_ExpTankP', 'SineWave', 1500000, 4.0, 200.0, 'kPa')
    # ---- per chiller
    for n in UNITS:
        c, Pt, Mo = f'CH{n}', f'Chiller{n}/Points', f'Chiller{n}/Monitor'
        for nm, v, u, note in (('ChwSupplyTemp', 7.0, 'C', 'TT evaporator leaving'), ('ChwReturnTemp', 12.0, 'C', 'TT evaporator entering'),
                               ('CdwEnteringTemp', 30.0, 'C', 'TT condenser entering (from towers)'), ('CdwLeavingTemp', 35.0, 'C', 'TT condenser leaving'),
                               ('ChwFlow', 0.0, 'm3h', 'FM evaporator flow (electromagnetic)'), ('CdwFlow', 0.0, 'm3h', 'FM condenser flow'),
                               ('EvapSatTemp', 6.0, 'C', 'Chiller BACnet: evaporator saturated refrigerant temp'),
                               ('CondSatTemp', 36.0, 'C', 'Chiller BACnet: condenser saturated refrigerant temp')):
            ai(S, Pt, f'{c}_{nm}', v, u, note=note)
        for nm, v, u, note in (('EvapDP', 0.0, 'kPa', 'DPT evaporator water pressure drop'), ('CondDP', 0.0, 'kPa', 'DPT condenser water pressure drop'),
                               ('Amps', 0.0, 'A', 'CT (current transformer) / power meter'), ('Volts', 400.0, 'V', 'Power meter'),
                               ('PF', 0.9, 'none', 'Power meter power factor')):
            ai(S, Pt, f'{c}_{nm}', v, u, prec=2 if nm == 'PF' else 1, note=note, hist='5min')
        MATH(S, Mo, f'{c}DeltaTCalc', 'Subtract', f'{c}_ChwReturnTemp', f'{c}_ChwSupplyTemp')
        S.npoint(Mo, f'{c}_DeltaT', f'{c}DeltaTCalc', 'none', 2)
        MATH(S, Mo, f'{c}LoadKWCalc', 'Multiply', f'{c}_ChwFlow', f'{c}DeltaTCalc', 'Water_kW_Factor')
        LIMIT(S, Mo, f'{c}LoadKWPos', f'{c}LoadKWCalc', 0, 100000)
        MATH(S, Mo, f'{c}RTCalc', 'Divide', f'{c}LoadKWPos', 'kW_per_RT')
        S.npoint(Mo, f'{c}_RT', f'{c}RTCalc', 'tR', 1)
        MATH(S, Mo, f'{c}RTGuard', 'Maximum', f'{c}RTCalc', 'KpiMinRT')
        MATH(S, Mo, f'{c}KwPerRTCalc', 'Divide', f'{c}_kW', f'{c}RTGuard')
        S.npoint(Mo, f'{c}_kW_per_RT', f'{c}KwPerRTCalc', 'none', 3)
        MATH(S, Mo, f'{c}EvapApproachCalc', 'Subtract', f'{c}_ChwSupplyTemp', f'{c}_EvapSatTemp')
        S.npoint(Mo, f'{c}_EvapApproach', f'{c}EvapApproachCalc', 'none', 2)
        MATH(S, Mo, f'{c}CondApproachCalc', 'Subtract', f'{c}_CondSatTemp', f'{c}_CdwLeavingTemp')
        S.npoint(Mo, f'{c}_CondApproach', f'{c}CondApproachCalc', 'none', 2)
        MATH(S, Mo, f'{c}LiftCalc', 'Subtract', f'{c}_CondSatTemp', f'{c}_EvapSatTemp')
        S.npoint(Mo, f'{c}_Lift', f'{c}LiftCalc', 'none', 1)
        DLY(S, Mo, f'{c}Running15min', f'{c}RunProofSelected', 900000)
        CMP(S, 'Alarms', f'{c}EvapApproachHigh', 'GreaterThan', f'{c}EvapApproachCalc', 'CH_EvapApproachMax')
        AND(S, 'Alarms', f'{c}EvapApproachLogic', f'{c}EvapApproachHigh', f'{c}Running15min')
        DLY(S, 'Alarms', f'{c}EvapApproachDelay', f'{c}EvapApproachLogic', 1800000)
        S.bpoint('Alarms', f'{c}EvapApproachAlarm', f'{c}EvapApproachDelay', 'High', 'Normal')
        CMP(S, 'Alarms', f'{c}CondApproachHigh', 'GreaterThan', f'{c}CondApproachCalc', 'CH_CondApproachMax')
        AND(S, 'Alarms', f'{c}CondApproachLogic', f'{c}CondApproachHigh', f'{c}Running15min')
        DLY(S, 'Alarms', f'{c}CondApproachDelay', f'{c}CondApproachLogic', 1800000)
        S.bpoint('Alarms', f'{c}CondApproachAlarm', f'{c}CondApproachDelay', 'High', 'Normal')
        CMP(S, 'Alarms', f'{c}FlowBelowMin', 'LessThan', f'{c}_ChwFlow', f'{c}_MinFlow')
        AND(S, 'Alarms', f'{c}LowFlowLogic', f'{c}FlowBelowMin', f'{c}RunProofSelected')
        DLY(S, 'Alarms', f'{c}LowFlowDelay', f'{c}LowFlowLogic', 60000)
        S.bpoint('Alarms', f'{c}EvapLowFlowAlarm', f'{c}LowFlowDelay', 'Low flow', 'Normal')
        # energy meter register
        # (CH0x_kW already carries the Energy totalizer from V6 -> CH0x_kWh)
        # ---- emulation
        SW(S, SI, f'Sim_{c}_ChwOn', f'Sim_{c}_ChwFlowFb', 'One', 'ZeroSpeed')
        SW(S, SI, f'Sim_{c}_CdwOn', f'Sim_{c}_CdwFlowFb', 'One', 'ZeroSpeed')
        SW(S, SI, f'Sim_{c}_ChwSupply', f'{c}RunProofSelected', 'CHWS', 'CHWR'); simlink(S, f'{c}_ChwSupplyTemp', f'Sim_{c}_ChwSupply')
        simlink(S, f'{c}_ChwReturnTemp', 'CHWR', 'plant CHWR (common return)')
        simlink(S, f'{c}_CdwEnteringTemp', 'CDS', 'plant CDS (common tower supply)')
        SW(S, SI, f'Sim_{c}_CdwLeaving', f'{c}RunProofSelected', 'CDR', 'CDS'); simlink(S, f'{c}_CdwLeavingTemp', f'Sim_{c}_CdwLeaving')
        MATH(S, SI, f'Sim_{c}_EvapSatRun', 'Add', 'CHWS', 'Sim_EvapSatOffset')
        SW(S, SI, f'Sim_{c}_EvapSat', f'{c}RunProofSelected', f'Sim_{c}_EvapSatRun', 'CHWR'); simlink(S, f'{c}_EvapSatTemp', f'Sim_{c}_EvapSat')
        MATH(S, SI, f'Sim_{c}_CondSatRun', 'Add', 'CDR', 'Sim_CondSatOffset')
        SW(S, SI, f'Sim_{c}_CondSat', f'{c}RunProofSelected', f'Sim_{c}_CondSatRun', 'CDS'); simlink(S, f'{c}_CondSatTemp', f'Sim_{c}_CondSat')
        MATH(S, SI, f'Sim_{c}_Amps', 'Multiply', f'{c}_kW', 'Amps_per_kW'); simlink(S, f'{c}_Amps', f'Sim_{c}_Amps')
        simlink(S, f'{c}_Volts', 'Sim_GridVolts'); simlink(S, f'{c}_PF', 'Sim_PowerFactor')
    MATH(S, SI, 'Sim_ChwOnCount', 'Add', 'Sim_CH01_ChwOn', 'Sim_CH02_ChwOn')
    MATH(S, SI, 'Sim_ChwOnGuard', 'Maximum', 'Sim_ChwOnCount', 'One')
    MATH(S, SI, 'Sim_ChwFlowShare', 'Divide', 'CHWFlow', 'Sim_ChwOnGuard')
    for eq in ('CHP', 'CDP'):
        for n in UNITS:
            SW(S, SI, f'Sim_{eq}{n}_On', f'Sim_{eq}{n}_RunFb', 'One', 'ZeroSpeed')
    MATH(S, SI, 'Sim_CdpOnCount', 'Add', 'Sim_CDP01_On', 'Sim_CDP02_On')
    MATH(S, SI, 'Sim_CdwPlantFlow', 'Multiply', 'Sim_CdpOnCount', 'CDP_DesignFlow')
    MATH(S, SI, 'Sim_CdwOnCount', 'Add', 'Sim_CH01_CdwOn', 'Sim_CH02_CdwOn')
    MATH(S, SI, 'Sim_CdwOnGuard', 'Maximum', 'Sim_CdwOnCount', 'One')
    MATH(S, SI, 'Sim_CdwFlowShare', 'Divide', 'Sim_CdwPlantFlow', 'Sim_CdwOnGuard')
    for n in UNITS:
        c = f'CH{n}'
        MATH(S, SI, f'Sim_{c}_ChwFlow', 'Multiply', 'Sim_ChwFlowShare', f'Sim_{c}_ChwOn'); simlink(S, f'{c}_ChwFlow', f'Sim_{c}_ChwFlow')
        MATH(S, SI, f'Sim_{c}_CdwFlow', 'Multiply', 'Sim_CdwFlowShare', f'Sim_{c}_CdwOn'); simlink(S, f'{c}_CdwFlow', f'Sim_{c}_CdwFlow')
        MATH(S, SI, f'Sim_{c}_EvapDP', 'Multiply', f'Sim_{c}_ChwFlow', f'Sim_{c}_ChwFlow', 'Sim_EvapDPk'); simlink(S, f'{c}_EvapDP', f'Sim_{c}_EvapDP')
        MATH(S, SI, f'Sim_{c}_CondDP', 'Multiply', f'Sim_{c}_CdwFlow', f'Sim_{c}_CdwFlow', 'Sim_CondDPk'); simlink(S, f'{c}_CondDP', f'Sim_{c}_CondDP')
    # ---- per pump (CHP / CDP)
    for eq in ('CHP', 'CDP'):
        for n in UNITS:
            u, Pt, L = f'{eq}{n}', f'{eq}{n}/Points', f'{eq}{n}/Logic'
            ai(S, Pt, f'{u}_SpeedFeedbackHz', 0.0, 'Hz', note='VFD output frequency (BACnet/Modbus)', hist='5min')
            ai(S, Pt, f'{u}_Amps', 0.0, 'A', note='VFD motor current / CT', hist='5min')
            ai(S, Pt, f'{u}_SuctionPressure', 150.0, 'kPa', note='PT pump suction', hist='5min')
            ai(S, Pt, f'{u}_DischargePressure', 150.0, 'kPa', note='PT pump discharge', hist='5min')
            MATH(S, L, f'{u}DPCalc', 'Subtract', f'{u}_DischargePressure', f'{u}_SuctionPressure')
            S.npoint(f'{u}/Monitor', f'{u}_DiffPressure', f'{u}DPCalc', 'kPa', 1)
            for s_ in ('Suction', 'Discharge'):
                CMP(S, L, f'{u}{s_}AboveMin', 'GreaterThanEqual', f'{u}_{s_}Pressure', 'Press_MinValid')
                CMP(S, L, f'{u}{s_}BelowMax', 'LessThanEqual', f'{u}_{s_}Pressure', 'Press_MaxValid')
            AND(S, L, f'{u}PressValid', f'{u}SuctionAboveMin', f'{u}SuctionBelowMax', f'{u}DischargeAboveMin', f'{u}DischargeBelowMax')
            CMP(S, L, f'{u}DPLow', 'LessThan', f'{u}DPCalc', 'Pump_MinDP')
            AND(S, L, f'{u}NoDPLogic', f'{u}RunProof', f'{u}DPLow', f'{u}PressValid', 'Pump_DpFailoverEnable')
            DLY(S, L, f'{u}NoDPDelay', f'{u}NoDPLogic', 20000, note='running without differential pressure 20 s -> unit failed (standby starts)')
            NOT(S, L, f'{u}DPNotLow', f'{u}DPLow'); NOT(S, L, f'{u}PressInvalid', f'{u}PressValid')
            OR(S, L, f'{u}DPOk', f'{u}DPNotLow', f'{u}PressInvalid')
            S.rewire(f'{u}ProvenGood', 'inB', f'{u}DPOk', T)
            S.rewire(f'{u}FailTripLogic', 'inB', f'{u}NoDPDelay', F)
            S.bpoint('Alarms', f'{u}NoDeltaPAlarm', f'{u}NoDPDelay', 'No dP', 'Normal')
            CMP(S, 'Alarms', f'{u}SuctionLow', 'LessThan', f'{u}_SuctionPressure', 'Pump_MinSuction')
            AND(S, 'Alarms', f'{u}SuctionLowLogic', f'{u}SuctionLow', f'{u}RunProof', f'{u}PressValid')
            DLY(S, 'Alarms', f'{u}SuctionLowDelay', f'{u}SuctionLowLogic', 60000)
            S.bpoint('Alarms', f'{u}LowSuctionAlarm', f'{u}SuctionLowDelay', 'Low', 'Normal')
            add_ext(S, f'{u}_kW', 'Energy', 'c:NumericTotalizerExt', [('totalizationInterval', None, 'hourly')])
            S.npoint(f'{u}/Monitor', f'{u}_kWh', f'{u}_kW:Energy.total', 'kWh', 1)
            # emulation
            MATH(S, SI, f'Sim_{u}_HzRun', 'Multiply', f'{u}SpeedCmd', 'HzPerPct')
            SW(S, SI, f'Sim_{u}_Hz', f'Sim_{u}_RunFb', f'Sim_{u}_HzRun', 'ZeroSpeed'); simlink(S, f'{u}_SpeedFeedbackHz', f'Sim_{u}_Hz')
            MATH(S, SI, f'Sim_{u}_Amps', 'Multiply', f'{u}_kW', 'Amps_per_kW'); simlink(S, f'{u}_Amps', f'Sim_{u}_Amps')
            if eq == 'CHP':
                MATH(S, SI, f'Sim_{u}_Suction', 'Add', 'Sim_ExpTankP', 'ZeroSpeed')
            else:
                MATH(S, SI, f'Sim_{u}_Suction', 'Add', 'CDP_StaticSuction', 'ZeroSpeed')
            simlink(S, f'{u}_SuctionPressure', f'Sim_{u}_Suction')
            MATH(S, SI, f'Sim_{u}_Head', 'Multiply', f'Sim_{u}_SpeedFrac', f'Sim_{u}_SpeedFrac', f'{eq}_DesignHead', f'Sim_{u}_On')
            MATH(S, SI, f'Sim_{u}_Discharge', 'Add', f'Sim_{u}_Suction', f'Sim_{u}_Head'); simlink(S, f'{u}_DischargePressure', f'Sim_{u}_Discharge')
    # ---- per cooling tower
    for n in UNITS:
        u, Pt, L = f'CT{n}', f'CT{n}/Points', f'CT{n}/Logic'
        ai(S, Pt, f'{u}_FanSpeedHz', 0.0, 'Hz', note='VFD output frequency', hist='5min')
        ai(S, Pt, f'{u}_Amps', 0.0, 'A', note='VFD motor current / CT', hist='5min')
        ai(S, Pt, f'{u}_BasinTemp', 30.0, 'C', note='TT basin water')
        ai(S, Pt, f'{u}_OutletTemp', 30.0, 'C', note='TT cell leaving water')
        ai(S, Pt, f'{u}_BasinLevel', 75.0, 'pct', note='LT basin level (ultrasonic / hydrostatic)', hist='5min')
        di(S, Pt, f'{u}_LowLevelSwitch', False, 'Low', 'Normal', note='LS basin low level')
        di(S, Pt, f'{u}_HighLevelSwitch', False, 'High', 'Normal', note='LS basin high level / overflow')
        CMP(S, 'Alarms', f'{u}LevelBelowLow', 'LessThan', f'{u}_BasinLevel', 'CT_LevelLowPct')
        OR(S, 'Alarms', f'{u}LevelLowLogic', f'{u}LevelBelowLow', f'{u}_LowLevelSwitch')
        DLY(S, 'Alarms', f'{u}LevelLowDelay', f'{u}LevelLowLogic', 60000)
        S.bpoint('Alarms', f'{u}BasinLowLevelAlarm', f'{u}LevelLowDelay', 'Low', 'Normal')
        CMP(S, 'Alarms', f'{u}LevelAboveHigh', 'GreaterThan', f'{u}_BasinLevel', 'CT_LevelHighPct')
        OR(S, 'Alarms', f'{u}LevelHighLogic', f'{u}LevelAboveHigh', f'{u}_HighLevelSwitch')
        DLY(S, 'Alarms', f'{u}LevelHighDelay', f'{u}LevelHighLogic', 300000)
        S.bpoint('Alarms', f'{u}BasinHighLevelAlarm', f'{u}LevelHighDelay', 'High', 'Normal')
        add_ext(S, f'{u}_kW', 'Energy', 'c:NumericTotalizerExt', [('totalizationInterval', None, 'hourly')])
        S.npoint(f'{u}/Monitor', f'{u}_kWh', f'{u}_kW:Energy.total', 'kWh', 1)
        MATH(S, SI, f'Sim_{u}_HzRun', 'Multiply', f'{u}SpeedCmd', 'HzPerPct')
        SW(S, SI, f'Sim_{u}_Hz', f'Sim_{u}_RunFb', f'Sim_{u}_HzRun', 'ZeroSpeed'); simlink(S, f'{u}_FanSpeedHz', f'Sim_{u}_Hz')
        MATH(S, SI, f'Sim_{u}_Amps', 'Multiply', f'{u}_kW', 'Amps_per_kW'); simlink(S, f'{u}_Amps', f'Sim_{u}_Amps')
        simlink(S, f'{u}_BasinTemp', 'CDS', 'basin = tower leaving (CDS)')
        SW(S, SI, f'Sim_{u}_Outlet', f'Sim_{u}_ValveFb', 'CDS', 'CDR'); simlink(S, f'{u}_OutletTemp', f'Sim_{u}_Outlet')
        ramp(S, f'Sim_{u}_Level', 'SineWave', 1300000 + int(n) * 170000, 9.0, 74.0, 'pct', target=f'{u}_BasinLevel')
    ai(S, 'CdwLoop/Points', 'CT_MakeupFlow', 0.0, 'm3h', note='FM tower make-up water (pulse meter)')
    add_ext(S, 'CT_MakeupFlow', 'Volume', 'c:NumericTotalizerExt', [('totalizationInterval', None, 'hourly')])
    S.npoint('CdwLoop/Monitor', 'CT_MakeupVolume', 'CT_MakeupFlow:Volume.total', 'm3', 1)
    ai(S, 'CdwLoop/Points', 'CT_Conductivity', 1200.0, 'none', prec=0, note='Water treatment conductivity uS/cm', hist='5min')
    CMP(S, 'Alarms', 'CT_ConductivityHigh', 'GreaterThan', 'CT_Conductivity', 'CT_ConductivityMax')
    DLY(S, 'Alarms', 'CT_ConductivityDelay', 'CT_ConductivityHigh', 600000)
    S.bpoint('Alarms', 'CT_ConductivityHighAlarm', 'CT_ConductivityDelay', 'High', 'Normal')
    MATH(S, SI, 'Sim_CT_Makeup', 'Multiply', 'CoolingLoad_RT', 'MakeupPerRT'); simlink(S, 'CT_MakeupFlow', 'Sim_CT_Makeup')
    ramp(S, 'Sim_CT_Conductivity', 'Ramp', 7200000, 500.0, 1500.0, 'none', target='CT_Conductivity')
    # ---- plant headers
    ai(S, 'ChwLoop/Points', 'CHW_SupplyHeaderPressure', 320.0, 'kPa', note='PT CHW supply header', hist='5min')
    ai(S, 'ChwLoop/Points', 'CHW_ReturnHeaderPressure', 200.0, 'kPa', note='PT CHW return header', hist='5min')
    ai(S, 'ChwLoop/Points', 'CHW_ExpansionTankPressure', 200.0, 'kPa', note='PT expansion tank / make-up', hist='5min')
    ai(S, 'ChwLoop/Points', 'CHW_BypassFlow', 0.0, 'm3h', note='FM decoupler / bypass flow')
    ai(S, 'CdwLoop/Points', 'CDW_Flow', 0.0, 'm3h', note='FM condenser water header flow')
    ai(S, 'CdwLoop/Points', 'CDW_SupplyHeaderPressure', 250.0, 'kPa', note='PT condenser supply header', hist='5min')
    simlink(S, 'CHW_ReturnHeaderPressure', 'Sim_ExpTankP'); simlink(S, 'CHW_ExpansionTankPressure', 'Sim_ExpTankP')
    MATH(S, SI, 'Sim_ChwSupplyP', 'Add', 'Sim_ExpTankP', 'CHWDP'); simlink(S, 'CHW_SupplyHeaderPressure', 'Sim_ChwSupplyP')
    MATH(S, SI, 'Sim_BypassFlow', 'Multiply', 'CHW_BypassValveFeedback', 'BypassFlowPerPct'); simlink(S, 'CHW_BypassFlow', 'Sim_BypassFlow')
    simlink(S, 'CDW_Flow', 'Sim_CdwPlantFlow')
    MATH(S, SI, 'Sim_CdwHeadMax', 'Maximum', 'Sim_CDP01_Discharge', 'Sim_CDP02_Discharge'); simlink(S, 'CDW_SupplyHeaderPressure', 'Sim_CdwHeadMax')
    S.param('CH_CdwMinFlow', 80.0, 'm3h', note='OEM condenser minimum flow per chiller PROJECT/OEM')
    for n in UNITS:
        SW(S, 'Alarms', f'Cdw_CH{n}MinFlow', f'CH{n}CdwValveOpenCmd', 'CH_CdwMinFlow', 'ZeroSpeed')
    MATH(S, 'Alarms', 'Cdw_MinFlowSum', 'Add', 'Cdw_CH01MinFlow', 'Cdw_CH02MinFlow')
    CMP(S, 'Alarms', 'CdwFlowLow', 'LessThan', 'CDW_Flow', 'Cdw_MinFlowSum')
    AND(S, 'Alarms', 'CdwFlowLowLogic', 'CdwFlowLow', 'AnyChillerProven', 'CDP_AnyProven')
    DLY(S, 'Alarms', 'CdwFlowLowDelay', 'CdwFlowLowLogic', 120000)
    S.bpoint('Alarms', 'CDW_FlowLowAlarm', 'CdwFlowLowDelay', 'Low', 'Normal')
    # ---- BTU meter (primary load source, fail-safe to flow x dT)
    B = 'Metering/BTU'
    ai(S, B, 'BTU_Flow', 0.0, 'm3h', note='BTU meter volume flow')
    ai(S, B, 'BTU_SupplyTemp', 7.0, 'C', prec=2, note='BTU meter supply sensor'); ai(S, B, 'BTU_ReturnTemp', 12.0, 'C', prec=2, note='BTU meter return sensor')
    ai(S, B, 'BTU_Power_RT', 0.0, 'tR', note='BTU meter thermal power')
    ai(S, B, 'BTU_EnergyTotal', 0.0, 'RTh', note='BTU meter energy register (RTh)')
    di(S, B, 'BTU_CommOk', True, 'OK', 'Comm fail', note='BTU meter communication status')
    MATH(S, B, 'BTU_DeltaTCalc', 'Subtract', 'BTU_ReturnTemp', 'BTU_SupplyTemp')
    S.npoint(B, 'BTU_DeltaT', 'BTU_DeltaTCalc', 'none', 2)
    CMP(S, B, 'BTU_PowerAboveMin', 'GreaterThanEqual', 'BTU_Power_RT', 'ZeroSpeed')
    CMP(S, B, 'BTU_PowerBelowMax', 'LessThanEqual', 'BTU_Power_RT', 'BTU_MaxValidRT')
    AND(S, B, 'BTU_ValidLogic', 'BTU_CommOk', 'BTU_PowerAboveMin', 'BTU_PowerBelowMax')
    S.bpoint(B, 'BTU_Valid', 'BTU_ValidLogic', 'Valid', 'Invalid')
    AND(S, B, 'BTU_UseForLoad', 'LoadSource_BTU', 'BTU_ValidLogic')
    MATH(S, B, 'BTU_kWCalc', 'Multiply', 'BTU_Power_RT', 'kW_per_RT')
    SW(S, 'Energy', 'CoolingLoadSelect', 'BTU_UseForLoad', 'BTU_kWCalc', 'CoolingLoadRaw', note='BTU meter when valid, else flow x dT')
    S.rewire('CoolingLoadKW', 'inA', 'CoolingLoadSelect', 'CoolingLoadRaw')
    S.bpoint('Energy', 'CoolingLoadSource', 'BTU_UseForLoad', 'BTU meter', 'Calculated')
    MATH(S, 'Energy', 'CoolingLoadCalcRT', 'Divide', 'CoolingLoadRaw', 'kW_per_RT')
    MATH(S, 'Alarms', 'BtuVsCalcDiff', 'Subtract', 'BTU_Power_RT', 'CoolingLoadCalcRT')
    S.kc('Alarms', 'BtuVsCalcAbs', 'AbsValue', {'inA': 'BtuVsCalcDiff'})
    MATH(S, 'Alarms', 'BtuCalcGuard', 'Maximum', 'CoolingLoadCalcRT', 'KpiMinRT')
    MATH(S, 'Alarms', 'BtuDevLimit', 'Multiply', 'BtuCalcGuard', 'Meter_DeviationPct', 'Pct_to_Frac')
    CMP(S, 'Alarms', 'BtuDevHigh', 'GreaterThan', 'BtuVsCalcAbs', 'BtuDevLimit')
    AND(S, 'Alarms', 'BtuDevLogic', 'BtuDevHigh', 'BTU_ValidLogic', 'PlantRunning30min')
    DLY(S, 'Alarms', 'BtuDevDelay', 'BtuDevLogic', 1800000)
    S.bpoint('Alarms', 'BTU_DeviationAlarm', 'BtuDevDelay', 'Deviation', 'Normal')
    DLY(S, B, 'BtuDevFallback', 'BtuDevLogic', 300000, 600000, note='5 min deviation -> use calculated load (zero / stuck meter)')
    NOT(S, B, 'BtuNoDeviation', 'BtuDevFallback')
    S.rewire('BTU_UseForLoad', 'inC', 'BtuNoDeviation', T)
    NOT(S, 'Alarms', 'BTU_InvalidLogic', 'BTU_ValidLogic')
    S.bpoint('Alarms', 'BTU_InvalidAlarm', 'BTU_InvalidLogic', 'Invalid', 'Normal')
    simlink(S, 'BTU_Flow', 'CHWFlow'); simlink(S, 'BTU_SupplyTemp', 'CHWS'); simlink(S, 'BTU_ReturnTemp', 'CHWR')
    LIMIT(S, SI, 'Sim_BTU_RTCalc', 'CoolingLoadCalcRT', 0, 100000)
    S.npoint(SI, 'Sim_BTU_Meter', 'Sim_BTU_RTCalc', 'tR', 1, kind='sim'); M6.NO_HISTORY.add('Sim_BTU_Meter')
    add_ext(S, 'Sim_BTU_Meter', 'Energy', 'c:NumericTotalizerExt', [('totalizationInterval', None, 'hourly')])
    simlink(S, 'BTU_Power_RT', 'Sim_BTU_Meter'); simlink(S, 'BTU_EnergyTotal', 'Sim_BTU_Meter:Energy.total')
    # ---- plant main power meter
    Pm = 'Metering/Power'
    for nm, v, u, h in (('kW', 0.0, 'kW', '1min'), ('kWh', 0.0, 'kWh', '1min'), ('Volts', 400.0, 'V', '5min'), ('Amps', 0.0, 'A', '5min'),
                        ('PF', 0.9, 'none', '5min'), ('Hz', 50.0, 'Hz', '5min')):
        ai(S, Pm, f'PM_Main_{nm}', v, u, prec=2 if nm in ('PF', 'Hz') else 1, note=f'Main plant power meter {nm} (Modbus)', hist=h)
    di(S, Pm, 'PM_Main_CommOk', True, 'OK', 'Comm fail', note='Power meter communication')
    MATH(S, SI, 'Sim_PM_kWRaw', 'Multiply', 'Plant_kW', 'MeterFactor')
    MATH(S, SI, 'Sim_PM_kW', 'Add', 'Sim_PM_kWRaw', 'MeterFixed_kW'); simlink(S, 'PM_Main_kW', 'Sim_PM_kW')
    S.npoint(SI, 'Sim_PM_Meter', 'Sim_PM_kW', 'kW', 1, kind='sim'); M6.NO_HISTORY.add('Sim_PM_Meter')
    add_ext(S, 'Sim_PM_Meter', 'Energy', 'c:NumericTotalizerExt', [('totalizationInterval', None, 'hourly')])
    simlink(S, 'PM_Main_kWh', 'Sim_PM_Meter:Energy.total')
    MATH(S, SI, 'Sim_PM_Amps', 'Multiply', 'Sim_PM_kW', 'Amps_per_kW'); simlink(S, 'PM_Main_Amps', 'Sim_PM_Amps')
    simlink(S, 'PM_Main_Volts', 'Sim_GridVolts'); simlink(S, 'PM_Main_PF', 'Sim_PowerFactor'); simlink(S, 'PM_Main_Hz', 'Sim_GridHz')
    MATH(S, 'Alarms', 'PmVsSumDiff', 'Subtract', 'PM_Main_kW', 'Plant_kW')
    S.kc('Alarms', 'PmVsSumAbs', 'AbsValue', {'inA': 'PmVsSumDiff'})
    MATH(S, 'Alarms', 'PmGuard', 'Maximum', 'Plant_kW', 'MinLoadForKpi')
    MATH(S, 'Alarms', 'PmDevLimit', 'Multiply', 'PmGuard', 'Meter_DeviationPct', 'Pct_to_Frac')
    CMP(S, 'Alarms', 'PmDevHigh', 'GreaterThan', 'PmVsSumAbs', 'PmDevLimit')
    AND(S, 'Alarms', 'PmDevLogic', 'PmDevHigh', 'PM_Main_CommOk', 'PlantRunning30min')
    DLY(S, 'Alarms', 'PmDevDelay', 'PmDevLogic', 1800000)
    S.bpoint('Alarms', 'PowerMeter_DeviationAlarm', 'PmDevDelay', 'Deviation', 'Normal')
    for pt, v in {'CT01BasinLowLevelAlarm': (True, 'Critical', 'CT01 basin level low - check make-up water'),
                  'CT02BasinLowLevelAlarm': (True, 'Critical', 'CT02 basin level low - check make-up water'),
                  'CT01BasinHighLevelAlarm': (True, 'Warning', 'CT01 basin level high - make-up valve / overflow'),
                  'CT02BasinHighLevelAlarm': (True, 'Warning', 'CT02 basin level high - make-up valve / overflow'),
                  'CT_ConductivityHighAlarm': (True, 'Warning', 'Condenser water conductivity high - bleed-off / treatment'),
                  'CDW_FlowLowAlarm': (True, 'Critical', 'Condenser water flow below chiller minimum'),
                  'BTU_DeviationAlarm': (True, 'Warning', 'BTU meter differs > 15 % from flow x dT (meter / sensor drift)'),
                  'BTU_InvalidAlarm': (True, 'Warning', 'BTU meter invalid - load from flow x dT'),
                  'PowerMeter_DeviationAlarm': (True, 'Warning', 'Main power meter differs > 15 % from sub-meter sum'),
                  **{f'CH{n}EvapApproachAlarm': (True, 'Warning', f'Chiller {n} evaporator approach high (fouling / refrigerant)') for n in UNITS},
                  **{f'CH{n}CondApproachAlarm': (True, 'Warning', f'Chiller {n} condenser approach high (tube cleaning)') for n in UNITS},
                  **{f'CH{n}EvapLowFlowAlarm': (True, 'Critical', f'Chiller {n} evaporator flow below OEM minimum while running') for n in UNITS},
                  **{f'{e}{n}NoDeltaPAlarm': (True, 'Critical', f'{e}{n} running without differential pressure - failed over') for e in ('CHP', 'CDP') for n in UNITS},
                  **{f'{e}{n}LowSuctionAlarm': (True, 'Warning', f'{e}{n} low suction pressure') for e in ('CHP', 'CDP') for n in UNITS},
                  **{f'CT{n}_LowLevelSwitch': (True, 'Critical', f'CT{n} low level switch') for n in UNITS},
                  **{f'CT{n}_HighLevelSwitch': (True, 'Warning', f'CT{n} high level switch') for n in UNITS},
                  'BTU_CommOk': (False, 'Warning', 'BTU meter communication lost'),
                  'PM_Main_CommOk': (False, 'Warning', 'Main power meter communication lost')}.items():
        M6.COS[pt] = v
    M6.OOR.update({'CHW_SupplyHeaderPressure': (100.0, 600.0, 'Warning', 300000, True), 'CHW_ExpansionTankPressure': (120.0, 400.0, 'Critical', 300000, False),
                   'CH01_ChwSupplyTemp': (3.0, 15.0, 'Warning', 900000, True), 'CH02_ChwSupplyTemp': (3.0, 15.0, 'Warning', 900000, True),
                   'PM_Main_Volts': (360.0, 440.0, 'Warning', 60000, False), 'PM_Main_PF': (0.85, 1.0, 'Info', 900000, True)})


# ============================================================ 3. air-side standard library
AIR = 'AirSide'
AIR_UNITS = [  # (name, template, schedule, description)
    ('AHU01', 'AHU', 'Sch_AHU', 'Air handling unit, VSD supply fan, CHW valve, CO2 demand ventilation'),
    ('AHU02', 'AHU', 'Sch_AHU', 'Air handling unit, VSD supply fan, CHW valve, CO2 demand ventilation'),
    ('OAU01', 'OAU', 'Sch_AHU', 'Outdoor air unit, leaving-air (dew-point) control, constant airflow'),
    ('FCU01', 'FCU', 'Sch_FCU', 'Fan coil unit, 3-speed fan by room temperature band, on/off valve'),
    ('FCU02', 'FCU', 'Sch_FCU', 'Fan coil unit, 3-speed fan by room temperature band, on/off valve'),
    ('FCU03', 'FCU', 'Sch_FCU', 'Fan coil unit, 3-speed fan by room temperature band, on/off valve'),
    ('FCU04', 'FCU', 'Sch_FCU', 'Fan coil unit, 3-speed fan by room temperature band, on/off valve'),
    ('EF01', 'EF_CSV', 'Sch_EF', 'Exhaust fan, constant speed (SOO FAN-1)'),
    ('EF02', 'EF_PRESS', 'Sch_EF', 'Exhaust fan, VSD on duct static pressure (SOO FAN-3)'),
    ('EF03', 'EF_TEMP', 'Sch_EF', 'Ventilation fan, VSD on space temperature (SOO FAN-4, plant/electrical room)'),
    ('CPEF01', 'EF_CO', 'Sch_CarPark', 'Car-park exhaust fan, VSD on CO, smoke mode on fire alarm'),
    ('LSF01', 'LSF', None, 'Stair pressurisation fan, fire alarm start, VSD on stair dP (SOO LSF-1)'),
    ('SEF01', 'SEF', None, 'Smoke exhaust fan, fire alarm start (life safety)'),
]
FAN_KW = {'AHU': 15.0, 'OAU': 11.0, 'FCU': 0.25, 'EF_CSV': 2.2, 'EF_PRESS': 5.5, 'EF_TEMP': 4.0, 'EF_CO': 7.5, 'LSF': 11.0, 'SEF': 15.0}


def airside(S, prof):
    C, SC, SIM = f'{AIR}/Common', f'{AIR}/Schedules', f'{AIR}/Simulation'
    di(S, C, 'FireAlarmSignal', False, 'FIRE', 'Normal', note='Fire alarm control panel (FACP) general alarm, volt-free contact')
    S.bpoint(C, 'FireModeActive', 'FireAlarmSignal', 'Fire mode', 'Normal')
    NOT(S, C, 'NotFireAlarm', 'FireAlarmSignal')
    S.bparam('AirSide_FireStopsFCU', True, folder=C, t='Stop', f='Run', note='FCUs stop on fire alarm (PROJECT fire strategy)')
    NOT(S, C, 'FcuFireStopLogic', 'AirSide_FireStopsFCU')
    OR(S, C, 'FcuFirePermit', 'NotFireAlarm', 'FcuFireStopLogic')
    for sch, win in (('Sch_AHU', ('07:00:00.000', '22:00:00.000')), ('Sch_FCU', ('08:00:00.000', '20:00:00.000')),
                     ('Sch_EF', ('06:00:00.000', '23:00:00.000')), ('Sch_CarPark', ('06:00:00.000', '23:59:00.000'))):
        el = M6.schedule_el(S, sch, weekly=win)
        S.comp[sch] = el; S.folder_of[sch] = SC
        S.log.append(('ADD', SC, sch, 'sch:BooleanSchedule', f'Mon-Sun {win[0][:5]}-{win[1][:5]}', 'edit in Workbench Scheduler view'))
    for n_, v_ in (('AHU_ServiceHours', 4000.0), ('FAN_ServiceHours', 8000.0), ('FCU_ServiceHours', 4000.0)):
        S.param(n_, v_, 'hr', folder=C, note='Runtime exceeded (maintenance due) - SOO FAN-1/3')
    const(S, 'Zero', 0.0); const(S, 'HundredPct', 100.0, 'pct')
    calls, reqs, running = [], [], []
    for name, tpl, sch, desc in AIR_UNITS:
        fn = {'AHU': ahu, 'OAU': oau, 'FCU': fcu, 'EF_CSV': ef_csv, 'EF_PRESS': ef_press, 'EF_TEMP': ef_temp,
              'EF_CO': ef_co, 'LSF': lsf, 'SEF': sef}[tpl]
        r = fn(S, name, sch, prof)
        S.log.append(('TEMPLATE', f'{AIR}/{name}', name, tpl, desc, 'air-side standard library'))
        calls += r.get('call', []); reqs += r.get('req', []); running += r.get('run', [])
    # ---- plant interface: cooling calls (plant demand mode) + CHW requests (Trim & Respond)
    def count(name, lst):
        nums = []
        for b in lst:
            SW(S, C, f'Cnt_{b}', b, 'One', 'ZeroSpeed'); nums.append(f'Cnt_{b}')
        prev = None
        for i in range(0, len(nums), 3):
            grp = ([prev] if prev else []) + nums[i:i + 3]
            nm = f'{name}Sum{i // 3}'
            MATH(S, C, nm, 'Add', *grp); prev = nm
        return prev
    S.npoint(C, 'AirSide_CoolingCalls', count('Calls', calls), 'none', 0)
    S.npoint(C, 'AirSide_ChwRequests', count('Reqs', reqs), 'none', 0)
    S.npoint(C, 'AirSide_UnitsRunning', count('Run', running), 'none', 0)   # AHU / OAU only (units that raise T&R requests)
    # plant demand mode (SOO ETS mode 4 / chiller manager 'number of buildings calling')
    S.bparam('PlantDemandMode', False, folder='PlantControl/Points', t='Demand', f='Always', note='true = plant runs only while >= N air-side units call for cooling')
    S.param('Plant_DemandMinCalls', 1.0, 'none', prec=0, note='Air-side cooling calls needed to enable the plant (demand mode)')
    E0 = 'PlantControl/Enable'
    CMP(S, E0, 'AirSideCallsEnough', 'GreaterThanEqual', 'AirSide_CoolingCalls', 'Plant_DemandMinCalls')
    DLY(S, E0, 'AirSideCallsStable', 'AirSideCallsEnough', 300000, 900000, note='5 min on / 15 min off (anti short-cycle)')
    NOT(S, E0, 'DemandNotRequired', 'PlantDemandMode')
    OR(S, E0, 'DemandOk', 'DemandNotRequired', 'AirSideCallsStable')
    S.rewire('PlantEnableEffective', 'inC', 'DemandOk', T)
    # Trim & Respond (ASHRAE GPC36 5.1.14 structure) from AHU/OAU valve requests -> plant reset request 0-100 %
    O = 'Optimization'
    S.bparam('ResetSource_AirSide', True, folder='ModeControl', t='AHU requests', f='Plant load', note='Plant reset from AHU valve requests (T&R) when air side online, else plant-load proxy')
    S.param('TR_IgnoreRequests', 1.0, 'none', folder=O, prec=0, note='T&R: requests ignored (trim when fewer)')
    CMP(S, O, 'AirSideOnline', 'GreaterThanEqual', 'AirSide_UnitsRunning', 'One')
    AND(S, O, 'TR_Use', 'ResetSource_AirSide', 'AirSideOnline', 'PlantRunRequest')
    PID(S, O, 'TR_Loop', 'AirSide_ChwRequests', 'TR_IgnoreRequests', 'TR_Use', 'direct', 2.0, 0.5, 20.0, 100.0,
        note='integrating trim & respond: +1 %/min per request above ignore, -1 %/min when none')
    SW(S, O, 'TR_ResetSelect', 'TR_Use', 'TR_Loop', 'PlantLoadPct', note='fail-safe: plant load proxy when no AHU online')
    S.rewire('PlantResetRequest', 'inA', 'TR_ResetSelect', 'PlantLoadPct')
    S.bpoint(O, 'PlantResetSource', 'TR_Use', 'AHU requests', 'Plant load')
    M6.COS['FireAlarmSignal'] = (True, 'Emergency', 'FIRE ALARM - air-side fire mode active')


# ---------------------------------------------------------------- template helpers
def _f(u, sub): return f'{AIR}/{u}/{sub}'


_STAGGER = [0]


def unit_core(S, u, sch, prof, *, vsd=False, fire='stop', service='FAN_ServiceHours', rated=2.2, extra_run=None, extra_perm=None, hoa=True):
    """Common start/stop core (SOO AHU/FAN-1: Run condition -> Fire -> HOA -> Overload -> start -> proof).
    fire: 'stop' (normal HVAC), 'run' (life safety: fire starts the fan), 'fcu' (FCU policy switch)."""
    Pt, L, Mo = _f(u, 'Points'), _f(u, 'Logic'), _f(u, 'Monitor')
    di(S, Pt, f'{u}_Status', False, 'Run', 'Stop', note='fan run status (DP switch / CT relay / VFD run)')
    di(S, Pt, f'{u}_InAuto', True, 'Auto', 'Hand/Off', note='HOA selector')
    di(S, Pt, f'{u}_Overload', False, 'Trip', 'Normal', note='motor overload / MCCB trip')
    if vsd: di(S, Pt, f'{u}_VfdFault', False, 'Fault', 'Normal', note='VFD fault')
    S.bparam(f'{u}_ModeAuto', True, folder=Pt, t='Auto', f='Manual', note='Auto = schedule, Manual = ON/OFF command')
    S.bparam(f'{u}_ManualOn', False, folder=Pt, t='On', f='Off', note='Manual mode command (override 24 h)')
    NOT(S, L, f'{u}NotModeAuto', f'{u}_ModeAuto')
    if sch:
        AND(S, L, f'{u}SchedRun', f'{u}_ModeAuto', sch)
    else:
        S.bparam(f'{u}_TestRun', False, folder=Pt, t='Test', f='Normal', note='Weekly life-safety test run (manual)')
        AND(S, L, f'{u}SchedRun', f'{u}_ModeAuto', f'{u}_TestRun')
    AND(S, L, f'{u}ManRun', f'{u}NotModeAuto', f'{u}_ManualOn')
    if extra_run:
        AND(S, L, f'{u}ExtraRun', extra_run[0], f'{u}_ModeAuto')
    OR(S, L, f'{u}RunRequest', f'{u}SchedRun', f'{u}ManRun', *([f'{u}ExtraRun'] if extra_run else []))
    NOT(S, L, f'{u}NotOverload', f'{u}_Overload')
    trips = [f'{u}NotOverload'] + ([f'{u}NotVfdFault'] if vsd else [])
    if vsd: NOT(S, L, f'{u}NotVfdFault', f'{u}_VfdFault')
    firep = {'stop': 'NotFireAlarm', 'fcu': 'FcuFirePermit', 'run': T}[fire]
    if fire != 'run':        # staggered restart after the fire alarm clears (10 s per unit)
        _STAGGER[0] += 1
        DLY(S, L, f'{u}FireClearDelay', firep, 10000 * _STAGGER[0], 0, note='staggered restart after fire reset')
        firep = f'{u}FireClearDelay'
    AND(S, L, f'{u}Permissive', f'{u}_InAuto', *trips, *(extra_perm or []))
    AND(S, L, f'{u}NormalStart', f'{u}RunRequest', f'{u}Permissive', firep)
    if fire == 'run':      # life safety: fire alarm starts the fan (HOA must be AUTO; overload/VFD trips bypassed in fire mode)
        AND(S, L, f'{u}FireStart', 'FireAlarmSignal', f'{u}_InAuto')
        OR(S, L, f'{u}StartRequest', f'{u}NormalStart', f'{u}FireStart')
    else:
        OR(S, L, f'{u}StartRequest', f'{u}NormalStart')
    # anti short-cycle: minimum off time before a restart
    S.kc(L, f'{u}StartLogic', 'And', {'inA': f'{u}StartRequest', 'inC': T, 'inD': T})
    NOT(S, L, f'{u}NotStartLogic', f'{u}StartLogic')
    DLY(S, L, f'{u}MinOffDone', f'{u}NotStartLogic', prof['fan_min_off'], note='minimum off time')
    OR(S, L, f'{u}MinOffPermit', f'{u}MinOffDone', f'{u}StartLogic')
    S.link(S.comp[f'{u}StartLogic'], f'{u}MinOffPermit', 'inB')
    if fire == 'run':       # fire start bypasses the minimum-off timer
        OR(S, L, f'{u}StartFinal', f'{u}StartLogic', f'{u}FireStart')
        S.bpoint(Pt, f'{u}_StartCmd', f'{u}StartFinal', 'ON', 'OFF', kind='do')
    else:
        S.bpoint(Pt, f'{u}_StartCmd', f'{u}StartLogic', 'ON', 'OFF', kind='do')
    NOT(S, L, f'{u}NotStatus', f'{u}_Status')
    AND(S, L, f'{u}FailLogic', f'{u}_StartCmd', f'{u}NotStatus')
    DLY(S, L, f'{u}FailDelay', f'{u}FailLogic', prof['fan_proof'], note='Fan Failure: commanded ON, status OFF')
    S.bpoint(Mo, f'{u}_FanFailAlarm', f'{u}FailDelay', 'Fan fail', 'Normal')
    NOT(S, L, f'{u}NotStartCmd', f'{u}_StartCmd')
    AND(S, L, f'{u}HandLogic', f'{u}NotStartCmd', f'{u}_Status')
    DLY(S, L, f'{u}HandDelay', f'{u}HandLogic', 60000, note='Fan in Hand: commanded OFF, status ON')
    S.bpoint(Mo, f'{u}_FanInHandAlarm', f'{u}HandDelay', 'In hand', 'Normal')
    add_ext(S, f'{u}_Status', 'Runtime', 'c:DiscreteTotalizerExt')
    S.kc(L, f'{u}RuntimeCalc', 'Divide', {'inA': f'{u}_Status:Runtime.elapsedActiveTimeNumeric', 'inB': 'MsPerHour'})
    S.npoint(Mo, f'{u}_RuntimeHours', f'{u}RuntimeCalc', 'hr', 1)
    CMP(S, L, f'{u}RuntimeOver', 'GreaterThan', f'{u}RuntimeCalc', service)
    S.bpoint(Mo, f'{u}_RuntimeExceededAlarm', f'{u}RuntimeOver', 'Service due', 'Normal')
    DLY(S, L, f'{u}Running30min', f'{u}_Status', 1800000)
    # power (emulated meter on the fan)
    ai(S, Pt, f'{u}_kW', 0.0, 'kW', prec=2, note='fan power (VFD / meter)', hist='5min')
    SIM = f'{AIR}/Simulation'
    DLY(S, SIM, f'Sim_{u}_StatusFb', f'{u}_StartCmd', 3000, 2000)
    simlink(S, f'{u}_Status', f'Sim_{u}_StatusFb', 'emulated fan status')
    const(S, f'{u}_RatedKW', rated, 'kW', 2, note='SIM: fan motor rating')
    for pt, v in {f'{u}_FanFailAlarm': (True, 'Critical', f'{u} fan failure (commanded ON, no status)'),
                  f'{u}_FanInHandAlarm': (True, 'Warning', f'{u} running in HAND (commanded OFF)'),
                  f'{u}_Overload': (True, 'Critical', f'{u} overload trip'),
                  f'{u}_RuntimeExceededAlarm': (True, 'Info', f'{u} runtime exceeded - maintenance due'),
                  f'{u}_InAuto': (False, 'Warning', f'{u} HOA not in AUTO')}.items():
        M6.COS[pt] = v
    if vsd: M6.COS[f'{u}_VfdFault'] = (True, 'Critical', f'{u} VFD fault')
    return Pt, L, Mo


def fan_speed(S, u, L, Pt, pid_or_calc, valid, failsafe, min_pct, gate):
    """VSD speed: control output when the sensor is valid, fail-safe speed otherwise, 0 when the fan is not started."""
    SW(S, L, f'{u}SpeedSafe', valid, pid_or_calc, failsafe, note='sensor invalid -> fixed fail-safe speed')
    LIMIT(S, L, f'{u}SpeedClamp', f'{u}SpeedSafe', min_pct, 100.0)
    SW(S, L, f'{u}SpeedGate', gate, f'{u}SpeedClamp', 'ZeroSpeed')
    RATE(S, L, f'{u}SpeedRamp', f'{u}SpeedGate', 5.0, note='VFD ramp 5 %/s')
    S.npoint(Pt, f'{u}_SpeedCmd', f'{u}SpeedRamp', 'pct', 1, kind='ao')
    ai(S, Pt, f'{u}_SpeedFeedbackHz', 0.0, 'Hz', note='VFD output frequency', hist='5min')
    SIM = f'{AIR}/Simulation'
    MATH(S, SIM, f'Sim_{u}_HzRun', 'Multiply', f'{u}_SpeedCmd', 'HzPerPct')
    SW(S, SIM, f'Sim_{u}_Hz', f'Sim_{u}_StatusFb', f'Sim_{u}_HzRun', 'ZeroSpeed'); simlink(S, f'{u}_SpeedFeedbackHz', f'Sim_{u}_Hz')
    MATH(S, SIM, f'Sim_{u}_Frac', 'Divide', f'{u}_SpeedCmd', 'HundredPct')
    SW(S, SIM, f'Sim_{u}_On', f'Sim_{u}_StatusFb', 'One', 'ZeroSpeed')
    MATH(S, SIM, f'Sim_{u}_kW', 'Multiply', f'Sim_{u}_Frac', f'Sim_{u}_Frac', f'Sim_{u}_Frac', f'{u}_RatedKW')
    simlink(S, f'{u}_kW', f'Sim_{u}_kW', 'affinity law')


def range_valid(S, L, u, pt, lo, hi):
    const(S, f'Valid_{pt}_Lo', lo); const(S, f'Valid_{pt}_Hi', hi)
    CMP(S, L, f'{pt}AboveMin', 'GreaterThanEqual', pt, f'Valid_{pt}_Lo')
    CMP(S, L, f'{pt}BelowMax', 'LessThanEqual', pt, f'Valid_{pt}_Hi')
    AND(S, L, f'{pt}Valid', f'{pt}AboveMin', f'{pt}BelowMax')
    NOT(S, L, f'{pt}Invalid', f'{pt}Valid')
    S.bpoint(_f(u, 'Monitor'), f'{pt}_SensorAlarm', f'{pt}Invalid', 'Invalid', 'Normal')
    M6.COS[f'{pt}_SensorAlarm'] = (True, 'Warning', f'{pt} sensor invalid - fail-safe output')
    return f'{pt}Valid'


def valve_loop(S, u, L, Pt, cv, sp, enable_gate, valid, failsafe, kp=5.0, ki=0.5, name='Valve'):
    PID(S, L, f'{u}{name}PID', cv, sp, enable_gate, 'direct', kp, ki, 0.0, 100.0, note='cooling: temperature above setpoint -> open')
    SW(S, L, f'{u}{name}Safe', valid, f'{u}{name}PID', failsafe, note='sensor invalid -> fail-safe position')
    SW(S, L, f'{u}{name}Gate', enable_gate, f'{u}{name}Safe', 'ZeroSpeed', note='closed when fan not proven (no coil freeze / condensation)')
    S.npoint(Pt, f'{u}_{name}Cmd', f'{u}{name}Gate', 'pct', 1, kind='ao')
    ai(S, Pt, f'{u}_{name}Feedback', 0.0, 'pct', note='valve position feedback', hist='5min')
    RATE(S, f'{AIR}/Simulation', f'Sim_{u}_{name}Fb', f'{u}_{name}Cmd', 2.0, note='actuator 2 %/s'); simlink(S, f'{u}_{name}Feedback', f'Sim_{u}_{name}Fb')
    MATH(S, L, f'{u}{name}Dev', 'Subtract', f'{u}_{name}Cmd', f'{u}_{name}Feedback')
    S.kc(L, f'{u}{name}DevAbs', 'AbsValue', {'inA': f'{u}{name}Dev'})
    CMP(S, L, f'{u}{name}DevHigh', 'GreaterThan', f'{u}{name}DevAbs', 'BypassMismatchPct')
    DLY(S, L, f'{u}{name}DevDelay', f'{u}{name}DevHigh', 300000)
    S.bpoint(_f(u, 'Monitor'), f'{u}_{name}MismatchAlarm', f'{u}{name}DevDelay', 'Mismatch', 'Normal')
    M6.COS[f'{u}_{name}MismatchAlarm'] = (True, 'Warning', f'{u} valve command/feedback mismatch (actuator)')
    return f'{u}_{name}Cmd'


def cooling_calls(S, u, L, Mo, valve):
    const(S, 'AirCallPct', 10.0, 'pct'); const(S, 'AirRequestPct', 95.0, 'pct')
    CMP(S, L, f'{u}ValveAboveCall', 'GreaterThan', valve, 'AirCallPct')
    AND(S, L, f'{u}CallLogic', f'{u}ValveAboveCall', f'{u}_Status')
    S.bpoint(Mo, f'{u}_CoolingCall', f'{u}CallLogic', 'Calling', 'Satisfied')
    CMP(S, L, f'{u}ValveNearFull', 'GreaterThan', valve, 'AirRequestPct')
    AND(S, L, f'{u}ReqLogic', f'{u}ValveNearFull', f'{u}_Status')
    DLY(S, L, f'{u}ReqDelay', f'{u}ReqLogic', 300000, 60000, note='T&R request: valve > 95 % for 5 min')
    S.bpoint(Mo, f'{u}_ChwRequest', f'{u}ReqDelay', 'Request', 'None')
    return f'{u}_CoolingCall', f'{u}_ChwRequest'


def filter_alarm(S, u, L, Mo, Pt, sim_mid):
    ai(S, Pt, f'{u}_FilterDP', sim_mid, 'Pa', prec=0, note='filter differential pressure transmitter', hist='5min')
    S.param(f'{u}_FilterDPMax', 250.0, 'Pa', folder=Pt, prec=0, note='dirty filter limit')
    CMP(S, L, f'{u}FilterHigh', 'GreaterThan', f'{u}_FilterDP', f'{u}_FilterDPMax')
    AND(S, L, f'{u}FilterLogic', f'{u}FilterHigh', f'{u}_Status')
    DLY(S, L, f'{u}FilterDelay', f'{u}FilterLogic', 300000)
    S.bpoint(Mo, f'{u}_FilterDirtyAlarm', f'{u}FilterDelay', 'Dirty', 'Clean')
    M6.COS[f'{u}_FilterDirtyAlarm'] = (True, 'Warning', f'{u} filter dirty - replace / clean')
    ramp(S, f'Sim_{u}_FilterDP', 'Ramp', 5400000 + len(u) * 60000, 85.0, sim_mid, 'Pa', target=f'{u}_FilterDP')


# ---------------------------------------------------------------- templates
def ahu(S, u, sch, prof):
    di(S, _f(u, 'Points'), f'{u}_SmokeDetected', False, 'SMOKE', 'Normal', note='duct smoke detector (return / supply air)')
    PULSE(S, _f(u, 'Logic'), f'{u}SmokeResetFire', note='Px RESET smoke shutdown -> action fire')
    sealin(S, _f(u, 'Logic'), f'{u}SmokeLatch', f'{u}_SmokeDetected', f'{u}SmokeResetFire', note='smoke shutdown latched until RESET')
    S.bpoint(_f(u, 'Monitor'), f'{u}_SmokeShutdown', f'{u}SmokeLatch', 'Latched', 'Normal')
    NOT(S, _f(u, 'Logic'), f'{u}NoSmoke', f'{u}SmokeLatch')
    Pt, L, Mo = unit_core(S, u, sch, prof, vsd=True, fire='stop', service='AHU_ServiceHours', rated=FAN_KW['AHU'], extra_perm=[f'{u}NoSmoke'])
    M6.COS[f'{u}_SmokeDetected'] = (True, 'Emergency', f'{u} duct smoke detected - unit stopped')
    SIM = f'{AIR}/Simulation'
    for nm, v, un, note in (('SAT', 14.0, 'C', 'TT supply air'), ('RAT', 24.0, 'C', 'TT return air (space proxy)'),
                            ('RA_RH', 55.0, 'RH', 'RH return air'), ('RA_CO2', 700.0, 'ppm', 'CO2 return air'),
                            ('DuctStatic', 250.0, 'Pa', 'PT supply duct static pressure')):
        ai(S, Pt, f'{u}_{nm}', v, un, prec=0 if un in ('ppm', 'Pa') else 1, note=note)
    S.param(f'{u}_RAT_SP', 24.0, 'C', folder=Pt, lo=18.0, hi=30.0, note='Return air / space setpoint')
    S.param(f'{u}_SAT_Min', 13.0, 'C', folder=Pt, note='SAT reset low limit (full cooling)')
    S.param(f'{u}_SAT_Max', 18.0, 'C', folder=Pt, note='SAT reset high limit (low load, energy)')
    S.param(f'{u}_SAT_Default', 15.0, 'C', folder=Pt, note='SAT setpoint when RAT sensor invalid')
    S.param(f'{u}_DuctStatic_SP', 250.0, 'Pa', folder=Pt, prec=0)
    S.param(f'{u}_CO2_Low', 800.0, 'ppm', folder=Pt, prec=0, note='DCV: minimum OA below this CO2')
    S.param(f'{u}_CO2_High', 1100.0, 'ppm', folder=Pt, prec=0, note='DCV: 100 % OA damper at this CO2')
    S.param(f'{u}_OAD_Min', 20.0, 'pct', folder=Pt, note='minimum outdoor air damper (ventilation code)')
    ratv = range_valid(S, L, u, f'{u}_RAT', 5.0, 45.0)
    satv = range_valid(S, L, u, f'{u}_SAT', 2.0, 45.0)
    stv = range_valid(S, L, u, f'{u}_DuctStatic', 0.0, 1500.0)
    co2v = range_valid(S, L, u, f'{u}_RA_CO2', 300.0, 5000.0)
    # SAT reset from return air (RAT_SP -1 K -> SAT max, RAT_SP +1 K -> SAT min)
    MATH(S, L, f'{u}RatSpLo', 'Subtract', f'{u}_RAT_SP', 'One'); MATH(S, L, f'{u}RatSpHi', 'Add', f'{u}_RAT_SP', 'One')
    RESET(S, L, f'{u}SatReset', f'{u}_RAT', f'{u}RatSpLo', f'{u}RatSpHi', f'{u}_SAT_Max', f'{u}_SAT_Min', note='SAT reset (energy)')
    SW(S, L, f'{u}SatSpSelect', ratv, f'{u}SatReset', f'{u}_SAT_Default', note='RAT invalid -> fixed SAT setpoint')
    S.npoint(Pt, f'{u}_SAT_SP', f'{u}SatSpSelect', 'C', 1, kind='sp')
    const(S, 'AHU_ValveFailSafe', 60.0, 'pct', note='valve position when SAT sensor invalid')
    valve = valve_loop(S, u, L, Pt, f'{u}_SAT', f'{u}_SAT_SP', f'{u}_Status', satv, 'AHU_ValveFailSafe')
    PID(S, L, f'{u}StaticPID', f'{u}_DuctStatic', f'{u}_DuctStatic_SP', f'{u}_StartCmd', 'reverse', 0.05, 1.0, 30.0, 100.0,
        note='duct static below setpoint -> speed up')
    const(S, 'Fan_FailSafeSpeed', 80.0, 'pct')
    fan_speed(S, u, L, Pt, f'{u}StaticPID', stv, 'Fan_FailSafeSpeed', 30.0, f'{u}_StartCmd')
    # CO2 demand-controlled ventilation
    RESET(S, L, f'{u}OadReset', f'{u}_RA_CO2', f'{u}_CO2_Low', f'{u}_CO2_High', f'{u}_OAD_Min', 'HundredPct')
    const(S, 'OAD_FailSafe', 50.0, 'pct')
    SW(S, L, f'{u}OadSafe', co2v, f'{u}OadReset', 'OAD_FailSafe')
    SW(S, L, f'{u}OadGate', f'{u}_Status', f'{u}OadSafe', 'ZeroSpeed')
    S.npoint(Pt, f'{u}_OADamperCmd', f'{u}OadGate', 'pct', 1, kind='ao')
    filter_alarm(S, u, L, Mo, Pt, 180.0)
    # comfort / tracking alarms
    const(S, 'AirSatMargin', 3.0); const(S, 'AirRatMargin', 2.0)
    MATH(S, L, f'{u}SatLimit', 'Add', f'{u}_SAT_SP', 'AirSatMargin'); CMP(S, L, f'{u}SatHigh', 'GreaterThan', f'{u}_SAT', f'{u}SatLimit')
    AND(S, L, f'{u}SatHighLogic', f'{u}SatHigh', f'{u}Running30min', satv)
    DLY(S, L, f'{u}SatHighDelay', f'{u}SatHighLogic', 900000)
    S.bpoint(Mo, f'{u}_SATNotTrackingAlarm', f'{u}SatHighDelay', 'High', 'Normal')
    MATH(S, L, f'{u}RatLimit', 'Add', f'{u}_RAT_SP', 'AirRatMargin'); CMP(S, L, f'{u}RatHigh', 'GreaterThan', f'{u}_RAT', f'{u}RatLimit')
    AND(S, L, f'{u}RatHighLogic', f'{u}RatHigh', f'{u}Running30min', ratv)
    DLY(S, L, f'{u}RatHighDelay', f'{u}RatHighLogic', 1800000)
    S.bpoint(Mo, f'{u}_SpaceTempHighAlarm', f'{u}RatHighDelay', 'Hot', 'Normal')
    M6.COS[f'{u}_SATNotTrackingAlarm'] = (True, 'Warning', f'{u} supply air above setpoint + 3 K for 15 min (CHW / valve)')
    M6.COS[f'{u}_SpaceTempHighAlarm'] = (True, 'Warning', f'{u} return air above setpoint + 2 K for 30 min')
    call, req = cooling_calls(S, u, L, Mo, valve)
    # ---- emulation: RAT disturbance, SAT closed loop on valve, static on fan speed
    k = int(u[-2:])
    ramp(S, f'Sim_{u}_RAT', 'SineWave', 1500000 + k * 300000, 1.5, 24.3 + 0.3 * k, 'C', target=f'{u}_RAT')
    const(S, 'Sim_AhuCoilK', -0.12, prec=3)
    MATH(S, SIM, f'Sim_{u}_CoilDrop', 'Multiply', f'{u}_ValveFeedback', 'Sim_AhuCoilK', f'Sim_{u}_On')
    RATE(S, SIM, f'Sim_{u}_CoilLag', f'Sim_{u}_CoilDrop', 0.1, note='coil thermal lag 0.1 K/s (starts at 0 = no cooling)')
    MATH(S, SIM, f'Sim_{u}_SAT', 'Add', f'{u}_RAT', f'Sim_{u}_CoilLag'); simlink(S, f'{u}_SAT', f'Sim_{u}_SAT')
    const(S, 'Sim_StaticPerPct', 3.4, prec=2)
    MATH(S, SIM, f'Sim_{u}_Static', 'Multiply', f'{u}_SpeedCmd', 'Sim_StaticPerPct', f'Sim_{u}_On'); simlink(S, f'{u}_DuctStatic', f'Sim_{u}_Static')
    ramp(S, f'Sim_{u}_RH', 'SineWave', 2100000, 7.0, 55.0, 'RH', target=f'{u}_RA_RH')
    ramp(S, f'Sim_{u}_CO2', 'Ramp', 3600000 + k * 600000, 300.0, 850.0, 'ppm', target=f'{u}_RA_CO2')
    return {'call': [call], 'req': [req], 'run': [f'{u}_Status']}


def oau(S, u, sch, prof):
    Pt, L, Mo = unit_core(S, u, sch, prof, vsd=True, fire='stop', service='AHU_ServiceHours', rated=FAN_KW['OAU'])
    SIM = f'{AIR}/Simulation'
    ai(S, Pt, f'{u}_LAT', 16.5, 'C', note='TT leaving (off-coil) air'); ai(S, Pt, f'{u}_LAT_RH', 92.0, 'RH', note='RH leaving air')
    ai(S, Pt, f'{u}_Airflow', 6000.0, 'm3h_air', prec=0, note='airflow station / VFD calculated airflow')
    S.param(f'{u}_LAT_SP', 16.5, 'C', folder=Pt, lo=9.0, hi=20.0, note='SOO OAU: 16.5 (general) / 10.5 (office dehumidification)')
    S.param(f'{u}_Airflow_SP', 6000.0, 'm3h_air', folder=Pt, prec=0, note='equipment schedule design airflow')
    S.kc(L, f'{u}Psychro', 'Psychrometric', {'inTemp': f'{u}_LAT', 'inHumidity': f'{u}_LAT_RH'}, props=[('unitSelect', None, 'metric')])
    S.npoint(Mo, f'{u}_LAT_DewPoint', f'{u}Psychro.outDewPoint', 'C', 1)
    latv = range_valid(S, L, u, f'{u}_LAT', 2.0, 45.0)
    afv = range_valid(S, L, u, f'{u}_Airflow', 0.0, 50000.0)
    const(S, 'OAU_ValveFailSafe', 70.0, 'pct', note='OAU valve when LAT sensor invalid (dehumidify)')
    valve = valve_loop(S, u, L, Pt, f'{u}_LAT', f'{u}_LAT_SP', f'{u}_Status', latv, 'OAU_ValveFailSafe')
    PID(S, L, f'{u}AirflowPID', f'{u}_Airflow', f'{u}_Airflow_SP', f'{u}_StartCmd', 'reverse', 0.005, 1.0, 20.0, 100.0,
        note='constant airflow (SOO OAU: VSD tracks equipment-schedule airflow)')
    const(S, 'Fan_FailSafeSpeed', 80.0, 'pct')
    fan_speed(S, u, L, Pt, f'{u}AirflowPID', afv, 'Fan_FailSafeSpeed', 20.0, f'{u}_StartCmd')
    filter_alarm(S, u, L, Mo, Pt, 170.0)
    const(S, 'AirSatMargin', 3.0)
    MATH(S, L, f'{u}LatLimit', 'Add', f'{u}_LAT_SP', 'AirSatMargin'); CMP(S, L, f'{u}LatHigh', 'GreaterThan', f'{u}_LAT', f'{u}LatLimit')
    AND(S, L, f'{u}LatHighLogic', f'{u}LatHigh', f'{u}Running30min', latv)
    DLY(S, L, f'{u}LatHighDelay', f'{u}LatHighLogic', 900000)
    S.bpoint(Mo, f'{u}_LATHighAlarm', f'{u}LatHighDelay', 'High', 'Normal')
    M6.COS[f'{u}_LATHighAlarm'] = (True, 'Warning', f'{u} leaving air above setpoint + 3 K (humid air to building)')
    call, req = cooling_calls(S, u, L, Mo, valve)
    const(S, 'Sim_OauCoilK', -0.17, prec=3)
    MATH(S, SIM, f'Sim_{u}_CoilDrop', 'Multiply', f'{u}_ValveFeedback', 'Sim_OauCoilK', f'Sim_{u}_On')
    RATE(S, SIM, f'Sim_{u}_CoilLag', f'Sim_{u}_CoilDrop', 0.1)
    MATH(S, SIM, f'Sim_{u}_LAT', 'Add', 'OA_Temperature', f'Sim_{u}_CoilLag'); simlink(S, f'{u}_LAT', f'Sim_{u}_LAT')
    const(S, 'Sim_AirflowPerPct', 70.0, prec=1)
    MATH(S, SIM, f'Sim_{u}_Airflow', 'Multiply', f'{u}_SpeedCmd', 'Sim_AirflowPerPct', f'Sim_{u}_On'); simlink(S, f'{u}_Airflow', f'Sim_{u}_Airflow')
    ramp(S, f'Sim_{u}_LAT_RH', 'SineWave', 1700000, 4.0, 91.0, 'RH', target=f'{u}_LAT_RH')
    return {'call': [call], 'req': [req], 'run': [f'{u}_Status']}


def fcu(S, u, sch, prof):
    Pt, L, Mo = unit_core(S, u, sch, prof, vsd=False, fire='fcu', service='FCU_ServiceHours', rated=FAN_KW['FCU'])
    SIM = f'{AIR}/Simulation'
    ai(S, Pt, f'{u}_RoomTemp', 25.0, 'C', note='room temperature sensor / thermostat')
    S.param(f'{u}_RoomTemp_SP', 24.0, 'C', folder=Pt, lo=18.0, hi=30.0)
    rtv = range_valid(S, L, u, f'{u}_RoomTemp', 5.0, 45.0)
    MATH(S, L, f'{u}Error', 'Subtract', f'{u}_RoomTemp', f'{u}_RoomTemp_SP')
    S.npoint(Mo, f'{u}_RoomTempError', f'{u}Error', 'none', 1)
    HYST(S, L, f'{u}BandHigh', f'{u}Error', 1.0, 1.5, note='SOO FCU-2: > SP+1.5 K -> HIGH (off below SP+1)')
    HYST(S, L, f'{u}BandMed', f'{u}Error', 0.25, 0.75, note='> SP+0.75 K -> MEDIUM (off below SP+0.25)')
    HYST(S, L, f'{u}BandCool', f'{u}Error', -0.5, 0.5, note='valve opens above SP+0.5, closes below SP-0.5')
    NOT(S, L, f'{u}Invalid', rtv)
    OR(S, L, f'{u}MedOrFail', f'{u}BandMed', f'{u}Invalid', note='sensor invalid -> MEDIUM fan + valve open (fail-safe cooling)')
    AND(S, L, f'{u}HighLogic', f'{u}_StartCmd', f'{u}BandHigh', rtv)
    NOT(S, L, f'{u}NotHigh', f'{u}HighLogic')
    AND(S, L, f'{u}MedLogic', f'{u}_StartCmd', f'{u}MedOrFail', f'{u}NotHigh')
    NOT(S, L, f'{u}NotMedOrFail', f'{u}MedOrFail')
    AND(S, L, f'{u}LowLogic', f'{u}_StartCmd', f'{u}NotMedOrFail', f'{u}NotHigh')
    S.bpoint(Pt, f'{u}_FanLowCmd', f'{u}LowLogic', 'ON', 'OFF', kind='do')
    S.bpoint(Pt, f'{u}_FanMedCmd', f'{u}MedLogic', 'ON', 'OFF', kind='do')
    S.bpoint(Pt, f'{u}_FanHighCmd', f'{u}HighLogic', 'ON', 'OFF', kind='do')
    for sp, v in (('L', 1.0), ('M', 2.0), ('H', 3.0)): const(S, f'FcuSpeed{sp}', v, prec=0)
    SW(S, L, f'{u}SpdL', f'{u}LowLogic', 'FcuSpeedL', 'ZeroSpeed'); SW(S, L, f'{u}SpdM', f'{u}MedLogic', 'FcuSpeedM', 'ZeroSpeed')
    SW(S, L, f'{u}SpdH', f'{u}HighLogic', 'FcuSpeedH', 'ZeroSpeed')
    MATH(S, L, f'{u}SpdSum', 'Add', f'{u}SpdL', f'{u}SpdM', f'{u}SpdH')
    S.npoint(Mo, f'{u}_FanSpeedStage', f'{u}SpdSum', 'none', 0)
    OR(S, L, f'{u}CoolOrFail', f'{u}BandCool', f'{u}Invalid')
    AND(S, L, f'{u}ValveLogic', f'{u}CoolOrFail', f'{u}_Status', note='valve only with fan proven (SOO FCU-2)')
    S.bpoint(Pt, f'{u}_ValveCmd', f'{u}ValveLogic', 'OPEN', 'CLOSE', kind='do')
    const(S, 'FcuHighMargin', 3.0)
    CMP(S, L, f'{u}TooHot', 'GreaterThan', f'{u}Error', 'FcuHighMargin')
    AND(S, L, f'{u}HotLogic', f'{u}TooHot', f'{u}Running30min', rtv)
    DLY(S, L, f'{u}HotDelay', f'{u}HotLogic', 1800000)
    S.bpoint(Mo, f'{u}_RoomTempHighAlarm', f'{u}HotDelay', 'Hot', 'Normal')
    M6.COS[f'{u}_RoomTempHighAlarm'] = (True, 'Warning', f'{u} room above setpoint + 3 K for 30 min')
    S.bpoint(Mo, f'{u}_CoolingCall', f'{u}ValveLogic', 'Calling', 'Satisfied')
    # emulation: room drifts to a base load temperature, cooled while valve open and fan running
    k = int(u[-2:])
    ramp(S, f'Sim_{u}_Base', 'SineWave', 1800000 + k * 240000, 1.2, 25.8 + 0.2 * k, 'C')
    const(S, 'Sim_FcuCoolK', -3.5, prec=2)
    SW(S, SIM, f'Sim_{u}_ValveOn', f'{u}_ValveCmd', 'One', 'ZeroSpeed')
    MATH(S, SIM, f'Sim_{u}_Cooling', 'Multiply', f'Sim_{u}_ValveOn', 'Sim_FcuCoolK')
    RATE(S, SIM, f'Sim_{u}_CoolLag', f'Sim_{u}_Cooling', 0.01, note='room thermal lag 0.01 K/s')
    MATH(S, SIM, f'Sim_{u}_Room', 'Add', f'Sim_{u}_Base', f'Sim_{u}_CoolLag'); simlink(S, f'{u}_RoomTemp', f'Sim_{u}_Room')
    SW(S, SIM, f'Sim_{u}_kWStage', f'Sim_{u}_StatusFb', f'{u}SpdSum', 'ZeroSpeed')
    const(S, 'Third', 0.3333, prec=4)
    MATH(S, SIM, f'Sim_{u}_kW', 'Multiply', f'Sim_{u}_kWStage', f'{u}_RatedKW', 'Third')
    simlink(S, f'{u}_kW', f'Sim_{u}_kW')
    return {'call': [f'{u}_CoolingCall']}


def _csv_power(S, u):
    SIM = f'{AIR}/Simulation'
    SW(S, SIM, f'Sim_{u}_kW', f'Sim_{u}_StatusFb', f'{u}_RatedKW', 'ZeroSpeed'); simlink(S, f'{u}_kW', f'Sim_{u}_kW')


def ef_csv(S, u, sch, prof):
    unit_core(S, u, sch, prof, vsd=False, fire='stop', rated=FAN_KW['EF_CSV'])
    _csv_power(S, u)
    return {}


def ef_press(S, u, sch, prof):
    Pt, L, Mo = unit_core(S, u, sch, prof, vsd=True, fire='stop', rated=FAN_KW['EF_PRESS'])
    ai(S, Pt, f'{u}_DuctPressure', 125.0, 'Pa', prec=0, note='PT exhaust duct static pressure')
    S.param(f'{u}_DuctPressure_SP', 125.0, 'Pa', folder=Pt, prec=0, note='SOO FAN-3: 125 Pa (adj.)')
    pv = range_valid(S, L, u, f'{u}_DuctPressure', 0.0, 1500.0)
    PID(S, L, f'{u}PressPID', f'{u}_DuctPressure', f'{u}_DuctPressure_SP', f'{u}_StartCmd', 'reverse', 0.1, 1.0, 20.0, 100.0)
    const(S, 'Fan_FailSafeSpeed', 80.0, 'pct')
    fan_speed(S, u, L, Pt, f'{u}PressPID', pv, 'Fan_FailSafeSpeed', 20.0, f'{u}_StartCmd')
    const(S, 'PressHiFactor', 1.25, prec=2); const(S, 'PressLoFactor', 0.75, prec=2)
    MATH(S, L, f'{u}PressHiLim', 'Multiply', f'{u}_DuctPressure_SP', 'PressHiFactor'); MATH(S, L, f'{u}PressLoLim', 'Multiply', f'{u}_DuctPressure_SP', 'PressLoFactor')
    CMP(S, L, f'{u}PressHi', 'GreaterThan', f'{u}_DuctPressure', f'{u}PressHiLim'); CMP(S, L, f'{u}PressLo', 'LessThan', f'{u}_DuctPressure', f'{u}PressLoLim')
    OR(S, L, f'{u}PressDev', f'{u}PressHi', f'{u}PressLo')
    DLY(S, L, f'{u}Running5min', f'{u}_Status', 300000)
    AND(S, L, f'{u}PressAlmLogic', f'{u}PressDev', f'{u}Running5min', pv)
    DLY(S, L, f'{u}PressAlmDelay', f'{u}PressAlmLogic', 300000)
    S.bpoint(Mo, f'{u}_PressureAlarm', f'{u}PressAlmDelay', 'Hi/Lo', 'Normal')
    M6.COS[f'{u}_PressureAlarm'] = (True, 'Warning', f'{u} duct pressure outside setpoint +/-25 % (SOO FAN-3)')
    const(S, 'Sim_EfPressPerPct', 1.6, prec=2)
    SIM = f'{AIR}/Simulation'
    MATH(S, SIM, f'Sim_{u}_Press', 'Multiply', f'{u}_SpeedCmd', 'Sim_EfPressPerPct', f'Sim_{u}_On'); simlink(S, f'{u}_DuctPressure', f'Sim_{u}_Press')
    return {}


def ef_temp(S, u, sch, prof):
    Pt, L = _f(u, 'Points'), _f(u, 'Logic')
    ai(S, Pt, f'{u}_SpaceTemp', 38.0, 'C', note='TT space (plant / electrical room)')
    S.param(f'{u}_SpaceTemp_SP', 40.0, 'C', folder=Pt, lo=25.0, hi=50.0, note='SOO FAN-4: 40 degC (adj.)')
    CMP(S, L, f'{u}TempHighRun', 'GreaterThan', f'{u}_SpaceTemp', f'{u}_SpaceTemp_SP', note='24 h: runs whenever the room is above setpoint')
    Pt, L, Mo = unit_core(S, u, sch, prof, vsd=True, fire='stop', rated=FAN_KW['EF_TEMP'], extra_run=[f'{u}TempHighRun'])
    tv = range_valid(S, L, u, f'{u}_SpaceTemp', 0.0, 70.0)
    PID(S, L, f'{u}TempPID', f'{u}_SpaceTemp', f'{u}_SpaceTemp_SP', f'{u}_StartCmd', 'direct', 10.0, 0.5, 20.0, 100.0,
        note='space above setpoint -> faster')
    const(S, 'Fan_FailSafeSpeed', 80.0, 'pct')
    fan_speed(S, u, L, Pt, f'{u}TempPID', tv, 'Fan_FailSafeSpeed', 20.0, f'{u}_StartCmd')
    const(S, 'EfHotMargin', 5.0)
    MATH(S, L, f'{u}HotLim', 'Add', f'{u}_SpaceTemp_SP', 'EfHotMargin'); CMP(S, L, f'{u}Hot', 'GreaterThan', f'{u}_SpaceTemp', f'{u}HotLim')
    DLY(S, L, f'{u}HotDelay', f'{u}Hot', 900000)
    S.bpoint(Mo, f'{u}_SpaceTempHighAlarm', f'{u}HotDelay', 'Hot', 'Normal')
    M6.COS[f'{u}_SpaceTempHighAlarm'] = (True, 'Critical', f'{u} room temperature above setpoint + 5 K (equipment at risk)')
    ramp(S, f'Sim_{u}_Space', 'SineWave', 2400000, 5.0, 39.0, 'C', target=f'{u}_SpaceTemp')
    return {}


def ef_co(S, u, sch, prof):
    L = _f(u, 'Logic'); Pt = _f(u, 'Points')
    ai(S, Pt, f'{u}_CO', 10.0, 'ppm', prec=0, note='CO sensor (car park average)')
    S.param(f'{u}_CO_Start', 25.0, 'ppm', folder=Pt, prec=0, note='start / minimum speed at this CO')
    S.param(f'{u}_CO_Full', 50.0, 'ppm', folder=Pt, prec=0, note='100 % speed at this CO')
    S.param(f'{u}_CO_Alarm', 100.0, 'ppm', folder=Pt, prec=0, note='high CO alarm')
    covalid = range_valid(S, L, u, f'{u}_CO', 0.0, 500.0)
    HYST(S, L, f'{u}CODemand', f'{u}_CO', 15.0, 25.0, note='start above 25 ppm, stop below 15 ppm')
    NOT(S, L, f'{u}COInvalid', covalid)
    OR(S, L, f'{u}CORun', f'{u}CODemand', f'{u}COInvalid', note='sensor invalid -> run (fail-safe ventilation)')
    Pt, L, Mo = unit_core(S, u, sch, prof, vsd=True, fire='run', rated=FAN_KW['EF_CO'], extra_run=[f'{u}CORun'])
    const(S, 'CpefMinSpeed', 30.0, 'pct')
    RESET(S, L, f'{u}COReset', f'{u}_CO', f'{u}_CO_Start', f'{u}_CO_Full', 'CpefMinSpeed', 'HundredPct')
    SW(S, L, f'{u}FireSpeed', 'FireAlarmSignal', 'HundredPct', f'{u}COReset', note='fire alarm -> 100 % smoke clearance')
    const(S, 'Fan_FailSafeSpeed', 80.0, 'pct')
    OR(S, L, f'{u}SpeedValid', covalid, 'FireAlarmSignal')
    fan_speed(S, u, L, Pt, f'{u}FireSpeed', f'{u}SpeedValid', 'Fan_FailSafeSpeed', 30.0, f'{u}_StartCmd')
    CMP(S, L, f'{u}COHigh', 'GreaterThan', f'{u}_CO', f'{u}_CO_Alarm')
    DLY(S, L, f'{u}COHighDelay', f'{u}COHigh', 600000)
    S.bpoint(Mo, f'{u}_COHighAlarm', f'{u}COHighDelay', 'High CO', 'Normal')
    M6.COS[f'{u}_COHighAlarm'] = (True, 'Critical', f'{u} carbon monoxide above alarm level for 10 min')
    ramp(S, f'Sim_{u}_CO', 'Ramp', 3000000, 32.0, 35.0, 'ppm', target=f'{u}_CO')
    return {}


def lsf(S, u, sch, prof):
    Pt, L, Mo = unit_core(S, u, None, prof, vsd=True, fire='run', rated=FAN_KW['LSF'])
    ai(S, Pt, f'{u}_StairDP', 0.0, 'Pa', prec=0, note='PT stair-to-lobby differential pressure')
    S.param(f'{u}_StairDP_SP', 45.0, 'Pa', folder=Pt, prec=0, note='stair pressurisation 38-50 Pa (PROJECT fire engineer)')
    dv = range_valid(S, L, u, f'{u}_StairDP', 0.0, 300.0)
    PID(S, L, f'{u}DPPID', f'{u}_StairDP', f'{u}_StairDP_SP', f'{u}_StartCmd', 'reverse', 1.0, 10.0, 30.0, 100.0)
    fan_speed(S, u, L, Pt, f'{u}DPPID', dv, 'HundredPct', 30.0, f'{u}_StartCmd')
    const(S, 'Sim_StairDPPerPct', 0.6, prec=2)
    SIM = f'{AIR}/Simulation'
    MATH(S, SIM, f'Sim_{u}_DP', 'Multiply', f'{u}_SpeedCmd', 'Sim_StairDPPerPct', f'Sim_{u}_On'); simlink(S, f'{u}_StairDP', f'Sim_{u}_DP')
    AND(S, L, f'{u}FireNoRunLogic', 'FireAlarmSignal', f'{u}NotStatus')
    DLY(S, L, f'{u}FireNoRun', f'{u}FireNoRunLogic', prof['fan_proof'], note='fire alarm and fan not running (any cause incl. HOA)')
    S.bpoint(Mo, f'{u}_FireFailAlarm', f'{u}FireNoRun', 'NOT RUNNING', 'Normal')
    M6.COS[f'{u}_FireFailAlarm'] = (True, 'Emergency', f'{u} life-safety fan failed to run during fire alarm')
    return {}


def sef(S, u, sch, prof):
    Pt, L, Mo = unit_core(S, u, None, prof, vsd=False, fire='run', rated=FAN_KW['SEF'])
    _csv_power(S, u)
    AND(S, L, f'{u}FireNoRunLogic', 'FireAlarmSignal', f'{u}NotStatus')
    DLY(S, L, f'{u}FireNoRun', f'{u}FireNoRunLogic', prof['fan_proof'])
    S.bpoint(Mo, f'{u}_FireFailAlarm', f'{u}FireNoRun', 'NOT RUNNING', 'Normal')
    M6.COS[f'{u}_FireFailAlarm'] = (True, 'Emergency', f'{u} smoke exhaust fan failed to run during fire alarm')
    return {}


# ============================================================ build
def _path_of(self, n):
    f = self.folder_of[n]
    return ('/' if f.startswith(AIR) else '/ChillerPlant/') + f + '/' + n


M6.Station.path_of = _path_of
_hist_orig = M6.history_ext


def history_ext_v7(S, name, kind_bool, cov):
    """V6 history + storage policy: auxiliary instrumentation (volts, PF, Hz, amps, pressures, levels, feedback)
    at 5-min interval / 1 year (105 120 records) instead of 1-min / 550 000."""
    en, how, cap = _hist_orig(S, name, kind_bool, cov)
    if not cov and S.meta.get(name, {}).get('hist') == '5min':
        e = child(S.comp[name], en)
        cfg = child(e, 'historyConfig')
        child(cfg, 'capacity').set('v', '1:105120'); child(cfg, 'interval').set('v', 'false:300000')
        child(e, 'interval').set('v', '300000')
        return en, 'Interval 5 min', '1:105120'
    return en, how, cap


M6.history_ext = history_ext_v7

PX_PLANT = [('Plant', 'ALT_V7_Plant'), ('PlantDetail', 'ALT_V7_PlantDetail'), ('Optimization', 'ALT_CP_Optimization'),
            ('EnergyDashboard', 'ALT_CP_EnergyDashboard'), ('Energy', 'ALT_CP_Energy'), ('AlarmsHistory', 'ALT_CP_AlarmsHistory'),
            ('Simulation', 'ALT_CP_Simulation')]
PX_AIR = [('AirSide', 'ALT_V7_AirSide'), ('AHU01', 'ALT_V7_AHU01'), ('AHU02', 'ALT_V7_AHU02'), ('OAU01', 'ALT_V7_OAU01'),
          ('FCU', 'ALT_V7_FCU'), ('Ventilation', 'ALT_V7_Ventilation')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('groups'); ap.add_argument('out'); ap.add_argument('--regdir', default='.')
    ap.add_argument('--timing', choices=('site', 'fpt'), default='site')
    a = ap.parse_args()
    prof = M6.TIMING[a.timing]
    with zipfile.ZipFile(a.src) as z:
        assert z.testzip() is None
        root = ET.fromstring(z.read('file.xml'))
    groups = {}
    for line in open(a.groups, encoding='utf-8'):
        k, g, _ = line.rstrip('\n').split('\t'); groups[k] = g
    PF = M6.PARENT_FOLDERS
    PF['PlantControl'] = PF['PlantControl'] + ['EquipmentPools']
    PF['Simulation'] = PF['Simulation'] + ['Instruments']
    items = list(PF.items())
    PF.clear()
    for k, v in items:
        if k == 'Energy': PF['Metering'] = ['BTU', 'Power']
        PF[k] = v
    PF[AIR] = ['Common', 'Schedules'] + [u for u, *_ in AIR_UNITS] + ['Simulation']
    S = M6.Station(root)
    M6.enrich_facets(S)
    ramps, fb = M6.build(S, groups)
    M6.failsafe(S)
    M6.complete_logic(S, prof)
    headered(S, prof)
    instrumentation(S, prof)
    airside(S, prof)
    M6.enrich_facets(S)
    for n in S.comp:
        if re.search(r'_(Today|Yesterday|Month|LastMonth)$|RuntimeHours$|_kWh$|_RTh$|Volume$', n):
            S.meta.setdefault(n, {})['hist'] = '5min'
    reg_hist, reg_alarm, reg_tag = M6.instrument(S)
    M6.alarm_service(S)
    new_ext = child(S.comp['PlantEnable'], 'BooleanCov')
    for L in S.comp['HistoryActiveConverter']:
        if L.get('t') == 'b:Link' and child(L, 'sourceOrd').get('v') == 'h:1103':
            child(L, 'sourceOrd').set('v', 'h:' + new_ext.get('h'))
    child(S.st, 'stationName').set('v', STATION)
    fox = next(e for e in root.iter('p') if e.get('n') == 'FoxService')
    child(child(fox, 'foxsPort'), 'publicServerPort').set('v', FOXS_PORT)
    folders, lay = M6.build_folders_and_layout(S)
    # AirSide becomes a sibling of ChillerPlant under Config (standard library root)
    air = folders[AIR]
    S.rp.remove(air)
    kids = list(S.st)
    S.st.insert(kids.index(S.rp) + 1, air)
    for i, (vn, fn) in enumerate(PX_PLANT):
        v = ET.Element('p', {'n': 'Px_' + vn, 'f': 'o', 't': 'b:PxView'}); P(v, 'pxFile', 'b:Ord', f'file:^px/{fn}.px'); S.rp.insert(i, v)
    for i, (vn, fn) in enumerate(PX_AIR):
        v = ET.Element('p', {'n': 'Px_' + vn, 'f': 'o', 't': 'b:PxView'}); P(v, 'pxFile', 'b:Ord', f'file:^px/{fn}.px'); air.insert(i, v)
    first_sch = next(e for e in root.iter('p') if (e.get('t') or '').startswith('sch:'))
    first_sch.set('m', 'sch=schedule')
    type_fix = M6.fix_frozen_types(root)
    M6.fix_symbols(root)
    lit = [e.get('n') for e in root.iter('p') if '&#x' in (e.get('v') or '')]
    assert not lit, lit[:5]
    dup, bad_links, sib, sym = M6.validate(root)
    assert not dup and not bad_links and not sib and not sym, (list(dup)[:5], bad_links[:5], sib[:5], sym[:5])
    if os.path.exists(a.out): raise SystemExit('refusing to overwrite ' + a.out)
    with zipfile.ZipFile(a.out, 'x', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('file.xml', ET.tostring(root, encoding='utf-8', xml_declaration=True))
    sha = hashlib.sha256(open(a.out, 'rb').read()).hexdigest().upper()
    n_links = sum(1 for e in root.iter('p') if e.get('t') == 'b:Link')
    print(f'out {a.out} sha256 {sha}')
    print(f'components {len(S.comp)} folders {len(folders)} links {n_links} histories {len(reg_hist)} alarms {len(reg_alarm)} tagged {len(reg_tag)} typefix {type_fix}')
    os.makedirs(a.regdir, exist_ok=True)
    def wcsv(fn, head, rows):
        with open(os.path.join(a.regdir, fn), 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f); w.writerow(head); w.writerows(rows)
    wcsv('V7_HISTORY_REGISTER.csv', ['Point', 'Slot_Path', 'History_ID', 'Extension', 'Method', 'Capacity'], reg_hist)
    wcsv('V7_ALARM_REGISTER.csv', ['Point', 'Slot_Path', 'Alarm_Type', 'Alarm_Class', 'Condition', 'Offnormal_Text', 'Inhibit'], reg_alarm)
    wcsv('V7_TAG_REGISTER.csv', ['Point', 'Slot_Path', 'Tag', 'Value'], reg_tag)
    wcsv('V7_CHANGE_LOG.csv', ['Action', 'Folder', 'Component', 'Type_or_Slot', 'Links_or_Value', 'Note'], S.log)
    wcsv('V7_COMPONENTS.csv', ['Component', 'Folder', 'Type', 'Handle'], [(n, S.folder_of[n], el.get('t'), el.get('h')) for n, el in S.comp.items()])
    wcsv('V7_FOLDER_LAYOUT.csv', ['Folder', 'Components', 'Width_cells', 'Height_cells'], [(p, *v) for p, v in lay.items()])
    pts = [(n, S.path_of(n), el.get('t').split(':')[1], S.meta.get(n, {}).get('kind', ''), S.meta.get(n, {}).get('unit', ''),
            S.meta.get(n, {}).get('ramp', ''), next((r[5] for r in S.log if r[0] == 'ADD' and r[2] == n), ''))
           for n, el in S.comp.items() if el.get('t') in ('c:NumericWritable', 'c:BooleanWritable')]
    wcsv('V7_POINT_LIST.csv', ['Point', 'Slot_Path', 'Type', 'Kind', 'Unit', 'Simulation', 'Note'], pts)
    return S


if __name__ == '__main__':
    main()
