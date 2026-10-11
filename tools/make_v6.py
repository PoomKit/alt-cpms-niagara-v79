"""Build ALT_CP_Ref_V6 — energy-optimised, fully instrumented reference chiller plant.

Base: compact V5 (`c_v5.bog`: V4 logic proven by FPT + V5 corrections).
Everything is generated from patterns verified in this N4.15 installation:
  * kitControl slot names via javap of kitControl-rt.jar
  * alarm / history / totalizer / tag XML shapes copied from working stations
    ST5130_Klongluang and Makro_PraditBackup230926 on the same workstation
  * MELCO 212_Point rules: AlarmClass Emergency/Critical/Warning/Info, History
    CoV cap 4000 / Interval cap 550000, melco:pointNameString, _AI/_LOCAL/_ACTIVE,
    folder UpperCamelCase with 2-digit equipment numbers.
REFERENCE SIMULATION – NOT PROJECT APPROVED.  Output is a NEW station file.
"""
import sys, os, re, csv, zipfile, hashlib, argparse, math
import xml.etree.ElementTree as ET
from copy import deepcopy
from collections import Counter, OrderedDict, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from check_symbols import check as check_symbols, fix as fix_symbols

STATION = 'ALT_CP_Ref_V6_3'   # new station next to V6/V6_2 (no config.bog overwrite)
FOXS_PORT = '4917'
TZ = 'Asia/Bangkok;25200000;0;null;null'
U = {  # unit facet encodings copied from working station BOGs
    'C': 'units=u:celsius;\u00b0C;(K);+273.15;', 'pct': 'units=u:percent;%;;;',
    'RH': 'units=u:percent relative humidity;%RH;;;', 'kPa': 'units=u:kilopascal;kPa;(m-1)(kg)(s-2);*1000.0;',
    'kW': 'units=u:kilowatt;kW;(m2)(kg)(s-3);*1000.0;', 'kWh': 'units=u:kilowatt hour;kW-hr;(m2)(kg)(s-2);*3600000.0;',
    'm3h': 'units=u:cubic meters per hour;m\u00b3/hr;(m3)(s-1);*2.777777777777778E-4;',
    'tR': 'units=u:tons refrigeration;tR;(m2)(kg)(s-3);*3516.853;', 'hr': 'units=u:hour;hr;(s);*3600.0;',
    'none': 'units=u:null;;;;',
}
PARENT_FOLDERS = OrderedDict([
    ('PlantControl', ['Points', 'Enable', 'Restart', 'SensorValidation', 'LeadLag', 'Staging', 'Monitor']),
    ('ModeControl', []), ('AI_Heartbeat', []), ('OutdoorAir', []), ('Optimization', []),
    ('ChwLoop', ['Points', 'DpControl', 'MinFlowBypass', 'Monitor']),
    ('CdwLoop', ['Points', 'TowerControl', 'Monitor']),
    ('Chiller01', ['Points', 'Request', 'Permissive', 'Command', 'Proof', 'Fault', 'Stop', 'Monitor']),
    ('Chiller02', ['Points', 'Request', 'Permissive', 'Command', 'Proof', 'Fault', 'Stop', 'Monitor']),
    ('CHP01', ['Points', 'Logic', 'Monitor']), ('CHP02', ['Points', 'Logic', 'Monitor']),
    ('CDP01', ['Points', 'Logic', 'Monitor']), ('CDP02', ['Points', 'Logic', 'Monitor']),
    ('CT01', ['Points', 'Logic', 'Monitor']), ('CT02', ['Points', 'Logic', 'Monitor']),
    ('Energy', []), ('Alarms', []), ('Parameters', []),
    ('Simulation', ['Ramps', 'Feedback']),
])


def child(el, n):
    return next((c for c in el if c.tag == 'p' and c.get('n') == n), None)


def P(parent, n, t=None, v=None, h=None, f=None):
    a = {'n': n}
    if h: a['h'] = h
    if f: a['f'] = f
    if t: a['t'] = t
    if v is not None: a['v'] = v
    return ET.SubElement(parent, 'p', a)


class Station:
    def __init__(self, root):
        self.root = root
        self.st = root.find('p')
        self.rp = child(self.st, 'ReferencePlant')
        used = [int(h, 16) for h in (e.get('h') for e in root.iter('p')) if h and re.fullmatch('[0-9a-f]+', h)]
        self.nh = max(max(used) + 1, 0x2000)
        self.comp = OrderedDict()      # name -> element (all ReferencePlant components)
        self.folder_of = {}            # name -> folder path
        self.meta = {}                 # name -> dict(kind, unit, ...)
        self.log = []                  # change log rows
        self.ext_handle = {}           # 'Point:ExtName' -> handle
        for f in list(self.rp):
            if f.get('n') in ('SimInputs', 'PlantLogic', 'SimOutputs'):
                for c in list(f):
                    if c.tag == 'p' and c.get('t') and c.get('t') != 'b:WsAnnotation':
                        self.comp[c.get('n')] = c
                self.rp.remove(f)

    def path_of(self, n):
        return '/ChillerPlant/' + self.folder_of[n] + '/' + n

    def h(self):
        v = format(self.nh, 'x'); self.nh += 1; return v

    def handle(self, name):
        if '.' in name: name = name.split('.')[0]
        return self.comp[name].get('h')

    # ---------------------------------------------------------------- builders
    def link(self, target_el, src, tslot):
        sslot = 'out'
        if '.' in src:
            src, sslot = src.split('.', 1)
        existing = [c.get('n') for c in target_el if c.get('t') == 'b:Link']
        i = 0
        while ('Link' if i == 0 else f'Link{i}') in existing: i += 1
        L = P(target_el, 'Link' if i == 0 else f'Link{i}', 'b:Link')
        src_h = self.ext_handle[src] if src in self.ext_handle else self.handle(src)
        for n, v in (('sourceOrd', 'h:' + src_h), ('relationTags', ''), ('relationId', 'n:dataLink'),
                     ('sourceSlotName', sslot), ('targetSlotName', tslot)):
            P(L, n, v=v)

    def add(self, folder, name, typ, links=None, props=(), fallback=None, facets=None, note=''):
        if name in self.comp: raise SystemExit('duplicate ' + name)
        el = ET.Element('p', {'n': name, 'h': self.h(), 't': typ})
        if facets:
            P(el, 'facets', 'b:Facets', facets)
        if fallback is not None:
            kind, val = fallback
            fb = P(el, 'fallback', 'b:StatusBoolean' if kind == 'b' else 'b:StatusNumeric')
            P(fb, 'value', v=str(val).lower() if kind == 'b' else repr(float(val)))
        for pn, pt, pv in props:
            if pt == 'SN':  # static StatusNumeric property value
                s = P(el, pn, 'b:StatusNumeric'); P(s, 'value', v=repr(float(pv)))
            elif pt == 'SB':
                s = P(el, pn, 'b:StatusBoolean'); P(s, 'value', v=str(pv).lower())
            else:
                P(el, pn, pt, pv)
        self.comp[name] = el
        self.folder_of[name] = folder
        for tslot, src in (links or {}).items():
            self.link(el, src, tslot)
        self.log.append(('ADD', folder, name, typ, ';'.join(f'{k}<-{v}' for k, v in (links or {}).items()), note))
        return name

    def param(self, name, value, unit='none', folder='Parameters', prec=1, lo=None, hi=None, note=''):
        fac = U[unit] + f'|precision=i:{prec}|min=d:{lo if lo is not None else "-inf"}|max=d:{hi if hi is not None else "+inf"}'
        self.meta[name] = {'kind': 'param', 'unit': unit}
        return self.add(folder, name, 'c:NumericWritable', fallback=('n', value), facets=fac, note=note)

    def bparam(self, name, value, folder='Parameters', t='true', f='false', note=''):
        self.meta[name] = {'kind': 'bparam'}
        return self.add(folder, name, 'c:BooleanWritable', fallback=('b', value),
                        facets=f'trueText=s:{t}|falseText=s:{f}', note=note)

    def npoint(self, folder, name, src, unit='none', prec=2, kind='calc', note=''):
        """Numeric point driven at in16 by logic (history/alarm/tag/graphic carrier)."""
        self.meta[name] = {'kind': kind, 'unit': unit}
        return self.add(folder, name, 'c:NumericWritable', links={'in16': src},
                        facets=U[unit] + f'|precision=i:{prec}|min=d:-inf|max=d:+inf', note=note)

    def bpoint(self, folder, name, src, t='true', f='false', kind='calc', note=''):
        self.meta[name] = {'kind': kind}
        return self.add(folder, name, 'c:BooleanWritable', links={'in16': src},
                        facets=f'trueText=s:{t}|falseText=s:{f}', note=note)

    def kc(self, folder, name, typ, links=None, props=(), note=''):
        return self.add(folder, name, 'kitControl:' + typ, links=links, props=props, note=note)

    def rewire(self, target, tslot, new_src, old_src=None):
        el = self.comp[target]
        L = [c for c in el if c.get('t') == 'b:Link' and child(c, 'targetSlotName').get('v') == tslot]
        if len(L) != 1: raise SystemExit(f'rewire {target}.{tslot}: {len(L)} links')
        so = child(L[0], 'sourceOrd')
        if old_src and so.get('v') != 'h:' + self.handle(old_src):
            raise SystemExit(f'rewire {target}.{tslot}: unexpected source')
        sslot = 'out'
        if '.' in new_src: new_src, sslot = new_src.split('.', 1)
        so.set('v', 'h:' + self.handle(new_src)); child(L[0], 'sourceSlotName').set('v', sslot)
        self.log.append(('REWIRE', '', target, tslot, f'{old_src} -> {new_src}', ''))

    def set_fallback(self, name, value):
        fb = child(self.comp[name], 'fallback'); child(fb, 'value').set('v', str(value).lower() if isinstance(value, bool) else repr(float(value)))
        self.log.append(('SET', '', name, 'fallback', str(value), ''))

    def set_prop(self, name, prop, value, typ=None):
        el = self.comp[name]; p = child(el, prop)
        if p is None: p = P(el, prop, typ, value)
        else: p.set('v', value)
        self.log.append(('SET', '', name, prop, value, ''))


# ============================================================ existing -> folders
PARAM_NAMES = {'ConstantTrue', 'ConstantFalse', 'ZeroSpeed', 'FixedCDPSpeedPct', 'StageZero', 'StageOne', 'StageTwo',
               'MinDeltaTStage2', 'CHWSMinValid', 'CHWSMaxValid', 'CDSMinValid', 'CDSMaxValid'}
PLANT_POINTS = {'PlantEnable', 'CommunicationHealthy', 'AutoMode', 'BootQualified', 'Stage2Demand', 'RotationRequest',
                'PlantLoadPct', 'LeadCH01', 'PlantRunRequest', 'PlantStage', 'Stage2Request'}


def add_ext(S, point, name, typ, props=()):
    el = S.comp[point]
    h = S.h()
    e = P(el, name, typ, h=h)
    for pn, pt, pv in props:
        P(e, pn, pt, pv)
    S.ext_handle[f'{point}:{name}'] = h
    S.log.append(('EXT', '', point, name, typ, ''))
    return e


def existing_folder(name, group, top):
    if name in PARAM_NAMES: return 'Parameters'
    if name in PLANT_POINTS: return 'PlantControl/Points'
    if name in ('CHWDPSetpoint', 'CDSSetpoint'): return 'ModeControl'
    if top == 'PlantLogic':
        m = {'Restart': 'PlantControl/Restart', 'Sensors': 'PlantControl/SensorValidation', 'Plant': 'PlantControl/Enable',
             'History': 'PlantControl/Enable', 'LeadLag': 'PlantControl/LeadLag', 'Staging': 'PlantControl/Staging',
             'CHWControl': 'ChwLoop/DpControl', 'CTControl': 'CdwLoop/TowerControl'}
        if group in m: return m[group]
        if group.startswith('CH0'): return 'Chiller' + group[2:]            # CH01/Request -> Chiller01/Request
        return group + '/Logic'                                              # CHP01 -> CHP01/Logic
    if top == 'SimInputs':
        if group in ('CHW',): return 'ChwLoop/Points'
        if group in ('Condenser',): return 'CdwLoop/Points'
        if group.startswith('CH0'): return 'Chiller' + group[2:4] + '/Points'
        return group + '/Points'
    # SimOutputs
    if group in ('Plant', 'Staging', 'Restart', 'Sensors', 'History'): return 'PlantControl/Monitor'
    if group == 'CHWControl': return 'ChwLoop/Monitor'
    if group == 'CTControl': return 'CdwLoop/Monitor'
    if group.startswith('CH0'):
        return 'Chiller' + group[2:4] + ('/Points' if group.endswith('Command') else '/Monitor')
    return group + ('/Monitor' if name.startswith('Obs') else '/Points')


