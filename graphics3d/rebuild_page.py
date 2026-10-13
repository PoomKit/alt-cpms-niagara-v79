# -*- coding: utf-8 -*-
"""Assemble station/shared/web/ALT_V79_Building3D.html from its sources (no station or lotus helpers needed):
  page79.html (template) + scene79.js / office79.js (bundled with esbuild from package-lock.json)
  data/page_base.json      ALARMS / EFFECTS / PTS / MAP of the V7.9 r2 build (gen3d79.py output)
  data/r9_model.json       MODEL: R9 coordinated geometry (plant in basement B1)
  data/office79.json       OFFICE: R9 office design (rooms, VAV, ducts, sensors, meters)
  data/office_points.json  r4 station points + alarms (tools/office_points.py) -> merged into PTS / MAP / ALARMS
  data/r9_bindings.json    r5 station point of each R9 device (tools/r9_bindings.py) -> window.R9BIND, merged into PTS / MAP
  models/*.glb             Blender equipment models (tools/blender/equipment79.py) -> alt79/models/*.glb (fetched, not base64)
r8 output: small HTML + content-hashed alt79/*.js|bin|glb (old hashed files of this page are removed on rebuild)
usage: python3 rebuild_page.py [--check]      --check: exit 1 if the committed page is not what the sources give (CI)"""
import array, glob, hashlib, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(HERE, '..', 'station', 'shared', 'web')
D = lambda n: json.load(open(os.path.join(HERE, 'data', n), encoding='utf-8'))
J = lambda v: json.dumps(v, ensure_ascii=False, separators=(',', ':'))


def r6(o):
    """drop float noise only (-2.0749999999999997 -> -2.075); values keep 6 decimals"""
    if isinstance(o, float): v = round(o, 6); return int(v) if v == int(v) and abs(v) < 1e15 else v
    if isinstance(o, list): return [r6(x) for x in o]
    if isinstance(o, dict): return {k: r6(v) for k, v in o.items()}
    return o


def h8(b): return hashlib.sha256(b if isinstance(b, bytes) else b.encode('utf-8')).hexdigest()[:8]


