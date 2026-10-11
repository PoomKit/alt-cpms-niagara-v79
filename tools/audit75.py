"""Static completeness audit of the V7 BOG (ChillerPlant + AirSide) (structure + Niagara services + control chains).
usage: audit75.py v75.bog out.csv  (V7.5: fail-safe path check ignores the plant emulation)
"""
import sys, os, csv, zipfile, re
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_symbols import check as check_symbols

bog, out = sys.argv[1], sys.argv[2]
root = ET.fromstring(zipfile.ZipFile(bog).read('file.xml'))
child = lambda el, n: next((c for c in el if c.tag == 'p' and c.get('n') == n), None)
cp = next(e for e in root.iter('p') if e.get('n') == 'ChillerPlant')

comp, path, ext_of = {}, {}, defaultdict(list)
def walk(el, pre):
    for c in el:
        if c.tag != 'p' or not c.get('t'): continue
        if c.get('t') == 'b:Folder': walk(c, pre + '/' + c.get('n')); continue
        if c.get('t') in ('b:WsAnnotation', 'b:PxView'): continue
        comp[c.get('n')] = c; path[c.get('n')] = pre + '/' + c.get('n')
        for x in c:
            if x.get('h') and x.get('t') and x.get('t') != 'b:Link':
                ext_of[c.get('n')].append(x)
walk(cp, '/ChillerPlant')
air = next(e for e in root.iter('p') if e.get('n') == 'AirSide' and e.get('t') == 'b:Folder')
walk(air, '/AirSide')
regdir = os.environ.get('REGDIR') or os.path.join(os.path.dirname(os.path.abspath(bog)), 'reg')
KIND = {r['Point']: r['Kind'] for r in csv.DictReader(open(os.path.join(regdir, 'V7_POINT_LIST.csv'), encoding='utf-8-sig'))}
h2n = {}
for n, c in comp.items():
    h2n[c.get('h')] = n
    for x in ext_of[n]:
        h2n[x.get('h')] = n
        for y in x.iter('p'):
            if y.get('h'): h2n[y.get('h')] = n
all_h = [e.get('h') for e in root.iter('p') if e.get('h')]
up = defaultdict(set)
broken = []
for n, c in comp.items():
    for L in c.iter('p'):
        if L.get('t') == 'b:Link':
            s = child(L, 'sourceOrd').get('v')[2:]
            if s in h2n: up[n].add(h2n[s])
            elif s not in all_h: broken.append((n, s))
typ = {n: c.get('t').split(':')[1] for n, c in comp.items()}

def upstream(n):
    seen, st = set(), [n]
    while st:
        x = st.pop()
        for y in up[x]:
            if y not in seen: seen.add(y); st.append(y)
    return seen

rows = []
def add(area, check, ok, evidence):
    rows.append({'Area': area, 'Check': check, 'Result': 'PASS' if ok else 'GAP', 'Evidence': evidence})

# ---------------- structure
dup_h = [h for h, k in Counter(all_h).items() if k > 1]
add('Structure', 'Unique handles', not dup_h, f'{len(all_h)} handles, duplicates={dup_h[:5]}')
add('Structure', 'All links resolve', not broken, f'broken={broken[:5]}')
add('Structure', 'Module symbols declared before use', not check_symbols(root), 'check_symbols() = []')
folders = [e for e in cp.iter('p') if e.get('t') == 'b:Folder']
add('Structure', 'Logic split into function/equipment folders', len(folders) >= 40, f'{len(folders)} folders, {len(comp)} components')
loose = [c.get('n') for c in cp if c.tag == 'p' and c.get('t') not in ('b:Folder', 'b:WsAnnotation', None)]
add('Structure', 'AirSide library root is a sibling of ChillerPlant', air is not None and any(k.startswith('/AirSide/AHU01/') for k in path.values()), f"{sum(1 for v in path.values() if v.startswith('/AirSide/'))} air-side components")
add('Structure', 'No loose logic at ChillerPlant root (only notes + Px views)', all(n == 'EngineeringNotes' or n.startswith('Px_') for n in loose), f'root slots={loose}')

