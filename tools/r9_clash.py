# -*- coding: utf-8 -*-
"""V7.9 r7: pipe / valve / instrument coordination of the 3D model (r9_model.json + office79.json).

  --apply   one-time coordination fixes (idempotent):
            * pipe routes that ran through another pipe: CDW headers through the CHW risers (B1), CDS / CDR headers on the same
              line (B1), chiller CDW return branch through the CHW supply branch, CHW return branch through the CDS header, CHS header
              corner against the CHR suction drop, roof OAU / MAU coil pipes through the CDS / CDR roof headers and the risers, AHU-02
              coil return through the floor-1 meter feed; pipes that doubled back on themselves (dead stubs) are cleaned
            * legacy AHU CHW valves replaced by the R9 PICV are hidden (R9 replacedLegacyValves)
            * every valve / fitting / instrument is kept on its pipe axis, out of the bends and the pipe ends, spaced along the pipe
              by its body length, and its stem (actuator / transmitter head) is turned away from neighbouring pipes
  (default) check, exit 1 on a finding (CI):
            * pipe against pipe (outside radius incl. insulation; coaxial continuations and perpendicular tees are connections)
            * valve / instrument bodies overlapping on a pipe, inside a bend or at a pipe end, off the pipe axis
            * stems / heads running into another pipe
usage: python3 r9_clash.py [--apply]"""
import json, math, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
MODEL = os.path.join(ROOT, 'graphics3d', 'data', 'r9_model.json')
OFFICE = os.path.join(ROOT, 'graphics3d', 'data', 'office79.json')
GAP = .03                                    # clear distance between two bodies on a pipe (m)

# ---------------------------------------------------------------------------------------------------------------- vector helpers
def sub(a, b): return [a[i] - b[i] for i in range(3)]
def add(a, b): return [a[i] + b[i] for i in range(3)]
def mul(a, k): return [x * k for x in a]
def dot(a, b): return sum(a[i] * b[i] for i in range(3))
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def norm(a): return math.sqrt(dot(a, a))
def unit(a): n = norm(a); return [x / n for x in a] if n > 1e-12 else [0, 0, 0]
def dist(a, b): return norm(sub(a, b))
def pt_seg(p, a, b):
    ab = sub(b, a); L = dot(ab, ab); t = 0 if L < 1e-12 else max(0, min(1, dot(sub(p, a), ab) / L)); return dist(p, add(a, mul(ab, t))), t
def seg_seg(p1, q1, p2, q2):
    d1, d2, r = sub(q1, p1), sub(q2, p2), sub(p1, p2); a, e, f = dot(d1, d1), dot(d2, d2), dot(d2, r)
    if a < 1e-12: s = 0; t = max(0, min(1, f / e)) if e > 1e-12 else 0
    else:
        c = dot(d1, r)
        if e < 1e-12: t = 0; s = max(0, min(1, -c / a))
        else:
            b = dot(d1, d2); den = a * e - b * b; s = max(0, min(1, (b * f - c * e) / den)) if den > 1e-12 else 0
            t = (b * s + f) / e
            if t < 0: t = 0; s = max(0, min(1, -c / a))
            elif t > 1: t = 1; s = max(0, min(1, (b - c) / a))
    return dist(add(p1, mul(d1, s)), add(p2, mul(d2, t)))

# ---------------------------------------------------------------------------------------------------------------- data
def load():
    return json.load(open(MODEL, encoding='utf-8')), json.load(open(OFFICE, encoding='utf-8'))

def pipes_of(M, D):
    """id -> {pts (m), r (bare outside radius), ro (incl. insulation), svc, src, rb (bend radius of the 3D page, 0 = mitred)}"""
    P = {}
    for p in M['pipes']:
        r = p['dn'] * 25.4 / 2 * 1.08 / 1000; ins = .045 if M['service'][p['svc']][2] else 0
        P[p['id']] = {'pts': [[c / 1000 for c in q] for q in p['pts']], 'r': r, 'ro': r + ins, 'ins': ins, 'svc': p['svc'], 'src': 'M',
                      'rb': max(.15, p['dn'] * 25.4 * 1.5 / 1000), 'raw': p}
    for p in D['waterPipes']:
        r = p['outsideRadius_m']
        P[p['id']] = {'pts': p['points'], 'r': r, 'ro': r, 'ins': 0, 'svc': p['service'], 'src': 'W', 'rb': 0, 'raw': p}
    return P