def build(S, groups):
    for name in list(S.comp):
        key = [k for k in groups if k.split('/', 1)[1] == name]
        top, grp = key[0].split('/', 1)[0], groups[key[0]]
        S.folder_of[name] = existing_folder(name, grp, top)
    # remove legacy history exts (regenerated uniformly with V6 station id) and annotations
    for name, el in S.comp.items():
        for c in list(el):
            if (c.get('t') or '').endswith('HistoryExt') or c.get('n') == 'wsAnnotation':
                el.remove(c)
    T, F = 'ConstantTrue', 'ConstantFalse'

    # ------------------------------------------------------------ parameters
    S.param('CT_Approach', 3.0, 'none', note='Tower approach above OA wet-bulb (K); SOO ref: WB + 4.5 F')
    S.param('CDW_MinSetpoint', 24.0, 'C', note='Min CDW supply SP (chiller min ECWT) PROJECT/OEM')
    S.param('CDW_MaxSetpoint', 32.0, 'C', note='Max CDW supply SP')
    S.param('OA_WetBulbDefault', 27.0, 'C', note='Fallback WB when OA sensor invalid')
    S.param('OA_TempMinValid', 0.0, 'C'); S.param('OA_TempMaxValid', 50.0, 'C')
    S.param('OA_HumMinValid', 5.0, 'RH'); S.param('OA_HumMaxValid', 100.0, 'RH')
    S.param('DP_MinSetpoint', 60.0, 'kPa', note='Plant reset: DP at 0 % request')
    S.param('DP_MaxSetpoint', 150.0, 'kPa', note='Plant reset: DP at 50 % request')
    S.param('CHWST_MinSetpoint', 7.0, 'C', note='Plant reset: CHWST at 100 % request')
    S.param('CHWST_MaxSetpoint', 10.0, 'C', note='Plant reset: CHWST at 50 % request (dehumidification cap)')
    S.param('PlantReset_Zero', 0.0, 'pct'); S.param('PlantReset_Half', 50.0, 'pct'); S.param('PlantReset_Full', 100.0, 'pct')
    S.param('CH01_MinFlow', 60.0, 'm3h', note='OEM evaporator minimum flow PROJECT/OEM')
    S.param('CH02_MinFlow', 60.0, 'm3h', note='OEM evaporator minimum flow PROJECT/OEM')
    S.param('Byp_InactivePosition', 0.0, 'pct', note='Bypass position when loop disabled PROJECT (fail-safe)')
    S.param('StageUpTempMargin', 1.5, 'none', note='CHWS above ACTIVE SP (K) for failsafe stage-up')
    S.param('ChwstNotTrackingMargin', 2.0, 'none', note='MELCO Critical: CHWS above SP (K)')
    S.param('CdsNotTrackingMargin', 2.0, 'none', note='CDW supply above tower setpoint (K)')
    S.param('LowFlowRatio', 0.5, 'none', note='Emergency low flow = flow < ratio x min-flow SP')
    S.param('CH01_RatedKW', 180.0, 'kW', note='SIM: ~300 RT chiller @0.6 kW/RT (PROJECT value)'); S.param('CH02_RatedKW', 180.0, 'kW', note='SIM: ~300 RT chiller (PROJECT value)')
    S.param('CHP_RatedKW', 15.0, 'kW'); S.param('CDP_RatedKW', 18.5, 'kW'); S.param('CT_RatedKW', 11.0, 'kW')
    S.param('HB_RequiredBeats', 2.0, 'none', prec=0, note='MELCO: Pre_Connect -> Connect after 2 heartbeats')
    S.param('Water_kW_Factor', 1.1628, 'none', prec=4, note='kW per (m3/h x K) = 4.186 x 1000 / 3600')
    S.param('kW_per_RT', 3.517, 'none', prec=3)
    S.param('RuntimeRotationHours', 24.0, 'hr', note='Runtime imbalance before auto rotation (hysteresis +/-)')
    S.param('MsPerHour', 3600000.0, 'none', prec=0)
    S.param('BypassMismatchPct', 10.0, 'pct', note='Valve cmd/feedback deviation for mismatch alarm')
    S.param('AI_ChwstMin', 6.0, 'C'); S.param('AI_ChwstMax', 12.0, 'C')
    S.param('AI_DpMin', 50.0, 'kPa'); S.param('AI_DpMax', 200.0, 'kPa')
    S.param('One', 1.0, 'none', prec=0); S.param('MinLoadForKpi', 5.0, 'tR')

    # ------------------------------------------------------------ outdoor air + psychrometrics
    S.param('OA_Temperature', 31.0, 'C', folder='OutdoorAir', note='SIM INPUT (ramped)'); S.meta['OA_Temperature'] = {'kind': 'ai', 'unit': 'C'}
    S.param('OA_Humidity', 70.0, 'RH', folder='OutdoorAir', note='SIM INPUT (ramped)'); S.meta['OA_Humidity'] = {'kind': 'ai', 'unit': 'RH'}
    S.bparam('OA_SensorFault', False, folder='OutdoorAir', t='Fault', f='Normal', note='SIM INPUT (manual fault injection)')
    S.meta['OA_SensorFault'] = {'kind': 'di'}
    OA = 'OutdoorAir'
    S.kc(OA, 'OA_Psychrometric', 'Psychrometric', {'inTemp': 'OA_Temperature', 'inHumidity': 'OA_Humidity'},
         props=[('unitSelect', None, 'metric')])
    S.kc(OA, 'OA_TempAboveMin', 'GreaterThanEqual', {'inA': 'OA_Temperature', 'inB': 'OA_TempMinValid'})
    S.kc(OA, 'OA_TempBelowMax', 'LessThanEqual', {'inA': 'OA_Temperature', 'inB': 'OA_TempMaxValid'})
    S.kc(OA, 'OA_HumAboveMin', 'GreaterThanEqual', {'inA': 'OA_Humidity', 'inB': 'OA_HumMinValid'})
    S.kc(OA, 'OA_HumBelowMax', 'LessThanEqual', {'inA': 'OA_Humidity', 'inB': 'OA_HumMaxValid'})
    S.kc(OA, 'NotOA_SensorFault', 'Not', {'in': 'OA_SensorFault'})
    S.kc(OA, 'OA_RangeOk', 'And', {'inA': 'OA_TempAboveMin', 'inB': 'OA_TempBelowMax', 'inC': 'OA_HumAboveMin', 'inD': 'OA_HumBelowMax'})
    S.kc(OA, 'OA_ValidLogic', 'And', {'inA': 'OA_RangeOk', 'inB': 'NotOA_SensorFault', 'inC': T, 'inD': T})
    S.bpoint(OA, 'OA_Valid', 'OA_ValidLogic', 'Valid', 'Invalid')
    S.kc(OA, 'OA_WetBulbSelect', 'NumericSwitch', {'inSwitch': 'OA_ValidLogic', 'inTrue': 'OA_Psychrometric.outWetBulbTemp', 'inFalse': 'OA_WetBulbDefault'})
    S.npoint(OA, 'OA_WetBulb', 'OA_WetBulbSelect', 'C')
    S.npoint(OA, 'OA_DewPoint', 'OA_Psychrometric.outDewPoint', 'C')
    S.npoint(OA, 'OA_Enthalpy', 'OA_Psychrometric.outEnthalpy', 'none')

    # ------------------------------------------------------------ plant reset (GPC36 structure) + CDW approach
    O = 'Optimization'
    S.kc(O, 'PlantResetRequest', 'Limiter', {'inA': 'PlantLoadPct'}, props=[('inMin', None, '0.0'), ('inMax', None, '100.0')],
         note='Reset variable 0-100 %. Reference proxy = plant load; PROJECT: Trim & Respond from AHU valve requests')
    S.npoint(O, 'PlantResetPct', 'PlantResetRequest', 'pct')
    S.kc(O, 'Opt_DpReset', 'Reset', {'inA': 'PlantResetRequest', 'inputLowLimit': 'PlantReset_Zero', 'inputHighLimit': 'PlantReset_Half',
                                     'outputLowLimit': 'DP_MinSetpoint', 'outputHighLimit': 'DP_MaxSetpoint'})
    S.kc(O, 'Opt_ChwstReset', 'Reset', {'inA': 'PlantResetRequest', 'inputLowLimit': 'PlantReset_Half', 'inputHighLimit': 'PlantReset_Full',
                                        'outputLowLimit': 'CHWST_MaxSetpoint', 'outputHighLimit': 'CHWST_MinSetpoint'})
    S.kc(O, 'Opt_CdwSetpointRaw', 'Add', {'inA': 'OA_WetBulbSelect', 'inB': 'CT_Approach'})
    S.kc(O, 'Opt_CdwAboveMin', 'Maximum', {'inA': 'Opt_CdwSetpointRaw', 'inB': 'CDW_MinSetpoint'})
    S.kc(O, 'Opt_CdwSetpointLimited', 'Minimum', {'inA': 'Opt_CdwAboveMin', 'inB': 'CDW_MaxSetpoint'})
    S.npoint(O, 'Opt_DpSetpoint', 'Opt_DpReset', 'kPa', 1)
    S.npoint(O, 'Opt_ChwstSetpoint', 'Opt_ChwstReset', 'C', 1)
    S.npoint(O, 'Opt_CdwSetpoint', 'Opt_CdwSetpointLimited', 'C', 1)

    # ------------------------------------------------------------ heartbeat (MELCO state model, native blocks)
    H = 'AI_Heartbeat'
    S.param('HeartbeatTimestampSetpoint', 0.0, 'none', folder=H, prec=0, note='AI writes a new value every 5 min'); S.meta['HeartbeatTimestampSetpoint']['kind'] = 'ai_w'
    S.kc(H, 'HB_SampleClock', 'MultiVibrator', props=[('period', None, '60000'), ('dutyCycle', None, '50.0')])
    S.kc(H, 'HB_LastSample', 'NumericLatch', {'in': 'HeartbeatTimestampSetpoint', 'clock': 'HB_SampleClock'})
    S.kc(H, 'HB_Changed', 'NotEqual', {'inA': 'HeartbeatTimestampSetpoint', 'inB': 'HB_LastSample'})
    S.kc(H, 'HB_Recent', 'BooleanDelay', {'in': 'HB_Changed'}, props=[('onDelay', 'b:RelTime', '0'), ('offDelay', 'b:RelTime', '360000')],
         note='Connect -> Pre_Disconnect after 6 min without heartbeat')
    S.kc(H, 'HB_NotRecent', 'Not', {'in': 'HB_Recent'})
    S.kc(H, 'HB_DisconnectDelay', 'BooleanDelay', {'in': 'HB_NotRecent'}, props=[('onDelay', 'b:RelTime', '360000'), ('offDelay', 'b:RelTime', '0')],
         note='Pre_Disconnect -> Disconnect after further 6 min (12 min total)')
    S.kc(H, 'HB_BeatCounter', 'Counter', {'countUp': 'HB_Changed', 'clearIn': 'HB_DisconnectDelay'},
         note='Disconnect -> Pre_Connect (1 beat) -> Connect (2 beats)')
    S.kc(H, 'HB_EnoughBeats', 'GreaterThanEqual', {'inA': 'HB_BeatCounter', 'inB': 'HB_RequiredBeats'})
    S.kc(H, 'HB_NotDisconnected', 'Not', {'in': 'HB_DisconnectDelay'})
    S.kc(H, 'HB_OkLogic', 'And', {'inA': 'HB_EnoughBeats', 'inB': 'HB_NotDisconnected', 'inC': T, 'inD': T})
    S.bpoint(H, 'HeartbeatDetectorStatus', 'HB_OkLogic', 'OK', 'NG')
    S.bpoint(H, 'HeartbeatPreDisconnect', 'HB_NotRecent', 'PreDisconnect', 'Normal')

    # ------------------------------------------------------------ mode control (_AI / _LOCAL / _ACTIVE)
    M = 'ModeControl'
    S.bparam('ModeCmd_UI', False, folder=M, t='AI', f='Local', note='User mode request (highest priority)'); S.meta['ModeCmd_UI']['kind'] = 'mode'
    S.bparam('OptimizationEnable', True, folder=M, t='Enabled', f='Disabled', note='LOCAL mode: use optimiser (true) or fixed LOCAL SP')
    S.param('CHW_LeavingTemperatureSetpoint_LOCAL', 7.0, 'C', folder=M, lo=5.0, hi=20.0)
    S.param('CHW_LeavingTemperatureSetpoint_AI', 7.0, 'C', folder=M, lo=5.0, hi=20.0); S.meta['CHW_LeavingTemperatureSetpoint_AI']['kind'] = 'ai_w'
    S.param('CHWDP_Setpoint_AI', 120.0, 'kPa', folder=M, lo=30.0, hi=250.0); S.meta['CHWDP_Setpoint_AI']['kind'] = 'ai_w'
    S.param('CDS_Setpoint_AI', 29.0, 'C', folder=M, lo=20.0, hi=35.0); S.meta['CDS_Setpoint_AI']['kind'] = 'ai_w'
    S.meta['CHWDPSetpoint'] = {'kind': 'param', 'unit': 'kPa'}; S.meta['CDSSetpoint'] = {'kind': 'param', 'unit': 'C'}
    S.kc(M, 'AI_ChwstAboveMin', 'GreaterThanEqual', {'inA': 'CHW_LeavingTemperatureSetpoint_AI', 'inB': 'AI_ChwstMin'})
    S.kc(M, 'AI_ChwstBelowMax', 'LessThanEqual', {'inA': 'CHW_LeavingTemperatureSetpoint_AI', 'inB': 'AI_ChwstMax'})
    S.kc(M, 'AI_DpAboveMin', 'GreaterThanEqual', {'inA': 'CHWDP_Setpoint_AI', 'inB': 'AI_DpMin'})
    S.kc(M, 'AI_DpBelowMax', 'LessThanEqual', {'inA': 'CHWDP_Setpoint_AI', 'inB': 'AI_DpMax'})
    S.kc(M, 'AI_CdsAboveMin', 'GreaterThanEqual', {'inA': 'CDS_Setpoint_AI', 'inB': 'CDW_MinSetpoint'})
    S.kc(M, 'AI_CdsBelowMax', 'LessThanEqual', {'inA': 'CDS_Setpoint_AI', 'inB': 'CDW_MaxSetpoint'})
    S.kc(M, 'AI_ValuesValidA', 'And', {'inA': 'AI_ChwstAboveMin', 'inB': 'AI_ChwstBelowMax', 'inC': 'AI_DpAboveMin', 'inD': 'AI_DpBelowMax'})
    S.kc(M, 'AI_ValuesValid', 'And', {'inA': 'AI_ValuesValidA', 'inB': 'AI_CdsAboveMin', 'inC': 'AI_CdsBelowMax', 'inD': T})
    S.kc(M, 'AI_AvailableLogic', 'And', {'inA': 'HB_OkLogic', 'inB': 'AI_ValuesValid', 'inC': T, 'inD': T})
    S.bpoint(M, 'AI_Available', 'AI_AvailableLogic', 'OK', 'NG')
    S.kc(M, 'OperationModeAI', 'And', {'inA': 'ModeCmd_UI', 'inB': 'AI_AvailableLogic', 'inC': T, 'inD': T},
         note='User Local always wins; AI only when heartbeat OK and AI values in range')
    S.bpoint(M, 'OperationMode', 'OperationModeAI', 'AI', 'Local')
    S.kc(M, 'NotOperationModeAI', 'Not', {'in': 'OperationModeAI'})
    S.kc(M, 'LocalModeProlongedDelay', 'BooleanDelay', {'in': 'NotOperationModeAI'},
         props=[('onDelay', 'b:RelTime', '3600000'), ('offDelay', 'b:RelTime', '0')])
    S.kc(M, 'AiRequestedButLocal', 'And', {'inA': 'ModeCmd_UI', 'inB': 'NotOperationModeAI', 'inC': T, 'inD': T})
    for base, loc, ai, opt, unit, lo, hi in (('Chwst', 'CHW_LeavingTemperatureSetpoint_LOCAL', 'CHW_LeavingTemperatureSetpoint_AI', 'Opt_ChwstReset', 'C', 5.0, 20.0),
                                             ('Dp', 'CHWDPSetpoint', 'CHWDP_Setpoint_AI', 'Opt_DpReset', 'kPa', 30.0, 250.0),
                                             ('Cds', 'CDSSetpoint', 'CDS_Setpoint_AI', 'Opt_CdwSetpointLimited', 'C', 20.0, 35.0)):
        S.kc(M, f'{base}LocalSelect', 'NumericSwitch', {'inSwitch': 'OptimizationEnable', 'inTrue': opt, 'inFalse': loc})
        S.kc(M, f'{base}ActiveSelect', 'NumericSwitch', {'inSwitch': 'OperationModeAI', 'inTrue': ai, 'inFalse': f'{base}LocalSelect'})
        S.kc(M, f'{base}ActiveClamp', 'Limiter', {'inA': f'{base}ActiveSelect'}, props=[('inMin', None, repr(lo)), ('inMax', None, repr(hi))],
             note='Protection: out-of-range values never reach equipment')
    S.npoint(M, 'CHW_LeavingTemperatureSetpoint_ACTIVE', 'ChwstActiveClamp', 'C', 1, kind='ao')
    S.npoint(M, 'CHWDP_Setpoint_ACTIVE', 'DpActiveClamp', 'kPa', 1, kind='sp')
    S.npoint(M, 'CDS_Setpoint_ACTIVE', 'CdsActiveClamp', 'C', 1, kind='sp')
    S.rewire('CHWDP_PID', 'setpoint', 'CHWDP_Setpoint_ACTIVE', 'CHWDPSetpoint')
    S.rewire('CDS_PID', 'setpoint', 'CDS_Setpoint_ACTIVE', 'CDSSetpoint')
    # tower / pump minimum speeds (energy + equipment protection)
    S.set_prop('CDS_Clamp', 'inMin', '20.0'); S.set_prop('CHWDP_Clamp', 'inMin', '30.0')
    # loop tuning: kitControl LoopPoint = Kp*e + Kp*Ki*sum(e*dt[s])/60 (Ki in repeats/min, from BLoopPoint bytecode).
    # V4 Kp 0.5 / Ki 0.01 gives < 1 %/h integral action -> fans/pumps sit on their minimum clamp. START-UP VALUES, tune on site.
    S.set_prop('CDS_PID', 'proportionalConstant', '10.0'); S.set_prop('CDS_PID', 'integralConstant', '0.5')
    S.set_prop('CHWDP_PID', 'proportionalConstant', '1.0'); S.set_prop('CHWDP_PID', 'integralConstant', '0.5')

    # ------------------------------------------------------------ CHW minimum-flow bypass (Forestias pattern)
    B = 'ChwLoop/MinFlowBypass'
    S.kc(B, 'Byp_CH01MinFlow', 'NumericSwitch', {'inSwitch': 'CH01ValveOpenCmd', 'inTrue': 'CH01_MinFlow', 'inFalse': 'ZeroSpeed'})
    S.kc(B, 'Byp_CH02MinFlow', 'NumericSwitch', {'inSwitch': 'CH02ValveOpenCmd', 'inTrue': 'CH02_MinFlow', 'inFalse': 'ZeroSpeed'})
    S.kc(B, 'Byp_MinFlowSum', 'Add', {'inA': 'Byp_CH01MinFlow', 'inB': 'Byp_CH02MinFlow'})
    S.npoint(B, 'CHW_MinFlowSetpoint', 'Byp_MinFlowSum', 'm3h', 1)
    S.kc(B, 'Byp_AnyPumpProven', 'Or', {'inA': 'CHP01RunProof', 'inB': 'CHP02RunProof', 'inC': F, 'inD': F})
    S.kc(B, 'Byp_Enable', 'And', {'inA': 'PlantPermissive', 'inB': 'Byp_AnyPumpProven', 'inC': T, 'inD': T})
    S.kc(B, 'Byp_PID', 'LoopPoint', {'controlledVariable': 'CHWFlow', 'setpoint': 'Byp_MinFlowSum', 'loopEnable': 'Byp_Enable'},
         props=[('loopAction', None, 'reverse'), ('proportionalConstant', None, '0.5'), ('integralConstant', None, '1.0'),
                ('maximumOutput', None, '100.0'), ('minimumOutput', None, '0.0')],
         note='Flow below minimum -> open bypass (reverse acting)')
    S.kc(B, 'Byp_Select', 'NumericSwitch', {'inSwitch': 'Byp_Enable', 'inTrue': 'Byp_PID', 'inFalse': 'Byp_InactivePosition'})
    S.kc(B, 'Byp_RateLimit', 'NumericDelay', {'in': 'Byp_Select'}, props=[('maxStepSize', None, '5.0')])
    S.npoint('ChwLoop/Points', 'CHW_BypassValveCmd', 'Byp_RateLimit', 'pct', 1, kind='ao')
    S.param('CHW_BypassValveFeedback', 0.0, 'pct', folder='ChwLoop/Points', note='SIM INPUT (feedback emulated)'); S.meta['CHW_BypassValveFeedback'] = {'kind': 'ai', 'unit': 'pct'}
    S.kc(B, 'Byp_CmdMinusFb', 'Subtract', {'inA': 'CHW_BypassValveCmd', 'inB': 'CHW_BypassValveFeedback'})
    S.kc(B, 'Byp_Deviation', 'AbsValue', {'inA': 'Byp_CmdMinusFb'})
    S.kc(B, 'Byp_DeviationHigh', 'GreaterThan', {'inA': 'Byp_Deviation', 'inB': 'BypassMismatchPct'})
    S.kc(B, 'Byp_MismatchDelay', 'BooleanDelay', {'in': 'Byp_DeviationHigh'}, props=[('onDelay', 'b:RelTime', '120000'), ('offDelay', 'b:RelTime', '0')])

    # ------------------------------------------------------------ staging: failsafe stage-up on CHWS deviation (GPC36)
    ST = 'PlantControl/Staging'
    S.kc(ST, 'ChwstStageUpLimit', 'Add', {'inA': 'CHW_LeavingTemperatureSetpoint_ACTIVE', 'inB': 'StageUpTempMargin'})
    S.kc(ST, 'ChwsAboveStageUpLimit', 'GreaterThan', {'inA': 'CHWS', 'inB': 'ChwstStageUpLimit'})
    S.kc(ST, 'ChwsDeviationStageUp', 'BooleanDelay', {'in': 'ChwsAboveStageUpLimit'}, props=[('onDelay', 'b:RelTime', '600000'), ('offDelay', 'b:RelTime', '0')])
    S.kc(ST, 'Stage2LoadOrTemp', 'Or', {'inA': 'AutoStage2Hysteresis', 'inB': 'ChwsDeviationStageUp', 'inC': F, 'inD': F})
    S.rewire('Stage2Selected', 'inTrue', 'Stage2LoadOrTemp', 'AutoStage2Hysteresis')

    # ------------------------------------------------------------ energy KPIs (+ emulated power)
    E = 'Energy'
    for n, cmd, rated in (('CHP01', 'CHP01SpeedCmd', 'CHP_RatedKW'), ('CHP02', 'CHP02SpeedCmd', 'CHP_RatedKW'),
                          ('CDP01', 'CDP01SpeedCmd', 'CDP_RatedKW'), ('CDP02', 'CDP02SpeedCmd', 'CDP_RatedKW'),
                          ('CT01', 'CT01SpeedCmd', 'CT_RatedKW'), ('CT02', 'CT02SpeedCmd', 'CT_RatedKW')):
        S.kc('Simulation/Feedback', f'Sim_{n}_SpeedFrac', 'Divide', {'inA': cmd, 'inB': 'PlantReset_Full'})
        S.kc('Simulation/Feedback', f'Sim_{n}_kWCalc', 'Multiply', {'inA': f'Sim_{n}_SpeedFrac', 'inB': f'Sim_{n}_SpeedFrac', 'inC': f'Sim_{n}_SpeedFrac', 'inD': rated},
             note='Affinity law kW = rated x (speed)^3 — emulated meter')
        S.npoint(f'{n}/Points', f'{n}_kW', f'Sim_{n}_kWCalc', 'kW', 1, kind='ai_emul')
    for n in ('01', '02'):
        S.kc('Simulation/Feedback', f'Sim_CH{n}_LoadFrac', 'Divide', {'inA': f'CH{n}LoadPct', 'inB': 'PlantReset_Full'})
        S.kc('Simulation/Feedback', f'Sim_CH{n}_kWRunning', 'Multiply', {'inA': f'Sim_CH{n}_LoadFrac', 'inB': f'CH{n}_RatedKW'})
        S.kc('Simulation/Feedback', f'Sim_CH{n}_kWCalc', 'NumericSwitch', {'inSwitch': f'CH{n}RunProofSelected', 'inTrue': f'Sim_CH{n}_kWRunning', 'inFalse': 'ZeroSpeed'},
             note='Emulated chiller meter: load x rated kW while proven')
        S.npoint(f'Chiller{n}/Points', f'CH{n}_kW', f'Sim_CH{n}_kWCalc', 'kW', 1, kind='ai_emul')
    S.kc(E, 'PumpKWSum', 'Add', {'inA': 'CHP01_kW', 'inB': 'CHP02_kW', 'inC': 'CDP01_kW', 'inD': 'CDP02_kW'})
    S.kc(E, 'AuxKWSum', 'Add', {'inA': 'PumpKWSum', 'inB': 'CT01_kW', 'inC': 'CT02_kW'})
    S.kc(E, 'PlantKWSum', 'Add', {'inA': 'CH01_kW', 'inB': 'CH02_kW', 'inC': 'AuxKWSum'})
    S.npoint(E, 'Aux_kW', 'AuxKWSum', 'kW', 1)
    S.npoint(E, 'Plant_kW', 'PlantKWSum', 'kW', 1)
    S.kc(E, 'CoolingLoadRaw', 'Multiply', {'inA': 'CHWFlow', 'inB': 'CHWDeltaT', 'inC': 'Water_kW_Factor', 'inD': 'One'})
    S.kc(E, 'CoolingLoadKW', 'Limiter', {'inA': 'CoolingLoadRaw'}, props=[('inMin', None, '0.0'), ('inMax', None, '100000.0')])
    S.npoint(E, 'CoolingLoad_kW', 'CoolingLoadKW', 'kW', 1)
    S.kc(E, 'CoolingLoadRT', 'Divide', {'inA': 'CoolingLoadKW', 'inB': 'kW_per_RT'})
    S.npoint(E, 'CoolingLoad_RT', 'CoolingLoadRT', 'tR', 1)
    S.kc(E, 'KpiLoadGuard', 'Maximum', {'inA': 'CoolingLoadRT', 'inB': 'MinLoadForKpi'})
    S.kc(E, 'KpiKWperRT', 'Divide', {'inA': 'PlantKWSum', 'inB': 'KpiLoadGuard'})
    S.npoint(E, 'Plant_kW_per_RT', 'KpiKWperRT', 'none', 3)
    S.kc(E, 'KpiPowerGuard', 'Maximum', {'inA': 'PlantKWSum', 'inB': 'One'})
    S.kc(E, 'KpiCOP', 'Divide', {'inA': 'CoolingLoadKW', 'inB': 'KpiPowerGuard'})
    S.npoint(E, 'Plant_COP', 'KpiCOP', 'none', 2)

    # ------------------------------------------------------------ runtime totalizers (DiscreteTotalizerExt)
    for pt in ('Obs_CH01RunProofSelected', 'Obs_CH02RunProofSelected', 'CHP01RunProof', 'CHP02RunProof',
               'CDP01RunProof', 'CDP02RunProof', 'CT01RunProof', 'CT02RunProof'):
        add_ext(S, pt, 'Runtime', 'c:DiscreteTotalizerExt')
    # ------------------------------------------------------------ runtime based rotation (MELCO: depend on runtime)
    LL = 'PlantControl/LeadLag'
    S.bparam('RotationMode_Runtime', False, folder='PlantControl/Points', t='Runtime', f='Manual')
    S.kc(LL, 'CH01RuntimeHours', 'Divide', {'inA': 'Obs_CH01RunProofSelected:Runtime.elapsedActiveTimeNumeric', 'inB': 'MsPerHour'})
    S.kc(LL, 'CH02RuntimeHours', 'Divide', {'inA': 'Obs_CH02RunProofSelected:Runtime.elapsedActiveTimeNumeric', 'inB': 'MsPerHour'})
    S.kc(LL, 'RuntimeDiffHours', 'Subtract', {'inA': 'CH01RuntimeHours', 'inB': 'CH02RuntimeHours'})
    S.kc(LL, 'RuntimeImbalance', 'Hysteresis', {'in': 'RuntimeDiffHours'}, props=[('inLow', None, '-24.0'), ('inHigh', None, '24.0')],
         note='+24 h -> CH02 leads; -24 h -> CH01 leads (inHigh/inLow are fixed properties)')
    S.kc(LL, 'AutoRotationRequest', 'And', {'inA': 'RotationMode_Runtime', 'inB': 'RuntimeImbalance', 'inC': T, 'inD': T})
    S.kc(LL, 'RotationRequestFinal', 'Or', {'inA': 'RotationRequest', 'inB': 'AutoRotationRequest', 'inC': F, 'inD': F})
    S.rewire('RotatedLeadCH01', 'inSwitch', 'RotationRequestFinal', 'RotationRequest')
    S.npoint('Chiller01/Monitor', 'CH01_RuntimeHours', 'CH01RuntimeHours', 'hr', 1)
    S.npoint('Chiller02/Monitor', 'CH02_RuntimeHours', 'CH02RuntimeHours', 'hr', 1)
    # energy totals (NumericTotalizerExt, hourly -> kWh)
    for pt in ('Plant_kW', 'CH01_kW', 'CH02_kW', 'Aux_kW'):
        add_ext(S, pt, 'Energy', 'c:NumericTotalizerExt', [('totalizationInterval', None, 'hourly')])
        S.npoint('Energy', pt + 'h', f'{pt}:Energy.total', 'kWh', 1)

    # ------------------------------------------------------------ plant alarm logic (alarm-only points)
    A = 'Alarms'
    S.kc(A, 'PlantRunning30min', 'BooleanDelay', {'in': 'PlantRunRequest'}, props=[('onDelay', 'b:RelTime', '1800000'), ('offDelay', 'b:RelTime', '0')],
         note='MELCO: process alarms enabled 30 min after StartStopCmd false->true')
    S.kc(A, 'ProcessAlarmInhibit', 'Not', {'in': 'PlantRunning30min'})
    S.kc(A, 'AnyChillerProven', 'Or', {'inA': 'CH01RunProofSelected', 'inB': 'CH02RunProofSelected', 'inC': F, 'inD': F})
    S.kc(A, 'NoChillerProven', 'Not', {'in': 'AnyChillerProven'})
    S.kc(A, 'PlantNoChillerLogic', 'And', {'inA': 'PlantRunRequest', 'inB': 'NoChillerProven', 'inC': T, 'inD': T})
    S.kc(A, 'PlantNoChillerDelay', 'BooleanDelay', {'in': 'PlantNoChillerLogic'}, props=[('onDelay', 'b:RelTime', '900000'), ('offDelay', 'b:RelTime', '0')])
    S.bpoint(A, 'PlantStartStopMismatch', 'PlantNoChillerDelay', 'Alarm', 'Normal')
    S.kc(A, 'LowFlowLimit', 'Multiply', {'inA': 'Byp_MinFlowSum', 'inB': 'LowFlowRatio', 'inC': 'One', 'inD': 'One'})
    S.kc(A, 'ChwFlowBelowLimit', 'LessThan', {'inA': 'CHWFlow', 'inB': 'LowFlowLimit'})
    S.kc(A, 'ChwFlowLowLogic', 'And', {'inA': 'ChwFlowBelowLimit', 'inB': 'AnyChillerProven', 'inC': T, 'inD': T})
    S.kc(A, 'ChwFlowLowDelay', 'BooleanDelay', {'in': 'ChwFlowLowLogic'}, props=[('onDelay', 'b:RelTime', '120000'), ('offDelay', 'b:RelTime', '0')])
    S.bpoint(A, 'CHW_FlowLowAlarm', 'ChwFlowLowDelay', 'Alarm', 'Normal')
    S.kc(A, 'ChwstNotTrackLimit', 'Add', {'inA': 'CHW_LeavingTemperatureSetpoint_ACTIVE', 'inB': 'ChwstNotTrackingMargin'})
    S.kc(A, 'ChwsAboveTrackLimit', 'GreaterThan', {'inA': 'CHWS', 'inB': 'ChwstNotTrackLimit'})
    S.kc(A, 'ChwstNotTrackingLogic', 'And', {'inA': 'ChwsAboveTrackLimit', 'inB': 'PlantRunning30min', 'inC': T, 'inD': T})
    S.kc(A, 'ChwstNotTrackingDelay', 'BooleanDelay', {'in': 'ChwstNotTrackingLogic'}, props=[('onDelay', 'b:RelTime', '900000'), ('offDelay', 'b:RelTime', '0')])
    S.bpoint(A, 'CHWST_NotTrackingAlarm', 'ChwstNotTrackingDelay', 'Alarm', 'Normal')
    S.kc(A, 'CdsNotTrackLimit', 'Add', {'inA': 'CDS_Setpoint_ACTIVE', 'inB': 'CdsNotTrackingMargin'})
    S.kc(A, 'CdsAboveTrackLimit', 'GreaterThan', {'inA': 'CDS', 'inB': 'CdsNotTrackLimit'})
    S.kc(A, 'CdsNotTrackingLogic', 'And', {'inA': 'CdsAboveTrackLimit', 'inB': 'PlantRunning30min', 'inC': T, 'inD': T})
    S.kc(A, 'CdsNotTrackingDelay', 'BooleanDelay', {'in': 'CdsNotTrackingLogic'}, props=[('onDelay', 'b:RelTime', '1200000'), ('offDelay', 'b:RelTime', '0')])
    S.bpoint(A, 'CDS_NotTrackingAlarm', 'CdsNotTrackingDelay', 'Alarm', 'Normal')
    S.kc(A, 'LowDeltaTRunning', 'And', {'inA': 'LowDeltaT', 'inB': 'PlantRunning30min', 'inC': T, 'inD': T})
    S.kc(A, 'LowDeltaTDelay', 'BooleanDelay', {'in': 'LowDeltaTRunning'}, props=[('onDelay', 'b:RelTime', '900000'), ('offDelay', 'b:RelTime', '0')])
    S.bpoint(A, 'LowDeltaTAlarm', 'LowDeltaTDelay', 'Alarm', 'Normal')
    S.bpoint(A, 'CH01LockoutAlarm', 'CH01TimeoutLockout', 'Lockout', 'Normal')
    S.bpoint(A, 'CH02LockoutAlarm', 'CH02TimeoutLockout', 'Lockout', 'Normal')
    S.bpoint(A, 'CHW_BypassValvePositionMismatch', 'Byp_MismatchDelay', 'Mismatch', 'Normal')
    S.kc(A, 'OA_Invalid', 'Not', {'in': 'OA_ValidLogic'})
    S.bpoint(A, 'OA_SensorInvalidAlarm', 'OA_Invalid', 'Invalid', 'Normal')
    S.bpoint(A, 'LocalModeProlongedAlarm', 'LocalModeProlongedDelay', 'Alarm', 'Normal')
    S.bpoint(A, 'AiRequestedButLocalAlarm', 'AiRequestedButLocal', 'ForcedLocal', 'Normal')

    # ------------------------------------------------------------ simulation: feedback emulation + ramps
    SF = 'Simulation/Feedback'
    fb = []
    for eq in ('CHP01', 'CHP02', 'CDP01', 'CDP02', 'CT01', 'CT02'):
        S.kc(SF, f'Sim_{eq}_RunFb', 'BooleanDelay', {'in': f'{eq}StartCmd'}, props=[('onDelay', 'b:RelTime', '2000'), ('offDelay', 'b:RelTime', '1000')])
        fb.append((f'{eq}RunProof', f'Sim_{eq}_RunFb'))
    for n in ('01', '02'):
        S.kc(SF, f'Sim_CH{n}_RunFb', 'BooleanDelay', {'in': f'CH{n}StartCmd'}, props=[('onDelay', 'b:RelTime', '3000'), ('offDelay', 'b:RelTime', '1000')])
        S.kc(SF, f'Sim_CH{n}_ValveFb', 'BooleanDelay', {'in': f'CH{n}ValveOpenCmd'}, props=[('onDelay', 'b:RelTime', '2000'), ('offDelay', 'b:RelTime', '2000')])
        S.kc(SF, f'Sim_CH{n}_ChwFlowFb', 'And', {'inA': f'Sim_CH{n}_ValveFb', 'inB': f'Sim_CHP{n}_RunFb', 'inC': T, 'inD': T})
        S.kc(SF, f'Sim_CH{n}_CdwFlowFb', 'And', {'inA': f'Sim_CH{n}_ValveFb', 'inB': f'Sim_CDP{n}_RunFb', 'inC': T, 'inD': T})
        fb += [(f'CH{n}RunProof', f'Sim_CH{n}_RunFb'), (f'CH{n}ValveOpenProof', f'Sim_CH{n}_ValveFb'),
               (f'CH{n}CHWFlowProof', f'Sim_CH{n}_ChwFlowFb'), (f'CH{n}CDWFlowProof', f'Sim_CH{n}_CdwFlowFb')]
        S.set_fallback(f'CH{n}AutoProofEnabled', False)
    S.kc(SF, 'Sim_BypassValveFb', 'NumericDelay', {'in': 'CHW_BypassValveCmd'}, props=[('maxStepSize', None, '2.0')])
    fb.append(('CHW_BypassValveFeedback', 'Sim_BypassValveFb'))
    for tgt, src in fb:
        S.link(S.comp[tgt], src, 'in10')
        S.log.append(('SIMLINK', '', tgt, 'in10', src, 'emulated feedback'))
    SR = 'Simulation/Ramps'
    ramps = [  # point, type, period ms, amplitude, offset  (Ramp triangle / SineWave: offset +/- amplitude)
        ('OA_Temperature', 'SineWave', 1800000, 4.0, 31.0), ('OA_Humidity', 'Ramp', 2400000, 20.0, 70.0),
        ('PlantLoadPct', 'Ramp', 3600000, 60.0, 80.0), ('CHWS', 'SineWave', 1200000, 0.8, 7.3),
        ('CHWR', 'SineWave', 1500000, 1.5, 12.0), ('CHWFlow', 'Ramp', 2700000, 90.0, 150.0),
        ('CHWDP', 'SineWave', 900000, 40.0, 120.0), ('CDS', 'SineWave', 1800000, 2.0, 30.0),
        ('CDR', 'SineWave', 1800000, 2.0, 35.0), ('CH01LoadPct', 'Ramp', 2400000, 40.0, 55.0),
        ('CH02LoadPct', 'Ramp', 3000000, 40.0, 55.0)]
    for pt, typ, per, amp, off in ramps:
        props = [('period', None, str(per)), ('amplitude', None, repr(amp)), ('offset', None, repr(off))]
        if typ == 'Ramp': props.append(('waveform', None, 'triangle'))
        props.append(('facets', 'b:Facets', U[S.meta.get(pt, {}).get('unit', 'none')] + '|precision=i:1|min=d:-inf|max=d:+inf'))
        S.kc(SR, f'Ramp_{pt}', typ, props=props, note=f'{off - amp:g} .. {off + amp:g}, period {per / 60000:g} min')
        S.link(S.comp[pt], f'Ramp_{pt}', 'in10')
        S.log.append(('SIMLINK', '', pt, 'in10', f'Ramp_{pt}', 'ramp up/down'))
        S.meta.setdefault(pt, {})['ramp'] = f'{typ} {off - amp:g}..{off + amp:g} / {per / 60000:g} min'
    # AI write emulation: heartbeat step every 5 min (Counter) + AI setpoints ramping inside their AI ranges
    S.bparam('Sim_AiHeartbeatEnable', True, folder=SR, t='Beating', f='Stopped', note='false = emulate AI heartbeat loss')
    S.kc(SR, 'Sim_AiBeatClock', 'MultiVibrator', props=[('period', None, '295000'), ('dutyCycle', None, '50.0')])
    S.kc(SR, 'Sim_AiBeatGate', 'And', {'inA': 'Sim_AiBeatClock', 'inB': 'Sim_AiHeartbeatEnable', 'inC': 'ConstantTrue', 'inD': 'ConstantTrue'})
    S.kc(SR, 'Sim_AiBeatCounter', 'Counter', {'countUp': 'Sim_AiBeatGate'}, note='new heartbeat value every 5 min')
    S.link(S.comp['HeartbeatTimestampSetpoint'], 'Sim_AiBeatCounter', 'in10')
    S.log.append(('SIMLINK', '', 'HeartbeatTimestampSetpoint', 'in10', 'Sim_AiBeatCounter', 'AI heartbeat emulation'))
    S.meta['HeartbeatTimestampSetpoint']['ramp'] = 'Counter +1 every 5 min (Sim_AiHeartbeatEnable)'
    ai_ramps = [('CHW_LeavingTemperatureSetpoint_AI', 'Ramp', 3600000, 1.0, 8.0), ('CHWDP_Setpoint_AI', 'Ramp', 3600000, 35.0, 105.0),
                ('CDS_Setpoint_AI', 'Ramp', 3600000, 2.5, 28.5)]
    for pt, typ, per, amp, off in ai_ramps:
        props = [('period', None, str(per)), ('amplitude', None, repr(amp)), ('offset', None, repr(off)), ('waveform', None, 'triangle'),
                 ('facets', 'b:Facets', U[S.meta.get(pt, {}).get('unit', 'none')] + '|precision=i:1|min=d:-inf|max=d:+inf')]
        S.kc(SR, f'Ramp_{pt}', typ, props=props, note=f'AI write emulation {off - amp:g} .. {off + amp:g}')
        S.link(S.comp[pt], f'Ramp_{pt}', 'in10')
        S.log.append(('SIMLINK', '', pt, 'in10', f'Ramp_{pt}', 'AI write emulation'))
        S.meta.setdefault(pt, {})['ramp'] = f'{typ} {off - amp:g}..{off + amp:g} / {per / 60000:g} min'
    ramps = ramps + ai_ramps
    return ramps, fb


