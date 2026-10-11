# -*- coding: utf-8 -*-
"""V7.9 chiller plant schematic (V7.8 style: kitPx pictures + piping) with 6 slots per type, same equipment as the 3D twin.
Roof: CT-01..06 between the CDWR / CDWS headers.  Floor 1: one row per slot: CDP -> chiller -> CHP, headered pools."""
import gen_px7 as P7
import gen_px as G
from gen_px7 import val, lbl, panel, rows, pic, pic_bool, kpi_strip, status_led, Pipes, EDGE, LBL, RUN, OFF, FLT, WARN, TXT

N = 6
Y0, RH = 340, 150                     # first chiller row top, row pitch
CHX = 600                             # chiller picture x
GOOD = '#1f6f43'
CT_ON = 'CoolingTowers/PushThru/CoolingTower_PushThru_Left/CoolingTower_PushThru_Left_On.gif'
CT_OFF = 'CoolingTowers/PushThru/CoolingTower_PushThru_Left/CoolingTower_PushThru_Left_Off.png'


def has(pt): return pt in P7.PATH


def first(*pts):
    return next((q for q in pts if has(q)), pts[0])


def v(p, x, y, w, pt, what, **kw):
    if has(pt): val(p, x, y, w, pt, what, **kw)
    else: lbl(p, x, y, w, '—', 9, '#566573', h=kw.get('h', 20))


def pts(kind, i):
    """slot -> point names (slots 01-02 are the V7.8 base equipment, 03-06 the expansion slots)."""
    u = f'{kind}{i:02d}'
    if kind == 'CH':
        return dict(run=first(f'{u}RunProof', f'{u}RunProofSelected'), load=f'{u}LoadPct', lwt=f'{u}_ChwSupplyTemp', kw=f'{u}_kW',
                    flow=first(f'{u}_ChwFlow', f'{u}_ChwFlowSw'), chwv=f'Gfx_{u}_ChwIso_Pos', cdwv=f'Gfx_{u}_CdwIso_Pos',
                    inst=f'{u}_Installed', flt=f'{u}Fault')
    if kind == 'CT':
        return dict(run=first(f'{u}_01RunProof', f'{u}RunProof'), spd=first(f'{u}_01SpeedCmd', f'{u}SpeedCmd'),
                    vlv=first(f'Gfx_{u}_InletMV_Pos', f'Gfx_{u}_Valve_Pos'), inst=f'{u}_Installed', flt=f'{u}Fault')
    return dict(run=f'{u}RunProof', spd=f'{u}SpeedCmd', vlv=first(f'Gfx_{u}_DischargeMV_Pos', f'Gfx_{u}_MV_Pos'), kw=f'{u}_kW',
                inst=f'{u}_Installed', flt=f'{u}Fault')


def pic_scaled(p, x, y, point, on, off, what, s):
    from xml.sax.saxutils import quoteattr
    iw, ih = P7.img_size(off); o = p.ord(point); KG = P7.KG
    p.el.append(f'<Picture layout="{x:.1f},{y:.1f},{iw * s:.1f},{ih * s:.1f}" image="{KG}/{off}" scaleFactor="1.0">\n'
                f'  <ValueBinding ord={quoteattr(o)}>\n    <IBooleanToSimple name="image">\n'
                f'      <Image name="trueValue" value="{KG}/{on}"/>\n      <Image name="falseValue" value="{KG}/{off}"/>\n'
                f'    </IBooleanToSimple>\n  </ValueBinding>\n</Picture>')
    p.map.append((point, o, what, 'display (image on/off)'))


def inst_led(p, x, y, pt, title):
    if has(pt): status_led(p, x, y, pt, f'{title} installed', 'run')
    lbl(p, x + 16, y - 2, 56, 'Installed', 8, 'white', h=16)


