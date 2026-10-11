"""V7.7 r2 layer (user request 1 Oct 2026 21:00), installed by make_v77.py:
  1  FIELD INTERFACE  every field point (AI / DI / DO / AO, 500+) gets a landing point IO_<point> in FieldIO/<group>
     (ChillerPlant/FieldIO, AirSide/FieldIO). Inputs: <point>.in10 <- IOS_<point> = FieldMode ? IO_<point> : simulation
     (or {null} for manual / fault-injection DIs). Outputs: IO_<point>.in10 <- IOS_<point> = OutEnable ? <point> : {null}.
     Field / simulation per group (IO_<grp>_UseField) or plant-wide (IO_AllField); IO_<grp>_Protocol selects the driver
     (1 BACnet/IP, 2 BACnet MS/TP, 3 Modbus TCP, 4 Modbus RTU, 5 Hard-wired I/O) for the address register / export tool.
  2  COMMISSIONING   CX test mode, point-to-point helpers per group (status, output isolation, AO stroke), 10 automated
     functional tests (software injection at in9 or physical trigger, timed expected-result check, pass / fail latches,
     result code historised), run-all sequence with recovery delay + automatic alarm reset; report tool cx_report.py
  3  HISTORY         logic-driven numeric 'setpoints' were COV with tolerance 0 (flooded 4 000 records in ~1 h) -> 1-min
     interval; boot debug observers removed from history"""
import os, sys, re, csv
import make_v6 as M6
import make_v7 as M7
from make_v6 import child
from make_v7 import AND, OR, NOT, DLY, PULSE, SW, BSW, const, sealin

T, F = 'ConstantTrue', 'ConstantFalse'
AIR = M7.AIR
PROF = [M6.TIMING['site']]
PROTO = {1: 'BACnet/IP', 2: 'BACnet MS/TP', 3: 'Modbus TCP', 4: 'Modbus RTU', 5: 'Hard-wired I/O'}
LEGACY_IN = re.compile(r'^(CHWS|CHWR|CHWFlow|CHWDP|CDS|CDR|CH0\dLoadPct|(CH|CHP|CDP|CT)0\d(Available|Fault|RunProof)|'
                       r'CH0\d(CHWFlowProof|CDWFlowProof|ValveOpenProof))$')
LEGACY_DO = re.compile(r'^((CH|CHP|CDP|CT)0\dStartCmd|CH0\dValveOpenCmd)$')
LEGACY_AO = re.compile(r'^(CHP|CDP|CT)0\dSpeedCmd$')
GROUP_ALIAS = {'Chiller01': 'CH01', 'Chiller02': 'CH02', 'PlantControl': 'PlantCommon', 'Parameters': 'PlantCommon', 'Alarms': 'PlantCommon',
               'Simulation': 'PlantCommon', 'ModeControl': 'PlantCommon', 'Graphics': 'PlantCommon', 'Energy': 'Metering', 'Common': 'AirCommon'}
DEFAULT_PROTO = [(r'^CH0\d$|^AI_', 1), (r'^(CHP|CDP|CT)0\d$|^Metering$|^MakeupWater$', 4), (r'^FCU|^Zones$', 2)]
REG = {'io': [], 'hist': [], 'ft': [], 'p2p': []}
FT_LIST = []


def tm(site, fpt):
    return site if PROF[0] is M6.TIMING['site'] else fpt


# ------------------------------------------------------------------ 3  history
_he = M6.history_ext
FORCE_COV = set()


def history_ext_r2(S, name, kind_bool, cov):
    if name in FORCE_COV: cov = True
    elif cov and not kind_bool and any(c.get('t') == 'b:Link' for c in S.comp[name]):
        cov = False                                     # logic / emulation driven -> interval (was COV tol 0)
        REG['hist'].append((name, S.path_of(name), 'NumericCov tol 0 -> NumericInterval 1 min', 'value driven by logic, changes every scan'))
    return _he(S, name, kind_bool, cov)


M6.history_ext = history_ext_r2
for n in ('Obs_BootOscillator', 'Obs_BootFreshEdgeDelay', 'Obs_BootPulse', 'Obs_BootPulseDone'):
    M6.NO_HISTORY.add(n)
    REG['hist'].append((n, '', 'BooleanCov removed', 'boot debug observer toggles continuously (filled 4 000 records within minutes)'))