def files():
    """-> {relative path under station/shared/web: bytes}.  r8 lean layout: small HTML + content-hashed files in alt79/
       (app bundle, core data, office data, duct shells as Float32, GLB models, point mapping table loaded on demand)"""
    base, op = D('page_base.json'), D('office_points.json')
    pts = dict(base['PTS']); have = {r['p'] for r in base['MAP']}; mp = list(base['MAP'])
    for n, s in sorted(op['points'].items()):
        pts.setdefault(n, s)
        if n not in have: mp.append({'p': n, 's': s, 'u': 'office / r4 point', 'ok': True})
    for n, b in sorted(D('r9_bindings.json')['bind'].items()):
        pts.setdefault(b['p'], b['s'])
        if b['p'] not in have and b['p'] not in op['points']: have.add(b['p']); mp.append({'p': b['p'], 's': b['s'], 'u': 'R9 device ' + n, 'ok': True})
    names = {a['n'] for a in base['ALARMS']}
    alarms = base['ALARMS'] + [a for a in op['alarms'] if a['n'] not in names]
    out = {}
    def put(name, ext, data):
        b = data if isinstance(data, bytes) else data.encode('utf-8'); p = f'alt79/{name}.{h8(b)}.{ext}'; out[p] = b; return p[len('alt79/'):]
    glb_url = {os.path.basename(g)[:-4]: put('models/' + os.path.basename(g)[:-4], 'glb', open(g, 'rb').read()) for g in sorted(glob.glob(os.path.join(HERE, 'models', '*.glb')))}
    office = r6(D('office79.json')); shells = office.pop('ductShells', [])
    if office.get('ductBodies'):     # the page draws ductBodies; plan.ducts is only read for supply-air airflow paths (r9office.js r7 block)
        office['ducts'] = [d for d in office['ducts'] if d['floor'] < 9 and d['service'] == 'SA' and not d['id'].startswith('BR-')]
    vals, idx, items = array.array('f'), array.array('H'), []          # lossless: unique vertices + uint16 triangle index per shell
    for sh in shells:
        q = array.array('f', sh['positions']); uniq = {}; loc = []
        for i in range(0, len(q), 3):
            v = (q[i], q[i + 1], q[i + 2]); loc.append(uniq.setdefault(v, len(uniq)))
        assert len(uniq) < 65536
        for v in uniq: vals.extend(v)
        idx.extend(loc); items.append([sh['floor'], sh['service'], len(uniq), len(loc)])
    office['ductShellsBin'] = {'src': put('office-shells', 'bin', vals.tobytes() + idx.tobytes()), 'nv': len(vals) // 3, 'items': items}
    # compact slot paths: '/A/B/<key>' -> 'A/B' (the page restores '/' + folder + '/' + key)
    cpts = {k: (v[1:-len(k) - 1] if v.startswith('/') and v.endswith('/' + k) else v) for k, v in pts.items()}
    def ca(a):
        a = dict(a); s = a.get('s') or ''
        if s.startswith('/') and s.endswith('/' + a['n']): a['f'] = s[1:-len(a['n']) - 1]; del a['s']
        return a
    map_src = put('alt79-map', 'js', f'window.MAP={J(mp)};')
    data = (f"window.MODEL={J(D('r9_model.json'))};window.ALARMS={J([ca(a) for a in alarms])};window.PTS={J(cpts)};window.MAP_SRC={J(map_src)};"
            f"window.EFFECTS={J(base['EFFECTS'])};window.R9BIND={J(D('r9_bindings.json')['bind'])};window.GLB_URL={J(glb_url)};")
    data_src = put('alt79-data', 'js', data)
    office_src = put('alt79-office', 'js', f'window.OFFICE_DESIGN=window.OFFICE={J(office)};')
    subprocess.run(['npx', 'esbuild', 'scene79.js', '--bundle', '--minify', '--legal-comments=none', '--format=iife', '--outfile=build/scene79.min.js'],
                   check=True, cwd=HERE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    app_src = put('alt79-app', 'js', open(os.path.join(HERE, 'build', 'scene79.min.js'), 'rb').read())
    tpl = open(os.path.join(HERE, 'page79.html'), encoding='utf-8').read()
    out['ALT_V79_Building3D.html'] = (tpl.replace('<script>/*DATA*/</script>', f'<script src="alt79/{data_src}"></script><script src="alt79/{office_src}"></script>')
                                      .replace('<script>/*APP*/</script>', f'<script src="alt79/{app_src}"></script>')).encode('utf-8')
    return out


if __name__ == '__main__':
    new = files()
    if '--check' in sys.argv:
        bad = [p for p, b in new.items() if not os.path.exists(os.path.join(WEB, p)) or open(os.path.join(WEB, p), 'rb').read() != b]
        if bad: print('3D page files are not built from the current sources:', bad[:5], '-> run graphics3d/rebuild_page.py'); sys.exit(1)
        print('3D page matches its sources'); sys.exit(0)
    old = [os.path.join(WEB, 'alt79', f) for f in os.listdir(os.path.join(WEB, 'alt79'))] if os.path.isdir(os.path.join(WEB, 'alt79')) else []
    for p, b in new.items():
        os.makedirs(os.path.dirname(os.path.join(WEB, p)) or WEB, exist_ok=True); open(os.path.join(WEB, p), 'wb').write(b)
    keep = {os.path.normpath(os.path.join(WEB, p)) for p in new}
    for root, _, fs in os.walk(os.path.join(WEB, 'alt79')):          # previous content-hashed builds of this page only
        for f in fs:
            q = os.path.normpath(os.path.join(root, f))
            if q not in keep: os.remove(q)
    for p, b in sorted(new.items()): print(f'{len(b):>10}  {p}')
