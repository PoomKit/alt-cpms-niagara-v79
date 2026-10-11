"""V7.4 equipment models (bpy) built on assets73 primitives.  Form factors follow the real product families named by the user
(ONICON insertion magnetic flow meter + System-10 style BTU calculator, Mitsubishi ME96SS panel multi-meter, ABB ACH580 wall-mount
HVAC drive, outdoor T/RH transmitter in a multi-plate radiation shield, RTD with DIN head, pressure transmitter with isolation
valve).  ORIGINAL geometry only: no logos, no brand wordmarks, no photographs.  Units: metres, front of every device = -y."""
import math
import bpy
from mathutils import Vector
import assets73 as A
from assets73 import mat, cyl, cyl_dir, box, sphere, torus, AX


def M4():
    m = A.M()
    m.update(
        alu=mat('alu', (0.70, 0.72, 0.74), metal=0.85, rough=0.32),
        alu_dark=mat('alu_dark', (0.42, 0.44, 0.47), metal=0.8, rough=0.38),
        ss=mat('ss', (0.78, 0.79, 0.80), metal=0.95, rough=0.18),
        head_grey=mat('head_grey', (0.55, 0.58, 0.61), metal=0.55, rough=0.35, coat=0.3),
        head_blue=mat('head_blue', (0.20, 0.33, 0.52), metal=0.35, rough=0.35, coat=0.4),
        gland=mat('gland', (0.03, 0.03, 0.035), rough=0.5),
        lever_red=mat('lever_red', (0.75, 0.06, 0.05), rough=0.4, coat=0.4),
        enc_grey=mat('enc_grey', (0.60, 0.62, 0.64), metal=0.25, rough=0.38, coat=0.25),
        enc_light=mat('enc_light', (0.84, 0.85, 0.86), rough=0.42),
        drive_white=mat('drive_white', (0.90, 0.905, 0.91), rough=0.36, coat=0.25),
        drive_grey=mat('drive_grey', (0.30, 0.31, 0.33), metal=0.3, rough=0.45),
        fin=mat('fin', (0.34, 0.36, 0.38), metal=0.85, rough=0.35),
        panel_black=mat('panel_black', (0.03, 0.03, 0.035), rough=0.35, coat=0.4),
        screen=mat('screen', (0.02, 0.05, 0.08), emit=(0.35, 0.65, 1.0), es=1.4),
        screen_off=mat('screen_off', (0.03, 0.04, 0.05), rough=0.2),
        key=mat('key', (0.18, 0.19, 0.21), rough=0.4),
        key_green=mat('key_green', (0.10, 0.55, 0.20), rough=0.4),
        key_red=mat('key_red', (0.70, 0.10, 0.08), rough=0.4),
        lcd_white=mat('lcd_white', (0.80, 0.86, 0.84), emit=(0.85, 0.95, 0.90), es=0.6),
        bezel=mat('bezel', (0.08, 0.085, 0.09), rough=0.45),
        shield=mat('shield', (0.93, 0.93, 0.91), rough=0.5),
        bracket=mat('bracket', (0.55, 0.57, 0.60), metal=0.8, rough=0.35),
        amber=mat('amber', (0.95, 0.60, 0.05), emit=(1.0, 0.6, 0.05), es=4.0),
    )
    return m


def _hex(p, r, depth, axis, m):
    return cyl(p, r, depth, axis, m, verts=6)


# ------------------------------------------------------------------------ temperature transmitter (RTD + thermowell + DIN head)
def rtd(p, up='z', mm=None, s=1.0):
    """1/2" thermowell, hex bushing, lagging extension, DIN form-B aluminium head with screw lid and cable gland."""
    mm = mm or M4(); p = Vector(p); u = AX(up)
    ax = up.lstrip('-')
    _hex(p + u * 0.03 * s, 0.032 * s, 0.03 * s, ax, mm['ss'])                 # hex bushing on the pipe boss
    cyl_dir(p + u * 0.045 * s, p + u * 0.14 * s, 0.012 * s, mm['ss'])          # extension nipple
    _hex(p + u * 0.15 * s, 0.022 * s, 0.02 * s, ax, mm['ss'])                  # union nut
    h = p + u * 0.215 * s
    cyl(h, 0.046 * s, 0.075 * s, ax, mm['alu'], 36)                           # head body
    cyl(h + u * 0.045 * s, 0.048 * s, 0.018 * s, ax, mm['head_blue'], 36)     # screw lid
    cyl(h + u * 0.058 * s, 0.03 * s, 0.01 * s, ax, mm['head_blue'], 24)       # lid boss
    side = Vector((1, 0, 0)) if ax != 'x' else Vector((0, 0, 1))
    cyl_dir(h + side * 0.04 * s, h + side * 0.075 * s, 0.013 * s, mm['gland'])  # cable gland
    cyl_dir(h + side * 0.075 * s, h + side * 0.16 * s, 0.006 * s, mm['cable'])
    return h + u * 0.07 * s


