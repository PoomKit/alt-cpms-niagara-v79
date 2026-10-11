# -*- coding: utf-8 -*-
"""V7.9 2D drawing set (DXF per sheet + one PDF) from model79.py.  Re-uses the drafting helpers of the V7.8 set (lotus/gen2d.py):
A1 sheet, Thai / English title block, EIT practice symbols.  Slots that are not installed are drawn dashed (layer M-HID)."""
import math, os, sys
sys.path.insert(0, '/home/claude/lotus'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model79 as MD
import gen2d as G
import prims as PR
from ezdxf.enums import TextEntityAlignment as TA

OUT = '/home/claude/b79/out/dwg'; os.makedirs(OUT, exist_ok=True)
G.OUT = OUT
G.MD = MD
B, RM = MD.B, MD.ROOM
G.R = {'x': B['x'], 'y': B['y'], 'h': RM['h'], 'slab': B['slab'], 'wall': RM['wall'], 'ffs': 300}
T, L, rect, View = G.T, G.L, G.rect, G.View
ALL_EQ = MD.EQ + MD.AIR_EQ


def frame79(msp, no, title_en, title_th, scale_txt):
    W, H = 841, 594
    rect(msp, 0, 0, W, H, 'M-FRAME'); rect(msp, 20, 10, W - 10, H - 10, 'M-FRAME', 70)
    x0 = W - 10 - 125; rect(msp, x0, 10, W - 10, H - 10, 'M-FRAME', 50); y = H - 10
    def box(hh, lines, big=None):
        nonlocal y; rect(msp, x0, y - hh, W - 10, y, 'M-FRAME', 25); yy = y - 5
        if big: T(msp, x0 + 62.5, y - hh / 2 - 3, big, 6, align=TA.MIDDLE_CENTER)
        for s, h in lines: T(msp, x0 + 3, yy - h, s, h); yy -= h * 1.7
        y -= hh
    box(28, [], 'AETERLINK'); T(msp, x0 + 62.5, y + 5, 'AETERLINK (THAILAND) CO., LTD.  ·  BMS / CPMS', 2.2, align=TA.MIDDLE_CENTER)
    box(44, [('PROJECT / โครงการ :', 2.2), ('อาคารอ้างอิง 8 ชั้น (CPMS V7.9)', 3.0), (MD.PROJECT['name'], 2.6), ('STATION :', 2.2), (MD.PROJECT['station'], 2.4)])
    box(22, [('OWNER / เจ้าของโครงการ :', 2.2), ('[ระบุตามโครงการ]', 2.6)])
    box(34, [('BASIS / ที่มา :', 2.2), ('Reference design for logic & graphics', 2.3), ('Max. equipment 6 / type (register)', 2.3), ('Site survey: NOT DONE (ต้องสำรวจ)', 2.3)])
    box(58, [('ENGINEERS / วิศวกรผู้ออกแบบ-ตรวจสอบ', 2.4), ('วิศวกรเครื่องกล : ........................................', 2.3), ('ใบอนุญาต ภก./สก. เลขที่ : ..........................', 2.3),
             ('ลงนาม : ....................  วันที่ : ..............', 2.3), ('วิศวกรไฟฟ้า : ........................................', 2.3), ('ใบอนุญาต ภฟ./สฟ. เลขที่ : ..........................', 2.3)])
    rh = 7; box(rh * 6, [('REVISION / แก้ไข', 2.4)])
    for i, (r, d, t) in enumerate([('A', G.DATE, 'FOR REVIEW - generated from the V7.9 model'), ('', '', ''), ('', '', ''), ('', '', '')]):
        yy = y + rh * (4 - i); L(msp, (x0, yy), (W - 10, yy), 'M-FRAME'); T(msp, x0 + 2, yy + 2, r, 2.2); T(msp, x0 + 12, yy + 2, d, 2.2); T(msp, x0 + 38, yy + 2, t, 2.0)
    sy = y; box(24, []); T(msp, x0 + 62.5, sy - 10, 'FOR REVIEW · ไม่ใช่แบบก่อสร้าง', 4, align=TA.MIDDLE_CENTER); T(msp, x0 + 62.5, sy - 18, 'NOT FOR CONSTRUCTION', 3, align=TA.MIDDLE_CENTER)
    box(36, [('DRAWING TITLE / ชื่อแบบ :', 2.2), (title_th, 3.2), (title_en, 2.8)])
    box(30, [('DRAWN : AETERLINK model generator', 2.2), ('CHECKED : ..................', 2.2), ('APPROVED : ................', 2.2), ('SCALE : ' + scale_txt + '     DATE : ' + G.DATE, 2.2)])
    rect(msp, x0, 10, W - 10, y, 'M-FRAME', 25); T(msp, x0 + 3, y - 6, 'DRAWING NO. / เลขที่แบบ', 2.2); T(msp, x0 + 62.5, (10 + y) / 2 - 6, no, 9, align=TA.MIDDLE_CENTER)
    T(msp, x0 + 62.5, 14, 'หน่วยวัดเป็นมิลลิเมตร ระดับอ้างอิงพื้นชั้น 1 ±0.000', 2.0, align=TA.BOTTOM_CENTER)
G.frame = frame79


def installed(e):
    return e.get('installed', True)


def draw_eq(V, eqs, label=True, zmin=-1e9, zmax=1e9):
    for e in eqs:
        if not zmin <= e['z'] <= zmax: continue
        lay = 'M-EQ' if installed(e) else 'M-HID'
        for p in PR.eq_prims(e): G.draw_prim(V, PR.to_world(e, p), lay)
        if label:
            if V.vn == 'plan': T(V.msp, *V.p(e['x'], e['y']), e['id'] + ('' if installed(e) else ' (slot ว่าง)'), 2.2, 'M-TXT', TA.MIDDLE_CENTER)
            else: T(V.msp, *V.p(e['x'], e['y'], e['z'] + e['H'] + 400), e['id'], 2.0, 'M-TXT', TA.BOTTOM_CENTER)


def draw_pipes(V, pipes, zmin=-1e9, zmax=1e9, labels=True):
    m = V.msp
    for p in pipes:
        lay = 'M-' + p['svc']; r = p['dn'] * 25.4 / 2 + (40 if MD.SERVICE[p['svc']][2] else 0)
        if p.get('slot') and not MD.INST.get(p['slot'], True): lay = 'M-HID'
        best = None
        for a, b in zip(p['pts'], p['pts'][1:]):
            if max(a[2], b[2]) < zmin or min(a[2], b[2]) > zmax: continue
            pa, pb = V.p(*a), V.p(*b); d = math.dist(pa, pb)
            if d < 1e-6: m.add_circle(pa, max(.6, r / V.sc), dxfattribs={'layer': lay}); continue
            ux, uy = (pb[0] - pa[0]) / d, (pb[1] - pa[1]) / d; o = max(.35, r / V.sc)
            for s in (-1, 1): L(m, (pa[0] - uy * o * s, pa[1] + ux * o * s), (pb[0] - uy * o * s, pb[1] + ux * o * s), lay, 25)
            if not best or d > best[0]: best = (d, pa, pb, ux, uy, o)
        if labels and best and best[0] > 25 and p['dn'] >= 8:
            d, pa, pb, ux, uy, o = best; mx, my = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2; ang = math.degrees(math.atan2(uy, ux))
            if ang > 90 or ang < -90: ang += 180
            T(m, mx - uy * (o + 1.2), my + ux * (o + 1.2), f'{p["svc"]} Ø{p["dn"]}"', 1.8, lay, TA.BOTTOM_CENTER, ang)


def valves(V, zmin=-1e9, zmax=1e9):
    for v in MD.VALVES:
        xyz, _, _ = MD.valve_xyz(v)
        if zmin <= xyz[2] <= zmax: G.valve_sym(V, v)


def grid_lines(V, x0, x1, y0, y1):
    m = V.msp
    for n, x in MD.GRID_X:
        if x0 <= x <= x1: a, b = V.p(x, y0 - 2500), V.p(x, y1 + 1500); L(m, a, b, 'M-GRID'); m.add_circle((a[0], a[1] - 4), 3.5, dxfattribs={'layer': 'M-GRID'}); T(m, a[0], a[1] - 4, n, 2.4, align=TA.MIDDLE_CENTER)
    for n, y in MD.GRID_Y:
        if y0 <= y <= y1: a, b = V.p(x0 - 2500, y), V.p(x1 + 1500, y); L(m, a, b, 'M-GRID'); m.add_circle((a[0] - 4, a[1]), 3.5, dxfattribs={'layer': 'M-GRID'}); T(m, a[0] - 4, a[1], n, 2.4, align=TA.MIDDLE_CENTER)


def outline(V, x0, y0, x1, y1, lay='M-WALL', lw=50):
    rect(V.msp, *V.p(x0, y0), *V.p(x1, y1), lay, lw)


def zones(V, floor):
    for z in MD.ZONES:
        if z['floor'] != floor: continue
        outline(V, z['x0'], z['y0'], z['x1'], z['y1'], 'M-GRID', 13)
        cx, cy = (z['x0'] + z['x1']) / 2, (z['y0'] + z['y1']) / 2
        T(V.msp, *V.p(cx, cy + 900), f"ZONE {z['code']}", 2.2, align=TA.MIDDLE_CENTER); T(V.msp, *V.p(cx, cy - 900), z['name'], 2.0, align=TA.MIDDLE_CENTER)
        T(V.msp, *V.p(cx, cy - 2600), f"TT/RH: ZoneTemperatureAvg_{z['code']}", 1.6, align=TA.MIDDLE_CENTER)


def sheet_cover():
    G.DRAWING_LIST[:] = DL
    G.GENERAL_NOTES[:] = NOTES
    S = G.sheet_legend(); m = S['msp']
    for e in m.query('TEXT'):
        t = e.dxf.text
        if 'โลตัส' in t: e.dxf.text = 'งานระบบปรับอากาศและน้ำเย็น — อาคารอ้างอิง 8 ชั้น (CPMS V7.9)'
        elif "LOTUS'S" in t: e.dxf.text = 'CPMS REFERENCE BUILDING V7.9 · CHILLER PLANT (MAX 6 PER TYPE) · AIR SIDE · MODEL-GENERATED DRAWING SET'
    return S


def sheet_site_1f():
    S = G.new_sheet('M-101', 'GROUND FLOOR PLAN - BUILDING', 'แปลนชั้น 1 ทั้งอาคาร (ห้องเครื่อง + พื้นที่ใช้งาน)', '1:200')
    V = View(S, 'plan', 70, 200, 200); outline(V, 0, 0, B['x'], B['y']); outline(V, 0, 0, RM['x'], RM['y'], 'M-WALL', 70)
    outline(V, MD.CORE['x0'], MD.CORE['y0'], MD.CORE['x1'], MD.CORE['y1'], 'M-WALL', 35); T(S['msp'], *V.p(44000, 21000), 'CORE (บันได/ลิฟต์/shaft)', 2.2, align=TA.MIDDLE_CENTER)
    grid_lines(V, 0, B['x'], 0, B['y']); zones(V, 1)
    draw_eq(V, MD.EQ, label=False, zmax=3000); draw_eq(V, [e for e in MD.AIR_EQ if e['floor'] == 1 and e['type'] != 'fan' or e['id'] == 'EF-03'])
    T(S['msp'], *V.p(RM['x'] / 2, RM['y'] / 2), 'CHILLER PLANT ROOM (ดู M-102)', 3.2, align=TA.MIDDLE_CENTER)
    V.dim(V.p(0, 0), V.p(B['x'], 0), (0, V.oy - 22)); V.dim(V.p(0, 0), V.p(0, B['y']), (V.ox - 22, 0), angle=90)
    V.dim(V.p(0, 0), V.p(RM['x'], 0), (0, V.oy - 14)); V.dim(V.p(B['x'], 0), V.p(B['x'], RM['y']), (V.p(B['x'], 0)[0] + 12, 0), angle=90)
    G.north(S['msp'], 680, 520); G.view_title(V, 70, 150, '1', 'แปลนชั้น 1 / GROUND FLOOR PLAN', '1:200')
    G.key_notes(S['msp'], 70, 120, ['1. ห้องเครื่องทำน้ำเย็น 44.0 x 15.0 ม. สูง 5.5 ม. ด้านทิศใต้-ตะวันตกของอาคาร', '2. Zone 01_0101..0112 = จุด ZoneTemperatureAvg / ZoneHumidityAvg ใน station',
                                     '3. AHU-01 / AHU-02 / FCU-01..04 = air side ชั้น 1 (V7.8)', '4. ท่อ CHW ขึ้นอาคารผ่าน shaft ข้าง core (ดู M-104, M-502)'])
    return S


def sheet_plantroom():
    S = G.new_sheet('M-102', 'CHILLER PLANT ROOM PLAN', 'แปลนห้องเครื่องทำน้ำเย็น (สูงสุด 6 ชุดต่อชนิด)', '1:100')
    V = View(S, 'plan', 60, 300, 100); outline(V, 0, 0, RM['x'], RM['y'], 'M-WALL', 70); grid_lines(V, 0, RM['x'], 0, RM['y'])
    draw_eq(V, [e for e in MD.EQ if e['z'] < 3000]); draw_pipes(V, MD.PIPES, zmax=RM['h']); valves(V, zmax=RM['h'])
    xs = [0] + MD.CH_X + [RM['x']]
    for a, b in zip(xs, xs[1:]): V.dim(V.p(a, MD.CH_Y), V.p(b, MD.CH_Y), (0, V.p(0, RM['y'])[1] + 8))
    V.dim(V.p(0, 0), V.p(RM['x'], 0), (0, V.oy - 14)); V.dim(V.p(0, 0), V.p(0, RM['y']), (V.ox - 14, 0), angle=90)
    ys = [0] + MD.PUMP_Y + [RM['y']]
    for a, b in zip(ys, ys[1:]): V.dim(V.p(RM['x'], a), V.p(RM['x'], b), (V.p(RM['x'], 0)[0] + 10, 0), angle=90)
    G.north(S['msp'], 680, 520); G.view_title(V, 60, 250, '2', 'แปลนห้องเครื่อง / PLANT ROOM PLAN', '1:100')
    G.key_notes(S['msp'], 60, 225, ['1. เส้นประ = slot ที่ยังไม่ติดตั้ง (CHxx/CHPxx/CDPxx/CTxx _Installed = ปิด) เผื่อพื้นที่ ฐาน และ tee ไว้แล้ว',
                                    '2. Header ทุกเส้นเป็นท่อตรง ปลาย cap + drain · riser ขึ้นอาคาร/ดาดฟ้าใน shaft',
                                    '3. ระดับศูนย์ท่อ: ดูดปั๊ม +0.620 · CDW ไป condenser +1.800 · CHW ไป evaporator +2.600 · CHS +3.300 · CDR +4.200',
                                    '4. Chiller ทุกเครื่องมี MBFV ฝั่งน้ำเย็น/น้ำระบายความร้อน + flow switch · ปั๊มมี check + MBFV ด้านจ่าย',
                                    '5. ปั๊ม CHP / CDP แบบ headered: จำนวนเครื่องเดินตามจำนวน chiller ที่ต้องการน้ำ (v79_scale.py)'])
    return S


def sheet_roof():
    S = G.new_sheet('M-103', 'ROOF PLAN - COOLING TOWERS', 'แปลนดาดฟ้า - หอระบายความร้อน 6 ชุด (12 cell)', '1:100')
    V = View(S, 'plan', 60, 330, 100); m = S['msp']; outline(V, 0, 0, 46000, 16000, 'M-WALL', 35); grid_lines(V, 0, 44000, 0, 16000)
    draw_eq(V, [e for e in MD.EQ if e['type'] == 'ct']); draw_pipes(V, MD.PIPES, zmin=MD.ROOF_Z - 1); valves(V, zmin=MD.ROOF_Z)
    draw_eq(V, [e for e in MD.AIR_EQ if e['z'] >= MD.ROOF_Z and e['x'] < 46000 and e['y'] < 16000])
    xs = [MD.CT_X[0] - 1300] + [x + 1300 for x in MD.CT_X]
    V.dim(V.p(xs[0], 4700), V.p(xs[-1], 4700), (0, V.p(0, 3000)[1] - 10))
    G.north(m, 680, 520); G.view_title(V, 60, 280, '3', 'แปลนดาดฟ้า / ROOF PLAN (เฉพาะพื้นที่เหนือห้องเครื่อง)', '1:100')
    G.key_notes(m, 60, 255, ['1. CT แต่ละชุด 2 cell ตั้งบนโครงเหล็ก (grillage) สูง 1.0 ม. จากพื้นดาดฟ้า', '2. CT-01/02 = เครื่องเดิม V7.8 (MBFV เข้า/ออกแยก) · CT-03..06 = slot ขยาย (วาล์วชุดเดียว)',
                             '3. Header CDR จ่ายน้ำร้อนเข้าแต่ละ cell / header CDS รวมน้ำเย็นลง riser', '4. OAU-01, EF, LSF, SEF อยู่บนดาดฟ้า (ดู M-104)'])
    return S


def sheet_typical():
    S = G.new_sheet('M-104', 'TYPICAL FLOOR PLAN (FLOORS 2-8) - AIR SIDE', 'แปลนชั้นทั่วไป 2-8 ระบบปรับอากาศ (AHU + zone)', '1:200')
    V = View(S, 'plan', 70, 200, 200); m = S['msp']; outline(V, 0, 0, B['x'], B['y']); outline(V, MD.CORE['x0'], MD.CORE['y0'], MD.CORE['x1'], MD.CORE['y1'], 'M-WALL', 35)
    grid_lines(V, 0, B['x'], 0, B['y']); zones(V, 2)
    draw_eq(V, [e for e in MD.AIR_EQ if e['floor'] == 2]); draw_pipes(V, [p for p in MD.PIPES if p['id'] in ('CHS-F2', 'CHR-F2')], labels=False)
    for x, y, n in ((MD.X_CHS_R, MD.Y_CHS_R, 'CHS riser'), (MD.X_CHR_R, MD.Y_CHR_R, 'CHR riser')):
        m.add_circle(V.p(x, y), 1.6, dxfattribs={'layer': 'M-CHS' if 'CHS' in n else 'M-CHR'}); T(m, *V.p(x, y - 1500), n, 1.8, align=TA.MIDDLE_CENTER)
    G.north(m, 680, 520); G.view_title(V, 70, 150, '4', 'แปลนชั้นทั่วไป / TYPICAL FLOOR (ชั้น 2 แสดง, ชั้น 3-8 เหมือนกัน)', '1:200')
    G.key_notes(m, 70, 120, ['1. AHU_Fnn ชั้นละ 1 ชุด คุม CHW valve ตามอุณหภูมิเฉลี่ย 4 zone (zone OOS ไม่นับ) + RH สูง = valve ขั้นต่ำ (dehum)',
                             '2. Zone code nn_nn01..04 = ZoneTemperatureAvg / ZoneHumidityAvg (AirPlug / Sense-T)',
                             '3. ท่อ CHW แยกจาก riser ใน shaft เข้า AHU ผ่าน MCV (AHU_Fnn_ValveCmd)', '4. ระบบอื่นในอนาคต (fire alarm, sprinkler, lighting) เพิ่มใน register sheet Systems'])
    return S


def sheet_section():
    S = G.new_sheet('M-201', 'BUILDING SECTION', 'รูปตัดอาคาร (ห้องเครื่องชั้น 1 - riser - cooling tower ดาดฟ้า)', '1:200')
    V = View(S, 'S', 70, 90, 200); m = S['msp']
    def P(x, z): return (V.ox + x / V.sc, V.oy + z / V.sc)
    for f in range(1, B['floors'] + 2):
        z = MD.zf(f) if f <= B['floors'] else MD.ROOF_Z
        rect(m, *P(0, z - B['slab']), *P(B['x'], z), 'M-WALL', 35)
        T(m, *P(B['x'] + 1500, z + 300), (f'ชั้น {f}  +{z / 1000:.3f}' if f <= B['floors'] else f'ดาดฟ้า  +{z / 1000:.3f}'), 2.2)
    rect(m, *P(0, -300), *P(B['x'], 0), 'M-WALL', 50); L(m, P(-3000, -300), P(B['x'] + 3000, -300), 'M-WALL', 50)
    for x in (0, B['x']): L(m, P(x, 0), P(x, MD.ROOF_Z + B['parapet']), 'M-WALL', 50)
    rect(m, *P(MD.CORE['x0'], 0), *P(MD.CORE['x1'], MD.ROOF_Z + 3500), 'M-WALL', 25)
    draw_eq(V, [e for e in MD.EQ if e['type'] in ('chiller', 'ct')], label=False)
    draw_eq(V, [e for e in MD.AIR_EQ if e['type'] == 'ahu'], label=False)
    draw_pipes(V, [p for p in MD.PIPES if p['id'] in ('CHS-R', 'CHR-R', 'CDS-R', 'CDR-R', 'CDS-RH', 'CDR-RH')], labels=True)
    V.dim(P(-2000, 0), P(-2000, MD.ROOF_Z), (V.ox - 12, 0), angle=90)
    G.view_title(V, 70, 60, '5', 'รูปตัดอาคาร / BUILDING SECTION (มองทิศเหนือ)', '1:200')
    return S


def _box(m, x, y, w, h, t, lay='M-EQ', sub=None):
    rect(m, x, y, x + w, y + h, lay, 35); T(m, x + w / 2, y + h / 2 + (1.6 if sub else 0), t, 2.4, align=TA.MIDDLE_CENTER)
    if sub: T(m, x + w / 2, y + h / 2 - 2.6, sub, 1.7, align=TA.MIDDLE_CENTER)


def sheet_schematic():
    S = G.new_sheet('M-501', 'CHW / CDW SCHEMATIC - 6 SLOTS PER TYPE', 'แผนผังระบบท่อน้ำเย็น / น้ำระบายความร้อน (6 slot ต่อชนิด)', 'NTS'); m = S['msp']
    def pipe(pts, svc, lay=None):
        m.add_lwpolyline(pts, dxfattribs={'layer': lay or 'M-' + svc}).dxf.lineweight = 50
    xs = [70 + i * 95 for i in range(6)]
    # headers
    pipe([(50, 300), (640, 300)], 'CHS'); T(m, 52, 303, 'CHS header → อาคาร (riser)', 2.4)
    pipe([(50, 250), (640, 250)], 'CHR'); T(m, 52, 253, 'CHR header (จากปั๊ม CHP)', 2.4)
    pipe([(50, 200), (640, 200)], 'CDS'); T(m, 52, 203, 'CDS header (จากปั๊ม CDP)', 2.4)
    pipe([(50, 150), (640, 150)], 'CDR'); T(m, 52, 153, 'CDR header → cooling tower', 2.4)
    for i, x in enumerate(xs):
        s = f'CH{i + 1:02d}'; inst = MD.INST[s]; lay = None if inst else 'M-HID'
        _box(m, x, 210, 60, 30, f'CH-{i + 1:02d}', 'M-EQ' if inst else 'M-HID', 'V7.8 base' if i < 2 else ('installed' if inst else 'slot ว่าง'))
        pipe([(x + 15, 250), (x + 15, 240)], 'CHR', lay); pipe([(x + 45, 240), (x + 45, 300)], 'CHS', lay)
        pipe([(x + 10, 200), (x + 10, 210)], 'CDS', lay); pipe([(x + 50, 210), (x + 50, 150)], 'CDR', lay)
        for (px, py) in ((x + 15, 245), (x + 10, 205)): G._sym(type('V', (), {'msp': m})(), 'MBFV', (px, py), (0, 1))
    for k, (kind, y0, svc_in, svc_out) in enumerate((('CHP', 430, 'CHR', 'CHR'), ('CDP', 370, 'CDS', 'CDS'))):
        T(m, 52, y0 + 22, f'{kind} pumps (headered, VSD)', 2.6)
        for i, x in enumerate(xs):
            s = f'{kind}{i + 1:02d}'; inst = MD.INST[s]
            m.add_circle((x + 30, y0), 9, dxfattribs={'layer': 'M-EQ' if inst else 'M-HID'}); T(m, x + 30, y0, f'{kind}-{i + 1:02d}', 2.0, align=TA.MIDDLE_CENTER)
            if not inst: T(m, x + 30, y0 - 13, 'slot ว่าง', 1.7, align=TA.MIDDLE_CENTER)
            hy = 250 if kind == 'CHP' else 200
            m.add_lwpolyline([(x + 30, y0 - 9), (x + 30, hy)], dxfattribs={'layer': ('M-' + svc_out) if inst else 'M-HID'})
    for i, x in enumerate(xs):
        s = f'CT{i + 1:02d}'; inst = MD.INST[s]
        _box(m, x, 500, 60, 28, f'CT-{i + 1:02d} (2 cells)', 'M-EQ' if inst else 'M-HID', 'roof +34.900' if inst else 'slot ว่าง')
    T(m, 52, 545, 'COOLING TOWERS (ดาดฟ้า)', 2.8)
    G.key_notes(m, 52, 120, ['1. ทุกชนิดมี 6 slot: 01-02 = เครื่องเดิม V7.8 (logic เดิม), 03-06 = slot ขยาย (Expansion/<slot> ใน station)',
                             '2. เส้นประ = ยังไม่ติดตั้ง · เปิดใช้งาน: ตั้ง <slot>_Installed = true หรือแก้ register แล้วสร้างใหม่',
                             '3. ลำดับเดิน slot 03 → 06 ข้ามเครื่องที่ไม่พร้อม (fault / maintenance / start fail) อัตโนมัติ',
                             '4. จำนวน CHP / CDP / CT ที่เดิน = จำนวน chiller ที่ต้องการน้ำ (รวม post-run) ลบด้วยเครื่องเดิมที่พร้อม'])
    return S


def sheet_riser():
    S = G.new_sheet('M-502', 'CHW RISER DIAGRAM', 'แผนผัง riser น้ำเย็นไป AHU ทุกชั้น', 'NTS'); m = S['msp']
    x1, x2 = 200, 240
    for f in range(1, B['floors'] + 2):
        y = 60 + (f - 1) * 55; L(m, (80, y), (640, y), 'M-WALL', 35); T(m, 82, y + 2, f'ชั้น {f}' if f <= B['floors'] else 'ดาดฟ้า', 2.6)
        if 2 <= f <= B['floors']:
            m.add_lwpolyline([(x2, y + 30), (330, y + 30), (330, y + 20)], dxfattribs={'layer': 'M-CHS'}); m.add_lwpolyline([(x1, y + 35), (360, y + 35), (360, y + 20)], dxfattribs={'layer': 'M-CHR'})
            _box(m, 320, y + 6, 55, 14, f'AHU_F{f:02d}', sub='MCV: AHU_F%02d_ValveCmd' % f)
            G._sym(type('V', (), {'msp': m})(), 'MCV', (300, y + 30), (1, 0))
    L(m, (x1, 60), (x1, 60 + 8 * 55), 'M-CHR', 70); L(m, (x2, 60), (x2, 60 + 8 * 55), 'M-CHS', 70)
    T(m, x1 - 2, 40, 'CHR riser Ø16"', 2.4, align=TA.RIGHT); T(m, x2 + 2, 40, 'CHS riser Ø16"', 2.4)
    _box(m, 150, 30, 140, 22, 'CHILLER PLANT (ชั้น 1)', sub='ดู M-102 / M-501')
    return S


DL = [('M-000', 'ปก รายการแบบ สัญลักษณ์ หมายเหตุทั่วไป'), ('M-101', 'แปลนชั้น 1 ทั้งอาคาร 1:200'), ('M-102', 'แปลนห้องเครื่องทำน้ำเย็น 1:100'),
      ('M-103', 'แปลนดาดฟ้า cooling tower 1:100'), ('M-104', 'แปลนชั้นทั่วไป 2-8 air side 1:200'), ('M-201', 'รูปตัดอาคาร 1:200'),
      ('M-501', 'แผนผังระบบท่อ CHW / CDW (6 slot)'), ('M-502', 'แผนผัง riser น้ำเย็นไป AHU'), ('M-601', 'ตารางอุปกรณ์')]
NOTES = ['1. แบบชุดนี้สร้างอัตโนมัติจาก model79.py ชุดเดียวกับกราฟิก 3D และ BOQ — แก้ที่ทะเบียน/แบบจำลองแล้วสร้างใหม่ทั้งชุด',
         '2. เป็นแบบอ้างอิงสำหรับ logic และกราฟิก ขนาดและตำแหน่งต้องออกแบบ/สำรวจยืนยันตามโครงการจริง',
         '3. หน่วยวัดเป็นมิลลิเมตร ระดับอ้างอิงพื้นชั้น 1 ±0.000',
         '4. ท่อน้ำเย็น/น้ำระบายความร้อน: ท่อเหล็กดำ ASTM A53 Sch.40 ข้อต่อเชื่อม/หน้าแปลน PN16',
         '5. ท่อน้ำเย็นหุ้มฉนวนยางสังเคราะห์ 25 มม. คาดแถบสีและลูกศรทิศทางการไหลทุก 3 ม.',
         '6. อุปกรณ์เส้นประ = slot ที่เตรียมพื้นที่/tee ไว้แต่ยังไม่ติดตั้ง (Installed = N ในทะเบียน)',
         '7. การออกแบบอ้างอิงมาตรฐานระบบปรับอากาศ วสท. และ ASHRAE',
         '8. วาล์ว M / C และเครื่องมือวัดเชื่อมกับ BMS ' + MD.PROJECT['station'] + ' ตาม Field IO register',
         '9. ผู้รับจ้างต้องจัดทำ shop drawing ลงนามโดยวิศวกรผู้มีใบอนุญาตก่อนดำเนินการ']


def build():
    G.SHEETS.clear()
    sheet_cover(); sheet_site_1f(); sheet_plantroom(); sheet_roof(); sheet_typical(); sheet_section(); sheet_schematic(); sheet_riser()
    rows = []
    for e in ALL_EQ:
        d = e['data']; rows.append((e['id'], e['type'].upper(), d.get('Model') or d.get('Service') or d.get('Type', ''),
                                    ' · '.join(str(v) for k, v in d.items() if k in ('Capacity', 'Flow', 'Head', 'Motor', 'Fan', 'Volume', 'Efficiency', 'Airflow')),
                                    'ROOF' if e['z'] >= MD.ROOF_Z else f"ชั้น {e.get('floor', 1)}", 'ติดตั้ง' if installed(e) else 'slot ว่าง', e['pt'] or '-'))
    G.sheet_schedule(rows[:65])
    for S in G.SHEETS: S['doc'].saveas(f"{OUT}/{S['no']}.dxf")
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; from matplotlib.backends.backend_pdf import PdfPages
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, ColorPolicy
    cfg = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.COLOR, lineweight_scaling=.6)
    with PdfPages('/home/claude/b79/out/ALT_V79_DrawingSet.pdf') as pdf:
        for S in G.SHEETS:
            fig = plt.figure(figsize=(841 / 25.4, 594 / 25.4)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
            Frontend(RenderContext(S['doc']), MatplotlibBackend(ax), config=cfg).draw_layout(S['doc'].modelspace(), finalize=True)
            ax.set_xlim(0, 841); ax.set_ylim(0, 594); ax.set_aspect('equal'); fig.set_size_inches(841 / 25.4, 594 / 25.4); ax.set_position([0, 0, 1, 1]); pdf.savefig(fig); plt.close(fig)
    print('sheets', [S['no'] for S in G.SHEETS])


if __name__ == '__main__':
    build()
