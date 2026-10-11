# -*- coding: utf-8 -*-
"""Assemble station/shared/web/ALT_V79_Building3D.html from its sources (no station or lotus helpers needed):
  page79.html (template) + scene79.js / office79.js (bundled with esbuild from package-lock.json)
  data/page_base.json      ALARMS / EFFECTS / PTS / MAP of the V7.9 r2 build (gen3d79.py output)
  data/r9_model.json       MODEL: R9 coordinated geometry (plant in basement B1)
  data/office79.json       OFFICE: R9 office design (rooms, VAV, ducts, sensors, meters)
  data/office_points.json  r4 station points + alarms (tools/office_points.py) -> merged into PTS / MAP / ALARMS
  models/*.glb             Blender equipment models (tools/blender/equipment79.py) -> GLB (base64)
usage: python3 rebuild_page.py [--check]      --check: exit 1 if the committed page is not what the sources give (CI)"""
import base64, glob, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, '..', 'station', 'shared', 'web', 'ALT_V79_Building3D.html')
D = lambda n: json.load(open(os.path.join(HERE, 'data', n), encoding='utf-8'))
J = lambda v: json.dumps(v, ensure_ascii=False, separators=(',', ':'))


def data_block():
    base, op = D('page_base.json'), D('office_points.json')
    pts = dict(base['PTS']); have = {r['p'] for r in base['MAP']}; mp = list(base['MAP'])
    for n, s in sorted(op['points'].items()):
        pts.setdefault(n, s)
        if n not in have: mp.append({'p': n, 's': s, 'u': 'office / r4 point', 'ok': True})
    names = {a['n'] for a in base['ALARMS']}
    alarms = base['ALARMS'] + [a for a in op['alarms'] if a['n'] not in names]
    glbs = {os.path.basename(f)[:-4]: base64.b64encode(open(f, 'rb').read()).decode() for f in sorted(glob.glob(os.path.join(HERE, 'models', '*.glb')))}
    return (f"window.MODEL={J(D('r9_model.json'))};window.ALARMS={J(alarms)};window.PTS={J(pts)};window.MAP={J(mp)};"
            f"window.EFFECTS={J(base['EFFECTS'])};window.OFFICE={J(D('office79.json'))};window.GLB={J(glbs)};")


def build():
    subprocess.run(['npx', 'esbuild', 'scene79.js', '--bundle', '--minify', '--format=iife', '--outfile=build/scene79.min.js'],
                   check=True, cwd=HERE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    js = open(os.path.join(HERE, 'build', 'scene79.min.js'), encoding='utf-8').read()
    tpl = open(os.path.join(HERE, 'page79.html'), encoding='utf-8').read()
    return tpl.replace('/*DATA*/', data_block().replace('</script', '<\\/script')).replace('/*APP*/', js.replace('</script', '<\\/script'))


if __name__ == '__main__':
    new = build()
    if '--check' in sys.argv:
        cur = open(PAGE, encoding='utf-8').read()
        if new != cur:
            print('ALT_V79_Building3D.html is not built from the current sources: run graphics3d/rebuild_page.py'); sys.exit(1)
        print('3D page matches its sources'); sys.exit(0)
    open(PAGE, 'w', encoding='utf-8').write(new)
    print('rebuilt', PAGE, len(new) // 1024, 'kB')