def cum(pts):
    c = [0]
    for i in range(len(pts) - 1): c.append(c[-1] + dist(pts[i], pts[i + 1]))
    return c

def project(pts, p):
    """nearest point of the polyline: (s along the pipe, distance, segment index)"""
    c = cum(pts); best = (1e9, 0, 0)
    for i in range(len(pts) - 1):
        d, t = pt_seg(p, pts[i], pts[i + 1])
        if d < best[0] - 1e-9: best = (d, c[i] + t * (c[i + 1] - c[i]), i)
    return best[1], best[0], best[2]

def at(pts, s):
    c = cum(pts)
    for i in range(len(pts) - 1):
        if s <= c[i + 1] + 1e-9 or i == len(pts) - 2:
            L = c[i + 1] - c[i]; t = 0 if L < 1e-12 else max(0, min(1, (s - c[i]) / L)); return add(pts[i], mul(sub(pts[i + 1], pts[i]), t)), i
    return pts[-1], len(pts) - 2

# ---------------------------------------------------------------------------------------------------------------- items
SCALED = {'MBFV': .1, 'FM': .1, 'PICV': .035}            # devices79.js PIPE_REF: R9 models sized by the pipe radius
def items_of(M, D, P):
    """every valve / fitting / instrument on a pipe: {o, src, kind, pipe, pos (m), half (axial half length), fixed, stem_len}"""
    out = []
    for v in M['valves']:
        if v['pipe'] not in P or v.get('hidden'): continue
        pr = P[v['pipe']]; K = v['kind']; r = (v.get('dn') or pr['raw']['dn']) * 25.4 / 2 * 1.08 / 1000; ins = pr['ins']
        half = {'BFV': max(.08, r * 1.1), 'MBFV': .125, 'MCV': .125, 'CHECK': .07, 'STRAINER': r * 1.45, 'FLEX': r * 1.12,
                'FM': max(r * 1.12, .09), 'PG': .05, 'TT': .05, 'FS': .05, 'PT': .05, 'AAV': .04, 'DRAIN': .04}.get(K, .05)
        stem = {'BFV': r * 1.3 + .16, 'MBFV': r * 1.3 + .47, 'MCV': r * 1.3 + .47, 'FM': r * 1.2 + .23, 'PG': r + ins + .19,
                'TT': r + ins + .14, 'FS': r + ins + .14, 'PT': r + ins + .14, 'STRAINER': r * 2.2}.get(K, 0)
        out.append({'o': v, 'src': 'V', 'kind': K, 'pipe': v['pipe'], 'pos': [c / 1000 for c in v['xyz']], 'half': half,
                    'fixed': K in ('CAP', 'RED_E', 'RED_C') or K.startswith('RED'), 'stem_len': stem, 'r': r})
    for d in D['instruments']:
        if d.get('pipe') not in P: continue
        pr = P[d['pipe']]; K = d['kind']; r = pr['r']; ref = SCALED.get(K); s = max(.35, min(3, r / ref)) if ref else 1
        half = {'MBFV': max(.085 * s, .06), 'FM': .159 * s, 'PICV': .07 * s, 'BTU': .1, 'TT': .06, 'PT': .07}.get(K, .06)
        stem = {'MBFV': .357 * s, 'FM': .3 * s, 'PICV': .161 * s, 'BTU': r + .32, 'TT': r + .19, 'PT': r + .21}.get(K, r + .2)
        out.append({'o': d, 'src': 'I', 'kind': K, 'pipe': d['pipe'], 'pos': list(d['position']), 'half': half, 'fixed': False,
                    'stem_len': stem, 'r': r})
    return out