# ------------------------------------------------------------------ 1  field interface
def field_points(S):
    out = []
    for n, el in S.comp.items():
        t = el.get('t')
        if t not in ('c:NumericWritable', 'c:BooleanWritable') or n.startswith(('IO_', 'CX_', 'Sim_', 'Gfx_')): continue
        k = S.meta.get(n, {}).get('kind', '') or ''
        b = t == 'c:BooleanWritable'
        if k in ('ai', 'ai_w', 'ai_emul', 'di') or (k == '' and LEGACY_IN.match(n)): d = 'in'
        elif k in ('do', 'ao') or (k == '' and (LEGACY_DO.match(n) or LEGACY_AO.match(n))): d = 'out'
        else: continue
        typ = ('DI' if b else 'AI') if d == 'in' else ('DO' if b else 'AO')
        out.append((n, d, typ, b))
    return out


def group_of(S, n):
    f = S.folder_of[n].split('/')
    air = f[0] == AIR
    g = f[1] if air and len(f) > 1 else f[0]
    g = GROUP_ALIAS.get(g, g)
    return g, (f'{AIR}/FieldIO/{g}' if air else f'FieldIO/{g}')


def facets_of(S, n):
    f = child(S.comp[n], 'facets')
    return f.get('v') if f is not None else None


def or_tree(S, f, name, ins):
    lvl, i = list(ins), 0
    while len(lvl) > 1:
        lvl = [OR(S, f, f'{name}{(i := i + 1)}', *lvl[j:j + 4]) for j in range(0, len(lvl), 4)]
    return lvl[0]


