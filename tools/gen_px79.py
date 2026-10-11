# -*- coding: utf-8 -*-
"""V7.9 Px pages that show the same data as the 3D page (ALT_V79_Building3D.html):
  ALT_V79_Plant     chiller / CHW pump / CDW pump / cooling tower slots 01-06 (installed, running, load / speed, valve, fault),
                    expansion supervisor, plant KPI
  ALT_V79_Building  8 floors: floor AHU + every zone temperature / humidity / CO2 (same points as the 3D zones)
usage: gen_px79.py v79.bog kitdir outdir"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_px7 as P7
import gen_px as G
from gen_px7 import val, lbl, panel, rows, pic_bool, kpi_strip, PANEL, EDGE, LBL, RUN, OFF, FLT, WARN

# pages opened by navigation instead of a popup: the 3D page is HTML (BajaScript) and must work in the HTML5 / browser profile
LINKS = {'ALT_V79_Building3D': 'file:^web/ALT_V79_Building3D.html'}
PAGES = [('ALT_V79_Plant', 'Plant overview'), ('ALT_V79_Plant_Details', 'Plant schematic'), ('ALT_V79_PlantCards', 'Plant cards'), ('ALT_V79_Building', 'Building / Zones'), 
         ('ALT_V79_Building3D', '3D Live'), ('ALT_V77_FieldIO', 'Field IO'), ('ALT_CP_AlarmsHistory', 'Alarms')]
IMG = {'CH': ('Chillers/Turbo/Chiller_Turbo_Left/Chiller_Turbo_Left_On.gif', 'Chillers/Turbo/Chiller_Turbo_Left/Chiller_Turbo_Left_Off.png'),
       'P': ('Pumps/Pumps_Base/Pump_Base_Left/Pump_Base_Left_On.gif', 'Pumps/Pumps_Base/Pump_Base_Left/Pump_Base_Left_Off.png'),
       'CT': ('CoolingTowers/PushThru/CoolingTower_PushThru_Left/CoolingTower_PushThru_Left_On.gif',
              'CoolingTowers/PushThru/CoolingTower_PushThru_Left/CoolingTower_PushThru_Left_Off.png')}


def header(p):
    W = p.size[0]
    p.rect(0, 0, W, p.size[1], fill='#12161b', stroke='#12161b', pen=1.0)
    p.label(0, 0, W, 40, f'  ALT Reference V7.9 — {p.title}', 18, True, 'white', '#0b0e11')
    p.label(W - 470, 8, 460, 24, 'SAME DATA AS 3D DIGITAL TWIN · REFERENCE SIMULATION', 10, True, '#263238', '#ffca28', 'center')
    x = 8
    for name, title in PAGES:
        cur = name == p.name
        p.label(x, 44, 150, 26, title, 9, True, 'white' if cur else '#cfd8dc', '#1e88e5' if cur else '#2c3440', 'center',
                popup=None if cur else f'file:^px/{name}.px', ptitle=title, link=None if cur else LINKS.get(name))
        x += 154


def card(p, x, y, w, h, title, img, run, items, inst, fault=None, scale=1.0):
    panel(p, x, y, w, h, title)
    val(p, x + w - 92, y + 2, 88, inst, f'{title} installed', h=16, size=8, bool_c=('#1f6f43', '#5d6d7e'))
    iw, ih = P7.img_size(img[1])
    s = min(scale, (w - 16) / iw, 92 / ih)
    pic_bool_scaled(p, x + (w - iw * s) / 2, y + 24, run, img[0], img[1], f'{title} running', iw * s, ih * s)
    yy = y + 24 + ih * s + 4
    rows(p, x + 2, yy, w - 4, items, rh=20)
    if fault: P7.status_led(p, x + 6, y + 24, fault, f'{title} fault', 'alarm')


def pic_bool_scaled(p, x, y, point, on, off, what, w, h):
    from xml.sax.saxutils import quoteattr
    o = p.ord(point); KG = P7.KG
    p.el.append(f'<Picture layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" image="{KG}/{off}" scaleFactor="1.0">\n'
                f'  <ValueBinding ord={quoteattr(o)}>\n    <IBooleanToSimple name="image">\n'
                f'      <Image name="trueValue" value="{KG}/{on}"/>\n      <Image name="falseValue" value="{KG}/{off}"/>\n'
                f'    </IBooleanToSimple>\n  </ValueBinding>\n</Picture>')
    p.map.append((point, o, what, 'display (image on/off)'))


def plant79():
    p = G.Page('ALT_V79_PlantCards', 'Chiller plant · 6 slots per type (cards)', (1920, 1080)); header(p)
    kpi_strip(p)
    W, X0 = 228, 8
    y = 136
    lbl(p, 8, y, 300, 'CHILLERS  (slot 01-02 = V7.8 base · 03-06 = expansion)', 10, 'white', True); y += 20
    for i in range(1, 7):
        u = f'CH{i:02d}'
        card(p, X0 + (i - 1) * (W + 6), y, W, 238, f'CH-{i:02d}', IMG['CH'], f'{u}RunProof',
             [('Load %', f'{u}LoadPct'), ('LWT °C', f'{u}_ChwSupplyTemp'), ('CHW valve %', f'Gfx_{u}_ChwIso_Pos'),
              ('CDW valve %', f'Gfx_{u}_CdwIso_Pos')], f'{u}_Installed', f'{u}Fault')
    y += 248
    for k, name in (('CHP', 'CHW PUMPS'), ('CDP', 'CDW PUMPS')):
        lbl(p, 8, y, 300, name, 10, 'white', True); y += 20
        for i in range(1, 7):
            u = f'{k}{i:02d}'; mv = f'Gfx_{u}_DischargeMV_Pos' if i <= 2 else f'Gfx_{u}_MV_Pos'
            card(p, X0 + (i - 1) * (W + 6), y, W, 150, f'{k}-{i:02d}', IMG['P'], f'{u}RunProof',
                 [('Speed %', f'{u}SpeedCmd'), ('Valve %', mv)], f'{u}_Installed', f'{u}Fault', scale=.7)
        y += 158
    lbl(p, 8, y, 300, 'COOLING TOWERS (roof)', 10, 'white', True); y += 20
    for i in range(1, 7):
        u = f'CT{i:02d}'
        run, spd = (f'{u}_01RunProof', f'{u}_01SpeedCmd') if i <= 2 else (f'{u}RunProof', f'{u}SpeedCmd')
        vp = f'Gfx_{u}_InletMV_Pos' if i <= 2 else f'Gfx_{u}_Valve_Pos'
        card(p, X0 + (i - 1) * (W + 6), y, W, 150, f'CT-{i:02d}' + (' (2 cells)' if i <= 2 else ''), IMG['CT'], run,
             [('Fan speed %', spd), ('Valve %', vp)], f'{u}_Installed', f'{u}Fault', scale=.55)
    # supervisor
    x = X0 + 6 * (W + 6) + 4; panel(p, x, 136, 1920 - x - 8, 360, 'EXPANSION SUPERVISOR')
    rows(p, x + 4, 160, 1920 - x - 16, [('Expansion slots in use', 'CHX_Enable', {'bool_c': (RUN, OFF)}), ('Chillers wanted (03-06)', 'CHX_TargetNum'),
                                         ('Added for load', 'CHX_StageAdd'), ('Average load %', 'CHX_AverageLoad'),
                                         ('Chillers needing water', 'CHX_ChillersNeedingWater'), ('Stage 2 request', 'Stage2Request', {'bool_c': (RUN, OFF)}),
                                         ('Add chiller above %', 'CHX_UpLoadPct', {'action': True}), ('Remove below %', 'CHX_DownLoadPct', {'action': True})], rh=24)
    lbl(p, x + 6, 360, 1920 - x - 20, 'Installed = yes: unit counted by the logic.  Grey picture = not running.  '
        'Change <slot>_Installed in Workbench or the equipment register (ALT_V79_Equipment_Register.xlsx).', 9, LBL, h=120)
    panel(p, x, 506, 1920 - x - 8, 250, 'PLANT')
    rows(p, x + 4, 530, 1920 - x - 16, [('CHW flow gpm', 'CHWFlow'), ('CDW flow gpm', 'CDW_Flow'), ('CDS °C', 'CDS'), ('CDR °C', 'CDR'),
                                         ('Bypass valve %', 'Gfx_CHW_BypassMV_Pos'), ('Plant kW', 'Plant_kW'), ('kW/RT', 'Plant_kW_per_RT'),
                                         ('Running chillers', 'CHX_TotalRun')], rh=24)
    return p


def building79(zones):
    p = G.Page('ALT_V79_Building', 'Building · floors / zones (temp · RH · CO2)', (1920, 1080)); header(p)
    by = {}
    for c in zones: by.setdefault(int(c[:2]), []).append(c)
    y = 80
    for fl in range(8, 0, -1):
        zs = by.get(fl, [])
        panel(p, 8, y, 1904, 112, f'FLOOR {fl}' + ('  · plant room + retail (12 zones)' if fl == 1 else ''))
        if fl > 1:
            u = f'AHU_F{fl:02d}'
            rows(p, 12, y + 24, 230, [('AHU run', f'{u}_Status', {'bool_c': (RUN, OFF)}), ('CHW valve %', f'{u}_ValveCmd'), ('Floor avg °C', f'Zone_F{fl:02d}_AvgTemp'),
                                      ('Return CO2', f'{u}_RA_CO2')], rh=21)
        x = 250; n = len(zs); w = min(270, (1904 - 250) // max(n, 1) - 4)
        for c in zs:
            p.rect(x, y + 24, w, 82, fill='#171c22', stroke=EDGE, pen=1.0)
            lbl(p, x + 4, y + 26, w - 8, f'Zone {c}', 9, 'white', True, h=16)
            small = w < 200
            val(p, x + 4, y + 44, w - 8, f'ZoneTemperatureAvg_{c}', f'zone {c} temp', h=20, size=11)
            val(p, x + 4, y + 64, (w - 12) // 2, f'ZoneHumidityAvg_{c}', f'zone {c} RH', h=18, size=9)
            val(p, x + 8 + (w - 12) // 2, y + 64, (w - 12) // 2, f'ZoneCO2_{c}', f'zone {c} CO2', h=18, size=9)
            if not small: lbl(p, x + 4, y + 84, w - 8, '°C  ·  %RH  ·  CO2 ppm', 8, LBL, h=16)
            x += w + 4
        y += 120
    return p


if __name__ == '__main__':
    bog, P7.KITDIR, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    P7.PATH.update(P7.load_paths(bog))
    G.FOLDER = {n: q.rsplit('/', 1)[0].replace('/ChillerPlant/', '').replace('/ChillerPlant', '') for n, q in P7.PATH.items()}
    G.STATION_NAME = 'ALT_CP_Ref_V7_9'
    zones = sorted(n[len('ZoneTemperatureAvg_'):] for n in P7.PATH if n.startswith('ZoneTemperatureAvg_') and len(n) == len('ZoneTemperatureAvg_01_0101'))
    os.makedirs(os.path.join(outdir, 'px'), exist_ok=True)
    bad = []
    import gen_px79s
    for p in (gen_px79s.schematic(header), plant79(), building79(zones)):
        x = p.xml()
        import xml.etree.ElementTree as ET; ET.fromstring(x.encode('utf-8'))
        open(os.path.join(outdir, 'px', p.name + '.px'), 'w', encoding='utf-8').write(x)
        bad += [(p.name, pt) for pt, o, w, m in p.map if pt != '(BQL)' and pt not in P7.PATH]
        print(p.name, len(p.el), 'elements', len(p.map), 'bindings')
    print('missing', bad[:30])