from collections import Counter as _C
dup_ext = [(n, t) for n in comp for t, k in _C(x.get('t') for x in ext_of[n] if x.get('t') not in ('b:Link',) and not x.get('t', '').startswith('b:')).items() if k > 1]
add('Structure', 'At most one extension of each type per point (BPointExtension.isSiblingLegal)', not dup_ext, f'duplicates={dup_ext[:6]}')

# ---------------- histories
hist = {n: x for n in comp for x in ext_of[n] if x.get('t', '').endswith('HistoryExt')}
ids = [child(child(x, 'historyConfig'), 'id').get('v') for x in hist.values()]
add('History', 'History IDs unique', len(ids) == len(set(ids)), f'{len(ids)} histories')
bad_src = [n for n, x in hist.items() if child(child(x, 'historyConfig'), 'source').get('v') != f'station:|slot:{path[n]}/{x.get("n")}']
add('History', 'History source ORD = real slot path', not bad_src, f'mismatch={bad_src[:5]}')
writ = [n for n in comp if typ[n] in ('NumericWritable', 'BooleanWritable')]
nohist = [n for n in writ if n not in hist]
CONST = {n for n in writ if path[n].startswith('/ChillerPlant/Parameters/') or n.startswith(('Sim_', 'Gfx_'))}   # Gfx_ = graphics-only helpers (V7.4)
add('History', 'Every point has a history (except fixed constants / validity limits in Parameters)', set(nohist) <= CONST,
    f'{len(hist)}/{len(writ)} points trended; not trended outside Parameters: {[n for n in nohist if n not in CONST][:8]}')
outs = [n for n in writ if re.search(r'(StartCmd|SpeedCmd|ValveOpenCmd|BypassValveCmd|_ACTIVE|Opt_|_kW$|kW_per_RT|COP|_kWh|RuntimeHours)', n) and not n.startswith('Obs') and n not in CONST]
add('History', 'All outputs / setpoints / KPIs trended', all(n in hist for n in outs), f'{sum(n in hist for n in outs)}/{len(outs)} output points trended; missing={[n for n in outs if n not in hist]}')
pv_int = [n for n in ('CHWS', 'CHWR', 'CHWFlow', 'CHWDP', 'CDS', 'CDR', 'OA_Temperature', 'OA_Humidity', 'OA_WetBulb', 'Plant_kW', 'Plant_kW_per_RT')
          if hist.get(n) is not None and 'Interval' in hist[n].get('t')]
add('History', 'Process values on 1-min interval (MELCO 550000)', len(pv_int) == 11, ', '.join(pv_int))

# ---------------- alarms
aclasses = {c.get('n') for e in root.iter('p') if e.get('n') == 'AlarmService' for c in e if c.get('t') == 'a:AlarmClass'}
alarms = {(n, x.get('n')): x for n in comp for x in ext_of[n] if x.get('t') == 'a:AlarmSourceExt'}
bad_cls = [k for k, x in alarms.items() if child(x, 'alarmClass').get('v') not in aclasses]
add('Alarm', 'AlarmService + classes Emergency/Critical/Warning/Info + console recipient', aclasses >= {'Emergency', 'Critical', 'Warning', 'Info'}, f'classes={sorted(aclasses)}')
add('Alarm', 'Every alarm extension uses a defined class', not bad_cls, f'{len(alarms)} alarm extensions')
cmds = [n for n in writ if re.search(r'(StartCmd|ValveOpenCmd)$', n) and not n.startswith('Obs') and not path[n].startswith('/AirSide/')]
cf = [n for n in cmds if any(x.get('t') == 'a:AlarmSourceExt' and child(x, 'offnormalAlgorithm').get('t') == 'a:BooleanCommandFailureAlgorithm' for x in ext_of[n])]
add('Alarm', 'Every plant start/valve command has CommandFailure (air side: fan-fail logic, see Air chains)', len(cf) == len(cmds), f'{len(cf)}/{len(cmds)}')
faults = [n for n in writ if n.endswith('Fault') and not n.startswith('OA')]
add('Alarm', 'Every equipment fault input alarms (COS)', all(any(x.get('t') == 'a:AlarmSourceExt' for x in ext_of[n]) for n in faults), f'{len(faults)} fault inputs')
inh = {k[0] for k, x in alarms.items() if child(x, 'offnormalAlgorithm').get('t') == 'a:OutOfRangeAlgorithm'
       and any(L.get('t') == 'b:Link' and child(L, 'targetSlotName').get('v') == 'alarmInhibit' for L in x)}
