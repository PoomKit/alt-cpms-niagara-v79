"""Compact Wire Sheet layout in real Niagara grid units (layout-only).

Ground truth for units comes from a Workbench-written BOG (Codex's disposable
`Arrange All` probe, test_logs/layout_probe.bog): wsAnnotation = "x,y,width" in
wire-sheet grid cells (~12 px at 100 % zoom), default width 8, and vertical
pitch per type (height + 1 cell gap) as measured there:
  And/Or 9, BooleanSwitch/NumericSwitch/LoopPoint 8, BooleanDelay/Latch/
  OneShot/compare/Subtract 7, Not/Hysteresis/Limiter/NumericDelay/
  BooleanToStatusBoolean 6, MultiVibrator 5.
Writables were not in that probe: estimated 6 (Out only) / 7 (with a linked
in16 or fallback), one cell more than the slot-count formula, for safety.

Functional grouping (Request -> Permissive -> Command -> Proof -> Fault -> Stop
per chiller, etc.) is kept from the reviewed V4 map; only coordinates and
widths change. Tall groups wrap into sub-columns.

usage: compact_layout.py in.bog groups_v4.tsv out.bog [--report positions.tsv]
"""
import sys, csv, math, zipfile, hashlib, argparse, os
import xml.etree.ElementTree as ET
from copy import deepcopy
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PITCH = {'And': 9, 'Or': 9, 'BooleanSwitch': 8, 'NumericSwitch': 8, 'LoopPoint': 8,
         'BooleanDelay': 7, 'BooleanLatch': 7, 'OneShot': 7, 'GreaterThanEqual': 7,
         'LessThanEqual': 7, 'LessThan': 7, 'Subtract': 7, 'Not': 6, 'Hysteresis': 6,
         'Limiter': 6, 'NumericDelay': 6, 'BooleanToStatusBoolean': 6, 'MultiVibrator': 5}
COL_GAP, BAND_GAP, MAX_COL_H, ORIGIN = 3, 4, 46, 2

# V5 additions -> existing functional group
V5_GROUP = {
    'TrainHealthy': 'Permissive', 'WaterReady': 'Fault', 'WaterNotReady': 'Fault',
    'AuxProofPending': 'Fault', 'AuxProofTimeout': 'Fault', 'ResetPulse': 'Fault',
    'NotLockoutReset': 'Fault', 'LockoutClock': 'Fault', 'HandoverHold': 'Request'}


def width_cells(name):
    return max(8, math.ceil((len(name) * 5.6 + 30) / 12))


def pitch(c, linked):
    t = c['type'].split(':')[1]
    if t in PITCH:
        return PITCH[t]
    if t.endswith('Writable'):
        return 7 if linked else 6
    return 9


def groups_from_bounds(C, bounds_file):
    B = list(csv.DictReader(open(bounds_file), delimiter='\t'))
    G = {}
    for k, c in C.items():
        if c['pos'] is None:
            continue
        x, y, _ = c['pos']
        for b in B:
            if (b['sheet'] == c['folder'] and int(b['x']) <= x <= int(b['x']) + int(b['width'])
                    and int(b['y']) <= y <= int(b['y']) + int(b['height'])):
                G[k] = (int(b['row']), int(b['x']), b['group']); break
    order = {(b['sheet'], b['group']): (int(b['row']), int(b['x'])) for b in B}
    # V5 components (outside V4 bounds) -> named group
    for k, c in C.items():
        if k in G:
            continue
        n, f = c['name'], c['folder']
        grp = None
        for ch in ('CH01', 'CH02'):
            if ch in n:
                if f == 'SimInputs':
                    grp = ch + '/Inputs'
                elif f == 'SimOutputs':
                    grp = ch + '/Monitor'
                else:
                    for suf, g in V5_GROUP.items():
                        if n.endswith(suf):
                            grp = ch + '/' + g
                if n in ('NotCH02TrainHealthy', 'LeadCH01Selectable', 'Obs_LeadCH01Selectable'):
                    grp = None
                break
        if n in ('NotCH02TrainHealthy', 'LeadCH01Selectable'):
            grp = 'LeadLag'
        if n.startswith('Stage2') and f == 'PlantLogic':
            grp = 'Staging'
        if n in ('Obs_LeadCH01Selectable', 'Obs_Stage2NoLowDTOrRunning'):
            grp = 'Plant'
        if grp is None or (f, grp) not in order:
            raise SystemExit('no group for ' + k)
        G[k] = order[(f, grp)] + (grp,)
    return G


