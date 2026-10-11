"""V6 scenario suite (offline model, review aid — NOT native Niagara FPT).

Plant feedback comes from the station's own Simulation/Feedback blocks (in10).
Faults are injected the way an engineer would on site: Override (in8) on the
field point.  Ramps are OFF for regression (fixed inputs) and ON for E09.
usage: scenarios6.py v6.bog [out.csv]
"""
import sys, os, csv, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim7 import Model6
from simstart import faithful

BASE = [(0.0, {'PlantEnable': True, 'PlantLoadPct': 20.0, 'CHWFlow': 150.0}), (1.0, {'BootQualified': True})]
FAIL = {'CH01': {'CH01RunProof': False}, 'CH02': {'CH02RunProof': False}, 'CHP01': {'CHP01RunProof': False},
        'STUCK01': {'CH01RunProof': True}}


def ft(tr, cond, after=0.0):
    for t, s in tr:
        if t >= after and cond(s): return t
    return None


def gap(tr, a, b):
    longest = cur = 0.0; prev = None
    for t, s in tr:
        if t < a or t > b: continue
        none = not (s['CH01StartSuccess'] or s['CH02StartSuccess'])
        if none and prev is not None: cur += t - prev
        elif not none: cur = 0.0
        longest = max(longest, cur); prev = t
    return round(longest, 1)


SAMPLE = ['CH01StartCmd', 'CH02StartCmd', 'CH01StartSuccess', 'CH02StartSuccess', 'CH01TimeoutLockout', 'CH02TimeoutLockout',
          'CHP01StartCmd', 'CDP01StartCmd', 'CT01StartCmd', 'CHP02StartCmd', 'Stage2Allowed', 'CH01Request', 'CH02Request',
          'CH01ValveOpenCmd', 'CH02ValveOpenCmd', 'PlantStage', 'CHW_BypassValveCmd', 'OperationMode', 'CHW_LeavingTemperatureSetpoint_ACTIVE',
          'CDS_Setpoint_ACTIVE', 'CHWDP_Setpoint_ACTIVE', 'HeartbeatDetectorStatus', 'AI_Available']


def fire(name, ms=2000):
    """Px button: invoke the OneShot 'fire' action."""
    def f(m):
        m.st[name]['rem'] = ms / 1000.0; m.out[name] = True
    return f


def sim(events, dur, fail=(), ramps=False, every=0.5, extra=(), base=True):
    m = faithful(Model6(BOG, ramps=ramps))      # start-up edges before a block runs are lost (as in Niagara)
    ev = (BASE if base else []) + list(events)
    for f in fail:
        ev.append((0.0, FAIL[f]))
    tr = m.run(dur, ev, sample=SAMPLE + list(extra), every=every)
    return m, tr


def row(cid, area, title, expect, ok, observed):
    return {'id': cid, 'area': area, 'title': title, 'expectation': expect, 'observed': observed, 'result': 'PASS' if ok else 'FINDING'}


def r(v, n=2):
    return round(v, n) if isinstance(v, float) else v


