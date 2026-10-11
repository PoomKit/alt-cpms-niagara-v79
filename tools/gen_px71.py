"""V7.1 Px graphics (dark theme everywhere) for ALT_CP_Ref_V7_1.

 * Plant page re-drawn nozzle-accurate: pipes are ONE rendered PNG layer (shaded cylinders, bends, flanges, flow arrows) in the
   user colour standard CHWS blue / CHWR light blue / CDWS yellow / CDWR orange; kitPxGraphics chillers, pumps, towers,
   valves, sensors are placed on the measured nozzles (Chiller_Generic ends y+45/y+55, Pump_Base suction/discharge,
   CoolingTower_PushThru inlet y+64.5 / outlet y+104.5).
 * PT before/after every pump, TT entering/leaving every chiller (both barrels) and every tower, CT HIGH / HIGH-HIGH level.
 * Faceplate pop-ups (ALT_V71_FP_*.px) for chillers, VSDs, power meters, BTU meter, flow meters, OA sensor.
 * New pages: Chillers, Drives (VSD min/max), Meters, Schedules (native weekly scheduler pop-ups, set 1/2, rotation), 3D plant.
 * Old V6 pages (Optimisation, Energy, Alarms, Simulation) converted to the dark theme; Energy dashboard with ASHRAE kW/ton scale.
usage: gen_px71.py v71.bog kit/kitPxGraphics-wb outdir
"""
import sys, os, re, csv, zipfile, shutil
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_px7 as G7
from gen_px7 import pic, pic_bool, pic_pct, val, lbl, panel, rows, status_led, BG, PANEL, EDGE, LBL, VAL, TXT, RUN, OFF, FLT, WARN, KG
import gen_px as G
import pipes71

OKC = '#1f6f43'
STATION = 'ALT_CP_Ref_V7_2'
PAGES = [('ALT_V7_Plant', 'Plant'), ('ALT_V71_Plant3D', 'Plant 3D'), ('ALT_V71_Chillers', 'Chillers'), ('ALT_V7_PlantDetail', 'Pumps/Towers'),
         ('ALT_V71_Drives', 'Drives (VSD)'), ('ALT_V71_Valves', 'Valves'), ('ALT_V71_Meters', 'Meters'), ('ALT_V71_Schedules', 'Schedules'), ('ALT_CP_Optimization', 'Optimisation'),
         ('ALT_CP_EnergyDashboard', 'Energy Dash'), ('ALT_CP_Energy', 'Energy/KPI'), ('ALT_CP_AlarmsHistory', 'Alarms'), ('ALT_CP_Simulation', 'Simulation'),
         ('ALT_V7_AirSide', 'Air Side'), ('ALT_V7_AHU01', 'AHU-01'), ('ALT_V7_AHU02', 'AHU-02'), ('ALT_V7_OAU01', 'OAU-01'), ('ALT_V7_FCU', 'FCU'),
         ('ALT_V7_Ventilation', 'Ventilation')]
FACEPLATES = []          # (name) of faceplate pop-up pages
OUT = None
IMG = []                 # generated images (relative to shared/px/img)
ASHRAE = [(0.0, 0.01, '#2c3440', '—'), (0.01, 0.75, '#1e8449', 'EXCELLENT < 0.75'), (0.75, 0.90, '#7dcea0', 'GOOD 0.75–0.90'),
          (0.90, 1.00, '#f4d03f', 'FAIR 0.90–1.00'), (1.00, 99.0, '#e74c3c', 'NEEDS IMPROVEMENT > 1.00')]
KWRT_MAP = 'gx:Brush ' + ';'.join(f'{lo}:{hi}={c}' for lo, hi, c, _ in ASHRAE) + ';default=#2c3440;'


# ================================================================ theme + header
def header(self):
    W, H = self.size
    self.rect(0, 0, W, H, fill=BG, stroke=BG, pen=1.0)
    if self.name.startswith('ALT_V71_FP_'):
        self.label(0, 0, W, 34, f'  {self.title}', 14, True, 'white', '#0b0e11')
        return
    self.label(0, 0, W, 40, f'  ALT Reference V7.2 — {self.title}', 18, True, 'white', '#0b0e11')
    self.label(W - 470, 8, 460, 24, 'REFERENCE SIMULATION – NOT PROJECT APPROVED', 10, True, '#263238', '#ffca28', 'center')
    n = len(PAGES); bw = (W - 8) / n
    for i, (name, title) in enumerate(PAGES):
        cur = name == self.name
        air = name.startswith('ALT_V7_A') or name in ('ALT_V7_OAU01', 'ALT_V7_FCU', 'ALT_V7_Ventilation')
        self.label(4 + i * bw, 44, bw - 4, 26, title, 8.5, True, 'white' if cur else '#cfd8dc',
                   '#1e88e5' if cur else ('#233a33' if air else '#2c3440'), 'center',
                   popup=None if cur else f'file:^px/{name}.px', ptitle=title)


G.Page.header = header
_init = G.Page.__init__


def _page_init(self, name, title, size=(1920, 1080)):
    _init(self, name, title, size)


G.Page.__init__ = _page_init
_button = G.Page.button


def _dark_button(self, *a, **k):
    _button(self, *a, **k)
    self.el[-1] = self.el[-1].replace('value="#00a000"', 'value="#1e8449"').replace('value="#546e7a"', 'value="#7b241c"') \
        .replace('value="white"', 'value="#2c3440"')
    if ' foreground=' not in self.el[-1].split('>')[0]:
        self.el[-1] = self.el[-1].replace('<Button ', '<Button foreground="white" ', 1)


G.Page.button = _dark_button
_lbl0 = G7.lbl


def _lbl(p, x, y, w, text, size=9, fg=LBL, bold=False, h=20, halign='left', bg=None):
    fg = {LBL: '#c9d3dd', '#566573': '#aab6c2'}.get(fg, fg)
    _lbl0(p, x, y, w, text, max(size, 8), fg, bold, h, halign, bg)


G7.lbl = _lbl
lbl = _lbl
G.Page.ord = G7._ord
G.Page.table = G7._table

BGMAP = {'white': PANEL, '#ffffff': PANEL, '#fafafa': PANEL, '#f7f9fa': PANEL, '#eceff1': BG, '#cfd8dc': '#2c3440', '#c8e6c9': '#1d3b2a',
         '#e8f5e9': '#1d3b2a', '#e3f2fd': '#16324a', '#bbdefb': '#16324a', '#fffde7': '#3d3420', '#ffe0b2': '#3d3420', '#90a4ae': EDGE}
FGMAP = {'black': TXT, '#37474f': LBL, '#263238': TXT, '#455a64': LBL, '#546e7a': LBL, '#607d8b': LBL}
STROKE = {'#78909c': EDGE, '#90a4ae': EDGE, '#607d8b': EDGE, '#37474f': EDGE, '#eceff1': BG}


def darken(el):
    tag = el.split()[0][1:]
    def sub(attr, table, s):
        return re.sub(attr + r'="([^"]+)"', lambda m: f'{attr}="{table.get(m.group(1).lower(), m.group(1))}"', s)
    el = sub('fill', BGMAP, el); el = sub('stroke', STROKE, el)
    if tag in ('Label', 'Button'):
        el = sub('background', {**BGMAP, '#607d8b': '#2c3e50', '#455a64': '#2c3e50', '#263238': '#0b0e11'}, el)
        el = sub('foreground', FGMAP, el)
    if tag == 'BoundLabel':
        el = sub('foreground', {'black': VAL}, el)
        el = el.replace('border="1.0 solid #90a4ae"', f'border="1.0 solid {EDGE}"')
        if ' background=' not in el.split('>')[0]:
            el = el.replace('<BoundLabel ', '<BoundLabel background="#0b0e11" ', 1)
    el = re.sub(r'(<Brush name="(?:trueValue|falseValue)" value=")([^"]+)(")',
                lambda m: m.group(1) + {'#ffffff': '#1f2a33', 'white': '#1f2a33', '#cfd8dc': OFF, '#c8e6c9': OKC, '#e8f5e9': OKC}.get(m.group(2).lower(), m.group(2)) + m.group(3), el)
    el = re.sub(r'map="gx:Brush 0\.0:0\.65=#66bb6a[^"]*"', f'map="{KWRT_MAP}"', el)
    el = re.sub(r'(map="gx:Brush [^"]*)', lambda m: m.group(1).replace('#cfd8dc', '#2c3440').replace('#eceff1', '#2c3440'), el)
    if tag == 'Bargraph':
        el = el.replace('<Bargraph ', f'<Bargraph background="#0b0e11" foreground="{TXT}" ', 1)
    return el


def dark_page(p):
    p.el = [darken(e) for e in p.el]
    return p


# ================================================================ small helpers
def ximg(p, x, y, name, w, h, popup=None, ptitle='', bottom=False):
    o = f'file:^px/img/{name}'
    if bottom:                     # directly above the page background rect -> below every other widget
        p.el.insert(1, f'<Picture layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" image="{o}"/>')
    elif popup:
        p.el.append(f'<Label layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" image="{o}">\n  <PopupBinding ord={quoteattr(popup)} title={quoteattr(ptitle)}/>\n</Label>')
    else:
        p.el.append(f'<Picture layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" image="{o}"/>')
    if name not in IMG: IMG.append(name)


def hot(p, x, y, w, h, fp, title):
    """invisible click area -> faceplate pop-up"""
    p.el.append(f'<Label layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" text="">\n  <PopupBinding ord="file:^px/{fp}.px" title={quoteattr(title)}/>\n</Label>')


def tag(p, x, y, w, point, what, pre='', size=9, h=18, fg=VAL, **kw):
    fmt = (pre + ' ' if pre else '') + '%out.value%'
    val(p, x, y, w, point, what, h=h, size=size, fg=fg, fmt=fmt, **kw)


def isa(p, x, y, text, fill='#0b0e11', fg='#8fd3ff'):
    """ISA-style instrument bubble label (e.g. TT, PT, FT)."""
    p.label(x, y, 26, 14, text, 7, True, fg, fill, 'center')


# sensor placement on pipes (cx, cy = pipe centre; kit images measured)
def tt_top(p, cx, cy):
    pic(p, cx - 13.5, cy - 5 - 20, 'Sensors/sensor_pipe_welltemp2_hor_top.png')


def tt_bot(p, cx, cy):
    pic(p, cx - 13.5, cy + 5, 'Sensors/sensor_pipe_welltemp2_hor_bottom.png')


def pt_top(p, cx, cy):
    pic(p, cx - 14.5, cy - 5 - 60, 'Sensors/sensor_pipe_dp_hor_up_2.png')


def fm_h(p, cx, cy):
    pic(p, cx - 25, cy - 14.5, 'Sensors/sensor_pipe_wtrflowmtr_hor.png')


def fm_v(p, cx, cy):
    pic(p, cx - 14.5, cy - 25, 'Sensors/sensor_pipe_wtrflowmtr_vert.png')


def btu_h(p, cx, cy):
    pic(p, cx - 42.5, cy - 14.5, 'Sensors/sensor_watermtr_horz_largepipe.png')


def valve_h(p, cx, cy, point=None, what=''):
    pic(p, cx - 15, cy - 14.5, 'Valves/valve_2way_elec_bottom.png')
    if point: status_led(p, cx + 12, cy + 8, point, what, 'run')


def valve_v(p, cx, cy, point=None, what=''):
    pic(p, cx - 14.5, cy - 20, 'Valves/valve_2way_elec_left.png')
    if point: status_led(p, cx + 8, cy - 7, point, what, 'run')


def strainer_h(p, cx, cy):
    pic(p, cx - 15, cy - 14, 'Valves/valve_strainer_left.png')


def manual_h(p, cx, cy):
    pic(p, cx - 10, cy - 14, 'Valves/valve_manual_hor.png')


# ================================================================ plant page geometry (V7.2: full detail, header layout, 2100 x 1180)
PW, PH = 2100, 1180
CHP = {'01': (500, 440), '02': (500, 720)}                # Pump_Base_Left: suction (9, 44.5), discharge (24, 9)
CH = {'01': (830, 450), '02': (830, 720)}                 # Chiller_Generic 220x100: nozzles left/right at y+45 (upper) / y+55 (lower)
CDP = {'01': (1220, 560), '02': (1220, 830)}              # Pump_Base_Right: suction (100, 44.5), discharge (85, 9)
CT = {'01': (1560, 150), '02': (1840, 150)}               # CoolingTower_PushThru_Left: inlet (0, 64.5), outlet (0, 104.5)
X_BLD, X_DPT, X_BYP, Y_CHWS, Y_CHWR = 100, 118, 150, 196, 950
X_SUC, X_DIS, X_RIS = 430, 680, 740
X_CDR, X_CDS, X_CDSUC, Y_CDR, Y_CDWS = 1120, 1180, 1420, 140, 300
CT_DROP = {'01': 1500, '02': 1780}
X_CT2OUT = 1740
HW, EXT = 16, 30
C_CHWS, C_CHWR, C_CDWS, C_CDWR = '#5aa2ff', '#8fdcff', '#ffd84a', '#ffa550'
TANK_X = 385


