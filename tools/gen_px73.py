"""V7.3 Px graphics for ALT_CP_Ref_V7_3 (extends gen_px71 / gen_px7 / gen_px, which stay unchanged).

 * Plant (2-D schematic): towers = 2 fan cells each (CT-01/01 ... CT-02/02) drawn from the V7.3 Blender assets (animated fans
   when running), butterfly motorised valves (red actuator = on/off, green = modulating, handwheel = manual), electromagnetic
   flow / BTU meters, CHW min-flow bypass (MOD valve + isolation valves + manual bypass loop, no bypass flow meter), make-up
   water to every basin + CHW loop fill (RPZ / meter / solenoid), bypass (pot) chemical feeder, CDW dosing + bleed-off,
   outdoor-air table and the plant kW/ton dial gauge (kitPx AnalogMeter over an ASHRAE-banded face).
 * New pages: Chiller Plant (3-D), CT Plant (3-D, SOO staging panel, cells + VSD per cell), Zones (floor plan for
   AETERLINK Sense-T / AirPlug T + RH, live temperature colour per room).  Plant 3D re-rendered with the same model.
 * Faceplates: tower (basin, valves, cells), one per fan cell (VSD, min / max, faults, RESET, service), updated drives /
   valves / meters pages.
usage: gen_px73.py v73.bog kit/kitPxGraphics-wb outdir regdir spritedir
"""
import sys, os, re, csv, json, shutil, inspect
from xml.sax.saxutils import quoteattr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_px71 as G71
import gen_px7 as G7
import gen_px as G
from gen_px7 import pic, pic_bool, val, lbl, panel, rows, status_led, BG, PANEL, EDGE, LBL, VAL, TXT, RUN, OFF, FLT, WARN
from gen_px71 import ximg, hot, tag, isa, tt_top, tt_bot, pt_top, hdr_text, pct_tag, kwrt_val, card, fp, drive_rows, OKC, KWRT_MAP, ASHRAE
import pipes71
import gauge73

STATION = 'ALT_CP_Ref_V7_3'
G71.STATION = STATION
pipes71.COL.update({'mu': (60, 190, 100), 'chem': (170, 110, 230), 'drain': (150, 150, 150)})
PAGES = [('ALT_V7_Plant', 'Plant'), ('ALT_V73_ChillerPlant', 'Chiller Plant'), ('ALT_V73_CTPlant', 'CT Plant'), ('ALT_V71_Plant3D', 'Plant 3D'),
         ('ALT_V71_Chillers', 'Chillers'), ('ALT_V7_PlantDetail', 'Pools'), ('ALT_V71_Drives', 'Drives'), ('ALT_V71_Valves', 'Valves'),
         ('ALT_V71_Meters', 'Meters'), ('ALT_V71_Schedules', 'Schedules'), ('ALT_CP_Optimization', 'Optimise'), ('ALT_CP_EnergyDashboard', 'Energy'),
         ('ALT_CP_Energy', 'KPI'), ('ALT_CP_AlarmsHistory', 'Alarms'), ('ALT_CP_Simulation', 'Sim'),
         ('ALT_V7_AirSide', 'Air Side'), ('ALT_V73_Zones', 'Zones'), ('ALT_V7_AHU01', 'AHU-01'), ('ALT_V7_AHU02', 'AHU-02'), ('ALT_V7_OAU01', 'OAU-01'),
         ('ALT_V7_FCU', 'FCU'), ('ALT_V7_Ventilation', 'Ventilation')]
AIRPAGES = {'ALT_V7_AirSide', 'ALT_V73_Zones', 'ALT_V7_AHU01', 'ALT_V7_AHU02', 'ALT_V7_OAU01', 'ALT_V7_FCU', 'ALT_V7_Ventilation'}
G71.PAGES = PAGES
CELLS = [('CT01', 'CT01_01'), ('CT01', 'CT01_02'), ('CT02', 'CT02_01'), ('CT02', 'CT02_02')]
CN = {c: f'CT-{c[2:4]}/{c[5:]}' for _, c in CELLS}
SPR = {}                     # sprite json
OUT = None
C_MU, C_CHEM = '#3cbe64', '#aa6ee6'


# ================================================================ header (V7.3)
def header(self):
    W, H = self.size
    self.rect(0, 0, W, H, fill=BG, stroke=BG, pen=1.0)
    if self.name.startswith(('ALT_V71_FP_', 'ALT_V73_FP_')):
        self.label(0, 0, W, 34, f'  {self.title}', 14, True, 'white', '#0b0e11')
        return
    self.label(0, 0, W, 40, f'  ALT Reference V7.3 — {self.title}', 18, True, 'white', '#0b0e11')
    self.label(W - 470, 8, 460, 24, 'REFERENCE SIMULATION – NOT PROJECT APPROVED', 10, True, '#263238', '#ffca28', 'center')
    n = len(PAGES); bw = (W - 8) / n
    for i, (name, title) in enumerate(PAGES):
        cur = name == self.name
        self.label(4 + i * bw, 44, bw - 3, 26, title, 8.5, True, 'white' if cur else '#cfd8dc',
                   '#1e88e5' if cur else ('#233a33' if name in AIRPAGES else '#2c3440'), 'center',
                   popup=None if cur else f'file:^px/{name}.px', ptitle=title)


G.Page.header = header


# ================================================================ helpers
def own(name):
    if name not in G71.IMG: G71.IMG.append(name)
    return f'file:^px/img/{name}'


def ximg_bool(p, x, y, w, h, point, on, off, what, popup=None, ptitle=''):
    o = p.ord(point)
    pop = f'\n  <PopupBinding ord={quoteattr(popup)} title={quoteattr(ptitle)}/>' if popup else ''
    tagn = 'Label' if popup else 'Picture'
    p.el.append(f'<{tagn} layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" image="{own(off)}">\n'
                f'  <ValueBinding ord={quoteattr(o)}>\n    <IBooleanToSimple name="image">\n'
                f'      <Image name="trueValue" value="{own(on)}"/>\n      <Image name="falseValue" value="{own(off)}"/>\n'
                f'    </IBooleanToSimple>\n  </ValueBinding>{pop}\n</{tagn}>')
    p.map.append((point, o, what, 'display (image on/off)'))


def sprite(p, name, ax, ay, anchor='c', ext='.png', popup=None, ptitle=''):
    """place sprite <name> so that its anchor pixel lands on (ax, ay); returns (x, y, w, h)"""
    s = SPR[name]; w, h = s['size']; a = s['anchors'][anchor]
    x, y = ax - a[0], ay - a[1]
    ximg(p, x, y, name + ext, w, h, popup=popup, ptitle=ptitle)
    return x, y, w, h


def bfv(p, cx, cy, orient='h', mode='onoff', led=None, pct=None, what='', pct_at=None, led_at=None):
    """butterfly valve sprite centred on the pipe (cx, cy) + optional open LED / % tag"""
    x, y, w, h = sprite(p, f'v73_bfv_{mode}_{orient}', cx, cy)
    if led:
        lx, ly = led_at or ((x + w - 6, y + 2) if orient == 'h' else (x + w - 12, y + h - 6))
        status_led(p, lx, ly, led, what or f'{led} open', 'run')
    if pct:
        px_, py_ = pct_at or ((x + w + 2, y + 4) if orient == 'h' else (x + w + 2, y + h / 2 - 8))
        pct_tag(p, px_, py_, pct, what or pct)


def gauge(p, x, y, S, point='Plant_kW_per_RT', what='Plant kW/RT gauge'):
    """dial: ASHRAE face image + kitPx AnalogMeter (needle + ticks) laid exactly over it"""
    name = f'v73_gauge_{S}.png'
    path = os.path.join(OUT, 'px', 'img', name)
    if not os.path.exists(path): gauge73.face(path, S)
    ximg(p, x, y, name, S, S)
    o = p.ord(point)
    p.el.append(f'<AnalogMeter layout="{x:.1f},{y:.1f},{S:.1f},{S:.1f}" min="0.4" max="1.4" startAngle="225" arcAngle="270" numDivisions="10" '
                f'numSubDivisions="2" showSubDivisions="true" scaleVisible="false" valueVisible="false" fillCircle="false" '
                f'foreground="#c9d3dd" background="rgba(0,0,0,0.0)" needleBrush="#ffffff" needlePen="3.0">\n'
                f'  <ValueBinding ord={quoteattr(o)}>\n    <INumericToNumber name="value"/>\n'
                f'  </ValueBinding>\n</AnalogMeter>')
    p.map.append((point, o, what, 'display (dial gauge)'))


def gauge_panel(p, x, y, w, h, point='Plant_kW_per_RT', title='PLANT kW/RT — ASHRAE'):
    panel(p, x, y, w, h, title)
    S = min(h - 26, 200)
    gauge(p, x + 6, y + 23, S, point)
    vx = x + S + 16; vw = w - S - 24
    val(p, vx, y + 30, vw, point, 'Plant kW/RT (ASHRAE colour)', h=40, size=17, fg='white', fmt='%out.value%')
    p.el[-1] = p.el[-1].replace('<ObjectToString', f'<INumericToSimple name="background" map="{KWRT_MAP}"/>\n    <ObjectToString')
    names = ('EXCELLENT  < 0.75', 'GOOD  0.75–0.90', 'FAIR  0.90–1.00', 'NEEDS IMPROV.  > 1.00')
    rh = min(22, (h - 84) / 4)
    for i, (lo, hi, c, _) in enumerate(ASHRAE[1:]):
        yy = y + 78 + i * rh
        p.rect(vx, yy + 3, 14, rh - 6, fill=c, stroke=c, pen=1.0)
        lbl(p, vx + 18, yy, vw - 18, names[i], 8, '#c9d3dd', h=rh)


def leader(p, ax, ay, bx, by, col='#8fd3ff'):
    p.line([(ax, ay), (bx, by)], col, 1.0)
    p.rect(ax - 3, ay - 3, 6, 6, fill=col, stroke='#0b0e11', pen=1.0)


def oa_rows(p, x, y, w, rh=22, lw=None):
    rows(p, x, y, w, [('Dry bulb', 'OA_Temperature'), ('Relative humidity', 'OA_Humidity'), ('Wet bulb (calc)', 'OA_WetBulb'),
                      ('Dew point (calc)', 'OA_DewPoint'), ('Enthalpy (calc)', 'OA_Enthalpy'), ('Sensor valid', 'OA_Valid', {'bool_c': (RUN, FLT)})],
         lw=lw or int(w * 0.55), rh=rh)


# ================================================================ Plant (2-D schematic)
PW, PH = 2100, 1180
CHP = {'01': (500, 440), '02': (500, 720)}
CH = {'01': (830, 450), '02': (830, 720)}
CDP = {'01': (1220, 560), '02': (1220, 830)}
X_BLD, X_DPT, X_BYP, X_BYL, Y_CHWS, Y_CHWR = 100, 106, 158, 128, 196, 950
X_SUC, X_DIS, X_RIS = 430, 680, 740
X_CDR, X_CDS, X_CDSUC, Y_CDR, Y_CDWS = 1120, 1180, 1420, 140, 364
TWX = {'01': 1500, '02': 1800}; TWY = 150
CT_DROP = {'01': 1470, '02': 1775}
X_CT2OUT = 1745
Y_MU = 972; X_MUR = 2092; Y_MUH = 349
HW, EXT = 16, 30
C_CHWS, C_CHWR, C_CDWS, C_CDWR = G71.C_CHWS, G71.C_CHWR, G71.C_CDWS, G71.C_CDWR
TANK_X = 385; X_FILL = 444
POT = (600, 836); DOS = (1010, 132)


def ct_anchor(n, k):
    a = SPR['v73_ct2_off']['anchors'][k]
    return TWX[n] + a[0], TWY + a[1]


