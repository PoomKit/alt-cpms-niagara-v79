"""ALT_CP_Ref_V7_4 Px graphics = V7.3 pages (gen_px73, imported) + V7.4 changes:
  - instruments: new TT (RTD + DIN head), PT (transmitter + isolation valve), ONICON-form insertion magmeters / System-10 BTU,
    ME96SS-form panel power meter, ACH580-form drives, OA T/RH in a radiation shield (original renders, no logos)
  - butterfly valves: 9-position actuator frames bound to the valve position; amber 'motor running' indicator while travelling
  - plant schematic: animated flow chevrons in the true flow direction, shown only where water is flowing
  - units bar / gpm in the page texts; faceplates redesigned around the equipment render
usage: gen_px74.py bog kitdir outdir regdir sprites73dir sprites74dir"""
import sys, os, re, csv, json, shutil, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xml.sax.saxutils import quoteattr
import numpy as np
from PIL import Image, ImageDraw
import gen_px73 as G73
from gen_px73 import G, G7, G71, SPR, own, ximg_bool, val, lbl, panel, rows, status_led, BG, PANEL, EDGE, LBL, VAL, TXT, RUN, OFF, FLT, WARN, OKC
from gen_px71 import ximg, hot, tag, isa

STATION = 'ALT_CP_Ref_V7_4'
G73.STATION = STATION


# ================================================================ header
def header(self):
    W, H = self.size
    self.rect(0, 0, W, H, fill=BG, stroke=BG, pen=1.0)
    if self.name.startswith(('ALT_V71_FP_', 'ALT_V73_FP_', 'ALT_V74_FP_')):
        self.label(0, 0, W, 34, f'  {self.title}', 14, True, 'white', '#0b0e11')
        return
    self.label(0, 0, W, 40, f'  ALT Reference V7.4 — {self.title}', 18, True, 'white', '#0b0e11')
    self.label(W - 470, 8, 460, 24, 'REFERENCE SIMULATION – NOT PROJECT APPROVED', 10, True, '#263238', '#ffca28', 'center')
    n = len(G73.PAGES); bw = (W - 8) / n
    for i, (name, title) in enumerate(G73.PAGES):
        cur = name == self.name
        self.label(4 + i * bw, 44, bw - 3, 26, title, 8.5, True, 'white' if cur else '#cfd8dc',
                   '#1e88e5' if cur else ('#233a33' if name in G73.AIRPAGES else '#2c3440'), 'center',
                   popup=None if cur else f'file:^px/{name}.px', ptitle=title)


G.Page.header = header
G73.header = header

# ================================================================ sprites: aliases + new instruments
ALIAS = {'v73_fm_h': 'v74_fm_h', 'v73_fm_v': 'v74_fm_v', 'v73_fm_vl': 'v74_fm_vl', 'v73_btu_h': 'v74_btu_h', 'v73_oa': 'v74_oa',
         'v73_vsd_on': 'v74_vsd_on', 'v73_vsd_off': 'v74_vsd_off',
         'v73_bfv_onoff_h': 'v74_bfv_onoff_h_8', 'v73_bfv_mod_h': 'v74_bfv_mod_h_4', 'v73_bfv_man_h': 'v74_bfv_man_h',
         'v73_bfv_onoff_v': 'v74_bfv_onoff_v_8', 'v73_bfv_mod_v': 'v74_bfv_mod_v_4', 'v73_bfv_man_v': 'v74_bfv_man_v'}
_sprite73 = G73.sprite


def sprite(p, name, ax, ay, anchor='c', ext='.png', popup=None, ptitle=''):
    name = ALIAS.get(name, name)
    if anchor not in SPR[name]['anchors']: anchor = 'c'
    return _sprite73(p, name, ax, ay, anchor, ext, popup, ptitle)


G73.sprite = sprite


def tt_top(p, cx, cy): sprite(p, 'v74_tt_top', cx, cy + 3)
def tt_bot(p, cx, cy): sprite(p, 'v74_tt_bot', cx, cy - 3)
def pt_top(p, cx, cy): sprite(p, 'v74_pt_top', cx, cy + 2)


_pic73 = G73.pic


def pic(p, x, y, rel, w=None, h=None):
    if rel == 'Sensors/sensor_pipe_welltemp2_ver_left.png': return sprite(p, 'v74_tt_left', x + 35, y + 13.5)
    if rel == 'Sensors/sensor_pipe_welltemp2_ver_right.png': return sprite(p, 'v74_tt_right', x - 8, y + 13.5)
    return _pic73(p, x, y, rel, w, h)


for mod in (G73, G71):
    mod.tt_top, mod.tt_bot, mod.pt_top = tt_top, tt_bot, pt_top
G73.pic = pic

# ---------------------------------------------------------------- 3-D pages: the fixed legend row is reserved for the card placer
_page3d73, _legend3d73 = G73.page3d, G73.legend3d
_LASTP = {}


def page3d(name, title, view):
    p, A, P = _page3d73(name, title, view)
    _LASTP['P'] = P
    return p, A, P


def legend3d(p, x, y):
    _legend3d73(p, x, y)
    if 'P' in _LASTP: _LASTP['P'].block(x, y - 136, 820, 22)          # placer works in render coordinates (page y - 136)


G73.page3d, G73.legend3d = page3d, legend3d