proc = ['CHWS', 'CHWR', 'CHWDP', 'CDS', 'CDR', 'Plant_kW_per_RT', 'CH01_ChwSupplyTemp', 'CH02_ChwSupplyTemp', 'CHW_SupplyHeaderPressure']
add('Alarm', 'Process (out-of-range) alarms inhibited until plant ran 30 min (safety OOR: expansion tank, voltage stay live)', all(p in inh for p in proc), f'{len(inh)} inhibited: {sorted(inh)}')

# ---------------- tags
tagged = [n for n in comp if child(comp[n], 'melco$3apointNameString') is not None]
hs = [n for n in comp if any(c.get('n', '').startswith('hs$3a') for c in comp[n])]
add('Tag', 'MELCO pointNameString on BMS point list', len(tagged) >= 60, f'{len(tagged)} points; STORE/FLOOR/COORD placeholders (ALTREF/1F/NA)')
add('Tag', 'Haystack markers for search / analytics', len(hs) >= 100, f'{len(hs)} points with hs: markers')

# ---------------- simulation
ai = [n for n in writ if KIND.get(n) == 'ai'] + ['CHWS', 'CHWR', 'CHWFlow', 'CHWDP', 'CDS', 'CDR', 'CH01LoadPct', 'CH02LoadPct', 'HeartbeatTimestampSetpoint']
def in10(n):
    for L in comp[n]:
        if L.get('t') == 'b:Link' and child(L, 'targetSlotName').get('v') == 'in10':
            return h2n.get(child(L, 'sourceOrd').get('v')[2:])
ramped = {n: in10(n) for n in ai}
add('Simulation', 'Every analog field input is simulated (ramp / emulation at in10)', all(ramped[n] for n in ai),
    f'{len(ai)} analog inputs; missing: {[n for n in ai if not ramped[n]][:8]}')
fbk = [n for n in writ if re.search(r'(RunProof|FlowProof|ValveOpenProof|BypassValveFeedback|_Status|ValveFeedback)$', n)
       and not re.fullmatch(r'CT0\dRunProof', n)]   # V7.3: tower proof = OR of its fan cells (each cell emulated)
add('Simulation', 'PlantLoadPct = measured cooling load / chiller rating (in16 calc, no ramp) - V7.4 coherent model', in10('PlantLoadPct') is None, 'PlantLoadPct not ramped')
add('Simulation', 'Every feedback input emulated from its command (in10)', all(in10(n) and in10(n).startswith('Sim_') for n in fbk), f'{len(fbk)} feedback inputs')
man = [n for n in writ if re.search(r'(Available|Fault|SensorHealthy|CommunicationHealthy|InAuto|Overload|VibrationAlarm|SmokeDetected|FireAlarmSignal|CommOk)$', n)]
add('Simulation', 'Status inputs (Available/Fault/Healthy) left for manual Override tests', all(in10(n) is None for n in man), f'{len(man)} points: fault injection by in8 Override')

