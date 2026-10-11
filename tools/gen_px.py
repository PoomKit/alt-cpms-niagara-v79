"""Generate V6 Px graphics + point-mapping register.

Only widget/binding/converter vocabulary seen in the working ST5130 station px files is
used (Label, BoundLabel, BoundLabelBinding, ValueBinding, ActionBinding, PopupBinding,
ObjectToString, IBooleanToSimple, INumericToSimple, INumericToNumber, Bargraph, Rect,
Line, Polygon, Button, BoundTable, TableBinding). No image files are referenced.
usage: gen_px.py v6.bog outdir   -> outdir/px/*.px + outdir/V6_GRAPHIC_POINT_MAPPING.csv
"""
import sys, os, csv, zipfile, re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr

BASE = '/ChillerPlant'
C_RUN, C_OFF, C_FLT, C_WARN = '#3cb371', '#cfd8dc', '#e53935', '#ffb300'
CHWS_C, CHWR_C, CDS_C, CDR_C = '#1565c0', '#90caf9', '#2e7d32', '#a5d6a7'
PAGES = [('ALT_CP_Overview', 'Plant Overview'), ('ALT_CP_Optimization', 'Optimisation & Mode'),
         ('ALT_CP_EnergyDashboard', 'Energy Dashboard'), ('ALT_CP_Energy', 'Energy & KPI'), ('ALT_CP_AlarmsHistory', 'Alarms & History'),
         ('ALT_CP_Simulation', 'Simulation')]
STATION_NAME = 'ALT_CP_Ref_V6_3'


