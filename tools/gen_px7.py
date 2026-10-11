"""V7 Px graphics: realistic plant + air-side pages built from the Niagara kitPxGraphics library.

Vocabulary (checked against this installation):
  * Picture + ValueBinding + IBooleanToSimple/INumericToSimple name="image" with <Image .../>   (ST5130 'Chiller Plant.px',
    kitPxGraphics / kitPxN4svg module.palette)
  * module://kitPxGraphics/... image ords exactly as in the kitPxGraphics-wb palette (pumps/chillers/towers On.gif / Off.png,
    large_piping tiles, valves, sensors, coils 0-4, dampers 0-4, filters, fans, FCU, roof exhaust)
  * Pipes are composed from the fixed-size large_piping tiles (10 px pipe); fittings (elbow / tee / 4-way) are chosen
    automatically from the pipe graph so every joint is a real kitPx fitting.
usage: gen_px7.py v7.bog kitdir outdir
"""
import sys, os, re, csv, zipfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr
from collections import defaultdict
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_px as G

KG = 'module://kitPxGraphics'
BG, PANEL, EDGE, LBL, VAL, TXT = '#12161b', '#1f252c', '#3b4652', '#9aa5b1', '#ffe066', '#e8edf2'
RUN, OFF, FLT, WARN = '#2ecc71', '#5d6d7e', '#e74c3c', '#f39c12'
PAGES = [('ALT_V7_Plant', 'Plant'), ('ALT_V7_PlantDetail', 'Plant Detail'), ('ALT_CP_Optimization', 'Optimisation'),
         ('ALT_CP_EnergyDashboard', 'Energy Dash'), ('ALT_CP_Energy', 'Energy & KPI'), ('ALT_CP_AlarmsHistory', 'Alarms/History'),
         ('ALT_CP_Simulation', 'Simulation'), ('ALT_V7_AirSide', 'Air Side'), ('ALT_V7_AHU01', 'AHU-01'), ('ALT_V7_AHU02', 'AHU-02'),
         ('ALT_V7_OAU01', 'OAU-01'), ('ALT_V7_FCU', 'FCU'), ('ALT_V7_Ventilation', 'Ventilation')]
PATH = {}
KITDIR = None
SIZE = {}


def img_size(rel):
    if rel not in SIZE:
        SIZE[rel] = Image.open(os.path.join(KITDIR, rel)).size
    return SIZE[rel]


# ---------------------------------------------------------------- Page extensions
def _ord(self, point):
    return f'station:|slot:{PATH[point]}'


def _header(self):
    W = self.size[0]
    dark = self.name.startswith('ALT_V7')
    self.rect(0, 0, W, self.size[1], fill=BG if dark else '#eceff1', stroke=BG if dark else '#eceff1', pen=1.0)
    self.label(0, 0, W, 40, f'  ALT Reference V7 — {self.title}', 18, True, 'white', '#0b0e11')
    self.label(W - 470, 8, 460, 24, 'REFERENCE SIMULATION – NOT PROJECT APPROVED', 10, True, '#263238', '#ffca28', 'center')
    x = 8
    for name, title in PAGES:
        cur = name == self.name
        self.label(x, 44, 116, 26, title, 9, True, 'white' if cur else '#cfd8dc', '#1e88e5' if cur else '#2c3440', 'center',
                   popup=None if cur else f'file:^px/{name}.px', ptitle=title)
        x += 120


G.Page.ord = _ord


def _table(self, x, y, w, h, bql, what):
    o = f'station:|slot:/|bql:{bql}'              # whole station: ChillerPlant + AirSide
    self.el.append(f'<BoundTable layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}">\n  <TableBinding ord={quoteattr(o)}/>\n</BoundTable>')
    self.map.append(('(BQL)', o, what, 'table'))


G.Page.table = _table
G.Page.header = _header


def pic(p, x, y, rel, w=None, h=None):
    w0, h0 = img_size(rel)
    p.el.append(f'<Picture layout="{x:.1f},{y:.1f},{(w or w0):.1f},{(h or h0):.1f}" image="{KG}/{rel}"/>')


def pic_bool(p, x, y, point, on, off, what):
    w, h = img_size(off)
    o = p.ord(point)
    p.el.append(f'<Picture layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" image="{KG}/{off}">\n'
                f'  <ValueBinding ord={quoteattr(o)}>\n    <IBooleanToSimple name="image">\n'
                f'      <Image name="trueValue" value="{KG}/{on}"/>\n      <Image name="falseValue" value="{KG}/{off}"/>\n'
                f'    </IBooleanToSimple>\n  </ValueBinding>\n</Picture>')
    p.map.append((point, o, what, 'display (image on/off)'))


def pic_pct(p, x, y, point, base, n, what):
    """5/6-state kitPx images (coil / damper / filter) by 0-100 % value, map as in the kitPxGraphics palette."""
    w, h = img_size(f'{base}_0.png')
    o = p.ord(point)
    step = 100.0 / (n - 1)
    edges = [-1e9] + [step * (i + 0.5) for i in range(n - 1)] + [1e9]
    parts = []
    for i in range(n):
        lo = '-inf' if i == 0 else f'{edges[i]:.1f}'
        hi = '+inf' if i == n - 1 else f'{edges[i + 1]:.1f}'
        parts.append(f'{lo}:{hi}={KG}/{base}_{i}.png')
    mp = 'gx:Image ' + ';'.join(parts) + f';default={KG}/{base}_0.png;'
    p.el.append(f'<Picture layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" image="{KG}/{base}_0.png">\n'
                f'  <ValueBinding ord={quoteattr(o)}>\n    <INumericToSimple name="image" map="{mp}"/>\n  </ValueBinding>\n</Picture>')
    p.map.append((point, o, what, 'display (image by %)'))


def val(p, x, y, w, point, what, h=20, size=10, fg=VAL, bool_c=None, action=False, fmt='%out.value%'):
    o = p.ord(point)
    conv = f'    <ObjectToString name="text" format={quoteattr(fmt)}/>\n'
    if bool_c:
        conv += f'    <IBooleanToSimple name="background">\n      <Brush name="trueValue" value="{bool_c[0]}"/>\n      <Brush name="falseValue" value="{bool_c[1]}"/>\n    </IBooleanToSimple>\n'
    inner = f'  <ActionBinding ord={quoteattr(o + "/set")} widgetEvent="actionPerformed"/>\n' if action else ''
    inner += f'  <BoundLabelBinding ord={quoteattr(o)} popupEnabled="true" statusEffect="none">\n{conv}  </BoundLabelBinding>\n'
    fgc = 'white' if bool_c else fg
    p.el.append(f'<BoundLabel layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" font="bold {size:.1f}pt sans-serif" foreground="{fgc}" '
                f'background="#0b0e11" halign="center" border="1.0 solid #3b4652"{" mouseOver=" + chr(34) + "outline" + chr(34) if action else ""}>\n{inner}</BoundLabel>')
    p.map.append((point, o, what, 'write (set)' if action else 'display'))


def lbl(p, x, y, w, text, size=9, fg=LBL, bold=False, h=20, halign='left', bg=None):
    p.label(x, y, w, h, text, size, bold, fg, bg, halign)


def panel(p, x, y, w, h, title, link=None):
    p.rect(x, y, w, h, fill=PANEL, stroke=EDGE, pen=1.0)
    if link:
        p.label(x, y, w, 20, '  ' + title + '  ⊞', 10, True, 'white', '#2c3e50', 'left', popup=link, ptitle=title)
    else:
        p.label(x, y, w, 20, '  ' + title, 10, True, 'white', '#2c3e50')


def rows(p, x, y, w, items, lw=None, rh=21):
    lw = lw or int(w * 0.52)
    for i, it in enumerate(items):
        text, pt = it[0], it[1]
        kw = it[2] if len(it) > 2 else {}
        lbl(p, x + 4, y + i * rh, lw - 4, text)
        val(p, x + lw, y + i * rh + 1, w - lw - 4, pt, f'{text}', h=rh - 3, **kw)


def status_led(p, x, y, point, what, mode='run'):
    cols = {'run': (RUN, OFF), 'alarm': (FLT, '#1f6f43'), 'warn': (WARN, '#1f6f43')}[mode]
    o = p.ord(point)
    p.el.append(f'<BoundLabel layout="{x:.1f},{y:.1f},14.0,14.0" border="1.0 solid #0b0e11">\n'
                f'  <BoundLabelBinding ord={quoteattr(o)} popupEnabled="true" statusEffect="none">\n'
                f'    <ObjectToString name="text" format=""/>\n    <IBooleanToSimple name="background">\n'
                f'      <Brush name="trueValue" value="{cols[0]}"/>\n      <Brush name="falseValue" value="{cols[1]}"/>\n'
                f'    </IBooleanToSimple>\n  </BoundLabelBinding>\n</BoundLabel>')
    p.map.append((point, o, what, 'display (LED)'))