# ---------------- control chains (graph reachability)
chains = [
    ('OA -> Cooling tower', 'OA temperature and humidity drive tower fan speed (WB + approach)', ['OA_Temperature', 'OA_Humidity'], ['CT01_01SpeedCmd', 'CT02_01SpeedCmd']),
    ('OA -> Cooling tower', 'OA sensor validity selects default wet-bulb', ['OA_SensorFault', 'OA_WetBulbDefault'], ['CDS_Setpoint_ACTIVE']),
    ('Min-flow bypass', 'Bypass valve controlled from CHW flow vs sum of chiller minimum flows', ['CHWFlow', 'CH01_MinFlow', 'CH02_MinFlow', 'CH01ValveOpenCmd'], ['CHW_BypassValveCmd']),
    ('Pump DP reset', 'Plant load resets DP setpoint -> CHW pump speed', ['PlantLoadPct', 'DP_MinSetpoint', 'DP_MaxSetpoint'], ['CHP01SpeedCmd', 'CHP02SpeedCmd']),
    ('CHWST reset', 'Plant load resets CHW supply setpoint written to chillers', ['PlantLoadPct', 'CHWST_MinSetpoint', 'CHWST_MaxSetpoint'], ['CHW_LeavingTemperatureSetpoint_ACTIVE']),
    ('Mode / AI', 'Heartbeat + user mode select AI or Local setpoints', ['HeartbeatTimestampSetpoint', 'ModeCmd_UI', 'CHW_LeavingTemperatureSetpoint_AI'], ['CHW_LeavingTemperatureSetpoint_ACTIVE', 'CHWDP_Setpoint_ACTIVE', 'CDS_Setpoint_ACTIVE']),
    ('Staging', 'Load hysteresis and CHWS deviation stage the lag chiller', ['PlantLoadPct', 'CHWS', 'StageUpTempMargin'], ['CH02StartCmd']),
    ('Staging', 'Low delta-T inhibits stage-up', ['CHWR', 'MinDeltaTStage2'], ['CH02StartCmd']),
    ('Rotation', 'Runtime totaliser drives lead/lag rotation', ['Obs_CH01RunProofSelected', 'RotationMode_Runtime', 'RotationRequest'], ['CH01StartCmd', 'CH02StartCmd']),
    ('Failover', 'Proof timeout lockout + operator reset', ['CH01RunProof', 'CH01LockoutReset', 'CHP01RunProof'], ['CH01StartCmd', 'CH02StartCmd']),
    ('Sequence', 'Chiller start needs pumps/tower/valve proofs', ['CHP01RunProof', 'CDP01RunProof', 'CT01RunProof', 'CH01CHWFlowProof', 'CH01CDWFlowProof', 'CH01ValveOpenProof'], ['CH01StartCmd']),
    ('Fail-safe', 'CDS invalid -> tower fail-safe speed', ['CDSSensorHealthy', 'CDSMinValid', 'CT_FailSafeSpeed'], ['CT01_01SpeedCmd', 'CT02_01SpeedCmd']),
    ('Fail-safe', 'CHW DP invalid -> pump fail-safe speed', ['CHWDP_MinValid', 'CHWDP_MaxValid', 'CHP_FailSafeSpeed'], ['CHP01SpeedCmd', 'CHP02SpeedCmd']),
    ('Fail-safe', 'CHW flow invalid -> bypass fail-safe position', ['CHWFlow_MinValid', 'CHWFlow_MaxValid', 'Byp_FailSafePosition'], ['CHW_BypassValveCmd']),
    ('Fail-safe', 'Sensor invalid alarms', ['CHWSSensorHealthy', 'CHWSMinValid'], ['CHWS_SensorInvalidAlarm']),
    ('Fail-safe', 'Program lockout: auto-retry + manual/global RESET reach the start command', ['CH_AutoRetryEnable', 'CH_MaxAutoRetries', 'PlantAlarmResetFire', 'CH01ResetFire', 'CH01LockoutReset'], ['CH01StartCmd']),
    ('Fail-safe', 'Station restart auto-qualify', ['BootAutoQualifyEnable', 'BootQualified'], ['CH01StartCmd']),
    ('Staging', 'Measured cooling load (% of one chiller) drives staging', ['CoolingLoad_RT', 'CH_RatedRT'], ['PlantLoadPct']),
    ('Staging', 'Lead-chiller overload stage-up (load-calc independent)', ['CH01LoadPct', 'Stage_UpLoadPct' if 'Stage_UpLoadPct' in comp else 'LeadOverloadPct', 'StageDownChillerSumPct'], ['CH02StartCmd']),
    ('Protection', 'Tower low-temperature fan cut-out', ['CdsAboveLowLimit'], ['CT01_01SpeedCmd', 'CT02_01SpeedCmd']),
    ('Schedule', 'Optional operating schedule gates plant enable', ['PlantScheduleMode', 'PlantSchedule'], ['CH01StartCmd']),
    ('Energy', 'Daily / monthly energy, kW/RT, cost, CO2, savings', ['Plant_kW', 'CoolingLoad_RT', 'Tariff_THB_per_kWh', 'Baseline_kW_per_RT'], ['Saving_THB_Month']),
    ('Energy', 'Day rollover (TimeTrigger 00:00 / 23:59:59 -> latch actions)', ['DayStartTrigger', 'DayEndTrigger'], ['Plant_kWh_Yesterday']),
    ('Energy', 'Month rollover (schedule day 1 00:02 / 00:02:30)', ['MonthStartSchedule', 'MonthResetDelay'], ['Plant_kWh_LastMonth']),
    ('Energy', 'kW/RT and COP from emulated power and CHW flow x dT', ['CHWFlow', 'CHWS', 'CHWR', 'CH01LoadPct', 'CHP01SpeedCmd', 'CT01_01SpeedCmd'], ['Plant_kW_per_RT', 'Plant_COP']),
    ('Energy', 'kWh totalisers on plant / chillers / auxiliaries', ['Plant_kW', 'CH01_kW', 'Aux_kW'], ['Plant_kWh', 'CH01_kWh', 'Aux_kWh']),
]
chains += [
    ('Pools (V7)', 'CDP01 + CHP02 unavailable -> CH01 still served by CHP02/CDP02 health (cross-set)', ['CHP02Healthy', 'CDP02Healthy', 'CT02Healthy'], ['CH01StartCmd']),
    ('Pools (V7)', 'Every pump/tower request follows BOTH chillers (headered)', ['CH01PostRun', 'CH02PostRun'], ['CHP01StartCmd', 'CHP02StartCmd', 'CDP01StartCmd', 'CDP02StartCmd', 'CT01StartCmd', 'CT02StartCmd']),
    ('Pools (V7)', 'Proof failure / VFD fault / HOA / no-dP / vibration -> standby unit', ['CHP01RunProof', 'CHP01VfdFault', 'CHP01InAuto', 'CHP01_DischargePressure'], ['CHP02StartCmd']),
    ('Pools (V7)', 'Tower vibration / valve failure -> other tower', ['CT01VibrationAlarm', 'CT01ValveOpenProof'], ['CT02StartCmd']),
    ('Pools (V7)', 'Unit failure latch reset by RESET buttons', ['PlantAlarmResetFire', 'CHP01ResetFire', 'CT01ResetFire'], ['CHP01StartCmd', 'CT01StartCmd']),
    ('Pools (V7)', 'Runtime rotation per pool', ['CHP_RotationMode_Runtime', 'CHP01RunProof'], ['CHP02StartCmd']),
    ('Pools (V7)', 'Stage 2 limited by pool capacity', ['CHP02Healthy', 'CDP02Healthy'], ['CH02StartCmd']),
    ('Pools (V7)', 'Chiller CDW isolation valve proof in start permissive', ['CH01CdwValveOpenProof', 'CT01ValveOpenProof'], ['CH01StartCmd']),
    ('Meters (V7)', 'BTU meter primary load source with fail-safe to flow x dT', ['BTU_Power_RT', 'BTU_CommOk', 'LoadSource_BTU', 'CHWFlow'], ['CoolingLoad_RT']),
    ('Meters (V7)', 'Per-chiller kW/RT from chiller flow meter + TT + power meter', ['CH01_ChwFlow', 'CH01_ChwSupplyTemp', 'CH01_ChwReturnTemp', 'CH01_kW'], ['CH01_kW_per_RT']),
    ('Meters (V7)', 'Evaporator approach diagnostic', ['CH01_EvapSatTemp', 'CH01_ChwSupplyTemp'], ['CH01EvapApproachAlarm']),
    ('Meters (V7)', 'Condenser approach diagnostic', ['CH01_CondSatTemp', 'CH01_CdwLeavingTemp'], ['CH01CondApproachAlarm']),
    ('Meters (V7)', 'Basin level transmitter + switches alarm', ['CT01_BasinLevel', 'CT01_LowLevelSwitch'], ['CT01BasinLowLevelAlarm']),
    ('Air (V7)', 'Plant demand mode from air-side cooling calls', ['AHU01_ValveCmd', 'FCU01_ValveCmd', 'PlantDemandMode'], ['PlantRunRequest']),
    ('Air (V7)', 'Trim & Respond: AHU/OAU valve requests reset plant DP / CHWST', ['AHU01_ValveCmd', 'OAU01_ValveCmd', 'ResetSource_AirSide'], ['CHWDP_Setpoint_ACTIVE', 'CHW_LeavingTemperatureSetpoint_ACTIVE']),
]
for u in ('AHU01', 'AHU02', 'OAU01', 'FCU01', 'EF01', 'EF02', 'EF03', 'CPEF01'):
    chains.append(('Air (V7)', f'{u}: fire / HOA / overload / mode interlocks', ['FireAlarmSignal', f'{u}_InAuto', f'{u}_Overload', f'{u}_ModeAuto'], [f'{u}_StartCmd']))
    chains.append(('Air (V7)', f'{u}: fan fail from command vs status', [f'{u}_StartCmd', f'{u}_Status'], [f'{u}_FanFailAlarm']))