# ============================================================ V6.2 fail-safe layer ("plant must not go dark")
def remove_comp(S, name):
    S.comp.pop(name); S.folder_of.pop(name, None); S.meta.pop(name, None)
    S.log.append(('REMOVE', '', name, '', '', 'replaced by V6.2 fail-safe logic'))


def failsafe(S):
    T, F = 'ConstantTrue', 'ConstantFalse'
    P_ = 'Parameters'
    S.bparam('CH_AutoRetryEnable', True, t='Enabled', f='Disabled', note='Program lockout auto-reset after 180 s')
    S.param('CH_MaxAutoRetries', 3.0, 'none', prec=0, note='Auto-resets before manual reset is required')
    S.bparam('BootAutoQualifyEnable', True, t='Enabled', f='Disabled', note='Auto qualify 120 s after station start (no manual QUALIFY)')
    S.param('CHP_FailSafeSpeed', 80.0, 'pct', note='CHW pump speed when DP sensor invalid')
    S.param('CT_FailSafeSpeed', 80.0, 'pct', note='Tower fan speed when CDS sensor invalid')
    S.param('Byp_FailSafePosition', 20.0, 'pct', note='Bypass position when CHW flow sensor invalid')
    S.param('CHWDP_MinValid', 5.0, 'kPa'); S.param('CHWDP_MaxValid', 400.0, 'kPa')
    S.param('CHWFlow_MinValid', 0.0, 'm3h'); S.param('CHWFlow_MaxValid', 2000.0, 'm3h')

    # ---- 1. boot: auto qualification (a station restart must not leave the plant off)
    R = 'PlantControl/Restart'
    S.kc(R, 'BootAutoQualifyDelay', 'BooleanDelay', {'in': 'BootFreshEdgeLatch'}, props=[('onDelay', 'b:RelTime', '120000'), ('offDelay', 'b:RelTime', '0')],
         note='120 s after the boot oscillator proves the station is executing')
    S.kc(R, 'BootAutoQualified', 'And', {'inA': 'BootAutoQualifyDelay', 'inB': 'BootAutoQualifyEnable', 'inC': T, 'inD': T})
    S.kc(R, 'BootQualifiedEffective', 'Or', {'inA': 'BootQualified', 'inB': 'BootAutoQualified', 'inC': F, 'inD': F})
    S.rewire('BootEpochQualifiedProbe', 'inA', 'BootQualifiedEffective', 'BootQualified')
    S.rewire('BootEpochLatchProbe', 'clock', 'BootQualifiedEffective', 'BootQualified')

    # ---- 2. plant permissive: sensor or comms faults alarm but never stop a running plant
    S.rewire('PlantPermissive', 'inB', T, 'SensorReady')
    S.rewire('PlantReady', 'inD', T, 'CommunicationHealthy')

    # ---- 3. sensor fail-safe per control loop
    SV = 'PlantControl/SensorValidation'
    S.kc(SV, 'CHWSValid', 'And', {'inA': 'CHWSRangeValid', 'inB': 'CHWSSensorHealthy', 'inC': T, 'inD': T})
    S.kc(SV, 'CDSValid', 'And', {'inA': 'CDSRangeValid', 'inB': 'CDSSensorHealthy', 'inC': T, 'inD': T})
    S.kc(SV, 'CHWDPAboveMin', 'GreaterThanEqual', {'inA': 'CHWDP', 'inB': 'CHWDP_MinValid'})
    S.kc(SV, 'CHWDPBelowMax', 'LessThanEqual', {'inA': 'CHWDP', 'inB': 'CHWDP_MaxValid'})
    S.kc(SV, 'CHWDPValid', 'And', {'inA': 'CHWDPAboveMin', 'inB': 'CHWDPBelowMax', 'inC': T, 'inD': T})
    S.kc(SV, 'CHWFlowAboveMin', 'GreaterThanEqual', {'inA': 'CHWFlow', 'inB': 'CHWFlow_MinValid'})
    S.kc(SV, 'CHWFlowBelowMax', 'LessThanEqual', {'inA': 'CHWFlow', 'inB': 'CHWFlow_MaxValid'})
    S.kc(SV, 'CHWFlowValid', 'And', {'inA': 'CHWFlowAboveMin', 'inB': 'CHWFlowBelowMax', 'inC': T, 'inD': T})
    S.kc('ChwLoop/DpControl', 'CHWDP_FailSafeSelect', 'NumericSwitch', {'inSwitch': 'CHWDPValid', 'inTrue': 'CHWDP_Clamp', 'inFalse': 'CHP_FailSafeSpeed'},
         note='DP sensor invalid -> fixed pump speed')
    S.rewire('CHWDP_SafeSelect', 'inTrue', 'CHWDP_FailSafeSelect', 'CHWDP_Clamp')
    S.kc('CdwLoop/TowerControl', 'CDS_FailSafeSelect', 'NumericSwitch', {'inSwitch': 'CDSValid', 'inTrue': 'CDS_Clamp', 'inFalse': 'CT_FailSafeSpeed'},
         note='CDS sensor invalid -> fixed fan speed')
    S.rewire('CDS_SafeSelect', 'inTrue', 'CDS_FailSafeSelect', 'CDS_Clamp')
    S.kc('ChwLoop/MinFlowBypass', 'Byp_FailSafeSelect', 'NumericSwitch', {'inSwitch': 'CHWFlowValid', 'inTrue': 'Byp_PID', 'inFalse': 'Byp_FailSafePosition'},
         note='Flow sensor invalid -> fixed bypass opening')
    S.rewire('Byp_Select', 'inTrue', 'Byp_FailSafeSelect', 'Byp_PID')
    A = 'Alarms'
    for pt, src in (('CHWS_SensorInvalidAlarm', 'CHWSValid'), ('CDS_SensorInvalidAlarm', 'CDSValid'),
                    ('CHWDP_SensorInvalidAlarm', 'CHWDPValid'), ('CHWFlow_SensorInvalidAlarm', 'CHWFlowValid')):
        S.kc(A, 'Not' + src, 'Not', {'in': src})
        S.bpoint(A, pt, 'Not' + src, 'Invalid', 'Normal')

    # ---- 4. reset commands (momentary: Px buttons invoke the OneShot 'fire' action)
    S.kc(A, 'PlantAlarmResetFire', 'OneShot', props=[('time', 'b:RelTime', '2000')],
         note='Px RESET PROGRAM ALARMS -> action fire (resets both lockouts + retry counters)')

    for n in ('01', '02'):
        FL = f'Chiller{n}/Fault'
        # proof freshness no longer depends on a start-up edge (BLatch ignores edges before it runs -> deadlock + lockout)
        S.rewire(f'CH{n}ProofArmed', 'inA', T, f'CH{n}ProofSeenFalse')
        S.kc(FL, f'CH{n}ResetFire', 'OneShot', props=[('time', 'b:RelTime', '2000')], note='Px chiller RESET -> action fire')
        S.kc(FL, f'CH{n}LockoutTrip', 'Or', {'inA': f'CH{n}StartTimeoutDelay', 'inB': f'CH{n}AuxProofTimeout', 'inC': F, 'inD': F})
        S.kc(FL, f'CH{n}AutoRetryArm', 'And', {'inA': f'CH{n}TimeoutLockout', 'inC': 'CH_AutoRetryEnable', 'inD': T})   # inB linked below (loop)
        S.kc(FL, f'CH{n}AutoRetryDelay', 'BooleanDelay', {'in': f'CH{n}AutoRetryArm'}, props=[('onDelay', 'b:RelTime', '180000'), ('offDelay', 'b:RelTime', '0')])
        S.kc(FL, f'CH{n}AutoRetryPulse', 'OneShot', {'in': f'CH{n}AutoRetryDelay'}, props=[('time', 'b:RelTime', '2000')])
        S.kc(FL, f'CH{n}ManualReset', 'Or', {'inA': f'CH{n}ResetPulse', 'inB': f'CH{n}ResetFire', 'inC': 'PlantAlarmResetFire', 'inD': F})
        S.kc(FL, f'CH{n}ResetAny', 'Or', {'inA': f'CH{n}ManualReset', 'inB': f'CH{n}AutoRetryPulse', 'inC': F, 'inD': F})
        S.kc(FL, f'CH{n}NotResetAny', 'Not', {'in': f'CH{n}ResetAny'})
        S.kc(FL, f'CH{n}LockoutHold', 'And', {'inA': f'CH{n}TimeoutLockout', 'inB': f'CH{n}NotResetAny', 'inC': T, 'inD': T})
        # CHnTimeoutLockout: BooleanLatch -> seal-in Or (same handle/name; order-independent set/reset)
        el = S.comp[f'CH{n}TimeoutLockout']
        for c in list(el): el.remove(c)
        el.set('t', 'kitControl:Or')
        for tslot, src in (('inA', f'CH{n}LockoutTrip'), ('inB', f'CH{n}LockoutHold'), ('inC', F), ('inD', F)):
            S.link(el, src, tslot)
        S.log.append(('RETYPE', FL, f'CH{n}TimeoutLockout', 'BooleanLatch->Or', 'seal-in: Trip OR (Lockout AND NOT Reset)', ''))
        for old in (f'CH{n}LockoutClock', f'CH{n}NotLockoutReset'):
            remove_comp(S, old)
        # retry bookkeeping
        S.kc(FL, f'CH{n}RunStable', 'BooleanDelay', {'in': f'CH{n}StartSuccess'}, props=[('onDelay', 'b:RelTime', '1800000'), ('offDelay', 'b:RelTime', '0')])
        S.kc(FL, f'CH{n}RetryClear', 'Or', {'inA': f'CH{n}RunStable', 'inB': f'CH{n}ManualReset', 'inC': F, 'inD': F})
        S.kc(FL, f'CH{n}RetryCounter', 'Counter', {'countUp': f'CH{n}AutoRetryPulse', 'clearIn': f'CH{n}RetryClear'})
        S.kc(FL, f'CH{n}RetriesLeft', 'LessThan', {'inA': f'CH{n}RetryCounter', 'inB': 'CH_MaxAutoRetries'})
        S.link(S.comp[f'CH{n}AutoRetryArm'], f'CH{n}RetriesLeft', 'inB')
        S.kc(FL, f'CH{n}NoRetriesLeft', 'Not', {'in': f'CH{n}RetriesLeft'})
        S.kc(FL, f'CH{n}HardLockoutLogic', 'And', {'inA': f'CH{n}TimeoutLockout', 'inB': f'CH{n}NoRetriesLeft', 'inC': T, 'inD': T})
        S.npoint(f'Chiller{n}/Monitor', f'CH{n}_AutoRetryCount', f'CH{n}RetryCounter', 'none', 0)
        S.bpoint(A, f'CH{n}HardLockoutAlarm', f'CH{n}HardLockoutLogic', 'ManualReset', 'Normal')

    # ---- 5. plant-level: no chiller can run while the plant is requested
    S.kc(A, 'NotCH01TrainHealthy', 'Not', {'in': 'CH01TrainHealthy'})
    S.kc(A, 'AllChillersUnavailableLogic', 'And', {'inA': 'PlantRunRequest', 'inB': 'NotCH01TrainHealthy', 'inC': 'NotCH02TrainHealthy', 'inD': T})
    S.kc(A, 'AllChillersUnavailableDelay', 'BooleanDelay', {'in': 'AllChillersUnavailableLogic'}, props=[('onDelay', 'b:RelTime', '30000'), ('offDelay', 'b:RelTime', '0')])
    S.bpoint(A, 'AllChillersUnavailableAlarm', 'AllChillersUnavailableDelay', 'Alarm', 'Normal')