def run_window(P, pid, seg, half, ends):
    """usable [lo, hi] (s along the pipe) of segment seg for a body of half length `half`"""
    pr = P[pid]; pts = pr['pts']; c = cum(pts); n = len(pts) - 1
    def bend(i):                                          # clearance taken by the bend at vertex i (1 .. n-1)
        L1, L2 = c[i] - c[i - 1], c[i + 1] - c[i]
        return (min(pr['rb'], L1 * .48, L2 * .48) if pr['rb'] else pr['ro']) + .02
    lo = c[seg] + (ends[0] if seg == 0 else bend(seg)) + half
    hi = c[seg + 1] - (ends[1] if seg == n - 1 else bend(seg + 1)) - half
    return lo, hi

def end_clear(P, pid):
    """clearance at the two pipe ends: a branch that starts on another pipe's axis (tee) keeps out of that pipe"""
    pts = P[pid]['pts']; res = []
    for e in (pts[0], pts[-1]):
        c = .04
        for q, pr in P.items():
            if q == pid: continue
            for i in range(len(pr['pts']) - 1):
                d, t = pt_seg(e, pr['pts'][i], pr['pts'][i + 1])
                if d < pr['ro'] * .6 and .001 < t < .999: c = max(c, pr['ro'] + .05)
            for o in (pr['pts'][0], pr['pts'][-1]):                       # end-to-end joint with another pipe (elbow / tee)
                if dist(o, e) < .005: c = max(c, pr['ro'] + .06)
        res.append(c)
    return res

# ---------------------------------------------------------------------------------------------------------------- checks
def pipe_clashes(P):
    segs = []
    for pid, pr in P.items():
        for i in range(len(pr['pts']) - 1): segs.append((pid, pr, pr['pts'][i], pr['pts'][i + 1]))
    out = []
    for i in range(len(segs)):
        a = segs[i]
        for j in range(i + 1, len(segs)):
            b = segs[j]
            if a[0] == b[0]: continue
            need = a[1]['ro'] + b[1]['ro']
            if max(min(a[2][k], a[3][k]) - max(b[2][k], b[3][k]) for k in range(3)) > need: continue   # bounding boxes apart
            d = seg_seg(a[2], a[3], b[2], b[3])
            if d >= need - .005: continue
            u, w = unit(sub(a[3], a[2])), unit(sub(b[3], b[2]))
            par = abs(dot(u, w)) > .995
            if par and a[1]['svc'] == b[1]['svc'] and norm(cross(sub(b[2], a[2]), w)) < .01:
                continue                                                           # coaxial continuation of the same service
            tee = False
            for (e, s2, o) in ((a[2], b, a), (a[3], b, a), (b[2], a, b), (b[3], a, b)):
                dd, t = pt_seg(e, s2[2], s2[3])
                if dd < s2[1]['ro'] + .02 and abs(dot(unit(sub(o[3], o[2])), unit(sub(s2[3], s2[2])))) < .5: tee = True
            if tee: continue
            out.append(f'pipe {a[0]} ({a[1]["svc"]}) / {b[0]} ({b[1]["svc"]}): axes {d:.3f} m apart, need {need:.3f} m')
    return out

def stem_dir(it):
    o = it['o']; s = o.get('stem')
    return s if s else None

def stem_hits(P, it, d, pos=None):
    """other pipes hit by the stem of item `it` pointing to unit vector d"""
    pos = pos or it['pos']; hits = []; L = it['stem_len']
    if L <= 0: return hits
    pts = P[it['pipe']]['pts']; i0 = project(pts, pos)[2]; ax = unit(sub(pts[i0 + 1], pts[i0]))
    a = add(pos, mul(d, P[it['pipe']]['ro'] + .02)); b = add(pos, mul(d, L))
    for q, pr in P.items():
        if q == it['pipe']: continue
        for i in range(len(pr['pts']) - 1):
            if seg_seg(a, b, pr['pts'][i], pr['pts'][i + 1]) < pr['ro'] + .06:
                # a stem may touch the pipe it continues into at a tee / continuation only if same service and coaxial ends
                w = unit(sub(pr['pts'][i + 1], pr['pts'][i]))
                if abs(dot(w, ax)) > .995 and norm(cross(sub(pr['pts'][i], pos), ax)) < .01: continue   # coaxial continuation
                hits.append(q); break
    return hits

