# -*- coding: utf-8 -*-
"""V7.9 r5: station point of every R9 field device / design unit shown on the 3D page, and the coverage report.

Every device of the R9 design (graphics3d/data/office79.json: instruments, AHU air devices, motorised dampers, roof design units,
and the plant units ET-01 / DPB-01 of r9_model.json) is mapped by rule to the station point that measures or drives it.
A point is only accepted when it exists:
  * in the last full station build (registers/V7_COMPONENTS.csv, V7.8 base + V7.9 r2 layer), or
  * in the r4 office layer (graphics3d/data/office_points.json, built by tools/office_points.py from the layer code).
Devices without a point are listed as UNBOUND with the reason (design gap / point to be added), never guessed.
Outputs: graphics3d/data/r9_bindings.json (read by graphics3d/rebuild_page.py) and docs/R9_POINT_COVERAGE.csv.
usage: python3 r9_bindings.py            --check: exit 1 if a committed output is stale (CI)"""
import csv, io, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
OUT_JSON = os.path.join(ROOT, 'graphics3d', 'data', 'r9_bindings.json')
OUT_CSV = os.path.join(ROOT, 'docs', 'R9_POINT_COVERAGE.csv')


def station_points():
    pts = {}
    with open(os.path.join(ROOT, 'registers', 'V7_COMPONENTS.csv'), encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if not r['Type'].startswith('c:'): continue          # writable / point components only (not logic blocks)
            fo = r['Folder']
            pts[r['Component']] = ('/' + fo if fo.startswith('AirSide') else '/ChillerPlant/' + fo) + '/' + r['Component'], 'V7.8 base / V7.9 r2'
    op = json.load(open(os.path.join(ROOT, 'graphics3d', 'data', 'office_points.json'), encoding='utf-8'))
    for n, s in op['points'].items(): pts.setdefault(n, (s, 'V7.9 r4 office layer'))
    return pts


def ahu_key(eq):
    """R9 equipment id -> station prefix: AHU-F02 -> ('F', 'AHU_F02'), AHU-01 -> ('B', 'AHU01'), OAU-01 -> ('B', 'OAU01')"""
    m = re.match(r'AHU-F(\d\d)$', eq)
    if m: return 'F', f'AHU_F{m.group(1)}'
    m = re.match(r'(AHU|OAU)-(\d\d)$', eq)
    if m: return 'B', f'{m.group(1)}{m.group(2)}'
    return None, None


# AHU air devices: R9 kind / id prefix -> point suffix (floor AHUs of the r4 layer, base AHUs of V7.8)
AIR_F = {'VSD': 'SpeedFb', 'SAT': 'SAT', 'RAT': 'RAT', 'MAT': 'MAT', 'OA-AF': 'OAFlow', 'FILTER-DP': 'FilterDP', 'DUCT-DP': 'DuctSP',
         'MD-OA': 'OADmpFb', 'MD-RA': 'RADmpFb', 'MD-RELIEF': 'RelDmpFb'}                       # measured feedbacks (r4 layer field AIs)
AIR_B = {'VSD': 'SpeedFeedbackHz', 'SAT': 'SAT', 'RAT': 'RAT', 'FILTER-DP': 'FilterDP', 'DUCT-DP': 'DuctStatic', 'MD-OA': 'OADamperCmd',
         'MAT': 'MAT', 'OA-AF': 'OAFlow', 'MD-RA': 'RADmpFb', 'MD-RELIEF': 'RelDmpFb'}                 # r6: ground-floor AHU devices (v79_r6.py)


def rule(d, kind):
    """candidate point names of one device (first existing one wins) + reason text when none exists"""
    i = d['id']
    if kind == 'air':
        pre = i.rsplit('-AHU-', 1)[0]
        typ, k = ahu_key(d['equipment'])
        tab = AIR_F if typ == 'F' else AIR_B
        if pre in tab: return [f'{k}_{tab[pre]}'], ''
        return [], f'{d["equipment"]}: no {pre} point in the station (V7.8 AHU has no {pre} sensor / actuator)'
    if kind == 'inst':
        m = re.match(r'(TT|PT|FM|BTU|MBFV)-CH-(\d\d)(?:-(\w+))?$', i)
        if m:
            k, n, s = m.groups(); c = f'CH{n}'
            if k == 'TT': return [{'CHR': f'{c}_ChwReturnTemp', 'CDS': f'{c}_CdwEnteringTemp', 'CDR': f'{c}_CdwLeavingTemp', 'CHS': f'{c}_ChwSupplyTemp'}[s]], ''
            if k == 'PT': return [f'{c}_EvapDP' if s in ('CHS', 'CHR') else f'{c}_CondDP'], f'{c}: the station has no {"evaporator" if s in ("CHS", "CHR") else "condenser"} pressure point for this slot'
            if k == 'FM': return [f'{c}_ChwFlow'], ''
            if k == 'BTU': return [f'{c}_RT'], ''
            if k == 'MBFV': return ([f'{c}_ChwFCVFb', f'{c}_ChwIsoFb'] if s == 'CHS' else [f'{c}_CdwHPVFb', f'{c}_CdwIsoFb']), ''
        m = re.match(r'PT-(CHP|CDP)-(\d\d)$', i)
        if m: return [f'{m.group(1)}{m.group(2)}_DischargePressure'], ''
        m = re.match(r'PICV-(.+)$', i)
        if m:
            typ, k = ahu_key(m.group(1))
            if typ == 'F': return [f'{k}_PICVFb', f'{k}_ValveCmd'], ''
            if typ == 'B': return [f'{k}_ValveFeedback', f'{k}_ValveCmd'], ''
            return (['MAU_ValveCmd'], '') if m.group(1) == 'MAU-DESIGN' else ([], f'{m.group(1)} is a design unit without station points')
        m = re.match(r'(FM|TT-S|TT-R)-F(\d\d)$', i)
        if m: return [{'FM': f'FM_F{m.group(2)}_Flow', 'TT-S': f'TT_S_F{m.group(2)}', 'TT-R': f'TT_R_F{m.group(2)}'}[m.group(1)]], ''
        m = re.match(r'MBFV-([SR])-F(\d\d)$', i)
        if m: return [f"ISO_F{m.group(2)}_{'CHS' if m.group(1) == 'S' else 'CHR'}_Fb"], 'floor isolation valve point not built'
        m = re.match(r'(TT|PT|MBFV)-(AHU-F\d\d|AHU-\d\d|OAU-\d\d|MAU-DESIGN)(?:-(CHS|CHR))?$', i)
        if m:                                                        # r6: coil instruments (v79_r6.instruments)
            k, e, svc = m.groups(); typ, u = ahu_key(e); u = 'MAU' if e == 'MAU-DESIGN' else u
            return [{'TT': f'COIL_{u}_{svc}_T', 'PT': f'COIL_{u}_DP', 'MBFV': f'ISO_{u}_{svc}_Fb'}[k]], 'coil instrument point not built'
        return [], 'no rule'
    if kind == 'md':
        if d.get('integralVAV'): return [f"VAV_{re.sub(r'[^A-Za-z0-9]+', '_', d['room'])}_DmpFb"], ''
        return [f"TE_{re.sub(r'[^A-Za-z0-9]+', '_', d['room'])}_DmpFb"], 'toilet / janitor exhaust damper: point not built'
    if kind == 'unit':
        return {'ET-01': (['CHW_ExpansionTankPressure'], ''), 'DPB-01': (['CHW_BypassValveFeedback'], ''),
                'KEF-DESIGN': (['KEF_Status'], ''), 'TEF-DESIGN': (['TEF_Status'], ''), 'MAU-DESIGN': (['MAU_Status'], ''), 'RF-RELIEF': (['RF_Status'], ''),
                'CP-01': ([], 'control panel (no single point)')}.get(i, ([], 'R9 design unit (roof): not in the station'))
    return [], 'no rule'


def build():
    import io as _io                                            # noqa: F401
    D = json.load(open(os.path.join(ROOT, 'graphics3d', 'data', 'office79.json'), encoding='utf-8'))
    M = json.load(open(os.path.join(ROOT, 'graphics3d', 'data', 'r9_model.json'), encoding='utf-8'))
    pts = station_points()
    devs = [(d, 'inst', d['kind']) for d in D['instruments']] + [(d, 'air', d['kind']) for d in D['ahuAirDevices']] + \
           [(d, 'md', 'MD') for d in D['motorizedDampers']] + [(d, 'unit', d['type']) for d in D['equipment']] + \
           [(e, 'unit', e['type']) for e in M['equipment'] if e['type'] in ('exptank', 'bypass', 'panel')]
    bind, rows = {}, []
    for d, kind, typ in devs:
        cands, why = rule(d, kind)
        hit = next((c for c in cands if c in pts), None)
        fl = d.get('floor')
        if hit:
            bind[d['id']] = {'p': hit, 's': pts[hit][0]}
            rows.append([d['id'], typ, fl, 'BOUND', hit, pts[hit][0], pts[hit][1], ''])
        else:
            rows.append([d['id'], typ, fl, 'UNBOUND', '', '', '', why or ('no station point: ' + ', '.join(cands))])
    return bind, rows


def outputs():
    bind, rows = build()
    js = json.dumps({'note': 'generated by tools/r9_bindings.py - do not edit', 'bind': bind}, ensure_ascii=False, indent=0, sort_keys=True)
    buf = io.StringIO(); w = csv.writer(buf, lineterminator='\n')
    w.writerow(['device', 'kind', 'floor', 'status', 'point', 'slot_path', 'source', 'reason_if_unbound']); w.writerows(rows)
    return js, buf.getvalue(), rows


if __name__ == '__main__':
    js, cs, rows = outputs()
    if '--check' in sys.argv:
        bad = [p for p, new in ((OUT_JSON, js), (OUT_CSV, cs)) if not os.path.exists(p) or open(p, encoding='utf-8').read() != new]
        if bad: print('stale:', ', '.join(bad), '- run tools/r9_bindings.py'); sys.exit(1)
        print('r9_bindings.json / R9_POINT_COVERAGE.csv up to date'); sys.exit(0)
    open(OUT_JSON, 'w', encoding='utf-8').write(js); open(OUT_CSV, 'w', encoding='utf-8').write(cs)
    from collections import Counter
    c = Counter((r[1], r[3]) for r in rows)
    print('devices', len(rows), 'bound', sum(r[3] == 'BOUND' for r in rows))
    for k in sorted({r[1] for r in rows}): print(f'  {k:8s} bound {c[(k, "BOUND")]:4d}  unbound {c[(k, "UNBOUND")]:4d}')