# ------------------------------------------------------------------------ pressure transmitter + isolation ball valve + snubber
def ptx(p, up='z', mm=None, s=1.0):
    mm = mm or M4(); p = Vector(p); u = AX(up); ax = up.lstrip('-')
    cyl_dir(p, p + u * 0.05 * s, 0.012 * s, mm['brass'])                      # nipple
    b = p + u * 0.075 * s
    cyl(b, 0.024 * s, 0.05 * s, ax, mm['brass'], 24)                          # ball valve body
    lever_dir = Vector((1, 0, 0)) if ax != 'x' else Vector((0, 0, 1))
    box(b + lever_dir * 0.055 * s - Vector((0, 0.012 * s, 0)), (0.09 * s, 0.012 * s, 0.012 * s) if ax != 'x' else (0.012 * s, 0.012 * s, 0.09 * s), mm['lever_red'], 0.003)
    cyl_dir(b + u * 0.025 * s, b + u * 0.06 * s, 0.01 * s, mm['ss'])           # snubber
    _hex(b + u * 0.07 * s, 0.02 * s, 0.018 * s, ax, mm['ss'])                 # process hex
    c = b + u * 0.135 * s
    cyl(c, 0.0175 * s, 0.10 * s, ax, mm['ss'], 32)                           # transmitter body
    cyl(c + u * 0.054 * s, 0.019 * s, 0.01 * s, ax, mm['alu_dark'], 32)       # ring
    k = c + u * 0.085 * s                                                      # DIN 43650 plug
    box(k, (0.042 * s, 0.03 * s, 0.05 * s) if ax == 'z' else ((0.05 * s, 0.03 * s, 0.042 * s) if ax == 'x' else (0.042 * s, 0.05 * s, 0.03 * s)), mm['gland'], 0.004)
    box(k - Vector((0, 0.0155 * s, 0)), (0.02 * s, 0.002, 0.02 * s) if ax != 'y' else (0.02 * s, 0.002, 0.02 * s), mm['key'])
    cyl_dir(k + u * 0.028 * s, k + u * 0.05 * s, 0.008 * s, mm['gland'])
    return k + u * 0.05 * s


# ------------------------------------------------------------------------ butterfly valve: sectioned body shows the disc angle
def bfv4(p, axis, r=0.085, mode='onoff', up='z', open_frac=0.0, mm=None, handwheel=False, moving=False):
    """lug butterfly valve + quarter-turn actuator.  The front half of the body is cut away (section view) so the disc angle
    is visible; the yellow position arrow on top turns 0..90 deg with it."""
    mm = mm or M4()
    p = Vector(p); a = AX(axis); u = AX(up)
    ang = open_frac * math.pi / 2
    # lug body + liner
    cyl_dir(p - a * 0.055, p + a * 0.055, r * 1.62, mm['vbody'], 40)
    cyl_dir(p - a * 0.062, p + a * 0.062, r * 1.2, mm['disc'], 40)
    w0 = (Vector((0, 0, 1)).cross(a) if axis.lstrip('-') != 'z' else Vector((1, 0, 0))).normalized()
    v0 = a.cross(w0).normalized()
    for k in range(4):                                                          # lug bolts
        t = k * math.pi / 2 + math.pi / 4
        q = p + (w0 * math.cos(t) + v0 * math.sin(t)) * r * 1.45
        cyl_dir(q - a * 0.075, q + a * 0.075, 0.01, mm['steel'], 12)
    top = p + u * (r * 1.62)
    cyl_dir(top, top + u * 0.10, 0.03, mm['steel'])                            # neck
    sz = lambda s1, s2: (s1, s1, s2) if up.endswith('z') else ((s2, s1, s1) if up.endswith('x') else (s1, s2, s1))
    box(top + u * 0.12, sz(0.15, 0.04), mm['steel'])                           # ISO 5211 plate
    if handwheel:
        box(top + u * 0.19, sz(0.14, 0.10), mm['act_body'], 0.01)
        c = top + u * 0.19 - Vector((0, 0.12, 0))
        torus(c, 0.10, 0.011, 'y', mm['steel']); cyl_dir(c, c + Vector((0, 0.05, 0)), 0.014, mm['steel'])
        return {'top': top + u * 0.3}
    act = mm['act_mod'] if mode == 'mod' else mm['act_onoff']
    c = top + u * 0.24
    box(c, sz(0.26, 0.20) if not up.endswith('y') else (0.26, 0.2, 0.26), act, 0.03)
    if not up.endswith('y'):
        box(c - Vector((0, 0.131, 0)), (0.15, 0.004, 0.08) if up.endswith('z') else (0.08, 0.004, 0.15), mm['act_body'])   # plate
        box(c - Vector((0, 0.132, 0)) + (Vector((0.09, 0, 0.0)) if up.endswith('z') else Vector((0, 0, -0.09))),
            (0.018, 0.004, 0.018), mm['amber'] if moving else mm['led_off'])                                            # motor LED
    dome = c + u * 0.10
    cyl_dir(dome, dome + u * 0.05, 0.055, mm['glass'], 28)                      # clear indicator dome
    # position arrow: rotates with the disc (0 = across the pipe = closed, 90 = along the pipe = open)
    from mathutils import Quaternion as Q
    w = (Vector((0, 0, 1)).cross(a) if axis.lstrip('-') != 'z' else Vector((1, 0, 0))).normalized()
    arrow_dir = Q(u, ang) @ w
    ctr = dome + u * 0.04
    cyl_dir(ctr - arrow_dir * 0.045, ctr + arrow_dir * 0.03, 0.009, mm['indicator'], 10)
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=0.022, radius2=0.0, depth=0.035, location=ctr + arrow_dir * 0.045)
    cone = bpy.context.object; cone.rotation_mode = 'QUATERNION'; cone.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(arrow_dir)
    cone.data.materials.append(mm['indicator'])
    return {'top': dome + u * 0.06}