def candidates(P, it):
    pts = P[it['pipe']]['pts']; s, _, i = project(pts, it['pos']); ax = unit(sub(pts[i + 1], pts[i]))
    if abs(ax[2]) > .9:                                     # vertical pipe: horizontal stems
        return [[1, 0, 0], [0, 1, 0], [-1, 0, 0], [0, -1, 0]]
    side = unit(cross(ax, [0, 0, 1]))
    return [[0, 0, 1], side, mul(side, -1), [0, 0, -1]]

def item_checks(P, items):
    out = []
    by = {}
    for it in items: by.setdefault(it['pipe'], []).append(it)
    for pid, L in by.items():
        ends = end_clear(P, pid); pts = P[pid]['pts']; rows = []
        for it in L:
            s, d, seg = project(pts, it['pos']); name = it['o'].get('id') or f"{it['kind']} {it['o'].get('tag', '')}".strip()
            if d > .005: out.append(f'{pid}: {name} {d:.3f} m off the pipe axis')
            if not it['fixed']:
                lo, hi = run_window(P, pid, seg, it['half'], ends)
                if lo <= hi and not (lo - .005 <= s <= hi + .005): out.append(f'{pid}: {name} in a bend / pipe end (s {s:.2f}, run {lo:.2f}..{hi:.2f})')
            rows.append((s, it, name))
            sd = stem_dir(it)
            if sd and stem_hits(P, it, sd): out.append(f'{pid}: {name} stem runs into {", ".join(stem_hits(P, it, sd))}')
        rows.sort(key=lambda r: r[0])
        for (s1, a, n1), (s2, b, n2) in zip(rows, rows[1:]):
            if s2 - s1 < a['half'] + b['half'] + GAP - .005 and not (a['fixed'] and b['fixed']):
                out.append(f'{pid}: {n1} / {n2} overlap ({s2 - s1:.3f} m apart, need {a["half"] + b["half"] + GAP:.3f} m)')
    return out

# ---------------------------------------------------------------------------------------------------------------- fixes
def mm(pts): return [[round(c * 1000, 1) for c in q] for q in pts]

CHP_SHIFT = 600.0   # CHW pumps moved east: the suction pipe (0.78 m) had no room for valve + strainer + flexible connector
ROUTES_M = {      # pipe id -> new route (mm); ends unchanged (equipment / riser connections)
    'CDR-H': [[3680.0, 6700.0, -1800.0], [62600.0, 6700.0, -1800.0], [62600.0, 15000.0, -1800.0], [39000.0, 15000.0, -1800.0],
              [39000.0, 20100.0, -1800.0], [38200.0, 20100.0, -1800.0]],
    'CDS-SH': [[37200, 20100, -1800], [36400, 20100, -1800], [36400, 14200, -1800], [56700, 14200, -1800], [56700, 14200, -5380],
               [56700, 700, -5380]],                                  # suction header 1000 mm west: room for valve, strainer, flex
    'CHR-SH': [[37200, 18500, -2400], [37200, 13600, -2400], [51300, 13600, -2400], [51300, 13600, -5380], [51300, 700, -5380]],
    'CHW-BP': [[50000.0, 6100, -2700.0], [50000.0, 6100, -4900.0], [50000.0, 8600.0, -4900.0], [51300.0, 8600.0, -4900.0],
               [51300.0, 8600.0, -5380.0]],
    'CHR-DH': [[53075.0, 700.0, -3400.0], [53075.0, 11900.0, -3400.0]],      # CHW pumps 600 mm east (CHP_SHIFT)
    'CHR-EH': [[53075.0, 6600, -3400.0], [51700.0, 6600, -3400.0], [51700.0, 7300, -3400.0], [4130.0, 7300, -3400.0]],
    'CHS-H': [[3630, 6100, -2700], [51900, 6100, -2700], [51900, 14200, -2700], [38200, 14200, -2700], [38200, 18500, -2700]],
}
def chiller_routes(M):
    """CDR branch: offset 720 mm east before it rises (it rose through the CHS branch); CHR branch: drops 500 mm further from the
    CDS header (it ran through it)"""
    out = {}
    for p in M['pipes']:
        q = p['pts']
        if p['id'][:5] == 'CDS-P' and q[0][0] == 57700.0:                  # CDW pump suction from the moved header
            out[p['id']] = [[56700.0, q[0][1], q[0][2]]] + q[1:]
        if p['id'][:5] == 'CHR-P' and q[-1][0] == 52080.0:                 # CHW pumps 600 mm east: suction, discharge
            out[p['id']] = q[:-1] + [[52080.0 + CHP_SHIFT, q[-1][1], q[-1][2]]]
        if p['id'][:5] == 'CHR-D' and q[0][0] == 52475.0:
            out[p['id']] = [[52475.0 + CHP_SHIFT, c[1], c[2]] for c in q]
        if p['id'].startswith('CDR-C') and len(q) == 3 and q[0][1] > q[1][1]:
            x, y0, z0 = q[0]; y1, z1 = q[1][1], q[2][2]; x2 = x + 720
            out[p['id']] = [[x, y0, z0], [x, y1 + 1100, z0], [x2, y1 + 1100, z0], [x2, y1, z0], [x2, y1, z1]]
        if p['id'].startswith('CHR-E') and len(q) == 3 and q[0][1] < q[2][1] and q[0][2] > q[1][2]:
            x, y0, z0 = q[0]; z1, y2 = q[1][2], q[2][1]
            out[p['id']] = [[x, y0, z0], [x, y0 + 500, z0], [x, y0 + 500, z1], [x, y2, z1]]
    return out

