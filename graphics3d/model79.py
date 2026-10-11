# -*- coding: utf-8 -*-
"""V7.9 reference building - single source of truth for 3D (gen3d79.py), 2D drawings (gen2d79.py) and IFC / BOQ (genbim79.py).
8-storey building 64 x 40 m.  Chiller plant on the ground floor (room 44 x 15 m), cooling towers on the roof, CHW risers to a
floor AHU on every floor.  The plant is drawn for the MAXIMUM equipment (6 chillers, 6 CHW pumps, 6 CDW pumps, 6 towers x 2
cells); a slot that is not installed (register / <slot>_Installed) is drawn as a ghost.  Units: mm, x east, y north, z up,
origin = ground floor level at the south-west corner.  Point names = station ALT_CP_Ref_V7_9."""
import math, os, sys
sys.path.insert(0, '/home/claude/v7/tools')
import eqreg

REGISTER = os.environ.get('V79_REGISTER', '/home/claude/b79/ALT_V79_Equipment_Register.xlsx')
REG = eqreg.load(REGISTER)
INST = {r['Slot']: eqreg.installed(r) for r in REG['Equipment']}
PROJECT = {'name': 'CPMS Reference Building V7.9', 'name_th': 'อาคารอ้างอิง 8 ชั้น - ห้องเครื่องทำน้ำเย็นชั้น 1, cooling tower บนดาดฟ้า',
           'station': 'ALT_CP_Ref_V7_9', 'company': 'AETERLINK (Thailand) Co., Ltd.',
           'note': 'Reference design for the logic and graphics (not a construction drawing): sizes and positions to be confirmed per site.'}
B = {'x': 64000, 'y': 40000, 'floors': 8, 'f1_h': 5500, 'typ_h': 4200, 'slab': 250, 'parapet': 1200}
ROOF_Z = B['f1_h'] + (B['floors'] - 1) * B['typ_h']                     # 34 900
def zf(f): return 0 if f == 1 else B['f1_h'] + (f - 2) * B['typ_h']
ROOM = {'x0': 0, 'y0': 0, 'x': 44000, 'y': 15000, 'h': B['f1_h'], 'wall': 200}
CORE = {'x0': 40000, 'y0': 15000, 'x1': 48000, 'y1': 27000}
SHAFT = {'x0': 31800, 'y0': 13300, 'x1': 37600, 'y1': 14700}
GRID_X = [(str(i + 1), i * 8000) for i in range(9)]
GRID_Y = [(c, i * 8000) for i, c in enumerate('ABCDEF')]
N = eqreg.MAX_UNITS

# ------------------------------------------------------------------ equipment
CHW_Z, CDW_Z, PS_Z, PD_Z = 1180, 720, 620, 1110
CH_Y, CH_X = 11000, [4000 + i * 5000 for i in range(N)]
PUMP_Y = [1600 + i * 2000 for i in range(N)]
CHP_X, CDP_X = 34000, 40000
CT_Y = 6000; CT_X = [4000 + k * 2800 for k in range(2 * N)]; CT_Z = ROOF_Z + 1000
CHILLER_DATA = {'Model': 'Water-cooled screw / centrifugal (reference)', 'Capacity': '334 TR', 'Efficiency': '0.614 kW/TR', 'CHW': '6.7 -> 12.2 C', 'Power': '380 V / 3 Ph / 50 Hz'}
EQ = []
for i in range(N):
    s = f'CH{i + 1:02d}'
    EQ.append(dict(id=f'CH-{i + 1:02d}', type='chiller', x=CH_X[i], y=CH_Y, z=100, rot=90, L=3774, W=1771, H=2033, pt=s, slot=s,
                   installed=INST[s], data={**CHILLER_DATA, 'Slot': s, 'Logic': 'V7.8 base unit' if i < 2 else 'V7.9 expansion slot'}))
for kind, X0, desc, flow, kw in (('CHP', CHP_X, 'Chilled water pump (primary-variable, headered)', '800 USgpm', '22 kW'),
                                 ('CDP', CDP_X, 'Condenser water pump (headered)', '1,000 USgpm', '30 kW')):
    for i in range(N):
        s = f'{kind}{i + 1:02d}'
        EQ.append(dict(id=f'{kind}-{i + 1:02d}', type='pump', x=X0, y=PUMP_Y[i], z=0, rot=0, L=1750, W=650, H=850, pt=s, slot=s, installed=INST[s],
                       data={'Service': desc, 'Type': 'End suction, VSD', 'Flow': flow, 'Head': '80 ft', 'Motor': kw + ', 380/3/50', 'Slot': s}))
