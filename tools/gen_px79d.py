# -*- coding: utf-8 -*-
"""V7.9 r2 chiller plant schematic (Px_Plant = ALT_V79_Plant.px): V7.8 detail level for 6 slots per type.
 * equipment pictures rendered from the SAME 3-D models as ALT_V79_Building3D.html (chiller, end-suction pump, 2-cell tower)
   grey = stopped, colour = running, tower fans animate
 * shaded pipe layer (CHWS / CHWR / CDWS / CDWR headers, risers, branches, arrows), butterfly valves with position frames,
   TT / PT / FT instruments, flow switches, BTU meter, bypass (MOD + isolation + manual loop), expansion tank
 * cards per pump, info strip per chiller, tower / chiller tables, supervisor, condenser water, outdoor air, legend,
   pools, alarms, control, kW/RT gauge
usage: gen_px79d.py v79.bog kitdir outdir sprites73 sprites74 rawdir"""
import sys, os, json
from xml.sax.saxutils import quoteattr
import numpy as np
from PIL import Image, ImageEnhance
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_px78 as G78                                      # full V7.8 Px stack (helpers, sprites, header patches)
from gen_px78 import G74, G73, G71, G7, G
from gen_px7 import val, lbl, panel, status_led, RUN, OFF, FLT, WARN, TXT
from gen_px71 import ximg, hot, tag, isa, hdr_text, kwrt_val, OKC
import pipes71
import gen_px79 as P79

SPR = G73.SPR
PW, PH = 2400, 1752
N = 6
Y0, RP = 430, 180                                           # first row top, row pitch
ROW = [Y0 + i * RP for i in range(N)]
X_BLD, X_BYP, X_BYL = 100, 128, 112
X_SUC, X_DIS, X_RIS, CHX = 410, 590, 640, 700
X_CDR, X_CDS, X_CDSUC = 1000, 1040, 1200
PX_CHP, PX_CDP = 440, 1060
Y_CHWS, Y_CDR, Y_CDWS = 200, 140, 405
Y_CHWR = ROW[-1] + 196
TX = [1080 + j * 215 for j in range(N)]; TY = 185
RX = 1470; RW = 2390 - RX
GOOD = OKC
C_MU, C_CHEM = '#3cbe64', '#aa6ee6'


def has(pt): return pt in G7.PATH


def first(*pts): return next((q for q in pts if has(q)), pts[0])


def v(p, x, y, w, pt, what, h=18, size=8, **kw):
    if has(pt): val(p, x, y, w, pt, what, h=h, size=size, **kw)
    else: lbl(p, x, y, w, '—', size, '#566573', h=h, halign='center')


def rows(p, x, y, w, items, lw=None, rh=21):
    lw = lw or int(w * 0.52)
    for i, it in enumerate(items):
        lbl(p, x + 4, y + i * rh, lw - 4, it[0])
        v(p, x + lw, y + i * rh + 1, w - lw - 4, it[1], it[0], h=rh - 3, size=10, **(it[2] if len(it) > 2 else {}))


def t_(p, x, y, w, pt, what, pre, size=8):
    if has(pt): tag(p, x, y, w, pt, what, pre, size=size)


# ================================================================ equipment sprites from the 3-D renders
def _grey(im):
    a = im.getchannel('A'); g = ImageEnhance.Color(im.convert('RGB')).enhance(0.12); g = ImageEnhance.Brightness(g).enhance(0.62)
    g = g.convert('RGBA'); g.putalpha(a); return g


def _matte(im, bg=(18, 22, 27)):
    """semi-transparent edge pixels pre-blended on the page colour (GIF has 1-bit alpha)"""
    a = np.asarray(im).astype(np.float32); al = a[..., 3:4] / 255.0
    rgb = a[..., :3] * al + np.array(bg, np.float32) * (1 - al)
    out = np.concatenate([rgb, np.where(al > .35, 255, 0)], axis=2).astype(np.uint8)
    return Image.fromarray(out, 'RGBA')


def eq_sprites(raw):
    img = os.path.join(G73.OUT, 'px', 'img')
    def load(n, k=0): return Image.open(os.path.join(raw, f'{n}_{k}.png')).convert('RGBA')
    def meta(n): return json.load(open(os.path.join(raw, f'{n}.json')))
    def reg(name, size, anc): SPR[name] = {'size': list(size), 'anchors': {k: [round(a[0], 1), round(a[1], 1)] for k, a in anc.items()}}
    # chiller
    m = meta('chiller'); s = 260 / m['size'][0]; im = load('chiller'); im = im.resize((260, round(im.height * s)), Image.LANCZOS)
    im.save(f'{img}/v79_chiller_on.png'); _grey(im).save(f'{img}/v79_chiller_off.png')
    reg('v79_chiller', im.size, {k: (a[0] * s, a[1] * s) for k, a in m['anchors'].items()})
    # pump: rendered with suction on the left (CHP); mirrored for CDP
    m = meta('pump'); s = 112 / m['size'][0]; im = load('pump'); im = im.resize((112, round(im.height * s)), Image.LANCZOS)
    im.save(f'{img}/v79_pump_l_on.png'); _grey(im).save(f'{img}/v79_pump_l_off.png')
    reg('v79_pump_l', im.size, {k: (a[0] * s, a[1] * s) for k, a in m['anchors'].items()})
    mr = im.transpose(Image.FLIP_LEFT_RIGHT); mr.save(f'{img}/v79_pump_r_on.png'); _grey(mr).save(f'{img}/v79_pump_r_off.png')
    reg('v79_pump_r', mr.size, {k: (112 - a[0] * s, a[1] * s) for k, a in m['anchors'].items()})
    # 2-cell tower: legs cropped, fans animate
    m = meta('ct'); s = 212 / m['size'][0]; crop = 470
    fr = [load('ct', k).crop((0, 0, m['size'][0], crop)) for k in range(8)]
    fr = [f.resize((212, round(crop * s)), Image.LANCZOS) for f in fr]
    G74.save_gif([_matte(f) for f in fr], f'{img}/v79_ct_on.gif', 110)
    _grey(fr[0]).save(f'{img}/v79_ct_off.png')
    reg('v79_ct', fr[0].size, {k: (a[0] * s, a[1] * s) for k, a in m['anchors'].items()})
    for n in ('v79_chiller_on.png', 'v79_chiller_off.png', 'v79_pump_l_on.png', 'v79_pump_l_off.png', 'v79_pump_r_on.png', 'v79_pump_r_off.png',
              'v79_ct_on.gif', 'v79_ct_off.png'):
        G73.own(n)