def suite():
    R = []
    o = lambda m, n: m.lv(n)
    # ======================================================= regression (V4/V5 behaviour must be kept)
    m, tr = sim([], 40)
    R.append(row('R01', 'Sequence', 'Normal CH01 start', 'CH01 cmd+success, CHP01/CDP01/CT01 on, CH02 off',
                 o(m, 'CH01StartCmd') and o(m, 'CH01StartSuccess') and o(m, 'CHP01StartCmd') and o(m, 'CT01StartCmd') and not o(m, 'CH02StartCmd'),
                 f"CH01Cmd@{ft(tr, lambda s: s['CH01StartCmd'])}s success@{ft(tr, lambda s: s['CH01StartSuccess'])}s"))
    m, tr = sim([(40.0, {'PlantEnable': False})], 60)
    a, b = ft(tr, lambda s: not s['CH01StartCmd'], 40), ft(tr, lambda s: not s['CHP01StartCmd'], 40)
    R.append(row('R02', 'Sequence', 'Normal stop, 5 s auxiliary post-run', 'CH01 off first; CHP01 off ~5 s later',
                 a is not None and b is not None and 4.5 <= b - a <= 6.0, f"CH01 off@{a}s CHP01 off@{b}s"))
    m, tr = sim([(30.0, {'PlantLoadPct': 80.0})], 70)
    R.append(row('R03', 'Staging', 'Stage up at 80 % load', 'Both chillers proven', o(m, 'CH01StartSuccess') and o(m, 'CH02StartSuccess'),
                 f"CH02 success@{ft(tr, lambda s: s['CH02StartSuccess'])}s"))
    m, tr = sim([(30.0, {'PlantLoadPct': 80.0}), (70.0, {'PlantLoadPct': 20.0, 'CHWFlow': 40.0})], 100)   # V7.6: flow falls with load (VPF hold)
    R.append(row('R04', 'Staging', 'Stage down at 20 % load', 'CH02 off, CH01 stays', o(m, 'CH01StartCmd') and not o(m, 'CH02StartCmd'),
                 f"CH02 off@{ft(tr, lambda s: not s['CH02StartCmd'], 70)}s"))
    m, tr = sim([], 60, fail=['CH01'])
    R.append(row('R05', 'Failover', 'CH01 fails to prove -> lockout -> CH02', 'CH01 lockout, CH02 proven',
                 o(m, 'CH01TimeoutLockout') and o(m, 'CH02StartSuccess') and o(m, 'CH01LockoutAlarm'),
                 f"lockout@{ft(tr, lambda s: s['CH01TimeoutLockout'])}s CH02 success@{ft(tr, lambda s: s['CH02StartSuccess'])}s alarm point={o(m, 'CH01LockoutAlarm')}"))
    m, tr = sim([(0.0, {'CHWS': 7.0, 'CHWR': 8.0}), (30.0, {'PlantLoadPct': 80.0})], 60)
    R.append(row('R18', 'Staging', 'Low delta-T inhibits stage-up', 'Stage2 not allowed at 80 % with dT 1 K',
                 not o(m, 'Stage2Allowed') and not o(m, 'CH02StartCmd'), f"Stage2Allowed={o(m, 'Stage2Allowed')} CH02Cmd={o(m, 'CH02StartCmd')}"))
    m, tr = sim([(0.0, {'RotationRequest': True}), (40.0, {'CH02Fault': True})], 90)
    R.append(row('F01', 'Failover', 'CH02 lead faults', 'CH01 takes over', o(m, 'CH01StartSuccess'), f"CH01Success={o(m, 'CH01StartSuccess')} gap={gap(tr, 40, 90)} s"))
    m, tr = sim([(40.0, {'CHP01Fault': True})], 90)
    R.append(row('F02', 'Failover', 'CHP01 faults while running', 'V7 headered: CHP02 (standby) takes over, chiller keeps running (V6: train 2)',
                 (o(m, 'CH01StartSuccess') or o(m, 'CH02StartSuccess')) and o(m, 'CHP02StartCmd') and gap(tr, 40, 90) <= 10,
                 f"CH01Success={o(m, 'CH01StartSuccess')} CHP02={o(m, 'CHP02StartCmd')} gap={gap(tr, 40, 90)} s"))
    m, tr = sim([], 90, fail=['CHP01'])
    R.append(row('F03', 'Failover', 'CHP01 never proves', 'V7 headered: CHP01 latched failed, CHP02 starts, no chiller lockout (V6: train 2)',
                 (o(m, 'CH01StartSuccess') or o(m, 'CH02StartSuccess')) and o(m, 'CHP01FailLatch') and not o(m, 'CH01TimeoutLockout'),
                 f"CHP01 failed={o(m, 'CHP01FailLatch')} CH01Lockout={o(m, 'CH01TimeoutLockout')} CH01Success={o(m, 'CH01StartSuccess')}"))
    m, tr = sim([(40.0, {'RotationRequest': True})], 100)
    R.append(row('F04', 'Rotation', 'Rotation while running', 'Make-before-break', gap(tr, 40, 100) == 0.0,
                 f"gap={gap(tr, 40, 100)} s; CH01 off@{ft(tr, lambda s: not s['CH01StartCmd'], 40)}s"))
    m, tr = sim([(40.0, {'PlantEnable': False}), (46.0, FAIL['STUCK01']), (60.0, {'PlantEnable': True})], 70)
    x = row('F05', 'Proof', 'Restart with run proof stuck ON', 'No StartSuccess without fresh proof',
            not (o(m, 'CH01StartSuccess') and o(m, 'CH01StartCmd')), f"re-cmd@{ft(tr, lambda s: s['CH01StartCmd'], 60)}s success@{ft(tr, lambda s: s['CH01StartSuccess'], 60)}s")
    if x['result'] == 'FINDING':   # known, documented in 02 §6: interlock is a PROJECT/OEM decision
        x['result'] = 'OPEN-DECISION'
        x['observed'] += '; V6 mitigation: CH01StartCmd CommandFailure alarm (proof ON while command OFF) + CH01RunProof history'
    R.append(x)
    m, tr = sim([(40.0, {'CH01RunProof': None}), (45.0, {'CH01LockoutReset': True}), (46.0, {'CH01LockoutReset': False})], 90, fail=['CH01'])
    R.append(row('F06', 'Lockout', 'Lockout reset after repair', 'CH01 returns without restart', not o(m, 'CH01TimeoutLockout'),
                 f"CH01TimeoutLockout at 90 s = {o(m, 'CH01TimeoutLockout')}"))
    m, tr = sim([(30.0, {'PlantLoadPct': 80.0}), (80.0, {'CHWS': 7.0, 'CHWR': 8.0})], 120)
    R.append(row('F07', 'Staging', 'Low dT while stage 2 runs', 'Stage 2 kept', o(m, 'CH02StartCmd') and o(m, 'CH01StartCmd'), f"CH02Cmd={o(m, 'CH02StartCmd')}"))
    m, tr = sim([(0.0, {'CH01Fault': True, 'CH02Fault': True})], 40)
    R.append(row('V01', 'Failover', 'Both trains unavailable', 'No chiller commanded', not o(m, 'CH01StartCmd') and not o(m, 'CH02StartCmd'), f"CH01Cmd={o(m, 'CH01StartCmd')} CH02Cmd={o(m, 'CH02StartCmd')}"))
    m, tr = sim([(30.0, {'PlantLoadPct': 80.0})], 80, fail=['CH02'])
    R.append(row('V02', 'Failover', 'Lag CH02 fails in stage 2', 'CH01 keeps running; CH02 lockout',
                 o(m, 'CH01StartSuccess') and o(m, 'CH02TimeoutLockout') and gap(tr, 10, 80) == 0.0, f"gap={gap(tr, 10, 80)} s"))
    m, tr = sim([(0.0, {'CH01LockoutReset': True})], 60, fail=['CH01'])
    R.append(row('V03', 'Lockout', 'Reset held ON', 'Held reset must not mask lockout', o(m, 'CH01TimeoutLockout'), f"lockout={o(m, 'CH01TimeoutLockout')}"))
    m, tr = sim([(30.0, {'PlantLoadPct': 80.0}), (70.0, {'CHWS': 7.0, 'CHWR': 8.0}), (90.0, {'PlantLoadPct': 20.0, 'CHWFlow': 40.0})], 120)
    R.append(row('V04', 'Staging', 'Low dT in stage 2 then load falls', 'Normal stage-down', o(m, 'CH01StartCmd') and not o(m, 'CH02StartCmd'), f"CH02 off@{ft(tr, lambda s: not s['CH02StartCmd'], 90)}s"))
    m, tr = sim([(40.0, {'RotationRequest': True}), (90.0, {'RotationRequest': False})], 140)
    R.append(row('V05', 'Rotation', 'Rotate CH02 then back', 'Make-before-break both ways', gap(tr, 40, 140) == 0.0 and o(m, 'CH01StartSuccess') and not o(m, 'CH02StartCmd'), f"gap={gap(tr, 40, 140)} s"))
    m, tr = sim([(0.0, {'CH02Available': False}), (40.0, {'RotationRequest': True})], 80)
    R.append(row('V06', 'Rotation', 'Rotation while CH02 unavailable', 'CH01 stays lead', o(m, 'CH01StartSuccess') and gap(tr, 10, 80) == 0.0, f"gap={gap(tr, 10, 80)} s"))

    # ======================================================= V6 energy / new features
    # E01 CT approach control from outdoor air wet-bulb
    res = []
    for T, RH, exp in ((33.0, 60.0, None), (25.0, 40.0, 24.0), (40.0, 95.0, 32.0)):
        m, tr = sim([(0.0, {'OA_Temperature': T, 'OA_Humidity': RH})], 20)
        wb = o(m, 'OA_WetBulb'); sp = o(m, 'CDS_Setpoint_ACTIVE')
        want = exp if exp is not None else wb + 3.0
        res.append((T, RH, r(wb), r(sp), abs(sp - want) < 0.05 and abs(o(m, 'Opt_CdwSetpoint') - sp) < 1e-6))
    R.append(row('E01', 'OA->CT', 'CDW setpoint = OA wet-bulb + approach, clamped 24..32 °C',
                 'SP = WB+3 inside limits; 24 at cool/dry; 32 at hot/humid', all(x[-1] for x in res),
                 '; '.join(f"OA {T}°C/{RH}% -> WB {wb} SP {sp}" for T, RH, wb, sp, _ in res)))
    # E01b tower fan follows the SP (direct acting): CDS above SP -> more fan
    m, tr = sim([(0.0, {'OA_Temperature': 30.0, 'OA_Humidity': 60.0, 'CDS': 25.0}), (120.0, {'CDS': 33.0})], 400, every=5.0, extra=['CT01SpeedCmd', 'CDS'])
    s1 = [s['CT01SpeedCmd'] for t, s in tr if 100 <= t <= 120]; s2 = o(m, 'CT01SpeedCmd')
    R.append(row('E01b', 'OA->CT', 'Tower fan PID direction and minimum speed', 'CDS 25 °C below SP -> 20 % minimum; CDS 33 °C above SP -> fan speeds up (direct acting)',
                 min(s1) >= 20.0 - 1e-6 and max(s1) <= 21 and s2 > 60, f"SP={r(o(m, 'CDS_Setpoint_ACTIVE'))}; CT01 speed @CDS 25 = {r(max(s1), 1)} %, @CDS 33 (280 s later) = {r(s2, 1)} %"))
    # E02 plant reset (GPC36 style: DP first, then CHWST)
    res = []
    for load in (10.0, 25.0, 50.0, 75.0, 100.0):
        m, tr = sim([(0.0, {'PlantLoadPct': load})], 10, base=False)
        res.append((load, r(o(m, 'CHWDP_Setpoint_ACTIVE'), 1), r(o(m, 'CHW_LeavingTemperatureSetpoint_ACTIVE'), 2)))
    exp = {l: (60.0 + 90.0 * min(l, 50.0) / 50.0, 10.0 - 3.0 * max(l - 50.0, 0.0) / 50.0) for l in (10.0, 25.0, 50.0, 75.0, 100.0)}
    ok = all(abs(dp - exp[l][0]) < 0.5 and abs(tw - exp[l][1]) < 0.05 for l, dp, tw in res)
    R.append(row('E02', 'Reset', 'CHW DP / CHWST reset vs plant load', 'DP 60->150 kPa for 0-50 %, CHWST 10->7 °C for 50-100 %', ok,
                 '; '.join(f"{int(l)}% -> DP {dp} CHWST {tw}" for l, dp, tw in res)))
    m, tr = sim([(0.0, {'PlantLoadPct': 25.0, 'OptimizationEnable': False})], 10, base=False)
    R.append(row('E02b', 'Reset', 'Optimisation disabled -> fixed LOCAL setpoints', 'ACTIVE = LOCAL values',
                 abs(o(m, 'CHW_LeavingTemperatureSetpoint_ACTIVE') - o(m, 'CHW_LeavingTemperatureSetpoint_LOCAL')) < 1e-6 and abs(o(m, 'CHWDP_Setpoint_ACTIVE') - o(m, 'CHWDPSetpoint')) < 1e-6,
                 f"CHWST {o(m, 'CHW_LeavingTemperatureSetpoint_ACTIVE')} DP {o(m, 'CHWDP_Setpoint_ACTIVE')} CDS {o(m, 'CDS_Setpoint_ACTIVE')}"))
    # E03 OA sensor failure -> fallback wet-bulb + alarm point
    res = []
    for ev in ({'OA_SensorFault': True}, {'OA_Temperature': 80.0}, {'OA_Humidity': 0.0}):
        m, tr = sim([(0.0, dict(ev, **({} if 'OA_Humidity' in ev else {'OA_Humidity': 60.0})))], 10)
        res.append((list(ev.items())[0], o(m, 'OA_Valid'), r(o(m, 'OA_WetBulb')), r(o(m, 'CDS_Setpoint_ACTIVE')), o(m, 'OA_SensorInvalidAlarm')))
    R.append(row('E03', 'OA->CT', 'OA sensor fault / out of range', 'OA_Valid false, WB = default 27 °C, CDW SP 30 °C, alarm point true',
                 all((not v) and wb == 27.0 and sp == 30.0 and al for _, v, wb, sp, al in res),
                 '; '.join(f"{k}={x}: valid={v} WB={wb} SP={sp} alarm={al}" for (k, x), v, wb, sp, al in res)))
    # E04 minimum-flow bypass
    ev_pt = ['CHW_EvapFlowTotal'] if 'CHW_EvapFlowTotal' in Model6(BOG, ramps=False).C else []
    m, tr = sim([(0.0, {'CHWFlow': 150.0}), (60.0, {'CHWFlow': 40.0}), (400.0, {'CHWFlow': 150.0})], 700, every=5.0,
                extra=['CHWFlow', 'CHW_MinFlowSetpoint', 'CHW_BypassValveFeedback', 'CHW_BypassValvePositionMismatch'] + ev_pt)
    at = lambda T, k: next(s[k] for t, s in tr if t >= T)
    # open-loop emulation (<= V7.3): PID winds > 20 %;  closed-loop (V7.4): valve opens until evaporator flow >= min flow
    opened = at(395, 'CHW_BypassValveCmd') > 20 or (bool(ev_pt) and at(395, 'CHW_BypassValveCmd') > 5 and at(395, 'CHW_EvapFlowTotal') >= at(395, 'CHW_MinFlowSetpoint'))
    ok = at(55, 'CHW_BypassValveCmd') == 0.0 and opened and at(695, 'CHW_BypassValveCmd') < 1.0 and at(395, 'CHW_MinFlowSetpoint') == 60.0
    R.append(row('E04', 'MinFlow', 'Bypass valve holds chiller minimum flow', 'Flow 150 -> closed; flow 40 < min 60 -> opens (reverse PID, rate-limited); flow back -> closes',
                 ok, f"SP={at(395, 'CHW_MinFlowSetpoint')} m3/h" + (f" evap flow @395s={r(at(395, 'CHW_EvapFlowTotal'), 1)}" if ev_pt else '') + f"; valve @55s={r(at(55, 'CHW_BypassValveCmd'), 1)} @395s={r(at(395, 'CHW_BypassValveCmd'), 1)} @695s={r(at(695, 'CHW_BypassValveCmd'), 1)} %"))
    m, tr = sim([(30.0, {'PlantLoadPct': 80.0}), (200.0, {'CHWFlow': 90.0})], 500, every=5.0, extra=['CHW_MinFlowSetpoint'])
    R.append(row('E04b', 'MinFlow', 'Min-flow SP follows open chiller valves', 'Stage 2 -> SP 120 m3/h; flow 90 -> bypass opens',
                 at(190, 'CHW_MinFlowSetpoint') == 120.0 and o(m, 'CHW_BypassValveCmd') > 20, f"SP stage2={at(190, 'CHW_MinFlowSetpoint')} valve={r(o(m, 'CHW_BypassValveCmd'), 1)} %"))
    m, tr = sim([(0.0, {'CHWFlow': 30.0, 'CHW_BypassValveFeedback': 0.0})], 400, every=5.0, extra=['CHW_BypassValvePositionMismatch'])
    t_al = ft(tr, lambda s: s['CHW_BypassValvePositionMismatch'])
    R.append(row('E04c', 'MinFlow', 'Bypass command/feedback mismatch alarm', 'Feedback stuck at 0 % while cmd > 10 % for 120 s -> alarm point',
                 t_al is not None, f"mismatch alarm point true @{t_al}s"))
    # E05 heartbeat + mode control
    m, tr = sim([(0.0, {'ModeCmd_UI': True})], 1200, every=10.0)
    t_ai = ft(tr, lambda s: s['OperationMode'])
    ai_sp = o(m, 'CHW_LeavingTemperatureSetpoint_AI')
    ok1 = t_ai is not None and abs(o(m, 'CHW_LeavingTemperatureSetpoint_ACTIVE') - ai_sp) < 1e-6
    m2, tr2 = sim([(0.0, {'ModeCmd_UI': True}), (900.0, {'CHW_LeavingTemperatureSetpoint_AI': 15.0})], 960, every=10.0)
    ok2 = not o(m2, 'OperationMode') and o(m2, 'AI_Available') is False and o(m2, 'CHW_LeavingTemperatureSetpoint_ACTIVE') <= 12.0
    m3, tr3 = sim([(0.0, {'ModeCmd_UI': True}), (900.0, {'Sim_AiHeartbeatEnable': False})], 2700, every=10.0, extra=['HeartbeatPreDisconnect'])
    t_pre = ft(tr3, lambda s: s['HeartbeatPreDisconnect'], 900); t_loc = ft(tr3, lambda s: not s['OperationMode'], 900)
    m4, tr4 = sim([(0.0, {'ModeCmd_UI': True}), (900.0, {'ModeCmd_UI': False})], 920, every=5.0)
    t_usr = ft(tr4, lambda s: not s['OperationMode'], 900)
    R.append(row('E05', 'Mode/AI', 'AI mode via heartbeat, range protection, fallback to Local',
                 'AI after 2 beats; AI SP out of range -> Local; heartbeat lost -> PreDisconnect 6 min, Local at 12 min; user Local wins immediately',
                 ok1 and ok2 and t_pre is not None and t_loc is not None and 700 <= t_loc - 900 <= 1100 and t_usr is not None and t_usr - 900 <= 5,
                 f"AI@{t_ai}s ACTIVE=AI {r(ai_sp)}; AI SP 15 °C -> mode={'AI' if o(m2, 'OperationMode') else 'Local'} alarm AiRequestedButLocal={o(m2, 'AiRequestedButLocalAlarm')}; "
                 f"beat stop @900 -> PreDisconnect @{t_pre}s Local @{t_loc}s; user Local @{t_usr}s"))
    # E06 failsafe stage-up on CHWS deviation
    m, tr = sim([(0.0, {'PlantLoadPct': 40.0, 'CHWR': 17.0}), (60.0, {'CHWS': 12.0})], 800, every=5.0)
    t2 = ft(tr, lambda s: s['CH02StartCmd'])
    R.append(row('E06', 'Staging', 'Failsafe stage-up: CHWS > SP + 1.5 K for 10 min', 'CH02 starts ~600 s after deviation even at 40 % load',
                 t2 is not None and 640 <= t2 <= 700, f"ACTIVE SP={o(m, 'CHW_LeavingTemperatureSetpoint_ACTIVE')} CHWS=12 -> CH02 cmd @{t2}s"))
    # E07 KPIs
    m, tr = sim([(0.0, {'PlantLoadPct': 60.0, 'CH01LoadPct': 60.0, 'CHWS': 7.0, 'CHWR': 12.0, 'CHWFlow': 150.0})], 600, every=10.0)
    pk = o(m, 'Plant_kW'); aux = o(m, 'Aux_kW'); ql = o(m, 'CoolingLoad_kW'); rt = o(m, 'CoolingLoad_RT')
    ok = (abs(ql - 150 * 5 * 1.1628) < 0.1 and abs(rt - ql / 3.5169) < 0.1 and abs(o(m, 'Plant_kW_per_RT') - pk / rt) < 1e-3
          and abs(o(m, 'Plant_COP') - ql / pk) < 1e-3 and abs(pk - aux - o(m, 'CH01_kW') - o(m, 'CH02_kW')) < 1e-6)
    R.append(row('E07', 'Energy', 'Cooling load, kW/RT, COP, kWh totalisers', 'Q = flow x dT x 1.163; kW/RT = kW/RT; COP = Q/kW; kWh accumulates',
                 ok and o(m, 'Plant_kWh') > 0, f"Q={r(ql, 1)} kW ({r(rt, 1)} RT) plant={r(pk, 1)} kW (aux {r(aux, 1)}) kW/RT={r(o(m, 'Plant_kW_per_RT'), 3)} COP={r(o(m, 'Plant_COP'), 2)} kWh(10 min)={r(o(m, 'Plant_kWh'), 2)}"))
    # E08 runtime-based rotation
    def preset(mm):
        mm.extv[('Obs_CH01RunProofSelected', 'Runtime', 'elapsedActiveTimeNumeric')] = 25 * 3600 * 1000.0
    m, tr = sim([(0.0, {'RotationMode_Runtime': True}), (60.0, preset)], 160, every=0.5, extra=['CH01_RuntimeHours'])
    R.append(row('E08', 'Rotation', 'Runtime equalisation (CH01 24 h ahead -> CH02 lead)', 'Make-before-break transfer to CH02',
                 o(m, 'CH02StartSuccess') and not o(m, 'CH01StartCmd') and gap(tr, 60, 160) == 0.0,
                 f"CH01 runtime {r(o(m, 'CH01_RuntimeHours'), 1)} h; CH02 success@{ft(tr, lambda s: s['CH02StartSuccess'], 60)}s CH01 off@{ft(tr, lambda s: not s['CH01StartCmd'], 60)}s gap={gap(tr, 60, 160)} s"))
    # E10 alarm logic
    m, tr = sim([(0.0, {'CH01RunProof': False, 'CH02RunProof': False})], 1000, every=10.0, extra=['PlantStartStopMismatch'])
    t_m = ft(tr, lambda s: s['PlantStartStopMismatch'])
    R.append(row('E10a', 'Alarm', 'Plant run request but no chiller proven', 'PlantStartStopMismatch after 15 min', t_m is not None and 895 <= t_m <= 920, f"alarm point @{t_m}s"))
    m, tr = sim([(0.0, {'CHWFlow': 150.0}), (100.0, {'CHWFlow': 20.0})], 400, every=5.0, extra=['CHW_FlowLowAlarm'])
    t_f = ft(tr, lambda s: s['CHW_FlowLowAlarm'])
    R.append(row('E10b', 'Alarm', 'CHW flow below 50 % of chiller minimum while running', 'CHW_FlowLowAlarm after delay', t_f is not None, f"alarm point @{t_f}s (LowFlowRatio x SP = {r(o(m, 'LowFlowLimit'), 1)} m3/h)"))
    m, tr = sim([(0.0, {'CHWS': 7.0, 'CHWR': 8.0})], 3000, every=30.0, extra=['LowDeltaTAlarm', 'CHWST_NotTrackingAlarm'])
    t_d = ft(tr, lambda s: s['LowDeltaTAlarm'])
    R.append(row('E10c', 'Alarm', 'Low delta-T alarm: 30 min start-up inhibit + 15 min delay', 'No alarm before 45 min; alarm after', t_d is not None and t_d >= 2700, f"LowDeltaTAlarm @{t_d}s"))
    m, tr = sim([(0.0, {'OA_Temperature': 30.0, 'OA_Humidity': 60.0, 'CDS': 33.0})], 3300, every=30.0, extra=['CDS_NotTrackingAlarm'])
    t_c = ft(tr, lambda s: s['CDS_NotTrackingAlarm'])
    R.append(row('E10d', 'Alarm', 'Tower cannot hold CDW setpoint (CDS > SP + 2 K)', 'Alarm after 30 min inhibit + 20 min delay', t_c is not None and t_c >= 3000,
                 f"SP={r(o(m, 'CDS_Setpoint_ACTIVE'))} CDS=33 -> CDS_NotTrackingAlarm @{t_c}s (fans {r(o(m, 'CT01SpeedCmd'), 0)} %)"))
    # ======================================================= V6.2 fail-safe ("plant must not go dark")
    m, tr = sim([(10.0, {'BootQualified': True}), (15.0, {'PlantEnable': True, 'PlantLoadPct': 20.0, 'CHWFlow': 150.0})], 120, base=False)
    R.append(row('G01', 'FailSafe', 'Fresh station start (real-station bug 28 Sep: both CH lockout)', 'QUALIFY + ON -> CH01 proven, no lockout',
                 o(m, 'CH01StartSuccess') and not o(m, 'CH01TimeoutLockout') and not o(m, 'CH02TimeoutLockout'),
                 f"CH01 success@{ft(tr, lambda s: s['CH01StartSuccess'])}s lockout CH01={o(m, 'CH01TimeoutLockout')} CH02={o(m, 'CH02TimeoutLockout')} (V6.1 with start-up-faithful latches: both locked out @~23 s)"))
    m, tr = sim([(0.0, {'PlantEnable': True, 'PlantLoadPct': 20.0, 'CHWFlow': 150.0})], 200, base=False, every=1.0)
    t_s = ft(tr, lambda s: s['CH01StartSuccess'])
    R.append(row('G02', 'FailSafe', 'Station restart, nobody presses QUALIFY', 'Auto-qualify after 120 s, plant restarts by itself',
                 t_s is not None and 120 <= t_s <= 140, f"CH01 success@{t_s}s without operator"))
    m, tr = sim([], 260, fail=['CH01'], every=1.0, extra=['CH01_AutoRetryCount', 'CH01LockoutAlarm'])
    t_l = ft(tr, lambda s: s['CH01TimeoutLockout']); t_r = ft(tr, lambda s: not s['CH01TimeoutLockout'], (t_l or 0) + 1)
    R.append(row('G03', 'FailSafe', 'CH01 proof fails once -> CH02 carries plant -> automatic lockout reset', 'Lockout, CH02 runs, auto-reset after 180 s, retry counted',
                 t_l is not None and t_r is not None and 180 <= t_r - t_l <= 186 and o(m, 'CH02StartSuccess') and o(m, 'CH01_AutoRetryCount') == 1.0,
                 f"lockout@{t_l}s auto-reset@{t_r}s count={o(m, 'CH01_AutoRetryCount')} CH02 running={o(m, 'CH02StartSuccess')} no-chiller gap={gap(tr, 10, 260)} s"))
    ev = [(900.0, {'CH01RunProof': None, 'CH02RunProof': None}), (905.0, fire('PlantAlarmResetFire'))]
    m, tr = sim(ev, 1000, fail=['CH01', 'CH02'], every=5.0, extra=['CH01HardLockoutAlarm', 'CH02HardLockoutAlarm', 'AllChillersUnavailableAlarm', 'CH01_AutoRetryCount'])
    at = lambda T, k: next(s[k] for t, s in tr if t >= T)
    ok = (at(60, 'AllChillersUnavailableAlarm') and at(895, 'CH01HardLockoutAlarm') and at(895, 'CH02HardLockoutAlarm') and at(895, 'CH01_AutoRetryCount') == 3.0
          and o(m, 'CH01StartSuccess') and not o(m, 'CH01HardLockoutAlarm') and not o(m, 'AllChillersUnavailableAlarm') and o(m, 'CH01_AutoRetryCount') == 0.0)
    R.append(row('G04', 'FailSafe', 'Both chillers fail repeatedly, then repair + RESET PROGRAM ALARMS', 'Emergency alarm, 3 auto-retries each, hard lockout; one RESET restores plant',
                 ok, f"AllUnavailable@{ft(tr, lambda s: s['AllChillersUnavailableAlarm'])}s hard lockout@{ft(tr, lambda s: s['CH01HardLockoutAlarm'])}s retries={at(895, 'CH01_AutoRetryCount')}; after RESET: CH01 success@{ft(tr, lambda s: s['CH01StartSuccess'], 905)}s"))
    m, tr = sim([(0.0, {'CH_AutoRetryEnable': False}), (60.0, {'CH01RunProof': None}), (65.0, fire('CH01ResetFire'))], 90, fail=['CH01'])
    R.append(row('G05', 'Reset', 'Chiller RESET button (Px fire action)', 'Lockout cleared immediately after repair',
                 not o(m, 'CH01TimeoutLockout'), f"CH01 lockout before={any(s['CH01TimeoutLockout'] for t, s in tr if 20 < t < 64)} after RESET={o(m, 'CH01TimeoutLockout')}"))
    res = []
    for label, ev, chk in (('DP sensor 999 kPa', {'CHWDP': 999.0}, lambda m: m.out['CHP01SpeedCmd'] == 80.0 and m.out['CHWDP_SensorInvalidAlarm']),
                           ('CDS sensor unhealthy', {'CDSSensorHealthy': False}, lambda m: m.out['CT01SpeedCmd'] == 80.0 and m.out['CDS_SensorInvalidAlarm']),
                           ('CHWS sensor 99 °C', {'CHWS': 99.0}, lambda m: m.out['CHWS_SensorInvalidAlarm']),
                           ('CHW flow -5 m3/h', {'CHWFlow': -5.0}, lambda m: m.out['CHW_BypassValveCmd'] == 20.0 and m.out['CHWFlow_SensorInvalidAlarm']),
                           ('Comms fault', {'CommunicationHealthy': False}, lambda m: True)):
        m, tr = sim([(0.0, {'CHWDP': 120.0, 'CDS': 30.0}), (60.0, ev)], 120)
        res.append((label, bool(o(m, 'CH01StartSuccess') and o(m, 'PlantRunRequest') and chk(m)),
                    f"CHP01 {r(o(m, 'CHP01SpeedCmd'), 0)}% CT01 {r(o(m, 'CT01SpeedCmd'), 0)}% byp {r(o(m, 'CHW_BypassValveCmd'), 0)}%"))
    R.append(row('G06', 'FailSafe', 'Sensor / comms failure while running', 'Plant keeps running; failed loop goes to fail-safe output; alarm point set (V4/V5 stopped the plant)',
                 all(x[1] for x in res), '; '.join(f"{l}: {'running' if ok else 'FAIL'} ({d})" for l, ok, d in res)))
    # E09 all ramps on for 2 h: stability, coverage, no NaN
    m = Model6(BOG, ramps=True)
    ramped = [n for n in m.C if any(k == 'in10' and v[0][0] and m.typ(v[0][0]) in ('Ramp', 'SineWave', 'Counter') for k, v in m.inc[n].items())]
    num_out = [n for n in m.C if m.typ(n) == 'NumericWritable']
    tr = m.run(7200, [(0.0, {'PlantEnable': True}), (1.0, {'BootQualified': True})], sample=ramped + num_out + ['CH01StartCmd', 'CH02StartCmd'], every=10.0)
    span = {n: (min(s[n] for _, s in tr), max(s[n] for _, s in tr)) for n in ramped}
    nan = [n for n in num_out if any(isinstance(s[n], float) and (math.isnan(s[n]) or math.isinf(s[n])) for _, s in tr)]
    st2 = sum(1 for _, s in tr if s['CH02StartCmd'])
    R.append(row('E09', 'Simulation', f'2 h run with all {len(ramped)} simulated inputs ramping', 'Every ramped input sweeps its range; no NaN/Inf on numeric points; stage 2 exercised',
                 not nan and all(hi - lo > 0 for lo, hi in span.values()) and st2 > 0,
                 f"NaN/Inf points={nan or 'none'}; stage-2 samples={st2}; " + ', '.join(f"{n} {r(lo, 1)}..{r(hi, 1)}" for n, (lo, hi) in span.items())))
    return R


if __name__ == '__main__':
    BOG = sys.argv[1]
    rows = suite()
    for x in rows:
        print(f"{x['id']:5} {x['result']:8} {x['title']}\n       {x['observed']}")
    print('PASS', sum(x['result'] == 'PASS' for x in rows), '/', len(rows), ' OPEN-DECISION', sum(x['result'] == 'OPEN-DECISION' for x in rows))
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.DictWriter(f, fieldnames=['id', 'area', 'title', 'expectation', 'observed', 'result'])
            w.writeheader(); w.writerows(rows)
