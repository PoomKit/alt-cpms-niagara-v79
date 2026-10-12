# -*- coding: utf-8 -*-
"""Upgrade an existing ALT_CP_Ref_V7_9 config.bog to the logic of this repository (when the V5 source c_v5.bog is not available).

The full build (make_v79.py) starts from c_v5.bog. Without it, this tool loads a V7.9 station config.bog and re-runs every builder
of the instrument phase of the current code on it - V7.7 smart / cloud / r9, V7.8 improve / finish, V7.9 r1..r7 (expansion slots,
floors, office VAV / rooms / metering, r6 / r7 logic), Field IO, commissioning, histories / alarms / tags:
  * a component the builders create that already exists is rebuilt from the current code and keeps its handle (links from the
    components that are not rebuilt stay valid); its history / alarm extensions and tags are regenerated
  * site-tuned values are kept: the fallback of an existing parameter (kind param / bparam) stays as it was in the station
  * rewires already applied in the station are skipped; a rewire whose source differs from the expected one is applied and listed
  * components built before the instrument phase (V6 .. V7.6 plant logic) are kept as they are in the station
  * folders and wire-sheet layout are rebuilt; Px views of ChillerPlant / AirSide are kept
  * the result is checked with make_v6.validate (unique handles, every link source exists, unique slot names, symbols) before it
    is written; the output is a NEW file (never overwrites)
usage: python3 upgrade_v79.py <station config.bog> <out.bog> [--regdir D] [--register ALT_V79_Equipment_Register.xlsx]
Reports in --regdir: UPGRADE_REPORT.csv (rebuilt / new / kept-value / forced rewire) + the usual V7_*.csv registers.
REFERENCE SIMULATION - verify in Workbench on a test station before use; never on the reference station."""
import csv, hashlib, os, re, sys, zipfile, xml.etree.ElementTree as ET
from collections import OrderedDict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_argv = list(sys.argv); sys.argv = sys.argv[:1]                   # builders read sys.argv at import / run time
import make_v79                                                   # noqa: F401,E402  (whole chain + V7.9 layers)
import make_v6 as M6                                              # noqa: E402
import make_v7 as M7                                              # noqa: E402
import v77_fieldcx as FCX                                         # noqa: E402
import v77_smart                                                  # noqa: E402
import v79_scale                                                  # noqa: E402
import eqreg                                                      # noqa: E402
sys.argv = _argv
child, P = M6.child, M6.P
SKIP_T = ('b:Folder', 'b:PxView', 'b:WsAnnotation')
KEEP_TOP = ('wsAnnotation',)