# ------------------------------------------------------------------------ insertion electromagnetic flow meter (ONICON F-3500 form)
def ins_magmeter(p, up='z', r=0.085, mm=None, s=1.0):
    """hot-tap insertion magmeter: weld-o-let + 1" full-port ball valve + stainless probe stem with depth scale + cast electronics
    housing (dual cable glands) on top.  p = pipe centre."""
    mm = mm or M4(); p = Vector(p); u = AX(up); ax = up.lstrip('-')
    base = p + u * r
    cyl_dir(base - u * 0.01, base + u * 0.04 * s, 0.028 * s, mm['steel'])         # weld-o-let
    b = base + u * 0.075 * s
    cyl(b, 0.038 * s, 0.07 * s, ax, mm['brass'], 28)                            # isolation ball valve
    ld = Vector((1, 0, 0)) if ax != 'x' else Vector((0, 0, 1))
    box(b + ld * 0.075 * s - Vector((0, 0.02 * s, 0)), (0.13 * s, 0.014 * s, 0.014 * s) if ax != 'x' else (0.014 * s, 0.014 * s, 0.13 * s), mm['lever_red'], 0.004)
    _hex(b + u * 0.05 * s, 0.03 * s, 0.03 * s, ax, mm['ss'])                    # packing gland
    cyl_dir(b + u * 0.065 * s, b + u * 0.24 * s, 0.013 * s, mm['ss'])           # probe stem
    for k in range(5):                                                           # depth scale marks
        q = b + u * (0.09 + k * 0.03) * s
        cyl_dir(q, q + u * 0.003, 0.0145 * s, mm['dark'], 12)
    h = b + u * 0.31 * s
    box(h, (0.15 * s, 0.11 * s, 0.13 * s) if ax == 'z' else ((0.13 * s, 0.11 * s, 0.15 * s) if ax == 'x' else (0.15 * s, 0.13 * s, 0.11 * s)),
        mm['enc_grey'], 0.018 * s)                                              # electronics housing
    box(h - Vector((0, 0.056 * s, 0)), (0.11 * s, 0.004, 0.085 * s) if ax != 'x' else (0.085 * s, 0.004, 0.11 * s), mm['head_blue'], 0.004)  # lid
    box(h - Vector((0, 0.059 * s, 0)) + u * 0.012 * s, (0.06 * s, 0.003, 0.03 * s) if ax != 'x' else (0.03 * s, 0.003, 0.06 * s), mm['lcd'])  # display
    side = Vector((1, 0, 0)) if ax != 'x' else Vector((0, 0, 1))
    for k in (-1, 1):
        g = h + side * 0.075 * s * k - u * 0.03 * s
        cyl_dir(g, g + side * 0.02 * s * k, 0.011 * s, mm['gland'], 16)
    return {'head': h, 'top': h + u * 0.07 * s}