def field_io(S):
    C = 'FieldIO/Common'
    S.bparam('IO_AllField', False, folder=C, t='FIELD (all)', f='Per group', note='master: all groups use real field points')
    S.bparam('IO_DriversInstalled', False, folder=C, t='Drivers installed', f='Not installed (simulation only)',
             note='r4 interlock: FIELD selection takes effect only after the driver proxy points are linked to the IO_ points')
    for nm, typ in (('IO_NullN', 'c:NumericWritable'), ('IO_NullB', 'c:BooleanWritable')):
        S.add(C, nm, typ, note='no fallback = {null}: input slot ignored by the priority array'); S.meta[nm] = {'kind': 'io'}
        M6.NO_HISTORY.add(nm)
    pts = field_points(S)
    groups = {}
    for n, d, typ, b in pts:
        g, fld = group_of(S, n)
        groups.setdefault(g, {'folder': fld, 'pts': []})['pts'].append((n, d, typ, b))
    PP = 'Commissioning/PointToPoint'
    SEL, FMODE = [], []
    for gi, (g, G) in enumerate(sorted(groups.items()), 1):
        fld = G['folder']
        proto = next((p for rx, p in DEFAULT_PROTO if re.search(rx, g)), 5)
        S.param(f'IO_{g}_Protocol', proto, folder=fld, prec=0, lo=1, hi=5,
                note='1 BACnet/IP · 2 BACnet MS/TP · 3 Modbus TCP · 4 Modbus RTU · 5 hard-wired I/O (driver for the export tool)')
        S.bparam(f'IO_{g}_UseField', False, folder=fld, t='FIELD', f='SIMULATION', note='this group uses real field points')
        OR(S, fld, f'IO_{g}_FieldSelected', 'IO_AllField', f'IO_{g}_UseField')
        AND(S, fld, f'IO_{g}_FieldModeLogic', f'IO_{g}_FieldSelected', 'IO_DriversInstalled')
        S.bpoint(fld, f'IO_{g}_FieldMode', f'IO_{g}_FieldModeLogic', 'FIELD', 'SIMULATION')
        SEL.append(f'IO_{g}_FieldSelected'); FMODE.append(f'IO_{g}_FieldMode')
        S.bparam(f'IO_{g}_CommFault', False, folder=fld, t='Device down', f='OK',
                 note='FIELD: link the driver device status (down / fault) here')
        AND(S, fld, f'IO_{g}_CommFaultField', f'IO_{g}_FieldMode', f'IO_{g}_CommFault')
        DLY(S, fld, f'IO_{g}_CommFaultDly', f'IO_{g}_CommFaultField', 30000)
        S.bpoint(fld, f'IO_{g}_CommAlarm', f'IO_{g}_CommFaultDly', 'Comm fail', 'Normal')
        M6.COS[f'IO_{g}_CommAlarm'] = (True, 'Critical', f'{g} field device communication failure (field mode)')
        # P2P helpers
        S.param(f'CX_P2P_{g}_Status', 0, folder=PP, prec=0, lo=0, hi=3, note='0 not started · 1 in progress · 2 passed · 3 failed (historised)')
        S.bparam(f'CX_P2P_{g}_Isolate', False, folder=PP, t='ISOLATED', f='Logic', note='P2P: outputs released from logic (manual override at IO_ point)')
        AND(S, PP, f'CX_P2P_{g}_IsolateOn', f'CX_P2P_{g}_Isolate', 'CX_TestMode')
        NOT(S, PP, f'CX_P2P_{g}_NotIsolated', f'CX_P2P_{g}_IsolateOn')
        AND(S, fld, f'IO_{g}_OutEnable', f'IO_{g}_FieldMode', f'CX_P2P_{g}_NotIsolated')
        stroke = [n for n, d, typ, b in G['pts'] if typ == 'AO' and S.meta.get(n, {}).get('unit') == 'pct']
        if stroke:
            S.bparam(f'CX_P2P_{g}_Stroke', False, folder=PP, t='STROKE', f='Off', note='P2P: % outputs follow CX_StrokeValue')
            AND(S, PP, f'CX_P2P_{g}_StrokeOn', f'CX_P2P_{g}_Stroke', 'CX_TestMode')
            SW(S, PP, f'CX_P2P_{g}_StrokeSel', f'CX_P2P_{g}_StrokeOn', 'CX_StrokeValue', 'IO_NullN')
        REG['p2p'].append((g, len(G['pts']), PROTO[proto]))
        cnt = {}
        for n, d, typ, b in G['pts']:
            io, sw = 'IO_' + n, 'IOS_' + n
            S.add(fld, io, 'c:BooleanWritable' if b else 'c:NumericWritable', facets=facets_of(S, n),
                  note=f'FIELD {typ}: link the {"driver proxy point" if d == "in" else "IO_ out to the driver proxy point"}')
            S.meta[io] = {'kind': 'io', 'unit': S.meta.get(n, {}).get('unit', 'none')}
            M6.NO_HISTORY.add(io)
            null = 'IO_NullB' if b else 'IO_NullN'
            kind = 'BooleanSwitch' if b else 'NumericSwitch'
            el = S.comp[n]
            sim = ''
            if d == 'in':
                S.kc(fld, sw, kind, {'inSwitch': f'IO_{g}_FieldMode', 'inTrue': io})
                L10 = [c for c in el if c.get('t') == 'b:Link' and child(c, 'targetSlotName').get('v') == 'in10']
                if L10:
                    L = L10[0]; el.remove(L)
                    child(L, 'targetSlotName').set('v', 'inFalse'); L.set('n', 'Link2'); S.comp[sw].append(L)
                    src = child(L, 'sourceOrd').get('v')[2:]
                    sim = next((k for k, e in S.comp.items() if e.get('h') == src), src)
                else:
                    S.link(S.comp[sw], null, 'inFalse')
                    sim = 'manual / fallback'
                S.link(el, sw, 'in10')
            else:
                S.kc(fld, sw, kind, {'inSwitch': f'IO_{g}_OutEnable', 'inTrue': n, 'inFalse': null})
                S.link(S.comp[io], sw, 'in10')
                if n in stroke: S.link(S.comp[io], f'CX_P2P_{g}_StrokeSel', 'in9')
            k = cnt[typ] = cnt.get(typ, 0) + 1
            unit = S.meta.get(n, {}).get('unit', '') or ''
            sig = {'AI': '10k NTC type II' if unit == 'C' else '4-20 mA', 'DI': 'volt-free contact', 'DO': 'relay 24 VAC', 'AO': '0-10 VDC'}[typ]
            bac = {'AI': 'analog-input', 'DI': 'binary-input', 'DO': 'binary-output', 'AO': 'analog-output'}[typ]
            mb = {'AI': f'3x {30000 + 2 * k - 1} float32', 'DI': f'1x {10000 + k}', 'DO': f'0x {k:05d} coil', 'AO': f'4x {40000 + 2 * k - 1} float32'}[typ]
            ioc = {'AI': f'UI{k}', 'DI': f'DI{k}', 'DO': f'DO{k}', 'AO': f'AO{k}'}[typ]
            REG['io'].append(dict(Group=g, Point=n, IO_Point=io, Direction=d, Type=typ, Unit=unit, Protocol=proto, Protocol_Name=PROTO[proto],
                                  BACnet_Device=7700 + gi, BACnet_Object=f'{bac}:{k}', Modbus_Unit=gi, Modbus_Register=mb,
                                  IO_Module=f'IOM-{g}', IO_Channel=ioc, Signal=sig, Simulation_Source=sim if d == 'in' else '(logic command)',
                                  Point_Path=S.path_of(n), IO_Path=('/' + fld + '/' + io) if fld.startswith(AIR) else '/ChillerPlant/' + fld + '/' + io))
    # r4: plant-wide source indication (every page header) + field selected while drivers not installed
    S.bpoint(C, 'IO_AnyFieldSts', or_tree(S, C, 'IO_AnyFieldOr', FMODE), 'FIELD I/O', 'SIMULATION I/O')
    AND(S, C, 'IO_FieldBlockedLogic', or_tree(S, C, 'IO_AnySelectedOr', SEL), NOT(S, C, 'IO_NotDriversInstalled', 'IO_DriversInstalled'))
    S.bpoint(C, 'IO_FieldBlockedSts', 'IO_FieldBlockedLogic', 'FIELD selected - drivers not installed: still SIMULATION', 'OK')
    S.log.append(('V7.7r2', 'FieldIO', f'{len(pts)} field points / {len(groups)} groups', 'IO_ landing + IOS_ selector', '', ''))
    return groups