for t in range(N):
    s = f'CT{t + 1:02d}'
    for c in (1, 2):
        k = 2 * t + c - 1
        EQ.append(dict(id=f'CT-{t + 1:02d}/{c}', type='ct', x=CT_X[k], y=CT_Y, z=CT_Z, rot=0, L=2600, W=2600, H=2700, slot=s, tower=s,
                       pt=f'{s}_{c:02d}' if t < 2 else s, installed=INST[s], cell=c,
                       data={'Type': 'Crossflow, induced draft (FRP)', 'Cell': f'{c} of 2', 'Capacity': '420 TR per tower', 'Fan': '5.5 kW VSD', 'Slot': s}))
EQ += [dict(id='ET-01', type='exptank', x=31000, y=12900, z=0, rot=0, L=900, W=900, H=1600, pt=None, data={'Service': 'Expansion tank', 'Volume': '1,000 L'}),
       dict(id='DPB-01', type='bypass', x=30000, y=8600, z=0, rot=0, L=2400, W=500, H=800, pt='Byp', data={'Service': 'CHW minimum-flow bypass'}),
       dict(id='CP-01', type='panel', x=2500, y=14600, z=0, rot=0, L=2400, W=500, H=2100, pt='Plant',
            data={'Service': 'CPMS control panel (Niagara JACE / Supervisor)', 'Station': PROJECT['station']})]
# air side (floor 1 = V7.8 units, floors 2-8 = floor AHUs, roof fans)
AHU_DATA = {'Type': 'Air handling unit, CHW coil, VSD fan', 'Airflow': '12,000 CFM'}
AIR_EQ = [dict(id='AHU-01', type='ahu', x=50000, y=12500, z=0, rot=0, L=3600, W=1800, H=2100, pt='AHU01', floor=1, data={**AHU_DATA, 'Serves': 'Lobby / reception / open office'}),
          dict(id='AHU-02', type='ahu', x=58000, y=12500, z=0, rot=0, L=3600, W=1800, H=2100, pt='AHU02', floor=1, data={**AHU_DATA, 'Serves': 'Meeting / training / executive'}),
          dict(id='OAU-01', type='ahu', x=50000, y=33000, z=ROOF_Z, rot=0, L=4200, W=2000, H=2200, pt='OAU01', floor=9, data={'Type': 'Outdoor air unit (dew point control)'})]
for k, (x, y) in enumerate([(4000, 36500), (15000, 36500), (26000, 36500), (37000, 36500)], 1):
    AIR_EQ.append(dict(id=f'FCU-{k:02d}', type='fcu', x=x, y=y, z=B['f1_h'] - 900, rot=0, L=1400, W=700, H=300, pt=f'FCU{k:02d}', floor=1,
                       data={'Type': 'Fan coil unit, 3-speed fan, on/off valve'}))
for f in range(2, B['floors'] + 1):
    AIR_EQ.append(dict(id=f'AHU-F{f:02d}', type='ahu', x=35000, y=17500, z=zf(f), rot=0, L=3600, W=1800, H=2100, pt=f'AHU_F{f:02d}', floor=f,
                       data={**AHU_DATA, 'Serves': f'Floor {f} (4 zones)'}))
for k, (n, x, y, pt) in enumerate([('EF-01', 20000, 30000, 'EF01'), ('EF-02', 26000, 30000, 'EF02'), ('EF-03', 42000, 4000, 'EF03'),
                                   ('CPEF-01', 58000, 30000, 'CPEF01'), ('LSF-01', 44000, 24000, 'LSF01'), ('SEF-01', 46000, 18000, 'SEF01')]):
    z = 3800 if n == 'EF-03' else ROOF_Z
    AIR_EQ.append(dict(id=n, type='fan', x=x, y=y, z=z, rot=0, L=1200, W=1200, H=1100, pt=pt, floor=9 if z > 30000 else 1, data={'Type': 'Fan'}))