# ============================================================ V6.3 logic completion
# Timer profiles: 'site' = commissioning defaults for real equipment (PROJECT/OEM to confirm);
# 'fpt' = the compressed V4 test timings, used only to re-run the V4/V5 regression suite.
TIMING = {
    'site': dict(start_timeout=180000, aux_timeout=60000, min_off=180000, min_run=900000, post_run=120000,
                 sim_ch=45000, sim_valve=15000, sim_aux_on=5000, sim_aux_off=3000,
                 stage_up=600000, stage_down=900000, overload=600000, stage_hi=90.0, stage_lo=60.0),
    'fpt': dict(start_timeout=5000, aux_timeout=10000, min_off=2000, min_run=5000, post_run=5000,
                sim_ch=3000, sim_valve=2000, sim_aux_on=2000, sim_aux_off=1000,
                stage_up=0, stage_down=0, overload=600000, stage_hi=70.0, stage_lo=40.0),
}


def schedule_el(S, name, weekly=None, special_day1=None):
    """sch:BooleanSchedule built on the structure of the working ST5130 schedule (Sch_Reset1).
    weekly=(start, finish) -> every weekday true in that window; special_day1=(start, finish) -> day 1 of every month."""
    el = ET.Element('p', {'n': name, 'h': S.h(), 't': 'sch:BooleanSchedule'})   # 'sch' declared once in main()
    P(el, 'cleanupExpiredEvents', v='false')
    def date_sched(parent, n, day=None):
        d = P(parent, n, 'sch:DateSchedule', h=S.h())
        y = P(d, 'yearSchedule', 'sch:YearSchedule', h=S.h()); P(y, 'alwaysEffective', v='true')
        mo = P(d, 'monthSchedule', 'sch:MonthSchedule', h=S.h())      # empty set = any month
        P(mo, 'singleSelection', v='true')
        dm = P(d, 'daySchedule', 'sch:DayOfMonthSchedule', h=S.h())
        if day: P(dm, 'set', 'b:EnumSet', str(day))
        P(dm, 'singleSelection', v='true')
        w = P(d, 'weekdaySchedule', 'sch:WeekdaySchedule', h=S.h()); P(w, 'singleSelection', v='true')
        return d
    def day_sched(parent, window):
        dy = P(parent, 'day', 'sch:DaySchedule', h=S.h())
        if window:
            ts = P(dy, 'time', 'sch:TimeSchedule', h=S.h())
            P(ts, 'start', 'b:Time', window[0]); P(ts, 'finish', 'b:Time', window[1])
            ev = P(ts, 'effectiveValue', 'b:StatusBoolean', f='o'); P(ev, 'value', v='true')
    eff = P(el, 'effective', 'sch:DateRangeSchedule', h=S.h())
    date_sched(eff, 'start'); date_sched(eff, 'end')
    sc = P(el, 'schedule', 'sch:CompositeSchedule', h=S.h())
    sp = P(sc, 'specialEvents', 'sch:CompositeSchedule', h=S.h())
    if special_day1:
        ev = P(sp, 'MonthStart', 'sch:DailySchedule', h=S.h())
        day_sched(ev, special_day1)
        date_sched(ev, 'days', day=1)
    wk = P(sc, 'week', 'sch:WeekSchedule', h=S.h())
    for i, dn in enumerate(('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')):
        d = P(wk, dn, 'sch:DailySchedule', h=S.h())
        day_sched(d, weekly)
        ws = P(d, 'days', 'sch:WeekdaySchedule', h=S.h()); P(ws, 'set', 'b:EnumSet', str(i))
    return el