for u in ('AHU01', 'AHU02'):
    chains.append(('Air (V7)', f'{u}: SAT reset, valve, static, CO2, smoke', [f'{u}_RAT', f'{u}_SAT', f'{u}_SmokeDetected'], [f'{u}_ValveCmd']))
    chains.append(('Air (V7)', f'{u}: static PID + DCV', [f'{u}_DuctStatic', f'{u}_RA_CO2'], [f'{u}_SpeedCmd', f'{u}_OADamperCmd']) if False else
                  ('Air (V7)', f'{u}: static PID -> speed', [f'{u}_DuctStatic'], [f'{u}_SpeedCmd']))
    chains.append(('Air (V7)', f'{u}: CO2 DCV -> OA damper', [f'{u}_RA_CO2'], [f'{u}_OADamperCmd']))
chains += [('Air (V7)', 'OAU leaving-air + airflow control', ['OAU01_LAT', 'OAU01_Airflow'], ['OAU01_ValveCmd', 'OAU01_SpeedCmd']) if False else
           ('Air (V7)', 'OAU leaving-air control', ['OAU01_LAT', 'OAU01_LAT_SP'], ['OAU01_ValveCmd']),
           ('Air (V7)', 'OAU constant airflow', ['OAU01_Airflow', 'OAU01_Airflow_SP'], ['OAU01_SpeedCmd']),
           ('Air (V7)', 'FCU temperature bands -> fan speed + valve', ['FCU01_RoomTemp', 'FCU01_RoomTemp_SP'], ['FCU01_FanHighCmd', 'FCU01_FanMedCmd', 'FCU01_FanLowCmd', 'FCU01_ValveCmd']),
           ('Air (V7)', 'EF02 duct pressure / EF03 space temp / CPEF01 CO -> VSD', ['EF02_DuctPressure'], ['EF02_SpeedCmd']),
           ('Air (V7)', 'EF03 space temperature -> VSD', ['EF03_SpaceTemp'], ['EF03_SpeedCmd']),
           ('Air (V7)', 'CPEF01 CO -> VSD, fire -> 100 %', ['CPEF01_CO', 'FireAlarmSignal'], ['CPEF01_SpeedCmd']),
           ('Air (V7)', 'LSF01 / SEF01 start on fire alarm', ['FireAlarmSignal'], ['LSF01_StartCmd', 'SEF01_StartCmd']),
           ('Air (V7)', 'LSF01 stair dP control', ['LSF01_StairDP', 'LSF01_StairDP_SP'], ['LSF01_SpeedCmd'])]