def roof_routes(D):
    """roof coil pipes: CHS climbs at the riser and crosses below the CDR header, CHR leaves the riser below the CDS header"""
    out = {}
    for p in D['waterPipes']:
        q = p['points']
        if p['id'] in ('CHS-OAU-01-COIL', 'CHS-MAU-DESIGN-COIL') and q[1] == [38.2, 18.5, 35.9]:
            out[p['id']] = [q[0], [38.2, 18.5, 34.9], [39.3, 18.5, 34.9], [39.3, 18.5, 35.9]] + q[3:]
        if p['id'] in ('CHR-OAU-01-COIL', 'CHR-MAU-DESIGN-COIL') and q[-3] == [39.3, 18.5, 35.6]:
            out[p['id']] = q[:-3] + [[39.3, 19.1, 35.6], [39.3, 19.1, 34.6], [37.2, 19.1, 34.6], [37.2, 18.5, 34.6], [37.2, 18.5, 34.3]]
        if p['id'] == 'CHR-AHU-02-COIL' and [39.3, 18.5, 1.95] in q:
            out[p['id']] = q[:3] + [[39.3, 28.2, 1.95], [39.3, 19.75, 1.95], [37.65, 19.75, 1.95], [37.65, 19.35, 1.95], [37.65, 19.35, 2.2]]
    return out

def unbacktrack(q):
    """remove vertices where the route doubles back on itself (dead stub)"""
    q = [list(x) for x in q]; ch = True
    while ch:
        ch = False
        for i in range(1, len(q) - 1):
            u, w = sub(q[i], q[i - 1]), sub(q[i + 1], q[i])
            if norm(u) > 1e-9 and norm(w) > 1e-9 and dot(unit(u), unit(w)) < -.999: del q[i]; ch = True; break
            if norm(u) < 1e-9: del q[i]; ch = True; break
    return q