def complete_logic(S, prof):
    T, F = 'ConstantTrue', 'ConstantFalse'
    # ---- 1. realistic sequence timers (profile)
    for n in ('01', '02'):
        S.set_prop(f'CH{n}StartTimeoutDelay', 'onDelay', str(prof['start_timeout']))
        S.set_prop(f'CH{n}AuxProofTimeout', 'onDelay', str(prof['aux_timeout']))
        S.set_prop(f'CH{n}MinOffDelay', 'onDelay', str(prof['min_off']))
        S.set_prop(f'CH{n}MinRunDelay', 'onDelay', str(prof['min_run']))
        S.set_prop(f'CH{n}PostRun', 'offDelay', str(prof['post_run']))
        S.set_prop(f'Sim_CH{n}_RunFb', 'onDelay', str(prof['sim_ch']))
        S.set_prop(f'Sim_CH{n}_ValveFb', 'onDelay', str(prof['sim_valve'])); S.set_prop(f'Sim_CH{n}_ValveFb', 'offDelay', str(prof['sim_valve']))
        for eq in ('CHP', 'CDP', 'CT'):
            S.set_prop(f'Sim_{eq}{n}_RunFb', 'onDelay', str(prof['sim_aux_on'])); S.set_prop(f'Sim_{eq}{n}_RunFb', 'offDelay', str(prof['sim_aux_off']))

    # ---- 2. staging on measured plant load (% of ONE chiller) with timers + lead-chiller overload
    S.param('CH_RatedRT', 300.0, 'tR', note='Nameplate capacity per chiller (PROJECT/OEM)')
    S.param('Hundred', 100.0, 'none', prec=0)
    S.param('StageDownChillerSumPct', 80.0, 'pct', note='CH01 + CH02 load below this -> lag not needed (overload stage only)')
    S.param('LeadOverloadPct', 95.0, 'pct', note='Lead chiller load for stage-up when load calc is unavailable')
    ST = 'PlantControl/Staging'
    S.kc(ST, 'PlantLoadRatio', 'Divide', {'inA': 'CoolingLoad_RT', 'inB': 'CH_RatedRT'})
    S.kc(ST, 'PlantLoadCalcPct', 'Multiply', {'inA': 'PlantLoadRatio', 'inB': 'Hundred', 'inC': 'One', 'inD': 'One'})
    S.kc(ST, 'PlantLoadCalc', 'Limiter', {'inA': 'PlantLoadCalcPct'}, props=[('inMin', None, '0.0'), ('inMax', None, '200.0')],
         note='PlantLoadPct basis = % of ONE chiller (can reach 200 %)')
    S.link(S.comp['PlantLoadPct'], 'PlantLoadCalc', 'in16')
    S.set_prop('AutoStage2Hysteresis', 'inHigh', repr(prof['stage_hi'])); S.set_prop('AutoStage2Hysteresis', 'inLow', repr(prof['stage_lo']))
    S.kc(ST, 'StageLoadTimer', 'BooleanDelay', {'in': 'AutoStage2Hysteresis'},
         props=[('onDelay', 'b:RelTime', str(prof['stage_up'])), ('offDelay', 'b:RelTime', str(prof['stage_down']))],
         note='Stage-up after load high 10 min, stage-down after load low 15 min (anti short-cycle)')
    S.rewire('Stage2LoadOrTemp', 'inA', 'StageLoadTimer', 'AutoStage2Hysteresis')
    S.kc(ST, 'LeadChillerLoad', 'NumericSwitch', {'inSwitch': 'EffectiveLeadCH01', 'inTrue': 'CH01LoadPct', 'inFalse': 'CH02LoadPct'})
    S.kc(ST, 'LeadOverload', 'GreaterThan', {'inA': 'LeadChillerLoad', 'inB': 'LeadOverloadPct'})
    S.kc(ST, 'LeadOverloadRunning', 'And', {'inA': 'LeadOverload', 'inB': 'AnyChillerProven', 'inC': T, 'inD': T})
    S.kc(ST, 'LeadOverloadDelay', 'BooleanDelay', {'in': 'LeadOverloadRunning'}, props=[('onDelay', 'b:RelTime', str(prof['overload'])), ('offDelay', 'b:RelTime', '0')])
    # overload-initiated stage 2 is held until the two chillers together carry < 80 % of one chiller (then one can take it)
    S.kc(ST, 'ChillerLoadSum', 'Add', {'inA': 'CH01LoadPct', 'inB': 'CH02LoadPct'})
    S.kc(ST, 'LagNotNeeded', 'LessThan', {'inA': 'ChillerLoadSum', 'inB': 'StageDownChillerSumPct'})
    S.kc(ST, 'LagNotNeededDelay', 'BooleanDelay', {'in': 'LagNotNeeded'}, props=[('onDelay', 'b:RelTime', str(prof['stage_down'])), ('offDelay', 'b:RelTime', '0')])
    S.kc(ST, 'NotLowLoadDelay', 'Not', {'in': 'LagNotNeededDelay'})
    S.kc(ST, 'Stage2Overload', 'Or', {'inA': 'LeadOverloadDelay', 'inC': F, 'inD': F})
    S.kc(ST, 'Stage2OverloadHold', 'And', {'inA': 'Stage2Overload', 'inB': 'NotLowLoadDelay', 'inC': T, 'inD': T})
    S.link(S.comp['Stage2Overload'], 'Stage2OverloadHold', 'inB')          # seal-in until load is low
    S.rewire('Stage2LoadOrTemp', 'inC', 'Stage2Overload', 'ConstantFalse')

    # ---- 3. cooling tower low-temperature protection (fan to 0 % below 21 degC, back above 23 degC)
    TC = 'CdwLoop/TowerControl'
    S.kc(TC, 'CdsAboveLowLimit', 'Hysteresis', {'in': 'CDS'}, props=[('inLow', None, '21.0'), ('inHigh', None, '23.0')])
    S.kc(TC, 'CdsBelowLowLimit', 'Not', {'in': 'CdsAboveLowLimit'})
    S.kc(TC, 'CdsLowCutout', 'And', {'inA': 'CdsBelowLowLimit', 'inB': 'CDSValid', 'inC': T, 'inD': T})
    S.kc(TC, 'CDS_LowTempSelect', 'NumericSwitch', {'inSwitch': 'CdsLowCutout', 'inTrue': 'ZeroSpeed', 'inFalse': 'CDS_FailSafeSelect'})
    S.rewire('CDS_SafeSelect', 'inTrue', 'CDS_LowTempSelect', 'CDS_FailSafeSelect')
    S.bpoint('CdwLoop/Monitor', 'CT_LowTempCutout', 'CdsLowCutout', 'Cutout', 'Normal')

    # ---- 4. operating schedule (optional; manual PlantEnable stays the master switch)
    E0 = 'PlantControl/Enable'
    S.bparam('PlantScheduleMode', False, folder='PlantControl/Points', t='Schedule', f='Manual', note='true = plant follows PlantSchedule')
    sch = schedule_el(S, 'PlantSchedule', weekly=('07:00:00.000', '19:00:00.000'))
    S.comp['PlantSchedule'] = sch; S.folder_of['PlantSchedule'] = E0
    S.log.append(('ADD', E0, 'PlantSchedule', 'sch:BooleanSchedule', 'Mon-Sun 07:00-19:00', 'edit in Workbench Scheduler view'))
    S.kc(E0, 'ScheduleNotRequired', 'Not', {'in': 'PlantScheduleMode'})
    S.kc(E0, 'ScheduleOk', 'Or', {'inA': 'ScheduleNotRequired', 'inB': 'PlantSchedule', 'inC': F, 'inD': F})
    S.kc(E0, 'PlantEnableEffective', 'And', {'inA': 'PlantEnable', 'inB': 'ScheduleOk', 'inC': T, 'inD': T})
    S.rewire('PlantReady', 'inA', 'PlantEnableEffective', 'PlantEnable')

    # ---- 5. energy periods: today / yesterday / month / last month (+ kW/RT, cost, CO2, savings)
    E = 'Energy'
    S.param('Tariff_THB_per_kWh', 4.18, 'none', prec=2, note='Blended tariff (PROJECT)')
    S.param('CO2_kg_per_kWh', 0.4999, 'none', prec=4, note='Thailand grid emission factor (TGO) - confirm current value')
    S.param('Baseline_kW_per_RT', 0.85, 'none', prec=3, note='Baseline plant efficiency for savings (PROJECT M&V)')
    for n_, v_ in (('DayStartTrigger', '00:00:00.000;7f;0'), ('DayEndTrigger', '23:59:59.000;7f;0')):
        S.add(E, n_, 'c:TimeTrigger', props=[('triggerMode', 'c:DailyTriggerMode', v_)], note='fireTrigger -> action links')
    msch = schedule_el(S, 'MonthStartSchedule', special_day1=('00:02:00.000', '00:03:00.000'))
    S.comp['MonthStartSchedule'] = msch; S.folder_of['MonthStartSchedule'] = E
    S.log.append(('ADD', E, 'MonthStartSchedule', 'sch:BooleanSchedule', 'day 1 00:02-00:03', 'month rollover'))
    S.kc(E, 'MonthResetDelay', 'BooleanDelay', {'in': 'MonthStartSchedule'}, props=[('onDelay', 'b:RelTime', '30000'), ('offDelay', 'b:RelTime', '0')],
         note='month-start latch at 00:02:30, after the last-month latches at 00:02')
    # ONE totalizer per point (BPointExtension.isSiblingLegal forbids two of the same type): periods = cumulative - latched start
    add_ext(S, 'CoolingLoad_RT', 'Energy', 'c:NumericTotalizerExt', [('totalizationInterval', None, 'hourly')])
    S.npoint(E, 'Cooling_RTh', 'CoolingLoad_RT:Energy.total', 'none', 1)
    for base, unit in (('Plant_kWh', 'kWh'), ('Aux_kWh', 'kWh'), ('Cooling_RTh', 'none')):
        S.kc(E, f'{base}_DayStartLatch', 'NumericLatch', {'in': base}, note='latched by DayStartTrigger 00:00 (action link)')
        S.link(S.comp[f'{base}_DayStartLatch'], 'DayStartTrigger.fireTrigger', 'latch')
        S.kc(E, f'{base}_TodayCalc', 'Subtract', {'inA': base, 'inB': f'{base}_DayStartLatch'})
        S.npoint(E, f'{base}_Today', f'{base}_TodayCalc', unit, 1)
        S.kc(E, f'{base}_YesterdayLatch', 'NumericLatch', {'in': f'{base}_Today'}, note='latched by DayEndTrigger 23:59:59')
        S.link(S.comp[f'{base}_YesterdayLatch'], 'DayEndTrigger.fireTrigger', 'latch')
        S.npoint(E, f'{base}_Yesterday', f'{base}_YesterdayLatch', unit, 1)
        S.kc(E, f'{base}_MonthStartLatch', 'NumericLatch', {'in': base, 'clock': 'MonthResetDelay'}, note='00:02:30 on day 1')
        S.kc(E, f'{base}_MonthCalc', 'Subtract', {'inA': base, 'inB': f'{base}_MonthStartLatch'})
        S.npoint(E, f'{base}_Month', f'{base}_MonthCalc', unit, 1)
        S.kc(E, f'{base}_LastMonthLatch', 'NumericLatch', {'in': f'{base}_Month', 'clock': 'MonthStartSchedule'}, note='00:02 on day 1, before the month restarts')
        S.npoint(E, f'{base}_LastMonth', f'{base}_LastMonthLatch', unit, 1)
    for per in ('Today', 'Yesterday', 'Month', 'LastMonth'):
        S.kc(E, f'RThGuard_{per}', 'Maximum', {'inA': f'Cooling_RTh_{per}', 'inB': 'One'})
        S.kc(E, f'KwPerRT_{per}Calc', 'Divide', {'inA': f'Plant_kWh_{per}', 'inB': f'RThGuard_{per}'})
        S.npoint(E, f'Plant_kW_per_RT_{per}', f'KwPerRT_{per}Calc', 'none', 3)
        S.kc(E, f'Cost_{per}Calc', 'Multiply', {'inA': f'Plant_kWh_{per}', 'inB': 'Tariff_THB_per_kWh'})
        S.npoint(E, f'Energy_Cost_THB_{per}', f'Cost_{per}Calc', 'none', 0)
        S.kc(E, f'CO2_{per}Calc', 'Multiply', {'inA': f'Plant_kWh_{per}', 'inB': 'CO2_kg_per_kWh'})
        S.npoint(E, f'CO2_kg_{per}', f'CO2_{per}Calc', 'none', 0)
    for per in ('Month', 'LastMonth'):
        S.kc(E, f'Baseline_{per}Calc', 'Multiply', {'inA': f'Cooling_RTh_{per}', 'inB': 'Baseline_kW_per_RT'})
        S.kc(E, f'Saving_{per}Calc', 'Subtract', {'inA': f'Baseline_{per}Calc', 'inB': f'Plant_kWh_{per}'})
        S.npoint(E, f'Saving_kWh_{per}', f'Saving_{per}Calc', 'kWh', 0)
        S.kc(E, f'SavingTHB_{per}Calc', 'Multiply', {'inA': f'Saving_kWh_{per}', 'inB': 'Tariff_THB_per_kWh'})
        S.npoint(E, f'Saving_THB_{per}', f'SavingTHB_{per}Calc', 'none', 0)


