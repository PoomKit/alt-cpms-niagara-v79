# -*- coding: utf-8 -*-
"""Build the V7.9 3D page: model79.py + station registers (V7_POINT_LIST / V7_ALARM_REGISTER of the V7.9 build) -> one self-contained HTML.
Point mapping is generated: every point the page reads, its slot path in the station and what it drives in 3D."""
import json, csv, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model79 as MD, alarms79 as AM
REGD = os.environ.get('V79_REGDIR', '/home/claude/v79/b2/reg')
PL = f'{REGD}/V7_POINT_LIST.csv'
P = {r['Point']: r['Slot_Path'] for r in csv.DictReader(open(PL, encoding='utf-8-sig'))}
USE = {}
def use(pt, what):
    if pt: USE.setdefault(pt, what)
for k in ('OA_Temperature', 'OA_Humidity', 'OA_WetBulb'): use(k, 'weather / sky')
for k in ('CHWS', 'CHWR', 'CDS', 'CDR', 'CHWFlow', 'CDW_Flow', 'Plant_kW_per_RT', 'CoolingLoad_RT', 'Plant_kW'): use(k, 'KPI card / water speed')
for v in MD.VALVES:
    if v['pt']: use(v['pt'], f"{v['kind']} {v['tag'] or v['pipe']} (position / value)")
for p in MD.PIPES:
    if p['fl']: use(p['fl'], f"water flow {p['id']}"); use(p['fl'].replace('_Fwd', '_Rev'), f"reverse flow {p['id']}")
air = []
for e in MD.AIR_EQ:
    e = dict(e, layer='air', run=f"{e['pt']}_Status"); air.append(e); use(e['run'], f"{e['id']} running")
    if e['type'] == 'ahu': use(f"{e['pt']}_ValveCmd", f"{e['id']} CHW valve")
eqs = []
for e in MD.EQ:
    e = dict(e, layer='plant')
    if e['type'] in ('chiller', 'pump', 'ct'):
        e['run'] = e['pt'] + 'RunProof'; use(e['run'], f"{e['id']} running (rotation, label)")
        if e['type'] != 'chiller': use(e['pt'] + 'SpeedCmd', f"{e['id']} speed")
        else: use(e['pt'] + 'LoadPct', f"{e['id']} load"); use(e['pt'] + '_ChwSupplyTemp', f"{e['id']} leaving water")
        use(e['slot'] + '_Installed', f"{e['slot']} installed (ghost when off)")
    eqs.append(e)
zones = []
for z in MD.ZONES:
    c = z['code']; z = dict(z, t=f'ZoneTemperatureAvg_{c}', h=f'ZoneHumidityAvg_{c}', c=f'ZoneCO2_{c}', oos=f'ZoneOutOfService_{c}'); zones.append(z)
    use(z['t'], f"zone {c} colour / label"); use(z['h'], f"zone {c} humidity"); use(z['c'], f"zone {c} CO2"); use(z['oos'], f"zone {c} out of service")
for sy in MD.SYSTEMS:
    for d in sy['devices']: use(d['pt'], f"{sy['name']} {d['tag']}")
PTS = {k: P[k] for k in USE if k in P}
MAP = [{'p': k, 's': P.get(k, ''), 'u': u, 'ok': k in P} for k, u in USE.items()]
missing = [m['p'] for m in MAP if not m['ok'] and not m['p'].endswith('_Rev')]
A = AM.build(f'{REGD}/V7_ALARM_REGISTER.csv', PL)
cond = {r['Point']: r['Condition'] for r in csv.DictReader(open(f'{REGD}/V7_ALARM_REGISTER.csv', encoding='utf-8-sig'))}
for a in A: a['av'] = 'alarmValue=false' not in cond.get(a['n'], '')
valves = []
for v in MD.VALVES:
    xyz, d, p = MD.valve_xyz(v); L = MD.length(p); valves.append({**v, 'xyz': xyz, 'dir': d, 's': v['d'] if v['d'] >= 0 else L + v['d']})
def pfloor(p):
    zs = [q[2] for q in p['pts']]
    if min(zs) > MD.ROOF_Z: return 9
    if p['id'].startswith(('CHS-F', 'CHR-F')): return int(p['id'][5:])
    return None
pipes = [{**p, 'span': MD.flow_span(p), 'floor': pfloor(p)} for p in MD.PIPES]
cts = [e['x'] for e in MD.EQ if e['type'] == 'ct']
mdl = {'building': MD.B, 'roof_z': MD.ROOF_Z, 'room': MD.ROOM, 'core': MD.CORE, 'grid_x': MD.GRID_X, 'grid_y': MD.GRID_Y, 'equipment': eqs, 'air_equipment': air,
       'pipes': pipes, 'valves': valves, 'service': MD.SERVICE, 'project': MD.PROJECT, 'zones': zones, 'systems': MD.SYSTEMS, 'installed': MD.INST,
       'ct_span': [min(cts), max(cts)]}
if __name__ == '__main__':
    subprocess.run(['npx', 'esbuild', 'scene79.js', '--bundle', '--minify', '--format=iife', '--outfile=build/scene79.min.js'], check=True, cwd=os.path.dirname(os.path.abspath(__file__)))
    js = open('build/scene79.min.js', encoding='utf-8').read()
    tpl = open('page79.html', encoding='utf-8').read()
    html = (tpl.replace('/*DATA*/', 'window.MODEL=' + json.dumps(mdl, ensure_ascii=False) + ';window.ALARMS=' + json.dumps(A, ensure_ascii=False) +
                        ';window.PTS=' + json.dumps(PTS) + ';window.MAP=' + json.dumps(MAP, ensure_ascii=False) + ';window.EFFECTS=' + json.dumps(AM.EFFECTS, ensure_ascii=False) + ';')
               .replace('/*APP*/', js.replace('</script', '<\\/script')))
    os.makedirs('out', exist_ok=True)
    open('out/ALT_V79_Building3D.html', 'w', encoding='utf-8').write(html)
    json.dump(MAP, open('out/map79.json', 'w'), ensure_ascii=False, indent=0)
    print('3D page', len(html) // 1024, 'kB; live points', len(PTS), 'of', len(USE), '; alarms', len(A), '; missing', missing[:30])