class Upgrade(M6.Station):
    def __init__(self, root):
        self.root = root; self.st = root.find('p')
        self.rp = child(self.st, 'ChillerPlant'); self.air = child(self.st, 'AirSide')
        used = [int(h, 16) for h in (e.get('h') for e in root.iter('p')) if h and re.fullmatch('[0-9a-f]+', h)]
        self.nh = max(used) + 1
        self.comp, self.folder_of, self.meta, self.log, self.ext_handle = OrderedDict(), {}, {}, [], {}
        self.orig, self.rebuilt, self.report = set(), set(), []
        self.air_views = [c for c in self.air if c.get('t') == 'b:PxView']
        def walk(folder, rel):
            for c in list(folder):
                t = c.get('t') or ''
                if c.tag != 'p': continue
                if t == 'b:Folder': walk(c, f'{rel}/{c.get("n")}' if rel else c.get('n')); folder.remove(c); continue
                if t in SKIP_T or c.get('n') in KEEP_TOP: continue
                if not rel: continue                                       # direct children of the roots stay (notes)
                for a in [x for x in c if x.get('n') == 'wsAnnotation']: c.remove(a)
                self.comp[c.get('n')] = c; self.folder_of[c.get('n')] = rel; self.orig.add(c.get('n')); folder.remove(c)
        walk(self.rp, ''); walk(self.air, M7.AIR)
        for c in [x for x in self.rp if x.get('n') == 'wsAnnotation'] + [x for x in self.air if x.get('n') == 'wsAnnotation']:
            (self.rp if c in list(self.rp) else self.air).remove(c)
        self.st.remove(self.air)

    def add(self, folder, name, typ, links=None, props=(), fallback=None, facets=None, note=''):
        if name in self.orig:
            old = self.comp.pop(name); self.orig.discard(name)
            r = super().add(folder, name, typ, links, props, fallback, facets, note)
            new = self.comp[name]; new.set('h', old.get('h'))
            ofb, nfb = child(old, 'fallback'), child(new, 'fallback')
            kind = self.meta.get(name, {}).get('kind')
            if ofb is not None and nfb is not None and kind in ('param', 'bparam'):
                ov, nv = child(ofb, 'value'), child(nfb, 'value')
                if ov is not None and nv is not None and ov.get('v') != nv.get('v'):
                    self.report.append(('KEPT_VALUE', name, f'station {ov.get("v")} (code default {nv.get("v")})')); nv.set('v', ov.get('v'))
            self.rebuilt.add(name); return r
        r = super().add(folder, name, typ, links, props, fallback, facets, note)
        self.rebuilt.add(name); self.report.append(('NEW', name, folder)); return r

    def unapply_field_io(self):
        """Field IO (v77_fieldcx.field_io) moves a field input's in10 link into IOS_<point>.inFalse and links IOS_ -> in10. Undo that
        on the station before the run so field_io works on the plain point again (otherwise the selector would read itself)"""
        h2n = {e.get('h'): n for n, e in self.comp.items()}; n_ok = 0
        def lk(el, slot): return next((c for c in el if c.get('t') == 'b:Link' and child(c, 'targetSlotName').get('v') == slot), None)
        for sw in [x for x in self.comp if x.startswith('IOS_')]:
            pt = self.comp.get(sw[4:])
            if pt is None: continue
            L = lk(pt, 'in10')
            if L is None or child(L, 'sourceOrd').get('v') != 'h:' + self.comp[sw].get('h'): continue
            F = lk(self.comp[sw], 'inFalse'); src = F is not None and h2n.get(child(F, 'sourceOrd').get('v')[2:])
            if not src or src.startswith('IO_Null'): pt.remove(L)
            else:
                child(L, 'sourceOrd').set('v', child(F, 'sourceOrd').get('v')); child(L, 'sourceSlotName').set('v', child(F, 'sourceSlotName').get('v'))
            n_ok += 1
        return n_ok

    def link(self, target_el, src, tslot):
        # a link the rebuilt code adds to a kept component is skipped when the station already has it (same slot, same source)
        if target_el.get('n') in self.orig:
            s0 = src.split('.', 1)[0]
            h = self.ext_handle.get(s0) or (self.comp[s0].get('h') if s0 in self.comp else None)
            if h and any(c.get('t') == 'b:Link' and child(c, 'targetSlotName').get('v') == tslot and child(c, 'sourceOrd').get('v') == 'h:' + h
                         for c in target_el):
                return
        return super().link(target_el, src, tslot)

    def unlink_from(self, prefix_or_names, slots):
        """remove links on `slots` of kept components whose source is a component built again by the run (commissioning injection
        / reset links are asserted free before they are linked)"""
        h2n = {e.get('h'): n for n, e in self.comp.items()}; n = 0
        for name in list(self.orig):
            el = self.comp[name]
            for c in [c for c in el if c.get('t') == 'b:Link' and child(c, 'targetSlotName').get('v') in slots]:
                src = h2n.get(child(c, 'sourceOrd').get('v')[2:], '')
                if src.startswith(prefix_or_names) : el.remove(c); n += 1
        return n

    def rewire(self, target, tslot, new_src, old_src=None):
        el = self.comp[target]
        L = [c for c in el if c.get('t') == 'b:Link' and child(c, 'targetSlotName').get('v') == tslot]
        if len(L) != 1: raise SystemExit(f'rewire {target}.{tslot}: {len(L)} links')
        so = child(L[0], 'sourceOrd'); ns, sslot = (new_src.split('.', 1) + ['out'])[:2]
        if so.get('v') == 'h:' + self.handle(ns) and child(L[0], 'sourceSlotName').get('v') == sslot: return      # already applied
        if old_src and so.get('v') != 'h:' + self.handle(old_src):
            self.report.append(('FORCED_REWIRE', f'{target}.{tslot}', f'expected {old_src}, set {new_src}'))
        so.set('v', 'h:' + self.handle(ns)); child(L[0], 'sourceSlotName').set('v', sslot)
        self.log.append(('REWIRE', '', target, tslot, f'{old_src} -> {new_src}', ''))