def A(name, k, x, y):
    a = SPR[name]['anchors'][k]; return x + a[0], y + a[1]


def eq_img(p, name, x, y, run, what, popup=None, ptitle='', on_ext='.png'):
    w, h = SPR[name]['size']
    G73.ximg_bool(p, x, y, w, h, run, f'{name}_on{on_ext}', f'{name}_off.png', what, popup=popup, ptitle=ptitle)


# ================================================================ valves (base slots animate via V7.4 VTAG, expansion via Gfx_<u>_..._Pos)
def valve(p, cx, cy, orient='h', mode='onoff', led=None, pos=None, what=''):
    if mode == 'man' or (led is None and pos is None):
        G74.bfv(p, cx, cy, orient, 'man' if mode == 'man' or led is None else mode); return
    if led in G74.VTAG:
        G74.bfv(p, cx, cy, orient, mode, led=led if has(led) else None, what=what); return
    base = f'v74_bfv_{mode}_{orient}'; s = SPR[base + '_0']; w, h = s['size']; a = s['anchors']['c']; x, y = cx - a[0], cy - a[1]
    if pos and has(pos):
        o = p.ord(pos)
        p.el.append(f'<Picture layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" image="{G73.own(base + "_0.png")}">\n'
                    f'  <ValueBinding ord={quoteattr(o)}>\n    <INumericToSimple name="image" map="{G74.frame_map(base)}"/>\n'
                    f'  </ValueBinding>\n</Picture>')
        p.map.append((pos, o, f'{what} position (animation)', 'display (image by %)'))
    else:
        ximg(p, x, y, base + '_8.png', w, h)
    if led and has(led):
        lx, ly = (x - 6, y + 6) if orient == 'h' else (x + w - 16, y + h + 1)
        status_led(p, lx, ly, led, what, 'run')


# ================================================================ pipes
def pipes(name):
    L = pipes71.Layer(PW, PH)
    cap = lambda x, y, hz: ((x, y), hz)
    ch = lambda r, k: A('v79_chiller', k, CHX, ROW[r] + 2)
    chp = lambda r, k: A('v79_pump_l', k, PX_CHP, ROW[r] + 92)
    cdp = lambda r, k: A('v79_pump_r', k, PX_CDP, ROW[r] + 92)
    BR = 8
    # ---- CHW
    for r in range(N):
        s_ = chp(r, 'suction'); d_ = chp(r, 'discharge'); yd = ROW[r] + 52
        L.pipe([(X_SUC, s_[1]), (s_[0] + 4, s_[1])], 'chwr', w=BR, arrows_every=60)
        L.pipe([(d_[0], d_[1] + 6), (d_[0], yd), (X_DIS, yd)], 'chwr', w=BR, arrows_every=70)
        ci = ch(r, 'chw_in'); co = ch(r, 'chw_out')
        L.pipe([(X_DIS, ci[1]), (ci[0] + 6, ci[1])], 'chwr', w=BR, arrows_every=60)
        L.pipe([(co[0] + 6, co[1]), (X_RIS, co[1])], 'chws', w=BR, arrows_every=60)
    L.pipe([(X_DIS, ROW[0] + 52 - 24), (X_DIS, ch(N - 1, 'chw_in')[1] + 24)], 'chwr', w=16, flow=False,
           flanges=[cap(X_DIS, ROW[0] + 28, False), cap(X_DIS, ch(N - 1, 'chw_in')[1] + 24, False)])
    L.pipe([(X_RIS, ch(N - 1, 'chw_out')[1] + 20), (X_RIS, Y_CHWS)], 'chws', w=16, flow=False, flanges=[cap(X_RIS, ch(N - 1, 'chw_out')[1] + 20, False)])
    L.pipe([(X_BLD, Y_CHWS), (X_RIS + 24, Y_CHWS)], 'chws', w=16, flow=False, flanges=[cap(X_RIS + 24, Y_CHWS, True)])
    L.pipe([(X_SUC, chp(0, 'suction')[1] - 24), (X_SUC, Y_CHWR)], 'chwr', w=16, flow=False, flanges=[cap(X_SUC, chp(0, 'suction')[1] - 24, False)])
    L.pipe([(X_BLD, Y_CHWR), (X_SUC + 24, Y_CHWR)], 'chwr', w=16, flow=False, flanges=[cap(X_SUC + 24, Y_CHWR, True)])
    L.pipe([(X_BYP, Y_CHWR), (X_BYP, Y_CHWS)], 'chwr', w=10, flow=False)                       # min-flow bypass
    L.pipe([(X_BYP, 760), (X_BYL, 760), (X_BYL, 920), (X_BYP, 920)], 'chwr', w=6, flow=False)   # manual bypass loop
    L.pipe([(300, Y_CHWR), (300, Y_CHWR - 10)], 'chwr', w=8, flow=False)                         # expansion tank
    for a, d in (((X_BLD + 30, Y_CHWS), (-1, 0)), ((X_BLD + 30, Y_CHWR), (1, 0)), ((X_SUC, 1000), (0, -1)), ((X_RIS, 330), (0, -1)), ((X_DIS, 700), (0, 1))):
        L.arrow(a, d, 9)
    # ---- CDW
    for r in range(N):
        s_ = cdp(r, 'suction'); d_ = cdp(r, 'discharge'); yd = ROW[r] + 40
        L.pipe([(X_CDSUC, s_[1]), (s_[0] - 4, s_[1])], 'cdws', w=BR, arrows_every=40)
        L.pipe([(d_[0], d_[1] + 6), (d_[0], yd), (X_CDS, yd)], 'cdws', w=BR, arrows_every=60)
        ci = ch(r, 'cdw_in'); co = ch(r, 'cdw_out')
        L.pipe([(X_CDS, ci[1]), (ci[0] - 6, ci[1])], 'cdws', w=BR, arrows_every=50)
        L.pipe([(co[0] - 6, co[1]), (X_CDR, co[1])], 'cdwr', w=BR, arrows_every=50)
    L.pipe([(X_CDS, ROW[0] + 16), (X_CDS, ch(N - 1, 'cdw_in')[1] + 24)], 'cdws', w=16, flow=False,
           flanges=[cap(X_CDS, ROW[0] + 16, False), cap(X_CDS, ch(N - 1, 'cdw_in')[1] + 24, False)])
    L.pipe([(X_CDR, ch(N - 1, 'cdw_out')[1] + 20), (X_CDR, Y_CDR)], 'cdwr', w=16, flow=False, flanges=[cap(X_CDR, ch(N - 1, 'cdw_out')[1] + 20, False)])
    lastin = A('v79_ct', 'in1', TX[-1], TY)[0]
    L.pipe([(X_CDR, Y_CDR), (lastin + 20, Y_CDR)], 'cdwr', w=16, flow=False, flanges=[cap(lastin + 20, Y_CDR, True)])
    L.pipe([(X_CDSUC, Y_CDWS), (X_CDSUC, cdp(N - 1, 'suction')[1] + 24)], 'cdws', w=16, flow=False, flanges=[cap(X_CDSUC, cdp(N - 1, 'suction')[1] + 24, False)])
    lastout = A('v79_ct', 'out', TX[-1], TY)[0]
    L.pipe([(X_CDSUC, Y_CDWS), (lastout + 20, Y_CDWS)], 'cdws', w=16, flow=False, flanges=[cap(lastout + 20, Y_CDWS, True)])
    for j in range(N):
        for k in ('in1', 'in2'):
            ix, iy = A('v79_ct', k, TX[j], TY); L.pipe([(ix, Y_CDR), (ix, iy)], 'cdwr', w=8, flow=False)
        ox, oy = A('v79_ct', 'out', TX[j], TY); L.pipe([(ox, oy), (ox, Y_CDWS)], 'cdws', w=8, flow=False)
    for a, d in (((X_CDR, 300), (0, -1)), ((1060, Y_CDR), (1, 0)), ((1180, Y_CDWS), (-1, 0)), ((X_CDSUC, 700), (0, 1)), ((X_CDS, 900), (0, -1))):
        L.arrow(a, d, 9)
    L.render(os.path.join(G73.OUT, 'px', 'img', name)); G73.own(name)