def plant_pipes(name):
    L = pipes71.Layer(PW, PH)
    ev = lambda n, k: (CH[n][0] + 4, CH[n][1] + k)
    cd = lambda n, k: (CH[n][0] + 198, CH[n][1] + k)
    capv = lambda x, y: ((x, y), False)
    caph = lambda x, y: ((x, y), True)
    y_ch2i, y_ch2o, y_ch1i = CH['02'][1] + 55, CH['02'][1] + 45, CH['01'][1] + 55
    # ---------- CHW: bypass (MOD + isolation + manual loop), DPT
    L.pipe([(X_BYP, Y_CHWR), (X_BYP, Y_CHWS)], 'chwr', flow=False)
    L.pipe([(X_BYP, 560), (X_BYL, 560), (X_BYL, 720), (X_BYP, 720)], 'chwr', w=6, flow=False)
    L.pipe([(X_DPT, Y_CHWS), (X_DPT, Y_CHWR)], (150, 150, 150), w=2, flow=False)
    L.pipe([(TANK_X, Y_CHWR), (TANK_X, Y_CHWR - 10)], 'chwr', flow=False)
    for n, (x, y) in CHP.items():
        L.pipe([(X_SUC, y + 44.5), (x + 12, y + 44.5)], 'chwr', flanges=[((x + 10, y + 44.5), True)], arrows_every=60)
        L.pipe([(x + 24, y + 12), (x + 24, y - 40), (X_DIS, y - 40)], 'chwr', flanges=[((x + 24, y + 10), False)], arrows_every=90)
    for n, (x, y) in CH.items():
        L.pipe([ev(n, 45), (X_RIS, y + 45)], 'chws', flanges=[((x + 6, y + 45), True)], arrows_every=60)
    L.pipe([(X_RIS, y_ch2o + 12), (X_RIS, Y_CHWS)], 'chws', w=HW, flow=False, flanges=[capv(X_RIS, y_ch2o + 12)])
    for n, (x, y) in CH.items():
        L.shadow(X_DIS, y + 50, x, y + 60)
        L.pipe([(X_DIS, y + 55), ev(n, 55)], 'chwr', flanges=[((x + 6, y + 55), True)], arrows_every=80)
    L.pipe([(X_DIS, CHP['01'][1] - 40 - EXT), (X_DIS, y_ch2i + EXT)], 'chwr', w=HW, flow=False,
           flanges=[capv(X_DIS, CHP['01'][1] - 40 - EXT), capv(X_DIS, y_ch2i + EXT)])
    L.pipe([(X_SUC, CHP['01'][1] + 44.5 - EXT), (X_SUC, Y_CHWR)], 'chwr', w=HW, flow=False, flanges=[capv(X_SUC, CHP['01'][1] + 44.5 - EXT)])
    L.pipe([(X_BLD, Y_CHWS), (X_RIS + EXT, Y_CHWS)], 'chws', w=HW, flow=False, flanges=[caph(X_RIS + EXT, Y_CHWS)])
    L.pipe([(X_BLD, Y_CHWR), (X_SUC + EXT, Y_CHWR)], 'chwr', w=HW, flow=False, flanges=[caph(X_SUC + EXT, Y_CHWR)])
    # chemical pot feeder across the CHP headers (discharge -> feeder -> suction)
    pf = SPR['v73_potfeeder']['anchors']; PFX, PFY = POT
    L.pipe([(X_DIS, 800), (PFX + pf['in'][0] + 6, 800), (PFX + pf['in'][0] + 6, PFY + pf['in'][1])], 'chem', w=4, flow=False)
    L.pipe([(PFX + pf['out'][0], PFY + pf['out'][1]), (PFX + pf['out'][0], 918), (X_SUC, 918)], 'chem', w=4, flow=False)
    for a, d in (((X_BLD + 30, Y_CHWS), (-1, 0)), ((X_BLD + 30, Y_CHWR), (1, 0)), ((X_SUC, 880), (0, -1)), ((X_RIS, 330), (0, -1)), ((X_DIS, 620), (0, 1))):
        L.arrow(a, d, 9)
    # ---------- CDW
    for n, (x, y) in CH.items():
        L.pipe([cd(n, 45), (X_CDR, y + 45)], 'cdwr', flanges=[((x + 196, y + 45), True)], arrows_every=60)
    L.pipe([(X_CDR, y_ch2o + 12), (X_CDR, Y_CDR)], 'cdwr', w=HW, flow=False, flanges=[capv(X_CDR, y_ch2o + 12)])
    for n in TWX:
        ix, iy = ct_anchor(n, 'inlet')
        L.pipe([(CT_DROP[n], Y_CDR), (CT_DROP[n], iy), (ix + 4, iy)], 'cdwr', arrows_every=50)
    L.pipe([(X_CDR - EXT, Y_CDR), (CT_DROP['02'] + EXT, Y_CDR)], 'cdwr', w=HW, flow=False,
           flanges=[caph(X_CDR - EXT, Y_CDR), caph(CT_DROP['02'] + EXT, Y_CDR)])
    o1 = ct_anchor('01', 'outlet'); o2 = ct_anchor('02', 'outlet')
    L.pipe([(o1[0] + 4, o1[1]), (X_CDSUC, o1[1])], 'cdws', arrows_every=40)
    L.pipe([(o2[0] + 4, o2[1]), (X_CT2OUT, o2[1]), (X_CT2OUT, Y_CDWS)], 'cdws', arrows_every=40)
    for n, (x, y) in CDP.items():
        L.pipe([(X_CDSUC, y + 44.5), (x + 98, y + 44.5)], 'cdws', flanges=[((x + 100, y + 44.5), True)], arrows_every=50)
        L.pipe([(x + 85, y + 12), (x + 85, y - 20), (X_CDS, y - 20)], 'cdws', flanges=[((x + 85, y + 10), False)], arrows_every=80)
    for n, (x, y) in CH.items():
        L.shadow(x + 198, y + 50, X_CDS, y + 60)
        L.pipe([(X_CDS, y + 55), cd(n, 55)], 'cdws', flanges=[((x + 196, y + 55), True)], arrows_every=80)
    L.pipe([(X_CDS, y_ch1i - EXT), (X_CDS, CDP['02'][1] - 20 + EXT)], 'cdws', w=HW, flow=False,
           flanges=[capv(X_CDS, y_ch1i - EXT), capv(X_CDS, CDP['02'][1] - 20 + EXT)])
    L.pipe([(X_CDSUC, o1[1] - EXT), (X_CDSUC, CDP['02'][1] + 44.5 + EXT)], 'cdws', w=HW, flow=False,
           flanges=[capv(X_CDSUC, o1[1] - EXT), capv(X_CDSUC, CDP['02'][1] + 44.5 + EXT)])
    L.pipe([(X_CDSUC, Y_CDWS), (X_CT2OUT + EXT, Y_CDWS)], 'cdws', w=HW, flow=False, flanges=[caph(X_CT2OUT + EXT, Y_CDWS)])
    # bleed-off (CDWR riser -> solenoid -> drain) and dosing (skid -> CDWR riser)
    L.pipe([(X_CDR, 262), (1178, 262), (1178, 300)], 'drain', w=5, flow=False)
    ds = SPR['v73_dosing']['anchors']['out']
    L.pipe([(DOS[0] + ds[0], DOS[1] + ds[1]), (DOS[0] + ds[0], 190), (X_CDR, 190)], 'chem', w=4, flow=False)
    # ---------- make-up water: source (right) -> CHW fill (bottom, left) and riser -> basin header -> each basin
    L.pipe([(X_MUR, Y_MU), (X_FILL, Y_MU), (X_FILL, Y_CHWR + 6)], 'mu', w=6, flow=False)
    L.pipe([(X_MUR, Y_MU), (X_MUR, Y_MUH), (ct_anchor('01', 'makeup')[0] - 2, Y_MUH)], 'mu', w=6, flow=False)
    for n in TWX:
        mx, my = ct_anchor(n, 'makeup')
        L.pipe([(mx + 8, Y_MUH), (mx + 8, my), (mx - 2, my)], 'mu', w=5, flow=False)
    for a, d in (((X_CDR, 330), (0, -1)), ((1300, Y_CDR), (1, 0)), ((1600, Y_CDWS), (-1, 0)), ((X_CDSUC, 700), (0, 1)), ((X_CDS, 690), (0, -1)),
                 ((1500, Y_MU), (-1, 0)), ((X_MUR, 700), (0, -1))):
        L.arrow(a, d, 9)
    L.render(os.path.join(OUT, 'px', 'img', name))
    if name not in G71.IMG: G71.IMG.append(name)