# ---------------------------------------------------------------- animated butterfly valves
VTAG = {'CH01ValveOpenProof': 'CH01_ChwIso', 'CH02ValveOpenProof': 'CH02_ChwIso', 'CH01CdwValveOpenProof': 'CH01_CdwIso',
        'CH02CdwValveOpenProof': 'CH02_CdwIso', 'CH01_ChwFCVCmd': 'CH01_ChwFCV', 'CH02_ChwFCVCmd': 'CH02_ChwFCV',
        'CH01_CdwHPVCmd': 'CH01_CdwHPV', 'CH02_CdwHPVCmd': 'CH02_CdwHPV', 'CT01ValveOpenProof': 'CT01_InletMV', 'CT02ValveOpenProof': 'CT02_InletMV',
        'CT01_OutletMVCmd': 'CT01_OutletMV', 'CT02_OutletMVCmd': 'CT02_OutletMV', 'CHW_BypassValveCmd': 'CHW_BypassMV'}
for u in ('CHP01', 'CHP02', 'CDP01', 'CDP02'):
    for sd in ('Suction', 'Discharge'): VTAG[f'{u}_{sd}MVCmd'] = f'{u}_{sd}MV'
VALVE_USED = []


def frame_map(base):
    parts = []
    for k in range(9):
        lo = '-inf' if k == 0 else f'{k * 12.5 - 6.25:g}'
        hi = '+inf' if k == 8 else f'{k * 12.5 + 6.25:g}'
        parts.append(f'{lo}:{hi}={own(f"{base}_{k}.png")}')
    return 'gx:Image ' + ';'.join(parts) + f';default={own(base + "_0.png")};'


def bfv(p, cx, cy, orient='h', mode='onoff', led=None, pct=None, what='', pct_at=None, led_at=None):
    """butterfly valve: actuator frame follows the valve position (Gfx_<tag>_Pos), amber indicator while it travels"""
    if mode == 'man':
        x, y, w, h = sprite(p, f'v74_bfv_man_{orient}', cx, cy)
    else:
        base = f'v74_bfv_{mode}_{orient}'
        s = SPR[base + '_0']; w, h = s['size']; a = s['anchors']['c']
        x, y = cx - a[0], cy - a[1]
        tg = VTAG.get(pct) or VTAG.get(led)
        if tg:
            o = p.ord(f'Gfx_{tg}_Pos')
            p.el.append(f'<Picture layout="{x:.1f},{y:.1f},{w:.1f},{h:.1f}" image="{own(base + "_0.png")}">\n'
                        f'  <ValueBinding ord={quoteattr(o)}>\n    <INumericToSimple name="image" map="{frame_map(base)}"/>\n'
                        f'  </ValueBinding>\n</Picture>')
            p.map.append((f'Gfx_{tg}_Pos', o, f'{what or tg} actuator position (animation)', 'display (image by %)'))
            t = s['anchors']['top']
            ximg_bool(p, x + t[0] - 7, y + t[1] - 7, 14, 14, f'Gfx_{tg}_Moving', 'v74_moving.gif', 'v74_blank.png',
                      f'{what or tg} actuator running')
            VALVE_USED.append(tg)
        else:
            ximg(p, x, y, base + '_8.png', w, h)
    if led:
        lx, ly = led_at or ((x - 6, y + 6) if orient == 'h' else (x + w - 16, y + h + 1))
        status_led(p, lx, ly, led, what or f'{led} open', 'run')
    if pct:
        px_, py_ = pct_at or ((x + w + 2, y + 4) if orient == 'h' else (x + w + 2, y + h / 2 - 8))
        G73.pct_tag(p, px_, py_, pct, what or pct)


G73.bfv = bfv