def restricted_instrument(S):
    """make_v6.instrument limited to the rebuilt / new components (kept components keep their extensions and tags)"""
    R = S.rebuilt; reg_hist, reg_alarm, reg_tag = [], [], []
    S.kc('ModeControl', 'NotModeCmdUI', 'Not', {'in': 'ModeCmd_UI'})
    for name, el in S.comp.items():
        t = el.get('t')
        if name not in R or t not in ('c:BooleanWritable', 'c:NumericWritable') or name in M6.NO_HISTORY: continue
        m = S.meta.get(name, {}); is_bool = t == 'c:BooleanWritable'
        cov = is_bool or m.get('kind') in ('param', 'bparam', 'sp', 'mode', 'ai_w') or 'Setpoint' in name
        if name.startswith('Opt_') or name.endswith('_ACTIVE'): cov = False
        en, how, cap = M6.history_ext(S, name, is_bool, cov)
        reg_hist.append((name, S.path_of(name), f'/{M6.STATION}/{name}', en, how, cap))
    for pt, (val, cls, text) in M6.COS.items():
        if pt not in R: continue
        inh = 'NotModeCmdUI' if pt in M6.AI_INHIBIT else None
        M6.alarm_ext(S, pt, 'cos', cls, text, value=val, inhibit=inh)
        reg_alarm.append((pt, S.path_of(pt), 'ChangeOfState', cls, f'alarmValue={str(val).lower()}', text, 'ModeCmd_UI=Local' if inh else ''))
    for pt, (fb, cls, dly) in M6.CMD_FAIL.items():
        if pt not in R: continue
        M6.alarm_ext(S, pt, 'cmd', cls, f'{pt} command/status mismatch', delay=dly, feedback=fb)
        reg_alarm.append((pt, S.path_of(pt), 'CommandFailure', cls, f'feedback={fb}; delay {dly // 1000} s', 'StartStopMismatch', ''))
    for pt, (lo, hi, cls, dly, inh) in M6.OOR.items():
        if pt not in R: continue
        M6.alarm_ext(S, pt, 'oor', cls, f'{pt} out of range', delay=dly, lo=lo, hi=hi, inhibit='ProcessAlarmInhibit' if inh else None)
        reg_alarm.append((pt, S.path_of(pt), 'OutOfRange', cls, f'{lo:g}..{hi:g}; delay {dly // 1000} s', f'{pt} out of range', 'until plant ran 30 min' if inh else ''))
    for i, (pt, loc, cat, ptype) in enumerate(M6.MELCO, 1):
        if pt not in R: continue
        v = f'{i:03d}_{M6.STORE}_{M6.FLOOR}_{M6.COORD}_{loc}_{cat}_{ptype}'
        M6.tag(S.comp[pt], 'melco$3apointNameString', 'b:String', v); reg_tag.append((pt, S.path_of(pt), 'melco:pointNameString', v))
    for name, el in S.comp.items():
        if name not in R or el.get('t') not in ('c:BooleanWritable', 'c:NumericWritable') or name in M6.NO_HISTORY: continue
        marks = {'point'}; kind = S.meta.get(name, {}).get('kind')
        if name.endswith(('Cmd', '_ACTIVE')) or kind == 'ao': marks.add('cmd')
        elif kind in ('param', 'bparam', 'ai_w', 'mode') or 'Setpoint' in name: marks.add('sp')
        else: marks.add('sensor')
        for rx, mk in M6.HS_RULES:
            if re.search(rx, name): marks.update(mk.split())
        marks.add('his')
        for mk in sorted(marks): M6.tag(el, f'hs$3a{mk}', 'b:Marker', 'M')
        reg_tag.append((name, S.path_of(name), 'hs markers', ' '.join(sorted(marks))))
    return reg_hist, reg_alarm, reg_tag


_base_instrument = v77_smart._orig_instrument