def plant_page():
    p = G.Page('ALT_V7_Plant', 'Plant (schematic)', (PW, PH)); p.header()
    plant_pipes('v73_plant_pipes.png')
    ximg(p, 0, 0, 'v73_plant_pipes.png', PW, PH, bottom=True)
    G7.kpi_strip(p)
    hot(p, 8 + 116 * 10, 80, 224, 48, 'ALT_V71_FP_OA', 'Outdoor air sensor')
    # ================= building + CHW side
    p.rect(16, 176, X_BLD - 20, 790, fill='#18212b', stroke='#5d6d7e', pen=2.0)
    p.label(16, 186, X_BLD - 20, 22, 'BUILDING', 10, True, TXT, None, 'center')
    p.label(20, 210, X_BLD - 28, 20, 'Air side ⊞', 9, True, '#8fd3ff', '#1f2a36', 'center', popup='file:^px/ALT_V7_AirSide.px', ptitle='Air side')
    p.label(20, 232, X_BLD - 28, 20, 'Zones ⊞', 9, True, '#8fd3ff', '#1f2a36', 'center', popup='file:^px/ALT_V73_Zones.px', ptitle='Zones')
    for i, (t, pt, kw) in enumerate((('Cooling calls', 'AirSide_CoolingCalls', {}), ('CHW requests', 'AirSide_ChwRequests', {}),
                                      ('Units running', 'AirSide_UnitsRunning', {}), ('Reset %', 'PlantResetPct', {}),
                                      ('Fire alarm', 'FireModeActive', {'bool_c': (FLT, OKC)}), ('CHW ΔP', 'CHWDP', {}), ('ΔP SP', 'CHWDP_Setpoint_ACTIVE', {}),
                                      ('Zone avg AHU1', 'Zone_AHU01_AvgTemp', {}))):
        lbl(p, 20, 262 + i * 44, 76, t, 8, '#c9d3dd')
        val(p, 20, 280 + i * 44, 72, pt, f'Building {t}', h=20, size=9, **kw)
    # CHWS header instruments: BTU meter (flow + calculator), TT, PT
    bx, by, bw_, bh_ = sprite(p, 'v73_btu_h', 262, Y_CHWS, popup='file:^px/ALT_V71_FP_BTU.px', ptitle='BTU meter')
    tag(p, 336, 150, 92, 'BTU_Power_RT', 'BTU power', 'BTU', size=9)
    isa(p, 200, 152, 'BTU')
    tt_top(p, 450, Y_CHWS - 3); tag(p, 432, 150, 80, 'CHWS', 'CHWS header temp', 'TT', size=9)
    pt_top(p, 540, Y_CHWS - 3); tag(p, 556, 150, 100, 'CHW_SupplyHeaderPressure', 'CHW supply pressure', 'PT', size=9)
    hdr_text(p, 640, 176, 'CHWS HEADER', C_CHWS)
    tt_top(p, 196, Y_CHWR - 3); tag(p, 150, 898, 84, 'CHWR', 'CHWR header temp', 'TT', size=9)
    sprite(p, 'v73_fm_h', 262, Y_CHWR, popup='file:^px/ALT_V71_FP_Flow.px', ptitle='Flow meters')
    tag(p, 288, 910, 96, 'CHWFlow', 'CHW flow', 'FT', size=9)
    sprite(p, 'v73_exptank', TANK_X, Y_CHWR - 8, anchor='bottom')
    tag(p, 470, 900, 100, 'CHW_ExpansionTankPressure', 'Expansion tank pressure', 'EXP', size=9)
    hdr_text(p, 296, Y_CHWR + 12, 'CHWR HEADER', C_CHWR)
    # min-flow bypass: isolation (handwheel) / MODULATING / isolation + manual bypass loop
    bfv(p, X_BYP, 600, 'v', 'man')
    bfv(p, X_BYP, 640, 'v', 'mod', pct='CHW_BypassValveCmd', what='CHW bypass valve %', pct_at=(X_BYP + 34, 628))
    bfv(p, X_BYP, 680, 'v', 'man')
    x, y, w, h = sprite(p, 'v73_gate_vl', X_BYL, 640)
    val(p, X_BYL - 26, 726, 62, 'CHW_BypassManualOpen', 'Manual bypass open', h=16, size=7, bool_c=(WARN, OKC), fmt='MAN BYP')
    isa(p, X_BYP - 13, 540, 'MOD')
    hdr_text(p, X_SUC + 12, 872, 'CHP SUCTION HDR', C_CHWR, 130)
    hdr_text(p, 546, 560, 'CHP DISCH. HDR ▶', C_CHWR, 124)
    hdr_text(p, X_RIS + 12, 600, 'CHWS', C_CHWS, 56); hdr_text(p, X_RIS + 12, 616, 'RISER', C_CHWS, 56)
    panel(p, 166, 214, 350, 194, 'CHILLED WATER')
    rows(p, 166, 238, 175, [('CHWS SP', 'CHW_LeavingTemperatureSetpoint_ACTIVE'), ('CHWS', 'CHWS'), ('CHWR', 'CHWR'), ('Load RT', 'CoolingLoad_RT'),
                            ('Flow', 'CHWFlow'), ('Lead CHP', 'CHP_Lead'), ('Return kPa', 'CHW_ReturnHeaderPressure')], lw=74, rh=24)
    rows(p, 341, 238, 175, [('DP', 'CHWDP'), ('DP SP', 'CHWDP_Setpoint_ACTIVE'), ('Bypass %', 'CHW_BypassValveCmd'), ('Bypass fb', 'CHW_BypassValveFeedback'),
                            ('Evap flow', 'CHW_EvapFlowTotal'), ('Min-flow SP', 'CHW_BypassMinFlowSP'), ('Exp. tank', 'CHW_ExpansionTankPressure')], lw=76, rh=24)
    # chemical pot feeder
    sprite(p, 'v73_potfeeder', POT[0] + SPR['v73_potfeeder']['anchors']['in'][0], POT[1] + SPR['v73_potfeeder']['anchors']['in'][1], anchor='in')
    val(p, 664, 884, 92, 'CHW_ChemFeederOpen', 'CHW pot feeder', h=16, size=7, bool_c=(C_CHEM, OFF), fmt='POT FEEDER')
    for n, (x, y) in CHP.items():
        u = f'CHP{n}'
        pic_bool(p, x, y, f'{u}RunProof', 'Pumps/Pumps_Base/Pump_Base_Left/Pump_Base_Left_On.gif', 'Pumps/Pumps_Base/Pump_Base_Left/Pump_Base_Left_Off.png', f'{u} image')
        hot(p, x, y + 10, 110, 70, f'ALT_V71_FP_{u}', f'{u} pump + VSD')
        bfv(p, 460, y + 44.5, 'h', 'onoff', led=f'{u}_SuctionMVCmd', what=f'{u} suction valve open')
        pt_top(p, 488, y + 44.5); tag(p, 434, y + 76, 80, f'{u}_SuctionPressure', f'{u} suction pressure', 'S', size=8)
        pt_top(p, 574, y - 40); tag(p, 590, y - 100, 84, f'{u}_DischargePressure', f'{u} discharge pressure', 'D', size=8)
        bfv(p, 640, y - 40, 'h', 'onoff', led=f'{u}_DischargeMVCmd', what=f'{u} discharge valve open')
        card(p, 174, y - 10, 236, f'CHP-{n}', f'ALT_V71_FP_{u}', f'{u}RunProof',
             [('Status', f'{u}RunProof', {'bool_c': (RUN, OFF)}), ('Speed %', f'{u}SpeedCmd'), ('Hz', f'{u}_SpeedFeedbackHz'), ('kW', f'{u}_kW'),
              ('Pump dP', f'{u}_DiffPressure'), ('Valves / svc', f'{u}_ServiceIsolate', {'action': True})], '#1b4f72', reset=f'{u}ResetFire', lw=92)
    # ================= chillers
    for n, (x, y) in CH.items():
        c = f'CH{n}'
        pic_bool(p, x, y, f'{c}RunProofSelected', 'Chillers/Generic/Chiller_Generic_On.gif', 'Chillers/Generic/Chiller_Generic_Off.png', f'Chiller {n} image')
        hot(p, x + 20, y, 170, 100, f'ALT_V71_FP_{c}', f'Chiller {n}')
        bfv(p, 768, y + 45, 'h', 'mod', pct=f'{c}_ChwFCVCmd', what=f'{c} evaporator FCV', pct_at=(748, y + 2))
        tt_top(p, 810, y + 45); tag(p, 790, y - 20, 76, f'{c}_ChwSupplyTemp', f'{c} CHW leaving', 'LWT', size=8)
        bfv(p, 708, y + 55, 'h', 'onoff', led=f'{c}ValveOpenProof', what=f'{c} CHW isolation valve open', led_at=(716, y + 64))
        tt_bot(p, 806, y + 55); tag(p, 770, y + 88, 72, f'{c}_ChwReturnTemp', f'{c} CHW entering', 'EWT', size=8)
        tt_top(p, x + 222, y + 45); tag(p, x + 198, y - 20, 76, f'{c}_CdwLeavingTemp', f'{c} CDW leaving', 'LWT', size=8)
        bfv(p, x + 262, y + 45, 'h', 'mod', pct=f'{c}_CdwHPVCmd', what=f'{c} condenser HPV', pct_at=(x + 206, y + 2))
        tt_bot(p, x + 222, y + 55); tag(p, x + 222, y + 88, 72, f'{c}_CdwEnteringTemp', f'{c} CDW entering', 'EWT', size=8)
        bfv(p, X_CDS - 30, y + 55, 'h', 'onoff', led=f'{c}CdwValveOpenProof', what=f'{c} CDW isolation valve open', led_at=(X_CDS - 22, y + 64))
        by = y + 108; w = 236
        p.rect(x, by, w, 108, fill='#161c22', stroke='#4a5866', pen=1.0)
        p.label(x, by, w, 22, f'  CHILLER {n}  ⊞', 10, True, 'white', '#4a5866', 'left', popup=f'file:^px/ALT_V71_FP_{c}.px', ptitle=f'Chiller {n}')
        status_led(p, x + w - 18, by + 4, f'{c}RunProofSelected', f'{c} running', 'run')
        for r_, ((t1, p1, k1), (t2, p2)) in enumerate(((('Load', f'{c}LoadPct', 0), ('kW', f'{c}_kW')), (('kW/RT', f'{c}_kW_per_RT', 1), ('RT', f'{c}_RT')),
                                                     (('Flow', f'{c}_ChwFlow', 0), ('Lift', f'{c}_Lift')))):
            yy = by + 24 + r_ * 21
            lbl(p, x + 5, yy, 42, t1, 9, '#c9d3dd')
            if k1: kwrt_val(p, x + 46, yy + 1, 74, p1, f'{c} {t1}')
            else: val(p, x + 46, yy + 1, 74, p1, f'{c} {t1}', h=18, size=9)
            lbl(p, x + 124, yy, 30, t2, 9, '#c9d3dd'); val(p, x + 152, yy + 1, 80, p2, f'{c} {t2}', h=18, size=9)
        yy = by + 24 + 3 * 21
        status_led(p, x + 6, yy + 3, f'{c}InAuto', f'{c} remote'); lbl(p, x + 22, yy, 50, 'Remote', 8)
        val(p, x + 74, yy + 1, 36, f'{c}TimeoutLockout', f'{c} lockout', h=18, size=8, bool_c=(FLT, OKC), fmt='LO')
        p.fire(x + 124, yy + 1, 108, 18, f'RESET {c}', f'{c}ResetFire', f'{c} reset')
    panel(p, 760, 214, 346, 214, 'PLANT SEQUENCE / STAGING')
    rows(p, 760, 238, 346, [('Stage', 'PlantStage'), ('Lead set', 'LeadSet', {'bool_c': ('#2471a3', '#7d3c98')}), ('Pumps / towers', 'Set_LinkPools', {'action': True}),
                            ('Stage-2 request', 'Stage2Request', {'bool_c': (RUN, OFF)}), ('Mode', 'OperationMode', {'bool_c': ('#8e44ad', '#34495e')}),
                            ('', 'PlantScheduleMode', {'action': True}), ('Plant load (% of 1 CH)', 'PlantLoadPct'),
                            ('Start next CH at ≥ %', 'Stage_UpLoadPct', {'action': True, 'fg': '#7dcea0'}),
                            ('Stop lag CH at ≤ %', 'Stage_DownLoadPct', {'action': True, 'fg': '#7dcea0'})], lw=170, rh=21)
    p.label(760, 238 + 5 * 21, 170, 20, '  Schedule ⊞', 9, True, '#8fd3ff', None, 'left', popup='file:^px/ALT_V71_Schedules.px', ptitle='Schedules')
    # ================= CDW side: dosing + bleed on the CDWR riser
    sprite(p, 'v73_dosing', DOS[0] + SPR['v73_dosing']['anchors']['out'][0], DOS[1] + SPR['v73_dosing']['anchors']['out'][1], anchor='out')
    val(p, 930, 150, 72, 'CT_ChemDosingPumpCmd', 'CDW dosing pump', h=16, size=7, bool_c=(C_CHEM, OFF), fmt='DOSING')
    val(p, 930, 168, 72, 'CT_ChemTankLowLevel', 'Chemical tank low', h=16, size=7, bool_c=(WARN, OKC), fmt='CHEM LOW')
    sprite(p, 'v73_sol_h', 1152, 262)
    val(p, 1128, 280, 58, 'CT_BleedValveCmd', 'CDW bleed-off valve', h=16, size=7, bool_c=(RUN, OFF), fmt='BLEED')
    for n, (x, y) in CDP.items():
        u = f'CDP{n}'
        pic_bool(p, x, y, f'{u}RunProof', 'Pumps/Pumps_Base/Pump_Base_Right/Pump_Base_Right_On.gif', 'Pumps/Pumps_Base/Pump_Base_Right/Pump_Base_Right_Off.png', f'{u} image')
        hot(p, x, y + 10, 110, 70, f'ALT_V71_FP_{u}', f'{u} pump + VSD')
        bfv(p, 1392, y + 44.5, 'h', 'onoff', led=f'{u}_SuctionMVCmd', what=f'{u} suction valve open')
        pt_top(p, 1352, y + 44.5); tag(p, 1314, y + 76, 80, f'{u}_SuctionPressure', f'{u} suction pressure', 'S', size=8)
        pt_top(p, 1262, y - 20); tag(p, 1278, y - 80, 84, f'{u}_DischargePressure', f'{u} discharge pressure', 'D', size=8)
        bfv(p, 1214, y - 20, 'h', 'onoff', led=f'{u}_DischargeMVCmd', what=f'{u} discharge valve open')
        card(p, 1444, y - 8, 244, f'CDP-{n}', f'ALT_V71_FP_{u}', f'{u}RunProof',
             [('Status', f'{u}RunProof', {'bool_c': (RUN, OFF)}), ('Speed %', f'{u}SpeedCmd'), ('Hz', f'{u}_SpeedFeedbackHz'), ('kW', f'{u}_kW'),
              ('Pump dP', f'{u}_DiffPressure'), ('Valves / svc', f'{u}_ServiceIsolate', {'action': True})], '#7d6608', reset=f'{u}ResetFire', lw=96, rh=20)
    hdr_text(p, X_CDS - 136, CDP['02'][1] + 16, 'CDP DISCH. HDR ▶', C_CDWS, 132)
    hdr_text(p, X_CDSUC - 118, 530, 'CDP SUCTION HDR', C_CDWS, 112)
    hdr_text(p, X_CDR - 50, 668, 'CDWR', C_CDWR, 46); hdr_text(p, X_CDR - 50, 684, 'RISER', C_CDWR, 46)
    hdr_text(p, 1330, Y_CDR + 12, 'CDWR HEADER', C_CDWR)
    tt_bot(p, 1300, Y_CDR + 3)
    pic(p, X_CDSUC - 8 - 27, 440 - 13.5, 'Sensors/sensor_pipe_welltemp2_ver_left.png'); tag(p, X_CDSUC - 128, 420, 88, 'CDS', 'CDW supply header temp', 'TT', size=9)
    sprite(p, 'v73_fm_vl', X_CDSUC, 500, popup='file:^px/ALT_V71_FP_Flow.px', ptitle='Flow meters'); tag(p, X_CDSUC - 150, 506, 94, 'CDW_Flow', 'CDW header flow', 'FT', size=9)
    panel(p, 1190, 196, 218, 214, 'CONDENSER WATER')
    rows(p, 1190, 220, 218, [('CDS SP', 'CDS_Setpoint_ACTIVE'), ('CDS', 'CDS'), ('CDR', 'CDR'), ('CDW flow', 'CDW_Flow'), ('Make-up m3/h', 'CT_MakeupFlow'),
                             ('Conductivity', 'CT_Conductivity'), ('Lead CDP', 'CDP_Lead'), ('Lead CT', 'CT_Lead'), ('Towers', 'CT_Mode2Towers', {'bool_c': ('#935116', '#2c3e50')})],
         lw=98, rh=21)
    # ================= cooling towers: 2 cells each (animated fans), inlet / outlet MVs, make-up, cards
    for n in TWX:
        u = f'CT{n}'; x0, y0 = TWX[n], TWY
        w, h = SPR['v73_ct2_off']['size']
        ximg_bool(p, x0, y0, w, h, f'{u}RunProof', 'v73_ct2_on.gif', 'v73_ct2_off.png', f'{u} image (fans animate when running)')
        for k in ('01', '02'):
            cx, cy = ct_anchor(n, f'cell{int(k)}')
            hot(p, cx - 44, cy - 10, 88, 60, f'ALT_V73_FP_{u}_{k}', f'{CN[u + "_" + k]} fan cell')
            status_led(p, cx - 7, cy + 36, f'{u}_{k}RunProof', f'{CN[u + "_" + k]} running', 'run')
        hot(p, x0 + 30, y0 + 110, w - 60, 70, f'ALT_V71_FP_{u}', f'Cooling tower {n}')
        ix, iy = ct_anchor(n, 'inlet')
        bfv(p, CT_DROP[n], 190, 'v', 'onoff', led=f'{u}ValveOpenProof', what=f'{u} inlet valve open')
        tt_top(p, CT_DROP[n] + 14, iy)
        ox, oy = ct_anchor(n, 'outlet')
        bfv(p, 1462 if n == '01' else 1772, oy, 'h', 'onoff', led=f'{u}_OutletMVCmd', what=f'{u} outlet valve open')
        mx, my = ct_anchor(n, 'makeup')
        sprite(p, 'v73_sol_h', mx + 30, Y_MUH)
        status_led(p, mx + 38, Y_MUH - 22, f'{u}_MakeupValveCmd', f'{u} make-up valve open', 'run')
        # tower + cells card
        bx, by, bw = (1440, 378, 296) if n == '01' else (1786, 378, 296)
        p.rect(bx, by, bw, 166, fill='#161c22', stroke='#4a5866', pen=1.0)
        p.label(bx, by, bw, 22, f'  CT-{n}  (2 cells) ⊞', 10, True, 'white', '#935116', 'left', popup=f'file:^px/ALT_V71_FP_{u}.px', ptitle=f'Cooling tower {n}')
        status_led(p, bx + bw - 18, by + 4, f'{u}RunProof', f'{u} running', 'run')
        p.fire(bx + bw - 90, by + 2, 66, 18, 'RESET', f'{u}ResetFire', f'Reset {u}')
        cw = (bw - 86) / 2
        for j, k in enumerate(('01', '02')):
            c = f'{u}_{k}'; xx = bx + 84 + j * cw
            p.label(xx, by + 24, cw - 4, 18, f'{CN[c]} ⊞', 8, True, 'white', '#5b3a1a', 'center', popup=f'file:^px/ALT_V73_FP_{c}.px', ptitle=f'{CN[c]} fan cell')
            val(p, xx, by + 44, cw - 4, f'{c}SpeedCmd', f'{CN[c]} speed', h=18, size=8)
            val(p, xx, by + 64, cw - 4, f'{c}_FanSpeedHz', f'{CN[c]} Hz', h=18, size=8)
            val(p, xx, by + 84, cw - 4, f'{c}_kW', f'{CN[c]} kW', h=18, size=8)
            val(p, xx, by + 104, cw - 4, f'{c}_FaultSts', f'{CN[c]} fault', h=18, size=8, bool_c=(FLT, OKC), fmt='%out.value%')
        for i, t in enumerate(('Fan speed', 'Output Hz', 'Power', 'Fault / svc')):
            lbl(p, bx + 4, by + 43 + i * 20, 80, t, 8, '#c9d3dd')
        lbl(p, bx + 4, by + 124, 80, 'In / out °C', 8, '#c9d3dd')
        val(p, bx + 84, by + 125, cw - 4, f'{u}_InletTemp', f'{u} water in', h=18, size=8)
        val(p, bx + 84 + cw, by + 125, cw - 4, f'{u}_OutletTemp', f'{u} water out', h=18, size=8)
        yy = by + 146
        val(p, bx + 2, yy, 70, f'{u}_BasinLevel', f'{u} basin level', h=18, size=8, fmt='LVL %out.value%')
        for j, (pt, t, cc) in enumerate(((f'{u}BasinLowLowLevelAlarm', 'LL', FLT), (f'{u}BasinLowLevelAlarm', 'LOW', FLT), (f'{u}BasinHighLevelAlarm', 'HI', WARN),
                                         (f'{u}BasinHighHighLevelAlarm', 'HH', FLT), (f'{u}_MakeupValveCmd', 'FILL', RUN))):
            val(p, bx + 76 + j * 44, yy, 42, pt, f'{u} {t}', h=18, size=8, bool_c=(cc, OKC if t != 'FILL' else OFF), fmt=t)
    hdr_text(p, 1970, Y_MUH + 4, 'MAKE-UP', C_MU, 70)
    # ================= outdoor air + legend
    panel(p, 1716, 552, 366, 188, 'OUTDOOR AIR', link='file:^px/ALT_V71_FP_OA.px')
    sprite(p, 'v73_oa', 1742, 600, anchor='top')
    oa_rows(p, 1776, 576, 300, rh=26, lw=150)
    panel(p, 1716, 750, 366, 214, 'LEGEND')
    items = (('CHW supply', '#1665d6'), ('CHW return', '#5ec4f2'), ('CDW supply', '#f2c416'), ('CDW return', '#f07a12'),
             ('Make-up water', C_MU), ('Chemical', C_CHEM), ('Bleed / drain', '#969696'))
    for i, (t, c) in enumerate(items):
        yy = 776 + i * 22
        p.rect(1726, yy + 6, 30, 9, fill=c, stroke=c, pen=1.0); lbl(p, 1762, yy, 140, t, 8, TXT)
    for i, (nm, t) in enumerate((('v73_bfv_onoff_h', 'on/off MV (LED = open)'), ('v73_bfv_mod_h', 'modulating MV (%)'), ('v73_bfv_man_h', 'manual (handwheel)'))):
        sprite(p, nm, 1918, 792 + i * 52)
        lbl(p, 1944, 780 + i * 52, 136, t, 8, TXT)
    lbl(p, 1726, 932, 350, 'thick = header, thin = branch · tower fans animate when running', 8, TXT)
    # ================= bottom band
    y0 = 992
    panel(p, 10, y0, 470, 182, 'EQUIPMENT POOLS / SET')
    for i, eq in enumerate(('CHP', 'CDP', 'CT')):
        yy = y0 + 28 + i * 34
        lbl(p, 16, yy, 44, eq, 10, TXT, True)
        lbl(p, 56, yy, 40, 'Lead'); val(p, 92, yy + 1, 60, f'{eq}_Lead', f'{eq} lead', h=20, size=9)
        val(p, 156, yy + 1, 70, f'{eq}_RotationMode_Runtime', f'{eq} rotation mode', h=20, size=9, action=True)
        val(p, 230, yy + 1, 116, f'{eq}_PoolDegradedAlarm', f'{eq} standby lost', h=20, size=8, bool_c=(WARN, OKC), fmt='Standby: %out.value%')
        val(p, 350, yy + 1, 124, f'{eq}_PoolUnavailableAlarm', f'{eq} none available', h=20, size=8, bool_c=(FLT, OKC), fmt='No unit: %out.value%')
    lbl(p, 16, y0 + 136, 130, 'Lead chiller (set)'); val(p, 136, y0 + 137, 96, 'LeadCH01', 'Lead chiller select', h=20, size=9, action=True)
    val(p, 236, y0 + 137, 110, 'Set_LinkPools', 'Pools linked to set', h=20, size=8, action=True)
    val(p, 350, y0 + 137, 124, 'Stage2BlockedByPoolAlarm', 'Stage 2 blocked', h=20, size=8, bool_c=(WARN, OKC), fmt='S2 blocked: %out.value%')
    panel(p, 490, y0, 610, 182, 'PLANT ALARMS', link='file:^px/ALT_CP_AlarmsHistory.px')
    al = [('All chillers unavailable', 'AllChillersUnavailableAlarm'), ('CHW flow low', 'CHW_FlowLowAlarm'), ('CDW flow low', 'CDW_FlowLowAlarm'),
          ('CHWST not tracking', 'CHWST_NotTrackingAlarm'), ('Low delta-T', 'LowDeltaTAlarm'), ('Manual bypass open', 'CHW_BypassManualOpenAlarm'),
          ('CHW fill lock-out (leak)', 'CHW_FillLockoutAlarm'), ('CT01 basin LOW-LOW', 'CT01BasinLowLowLevelAlarm'), ('CT02 basin LOW-LOW', 'CT02BasinLowLowLevelAlarm'),
          ('CT start inhibited', 'CT_StartInhibitedAlarm'), ('CT basin HIGH-HIGH', 'CT01BasinHighHighLevelAlarm'), ('Conductivity high', 'CT_ConductivityHighAlarm'),
          ('Make-up pressure low', 'MU_SupplyLowAlarm'), ('Both basins dry (CDP stop)', 'CT_AllBasinsDryAlarm')]
    for i, (t, pt) in enumerate(al):
        cx, cy = 500 + (i // 7) * 300, y0 + 26 + (i % 7) * 22
        status_led(p, cx, cy + 3, pt, t, 'alarm'); lbl(p, cx + 20, cy, 272, t, 9, TXT)
    panel(p, 1110, y0, 540, 182, 'CONTROL')
    rows(p, 1110, y0 + 24, 270, [('Plant enable', 'PlantEnable', {'bool_c': (RUN, OFF), 'action': True}), ('Schedule mode', 'PlantScheduleMode', {'action': True}),
                                 ('Demand mode', 'PlantDemandMode', {'action': True}), ('Pump valves', 'Pump_StandbyValvesOpen', {'action': True}),
                                 ('Towers (SOO)', 'CT_RunAllAvailable', {'action': True}), ('Load source', 'CoolingLoadSource')], lw=120, rh=25)
    rows(p, 1380, y0 + 24, 270, [('Plant main kW', 'PM_Main_kW'), ('Plant kWh today', 'Plant_kWh_Today'), ('Cost today', 'Energy_Cost_THB_Today'),
                                 ('CHWS valid', 'CHWS_SensorInvalidAlarm', {'bool_c': (FLT, OKC)}), ('Rotation daily', 'RotationMode_Daily', {'action': True}),
                                 ('Rotation weekly', 'RotationMode_Weekly', {'action': True})], lw=120, rh=25)
    gauge_panel(p, 1660, y0, 432, 182)
    # make-up / fill labels + components (drawn last: over the pipe layer)
    sprite(p, 'v73_rpz', 700, Y_MU)
    sprite(p, 'v73_fm_h', 616, Y_MU)
    sprite(p, 'v73_sol_h', 556, Y_MU)
    status_led(p, 566, Y_MU - 30, 'CHW_FillValveCmd', 'CHW fill valve open', 'run')
    lbl(p, 470, 928, 360, '◀ CHW LOOP FILL: solenoid · meter · RPZ  (make-up water)', 8, C_MU, True, h=16)
    val(p, 760, Y_MU - 26, 92, 'CHW_FillLockoutAlarm', 'CHW fill lock-out', h=16, size=7, bool_c=(FLT, OKC), fmt='FILL LOCK-OUT')
    lbl(p, 1890, Y_MU - 22, 190, 'MAKE-UP WATER (tank) ▶', 8, C_MU, True, h=16, halign='right')
    return p


# ================================================================ 3-D pages: automatic card placement on the render
import numpy as np
from PIL import Image


class Placer:
    """greedy placement of value cards next to their anchors, avoiding the equipment (mask alpha) and each other"""
    def __init__(self, mask_png, W=1920, H=944):
        a = np.asarray(Image.open(mask_png).convert('RGBA'))[..., 3] > 60
        self.W, self.H = W, H
        self.busy = a.astype(np.float32)
        self.cards = np.zeros_like(self.busy)
        self.anchors = []

    def block(self, x, y, w, h, margin=6):
        x0, y0 = max(0, int(x - margin)), max(0, int(y - margin))
        self.cards[y0:int(y + h + margin), x0:int(x + w + margin)] = 1

    def _sum(self, I, x, y, w, h):
        return I[y + h, x + w] - I[y, x + w] - I[y + h, x] + I[y, x]

    def place(self, ax, ay, w, h, reach=420, step=8, prefer=None):
        Ib = np.pad(self.busy, ((1, 0), (1, 0))).cumsum(0).cumsum(1)
        Ic = np.pad(self.cards, ((1, 0), (1, 0))).cumsum(0).cumsum(1)
        best = None
        for cy in range(max(4, int(ay - h - reach)), min(self.H - h - 4, int(ay + reach)), step):
            for cx in range(max(4, int(ax - w - reach)), min(self.W - w - 4, int(ax + reach)), step):
                ov = self._sum(Ic, cx, cy, w, h)
                if ov > 0: continue
                bz = self._sum(Ib, cx, cy, w, h) / (w * h)
                nx, ny = min(max(ax, cx), cx + w), min(max(ay, cy), cy + h)
                dist = ((nx - ax) ** 2 + (ny - ay) ** 2) ** 0.5
                if dist < 1: continue                                   # never cover its own anchor
                cost = bz * 900 + dist * 1.0
                for (bx, by) in self.anchors:                          # keep other anchors visible
                    if cx - 8 <= bx <= cx + w + 8 and cy - 8 <= by <= cy + h + 8: cost += 400
                if prefer == 'up' and cy + h > ay: cost += 150
                if prefer == 'down' and cy < ay: cost += 150
                if best is None or cost < best[0]: best = (cost, cx, cy)
        if best is None: raise SystemExit(f'no room for card at {ax},{ay}')
        _, cx, cy = best
        self.block(cx, cy, w, h)
        return cx, cy


def card3d(p, P, A, key, title, fpn, run, vals, w=156, col='#2c3e50', y0=136, prefer=None, chips=(), extra_h=0, reset=None, pos=None):
    ax, ay = A[key]
    if not (10 <= ax <= 1910 and 10 <= ay <= 934): return None          # equipment outside this view
    h = 22 + 20 * len(vals) + (22 if chips else 0) + extra_h
    cx, cy = pos if pos else P.place(ax, ay, w, h, prefer=prefer)
    if pos: P.block(cx, cy, w, h)
    X, Y = cx, cy + y0
    nx, ny = min(max(ax, X), X + w), min(max(ay + y0, Y), Y + h)
    leader(p, ax, ay + y0, nx, ny)
    p.rect(X, Y, w, h, fill='#0b0e11', stroke='#5dade2', pen=1.0)
    p.label(X, Y, w, 20, f'  {title}  ⊞' if fpn else f'  {title}', 9, True, 'white', col, 'left', popup=f'file:^px/{fpn}.px' if fpn else None, ptitle=title)
    if run: status_led(p, X + w - 18, Y + 3, run, f'{title} running', 'run')
    if reset: p.fire(X + w - 70 - (20 if run else 0), Y + 2, 48, 16, 'RESET', reset, f'Reset {title}')
    for i, it in enumerate(vals):
        pre, pt = it[0], it[1]; kw = it[2] if len(it) > 2 else {}
        if kw.get('kwrt'):
            lbl(p, X + 4, Y + 21 + i * 20, 44, pre, 8, '#c9d3dd')
            kwrt_val(p, X + 48, Y + 22 + i * 20, w - 52, pt, f'3D {title} {pre}', h=18, size=8)
        else:
            tag(p, X + 2, Y + 21 + i * 20, w - 4, pt, f'3D {title} {pre}', pre, size=8, **{k: v for k, v in kw.items() if k != 'kwrt'})
    if chips:
        cw = (w - 4) / len(chips)
        for j, (pt, t, cc, oc) in enumerate(chips):
            val(p, X + 2 + j * cw, Y + 22 + 20 * len(vals), cw - 2, pt, f'3D {title} {t}', h=18, size=7, bool_c=(cc, oc), fmt=t)
    return X, Y, w, h


def page3d(name, title, view):
    p = G.Page(name, title, (1920, 1080)); p.header()
    G7.kpi_strip(p)
    A = json.load(open(os.path.join(OUT, 'px', 'img', f'v73_3d_{view}_anchors.json')))['anchors']
    ximg(p, 0, 136, f'v73_3d_{view}.png', 1920, 944, bottom=True)
    P = Placer(os.path.join(OUT, f'v73_3d_{view}_mask.png'))
    P.anchors = list(A.values())
    return p, A, P


def fixed_panel(p, P, x, y, w, h, title, link=None, y0=136):
    panel(p, x, y, w, h, title, link)
    P.block(x, y - y0, w, h, margin=8)


def legend3d(p, x, y):
    for i, (t, c) in enumerate((('CHWS', '#1665d6'), ('CHWR', '#5ec4f2'), ('CDWS', '#f2c416'), ('CDWR', '#f07a12'), ('MAKE-UP', C_MU), ('CHEM', C_CHEM))):
        p.rect(x + i * 92, y + 6, 22, 9, fill=c, stroke=c, pen=1.0); lbl(p, x + 26 + i * 92, y, 64, t, 8, TXT, True)
    p.rect(x + 560, y + 5, 12, 10, fill='#c0392b', stroke='#c0392b', pen=1.0); lbl(p, x + 576, y, 110, 'on/off MV', 8, TXT, True)
    p.rect(x + 660, y + 5, 12, 10, fill='#1e8449', stroke='#1e8449', pen=1.0); lbl(p, x + 676, y, 130, 'modulating MV', 8, TXT, True)


SOO_ROWS = [('Towers requested', 'CT_Mode2Towers', {'bool_c': ('#935116', '#2c3e50')}), ('Lead tower', 'CT_Lead'),
            ('Chillers', 'CT_OneChillerModeSts', {'bool_c': ('#2471a3', '#34495e')}), ('Fan enable (CDP + CDW flow)', 'CT_FanEnableSts', {'bool_c': (RUN, FLT)}),
            ('Lag staged', 'CT_LagStagedSts', {'bool_c': ('#935116', '#2c3e50')}), ('Stage-up A+B', 'CT_StageUpCondSts', {'bool_c': (WARN, OFF)}),
            ('Reduce A+B+C', 'CT_StageDownCondSts', {'bool_c': (WARN, OFF)}), ('Lag minimum stop', 'CT_LagMinStopSts', {'bool_c': (WARN, OFF)}),
            ('CDS / SP', 'CDS'), ('', 'CDS_Setpoint_ACTIVE'), ('Stage-up above °C', 'CT_CdsStageUpSP'), ('Reduce below °C', 'CT_CdsStageDownSP'),
            ('Lead fan speed % (B)', 'CT_LeadSpeed'), ('PID request %', 'CT_CommonSpeed')]
SOO_SET = [('A: CDS > SP + K', 'CT_StageUpDeltaK', {'action': True, 'fg': '#7dcea0'}), ('B: lead speed ≥ %', 'CT_StageUpSpeedPct', {'action': True, 'fg': '#7dcea0'}),
           ('Reduce: CDS < SP − K', 'CT_StageDownDeltaK', {'action': True, 'fg': '#7dcea0'}), ('Reduce: speed ≤ %', 'CT_LowSpeedPct', {'action': True, 'fg': '#7dcea0'}),
           ('Initial fan speed %', 'CT_InitialSpeed', {'action': True, 'fg': '#7dcea0'}), ('Min CDW flow m³/h', 'CT_CdwMinFlow', {'action': True, 'fg': '#7dcea0'}),
           ('1 tower w/ 2 CH', 'CT_SingleTowerVerified', {'action': True}), ('Cell lost → lag', 'CT_StageOnCellFail', {'action': True}),
           ('Lead tower by', 'CT_LeadByRuntime', {'action': True}), ('Towers mode', 'CT_RunAllAvailable', {'action': True})]


def ctplant_page():
    p, A, P = page3d('ALT_V73_CTPlant', 'Cooling tower plant — 2 towers × 2 fan cells (VSD per cell), SOO staging', 'ct')
    legend3d(p, 470, 142)
    fixed_panel(p, P, 10, 146, 450, 22 + len(SOO_ROWS) * 20 + 8, 'COOLING TOWER SOO — ADD / REDUCE')
    rows(p, 10, 170, 450, SOO_ROWS, lw=240, rh=20)
    y = 146 + 22 + len(SOO_ROWS) * 20 + 14
    fixed_panel(p, P, 10, y, 450, 22 + len(SOO_SET) * 20 + 8, 'SOO SETTINGS (click green values)')
    rows(p, 10, y + 24, 450, SOO_SET, lw=240, rh=20)
    y2 = y + 22 + len(SOO_SET) * 20 + 14
    fixed_panel(p, P, 10, y2, 450, 22 + 6 * 19 + 10, 'SOO SUMMARY (Kittipoom S.)')
    for i, t in enumerate(('Enable: ≥1 chiller request · CDP running · CDW flowing · no critical interlock',
                           '1 chiller: lead tower (lowest runtime) → valves proven → fans at initial speed → PID',
                           'Stage LAG: CDS > SP+1.0 K AND lead ≥ 90 % for 10 min (timer resets)',
                           'Reduce: 1 chiller AND CDS < SP−0.5 K AND fans ≤ low for 30 min → lag off, min stop',
                           '2 chillers: both towers, reduction locked out (unless verified)',
                           'Added: cell lost / CDS invalid → lag staged; basin LOW-LOW → tower isolated')):
        lbl(p, 18, y2 + 24 + i * 19, 436, t, 8, TXT, h=18)
    fixed_panel(p, P, 1480, 882, 432, 190, 'PLANT kW/RT — ASHRAE')
    gauge_panel(p, 1480, 882, 432, 190)
    fixed_panel(p, P, 1480, 668, 432, 206, 'WATER TREATMENT & MAKE-UP')
    rows(p, 1480, 692, 432, [('Conductivity µS/cm', 'CT_Conductivity'), ('Bleed-off valve', 'CT_BleedValveCmd', {'bool_c': (RUN, OFF)}),
                             ('Dosing pump', 'CT_ChemDosingPumpCmd', {'bool_c': (C_CHEM, OFF)}), ('Chemical tank', 'CT_ChemTankLowLevel', {'bool_c': (WARN, OKC)}),
                             ('Make-up flow / volume', 'CT_MakeupFlow'), ('', 'CT_MakeupVolume'), ('Make-up header kPa', 'MU_SupplyPressure'),
                             ('Bleed on / off µS', 'CT_BleedOnUs', {'action': True, 'fg': '#7dcea0'})], lw=230, rh=22)
    # ---- cards
    for tw in ('CT01', 'CT02'):
        for k in ('01', '02'):
            c = f'{tw}_{k}'
            card3d(p, P, A, c, CN[c], f'ALT_V73_FP_{c}', f'{c}RunProof',
                   [('SPD', f'{c}SpeedCmd'), ('Hz', f'{c}_FanSpeedHz'), ('kW', f'{c}_kW')], w=150, col='#5b3a1a', prefer='up',
                   chips=[(f'{c}_FaultSts', '%out.value%', FLT, OKC), (f'{c}_ServiceIsolate', 'SERVICE', WARN, OFF)], reset=None)
    for tw in ('CT01', 'CT02'):
        card3d(p, P, A, f'{tw}_basin', f'TOWER {tw[2:]}', f'ALT_V71_FP_{tw}', f'{tw}RunProof',
               [('IN', f'{tw}_InletTemp'), ('OUT', f'{tw}_OutletTemp'), ('RANGE', f'{tw}_Range'), ('APPR', f'{tw}_Approach'), ('LVL', f'{tw}_BasinLevel')],
               w=160, col='#935116', prefer='down',
               chips=[(f'{tw}BasinLowLowLevelAlarm', 'LL', FLT, OKC), (f'{tw}BasinLowLevelAlarm', 'LO', FLT, OKC), (f'{tw}BasinHighLevelAlarm', 'HI', WARN, OKC),
                      (f'{tw}BasinHighHighLevelAlarm', 'HH', FLT, OKC)])
        card3d(p, P, A, f'{tw}_in', f'{tw} INLET MV', None, f'{tw}ValveOpenProof', [], w=124, col='#8a4a10')
        card3d(p, P, A, f'{tw}_mu', f'{tw} MAKE-UP', None, f'{tw}_MakeupValveCmd', [], w=120, col='#1e6b3a')
    for u in ('CDP01', 'CDP02'):
        card3d(p, P, A, u, u, f'ALT_V71_FP_{u}', f'{u}RunProof', [('SPD', f'{u}SpeedCmd'), ('kW', f'{u}_kW'), ('dP', f'{u}_DiffPressure')], w=140, col='#7d6608')
    card3d(p, P, A, 'CDWR', 'CDWR HEADER', None, None, [('T', 'CDR')], w=130, col='#8a4a10')
    card3d(p, P, A, 'FT_CDW', 'CDWS / FLOW', 'ALT_V71_FP_Flow', None, [('T', 'CDS'), ('F', 'CDW_Flow')], w=140, col='#8a7a10')
    card3d(p, P, A, 'BLEED', 'BLEED-OFF', None, 'CT_BleedValveCmd', [], w=110, col='#566573')
    card3d(p, P, A, 'DOSING', 'DOSING', None, 'CT_ChemDosingPumpCmd', [('µS', 'CT_Conductivity')], w=120, col='#5b2c83')
    card3d(p, P, A, 'OA', 'OUTDOOR AIR', 'ALT_V71_FP_OA', None, [('DB', 'OA_Temperature'), ('RH', 'OA_Humidity'), ('WB', 'OA_WetBulb'), ('DP', 'OA_DewPoint')],
           w=150, col='#1b3a2f')
    return p


def chillerplant_page():
    p, A, P = page3d('ALT_V73_ChillerPlant', 'Chiller plant room — chillers, CHW pumps, bypass, BTU, fill, chemical feeder', 'chiller')
    legend3d(p, 470, 142)
    fixed_panel(p, P, 10, 146, 440, 22 + 8 * 22 + 8, 'CHILLED WATER')
    rows(p, 10, 170, 220, [('CHWS SP', 'CHW_LeavingTemperatureSetpoint_ACTIVE'), ('CHWS', 'CHWS'), ('CHWR', 'CHWR'), ('Load RT', 'CoolingLoad_RT'),
                           ('Flow', 'CHWFlow'), ('Lead CHP', 'CHP_Lead'), ('DP', 'CHWDP'), ('DP SP', 'CHWDP_Setpoint_ACTIVE')], lw=90, rh=22)
    rows(p, 230, 170, 220, [('Bypass cmd', 'CHW_BypassValveCmd'), ('Bypass fb', 'CHW_BypassValveFeedback'), ('Evap flow', 'CHW_EvapFlowTotal'),
                            ('Min-flow SP', 'CHW_BypassMinFlowSP'), ('Manual byp.', 'CHW_BypassManualOpen', {'bool_c': (WARN, OKC)}),
                            ('Exp. tank', 'CHW_ExpansionTankPressure'), ('Fill valve', 'CHW_FillValveCmd', {'bool_c': (RUN, OFF)}),
                            ('Fill m³', 'CHW_FillVolume')], lw=96, rh=22)
    y = 146 + 22 + 8 * 22 + 16
    fixed_panel(p, P, 10, y, 440, 22 + 9 * 21 + 8, 'PLANT SEQUENCE / STAGING')
    rows(p, 10, y + 24, 440, [('Stage', 'PlantStage'), ('Lead set', 'LeadSet', {'bool_c': ('#2471a3', '#7d3c98')}), ('Stage-2 request', 'Stage2Request', {'bool_c': (RUN, OFF)}),
                              ('Mode', 'OperationMode', {'bool_c': ('#8e44ad', '#34495e')}), ('Plant load (% of 1 CH)', 'PlantLoadPct'),
                              ('Start next CH at ≥ %', 'Stage_UpLoadPct', {'action': True, 'fg': '#7dcea0'}), ('Stop lag CH at ≤ %', 'Stage_DownLoadPct', {'action': True, 'fg': '#7dcea0'}),
                              ('Pump valves', 'Pump_StandbyValvesOpen', {'action': True}), ('Min-flow margin', 'Byp_MinFlowMargin', {'action': True, 'fg': '#7dcea0'})], lw=240, rh=21)
    fixed_panel(p, P, 1480, 882, 432, 190, 'PLANT kW/RT — ASHRAE')
    gauge_panel(p, 1480, 882, 432, 190)
    fixed_panel(p, P, 1480, 700, 432, 174, 'OUTDOOR AIR', link='file:^px/ALT_V71_FP_OA.px')
    oa_rows(p, 1480, 724, 432, rh=24, lw=230)
    for n in ('01', '02'):
        c = f'CH{n}'
        card3d(p, P, A, c, f'CHILLER {n}', f'ALT_V71_FP_{c}', f'{c}RunProofSelected',
               [('LOAD', f'{c}LoadPct'), ('kW', f'{c}_kW'), ('kW/RT', f'{c}_kW_per_RT', {'kwrt': True}), ('RT', f'{c}_RT')], w=160, col='#4a5866',
               chips=[(f'{c}InAuto', 'REMOTE', RUN, WARN), (f'{c}TimeoutLockout', 'LOCKOUT', FLT, OKC)])
        card3d(p, P, A, f'{c}_chw', f'{c} CHW', None, None, [('LWT', f'{c}_ChwSupplyTemp'), ('EWT', f'{c}_ChwReturnTemp'), ('FCV', f'{c}_ChwFCVCmd')], w=130, col='#1a4a8a')
        u = f'CHP{n}'
        card3d(p, P, A, u, u, f'ALT_V71_FP_{u}', f'{u}RunProof', [('SPD', f'{u}SpeedCmd'), ('Hz', f'{u}_SpeedFeedbackHz'), ('kW', f'{u}_kW'), ('dP', f'{u}_DiffPressure')],
               w=140, col='#1b4f72', chips=[(f'{u}_SuctionMVCmd', 'SUC MV', RUN, OFF), (f'{u}_DischargeMVCmd', 'DIS MV', RUN, OFF)])
    card3d(p, P, A, 'BTU', 'BTU METER', 'ALT_V71_FP_BTU', None, [('RT', 'BTU_Power_RT'), ('FLOW', 'BTU_Flow'), ('ΔT', 'BTU_DeltaT')], w=140, col='#154360')
    card3d(p, P, A, 'CHWS', 'CHWS HEADER', None, None, [('T', 'CHWS'), ('P', 'CHW_SupplyHeaderPressure')], w=130, col='#1a4a8a')
    card3d(p, P, A, 'FT_CHW', 'CHWR / FT', 'ALT_V71_FP_Flow', None, [('T', 'CHWR'), ('F', 'CHWFlow')], w=130, col='#2a6f8f')
    card3d(p, P, A, 'BYPASS', 'MIN-FLOW BYPASS', None, None, [('CMD', 'CHW_BypassValveCmd'), ('FB', 'CHW_BypassValveFeedback'), ('SP', 'CHW_BypassMinFlowSP')],
           w=150, col='#1e8449', chips=[('CHW_BypassManualOpen', 'MANUAL BYPASS', WARN, OKC)])
    card3d(p, P, A, 'EXP', 'EXPANSION TANK', None, None, [('P', 'CHW_ExpansionTankPressure')], w=140, col='#1a4a8a')
    card3d(p, P, A, 'FILL', 'CHW FILL (MAKE-UP)', None, 'CHW_FillValveCmd', [('VOL', 'CHW_FillVolume')], w=160, col='#1e6b3a',
           chips=[('CHW_FillLockoutAlarm', 'LOCK-OUT', FLT, OKC)])
    card3d(p, P, A, 'POT', 'POT FEEDER', None, 'CHW_ChemFeederOpen', [], w=120, col='#5b2c83')
    card3d(p, P, A, 'BUILDING', 'BUILDING', 'ALT_V73_Zones', None, [('ΔP', 'CHWDP'), ('AHU1 zone', 'Zone_AHU01_AvgTemp')], w=150, col='#1b3a2f')
    return p


def plant3d_page():
    p, A, P = page3d('ALT_V71_Plant3D', 'Plant 3D — whole plant (isometric render + live values)', 'plant')
    legend3d(p, 20, 142)
    fixed_panel(p, P, 1480, 882, 432, 190, 'PLANT kW/RT — ASHRAE')
    gauge_panel(p, 1480, 882, 432, 190)
    for tw in ('CT01', 'CT02'):
        c1, c2 = f'{tw}_01', f'{tw}_02'
        card3d(p, P, A, tw, f'TOWER {tw[2:]}', f'ALT_V71_FP_{tw}', f'{tw}RunProof',
               [(CN[c1][3:], f'{c1}SpeedCmd'), (CN[c2][3:], f'{c2}SpeedCmd'), ('IN', f'{tw}_InletTemp'), ('OUT', f'{tw}_OutletTemp'), ('LVL', f'{tw}_BasinLevel')],
               w=150, col='#935116', prefer='up')
    for n in ('01', '02'):
        c = f'CH{n}'
        card3d(p, P, A, c, f'CHILLER {n}', f'ALT_V71_FP_{c}', f'{c}RunProofSelected', [('LOAD', f'{c}LoadPct'), ('kW', f'{c}_kW'), ('kW/RT', f'{c}_kW_per_RT', {'kwrt': True})],
               w=150, col='#4a5866')
        for u in (f'CHP{n}', f'CDP{n}'):
            card3d(p, P, A, u, u, f'ALT_V71_FP_{u}', f'{u}RunProof', [('SPD', f'{u}SpeedCmd'), ('kW', f'{u}_kW')], w=130, col='#1b4f72' if u.startswith('CHP') else '#7d6608')
    card3d(p, P, A, 'CHWS', 'CHWS', None, None, [('T', 'CHWS')], w=110, col='#1a4a8a')
    card3d(p, P, A, 'CHWR', 'CHWR', None, None, [('T', 'CHWR')], w=110, col='#2a6f8f')
    card3d(p, P, A, 'CDWR', 'CDWR', None, None, [('T', 'CDR')], w=110, col='#8a4a10')
    card3d(p, P, A, 'CDWS', 'CDWS', None, None, [('T', 'CDS')], w=110, col='#8a7a10')
    card3d(p, P, A, 'BTU', 'BTU', 'ALT_V71_FP_BTU', None, [('RT', 'BTU_Power_RT')], w=120, col='#154360')
    card3d(p, P, A, 'BYPASS', 'BYPASS', None, None, [('%', 'CHW_BypassValveCmd')], w=110, col='#1e8449')
    card3d(p, P, A, 'OA', 'OUTDOOR AIR', 'ALT_V71_FP_OA', None, [('DB', 'OA_Temperature'), ('WB', 'OA_WetBulb')], w=130, col='#1b3a2f')
    lbl(p, 20, 1058, 900, 'Rendered with Blender (bpy / Cycles) from tools/plant3d73.py — same model as Chiller Plant / CT Plant pages; click a card title for the faceplate.', 8, LBL)
    return p


# ================================================================ Zones (Sense-T / AirPlug)
ZONES = [('01_0101', 'Lobby', 'AHU01'), ('01_0102', 'Reception', 'AHU01'), ('01_0103', 'Open office A', 'AHU01'), ('01_0104', 'Open office B', 'AHU01'),
         ('01_0105', 'Meeting 1', 'AHU02'), ('01_0106', 'Meeting 2', 'AHU02'), ('01_0107', 'Training', 'AHU02'), ('01_0108', 'Executive', 'AHU02'),
         ('01_0109', 'Server room', 'FCU'), ('01_0110', 'Pantry', 'FCU'), ('01_0111', 'Storage', 'OAU01'), ('01_0112', 'Corridor', 'OAU01')]
TMAP = [(-50.0, 22.0, 'rgba(66,133,244,0.42)', '#4285f4', '< 22 °C'), (22.0, 23.0, 'rgba(0,188,212,0.38)', '#00bcd4', '22–23'),
        (23.0, 26.0, 'rgba(76,175,80,0.34)', '#4caf50', '23–26 comfort'), (26.0, 27.0, 'rgba(255,193,7,0.40)', '#ffc107', '26–27'),
        (27.0, 28.0, 'rgba(255,112,67,0.45)', '#ff7043', '27–28'), (28.0, 99.0, 'rgba(229,57,53,0.50)', '#e53935', '> 28 °C')]
TMAP_S = 'gx:Brush ' + ';'.join(f'{lo}:{hi}={c}' for lo, hi, c, _, _ in TMAP) + ';default=rgba(0,0,0,0.0);'
TMAP_T = 'gx:Brush ' + ';'.join(f'{lo}:{hi}={c}' for lo, hi, _, c, _ in TMAP) + ';default=#ffe066;'


def zones_page():
    p = G.Page('ALT_V73_Zones', 'Zone temperature & humidity — AETERLINK Sense-T / AirPlug (ready)', (1920, 1080)); p.header()
    FX, FY = 10, 136
    R = json.load(open(os.path.join(OUT, 'px', 'img', 'v73_floor_rooms.json')))
    FW, FH = R['size']
    ximg(p, FX, FY, 'v73_floor.png', FW, FH, bottom=True)
    lbl(p, FX, 80, 900, 'LEVEL 01 — reference floor (12 zones).  Room colour = live zone temperature, card = Sense-T average T / RH.', 10, TXT, True)
    for i, (lo, hi, _, c, t) in enumerate(TMAP):
        p.rect(FX + 960 + i * 92, 84, 16, 12, fill=c, stroke=c, pen=1.0); lbl(p, FX + 980 + i * 92, 80, 76, t, 8, TXT)
    for code, room, srv in ZONES:
        x0, y0, x1, y1 = R['rooms'][code]['rect']
        t, h, oos = f'ZoneTemperatureAvg_{code}', f'ZoneHumidityAvg_{code}', f'ZoneOutOfService_{code}'
        o = p.ord(t)
        p.el.append(f'<BoundLabel layout="{FX + x0 + 2:.1f},{FY + y0 + 2:.1f},{x1 - x0 - 4:.1f},{y1 - y0 - 4:.1f}" background="rgba(0,0,0,0.0)" border="1.0 solid #0b0e11">\n'
                    f'  <BoundLabelBinding ord={quoteattr(o)} popupEnabled="true" statusEffect="none">\n    <ObjectToString name="text" format=""/>\n'
                    f'    <INumericToSimple name="background" map="{TMAP_S}"/>\n  </BoundLabelBinding>\n</BoundLabel>')
        p.map.append((t, o, f'{room} temperature colour', 'display (room colour)'))
        cw, ch = (132, 64) if code != '01_0112' else (240, 22)
        cx = FX + (x0 + x1) / 2 - cw / 2; cy = FY + (y0 + y1) / 2 - ch / 2 + (8 if code != '01_0112' else 0)
        if code == '01_0112':
            p.rect(cx, cy, cw, ch, fill='rgba(11,14,17,0.82)', stroke='#5dade2', pen=1.0)
            lbl(p, cx + 4, cy + 1, 70, room, 8, 'white', True, h=20)
            val(p, cx + 76, cy + 2, 76, t, f'{room} temperature', h=18, size=9, fmt='%out.value%')
            val(p, cx + 156, cy + 2, 64, h, f'{room} humidity', h=18, size=8, fg='#8fd3ff')
            status_led(p, cx + cw - 16, cy + 4, oos, f'{room} sensor out of service', 'warn')
            continue
        p.rect(cx, cy, cw, ch, fill='rgba(11,14,17,0.82)', stroke='#5dade2', pen=1.0)
        lbl(p, cx + 4, cy + 1, cw - 24, f'{room}', 8, 'white', True, h=16)
        lbl(p, cx + 4, cy + 14, cw - 8, f'{code.replace("_", "-")} · {srv}', 7, '#8fa3b5', h=13)
        val(p, cx + 4, cy + 28, 70, t, f'{room} temperature', h=20, size=11, fmt='%out.value%')
        p.el[-1] = p.el[-1].replace('foreground="#ffe066"', 'foreground="white"').replace('<ObjectToString', f'<INumericToSimple name="background" map="{TMAP_T}"/>\n    <ObjectToString')
        val(p, cx + 78, cy + 28, 50, h, f'{room} humidity', h=20, size=9, fg='#8fd3ff')
        status_led(p, cx + cw - 18, cy + 3, oos, f'{room} sensor out of service', 'warn')
        p.map[-1] = p.map[-1]
    # ---- right: table + settings + gateway
    X = 1522
    panel(p, X, 136, 388, 22 + 13 * 26 + 8, 'ZONES (Sense-T average)')
    for j, (t, w) in enumerate((('Zone', 150), ('°C', 70), ('%RH', 66), ('Alarm', 90))):
        p.label(X + 4 + sum((150, 70, 66, 90)[:j]), 158, w - 4, 20, t, 8, True, 'white', '#2c3e50', 'center')
    for i, (code, room, srv) in enumerate(ZONES):
        y = 182 + i * 26
        p.label(X + 4, y, 146, 22, f' {room}', 8, True, 'white', '#1b2631', 'left')
        val(p, X + 154, y + 1, 66, f'ZoneTemperatureAvg_{code}', f'{room} T', h=20, size=9)
        p.el[-1] = p.el[-1].replace('foreground="#ffe066"', 'foreground="white"').replace('<ObjectToString', f'<INumericToSimple name="background" map="{TMAP_T}"/>\n    <ObjectToString')
        val(p, X + 224, y + 1, 62, f'ZoneHumidityAvg_{code}', f'{room} RH', h=20, size=9, fg='#8fd3ff')
        val(p, X + 290, y + 1, 42, f'Zone_{code}_TempHighAlarm', f'{room} hot', h=20, size=7, bool_c=(FLT, OKC), fmt='HOT')
        val(p, X + 334, y + 1, 42, f'Zone_{code}_RHHighAlarm', f'{room} humid', h=20, size=7, bool_c=(WARN, OKC), fmt='RH')
    y = 136 + 22 + 13 * 26 + 18
    panel(p, X, y, 388, 22 + 8 * 23 + 8, 'AVERAGE BY SERVING UNIT')
    rows(p, X, y + 24, 388, [('AHU-01 zones °C', 'Zone_AHU01_AvgTemp'), ('AHU-01 zones %RH', 'Zone_AHU01_AvgRH'), ('AHU-02 zones °C', 'Zone_AHU02_AvgTemp'),
                             ('AHU-02 zones %RH', 'Zone_AHU02_AvgRH'), ('FCU zones °C', 'Zone_FCU_AvgTemp'), ('FCU zones %RH', 'Zone_FCU_AvgRH'),
                             ('OAU-01 zones °C', 'Zone_OAU01_AvgTemp'), ('OAU-01 zones %RH', 'Zone_OAU01_AvgRH')], lw=220, rh=23)
    y2 = y + 22 + 8 * 23 + 18
    panel(p, X, y2, 388, 1072 - y2, 'AIRPLUG GATEWAY & SETTINGS')
    rows(p, X, y2 + 24, 388, [('Gateway (BACnet)', 'AirPlug_GatewayOnline', {'bool_c': (RUN, FLT)}), ('Comfort band low °C', 'Zone_TempLow', {'action': True, 'fg': '#7dcea0'}),
                              ('Comfort band high °C', 'Zone_TempHigh', {'action': True, 'fg': '#7dcea0'}), ('Over-temp alarm °C', 'Zone_TempAlarmHigh', {'action': True, 'fg': '#7dcea0'}),
                              ('High RH alarm %', 'Zone_RHAlarmHigh', {'action': True, 'fg': '#7dcea0'})], lw=220, rh=23)
    yy = FY + FH + 8
    panel(p, FX, yy, 1500, 1072 - yy, 'SENSE-T / AIRPLUG INTEGRATION (prepared)')
    for i, t in enumerate(('Each zone has AirPlug-named points: ZoneTemperatureAvg_<floor>_<zone>, ZoneHumidityAvg_<floor>_<zone>, ZoneOutOfService_<floor>_<zone> '
                           '(same object names as the AirPlug gateway BACnet AVs, e.g. ZoneTemperatureAvg_05_0101).',
                           'Go-live: add the AirPlug gateway to the BACnet network, discover the AVs and link each proxy point out → in10 of the matching zone point '
                           '(replaces the simulation ramp), or map the proxies directly with the same names. Alarms, colours and averages then work unchanged.',
                           'White pucks on the plan = Sense-T sensor positions (1 per zone, wall mounted ~1.5 m). Add zones by copying a Zone folder and a room card.')):
        lbl(p, FX + 10, yy + 24 + i * 22, 1480, t, 8, TXT, h=20)
    return p


# ================================================================ faceplates: tower + fan cell
def fp_cell(c):
    tw = c[:4]; nm = CN[c]
    p = fp(f'ALT_V73_FP_{c}', f'{nm} — fan cell + variable speed drive', (620, 800))
    ximg(p, 16, 40, 'vsd_drive.png', 50, 106)
    rows(p, 80, 44, 530, [('Start command', f'{c}StartCmd', {'bool_c': (RUN, OFF)}), ('Run status (VFD)', f'{c}RunProof', {'bool_c': (RUN, OFF)}),
                          ('HOA in AUTO', f'{c}InAuto', {'bool_c': (RUN, WARN)}), ('Service (click)', f'{c}_ServiceIsolate', {'action': True}),
                          ('Runtime h', f'{c}_RuntimeHours')], lw=240, rh=21)
    panel(p, 10, 158, 600, 22 + 15 * 22 + 6, 'VARIABLE SPEED DRIVE (one per cell)')
    drive_rows(p, 10, 180, 600, c)
    y = 180 + 15 * 22 + 14
    panel(p, 10, y, 600, 22 + 6 * 22 + 6, 'FAULTS & PROTECTION')
    rows(p, 10, y + 22, 600, [('VFD fault (DI)', f'{c}VfdFault', {'bool_c': (FLT, OKC)}), ('Fan vibration switch', f'{c}VibrationAlarm', {'bool_c': (FLT, OKC)}),
                              ('Motor overload / isolator', f'{c}Fault', {'bool_c': (FLT, OKC)}), ('Failed to prove (latched)', f'{c}_FailAlarm', {'bool_c': (FLT, OKC)}),
                              ('Not in AUTO', f'{c}_NotInAutoAlarm', {'bool_c': (WARN, OKC)}), ('Tower command (both cells)', f'{tw}StartCmd', {'bool_c': (RUN, OFF)})], lw=330, rh=22)
    p.fire(10, 764, 160, 26, f'RESET {nm}', f'{c}ResetFire', f'{nm} reset')
    lbl(p, 180, 766, 430, 'cell speed = common CDS PID after the initial-speed hold, limited by MIN / MAX', 8, '#c9d3dd')
    return p


def fp_ct(u):
    p = fp(f'ALT_V71_FP_{u}', f'{u} — cooling tower (2 fan cells), valves, basin', (620, 860))
    w, h = SPR['v73_ct2_off']['size']
    ximg_bool(p, 14, 40, w * 0.8, h * 0.8, f'{u}RunProof', 'v73_ct2_on.gif', 'v73_ct2_off.png', f'{u} image')
    rows(p, 180, 44, 430, [('Tower command', f'{u}StartCmd', {'bool_c': (RUN, OFF)}), ('Proven (any cell)', f'{u}RunProof', {'bool_c': (RUN, OFF)}),
                           ('Healthy', f'{u}Healthy', {'bool_c': (RUN, FLT)}), ('Both cells healthy', f'{u}_CellsHealthy', {'bool_c': (RUN, WARN)}),
                           ('Failed (latched)', f'{u}FailLatch', {'bool_c': (FLT, OKC)}), ('Outlet MV failed (latched)', f'{u}_MVFailLatchedAlarm', {'bool_c': (FLT, OKC)}),
                           ('Runtime h', f'{u}_RuntimeHours')], lw=230, rh=22)
    panel(p, 10, 206, 600, 22 + 5 * 22 + 6, 'FAN CELLS (click for the cell VSD)')
    for j, k in enumerate(('01', '02')):
        c = f'{u}_{k}'; x = 180 + j * 215
        p.label(x, 230, 210, 20, f'{CN[c]}  ⊞', 9, True, 'white', '#5b3a1a', 'center', popup=f'file:^px/ALT_V73_FP_{c}.px', ptitle=CN[c])
        for i, (t, pt, kw) in enumerate(((None, f'{c}RunProof', {'bool_c': (RUN, OFF)}), (None, f'{c}SpeedCmd', {}), (None, f'{c}_FanSpeedHz', {}), (None, f'{c}_kW', {}))):
            val(p, x, 252 + i * 22, 210, pt, f'{CN[c]} {pt}', h=20, size=9, **kw)
    for i, t in enumerate(('Run', 'Speed', 'Output Hz', 'Power')):
        lbl(p, 20, 251 + i * 22, 150, t, 9, '#c9d3dd')
    y = 206 + 22 + 5 * 22 + 14
    panel(p, 10, y, 600, 22 + 14 * 22 + 6, 'WATER & BASIN (TT in / out, LT, LSL / LSLL / LSH)')
    rows(p, 10, y + 22, 600, [('Entering water TT (hot)', f'{u}_InletTemp'), ('Leaving water TT (cold)', f'{u}_OutletTemp'), ('Range', f'{u}_Range'),
                              ('Approach to OA wet bulb', f'{u}_Approach'), ('Basin level LT', f'{u}_BasinLevel'),
                              ('Make-up valve', f'{u}_MakeupValveCmd', {'bool_c': (RUN, OFF)}), ('Level LOW-LOW (fans stop, tower isolated)', f'{u}BasinLowLowLevelAlarm', {'bool_c': (FLT, OKC)}),
                              ('Low-low float switch', f'{u}_LowLowLevelSwitch', {'bool_c': (FLT, OKC)}), ('Level LOW', f'{u}BasinLowLevelAlarm', {'bool_c': (FLT, OKC)}),
                              ('Level HIGH', f'{u}BasinHighLevelAlarm', {'bool_c': (WARN, OKC)}), ('Level HIGH-HIGH / overflow', f'{u}BasinHighHighLevelAlarm', {'bool_c': (FLT, OKC)}),
                              ('High level float switch', f'{u}_HighLevelSwitch', {'bool_c': (WARN, OKC)}), ('Low level float switch', f'{u}_LowLevelSwitch', {'bool_c': (FLT, OKC)}),
                              ('LOW-LOW trip / reset %', 'CT_LevelLowLowPct', {'action': True, 'fg': '#7dcea0'})], lw=360, rh=22)
    y2 = y + 22 + 14 * 22 + 14
    panel(p, 10, y2, 600, 22 + 4 * 22 + 6, 'MOTORISED VALVES (butterfly, on/off)')
    rows(p, 10, y2 + 22, 600, [('Inlet MV command / end switch', f'{u}ValveOpenCmd', {'bool_c': (RUN, OFF)}), ('', f'{u}ValveOpenProof', {'bool_c': (RUN, OFF)}),
                               ('Outlet MV command / feedback', f'{u}_OutletMVCmd', {'bool_c': (RUN, OFF)}), ('', f'{u}_OutletMVFb')], lw=360, rh=22)
    p.fire(10, y2 + 22 + 4 * 22 + 14, 140, 26, f'RESET {u}', f'{u}ResetFire', f'{u} reset')
    return p


# ================================================================ drives / valves / meters (V7.3 lists)
PLANT_VSD = ['CHP01', 'CHP02', 'CDP01', 'CDP02', 'CT01_01', 'CT01_02', 'CT02_01', 'CT02_02']
AIR_VSD = G71.AIR_VSD


def drives_page():
    p = G.Page('ALT_V71_Drives', 'Variable speed drives — status, diagnostics, MIN / MAX speed (tower: one drive per fan cell)', (1920, 1080)); p.header()
    cols = [('Drive', 150), ('Run', 90), ('Speed cmd', 110), ('Hz', 100), ('Volts', 100), ('Amps', 100), ('kW', 100), ('Heatsink', 100), ('Fault code', 100),
            ('VFD fault', 110), ('Over-temp', 110), ('MIN %', 100), ('MAX %', 100), ('Runtime h', 110), ('Detail', 90)]
    x = 20
    for t, w in cols:
        p.label(x, 84, w - 4, 26, t, 10, True, 'white', '#2c3e50', 'center'); x += w
    for r, u in enumerate(PLANT_VSD + AIR_VSD):
        plant = u in PLANT_VSD
        y = 114 + r * 32 + (12 if not plant else 0)
        cmd = f'{u}SpeedCmd' if plant else f'{u}_SpeedCmd'
        hz = f'{u}_FanSpeedHz' if u.startswith('CT') else f'{u}_SpeedFeedbackHz'
        run = f'{u}RunProof' if plant else f'{u}_Status'
        flt = f'{u}VfdFault' if plant else f'{u}_VfdFault'
        fpn = (f'ALT_V73_FP_{u}' if u.startswith('CT') else f'ALT_V71_FP_{u}') if plant else f'ALT_V71_FP_VSD_{u}'
        title = CN.get(u, u)
        pts = [None, (run, {'bool_c': (RUN, OFF)}), (cmd, {}), (hz, {}), (f'{u}_VfdOutputV', {}), (f'{u}_Amps', {}), (f'{u}_kW', {}), (f'{u}_VfdTemp', {}),
               (f'{u}_VfdFaultCode', {}), (flt, {'bool_c': (FLT, OKC)}), (f'{u}_VfdOverTempAlarm', {'bool_c': (WARN, OKC)}),
               (f'{u}_MinSpeed', {'action': True, 'fg': '#7dcea0'}), (f'{u}_MaxSpeed', {'action': True, 'fg': '#7dcea0'}), (f'{u}_RuntimeHours', {}), None]
        x = 20
        for (t, w), pt in zip(cols, pts):
            if t == 'Drive':
                bgc = '#5b3a1a' if u.startswith('CT') else ('#1b2631' if plant else '#1b3a2f')
                p.label(x, y, w - 4, 26, '  ' + title, 10, True, 'white', bgc, 'left', popup=f'file:^px/{fpn}.px', ptitle=title)
            elif t == 'Detail':
                p.label(x, y, w - 4, 26, 'open ⊞', 9, True, '#8fd3ff', '#1f252c', 'center', popup=f'file:^px/{fpn}.px', ptitle=title)
            else:
                val(p, x, y + 2, w - 4, pt[0], f'{title} {t}', h=22, size=10, **pt[1])
            x += w
    ximg(p, 1760, 600, 'vsd_drive.png', 120, 254)
    y = 114 + 15 * 32 + 30
    panel(p, 20, y, 1700, 180, 'HOW MIN / MAX IS APPLIED')
    for i, t in enumerate(('speed = MIN( MAX(control output, MIN speed), MAX(MAX speed, MIN speed) ) — after the PID / reset / fail-safe selection, before the start gate.',
                           'Cooling towers: every fan cell (CT-01/01, CT-01/02, CT-02/01, CT-02/02) has its own VSD, MIN / MAX and faults; a failed cell drops out and the other',
                           'cell of the tower keeps running. Cell speed = common CDS PID output (direct acting) after the SOO initial-speed hold.',
                           'CPEF01 ignores MAX during fire alarm (100 %). Values are writable (<unit>_MinSpeed / _MaxSpeed): click a green value to set.',
                           'Standard drive graphic is original; replace shared/px/img/vsd_drive.png with the project drive photo if required.')):
        lbl(p, 30, y + 26 + i * 28, 1680, t, 10, TXT)
    return p


VALVES = [v for v in G71.VALVES if not v[0].startswith('CHW bypass')] + [
    ('CHW bypass (min flow)', 'CHW min-flow bypass (MOD) + isolation + manual loop', 'MOD 0-100 %', 'CHW_BypassValveCmd', 'CHW_BypassValveFeedback', None),
    ('CHW manual bypass', 'Loop around the MOD valve (maintenance)', 'Manual (position sw)', None, 'CHW_BypassManualOpen', 'CHW_BypassManualOpenAlarm'),
    ('CHW fill (make-up)', 'Expansion tank / CHWR (RPZ + meter)', 'Solenoid on/off', 'CHW_FillValveCmd', None, 'CHW_FillLockoutAlarm'),
    ('CT01 make-up', 'Tower 01 basin', 'Solenoid on/off', 'CT01_MakeupValveCmd', None, None),
    ('CT02 make-up', 'Tower 02 basin', 'Solenoid on/off', 'CT02_MakeupValveCmd', None, None),
    ('CDW bleed-off', 'CDWR riser -> drain', 'Solenoid on/off', 'CT_BleedValveCmd', None, None)]


def valves_page():
    p = G.Page('ALT_V71_Valves', 'Motorised valves (butterfly) — type, command, feedback, alarms', (1920, 1080)); p.header()
    cols = [('Valve', 250), ('Location', 360), ('Actuator type', 200), ('Command', 170), ('Feedback / proof', 170), ('Alarm', 190)]
    x = 20
    for t, w in cols: p.label(x, 80, w - 4, 24, t, 10, True, 'white', '#2c3e50', 'center'); x += w
    for r, (v, loc, typ, c, f, a) in enumerate(VALVES):
        y = 106 + r * 27
        x = 20
        mod = '%' in typ
        p.label(x, y, 246, 24, '  ' + v, 9, True, 'white', '#1b2631', 'left'); x += 250
        lbl(p, x + 4, y + 2, 352, loc, 9, TXT); x += 360
        p.label(x, y, 196, 24, typ, 9, True, '#0b0e11', '#7dcea0' if mod else ('#8fd3ff' if 'on/off' in typ else '#d7bde2'), 'center'); x += 200
        for pt, what in ((c, 'command'), (f, 'feedback')):
            if pt: val(p, x, y + 1, 166, pt, f'{v} {what}', h=22, size=9)
            else: lbl(p, x + 4, y + 2, 166, '—', 9, '#8fa3b5')
            x += 170
        if a: val(p, x, y + 1, 186, a, f'{v} alarm', h=22, size=9, bool_c=(FLT, OKC))
        else: lbl(p, x + 4, y + 2, 186, 'end switch (DI)' if f and not c is None and 'ISO' in typ else '—', 9, '#c9d3dd')
    x0 = 1380
    panel(p, x0, 80, 530, 350, 'SYMBOLS (V7.3 butterfly valves)')
    for i, (nm, t) in enumerate((('v73_bfv_onoff_h', 'Butterfly + on/off actuator (red)'), ('v73_bfv_mod_h', 'Butterfly + modulating actuator (green)'),
                                 ('v73_bfv_man_h', 'Butterfly, manual gear + handwheel'), ('v73_gate_h', 'Gate valve (manual bypass loop)'),
                                 ('v73_sol_h', 'Solenoid valve (make-up / fill / bleed)'), ('v73_rpz', 'RPZ backflow preventer (CHW fill)'))):
        sprite(p, nm, x0 + 60, 136 + i * 50)
        lbl(p, x0 + 120, 122 + i * 50, 400, t, 9, TXT)
    y = 106 + len(VALVES) * 27 + 10
    panel(p, 20, y, 1890, 1072 - y, 'SELECTION RULE')
    for i, t in enumerate(('On/off (2-position) = isolation / sequencing: chiller inlets, pump suction + discharge (with the pump), tower inlets / outlets (latched on failure).',
                           'Modulating 0-100 % = controls a process variable: evaporator flow limit (FCV), condenser head pressure (HPV), CHW min-flow bypass (on the sum of evaporator flows).',
                           'Bypass: isolation butterflies (manual) both sides of the MOD valve + normally-closed manual bypass loop for maintenance (position switch alarm). No bypass flow meter.')):
        lbl(p, 34, y + 26 + i * 22, 1860, t, 9, TXT)
    return p


G71.FLOWS[:] = [f for f in G71.FLOWS if f[1] != 'CHW_BypassFlow'] + [('CHW fill (make-up)', 'CHW_FillFlow'), ('CHW fill volume', 'CHW_FillVolume')]
G71.PLANT_VSD[:] = PLANT_VSD


def meters_page():
    """V7.1 meters page with tighter rows: 12 flow meters (fill meter added, bypass meter removed) and 10 sub-meters (4 tower cells)"""
    import inspect
    src = inspect.getsource(G71.meters_page).replace('rows(p, 10, 534, 620, FLOWS, lw=300, rh=29)', 'rows(p, 10, 534, 620, FLOWS, lw=300, rh=24)')
    src = src.replace('yy = 560 + r * 30', 'yy = 560 + r * 27').replace("'  ' + e[0]", "'  ' + CN.get(e[0], e[0])")
    ns = dict(G71.__dict__); ns['CN'] = CN
    exec(src, ns)
    return ns['meters_page']()


def energy_dashboard():
    _as = G71.ashrae_scale
    G71.ashrae_scale = lambda p, x, y, w, h, point, title='', compact=False: gauge_panel(p, x, y, w, h, point, 'PLANT kW/RT — GAUGE')
    try:
        src = inspect.getsource(G.energy_dashboard)
        src = src.replace("tiles = [('Plant kW/RT (live)', 'Plant_kW_per_RT', kw_rt_map, 26), ", "tiles = [").replace('w = 226', 'w = 262')
        assert 'Plant kW/RT (live)' not in src and 'w = 262' in src
        ns = {}; exec(src, G.__dict__, ns); _ed = G.energy_dashboard; G.energy_dashboard = ns['energy_dashboard']
        try:
            p = G71.energy_dashboard()   # live kW/RT tile removed: the gauge panel already shows the value (no duplicate)
        finally:
            G.energy_dashboard = _ed
    finally:
        G71.ashrae_scale = _as
    return p


def plant_detail():
    """V7 'Pools' page: the bypass flow meter no longer exists -> show the bypass PV (sum of evaporator flows)"""
    G7.PATH['CHW_BypassFlow'] = G7.PATH['CHW_EvapFlowTotal']
    try:
        p = G7.plant_detail()
    finally:
        G7.PATH.pop('CHW_BypassFlow', None)
    p.el = [e.replace('>Bypass flow<', '>Evap flow<').replace('"Bypass flow"', '"Evap flow (bypass PV)"') for e in p.el]
    p.map = [('CHW_EvapFlowTotal' if m[0] == 'CHW_BypassFlow' else m[0],) + tuple(m[1:]) for m in p.map]
    return p


# ================================================================ main
def build_sprites(sdir):
    SPR.update(json.load(open(os.path.join(sdir, 'sprites73.json'))))
    # left-mirrored variants for vertical pipes that must keep their right side free
    for n in ('v73_gate_v', 'v73_fm_v', 'v73_bfv_man_v'):
        im = Image.open(os.path.join(sdir, n + '.png')); w, h = im.size
        im.transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(sdir, n + 'l.png'))
        SPR[n + 'l'] = {'size': [w, h], 'anchors': {k: [w - a[0], a[1]] for k, a in SPR[n]['anchors'].items()}}
    for f in os.listdir(sdir):
        if f.endswith(('.png', '.gif')): shutil.copy(os.path.join(sdir, f), os.path.join(OUT, 'px', 'img', f))