# ------------------------------------------------------------------ 2  commissioning
def cx_common(S):
    C = 'Commissioning/Common'
    S.bparam('CX_TestMode', False, folder=C, t='TEST MODE', f='Normal', note='enables P2P isolation / stroke and functional tests')
    S.bparam('CX_SoftInject', True, folder=C, t='Software injection', f='Physical trigger',
             note='tests inject the fault in software (priority 9) or wait for the physical trigger')
    S.bparam('CX_AutoResetAfterTest', True, folder=C, t='Auto reset', f='Manual reset', note='PLANT RESET 10 s after each test')
    S.bpoint(C, 'CX_TestModeSts', 'CX_TestMode', 'TEST MODE', 'Normal')
    DLY(S, C, 'CX_TestModeLong', 'CX_TestMode', tm(8 * 3600000, 600000))
    S.bpoint(C, 'CX_TestModeLeftOnAlarm', 'CX_TestModeLong', 'Left on', 'Normal')
    M6.COS['CX_TestModeLeftOnAlarm'] = (True, 'Warning', 'Commissioning test mode left ON for more than 8 h')
    NOT(S, C, 'CX_NotTestMode', 'CX_TestMode')
    PULSE(S, C, 'CX_AbortFire', note='Px ABORT -> action fire')
    PULSE(S, C, 'CX_RunAllFire', note='Px RUN ALL -> action fire')
    OR(S, C, 'CX_AbortAny', 'CX_AbortFire')            # r4: functional tests no longer need TEST MODE (START is the intent)
    # AO stroke source: triangle 0 -> 100 -> 0 % (10 min) or manual value
    S.kc(C, 'CX_StrokeRamp', 'Ramp', props=[('period', 'b:RelTime', '600000'), ('amplitude', None, '50.0'), ('offset', None, '50.0'),
                                             ('waveform', None, 'triangle')], note='AO stroke 0-100-0 % / 10 min')
    S.param('CX_StrokeManualPct', 50, 'pct', folder=C, prec=0, lo=0, hi=100, note='AO stroke manual value')
    S.bparam('CX_StrokeUseManual', True, folder=C, t='Manual value', f='Sweep 0-100-0', note='stroke = manual value or 10-min sweep')
    SW(S, C, 'CX_StrokeSel', 'CX_StrokeUseManual', 'CX_StrokeManualPct', 'CX_StrokeRamp')
    S.npoint(C, 'CX_StrokeValue', 'CX_StrokeSel', 'pct', 0)
    for v in range(6): const(S, f'CX_K{v}', v, prec=0)
    OR(S, C, 'CX_AnyChillerRun', 'CH01RunProof', 'CH02RunProof')
    NOT(S, C, 'CX_NoChillerCmd', OR(S, C, 'CX_AnyChillerCmd', 'CH01StartCmd', 'CH02StartCmd'))
    NOT(S, C, 'CX_NoAirFan', OR(S, C, 'CX_AnyAirFan', 'AHU01_StartCmd', 'AHU02_StartCmd', 'OAU01_StartCmd'))