ZONE_F1 = [('01_0101', 'Lobby'), ('01_0102', 'Reception'), ('01_0103', 'Open office A'), ('01_0104', 'Open office B'), ('01_0105', 'Meeting 1'),
           ('01_0106', 'Meeting 2'), ('01_0107', 'Training'), ('01_0108', 'Executive'), ('01_0109', 'Server room'), ('01_0110', 'Pantry'),
           ('01_0111', 'Storage'), ('01_0112', 'Corridor')]
ZONES = []
for i, (c, n) in enumerate(ZONE_F1):
    if i < 8: x0, y0 = (i % 4) * 10000, 15000 + (i // 4) * 12500; x1, y1 = x0 + 10000, y0 + 12500
    else: j = i - 8; x0, x1, y0, y1 = 48000, 64000, j * 10000, (j + 1) * 10000
    ZONES.append(dict(code=c, name=n, floor=1, x0=x0, y0=y0, x1=x1, y1=y1))
for f in range(2, B['floors'] + 1):
    for z, (n, x0, y0, x1, y1) in enumerate([('Office north', 0, 22000, 40000, 40000), ('Office south', 0, 0, 40000, 18000),
                                              ('Meeting', 48000, 0, 64000, 40000), ('Core / corridor', 40000, 0, 48000, 15000)], 1):
        ZONES.append(dict(code=f'{f:02d}_{f:02d}{z:02d}', name=n, floor=f, x0=x0, y0=y0, x1=x1, y1=y1))

# future systems (register sheet 'Systems'): layer frame, devices are added there and appear in 3D as markers with live status
SYSTEMS = [dict(id='fire_alarm', name='Fire alarm', name_th='ระบบแจ้งเหตุเพลิงไหม้', color='#d93025', status='planned', devices=[]),
           dict(id='fire_protection', name='Fire protection', name_th='ระบบดับเพลิง', color='#b3261e', status='planned', devices=[]),
           dict(id='lighting', name='Lighting', name_th='ระบบไฟฟ้าแสงสว่าง', color='#f0b323', status='planned', devices=[]),
           dict(id='power', name='Power metering', name_th='ระบบไฟฟ้ากำลัง / มิเตอร์', color='#5f6b78', status='planned', devices=[])]
for r in REG.get('Systems', []):
    sy = next((x for x in SYSTEMS if x['id'] == r.get('System')), None)
    if sy is None: sy = dict(id=r.get('System'), name=r.get('System'), name_th=r.get('System'), color='#7a8399', status='planned', devices=[]); SYSTEMS.append(sy)
    sy['devices'].append(dict(tag=r.get('Tag'), type=r.get('Type'), floor=int(r.get('Floor') or 1), x=float(r.get('X') or 0), y=float(r.get('Y') or 0),
                              z=float(r.get('Z') or 0), pt=r.get('Point'), note=r.get('Note') or ''))
    sy['status'] = 'in use'

EQ_BY_ID = {e['id']: e for e in EQ + AIR_EQ}
SERVICE = {'CHS': ('Chilled water supply', '#1f6fe0', True), 'CHR': ('Chilled water return', '#5fb2ff', True),
           'CDS': ('Condenser water supply', '#f2b632', False), 'CDR': ('Condenser water return', '#ef7d2d', False),
           'D': ('Drain', '#8a8f96', False), 'MU': ('Make-up water', '#3fbf7f', False)}
STUB = 300


def CH_NOZ(x):
    y = CH_Y - 3774 / 2 - 300
    return {'chw_in': (x + 430, y, CHW_Z), 'chw_out': (x - 70, y, CHW_Z), 'cdw_in': (x - 420, y, CDW_Z), 'cdw_out': (x - 20, y, CDW_Z)}


def _p(id, svc, dn, pts, cap=None, fl=None, eq=(), hdr=False, note='', slot=None):
    return dict(id=id, svc=svc, dn=dn, pts=[tuple(map(float, q)) for q in pts], cap=cap, fl=fl, eq=list(eq), hdr=hdr, note=note, slot=slot)


# header lines (plant room)
Y_CHR_EH, Y_CHS_H, Y_CDS_CH, Y_CDR_H = 8400, 7900, 7100, 6700
Z_CHR_EH, Z_CHS_H, Z_CDS_CH, Z_CDR_H = 2600, 3300, 1800, 4200
X_CHR_SH, X_CHR_DH, X_CDS_SH, X_CDS_DH = 32300, CHP_X - 525, 38700, CDP_X - 525
X_CHS_R, Y_CHS_R, X_CHR_R, Y_CHR_R = 37000, 14200, 32300, 13600
X_CDS_R, Y_CDS_R, X_CDR_R = 42500, 14200, 43600
Z_TOP = zf(B['floors']) + 3600
NOZ = [CH_NOZ(x) for x in CH_X]
x_first = NOZ[0]
PIPES = [
    # chilled water: building return riser -> CHP suction header -> pumps -> discharge header -> evaporator header -> chillers -> supply header -> riser
    _p('CHR-R', 'CHR', 16, [(X_CHR_R, Y_CHR_R, Z_TOP), (X_CHR_R, Y_CHR_R, PS_Z)], cap='start', fl='Gfx_ChwMain_Fwd', note='CHW return riser (shaft)'),
    _p('CHR-SH', 'CHR', 16, [(X_CHR_R, Y_CHR_R, PS_Z), (X_CHR_SH, PUMP_Y[0] - 900, PS_Z)], cap='end', fl='Gfx_ChwMain_Fwd', hdr=True, note='CHP suction header'),
    _p('CHR-DH', 'CHR', 16, [(X_CHR_DH, PUMP_Y[0] - 900, Z_CHR_EH), (X_CHR_DH, PUMP_Y[-1] + 300, Z_CHR_EH)], cap='both', fl='Gfx_EvapTotal_Fwd', hdr=True, note='CHP discharge header'),
    _p('CHR-EH', 'CHR', 16, [(X_CHR_DH, Y_CHR_EH, Z_CHR_EH), (x_first['chw_in'][0] - STUB, Y_CHR_EH, Z_CHR_EH)], cap='end', fl='Gfx_EvapTotal_Fwd', hdr=True, note='CHW header to evaporators'),
    _p('CHS-H', 'CHS', 16, [(x_first['chw_out'][0] - STUB, Y_CHS_H, Z_CHS_H), (X_CHS_R, Y_CHS_H, Z_CHS_H), (X_CHS_R, Y_CHS_R, Z_CHS_H)], cap='start', fl='Gfx_ChwMain_Fwd', hdr=True, note='CHW supply header'),
    _p('CHS-R', 'CHS', 16, [(X_CHS_R, Y_CHS_R, Z_CHS_H), (X_CHS_R, Y_CHS_R, Z_TOP)], cap='end', fl='Gfx_ChwMain_Fwd', note='CHW supply riser (shaft)'),
    _p('CHW-BP', 'CHS', 6, [(31000, Y_CHS_H, Z_CHS_H), (31000, Y_CHS_H, 1000), (31000, 8600, 1000), (X_CHR_SH, 8600, 1000), (X_CHR_SH, 8600, PS_Z)],
       fl='Gfx_Bypass_Fwd', eq=['DPB-01'], note='minimum-flow bypass'),
    _p('CHW-ET', 'CHR', 2, [(31450, 12900, 400), (31700, 12900, 400), (31700, 12900, PS_Z), (X_CHR_SH, 12900, PS_Z)], eq=['ET-01'], note='expansion tank'),
    # condenser water: roof collecting header -> riser -> CDP suction header -> pumps -> discharge header -> condenser header -> chillers -> return header -> riser -> roof
    _p('CDS-RH', 'CDS', 18, [(CT_X[0] - 700 - STUB, 3600, ROOF_Z + 450), (X_CDS_R, 3600, ROOF_Z + 450), (X_CDS_R, Y_CDS_R, ROOF_Z + 450)], cap='start', fl='Gfx_CdwTotal_Fwd', hdr=True, note='roof collecting header'),
    _p('CDS-R', 'CDS', 18, [(X_CDS_R, Y_CDS_R, ROOF_Z + 450), (X_CDS_R, Y_CDS_R, PS_Z)], fl='Gfx_CdwTotal_Fwd', note='CDW riser from the towers'),
    _p('CDS-SH', 'CDS', 18, [(X_CDS_R, Y_CDS_R, PS_Z), (X_CDS_SH, Y_CDS_R, PS_Z), (X_CDS_SH, PUMP_Y[0] - 900, PS_Z)], cap='end', fl='Gfx_CdwTotal_Fwd', hdr=True, note='CDP suction header'),
    _p('CDS-DH', 'CDS', 18, [(X_CDS_DH, PUMP_Y[0] - 900, Z_CDS_CH), (X_CDS_DH, PUMP_Y[-1] + 300, Z_CDS_CH)], cap='both', fl='Gfx_CdwTotal_Fwd', hdr=True, note='CDP discharge header'),
    _p('CDS-CH', 'CDS', 18, [(X_CDS_DH, Y_CDS_CH, Z_CDS_CH), (x_first['cdw_in'][0] - STUB, Y_CDS_CH, Z_CDS_CH)], cap='end', fl='Gfx_CdwTotal_Fwd', hdr=True, note='CDW header to condensers'),
    _p('CDR-H', 'CDR', 18, [(x_first['cdw_out'][0] - STUB, Y_CDR_H, Z_CDR_H), (X_CDR_R, Y_CDR_H, Z_CDR_H)], cap='start', fl='Gfx_CdwTotal_Fwd', hdr=True, note='CDW return header'),
    _p('CDR-R', 'CDR', 18, [(X_CDR_R, Y_CDR_H, Z_CDR_H), (X_CDR_R, Y_CDR_H, ROOF_Z + 1150), (X_CDR_R, 8200, ROOF_Z + 1150)], fl='Gfx_CdwTotal_Fwd', note='CDW return riser to the roof'),
    _p('CDR-RH', 'CDR', 18, [(X_CDR_R, 8200, ROOF_Z + 1150), (CT_X[0] - STUB, 8200, ROOF_Z + 1150)], cap='end', fl='Gfx_CdwTotal_Fwd', hdr=True, note='roof distribution header'),
]
for i in range(N):
    s, c, n = f'CH{i + 1:02d}', f'CH-{i + 1:02d}', NOZ[i]
    PIPES += [
        _p(f'CHR-E{i + 1}', 'CHR', 8, [(n['chw_in'][0], Y_CHR_EH, Z_CHR_EH), (n['chw_in'][0], Y_CHR_EH, CHW_Z), n['chw_in']], fl=f'Gfx_{s}Evap_Fwd', eq=[c], slot=s),
        _p(f'CHS-E{i + 1}', 'CHS', 8, [n['chw_out'], (n['chw_out'][0], Y_CHS_H, CHW_Z), (n['chw_out'][0], Y_CHS_H, Z_CHS_H)], fl=f'Gfx_{s}Evap_Fwd', eq=[c], slot=s),
        _p(f'CDS-C{i + 1}', 'CDS', 8, [(n['cdw_in'][0], Y_CDS_CH, Z_CDS_CH), (n['cdw_in'][0], Y_CDS_CH, CDW_Z), n['cdw_in']], fl=f'Gfx_{s}Cond_Fwd', eq=[c], slot=s),
        _p(f'CDR-C{i + 1}', 'CDR', 8, [n['cdw_out'], (n['cdw_out'][0], Y_CDR_H, CDW_Z), (n['cdw_out'][0], Y_CDR_H, Z_CDR_H)], fl=f'Gfx_{s}Cond_Fwd', eq=[c], slot=s)]
for kind, X0, XS, XD, svc in (('CHP', CHP_X, X_CHR_SH, X_CHR_DH, 'CHR'), ('CDP', CDP_X, X_CDS_SH, X_CDS_DH, 'CDS')):
    zh = Z_CHR_EH if kind == 'CHP' else Z_CDS_CH
    for i in range(N):
        s, y = f'{kind}{i + 1:02d}', PUMP_Y[i]
        PIPES += [_p(f'{svc}-P{i + 1}', svc, 8, [(XS, y, PS_Z), (X0 - 920, y, PS_Z)], fl=f'Gfx_{s}_Fwd', eq=[f'{kind}-{i + 1:02d}'], slot=s),
                  _p(f'{svc}-D{i + 1}', svc, 8, [(XD, y, PD_Z), (XD, y, zh)], fl=f'Gfx_{s}_Fwd', eq=[f'{kind}-{i + 1:02d}'], slot=s)]
H_CT = 2700
for k, x in enumerate(CT_X):
    t, c = k // 2, k % 2 + 1; s = f'CT{t + 1:02d}'; ct = f'CT-{t + 1:02d}/{c}'
    PIPES += [_p(f'CDR-T{k + 1}', 'CDR', 8, [(x, 8200, ROOF_Z + 1150), (x, 8200, CT_Z + H_CT + 140), (x, CT_Y + 300, CT_Z + H_CT + 140)], fl=f'Gfx_{s}_Fwd', eq=[ct], slot=s, note='cell inlet'),
              _p(f'CDS-T{k + 1}', 'CDS', 8, [(x - 700, CT_Y - 1300, CT_Z + 200), (x - 700, 3600, CT_Z + 200), (x - 700, 3600, ROOF_Z + 450)], fl=f'Gfx_{s}_Fwd', eq=[ct], slot=s, note='cell outlet')]
# CHW to the floor AHUs (risers in the shaft)
for f in range(2, B['floors'] + 1):
    z = zf(f); s = f'AHU_F{f:02d}'
    PIPES += [_p(f'CHS-F{f}', 'CHS', 4, [(X_CHS_R, Y_CHS_R, z + 3300), (X_CHS_R, 17500, z + 3300), (36400, 17500, z + 3300), (36400, 17500, z + 1500)], fl=f'Gfx_{s}_Fwd', eq=[f'AHU-F{f:02d}'], note=f'floor {f} AHU supply'),
              _p(f'CHR-F{f}', 'CHR', 4, [(33600, 17500, z + 900), (33600, 17500, z + 3600), (X_CHR_R, 17500, z + 3600), (X_CHR_R, Y_CHR_R, z + 3600)], fl=f'Gfx_{s}_Fwd', eq=[f'AHU-F{f:02d}'], note=f'floor {f} AHU return')]
PIPE_BY_ID = {p['id']: p for p in PIPES}

# valves / fittings / instruments
VALVES = []
def _v(pipe, d, kind, dn=None, tag='', pt=''):
    VALVES.append({'pipe': pipe, 'd': d, 'kind': kind, 'dn': dn, 'tag': tag, 'pt': pt})
for kind, svc in (('CHP', 'CHR'), ('CDP', 'CDS')):
    for i in range(N):
        s = f'{kind}{i + 1:02d}'; base = i < 2
        _v(f'{svc}-P{i + 1}', 150, 'MBFV' if base else 'BFV', tag=f'{s} suction', pt=f'Gfx_{s}_SuctionMV_Pos' if base else '')
        _v(f'{svc}-P{i + 1}', 420, 'STRAINER'); _v(f'{svc}-P{i + 1}', -160, 'FLEX', dn=6)
        _v(f'{svc}-D{i + 1}', 140, 'FLEX'); _v(f'{svc}-D{i + 1}', 420, 'CHECK')
        _v(f'{svc}-D{i + 1}', 760, 'MBFV', tag=f'{s} discharge MV', pt=f'Gfx_{s}_DischargeMV_Pos' if base else f'Gfx_{s}_MV_Pos')
for i in range(N):
    s = f'CH{i + 1:02d}'; base = i < 2
    _v(f'CHR-E{i + 1}', 400, 'BFV'); _v(f'CHR-E{i + 1}', -260, 'MBFV', tag=f'{s} CHW isolation', pt=f'Gfx_{s}_ChwIso_Pos'); _v(f'CHR-E{i + 1}', -120, 'FLEX')
    _v(f'CHS-E{i + 1}', 150, 'FLEX'); _v(f'CHS-E{i + 1}', 330, 'TT', pt=f'{s}_ChwSupplyTemp'); _v(f'CHS-E{i + 1}', 520, 'FS', tag=f'{s} evaporator flow switch')
    if base: _v(f'CHS-E{i + 1}', 900, 'MCV', tag=f'{s} CHW flow control', pt=f'Gfx_{s}_ChwFCV_Pos')
    _v(f'CDS-C{i + 1}', 400, 'BFV'); _v(f'CDS-C{i + 1}', -260, 'MBFV', tag=f'{s} CDW isolation', pt=f'Gfx_{s}_CdwIso_Pos'); _v(f'CDS-C{i + 1}', -120, 'FLEX')
    _v(f'CDR-C{i + 1}', 150, 'FLEX'); _v(f'CDR-C{i + 1}', 520, 'FS', tag=f'{s} condenser flow switch')
    if base: _v(f'CDR-C{i + 1}', 1000, 'MCV', tag=f'{s} head-pressure valve', pt=f'Gfx_{s}_CdwHPV_Pos')
for k in range(len(CT_X)):
    t = k // 2; s = f'CT{t + 1:02d}'; base = t < 2
    _v(f'CDR-T{k + 1}', 400, 'BFV'); _v(f'CDR-T{k + 1}', 900, 'MBFV', tag=f'{s} inlet', pt=f'Gfx_{s}_InletMV_Pos' if base else f'Gfx_{s}_Valve_Pos')
    _v(f'CDS-T{k + 1}', 250, 'MBFV', tag=f'{s} outlet', pt=f'Gfx_{s}_OutletMV_Pos' if base else f'Gfx_{s}_Valve_Pos'); _v(f'CDS-T{k + 1}', 700, 'BFV')
for f in range(2, B['floors'] + 1):
    _v(f'CHS-F{f}', -300, 'MCV', dn=4, tag=f'AHU_F{f:02d} CHW valve', pt=f'AHU_F{f:02d}_ValveCmd'); _v(f'CHR-F{f}', 300, 'BFV', dn=4)
_v('CHS-H', 1500, 'TT', tag='CHWS', pt='CHWS'); _v('CHS-H', 2200, 'FM', tag='CHWFlow', pt='CHWFlow'); _v('CHS-R', 1500, 'PT', tag='CHWDP')
_v('CHR-R', -600, 'TT', tag='CHWR', pt='CHWR'); _v('CHR-R', -900, 'PG')
_v('CHW-BP', 3000, 'BFV', dn=6); _v('CHW-BP', 3800, 'MCV', dn=6, tag='CHW bypass valve', pt='Gfx_CHW_BypassMV_Pos'); _v('CHW-BP', 4600, 'BFV', dn=6)
_v('CHW-ET', 120, 'BFV', dn=2)
_v('CDS-SH', 1200, 'TT', tag='CDS', pt='CDS'); _v('CDS-CH', 1800, 'FM', tag='CDW_Flow', pt='CDW_Flow'); _v('CDR-H', -1500, 'TT', tag='CDR', pt='CDR')


def length(p):
    return sum(math.dist(a, b) for a, b in zip(p['pts'], p['pts'][1:]))


def _on(pt, q):
    s = 0
    for a, b in zip(q['pts'], q['pts'][1:]):
        d = math.dist(a, b)
        if d and all(min(a[i], b[i]) - 1 <= pt[i] <= max(a[i], b[i]) + 1 for i in range(3)) and abs(math.dist(a, pt) + math.dist(pt, b) - d) < 2:
            t = s + math.dist(a, pt)
            if 1 < t < length(q) - 1: return t
        s += d
    return None


def _caps():
    for p in PIPES:
        for end in (('start',) if p['cap'] == 'start' else ('end',) if p['cap'] == 'end' else ('start', 'end') if p['cap'] == 'both' else ()):
            d = 1 if end == 'start' else -1
            _v(p['id'], d, 'CAP')
            z = p['pts'][0][2] if end == 'start' else p['pts'][-1][2]
            other = p['pts'][1][2] if end == 'start' else p['pts'][-2][2]
            if z < 1000: _v(p['id'], 25 * d, 'DRAIN', dn=1.5)
            elif z > other + 100: _v(p['id'], 60 * d, 'AAV')
_caps()

VALVE_INFO = {'BFV': 'Butterfly valve, lug type, PN16', 'MBFV': 'Motorized butterfly valve (on/off, 24 Vac)', 'CHECK': 'Check valve, silent / dual plate',
              'STRAINER': 'Y-strainer, 20 mesh', 'FLEX': 'Flexible connector, EPDM double sphere', 'PG': 'Pressure gauge 0-10 bar c/w cock',
              'TT': 'Temperature sensor 10k thermistor in well + thermometer', 'FS': 'Paddle flow switch', 'FM': 'Electromagnetic flow meter',
              'PT': 'Differential pressure transmitter 0-4 bar', 'AAV': 'Automatic air vent 3/4" c/w isolating ball valve',
              'MCV': 'Motorized control valve (modulating 0-10 V, position feedback)', 'RED_E': 'Eccentric reducer', 'RED_C': 'Concentric increaser',
              'CAP': 'End cap / blind flange (header stub)', 'DRAIN': 'Drain valve 1-1/2" c/w hose cap'}


def bends(p):
    pts = p['pts']; n = 0
    for a, b, c in zip(pts, pts[1:], pts[2:]):
        u = [b[i] - a[i] for i in range(3)]; v = [c[i] - b[i] for i in range(3)]
        if abs(sum(x * y for x, y in zip(u, v))) < 0.99 * math.hypot(*u) * math.hypot(*v): n += 1
    return n


def tees():
    T, seen = [], {}
    for p in PIPES:
        for end in (p['pts'][0], p['pts'][-1]):
            for q in PIPES:
                if q is not p and _on(end, q) is not None:
                    k = (q['id'], tuple(round(v) for v in end))
                    if k in seen: T[seen[k]] = (*T[seen[k]][:4], 'CROSS'); break
                    seen[k] = len(T); T.append((p['id'], q['id'], max(p['dn'], q['dn']), min(p['dn'], q['dn']), 'TEE')); break
    return T


def flow_span(p):
    L = length(p); S = []
    if p['cap'] not in ('start', 'both'): S.append(0)
    if p['cap'] not in ('end', 'both'): S.append(L)
    for q in PIPES:
        if q is p: continue
        for end in (q['pts'][0], q['pts'][-1]):
            t = _on(end, p)
            if t is not None: S.append(t)
    return (min(S), max(S)) if S else (0, L)


def valve_xyz(v):
    p = PIPE_BY_ID[v['pipe']]; pts = p['pts']; L = length(p)
    s = v['d'] if v['d'] >= 0 else L + v['d']
    for a, b in zip(pts, pts[1:]):
        d = math.dist(a, b)
        if s <= d: r = s / d if d else 0; return tuple(a[i] + (b[i] - a[i]) * r for i in range(3)), (b[0] - a[0], b[1] - a[1], b[2] - a[2]), p
        s -= d
    return pts[-1], (1, 0, 0), p


def clash_check(clear=40):
    """pipe-to-pipe surface clearance (mm) for segments that are not connected; returns the worst cases"""
    def segd(a, b, c, d):
        import numpy as np
        a, b, c, d = map(np.array, (a, b, c, d)); u, v, w = b - a, d - c, a - c
        A, Bv, C, D, E = u @ u, u @ v, v @ v, u @ w, v @ w; den = A * C - Bv * Bv
        sc, tc = (0.0, D / Bv if Bv else 0.0) if den < 1e-9 else ((Bv * E - C * D) / den, (A * E - Bv * D) / den)
        sc = min(1, max(0, sc)); tc = min(1, max(0, (E + sc * Bv) / C if C else 0)); sc = min(1, max(0, (tc * Bv - D) / A if A else 0))
        return float(np.linalg.norm(w + sc * u - tc * v))
    R = lambda p: p['dn'] * 25.4 / 2 * 1.08 + (45 if SERVICE[p['svc']][2] else 0)
    ends = lambda p: [p['pts'][0], p['pts'][-1]]
    bad = []
    for i, p in enumerate(PIPES):
        for q in PIPES[i + 1:]:
            conn = any(_on(e, q) is not None or any(math.dist(e, f) < 5 for f in ends(q)) for e in ends(p)) or any(_on(e, p) is not None for e in ends(q))
            if conn: continue
            for a, b in zip(p['pts'], p['pts'][1:]):
                for c, d in zip(q['pts'], q['pts'][1:]):
                    g = segd(a, b, c, d) - R(p) - R(q)
                    if g < clear: bad.append((round(g), p['id'], q['id']))
    return sorted(bad)


if __name__ == '__main__':
    print('equipment', len(EQ), 'air side', len(AIR_EQ), 'zones', len(ZONES), 'pipes', len(PIPES), 'valves', len(VALVES))
    print('clashes', clash_check()[:20])