# ================================================================ unit names (01-02 base, 03-06 expansion)
def U(kind, n):
    u = f'{kind}{n:02d}'; base = n <= 2
    if kind == 'CH':
        return dict(u=u, base=base, run=first(f'{u}RunProofSelected', f'{u}RunProof'), inst=f'{u}_Installed',
                    chw_led=first(f'{u}ValveOpenProof', f'{u}_ChwIsoFb'), chw_pos=f'Gfx_{u}_ChwIso_Pos',
                    cdw_led=first(f'{u}CdwValveOpenProof', f'{u}_CdwIsoFb'), cdw_pos=f'Gfx_{u}_CdwIso_Pos',
                    fs_e=first(f'{u}CHWFlowProof', f'{u}_ChwFlowSw'), fs_c=first(f'{u}CDWFlowProof', f'{u}_CdwFlowSw'),
                    reset=first(f'{u}ResetFire', f'{u}_ResetFire'), lo=first(f'{u}TimeoutLockout', f'{u}_FailLatch'),
                    fp=f'ALT_V71_FP_{u}' if base else 'ALT_V79_PlantCards')
    if kind in ('CHP', 'CDP'):
        return dict(u=u, base=base, run=f'{u}RunProof', inst=f'{u}_Installed',
                    suc_led=f'{u}_SuctionMVCmd' if base else None, dis_led=first(f'{u}_DischargeMVCmd', f'{u}_MVCmd'),
                    dis_pos=f'Gfx_{u}_MV_Pos', svc=first(f'{u}_ServiceIsolate', f'{u}_Maintenance'),
                    reset=first(f'{u}ResetFire', f'{u}_ResetFire'), fp=f'ALT_V71_FP_{u}' if base else 'ALT_V79_PlantCards')
    return dict(u=u, base=base, run=f'{u}RunProof', inst=f'{u}_Installed',
                c1=first(f'{u}_01RunProof', f'{u}RunProof'), c2=first(f'{u}_02RunProof', f'{u}RunProof'),
                spd=first(f'{u}_01SpeedCmd', f'{u}SpeedCmd'), hz=first(f'{u}_01_FanSpeedHz', f'{u}_FanSpeedHz'),
                kw=first(f'{u}CellsKW', f'{u}_kW'), vin=first(f'{u}ValveOpenProof', f'{u}_ValveFb'), vout=first(f'{u}_OutletMVCmd', f'{u}_ValveFb'),
                vpos=f'Gfx_{u}_Valve_Pos', flt=first(f'{u}Fault', f'{u}FaultAny'), reset=first(f'{u}ResetFire', f'{u}_ResetFire'),
                fp=f'ALT_V71_FP_{u}' if base else 'ALT_V79_PlantCards')


def inst_chip(p, x, y, w, pt, what):
    v(p, x, y, w, pt, what, h=16, size=7, bool_c=('#1f6f43', '#5d6d7e'))


def pcard(p, x, y, d, title, head):
    w = 236; rh = 18; items = [('Status', d['run'], {'bool_c': (RUN, OFF)}), ('Speed %', f"{d['u']}SpeedCmd"), ('Hz', f"{d['u']}_SpeedFeedbackHz"),
                               ('kW', f"{d['u']}_kW"), ('Pump dP', f"{d['u']}_DiffPressure"), ('Valves / svc', d['svc'], {'action': True})]
    p.rect(x, y, w, 22 + rh * len(items) + 4, fill='#161c22', stroke='#4a5866', pen=1.0)
    p.label(x, y, w, 20, f'  {title}  ⊞', 9, True, 'white', head, 'left', popup=f"file:^px/{d['fp']}.px", ptitle=title)
    status_led(p, x + w - 18, y + 3, d['run'], f'{title} running', 'run')
    if has(d['reset']): p.fire(x + w - 82, y + 2, 60, 16, 'RESET', d['reset'], f'Reset {title}')
    inst_chip(p, x + 92, y + 2, 56, d['inst'], f'{title} installed')
    for i, (t, pt, *kw) in enumerate(items):
        lbl(p, x + 6, y + 22 + i * rh, 84, t, 8, '#c9d3dd', h=rh)
        v(p, x + 92, y + 23 + i * rh, w - 98, pt, f'{title} {t}', h=rh - 2, size=8, **(kw[0] if kw else {}))