def plant_pipes(name, W=PW, H=PH):
    L = pipes71.Layer(W, H)
    ev = lambda n, k: (CH[n][0] + 4, CH[n][1] + k)
    cd = lambda n, k: (CH[n][0] + 198, CH[n][1] + k)
    capv = lambda x, y: ((x, y), False)
    caph = lambda x, y: ((x, y), True)
    y_ch2i, y_ch2o, y_ch1i = CH['02'][1] + 55, CH['02'][1] + 45, CH['01'][1] + 55
    # ---------- CHW (branches first, headers on top -> tees)
    L.pipe([(X_BYP, Y_CHWR), (X_BYP, Y_CHWS)], 'chwr', flow=False)
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
    for a, d in (((X_BLD + 30, Y_CHWS), (-1, 0)), ((X_BLD + 30, Y_CHWR), (1, 0)), ((X_SUC, 880), (0, -1)), ((X_RIS, 330), (0, -1)), ((X_DIS, 620), (0, 1))):
        L.arrow(a, d, 9)
    # ---------- CDW
    for n, (x, y) in CH.items():
        L.pipe([cd(n, 45), (X_CDR, y + 45)], 'cdwr', flanges=[((x + 196, y + 45), True)], arrows_every=60)
    L.pipe([(X_CDR, y_ch2o + 12), (X_CDR, Y_CDR)], 'cdwr', w=HW, flow=False, flanges=[capv(X_CDR, y_ch2o + 12)])
    for n, (x, y) in CT.items():
        dx = CT_DROP[n]
        L.pipe([(dx, Y_CDR), (dx, y + 64.5), (x + 4, y + 64.5)], 'cdwr', flanges=[((x + 2, y + 64.5), True)], arrows_every=50)
    L.pipe([(X_CDR - EXT, Y_CDR), (CT_DROP['02'] + EXT, Y_CDR)], 'cdwr', w=HW, flow=False,
           flanges=[caph(X_CDR - EXT, Y_CDR), caph(CT_DROP['02'] + EXT, Y_CDR)])
    L.pipe([(CT['01'][0] + 4, CT['01'][1] + 104.5), (X_CDSUC, CT['01'][1] + 104.5)], 'cdws', flanges=[((CT['01'][0] + 2, CT['01'][1] + 104.5), True)], arrows_every=60)
    L.pipe([(CT['02'][0] + 4, CT['02'][1] + 104.5), (X_CT2OUT, CT['02'][1] + 104.5), (X_CT2OUT, Y_CDWS)], 'cdws',
           flanges=[((CT['02'][0] + 2, CT['02'][1] + 104.5), True)], arrows_every=50)
    for n, (x, y) in CDP.items():
        L.pipe([(X_CDSUC, y + 44.5), (x + 98, y + 44.5)], 'cdws', flanges=[((x + 100, y + 44.5), True)], arrows_every=50)
        L.pipe([(x + 85, y + 12), (x + 85, y - 20), (X_CDS, y - 20)], 'cdws', flanges=[((x + 85, y + 10), False)], arrows_every=80)
    for n, (x, y) in CH.items():
        L.shadow(x + 198, y + 50, X_CDS, y + 60)
        L.pipe([(X_CDS, y + 55), cd(n, 55)], 'cdws', flanges=[((x + 196, y + 55), True)], arrows_every=80)
    L.pipe([(X_CDS, y_ch1i - EXT), (X_CDS, CDP['02'][1] - 20 + EXT)], 'cdws', w=HW, flow=False,
           flanges=[capv(X_CDS, y_ch1i - EXT), capv(X_CDS, CDP['02'][1] - 20 + EXT)])
    L.pipe([(X_CDSUC, CT['01'][1] + 104.5 - EXT), (X_CDSUC, CDP['02'][1] + 44.5 + EXT)], 'cdws', w=HW, flow=False,
           flanges=[capv(X_CDSUC, CT['01'][1] + 104.5 - EXT), capv(X_CDSUC, CDP['02'][1] + 44.5 + EXT)])
    L.pipe([(X_CDSUC, Y_CDWS), (X_CT2OUT + EXT, Y_CDWS)], 'cdws', w=HW, flow=False, flanges=[caph(X_CT2OUT + EXT, Y_CDWS)])
    for a, d in (((X_CDR, 330), (0, -1)), ((1300, Y_CDR), (1, 0)), ((1620, Y_CDWS), (-1, 0)), ((X_CDSUC, 700), (0, 1)), ((X_CDS, 690), (0, -1))):
        L.arrow(a, d, 9)
    os.makedirs(os.path.join(OUT, 'px', 'img'), exist_ok=True)
    L.render(os.path.join(OUT, 'px', 'img', name))
    if name not in IMG: IMG.append(name)


def valve_top(p, cx, cy):
    pic(p, cx - 15, cy - 24, 'Valves/valve_2way_elec_top.png')


def pct_tag(p, x, y, point, what, w=54):
    val(p, x, y, w, point, what, h=16, size=8, fg='#7dcea0', fmt='%out.value%')


def hdr_text(p, x, y, text, col, w=None):
    p.label(x, y, w or 9 * len(text), 16, text, 9, True, col, None, 'left')


def kwrt_val(p, x, y, w, point, what, h=18, size=9):
    val(p, x, y, w, point, what, h=h, size=size, fg='white')
    p.el[-1] = p.el[-1].replace('<ObjectToString', f'<INumericToSimple name="background" map="{KWRT_MAP}"/>\n    <ObjectToString')


def card(p, x, y, w, title, fp_, run_pt, items, head, reset=None, lw=None, rh=21):
    """Equipment card: coloured title (click = faceplate) + RESET + run LED, then label / value rows."""
    h = 24 + rh * len(items)
    p.rect(x, y, w, h, fill='#161c22', stroke='#4a5866', pen=1.0)
    p.label(x, y, w, 22, f'  {title}  ⊞', 10, True, 'white', head, 'left', popup=f'file:^px/{fp_}.px', ptitle=title)
    bx = x + w - 22
    if run_pt: status_led(p, bx + 4, y + 4, run_pt, f'{title} running', 'run')
    if reset: p.fire(bx - 70, y + 2, 66, 18, 'RESET', reset, f'Reset {title}')
    lw = lw or int(w * 0.44)
    for i, it in enumerate(items):
        t, pt = it[0], it[1]; kw = it[2] if len(it) > 2 else {}
        lbl(p, x + 6, y + 24 + i * rh, lw - 6, t, 9, '#c9d3dd')
        val(p, x + lw, y + 25 + i * rh, w - lw - 5, pt, f'{title} {t}', h=rh - 3, size=9, **kw)
    return h