for area, text, srcs, tgts in chains:
    pairs = list(zip(srcs, tgts)) if area == 'Energy' and len(srcs) == len(tgts) else [(s, t) for t in tgts for s in srcs]
    miss = [(s, t) for s, t in pairs if s not in upstream(t)]
    add(area, text, not miss, 'all sources reach ' + ', '.join(tgts) if not miss else f'missing paths: {miss}')

def upstream_logic(n):
    """V7.5: control logic only - the path must not run through the plant emulation (Sim_*: pump -> DP -> coil -> AHU call is physics)"""
    seen, st = set(), [n]
    while st:
        x = st.pop()
        for y in up[x]:
            if y not in seen and not y.startswith('Sim_'): seen.add(y); st.append(y)
    return seen


bad_up = [x for x in ('SensorReady', 'CommunicationHealthy', 'CHWSSensorHealthy', 'CDSSensorHealthy') if x in upstream_logic('PlantPermissive')]
add('Fail-safe', 'Plant permissive independent of sensor / comms health', not bad_up, f'upstream of PlantPermissive: {bad_up or "none"}')

dly = lambda n, p='onDelay': int(child(comp[n], p).get('v'))
site = {'CH01StartTimeoutDelay': 60000, 'CH01AuxProofTimeout': 30000, 'CH01MinOffDelay': 120000, 'CH01MinRunDelay': 300000}
add('Timing', 'Commissioning (site) timers, not compressed test timers', all(dly(k) >= v for k, v in site.items()) and dly('CH01PostRun', 'offDelay') >= 60000,
    f"start timeout {dly('CH01StartTimeoutDelay')//1000} s, aux timeout {dly('CH01AuxProofTimeout')//1000} s, min off {dly('CH01MinOffDelay')//1000} s, min run {dly('CH01MinRunDelay')//1000} s, post-run {dly('CH01PostRun', 'offDelay')//1000} s, stage up/down {dly('StageLoadTimer')//1000}/{dly('StageLoadTimer', 'offDelay')//1000} s")