# ------------------------------------------------------------------------ BTU calculator (System-10 style wall enclosure)
def btu_system10(p, mm=None, s=1.0):
    mm = mm or M4(); x, y, z = p
    box((x, y, z), (0.30 * s, 0.10 * s, 0.38 * s), mm['enc_light'], 0.02 * s)            # enclosure
    box((x, y - 0.051 * s, z), (0.285 * s, 0.004, 0.365 * s), mm['enc_light'], 0.012 * s)  # door
    box((x, y - 0.054 * s, z + 0.09 * s), (0.20 * s, 0.004, 0.08 * s), mm['bezel'], 0.004)  # display bezel
    box((x, y - 0.057 * s, z + 0.09 * s), (0.17 * s, 0.003, 0.055 * s), mm['lcd_white'])   # 2-line LCD
    for i in range(2):
        for j in range(3):
            box((x - 0.06 * s + j * 0.06 * s, y - 0.056 * s, z - 0.02 * s - i * 0.045 * s), (0.04 * s, 0.004, 0.028 * s), mm['key'], 0.003)
    for k, xx in enumerate((-0.09, -0.03, 0.03, 0.09)):                                   # bottom cable glands
        cyl((x + xx * s, y, z - 0.2 * s), 0.012 * s, 0.03 * s, 'z', mm['gland'], 16)
    for sx in (-1, 1): box((x + sx * 0.16 * s, y + 0.02 * s, z + 0.17 * s), (0.03 * s, 0.02 * s, 0.03 * s), mm['steel'])  # mounting ears
    return {'cables': [(x + xx * s, y, z - 0.215 * s) for xx in (-0.09, -0.03, 0.03, 0.09)]}


# ------------------------------------------------------------------------ panel multi-meter (Mitsubishi ME96SS form: 96 x 96 mm)
def me96(p, mm=None, s=1.0, panel=True):
    """96 x 96 mm DIN panel meter on a grey MCC door: black bezel, backlit segment LCD (4 lines), 4 keys under the display."""
    mm = mm or M4(); x, y, z = p
    if panel:
        box((x, y + 0.02 * s, z), (0.24 * s, 0.02 * s, 0.24 * s), mm['enc_grey'], 0.01 * s)     # door section
    box((x, y - 0.004 * s, z), (0.096 * s, 0.012 * s, 0.096 * s), mm['bezel'], 0.004 * s)       # bezel
    box((x, y - 0.0105 * s, z + 0.012 * s), (0.078 * s, 0.002, 0.056 * s), mm['lcd_white'])       # LCD window
    for i in range(4):                                                                           # segment rows (dark digits)
        box((x + 0.004 * s, y - 0.0118 * s, z + 0.032 * s - i * 0.0135 * s), (0.05 * s, 0.001, 0.007 * s), mm['dark'])
        box((x - 0.031 * s, y - 0.0118 * s, z + 0.032 * s - i * 0.0135 * s), (0.01 * s, 0.001, 0.005 * s), mm['dark'])
    for j in range(4):
        box((x - 0.03 * s + j * 0.02 * s, y - 0.0115 * s, z - 0.032 * s), (0.013 * s, 0.003, 0.009 * s), mm['key'], 0.002 * s)
    box((x + 0.036 * s, y - 0.0112 * s, z - 0.044 * s), (0.006 * s, 0.002, 0.004 * s), mm['led_g'])   # comm LED
    return {'c': (x, y, z)}