def pack(P, pid, free, fixed, ends):
    """place the bodies in pipe order: forward pass (each at its own position or just after the previous one, inside a straight
    run, clear of fixed fittings), then a backward pass for what ran past the pipe end"""
    n = len(P[pid]['pts']) - 1
    def runs(h): return [w for w in (run_window(P, pid, k, h, ends) for k in range(n)) if w[0] <= w[1]]
    def clear(it, x, d):                          # step past fixed fittings in direction d
        for _ in range(4):
            hit = [f for f in fixed if abs(x - f['s']) < it['half'] + f['half'] + GAP - 1e-6]
            if not hit: return x
            f = hit[0]; x = f['s'] + d * (it['half'] + f['half'] + GAP)
        return x
    row = sorted(free, key=lambda it: it['s']); prev = -1e9; over = False
    for it in row:
        want = max(it['s'], prev + it['half'] + GAP); place = None
        for lo, hi in runs(it['half']):
            if want <= hi:
                x = clear(it, max(want, lo), 1)
                if x <= hi: place = x; break
        if place is None: place = want; over = True
        it['s'] = place; prev = place + it['half']
    if over:
        nxt = 1e9
        for it in reversed(row):
            want = min(it['s'], nxt - it['half'] - GAP); place = None
            for lo, hi in reversed(runs(it['half'])):
                if want >= lo:
                    x = clear(it, min(want, hi), -1)
                    if x >= lo: place = x; break
            it['s'] = place if place is not None else want; nxt = it['s'] - it['half']

def merge_overlaps(R, svc):
    """pipes of one service that meet at a node and leave it on the same line (coaxial overlap, e.g. a floor branch drawn into
    the meter-feed node) are cut back to where the overlap ends, so the junction is where the pipes really part"""
    for _ in range(50):
        nodes = {}
        for pid, q in R.items():
            for end in (0, -1):
                k = tuple(round(c, 3) for c in q[end]); nodes.setdefault((svc[pid], k), []).append((pid, end))
        done = True
        for (_, k), mem in nodes.items():
            if len(mem) < 2: continue
            dirs = []
            for pid, end in mem:
                q = R[pid]; a, b = (q[0], q[1]) if end == 0 else (q[-1], q[-2]); dirs.append((unit(sub(b, a)), dist(a, b), pid, end))
            for i in range(len(dirs)):
                grp = [x for x in dirs if dot(x[0], dirs[i][0]) > .999]
                if len(grp) < 2: continue
                L = min(x[1] for x in grp); N = list(R[grp[0][2]][grp[0][3]]); nn = add(N, mul(grp[0][0], L))
                for d, ln, pid, end in grp:
                    q = R[pid]
                    if ln - L < 1e-4: q.pop(end)                     # the whole segment was overlap
                    else: q[end] = [round(c, 4) for c in nn]
                    if len(q) < 2: q[:] = [N, nn]
                done = False; break
            if not done: break
        if done: return

