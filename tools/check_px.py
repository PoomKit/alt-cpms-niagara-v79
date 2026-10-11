# -*- coding: utf-8 -*-
"""Static checks of the station graphics (no station needed):
  * every Px file is well-formed XML
  * every file:^px/... / file:^web/... the Px pages reference exists
  * every station:|slot:/... ORD exists in registers/V7_POINT_LIST.csv or registers/V7_COMPONENTS.csv
    (an action / property after the component name - .../set, .../fire, Runtime/resetElapsedActiveTime - is allowed)
  * the 3D point map (graphics3d/map79.json) has no unresolved point except the optional *_Rev flows
usage: python3 check_px.py        exit code 1 on any finding."""
import csv, glob, json, os, re, sys
import xml.etree.ElementTree as ET
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
PX = os.path.join(ROOT, 'station', 'shared', 'px')
WEB = os.path.join(ROOT, 'station', 'shared', 'web')
REG = os.path.join(ROOT, 'registers')


def main():
    bad = []
    paths = {r['Slot_Path'].rstrip('/') for r in csv.DictReader(open(os.path.join(REG, 'V7_POINT_LIST.csv'), encoding='utf-8-sig'))}
    comps = list(csv.DictReader(open(os.path.join(REG, 'V7_COMPONENTS.csv'), encoding='utf-8-sig')))
    # same rule as make_v7._path_of: AirSide folders sit at the station root, everything else under /ChillerPlant
    paths |= {(('/' if r['Folder'].startswith('AirSide') else '/ChillerPlant/') + f"{r['Folder']}/{r['Component']}").replace('//', '/') for r in comps}
    names = {r['Component'] for r in comps}
    prefixes = {p.rsplit('/', i)[0] for p in paths for i in range(1, p.count('/'))}
    files = sorted(glob.glob(os.path.join(PX, '*.px')))
    for f in files:
        n = os.path.basename(f); s = open(f, encoding='utf-8').read()
        try: ET.fromstring(s)
        except ET.ParseError as e: bad.append(f'{n}: XML {e}'); continue
        for m in set(re.findall(r'file:\^px/([^"\'|\s;)]+)', s)):
            if not os.path.exists(os.path.join(PX, m)): bad.append(f'{n}: missing file:^px/{m}')
        for m in set(re.findall(r'file:\^web/([^"\'|\s;)]+)', s)):
            if not os.path.exists(os.path.join(WEB, m)): bad.append(f'{n}: missing file:^web/{m}')
        for o in set(re.findall(r'station:\|slot:(/[^"|\s]+)', s)):
            o = o.rstrip('/'); parts = o.split('/')
            ok = o in paths or o in prefixes or any('/'.join(parts[:k]) in paths for k in range(len(parts) - 1, 2, -1)) \
                or any(p in names for p in parts[-3:-1])
            if not ok: bad.append(f'{n}: ORD not in the point list {o}')
    mp = json.load(open(os.path.join(ROOT, 'graphics3d', 'map79.json'), encoding='utf-8'))
    miss = [r['p'] for r in mp if not r['ok'] and not r['p'].endswith('_Rev')]
    bad += [f'map79.json: 3D point not in the station {p}' for p in miss]
    for b in bad: print('FINDING', b)
    print(f'{len(files)} Px files, {len(mp)} 3D points: {len(bad)} findings')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