# ---------------------------------------------------------------- pipes from kitPx tiles
class Pipes:
    """Orthogonal pipe network per service colour, rendered with kitPxGraphics large_piping tiles.
    add(colour, [(x,y), ...]) with centre-line coordinates; fittings are derived from the node degree."""
    def __init__(self):
        self.segs = defaultdict(list)

    def add(self, c, pts):
        for a, b in zip(pts, pts[1:]):
            assert a[0] == b[0] or a[1] == b[1], (c, a, b)
            self.segs[c].append((a, b))

    def render(self, p):
        for c, segs in self.segs.items():
            nodes = defaultdict(set)
            pts = {q for s in segs for q in s}
            for a, b in segs:                                   # split at every point lying on the segment
                for q in pts:
                    if a[0] == b[0] == q[0] and min(a[1], b[1]) < q[1] < max(a[1], b[1]) or \
                       a[1] == b[1] == q[1] and min(a[0], b[0]) < q[0] < max(a[0], b[0]):
                        pass
            cut = []
            for a, b in segs:
                on = sorted([q for q in pts if (a[0] == b[0] == q[0] and min(a[1], b[1]) <= q[1] <= max(a[1], b[1])) or
                             (a[1] == b[1] == q[1] and min(a[0], b[0]) <= q[0] <= max(a[0], b[0]))])
                cut += list(zip(on, on[1:]))
            for a, b in cut:
                for q, r in ((a, b), (b, a)):
                    d = ('E' if r[0] > q[0] else 'W') if r[1] == q[1] else ('S' if r[1] > q[1] else 'N')
                    nodes[q].add(d)
            fit = {}
            for q, ds in nodes.items():
                if len(ds) == 2 and ds in ({'E', 'W'}, {'N', 'S'}): continue
                if len(ds) == 1: continue
                fit[q] = ds
            # straight runs, trimmed at fittings
            for a, b in cut:
                (x1, y1), (x2, y2) = sorted([a, b])
                t1 = 15 if a in fit or b in fit else 0
                if y1 == y2:
                    s = x1 + (15 if (x1, y1) in fit else 0); e = x2 - (15 if (x2, y2) in fit else 0)
                    self.run(p, c, 'hor', s, e, y1)
                else:
                    s = y1 + (15 if (x1, y1) in fit else 0); e = y2 - (15 if (x2, y2) in fit else 0)
                    self.run(p, c, 'vert', s, e, x1)
            for (x, y), ds in fit.items():
                key = ''.join(sorted(ds))
                name, dx, dy = {'EN': ('elbow_NE', -5, -15), 'NW': ('elbow_NW', -15, -15), 'ES': ('elbow_SE', -5, -5), 'SW': ('elbow_SW', -15, -5),
                                'ESW': ('tee_down', -15, -5), 'ENW': ('tee_up', -15, -15), 'NSW': ('tee_left', -15, -15),
                                'ENS': ('tee_right', -5, -15), 'ENSW': ('4-way', -15, -15)}[key]
                pic(p, x + dx, y + dy, f'Piping/large_piping/{c}/{c}_{name}.png')

    def run(self, p, c, o, s, e, k):
        L = e - s
        if L <= 0: return
        tiles = sorted(((i, img_size(f'Piping/large_piping/{c}/{c}_{o}_{i}.png')) for i in range(1, 7)), key=lambda t: -t[1][0 if o == 'hor' else 1])
        pos = s
        while pos < e:
            rem = e - pos
            pick = next(((i, sz) for i, sz in tiles if (sz[0] if o == 'hor' else sz[1]) <= rem), tiles[-1])
            ln = pick[1][0] if o == 'hor' else pick[1][1]
            at = pos if ln <= rem else e - ln                     # last (short) piece aligned to the end, overlapping
            rel = f'Piping/large_piping/{c}/{c}_{o}_{pick[0]}.png'
            if o == 'hor': pic(p, at, k - 15, rel)
            else: pic(p, k - 5, at, rel)
            pos += ln


# ---------------------------------------------------------------- plant page
def kpi_strip(p, y=80):
    items = [('Plant', 'PlantRunRequest', {'bool_c': (RUN, OFF)}), ('Stage', 'PlantStage', {}), ('Mode', 'OperationMode', {'bool_c': ('#8e44ad', '#34495e')}),
             ('CHWS SP', 'CHW_LeavingTemperatureSetpoint_ACTIVE', {}), ('CHWS', 'CHWS', {}), ('CHWR', 'CHWR', {}),
             ('Load', 'CoolingLoad_RT', {}), ('Plant kW', 'Plant_kW', {}), ('kW/RT', 'Plant_kW_per_RT', {}), ('COP', 'Plant_COP', {}),
             ('OA DB', 'OA_Temperature', {}), ('OA WB', 'OA_WetBulb', {})]
    x = 8
    for t, pt, kw in items:
        p.rect(x, y, 112, 48, fill=PANEL, stroke=EDGE, pen=1.0)
        lbl(p, x, y + 2, 112, t, 9, LBL, halign='center', h=16)
        val(p, x + 6, y + 20, 100, pt, t, h=24, size=12, **kw)
        x += 116
    p.fire(x + 6, y + 2, 150, 22, 'RESET ALL', 'PlantAlarmResetFire', 'Reset all program lockouts / pool failures')
    p.button(x + 6, y + 26, 72, 22, 'PLANT ON', 'PlantEnable', True, 'Plant enable')
    p.button(x + 84, y + 26, 72, 22, 'OFF', 'PlantEnable', False, 'Plant disable')
    p.button(x + 164, y + 2, 90, 22, 'QUALIFY', 'BootQualified', True, 'Boot qualified')
    p.button(x + 164, y + 26, 90, 22, 'AI / LOCAL', 'ModeCmd_UI', True, 'AI request')