def plant_page():
    p = G.Page('ALT_V7_Plant', 'Chiller Plant', (PW, PH)); p.header()
    plant_pipes('v71_plant_pipes.png')
    ximg(p, 0, 0, 'v71_plant_pipes.png', PW, PH, bottom=True)          # pipe layer UNDER every widget (never blocks clicks)
    G7.kpi_strip(p)
    hot(p, 8 + 116 * 10, 80, 224, 48, 'ALT_V71_FP_OA', 'Outdoor air sensor')
    # ================= CHW side
    p.rect(16, 176, X_BLD - 20, 790, fill='#18212b', stroke='#5d6d7e', pen=2.0)
    p.label(16, 186, X_BLD - 20, 22, 'BUILDING', 10, True, TXT, None, 'center')
    p.label(20, 210, X_BLD - 28, 20, 'Air side ⊞', 9, True, '#8fd3ff', '#1f2a36', 'center', popup='file:^px/ALT_V7_AirSide.px', ptitle='Air side')
    for i, (t, pt, kw) in enumerate((('Cooling calls', 'AirSide_CoolingCalls', {}), ('CHW requests', 'AirSide_ChwRequests', {}),
                                      ('Units running', 'AirSide_UnitsRunning', {}), ('Reset %', 'PlantResetPct', {}),
                                      ('Fire alarm', 'FireModeActive', {'bool_c': (FLT, OKC)}), ('CHW ΔP', 'CHWDP', {}), ('ΔP SP', 'CHWDP_Setpoint_ACTIVE', {}))):
        lbl(p, 20, 240 + i * 44, 76, t, 8, '#c9d3dd')
        val(p, 20, 258 + i * 44, 72, pt, f'Building {t}', h=20, size=9, **kw)
    btu_h(p, 290, Y_CHWS); hot(p, 250, Y_CHWS - 15, 85, 30, 'ALT_V71_FP_BTU', 'BTU meter')
    p.rect(238, 134, 104, 42, fill='#154360', stroke='#5dade2', pen=1.0, popup='file:^px/ALT_V71_FP_BTU.px', ptitle='BTU meter')
    lbl(p, 238, 134, 104, 'BTU METER ⊞', 9, 'white', True, 18, 'center'); tag(p, 244, 154, 92, 'BTU_Power_RT', 'BTU power', size=9)
    tt_top(p, 396, Y_CHWS - 3); tag(p, 360, 146, 84, 'CHWS', 'CHWS header temp', 'TT', size=9)
    pt_top(p, 480, Y_CHWS - 3); tag(p, 498, 150, 100, 'CHW_SupplyHeaderPressure', 'CHW supply pressure', 'PT', size=9)
    hdr_text(p, 610, 176, 'CHWS HEADER', C_CHWS)
    tt_top(p, 196, Y_CHWR - 3); tag(p, 150, 898, 84, 'CHWR', 'CHWR header temp', 'TT', size=9)
    fm_h(p, 262, Y_CHWR); tag(p, 240, 898, 104, 'CHWFlow', 'CHW flow', 'FT', size=9); hot(p, 237, Y_CHWR - 15, 50, 30, 'ALT_V71_FP_Flow', 'Flow meters')
    pic(p, TANK_X - 14.5, Y_CHWR - 8 - 70, 'Tanks/Expansion/Tank_Expansion_Bottom.png')
    tag(p, 470, 900, 100, 'CHW_ExpansionTankPressure', 'Expansion tank pressure', 'EXP', size=9)
    hdr_text(p, 470, Y_CHWR + 12, 'CHWR HEADER', C_CHWR)
    valve_v(p, X_BYP, 610, None); isa(p, X_BYP - 13, 574, 'MOD')
    fm_v(p, X_BYP, 830); hot(p, X_BYP - 15, 805, 30, 50, 'ALT_V71_FP_Flow', 'Flow meters')
    hdr_text(p, X_SUC + 12, 872, 'CHP SUCTION HDR', C_CHWR, 130)
    hdr_text(p, 546, 560, 'CHP DISCH. HDR ▶', C_CHWR, 124)
    hdr_text(p, X_RIS + 12, 600, 'CHWS', C_CHWS, 56); hdr_text(p, X_RIS + 12, 616, 'RISER', C_CHWS, 56)
    panel(p, 166, 214, 350, 194, 'CHILLED WATER')
    rows(p, 166, 238, 175, [('CHWS SP', 'CHW_LeavingTemperatureSetpoint_ACTIVE'), ('CHWS', 'CHWS'), ('CHWR', 'CHWR'), ('Load RT', 'CoolingLoad_RT'),
                            ('Flow', 'CHWFlow'), ('Lead CHP', 'CHP_Lead'), ('Return kPa', 'CHW_ReturnHeaderPressure')], lw=74, rh=24)
    rows(p, 341, 238, 175, [('DP', 'CHWDP'), ('DP SP', 'CHWDP_Setpoint_ACTIVE'), ('Bypass %', 'CHW_BypassValveCmd'), ('Bypass fb', 'CHW_BypassValveFeedback'),
                            ('Bypass flow', 'CHW_BypassFlow'), ('Supply kPa', 'CHW_SupplyHeaderPressure'), ('Exp. tank', 'CHW_ExpansionTankPressure')], lw=76, rh=24)
    for n, (x, y) in CHP.items():
        u = f'CHP{n}'
        pic_bool(p, x, y, f'{u}RunProof', 'Pumps/Pumps_Base/Pump_Base_Left/Pump_Base_Left_On.gif', 'Pumps/Pumps_Base/Pump_Base_Left/Pump_Base_Left_Off.png', f'{u} image')
        hot(p, x, y + 10, 110, 70, f'ALT_V71_FP_{u}', f'{u} pump + VSD')
        valve_h(p, 454, y + 44.5); status_led(p, 466, y + 54, f'{u}_SuctionMVCmd', f'{u} suction valve open', 'run')
        pt_top(p, 488, y + 44.5); tag(p, 434, y + 76, 80, f'{u}_SuctionPressure', f'{u} suction pressure', 'S', size=8)
        pt_top(p, 574, y - 40); tag(p, 590, y - 100, 84, f'{u}_DischargePressure', f'{u} discharge pressure', 'D', size=8)
        valve_top(p, 640, y - 40); status_led(p, 660, y - 64, f'{u}_DischargeMVCmd', f'{u} discharge valve open', 'run')
        card(p, 166, y - 10, 244, f'CHP-{n}', f'ALT_V71_FP_{u}', f'{u}RunProof',
             [('Status', f'{u}RunProof', {'bool_c': (RUN, OFF)}), ('Speed %', f'{u}SpeedCmd'), ('Hz', f'{u}_SpeedFeedbackHz'), ('kW', f'{u}_kW'),
              ('Pump dP', f'{u}_DiffPressure'), ('Valves / svc', f'{u}_ServiceIsolate', {'action': True})], '#1b4f72', reset=f'{u}ResetFire', lw=96)
    # ================= chillers
    for n, (x, y) in CH.items():
        c = f'CH{n}'
        pic_bool(p, x, y, f'{c}RunProofSelected', 'Chillers/Generic/Chiller_Generic_On.gif', 'Chillers/Generic/Chiller_Generic_Off.png', f'Chiller {n} image')
        hot(p, x + 20, y, 170, 100, f'ALT_V71_FP_{c}', f'Chiller {n}')
        valve_top(p, 765, y + 45); pct_tag(p, 748, y + 2, f'{c}_ChwFCVCmd', f'{c} evaporator FCV')
        tt_top(p, 810, y + 45); tag(p, 790, y - 20, 76, f'{c}_ChwSupplyTemp', f'{c} CHW leaving', 'LWT', size=8)
        valve_h(p, 705, y + 55); status_led(p, 717, y + 64, f'{c}ValveOpenProof', f'{c} CHW isolation valve open', 'run')
        tt_bot(p, 806, y + 55); tag(p, 770, y + 88, 72, f'{c}_ChwReturnTemp', f'{c} CHW entering', 'EWT', size=8)
        tt_top(p, x + 222, y + 45); tag(p, x + 198, y - 20, 76, f'{c}_CdwLeavingTemp', f'{c} CDW leaving', 'LWT', size=8)
        valve_top(p, x + 262, y + 45); pct_tag(p, x + 206, y + 2, f'{c}_CdwHPVCmd', f'{c} condenser HPV')
        tt_bot(p, x + 222, y + 55); tag(p, x + 222, y + 88, 72, f'{c}_CdwEnteringTemp', f'{c} CDW entering', 'EWT', size=8)
        valve_h(p, X_CDS - 30, y + 55); status_led(p, X_CDS - 18, y + 64, f'{c}CdwValveOpenProof', f'{c} CDW isolation valve open', 'run')
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
    # ================= CDW side
    for n, (x, y) in CDP.items():
        u = f'CDP{n}'
        pic_bool(p, x, y, f'{u}RunProof', 'Pumps/Pumps_Base/Pump_Base_Right/Pump_Base_Right_On.gif', 'Pumps/Pumps_Base/Pump_Base_Right/Pump_Base_Right_Off.png', f'{u} image')
        hot(p, x, y + 10, 110, 70, f'ALT_V71_FP_{u}', f'{u} pump + VSD')
        valve_h(p, 1394, y + 44.5); status_led(p, 1406, y + 54, f'{u}_SuctionMVCmd', f'{u} suction valve open', 'run')
        pt_top(p, 1352, y + 44.5); tag(p, 1314, y + 76, 80, f'{u}_SuctionPressure', f'{u} suction pressure', 'S', size=8)
        pt_top(p, 1262, y - 20); tag(p, 1278, y - 80, 84, f'{u}_DischargePressure', f'{u} discharge pressure', 'D', size=8)
        valve_top(p, 1212, y - 20); status_led(p, 1232, y - 44, f'{u}_DischargeMVCmd', f'{u} discharge valve open', 'run')
        card(p, 1444, y - 20, 244, f'CDP-{n}', f'ALT_V71_FP_{u}', f'{u}RunProof',
             [('Status', f'{u}RunProof', {'bool_c': (RUN, OFF)}), ('Speed %', f'{u}SpeedCmd'), ('Hz', f'{u}_SpeedFeedbackHz'), ('kW', f'{u}_kW'),
              ('Pump dP', f'{u}_DiffPressure'), ('Valves / svc', f'{u}_ServiceIsolate', {'action': True})], '#7d6608', reset=f'{u}ResetFire', lw=96)
    hdr_text(p, X_CDS - 136, CDP['02'][1] + 16, 'CDP DISCH. HDR ▶', C_CDWS, 132)
    hdr_text(p, X_CDSUC + 14, 480, 'CDP SUCTION', C_CDWS); hdr_text(p, X_CDSUC + 14, 496, 'HEADER', C_CDWS)
    hdr_text(p, X_CDR - 50, 668, 'CDWR', C_CDWR, 46); hdr_text(p, X_CDR - 50, 684, 'RISER', C_CDWR, 46)
    hdr_text(p, 1390, Y_CDR + 14, 'CDWR HEADER', C_CDWR)
    hdr_text(p, 1450, Y_CDWS + 12, 'CDWS HEADER', C_CDWS)
    tt_bot(p, 1300, Y_CDR + 3)
    pic(p, X_CDSUC + 8, 360 - 13.5, 'Sensors/sensor_pipe_welltemp2_ver_right.png'); tag(p, X_CDSUC + 42, 350, 96, 'CDS', 'CDW supply header temp', 'TT', size=9)
    fm_v(p, X_CDSUC, 420); tag(p, X_CDSUC + 42, 410, 108, 'CDW_Flow', 'CDW header flow', 'FT', size=9); hot(p, X_CDSUC - 15, 395, 30, 50, 'ALT_V71_FP_Flow', 'Flow meters')
    panel(p, 1190, 196, 218, 214, 'CONDENSER WATER')
    rows(p, 1190, 220, 218, [('CDS SP', 'CDS_Setpoint_ACTIVE'), ('CDS', 'CDS'), ('CDR', 'CDR'), ('CDW flow', 'CDW_Flow'), ('Make-up m3/h', 'CT_MakeupFlow'),
                             ('Conductivity', 'CT_Conductivity'), ('Lead CDP', 'CDP_Lead'), ('Lead CT', 'CT_Lead'), ('Towers', 'CT_RunAllAvailable', {'action': True})],
         lw=98, rh=21)
    for n, (x, y) in CT.items():
        u = f'CT{n}'
        pic_bool(p, x, y, f'{u}RunProof', 'CoolingTowers/PushThru/CoolingTower_PushThru_Left/CoolingTower_PushThru_Left_On.gif',
                 'CoolingTowers/PushThru/CoolingTower_PushThru_Left/CoolingTower_PushThru_Left_Off.png', f'{u} image')
        hot(p, x + 20, y, 140, 130, f'ALT_V71_FP_{u}', f'Cooling tower {n}')
        dx = CT_DROP[n]
        valve_v(p, dx, Y_CDR + 38, f'{u}ValveOpenProof', f'{u} inlet valve open')
        tt_top(p, dx + 34, y + 64.5)
        ox = 1455 if n == '01' else 1812
        valve_h(p, ox, y + 104.5); status_led(p, ox + 12, y + 114, f'{u}_OutletMVCmd', f'{u} outlet valve open', 'run')
        tt_top(p, 1530 if n == '01' else 1770, y + 104.5)
        bx, by = (1560, 318) if n == '01' else (1840, 300)
        h = card(p, bx, by, 206, f'CT-{n}', f'ALT_V71_FP_{u}', f'{u}RunProof',
                 [('Fan speed', f'{u}SpeedCmd'), ('Fan Hz', f'{u}_FanSpeedHz'), ('Water in', f'{u}_InletTemp'), ('Water out', f'{u}_OutletTemp'),
                  ('Basin level', f'{u}_BasinLevel')], '#935116', reset=f'{u}ResetFire', lw=86, rh=20)
        yy = by + h + 2
        val(p, bx, yy, 49, f'{u}BasinLowLevelAlarm', f'{u} basin low', h=18, size=8, bool_c=(FLT, OKC), fmt='LOW')
        val(p, bx + 52, yy, 49, f'{u}BasinHighLevelAlarm', f'{u} basin high', h=18, size=8, bool_c=(WARN, OKC), fmt='HI')
        val(p, bx + 104, yy, 49, f'{u}BasinHighHighLevelAlarm', f'{u} basin high-high', h=18, size=8, bool_c=(FLT, OKC), fmt='HH')
        val(p, bx + 156, yy, 50, f'{u}_MakeupValveCmd', f'{u} make-up valve', h=18, size=8, bool_c=(RUN, OFF), fmt='FILL')
    # legend
    panel(p, 1840, 500, 250, 180, 'LEGEND')
    for i, (t, c) in enumerate((('CHW supply', '#1665d6'), ('CHW return', '#5ec4f2'), ('CDW supply', '#f2c416'), ('CDW return', '#f07a12'))):
        p.rect(1850, 530 + i * 20, 30, 10, fill=c, stroke=c, pen=1.0); lbl(p, 1888, 524 + i * 20, 190, t, 9, TXT)
    status_led(p, 1850, 612, 'CH01ValveOpenProof', 'legend LED', 'run'); lbl(p, 1870, 608, 210, 'on/off valve (LED = open)', 9, TXT)
    lbl(p, 1850, 630, 230, '% = modulating valve position', 9, '#7dcea0')
    lbl(p, 1850, 650, 230, 'thick = header, thin = branch', 9, TXT)
    # ================= bottom band
    y0 = 980
    panel(p, 10, y0, 470, 190, 'EQUIPMENT POOLS / SET')
    for i, eq in enumerate(('CHP', 'CDP', 'CT')):
        yy = y0 + 28 + i * 34
        lbl(p, 16, yy, 44, eq, 10, TXT, True)
        lbl(p, 56, yy, 40, 'Lead'); val(p, 92, yy + 1, 60, f'{eq}_Lead', f'{eq} lead', h=20, size=9)
        val(p, 156, yy + 1, 70, f'{eq}_RotationMode_Runtime', f'{eq} rotation mode', h=20, size=9, action=True)
        val(p, 230, yy + 1, 116, f'{eq}_PoolDegradedAlarm', f'{eq} standby lost', h=20, size=8, bool_c=(WARN, OKC), fmt='Standby: %out.value%')
        val(p, 350, yy + 1, 124, f'{eq}_PoolUnavailableAlarm', f'{eq} none available', h=20, size=8, bool_c=(FLT, OKC), fmt='No unit: %out.value%')
    lbl(p, 16, y0 + 140, 130, 'Lead chiller (set)'); val(p, 136, y0 + 141, 96, 'LeadCH01', 'Lead chiller select', h=20, size=9, action=True)
    val(p, 236, y0 + 141, 110, 'Set_LinkPools', 'Pools linked to set', h=20, size=8, action=True)
    val(p, 350, y0 + 141, 124, 'Stage2BlockedByPoolAlarm', 'Stage 2 blocked', h=20, size=8, bool_c=(WARN, OKC), fmt='S2 blocked: %out.value%')
    panel(p, 490, y0, 610, 190, 'PLANT ALARMS', link='file:^px/ALT_CP_AlarmsHistory.px')
    al = [('All chillers unavailable', 'AllChillersUnavailableAlarm'), ('CHW flow low', 'CHW_FlowLowAlarm'), ('CDW flow low', 'CDW_FlowLowAlarm'),
          ('CHWST not tracking', 'CHWST_NotTrackingAlarm'), ('Low delta-T', 'LowDeltaTAlarm'), ('BTU invalid', 'BTU_InvalidAlarm'),
          ('CT01 basin HIGH-HIGH', 'CT01BasinHighHighLevelAlarm'), ('CT02 basin HIGH-HIGH', 'CT02BasinHighHighLevelAlarm'),
          ('CT01 basin low', 'CT01BasinLowLevelAlarm'), ('CT02 basin low', 'CT02BasinLowLevelAlarm'), ('Conductivity high', 'CT_ConductivityHighAlarm'),
          ('Power meter deviation', 'PowerMeter_DeviationAlarm')]
    for i, (t, pt) in enumerate(al):
        cx, cy = 500 + (i // 6) * 300, y0 + 28 + (i % 6) * 26
        status_led(p, cx, cy + 3, pt, t, 'alarm'); lbl(p, cx + 20, cy, 272, t, 10, TXT)
    panel(p, 1110, y0, 540, 190, 'CONTROL')
    rows(p, 1110, y0 + 26, 270, [('Plant enable', 'PlantEnable', {'bool_c': (RUN, OFF), 'action': True}), ('Schedule mode', 'PlantScheduleMode', {'action': True}),
                                 ('Demand mode', 'PlantDemandMode', {'action': True}), ('Pump valves', 'Pump_StandbyValvesOpen', {'action': True}),
                                 ('Load source', 'CoolingLoadSource'), ('Reset source', 'PlantResetSource')], lw=120, rh=26)
    rows(p, 1380, y0 + 26, 270, [('Plant main kW', 'PM_Main_kW'), ('Plant kWh today', 'Plant_kWh_Today'), ('Cost today', 'Energy_Cost_THB_Today'),
                                 ('CHWS valid', 'CHWS_SensorInvalidAlarm', {'bool_c': (FLT, OKC)}), ('Rotation daily', 'RotationMode_Daily', {'action': True}),
                                 ('Rotation weekly', 'RotationMode_Weekly', {'action': True})], lw=120, rh=26)
    ashrae_scale(p, 1660, y0, 430, 190, 'Plant_kW_per_RT')
    return p


VALVES = [  # (valve, location, type, command point, feedback point, alarm point)
    ('CH01 CHW inlet', 'Chiller 01 evaporator in', 'ISO on/off', 'CH01ValveOpenCmd', 'CH01ValveOpenProof', None),
    ('CH01 CHW outlet', 'Chiller 01 evaporator out', 'FCV 0-100 %', 'CH01_ChwFCVCmd', 'CH01_ChwFCVFb', 'CH01_ChwFCVMismatchAlarm'),
    ('CH01 CDW inlet', 'Chiller 01 condenser in', 'ISO on/off', 'CH01CdwValveOpenCmd', 'CH01CdwValveOpenProof', None),
    ('CH01 CDW outlet', 'Chiller 01 condenser out', 'HPV 0-100 %', 'CH01_CdwHPVCmd', 'CH01_CdwHPVFb', 'CH01_CdwHPVMismatchAlarm'),
    ('CH02 CHW inlet', 'Chiller 02 evaporator in', 'ISO on/off', 'CH02ValveOpenCmd', 'CH02ValveOpenProof', None),
    ('CH02 CHW outlet', 'Chiller 02 evaporator out', 'FCV 0-100 %', 'CH02_ChwFCVCmd', 'CH02_ChwFCVFb', 'CH02_ChwFCVMismatchAlarm'),
    ('CH02 CDW inlet', 'Chiller 02 condenser in', 'ISO on/off', 'CH02CdwValveOpenCmd', 'CH02CdwValveOpenProof', None),
    ('CH02 CDW outlet', 'Chiller 02 condenser out', 'HPV 0-100 %', 'CH02_CdwHPVCmd', 'CH02_CdwHPVFb', 'CH02_CdwHPVMismatchAlarm')] + \
    [(f'{u} {s.lower()}', f'{u} pump {s.lower()}', 'ISO on/off (with pump)', f'{u}_{s}MVCmd', f'{u}_{s}MVFb', f'{u}_{s}MVFailAlarm')
     for u in ('CHP01', 'CHP02', 'CDP01', 'CDP02') for s in ('Suction', 'Discharge')] + \
    [(f'CT{n} inlet', f'Cooling tower {n} inlet', 'ISO on/off', f'CT{n}ValveOpenCmd', f'CT{n}ValveOpenProof', None) for n in ('01', '02')] + \
    [(f'CT{n} outlet', f'Cooling tower {n} outlet', 'ISO on/off', f'CT{n}_OutletMVCmd', f'CT{n}_OutletMVFb', f'CT{n}_OutletMVFailAlarm') for n in ('01', '02')] + \
    [('CHW bypass', 'CHW min-flow bypass', 'MOD 0-100 %', 'CHW_BypassValveCmd', 'CHW_BypassValveFeedback', None)]


def valves_page():
    p = G.Page('ALT_V71_Valves', 'Motorised valves — type, command, feedback, alarms', (1920, 1080)); p.header()
    cols = [('Valve', 250), ('Location', 330), ('Actuator type', 190), ('Command', 180), ('Feedback / proof', 180), ('Alarm', 200)]
    x = 20
    for t, w in cols: p.label(x, 84, w - 4, 26, t, 10, True, 'white', '#2c3e50', 'center'); x += w
    for r, (v, loc, typ, c, f, a) in enumerate(VALVES):
        y = 114 + r * 30
        x = 20
        mod = '%' in typ
        p.label(x, y, 246, 26, '  ' + v, 10, True, 'white', '#1b2631', 'left'); x += 250
        lbl(p, x + 4, y + 3, 322, loc, 10, TXT); x += 330
        p.label(x, y, 186, 26, typ, 10, True, '#0b0e11', '#7dcea0' if mod else '#8fd3ff', 'center'); x += 190
        val(p, x, y + 2, 176, c, f'{v} command', h=22, size=10); x += 180
        val(p, x, y + 2, 176, f, f'{v} feedback', h=22, size=10); x += 180
        if a: val(p, x, y + 2, 196, a, f'{v} alarm', h=22, size=10, bool_c=(FLT, OKC))
        else: lbl(p, x + 4, y + 3, 196, 'end switch (DI)', 9, '#c9d3dd')
    y = 114 + len(VALVES) * 30 + 12
    panel(p, 20, y, 1330, 1070 - y, 'SELECTION RULE')
    for i, t in enumerate(('On/off (2-position) = isolation / sequencing: chiller inlets, pump suction + discharge (open with the pump, closed when stopped), tower inlets / outlets.',
                           'Pump valves: open on request -> pump starts when both proven >= 80 % -> close 30 s after stop. Option "Standby valves OPEN" (Plant page, CONTROL) keeps healthy standby pumps open for a faster changeover.',
                           'Modulating 0-100 % = controls a process variable: evaporator flow-limit (FCV), condenser head pressure (HPV), CHW min-flow bypass.',
                           'On/off feedback: open >= 80 %, closed <= 20 % (MV_OpenPct / MV_ClosedPct); command failure after the stroke timeout.',
                           'Modulating feedback: mismatch alarm when |command - feedback| > 10 % for the stroke timeout.')):
        lbl(p, 34, y + 28 + i * 24, 1300, t, 10, TXT)
    return p


def ashrae_scale(p, x, y, w, h, point, title='PLANT kW/RT — ASHRAE SCALE', compact=False):
    panel(p, x, y, w, h, title)
    names = ('EXCELLENT', 'GOOD', 'FAIR', 'NEEDS IMPROVEMENT')
    rng = ('< 0.75', '0.75–0.90', '0.90–1.00', '> 1.00')
    bands = ASHRAE[1:]
    if compact:                                     # value left, colour bands right (single-row panel)
        vw = int(w * 0.36)
        val(p, x + 10, y + 30, vw, point, 'Plant kW/RT (ASHRAE colour)', h=44, size=18, fg='white', fmt='%out.value%')
        p.el[-1] = p.el[-1].replace('<ObjectToString', f'<INumericToSimple name="background" map="{KWRT_MAP}"/>\n    <ObjectToString')
        lbl(p, x + 10, y + 78, vw, 'kW/RT (whole plant)', 9, '#c9d3dd', halign='center')
        bx, bw = x + vw + 20, (w - vw - 30) / 4
        for i, (lo, hi, c, t) in enumerate(bands):
            p.rect(bx + i * bw, y + 30, bw - 3, 26, fill=c, stroke=c, pen=1.0)
            p.label(bx + i * bw, y + 30, bw - 3, 26, rng[i], 10, True, '#0b0e11', None, 'center')
            p.label(bx + i * bw, y + 58, bw - 3, 18, names[i] if i < 3 else 'NEEDS IMPROV.', 9, True, c, None, 'center')
        lbl(p, bx, y + 84, w - vw - 30, 'ASHRAE Journal plant efficiency scale (reference — confirm with project M&V)', 9, '#c9d3dd', h=36)
        return
    val(p, x + 10, y + 26, w - 20, point, 'Plant kW/RT (ASHRAE colour)', h=40, size=18, fg='white', fmt='%out.value% kW/RT')
    p.el[-1] = p.el[-1].replace('<ObjectToString', f'<INumericToSimple name="background" map="{KWRT_MAP}"/>\n    <ObjectToString')
    bw = (w - 20) / len(bands)
    for i, (lo, hi, c, t) in enumerate(bands):
        p.rect(x + 10 + i * bw, y + 74, bw - 2, 22, fill=c, stroke=c, pen=1.0)
        p.label(x + 10 + i * bw, y + 74, bw - 2, 22, rng[i], 9, True, '#0b0e11', None, 'center')
        p.label(x + 10 + i * bw, y + 98, bw - 2, 16, names[i] if i < 3 else 'NEEDS IMPROV.', 8, True, c, None, 'center')
    lbl(p, x + 10, y + 118, w - 20, 'Whole plant (chillers + CHP + CDP + tower fans) kW per ton — ASHRAE Journal efficiency scale', 8, '#c9d3dd', h=16)
    lbl(p, x + 10, y + 136, w - 20, '(Hartman 2001 / Erpelding). Reference bands — confirm with project M&V.', 8, '#c9d3dd', h=16)



# ================================================================ faceplates (pop-ups)
def fp(name, title, size=(620, 760)):
    FACEPLATES.append(name)
    p = G.Page(name, title, size); p.header()
    return p


def drive_rows(p, x, y, w, u, plant=True):
    cmd = f'{u}SpeedCmd' if plant else f'{u}_SpeedCmd'
    hz = f'{u}_FanSpeedHz' if u.startswith('CT') else f'{u}_SpeedFeedbackHz'
    run = f'{u}RunProof' if plant else f'{u}_Status'
    flt = f'{u}VfdFault' if plant else f'{u}_VfdFault'
    items = [('Run feedback', run, {'bool_c': (RUN, OFF)}), ('Speed command', cmd), ('Output frequency', hz), ('Output voltage', f'{u}_VfdOutputV'),
             ('Output current', f'{u}_Amps'), ('Power', f'{u}_kW'), ('DC bus voltage', f'{u}_VfdDcBusV'), ('Heatsink temp', f'{u}_VfdTemp'),
             ('Fault code', f'{u}_VfdFaultCode'), ('VFD fault (DI)', flt, {'bool_c': (FLT, OKC)}), ('Over-temperature', f'{u}_VfdOverTempAlarm', {'bool_c': (WARN, OKC)}),
             ('Fault code active', f'{u}_VfdFaultCodeActive', {'bool_c': (WARN, OKC)}),
             ('MIN speed % (set)', f'{u}_MinSpeed', {'action': True, 'fg': '#7dcea0'}), ('MAX speed % (set)', f'{u}_MaxSpeed', {'action': True, 'fg': '#7dcea0'})]
    if plant: items.insert(6, ('Energy', f'{u}_kWh'))
    rows(p, x, y, w, items, lw=int(w * 0.55), rh=22)
    return y + len(items) * 22


def fp_pump(u):
    p = fp(f'ALT_V71_FP_{u}', f'{u} — pump, VSD, isolation valves, PT', (620, 950))
    img = 'Pumps/Pumps_Base/Pump_Base_Left/Pump_Base_Left' if u.startswith('CHP') else 'Pumps/Pumps_Base/Pump_Base_Right/Pump_Base_Right'
    pic_bool(p, 20, 50, f'{u}RunProof', img + '_On.gif', img + '_Off.png', f'{u} image')
    ximg(p, 150, 40, 'vsd_drive.png', 50, 106)
    rows(p, 220, 44, 390, [('Start command', f'{u}StartCmd', {'bool_c': (RUN, OFF)}), ('HOA in AUTO', f'{u}InAuto', {'bool_c': (RUN, WARN)}),
                           ('Failed (latched)', f'{u}FailLatch', {'bool_c': (FLT, OKC)}), ('Runtime h', f'{u}_RuntimeHours')], lw=200, rh=22)
    panel(p, 10, 150, 600, 22 + 15 * 22 + 6, 'VARIABLE SPEED DRIVE')
    drive_rows(p, 10, 172, 600, u)
    y = 172 + 15 * 22 + 14
    panel(p, 10, y, 600, 22 + 4 * 22 + 6, 'PRESSURE (PT before / after pump)')
    rows(p, 10, y + 22, 600, [('Suction PT (before)', f'{u}_SuctionPressure'), ('Discharge PT (after)', f'{u}_DischargePressure'),
                              ('Pump differential', f'{u}_DiffPressure'), ('No-dP / low suction', f'{u}NoDeltaPAlarm', {'bool_c': (FLT, OKC)})], lw=330, rh=22)
    y += 22 + 4 * 22 + 14
    panel(p, 10, y, 600, 22 + 7 * 22 + 6, 'MOTORISED ISOLATION VALVES (on/off, normally open)')
    rows(p, 10, y + 22, 600, [('Suction MV command / feedback', f'{u}_SuctionMVCmd', {'bool_c': (RUN, OFF)}), ('', f'{u}_SuctionMVFb'),
                              ('Discharge MV command / feedback', f'{u}_DischargeMVCmd', {'bool_c': (RUN, OFF)}), ('', f'{u}_DischargeMVFb'),
                              ('Suction MV command failure', f'{u}_SuctionMVFailAlarm', {'bool_c': (FLT, OKC)}),
                              ('Discharge MV command failure', f'{u}_DischargeMVFailAlarm', {'bool_c': (FLT, OKC)}),
                              ('Service isolation (click)', f'{u}_ServiceIsolate', {'action': True})], lw=330, rh=22)
    p.fire(10, 914, 140, 26, f'RESET {u}', f'{u}ResetFire', f'{u} reset')
    return p


def fp_ct(u):
    p = fp(f'ALT_V71_FP_{u}', f'{u} — cooling tower, fan VSD, basin', (620, 990))
    pic_bool(p, 20, 44, f'{u}RunProof', 'CoolingTowers/PushThru/CoolingTower_PushThru_Left/CoolingTower_PushThru_Left_On.gif',
             'CoolingTowers/PushThru/CoolingTower_PushThru_Left/CoolingTower_PushThru_Left_Off.png', f'{u} image')
    rows(p, 200, 44, 410, [('Start command', f'{u}StartCmd', {'bool_c': (RUN, OFF)}), ('Inlet valve cmd / proof', f'{u}ValveOpenCmd', {'bool_c': (RUN, OFF)}),
                           ('', f'{u}ValveOpenProof', {'bool_c': (RUN, OFF)}), ('Vibration', f'{u}VibrationAlarm', {'bool_c': (FLT, OKC)}),
                           ('Failed (latched)', f'{u}FailLatch', {'bool_c': (FLT, OKC)}), ('Runtime h', f'{u}_RuntimeHours')], lw=200, rh=22)
    panel(p, 10, 190, 600, 22 + 15 * 22 + 6, 'FAN VARIABLE SPEED DRIVE')
    drive_rows(p, 10, 212, 600, u)
    y = 212 + 15 * 22 + 14
    panel(p, 10, y, 600, 22 + 12 * 22 + 6, 'WATER & BASIN (TT entering / leaving, LT, LS)')
    rows(p, 10, y + 22, 600, [('Entering water TT (hot)', f'{u}_InletTemp'), ('Leaving water TT (cold)', f'{u}_OutletTemp'), ('Range', f'{u}_Range'),
                              ('Approach to OA wet bulb', f'{u}_Approach'), ('Basin temperature', f'{u}_BasinTemp'), ('Basin level LT', f'{u}_BasinLevel'),
                              ('Make-up valve', f'{u}_MakeupValveCmd', {'bool_c': (RUN, OFF)}), ('Level LOW', f'{u}BasinLowLevelAlarm', {'bool_c': (FLT, OKC)}),
                              ('Level HIGH', f'{u}BasinHighLevelAlarm', {'bool_c': (WARN, OKC)}), ('Level HIGH-HIGH / overflow', f'{u}BasinHighHighLevelAlarm', {'bool_c': (FLT, OKC)}),
                              ('High level float switch', f'{u}_HighLevelSwitch', {'bool_c': (WARN, OKC)}), ('Low level float switch', f'{u}_LowLevelSwitch', {'bool_c': (FLT, OKC)})], lw=330, rh=22)
    y2 = 870
    panel(p, 10, y2, 600, 22 + 3 * 22 + 6, 'OUTLET MOTORISED VALVE (on/off, feedback %)')
    rows(p, 10, y2 + 22, 600, [('Outlet MV command', f'{u}_OutletMVCmd', {'bool_c': (RUN, OFF)}), ('Outlet MV feedback', f'{u}_OutletMVFb'),
                               ('Outlet MV command failure', f'{u}_OutletMVFailAlarm', {'bool_c': (FLT, OKC)})], lw=330, rh=22)
    p.fire(10, 960, 140, 26, f'RESET {u}', f'{u}ResetFire', f'{u} reset')
    return p


CH_ITEMS = lambda c: [('Run proof', f'{c}RunProofSelected', {'bool_c': (RUN, OFF)}), ('Remote (auto)', f'{c}InAuto', {'bool_c': (RUN, WARN)}),
                      ('Load %', f'{c}LoadPct'), ('Capacity RT', f'{c}_RT'), ('kW/RT', f'{c}_kW_per_RT'), ('CHW leaving TT', f'{c}_ChwSupplyTemp'),
                      ('CHW entering TT', f'{c}_ChwReturnTemp'), ('CHW delta-T', f'{c}_DeltaT'), ('CHW flow FT', f'{c}_ChwFlow'), ('Evap dP', f'{c}_EvapDP'),
                      ('CDW entering TT', f'{c}_CdwEnteringTemp'), ('CDW leaving TT', f'{c}_CdwLeavingTemp'), ('CDW flow FT', f'{c}_CdwFlow'), ('Cond dP', f'{c}_CondDP'),
                      ('Evap sat. temp', f'{c}_EvapSatTemp'), ('Cond sat. temp', f'{c}_CondSatTemp'), ('Evap approach', f'{c}_EvapApproach'),
                      ('Cond approach', f'{c}_CondApproach'), ('Lift', f'{c}_Lift'), ('Runtime h', f'{c}_RuntimeHours')]
CH_PM = lambda c: [('Power kW', f'{c}_kW'), ('Apparent kVA', f'{c}_kVA'), ('Current A', f'{c}_Amps'), ('Voltage V', f'{c}_Volts'), ('Power factor', f'{c}_PF'), ('Energy kWh', f'{c}_kWh')]
CH_AL = lambda c: [('Evap approach high', f'{c}EvapApproachAlarm'), ('Cond approach high', f'{c}CondApproachAlarm'), ('Evap low flow', f'{c}EvapLowFlowAlarm'),
                   ('Program lockout', f'{c}TimeoutLockout'), ('Hard lockout', f'{c}HardLockoutAlarm'), ('Local (not remote)', f'{c}NotInAutoAlarm')]


def fp_ch(n):
    c = f'CH{n}'
    p = fp(f'ALT_V71_FP_{c}', f'Chiller {n} — TT / FT / DPT / power meter / valves', (620, 900))
    pic_bool(p, 20, 44, f'{c}RunProofSelected', 'Chillers/Generic/Chiller_Generic_On.gif', 'Chillers/Generic/Chiller_Generic_Off.png', f'{c} image')
    rows(p, 260, 44, 350, [('Start command', f'{c}StartCmd', {'bool_c': (RUN, OFF)}), ('CHW valve proof', f'{c}ValveOpenProof', {'bool_c': (RUN, OFF)}),
                           ('CDW valve proof', f'{c}CdwValveOpenProof', {'bool_c': (RUN, OFF)}), ('Auto-retry count', f'{c}_AutoRetryCount')], lw=180, rh=22)
    panel(p, 10, 150, 600, 22 + 10 * 22 + 6, 'THERMAL / HYDRONIC')
    it = CH_ITEMS(c)
    rows(p, 10, 172, 300, it[:10], lw=150, rh=22); rows(p, 310, 172, 300, it[10:], lw=150, rh=22)
    panel(p, 10, 430, 600, 22 + 3 * 22 + 6, 'POWER METER')
    pm = CH_PM(c)
    rows(p, 10, 452, 300, pm[:3], lw=150, rh=22); rows(p, 310, 452, 300, pm[3:], lw=150, rh=22)
    panel(p, 10, 540, 600, 110, 'ALARMS')
    for i, (t, pt) in enumerate(CH_AL(c)):
        status_led(p, 20 + (i % 2) * 300, 566 + (i // 2) * 24, pt, t, 'alarm'); lbl(p, 38 + (i % 2) * 300, 563 + (i // 2) * 24, 250, t, 9, TXT)
    panel(p, 10, 660, 600, 22 + 4 * 22 + 6, 'MOTORISED VALVES (inlet ISO on/off · outlet modulating)')
    rows(p, 10, 682, 300, [('CHW in ISO cmd', f'{c}ValveOpenCmd', {'bool_c': (RUN, OFF)}), ('CHW in ISO proof', f'{c}ValveOpenProof', {'bool_c': (RUN, OFF)}),
                           ('CHW out FCV cmd / fb', f'{c}_ChwFCVCmd'), ('', f'{c}_ChwFCVFb')], lw=150, rh=22)
    rows(p, 310, 682, 300, [('CDW in ISO cmd', f'{c}CdwValveOpenCmd', {'bool_c': (RUN, OFF)}), ('CDW in ISO proof', f'{c}CdwValveOpenProof', {'bool_c': (RUN, OFF)}),
                            ('CDW out HPV cmd / fb', f'{c}_CdwHPVCmd'), ('', f'{c}_CdwHPVFb')], lw=150, rh=22)
    rows(p, 10, 784, 600, [('FCV flow limit (m3/h)', 'CH_ChwFlowLimit', {'action': True}), ('HPV reset ECWT low / high', 'CH_HpvTempLow', {'action': True}),
                           ('', 'CH_HpvTempHigh', {'action': True})], lw=330, rh=22)
    p.fire(10, 860, 140, 26, f'RESET {c}', f'{c}ResetFire', f'{c} reset')
    return p


AIR_VSD = ['AHU01', 'AHU02', 'OAU01', 'EF02', 'EF03', 'CPEF01', 'LSF01']
PLANT_VSD = ['CHP01', 'CHP02', 'CDP01', 'CDP02', 'CT01', 'CT02']


def fp_air_vsd(u):
    p = fp(f'ALT_V71_FP_VSD_{u}', f'{u} — fan variable speed drive', (620, 520))
    ximg(p, 24, 40, 'vsd_drive.png', 50, 106)
    rows(p, 90, 44, 520, [('Start command', f'{u}_StartCmd', {'bool_c': (RUN, OFF)}), ('HOA in AUTO', f'{u}_InAuto', {'bool_c': (RUN, WARN)}),
                          ('Fan fail', f'{u}_FanFailAlarm', {'bool_c': (FLT, OKC)}), ('Runtime h', f'{u}_RuntimeHours')], lw=260, rh=22)
    panel(p, 10, 150, 600, 22 + 14 * 22 + 6, 'VARIABLE SPEED DRIVE')
    drive_rows(p, 10, 172, 600, u, plant=False)
    return p


def fp_btu():
    p = fp('ALT_V71_FP_BTU', 'BTU (energy) meter — CHW', (620, 520))
    pic(p, 20, 60, 'Sensors/sensor_watermtr_horz_largepipe.png')
    rows(p, 10, 110, 600, [('Flow', 'BTU_Flow'), ('Supply temperature', 'BTU_SupplyTemp'), ('Return temperature', 'BTU_ReturnTemp'), ('Delta-T', 'BTU_DeltaT'),
                           ('Cooling power', 'BTU_Power_RT'), ('Energy total', 'BTU_EnergyTotal'), ('Communication', 'BTU_CommOk', {'bool_c': (RUN, FLT)}),
                           ('Valid (range + comm)', 'BTU_Valid', {'bool_c': (RUN, FLT)}), ('Used for plant load', 'CoolingLoadSource'),
                           ('Deviation vs calculated', 'BTU_DeviationAlarm', {'bool_c': (WARN, OKC)}), ('Invalid alarm', 'BTU_InvalidAlarm', {'bool_c': (FLT, OKC)}),
                           ('Max valid RT', 'BTU_MaxValidRT', {'action': True})], lw=330, rh=26)
    return p


def fp_power():
    p = fp('ALT_V71_FP_Power', 'Main power meter (plant MCC)', (620, 520))
    pic(p, 20, 44, 'Sensors/sensor_elecmtr.png', 60, 70)
    rows(p, 10, 130, 600, [('Active power', 'PM_Main_kW'), ('Apparent power', 'PM_Main_kVA'), ('Feeder loading', 'PM_Main_LoadPct'), ('Energy', 'PM_Main_kWh'),
                           ('Voltage L-L', 'PM_Main_Volts'), ('Current', 'PM_Main_Amps'), ('Power factor', 'PM_Main_PF'), ('Frequency', 'PM_Main_Hz'),
                           ('Communication', 'PM_Main_CommOk', {'bool_c': (RUN, FLT)}), ('Meter vs sum of loads', 'PowerMeter_DeviationAlarm', {'bool_c': (WARN, OKC)}),
                           ('Sum of plant loads', 'Plant_kW'), ('Auxiliary kW', 'Aux_kW')], lw=330, rh=26)
    return p


FLOWS = [('CHW main (FT)', 'CHWFlow'), ('CH01 evaporator', 'CH01_ChwFlow'), ('CH02 evaporator', 'CH02_ChwFlow'), ('CHW bypass', 'CHW_BypassFlow'),
         ('BTU meter flow', 'BTU_Flow'), ('CDW header', 'CDW_Flow'), ('CH01 condenser', 'CH01_CdwFlow'), ('CH02 condenser', 'CH02_CdwFlow'),
         ('Tower make-up', 'CT_MakeupFlow'), ('Make-up volume', 'CT_MakeupVolume')]


def fp_flow():
    p = fp('ALT_V71_FP_Flow', 'Flow meters', (620, 560))
    pic(p, 20, 44, 'Sensors/sensor_pipe_wtrflowmtr_hor.png')
    rows(p, 10, 90, 600, FLOWS + [('CHW low-flow alarm', 'CHW_FlowLowAlarm', {'bool_c': (FLT, OKC)}), ('CDW low-flow alarm', 'CDW_FlowLowAlarm', {'bool_c': (FLT, OKC)}),
                                  ('CHW flow sensor invalid', 'CHWFlow_SensorInvalidAlarm', {'bool_c': (FLT, OKC)})], lw=330, rh=26)
    return p


def fp_oa():
    p = fp('ALT_V71_FP_OA', 'Outdoor air sensor (T + RH, psychrometrics)', (620, 480))
    pic(p, 20, 44, 'Sensors/sensor_oatemphum.png', 40, 100)
    rows(p, 80, 50, 530, [('Dry bulb', 'OA_Temperature'), ('Relative humidity', 'OA_Humidity'), ('Wet bulb (calc)', 'OA_WetBulb'), ('Dew point (calc)', 'OA_DewPoint'),
                          ('Enthalpy (calc)', 'OA_Enthalpy'), ('Sensor fault (DI)', 'OA_SensorFault', {'bool_c': (FLT, OKC)}), ('Valid', 'OA_Valid', {'bool_c': (RUN, FLT)}),
                          ('Invalid alarm', 'OA_SensorInvalidAlarm', {'bool_c': (FLT, OKC)}), ('Default wet bulb (fallback)', 'OA_WetBulbDefault', {'action': True}),
                          ('Valid range temp min / max', 'OA_TempMinValid', {'action': True}), ('', 'OA_TempMaxValid', {'action': True}),
                          ('Valid range RH min / max', 'OA_HumMinValid', {'action': True}), ('', 'OA_HumMaxValid', {'action': True})], lw=280, rh=26)
    return p


# ================================================================ pages
def chillers_page():
    p = G.Page('ALT_V71_Chillers', 'Chillers — detail', (1920, 1080)); p.header()
    for k, n in enumerate(('01', '02')):
        c = f'CH{n}'; x = 10 + k * 955
        panel(p, x, 80, 945, 990, f'CHILLER {n}', link=f'file:^px/ALT_V71_FP_{c}.px')
        pic_bool(p, x + 20, 110, f'{c}RunProofSelected', 'Chillers/Generic/Chiller_Generic_On.gif', 'Chillers/Generic/Chiller_Generic_Off.png', f'{c} image')
        # measured nozzles: evaporator left, condenser right
        tag(p, x + 10, 230, 118, f'{c}_ChwSupplyTemp', f'{c} CHW leaving', 'CHW LWT'); tag(p, x + 10, 252, 118, f'{c}_ChwReturnTemp', f'{c} CHW entering', 'CHW EWT')
        tag(p, x + 132, 230, 118, f'{c}_CdwLeavingTemp', f'{c} CDW leaving', 'CDW LWT'); tag(p, x + 132, 252, 118, f'{c}_CdwEnteringTemp', f'{c} CDW entering', 'CDW EWT')
        ashrae_mini(p, x + 270, 110, 300, f'{c}_kW_per_RT', f'{c} kW/RT (chiller only)')
        rows(p, x + 600, 110, 335, [('Start command', f'{c}StartCmd', {'bool_c': (RUN, OFF)}), ('Load %', f'{c}LoadPct'), ('Capacity RT', f'{c}_RT'),
                                    ('Power kW', f'{c}_kW'), ('CHW valve', f'{c}ValveOpenProof', {'bool_c': (RUN, OFF)}), ('CDW valve', f'{c}CdwValveOpenProof', {'bool_c': (RUN, OFF)})], lw=180, rh=24)
        it = CH_ITEMS(c)
        panel(p, x + 10, 290, 925, 22 + 10 * 26 + 8, 'THERMAL / HYDRONIC (TT, FT, DPT)')
        rows(p, x + 10, 312, 462, it[:10], lw=260, rh=26); rows(p, x + 472, 312, 462, it[10:], lw=260, rh=26)
        panel(p, x + 10, 600, 925, 22 + 3 * 26 + 8, 'POWER METER')
        pm = CH_PM(c)
        rows(p, x + 10, 622, 462, pm[:3], lw=260, rh=26); rows(p, x + 472, 622, 462, pm[3:], lw=260, rh=26)
        panel(p, x + 10, 720, 925, 130, 'ALARMS & LOCKOUTS')
        for i, (t, pt) in enumerate(CH_AL(c)):
            status_led(p, x + 24 + (i % 2) * 460, 748 + (i // 2) * 28, pt, t, 'alarm'); lbl(p, x + 44 + (i % 2) * 460, 745 + (i // 2) * 28, 400, t, 10, TXT)
        p.fire(x + 10, 862, 160, 28, f'RESET {c}', f'{c}ResetFire', f'{c} reset')
        panel(p, x + 10, 900, 925, 160, 'TRENDS (history pop-ups)')
        for i, (t, h) in enumerate(((f'{c} kW', f'{c}_kW'), (f'{c} kW/RT', f'{c}_kW_per_RT'), (f'{c} CHW leaving', f'{c}_ChwSupplyTemp'),
                                    (f'{c} CDW entering', f'{c}_CdwEnteringTemp'), (f'{c} load %', f'{c}LoadPct'), (f'{c} lift', f'{c}_Lift'))):
            o = f'history:/{STATION}/{h}'
            p.label(x + 24 + (i % 3) * 300, 932 + (i // 3) * 50, 280, 38, t + '  ↗', 10, True, 'white', '#1e5f8e', 'center', popup=o, ptitle=t)
            p.map.append((h, o, f'Trend popup {t}', 'history popup'))
    return p


def ashrae_mini(p, x, y, w, point, title):
    lbl(p, x, y, w, title, 9, LBL, True)
    val(p, x, y + 20, w, point, title, h=36, size=16, fg='white', fmt='%out.value% kW/RT')
    p.el[-1] = p.el[-1].replace('<ObjectToString', f'<INumericToSimple name="background" map="{KWRT_MAP}"/>\n    <ObjectToString')
    bw = w / 4
    for i, (lo, hi, c, t) in enumerate(ASHRAE[1:]):
        p.rect(x + i * bw, y + 60, bw - 2, 12, fill=c, stroke=c, pen=1.0)
        p.label(x + i * bw, y + 74, bw - 2, 14, ('<0.75', '0.75-0.90', '0.90-1.00', '>1.00')[i], 7, False, c, None, 'center')


def drives_page():
    p = G.Page('ALT_V71_Drives', 'Variable speed drives — status, diagnostics, MIN / MAX speed', (1920, 1080)); p.header()
    cols = [('Drive', 150), ('Run', 90), ('Speed cmd', 110), ('Hz', 100), ('Volts', 100), ('Amps', 100), ('kW', 100), ('Heatsink', 100), ('Fault code', 100),
            ('VFD fault', 110), ('Over-temp', 110), ('MIN %', 100), ('MAX %', 100), ('Runtime h', 110), ('Detail', 90)]
    x = 20
    for t, w in cols:
        p.label(x, 84, w - 4, 26, t, 10, True, 'white', '#2c3e50', 'center'); x += w
    for r, u in enumerate(PLANT_VSD + AIR_VSD):
        plant = u in PLANT_VSD
        y = 116 + r * 34 + (14 if not plant else 0)
        cmd = f'{u}SpeedCmd' if plant else f'{u}_SpeedCmd'
        hz = f'{u}_FanSpeedHz' if u.startswith('CT') else f'{u}_SpeedFeedbackHz'
        run = f'{u}RunProof' if plant else f'{u}_Status'
        flt = f'{u}VfdFault' if plant else f'{u}_VfdFault'
        fpn = f'ALT_V71_FP_{u}' if plant else f'ALT_V71_FP_VSD_{u}'
        pts = [None, (run, {'bool_c': (RUN, OFF)}), (cmd, {}), (hz, {}), (f'{u}_VfdOutputV', {}), (f'{u}_Amps', {}), (f'{u}_kW', {}), (f'{u}_VfdTemp', {}),
               (f'{u}_VfdFaultCode', {}), (flt, {'bool_c': (FLT, OKC)}), (f'{u}_VfdOverTempAlarm', {'bool_c': (WARN, OKC)}),
               (f'{u}_MinSpeed', {'action': True, 'fg': '#7dcea0'}), (f'{u}_MaxSpeed', {'action': True, 'fg': '#7dcea0'}),
               ((f'{u}_RuntimeHours'), {}), None]
        x = 20
        for (t, w), pt in zip(cols, pts):
            if t == 'Drive':
                p.label(x, y, w - 4, 28, '  ' + u, 11, True, 'white', '#1b2631' if plant else '#1b3a2f', 'left', popup=f'file:^px/{fpn}.px', ptitle=u)
            elif t == 'Detail':
                p.label(x, y, w - 4, 28, 'open ⊞', 9, True, '#8fd3ff', '#1f252c', 'center', popup=f'file:^px/{fpn}.px', ptitle=u)
            else:
                val(p, x, y + 2, w - 4, pt[0], f'{u} {t}', h=24, size=10, **pt[1])
            x += w
    ximg(p, 1720, 96, 'vsd_drive.png', 160, 338)
    lbl(p, 1690, 440, 220, 'Standard drive graphic (original).', 9, '#c9d3dd', halign='center')
    lbl(p, 1690, 458, 220, 'Project drive photo: replace', 9, '#c9d3dd', halign='center')
    lbl(p, 1690, 476, 220, 'shared/px/img/vsd_drive.png', 9, '#8fd3ff', halign='center')
    y = 116 + 13 * 34 + 30
    panel(p, 20, y, 1880, 150, 'HOW MIN / MAX IS APPLIED (logic: <unit>/Logic/<unit>SpeedMinMax)')
    for i, t in enumerate(('speed = MIN( MAX(control output, MIN speed), MAX(MAX speed, MIN speed) )  — applied after the PID / reset / fail-safe selection and before the start gate + ramp.',
                           'The drive still goes to 0 % when the start command is off (gate), so MIN never keeps a stopped fan / pump turning.',
                           'CPEF01 (car-park smoke clearance) ignores MAX during fire alarm (100 %); LSF01 stair pressurisation honours MIN / MAX (commissioned door-force limit).',
                           'Values are writable points (<unit>/Points/<unit>_MinSpeed, _MaxSpeed, 0-100 %): click a green value to set; defaults CHP/CDP 30 %, CT 20 %, AHU 30 %, OAU/EF 20 %.')):
        lbl(p, 30, y + 26 + i * 28, 1860, t, 10, TXT)
    return p


def meters_page():
    p = G.Page('ALT_V71_Meters', 'Meters — power, BTU, flow, outdoor air', (1920, 1080)); p.header()
    panel(p, 10, 80, 620, 420, 'MAIN POWER METER (plant MCC)', link='file:^px/ALT_V71_FP_Power.px')
    pic(p, 24, 110, 'Sensors/sensor_elecmtr.png', 80, 94)
    rows(p, 120, 108, 505, [('Active power', 'PM_Main_kW'), ('Apparent power', 'PM_Main_kVA'), ('Feeder loading', 'PM_Main_LoadPct'), ('Energy', 'PM_Main_kWh'),
                            ('Voltage L-L', 'PM_Main_Volts'), ('Current', 'PM_Main_Amps'), ('Power factor', 'PM_Main_PF'), ('Frequency', 'PM_Main_Hz'),
                            ('Communication', 'PM_Main_CommOk', {'bool_c': (RUN, FLT)}), ('Meter vs sum of loads', 'PowerMeter_DeviationAlarm', {'bool_c': (WARN, OKC)}),
                            ('Plant kW (sum)', 'Plant_kW'), ('Aux kW', 'Aux_kW'), ('Plant kWh today', 'Plant_kWh_Today'), ('Plant kW/RT', 'Plant_kW_per_RT')], lw=260, rh=26)
    panel(p, 640, 80, 620, 420, 'BTU METER (CHW)', link='file:^px/ALT_V71_FP_BTU.px')
    pic(p, 660, 120, 'Sensors/sensor_watermtr_horz_largepipe.png')
    rows(p, 640, 160, 620, [('Flow', 'BTU_Flow'), ('Supply temperature', 'BTU_SupplyTemp'), ('Return temperature', 'BTU_ReturnTemp'), ('Delta-T', 'BTU_DeltaT'),
                            ('Cooling power', 'BTU_Power_RT'), ('Energy total', 'BTU_EnergyTotal'), ('Communication', 'BTU_CommOk', {'bool_c': (RUN, FLT)}),
                            ('Valid', 'BTU_Valid', {'bool_c': (RUN, FLT)}), ('Load source in use', 'CoolingLoadSource'),
                            ('Deviation vs calculated', 'BTU_DeviationAlarm', {'bool_c': (WARN, OKC)}), ('Cooling RT-h today', 'Cooling_RTh_Today')], lw=300, rh=26)
    panel(p, 1270, 80, 640, 420, 'OUTDOOR AIR SENSOR', link='file:^px/ALT_V71_FP_OA.px')
    pic(p, 1290, 110, 'Sensors/sensor_oatemphum.png', 48, 120)
    rows(p, 1350, 108, 555, [('Dry bulb', 'OA_Temperature'), ('Relative humidity', 'OA_Humidity'), ('Wet bulb', 'OA_WetBulb'), ('Dew point', 'OA_DewPoint'),
                             ('Enthalpy', 'OA_Enthalpy'), ('Valid', 'OA_Valid', {'bool_c': (RUN, FLT)}), ('Invalid alarm', 'OA_SensorInvalidAlarm', {'bool_c': (FLT, OKC)}),
                             ('CT01 approach (to WB)', 'CT01_Approach'), ('CT02 approach (to WB)', 'CT02_Approach')], lw=280, rh=26)
    panel(p, 10, 510, 620, 330, 'FLOW METERS', link='file:^px/ALT_V71_FP_Flow.px')
    rows(p, 10, 534, 620, FLOWS, lw=300, rh=29)
    panel(p, 640, 510, 1270, 330, 'SUB-METERING (per equipment kW / A / kWh)')
    hdr = [('Equipment', 170), ('kW', 150), ('A', 150), ('kWh', 170), ('Runtime h', 150)]
    xx = 650
    for t, w in hdr: p.label(xx, 534, w - 4, 22, t, 9, True, 'white', '#2c3e50', 'center'); xx += w
    eqs = [('CH01', 'CH01_kW', 'CH01_Amps', 'CH01_kWh', 'CH01_RuntimeHours'), ('CH02', 'CH02_kW', 'CH02_Amps', 'CH02_kWh', 'CH02_RuntimeHours')] + \
          [(u, f'{u}_kW', f'{u}_Amps', f'{u}_kWh', f'{u}_RuntimeHours') for u in PLANT_VSD]
    for r, e in enumerate(eqs):
        xx = 650; yy = 560 + r * 30
        p.label(xx, yy, 166, 26, '  ' + e[0], 10, True, 'white', '#1b2631', 'left'); xx += 170
        for pt, (t, w) in zip(e[1:], hdr[1:]):
            val(p, xx, yy + 1, w - 4, pt, f'{e[0]} {t}', h=24, size=10); xx += w
    xx0 = 1450
    lbl(p, xx0, 534, 450, 'Air side fans', 10, TXT, True)
    for r, u in enumerate(AIR_VSD):
        yy = 560 + r * 30
        p.label(xx0, yy, 110, 26, '  ' + u, 10, True, 'white', '#1b3a2f', 'left', popup=f'file:^px/ALT_V71_FP_VSD_{u}.px', ptitle=u)
        val(p, xx0 + 114, yy + 1, 110, f'{u}_kW', f'{u} kW', h=24); val(p, xx0 + 228, yy + 1, 110, f'{u}_Amps', f'{u} A', h=24)
        val(p, xx0 + 342, yy + 1, 110, f'{u}_RuntimeHours', f'{u} runtime', h=24)
    panel(p, 10, 850, 1900, 220, 'COOLING TOWER WATER')
    rows(p, 10, 874, 630, [('Make-up flow', 'CT_MakeupFlow'), ('Make-up volume', 'CT_MakeupVolume'), ('Conductivity', 'CT_Conductivity'),
                           ('Conductivity high', 'CT_ConductivityHighAlarm', {'bool_c': (WARN, OKC)}), ('Basin HIGH-HIGH set %', 'CT_LevelHighHighPct', {'action': True}),
                           ('Make-up open below %', 'CT_LevelMakeupOpenPct', {'action': True}), ('Make-up close above %', 'CT_LevelMakeupClosePct', {'action': True})], lw=330, rh=26)
    for k, u in enumerate(('CT01', 'CT02')):
        rows(p, 650 + k * 630, 874, 620, [(f'{u} entering TT', f'{u}_InletTemp'), (f'{u} leaving TT', f'{u}_OutletTemp'), (f'{u} range', f'{u}_Range'),
                                          (f'{u} basin level', f'{u}_BasinLevel'), (f'{u} make-up valve', f'{u}_MakeupValveCmd', {'bool_c': (RUN, OFF)}),
                                          (f'{u} HIGH', f'{u}BasinHighLevelAlarm', {'bool_c': (WARN, OKC)}), (f'{u} HIGH-HIGH', f'{u}BasinHighHighLevelAlarm', {'bool_c': (FLT, OKC)})], lw=320, rh=26)
    return p


SCHEDULES = [('PlantSchedule', 'Chiller plant', 'PlantEnableEffective / ScheduleOk (when schedule mode = Scheduled)'),
             ('Sch_AHU', 'AHU / OAU', 'AHU01, AHU02, OAU01'), ('Sch_FCU', 'FCU', 'FCU01-FCU04'), ('Sch_EF', 'Exhaust / ventilation', 'EF01, EF02, EF03'),
             ('Sch_CarPark', 'Car park', 'CPEF01 (CO control inside schedule)')]


def schedules_page():
    p = G.Page('ALT_V71_Schedules', 'Schedules, operating set and rotation', (1920, 1080)); p.header()
    panel(p, 10, 80, 1180, 60 + 44 * len(SCHEDULES), 'WEEKLY SCHEDULES (click EDIT → native Niagara scheduler: days, times, special events, holidays)')
    cols = [('Schedule', 200), ('Serves', 330), ('Output now', 130), ('Next change', 250), ('Next value', 120), ('Edit', 130)]
    x = 20
    for t, w in cols: p.label(x, 106, w - 4, 24, t, 10, True, 'white', '#2c3e50', 'center'); x += w
    for r, (s, title, serves) in enumerate(SCHEDULES):
        y = 136 + r * 44
        o = f'station:|slot:{G7.PATH[s]}'
        p.label(20, y, 196, 36, '  ' + title, 11, True, 'white', '#1b2631', 'left', popup=o, ptitle=title + ' schedule')
        lbl(p, 222, y + 8, 326, serves, 9, TXT)
        val(p, 550, y + 4, 126, s, f'{s} output', h=28, size=11, bool_c=(RUN, OFF))
        sched_slot(p, 680, y + 4, 246, s, 'nextTime', f'{s} next time')
        sched_slot(p, 930, y + 4, 116, s, 'nextValue', f'{s} next value')
        p.label(1050, y + 4, 126, 28, 'EDIT ▸', 10, True, 'white', '#1e88e5', 'center', popup=o, ptitle=title + ' schedule')
        p.map.append((s, o, f'{title} schedule editor', 'popup (scheduler view)'))
    y = 80 + 60 + 44 * len(SCHEDULES) + 10
    panel(p, 10, y, 1180, 120, 'SCHEDULE USE')
    rows(p, 10, y + 24, 590, [('Plant schedule mode', 'PlantScheduleMode', {'action': True}), ('Plant enable (operator)', 'PlantEnable', {'bool_c': (RUN, OFF), 'action': True}),
                              ('Plant enable effective', 'PlantRunRequest', {'bool_c': (RUN, OFF)})], lw=300, rh=28)
    rows(p, 600, y + 24, 590, [('Plant demand mode', 'PlantDemandMode', {'action': True}), ('Air-side cooling calls', 'AirSide_CoolingCalls'),
                               ('Air-side units running', 'AirSide_UnitsRunning')], lw=300, rh=28)
    # ---- set + rotation
    panel(p, 1200, 80, 710, 560, 'OPERATING SET & ROTATION')
    lbl(p, 1214, 106, 690, 'SET 1 = CH01 + CHP01 + CDP01 + CT01      SET 2 = CH02 + CHP02 + CDP02 + CT02', 10, TXT, True)
    for k, (t, c) in enumerate((('SET 1', '#2471a3'), ('SET 2', '#7d3c98'))):
        xx = 1214 + k * 348
        p.rect(xx, 132, 336, 120, fill='#18212b', stroke=c, pen=2.0)
        lbl(p, xx, 136, 336, t, 14, 'white', True, 24, 'center')
        n = '01' if k == 0 else '02'
        for j, eq in enumerate(('CH', 'CHP', 'CDP', 'CT')):
            pt = f'CH{n}RunProofSelected' if eq == 'CH' else f'{eq}{n}RunProof'
            val(p, xx + 8 + j * 82, 170, 78, pt, f'{eq}{n} running', h=26, size=10, bool_c=(RUN, OFF), fmt=f'{eq}{n}')
        p.button(xx + 8, 208, 320, 34, f'SELECT {t} AS LEAD', 'LeadCH01', k == 0, f'Select {t} as lead')
    rows(p, 1200, 262, 710, [('Effective lead set', 'LeadSet', {'bool_c': ('#2471a3', '#7d3c98')}), ('Pumps / towers follow set', 'Set_LinkPools', {'action': True}),
                             ('Rotation: runtime (24 h hysteresis)', 'RotationMode_Runtime', {'action': True}),
                             ('Rotation: daily', 'RotationMode_Daily', {'action': True}), ('Rotation: weekly', 'RotationMode_Weekly', {'action': True}),
                             ('Days counted (rotation trigger)', 'RotationDayCount'), ('Manual rotate request', 'RotationRequest', {'action': True}),
                             ('Runtime CH01 / CH02 h', 'CH01_RuntimeHours'), ('', 'CH02_RuntimeHours'),
                             ('Runtime imbalance limit h', 'RuntimeRotationHours', {'action': True})], lw=380, rh=28)
    o = f'station:|slot:{G7.PATH["RotationTrigger"]}'
    p.label(1214, 548, 330, 30, 'CHANGE-OVER TIME (00:00) ▸', 10, True, 'white', '#1e88e5', 'center', popup=o, ptitle='Rotation trigger time')
    p.map.append(('RotationTrigger', o, 'Rotation change-over time (TimeTrigger)', 'popup (property sheet)'))
    lbl(p, 1214, 584, 690, 'Daily: lead set swaps every day at the trigger time. Weekly: every 7 days. Runtime mode has priority.', 9, LBL)
    lbl(p, 1214, 604, 690, 'Change-over is make-before-break (standby started and proven before the old lead stops).', 9, LBL)
    panel(p, 10, 510, 1180, 560, 'NOTES')
    for i, t in enumerate(('EDIT opens the BooleanSchedule in its default Workbench / web view (Scheduler): drag weekly blocks per day, add special events',
                           '(date, date range, week-and-day, custom) and link holiday calendars. Output now / next change / next value are live.',
                           'Schedules live in /AirSide/Schedules and /ChillerPlant/PlantControl; every unit links its schedule output into <unit>/Logic.',
                           'Plant: schedule mode = Scheduled -> plant enable follows PlantSchedule AND operator enable; demand mode -> plant follows air-side calls.',
                           'Set selection = lead chiller; with "Pumps / towers follow set" each pool leads with the same unit number; a failed unit is still',
                           'replaced by the standby of its pool (cross-set operation CHP01 + CDP02 remains possible).')):
        lbl(p, 24, 540 + i * 26, 1160, t, 10, TXT)
    return p


def sched_slot(p, x, y, w, s, slot, what):
    o = f'station:|slot:{G7.PATH[s]}'
    p.el.append(f'<BoundLabel layout="{x:.1f},{y:.1f},{w:.1f},28.0" font="bold 10.0pt sans-serif" foreground="{VAL}" background="#0b0e11" halign="center" border="1.0 solid {EDGE}">\n'
                f'  <BoundLabelBinding ord={quoteattr(o)} popupEnabled="true" statusEffect="none">\n    <ObjectToString name="text" format="%{slot}%"/>\n  </BoundLabelBinding>\n</BoundLabel>')
    p.map.append((s, o, what, f'display %{slot}%'))


def energy_dashboard():
    p = G.energy_dashboard()
    for i, e in enumerate(p.el):
        if 'gx:Brush 0.0:0.01=#eceff1' in e:
            p.el[i] = re.sub(r'map="gx:Brush 0\.0:0\.01=#eceff1[^"]*"', f'map="{KWRT_MAP}"', e)
    dark_page(p)
    ashrae_scale(p, 1600, 80, 310, 190, 'Plant_kW_per_RT', 'ASHRAE kW/RT SCALE (live)')
    for k, (t, pt) in enumerate((('Today', 'Plant_kW_per_RT_Today'), ('Yesterday', 'Plant_kW_per_RT_Yesterday'), ('This month', 'Plant_kW_per_RT_Month'),
                                 ('Last month', 'Plant_kW_per_RT_LastMonth'))):
        y = 290 + k * 60
        lbl(p, 1604, y, 300, t, 9, LBL, True)
        val(p, 1604, y + 18, 300, pt, f'kW/RT {t} (ASHRAE colour)', h=36, size=14, fg='white', fmt='%out.value% kW/RT')
        p.el[-1] = p.el[-1].replace('<ObjectToString', f'<INumericToSimple name="background" map="{KWRT_MAP}"/>\n    <ObjectToString')
    for k, (t, pt) in enumerate((('CH01 (chiller only)', 'CH01_kW_per_RT'), ('CH02 (chiller only)', 'CH02_kW_per_RT'))):
        ashrae_mini(p, 1604, 540 + k * 100, 300, pt, t)
    return p



# ================================================================ 3D page
def plant3d_page():
    import json
    p = G.Page('ALT_V71_Plant3D', 'Plant 3D (isometric render + live values)', (1920, 1080)); p.header()
    G7.kpi_strip(p)
    aj = os.path.join(OUT, 'v71_plant3d_anchors.json')
    A = json.load(open(aj))['anchors']
    Y0 = 136
    ximg(p, 0, Y0, 'v71_plant3d.png', 1920, 940, bottom=True)
    def card(key, title, fpn, run, vals, x, y, w=160, col='#2c3e50'):
        ax, ay = A[key]; ay += Y0
        h = 22 + 20 * len(vals)
        ey = y + h if ay > y + h else y
        ex = min(max(ax, x + 10), x + w - 10)
        p.line([(ax, ay), (ex, ey)], '#8fd3ff', 1.0)
        p.rect(ax - 3, ay - 3, 6, 6, fill='#8fd3ff', stroke='#0b0e11', pen=1.0)
        p.rect(x, y, w, h, fill='#0b0e11', stroke='#5dade2', pen=1.0)
        p.label(x, y, w, 20, f'  {title}  ⊞' if fpn else f'  {title}', 9, True, 'white', col, 'left', popup=f'file:^px/{fpn}.px' if fpn else None, ptitle=title)
        if run: status_led(p, x + w - 18, y + 3, run, f'{title} running', 'run')
        for i, (pre, pt) in enumerate(vals):
            tag(p, x + 2, y + 21 + i * 20, w - 4, pt, f'3D {title} {pre}', pre, size=8)
    card('CT02', 'TOWER 02', 'ALT_V71_FP_CT02', 'CT02RunProof', [('FAN', 'CT02SpeedCmd'), ('IN', 'CT02_InletTemp'), ('OUT', 'CT02_OutletTemp'), ('LVL', 'CT02_BasinLevel')], 1060, 150)
    card('CT01', 'TOWER 01', 'ALT_V71_FP_CT01', 'CT01RunProof', [('FAN', 'CT01SpeedCmd'), ('IN', 'CT01_InletTemp'), ('OUT', 'CT01_OutletTemp'), ('LVL', 'CT01_BasinLevel')], 1745, 190)
    card('CDWR', 'CDWR HEADER', None, None, [('T', 'CDR')], 1000, 380, col='#8a4a10')
    card('CH02_cdw', 'CH02 CDW', None, None, [('EWT', 'CH02_CdwEnteringTemp'), ('LWT', 'CH02_CdwLeavingTemp')], 790, 330, col='#8a4a10')
    card('CH02', 'CHILLER 02', 'ALT_V71_FP_CH02', 'CH02RunProofSelected', [('LOAD', 'CH02LoadPct'), ('kW', 'CH02_kW'), ('kW/RT', 'CH02_kW_per_RT')], 560, 420)
    card('CH02_chw', 'CH02 CHW', None, None, [('LWT', 'CH02_ChwSupplyTemp'), ('EWT', 'CH02_ChwReturnTemp')], 340, 540, col='#1a4a8a')
    card('CHWS', 'CHWS HEADER', None, None, [('T', 'CHWS'), ('P', 'CHW_SupplyHeaderPressure')], 130, 600, col='#1a4a8a')
    card('BUILDING', 'BUILDING / BTU', 'ALT_V71_FP_BTU', None, [('RT', 'BTU_Power_RT'), ('DP', 'CHWDP')], 20, 700, col='#1b3a2f')
    card('CHP02', 'CHP02', 'ALT_V71_FP_CHP02', 'CHP02RunProof', [('SPD', 'CHP02SpeedCmd'), ('PT-S', 'CHP02_SuctionPressure'), ('PT-D', 'CHP02_DischargePressure')], 20, 850)
    card('CHWR', 'CHWR / FLOW', 'ALT_V71_FP_Flow', None, [('T', 'CHWR'), ('F', 'CHWFlow')], 190, 985, col='#2a6f8f')
    card('CHP01', 'CHP01', 'ALT_V71_FP_CHP01', 'CHP01RunProof', [('SPD', 'CHP01SpeedCmd'), ('PT-S', 'CHP01_SuctionPressure'), ('PT-D', 'CHP01_DischargePressure')], 360, 985)
    card('CH01_chw', 'CH01 CHW', None, None, [('LWT', 'CH01_ChwSupplyTemp'), ('EWT', 'CH01_ChwReturnTemp')], 530, 985, col='#1a4a8a')
    card('CH01', 'CHILLER 01', 'ALT_V71_FP_CH01', 'CH01RunProofSelected', [('LOAD', 'CH01LoadPct'), ('kW', 'CH01_kW'), ('kW/RT', 'CH01_kW_per_RT')], 900, 985)
    card('CH01_cdw', 'CH01 CDW', None, None, [('EWT', 'CH01_CdwEnteringTemp'), ('LWT', 'CH01_CdwLeavingTemp')], 1070, 985, col='#8a4a10')
    card('CDP02', 'CDP02', 'ALT_V71_FP_CDP02', 'CDP02RunProof', [('SPD', 'CDP02SpeedCmd'), ('PT-S', 'CDP02_SuctionPressure'), ('PT-D', 'CDP02_DischargePressure')], 1560, 640)
    card('CDWS', 'CDWS HEADER', 'ALT_V71_FP_Flow', None, [('T', 'CDS'), ('F', 'CDW_Flow')], 1740, 640, col='#8a7a10')
    card('CDP01', 'CDP01', 'ALT_V71_FP_CDP01', 'CDP01RunProof', [('SPD', 'CDP01SpeedCmd'), ('PT-S', 'CDP01_SuctionPressure'), ('PT-D', 'CDP01_DischargePressure')], 1250, 985)
    for u in ('CT01', 'CT02'):
        ax, ay = A[f'{u}_basin']
        val(p, ax - 40, ay + Y0 + 8, 80, f'{u}BasinHighHighLevelAlarm', f'{u} HH level (3D)', h=18, size=8, bool_c=(FLT, OKC), fmt='HH LEVEL')
    ashrae_mini(p, 1600, 985, 300, 'Plant_kW_per_RT', 'PLANT kW/RT (ASHRAE scale)')
    for i, (t, c) in enumerate((('CHWS', '#1665d6'), ('CHWR', '#5ec4f2'), ('CDWS', '#f2c416'), ('CDWR', '#f07a12'))):
        p.rect(20 + i * 100, 146, 26, 10, fill=c, stroke=c, pen=1.0); lbl(p, 50 + i * 100, 140, 60, t, 8, TXT, True)
    lbl(p, 20, 162, 700, 'Rendered with Blender (bpy / Cycles) from tools/plant3d.py — click a card title for the equipment faceplate.', 8, LBL)
    p.rect(420, 146, 14, 10, fill='#c0392b', stroke='#c0392b', pen=1.0); lbl(p, 438, 140, 200, 'valve actuator: on/off isolation', 8, TXT, True)
    p.rect(650, 146, 14, 10, fill='#1e8449', stroke='#1e8449', pen=1.0); lbl(p, 668, 140, 200, 'modulating 0-100 %', 8, TXT, True)
    return p


# ================================================================ main
def build(pages, outdir, H, A):
    rows_, bad = [], []
    for p in pages:
        x = p.xml()
        ET.fromstring(x.encode('utf-8'))
        with open(os.path.join(outdir, 'px', p.name + '.px'), 'w', encoding='utf-8') as f: f.write(x)
        for pt, o, what, mode in p.map:
            if pt != '(BQL)' and not o.startswith('history:') and pt not in G7.PATH: bad.append((p.name, pt))
            rows_.append({'Graphic': p.name + '.px', 'Element': what, 'Point': pt, 'ORD': o, 'Binding': mode,
                          'History_ID': '; '.join(r['History_ID'] for r in H.get(pt, [])),
                          'Alarm': '; '.join(f"{r['Alarm_Type']}/{r['Alarm_Class']}" for r in A.get(pt, []))})
        imgs = re.findall(r'module://kitPxGraphics/([^";]+)', x)
        bad += [(p.name, 'image ' + i) for i in set(imgs) if not os.path.exists(os.path.join(G7.KITDIR, i))]
        own = re.findall(r'file:\^px/img/([^";]+)', x)
        bad += [(p.name, 'img ' + i) for i in set(own) if not os.path.exists(os.path.join(outdir, 'px', 'img', i))]
        files = re.findall(r'file:\^px/([^"/]+)\.px', x)
        known = {n for n, _ in PAGES} | set(FACEPLATES)
        bad += [(p.name, 'page ' + f) for f in files if f not in known and not os.environ.get('PARTIAL')]
        print(f'{p.name:32} {len(p.el):4} elements {len(p.map):4} bindings {len(set(imgs)):3} kit images')
    assert not bad, bad[:20]
    return rows_


if __name__ == '__main__':
    bog, G7.KITDIR, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
    G7.PATH.update(G7.load_paths(bog))
    G.FOLDER = {n: p.rsplit('/', 1)[0].replace('/ChillerPlant/', '').replace('/ChillerPlant', '') for n, p in G7.PATH.items()}
    G.STATION_NAME = STATION
    G.PAGES = PAGES; G7.PAGES = PAGES
    regdir = sys.argv[4] if len(sys.argv) > 4 else os.path.join(os.path.dirname(os.path.abspath(bog)), 'reg71')
    H, A = (G.read_reg(os.path.join(regdir, f)) for f in ('V7_HISTORY_REGISTER.csv', 'V7_ALARM_REGISTER.csv'))
    os.makedirs(os.path.join(OUT, 'px', 'img'), exist_ok=True)
    only = os.environ.get('ONLY')
    pages = [plant_page(), plant3d_page() if 'plant3d_page' in globals() else None, chillers_page(), G7.plant_detail(), drives_page(), valves_page(), meters_page(), schedules_page(),
             dark_page(G.optimization()), energy_dashboard(), dark_page(G.energy()), dark_page(G.alarms_history()), dark_page(G.simulation()),
             G7.airside_page(), G7.ahu_page('AHU01'), G7.ahu_page('AHU02'), G7.oau_page('OAU01'), G7.fcu_page(), G7.vent_page()]
    pages += [fp_ch('01'), fp_ch('02')] + [fp_pump(u) for u in ('CHP01', 'CHP02', 'CDP01', 'CDP02')] + [fp_ct('CT01'), fp_ct('CT02')]
    pages += [fp_air_vsd(u) for u in AIR_VSD] + [fp_btu(), fp_power(), fp_flow(), fp_oa()]
    pages = [q for q in pages if q is not None]
    if only: pages = [q for q in pages if any(o in q.name for o in only.split(','))]
    rows_ = build(pages, OUT, H, A)
    with open(os.path.join(OUT, 'V7_1_GRAPHIC_POINT_MAPPING.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows_[0].keys())); w.writeheader(); w.writerows(rows_)
    print('bindings', len(rows_), 'distinct points', len({r['Point'] for r in rows_ if r['Point'] != '(BQL)'}), 'images', IMG)