def functional_tests(S):
    """(code, title, inject target, value, inject ms or None, precondition, expected terms, check s (site, fpt))"""
    return [
        ('FT01', 'CHP-01 fault -> CHP-02 standby starts', 'CHP01Fault', True, None, 'CHP01RunProof', ['CHP02RunProof'], (240, 60)),
        ('FT02', 'CDP-01 fault -> CDP-02 standby starts', 'CDP01Fault', True, None, 'CDP01RunProof', ['CDP02RunProof'], (240, 60)),
        ('FT03', 'CT-01 fault -> CT-02 takes over', 'CT01Fault', True, None, 'CT01RunProof', ['CT02RunProof'], (300, 90)),
        ('FT04', 'CH-01 fault -> CH-02 starts', 'CH01Fault', True, None, 'CH01RunProof', ['CH02RunProof'], (900, 180)),
        ('FT05', 'CHWS sensor failure -> sensor fail-safe', 'CHWS', -20.0, None, T, ['!CHWSValid'], (60, 20)),
        ('FT06', 'Emergency stop -> chillers stop, plant interlocked', 'Plant_EmergencyStop', True, None, 'CX_AnyChillerRun',
         ['CX_NoChillerCmd', 'Plant_InterlockActive'], (30, 10)),
        ('FT07', 'Refrigerant 1 200 ppm -> vent ON + chillers OFF', 'PlantRoom_RefrigerantPPM', 1200.0, None, T,
         ['PlantRoom_EmergencyVentCmd', 'PlantRoom_RefLeakHighAlarm', 'CX_NoChillerCmd'], (90, 40)),
        ('FT08', 'Fire alarm -> AHU / OAU stop', 'FireAlarmSignal', True, None, T, ['CX_NoAirFan', 'FireModeActive'], (30, 10)),
        ('FT09', 'Phase failure 30 s -> automatic plant restart', 'Plant_PhaseFailRelay', True, (30000, 10000), 'CX_AnyChillerRun',
         ['CX_AnyChillerRun', '!Plant_InterlockActive'], (900, 240)),
        ('FT10', 'CH-01 evaporator flow switch lost -> trip', 'CH01CHWFlowProof', False, None, 'CH01RunProof', ['CH01_EvapFlowSwTripAlarm'], (60, 20)),
    ]


def latch(S, f, name):
    return S.kc(f, name, 'Or', {'inC': F, 'inD': F})


def close(S, f, name, trip, reset):
    """complete a forward-declared seal-in: name = trip OR (name AND NOT reset)"""
    NOT(S, f, name + 'NotReset', reset)
    AND(S, f, name + 'Hold', name, name + 'NotReset')
    S.link(S.comp[name], trip, 'inA'); S.link(S.comp[name], name + 'Hold', 'inB')