# ============================================================ instrumentation policy
ALARM_CLASSES = [('Emergency', 'toOffnormal=10;toFault=10;toNormal=200;toAlert=10;', None),
                 ('Critical', 'toOffnormal=50;toFault=50;toNormal=200;toAlert=50;', None),
                 ('Warning', 'toOffnormal=150;toFault=150;toNormal=200;toAlert=150;', None),
                 ('Info', 'toOffnormal=250;toFault=250;toNormal=250;toAlert=250;', '0')]
COS = {  # point: (alarmValue, class, offnormal text)
    'CH01Fault': (True, 'Critical', 'Chiller 01 fault'), 'CH02Fault': (True, 'Critical', 'Chiller 02 fault'),
    'CHP01Fault': (True, 'Warning', 'CHP01 fault'), 'CHP02Fault': (True, 'Warning', 'CHP02 fault'),
    'CDP01Fault': (True, 'Warning', 'CDP01 fault'), 'CDP02Fault': (True, 'Warning', 'CDP02 fault'),
    'CT01Fault': (True, 'Warning', 'CT01 fault'), 'CT02Fault': (True, 'Warning', 'CT02 fault'),
    'CommunicationHealthy': (False, 'Warning', 'Field communication fault - plant kept running'),
    'PlantStartStopMismatch': (True, 'Emergency', 'Plant commanded but no chiller proven (15 min)'),
    'CHW_FlowLowAlarm': (True, 'Emergency', 'CHW flow below safe minimum'),
    'CHWST_NotTrackingAlarm': (True, 'Critical', 'CHWS above setpoint + margin for 15 min'),
    'CDS_NotTrackingAlarm': (True, 'Warning', 'CDW supply above tower setpoint + margin for 20 min (tower capacity/control)'),
    'LowDeltaTAlarm': (True, 'Warning', 'Low CHW delta-T for 15 min'),
    'CH01LockoutAlarm': (True, 'Warning', 'Chiller 01 program lockout (auto-retry pending)'), 'CH02LockoutAlarm': (True, 'Warning', 'Chiller 02 program lockout (auto-retry pending)'),
    'CH01HardLockoutAlarm': (True, 'Critical', 'Chiller 01 lockout - auto-retries used, press RESET'), 'CH02HardLockoutAlarm': (True, 'Critical', 'Chiller 02 lockout - auto-retries used, press RESET'),
    'AllChillersUnavailableAlarm': (True, 'Emergency', 'Plant requested but no chiller train available'),
    'CHWS_SensorInvalidAlarm': (True, 'Critical', 'CHWS sensor invalid - temperature staging degraded'),
    'CDS_SensorInvalidAlarm': (True, 'Warning', 'CDS sensor invalid - tower fans at fail-safe speed'),
    'CHWDP_SensorInvalidAlarm': (True, 'Warning', 'CHW DP sensor invalid - pumps at fail-safe speed'),
    'CHWFlow_SensorInvalidAlarm': (True, 'Warning', 'CHW flow sensor invalid - bypass at fail-safe position'),

    'CHW_BypassValvePositionMismatch': (True, 'Warning', 'Bypass valve command/feedback mismatch'),
    'OA_SensorInvalidAlarm': (True, 'Warning', 'OA sensor invalid - WB default used'),
    'LocalModeProlongedAlarm': (True, 'Critical', 'Local mode > 1 h (no AI optimisation)'),
    'AiRequestedButLocalAlarm': (True, 'Critical', 'AI requested but forced to Local'),
    'HeartbeatDetectorStatus': (False, 'Critical', 'AI heartbeat lost'),
    'AI_Available': (False, 'Critical', 'AI control not available'),
    'OperationMode': (False, 'Info', 'Operation mode = Local'),
}
AI_INHIBIT = {'HeartbeatDetectorStatus', 'AI_Available'}     # inhibited while user selects Local
CMD_FAIL = {  # command point: (feedback point, class, delay ms)
    'CH01StartCmd': ('CH01RunProof', 'Warning', 60000), 'CH02StartCmd': ('CH02RunProof', 'Warning', 60000),
    'CHP01StartCmd': ('CHP01RunProof', 'Critical', 30000), 'CHP02StartCmd': ('CHP02RunProof', 'Critical', 30000),
    'CDP01StartCmd': ('CDP01RunProof', 'Critical', 30000), 'CDP02StartCmd': ('CDP02RunProof', 'Critical', 30000),
    'CT01StartCmd': ('CT01RunProof', 'Critical', 30000), 'CT02StartCmd': ('CT02RunProof', 'Critical', 30000),
    'CH01ValveOpenCmd': ('CH01ValveOpenProof', 'Warning', 60000), 'CH02ValveOpenCmd': ('CH02ValveOpenProof', 'Warning', 60000),
}
OOR = {  # point: (low, high, class, delay ms, inhibit-by-process?)
    'CHWS': (4.0, 12.0, 'Emergency', 300000, True), 'CHWR': (6.0, 18.0, 'Warning', 300000, True),
    'CHWDP': (30.0, 250.0, 'Warning', 300000, True), 'CDS': (18.0, 35.0, 'Warning', 300000, True),
    'CDR': (20.0, 40.0, 'Warning', 300000, True), 'Plant_kW_per_RT': (0.0, 1.2, 'Warning', 900000, True),
}
NO_HISTORY = {'ConstantTrue', 'ConstantFalse', 'ZeroSpeed', 'StageZero', 'StageOne', 'StageTwo', 'One', 'MsPerHour',
              'PlantReset_Zero', 'PlantReset_Half', 'PlantReset_Full', 'Water_kW_Factor', 'kW_per_RT'}