if __name__ == '__main__':
    bog, G7.KITDIR, OUT, regdir, sdir = sys.argv[1:6]
    G71.OUT = OUT
    G7.PATH.update(G7.load_paths(bog))
    G.FOLDER = {n: p.rsplit('/', 1)[0].replace('/ChillerPlant/', '').replace('/ChillerPlant', '') for n, p in G7.PATH.items()}
    G.STATION_NAME = STATION
    G.PAGES = PAGES; G7.PAGES = PAGES
    H, Al = (G.read_reg(os.path.join(regdir, f)) for f in ('V7_HISTORY_REGISTER.csv', 'V7_ALARM_REGISTER.csv'))
    os.makedirs(os.path.join(OUT, 'px', 'img'), exist_ok=True)
    build_sprites(sdir)
    shutil.copy(os.path.join(os.path.dirname(os.path.abspath(bog)), 'gfx72', 'px', 'img', 'vsd_drive.png'), os.path.join(OUT, 'px', 'img', 'vsd_drive.png'))
    only = os.environ.get('ONLY')
    pages = [plant_page(), chillerplant_page(), ctplant_page(), plant3d_page(), G71.chillers_page(), plant_detail(), drives_page(), valves_page(),
             meters_page(), G71.schedules_page(), G71.dark_page(G.optimization()), energy_dashboard(), G71.dark_page(G.energy()),
             G71.dark_page(G.alarms_history()), G71.dark_page(G.simulation()),
             G7.airside_page(), zones_page(), G7.ahu_page('AHU01'), G7.ahu_page('AHU02'), G7.oau_page('OAU01'), G7.fcu_page(), G7.vent_page()]
    pages += [G71.fp_ch('01'), G71.fp_ch('02')] + [G71.fp_pump(u) for u in ('CHP01', 'CHP02', 'CDP01', 'CDP02')] + [fp_ct('CT01'), fp_ct('CT02')]
    pages += [fp_cell(c) for _, c in CELLS]
    pages += [G71.fp_air_vsd(u) for u in AIR_VSD] + [G71.fp_btu(), G71.fp_power(), G71.fp_flow(), G71.fp_oa()]
    if only: pages = [q for q in pages if any(o in q.name for o in only.split(','))]
    G71.FACEPLATES[:] = [q.name for q in pages if q.name.startswith(('ALT_V71_FP_', 'ALT_V73_FP_'))]
    rows_ = G71.build(pages, OUT, H, Al)
    with open(os.path.join(OUT, 'V7_3_GRAPHIC_POINT_MAPPING.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows_[0].keys())); w.writeheader(); w.writerows(rows_)
    print('bindings', len(rows_), 'distinct points', len({r['Point'] for r in rows_ if r['Point'] != '(BQL)'}), 'images', len(G71.IMG))
