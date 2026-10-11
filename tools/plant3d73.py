"""V7.3 3-D plant (Blender / Cycles): one model, three isometric views + anchors for the live Px overlays.
   view 'plant'   -> ALT_V71_Plant3D (whole plant)        view 'chiller' -> ALT_V73_ChillerPlant (plant room)
   view 'ct'      -> ALT_V73_CTPlant (roof: 2 towers x 2 fan cells, VSD per cell, make-up, treatment)
Contents: 2 chillers, 2 CHP + 2 CDP (with VSDs), headers, butterfly MVs (red on/off, green modulating), CHW min-flow bypass
(modulating valve + isolation valves + manual bypass loop), BTU meter, mag flow meters, TT/PT, expansion tank, make-up water
(green) to the CHW loop (RPZ + meter + solenoid) and to every tower basin, bypass (pot) chemical feeder, CDW dosing skid +
bleed-off, OA sensor, 2 towers x 2 cells each with a VSD per cell.
usage: python3 plant3d73.py outdir view[,view...] [W H samples]"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import assets73 as A

OUT = sys.argv[1]; VIEWS = sys.argv[2].split(',')
W = int(sys.argv[3]) if len(sys.argv) > 3 else 1920
H = int(sys.argv[4]) if len(sys.argv) > 4 else 944
SAMPLES = int(sys.argv[5]) if len(sys.argv) > 5 else 64
A.reset(); sc = bpy.context.scene; mm = A.M()
ANC = {}
def anchor(k, p): ANC[k] = tuple(p)

# ---------------------------------------------------------------- floor, roof deck, building wall
FLOOR = [A.box((3.5, 0, -0.05), (38, 16, 0.1), mm['floor'])]
for gx in range(-15, 23, 2): FLOOR.append(A.box((gx, 0, 0.002), (0.02, 16, 0.004), mm['grid']))
for gy in range(-8, 9, 2): FLOOR.append(A.box((3.5, gy, 0.002), (38, 0.02, 0.004), mm['grid']))
DECK_Z = 3.625
A.box((14.6, 0, 3.5), (12.4, 7.8, 0.25), mm['concrete'])
for x in (8.6, 14.6, 20.6):
    for y in (-3.7, 3.7): A.box((x, y, 1.7), (0.35, 0.35, 3.4), mm['concrete'])
for x in (8.45, 20.75):
    A.box((x, 0, DECK_Z + 0.55), (0.04, 7.8, 0.04), mm['rail'])
A.box((14.6, -3.88, DECK_Z + 0.55), (12.4, 0.04, 0.04), mm['rail'])
A.box((-12.4, 0, 0.1), (1.6, 2.6, 0.2), mm['concrete'])                      # building riser plinth (pipes rise to the building)
anchor('BUILDING', (-12.4, 0, 6.6))

# ---------------------------------------------------------------- chillers
CHY = {'01': -3.2, '02': 3.2}
NZ = {}
for n, y in CHY.items():
    NZ[n] = A.chiller((0, y, 0), mm, running=False)
    anchor(f'CH{n}', NZ[n]['top']); anchor(f'CH{n}_panel', NZ[n]['panel'])
    anchor(f'CH{n}_chw', NZ[n]['chw_out']); anchor(f'CH{n}_cdw', NZ[n]['cdw_out'])

# ---------------------------------------------------------------- pumps (+ VSD cabinets)
PU = {}
for n, y in CHY.items():
    PU[f'CHP{n}'] = A.pump((-7.0, y, 0), 1, mm, running=False)
    PU[f'CDP{n}'] = A.pump((6.9, y, 0), 1, mm, running=False)
    for u in (f'CHP{n}', f'CDP{n}'):
        anchor(u, PU[u]['top'])
        vx = -8.6 if u.startswith('CHP') else 5.3
        vy = y - 1.4 if n == '01' else y + 1.4
        top = A.vsd((vx, vy, 0), mm, running=True)
        A.box((vx, vy + 0.2, 0.6), (0.06, 0.06, 1.2), mm['steel'])
        anchor(f'{u}_vsd', top)

# ---------------------------------------------------------------- CHW circuit
X_SUCH, X_DISH, X_RIS = -5.3, -4.6, -3.4
for n, y in CHY.items():
    s, d = PU[f'CHP{n}']['suction'], PU[f'CHP{n}']['discharge']
    A.pipe([s, (X_SUCH, y, s[2])], 'chwr')
    A.butterfly(((s[0] + X_SUCH) / 2, y, s[2]), 'x', mode='onoff', mm=mm)                    # CHP suction MV
    A.pipe([d, (d[0], y, 2.6), (X_DISH, y, 2.6)], 'chwr')
    A.butterfly((d[0], y, 1.9), 'z', mode='onoff', up='-y', mm=mm)                            # CHP discharge MV
    A.check_valve((d[0], y, 1.55), 'z', mm=mm)
    A.pt_gauge((s[0] + 0.25, y, s[2] + 0.16), mm=mm); A.pt_gauge((d[0], y - 0.16, 2.2), up='-y', mm=mm)
    ci = NZ[n]['chw_in']; co = NZ[n]['chw_out']
    A.pipe([(X_DISH, ci[1], 2.6), (X_DISH, ci[1], ci[2]), ci], 'chwr')                        # discharge header -> evaporator in
    A.butterfly((X_DISH + 0.8, ci[1], ci[2]), 'x', mode='onoff', mm=mm)                       # CH CHW inlet ISO
    A.pipe([co, (X_RIS, co[1], co[2]), (X_RIS, co[1], 3.8)], 'chws')                          # evaporator out -> CHWS riser
    A.butterfly(((co[0] + X_RIS) / 2, co[1], co[2]), 'x', mode='mod', mm=mm)                  # CH CHW outlet FCV
    A.tt((co[0] - 0.2, co[1], co[2] + 0.16), mm=mm)
A.pipe([(X_SUCH, -3.2 - 0.6, 0.64), (X_SUCH, 3.2 + 0.6, 0.64)], 'chwr')                       # CHP suction header
A.pipe([(X_DISH, -3.2 - 0.6, 2.6), (X_DISH, 3.2 + 0.6, 2.6)], 'chwr')                         # CHP discharge header
A.pipe([(X_RIS, -3.45 - 0.5, 3.8), (X_RIS, 2.95 + 0.5, 3.8)], 'chws')                         # CHWS header
A.pipe([(X_RIS, 0, 3.8), (-12.0, 0, 3.8), (-12.0, 0, 6.6)], 'chws')                           # CHWS to the building riser
A.pipe([(-12.8, 0, 6.6), (-12.8, 0, 0.3), (X_SUCH, 0, 0.3), (X_SUCH, 0, 0.64)], 'chwr')       # CHWR from the building riser
anchor('CHWS', (-7.0, 0, 4.3)); anchor('CHWR', (-7.0, 0, 0.7))
# BTU meter (on the CHWS to the building) + main CHW flow meter (CHWR) + header TT / PT
A.magmeter((-8.4, 0, 3.8), 'x', mm=mm); anchor('BTU', (-8.4, 0, 4.4))
A.tt((-9.4, 0, 3.96), mm=mm); A.tt((-9.4, 0, 0.46), mm=mm)
calc = A.btu_calc((-9.4, -1.0, 2.1), mm); A.box((-9.4, -0.95, 1.0), (0.05, 0.05, 1.9), mm['steel'])
A.magmeter((-8.4, 0, 0.3), 'x', mm=mm); anchor('FT_CHW', (-8.4, 0, 0.9))
A.pt_gauge((-6.2, 0, 3.96), mm=mm)
# CHW min-flow bypass: isolation (handwheel) - MODULATING valve - isolation, manual bypass loop around it
XB = -10.9
A.pipe([(XB, 0, 3.8), (XB, 0, 0.3)], 'chwr', flanges=False)
A.butterfly((XB, 0, 3.05), 'z', up='-y', handwheel=True, mm=mm)
A.butterfly((XB, 0, 2.05), 'z', mode='mod', up='-y', mm=mm)
A.butterfly((XB, 0, 1.05), 'z', up='-y', handwheel=True, mm=mm)
A.pipe([(XB, 0, 3.4), (XB + 0.8, 0, 3.4), (XB + 0.8, 0, 0.7), (XB, 0, 0.7)], 'chwr', r=0.08, flanges=False)
A.gate_valve((XB + 0.8, 0, 2.05), 'z', 0.06, mm, up='x')
anchor('BYPASS', (XB, -0.3, 2.3)); anchor('BYPASS_MAN', (XB + 0.8, 0, 2.4))
# expansion tank + CHW fill line (make-up water: RPZ -> meter -> solenoid)
et = A.exp_tank((-7.3, 1.5, 0), mm); anchor('EXP', et['top'])
A.pipe([(-7.3, 1.5, 0.12), (-7.3, 0.9, 0.12), (X_SUCH, 0.9, 0.12), (X_SUCH, 0.9, 0.64)], 'chwr', r=0.06, flanges=False)
Y_MU = 6.2
A.pipe([(-12.0, Y_MU, 0.45), (8.0, Y_MU, 0.45)], 'mu', r=0.07)                                   # make-up main (from water tank)
anchor('MU_IN', (-11.5, Y_MU, 0.9))
A.pipe([(-8.6, Y_MU, 0.45), (-8.6, 2.2, 0.45), (-7.3, 2.2, 0.45), (-7.3, 1.85, 0.45)], 'mu', r=0.05, flanges=False)
A.rpz((-8.6, 4.9, 0.45), 'y', mm); A.magmeter((-8.6, 3.8, 0.45), 'y', r=0.05, mm=mm); A.solenoid((-8.6, 2.9, 0.45), 'y', mm=mm)
anchor('FILL', (-8.6, 3.8, 1.0))
# bypass (pot) chemical feeder across the CHP headers
pf = A.pot_feeder((-4.0, 5.0, 0), mm); anchor('POT', pf['top'])
A.pipe([(X_DISH, 3.8, 2.6), (X_DISH, 5.0, 2.6), (X_DISH, 5.0, 1.05), pf['in']], 'chem', r=0.035, flanges=False)
A.pipe([pf['out'], (-5.3, 5.0, 0.45), (-5.3, 3.8, 0.45), (-5.3, 3.8, 0.64)], 'chem', r=0.035, flanges=False)
A.gate_valve((-4.6, 5.0, 1.6), 'z', 0.03, mm, up='-x'); A.gate_valve((-4.8, 5.0, 0.45), 'x', 0.03, mm)

# ---------------------------------------------------------------- CDW circuit
X_CDSUC, X_CDDIS, X_CDR = 8.3, 5.2, 3.3
for n, y in CHY.items():
    s, d = PU[f'CDP{n}']['suction'], PU[f'CDP{n}']['discharge']
    A.pipe([s, (X_CDSUC, y, s[2])], 'cdws')
    A.pipe([d, (d[0], y, 1.95), (X_CDDIS, y, 1.95)], 'cdws')
    A.butterfly((d[0], y, 1.62), 'z', mode='onoff', up='-y', mm=mm)
    A.butterfly(((s[0] + X_CDSUC) / 2 + 0.03, y, s[2]), 'x', mode='onoff', mm=mm)
    ci, co = NZ[n]['cdw_in'], NZ[n]['cdw_out']
    A.pipe([(X_CDDIS, ci[1], 1.95), (X_CDDIS, ci[1], ci[2]), ci], 'cdws')
    A.butterfly((X_CDDIS - 0.9, ci[1], ci[2]), 'x', mode='onoff', mm=mm)                     # CH CDW inlet ISO
    A.pipe([co, (X_CDR, co[1], co[2]), (X_CDR, co[1], 4.6)], 'cdwr')
    A.butterfly(((co[0] + X_CDR) / 2, co[1], co[2]), 'x', mode='mod', mm=mm)                 # CH CDW outlet HPV
A.pipe([(X_CDSUC, -3.8, 0.64), (X_CDSUC, 3.8, 0.64)], 'cdws')
A.pipe([(X_CDDIS, -3.8, 1.95), (X_CDDIS, 3.8, 1.95)], 'cdws')
A.pipe([(X_CDR, -3.6, 4.6), (X_CDR, 3.2, 4.6)], 'cdwr')
anchor('CDWR', (X_CDR, 0, 5.1)); anchor('CDWS', (X_CDSUC, 1.2, 1.1))
A.magmeter((X_CDSUC, -1.4, 0.64), 'y', mm=mm); anchor('FT_CDW', (X_CDSUC, -1.4, 1.2))

# ---------------------------------------------------------------- cooling towers: 2 towers x 2 fan cells on the roof deck
TW = {'01': 11.4, '02': 17.0}
TA = {}
for n, x in TW.items():
    TA[n] = A.tower((x, 0, DECK_Z), 2, mm, running=(False, False), fan_angle=0.3 * int(n))
    anchor(f'CT{n}', TA[n]['top']); anchor(f'CT{n}_basin', TA[n]['basin_front']); anchor(f'CT{n}_lt', TA[n]['lt'])
    for k in (1, 2):
        cx = TA[n][f'cell{k}'][0]
        anchor(f'CT{n}_{k:02d}', TA[n][f'cell{k}'])
        top = A.vsd((cx, -3.35, DECK_Z), mm, running=True, scale=0.9)                    # VSD per cell
        anchor(f'CT{n}_{k:02d}_vsd', top)
# CDWR to the towers: riser from the header, distribution header in front of the towers, branch + inlet MV per tower
Y_IN = -2.5; Z_IN = TA['01']['inlet'][2]
A.pipe([(X_CDR, -2.2, 4.6), (X_CDR, Y_IN, 4.6), (8.1, Y_IN, 4.6), (8.1, Y_IN, Z_IN), (TA['02']['inlet'][0] + 0.25, Y_IN, Z_IN)], 'cdwr')
for n in TW:
    ix, iy, iz = TA[n]['inlet']
    A.pipe([(ix, Y_IN, iz), (ix, iy, iz)], 'cdwr', r=0.14)
    A.butterfly((ix, (Y_IN + iy) / 2, iz), 'y', mode='onoff', mm=mm)
    A.tt((ix, (Y_IN + iy) / 2 - 0.45, iz + 0.14), mm=mm)
    anchor(f'CT{n}_in', (ix, (Y_IN + iy) / 2, iz + 0.5))
# CDWS: basin outlet -> outlet MV -> collection header behind the towers -> drop to the CDP suction header
Y_OUT = 2.7; Z_OUT = TA['01']['outlet'][2]
for n in TW:
    ox, oy, oz = TA[n]['outlet']
    A.pipe([(ox, oy, oz), (ox, Y_OUT, oz)], 'cdws', r=0.16)
    A.butterfly((ox, (oy + Y_OUT) / 2, oz), 'y', mode='onoff', mm=mm)
    anchor(f'CT{n}_out', (ox, (oy + Y_OUT) / 2, oz + 0.5))
A.pipe([(TA['02']['outlet'][0] + 0.25, Y_OUT, Z_OUT), (X_CDSUC, Y_OUT, Z_OUT), (X_CDSUC, Y_OUT, 0.64)], 'cdws')
A.tt((X_CDSUC + 0.16, Y_OUT, 2.2), up='x', mm=mm)
# make-up water to every basin (solenoid + float), and bleed-off / dosing
A.pipe([(8.0, Y_MU, 0.45), (8.0, Y_MU, DECK_Z + 0.5), (8.0, 3.3, DECK_Z + 0.5), (TA['02']['makeup'][0], 3.3, DECK_Z + 0.5)], 'mu', r=0.06)
for n in TW:
    mx, my, mz = TA[n]['makeup']
    A.pipe([(mx, 3.3, DECK_Z + 0.5), (mx, my, DECK_Z + 0.5), (mx, my, mz)], 'mu', r=0.045, flanges=False)
    A.solenoid((mx, (3.3 + my) / 2, DECK_Z + 0.5), 'y', mm=mm)
    anchor(f'CT{n}_mu', (mx, (3.3 + my) / 2, DECK_Z + 1.0))
A.pipe([(X_CDR, -3.6, 4.6), (X_CDR, -4.4, 4.6), (X_CDR, -4.4, 0.25), (X_CDR + 0.8, -4.4, 0.25)], 'drain', r=0.05, flanges=False)
A.solenoid((X_CDR, -4.4, 2.2), 'z', mm=mm)
A.box((X_CDR + 1.0, -4.4, 0.03), (0.5, 0.5, 0.04), mm['dark'])                                # floor drain
anchor('BLEED', (X_CDR, -4.4, 2.6))
ds = A.dosing_skid((10.0, -5.6, 0), mm); anchor('DOSING', ds['top'])
A.pipe([ds['out'], (10.3, -4.4, 0.5), (X_CDSUC, -4.4, 0.5), (X_CDSUC, -3.8, 0.5), (X_CDSUC, -3.8, 0.64)], 'chem', r=0.03, flanges=False)
# OA sensor on the roof deck
oa = A.oa_sensor((20.2, -3.3, DECK_Z), mm); anchor('OA', oa)

# ---------------------------------------------------------------- lights
A.sun_and_world(sc, 3.4)
bpy.ops.object.light_add(type='AREA', location=(-8, -14, 16)); ar = bpy.context.object; ar.data.energy = 2600; ar.data.size = 14
ar.rotation_euler = (math.radians(50), 0, math.radians(-30))
A.render_setup(sc, W, H, SAMPLES)

CAMS = {'plant': ((-16.5, -33.0, 26.0), (4.0, 0.3, 3.2), 41.0),
        'chiller': ((-14.5, -27.0, 17.5), (-4.6, 0.6, 1.7), 21.0),
        'ct': ((5.0, -29.0, 22.0), (12.2, 0.0, 4.9), 24.5)}
res = {}
MASKONLY = os.environ.get('MASKONLY')
for v in VIEWS:
    loc, tgt, scale = CAMS[v]
    cam = A.ortho_cam(sc, loc, tgt, scale, 'cam_' + v); sc.camera = cam
    if not MASKONLY:
        sc.render.filepath = os.path.join(OUT, f'v73_3d_{v}.png')
        bpy.ops.render.render(write_still=True)
    # occupancy mask (equipment only, floor hidden) for automatic label placement - not published
    for o in FLOOR: o.hide_render = True
    smp = sc.cycles.samples; sc.cycles.samples = 1; sc.cycles.use_denoising = False
    sc.render.filepath = os.path.join(OUT, '..', '..', f'v73_3d_{v}_mask.png')
    bpy.ops.render.render(write_still=True)
    for o in FLOOR: o.hide_render = False
    sc.cycles.samples = smp; sc.cycles.use_denoising = True
    an = {}
    for k, p in ANC.items():
        q = world_to_camera_view(sc, cam, Vector(p))
        an[k] = (round(q.x * W, 1), round((1 - q.y) * H, 1))
    res[v] = {'size': [W, H], 'anchors': an}
    json.dump(res[v], open(os.path.join(OUT, f'v73_3d_{v}_anchors.json'), 'w'), indent=1)
    print('rendered', v, len(an), 'anchors', flush=True)
