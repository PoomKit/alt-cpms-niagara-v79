# -*- coding: utf-8 -*-
"""V7.9 r6: pipe and duct connections of the equipment against the Blender models (tools/blender/equipment79.py).

Ports are the nozzle / opening positions of the Blender models in the equipment frame (metres; x = length, y = up, z = depth,
origin = centre of the footprint at floor level, the frame scaled to the unit size like the 3D page does).
  --apply   one-time coordination fixes of the R9 data (idempotent):
            * AHU / OAU / MAU: sections ordered RA plenum -> mixing box (OA side inlet at mid length) -> filter -> coil -> fan -> SA,
              so the chilled-water coil connections move from the mixing / filter zone to the coil section (counter-flow:
              CHS on the leaving-air side, CHR on the entering-air side); pipes, valves and coil instruments move with them;
              MAT sensor to the mixing box, filter dP to the filter section
            * cooling towers: condenser-water return enters the hot-water header nozzle on the north face (it ended on the fan
              stack centre line), condenser-water supply leaves a basin outlet stub on the south face
  (default) check: every pipe end that belongs to an equipment meets a port of the same service within 25 mm; AHU duct necks meet
            the openings of the model. Exit 1 on a finding (CI).
usage: python3 r9_connections.py [--apply]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MODEL = os.path.join(ROOT, 'graphics3d', 'data', 'r9_model.json')
OFFICE = os.path.join(ROOT, 'graphics3d', 'data', 'office79.json')
TOL = 0.025

# ports per model type, reference size [L, W, H] of the Blender model; positions scale with the unit size
REF = {'chiller': (3.774, 1.771, 2.033), 'pump': (1.75, .65, .85), 'ahu': (3.6, 1.8, 2.1), 'ct': (2.6, 2.6, 2.7), 'exptank': (.9, .9, 1.6), 'bypass': (1.3, .5, 1.04)}
PORTS = {
    'chiller': {'CHR': [(-2.187, 1.08, .43)], 'CHS': [(-2.187, 1.08, -.07)], 'CDS': [(-2.187, .62, -.42)], 'CDR': [(-2.187, .62, -.02)]},
    'pump': {'*': [(-.92, .62, 0), (-.525, 1.11, 0)]},                    # suction (end), discharge (top)
    'ahu': {'CHS': [(1.15, 1.5, -.95)], 'CHR': [(.85, .9, -.95)]},          # coil section, back face (+0.05 m stub)
    'ct': {'CDR': [(0, 2.84, -1.45)], 'CDS': [(-.7, .2, 1.45)]},             # hot-water header nozzle (N), basin outlet (S)
    'exptank': {'*': [(.45, .4, 0)]},
    'bypass': {'*': [(.65, .62, 0), (-.65, .62, 0)]},
}
AHU_OLD = {'CHS': -.9, 'CHR': -1.3}            # R9 coil connection x (mixing / filter zone)
AHU_NEW = {'CHS': 1.15, 'CHR': .85}            # coil section (counter-flow)


def scale(e, p):
    L, W, H = REF[e['type']]
    return (p[0] * e['L'] / 1000 / L, p[1] * e['H'] / 1000 / H, p[2] * e['W'] / 1000 / W)


def to_world(e, p):
    """equipment frame (m) -> model world (mm): page frame x, y up, z = -north; rotation about the vertical axis"""
    lx, ly, lz = scale(e, p); a = math.radians(e.get('rot', 0)); c, s = math.cos(a), math.sin(a)
    dx, dz = c * lx + s * lz, -s * lx + c * lz
    return (e['x'] + dx * 1000, e['y'] - dz * 1000, e['z'] + ly * 1000)


def ahu_units(M):
    units = {e['id']: e for e in M['air_equipment'] if e['type'] == 'ahu'}
    units['MAU-DESIGN'] = {'id': 'MAU-DESIGN', 'type': 'ahu', 'x': 60600, 'y': 12000, 'z': 35200, 'L': 3200, 'W': 1800, 'H': 2000, 'rot': 0}
    return units


def apply():
    M = json.load(open(MODEL, encoding='utf-8')); D = json.load(open(OFFICE, encoding='utf-8'))
    units = ahu_units(M); moved = []
    def shift(px, e, svc, unit_mm):
        """x of a coil connection point: old R9 position -> coil section (only the points on the connection drop)"""
        k = 1000 if unit_mm else 1
        old = e['x'] / 1000 + AHU_OLD[svc]; new = e['x'] / 1000 + AHU_NEW[svc] * e['L'] / 3600   # R9 used fixed offsets for every size
        return new * k if abs(px / k - old) < 1e-3 else None
    # MODEL pipes CHS-Fn / CHR-Fn (mm) + their valves
    for p in M['pipes']:
        u = next((units[x] for x in p.get('eq', []) if x in units), None)
        if not u or p['svc'] not in AHU_OLD: continue
        for q in p['pts']:
            n = shift(q[0], u, p['svc'], True)
            if n is not None: q[0] = n; moved.append(p['id'])
    pmap = {p['id']: p for p in M['pipes']}
    for v in M['valves']:
        p = pmap.get(v['pipe']); u = p and next((units[x] for x in p.get('eq', []) if x in units), None)
        if u and p['svc'] in AHU_OLD:
            n = shift(v['xyz'][0], u, p['svc'], True)
            if n is not None: v['xyz'][0] = n
    # design water pipes *-COIL (m) + instruments on them
    for w in D['waterPipes']:
        if not w['id'].endswith('-COIL'): continue
        u = units[w['id'].split('-', 1)[1][:-5]]
        back_old, back_new = u['y'] / 1000 + .95, u['y'] / 1000 + .95 * u['W'] / 1800       # back face stub follows the unit width
        for q in w['points']:
            n = shift(q[0], u, w['service'], False)
            if n is not None: q[0] = n; moved.append(w['id'])
            if abs(q[1] - back_old) < 1e-3: q[1] = round(back_new, 4)
        end = w['points'][-1] if w['service'] == 'CHS' else w['points'][0]           # connection height scales with the unit height
        end[2] = round(to_world(u, PORTS['ahu'][w['service']][0])[2] / 1000, 4)
    floor_ahu = {u.get('floor'): u for u in units.values() if str(u['id']).startswith('AHU-F')}
    for i in D['instruments']:
        u = units.get(i.get('equipment', ''))
        if not u: continue
        svc = 'CHS' if i['id'].endswith('-CHS') else 'CHR' if (i['id'].endswith('-CHR') or i['kind'] in ('PICV', 'PT')) else None
        if svc:
            n = shift(i['position'][0], u, svc, False)
            if n is not None: i['position'][0] = n
            if abs(i['position'][1] - (u['y'] / 1000 + .95)) < 1e-3: i['position'][1] = round(u['y'] / 1000 + .95 * u['W'] / 1800, 4)
    for d in D['ahuAirDevices']:
        u = units.get(d['equipment'])
        if not u: continue
        if d['id'].startswith('MAT-'): d['position'][0] = round(u['x'] / 1000 - .3 * u['L'] / 3600, 3)
        if d['id'].startswith('FILTER-DP-'): d['position'][0] = round(u['x'] / 1000 + .6 * u['L'] / 3600, 3)
    # cooling towers: CDR -> north hot-water header nozzle, CDS <- south basin outlet stub
    towers = {e['id']: e for e in M['equipment'] if e['type'] == 'ct'}
    for p in M['pipes']:
        t = next((towers[x] for x in p.get('eq', []) if x in towers), None)
        if not t or p['svc'] not in ('CDR', 'CDS'): continue
        q = p['pts'][-1] if p['svc'] == 'CDR' else p['pts'][0]
        if p['svc'] == 'CDR' and abs(q[1] - (t['y'] + 300)) < 1: q[1] = t['y'] + 1450; moved.append(p['id'])
        if p['svc'] == 'CDS' and abs(q[1] - (t['y'] - 1300)) < 1: q[1] = t['y'] - 1450; moved.append(p['id'])
    for p in M['pipes']: p['span'] = [0, sum(math.dist(a, b) for a, b in zip(p['pts'], p['pts'][1:]))]
    json.dump(M, open(MODEL, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    json.dump(D, open(OFFICE, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('moved connection points on', len(set(moved)), 'pipes')


def check():
    M = json.load(open(MODEL, encoding='utf-8')); D = json.load(open(OFFICE, encoding='utf-8'))
    eq = {e['id']: e for e in M['equipment'] + M['air_equipment']}; units = ahu_units(M); bad = []; n = 0
    def near(e, svc, pt_mm):
        ports = PORTS.get(e['type'], {}); cand = ports.get(svc, []) + ports.get('*', [])
        return min((math.dist(to_world(e, c), pt_mm) for c in cand), default=None)
    for p in M['pipes']:
        for x in p.get('eq', []):
            e = eq.get(x)
            if not e or e['type'] not in PORTS: continue
            ds = [near(e, p['svc'], q) for q in (p['pts'][0], p['pts'][-1])]; d = min((x for x in ds if x is not None), default=1e9); n += 1
            if d > TOL * 1000: bad.append(f"{p['id']} -> {x}: nearest port {d:.0f} mm")
    for w in D['waterPipes']:
        if not w['id'].endswith('-COIL'): continue
        e = units[w['id'].split('-', 1)[1][:-5]]; q = [c * 1000 for c in (w['points'][-1] if w['service'] == 'CHS' else w['points'][0])]
        d = near(e, w['service'], q); n += 1
        if d is None or d > TOL * 1000: bad.append(f"{w['id']}: nearest coil port {d:.0f} mm")
    # AHU duct necks: RA top at the west end, SA top at the east end, OA side inlet into the mixing box (+z face)
    for d in D['ducts']:
        for kind, sx in (('RA-AHU-NECK', -.5), ('SA-AHU-COMMON', .5)):
            if d['id'].startswith(kind):
                f = d['floor']; u = next((x for x in units.values() if x.get('floor') == f and str(x['id']).startswith('AHU-F')), None)
                if u and abs(d['points'][0][0] * 1000 - (u['x'] + sx * u['L'])) > TOL * 1000: bad.append(f"{d['id']}: not at the AHU end face")
                n += 1
        if d['id'].startswith('OA-AHU-NECK'):
            f = d['floor']; u = next((x for x in units.values() if x.get('floor') == f and str(x['id']).startswith('AHU-F')), None)
            end = d['points'][-1]; n += 1
            if u and not (abs(end[1] * 1000 - (u['y'] - u['W'] / 2)) <= 160 and -.28 * u['L'] <= end[0] * 1000 - u['x'] <= .11 * u['L']):
                bad.append(f"{d['id']}: OA neck does not enter the mixing box")
    for b in bad: print('FINDING', b)
    print(f'{n} connections checked, {len(bad)} findings'); return not bad


if __name__ == '__main__':
    if '--apply' in sys.argv: apply()
    sys.exit(0 if check() else 1)