# ------------------------------------------------------------------------ wall-mount HVAC drive (ABB ACH580 form)
def ach580(p, mm=None, s=1.0, running=True):
    """IP21 wall-mount frame: white front with rounded edges, dark grey heatsink sides, control-panel holder near the top with
    the assistant panel (colour display + keypad), lower cable-entry cover with a horizontal parting line, glands underneath."""
    mm = mm or M4(); x, y, z = p; W, D, H = 0.26 * s, 0.24 * s, 0.56 * s
    box((x, y + 0.01 * s, z + H / 2), (W - 0.01 * s, D - 0.02 * s, H), mm['drive_grey'], 0.01 * s)           # chassis / heatsink
    for k in range(9):                                                                                 # side fins
        for sx in (-1, 1):
            box((x + sx * (W / 2 - 0.002), y + 0.03 * s, z + 0.08 * s + k * 0.05 * s), (0.006, D - 0.08 * s, 0.03 * s), mm['fin'])
    box((x, y - D / 2 + 0.03 * s, z + H * 0.56), (W, 0.06 * s, H * 0.86), mm['drive_white'], 0.025 * s)   # front cover
    box((x, y - D / 2 + 0.03 * s, z + H * 0.075), (W * 0.98, 0.055 * s, H * 0.13), mm['drive_white'], 0.02 * s)  # lower cover
    box((x, y - D / 2 - 0.001, z + H * 0.145), (W * 0.9, 0.004, 0.004), mm['drive_grey'])               # parting line
    ph = (x, y - D / 2 - 0.004, z + H * 0.74)                                                          # panel holder recess
    box(ph, (0.13 * s, 0.01, 0.19 * s), mm['drive_grey'], 0.01 * s)
    pp = (x, y - D / 2 - 0.012, z + H * 0.74)                                                          # assistant panel
    box(pp, (0.105 * s, 0.018 * s, 0.165 * s), mm['panel_black'], 0.012 * s)
    box((x, pp[1] - 0.0095 * s, z + H * 0.785), (0.084 * s, 0.002, 0.058 * s), mm['screen'] if running else mm['screen_off'])  # colour display
    for i, (dx, dz, mk) in enumerate(((-0.03, -0.02, 'key'), (0.03, -0.02, 'key'), (0, -0.02, 'key'), (0, -0.04, 'key'),
                                     (-0.03, -0.06, 'key_green'), (0.03, -0.06, 'key_red'))):
        box((x + dx * s, pp[1] - 0.0095 * s, z + H * 0.74 + dz * s), (0.02 * s, 0.003, 0.012 * s), mm[mk], 0.002)
    box((x + 0.045 * s, pp[1] - 0.0095 * s, z + H * 0.83), (0.008 * s, 0.002, 0.008 * s), mm['led_g'] if running else mm['led_off'])
    for k in range(4):                                                                                 # cable glands
        cyl((x - 0.08 * s + k * 0.053 * s, y - 0.02 * s, z - 0.012 * s), 0.013 * s, 0.03 * s, 'z', mm['gland'], 16)
    for dz in (0.02, H - 0.02):                                                                        # mounting lugs
        for sx in (-1, 1): box((x + sx * 0.1 * s, y + D / 2 - 0.01 * s, z + dz), (0.03 * s, 0.01 * s, 0.03 * s), mm['steel'])
    return {'top': (x, y, z + H), 'front': (x, y - D / 2, z + H / 2)}


# ------------------------------------------------------------------------ outdoor T/RH transmitter in a multi-plate radiation shield
def oa_shield(p, mm=None, s=1.0, pole=True):
    mm = mm or M4(); x, y, z = p
    if pole:
        cyl((x - 0.22 * s, y + 0.02 * s, z + 0.55 * s), 0.024 * s, 1.1 * s, 'z', mm['bracket'], 20)             # mast
        for dz in (0.72, 0.9):                                                                                # U-bolts
            torus((x - 0.22 * s, y + 0.02 * s, z + dz * s), 0.03 * s, 0.004 * s, 'z', mm['steel'])
        box((x - 0.12 * s, y + 0.02 * s, z + 0.81 * s), (0.2 * s, 0.03 * s, 0.012 * s), mm['bracket'])       # arm
    top = z + 0.98 * s
    for k in range(10):                                                                                   # louvred plates
        zz = top - k * 0.026 * s
        cyl((x, y, zz), (0.085 - (0.012 if k == 0 else 0.0)) * s, 0.008 * s, 'z', mm['shield'], 40)
        cyl((x, y, zz - 0.006 * s), 0.078 * s, 0.006 * s, 'z', mm['shield'], 40, r2=0.07 * s)
    cyl((x, y, top + 0.012 * s), 0.03 * s, 0.014 * s, 'z', mm['shield'], 24)                             # cap
    cyl((x, y, top - 0.285 * s), 0.013 * s, 0.07 * s, 'z', mm['ss'], 16)                                  # probe tip below
    box((x, y, top - 0.36 * s), (0.08 * s, 0.05 * s, 0.1 * s), mm['enc_light'], 0.01 * s)                  # transmitter housing
    cyl((x, y, top - 0.425 * s), 0.009 * s, 0.03 * s, 'z', mm['gland'], 12)
    cyl_dir((x, y, top - 0.44 * s), (x - 0.22 * s, y, top - 0.44 * s), 0.004 * s, mm['cable'], 8)
    for sx in (-1, 1):                                                                                    # stand-off rods
        cyl_dir((x + sx * 0.05 * s, y, top - 0.26 * s), (x + sx * 0.05 * s, y, top), 0.004 * s, mm['steel'], 8)
    return {'top': (x, y, top + 0.02 * s)}