# ================================================================ sprite build: v73 + v74, valve position bar, indicator gif
def build_sprites(s73, s74):
    G73.build_sprites(s73)
    SPR.update(json.load(open(os.path.join(s74, 'sprites74.json'))))
    img = os.path.join(G73.OUT, 'px', 'img')
    for f in os.listdir(s74):
        if f.endswith(('.png', '.gif')): shutil.copy(os.path.join(s74, f), os.path.join(img, f))
    # valve frames: add a position bar (0..100 %) beside the actuator so travel reads at 2-D scale
    for mode in ('onoff', 'mod'):
        for orient in ('h', 'v'):
            for k in range(9):
                fn = os.path.join(img, f'v74_bfv_{mode}_{orient}_{k}.png')
                im = Image.open(fn).convert('RGBA'); d = ImageDraw.Draw(im); w, h = im.size
                an = SPR[f'v74_bfv_{mode}_{orient}_{k}']['anchors']
                col = (125, 206, 160, 255) if mode == 'mod' else (255, 202, 40, 255)
                if orient == 'h':
                    x0, y0, y1 = w - 5, int(an['top'][1]) + 2, int(an['c'][1]) - 12
                    d.rectangle([x0, y0, x0 + 3, y1], fill=(11, 14, 17, 255), outline=(90, 100, 110, 255))
                    f = round((y1 - y0 - 2) * k / 8)
                    if f: d.rectangle([x0 + 1, y1 - 1 - f, x0 + 2, y1 - 1], fill=col)
                else:
                    y0, x0, x1 = h - 5, int(an['c'][0]) + 12, int(an['top'][0]) - 2
                    d.rectangle([x0, y0, x1, y0 + 3], fill=(11, 14, 17, 255), outline=(90, 100, 110, 255))
                    f = round((x1 - x0 - 2) * k / 8)
                    if f: d.rectangle([x0 + 1, y0 + 1, x0 + f, y0 + 2], fill=col)
                im.save(fn)
    # amber 'actuator running' indicator: rotating arc, 8 frames
    frames = []
    for k in range(8):
        im = Image.new('RGBA', (14, 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse([1, 1, 12, 12], outline=(60, 45, 10, 255), width=2)
        d.arc([1, 1, 12, 12], k * 45, k * 45 + 200, fill=(255, 176, 0, 255), width=2)
        d.ellipse([5, 5, 8, 8], fill=(255, 210, 90, 255))
        frames.append(im)
    save_gif(frames, os.path.join(img, 'v74_moving.gif'), 90)
    Image.new('RGBA', (4, 4), (0, 0, 0, 0)).save(os.path.join(img, 'v74_blank.png'))
    # drive image used by every VSD faceplate (keep the V7.3 file name / aspect 300 x 520)
    src = Image.open(os.path.join(s74, 'v74_fp_vsd_on.png')).convert('RGBA')
    sc_ = min(300 / src.size[0], 520 / src.size[1]); src = src.resize((int(src.size[0] * sc_), int(src.size[1] * sc_)), Image.LANCZOS)
    canvas = Image.new('RGBA', (300, 520), (0, 0, 0, 0)); canvas.alpha_composite(src, ((300 - src.size[0]) // 2, (520 - src.size[1]) // 2))
    canvas.save(os.path.join(img, 'vsd_drive.png'))


def save_gif(frames, path, dur):
    """RGBA frames -> GIF with binary transparency (index 255), one shared palette"""
    stack = Image.new('RGB', (frames[0].size[0], frames[0].size[1] * len(frames)))
    for i, f in enumerate(frames): stack.paste(f.convert('RGB'), (0, i * f.size[1]))
    pal = stack.quantize(255, method=Image.Quantize.MEDIANCUT)
    out = []
    for f in frames:
        q = f.convert('RGB').quantize(palette=pal, dither=Image.Dither.NONE)
        arr = np.asarray(q).copy(); arr[np.asarray(f)[..., 3] < 128] = 255
        q = Image.fromarray(arr, 'P'); q.putpalette(pal.getpalette()[:765] + [0, 0, 0]); out.append(q)
    out[0].save(path, save_all=True, append_images=out[1:], duration=dur, loop=0, transparency=255, disposal=2)


# ================================================================ animated pipe flow (plant schematic)
TINT = {'chws': (205, 228, 255), 'chwr': (225, 246, 255), 'cdws': (255, 250, 215), 'cdwr': (255, 232, 205),
        'mu': (215, 255, 225), 'chem': (240, 225, 255), 'drain': (235, 235, 235)}


def flow_segments():
    """(condition point, service, pipe width, polyline in the FLOW direction).  Geometry = gen_px73.plant_pipes."""
    g = G73
    CHP, CH, CDP = g.CHP, g.CH, g.CDP
    S = []
    add = lambda cond, svc, w, *pts: S.append((cond, svc, w, list(pts)))
    HW = g.HW
    ev = lambda n, k: (CH[n][0] + 4, CH[n][1] + k)
    cd = lambda n, k: (CH[n][0] + 198, CH[n][1] + k)
    y1o, y2o, y1i, y2i = CH['01'][1] + 45, CH['02'][1] + 45, CH['01'][1] + 55, CH['02'][1] + 55
    # ---- CHW
    add('Gfx_CH02Evap_Fwd', 'chws', HW, (g.X_RIS, y2o), (g.X_RIS, y1o))                         # riser (CH02 part)
    add('Gfx_EvapTotal_Fwd', 'chws', HW, (g.X_RIS, y1o), (g.X_RIS, g.Y_CHWS))                    # riser to header
    add('Gfx_EvapTotal_Fwd', 'chws', HW, (g.X_RIS, g.Y_CHWS), (g.X_BYP, g.Y_CHWS))               # CHWS header -> bypass tee
    add('Gfx_ChwMain_Fwd', 'chws', HW, (g.X_BYP, g.Y_CHWS), (g.X_BLD, g.Y_CHWS))                  # -> building
    add('Gfx_ChwMain_Fwd', 'chwr', HW, (g.X_BLD, g.Y_CHWR), (g.X_BYP, g.Y_CHWR))                  # building return
    add('Gfx_EvapTotal_Fwd', 'chwr', HW, (g.X_BYP, g.Y_CHWR), (g.X_SUC, g.Y_CHWR))               # return + bypass
    add('Gfx_Bypass_Fwd', 'chwr', 10, (g.X_BYP, g.Y_CHWS), (g.X_BYP, 560))                        # bypass (down)
    add('Gfx_BypMod_Fwd', 'chwr', 10, (g.X_BYP, 560), (g.X_BYP, 720))                             # through the MOD valve
    add('Gfx_ManBypass_Fwd', 'chwr', 6, (g.X_BYP, 560), (g.X_BYL, 560), (g.X_BYL, 720), (g.X_BYP, 720))
    add('Gfx_Bypass_Fwd', 'chwr', 10, (g.X_BYP, 720), (g.X_BYP, g.Y_CHWR))
    add('Gfx_EvapTotal_Fwd', 'chwr', HW, (g.X_SUC, g.Y_CHWR), (g.X_SUC, CHP['02'][1] + 44.5))     # suction header up
    add('Gfx_CHP01_Fwd', 'chwr', HW, (g.X_SUC, CHP['02'][1] + 44.5), (g.X_SUC, CHP['01'][1] + 44.5))
    for n, (x, y) in CHP.items():
        add(f'Gfx_CHP{n}_Fwd', 'chwr', 10, (g.X_SUC, y + 44.5), (x + 12, y + 44.5))
        add(f'Gfx_CHP{n}_Fwd', 'chwr', 10, (x + 24, y + 12), (x + 24, y - 40), (g.X_DIS, y - 40))
    taps = [CHP['01'][1] - 40, y1i, CHP['02'][1] - 40, y2i]                                       # X_DIS header (top -> bottom)
    for k in range(3):
        add(f'Gfx_ChpDis_S{k}_Fwd', 'chwr', HW, (g.X_DIS, taps[k]), (g.X_DIS, taps[k + 1]))
        add(f'Gfx_ChpDis_S{k}_Rev', 'chwr', HW, (g.X_DIS, taps[k + 1]), (g.X_DIS, taps[k]))
    for n in CH:
        add(f'Gfx_CH{n}Evap_Fwd', 'chwr', 10, (g.X_DIS, CH[n][1] + 55), ev(n, 55))
        add(f'Gfx_CH{n}Evap_Fwd', 'chws', 10, ev(n, 45), (g.X_RIS, CH[n][1] + 45))
    # ---- CDW
    for n in CH:
        add(f'Gfx_CH{n}Cond_Fwd', 'cdwr', 10, cd(n, 45), (g.X_CDR, CH[n][1] + 45))
        add(f'Gfx_CH{n}Cond_Fwd', 'cdws', 10, (g.X_CDS, CH[n][1] + 55), cd(n, 55))
    add('Gfx_CH02Cond_Fwd', 'cdwr', HW, (g.X_CDR, y2o), (g.X_CDR, y1o))
    add('Gfx_CdwTotal_Fwd', 'cdwr', HW, (g.X_CDR, y1o), (g.X_CDR, g.Y_CDR))
    add('Gfx_CdwTotal_Fwd', 'cdwr', HW, (g.X_CDR, g.Y_CDR), (g.CT_DROP['01'], g.Y_CDR))
    add('Gfx_CT02_Fwd', 'cdwr', HW, (g.CT_DROP['01'], g.Y_CDR), (g.CT_DROP['02'], g.Y_CDR))
    for n in g.TWX:
        ix, iy = g.ct_anchor(n, 'inlet')
        add(f'Gfx_CT{n}_Fwd', 'cdwr', 10, (g.CT_DROP[n], g.Y_CDR), (g.CT_DROP[n], iy), (ix + 4, iy))
    o1, o2 = g.ct_anchor('01', 'outlet'), g.ct_anchor('02', 'outlet')
    add('Gfx_CT01_Fwd', 'cdws', 10, (o1[0] + 4, o1[1]), (g.X_CDSUC, o1[1]))
    add('Gfx_CT02_Fwd', 'cdws', 10, (o2[0] + 4, o2[1]), (g.X_CT2OUT, o2[1]), (g.X_CT2OUT, g.Y_CDWS))
    add('Gfx_CT02_Fwd', 'cdws', HW, (g.X_CT2OUT, g.Y_CDWS), (g.X_CDSUC, g.Y_CDWS))
    add('Gfx_CT01_Fwd', 'cdws', HW, (g.X_CDSUC, o1[1]), (g.X_CDSUC, g.Y_CDWS))
    add('Gfx_CdwTotal_Fwd', 'cdws', HW, (g.X_CDSUC, g.Y_CDWS), (g.X_CDSUC, CDP['01'][1] + 44.5))
    add('Gfx_CDP02_Fwd', 'cdws', HW, (g.X_CDSUC, CDP['01'][1] + 44.5), (g.X_CDSUC, CDP['02'][1] + 44.5))
    for n, (x, y) in CDP.items():
        add(f'Gfx_CDP{n}_Fwd', 'cdws', 10, (g.X_CDSUC, y + 44.5), (x + 98, y + 44.5))
        add(f'Gfx_CDP{n}_Fwd', 'cdws', 10, (x + 85, y + 12), (x + 85, y - 20), (g.X_CDS, y - 20))
    taps = [y1i, CDP['01'][1] - 20, y2i, CDP['02'][1] - 20]                                         # X_CDS header (top -> bottom)
    for k in range(3):
        add(f'Gfx_CdpDis_S{k}_Fwd', 'cdws', HW, (g.X_CDS, taps[k]), (g.X_CDS, taps[k + 1]))
        add(f'Gfx_CdpDis_S{k}_Rev', 'cdws', HW, (g.X_CDS, taps[k + 1]), (g.X_CDS, taps[k]))
    # ---- make-up, chemical, bleed
    add('CHW_FillValveCmd', 'mu', 6, (g.X_MUR, g.Y_MU), (g.X_FILL, g.Y_MU), (g.X_FILL, g.Y_CHWR + 6))
    m1, m2 = g.ct_anchor('01', 'makeup'), g.ct_anchor('02', 'makeup')
    add('Gfx_MuTowers_Fwd', 'mu', 6, (g.X_MUR, g.Y_MU), (g.X_MUR, g.Y_MUH), (m2[0] + 8, g.Y_MUH))
    add('CT01_MakeupValveCmd', 'mu', 6, (m2[0] + 8, g.Y_MUH), (m1[0] + 8, g.Y_MUH))
    for n, (mx, my) in (('01', m1), ('02', m2)):
        add(f'CT{n}_MakeupValveCmd', 'mu', 5, (mx + 8, g.Y_MUH), (mx + 8, my), (mx - 2, my))
    pf = SPR['v73_potfeeder']['anchors']; PFX, PFY = g.POT
    add('Gfx_PotFeeder_Fwd', 'chem', 4, (g.X_DIS, 800), (PFX + pf['in'][0] + 6, 800), (PFX + pf['in'][0] + 6, PFY + pf['in'][1]))
    add('Gfx_PotFeeder_Fwd', 'chem', 4, (PFX + pf['out'][0], PFY + pf['out'][1]), (PFX + pf['out'][0], 918), (g.X_SUC, 918))
    ds = SPR['v73_dosing']['anchors']['out']
    add('CT_ChemDosingPumpCmd', 'chem', 4, (g.DOS[0] + ds[0], g.DOS[1] + ds[1]), (g.DOS[0] + ds[0], 190), (g.X_CDR, 190))
    add('CT_BleedValveCmd', 'drain', 5, (g.X_CDR, 262), (1178, 262), (1178, 300))
    return S


def _param_polys(size, polys):
    """per-pixel arc length S, lateral t (-1..1) and mask for orthogonal polylines with bends (same trimming as pipes71)"""
    W, H = size
    S = np.zeros((H, W), np.float32); T = np.zeros((H, W), np.float32); M = np.zeros((H, W), bool)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32) + 0.5
    for pts, w in polys:
        r = w / 2.0; R = w * 0.9
        segs = []
        for a_, b_ in zip(pts, pts[1:]):
            d = (np.sign(b_[0] - a_[0]), np.sign(b_[1] - a_[1]))
            segs.append([list(a_), list(b_), d])
        for i in range(1, len(segs)):
            s0, s1 = segs[i - 1], segs[i]
            if s0[2] != s1[2]:
                s0[1][0] -= s0[2][0] * R; s0[1][1] -= s0[2][1] * R
                s1[0][0] += s1[2][0] * R; s1[0][1] += s1[2][1] * R
        s_acc = 0.0
        for i, (a_, b_, d) in enumerate(segs):
            L = abs(b_[0] - a_[0]) + abs(b_[1] - a_[1])
            along = (xx - a_[0]) * d[0] + (yy - a_[1]) * d[1]
            lat = (xx - a_[0]) * (-d[1]) + (yy - a_[1]) * d[0]
            m = (along >= -0.5) & (along <= L + 0.5) & (np.abs(lat) <= r)
            S[m] = s_acc + along[m]; T[m] = lat[m] / r; M |= m
            s_acc += L
            if i + 1 < len(segs) and segs[i + 1][2] != d:
                d2 = segs[i + 1][2]
                c = pts[i + 1]
                cx, cy = c[0] - d[0] * R + d2[0] * R, c[1] - d[1] * R + d2[1] * R
                dx, dy = xx - cx, yy - cy
                dist = np.sqrt(dx * dx + dy * dy)
                v0 = (b_[0] - cx, b_[1] - cy)                        # start of the arc
                ang = np.abs(np.arctan2(v0[0] * dy - v0[1] * dx, v0[0] * dx + v0[1] * dy))
                vx, vy = c[0] - cx, c[1] - cy
                m = (np.abs(dist - R) <= r) & (dx * np.sign(vx) >= -0.5) & (dy * np.sign(vy) >= -0.5) & (ang <= np.pi / 2 + 0.02)
                # lateral sign: + on the side the straight lateral points to
                side = np.sign(d[0] * d2[1] - d[1] * d2[0])
                S[m] = s_acc + R * ang[m]; T[m] = (-side) * (dist[m] - R) / r; M |= m
                s_acc += R * np.pi / 2
    return S, T, M


def water_frames(size, polys, svc, frames=12, P=96.0):
    """water moving inside the pipe: the pipe's own cylinder shading + drifting light streaks and small bubbles,
    periodic along the flow so the GIF loops seamlessly (no arrows)"""
    import pipes71
    S, T, M = _param_polys(size, polys)
    M &= np.abs(T) <= 0.86                                               # keep the anti-aliased pipe wall from the pipe layer
    col = np.array(pipes71.COL.get(svc, (94, 196, 242)), np.float32) / 255.0
    lum, spec = pipes71._profile(T)
    base = np.clip(col[None, None, :] * lum[..., None] + spec[..., None], 0, 1)
    edge = np.clip((1 - np.abs(T)) * 6, 0, 1); base = base * (0.55 + 0.45 * edge[..., None])
    rng = np.random.default_rng(abs(hash(svc)) % 1000 + len(polys))
    streaks = [(rng.uniform(0, P), rng.uniform(-0.55, 0.55), rng.uniform(10, 22), rng.uniform(0.10, 0.2), rng.uniform(0.45, 0.9)) for _ in range(8)]
    bubbles = [(rng.uniform(0, P), rng.uniform(-0.5, 0.5), rng.uniform(0.6, 1.0)) for _ in range(5)]
    rpx = max(w for _, w in polys) / 2.0
    out = []
    for k in range(frames):
        u = (S - k * P / frames) % P
        st = np.zeros_like(S)
        for (ui, ti, su, sd, a) in streaks:
            du = ((u - ui + P / 2) % P) - P / 2
            st += a * np.exp(-(du / su) ** 2 - ((T - ti) / sd) ** 2)
        wave = 0.10 * np.cos(2 * np.pi * (u / P) * 2 + T * 1.5)
        bb = np.zeros_like(S)
        for (ui, ti, a) in bubbles:
            du = ((u - ui + P / 2) % P) - P / 2
            bb = np.maximum(bb, a * np.exp(-((du * du) + ((T - ti) * rpx) ** 2) / 1.6))
        bright = np.clip(st + wave, -0.2, 1.2)
        px = base * (1 + 0.55 * bright[..., None]) + 0.18 * np.clip(bright, 0, 1)[..., None] * np.array([0.85, 0.95, 1.0])
        px = px * (1 - bb[..., None]) + np.array([0.92, 0.97, 1.0]) * bb[..., None]
        rgba = np.zeros(S.shape + (4,), np.uint8)
        rgba[..., :3] = (np.clip(px, 0, 1) * 255).astype(np.uint8); rgba[..., 3] = np.where(M, 255, 0)
        out.append(Image.fromarray(rgba, 'RGBA'))
    return out


def flow_overlays(p):
    """one animated GIF per condition (all its segments), inserted just above the pipe layer"""
    groups = {}
    for cond, svc, w, pts in flow_segments():
        groups.setdefault((cond, svc), []).append((pts, w))
    els = []
    img = os.path.join(G73.OUT, 'px', 'img')
    for i, ((cond, svc), polys) in enumerate(sorted(groups.items())):
        xs = [q[0] for pts, _ in polys for q in pts]; ys = [q[1] for pts, _ in polys for q in pts]
        pad = 12
        x0, y0 = int(min(xs) - pad), int(min(ys) - pad); x1, y1 = int(max(xs) + pad), int(max(ys) + pad)
        rel = [([(a - x0, b - y0) for a, b in pts], w) for pts, w in polys]
        name = f'v74_flow_{cond}_{svc}.gif'.replace('Gfx_', '')
        save_gif(water_frames((x1 - x0, y1 - y0), rel, svc), os.path.join(img, name), 90)
        n0 = len(p.el)
        ximg_bool(p, x0, y0, x1 - x0, y1 - y0, cond, name, 'v74_blank.png', f'water flow animation {cond} (pump proven + flow meter)')
        els.append(p.el.pop())
    for k, e in enumerate(els): p.el.insert(2 + k, e)          # above the pipe layer (index 1), below all widgets
    return len(els)


PLANT_FIX = [("tag(p, 590, y - 100, 84, f'{u}_DischargePressure'", "tag(p, 590, y - 116, 84, f'{u}_DischargePressure'"),
             ("tag(p, 432, 150, 80, 'CHWS'", "tag(p, 432, 140, 80, 'CHWS'"),
             ("pct_at=(X_BYP + 34, 628))", "pct_at=(X_BYP + 44, 628))"),
             ("tag(p, X_CDSUC - 150, 506, 94, 'CDW_Flow'", "tag(p, X_CDSUC - 144, 506, 94, 'CDW_Flow'"),
             ("        sprite(p, nm, 1918, 792 + i * 52)\n        lbl(p, 1944, 780 + i * 52, 136, t, 8, TXT)",
              "        sprite(p, nm, 1918, 806 + i * 50)\n        lbl(p, 1944, 794 + i * 50, 136, t, 8, TXT)"),
             ("tag(p, 288, 910, 96, 'CHWFlow'", "tag(p, 196, 960, 96, 'CHWFlow'"),
             ("lbl(p, 470, 928, 360, '◀ CHW LOOP FILL: solenoid · meter · RPZ  (make-up water)', 8, C_MU, True, h=16)",
              "lbl(p, 452, 930, 150, '◀ CHW FILL (make-up)', 8, C_MU, True, h=16)"),
             ("pct=f'{c}_ChwFCVCmd', what=f'{c} evaporator FCV', pct_at=(748, y + 2))", "pct=f'{c}_ChwFCVCmd', what=f'{c} evaporator FCV', pct_at=(870, y - 20))"),
             ("pct=f'{c}_CdwHPVCmd', what=f'{c} condenser HPV', pct_at=(x + 206, y + 2))", "pct=f'{c}_CdwHPVCmd', what=f'{c} condenser HPV', pct_at=(x + 140, y - 20))"),
             ("hdr_text(p, X_CDS - 136, CDP['02'][1] + 16, 'CDP DISCH. HDR ▶', C_CDWS, 132)",
              "hdr_text(p, 1072, 944, 'CDP DISCH. HDR ▲', C_CDWS, 104)")]


def _patched(fn, fixes):
    import inspect, textwrap
    src = textwrap.dedent(inspect.getsource(fn))
    for a, b in fixes:
        assert a in src, a
        src = src.replace(a, b)
    ns = {}
    exec(compile(src, f'<patched {fn.__name__}>', 'exec'), fn.__globals__, ns)
    return ns[fn.__name__]


def plant_page():
    import pipes71
    G73.DOS = (1010, 127)
    pipes71.Layer.arrow = lambda self, *a, **k: None
    p = _patched(G73.plant_page, PLANT_FIX)()
    for i, e in enumerate(p.el):                                   # RPZ a little smaller so it clears the bottom band
        if 'v73_rpz.png' in e and e.startswith('<Picture'):
            x, y, w, h = (float(v) for v in re.search(r'layout="([^"]+)"', e).group(1).split(','))
            cx, cy = x + w / 2, y + h / 2; w2, h2 = w * 0.82, h * 0.82
            p.el[i] = re.sub(r'layout="[^"]+"', f'layout="{cx - w2 / 2:.1f},{cy - h2 / 2:.1f},{w2:.1f},{h2:.1f}"', e)
    n = flow_overlays(p)
    print('flow overlays', n)
    val(p, 392, 216, 120, 'Gfx_ChwPumpNoFlow', 'CHW pump on but no flow (flow meter check)', h=17, size=7, bool_c=(FLT, '#1f6f43'), fmt='%out.value%')
    val(p, 1298, 198, 108, 'Gfx_CdwPumpNoFlow', 'CDW pump on but no flow (flow meter check)', h=17, size=7, bool_c=(FLT, '#1f6f43'), fmt='%out.value%')
    for i, e in enumerate(p.el):
        if 'thick = header, thin = branch' in e:
            p.el[i] = e.replace('thick = header, thin = branch · tower fans animate when running',
                                'water moves in a pipe only when its pump is proven AND the flow meter confirms flow')
    return p


# ================================================================ valves page: V7.4 symbols + actuator animation note
VALVES_FIX = [("panel(p, x0, 80, 530, 350, 'SYMBOLS (V7.3 butterfly valves)')", "panel(p, x0, 80, 530, 420, 'SYMBOLS (V7.4 butterfly valves)')"),
              ("        sprite(p, nm, x0 + 60, 136 + i * 50)\n        lbl(p, x0 + 120, 122 + i * 50, 400, t, 9, TXT)",
               "        sprite(p, nm, x0 + 60, 150 + i * 52)\n        lbl(p, x0 + 120, 136 + i * 52, 400, t, 9, TXT)\n"
               "    for i, t in enumerate(('Actuator picture follows the valve position (9 steps) + yellow/green bar = % open.',\n"
               "                           'Amber rotating lamp on the actuator = motor running (command and position differ).',\n"
               "                           'On/off valves without a % feedback: position estimated from the stroke time.')):\n"
               "        lbl(p, x0 + 12, 430 + i * 20, 510, t, 8, '#c9d3dd')")]


def valves_page():
    return _patched(G73.valves_page, VALVES_FIX)()


# ================================================================ energy dashboard: no text inside the narrow bars (values shown below)
def energy_dashboard():
    p = G73.energy_dashboard()
    for i, e in enumerate(p.el):
        if e.startswith('<Bargraph'):
            e = e.replace('    <ObjectToString name="text" format="%out.value%"/>\n', '')
            p.el[i] = e.replace('<Bargraph ', '<Bargraph text=" " ', 1)
    x = 656
    for t, pt in (('CH01', 'CH01_kW'), ('CH02', 'CH02_kW'), ('CHP01', 'CHP01_kW'), ('CHP02', 'CHP02_kW'),
                  ('CDP01', 'CDP01_kW'), ('CDP02', 'CDP02_kW'), ('CT01', 'CT01_kW'), ('CT02', 'CT02_kW')):
        val(p, x + 12, 862, 76, pt, f'{t} kW value', h=18, size=8)
        x += 110
    return p


# ================================================================ units in page texts (points carry their own facets)
UNIT_TXT = [(re.compile(r'\bkPa\b'), 'bar'), (re.compile(r'm(?:3|³)/h(?:r)?\b'), 'gpm')]


def units_text(p):
    for i, e in enumerate(p.el):
        def fix(m):
            t = m.group(2)
            for rx, rep in UNIT_TXT: t = rx.sub(rep, t)
            return m.group(1) + t + '"'
        p.el[i] = re.sub(r'(text=")([^"]*)"', fix, e)


# ================================================================ faceplates around the equipment render
def fp_equipment(name, title, img, iw, ih, model, rows_, size=(900, 560), lw=300, rh=26, extra=None):
    p = G71.fp(name, title, size)
    W, H = size
    p.rect(10, 44, iw + 20, H - 54, fill='#0f1418', stroke='#2c3440', pen=1.0)
    ximg(p, 20, 54, img, iw, ih)
    for i, t in enumerate(model):
        lbl(p, 18, 64 + ih + i * 18, iw + 8, t, 8 if i else 9, '#8fd3ff' if i == 0 else '#c9d3dd', i == 0)
    x0 = iw + 42
    rows(p, x0, 50, W - x0 - 10, rows_, lw=lw, rh=rh)
    if extra: extra(p, x0)
    return p


def fp_btu():
    return fp_equipment('ALT_V71_FP_BTU', 'BTU (energy) meter — CHW main', 'v74_fp_btu.png', 330, 220,
                        ['ONICON System-10 BTU meter', 'FT-3500 insertion electromagnetic flow meter', 'matched RTD pair (supply / return)',
                         'BACnet MS/TP via System-10-BAC card', 'original render - no manufacturer artwork'],
                        [('Flow', 'BTU_Flow'), ('Supply temperature', 'BTU_SupplyTemp'), ('Return temperature', 'BTU_ReturnTemp'), ('Delta-T', 'BTU_DeltaT'),
                         ('Cooling power', 'BTU_Power_RT'), ('Energy total', 'BTU_EnergyTotal'), ('Communication', 'BTU_CommOk', {'bool_c': (RUN, FLT)}),
                         ('Valid (range + comm)', 'BTU_Valid', {'bool_c': (RUN, FLT)}), ('Used for plant load', 'CoolingLoadSource'),
                         ('Deviation vs calculated', 'BTU_DeviationAlarm', {'bool_c': (WARN, OKC)}), ('Invalid alarm', 'BTU_InvalidAlarm', {'bool_c': (FLT, OKC)}),
                         ('Max valid RT', 'BTU_MaxValidRT', {'action': True})], size=(960, 440), lw=260)


def fp_power():
    return fp_equipment('ALT_V71_FP_Power', 'Main power meter — plant MCC', 'v74_fp_me96.png', 220, 220,
                        ['Mitsubishi ME96SSHB-MB', '96 x 96 mm multi-measuring instrument', 'Modbus RTU (std) / Modbus TCP (option)',
                         'no native BACnet: via Niagara Modbus', 'or a Modbus-BACnet gateway', 'original render - no manufacturer artwork'],
                        [('Active power', 'PM_Main_kW'), ('Apparent power', 'PM_Main_kVA'), ('Feeder loading', 'PM_Main_LoadPct'), ('Energy', 'PM_Main_kWh'),
                         ('Voltage L-L', 'PM_Main_Volts'), ('Current', 'PM_Main_Amps'), ('Power factor', 'PM_Main_PF'), ('Frequency', 'PM_Main_Hz'),
                         ('Communication', 'PM_Main_CommOk', {'bool_c': (RUN, FLT)}), ('Meter vs sum of loads', 'PowerMeter_DeviationAlarm', {'bool_c': (WARN, OKC)}),
                         ('Sum of plant loads', 'Plant_kW'), ('Auxiliary kW', 'Aux_kW')], size=(860, 400), lw=250)


FLOWS = [('CHW main (FT)', 'CHWFlow'), ('CH01 evaporator', 'CH01_ChwFlow'), ('CH02 evaporator', 'CH02_ChwFlow'),
         ('Evaporator total (bypass PV)', 'CHW_EvapFlowTotal'), ('Bypass min-flow SP', 'CHW_BypassMinFlowSP'), ('BTU meter flow', 'BTU_Flow'),
         ('CDW header', 'CDW_Flow'), ('CH01 condenser', 'CH01_CdwFlow'), ('CH02 condenser', 'CH02_CdwFlow'), ('Tower make-up', 'CT_MakeupFlow'),
         ('Make-up volume', 'CT_MakeupVolume'), ('CHW fill (make-up)', 'CHW_FillFlow'), ('CHW fill volume', 'CHW_FillVolume'),
         ('CHW low-flow alarm', 'CHW_FlowLowAlarm', {'bool_c': (FLT, OKC)}), ('CDW low-flow alarm', 'CDW_FlowLowAlarm', {'bool_c': (FLT, OKC)}),
         ('CHW flow sensor invalid', 'CHWFlow_SensorInvalidAlarm', {'bool_c': (FLT, OKC)})]


def fp_flow():
    return fp_equipment('ALT_V71_FP_Flow', 'Flow meters (water: US gpm)', 'v74_fp_fm.png', 220, 280,
                        ['ONICON FT-3500 insertion', 'electromagnetic flow meter', 'hot-tap: ball valve + probe', 'BACnet MS/TP or analog 4-20 mA',
                         'original render - no manufacturer artwork'], FLOWS, size=(900, 520), lw=320, rh=27)


def fp_oa():
    return fp_equipment('ALT_V71_FP_OA', 'Outdoor air sensor (T + RH, psychrometrics)', 'v74_fp_oa.png', 200, 330,
                        ['Outdoor T / RH transmitter', 'in a 10-plate radiation shield', '(naturally aspirated, pole mount)', 'original render'],
                        [('Dry bulb', 'OA_Temperature'), ('Relative humidity', 'OA_Humidity'), ('Wet bulb (calc)', 'OA_WetBulb'), ('Dew point (calc)', 'OA_DewPoint'),
                         ('Enthalpy (calc)', 'OA_Enthalpy'), ('Sensor fault (DI)', 'OA_SensorFault', {'bool_c': (FLT, OKC)}), ('Valid', 'OA_Valid', {'bool_c': (RUN, FLT)}),
                         ('Invalid alarm', 'OA_SensorInvalidAlarm', {'bool_c': (FLT, OKC)}), ('Default wet bulb (fallback)', 'OA_WetBulbDefault', {'action': True}),
                         ('Valid temp min', 'OA_TempMinValid', {'action': True}), ('Valid temp max', 'OA_TempMaxValid', {'action': True}),
                         ('Valid RH min', 'OA_HumMinValid', {'action': True}), ('Valid RH max', 'OA_HumMaxValid', {'action': True})], size=(860, 480), lw=260)


# ================================================================ main
if __name__ == '__main__':
    bog, G7.KITDIR, OUT, regdir, s73, s74 = sys.argv[1:7]
    G73.OUT = G71.OUT = OUT
    G7.PATH.update(G7.load_paths(bog))
    G.FOLDER = {n: q.rsplit('/', 1)[0].replace('/ChillerPlant/', '').replace('/ChillerPlant', '') for n, q in G7.PATH.items()}
    G.STATION_NAME = STATION
    G.PAGES = G73.PAGES; G7.PAGES = G73.PAGES
    H, Al = (G.read_reg(os.path.join(regdir, f)) for f in ('V7_HISTORY_REGISTER.csv', 'V7_ALARM_REGISTER.csv'))
    os.makedirs(os.path.join(OUT, 'px', 'img'), exist_ok=True)
    build_sprites(s73, s74)
    only = os.environ.get('ONLY')
    pages = [plant_page(), G73.chillerplant_page(), G73.ctplant_page(), G73.plant3d_page(), G71.chillers_page(), G73.plant_detail(),
             G73.drives_page(), valves_page(), G73.meters_page(), G71.schedules_page(), G71.dark_page(G.optimization()), energy_dashboard(),
             G71.dark_page(G.energy()), G71.dark_page(G.alarms_history()), G71.dark_page(G.simulation()),
             G7.airside_page(), G73.zones_page(), G7.ahu_page('AHU01'), G7.ahu_page('AHU02'), G7.oau_page('OAU01'), G7.fcu_page(), G7.vent_page()]
    pages += [G71.fp_ch('01'), G71.fp_ch('02')] + [G71.fp_pump(u) for u in ('CHP01', 'CHP02', 'CDP01', 'CDP02')] + [G73.fp_ct('CT01'), G73.fp_ct('CT02')]
    pages += [G73.fp_cell(c) for _, c in G73.CELLS]
    pages += [G71.fp_air_vsd(u) for u in G73.AIR_VSD] + [fp_btu(), fp_power(), fp_flow(), fp_oa()]
    for q in pages:
        if q.name not in G73.AIRPAGES: units_text(q)          # air-side airflow stays m3/h
    if only: pages = [q for q in pages if any(o in q.name for o in only.split(','))]
    G71.FACEPLATES[:] = [q.name for q in pages if q.name.startswith(('ALT_V71_FP_', 'ALT_V73_FP_', 'ALT_V74_FP_'))]
    rows_ = G71.build(pages, OUT, H, Al)
    with open(os.path.join(OUT, 'V7_4_GRAPHIC_POINT_MAPPING.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows_[0].keys())); w.writeheader(); w.writerows(rows_)
    print('valves animated', len(set(VALVE_USED)), 'bindings', len(rows_), 'distinct points', len({r['Point'] for r in rows_ if r['Point'] != '(BQL)'}),
          'images', len(G71.IMG))