def main():
    a = sys.argv[1:]
    regdir = a[a.index('--regdir') + 1] if '--regdir' in a else '.'
    reg = a[a.index('--register') + 1] if '--register' in a else None
    pos = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or a[i - 1] not in ('--regdir', '--register'))]
    if len(pos) < 2: raise SystemExit(__doc__)
    src, out = pos[:2]
    if os.path.exists(out): raise SystemExit('refusing to overwrite ' + out)
    v79_scale.REG = eqreg.load(reg)
    FCX.PROF[0] = M6.TIMING['site']
    sys.argv = [sys.argv[0], '--regdir', regdir]
    with zipfile.ZipFile(src) as z:
        assert z.testzip() is None
        root = ET.fromstring(z.read('file.xml'))
    PF = M6.PARENT_FOLDERS                                         # folder parents as in make_v7.main
    PF['PlantControl'] = PF['PlantControl'] + ['EquipmentPools']; PF['Simulation'] = PF['Simulation'] + ['Instruments']
    items = list(PF.items()); PF.clear()
    for k, v in items:
        if k == 'Energy': PF['Metering'] = ['BTU', 'Power']
        PF[k] = v
    PF[M7.AIR] = ['Common', 'Schedules'] + [u for u, *_ in M7.AIR_UNITS] + ['Simulation']
    S = Upgrade(root)
    n0 = len(S.comp)
    # kind / unit / simulation of the components built before the instrument phase (field IO, histories and alarms read them):
    # from the point list of the last full build (registers/V7_POINT_LIST.csv)
    for r in csv.DictReader(open(os.path.join(HERE, '..', 'registers', 'V7_POINT_LIST.csv'), encoding='utf-8-sig')):
        if r['Point'] in S.comp:
            m = {k: v for k, v in (('kind', r['Kind']), ('unit', r['Unit']), ('ramp', r['Simulation'])) if v}
            if m: S.meta.setdefault(r['Point'], {}).update(m)
    v77_smart._orig_instrument = restricted_instrument
    S.report.append(('UNAPPLY', 'field_io', f'{S.unapply_field_io()} field inputs back on their simulation source before field_io'))
    S.report.append(('UNLINK', 'commissioning', f'{S.unlink_from(("CX_",), ("in9", "in"))} links of CX_ blocks on kept points (rebuilt)'))
    M6.enrich_facets(S)
    for n in S.comp:
        if re.search(r'_(Today|Yesterday|Month|LastMonth)$|RuntimeHours$|_kWh$|_RTh$|Volume$', n): S.meta.setdefault(n, {})['hist'] = '5min'
    reg_hist, reg_alarm, reg_tag = M6.instrument(S)                # V7.7 smart .. V7.9 r7 + Field IO + commissioning + histories
    M6.enrich_facets(S)
    folders, lay = M6.build_folders_and_layout(S)
    air = folders[M7.AIR]; S.rp.remove(air)
    kids = list(S.st); S.st.insert(kids.index(S.rp) + 1, air)
    for i, v in enumerate(S.air_views): air.insert(i, v)
    type_fix = M6.fix_frozen_types(root); M6.fix_symbols(root)
    dup, bad_links, sib, sym = M6.validate(root)
    h2n = {e.get('h'): e.get('n') for e in root.iter('p') if e.get('h')}
    loops = [e.get('n') for e in root.iter('p') if e.get('h') and any(L.get('t') == 'b:Link' and child(L, 'sourceOrd').get('v') == 'h:' + e.get('h') for L in e)]
    multi = [(e.get('n'), s_) for e in root.iter('p') for s_ in {child(L, 'targetSlotName').get('v') for L in e if L.get('t') == 'b:Link'}
             if e.get('n') != 'ConsoleRecipient' and sum(1 for L in e if L.get('t') == 'b:Link' and child(L, 'targetSlotName').get('v') == s_) > 1]
    if loops or multi: raise SystemExit(f'validation failed: self-links {loops[:5]} slots with 2 links {multi[:5]}')
    del h2n
    if dup or bad_links or sib or sym:
        raise SystemExit(f'validation failed: dup {list(dup)[:5]} links {bad_links[:5]} siblings {sib[:5]} symbols {sym[:5]}')
    with zipfile.ZipFile(out, 'x', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('file.xml', ET.tostring(root, encoding='utf-8', xml_declaration=True))
    sha = hashlib.sha256(open(out, 'rb').read()).hexdigest().upper()
    os.makedirs(regdir, exist_ok=True)
    def wcsv(fn, head, rows):
        with open(os.path.join(regdir, fn), 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f); w.writerow(head); w.writerows(rows)
    kept = sorted(S.orig)
    wcsv('UPGRADE_REPORT.csv', ['Action', 'Component', 'Detail'], S.report + [('KEPT_AS_IS', n, S.folder_of[n]) for n in kept])
    wcsv('V7_COMPONENTS.csv', ['Component', 'Folder', 'Type', 'Handle'], [(n, S.folder_of[n], el.get('t'), el.get('h')) for n, el in S.comp.items()])
    wcsv('V7_HISTORY_REGISTER.csv', ['Point', 'Slot_Path', 'History_ID', 'Extension', 'Method', 'Capacity'], reg_hist)
    wcsv('V7_ALARM_REGISTER.csv', ['Point', 'Slot_Path', 'Alarm_Type', 'Alarm_Class', 'Condition', 'Offnormal_Text', 'Inhibit'], reg_alarm)
    from collections import Counter
    c = Counter(r[0] for r in S.report)
    n_links = sum(1 for e in root.iter('p') if e.get('t') == 'b:Link')
    print(f'in {n0} components -> out {len(S.comp)}: rebuilt {len(S.rebuilt) - c["NEW"]}, new {c["NEW"]}, kept as is {len(kept)}, '
          f'kept site values {c["KEPT_VALUE"]}, forced rewires {c["FORCED_REWIRE"]}; links {n_links}; typefix {type_fix}')
    print(f'out {out} sha256 {sha}')


if __name__ == '__main__':
    main()