def commissioning(S):
    f = 'Commissioning/FunctionalTest'
    latch(S, f, 'CX_AutoSeq')
    tests = functional_tests(S)
    rec = tm(300000, 60000)
    reset_reqs, prev_fin = [], None
    for code, title, tgt, val, inj, pre, exp, (cs, cf) in tests:
        p = f'CX_{code}_'
        chk = tm(cs, cf) * 1000
        PULSE(S, f, p + 'StartFire', note=f'Px START {code} -> action fire')
        if prev_fin is None: DLY(S, f, p + 'AutoReq', 'CX_AutoSeq', 5000)
        else: DLY(S, f, p + 'AutoReq', AND(S, f, p + 'AutoAfterPrev', 'CX_AutoSeq', prev_fin), rec)
        PULSE(S, f, p + 'AutoStart', p + 'AutoReq')
        OR(S, f, p + 'StartEdge', p + 'StartFire', p + 'AutoStart')
        AND(S, f, p + 'Ready', pre)
        S.bpoint(f, p + 'ReadySts', p + 'Ready', 'Ready', 'Not ready')
        AND(S, f, p + 'RunTrip', p + 'StartEdge', p + 'Ready')
        latch(S, f, p + 'Running')
        DLY(S, f, p + 'Check', p + 'Running', chk)
        DLY(S, f, p + 'Done', p + 'Running', chk + 5000)
        close(S, f, p + 'Running', p + 'RunTrip', OR(S, f, p + 'RunReset', p + 'Done', 'CX_AbortAny'))
        terms = []
        for e in exp:
            if e.startswith('!'): terms.append(NOT(S, f, p + 'Not' + e[1:], e[1:]))
            else: terms.append(e)
        AND(S, f, p + 'ExpectOK', *terms)
        NOT(S, f, p + 'ExpectNotOK', p + 'ExpectOK')
        OR(S, f, p + 'ClearResult', p + 'StartEdge', 'CX_RunAllFire')
        sealin(S, f, p + 'Pass', AND(S, f, p + 'PassTrip', p + 'Check', p + 'ExpectOK'), p + 'ClearResult')
        sealin(S, f, p + 'Fail', AND(S, f, p + 'FailTrip', p + 'Check', p + 'ExpectNotOK'), p + 'ClearResult')
        NOT(S, f, p + 'NotReady0', p + 'Ready')
        OR(S, f, p + 'NotReadyReset', p + 'RunTrip', 'CX_RunAllFire')
        latch(S, f, p + 'Started'); latch(S, f, p + 'Aborted')
        NOT(S, f, p + 'NotStarted', p + 'Started')            # precondition judged at the start edge only
        sealin(S, f, p + 'NotReady', AND(S, f, p + 'NotReadyTrip', p + 'StartEdge', p + 'NotReady0', p + 'NotStarted'), p + 'NotReadyReset')
        close(S, f, p + 'Started', p + 'RunTrip', OR(S, f, p + 'StartedReset', p + 'Pass', p + 'Fail', p + 'Aborted'))
        close(S, f, p + 'Aborted', AND(S, f, p + 'AbortTrip', 'CX_AbortAny', p + 'Started'), p + 'ClearResult')
        OR(S, f, p + 'Finished', p + 'Pass', p + 'Fail', p + 'NotReady', p + 'Aborted')
        # injection (software) at priority 9 of the logic point
        ins = [p + 'Running', 'CX_SoftInject']
        if inj:
            DLY(S, f, p + 'InjEnd', p + 'Running', tm(*inj)); ins.append(NOT(S, f, p + 'InjWindow', p + 'InjEnd'))
        AND(S, f, p + 'Inject', *ins)
        if isinstance(val, bool):
            BSW(S, f, p + 'InjSel', p + 'Inject', T if val else F, 'IO_NullB')
        else:
            SW(S, f, p + 'InjSel', p + 'Inject', const(S, f'CX_{code}_InjValue', val), 'IO_NullN')
        el = S.comp[tgt]
        assert not [c for c in el if c.get('t') == 'b:Link' and child(c, 'targetSlotName').get('v') == 'in9'], tgt
        S.link(el, p + 'InjSel', 'in9')
        # result code 0 not run · 1 running · 2 pass · 3 fail · 4 not ready · 5 aborted
        SW(S, f, p + 'R5', p + 'Aborted', 'CX_K5', 'CX_K0')
        SW(S, f, p + 'R4', p + 'NotReady', 'CX_K4', p + 'R5')
        SW(S, f, p + 'R3', p + 'Fail', 'CX_K3', p + 'R4')
        SW(S, f, p + 'R2', p + 'Pass', 'CX_K2', p + 'R3')
        SW(S, f, p + 'R1', p + 'Running', 'CX_K1', p + 'R2')
        S.npoint(f, p + 'Result', p + 'R1', prec=0, note='0 not run · 1 running · 2 PASS · 3 FAIL · 4 not ready · 5 aborted')
        FORCE_COV.add(p + 'Result')
        for st, (tt, ff) in (('Running', ('RUNNING', 'idle')), ('Pass', ('PASS', '-')), ('Fail', ('FAIL', '-'))):
            S.bpoint(f, p + st + 'Sts', p + st, tt, ff)
        S.log.append(('CX', f, p + 'Result', title, '', ''))
        DLY(S, f, p + 'FinDly', p + 'Finished', 10000)
        reset_reqs.append(PULSE(S, f, p + 'ResetReq', p + 'FinDly'))
        prev_fin = p + 'Finished'
        FT_LIST.append((code, title, tgt, val, pre, ' AND '.join(exp), tm(cs, cf)))
    # run-all sequence
    close(S, f, 'CX_AutoSeq', 'CX_RunAllFire', OR(S, f, 'CX_AutoSeqReset', 'CX_AbortAny', prev_fin))
    S.bpoint(f, 'CX_AutoSeqSts', 'CX_AutoSeq', 'RUN ALL active', 'idle')
    # automatic PLANT RESET 10 s after each test (clears latched trips created by the test)
    lvl, i = list(reset_reqs), 0
    while len(lvl) > 1:
        nxt = []
        for j in range(0, len(lvl), 4):
            nxt.append(OR(S, f, f'CX_ResetOr{i}', *lvl[j:j + 4])); i += 1
        lvl = nxt
    AND(S, f, 'CX_ResetAfterTest', lvl[0], 'CX_AutoResetAfterTest')
    pr = S.comp['PlantAlarmResetFire']
    assert not [c for c in pr if c.get('t') == 'b:Link' and child(c, 'targetSlotName').get('v') == 'in']
    S.link(pr, 'CX_ResetAfterTest', 'in')
    S.log.append(('V7.7r2', 'Commissioning', f'{len(tests)} functional tests', 'P2P helpers, run-all, auto reset', '', ''))