def unit_panel(p, x, y, w, title, d):
    panel(p, x, y, w, 134, title)
    inst_led(p, x + w - 76, y + 3, d['inst'], title)
    it = [('Status', d['run'], {'bool_c': (RUN, OFF)}), ('Speed %', d['spd']), ('Valve %', d['vlv']), ('Fault', d['flt'], {'bool_c': (FLT, GOOD)})]
    for k, (t, pt, *kw) in enumerate(it):
        lbl(p, x + 4, y + 24 + k * 26, 70, t, 9)
        v(p, x + 76, y + 25 + k * 26, w - 82, pt, f'{title} {t}', h=20, size=9, **(kw[0] if kw else {}))


def schematic(header):
    p = G.Page('ALT_V79_Plant', 'Chiller plant schematic · 6 slots per type (same as 3D)', (1920, 1290)); header(p)
    kpi_strip(p, y=76)
    rowy = [Y0 + i * RH for i in range(N)]
    TX = [170 + j * 140 for j in range(N)]                  # tower picture x (roof)
    S_CT = .6
    P_ = Pipes()
    # ---------------- condenser water
    P_.add('cwr', [(TX[0] + 26, 140), (TX[-1] + 26, 140)])                 # CDWR header on the roof
    for tx in TX: P_.add('cwr', [(tx + 26, 140), (tx + 26, 172)])
    P_.add('cwr', [(540, 140), (540, rowy[-1] + 40)])                       # CDWR riser
    P_.add('cws', [(TX[0] + 70, 290), (TX[-1] + 70, 290)])                 # CDWS header (tower basins)
    for tx in TX: P_.add('cws', [(tx + 70, 250), (tx + 70, 290)])
    P_.add('cws', [(300, 290), (300, rowy[-1] + 115)])                      # CDP suction header
    P_.add('cws', [(480, rowy[0] + 90), (480, rowy[-1] + 90)])              # CDP discharge header
    for y in rowy:
        P_.add('cws', [(300, y + 115), (345, y + 115)])
        P_.add('cws', [(435, y + 90), (CHX + 20, y + 90)])
        P_.add('cwr', [(CHX + 20, y + 40), (540, y + 40)])
    # ---------------- chilled water
    BOT = rowy[-1] + 140
    P_.add('chws', [(1000, rowy[-1] + 40), (1000, 316), (1480, 316)])        # CHWS riser + header to building
    P_.add('chwr', [(960, rowy[0] + 90), (960, rowy[-1] + 90)])             # CHP discharge header
    P_.add('chwr', [(1480, BOT), (1200, BOT), (1200, rowy[0] + 115)])       # CHWR header from building
    P_.add('chwr', [(1460, 316), (1460, BOT)])                              # min-flow bypass
    for y in rowy:
        P_.add('chws', [(CHX + 180, y + 40), (1000, y + 40)])
        P_.add('chwr', [(1070, y + 90), (CHX + 180, y + 90)])
        P_.add('chwr', [(1165, y + 115), (1200, y + 115)])
    P_.render(p)

    # ---------------- roof: cooling towers
    p.rect(150, 128, 840, 200, fill=None, stroke='#37474f', pen=1.0)
    lbl(p, 156, 300, 200, 'ROOF · COOLING TOWERS', 8, LBL, True)
    for j, tx in enumerate(TX):
        d = pts('CT', j + 1)
        pic_scaled(p, tx, 172, d['run'], CT_ON, CT_OFF, f'CT{j + 1:02d} fan image', S_CT)
        lbl(p, tx, 152 + 30, 50, f'CT-{j + 1:02d}', 8, 'white', True, h=14, bg='#263238')
        if has(d['flt']): status_led(p, tx + 82, 176, d['flt'], f'CT{j + 1:02d} fault', 'alarm')
    lbl(p, 160, 270, 76, 'CDWS °C', 8); v(p, 160, 252, 70, 'CDS', 'CDW supply temp', h=18, size=9)
    lbl(p, 624, 318, 60, 'CDWR °C', 8); v(p, 550, 318, 70, 'CDR', 'CDW return temp', h=18, size=9)
    lbl(p, 1010, 128, 300, 'FLOOR 1 · PLANT ROOM', 9, LBL, True)

    # ---------------- floor 1 rows
    for i, y in enumerate(rowy):
        n = i + 1
        cdp, ch, chp = pts('CDP', n), pts('CH', n), pts('CHP', n)
        p.rect(4, y + 2, 1452, RH - 6, fill=None, stroke='#222b33', pen=1.0)
        unit_panel(p, 10, y + 6, 270, f'CDP-{n:02d}', cdp)
        pic_bool(p, 330, y + 60, cdp['run'], 'Pumps/Pumps_Base/Pump_Base_Right/Pump_Base_Right_On.gif',
                 'Pumps/Pumps_Base/Pump_Base_Right/Pump_Base_Right_Off.png', f'CDP{n:02d} image')
        pic_bool(p, CHX, y, ch['run'], 'Chillers/Turbo/Chiller_Turbo_Left/Chiller_Turbo_Left_On.gif',
                 'Chillers/Turbo/Chiller_Turbo_Left/Chiller_Turbo_Left_Off.png', f'Chiller {n:02d} image')
        lbl(p, CHX + 4, y + 2, 60, f'CH-{n:02d}', 10, 'white', True, h=18, bg='#263238')
        p.rect(CHX + 104, y + 2, 76, 18, fill='#263238', stroke='#263238', pen=1.0); inst_led(p, CHX + 106, y + 3, ch['inst'], f'CH{n:02d}')
        if has(ch['flt']): status_led(p, CHX + 66, y + 4, ch['flt'], f'CH{n:02d} fault', 'alarm')
        pic(p, 556, y + 20, 'Valves/valve_2way_elec_top.png'); v(p, 548, y + 60, 50, ch['cdwv'], f'CH{n:02d} CDW valve %', h=16, size=8)
        pic(p, 900, y + 20, 'Valves/valve_2way_elec_top.png')
        # chiller values (between the evaporator pipes and under the picture)
        lbl(p, 790, y + 58, 40, 'Load', 8); v(p, 826, y + 58, 52, ch['load'], f'CH{n:02d} load %', h=16, size=8)
        lbl(p, 882, y + 58, 30, 'LWT', 8); v(p, 906, y + 58, 48, ch['lwt'], f'CH{n:02d} leaving CHW', h=16, size=8)
        lbl(p, CHX, y + 124, 40, 'kW', 8); v(p, CHX + 26, y + 124, 58, ch['kw'], f'CH{n:02d} kW', h=18, size=8)
        lbl(p, CHX + 90, y + 124, 40, 'CHW%', 8); v(p, CHX + 132, y + 124, 48, ch['chwv'], f'CH{n:02d} CHW valve %', h=18, size=8)
        pic_bool(p, 1060, y + 60, chp['run'], 'Pumps/Pumps_Base/Pump_Base_Left/Pump_Base_Left_On.gif',
                 'Pumps/Pumps_Base/Pump_Base_Left/Pump_Base_Left_Off.png', f'CHP{n:02d} image')
        unit_panel(p, 1222, y + 6, 222, f'CHP-{n:02d}', chp)
        if n >= 3: lbl(p, 290, y + 132, 120, 'expansion slot', 7, '#78909c')

    # ---------------- CHW instruments, bypass, building
    lbl(p, 1030, 282, 60, 'CHWS °C', 8); v(p, 1090, 282, 62, 'CHWS', 'CHWS header temp', h=18, size=9)
    lbl(p, 1160, 282, 60, 'dP kPa', 8); v(p, 1210, 282, 62, 'CHWDP', 'CHW differential pressure', h=18, size=9)
    lbl(p, 1220, BOT + 18, 60, 'CHWR °C', 8); v(p, 1280, BOT + 18, 62, 'CHWR', 'CHWR header temp', h=18, size=9)
    lbl(p, 1350, BOT + 18, 50, 'Flow', 8); v(p, 1384, BOT + 18, 70, 'CHWFlow', 'CHW flow', h=18, size=9)
    p.rect(1482, 300, 136, BOT - 270, fill='#1b2631', stroke='#5d6d7e', pen=2.0)
    p.label(1482, 310, 136, 40, 'BUILDING ⊞', 13, True, TXT, None, 'center', popup='file:^px/ALT_V79_Building.px', ptitle='Building / zones')
    lbl(p, 1486, 350, 128, 'Floors 2-8 AHU + zones', 8, LBL, halign='center')
    p.label(1486, 380, 128, 26, '3D DIGITAL TWIN', 9, True, 'white', '#1e88e5', 'center', popup='file:^px/ALT_V79_Building3D.px', ptitle='3D Live')

    pic(p, 1445, 760, 'Valves/valve_2way_elec_left.png'); lbl(p, 1490, 760, 120, 'MIN-FLOW BYPASS %', 8, TXT, True)
    v(p, 1490, 780, 80, first('CHW_BypassValveCmd', 'Gfx_CHW_BypassMV_Pos'), 'Bypass valve', h=18, size=9)
    # ---------------- right column
    X, W = 1628, 284
    panel(p, X, 128, W, 236, 'EXPANSION SUPERVISOR')
    rows(p, X + 2, 152, W - 4, [('Expansion in use', 'CHX_Enable', {'bool_c': (RUN, OFF)}), ('Chillers wanted 03-06', 'CHX_TargetNum'),
                               ('Added for load', 'CHX_StageAdd'), ('Average load %', 'CHX_AverageLoad'),
                               ('Chillers needing water', 'CHX_ChillersNeedingWater'), ('Running chillers', 'CHX_TotalRun'),
                               ('Add chiller above %', 'CHX_UpLoadPct', {'action': True}), ('Remove below %', 'CHX_DownLoadPct', {'action': True})], rh=26)
    panel(p, X, 374, W, 196, 'COOLING TOWERS (roof)')
    for k, t in enumerate(('Inst', 'Run', 'Fan %', 'Valve %', 'Fault')):
        lbl(p, X + 50 + k * 46, 396, 46, t, 8, LBL, halign='center')
    for j in range(N):
        d = pts('CT', j + 1); yy = 414 + j * 25
        lbl(p, X + 4, yy, 46, f'CT-{j + 1:02d}', 9, TXT, True)
        for k, (pt, t) in enumerate(((d['inst'], 'installed'), (d['run'], 'running'), (d['spd'], 'fan %'), (d['vlv'], 'valve %'), (d['flt'], 'fault'))):
            if k in (2, 3): v(p, X + 50 + k * 46, yy + 1, 44, pt, f'CT{j + 1:02d} {t}', h=20, size=8)
            elif has(pt): status_led(p, X + 66 + k * 46, yy + 4, pt, f'CT{j + 1:02d} {t}', 'alarm' if k == 4 else 'run')
    panel(p, X, 580, W, 236, 'PLANT')
    rows(p, X + 2, 604, W - 4, [('CHW flow', 'CHWFlow'), ('CDW flow', 'CDW_Flow'), ('CDS °C', 'CDS'), ('CDR °C', 'CDR'),
                               ('Plant kW', 'Plant_kW'), ('kW/RT', 'Plant_kW_per_RT'), ('Load RT', 'CoolingLoad_RT'), ('Stage', 'PlantStage')], rh=26)
    panel(p, X, 826, W, 150, 'HOW TO READ')
    lbl(p, X + 6, 850, W - 12, 'Moving picture = running. Grey = stopped.  Inst = slot installed (counted by logic). '
        'Slots 03-06 are the expansion slots; set <slot>_Installed or use the equipment register.  '
        'Pumps and towers are headered: any unit serves any chiller.', 9, LBL, h=120)
    lbl(p, X, 1260, W, 'kitPxGraphics images', 8, '#566573')
    return p