class Page:
    def __init__(self, name, title, size=(1600, 900)):
        self.name, self.title, self.size, self.el, self.map = name, title, size, [], []

    # ---------------------------------------------------------------- primitives
    def rect(self, x, y, w, h, fill=None, stroke='#607d8b', pen=2.0, popup=None, ptitle=None):
        a = (f' fill="{fill}"' if fill else '') + f' stroke="{stroke}" pen="{pen}" geom="{x:.1f},{y:.1f},{w:.1f},{h:.1f}"'
        if popup:
            self.el.append(f'<Rect{a}>\n  <PopupBinding ord={quoteattr(popup)} title={quoteattr(ptitle or "")}/>\n</Rect>')
        else:
            self.el.append(f'<Rect{a}/>')

    def line(self, pts, color, pen=6.0):
        self.el.append(f'<Line stroke="{color}" pen="{pen}" geom="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + '"/>')

    def poly(self, pts, fill):
        self.el.append(f'<Polygon fill="{fill}" geom="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ' "/>')

    def label(self, x, y, w, h, text, size=12, bold=False, fg='black', bg=None, halign='left', popup=None, ptitle=None):
        per = int(w / (size * 0.62))
        if len(text) > per and h >= size * 3 and not popup:          # Px Label does not wrap: split into lines
            import textwrap
            lh = size * 1.7
            for i, ln in enumerate(textwrap.wrap(text, per)):
                self.label(x, y + i * lh, w, lh, ln, size, bold, fg, bg, halign)
            return
        a = f'layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" text={quoteattr(text)} font="{"bold " if bold else ""}{size:.1f}pt sans-serif" foreground="{fg}"'
        a += (f' background="{bg}"' if bg else '') + f' halign="{halign}"'
        if popup:
            self.el.append(f'<Label {a}>\n  <PopupBinding ord={quoteattr(popup)} title={quoteattr(ptitle or text)}/>\n</Label>')
        else:
            self.el.append(f'<Label {a}/>')

    def ord(self, point):
        return f'station:|slot:{BASE}/{FOLDER[point]}/{point}'

    def value(self, x, y, w, h, point, what, fmt='%out.value%', size=12, bold=False, bool_bg=None, num_bg=None, popup=True, action=False, fg='black'):
        """BoundLabel bound to a point. bool_bg=(true,false) colours; num_bg='gx:Brush a:b=c;...'."""
        o = self.ord(point)
        conv = f'  <ObjectToString name="text" format={quoteattr(fmt)}/>\n'
        if bool_bg:
            conv += f'  <IBooleanToSimple name="background">\n    <Brush name="trueValue" value="{bool_bg[0]}"/>\n    <Brush name="falseValue" value="{bool_bg[1]}"/>\n  </IBooleanToSimple>\n'
        if num_bg:
            conv += f'  <INumericToSimple name="background" map="{num_bg}"/>\n'
        inner = ''
        if action:
            inner += f'  <ActionBinding ord={quoteattr(o + "/set")} widgetEvent="actionPerformed"/>\n'
        inner += f'  <BoundLabelBinding ord={quoteattr(o)} popupEnabled="{"true" if popup else "false"}" statusEffect="none">\n' + \
                 ''.join('  ' + l + '\n' for l in conv.rstrip('\n').split('\n')) + '  </BoundLabelBinding>\n'
        mo = ' mouseOver="outline"' if action else ''
        self.el.append(f'<BoundLabel layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" font="{"bold " if bold else ""}{size:.1f}pt sans-serif" '
                       f'foreground="{fg}" halign="center" border="1.0 solid #90a4ae"{mo}>\n{inner}</BoundLabel>')
        self.map.append((point, o, what, 'write (set)' if action else 'display'))

    def button(self, x, y, w, h, text, point, arg, what):
        o = self.ord(point)
        on, off = ('#00a000', 'white') if arg else ('#546e7a', 'white')
        t, f = (on, off) if arg else (off, on)
        self.el.append(
            f'<Button layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" text={quoteattr(text)} font="bold 11.0pt sans-serif">\n'
            f'  <ActionBinding ord={quoteattr(o + "/set")} widgetEvent="actionPerformed">\n    <Boolean name="actionArg" value="{"true" if arg else "false"}"/>\n  </ActionBinding>\n'
            f'  <ValueBinding ord={quoteattr(o)} popupEnabled="false">\n    <IBooleanToSimple name="background">\n      <Brush name="trueValue" value="{t}"/>\n'
            f'      <Brush name="falseValue" value="{f}"/>\n    </IBooleanToSimple>\n  </ValueBinding>\n</Button>')
        self.map.append((point, o, what, f'write set({str(arg).lower()})'))

    def fire(self, x, y, w, h, text, block, what, bg='#c62828'):
        """Momentary button: invokes the kitControl OneShot 'fire' action (no writable left latched)."""
        o = self.ord(block)
        self.el.append(f'<Button layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" text={quoteattr(text)} font="bold 10.0pt sans-serif" '
                       f'foreground="white" background="{bg}">\n  <ActionBinding ord={quoteattr(o + "/fire")} widgetEvent="actionPerformed"/>\n</Button>')
        self.map.append((block, o, what, 'action fire'))

    def bar(self, x, y, w, h, point, mx, what, fill='#42a5f5'):
        o = self.ord(point)
        self.el.append(
            f'<Bargraph layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" max="{mx:.1f}" valueFont="11.0pt SansSerif" scaleFont="10.0pt SansSerif" scaleVisible="false">\n'
            f'  <ValueBinding ord={quoteattr(o)}>\n    <INumericToNumber name="value"/>\n    <ObjectToString name="text" format="%out.value%"/>\n'
            f'    <INumericToSimple name="fill" map="gx:Brush 0.0:{mx * 10:.1f}={fill};default=#cfd8dc;"/>\n  </ValueBinding>\n</Bargraph>')
        self.map.append((point, o, what, 'display (bargraph)'))

    def table(self, x, y, w, h, bql, what):
        o = f'station:|slot:{BASE}|bql:{bql}'
        self.el.append(f'<BoundTable layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}">\n  <TableBinding ord={quoteattr(o)}/>\n</BoundTable>')
        self.map.append(('(BQL)', o, what, 'table'))

    # ---------------------------------------------------------------- composites
    def panel(self, x, y, w, h, title):
        self.rect(x, y, w, h, fill='white', stroke='#78909c', pen=2.0)
        self.label(x, y, w, 24, '  ' + title, 12, True, 'white', '#455a64')

    def row(self, x, y, text, point, what, w1=150, w2=110, **kw):
        self.label(x, y, w1, 22, text, 11)
        self.value(x + w1, y, w2, 22, point, what, **kw)

    def header(self):
        W = self.size[0]
        self.rect(0, 0, W, self.size[1], fill='#eceff1', stroke='#eceff1', pen=1.0)
        self.label(0, 0, W, 40, f'  ALT Chiller Plant V6 — {self.title}', 18, True, 'white', '#263238')
        self.label(W - 520, 8, 510, 24, 'REFERENCE SIMULATION – NOT PROJECT APPROVED', 11, True, '#263238', '#ffca28', 'center')
        x = 10
        for name, title in PAGES:
            cur = name == self.name
            self.label(x, 46, 164, 26, title, 10, True, 'white' if cur else '#263238', '#1e88e5' if cur else '#cfd8dc', 'center',
                       popup=None if cur else f'file:^px/{name}.px', ptitle=title)
            x += 170

    def xml(self):
        W, H = self.size
        body = '\n\n'.join('    ' + e.replace('\n', '\n    ') for e in self.el)
        return ('<?xml version="1.0" encoding="UTF-8"?>\n<!-- Niagara Presentation XML -->\n<px version="1.0" media="uxBuilder:UxMedia">\n<import>\n'
                '  <module name="baja"/>\n  <module name="bajaui"/>\n  <module name="converters"/>\n  <module name="gx"/>\n  <module name="kitPx"/>\n</import>\n'
                f'<content>\n<ScrollPane>\n\n  <CanvasPane name="content" viewSize="{W:.1f},{H:.1f}" scale="fitRatio" minScaleFactor="0.5" maxScaleFactor="1.0">\n\n'
                f'{body}\n\n  </CanvasPane>\n\n</ScrollPane>\n</content>\n</px>\n')


def status_box(p, x, y, w, h, eq, title, run_pt, cmd_pt, flt_pt, extra):
    """Equipment symbol: background = run proof, title, command/fault flags and values; click opens equipment folder."""
    p.rect(x, y, w, h, fill='#fafafa', stroke='#37474f', pen=2.0, popup=f'station:|slot:{BASE}/{eq}', ptitle=eq)
    p.value(x + 4, y + 4, w - 8, 24, run_pt, f'{title} run status', fmt=title, size=12, bold=True, bool_bg=(C_RUN, C_OFF), popup=True)
    yy = y + 32
    p.label(x + 6, yy, 40, 20, 'Cmd', 10); p.value(x + 44, yy, w / 2 - 44, 20, cmd_pt, f'{title} start command', size=10, bool_bg=(C_RUN, C_OFF))
    p.value(x + w / 2 + 4, yy, w / 2 - 10, 20, flt_pt, f'{title} fault', size=10, bool_bg=(C_FLT, '#ffffff'))
    yy += 24
    for label, pt, what in extra:
        p.label(x + 6, yy, 56, 20, label, 10); p.value(x + 62, yy, w - 68, 20, pt, what, size=10); yy += 23


def overview():
    p = Page('ALT_CP_Overview', 'Plant Overview'); p.header()
    # ---- left: plant / mode
    p.panel(10, 80, 300, 318, 'PLANT CONTROL')
    y = 110
    p.label(18, y, 120, 26, 'Plant enable', 11); p.button(140, y, 78, 26, 'ON', 'PlantEnable', True, 'Plant enable ON'); p.button(222, y, 78, 26, 'OFF', 'PlantEnable', False, 'Plant enable OFF'); y += 32
    p.row(18, y, 'Plant run request', 'PlantRunRequest', 'Plant run request', bool_bg=(C_RUN, C_OFF)); y += 26
    p.row(18, y, 'Plant stage', 'PlantStage', 'Plant stage (0/1/2)'); y += 26
    p.label(18, y, 120, 26, 'Boot qualified', 11); p.button(140, y, 78, 26, 'QUALIFY', 'BootQualified', True, 'Restart qualification = true'); p.button(222, y, 78, 26, 'HOLD', 'BootQualified', False, 'Restart qualification = false'); y += 26
    p.label(18, y, 120, 26, 'Mode request', 11); p.button(140, y, 78, 26, 'LOCAL', 'ModeCmd_UI', False, 'User mode = Local'); p.button(222, y, 78, 26, 'AI', 'ModeCmd_UI', True, 'User mode = AI'); y += 32
    p.row(18, y, 'Operation mode', 'OperationMode', 'Operation mode (AI/Local)', bool_bg=('#7e57c2', '#90a4ae'), fg='black'); y += 26
    p.row(18, y, 'AI heartbeat', 'HeartbeatDetectorStatus', 'AI heartbeat status', bool_bg=(C_RUN, C_FLT)); y += 26
    p.row(18, y, 'AI available', 'AI_Available', 'AI available', bool_bg=(C_RUN, C_WARN)); y += 26
    p.label(18, y, 120, 26, 'Optimisation', 11); p.button(140, y, 78, 26, 'ENABLE', 'OptimizationEnable', True, 'Optimisation enable'); p.button(222, y, 78, 26, 'DISABLE', 'OptimizationEnable', False, 'Optimisation disable')
    # ---- outdoor air
    p.panel(10, 406, 300, 196, 'OUTDOOR AIR')
    y = 436
    for t, pt in (('Dry bulb', 'OA_Temperature'), ('Relative humidity', 'OA_Humidity'), ('Wet bulb', 'OA_WetBulb'), ('Dew point', 'OA_DewPoint'), ('Enthalpy', 'OA_Enthalpy')):
        p.row(18, y, t, pt, f'OA {t.lower()}'); y += 26
    p.row(18, y, 'Sensor valid', 'OA_Valid', 'OA sensor valid', bool_bg=(C_RUN, C_FLT))
    # ---- KPI
    p.panel(10, 610, 300, 280, 'PLANT PERFORMANCE')
    y = 640
    p.row(18, y, 'Plant power', 'Plant_kW', 'Plant power kW', size=12, bold=True); y += 28
    p.row(18, y, 'Cooling load', 'CoolingLoad_RT', 'Cooling load RT', size=12, bold=True); y += 28
    p.row(18, y, 'Plant kW/RT', 'Plant_kW_per_RT', 'Plant efficiency kW/RT', size=14, bold=True,
          num_bg='gx:Brush 0.0:0.65=#66bb6a;0.65:0.85=#d4e157;0.85:1.0=#ffca28;1.0:100.0=#ef5350;default=#cfd8dc;'); y += 30
    p.row(18, y, 'Plant COP', 'Plant_COP', 'Plant COP'); y += 26
    p.row(18, y, 'Chiller kW', 'CH01_kW', 'CH01 power', w1=80, w2=100); p.value(210, y, 92, 22, 'CH02_kW', 'CH02 power'); y += 26
    p.row(18, y, 'Auxiliary kW', 'Aux_kW', 'Aux (pumps+towers) power'); y += 26
    p.row(18, y, 'Plant energy', 'Plant_kWh', 'Plant energy kWh (totaliser)'); y += 26
    p.label(18, y, 280, 22, 'kW/RT: green < 0.65 · lime < 0.85 · amber < 1.0 · red', 9, fg='#546e7a')
    # ---- schematic
    p.rect(320, 80, 1000, 810, fill='#f7f9fa', stroke='#90a4ae', pen=1.0)
    for i, cx in enumerate((520, 830)):
        n = f'0{i + 1}'
        # condenser water: tower -> CDP -> condenser -> back to tower
        p.line([(cx - 40, 190), (cx - 40, 238)], CDS_C); p.line([(cx - 40, 300), (cx - 40, 360)], CDS_C)
        p.line([(cx + 60, 360), (cx + 60, 190)], CDR_C)
        # chilled water: return header -> CHP -> evaporator -> supply header
        p.line([(cx - 40, 720), (cx - 40, 670)], CHWR_C); p.line([(cx - 40, 610), (cx - 40, 545)], CHWR_C)
        p.line([(cx + 60, 545), (cx + 60, 585)], CHWS_C)
        status_box(p, cx - 100, 96, 200, 94, f'CT{n}', f'CT{n}', f'CT{n}RunProof', f'CT{n}StartCmd', f'CT{n}Fault',
                   [('Speed', f'CT{n}SpeedCmd', f'CT{n} fan speed command')])
        p.value(cx + 104, 120, 70, 22, f'CT{n}_kW', f'CT{n} power')
        status_box(p, cx - 110, 238, 140, 62 + 24, f'CDP{n}', f'CDP{n}', f'CDP{n}RunProof', f'CDP{n}StartCmd', f'CDP{n}Fault', [])
        p.value(cx + 70, 250, 70, 22, f'CDP{n}SpeedCmd', f'CDP{n} speed command'); p.value(cx + 70, 276, 70, 22, f'CDP{n}_kW', f'CDP{n} power')
        # chiller
        p.rect(cx - 110, 360, 240, 185, fill='#fafafa', stroke='#263238', pen=3.0, popup=f'station:|slot:{BASE}/Chiller{n}', ptitle=f'Chiller {n}')
        p.rect(cx - 106, 364, 232, 22, fill='#e8f5e9', stroke='#e8f5e9', pen=1.0); p.label(cx - 100, 364, 70, 22, 'condenser', 9, fg='#2e7d32')
        p.label(cx - 28, 365, 40, 20, 'retry', 9); p.value(cx + 8, 365, 38, 20, f'CH{n}_AutoRetryCount', f'CH{n} auto-retry count', size=9)
        p.fire(cx + 52, 365, 72, 20, 'RESET', f'CH{n}ResetFire', f'CH{n} lockout RESET (program)')
        p.rect(cx - 106, 519, 232, 22, fill='#e3f2fd', stroke='#e3f2fd', pen=1.0); p.label(cx - 100, 519, 200, 22, 'evaporator', 9, fg='#1565c0')
        p.value(cx - 100, 390, 220, 28, f'CH{n}RunProof', f'CH{n} run status', fmt=f'CHILLER {n}', size=13, bold=True, bool_bg=(C_RUN, C_OFF))
        yy = 422
        for lab, pt, what, bb in (('Command', f'CH{n}StartCmd', f'CH{n} start command', (C_RUN, C_OFF)),
                                  ('Fault', f'CH{n}Fault', f'CH{n} fault', (C_FLT, '#ffffff')),
                                  ('Lockout', f'CH{n}LockoutAlarm', f'CH{n} start/proof lockout', (C_FLT, '#ffffff'))):
            p.label(cx - 100, yy, 70, 20, lab, 10); p.value(cx - 30, yy, 64, 20, pt, what, size=10, bool_bg=bb); yy += 22
        p.label(cx + 37, 422, 36, 20, 'Load', 9); p.value(cx + 70, 422, 56, 20, f'CH{n}LoadPct', f'CH{n} load %', size=10)
        p.label(cx + 37, 444, 36, 20, 'kW', 9); p.value(cx + 70, 444, 56, 20, f'CH{n}_kW', f'CH{n} power', size=10)
        p.label(cx + 37, 466, 36, 20, 'Run h', 9); p.value(cx + 70, 466, 56, 20, f'CH{n}_RuntimeHours', f'CH{n} runtime hours', size=10)
        p.value(cx - 100, 494, 110, 22, f'CH{n}ValveOpenCmd', f'CH{n} isolation valve command', fmt='valve %out.value%', size=10, bool_bg=(C_RUN, C_OFF))
        p.value(cx + 14, 494, 110, 22, f'CH{n}ValveOpenProof', f'CH{n} isolation valve proof', fmt='proof %out.value%', size=10, bool_bg=(C_RUN, C_OFF))
        status_box(p, cx - 110, 586, 140, 86, f'CHP{n}', f'CHP{n}', f'CHP{n}RunProof', f'CHP{n}StartCmd', f'CHP{n}Fault', [])
        p.value(cx + 70, 598, 70, 22, f'CHP{n}SpeedCmd', f'CHP{n} speed command'); p.value(cx + 70, 624, 70, 22, f'CHP{n}_kW', f'CHP{n} power')
        p.value(cx + 64, 555, 70, 22, f'CH{n}CHWFlowProof', f'CH{n} CHW flow switch', fmt='CHW flow', size=9, bool_bg=(C_RUN, C_OFF))
        p.value(cx - 20, 330, 76, 22, f'CH{n}CDWFlowProof', f'CH{n} CDW flow switch', fmt='CDW flow', size=9, bool_bg=(C_RUN, C_OFF))
    # headers
    p.line([(480, 720), (1180, 720)], CHWR_C); p.line([(580, 585), (1180, 585)], CHWS_C); p.line([(890, 585), (890, 585)], CHWS_C)
    # load + bypass
    p.line([(1180, 585), (1180, 620)], CHWS_C); p.line([(1180, 690), (1180, 720)], CHWR_C)
    p.rect(1110, 620, 150, 70, fill='#fffde7', stroke='#8d6e63', pen=2.0); p.label(1118, 626, 140, 20, 'CHW LOAD (AHU/FCU)', 10, True)
    p.label(1118, 648, 60, 20, 'Load %', 10); p.value(1180, 648, 72, 20, 'PlantLoadPct', 'Plant load %', size=10)
    p.line([(1070, 585), (1070, 720)], '#78909c', 4.0)
    p.poly([(1060, 640), (1080, 640), (1060, 665), (1080, 665)], '#78909c')
    p.label(984, 598, 80, 18, 'BYPASS', 9, True); p.value(984, 616, 80, 20, 'CHW_BypassValveCmd', 'Bypass valve command %', size=10)
    p.value(984, 638, 80, 20, 'CHW_BypassValveFeedback', 'Bypass valve feedback %', size=10)
    p.label(984, 662, 80, 18, 'min flow SP', 9); p.value(984, 680, 80, 20, 'CHW_MinFlowSetpoint', 'Chiller minimum flow setpoint', size=10)
    # sensors
    p.label(1040, 560, 44, 20, 'CHWS', 10, True, CHWS_C); p.value(1084, 560, 76, 20, 'CHWS', 'CHW supply temperature', size=10)
    p.label(1040, 726, 44, 20, 'CHWR', 10, True, '#1e88e5'); p.value(1084, 726, 76, 20, 'CHWR', 'CHW return temperature', size=10)
    p.label(1190, 560, 44, 20, 'Flow', 10, True, CHWS_C); p.value(1234, 560, 80, 20, 'CHWFlow', 'CHW flow', size=10)
    p.label(1266, 630, 50, 20, 'DP', 10, True); p.value(1266, 650, 52, 20, 'CHWDP', 'CHW differential pressure', size=10)
    p.line([(1262, 600), (1262, 710)], '#8d6e63', 2.0)
    p.label(330, 196, 44, 20, 'CDS', 10, True, CDS_C); p.value(374, 196, 70, 20, 'CDS', 'CDW supply temperature', size=10)
    p.label(330, 220, 44, 20, 'CDR', 10, True, '#43a047'); p.value(374, 220, 70, 20, 'CDR', 'CDW return temperature', size=10)
    p.label(1030, 96, 280, 20, 'Pipe colours: CHWS / CHWR / CDS / CDR', 9, fg='#546e7a')
    p.line([(1030, 122), (1090, 122)], CHWS_C, 5); p.line([(1100, 122), (1160, 122)], CHWR_C, 5)
    p.line([(1170, 122), (1230, 122)], CDS_C, 5); p.line([(1240, 122), (1300, 122)], CDR_C, 5)
    p.label(1030, 140, 280, 18, 'Click equipment → its folder (property / wire sheet)', 9, fg='#546e7a')
    # ---- right: setpoints
    p.panel(1330, 80, 260, 206, 'SETPOINTS (ACTIVE)')
    y = 108
    for t, pt in (('CHW supply SP', 'CHW_LeavingTemperatureSetpoint_ACTIVE'), ('CHW DP SP', 'CHWDP_Setpoint_ACTIVE'),
                  ('CDW supply SP', 'CDS_Setpoint_ACTIVE'), ('Min flow SP', 'CHW_MinFlowSetpoint')):
        p.row(1338, y, t, pt, f'{t} (active)', w1=120, w2=120, bold=True); y += 24
    p.row(1338, y, 'Lead CH01', 'LeadCH01', 'Lead chiller selection (CH01)', w1=120, w2=120, bool_bg=('#bbdefb', '#ffe0b2')); y += 24
    p.row(1338, y, 'Stage 2 request', 'Stage2Request', 'Stage 2 request', w1=120, w2=120, bool_bg=(C_RUN, C_OFF)); y += 24
    p.label(1338, y + 2, 244, 18, 'Local setpoints & tuning → Optimisation page', 9, fg='#1565c0', popup='file:^px/ALT_CP_Optimization.px', ptitle='Optimisation & Mode')
    # ---- right: plant alarms (alarm-only logic points) + program reset
    p.panel(1330, 294, 260, 596, 'PLANT ALARMS')
    y = 322
    for t, pt in (('No chiller available', 'AllChillersUnavailableAlarm'), ('Start/stop mismatch', 'PlantStartStopMismatch'),
                  ('CHW flow low', 'CHW_FlowLowAlarm'), ('CH01 lockout (retry)', 'CH01LockoutAlarm'), ('CH01 lockout (RESET)', 'CH01HardLockoutAlarm'),
                  ('CH02 lockout (retry)', 'CH02LockoutAlarm'), ('CH02 lockout (RESET)', 'CH02HardLockoutAlarm'),
                  ('CHWS not tracking', 'CHWST_NotTrackingAlarm'), ('CDS not tracking', 'CDS_NotTrackingAlarm'), ('Low delta-T', 'LowDeltaTAlarm'),
                  ('Bypass mismatch', 'CHW_BypassValvePositionMismatch'), ('CHWS sensor', 'CHWS_SensorInvalidAlarm'), ('CDS sensor', 'CDS_SensorInvalidAlarm'),
                  ('CHW DP sensor', 'CHWDP_SensorInvalidAlarm'), ('CHW flow sensor', 'CHWFlow_SensorInvalidAlarm'), ('OA sensor', 'OA_SensorInvalidAlarm'),
                  ('Comms healthy', 'CommunicationHealthy'), ('Local > 1 h', 'LocalModeProlongedAlarm'), ('AI forced local', 'AiRequestedButLocalAlarm')):
        ok_is_true = pt.endswith('Healthy')
        p.row(1338, y, t, pt, f'{t} (alarm point)', w1=140, w2=104, size=9, bool_bg=(('#c8e6c9', C_FLT) if ok_is_true else (C_FLT, '#c8e6c9'))); y += 24
    p.fire(1338, y + 6, 244, 30, 'RESET PROGRAM ALARMS', 'PlantAlarmResetFire', 'Reset both chiller lockouts + retry counters')
    p.label(1338, y + 40, 244, 18, 'Equipment faults clear at the equipment.', 9, fg='#546e7a')
    p.label(1338, y + 58, 244, 18, 'Alarm list & histories →', 10, True, '#1565c0', popup='file:^px/ALT_CP_AlarmsHistory.px', ptitle='Alarms & History')
    return p


def optimization():
    p = Page('ALT_CP_Optimization', 'Optimisation & Mode'); p.header()
    # CT approach chain
    p.panel(10, 80, 780, 250, 'COOLING TOWER — CDW SETPOINT FROM OUTDOOR WET-BULB (approach control)')
    boxes = [('OA dry bulb', 'OA_Temperature'), ('OA RH', 'OA_Humidity'), ('OA wet bulb', 'OA_WetBulb'), ('+ approach', 'CT_Approach'),
             ('Optimised SP', 'Opt_CdwSetpoint'), ('ACTIVE SP', 'CDS_Setpoint_ACTIVE'), ('CDS actual', 'CDS'), ('CT01 speed', 'CT01SpeedCmd')]
    x = 20
    for i, (t, pt) in enumerate(boxes):
        p.label(x, 118, 88, 20, t, 10, True, halign='center')
        p.value(x, 140, 88, 30, pt, f'CT approach chain: {t}', size=12, bold=True, action=(pt == 'CT_Approach'))
        if i < len(boxes) - 1: p.poly([(x + 90, 148), (x + 96, 155), (x + 90, 162)], '#607d8b')
        x += 96
    y = 190
    p.row(20, y, 'CDW SP min', 'CDW_MinSetpoint', 'CDW setpoint low clamp', action=True); p.row(290, y, 'CDW SP max', 'CDW_MaxSetpoint', 'CDW setpoint high clamp', action=True)
    p.row(560, y, 'WB default', 'OA_WetBulbDefault', 'WB used when OA invalid', w1=110, w2=100, action=True); y += 28
    p.row(20, y, 'OA valid', 'OA_Valid', 'OA sensor valid', bool_bg=(C_RUN, C_FLT)); p.row(290, y, 'OA sensor fault', 'OA_SensorFault', 'OA sensor fault input', bool_bg=(C_FLT, '#ffffff'))
    p.row(560, y, 'Tower PID', 'ObsNum_CDS_PID', 'Tower PID output %', w1=110, w2=100); y += 28
    p.label(20, y + 4, 760, 40, 'CDW SP = clamp(OA wet-bulb + approach, min, max). Lower CDW temperature cuts chiller kW; the tower fan (20 % min) '
            'speeds up only when CDS is above SP. Invalid OA sensor → default wet-bulb + alarm.', 10, fg='#37474f')
    # Plant reset
    p.panel(800, 80, 790, 250, 'CHILLED-WATER RESET (ASHRAE GPC36 style: 0–50 % reset DP, 50–100 % reset CHWST)')
    x = 810
    for t, pt in (('Plant load', 'PlantLoadPct'), ('Reset request', 'PlantResetPct'), ('Optimised DP SP', 'Opt_DpSetpoint'), ('ACTIVE DP SP', 'CHWDP_Setpoint_ACTIVE'),
                  ('CHW DP', 'CHWDP'), ('CHP01 speed', 'CHP01SpeedCmd')):
        p.label(x, 118, 120, 20, t, 10, True, halign='center'); p.value(x, 140, 120, 28, pt, f'DP reset chain: {t}', size=12, bold=True); x += 128
    x = 810
    for t, pt in (('Optimised CHWST', 'Opt_ChwstSetpoint'), ('ACTIVE CHWST', 'CHW_LeavingTemperatureSetpoint_ACTIVE'), ('CHWS actual', 'CHWS')):
        p.label(x, 180, 120, 20, t, 10, True, halign='center'); p.value(x, 202, 120, 28, pt, f'CHWST reset chain: {t}', size=12, bold=True); x += 128
    y = 240
    p.row(1200, 180, 'DP min', 'DP_MinSetpoint', 'DP reset minimum', w1=80, w2=90, action=True); p.row(1390, 180, 'DP max', 'DP_MaxSetpoint', 'DP reset maximum', w1=80, w2=90, action=True)
    p.row(1200, 206, 'CHWST min', 'CHWST_MinSetpoint', 'CHWST reset minimum', w1=80, w2=90, action=True); p.row(1390, 206, 'CHWST max', 'CHWST_MaxSetpoint', 'CHWST reset maximum', w1=80, w2=90, action=True)
    p.label(810, y + 4, 770, 60, 'Low load → lower pump DP first (pump kW ~ speed³), then raise CHWST (chiller kW −2…3 %/K). '
            'Reset request here = plant load % (proxy). On site replace with trim & respond from AHU valve requests.', 10, fg='#37474f')
    # Mode & heartbeat
    p.panel(10, 340, 780, 300, 'OPERATION MODE — AI / LOCAL (user Local always wins)')
    y = 372
    p.label(20, y, 140, 26, 'User request', 11); p.button(160, y, 90, 26, 'LOCAL', 'ModeCmd_UI', False, 'User mode = Local'); p.button(256, y, 90, 26, 'AI', 'ModeCmd_UI', True, 'User mode = AI')
    p.row(380, y, 'Operation mode', 'OperationMode', 'Operation mode', bool_bg=('#7e57c2', '#90a4ae')); y += 30
    p.row(20, y, 'Heartbeat value', 'HeartbeatTimestampSetpoint', 'AI heartbeat value (AI writes)'); p.row(380, y, 'Heartbeat', 'HeartbeatDetectorStatus', 'Heartbeat status', bool_bg=(C_RUN, C_FLT)); y += 26
    p.row(20, y, 'Pre-disconnect', 'HeartbeatPreDisconnect', 'Heartbeat pre-disconnect (6 min)', bool_bg=(C_WARN, '#c8e6c9')); p.row(380, y, 'AI available', 'AI_Available', 'AI available', bool_bg=(C_RUN, C_WARN)); y += 26
    p.row(20, y, 'Optimisation', 'OptimizationEnable', 'Local-mode optimiser enable', action=True); p.row(380, y, 'Local > 1 h', 'LocalModeProlongedAlarm', 'Local mode prolonged', bool_bg=(C_WARN, '#c8e6c9')); y += 34
    for i, h in enumerate(('Setpoint', '_LOCAL (user)', '_AI (AI writes)', 'Optimised', '_ACTIVE (to plant)')):
        p.label(20 + i * 152, y, 148, 22, h, 10, True, 'white', '#607d8b', 'center')
    y += 26
    for t, loc, ai, opt, act in (('CHW supply °C', 'CHW_LeavingTemperatureSetpoint_LOCAL', 'CHW_LeavingTemperatureSetpoint_AI', 'Opt_ChwstSetpoint', 'CHW_LeavingTemperatureSetpoint_ACTIVE'),
                                 ('CHW DP kPa', 'CHWDPSetpoint', 'CHWDP_Setpoint_AI', 'Opt_DpSetpoint', 'CHWDP_Setpoint_ACTIVE'),
                                 ('CDW supply °C', 'CDSSetpoint', 'CDS_Setpoint_AI', 'Opt_CdwSetpoint', 'CDS_Setpoint_ACTIVE')):
        p.label(20, y, 148, 24, t, 11, True)
        p.value(172, y, 148, 24, loc, f'{t} local SP', action=True); p.value(324, y, 148, 24, ai, f'{t} AI SP')
        p.value(476, y, 148, 24, opt, f'{t} optimised SP'); p.value(628, y, 148, 24, act, f'{t} active SP', bold=True); y += 28
    p.label(20, y + 2, 760, 20, 'AI values are range-checked (AI_…Min/Max); ACTIVE is always clamped before it reaches equipment.', 10, fg='#37474f')
    # Min flow bypass
    p.panel(800, 340, 790, 300, 'CHW MINIMUM-FLOW BYPASS')
    y = 372
    for (t1, p1), (t2, p2) in ((('CH01 min flow', 'CH01_MinFlow'), ('CH02 min flow', 'CH02_MinFlow')),
                               (('CH01 valve cmd', 'CH01ValveOpenCmd'), ('CH02 valve cmd', 'CH02ValveOpenCmd')),
                               (('Min flow SP (Σ open)', 'CHW_MinFlowSetpoint'), ('CHW flow', 'CHWFlow')),
                               (('Bypass cmd', 'CHW_BypassValveCmd'), ('Bypass feedback', 'CHW_BypassValveFeedback')),
                               (('Mismatch alarm', 'CHW_BypassValvePositionMismatch'), ('Flow low alarm', 'CHW_FlowLowAlarm'))):
        kw1 = {'action': True} if p1.endswith('MinFlow') else ({'bool_bg': (C_RUN, C_OFF)} if 'Valve' in p1 and 'Cmd' in p1 else {})
        kw2 = {'action': True} if p2.endswith('MinFlow') else ({'bool_bg': (C_RUN, C_OFF)} if 'Valve' in p2 and 'Cmd' in p2 else {})
        if 'alarm' in t1.lower(): kw1 = {'bool_bg': (C_FLT, '#c8e6c9')}; kw2 = {'bool_bg': (C_FLT, '#c8e6c9')}
        p.row(810, y, t1, p1, t1, w1=170, w2=110, **kw1); p.row(1200, y, t2, p2, t2, w1=170, w2=110, **kw2); y += 30
    p.label(810, y + 6, 770, 60, 'SP = Σ minimum flow of chillers whose isolation valve is open. Reverse-acting PID opens the bypass when flow < SP '
            '(rate-limited). Bypass closed whenever plant/pumps are off. Command ≠ feedback > 10 % for 2 min → alarm.', 10, fg='#37474f')
    # Staging & rotation
    p.panel(10, 650, 1580, 240, 'STAGING, FAILSAFE & RUNTIME ROTATION')
    y = 682
    col = [[('Stage 2 request', 'Stage2Request', {'bool_bg': (C_RUN, C_OFF)}), ('Stage-up margin K', 'StageUpTempMargin', {'action': True}),
            ('Min ΔT for stage 2', 'MinDeltaTStage2', {'action': True}), ('Plant stage', 'PlantStage', {})],
           [('Lead CH01 (manual)', 'LeadCH01', {'action': True}), ('Rotation request', 'RotationRequest', {'action': True}),
            ('Runtime rotation', 'RotationMode_Runtime', {'action': True}), ('Rotation hours', 'RuntimeRotationHours', {'action': True})],
           [('CH01 runtime h', 'CH01_RuntimeHours', {}), ('CH02 runtime h', 'CH02_RuntimeHours', {}),
            ('CH01 retries used', 'CH01_AutoRetryCount', {}), ('CH02 retries used', 'CH02_AutoRetryCount', {})],
           [('Auto-retry lockout', 'CH_AutoRetryEnable', {'action': True}), ('Max auto-retries', 'CH_MaxAutoRetries', {'action': True}),
            ('Boot auto-qualify', 'BootAutoQualifyEnable', {'action': True}), ('CHP fail-safe %', 'CHP_FailSafeSpeed', {'action': True})],
           [('CT fail-safe %', 'CT_FailSafeSpeed', {'action': True}), ('Bypass fail-safe %', 'Byp_FailSafePosition', {'action': True}),
            ('CHW DP valid min', 'CHWDP_MinValid', {'action': True}), ('CHW flow valid max', 'CHWFlow_MaxValid', {'action': True})]]
    for ci, items in enumerate(col):
        yy = y
        for t, pt, kw in items:
            p.row(20 + ci * 316, yy, t, pt, t, w1=160, w2=130, size=11, **kw); yy += 30
    p.fire(20 + 2 * 316, y + 124, 140, 26, 'RESET CH01', 'CH01ResetFire', 'CH01 lockout RESET (program)')
    p.fire(20 + 2 * 316 + 150, y + 124, 140, 26, 'RESET CH02', 'CH02ResetFire', 'CH02 lockout RESET (program)')
    p.fire(20 + 3 * 316, y + 124, 290, 26, 'RESET PROGRAM ALARMS', 'PlantAlarmResetFire', 'Reset both chiller lockouts + retry counters')
    p.label(20, y + 158, 1560, 40, 'Stage 2 = plant load > 90 % of one chiller for 10 min (off < 60 % for 15 min) OR lead chiller > 95 % for 10 min OR CHWS > SP + margin 10 min. Program lockout (proof/aux timeout) auto-resets after 180 s, max N times, then RESET. '
            'Sensor/comms faults never stop the plant: the affected loop goes to its fail-safe output. Restart auto-qualifies after 120 s.', 10, fg='#37474f')
    return p


def energy():
    p = Page('ALT_CP_Energy', 'Energy & KPI'); p.header()
    p.panel(10, 80, 520, 380, 'PLANT EFFICIENCY')
    p.label(30, 116, 200, 26, 'Plant kW/RT', 14, True)
    p.value(230, 110, 280, 60, 'Plant_kW_per_RT', 'Plant efficiency kW/RT', size=30, bold=True,
            num_bg='gx:Brush 0.0:0.65=#66bb6a;0.65:0.85=#d4e157;0.85:1.0=#ffca28;1.0:100.0=#ef5350;default=#cfd8dc;')
    y = 190
    for t, pt in (('Plant COP', 'Plant_COP'), ('Cooling load kW', 'CoolingLoad_kW'), ('Cooling load RT', 'CoolingLoad_RT'),
                  ('Plant power kW', 'Plant_kW'), ('CH01 kW', 'CH01_kW'), ('CH02 kW', 'CH02_kW'), ('Auxiliary kW', 'Aux_kW'), ('CHW flow', 'CHWFlow'), ('CHW ΔT basis: CHWR', 'CHWR'), ('CHW ΔT basis: CHWS', 'CHWS')):
        p.row(30, y, t, pt, t, w1=200, w2=160, size=12); y += 28
    p.panel(540, 80, 1050, 380, 'POWER BY EQUIPMENT (kW, emulated from speed³ / load in simulation)')
    x = 570
    for pt, mx in (('CH01_kW', 200), ('CH02_kW', 200), ('CHP01_kW', 20), ('CHP02_kW', 20), ('CDP01_kW', 20), ('CDP02_kW', 20), ('CT01_kW', 12), ('CT02_kW', 12)):
        p.label(x, 116, 110, 20, pt.replace('_kW', ''), 11, True, halign='center')
        p.bar(x + 20, 140, 70, 250, pt, mx, f'{pt} bargraph', fill='#1e88e5' if pt.startswith('CH0') else '#43a047')
        p.value(x, 400, 110, 22, pt, f'{pt} value'); x += 125
    p.panel(10, 470, 780, 420, 'ENERGY TOTALISERS (kWh) & RUNTIME')
    y = 504
    for t, pt in (('Plant kWh', 'Plant_kWh'), ('CH01 kWh', 'CH01_kWh'), ('CH02 kWh', 'CH02_kWh'), ('Auxiliary kWh', 'Aux_kWh'),
                  ('CH01 runtime h', 'CH01_RuntimeHours'), ('CH02 runtime h', 'CH02_RuntimeHours')):
        p.row(30, y, t, pt, t, w1=200, w2=180, size=12); y += 30
    p.label(30, y + 10, 740, 60, 'kWh points are NumericTotalizerExt (hourly) on the kW points; runtime is DiscreteTotalizerExt on proven-run points. '
            'All are trended (interval 1 min) for daily/monthly reports in the History / Report services.', 10, fg='#37474f')
    p.panel(800, 470, 790, 420, 'ENERGY PARAMETERS (simulation / project values)')
    y = 504
    for t, pt in (('CH01 rated kW', 'CH01_RatedKW'), ('CH02 rated kW', 'CH02_RatedKW'), ('CHW pump rated kW', 'CHP_RatedKW'), ('CDW pump rated kW', 'CDP_RatedKW'),
                  ('Tower fan rated kW', 'CT_RatedKW'), ('Min load for KPI (RT)', 'MinLoadForKpi'), ('CHW kW factor', 'Water_kW_Factor')):
        p.row(820, y, t, pt, t, w1=220, w2=160, size=12, action=True); y += 30
    p.label(820, y + 10, 750, 60, 'Plant_kW_per_RT alarm: OutOfRange 0..1.2 kW/RT, 15 min delay, inhibited until the plant has run 30 min. '
            'In the real plant replace emulated kW with power-meter points (same point names keep the mapping).', 10, fg='#37474f')
    return p


def alarms_history():
    p = Page('ALT_CP_AlarmsHistory', 'Alarms & History'); p.header()
    p.label(10, 80, 800, 26, 'Alarm extensions in /ChillerPlant (class · algorithm · inhibit)', 14, True)
    p.table(10, 108, 1580, 360, "select parent.displayName as 'Point', parent.slotPath as 'Slot Path', type.typeName as 'Extension Type', "
            "alarmClass, alarmInhibit as 'Inhibit', offnormalAlgorithm, timeDelay from alarm:AlarmSourceExt", 'Alarm extension list (BQL)')
    p.label(10, 476, 800, 26, 'History extensions in /ChillerPlant', 14, True)
    p.table(10, 504, 1170, 386, "select parent.displayName as 'Point', type as 'History Type', historyConfig.id as 'History ID', historyConfig.capacity, "
            "enabled, status, parent.slotPath as 'Slot Path' from control:PointExtension where type = 'history:NumericIntervalHistoryExt' or "
            "type = 'history:NumericCovHistoryExt' or type = 'history:BooleanCovHistoryExt'", 'History extension list (BQL)')
    p.label(1190, 476, 400, 26, 'Alarm classes', 14, True)
    p.el.append('<BoundTable layout="1190.0,504.0,400.0,200.0">\n  <TableBinding ord="station:|slot:/|bql:select displayName, inAlarmCount as &#x27;inAlarm&#x27;, '
                'unackedAlarmCount as &#x27;unacked&#x27; from alarm:AlarmClass"/>\n</BoundTable>')
    p.map.append(('(BQL)', 'station:|slot:/|bql:select … from alarm:AlarmClass', 'Alarm class counters', 'table'))
    p.label(1190, 712, 400, 180, 'Open the Alarm Console (Station > Alarm) to acknowledge. Histories: Station > History > (station name). '
            'Process alarms are inhibited until the plant has run 30 min (MELCO rule).', 10, fg='#37474f')
    return p


def simulation():
    p = Page('ALT_CP_Simulation', 'Simulation'); p.header()
    p.panel(10, 80, 780, 520, 'SIMULATED ANALOG INPUTS (ramp / sine at priority in10 — Override in8 wins for manual tests)')
    y = 112
    for t, pt in (('OA dry bulb 27–35 °C / 30 min', 'OA_Temperature'), ('OA RH 50–90 % / 40 min', 'OA_Humidity'), ('Plant load 20–140 % of 1 CH / 60 min', 'PlantLoadPct'),
                  ('CHWS 6.5–8.1 °C / 20 min', 'CHWS'), ('CHWR 10.5–13.5 °C / 25 min', 'CHWR'), ('CHW flow 60–240 m³/h / 45 min', 'CHWFlow'),
                  ('CHW DP 80–160 kPa / 15 min', 'CHWDP'), ('CDS 28–32 °C / 30 min', 'CDS'), ('CDR 33–37 °C / 30 min', 'CDR'),
                  ('CH01 load 15–95 % / 40 min', 'CH01LoadPct'), ('CH02 load 15–95 % / 50 min', 'CH02LoadPct'),
                  ('AI CHWST SP 7–9 °C / 60 min', 'CHW_LeavingTemperatureSetpoint_AI'), ('AI DP SP 70–140 kPa / 60 min', 'CHWDP_Setpoint_AI'),
                  ('AI CDS SP 26–31 °C / 60 min', 'CDS_Setpoint_AI'), ('AI heartbeat +1 / ~5 min', 'HeartbeatTimestampSetpoint')):
        p.row(20, y, t, pt, f'Simulated input: {t}', w1=300, w2=160); y += 30
    p.label(20, y + 6, 760, 20, 'AI heartbeat emulation', 11, True)
    p.button(200, y + 2, 100, 26, 'BEATING', 'Sim_AiHeartbeatEnable', True, 'AI heartbeat emulation on')
    p.button(306, y + 2, 100, 26, 'STOPPED', 'Sim_AiHeartbeatEnable', False, 'AI heartbeat emulation off (test loss)')
    p.panel(800, 80, 790, 272, 'EMULATED FEEDBACK (from commands, priority in10)')
    y = 112
    for n in ('01', '02'):
        for t, pt in ((f'CH{n} run proof', f'CH{n}RunProof'), (f'CH{n} valve proof', f'CH{n}ValveOpenProof'), (f'CH{n} CHW flow', f'CH{n}CHWFlowProof'),
                      (f'CH{n} CDW flow', f'CH{n}CDWFlowProof'), (f'CHP{n} run proof', f'CHP{n}RunProof'), (f'CDP{n} run proof', f'CDP{n}RunProof'),
                      (f'CT{n} run proof', f'CT{n}RunProof')):
            p.row(810 if n == '01' else 1200, y if n == '01' else y, t, pt, f'Emulated feedback: {t}', w1=200, w2=160, bool_bg=(C_RUN, C_OFF))
            y += 30
        if n == '01': y = 112
    p.row(810, 330, 'Bypass valve feedback', 'CHW_BypassValveFeedback', 'Emulated bypass feedback', w1=200, w2=160)
    # quick start: everything needed to see the plant run in a fresh station
    p.panel(800, 360, 790, 240, 'QUICK START (fresh station: press 1 → 2, then watch Plant Overview)')
    y = 392
    p.label(810, y, 250, 26, '1. Restart qualified', 11, True); p.button(1070, y, 110, 26, 'QUALIFY', 'BootQualified', True, 'Quick start: boot qualified'); p.button(1186, y, 110, 26, 'HOLD', 'BootQualified', False, 'Quick start: boot hold'); y += 32
    p.label(810, y, 250, 26, '2. Plant enable', 11, True); p.button(1070, y, 110, 26, 'ON', 'PlantEnable', True, 'Quick start: plant ON'); p.button(1186, y, 110, 26, 'OFF', 'PlantEnable', False, 'Quick start: plant OFF'); y += 32
    p.label(810, y, 250, 26, '3. (optional) Mode request', 11, True); p.button(1070, y, 110, 26, 'LOCAL', 'ModeCmd_UI', False, 'Quick start: Local'); p.button(1186, y, 110, 26, 'AI', 'ModeCmd_UI', True, 'Quick start: AI'); y += 32
    p.row(810, y, 'Plant run request', 'PlantRunRequest', 'Quick start: run request', w1=250, w2=110, bool_bg=(C_RUN, C_OFF)); p.value(1186, y, 110, 22, 'PlantStage', 'Quick start: stage'); y += 28
    p.label(810, y + 4, 770, 60, 'Ramps run as soon as the station runs (no button). CH01 starts ~4 s after step 2; stage 2 follows plant load > 70 %. '
            'AI mode needs 2 emulated heartbeats (~10 min). Nobody pressing QUALIFY: the plant auto-qualifies 120 s after station start. An offline BOG never executes.', 10, fg='#37474f')
    p.panel(10, 610, 1580, 280, 'FAULT INJECTION (SET / CLR write the fallback of unlinked inputs; for proofs use right-click → Override)')
    y = 642
    items = [(f'{e}{n} {k}', f'{e}{n}{k2}') for n in ('01', '02') for e in ('CH', 'CHP', 'CDP', 'CT') for k, k2 in (('fault', 'Fault'), ('available', 'Available'))]
    items += [('OA sensor fault', 'OA_SensorFault'), ('CHWS sensor healthy', 'CHWSSensorHealthy'), ('CDS sensor healthy', 'CDSSensorHealthy'), ('Comms healthy', 'CommunicationHealthy')]
    for i, (t, pt) in enumerate(items):
        cx = 20 + (i % 4) * 392; cy = y + (i // 4) * 28 + (6 if i >= 16 else 0)
        bad_true = pt.endswith('Fault')
        p.label(cx, cy, 142, 22, t, 10)
        p.value(cx + 142, cy, 96, 22, pt, f'Fault injection: {t}', size=10, bool_bg=((C_FLT, '#c8e6c9') if bad_true else ('#c8e6c9', C_FLT)))
        p.button(cx + 242, cy, 64, 22, 'SET', pt, True, f'Fault injection: {t} = true')
        p.button(cx + 310, cy, 64, 22, 'CLR', pt, False, f'Fault injection: {t} = false')
    return p


def energy_dashboard():
    p = Page('ALT_CP_EnergyDashboard', 'Energy Dashboard'); p.header()
    kw_rt_map = 'gx:Brush 0.0:0.01=#eceff1;0.01:0.65=#66bb6a;0.65:0.85=#d4e157;0.85:1.0=#ffca28;1.0:100.0=#ef5350;default=#cfd8dc;'
    # ---- live KPI tiles
    tiles = [('Plant kW/RT (live)', 'Plant_kW_per_RT', kw_rt_map, 26), ('Plant COP', 'Plant_COP', None, 24), ('Plant power', 'Plant_kW', None, 22),
             ('Cooling load', 'CoolingLoad_RT', None, 22), ('Chiller power', 'CH01_kW', None, 16), ('Auxiliary power', 'Aux_kW', None, 22),
             ('OA wet bulb', 'OA_WetBulb', None, 22)]
    x = 10
    for t, pt, mp, fs in tiles:
        w = 226
        p.rect(x, 80, w - 6, 118, fill='white', stroke='#78909c', pen=2.0)
        p.label(x + 6, 86, w - 18, 22, t, 11, True, '#455a64')
        if t == 'Chiller power':
            p.label(x + 8, 116, 44, 26, 'CH01', 10); p.value(x + 52, 114, w - 70, 30, 'CH01_kW', 'CH01 power (live)', size=fs, bold=True)
            p.label(x + 8, 152, 44, 26, 'CH02', 10); p.value(x + 52, 150, w - 70, 30, 'CH02_kW', 'CH02 power (live)', size=fs, bold=True)
        else:
            p.value(x + 8, 116, w - 22, 64, pt, f'{t} tile', size=fs, bold=True, num_bg=mp)
        x += w
    # ---- energy periods table
    p.panel(10, 210, 930, 360, 'ENERGY BY PERIOD (resets: day 00:00, month day-1 00:02)')
    cols = [('Today', 'Today'), ('Yesterday', 'Yesterday'), ('This month', 'Month'), ('Last month', 'LastMonth')]
    rows = [('Plant energy', 'Plant_kWh_{}', None), ('Auxiliary energy', 'Aux_kWh_{}', None), ('Cooling delivered (RT-h)', 'Cooling_RTh_{}', None),
            ('Plant kW/RT', 'Plant_kW_per_RT_{}', kw_rt_map), ('Energy cost (THB)', 'Energy_Cost_THB_{}', None), ('CO2 (kg)', 'CO2_kg_{}', None)]
    for i, (h, _) in enumerate(cols):
        p.label(250 + i * 170, 242, 164, 26, h, 11, True, 'white', '#607d8b', 'center')
    y = 274
    for t, pat, mp in rows:
        p.label(24, y, 220, 30, t, 12, True)
        for i, (_, key) in enumerate(cols):
            pt = pat.format(key)
            p.value(250 + i * 170, y, 164, 30, pt, f'{t} {key}', size=13, bold=(mp is not None), num_bg=mp)
        y += 36
    p.label(24, y + 8, 900, 40, 'Today/yesterday: TimeTrigger 00:00 resets EnergyToday totalisers, 23:59 latches yesterday. Month: schedule day 1 00:02 latches last month, '
            'reset 30 s later. kW/RT = kWh / RT-h. All values are trended (1 min).', 10, fg='#37474f')
    # ---- comparisons
    p.panel(950, 210, 640, 360, 'COMPARISON')
    bars = [('Today', 'Plant_kWh_Today', 9000, '#1e88e5'), ('Yesterday', 'Plant_kWh_Yesterday', 9000, '#90caf9'),
            ('Month', 'Plant_kWh_Month', 270000, '#43a047'), ('Last month', 'Plant_kWh_LastMonth', 270000, '#a5d6a7')]
    x = 970
    p.label(970, 240, 300, 20, 'Plant kWh (day scale 9 MWh, month 270 MWh)', 9, fg='#546e7a')
    for t, pt, mx, c in bars:
        p.label(x, 262, 70, 20, t, 10, True, halign='center')
        p.bar(x + 10, 284, 50, 220, pt, mx, f'{t} kWh bar', fill=c)
        p.value(x - 4, 510, 78, 22, pt, f'{t} kWh value', size=9)
        x += 80
    x = 1300
    p.label(1300, 240, 290, 20, 'kW/RT vs baseline (scale 1.5)', 9, fg='#546e7a')
    for t, pt in (('Today', 'Plant_kW_per_RT_Today'), ('Yesterday', 'Plant_kW_per_RT_Yesterday'), ('Month', 'Plant_kW_per_RT_Month'), ('Baseline', 'Baseline_kW_per_RT')):
        p.label(x, 262, 70, 20, t, 10, True, halign='center')
        p.bar(x + 12, 284, 46, 220, pt, 1.5, f'{t} kW/RT bar', fill='#ffb300' if t == 'Baseline' else '#7e57c2')
        p.value(x - 2, 510, 74, 22, pt, f'{t} kW/RT value', size=9, action=(t == 'Baseline'))
        x += 72
    # ---- savings + tariffs
    p.panel(10, 580, 620, 310, 'SAVINGS vs BASELINE (M&V reference)')
    y = 612
    for t, pt, kw in (('Baseline plant kW/RT', 'Baseline_kW_per_RT', {'action': True}), ('Saving this month (kWh)', 'Saving_kWh_Month', {}),
                      ('Saving this month (THB)', 'Saving_THB_Month', {}), ('Saving last month (kWh)', 'Saving_kWh_LastMonth', {}),
                      ('Saving last month (THB)', 'Saving_THB_LastMonth', {}), ('Tariff (THB/kWh)', 'Tariff_THB_per_kWh', {'action': True}),
                      ('Grid factor (kgCO2/kWh)', 'CO2_kg_per_kWh', {'action': True})):
        p.row(24, y, t, pt, t, w1=260, w2=180, size=12, **kw); y += 32
    p.label(24, y + 6, 590, 40, 'Saving = RT-h x baseline kW/RT - measured kWh. Baseline, tariff and grid factor are PROJECT values (click to edit).', 10, fg='#37474f')
    # ---- trends (history popups) + breakdown
    p.panel(640, 580, 950, 310, 'TRENDS (click to open history) & LIVE BREAKDOWN')
    trends = [('Plant kW', 'Plant_kW'), ('Plant kW/RT', 'Plant_kW_per_RT'), ('Cooling load RT', 'CoolingLoad_RT'), ('Plant kWh today', 'Plant_kWh_Today'),
              ('kW/RT today', 'Plant_kW_per_RT_Today'), ('CHW supply temp', 'CHWS'), ('CDW supply temp', 'CDS'), ('OA wet bulb', 'OA_WetBulb')]
    for i, (t, h) in enumerate(trends):
        cx = 656 + (i % 4) * 150; cy = 614 + (i // 4) * 40
        o = f'history:/{STATION_NAME}/{h}'
        p.label(cx, cy, 142, 32, t + '  ↗', 10, True, 'white', '#1e88e5', 'center', popup=o, ptitle=t)
        p.map.append((h, o, f'Trend popup {t}', 'history popup'))
    p.label(656, 704, 590, 20, 'Live power split', 11, True, '#455a64')
    x = 656
    for t, pt, mx in (('CH01', 'CH01_kW', 200), ('CH02', 'CH02_kW', 200), ('CHP01', 'CHP01_kW', 20), ('CHP02', 'CHP02_kW', 20),
                      ('CDP01', 'CDP01_kW', 20), ('CDP02', 'CDP02_kW', 20), ('CT01', 'CT01_kW', 12), ('CT02', 'CT02_kW', 12)):
        p.label(x, 728, 100, 18, t, 9, True, halign='center')
        p.bar(x + 30, 748, 40, 110, pt, mx, f'{t} kW live bar', fill='#1e88e5' if t.startswith('CH0') else '#43a047')
        x += 110
    p.label(1540, 728, 50, 18, '', 9)
    return p


def load_folders(bog):
    root = ET.fromstring(zipfile.ZipFile(bog).read('file.xml'))
    cp = next(e for e in root.iter('p') if e.get('n') == 'ChillerPlant')
    out = {}
    def walk(el, pre):
        for c in el:
            if c.tag != 'p' or not c.get('t'): continue
            if c.get('t') == 'b:Folder': walk(c, (pre + '/' if pre else '') + c.get('n')); continue
            out[c.get('n')] = pre
    walk(cp, '')
    folders = {e.get('n') for e in cp.iter('p') if e.get('t') == 'b:Folder'}
    return out, folders


def read_reg(path, key='Point'):
    d = {}
    if os.path.exists(path):
        for r in csv.DictReader(open(path, encoding='utf-8-sig')):
            d.setdefault(r[key], []).append(r)
    return d


if __name__ == '__main__':
    bog, outdir = sys.argv[1], sys.argv[2]
    FOLDER, FOLDERS = load_folders(bog)
    regdir = os.path.join(os.path.dirname(os.path.abspath(bog)), 'reg')
    H, A, T = (read_reg(os.path.join(regdir, f)) for f in ('V6_HISTORY_REGISTER.csv', 'V6_ALARM_REGISTER.csv', 'V6_TAG_REGISTER.csv'))
    os.makedirs(os.path.join(outdir, 'px'), exist_ok=True)
    rows, bad = [], []
    for fn in (overview, optimization, energy_dashboard, energy, alarms_history, simulation):
        p = fn()
        x = p.xml()
        ET.fromstring(x.encode('utf-8'))           # well-formed
        with open(os.path.join(outdir, 'px', p.name + '.px'), 'w', encoding='utf-8') as f:
            f.write(x)
        for pt, o, what, mode in p.map:
            if pt != '(BQL)' and pt not in FOLDER: bad.append((p.name, pt))
            hist = '; '.join(r['History_ID'] for r in H.get(pt, []))
            alm = '; '.join(f"{r['Alarm_Type']}/{r['Alarm_Class']}" for r in A.get(pt, []))
            tag = '; '.join(r['Value'] for r in T.get(pt, []) if r['Tag'] == 'melco:pointNameString')
            rows.append({'Graphic': p.name + '.px', 'Element': what, 'Point': pt, 'ORD': o, 'Binding': mode,
                         'Folder': FOLDER.get(pt, ''), 'History_ID': hist, 'Alarm': alm, 'MELCO_Tag': tag})
        popups = re.findall(r'PopupBinding ord="station:\|slot:/ChillerPlant/([^"]+)"', x)
        bad += [(p.name, 'folder ' + f) for f in popups if f.split('/')[-1] not in FOLDERS]
        print(p.name, len(p.el), 'elements', len(p.map), 'bindings')
    assert not bad, bad
    with open(os.path.join(outdir, 'V6_GRAPHIC_POINT_MAPPING.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    pts = {r['Point'] for r in rows if r['Point'] != '(BQL)'}
    print('bindings', len(rows), 'distinct points', len(pts))