def plant_page():
    p = G.Page('ALT_V7_Plant', 'Chiller Plant (headered pools)', (1920, 1080)); p.header()
    kpi_strip(p)
    P_ = Pipes()
    CH = {'01': 410, '02': 630}                       # chiller image top y
    CHX = 840
    # condenser water: tower outlets -> CDWS header -> CDP suction header -> pumps -> discharge header -> condensers -> CDWR riser -> towers
    P_.add('cwr', [(300, 215), (300, 170), (750, 170), (750, CH['02'] + 40)])
    P_.add('cwr', [(480, 170), (480, 215)])
    for n, y in CH.items():
        P_.add('cwr', [(750, y + 40), (CHX + 20, y + 40)])
    P_.add('cws', [(300, 330), (300, 370), (520, 370), (520, CH['02'] + 115)])
    P_.add('cws', [(480, 330), (480, 370)])
    for n, y in CH.items():
        P_.add('cws', [(520, y + 115), (575, y + 115)])
        P_.add('cws', [(665, y + 90), (710, y + 90)])
        P_.add('cws', [(710, y + 90), (CHX + 20, y + 90)])
    P_.add('cws', [(710, CH['01'] + 90), (710, CH['02'] + 90)])
    # chilled water: evaporators -> CHWS riser -> CHWS header -> building -> CHWR header -> CHP suction -> pumps -> discharge header -> evaporators
    P_.add('chws', [(1090, CH['02'] + 40), (1090, 300), (1760, 300)])
    for n, y in CH.items():
        P_.add('chws', [(CHX + 160, y + 40), (1090, y + 40)])
    P_.add('chwr', [(1760, 880), (1340, 880), (1340, CH['01'] + 115)])
    for n, y in CH.items():
        P_.add('chwr', [(1340, y + 115), (1285, y + 115)])
        P_.add('chwr', [(1190, y + 90), (1130, y + 90)])
        P_.add('chwr', [(1130, y + 90), (CHX + 160, y + 90)])
    P_.add('chwr', [(1130, CH['01'] + 90), (1130, CH['02'] + 90)])
    P_.add('chwr', [(1560, 300), (1560, 880)])        # bypass / decoupler (min-flow bypass valve)
    P_.add('chwr', [(1680, 880), (1680, 840)])        # expansion tank connection
    P_.render(p)
    # ---- cooling towers
    for n, x in (('01', 220), ('02', 400)):
        pic_bool(p, x, 200, f'CT{n}RunProof', 'CoolingTowers/PushThru/CoolingTower_PushThru_Left/CoolingTower_PushThru_Left_On.gif',
                 'CoolingTowers/PushThru/CoolingTower_PushThru_Left/CoolingTower_PushThru_Left_Off.png', f'CT{n} fan image')
        pic(p, x + 60 + 20 - 20, 172, 'Valves/valve_2way_elec_top.png')
        status_led(p, x + 106, 180, f'CT{n}ValveOpenProof', f'CT{n} isolation valve open')
    panel(p, 10, 140, 200, 196, 'CT01 / CT02', link=None)
    lbl(p, 90, 162, 55, 'CT01', 9, TXT, True, halign='center'); lbl(p, 148, 162, 55, 'CT02', 9, TXT, True, halign='center')
    for i, (t, a) in enumerate((('Status', 'RunProof'), ('Speed %', 'SpeedCmd'), ('Hz', '_FanSpeedHz'), ('kW', '_kW'), ('Basin %', '_BasinLevel'),
                                ('Valve', 'ValveOpenProof'), ('Failed', 'FailLatch'))):
        yy = 182 + i * 21
        lbl(p, 14, yy, 76, t)
        for j, n in enumerate(('01', '02')):
            pt = f'CT{n}{a}'
            kw = {'bool_c': (RUN, OFF)} if a in ('RunProof', 'ValveOpenProof') else {'bool_c': (FLT, '#1f6f43')} if a == 'FailLatch' else {}
            val(p, 90 + j * 58, yy + 1, 55, pt, f'CT{n} {t}', h=18, size=9, **kw)
    p.fire(14, 340, 90, 20, 'RESET CT01', 'CT01ResetFire', 'Reset CT01 failure'); p.fire(108, 340, 90, 20, 'RESET CT02', 'CT02ResetFire', 'Reset CT02 failure')
    # tower sensors
    pic(p, 530, 353, 'Sensors/sensor_pipe_welltemp2_hor_top.png'); val(p, 572, 342, 62, 'CDS', 'CDW supply temp')
    pic(p, 560, 153, 'Sensors/sensor_pipe_welltemp2_hor_top.png'); val(p, 602, 142, 62, 'CDR', 'CDW return temp')
    lbl(p, 572, 322, 120, 'CDWS  SP', 8); val(p, 636, 342, 62, 'CDS_Setpoint_ACTIVE', 'CDW SP')
    lbl(p, 560, 122, 180, 'CDW flow / header press.', 8); val(p, 666, 142, 68, 'CDW_Flow', 'CDW header flow')
    # ---- condenser pumps
    for n, y in CH.items():
        u = f'CDP{n}'
        pic_bool(p, 560, y + 60, f'{u}RunProof', 'Pumps/Pumps_Base/Pump_Base_Right/Pump_Base_Right_On.gif',
                 'Pumps/Pumps_Base/Pump_Base_Right/Pump_Base_Right_Off.png', f'{u} image')
        panel(p, 330, y + 30, 180, 150, u)
        rows(p, 330, y + 52, 180, [('Status', f'{u}RunProof', {'bool_c': (RUN, OFF)}), ('Speed %', f'{u}SpeedCmd'), ('kW / A', f'{u}_kW'),
                                   ('dP kPa', f'{u}_DiffPressure'), ('Auto', f'{u}InAuto', {'bool_c': (RUN, WARN)}), ('Failed', f'{u}FailLatch', {'bool_c': (FLT, '#1f6f43')})], lw=78)
        p.fire(560, y + 150, 110, 20, f'RESET {u}', f'{u}ResetFire', f'Reset {u} failure')
    # ---- chillers
    for n, y in CH.items():
        c = f'CH{n}'
        pic_bool(p, CHX, y, f'{c}RunProofSelected', 'Chillers/Turbo/Chiller_Turbo_Left/Chiller_Turbo_Left_On.gif',
                 'Chillers/Turbo/Chiller_Turbo_Left/Chiller_Turbo_Left_Off.png', f'Chiller {n} image')
        pic(p, 770, y + 20, 'Valves/valve_2way_elec_top.png'); status_led(p, 812, y + 22, f'{c}CdwValveOpenProof', f'{c} CDW valve open')
        pic(p, 1030, y + 20, 'Valves/valve_2way_elec_top.png'); status_led(p, 1072, y + 50, f'{c}ValveOpenProof', f'{c} CHW valve open')
        lbl(p, CHX, y - 22, 180, f'CHILLER {n}', 11, TXT, True, halign='center')
        yy = y + 128
        lbl(p, CHX - 10, yy, 60, 'Load'); val(p, CHX + 40, yy + 1, 52, f'{c}LoadPct', f'{c} load', h=18, size=9)
        lbl(p, CHX + 96, yy, 34, 'kW'); val(p, CHX + 124, yy + 1, 60, f'{c}_kW', f'{c} kW', h=18, size=9)
        lbl(p, CHX - 10, yy + 20, 60, 'kW/RT'); val(p, CHX + 40, yy + 21, 52, f'{c}_kW_per_RT', f'{c} kW/RT', h=18, size=9)
        lbl(p, CHX + 96, yy + 20, 34, 'Flow'); val(p, CHX + 124, yy + 21, 60, f'{c}_ChwFlow', f'{c} CHW flow', h=18, size=9)
        lbl(p, CHX - 10, yy + 40, 60, 'LWT/EWT'); val(p, CHX + 40, yy + 41, 52, f'{c}_ChwSupplyTemp', f'{c} CHW leaving', h=18, size=9)
        val(p, CHX + 96, yy + 41, 52, f'{c}_ChwReturnTemp', f'{c} CHW entering', h=18, size=9)
        val(p, CHX + 152, yy + 41, 34, f'{c}TimeoutLockout', f'{c} lockout', h=18, size=8, bool_c=(FLT, '#1f6f43'), fmt='LO')
        p.fire(CHX + 190, y + 2, 64, 20, 'RESET', f'{c}ResetFire', f'{c} reset')
        status_led(p, CHX + 190, y + 28, f'{c}InAuto', f'{c} remote')
        lbl(p, CHX + 206, y + 24, 60, 'Remote', 8)
    # ---- chilled water pumps
    for n, y in CH.items():
        u = f'CHP{n}'
        pic_bool(p, 1180, y + 60, f'{u}RunProof', 'Pumps/Pumps_Base/Pump_Base_Left/Pump_Base_Left_On.gif',
                 'Pumps/Pumps_Base/Pump_Base_Left/Pump_Base_Left_Off.png', f'{u} image')
        panel(p, 1350, y + 30, 160, 150, u)
        rows(p, 1350, y + 52, 160, [('Status', f'{u}RunProof', {'bool_c': (RUN, OFF)}), ('Speed %', f'{u}SpeedCmd'), ('kW', f'{u}_kW'),
                                    ('dP kPa', f'{u}_DiffPressure'), ('Auto', f'{u}InAuto', {'bool_c': (RUN, WARN)}), ('Failed', f'{u}FailLatch', {'bool_c': (FLT, '#1f6f43')})], lw=70)
        p.fire(1185, y + 150, 110, 20, f'RESET {u}', f'{u}ResetFire', f'Reset {u} failure')
    # ---- CHW header instruments
    pic(p, 1150, 273, 'Sensors/sensor_pipe_welltemp2_hor_top.png'); val(p, 1192, 262, 62, 'CHWS', 'CHWS header temp')
    pic(p, 1270, 262, 'Sensors/sensor_mpress.png', 22, 34); val(p, 1296, 262, 70, 'CHW_SupplyHeaderPressure', 'CHW supply pressure')
    p.rect(1380, 250, 120, 40, fill='#154360', stroke='#5dade2', pen=1.0); lbl(p, 1380, 250, 120, 'BTU METER', 9, 'white', True, 18, 'center')
    val(p, 1386, 268, 108, 'BTU_Power_RT', 'BTU power', h=18, size=9)
    val(p, 1540, 262, 80, 'CHWDP', 'CHW differential pressure'); lbl(p, 1540, 238, 120, 'dP / SP', 8); val(p, 1624, 262, 60, 'CHWDP_Setpoint_ACTIVE', 'DP SP')
    pic(p, 1420, 853, 'Sensors/sensor_pipe_welltemp2_hor_top.png'); val(p, 1462, 842, 70, 'CHWR', 'CHWR header temp')
    lbl(p, 1370, 816, 90, 'CHWR / flow', 8); val(p, 1462, 818, 82, 'CHWFlow', 'CHW flow')
    pic(p, 1545, 570, 'Valves/valve_2way_elec_left.png'); lbl(p, 1582, 546, 150, 'MIN-FLOW BYPASS', 8, TXT, True)
    val(p, 1582, 568, 64, 'CHW_BypassValveCmd', 'Bypass valve cmd'); val(p, 1650, 568, 64, 'CHW_BypassValveFeedback', 'Bypass feedback')
    lbl(p, 1582, 590, 60, 'Flow', 8); val(p, 1650, 590, 64, 'CHW_BypassFlow', 'Bypass flow')
    pic(p, 1660, 766, 'Tanks/Expansion/Tank_Expansion_Top.png'); lbl(p, 1600, 740, 150, 'EXP. TANK', 8, TXT, True)
    val(p, 1576, 800, 82, 'CHW_ExpansionTankPressure', 'Expansion tank pressure')
    # building block
    p.rect(1762, 280, 140, 620, fill='#1b2631', stroke='#5d6d7e', pen=2.0)
    p.label(1762, 290, 140, 40, 'BUILDING', 13, True, TXT, None, 'center', popup='file:^px/ALT_V7_AirSide.px', ptitle='Air side')
    lbl(p, 1768, 330, 130, 'AHU / OAU / FCU  ⊞', 9, LBL, halign='center')
    rows(p, 1766, 360, 132, [('Calls', 'AirSide_CoolingCalls'), ('Requests', 'AirSide_ChwRequests'), ('Running', 'AirSide_UnitsRunning'),
                             ('Reset %', 'PlantResetPct'), ('Fire', 'FireModeActive', {'bool_c': (FLT, '#1f6f43')})], lw=62)
    # ---- pools / plant status
    panel(p, 10, 900, 520, 170, 'EQUIPMENT POOLS (any pump / tower serves any chiller)')
    for i, eq in enumerate(('CHP', 'CDP', 'CT')):
        yy = 924 + i * 44
        lbl(p, 16, yy, 44, eq, 10, TXT, True)
        lbl(p, 60, yy, 40, 'Lead'); val(p, 98, yy + 1, 70, f'{eq}_Lead', f'{eq} lead', h=18, size=9)
        lbl(p, 172, yy, 60, 'Runtime'); val(p, 226, yy + 1, 64, f'{eq}_RotationMode_Runtime', f'{eq} rotation mode', h=18, size=9, action=True)
        val(p, 294, yy + 1, 110, f'{eq}_PoolDegradedAlarm', f'{eq} standby lost', h=18, size=9, bool_c=(WARN, '#1f6f43'))
        val(p, 408, yy + 1, 116, f'{eq}_PoolUnavailableAlarm', f'{eq} none available', h=18, size=9, bool_c=(FLT, '#1f6f43'), fmt='No unit: %out.value%')
        if i == 0:
            lbl(p, 60, yy + 20, 100, 'Stage-2 blocked', 8); val(p, 160, yy + 21, 70, 'Stage2BlockedByPoolAlarm', 'Stage 2 blocked', h=18, size=8, bool_c=(WARN, '#1f6f43'))
    panel(p, 540, 900, 600, 170, 'PLANT ALARMS (program + equipment)')
    al = [('All chillers unavailable', 'AllChillersUnavailableAlarm'), ('CHW flow low', 'CHW_FlowLowAlarm'), ('CDW flow low', 'CDW_FlowLowAlarm'),
          ('CHWST not tracking', 'CHWST_NotTrackingAlarm'), ('Low delta-T', 'LowDeltaTAlarm'), ('CH01 hard lockout', 'CH01HardLockoutAlarm'),
          ('CH02 hard lockout', 'CH02HardLockoutAlarm'), ('BTU invalid', 'BTU_InvalidAlarm'), ('CT01 basin low', 'CT01BasinLowLevelAlarm'),
          ('CT02 basin low', 'CT02BasinLowLevelAlarm'), ('Conductivity high', 'CT_ConductivityHighAlarm'), ('Expansion tank', 'CHW_ExpansionTankPressure')]
    for i, (t, pt) in enumerate(al[:11]):
        cx, cy = 546 + (i // 6) * 296, 924 + (i % 6) * 24
        status_led(p, cx, cy + 3, pt, t, 'alarm'); lbl(p, cx + 18, cy, 270, t, 9, TXT)
    panel(p, 1150, 900, 600, 170, 'CONTROL')
    rows(p, 1150, 924, 300, [('Plant enable', 'PlantEnable', {'bool_c': (RUN, OFF), 'action': True}), ('Schedule mode', 'PlantScheduleMode', {'action': True}),
                             ('Demand mode', 'PlantDemandMode', {'action': True}), ('Towers: all healthy', 'CT_RunAllAvailable', {'action': True}),
                             ('Load source', 'CoolingLoadSource'), ('Reset source', 'PlantResetSource')], lw=150)
    rows(p, 1452, 924, 294, [('Stage 2 request', 'Stage2Request', {'bool_c': (RUN, OFF)}), ('Lead chiller', 'LeadCH01'), ('CHWS valid', 'CHWS_SensorInvalidAlarm', {'bool_c': (FLT, '#1f6f43')}),
                             ('Plant main kW', 'PM_Main_kW'), ('Plant kWh today', 'Plant_kWh_Today'), ('Cost today THB', 'Energy_Cost_THB_Today')], lw=150)
    lbl(p, 1760, 1050, 150, 'kitPxGraphics images', 8, '#566573')
    return p


def plant_detail():
    p = G.Page('ALT_V7_PlantDetail', 'Plant instruments & diagnostics', (1920, 1080)); p.header()
    x = 10
    for n in ('01', '02'):
        c = f'CH{n}'
        panel(p, x, 80, 470, 560, f'CHILLER {n}  (TT / FM / DPT / power meter / BACnet)')
        items = [('Run proof', f'{c}RunProofSelected', {'bool_c': (RUN, OFF)}), ('Remote (auto)', f'{c}InAuto', {'bool_c': (RUN, WARN)}),
                 ('Load %', f'{c}LoadPct'), ('Power kW', f'{c}_kW'), ('Current A', f'{c}_Amps'), ('Voltage V', f'{c}_Volts'), ('Power factor', f'{c}_PF'),
                 ('Energy kWh', f'{c}_kWh'), ('CHW leaving / entering', f'{c}_ChwSupplyTemp'), ('CHW entering', f'{c}_ChwReturnTemp'), ('CHW delta-T', f'{c}_DeltaT'),
                 ('CHW flow m3/h', f'{c}_ChwFlow'), ('Evap dP kPa', f'{c}_EvapDP'), ('CDW entering', f'{c}_CdwEnteringTemp'), ('CDW leaving', f'{c}_CdwLeavingTemp'),
                 ('CDW flow m3/h', f'{c}_CdwFlow'), ('Cond dP kPa', f'{c}_CondDP'), ('Evap sat. temp', f'{c}_EvapSatTemp'), ('Cond sat. temp', f'{c}_CondSatTemp'),
                 ('Evap approach K', f'{c}_EvapApproach'), ('Cond approach K', f'{c}_CondApproach'), ('Lift K', f'{c}_Lift'), ('Capacity RT', f'{c}_RT'),
                 ('kW/RT', f'{c}_kW_per_RT'), ('Runtime h', f'{c}_RuntimeHours')]
        rows(p, x, 102, 235, items[:13], lw=140); rows(p, x + 235, 102, 235, items[13:], lw=140)
        al = [('Evap approach high', f'{c}EvapApproachAlarm'), ('Cond approach high', f'{c}CondApproachAlarm'), ('Evap low flow', f'{c}EvapLowFlowAlarm'),
              ('Program lockout', f'{c}TimeoutLockout'), ('Hard lockout', f'{c}HardLockoutAlarm'), ('Local (not remote)', f'{c}NotInAutoAlarm')]
        for i, (t, pt) in enumerate(al):
            status_led(p, x + 8 + (i % 2) * 232, 390 + (i // 2) * 22 + 3, pt, t, 'alarm'); lbl(p, x + 26 + (i % 2) * 232, 390 + (i // 2) * 22, 200, t, 9, TXT)
        p.fire(x + 8, 460, 120, 22, f'RESET {c}', f'{c}ResetFire', f'{c} reset')
        x += 480
    x0, y0 = 970, 80
    for k, eq in enumerate(('CHP', 'CDP')):
        for j, n in enumerate(('01', '02')):
            u = f'{eq}{n}'
            px_, py_ = x0 + j * 470, y0 + k * 290
            panel(p, px_, py_, 460, 280, f'{u}  (VFD / PT / CT)')
            items = [('Command', f'{u}StartCmd', {'bool_c': (RUN, OFF)}), ('Run proof', f'{u}RunProof', {'bool_c': (RUN, OFF)}), ('HOA auto', f'{u}InAuto', {'bool_c': (RUN, WARN)}),
                     ('VFD fault', f'{u}VfdFault', {'bool_c': (FLT, '#1f6f43')}), ('Speed cmd %', f'{u}SpeedCmd'), ('Output Hz', f'{u}_SpeedFeedbackHz'),
                     ('Power kW', f'{u}_kW'), ('Current A', f'{u}_Amps'), ('Energy kWh', f'{u}_kWh'), ('Suction kPa', f'{u}_SuctionPressure'),
                     ('Discharge kPa', f'{u}_DischargePressure'), ('Pump dP kPa', f'{u}_DiffPressure')]
            rows(p, px_, py_ + 22, 230, items[:6], lw=120); rows(p, px_ + 230, py_ + 22, 230, items[6:], lw=120)
            for i, (t, pt) in enumerate((('Failed (latched)', f'{u}FailLatch'), ('No dP', f'{u}NoDeltaPAlarm'), ('Low suction', f'{u}LowSuctionAlarm'))):
                status_led(p, px_ + 8 + i * 150, py_ + 160, pt, t, 'alarm'); lbl(p, px_ + 26 + i * 150, py_ + 157, 130, t, 9, TXT)
            lbl(p, px_ + 8, py_ + 184, 100, 'Runtime h'); val(p, px_ + 110, py_ + 185, 70, f'{u}_RuntimeHours', f'{u} runtime', h=18)
            lbl(p, px_ + 190, py_ + 184, 60, 'Lead'); val(p, px_ + 240, py_ + 185, 70, f'{eq}_Lead', f'{eq} lead', h=18)
            p.fire(px_ + 8, py_ + 212, 110, 22, f'RESET {u}', f'{u}ResetFire', f'{u} reset')
    for j, n in enumerate(('01', '02')):
        u = f'CT{n}'
        px_, py_ = 10 + j * 480, 650
        panel(p, px_, py_, 470, 250, f'COOLING TOWER {n}  (VFD / LT / LS / TT / vibration)')
        items = [('Command', f'{u}StartCmd', {'bool_c': (RUN, OFF)}), ('Run proof', f'{u}RunProof', {'bool_c': (RUN, OFF)}), ('Valve cmd', f'{u}ValveOpenCmd', {'bool_c': (RUN, OFF)}),
                 ('Valve open', f'{u}ValveOpenProof', {'bool_c': (RUN, OFF)}), ('HOA auto', f'{u}InAuto', {'bool_c': (RUN, WARN)}), ('Vibration', f'{u}VibrationAlarm', {'bool_c': (FLT, '#1f6f43')}),
                 ('Speed %', f'{u}SpeedCmd'), ('Output Hz', f'{u}_FanSpeedHz'), ('Power kW', f'{u}_kW'), ('Current A', f'{u}_Amps'),
                 ('Basin level %', f'{u}_BasinLevel'), ('Basin temp', f'{u}_BasinTemp'), ('Cell outlet temp', f'{u}_OutletTemp'), ('Energy kWh', f'{u}_kWh')]
        rows(p, px_, py_ + 22, 235, items[:7], lw=120); rows(p, px_ + 235, py_ + 22, 235, items[7:], lw=120)
        p.fire(px_ + 8, py_ + 222, 110, 22, f'RESET {u}', f'{u}ResetFire', f'{u} reset')
    panel(p, 970, 660, 460, 240, 'BTU METER & MAIN POWER METER')
    rows(p, 970, 682, 230, [('BTU flow m3/h', 'BTU_Flow'), ('BTU supply', 'BTU_SupplyTemp'), ('BTU return', 'BTU_ReturnTemp'), ('BTU dT', 'BTU_DeltaT'),
                            ('BTU power RT', 'BTU_Power_RT'), ('BTU energy RTh', 'BTU_EnergyTotal'), ('BTU valid', 'BTU_Valid', {'bool_c': (RUN, FLT)}),
                            ('BTU vs calc', 'BTU_DeviationAlarm', {'bool_c': (WARN, '#1f6f43')})], lw=120)
    rows(p, 1200, 682, 230, [('Main kW', 'PM_Main_kW'), ('Main kWh', 'PM_Main_kWh'), ('Voltage V', 'PM_Main_Volts'), ('Current A', 'PM_Main_Amps'),
                             ('Power factor', 'PM_Main_PF'), ('Frequency Hz', 'PM_Main_Hz'), ('Comm', 'PM_Main_CommOk', {'bool_c': (RUN, FLT)}),
                             ('Meter vs sum', 'PowerMeter_DeviationAlarm', {'bool_c': (WARN, '#1f6f43')})], lw=120)
    panel(p, 1440, 660, 470, 240, 'HEADERS & WATER')
    rows(p, 1440, 682, 235, [('CHW supply kPa', 'CHW_SupplyHeaderPressure'), ('CHW return kPa', 'CHW_ReturnHeaderPressure'), ('Exp. tank kPa', 'CHW_ExpansionTankPressure'),
                             ('Bypass flow', 'CHW_BypassFlow'), ('CDW flow', 'CDW_Flow'), ('CDW supply kPa', 'CDW_SupplyHeaderPressure')], lw=130)
    rows(p, 1675, 682, 235, [('Make-up m3/h', 'CT_MakeupFlow'), ('Make-up m3', 'CT_MakeupVolume'), ('Conductivity', 'CT_Conductivity'),
                             ('CT01 level low', 'CT01BasinLowLevelAlarm', {'bool_c': (FLT, '#1f6f43')}), ('CT02 level low', 'CT02BasinLowLevelAlarm', {'bool_c': (FLT, '#1f6f43')}),
                             ('CDW flow low', 'CDW_FlowLowAlarm', {'bool_c': (FLT, '#1f6f43')})], lw=130)
    return p


# ---------------------------------------------------------------- air side
def duct_run(p, x, y, length):
    """horizontal duct from kitPx Ductwork tiles (99 px tall)."""
    tiles = [(850, 'Ductwork/Duct_Horz_XLong.png'), (510, 'Ductwork/Duct_Horz_Long.png'), (340, 'Ductwork/Duct_Horz_Med.png'), (170, 'Ductwork/Duct_Horz_Short.png')]
    pos, end = x, x + length
    while pos < end:
        rem = end - pos
        ln, rel = next(((l, r) for l, r in tiles if l <= rem), tiles[-1])
        pic(p, pos if ln <= rem else end - ln, y, rel); pos += ln


def ahu_page(u):
    p = G.Page(f'ALT_V7_{u}', f'{u} air handling unit', (1920, 1080)); p.header()
    y = 330
    duct_run(p, 200, y, 1300)
    lbl(p, 150, y + 38, 50, 'RA ▶', 12, TXT, True)
    pic_pct(p, 330, y, f'{u}_OADamperCmd', 'Dampers/Damper_Horz_Parallel/Damper_Horz_Parallel', 5, f'{u} OA damper')
    lbl(p, 316, y - 22, 120, 'OA damper (CO2)', 9, TXT)
    pic(p, 520, y, 'Filters/Filter_Single_Dp/Filter_Single_DP_0.png')
    pic_pct(p, 740, y, f'{u}_ValveFeedback', 'Coils/Coils_Cooling_2Way_Bottom/Coils_Cooling_2Way_Bottom', 5, f'{u} CHW coil')
    pic_bool(p, 1000, y, f'{u}_Status', 'Fans/Fans_Horz/Fans_Horz_Right/Fans_Horz_Right_On.gif', 'Fans/Fans_Horz/Fans_Horz_Right/Fans_Horz_Right_Off.png', f'{u} supply fan')
    lbl(p, 1500, y + 38, 60, '▶ SA', 12, TXT, True)
    pic(p, 250, y - 120, 'Sensors/sensor_duct_temphum_bottom.png'); pic(p, 1300, y - 120, 'Sensors/sensor_duct_avgtemp_bottom.png')
    pic(p, 1400, y - 120, 'Sensors/sensor_duct_sp_bottom.png')
    panel(p, 180, 110, 230, 110, 'RETURN AIR')
    rows(p, 180, 132, 230, [('RAT', f'{u}_RAT'), ('RAT setpoint', f'{u}_RAT_SP', {'action': True}), ('RH', f'{u}_RA_RH'), ('CO2 ppm', f'{u}_RA_CO2')], lw=110)
    panel(p, 480, 470, 200, 90, 'FILTER')
    rows(p, 480, 492, 200, [('dP Pa', f'{u}_FilterDP'), ('Limit', f'{u}_FilterDPMax', {'action': True}), ('Dirty', f'{u}_FilterDirtyAlarm', {'bool_c': (WARN, '#1f6f43')})], lw=90)
    panel(p, 700, 470, 240, 140, 'CHW VALVE (PID on SAT)')
    rows(p, 700, 492, 240, [('Command %', f'{u}_ValveCmd'), ('Feedback %', f'{u}_ValveFeedback'), ('Mismatch', f'{u}_ValveMismatchAlarm', {'bool_c': (WARN, '#1f6f43')}),
                            ('CHW request', f'{u}_ChwRequest', {'bool_c': (WARN, OFF)}), ('Cooling call', f'{u}_CoolingCall', {'bool_c': (RUN, OFF)})], lw=120)
    panel(p, 960, 470, 260, 160, 'SUPPLY FAN (VSD)')
    rows(p, 960, 492, 260, [('Command', f'{u}_StartCmd', {'bool_c': (RUN, OFF)}), ('Status', f'{u}_Status', {'bool_c': (RUN, OFF)}), ('Speed %', f'{u}_SpeedCmd'),
                            ('Hz', f'{u}_SpeedFeedbackHz'), ('kW', f'{u}_kW'), ('Runtime h', f'{u}_RuntimeHours')], lw=120)
    panel(p, 1240, 110, 300, 110, 'SUPPLY AIR')
    rows(p, 1240, 132, 300, [('SAT', f'{u}_SAT'), ('SAT setpoint (reset)', f'{u}_SAT_SP'), ('Duct static Pa', f'{u}_DuctStatic'), ('Static SP', f'{u}_DuctStatic_SP', {'action': True})], lw=170)
    panel(p, 1240, 470, 300, 250, 'MODE / SAFETY')
    rows(p, 1240, 492, 300, [('Mode', f'{u}_ModeAuto', {'action': True}), ('Manual ON', f'{u}_ManualOn', {'action': True}), ('HOA auto', f'{u}_InAuto', {'bool_c': (RUN, WARN)}),
                             ('Overload', f'{u}_Overload', {'bool_c': (FLT, '#1f6f43')}), ('VFD fault', f'{u}_VfdFault', {'bool_c': (FLT, '#1f6f43')}),
                             ('Smoke (latched)', f'{u}_SmokeShutdown', {'bool_c': (FLT, '#1f6f43')}), ('Fire alarm', 'FireAlarmSignal', {'bool_c': (FLT, '#1f6f43')}),
                             ('Fan fail', f'{u}_FanFailAlarm', {'bool_c': (FLT, '#1f6f43')}), ('SAT not tracking', f'{u}_SATNotTrackingAlarm', {'bool_c': (WARN, '#1f6f43')}),
                             ('Space hot', f'{u}_SpaceTempHighAlarm', {'bool_c': (WARN, '#1f6f43')})], lw=150)
    p.fire(1240, 730, 140, 24, 'RESET SMOKE', f'{u}SmokeResetFire', f'{u} smoke shutdown reset')
    panel(p, 180, 650, 500, 170, 'SETPOINTS (standard template)')
    rows(p, 180, 672, 250, [('SAT min', f'{u}_SAT_Min', {'action': True}), ('SAT max', f'{u}_SAT_Max', {'action': True}), ('SAT default', f'{u}_SAT_Default', {'action': True})], lw=130)
    rows(p, 430, 672, 250, [('CO2 low', f'{u}_CO2_Low', {'action': True}), ('CO2 high', f'{u}_CO2_High', {'action': True}), ('OA damper min', f'{u}_OAD_Min', {'action': True}),
                            ('OA damper cmd', f'{u}_OADamperCmd')], lw=130)
    lbl(p, 180, 840, 1300, 'Sequence: schedule/manual → fire, smoke, HOA, overload, VFD checks → fan start (min-off) → proof 30 s → '
        'SAT setpoint reset from RAT (SP−1 K → SAT max, SP+1 K → SAT min) → valve PID on SAT → static PID → CO2 DCV. Sensor invalid → fail-safe output + alarm.', 9, LBL, h=40)
    return p


def oau_page(u):
    p = G.Page(f'ALT_V7_{u}', f'{u} outdoor air unit', (1920, 1080)); p.header()
    y = 330
    duct_run(p, 200, y, 1300)
    lbl(p, 150, y + 38, 50, 'OA ▶', 12, TXT, True)
    pic(p, 330, y, 'Dampers/Damper_Horz_Parallel/Damper_Horz_Parallel_4.png')
    pic(p, 520, y, 'Filters/Filter_Single_Dp/Filter_Single_DP_0.png')
    pic_pct(p, 740, y, f'{u}_ValveFeedback', 'Coils/Coils_Cooling_2Way_Bottom/Coils_Cooling_2Way_Bottom', 5, f'{u} CHW coil')
    pic_bool(p, 1000, y, f'{u}_Status', 'Fans/Fans_Horz/Fans_Horz_Right/Fans_Horz_Right_On.gif', 'Fans/Fans_Horz/Fans_Horz_Right/Fans_Horz_Right_Off.png', f'{u} fan')
    lbl(p, 1500, y + 38, 60, '▶ SA', 12, TXT, True)
    pic(p, 1300, y - 120, 'Sensors/sensor_duct_temphum_bottom.png')
    panel(p, 180, 110, 260, 110, 'OUTDOOR AIR')
    rows(p, 180, 132, 260, [('OA dry bulb', 'OA_Temperature'), ('OA RH', 'OA_Humidity'), ('OA wet bulb', 'OA_WetBulb'), ('OA dew point', 'OA_DewPoint')], lw=130)
    panel(p, 1240, 110, 320, 130, 'LEAVING AIR (dehumidified)')
    rows(p, 1240, 132, 320, [('LAT', f'{u}_LAT'), ('LAT setpoint', f'{u}_LAT_SP', {'action': True}), ('LAT RH', f'{u}_LAT_RH'), ('LAT dew point', f'{u}_LAT_DewPoint'),
                             ('Airflow m3/h', f'{u}_Airflow')], lw=170)
    panel(p, 480, 470, 200, 90, 'FILTER')
    rows(p, 480, 492, 200, [('dP Pa', f'{u}_FilterDP'), ('Limit', f'{u}_FilterDPMax', {'action': True}), ('Dirty', f'{u}_FilterDirtyAlarm', {'bool_c': (WARN, '#1f6f43')})], lw=90)
    panel(p, 700, 470, 240, 140, 'CHW VALVE (PID on LAT)')
    rows(p, 700, 492, 240, [('Command %', f'{u}_ValveCmd'), ('Feedback %', f'{u}_ValveFeedback'), ('Mismatch', f'{u}_ValveMismatchAlarm', {'bool_c': (WARN, '#1f6f43')}),
                            ('CHW request', f'{u}_ChwRequest', {'bool_c': (WARN, OFF)}), ('Cooling call', f'{u}_CoolingCall', {'bool_c': (RUN, OFF)})], lw=120)
    panel(p, 960, 470, 260, 180, 'FAN (constant airflow)')
    rows(p, 960, 492, 260, [('Command', f'{u}_StartCmd', {'bool_c': (RUN, OFF)}), ('Status', f'{u}_Status', {'bool_c': (RUN, OFF)}), ('Speed %', f'{u}_SpeedCmd'),
                            ('Hz', f'{u}_SpeedFeedbackHz'), ('kW', f'{u}_kW'), ('Airflow SP', f'{u}_Airflow_SP', {'action': True}), ('Runtime h', f'{u}_RuntimeHours')], lw=120)
    panel(p, 1240, 470, 300, 210, 'MODE / SAFETY')
    rows(p, 1240, 492, 300, [('Mode', f'{u}_ModeAuto', {'action': True}), ('Manual ON', f'{u}_ManualOn', {'action': True}), ('HOA auto', f'{u}_InAuto', {'bool_c': (RUN, WARN)}),
                             ('Overload', f'{u}_Overload', {'bool_c': (FLT, '#1f6f43')}), ('VFD fault', f'{u}_VfdFault', {'bool_c': (FLT, '#1f6f43')}),
                             ('Fire alarm', 'FireAlarmSignal', {'bool_c': (FLT, '#1f6f43')}), ('Fan fail', f'{u}_FanFailAlarm', {'bool_c': (FLT, '#1f6f43')}),
                             ('LAT high', f'{u}_LATHighAlarm', {'bool_c': (WARN, '#1f6f43')})], lw=150)
    lbl(p, 180, 720, 1300, 'Sequence (SOO OAU): schedule → fire/HOA/overload → fan at minimum → VSD holds design airflow → CHW valve holds leaving air 16.5 °C '
        '(10.5 °C office dehumidification) after fan proof. LAT invalid → valve 70 %; airflow invalid → fan 80 %.', 9, LBL, h=40)
    return p


def fcu_page():
    p = G.Page('ALT_V7_FCU', 'Fan coil units', (1920, 1080)); p.header()
    for i, u in enumerate(('FCU01', 'FCU02', 'FCU03', 'FCU04')):
        x, y = 20 + (i % 2) * 950, 90 + (i // 2) * 480
        panel(p, x, y, 930, 460, u)
        pic(p, x + 20, y + 40, 'Misc/Misc_FCU/misc_fcu.png')
        pic_bool(p, x + 20 + 380, y + 40, f'{u}_Status', 'Misc/Misc_FCU/Fan/misc_fcu_fan_on.gif', 'Misc/Misc_FCU/Fan/misc_fcu_fan_off.png', f'{u} fan')
        pic_bool(p, x + 20 + 120, y + 40, f'{u}_ValveCmd', 'Misc/Misc_FCU/Cooling_Coil/misc_fcu_CoolingCoil_on.png', 'Misc/Misc_FCU/Cooling_Coil/misc_fcu_CoolingCoil_off.png', f'{u} coil')
        pic(p, x + 660, y + 40, 'Sensors/Sensors_Tstat/tstat04.png')
        val(p, x + 740, y + 60, 90, f'{u}_RoomTemp', f'{u} room temp', h=28, size=14)
        lbl(p, x + 740, y + 92, 90, 'setpoint', 8, LBL, halign='center'); val(p, x + 740, y + 110, 90, f'{u}_RoomTemp_SP', f'{u} setpoint', h=22, action=True)
        rows(p, x + 10, y + 160, 300, [('Command', f'{u}_StartCmd', {'bool_c': (RUN, OFF)}), ('Status', f'{u}_Status', {'bool_c': (RUN, OFF)}),
                                       ('Fan LOW', f'{u}_FanLowCmd', {'bool_c': (RUN, OFF)}), ('Fan MED', f'{u}_FanMedCmd', {'bool_c': (RUN, OFF)}),
                                       ('Fan HIGH', f'{u}_FanHighCmd', {'bool_c': (RUN, OFF)}), ('Speed stage', f'{u}_FanSpeedStage'),
                                       ('Valve', f'{u}_ValveCmd', {'bool_c': (RUN, OFF)}), ('Error K', f'{u}_RoomTempError')], lw=150)
        rows(p, x + 330, y + 160, 300, [('Mode', f'{u}_ModeAuto', {'action': True}), ('Manual ON', f'{u}_ManualOn', {'action': True}),
                                        ('Overload', f'{u}_Overload', {'bool_c': (FLT, '#1f6f43')}), ('Fan fail', f'{u}_FanFailAlarm', {'bool_c': (FLT, '#1f6f43')}),
                                        ('Sensor invalid', f'{u}_RoomTemp_SensorAlarm', {'bool_c': (WARN, '#1f6f43')}), ('Room hot', f'{u}_RoomTempHighAlarm', {'bool_c': (WARN, '#1f6f43')}),
                                        ('kW', f'{u}_kW'), ('Runtime h', f'{u}_RuntimeHours')], lw=150)
        lbl(p, x + 650, y + 160, 270, 'SOO FCU-2 bands:', 9, TXT, True)
        for k, t in enumerate(('≤ SP+0.75 K → LOW', '> SP+0.75 K → MEDIUM', '> SP+1.5 K → HIGH', 'valve: open > SP+0.5, close < SP−0.5',
                               'sensor invalid → MED + valve open', 'fire alarm → stop (policy switch)')):
            lbl(p, x + 650, y + 182 + k * 20, 270, t, 9)
    return p


def vent_page():
    p = G.Page('ALT_V7_Ventilation', 'Exhaust, car-park & life-safety fans', (1920, 1080)); p.header()
    cards = [('EF01', 'Exhaust fan — constant speed (FAN-1)', 'Misc/Misc_roofexh/misc_roofexh', []),
             ('EF02', 'Exhaust fan — VSD duct pressure (FAN-3)', 'Fans/Fans_Axial/Fans_Axial_Horz/Fans_Axial_Horz',
              [('Duct Pa', 'EF02_DuctPressure'), ('SP Pa', 'EF02_DuctPressure_SP', {'action': True}), ('Speed %', 'EF02_SpeedCmd'), ('Pressure alarm', 'EF02_PressureAlarm', {'bool_c': (WARN, '#1f6f43')})]),
             ('EF03', 'Ventilation — VSD space temp (FAN-4)', 'Fans/Fans_Axial/Fans_Axial_Horz/Fans_Axial_Horz',
              [('Space °C', 'EF03_SpaceTemp'), ('SP °C', 'EF03_SpaceTemp_SP', {'action': True}), ('Speed %', 'EF03_SpeedCmd'), ('Room hot', 'EF03_SpaceTempHighAlarm', {'bool_c': (FLT, '#1f6f43')})]),
             ('CPEF01', 'Car-park exhaust — CO control + smoke mode', 'Fans/Fans_Axial/Fans_Axial_Horz/Fans_Axial_Horz',
              [('CO ppm', 'CPEF01_CO'), ('Start ppm', 'CPEF01_CO_Start', {'action': True}), ('Speed %', 'CPEF01_SpeedCmd'), ('High CO', 'CPEF01_COHighAlarm', {'bool_c': (FLT, '#1f6f43')})]),
             ('LSF01', 'Stair pressurisation — fire start (LSF-1)', 'Fans/Fans_Axial/Fans_Axial_Horz/Fans_Axial_Horz',
              [('Stair dP Pa', 'LSF01_StairDP'), ('SP Pa', 'LSF01_StairDP_SP', {'action': True}), ('Speed %', 'LSF01_SpeedCmd'), ('Fail in fire', 'LSF01_FireFailAlarm', {'bool_c': (FLT, '#1f6f43')})]),
             ('SEF01', 'Smoke exhaust — fire start', 'Misc/Misc_roofexh/misc_roofexh',
              [('Fail in fire', 'SEF01_FireFailAlarm', {'bool_c': (FLT, '#1f6f43')}), ('Test run', 'SEF01_TestRun', {'action': True})])]
    for i, (u, title, img, extra) in enumerate(cards):
        x, y = 20 + (i % 3) * 630, 90 + (i // 3) * 480
        panel(p, x, y, 610, 460, f'{u} — {title}')
        on = f'{img}_On.gif'; off = f'{img}_Off.png'
        pic_bool(p, x + 20, y + 40, f'{u}_Status', on, off, f'{u} fan')
        base = [('Command', f'{u}_StartCmd', {'bool_c': (RUN, OFF)}), ('Status', f'{u}_Status', {'bool_c': (RUN, OFF)}), ('Mode', f'{u}_ModeAuto', {'action': True}),
                ('Manual ON', f'{u}_ManualOn', {'action': True}), ('HOA auto', f'{u}_InAuto', {'bool_c': (RUN, WARN)}), ('Overload', f'{u}_Overload', {'bool_c': (FLT, '#1f6f43')}),
                ('Fan fail', f'{u}_FanFailAlarm', {'bool_c': (FLT, '#1f6f43')}), ('In hand', f'{u}_FanInHandAlarm', {'bool_c': (WARN, '#1f6f43')}),
                ('kW', f'{u}_kW'), ('Runtime h', f'{u}_RuntimeHours'), ('Service due', f'{u}_RuntimeExceededAlarm', {'bool_c': (WARN, '#1f6f43')})]
        rows(p, x + 10, y + 200, 290, base, lw=140)
        rows(p, x + 310, y + 200, 290, extra, lw=140)
    lbl(p, 20, 1050, 1200, 'Fire alarm: normal HVAC fans stop; LSF01 / SEF01 / CPEF01 start (CPEF01 100 %). Fan fail / in hand / overload / runtime-exceeded alarms per SOO FAN-1/3.', 9, LBL)
    return p


def airside_page():
    p = G.Page('ALT_V7_AirSide', 'Air side overview (standard library)', (1920, 1080)); p.header()
    panel(p, 20, 90, 1880, 70, 'FIRE ALARM INTERFACE / PLANT INTERFACE')
    val(p, 30, 118, 240, 'FireModeActive', 'Fire mode', h=32, size=14, bool_c=(FLT, '#1f6f43'))
    rows(p, 290, 114, 380, [('Cooling calls', 'AirSide_CoolingCalls'), ('CHW requests (T&R)', 'AirSide_ChwRequests')], lw=200)
    rows(p, 690, 114, 380, [('Units running', 'AirSide_UnitsRunning'), ('Plant reset request %', 'PlantResetPct')], lw=200)
    rows(p, 1090, 114, 380, [('Plant demand mode', 'PlantDemandMode', {'action': True}), ('Plant run', 'PlantRunRequest', {'bool_c': (RUN, OFF)})], lw=200)
    rows(p, 1490, 114, 400, [('Reset source AHU T&R', 'ResetSource_AirSide', {'action': True}), ('FCU stop on fire', 'AirSide_FireStopsFCU', {'action': True})], lw=220)
    hdr = ['Unit', 'Command', 'Status', 'Main value', 'Setpoint', 'Output %', 'kW', 'Fan fail', 'Runtime h']
    xs = [20, 170, 330, 490, 690, 890, 1050, 1210, 1370]
    for x, h in zip(xs, hdr): lbl(p, x, 180, 150, h, 10, TXT, True)
    units = [('AHU01', 'AHU01_SAT', 'AHU01_SAT_SP', 'AHU01_ValveCmd', 'ALT_V7_AHU01'), ('AHU02', 'AHU02_SAT', 'AHU02_SAT_SP', 'AHU02_ValveCmd', 'ALT_V7_AHU02'),
             ('OAU01', 'OAU01_LAT', 'OAU01_LAT_SP', 'OAU01_ValveCmd', 'ALT_V7_OAU01'), ('FCU01', 'FCU01_RoomTemp', 'FCU01_RoomTemp_SP', None, 'ALT_V7_FCU'),
             ('FCU02', 'FCU02_RoomTemp', 'FCU02_RoomTemp_SP', None, 'ALT_V7_FCU'), ('FCU03', 'FCU03_RoomTemp', 'FCU03_RoomTemp_SP', None, 'ALT_V7_FCU'),
             ('FCU04', 'FCU04_RoomTemp', 'FCU04_RoomTemp_SP', None, 'ALT_V7_FCU'), ('EF01', None, None, None, 'ALT_V7_Ventilation'),
             ('EF02', 'EF02_DuctPressure', 'EF02_DuctPressure_SP', 'EF02_SpeedCmd', 'ALT_V7_Ventilation'), ('EF03', 'EF03_SpaceTemp', 'EF03_SpaceTemp_SP', 'EF03_SpeedCmd', 'ALT_V7_Ventilation'),
             ('CPEF01', 'CPEF01_CO', 'CPEF01_CO_Start', 'CPEF01_SpeedCmd', 'ALT_V7_Ventilation'), ('LSF01', 'LSF01_StairDP', 'LSF01_StairDP_SP', 'LSF01_SpeedCmd', 'ALT_V7_Ventilation'),
             ('SEF01', None, None, None, 'ALT_V7_Ventilation')]
    for r, (u, mv, sp, out, page) in enumerate(units):
        y = 206 + r * 34
        p.label(xs[0], y, 140, 28, '  ' + u + '  ⊞', 11, True, 'white', '#2c3e50', 'left', popup=f'file:^px/{page}.px', ptitle=u)
        val(p, xs[1], y + 2, 140, f'{u}_StartCmd', f'{u} command', h=24, bool_c=(RUN, OFF))
        val(p, xs[2], y + 2, 140, f'{u}_Status', f'{u} status', h=24, bool_c=(RUN, OFF))
        if mv: val(p, xs[3], y + 2, 180, mv, f'{u} main value', h=24)
        if sp: val(p, xs[4], y + 2, 180, sp, f'{u} setpoint', h=24, action=not sp.endswith('SAT_SP'))
        if out: val(p, xs[5], y + 2, 140, out, f'{u} output', h=24)
        val(p, xs[6], y + 2, 140, f'{u}_kW', f'{u} kW', h=24)
        val(p, xs[7], y + 2, 140, f'{u}_FanFailAlarm', f'{u} fan fail', h=24, bool_c=(FLT, '#1f6f43'))
        val(p, xs[8], y + 2, 140, f'{u}_RuntimeHours', f'{u} runtime', h=24)
    lbl(p, 20, 660, 1880, 'Standard library: each unit folder (/AirSide/<Unit>/Points | Logic | Monitor) is generated from one template — copy the template call in make_v7.py '
        'AIR_UNITS to add units for another site. Schedules: /AirSide/Schedules (Sch_AHU, Sch_FCU, Sch_EF, Sch_CarPark).', 9, LBL, h=40)
    return p


def load_paths(bog):
    root = ET.fromstring(zipfile.ZipFile(bog).read('file.xml'))
    out = {}
    def walk(el, pre):
        for c in el:
            if c.tag != 'p' or not c.get('t'): continue
            if c.get('t') == 'b:Folder': walk(c, pre + '/' + c.get('n')); continue
            if c.get('t') in ('b:PxView', 'b:WsAnnotation'): continue
            out[c.get('n')] = pre + '/' + c.get('n')
    for e in root.iter('p'):
        if e.get('n') in ('ChillerPlant', 'AirSide') and e.get('t') in ('b:Component', 'b:Folder'):
            walk(e, '/' + e.get('n'))
    return out


if __name__ == '__main__':
    bog, KITDIR, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    PATH.update(load_paths(bog))
    G.FOLDER = {n: p.rsplit('/', 1)[0].replace('/ChillerPlant/', '').replace('/ChillerPlant', '') for n, p in PATH.items()}
    G.STATION_NAME = 'ALT_CP_Ref_V7'
    G.PAGES = PAGES
    regdir = os.path.join(os.path.dirname(os.path.abspath(bog)), 'reg')
    H, A, T = (G.read_reg(os.path.join(regdir, f)) for f in ('V7_HISTORY_REGISTER.csv', 'V7_ALARM_REGISTER.csv', 'V7_TAG_REGISTER.csv'))
    os.makedirs(os.path.join(outdir, 'px'), exist_ok=True)
    rows_, bad = [], []
    pages = [plant_page(), plant_detail(), G.optimization(), G.energy_dashboard(), G.energy(), G.alarms_history(), G.simulation(),
             airside_page(), ahu_page('AHU01'), ahu_page('AHU02'), oau_page('OAU01'), fcu_page(), vent_page()]
    for p in pages:
        x = p.xml()
        ET.fromstring(x.encode('utf-8'))
        with open(os.path.join(outdir, 'px', p.name + '.px'), 'w', encoding='utf-8') as f: f.write(x)
        for pt, o, what, mode in p.map:
            if pt != '(BQL)' and pt not in PATH: bad.append((p.name, pt))
            rows_.append({'Graphic': p.name + '.px', 'Element': what, 'Point': pt, 'ORD': o, 'Binding': mode,
                          'History_ID': '; '.join(r['History_ID'] for r in H.get(pt, [])),
                          'Alarm': '; '.join(f"{r['Alarm_Type']}/{r['Alarm_Class']}" for r in A.get(pt, []))})
        imgs = re.findall(r'module://kitPxGraphics/([^";]+)', x)
        missing = [i for i in set(imgs) if not os.path.exists(os.path.join(KITDIR, i))]
        bad += [(p.name, 'image ' + i) for i in missing]
        files = re.findall(r'file:\^px/([^"]+)\.px', x)
        bad += [(p.name, 'page ' + f) for f in files if f not in {n for n, _ in PAGES}]
        print(p.name, len(p.el), 'elements', len(p.map), 'bindings', len(set(imgs)), 'images')
    assert not bad, bad[:20]
    with open(os.path.join(outdir, 'V7_GRAPHIC_POINT_MAPPING.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows_[0].keys())); w.writeheader(); w.writerows(rows_)
    print('bindings', len(rows_), 'distinct points', len({r['Point'] for r in rows_ if r['Point'] != '(BQL)'}))