def apply(M, D):
    changed = set(); log = []
    old = {p['id']: [[c / 1000 for c in q] for q in p['pts']] for p in M['pipes']}
    old.update({p['id']: [list(x) for x in p['points']] for p in D['waterPipes']})
    routes = dict(ROUTES_M); routes.update(chiller_routes(M))
    for p in M['pipes']:
        new = routes.get(p['id'], p['pts']); new = [[float(c) for c in q] for q in unbacktrack(new)]
        if new != [[float(c) for c in q] for q in p['pts']]:
            L0 = cum(old[p['id']])[-1]; p['pts'] = new; L1 = cum([[c / 1000 for c in q] for q in new])[-1] * 1000
            if p.get('span') and abs(p['span'][1] - L0 * 1000) < 2: p['span'] = [p['span'][0], round(L1, 1)]
            changed.add(p['id']); log.append(f'route {p["id"]}')
    for e in M['equipment']:
        if e['type'] == 'pump' and e['id'].startswith('CHP-') and e['x'] == 53000: e['x'] = 53000 + CHP_SHIFT; log.append(f'move {e["id"]}')
    rr = roof_routes(D)
    for p in D['waterPipes']:
        new = unbacktrack(rr.get(p['id'], p['points']))
        if new != p['points']: p['points'] = [[round(c, 4) for c in q] for q in new]; changed.add(p['id']); log.append(f'route {p["id"]}')
    R = {p['id']: [[c / 1000 for c in q] for q in p['pts']] for p in M['pipes']}; R.update({p['id']: [list(x) for x in p['points']] for p in D['waterPipes']})
    svc = {p['id']: p['svc'] for p in M['pipes']}; svc.update({p['id']: p['service'] for p in D['waterPipes']})
    before = {k: [list(x) for x in v] for k, v in R.items()}; merge_overlaps(R, svc)
    for p in M['pipes']:
        if R[p['id']] != before[p['id']]:
            L0 = cum(before[p['id']])[-1]; p['pts'] = [[round(c * 1000, 1) for c in q] for q in R[p['id']]]
            if p.get('span') and abs(p['span'][1] - L0 * 1000) < 2: p['span'] = [p['span'][0], round(cum(R[p['id']])[-1] * 1000, 1)]
            changed.add(p['id']); log.append(f'route {p["id"]} (overlap)')
    for p in D['waterPipes']:
        if R[p['id']] != before[p['id']]: p['points'] = R[p['id']]; changed.add(p['id']); log.append(f'route {p["id"]} (overlap)')
    # legacy AHU CHW valves replaced by the R9 PICV
    for r in D.get('replacedLegacyValves', []):
        for v in M['valves']:
            if v['pipe'] == r['originalPipe'] and v['kind'] == 'MCV' and not v.get('hidden'):
                v['hidden'] = f"replaced by {r['replacement']} (R9)"; log.append(f'hide {v["tag"]}')
    P = pipes_of(M, D); items = items_of(M, D, P)
    # items on re-routed pipes: nearest point of the new route (fixed fittings keep their distance along the pipe)
    for it in items:
        if it['pipe'] in changed:
            pts = P[it['pipe']]['pts']; s0 = project(old[it['pipe']], it['pos'])[0]
            it['pos'] = at(pts, s0)[0] if it['fixed'] else at(pts, project(pts, it['pos'])[0])[0]
    # spacing along each pipe, out of bends and pipe ends
    by = {}
    for it in items: by.setdefault(it['pipe'], []).append(it)
    for pid, L in by.items():
        pts = P[pid]['pts']; ends = end_clear(P, pid); n = len(pts) - 1; c = cum(pts)
        for it in L: it['s'], _, it['seg'] = project(pts, it['pos'])
        free = [it for it in L if not it['fixed']]; fixed = [it for it in L if it['fixed']]
        pack(P, pid, free, fixed, ends)
        for it in L:
            if not it['fixed']: it['pos'] = at(pts, it['s'])[0]
    # stems away from other pipes (first free direction of: up / side / other side / down; vertical pipes: the four sides)
    for it in items:
        if it['stem_len'] <= 0: continue
        cands = candidates(P, it); pick = next((d for d in cands if not stem_hits(P, it, d)), cands[0]); it['stem'] = [round(x, 4) for x in pick]
    # write back
    for it in items:
        pts = P[it['pipe']]['pts']; s, _, seg = project(pts, it['pos']); d = sub(pts[seg + 1], pts[seg])
        if it['src'] == 'V':
            v = it['o']; v['xyz'] = [round(c * 1000, 1) for c in it['pos']]; v['s'] = round(s * 1000, 1)
            v['dir'] = [round(c * 1000, 1) for c in d]
            if 'stem' in it: v['stem'] = it['stem']
        else:
            o = it['o']; o['position'] = [round(c, 4) for c in it['pos']]; o['direction'] = [round(c, 4) for c in d]
            o['radius'] = round(P[it['pipe']]['r'], 4); o['insulation'] = P[it['pipe']]['ins']
            if 'stem' in it: o['stem'] = it['stem']
    return log

def main():
    M, D = load()
    if '--apply' in sys.argv:
        log = apply(M, D)
        json.dump(M, open(MODEL, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        json.dump(D, open(OFFICE, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        print(f'applied: {len([x for x in log if x.startswith("route")])} routes, {len([x for x in log if x.startswith("hide")])} legacy valves hidden; '
              'items spaced and stems set')
    P = pipes_of(M, D); items = items_of(M, D, P)
    f = pipe_clashes(P) + item_checks(P, items)
    for x in f: print('FINDING', x)
    print(f'{len(P)} pipes, {len(items)} valves / instruments checked, {len(f)} findings')
    sys.exit(1 if f else 0)

if __name__ == '__main__':
    main()