# MELCO pointNameString: {Serial}_{Store}_{Floor}_{Coordinate}_{Location<No>}_{Category}_{PointType}
STORE, FLOOR, COORD = 'ALTREF', '1F', 'NA'   # PROJECT placeholders
MELCO = [  # point, location, category, pointType
    ('PlantRunRequest', 'CPL', 'STSP', 'CSP'), ('PlantEnable', 'CPL', 'STSP', 'SP'),
    ('CHW_LeavingTemperatureSetpoint_AI', 'CPL', 'OT', 'CSP'), ('CHW_LeavingTemperatureSetpoint_LOCAL', 'CPL', 'OT', 'SP'),
    ('CHW_LeavingTemperatureSetpoint_ACTIVE', 'CPL', 'OT', 'SP'), ('CHWDP_Setpoint_AI', 'CPL', 'DP', 'CSP'),
    ('CHWDP_Setpoint_ACTIVE', 'CPL', 'DP', 'SP'), ('CDS_Setpoint_AI', 'CT', 'OT', 'CSP'), ('CDS_Setpoint_ACTIVE', 'CT', 'OT', 'SP'),
    ('CHWS', 'CPL', 'OT', 'PV'), ('CHWR', 'CPL', 'IT', 'PV'), ('CHWFlow', 'CPL', 'UFM', 'PV'), ('CHWDP', 'CPL', 'DP', 'PV'),
    ('CDS', 'CT', 'OT', 'PV'), ('CDR', 'CT', 'IT', 'PV'), ('OA_Temperature', 'OD', 'TP', 'PV'), ('OA_Humidity', 'OD', 'HU', 'PV'),
    ('OA_WetBulb', 'OD', 'TP', 'PV'), ('Plant_kW', 'CPL', 'PM', 'PV'), ('Plant_kWh', 'CPL', 'PAM', 'PV'),
    ('HeartbeatTimestampSetpoint', 'SYS', 'HTB', 'CSP'), ('HeartbeatDetectorStatus', 'SYS', 'HTB', 'STS'),
    ('AI_Available', 'SYS', 'MDE', 'STS'), ('ModeCmd_UI', 'SYS', 'MDE', 'SP'), ('OperationMode', 'SYS', 'MDE', 'STS'),
    ('CHW_BypassValveCmd', 'MV', 'VLOP', 'CSP'), ('CHW_BypassValveFeedback', 'MV', 'VLOP', 'PV'),
] + [x for n in ('01', '02') for x in (
    (f'CH{n}StartCmd', f'CH{n}', 'STSP', 'CSP'), (f'CH{n}RunProof', f'CH{n}', 'STSP', 'STS'), (f'CH{n}Fault', f'CH{n}', 'FLT', 'STS'),
    (f'CH{n}LoadPct', f'CH{n}', 'ETC', 'PV'), (f'CH{n}_kW', f'CH{n}', 'PM', 'PV'),
    (f'CHP{n}StartCmd', f'CHP{n}', 'STSP', 'CSP'), (f'CHP{n}RunProof', f'CHP{n}', 'STSP', 'STS'), (f'CHP{n}Fault', f'CHP{n}', 'FLT', 'STS'),
    (f'CHP{n}SpeedCmd', f'CHP{n}', 'IVS', 'CSP'), (f'CDP{n}StartCmd', f'CDP{n}', 'STSP', 'CSP'), (f'CDP{n}RunProof', f'CDP{n}', 'STSP', 'STS'),
    (f'CDP{n}Fault', f'CDP{n}', 'FLT', 'STS'), (f'CDP{n}SpeedCmd', f'CDP{n}', 'IVS', 'CSP'),
    (f'CT{n}StartCmd', f'CT{n}', 'STSP', 'CSP'), (f'CT{n}RunProof', f'CT{n}', 'STSP', 'STS'), (f'CT{n}Fault', f'CT{n}', 'FLT', 'STS'),
    (f'CT{n}SpeedCmd', f'CT{n}', 'IVS', 'CSP'))]
HS_RULES = [  # (regex on name, haystack markers)
    (r'^(CHWS|CHW_LeavingTemperature)', 'chilled water leaving temp'), (r'^CHWR$', 'chilled water entering temp'),
    (r'^CHWFlow$', 'chilled water flow'), (r'^CHWDP$', 'chilled water pressure'), (r'^CDS$', 'condenser water leaving temp'),
    (r'^CDR$', 'condenser water entering temp'), (r'^OA_(Temperature|WetBulb|DewPoint)', 'outside air temp'),
    (r'^OA_Humidity', 'outside air humidity'), (r'_kW$', 'elec power'), (r'_kWh$', 'elec energy'),
    (r'StartCmd$', 'run'), (r'RunProof$', 'run'), (r'Fault$', 'fault'), (r'SpeedCmd$', 'speed'), (r'Bypass', 'bypass valve'),
    (r'Setpoint', 'temp'), (r'Alarm$|Mismatch$', 'alarm')]


def history_ext(S, name, kind_bool, cov):
    el = S.comp[name]
    ext_t = ('h:BooleanCovHistoryExt' if cov else 'h:BooleanIntervalHistoryExt') if kind_bool else \
            ('h:NumericCovHistoryExt' if cov else 'h:NumericIntervalHistoryExt')
    en = 'BooleanCov' if kind_bool and cov else 'NumericCov' if cov else 'NumericInterval'
    h = S.h(); e = P(el, en, ext_t, h=h)
    P(e, 'enabled', v='true')
    P(e, 'historyName', 'b:Format', '%parent.name%')
    cfg = P(e, 'historyConfig', 'h:HistoryConfig', h=S.h())
    P(cfg, 'id', 'h:HistoryId', f'/{STATION}/{name}')
    P(cfg, 'source', 'b:OrdList', f'station:|slot:{S.path_of(name)}/{en}')
    P(cfg, 'sourceHandle', 'b:Ord', f'h:{h}')
    P(cfg, 'timeZone', 'b:TimeZone', TZ)
    if kind_bool:
        P(cfg, 'recordType', 'b:TypeSpec', 'history:BooleanTrendRecord')
        P(cfg, 'schema', 'h:HistorySchema', 'timestamp,baja:AbsTime;trendFlags,history:TrendFlags;status,baja:Status;value,baja:Boolean')
    else:
        P(cfg, 'recordType', 'b:TypeSpec', 'history:NumericTrendRecord')
        P(cfg, 'schema', 'h:HistorySchema', 'timestamp,baja:AbsTime;trendFlags,history:TrendFlags;status,baja:Status;value,baja:Double')
    P(cfg, 'capacity', 'h:Capacity', '1:4000' if cov else '1:550000')
    if not cov:
        P(cfg, 'interval', 'h:CollectionInterval', 'false:60000')
    fac = child(el, 'facets')
    if fac is not None:
        P(cfg, 'valueFacets', 'b:Facets', fac.get('v'))
    if not cov:
        P(e, 'interval', 'b:RelTime', '60000')
    return en, ('COV' if cov else 'Interval 60 s'), ('1:4000' if cov else '1:550000')


def alarm_ext(S, point, kind, cls, text, delay=0, value=None, lo=None, hi=None, inhibit=None, feedback=None):
    el = S.comp[point]
    name = {'cos': 'ChangeOfStateAlarm', 'cmd': 'StartStopMismatch', 'oor': 'OutOfRangeAlarm'}[kind]
    e = P(el, name, 'a:AlarmSourceExt', h=S.h())
    if delay: P(e, 'timeDelay', v=str(delay))
    P(e, 'sourceName', 'b:Format', '%parent.parent.parent.name%_%parent.name%')
    P(e, 'toOffnormalText', 'b:Format', text)
    P(e, 'toNormalText', 'b:Format', 'Normal')
    P(e, 'faultAlgorithm', 'a:OutOfRangeFaultAlgorithm' if kind == 'oor' else 'a:FaultAlgorithm', h=S.h())
    if kind == 'cos':
        off = P(e, 'offnormalAlgorithm', 'a:BooleanChangeOfStateAlgorithm', h=S.h()); P(off, 'alarmValue', v=str(value).lower())
    elif kind == 'cmd':
        off = P(e, 'offnormalAlgorithm', 'a:BooleanCommandFailureAlgorithm', h=S.h()); S.link(off, feedback, 'feedbackValue')
    else:
        off = P(e, 'offnormalAlgorithm', 'a:OutOfRangeAlgorithm', h=S.h())
        P(off, 'highLimit', v=repr(hi)); P(off, 'lowLimit', v=repr(lo)); P(off, 'deadband', v='0.5')
        P(off, 'highLimitText', 'b:Format', f'{point} high (> {hi:g})'); P(off, 'lowLimitText', 'b:Format', f'{point} low (< {lo:g})')
        le = P(off, 'limitEnable', 'a:LimitEnable'); P(le, 'lowLimitEnable', v='true'); P(le, 'highLimitEnable', v='true')
    P(e, 'alarmClass', v=cls)
    if inhibit: S.link(e, inhibit, 'alarmInhibit')
    return name


def tag(el, name, typ, val):
    P(el, name, typ, val, f='m')


FACET_RULES_NUM = [  # display facets for inherited V4 points (display/history only, no logic effect)
    (r'^(CHWS|CHWR|CDS|CDR|CDSSetpoint|CHWSMinValid|CHWSMaxValid|CDSMinValid|CDSMaxValid)$', 'C', 2),
    (r'^MinDeltaTStage2$', 'none', 1), (r'^CHWFlow$', 'm3h', 1), (r'^(CHWDP|CHWDPSetpoint)$', 'kPa', 1),
    (r'(LoadPct|SpeedCmd|SpeedPct|^ZeroSpeed)$|^ObsNum_', 'pct', 1), (r'^(Obs_)?PlantStage$|^Stage(Zero|One|Two)$', 'none', 0)]
FACET_RULES_BOOL = [
    (r'(StartCmd|ValveOpenCmd)$', 'ON', 'OFF'), (r'(RunProof|RunProofSelected)$', 'Run', 'Stop'), (r'Fault$', 'Fault', 'Normal'),
    (r'Available$', 'Available', 'Unavailable'), (r'FlowProof$', 'Flow', 'No flow'), (r'ValveOpenProof$', 'Open', 'Closed'),
    (r'(SensorHealthy|CommunicationHealthy)$', 'OK', 'Fault'), (r'^PlantEnable$', 'Enabled', 'Disabled'), (r'^AutoMode$', 'Auto', 'Manual'),
    (r'^BootQualified$', 'Qualified', 'Waiting'), (r'^LeadCH01$', 'CH01 lead', 'CH02 lead'), (r'^RotationRequest$', 'Rotate', 'Normal'),
    (r'^(Stage2Demand|Stage2Request|ObserveStage2)$', 'Stage 2', 'Stage 1'), (r'^(Obs_)?PlantRunRequest$', 'Run', 'Stop'),
    (r'LockoutReset$', 'Reset', 'Normal'), (r'AutoProofEnabled$', 'Auto', 'Field')]


def enrich_facets(S):
    n_set = 0
    for name, el in S.comp.items():
        t = el.get('t')
        if child(el, 'facets') is not None or t not in ('c:NumericWritable', 'c:BooleanWritable'):
            continue
        v = None
        if t == 'c:NumericWritable':
            for rx, u, pr in FACET_RULES_NUM:
                if re.search(rx, name): v = U[u] + f'|precision=i:{pr}|min=d:-inf|max=d:+inf'; S.meta.setdefault(name, {}).setdefault('unit', u); break
        else:
            for rx, tt, ff in FACET_RULES_BOOL:
                if re.search(rx, name): v = f'trueText=s:{tt}|falseText=s:{ff}'; break
        if v:
            fe = ET.Element('p', {'n': 'facets', 't': 'b:Facets', 'v': v}); el.insert(0, fe); n_set += 1
            S.log.append(('FACETS', '', name, 'facets', v, 'display only'))
    return n_set


def instrument(S):
    reg_hist, reg_alarm, reg_tag = [], [], []
    S.kc('ModeControl', 'NotModeCmdUI', 'Not', {'in': 'ModeCmd_UI'})
    for name, el in S.comp.items():
        t = el.get('t')
        if t not in ('c:BooleanWritable', 'c:NumericWritable') or name in NO_HISTORY:
            continue
        m = S.meta.get(name, {})
        is_bool = t == 'c:BooleanWritable'
        cov = is_bool or m.get('kind') in ('param', 'bparam', 'sp', 'mode', 'ai_w') or 'Setpoint' in name
        if name.startswith('Opt_') or name.endswith('_ACTIVE'): cov = False   # continuous reset outputs trended at interval
        en, how, cap = history_ext(S, name, is_bool, cov)
        reg_hist.append((name, S.path_of(name), f'/{STATION}/{name}', en, how, cap))
    for pt, (val, cls, text) in COS.items():
        inh = 'NotModeCmdUI' if pt in AI_INHIBIT else None
        alarm_ext(S, pt, 'cos', cls, text, value=val, inhibit=inh)
        reg_alarm.append((pt, S.path_of(pt), 'ChangeOfState', cls, f'alarmValue={str(val).lower()}', text, 'ModeCmd_UI=Local' if inh else ''))
    for pt, (fb, cls, dly) in CMD_FAIL.items():
        alarm_ext(S, pt, 'cmd', cls, f'{pt} command/status mismatch', delay=dly, feedback=fb)
        reg_alarm.append((pt, S.path_of(pt), 'CommandFailure', cls, f'feedback={fb}; delay {dly // 1000} s', 'StartStopMismatch', ''))
    for pt, (lo, hi, cls, dly, inh) in OOR.items():
        alarm_ext(S, pt, 'oor', cls, f'{pt} out of range', delay=dly, lo=lo, hi=hi, inhibit='ProcessAlarmInhibit' if inh else None)
        reg_alarm.append((pt, S.path_of(pt), 'OutOfRange', cls, f'{lo:g}..{hi:g}; delay {dly // 1000} s', f'{pt} out of range',
                          'until plant ran 30 min' if inh else ''))
    for i, (pt, loc, cat, ptype) in enumerate(MELCO, 1):
        v = f'{i:03d}_{STORE}_{FLOOR}_{COORD}_{loc}_{cat}_{ptype}'
        tag(S.comp[pt], 'melco$3apointNameString', 'b:String', v)
        reg_tag.append((pt, S.path_of(pt), 'melco:pointNameString', v))
    for name, el in S.comp.items():
        if el.get('t') not in ('c:BooleanWritable', 'c:NumericWritable') or name in NO_HISTORY:
            continue
        marks = {'point'}
        kind = S.meta.get(name, {}).get('kind')
        if name.endswith(('Cmd', '_ACTIVE')) or kind == 'ao': marks.add('cmd')
        elif kind in ('param', 'bparam', 'ai_w', 'mode') or 'Setpoint' in name: marks.add('sp')
        else: marks.add('sensor')
        for rx, mk in HS_RULES:
            if re.search(rx, name): marks.update(mk.split())
        marks.add('his')
        for mk in sorted(marks):
            tag(el, f'hs$3a{mk}', 'b:Marker', 'M')
        reg_tag.append((name, S.path_of(name), 'hs markers', ' '.join(sorted(marks))))
    return reg_hist, reg_alarm, reg_tag


