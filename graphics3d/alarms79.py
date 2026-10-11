# -*- coding: utf-8 -*-
"""Station alarm register -> (3D equipment / zone, visual effect) for the V7.9 building.  Effects / rules as V7.8 (lotus/alarms.py)."""
import csv, re, sys
sys.path.insert(0, '/home/claude/lotus')
from alarms import EFFECTS, RULES
N = 6
EQUIP = [(r'Zone(TemperatureAvg|HumidityAvg|OutOfService)?_(\d\d_\d{4})', lambda m: ['Z-' + m.group(2)]),
         (r'^Zone_(\d\d_\d{4})_', lambda m: ['Z-' + m.group(1)]),
         (r'AHU_F(\d\d)', lambda m: [f'AHU-F{m.group(1)}']), (r'AHU0([12])', lambda m: [f'AHU-0{m.group(1)}']), (r'OAU01', lambda m: ['OAU-01']),
         (r'FCU0(\d)', lambda m: [f'FCU-0{m.group(1)}']), (r'(?<![A-Z])(CPEF|LSF|SEF|EF)0(\d)', lambda m: [f'{m.group(1)}-0{m.group(2)}']),
         (r'(?<![A-Z])CH0(\d)', lambda m: [f'CH-0{m.group(1)}']), (r'(CHP|CDP)0(\d)', lambda m: [f'{m.group(1)}-0{m.group(2)}']),
         (r'CT0(\d)_0(\d)', lambda m: [f'CT-0{m.group(1)}/{m.group(2)}']), (r'CT0(\d)', lambda m: [f'CT-0{m.group(1)}/1', f'CT-0{m.group(1)}/2']),
         (r'^CT_|CDW|^CDS|^CDR|^MU|CdwLoop', lambda m: ['CT-01/1', 'CT-01/2', 'CT-02/1', 'CT-02/2']),
         (r'^Byp|Bypass', lambda m: ['DPB-01']), (r'^CHW_(Chem|Fill)|Expansion', lambda m: ['ET-01']),
         (r'^PlantRoom|^RL_', lambda m: ['ROOM']), (r'AirSide|AirCommon|^Fire|Zone', lambda m: ['BUILDING']), (r'.', lambda m: ['CP-01'])]


def build(alarm_csv, point_csv):
    P = {r['Point']: r['Slot_Path'] for r in csv.DictReader(open(point_csv, encoding='utf-8-sig'))}
    out = []
    for r in csv.DictReader(open(alarm_csv, encoding='utf-8-sig')):
        n, txt = r['Point'], r['Offnormal_Text']
        eq = next(f(m) for rx, f in EQUIP if (m := re.search(rx, n)))
        eff = next(e for rx, e in RULES if re.search(rx, n + ' ' + txt, re.I))
        if (eq[0].startswith(('Z-', 'AHU', 'OAU', 'FCU', 'EF', 'CPEF', 'LSF', 'SEF')) or eq == ['BUILDING']) and eff not in ('fire', 'power', 'trip', 'sensor', 'maint'):
            eff = 'airside' if not eq[0].startswith('Z-') else 'perf'
        out.append({'n': n, 's': r['Slot_Path'] or P.get(n, ''), 'c': r['Alarm_Class'], 't': txt, 'e': eq, 'x': eff})
    return out