def topo_order(members, C, L, v4pos):
    ms = set(members)
    deps = defaultdict(set)
    for l in L:
        if l['source'] in ms and l['target'] in ms and l['source'] != l['target']:
            deps[l['target']].add(l['source'])
    placed, out = set(), []
    rest = sorted(members, key=lambda k: (v4pos.get(k, (0, 10 ** 6))[1], k))
    while rest:
        for k in rest:  # first member whose in-group sources are placed (cycles fall back to V4 order)
            if deps[k] <= placed:
                break
        else:
            k = rest[0]
        out.append(k); placed.add(k); rest.remove(k)
    return out


def layout(C, L, G):
    linked = {l['target'] for l in L}
    v4pos = {k: c['pos'] for k, c in C.items() if c['pos']}
    pos, rects = {}, defaultdict(list)
    for sheet in ('SimInputs', 'PlantLogic', 'SimOutputs'):
        bands = defaultdict(lambda: defaultdict(list))
        for k, (row, gx, grp) in G.items():
            if C[k]['folder'] == sheet:
                if sheet == 'PlantLogic' and row == 5:   # CT band beside CHW band
                    row, gx = 4, gx + 5000
                bands[row][(gx, grp)].append(k)
        y0 = ORIGIN
        for row in sorted(bands):
            x0, band_h = ORIGIN, 0
            for (gx, grp), members in sorted(bands[row].items()):
                seq = topo_order(members, C, L, v4pos)
                cols, cur, h = [], [], 0
                for k in seq:
                    p = pitch(C[k], k in linked)
                    if cur and h + p > MAX_COL_H:
                        cols.append(cur); cur, h = [], 0
                    cur.append(k); h += p
                cols.append(cur)
                for col in cols:
                    w = max(width_cells(C[k]['name']) for k in col)
                    y = y0
                    for k in col:
                        p = pitch(C[k], k in linked)
                        pos[k] = (x0, y, width_cells(C[k]['name']))
                        rects[sheet].append((k, x0, y, x0 + pos[k][2], y + p - 1))
                        y += p
                    band_h = max(band_h, y - y0)
                    x0 += w + COL_GAP
                x0 += 1  # extra cell between functional groups
            y0 += band_h + BAND_GAP
    return pos, rects


def check_overlap(rects):
    bad = 0
    for sheet, rs in rects.items():
        for i, a in enumerate(rs):
            for b in rs[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    bad += 1; print('OVERLAP', sheet, a[0], b[0])
    return bad


def apply(src, pos, out):
    with zipfile.ZipFile(src) as z:
        assert z.testzip() is None and z.namelist() == ['file.xml']
        orig = ET.fromstring(z.read('file.xml'))
    root = deepcopy(orig)
    rp = next(e for e in root.iter('p') if e.get('n') == 'ReferencePlant')
    n = 0
    for f in rp:
        if f.get('n') not in ('SimInputs', 'PlantLogic', 'SimOutputs'):
            continue
        for c in f:
            if c.tag != 'p' or c.get('t') is None:
                continue
            key = f.get('n') + '/' + c.get('n')
            ann = next((a for a in c if a.get('n') == 'wsAnnotation'), None)
            v = '%d,%d,%d' % pos[key]
            if ann is None:
                ET.SubElement(c, 'p', {'n': 'wsAnnotation', 'f': 'r', 't': 'b:WsAnnotation', 'v': v})
            else:
                ann.set('v', v)
            n += 1
    assert n == len(pos), (n, len(pos))

    def strip(r):
        r = deepcopy(r)
        for e in list(r.iter('p')):
            for c in list(e):
                if c.get('n') == 'wsAnnotation':
                    e.remove(c)
        return ET.tostring(r)
    assert strip(orig) == strip(root), 'non-layout XML changed'
    if os.path.exists(out):
        raise SystemExit('refusing to overwrite ' + out)
    with zipfile.ZipFile(out, 'x', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('file.xml', ET.tostring(root, encoding='utf-8', xml_declaration=True))
    return hashlib.sha256(open(out, 'rb').read()).hexdigest().upper()


if __name__ == '__main__':
    from bog_graph import parse
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('bounds'); ap.add_argument('out')
    ap.add_argument('--report')
    a = ap.parse_args()
    _, C, L, _ = parse(a.src)
    G = groups_from_bounds(C, a.bounds)
    pos, rects = layout(C, L, G)
    bad = check_overlap(rects)
    assert bad == 0
    sha = apply(a.src, pos, a.out)
    for sheet, rs in rects.items():
        W = max(r[3] for r in rs); H = max(r[4] for r in rs)
        print(f'{sheet}: {len(rs)} components, extent {W} x {H} cells (~{W * 12} x {H * 12} px at 100 %)')
    print('overlaps 0 | out', a.out, sha)
    if a.report:
        with open(a.report, 'w', encoding='utf-8') as f:
            for k in sorted(pos, key=lambda k: (C[k]['folder'], pos[k][1], pos[k][0])):
                f.write(f'{k}\t{G[k][2]}\t%d,%d,%d\n' % pos[k])