# ---------------- tuning / protection values
g = lambda n, p: (child(comp[n], p).get('v') if child(comp[n], p) is not None else None)
add('Protection', 'Minimum speeds: CHW pump 30 %, tower fan 20 %', g('CHWDP_Clamp', 'inMin') == '30.0' and g('CDS_Clamp', 'inMin') == '20.0', f"CHWDP_Clamp.inMin={g('CHWDP_Clamp', 'inMin')} CDS_Clamp.inMin={g('CDS_Clamp', 'inMin')}")
add('Protection', 'ACTIVE setpoints clamped (never out of range to equipment)', all(typ[x] == 'Limiter' for x in ('ChwstActiveClamp', 'DpActiveClamp', 'CdsActiveClamp')),
    f"CHWST {g('ChwstActiveClamp', 'inMin')}..{g('ChwstActiveClamp', 'inMax')} DP {g('DpActiveClamp', 'inMin')}..{g('DpActiveClamp', 'inMax')} CDS {g('CdsActiveClamp', 'inMin')}..{g('CdsActiveClamp', 'inMax')}")
add('Tuning', 'Loop actions: DP reverse, bypass reverse, tower direct', g('CHWDP_PID', 'loopAction') == 'reverse' and g('Byp_PID', 'loopAction') == 'reverse' and g('CDS_PID', 'loopAction') in (None, 'direct'),
    f"CHWDP Kp {g('CHWDP_PID', 'proportionalConstant')} Ki {g('CHWDP_PID', 'integralConstant')}/min; CDS Kp {g('CDS_PID', 'proportionalConstant')} Ki {g('CDS_PID', 'integralConstant')}/min; Byp Kp {g('Byp_PID', 'proportionalConstant')} Ki {g('Byp_PID', 'integralConstant')}/min (start-up values)")

INTD = {'LoopPoint': ('proportionalConstant', 'integralConstant', 'derivativeConstant', 'bias', 'maximumOutput', 'minimumOutput'),
        'Ramp': ('amplitude', 'offset'), 'SineWave': ('amplitude', 'offset')}
bad_t = [(n, c.get('n')) for n in comp if typ[n] in INTD for c in comp[n] if c.get('n') in INTD[typ[n]] and c.get('t') != 'b:Double']
bad_i = [n for n in comp if typ[n] == 'MultiVibrator' and child(comp[n], 'dutyCycle') is not None and not child(comp[n], 'dutyCycle').get('v').isdigit()]
add('Structure', 'kitControl slot value types (int-default doubles typed b:Double, dutyCycle int)', not bad_t and not bad_i, f'untyped={bad_t[:5]} bad dutyCycle={bad_i}')
with open(out, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=['Area', 'Check', 'Result', 'Evidence']); w.writeheader(); w.writerows(rows)
for x in rows:
    print(f"{x['Result']:4} {x['Area']:18} {x['Check']}\n     {x['Evidence'][:230]}")
print('PASS', sum(x['Result'] == 'PASS' for x in rows), '/', len(rows))