# ------------------------------------------------------------------ install (runs after all logic, before histories / alarms)
_instrument = M6.instrument


def instrument_r2(S):
    cx_common(S)
    field_io(S)
    commissioning(S)
    res = _instrument(S)
    rd = sys.argv[sys.argv.index('--regdir') + 1] if '--regdir' in sys.argv else '.'
    os.makedirs(rd, exist_ok=True)
    def w(fn, head, rows):
        with open(os.path.join(rd, fn), 'w', newline='', encoding='utf-8-sig') as fh:
            cw = csv.writer(fh); cw.writerow(head); cw.writerows(rows)
    head = list(REG['io'][0].keys())
    w('V7_7_FIELD_IO_REGISTER.csv', head, [[r[k] for k in head] for r in REG['io']])
    w('V7_7_P2P_CHECKLIST.csv', ['Group', 'Point', 'IO_Point', 'Type', 'Unit', 'Protocol', 'Address', 'Signal', 'Test method', 'Expected',
                                 'Field value', 'BMS value', 'Result (P/F)', 'Tested by', 'Date', 'Remark'],
      [[r['Group'], r['Point'], r['IO_Point'], r['Type'], r['Unit'], r['Protocol_Name'],
        {1: f"dev {r['BACnet_Device']} {r['BACnet_Object']}", 2: f"dev {r['BACnet_Device']} {r['BACnet_Object']}", 3: f"unit {r['Modbus_Unit']} {r['Modbus_Register']}",
         4: f"unit {r['Modbus_Unit']} {r['Modbus_Register']}", 5: f"{r['IO_Module']} {r['IO_Channel']}"}[r['Protocol']], r['Signal'],
        {'AI': 'compare field reading / reference meter', 'DI': 'operate device / contact at field', 'DO': 'override IO_ point ON / OFF',
         'AO': 'override IO_ point 0 / 50 / 100 % (or STROKE)'}[r['Type']],
        {'AI': 'BMS = reference ± accuracy', 'DI': 'BMS state follows field', 'DO': 'device / relay operates', 'AO': 'actuator position = command'}[r['Type']],
        '', '', '', '', '', ''] for r in REG['io']])
    w('V7_7_FUNCTIONAL_TESTS.csv', ['Test', 'Title', 'Injection point (in9)', 'Injection value', 'Precondition', 'Expected', 'Check after s'], FT_LIST)
    w('V7_7_HISTORY_FIXES.csv', ['Point', 'Path', 'Change', 'Reason'], REG['hist'])
    print(f"r2: field points {len(REG['io'])} groups {len(REG['p2p'])} functional tests {len(FT_LIST)} history fixes {len(REG['hist'])}")
    return res


M6.instrument = instrument_r2