# ================================================================ page
def plant():
    p = G.Page('ALT_V79_Plant', 'Chiller plant schematic · 6 slots per type (same equipment as 3D)', (PW, PH)); P79.header(p)
    pipes('v79_plant_pipes.png')
    ximg(p, 0, 0, 'v79_plant_pipes.png', PW, PH, bottom=True)
    G7.kpi_strip(p, y=76)
    # ---------------- building column + CHW headers
    p.rect(16, 176, X_BLD - 20, Y_CHWR - 150, fill='#18212b', stroke='#5d6d7e', pen=2.0)
    p.label(16, 186, X_BLD - 20, 22, 'BUILDING', 10, True, TXT, None, 'center')
    p.label(20, 210, X_BLD - 28, 20, 'Floors ⊞', 9, True, '#8fd3ff', '#1f2a36', 'center', popup='file:^px/ALT_V79_Building.px', ptitle='Building / zones')
    p.label(20, 232, X_BLD - 28, 20, '3D ⊞', 9, True, '#8fd3ff', '#1f2a36', 'center', popup='file:^px/ALT_V79_Building3D.px', ptitle='3D Live')
    for i, (t, pt, kw) in enumerate((('Cooling calls', 'AirSide_CoolingCalls', {}), ('CHW requests', 'AirSide_ChwRequests', {}),
                                      ('Units running', 'AirSide_UnitsRunning', {}), ('Reset %', 'PlantResetPct', {}),
                                      ('Fire alarm', 'FireModeActive', {'bool_c': (FLT, GOOD)}), ('CHW ΔP', 'CHWDP', {}), ('ΔP SP', 'CHWDP_Setpoint_ACTIVE', {}),
                                      ('CHWS', 'CHWS', {}), ('CHWR', 'CHWR', {}), ('Load RT', 'CoolingLoad_RT', {}))):
        lbl(p, 20, 262 + i * 44, 76, t, 8, '#c9d3dd')
        v(p, 20, 280 + i * 44, 72, pt, f'Building {t}', h=20, size=9, **kw)
    G73.sprite(p, 'v73_btu_h', 260, Y_CHWS, popup='file:^px/ALT_V71_FP_BTU.px', ptitle='BTU meter'); isa(p, 200, 152, 'BTU')
    t_(p, 232, 150, 96, 'BTU_Power_RT', 'BTU power', 'BTU', 9)
    G74.tt_top(p, 360, Y_CHWS - 3); t_(p, 340, 150, 84, 'CHWS', 'CHWS header temp', 'TT', 9)
    G74.pt_top(p, 450, Y_CHWS - 3); t_(p, 432, 150, 104, 'CHW_SupplyHeaderPressure', 'CHW supply pressure', 'PT', 9)
    hdr_text(p, 520, 178, 'CHWS HEADER', G73.C_CHWS)
    G74.tt_top(p, 180, Y_CHWR - 3); t_(p, 140, Y_CHWR + 14, 84, 'CHWR', 'CHWR header temp', 'TT', 9)
    G73.sprite(p, 'v73_fm_h', 240, Y_CHWR, popup='file:^px/ALT_V71_FP_Flow.px', ptitle='Flow meters'); t_(p, 226, Y_CHWR + 14, 96, 'CHWFlow', 'CHW flow', 'FT', 9)
    G73.sprite(p, 'v73_exptank', 300, Y_CHWR - 8, anchor='bottom'); t_(p, 330, Y_CHWR + 14, 104, 'CHW_ExpansionTankPressure', 'Expansion tank', 'EXP', 9)
    hdr_text(p, 300, Y_CHWR - 40, 'CHWR HEADER', G73.C_CHWR)
    hdr_text(p, X_SUC + 12, Y_CHWR - 60, 'CHP SUCTION HDR', G73.C_CHWR, 130)
    # bypass: isolation / MODULATING / isolation + manual loop
    valve(p, X_BYP, 800, 'v', 'man'); valve(p, X_BYP, 840, 'v', 'mod', led='CHW_BypassValveCmd', what='CHW bypass valve')
    G73.pct_tag(p, X_BYP + 30, 830, 'CHW_BypassValveCmd', 'CHW bypass valve %'); valve(p, X_BYP, 880, 'v', 'man')
    G73.sprite(p, 'v73_gate_vl', X_BYL, 840); isa(p, X_BYP - 13, 744, 'MOD')
    v(p, 104, 926, 60, 'CHW_BypassManualOpen', 'Manual bypass open', h=16, size=7, bool_c=(WARN, GOOD), fmt='MAN BYP')
    panel(p, 150, 222, 450, 192, 'CHILLED WATER')
    rows(p, 150, 246, 225, [('CHWS SP', 'CHW_LeavingTemperatureSetpoint_ACTIVE'), ('CHWS', 'CHWS'), ('CHWR', 'CHWR'), ('Load RT', 'CoolingLoad_RT'),
                            ('Flow', 'CHWFlow'), ('Lead CHP', 'CHP_Lead'), ('Plant ΔT', 'Plant_DeltaT')], lw=96, rh=23)
    rows(p, 375, 246, 225, [('DP', 'CHWDP'), ('DP SP eff', 'CHWDP_Setpoint_ACTIVE'), ('Bypass %', 'CHW_BypassValveCmd'), ('Bypass fb', 'CHW_BypassValveFeedback'),
                            ('Evap flow', 'CHW_EvapFlowTotal'), ('Min-flow SP', 'CHW_BypassMinFlowSP'), ('Exp. tank', 'CHW_ExpansionTankPressure')], lw=96, rh=23)
    # ---------------- plant sequence (between the CHWS riser and the CDWR riser)
    panel(p, 652, 136, 336, 278, 'PLANT SEQUENCE / STAGING')
    rows(p, 652, 160, 336, [('Stage (base CH01-02)', 'PlantStage'), ('Lead set', 'LeadSet', {'bool_c': ('#2471a3', '#7d3c98')}),
                            ('Stage-2 request', 'Stage2Request', {'bool_c': (RUN, OFF)}), ('Mode', 'OperationMode', {'bool_c': ('#8e44ad', '#34495e')}),
                            ('Schedule', 'PlantScheduleMode', {'action': True}), ('Plant load (% of 1 CH)', 'PlantLoadPct'),
                            ('Start next CH at ≥ %', 'Stage_UpLoadPct', {'action': True}), ('Stop lag CH at ≤ %', 'Stage_DownLoadPct', {'action': True}),
                            ('Expansion chillers 03-06', 'CHX_TargetNum'), ('Running chillers', 'CHX_TotalRun'), ('Chillers needing water', 'CHX_ChillersNeedingWater')],
         lw=180, rh=22)
    # ---------------- rows
    for r in range(N):
        n = r + 1; Y = ROW[r]
        c, hp, dp = U('CH', n), U('CHP', n), U('CDP', n)
        # CHP
        pcard(p, 150, Y + 8, hp, f'CHP-{n:02d}', '#1b4f72')
        eq_img(p, 'v79_pump_l', PX_CHP, Y + 92, hp['run'], f'CHP{n:02d} pump (3-D model)', popup=f"file:^px/{hp['fp']}.px", ptitle=f'CHP-{n:02d}')
        sx, sy = A('v79_pump_l', 'suction', PX_CHP, Y + 92); dx_, dy_ = A('v79_pump_l', 'discharge', PX_CHP, Y + 92)
        valve(p, X_SUC + 20, sy, 'h', 'onoff' if hp['base'] else 'man', led=hp['suc_led'], what=f'CHP{n:02d} suction valve')
        if has(f"{hp['u']}_SuctionPressure"): G74.pt_top(p, sx - 16, sy); t_(p, X_SUC + 2, sy + 12, 76, f"{hp['u']}_SuctionPressure", f'CHP{n:02d} suction pressure', 'S')
        valve(p, 540, Y + 52, 'h', 'onoff', led=hp['dis_led'], pos=hp['dis_pos'], what=f'CHP{n:02d} discharge valve')
        G74.pt_top(p, 500, Y + 52); t_(p, 470, Y + 14, 80, f"{hp['u']}_DischargePressure", f'CHP{n:02d} discharge pressure', 'D')
        # chiller
        eq_img(p, 'v79_chiller', CHX, Y + 2, c['run'], f'Chiller {n:02d} (3-D model)', popup=f"file:^px/{c['fp']}.px", ptitle=f'Chiller {n:02d}')
        ci = A('v79_chiller', 'chw_in', CHX, Y + 2); co = A('v79_chiller', 'chw_out', CHX, Y + 2)
        di_ = A('v79_chiller', 'cdw_in', CHX, Y + 2); do_ = A('v79_chiller', 'cdw_out', CHX, Y + 2)
        valve(p, 615, ci[1], 'h', 'onoff', led=c['chw_led'], pos=c['chw_pos'], what=f'CH{n:02d} CHW isolation valve')
        G74.tt_top(p, 680, co[1]); t_(p, 650, Y + 6, 76, f"{c['u']}_ChwSupplyTemp", f'CH{n:02d} CHW leaving', 'LWT')
        G74.tt_bot(p, 682, ci[1]); t_(p, 646, ci[1] + 12, 72, f"{c['u']}_ChwReturnTemp", f'CH{n:02d} CHW entering', 'EWT')
        valve(p, 1020, di_[1], 'h', 'onoff', led=c['cdw_led'], pos=c['cdw_pos'], what=f'CH{n:02d} CDW isolation valve')
        G74.tt_top(p, 974, do_[1]); t_(p, 905, Y + 6, 76, f"{c['u']}_CdwLeavingTemp", f'CH{n:02d} CDW leaving', 'LWT')
        G74.tt_bot(p, 976, di_[1]); t_(p, 940, di_[1] + 12, 72, f"{c['u']}_CdwEnteringTemp", f'CH{n:02d} CDW entering', 'EWT')
        # chiller strip
        yy = Y + 146
        p.label(CHX, yy, 62, 17, f' CH-{n:02d} ⊞', 9, True, 'white', '#4a5866', 'left', popup=f"file:^px/{c['fp']}.px", ptitle=f'Chiller {n:02d}')
        lbl(p, CHX + 64, yy, 30, 'Load', 8, '#c9d3dd', h=17); v(p, CHX + 92, yy, 50, f"{c['u']}LoadPct", f'CH{n:02d} load', h=17)
        lbl(p, CHX + 144, yy, 20, 'kW', 8, '#c9d3dd', h=17); v(p, CHX + 162, yy, 58, f"{c['u']}_kW", f'CH{n:02d} kW', h=17)
        if has(f"{c['u']}_kW_per_RT"): kwrt_val(p, CHX + 222, yy, 60, f"{c['u']}_kW_per_RT", f'CH{n:02d} kW/RT', h=17, size=8)
        yy += 18
        v(p, CHX, yy, 72, c['fs_e'], f'CH{n:02d} evaporator flow switch', h=16, size=7, bool_c=(RUN, '#5d6d7e'), fmt='FS evap %out.value%')
        v(p, CHX + 74, yy, 72, c['fs_c'], f'CH{n:02d} condenser flow switch', h=16, size=7, bool_c=(RUN, '#5d6d7e'), fmt='FS cond %out.value%')
        inst_chip(p, CHX + 148, yy, 62, c['inst'], f'CH{n:02d} installed')
        if has(c['reset']): p.fire(CHX + 212, yy, 70, 16, f'RESET', c['reset'], f'CH{n:02d} reset')
        # CDP
        eq_img(p, 'v79_pump_r', PX_CDP, Y + 92, dp['run'], f'CDP{n:02d} pump (3-D model)', popup=f"file:^px/{dp['fp']}.px", ptitle=f'CDP-{n:02d}')
        sx, sy = A('v79_pump_r', 'suction', PX_CDP, Y + 92)
        valve(p, X_CDSUC - 20, sy, 'h', 'onoff' if dp['base'] else 'man', led=dp['suc_led'], what=f'CDP{n:02d} suction valve')
        if has(f"{dp['u']}_SuctionPressure"): t_(p, X_CDSUC - 72, sy + 12, 70, f"{dp['u']}_SuctionPressure", f'CDP{n:02d} suction pressure', 'S')
        valve(p, 1090, Y + 40, 'h', 'onoff', led=dp['dis_led'], pos=dp['dis_pos'], what=f'CDP{n:02d} discharge valve')
        G74.pt_top(p, 1122, Y + 40); t_(p, 1096, Y + 4, 80, f"{dp['u']}_DischargePressure", f'CDP{n:02d} discharge pressure', 'D')
        pcard(p, 1222, Y + 8, dp, f'CDP-{n:02d}', '#7d6608')
    hdr_text(p, X_DIS - 190, 412, 'CHP DISCH. HDR ▶', G73.C_CHWR, 124)
    hdr_text(p, X_RIS - 96, 412, 'CHWS RISER', G73.C_CHWS, 90)
    hdr_text(p, X_CDR - 96, Y_CDWS + 4, 'CDWR RISER', G73.C_CDWR, 90)
    hdr_text(p, X_CDS + 6, ROW[-1] + 168, 'CDP DISCH. HDR ▲', G73.C_CDWS, 132)
    hdr_text(p, X_CDSUC + 6, Y_CDWS + 4, 'CDP SUCTION HDR', G73.C_CDWS, 130)
    G73.sprite(p, 'v73_fm_vl', X_CDSUC, Y_CDWS + 60, popup='file:^px/ALT_V71_FP_Flow.px', ptitle='Flow meters')
    # ---------------- roof: towers
    p.rect(1064, 128, 1326, 290, fill=None, stroke='#37474f', pen=1.0)
    lbl(p, 2150, 130, 236, 'ROOF · COOLING TOWERS (2 cells each)', 8, '#8fa3b5', True, h=14, halign='right')
    hdr_text(p, 1240, Y_CDR - 22, 'CDWR HEADER', G73.C_CDWR); hdr_text(p, 1500, Y_CDWS + 4, 'CDWS HEADER', G73.C_CDWS)
    G74.tt_bot(p, 1120, Y_CDR + 3); t_(p, 1090, Y_CDR + 10, 80, 'CDR', 'CDW return header temp', 'TT')
    G74.tt_top(p, 1140, Y_CDWS - 3); t_(p, 1080, Y_CDWS - 30, 84, 'CDS', 'CDW supply header temp', 'TT')
    t_(p, X_CDSUC + 22, Y_CDWS + 50, 100, 'CDW_Flow', 'CDW header flow', 'FT')
    for j in range(N):
        t = U('CT', j + 1); x0 = TX[j]
        eq_img(p, 'v79_ct', x0, TY, t['run'] if has(t['run']) else t['c1'], f"CT{j + 1:02d} (3-D model, fans animate)",
               popup=f"file:^px/{t['fp']}.px", ptitle=f'CT-{j + 1:02d}', on_ext='.gif')
        p.label(x0, TY - 18, 64, 16, f' CT-{j + 1:02d} ⊞', 8, True, 'white', '#935116', 'left', popup=f"file:^px/{t['fp']}.px", ptitle=f'CT-{j + 1:02d}')
        status_led(p, x0 + 68, TY - 16, t['c1'], f'CT{j + 1:02d} cell 1 running', 'run'); status_led(p, x0 + 84, TY - 16, t['c2'], f'CT{j + 1:02d} cell 2 running', 'run')
        ix, iy = A('v79_ct', 'in1', x0, TY)
        valve(p, ix, Y_CDR + 26, 'v', 'onoff', led=t['vin'], pos=t['vpos'], what=f'CT{j + 1:02d} inlet valve')
        ox, oy = A('v79_ct', 'out', x0, TY)
        valve(p, ox + 34, Y_CDWS, 'h', 'onoff', led=t['vout'], pos=t['vpos'], what=f'CT{j + 1:02d} outlet valve')
    # ---------------- right column
    panel(p, RX, 430, RW, 190, 'COOLING TOWERS', link='file:^px/ALT_V73_CTPlant.px')
    cols = (('Tower', 70), ('Inst', 60), ('Cell 1', 46), ('Cell 2', 46), ('Fan %', 66), ('Hz', 60), ('kW', 66), ('In °C', 70), ('Out °C', 70),
            ('Basin %', 66), ('Valve', 56), ('Fault', 70), ('', 70))
    xs = [RX + 6]; [xs.append(xs[-1] + w) for _, w in cols]
    for (t, w), x in zip(cols, xs): lbl(p, x, 452, w, t, 8, '#8fa3b5', True, halign='center')
    for j in range(N):
        t = U('CT', j + 1); u = t['u']; yy = 470 + j * 24; x = xs
        p.label(x[0], yy, 66, 20, f' CT-{j + 1:02d} ⊞', 8, True, 'white', '#5b3a1a', 'left', popup=f"file:^px/{t['fp']}.px", ptitle=f'CT-{j + 1:02d}')
        inst_chip(p, x[1] + 2, yy + 2, 56, t['inst'], f'{u} installed')
        status_led(p, x[2] + 16, yy + 3, t['c1'], f'{u} cell 1', 'run'); status_led(p, x[3] + 16, yy + 3, t['c2'], f'{u} cell 2', 'run')
        for k, (pt, wh) in enumerate(((t['spd'], 'fan speed'), (t['hz'], 'Hz'), (t['kw'], 'kW'), (f'{u}_InletTemp', 'water in'), (f'{u}_OutletTemp', 'water out'),
                                      (f'{u}_BasinLevel', 'basin level'))):
            v(p, x[4 + k] + 2, yy + 1, cols[4 + k][1] - 4, pt, f'{u} {wh}')
        v(p, x[10] + 2, yy + 1, 52, t['vin'], f'{u} valve', bool_c=(RUN, '#5d6d7e'))
        v(p, x[11] + 2, yy + 1, 66, t['flt'], f'{u} fault', bool_c=(FLT, GOOD))
        if has(t['reset']): p.fire(x[12] + 2, yy + 1, 64, 18, 'RESET', t['reset'], f'Reset {u}')
    panel(p, RX, 630, RW, 190, 'CHILLERS', link='file:^px/ALT_V71_Chillers.px')
    cols = (('Chiller', 70), ('Inst', 60), ('Run', 40), ('Load %', 62), ('kW', 66), ('kW/RT', 62), ('RT', 62), ('CHW flow', 70), ('LWT', 56), ('EWT', 56),
            ('CDW out', 60), ('CDW in', 60), ('Lift', 52), ('Remote', 50), ('', 70))
    xs = [RX + 6]; [xs.append(xs[-1] + w) for _, w in cols]
    for (t, w), x in zip(cols, xs): lbl(p, x, 652, w, t, 8, '#8fa3b5', True, halign='center')
    for i in range(N):
        c = U('CH', i + 1); u = c['u']; yy = 670 + i * 24; x = xs
        p.label(x[0], yy, 66, 20, f' CH-{i + 1:02d} ⊞', 8, True, 'white', '#4a5866', 'left', popup=f"file:^px/{c['fp']}.px", ptitle=f'Chiller {i + 1:02d}')
        inst_chip(p, x[1] + 2, yy + 2, 56, c['inst'], f'{u} installed'); status_led(p, x[2] + 13, yy + 3, c['run'], f'{u} running', 'run')
        for k, (pt, wh) in enumerate(((f'{u}LoadPct', 'load'), (f'{u}_kW', 'kW'))):
            v(p, x[3 + k] + 2, yy + 1, cols[3 + k][1] - 4, pt, f'{u} {wh}')
        if has(f'{u}_kW_per_RT'): kwrt_val(p, x[5] + 2, yy + 1, 58, f'{u}_kW_per_RT', f'{u} kW/RT', h=18, size=8)
        for k, (pt, wh) in enumerate(((f'{u}_RT', 'RT'), (f'{u}_ChwFlow', 'CHW flow'), (f'{u}_ChwSupplyTemp', 'LWT'), (f'{u}_ChwReturnTemp', 'EWT'),
                                      (f'{u}_CdwLeavingTemp', 'CDW leaving'), (f'{u}_CdwEnteringTemp', 'CDW entering'), (f'{u}_Lift', 'lift'))):
            v(p, x[6 + k] + 2, yy + 1, cols[6 + k][1] - 4, pt, f'{u} {wh}')
        status_led(p, x[13] + 18, yy + 3, f'{u}InAuto', f'{u} remote', 'run')
        if has(c['reset']): p.fire(x[14] + 2, yy + 1, 64, 18, 'RESET', c['reset'], f'Reset {u}')
    hw = RW // 2 - 5
    panel(p, RX, 830, hw, 250, 'EXPANSION SUPERVISOR (slots 03-06)')
    rows(p, RX, 854, hw, [('Expansion in use', 'CHX_Enable', {'bool_c': (RUN, OFF)}), ('Chillers wanted 03-06', 'CHX_TargetNum'),
                          ('Added for load', 'CHX_StageAdd'), ('Average load %', 'CHX_AverageLoad'), ('Base asked (01-02)', 'CHX_BaseAsked'),
                          ('Chillers needing water', 'CHX_ChillersNeedingWater'), ('Running chillers', 'CHX_TotalRun'),
                          ('Add chiller above %', 'CHX_UpLoadPct', {'action': True}), ('Remove below %', 'CHX_DownLoadPct', {'action': True})], lw=230, rh=24)
    X2 = RX + hw + 10
    panel(p, X2, 830, hw, 250, 'CONDENSER WATER')
    rows(p, X2, 854, hw // 2, [('CDS SP', 'CDS_Setpoint_ACTIVE'), ('CDS', 'CDS'), ('CDR', 'CDR'), ('CDW flow', 'CDW_Flow'), ('Make-up', 'CT_MakeupFlow'),
                               ('Conductivity', 'CT_Conductivity'), ('Lead CDP', 'CDP_Lead'), ('Lead CT', 'CT_Lead'), ('Towers', 'CT_Mode2Towers', {'bool_c': ('#935116', '#2c3e50')})],
         lw=96, rh=24)
    cx = X2 + hw // 2 + 6
    for i, (pt, t, cc, oc) in enumerate((('CT_ChemDosingPumpCmd', 'DOSING', C_CHEM, OFF), ('CT_ChemTankLowLevel', 'CHEM LOW', WARN, GOOD),
                                         ('CT_BiocideAPumpCmd', 'BIO A', C_CHEM, OFF), ('CT_BiocideBPumpCmd', 'BIO B', C_CHEM, OFF),
                                         ('CT_BleedValveCmd', 'BLEED', RUN, OFF), ('CT_BleedLockout', 'BLEED LOCK', WARN, OFF),
                                         ('CT01_MakeupValveCmd', 'CT01 FILL', RUN, OFF), ('CT02_MakeupValveCmd', 'CT02 FILL', RUN, OFF),
                                         ('CT_ConductivityHighAlarm', 'COND. HIGH', FLT, GOOD))):
        v(p, cx, 856 + i * 24, hw // 2 - 14, pt, t, h=20, size=8, bool_c=(cc, oc), fmt=t)
    panel(p, RX, 1090, hw, 196, 'OUTDOOR AIR', link='file:^px/ALT_V71_FP_OA.px')
    G73.sprite(p, 'v73_oa', RX + 26, 1136, anchor='top')
    G73.oa_rows(p, RX + 60, 1114, hw - 64, rh=27, lw=200)
    panel(p, X2, 1090, hw, 196, 'LEGEND')
    items = (('CHW supply', '#1665d6'), ('CHW return', '#5ec4f2'), ('CDW supply', '#f2c416'), ('CDW return', '#f07a12'))
    for i, (t, cc) in enumerate(items):
        yy = 1116 + i * 22; p.rect(X2 + 10, yy + 6, 30, 9, fill=cc, stroke=cc, pen=1.0); lbl(p, X2 + 46, yy, 140, t, 8, TXT)
    for i, (nm, t) in enumerate((('v73_bfv_onoff_h', 'on/off MV (LED = open)'), ('v73_bfv_mod_h', 'modulating MV (%)'), ('v73_bfv_man_h', 'manual (handwheel)'))):
        G73.sprite(p, nm, X2 + 216, 1128 + i * 44); lbl(p, X2 + 244, 1118 + i * 44, 210, t, 8, TXT)
    lbl(p, X2 + 10, 1214, hw - 20, 'Equipment pictures = the 3-D twin models. Colour = running, grey = stopped, tower fans turn. '
        'Slots 03-06 = expansion (set <slot>_Installed or the equipment register).', 8, TXT, h=60)
    panel(p, RX, 1296, hw, 236, 'EQUIPMENT POOLS / SET')
    for i, eq in enumerate(('CHP', 'CDP', 'CT')):
        yy = 1322 + i * 34
        lbl(p, RX + 6, yy, 40, eq, 10, TXT, True)
        lbl(p, RX + 44, yy, 36, 'Lead'); v(p, RX + 78, yy + 1, 60, f'{eq}_Lead', f'{eq} lead', h=20, size=9)
        v(p, RX + 142, yy + 1, 70, f'{eq}_RotationMode_Runtime', f'{eq} rotation mode', h=20, size=9, action=True)
        v(p, RX + 216, yy + 1, 112, f'{eq}_PoolDegradedAlarm', f'{eq} standby lost', h=20, size=8, bool_c=(WARN, GOOD), fmt='Standby: %out.value%')
        v(p, RX + 332, yy + 1, 112, f'{eq}_PoolUnavailableAlarm', f'{eq} none available', h=20, size=8, bool_c=(FLT, GOOD), fmt='No unit: %out.value%')
    lbl(p, RX + 6, 1428, 120, 'Lead chiller (set)'); v(p, RX + 126, 1429, 96, 'LeadCH01', 'Lead chiller select', h=20, size=9, action=True)
    v(p, RX + 226, 1429, 104, 'Set_LinkPools', 'Pools linked to set', h=20, size=8, action=True)
    v(p, RX + 334, 1429, 110, 'Stage2BlockedByPoolAlarm', 'Stage 2 blocked', h=20, size=8, bool_c=(WARN, GOOD), fmt='S2 blocked: %out.value%')
    panel(p, X2, 1296, hw, 236, 'CONTROL')
    rows(p, X2, 1320, hw // 2, [('Plant enable', 'PlantEnable', {'bool_c': (RUN, OFF), 'action': True}), ('Schedule', 'PlantScheduleMode', {'action': True}),
                                ('Demand', 'PlantDemandMode', {'action': True}), ('Pump valves', 'Pump_StandbyValvesOpen', {'action': True}),
                                ('Towers (SOO)', 'CT_RunAllAvailable', {'action': True}), ('Load source', 'CoolingLoadSource')], lw=96, rh=25)
    rows(p, X2 + hw // 2, 1320, hw // 2, [('Plant main kW', 'PM_Main_kW'), ('kWh today', 'Plant_kWh_Today'), ('Cost today', 'Energy_Cost_THB_Today'),
                                         ('CHWS valid', 'CHWS_SensorInvalidAlarm', {'bool_c': (FLT, GOOD)}), ('Rotation daily', 'RotationMode_Daily', {'action': True}),
                                         ('Rotation weekly', 'RotationMode_Weekly', {'action': True})], lw=104, rh=25)
    # ---------------- bottom band
    yb = Y_CHWR + 34
    panel(p, 10, yb, 1440, PH - yb - 10, 'PLANT ALARMS', link='file:^px/ALT_CP_AlarmsHistory.px')
    al = [('All chillers unavailable', 'AllChillersUnavailableAlarm'), ('CHW flow low', 'CHW_FlowLowAlarm'), ('CDW flow low', 'CDW_FlowLowAlarm'),
          ('CHWST not tracking', 'CHWST_NotTrackingAlarm'), ('Low delta-T', 'LowDeltaTAlarm'), ('Manual bypass open', 'CHW_BypassManualOpenAlarm'),
          ('CHW fill lock-out (leak)', 'CHW_FillLockoutAlarm'), ('CT01 basin LOW-LOW', 'CT01BasinLowLowLevelAlarm'), ('CT02 basin LOW-LOW', 'CT02BasinLowLowLevelAlarm'),
          ('CT start inhibited', 'CT_StartInhibitedAlarm'), ('Conductivity high', 'CT_ConductivityHighAlarm'), ('Make-up pressure low', 'MU_SupplyLowAlarm')]
    al += [(f'CH{n:02d} start failure', f'CH{n:02d}_StartFailAlarm') for n in range(3, 7)]
    al += [(f'CH{n:02d} no CHW flow', f'CH{n:02d}_ChwFailAlarm') for n in range(3, 7)]
    al = [a for a in al if has(a[1])]
    per = max(1, -(-len(al) // 4))
    for i, (t, pt) in enumerate(al):
        cx_, cy_ = 20 + (i // per) * 356, yb + 26 + (i % per) * 22
        status_led(p, cx_, cy_ + 3, pt, t, 'alarm'); lbl(p, cx_ + 20, cy_, 330, t, 9, TXT)
    G73.gauge_panel(p, RX, yb, RW, PH - yb - 10)
    return p


if __name__ == '__main__':
    bog, G7.KITDIR, OUT, s73, s74, raw = sys.argv[1:7]
    G73.OUT = G71.OUT = OUT
    G7.PATH.update(G7.load_paths(bog))
    G.FOLDER = {n: q.rsplit('/', 1)[0].replace('/ChillerPlant/', '').replace('/ChillerPlant', '') for n, q in G7.PATH.items()}
    G.STATION_NAME = G71.STATION = G73.STATION = G74.STATION = 'ALT_CP_Ref_V7_9'
    os.makedirs(os.path.join(OUT, 'px', 'img'), exist_ok=True)
    G74.build_sprites(s73, s74)
    eq_sprites(raw)
    p = plant()
    x = p.xml()
    import xml.etree.ElementTree as ET; ET.fromstring(x.encode('utf-8'))
    open(os.path.join(OUT, 'px', p.name + '.px'), 'w', encoding='utf-8').write(x)
    bad = sorted({pt for pt, o, w, m in p.map if pt != '(BQL)' and pt not in G7.PATH})
    print(p.name, len(p.el), 'elements', len(p.map), 'bindings; missing', bad[:40])
    json.dump(sorted(set(G71.IMG)), open(os.path.join(OUT, 'img_used.json'), 'w'))