def alarm_service(S):
    services = child(S.st, 'Services')
    svc = ET.Element('p', {'n': 'AlarmService', 'h': S.h(), 'm': 'a=alarm', 't': 'a:AlarmService'})
    idx = list(services).index(child(services, 'HistoryService')) + 1
    services.insert(idx, svc)
    cls_h = {}
    for name, prio, ack in ALARM_CLASSES:
        c = P(svc, name, 'a:AlarmClass', h=S.h()); cls_h[name] = c.get('h')
        if ack is not None: P(c, 'ackRequired', 'a:AlarmTransitionBits', ack)
        P(c, 'priority', 'a:AlarmPriorities', prio)
    rec = P(svc, 'ConsoleRecipient', 'a:ConsoleRecipient', h=S.h())
    for i, (name, _, _) in enumerate(ALARM_CLASSES):
        L = P(rec, 'Link' if i == 0 else f'Link{i}', 'b:Link')
        for n, v in (('sourceOrd', 'h:' + cls_h[name]), ('relationTags', ''), ('relationId', 'n:dataLink'),
                     ('sourceSlotName', 'alarm'), ('targetSlotName', 'routeAlarm')):
            P(L, n, v=v)


# ============================================================ folders + layout + output
PITCH_EXTRA = {'Psychrometric': 13, 'Reset': 11, 'Ramp': 6, 'SineWave': 6, 'NumericLatch': 7, 'NotEqual': 7, 'Counter': 10,
               'Add': 9, 'Multiply': 9, 'Maximum': 9, 'Minimum': 9, 'Divide': 7, 'AbsValue': 6, 'GreaterThan': 7,
               'MultiVibrator': 5, 'Hysteresis': 6, 'Limiter': 6, 'LoopPoint': 9}


def pitch_of(el, linked):
    from compact_layout import PITCH
    t = el.get('t').split(':')[1]
    if t in PITCH_EXTRA: return PITCH_EXTRA[t]
    if t in PITCH: return PITCH[t]
    if t.endswith('Writable'): return 7 if linked else 6
    return 10


def width_of(name):
    return max(8, math.ceil((len(name) * 5.6 + 30) / 12))


def build_folders_and_layout(S):
    rp = S.rp; rp.set('n', 'ChillerPlant')
    folders = OrderedDict()
    def folder(path):
        if path in folders: return folders[path]
        parent = rp if '/' not in path else folder(path.rsplit('/', 1)[0])
        el = ET.Element('p', {'n': path.rsplit('/', 1)[-1], 'h': S.h(), 't': 'b:Folder'})
        notes = child(rp, 'EngineeringNotes')
        if parent is rp and notes is not None:
            rp.insert(list(rp).index(notes), el)
        else:
            parent.append(el)
        folders[path] = el
        return el
    for top, subs in PARENT_FOLDERS.items():
        folder(top)
        for s_ in subs: folder(f'{top}/{s_}')
    for name, el in S.comp.items():
        folder(S.folder_of[name]).append(el)
    # ---- layout per folder
    h2n = {}
    for n, el in S.comp.items(): h2n[el.get('h')] = n
    links, linked = [], set()
    for n, el in S.comp.items():
        for L in el:
            if L.get('t') == 'b:Link':
                src = h2n.get(child(L, 'sourceOrd').get('v')[2:])
                if src: links.append((src, n))
                linked.add(n)
    by_folder = defaultdict(list)
    for n in S.comp: by_folder[S.folder_of[n]].append(n)
    report = {}
    for path, names in by_folder.items():
        S_ = set(names); src = defaultdict(set)
        for a, b in links:
            if a in S_ and b in S_ and a != b: src[b].add(a)
        depth = {n: 0 for n in names}
        for _ in range(len(names)):
            ch = False
            for n in names:
                d = min(max((depth[x] + 1 for x in src[n]), default=0), len(names))
                if d > depth[n]: depth[n] = d; ch = True
            if not ch: break
        cols = defaultdict(list)
        for n in names: cols[depth[n]].append(n)
        x, rects = 2, []
        for d in sorted(cols):
            col, y = cols[d], 2
            w = max(width_of(n) for n in col)
            for n in col:
                p = pitch_of(S.comp[n], n in linked)
                if y + p > 60 and y > 2:          # wrap very tall columns
                    x += w + 4; y = 2
                P(S.comp[n], 'wsAnnotation', 'b:WsAnnotation', f'{x},{y},{width_of(n)}', f='r')
                rects.append((n, x, y, x + width_of(n), y + p - 1)); y += p
            x += w + 4
        bad = sum(1 for i, a in enumerate(rects) for b in rects[i + 1:] if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4])
        assert bad == 0, (path, bad)
        report[path] = (len(names), max(r[3] for r in rects), max(r[4] for r in rects))
    # folder icons on parent sheets
    kids = defaultdict(list)
    for path in folders:
        kids[path.rsplit('/', 1)[0] if '/' in path else ''].append(path)
    for parent, lst in kids.items():
        x, y, per_row = 2, 2, 5
        for i, path in enumerate(lst):
            if i and i % per_row == 0: x, y = 2, y + 8
            w = width_of(path.rsplit('/', 1)[-1])
            P(folders[path], 'wsAnnotation', 'b:WsAnnotation', f'{x},{y},{w}', f='r'); x += w + 4
    return folders, report


# kitControl frozen slots whose DEFAULT is an int (javap: newProperty(IIL...)) but whose getter is double.
# A BOG value like "10.0" must then carry t="b:Double" (real ST5130 LoopPoint: f="s" t="b:Double" v="2.0").
INT_DEFAULT_DOUBLE = {'LoopPoint': ('proportionalConstant', 'integralConstant', 'derivativeConstant', 'bias', 'maximumOutput', 'minimumOutput'),
                      'Ramp': ('amplitude', 'offset'), 'SineWave': ('amplitude', 'offset')}
INT_SLOTS = {'MultiVibrator': ('dutyCycle',)}
RELTIME_SLOTS = {'MultiVibrator': ('period',), 'Ramp': ('period', 'updateInterval'), 'SineWave': ('period', 'updateInterval')}


def fix_frozen_types(root):
    n = Counter()
    for el in root.iter('p'):
        t = (el.get('t') or '')
        if not t.startswith('kitControl:'): continue
        k = t.split(':')[1]
        for c in el:
            if c.tag != 'p' or c.get('v') is None or c.get('t'): continue
            if c.get('n') in INT_DEFAULT_DOUBLE.get(k, ()):
                c.set('t', 'b:Double'); c.set('v', repr(float(c.get('v')))); n['double'] += 1
            elif c.get('n') in INT_SLOTS.get(k, ()):
                c.set('v', str(int(round(float(c.get('v')))))); n['int'] += 1
            elif c.get('n') in RELTIME_SLOTS.get(k, ()):
                c.set('t', 'b:RelTime'); n['reltime'] += 1
    for el in root.iter('p'):                     # keep Niagara's attribute order n,h,f,t,v,m
        a = dict(el.attrib)
        if list(a) != sorted(a, key=lambda k: 'nhftvm'.find(k) if k in 'nhftvm' else 9):
            el.attrib.clear()
            for k in sorted(a, key=lambda k: 'nhftvm'.find(k) if k in 'nhftvm' else 9): el.set(k, a[k])
    return dict(n)


def validate(root):
    hs = [e.get('h') for e in root.iter('p') if e.get('h')]
    dup = {h for h in hs if hs.count(h) > 1} if len(hs) != len(set(hs)) else set()
    hset = set(hs)
    bad_links = [child(L, 'sourceOrd').get('v') for L in root.iter('p') if L.get('t') == 'b:Link'
                 and child(L, 'sourceOrd').get('v')[2:] not in hset]
    sib = [(e.get('n'), n) for e in root.iter('p') for n in {c.get('n') for c in e if c.tag == 'p'}
           if sum(1 for c in e if c.tag == 'p' and c.get('n') == n) > 1]
    return dup, bad_links, sib, check_symbols(root)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('groups'); ap.add_argument('out'); ap.add_argument('--regdir', default='.')
    ap.add_argument('--timing', choices=('site', 'fpt'), default='site')
    a = ap.parse_args()
    with zipfile.ZipFile(a.src) as z:
        assert z.testzip() is None
        root = ET.fromstring(z.read('file.xml'))
    groups = {}
    for line in open(a.groups, encoding='utf-8'):
        k, g, _ = line.rstrip('\n').split('\t'); groups[k] = g
    S = Station(root)
    enrich_facets(S)                 # inherited V4 points first, so ramps can copy their units
    ramps, fb = build(S, groups)
    failsafe(S)
    complete_logic(S, TIMING[a.timing])
    enrich_facets(S)
    reg_hist, reg_alarm, reg_tag = instrument(S)
    alarm_service(S)
    # HistoryActiveConverter observed the legacy PlantEnable history ext (h:1103): repoint to the V6 ext
    new_ext = child(S.comp['PlantEnable'], 'BooleanCov')
    for L in S.comp['HistoryActiveConverter']:
        if L.get('t') == 'b:Link' and child(L, 'sourceOrd').get('v') == 'h:1103':
            child(L, 'sourceOrd').set('v', 'h:' + new_ext.get('h'))
            S.log.append(('REWIRE', '', 'HistoryActiveConverter', 'in', 'legacy history ext -> PlantEnable/BooleanCov.active', ''))
    child(S.st, 'stationName').set('v', STATION)
    fox = next(e for e in root.iter('p') if e.get('n') == 'FoxService')
    child(child(fox, 'foxsPort'), 'publicServerPort').set('v', FOXS_PORT)
    folders, lay = build_folders_and_layout(S)
    # Px views (files live in the station's shared/px folder; see gen_px.py)
    for i, (vn, fn) in enumerate((('Overview', 'ALT_CP_Overview'), ('Optimization', 'ALT_CP_Optimization'), ('EnergyDashboard', 'ALT_CP_EnergyDashboard'), ('Energy', 'ALT_CP_Energy'),
                                  ('AlarmsHistory', 'ALT_CP_AlarmsHistory'), ('Simulation', 'ALT_CP_Simulation'))):
        v = ET.Element('p', {'n': 'Px_' + vn, 'f': 'o', 't': 'b:PxView'})
        P(v, 'pxFile', 'b:Ord', f'file:^px/{fn}.px')
        S.rp.insert(i, v)
        S.log.append(('PXVIEW', '', 'ChillerPlant', vn, f'file:^px/{fn}.px', 'graphic view'))
    first_sch = next(e for e in root.iter('p') if (e.get('t') or '').startswith('sch:'))
    first_sch.set('m', 'sch=schedule')                     # declare the schedule module exactly once
    type_fix = fix_frozen_types(root)
    S.log.append(('TYPEFIX', '', '(kitControl)', 'frozen slot types', str(type_fix), 'int-default slots holding doubles get t=b:Double (as in ST5130)'))
    fix_symbols(root)
    lit = [e.get('n') for e in root.iter('p') if '&#x' in (e.get('v') or '')]
    assert not lit, ('literal character reference in value', lit[:5])
    dup, bad_links, sib, sym = validate(root)
    assert not dup and not bad_links and not sib and not sym, (dup, bad_links[:5], sib[:5], sym[:5])
    if os.path.exists(a.out): raise SystemExit('refusing to overwrite ' + a.out)
    with zipfile.ZipFile(a.out, 'x', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('file.xml', ET.tostring(root, encoding='utf-8', xml_declaration=True))
    sha = hashlib.sha256(open(a.out, 'rb').read()).hexdigest().upper()
    n_links = sum(1 for e in root.iter('p') if e.get('t') == 'b:Link')
    print(f'out {a.out} sha256 {sha}')
    print(f'components {len(S.comp)} folders {len(folders)} links {n_links} histories {len(reg_hist)} alarms {len(reg_alarm)} tagged {len(reg_tag)}')
    os.makedirs(a.regdir, exist_ok=True)
    def wcsv(fn, head, rows):
        with open(os.path.join(a.regdir, fn), 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f); w.writerow(head); w.writerows(rows)
    wcsv('V6_HISTORY_REGISTER.csv', ['Point', 'Slot_Path', 'History_ID', 'Extension', 'Method', 'Capacity'], reg_hist)
    wcsv('V6_ALARM_REGISTER.csv', ['Point', 'Slot_Path', 'Alarm_Type', 'Alarm_Class', 'Condition', 'Offnormal_Text', 'Inhibit'], reg_alarm)
    wcsv('V6_TAG_REGISTER.csv', ['Point', 'Slot_Path', 'Tag', 'Value'], reg_tag)
    wcsv('V6_CHANGE_LOG.csv', ['Action', 'Folder', 'Component', 'Type_or_Slot', 'Links_or_Value', 'Note'], S.log)
    wcsv('V6_COMPONENTS.csv', ['Component', 'Folder', 'Type', 'Handle'],
         [(n, S.folder_of[n], el.get('t'), el.get('h')) for n, el in S.comp.items()])
    wcsv('V6_FOLDER_LAYOUT.csv', ['Folder', 'Components', 'Width_cells', 'Height_cells'], [(p, *v) for p, v in lay.items()])
    wcsv('V6_SIMULATION.csv', ['Point', 'Source', 'Profile'],
         [(pt, f'Ramp_{pt}', f'{t} {o - am:g}..{o + am:g} period {pe / 60000:g} min') for pt, t, pe, am, o in ramps] +
         [(t, s_, 'emulated feedback') for t, s_ in fb] +
         [('HeartbeatTimestampSetpoint', 'Sim_AiBeatCounter', 'Counter +1 every 295 s while Sim_AiHeartbeatEnable')])
    return S


if __name__ == '__main__':
    main()
