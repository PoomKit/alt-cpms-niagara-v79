# -*- coding: utf-8 -*-
"""V7.9 r5: read-only comparison of a deployed station package (station/ALT_CP_Ref_V7_9.zip on main) with what this repository builds.

The ZIP is opened in memory; nothing is extracted or written, and no security values (users, passwords, keys, certificates) are
printed: only component names and slot paths of the ChillerPlant / AirSide trees are compared.
Reports
  * components of the last full repository build (registers/V7_COMPONENTS.csv) missing from the package, by group
  * points the 3D page subscribes to (station/shared/web/ALT_V79_Building3D.html, window.PTS) whose slot path is not in the package
  * r4 office-layer points and r5 R9 device bindings present / missing (they exist only after the layers are applied to config.bog)
  * file ORDs (file:^...) of config.bog that are missing from the package's shared folder
usage: python3 check_baseline_zip.py <station.zip> [--strict]      --strict: exit 1 when a page point is missing"""
import csv, io, json, os, re, sys, zipfile, xml.etree.ElementTree as ET
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')


def bog_tree(zf):
    bog = next(n for n in zf.namelist() if n.endswith('/config.bog') or n == 'config.bog')
    inner = zipfile.ZipFile(io.BytesIO(zf.read(bog)))
    root = ET.fromstring(inner.read('file.xml'))
    st = root[0]; paths, names = set(), {}
    def walk(e, p):
        for c in e:
            if c.tag == 'p' and c.get('n'):
                q = p + '/' + c.get('n')
                if not q.startswith('/Services'):                      # never look into the security / user services
                    paths.add(q); names.setdefault(c.get('n'), q); walk(c, q)
    walk(st, '')
    return bog, paths, names, inner.read('file.xml').decode('utf-8', 'replace')


def group(n):
    m = re.match(r'(IOS?|Sim|ZoneCO2|Zone|Z\d\d|CH0[3-6]|CHP0[3-6]|CDP0[3-6]|CT0[3-6]|AHU_F\d\d|VAV|RM)', n)
    return m.group(1) if m else 'other'


def main():
    if len(sys.argv) < 2: print(__doc__); sys.exit(2)
    zf = zipfile.ZipFile(sys.argv[1]); bog, paths, names, xml = bog_tree(zf)
    shared = {n.split('/shared/', 1)[1] for n in zf.namelist() if '/shared/' in n}
    print(f'package {os.path.basename(sys.argv[1])}: {bog}, {len(paths)} slots (Services not inspected), {len(shared)} shared files')
    with open(os.path.join(ROOT, 'registers', 'V7_COMPONENTS.csv'), encoding='utf-8-sig') as f:
        comps = [r['Component'] for r in csv.DictReader(f)]
    miss = [c for c in comps if c not in names]
    print(f'\n[1] repository full build (V7_COMPONENTS.csv): {len(comps)} components, missing in package: {len(miss)}')
    for g, n in Counter(group(c) for c in miss).most_common(): print(f'      {g:8s} {n}')
    page = open(os.path.join(ROOT, 'station', 'shared', 'web', 'ALT_V79_Building3D.html'), encoding='utf-8').read()
    m = re.search(r'window\.PTS=(\{.*?\});window\.MAP=', page); pts = json.loads(m.group(1)) if m else {}
    pm = sorted(n for n, s in pts.items() if s not in paths)
    print(f'\n[2] 3D page points (window.PTS): {len(pts)}, slot path not in package: {len(pm)}')
    for g, n in Counter(group(c) for c in pm).most_common(): print(f'      {g:8s} {n}')
    op = json.load(open(os.path.join(ROOT, 'graphics3d', 'data', 'office_points.json'), encoding='utf-8'))['points']
    rb = json.load(open(os.path.join(ROOT, 'graphics3d', 'data', 'r9_bindings.json'), encoding='utf-8'))['bind']
    print(f'\n[3] r4 office-layer points present: {sum(s in paths for s in op.values())} / {len(op)}'
          f'   r5 R9 device bindings present: {sum(b["s"] in paths for b in rb.values())} / {len(rb)}')
    ords = sorted(set(re.findall(r'file:\^([^"|&;<>]+\.(?:px|html|png|gif|jpg|svg|json))', xml)))
    fm = [o for o in ords if o not in shared]
    print(f'\n[4] file ORDs in config.bog: {len(ords)}, missing in package: {len(fm)} {fm[:10]}')
    if '--strict' in sys.argv and pm: sys.exit(1)


if __name__ == '__main__':
    main()
