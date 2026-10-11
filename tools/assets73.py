"""V7.3 Blender asset library (bpy): the plant equipment used by BOTH the isometric 3D pages and the 2-D sprites, so the
2-D schematic and the 3-D views show the same machines.  Original models (no vendor trade dress).
Units: metres. World: x right, y away from the viewer, z up.  Colour standard: CHWS blue, CHWR light blue, CDWS yellow,
CDWR orange, make-up water green, drain / bleed grey, chemical violet.  Valve actuators: red = on/off, green = modulating."""
import math
import bpy
from mathutils import Vector, Matrix

SVC = {'chws': (0.03, 0.22, 0.85), 'chwr': (0.22, 0.66, 0.95), 'cdws': (0.97, 0.74, 0.03), 'cdwr': (0.95, 0.36, 0.03),
       'mu': (0.16, 0.62, 0.30), 'drain': (0.42, 0.44, 0.46), 'chem': (0.55, 0.30, 0.78), 'steelp': (0.45, 0.47, 0.5)}
MATS = {}


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    MATS.clear()


def mat(name, rgb, metal=0.0, rough=0.45, emit=None, es=3.0, alpha=1.0, coat=0.0):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1)
    b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    if coat:
        try: b.inputs['Coat Weight'].default_value = coat
        except Exception: pass
    if emit:
        b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = es
    if alpha < 1.0:
        b.inputs['Alpha'].default_value = alpha
        try: m.blend_method = 'BLEND'
        except Exception: pass
    MATS[name] = m
    return m


def M():
    """shared materials"""
    return dict(
        shell=mat('shell', (0.80, 0.82, 0.84), metal=0.35, rough=0.28, coat=0.3),
        shell2=mat('shell2', (0.62, 0.65, 0.68), metal=0.3, rough=0.35),
        steel=mat('steel', (0.40, 0.42, 0.45), metal=0.85, rough=0.32),
        dark=mat('dark', (0.05, 0.055, 0.06), rough=0.55),
        paint_blue=mat('paint_blue', (0.07, 0.24, 0.55), metal=0.3, rough=0.32, coat=0.4),
        motor=mat('motor', (0.12, 0.30, 0.52), metal=0.35, rough=0.3, coat=0.4),
        motor_run=mat('motor_run', (0.10, 0.45, 0.30), metal=0.35, rough=0.3, coat=0.4),
        base=mat('base', (0.18, 0.19, 0.21), metal=0.6, rough=0.45),
        frp=mat('frp', (0.55, 0.58, 0.60), metal=0.05, rough=0.55),
        frp_dark=mat('frp_dark', (0.30, 0.33, 0.35), metal=0.05, rough=0.6),
        louvre=mat('louvre', (0.10, 0.11, 0.12), rough=0.7),
        concrete=mat('concrete', (0.22, 0.23, 0.24), rough=0.9),
        floor=mat('floor', (0.035, 0.04, 0.045), rough=0.85),
        grid=mat('grid', (0.07, 0.08, 0.09), rough=0.9),
        brass=mat('brass', (0.72, 0.52, 0.18), metal=0.9, rough=0.3),
        bronze=mat('bronze', (0.55, 0.36, 0.16), metal=0.85, rough=0.35),
        act_onoff=mat('act_onoff', (0.72, 0.07, 0.06), metal=0.15, rough=0.35, coat=0.5),
        act_mod=mat('act_mod', (0.08, 0.52, 0.24), metal=0.15, rough=0.35, coat=0.5),
        act_body=mat('act_body', (0.16, 0.17, 0.19), metal=0.4, rough=0.4),
        indicator=mat('indicator', (0.95, 0.78, 0.10), rough=0.3),
        vbody=mat('vbody', (0.14, 0.15, 0.17), metal=0.6, rough=0.35),
        disc=mat('disc', (0.7, 0.72, 0.74), metal=0.9, rough=0.2),
        meter=mat('meter', (0.10, 0.28, 0.52), metal=0.4, rough=0.3, coat=0.3),
        meter_head=mat('meter_head', (0.78, 0.80, 0.82), metal=0.2, rough=0.3),
        lcd=mat('lcd', (0.02, 0.08, 0.10), emit=(0.25, 0.85, 1.0), es=1.6),
        hmi=mat('hmi', (0.03, 0.12, 0.25), emit=(0.15, 0.45, 0.95), es=1.8),
        led_g=mat('led_g', (0.1, 0.8, 0.3), emit=(0.1, 1.0, 0.3), es=5.0),
        led_off=mat('led_off', (0.15, 0.17, 0.18), rough=0.4),
        white_poly=mat('white_poly', (0.88, 0.88, 0.84), rough=0.5),
        chem_liquid=mat('chem_liquid', (0.55, 0.30, 0.78), rough=0.2, alpha=0.8),
        tank_blue=mat('tank_blue', (0.10, 0.30, 0.62), metal=0.3, rough=0.3, coat=0.4),
        gauge_face=mat('gauge_face', (0.95, 0.95, 0.93), rough=0.3),
        glass=mat('glass', (0.7, 0.85, 0.95), rough=0.05, alpha=0.35),
        water=mat('water', (0.10, 0.35, 0.45), rough=0.05, alpha=0.8),
        fan_blade=mat('fan_blade', (0.30, 0.32, 0.35), metal=0.7, rough=0.3),
        blur=mat('blur', (0.35, 0.37, 0.40), metal=0.5, rough=0.4, alpha=0.55),
        cable=mat('cable', (0.02, 0.02, 0.02), rough=0.6),
        wall=mat('wall', (0.16, 0.20, 0.26), rough=0.7),
        rail=mat('rail', (0.85, 0.72, 0.10), metal=0.3, rough=0.4),
    )


# ------------------------------------------------------------------------ primitives (world coordinates)
def _fin(o, m, smooth=True):
    o.data.materials.append(m)
    if smooth:
        for p in o.data.polygons: p.use_smooth = len(p.vertices) == 4
    return o


def cyl(p, r, depth, axis='z', m=None, verts=40, r2=None, open_ends=False):
    rot = {'x': (0, math.pi / 2, 0), 'y': (math.pi / 2, 0, 0), 'z': (0, 0, 0)}[axis]
    fill = 'NOTHING' if open_ends else 'NGON'
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=p, rotation=rot, end_fill_type=fill)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=depth, location=p, rotation=rot, end_fill_type=fill)
    if open_ends:
        md = bpy.context.object.modifiers.new('s', 'SOLIDIFY'); md.thickness = 0.03
    return _fin(bpy.context.object, m)


def cyl_dir(a, b, r, m, verts=28):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d.length, location=(a + b) / 2)
    o = bpy.context.object; o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    return _fin(o, m)


def box(p, s, m, bevel=0.0, rotz=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=p)
    o = bpy.context.object; o.scale = s; o.rotation_euler = (0, 0, rotz)
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        md = o.modifiers.new('b', 'BEVEL'); md.width = bevel; md.segments = 3
    o.data.materials.append(m)
    return o


def sphere(p, r, m, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=p, segments=28, ring_count=14)
    o = bpy.context.object; o.scale = scale
    return _fin(o, m)


def torus(p, R, r, axis='z', m=None):
    rot = {'x': (0, math.pi / 2, 0), 'y': (math.pi / 2, 0, 0), 'z': (0, 0, 0)}[axis]
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=p, rotation=rot, major_segments=32, minor_segments=10)
    return _fin(bpy.context.object, m)


def AX(axis):
    if axis.startswith('-'): return -AX(axis[1:])
    return {'x': Vector((1, 0, 0)), 'y': Vector((0, 1, 0)), 'z': Vector((0, 0, 1))}[axis]


# ------------------------------------------------------------------------ pipes
def pipe(pts, svc, r=0.16, flanges=True, mm=None):
    m = mat('pipe_' + svc, SVC[svc], metal=0.25, rough=0.26, coat=0.5)
    fl = mat('flange', (0.25, 0.27, 0.30), metal=0.8, rough=0.35)
    for a, b in zip(pts, pts[1:]):
        if (Vector(b) - Vector(a)).length > 1e-6: cyl_dir(a, b, r, m)
    for q in pts[1:-1]: sphere(q, r * 1.02, m)
    if flanges:
        for q, nxt in ((pts[0], pts[1]), (pts[-1], pts[-2])):
            d = (Vector(nxt) - Vector(q)).normalized()
            c = Vector(q) + d * 0.04
            cyl_dir(c - d * 0.03, c + d * 0.03, r * 1.5, fl)


# ------------------------------------------------------------------------ valves / instruments
def butterfly(p, axis, r=0.16, mode='onoff', up='z', mm=None, handwheel=False):
    """wafer butterfly valve on a pipe (axis) with an electric actuator (on/off red / modulating green) or a gear + handwheel."""
    mm = mm or M()
    p = Vector(p); a = AX(axis); u = AX(up)
    cyl_dir(p - a * 0.07, p + a * 0.07, r * 1.55, mm['vbody'])                  # wafer body
    cyl_dir(p - a * 0.078, p + a * 0.078, r * 1.25, mm['disc'])                 # liner / disc edge
    top = p + u * (r * 1.55)
    cyl_dir(top, top + u * 0.14, 0.035, mm['steel'])                            # neck
    sz = lambda a, b: (a, a, b) if up.endswith('z') else ((b, a, a) if up.endswith('x') else (a, b, a))
    box(top + u * 0.17, sz(0.16, 0.05), mm['steel'])                            # mounting plate
    if handwheel:
        box(top + u * 0.24, sz(0.15, 0.12), mm['act_body'], 0.01)
        c = top + u * 0.24 - Vector((0, 0.13, 0)) if not up.endswith('y') else top + u * 0.36
        torus(c, 0.11, 0.012, 'y', mm['steel']); cyl_dir(c, c + Vector((0, 0.06, 0)), 0.015, mm['steel'])
        return top + u * 0.34
    act = mm['act_mod'] if mode == 'mod' else mm['act_onoff']
    c = top + u * 0.30
    box(c, (0.30, 0.22, 0.22) if up.endswith('z') else ((0.22, 0.22, 0.30) if up.endswith('x') else (0.30, 0.22, 0.22)), act, 0.025)
    if not up.endswith('y'):
        box(c - Vector((0, 0.112, 0)), (0.18, 0.004, 0.10) if up.endswith('z') else (0.10, 0.004, 0.18), mm['act_body'])   # label plate
    cyl_dir(c + u * 0.11, c + u * 0.16, 0.06, mm['indicator'], 24)             # position indicator dome
    return c + u * 0.18


def gate_valve(p, axis, r=0.08, mm=None, up='z'):
    mm = mm or M(); p = Vector(p); a = AX(axis); u = AX(up)
    cyl_dir(p - a * 0.12, p + a * 0.12, r * 1.35, mm['bronze'])
    sphere(p, r * 1.6, mm['bronze'])
    cyl_dir(p, p + u * 0.28, r * 0.55, mm['bronze'])
    torus(p + u * 0.30, 0.1, 0.012, up.lstrip('-'), mm['act_onoff'])
    return p + u * 0.32


def check_valve(p, axis, r=0.16, mm=None):
    mm = mm or M(); p = Vector(p); a = AX(axis)
    cyl_dir(p - a * 0.1, p + a * 0.1, r * 1.5, mm['vbody'])
    box(p + Vector((0, 0, r * 1.5)), (0.16, 0.12, 0.08), mm['vbody'], 0.01)


def solenoid(p, axis, r=0.05, mm=None):
    mm = mm or M(); p = Vector(p); a = AX(axis)
    cyl_dir(p - a * 0.1, p + a * 0.1, r * 1.6, mm['brass'])
    box(p + Vector((0, 0, r * 2.2)), (0.1, 0.1, 0.1), mm['brass'], 0.01)
    cyl(p + Vector((0, 0, r * 2.2 + 0.1)), 0.055, 0.12, 'z', mm['dark'])
    box(p + Vector((0.07, 0, r * 2.2 + 0.1)), (0.04, 0.05, 0.05), mm['dark'])
    return p + Vector((0, 0, 0.3))


def magmeter(p, axis, r=0.16, mm=None, up='z'):
    """electromagnetic flow meter: flanged spool + transmitter head with display"""
    mm = mm or M(); p = Vector(p); a = AX(axis); u = AX(up)
    L = 0.42
    cyl_dir(p - a * L / 2, p + a * L / 2, r * 1.35, mm['meter'])
    for s in (-1, 1): cyl_dir(p + a * s * (L / 2 - 0.02), p + a * s * (L / 2 + 0.02), r * 1.6, mm['steel'])
    n = p + u * r * 1.35
    cyl_dir(n, n + u * 0.16, 0.05, mm['meter'])
    h = n + u * 0.26
    box(h, (0.22, 0.2, 0.2) if up == 'z' else (0.2, 0.2, 0.22), mm['meter_head'], 0.03)
    box(h - Vector((0, 0.102, 0)), (0.12, 0.004, 0.09) if up == 'z' else (0.09, 0.004, 0.12), mm['lcd'])
    return h + u * 0.12


def tt(p, up='z', mm=None):
    mm = mm or M(); p = Vector(p); u = AX(up)
    cyl_dir(p, p + u * 0.2, 0.018, mm['steel'])
    cyl(p + u * 0.26, 0.045, 0.1, up, mm['meter_head'], 20)
    return p + u * 0.32


def pt_gauge(p, up='z', mm=None):
    mm = mm or M(); p = Vector(p); u = AX(up)
    cyl_dir(p, p + u * 0.22, 0.016, mm['brass'])
    c = p + u * 0.32
    cyl(c, 0.085, 0.04, 'y', mm['steel'], 28)
    cyl(c - Vector((0, 0.021, 0)), 0.075, 0.004, 'y', mm['gauge_face'], 28)
    box(c - Vector((0, 0.025, -0.02)), (0.006, 0.002, 0.06), mm['act_onoff'])
    return c + u * 0.1


# ------------------------------------------------------------------------ equipment
def chiller(p, mm=None, running=True):
    """water-cooled centrifugal chiller, length along x.  Evaporator (lower) nozzles on the LEFT end (upper = CHW out,
    lower = CHW in); condenser (upper) nozzles on the RIGHT end (upper = CDW out, lower = CDW in).  Returns nozzle points."""
    mm = mm or M(); x, y, z = p
    ev_z, cd_z, L = z + 0.95, z + 2.05, 4.4
    cyl((x, y, ev_z), 0.62, L, 'x', mm['shell']); cyl((x, y + 0.05, cd_z), 0.52, L - 0.3, 'x', mm['shell'])
    for s in (-1, 1):
        cyl((x + s * (L / 2 + 0.1), y, ev_z), 0.66, 0.2, 'x', mm['paint_blue'])            # evaporator water boxes
        cyl((x + s * (L / 2 - 0.05), y + 0.05, cd_z), 0.56, 0.18, 'x', mm['paint_blue'])   # condenser water boxes
        for k in range(16):                                                                # bolt ring
            ang = k * math.tau / 16
            cyl((x + s * (L / 2 + 0.005), y + math.cos(ang) * 0.64, ev_z + math.sin(ang) * 0.64), 0.018, 0.05, 'x', mm['steel'], 8)
        for dx in (-1.6, 1.6): pass
    for dx in (-1.55, 1.55):
        cyl((x + dx, y, ev_z), 0.655, 0.06, 'x', mm['shell2'])
        box((x + dx, y, z + 0.2), (0.28, 1.5, 0.4), mm['base'], 0.02)                     # feet
    box((x, y, z + 0.04), (L + 0.6, 1.6, 0.08), mm['base'])                                # skid
    # compressor + motor + oil separator
    cyl((x + 0.5, y + 0.05, cd_z + 0.95), 0.44, 1.3, 'x', mm['shell2'])
    cyl((x - 0.45, y + 0.05, cd_z + 0.95), 0.36, 0.7, 'x', mm['motor_run'] if running else mm['motor'])
    cyl((x + 1.35, y + 0.05, cd_z + 0.95), 0.5, 0.25, 'x', mm['shell2'])
    cyl_dir((x - 0.8, y + 0.05, cd_z + 0.95), (x - 1.25, y + 0.05, cd_z + 0.95), 0.2, mm['steel'])
    cyl_dir((x - 1.25, y + 0.05, cd_z + 0.95), (x - 1.25, y + 0.05, ev_z + 0.45), 0.2, mm['steel'])   # suction line to evaporator
    sphere((x - 1.25, y + 0.05, cd_z + 0.95), 0.2, mm['steel'])
    # control panel + HMI
    box((x - 0.2, y - 0.78, z + 1.55), (1.3, 0.24, 1.05), mm['dark'], 0.03)
    box((x - 0.2, y - 0.905, z + 1.78), (0.4, 0.01, 0.24), mm['hmi'])
    box((x + 0.35, y - 0.905, z + 1.35), (0.05, 0.01, 0.05), mm['led_g'] if running else mm['led_off'])
    # nozzles
    noz = {}
    for side, zz, yy, key in ((-1, ev_z + 0.28, y - 0.25, 'chw_out'), (-1, ev_z - 0.28, y + 0.25, 'chw_in'),
                               (1, cd_z + 0.24, y - 0.2, 'cdw_out'), (1, cd_z - 0.24, y + 0.3, 'cdw_in')):
        base = x + side * (L / 2 + 0.2 if key.startswith('chw') else L / 2 + 0.04)
        tip = base + side * 0.45
        cyl_dir((base, yy, zz), (tip, yy, zz), 0.16, mm['paint_blue'])
        cyl_dir((tip - side * 0.03, yy, zz), (tip + side * 0.03, yy, zz), 0.24, mm['steel'])
        noz[key] = (tip, yy, zz)
    noz['top'] = (x, y, cd_z + 1.6); noz['panel'] = (x - 0.2, y - 0.9, z + 1.2)
    return noz


def pump(p, facing=1, mm=None, running=True, vertical_discharge=True):
    """horizontal end-suction pump on a base; suction points +x*facing (axial), discharge up."""
    mm = mm or M(); x, y, z = p; s = facing
    box((x, y, z + 0.12), (2.1, 0.85, 0.24), mm['base'], 0.02)
    for dx in (-0.8, 0.8): box((x + dx, y, z + 0.02), (0.3, 0.95, 0.04), mm['base'])
    cyl((x - s * 0.4, y, z + 0.64), 0.31, 0.95, 'x', mm['motor_run'] if running else mm['motor'])
    for k in range(10):                                                              # cooling fins
        cyl((x - s * (0.05 + k * 0.08), y, z + 0.64), 0.325, 0.02, 'x', mm['motor_run'] if running else mm['motor'], 32)
    cyl((x - s * 0.93, y, z + 0.64), 0.24, 0.12, 'x', mm['dark'])                   # fan cover
    box((x - s * 0.4, y, z + 0.33), (0.7, 0.55, 0.1), mm['base'])
    box((x - s * 0.4, y - 0.22, z + 0.98), (0.18, 0.14, 0.12), mm['dark'], 0.01)     # terminal box
    cyl((x + s * 0.28, y, z + 0.64), 0.14, 0.32, 'x', mm['indicator'])              # coupling guard (yellow)
    cyl((x + s * 0.7, y, z + 0.66), 0.38, 0.32, 'x', mm['paint_blue'])              # volute
    sphere((x + s * 0.7, y, z + 0.66), 0.3, mm['paint_blue'], (0.6, 1, 1))
    box((x + s * 0.7, y, z + 0.3), (0.35, 0.4, 0.3), mm['paint_blue'], 0.02)       # pedestal
    suc0 = (x + s * 0.86, y, z + 0.64); suc = (x + s * 1.18, y, z + 0.64)
    cyl_dir(suc0, suc, 0.16, mm['paint_blue']); cyl_dir((suc[0] - s * 0.03, y, suc[2]), (suc[0] + s * 0.03, y, suc[2]), 0.24, mm['steel'])
    dis0 = (x + s * 0.7, y, z + 0.9); dis = (x + s * 0.7, y, z + 1.3)
    cyl_dir(dis0, dis, 0.15, mm['paint_blue']); cyl_dir((dis[0], y, dis[2] - 0.03), (dis[0], y, dis[2] + 0.03), 0.23, mm['steel'])
    return {'suction': suc, 'discharge': dis, 'top': (x, y, z + 1.5), 'motor': (x - s * 0.4, y, z + 0.64)}


def tower(p, cells=2, mm=None, running=(True, True), deck_z=0.0, fan_angle=0.0, blur=None):
    """induced-draft cooling tower, `cells` fan cells along x (each 2.4 m wide, 3.6 m deep, 3.4 m casing), shared basin.
    Hot water inlet on the LEFT side (x-) top, cold water outlet on the LEFT side of the basin.  Returns anchors."""
    mm = mm or M(); x, y, z = p
    cw, dp, hh = 2.4, 3.6, 3.4
    W = cells * cw
    x0 = x - W / 2
    box((x, y, z + 0.35), (W + 0.2, dp + 0.2, 0.7), mm['frp_dark'], 0.03)                      # basin
    box((x, y, z + 0.72), (W + 0.26, dp + 0.26, 0.06), mm['steel'])                              # basin lip
    box((x, y, z + 0.75 + hh / 2), (W, dp, hh), mm['frp'], 0.04)                                  # casing
    for c in range(cells):                                                                         # air-inlet louvres (front + back)
        cx = x0 + cw * c + cw / 2
        for k in range(8):
            zz = z + 0.9 + k * 0.17
            for sy in (-1, 1): box((cx, y + sy * (dp / 2 + 0.015), zz), (cw - 0.25, 0.03, 0.08), mm['louvre'])
        for k in range(5):                                                                         # casing panel seams
            box((x0 + cw * c + 0.3 + k * 0.45, y - dp / 2 - 0.01, z + 0.75 + 1.95 + hh / 3), (0.015, 0.01, hh * 0.5), mm['frp_dark'])
    for k in range(8):                                                                             # end louvres
        zz = z + 0.9 + k * 0.17
        for sx in (-1, 1): box((x + sx * (W / 2 + 0.015), y, zz), (0.03, dp - 0.25, 0.08), mm['louvre'])
    for c in range(1, cells): box((x0 + cw * c, y - dp / 2 - 0.02, z + 0.75 + hh / 2), (0.06, 0.03, hh), mm['frp_dark'])   # cell partition
    top = z + 0.75 + hh
    box((x, y, top + 0.05), (W + 0.05, dp + 0.05, 0.1), mm['steel'])                              # fan deck
    anchors = {}
    for c in range(cells):
        cx = x0 + cw * c + cw / 2
        cyl((cx, y, top + 0.45), 1.02, 0.8, 'z', mm['frp'], 56, r2=1.1, open_ends=True)          # fan stack (flared, open)
        cyl((cx, y, top + 0.45), 0.98, 0.78, 'z', mm['dark'], 56, r2=1.06, open_ends=True)       # stack inside (dark)
        torus((cx, y, top + 0.85), 1.1, 0.04, 'z', mm['frp_dark'])
        cyl((cx, y, top + 0.1), 0.99, 0.02, 'z', mm['dark'], 56)
        run = running[c] if c < len(running) else True
        if run and blur:
            cyl((cx, y, top + 0.8), 0.95, 0.01, 'z', mm['blur'], 56)                              # motion-blurred rotor
        else:
            for a in range(6):
                ang = a * math.tau / 6 + fan_angle + c * 0.4
                box((cx + math.cos(ang) * 0.49, y + math.sin(ang) * 0.49, top + 0.8), (0.92, 0.2, 0.025), mm['fan_blade'], rotz=ang + 0.25)
        cyl((cx, y, top + 0.8), 0.17, 0.1, 'z', mm['steel'])
        for g in range(5):                                                                         # fan guard (open mesh)
            box((cx - 0.8 + g * 0.4, y, top + 0.88), (0.008, 2.0, 0.008), mm['steel'])
        box((cx + 1.0, y - 1.3, top + 0.35), (0.3, 0.3, 0.5), mm['motor_run'] if run else mm['motor'], 0.02)   # external motor
        anchors[f'cell{c + 1}'] = (cx, y, top + 1.0)
        anchors[f'cell{c + 1}_front'] = (cx, y - dp / 2, z + 1.8)
    for sx in (-1, 1):                                                                             # handrail
        box((x + sx * W / 2, y, top + 1.1), (0.04, dp, 0.04), mm['rail'])
    box((x, y - dp / 2, top + 1.1), (W, 0.04, 0.04), mm['rail']); box((x, y + dp / 2, top + 1.1), (W, 0.04, 0.04), mm['rail'])
    for k in range(int(W / 1.2) + 1):
        box((x0 + k * 1.2, y - dp / 2, top + 0.6), (0.04, 0.04, 1.0), mm['rail'])
    # ladder on the right end
    for s in (-0.25, 0.25): box((x + W / 2 + 0.15, y + s, z + 2.4), (0.04, 0.04, 4.6), mm['rail'])
    for k in range(14): box((x + W / 2 + 0.15, y, z + 0.4 + k * 0.32), (0.04, 0.5, 0.03), mm['rail'])
    # hot water inlet header (top, left end) and basin outlet (left end, bottom)
    anchors['inlet'] = (x0 - 0.35, y - 0.6, top - 0.3)
    cyl_dir((x0 - 0.35, y - 0.6, top - 0.3), (x0, y - 0.6, top - 0.3), 0.16, mm['steel'])
    anchors['outlet'] = (x0 - 0.35, y + 0.6, z + 0.35)
    cyl_dir((x0 - 0.35, y + 0.6, z + 0.35), (x0 - 0.1, y + 0.6, z + 0.35), 0.18, mm['frp_dark'])
    anchors['makeup'] = (x + W / 2 + 0.1, y + 1.2, z + 0.6)
    anchors['basin_front'] = (x, y - dp / 2 - 0.1, z + 0.35)
    anchors['top'] = (x, y, top + 1.3)
    # level transmitter (stilling well) + float on the basin front
    cyl((x0 + 0.5, y - dp / 2 - 0.2, z + 0.9), 0.07, 1.2, 'z', mm['steel'])
    box((x0 + 0.5, y - dp / 2 - 0.2, z + 1.55), (0.16, 0.16, 0.14), mm['meter_head'], 0.02)
    anchors['lt'] = (x0 + 0.5, y - dp / 2 - 0.2, z + 1.6)
    return anchors


def vsd(p, mm=None, running=True, rotz=0.0, scale=1.0):
    """wall / stand mounted variable speed drive cabinet (original design), front towards -y."""
    mm = mm or M(); x, y, z = p; s = scale
    box((x, y, z + 0.5 * s), (0.5 * s, 0.3 * s, 1.0 * s), mm['meter_head'], 0.02)
    box((x, y - 0.151 * s, z + 0.7 * s), (0.22 * s, 0.01, 0.2 * s), mm['dark'], 0.01)
    box((x, y - 0.158 * s, z + 0.75 * s), (0.17 * s, 0.004, 0.07 * s), mm['lcd'])
    box((x + 0.08 * s, y - 0.158 * s, z + 0.64 * s), (0.02 * s, 0.004, 0.02 * s), mm['led_g'] if running else mm['led_off'])
    for k in range(6): box((x, y - 0.152 * s, z + (0.12 + k * 0.04) * s), (0.3 * s, 0.004, 0.012 * s), mm['dark'])
    box((x, y - 0.152 * s, z + 0.47 * s), (0.44 * s, 0.004, 0.012 * s), mm['paint_blue'])
    return (x, y - 0.16 * s, z + 1.05 * s)


def exp_tank(p, mm=None, r=0.35, h=1.1):
    mm = mm or M(); x, y, z = p
    cyl((x, y, z + 0.3 + h / 2), r, h, 'z', mm['tank_blue'])
    sphere((x, y, z + 0.3 + h), r, mm['tank_blue'], (1, 1, 0.45)); sphere((x, y, z + 0.3), r, mm['tank_blue'], (1, 1, 0.45))
    for a in range(3):
        ang = a * math.tau / 3
        box((x + math.cos(ang) * r * 0.8, y + math.sin(ang) * r * 0.8, z + 0.15), (0.05, 0.05, 0.3), mm['steel'])
    box((x, y - r - 0.01, z + 0.3 + h * 0.6), (0.2, 0.01, 0.1), mm['white_poly'])
    return {'bottom': (x, y, z + 0.1), 'top': (x, y, z + 0.3 + h + r * 0.45)}


def pot_feeder(p, mm=None):
    """bypass (pot) chemical feeder: vessel + screw cap + funnel, inlet / outlet valves"""
    mm = mm or M(); x, y, z = p
    cyl((x, y, z + 0.75), 0.2, 0.9, 'z', mm['white_poly'])
    sphere((x, y, z + 1.2), 0.2, mm['white_poly'], (1, 1, 0.4)); sphere((x, y, z + 0.3), 0.2, mm['white_poly'], (1, 1, 0.4))
    cyl((x, y, z + 1.32), 0.1, 0.08, 'z', mm['steel']); torus((x, y, z + 1.38), 0.12, 0.015, 'z', mm['act_onoff'])
    cyl((x + 0.12, y, z + 1.45), 0.07, 0.12, 'z', mm['steel'], 20, r2=0.02)
    for a in range(3):
        ang = a * math.tau / 3
        box((x + math.cos(ang) * 0.17, y + math.sin(ang) * 0.17, z + 0.15), (0.04, 0.04, 0.3), mm['steel'])
    box((x, y - 0.205, z + 0.8), (0.16, 0.01, 0.12), mm['chem_liquid'])
    return {'in': (x - 0.2, y, z + 1.05), 'out': (x + 0.2, y, z + 0.45), 'top': (x, y, z + 1.55)}


def dosing_skid(p, mm=None, running=True):
    mm = mm or M(); x, y, z = p
    box((x, y, z + 0.05), (1.0, 0.7, 0.1), mm['base'])
    cyl((x - 0.2, y, z + 0.55), 0.28, 0.9, 'z', mm['white_poly'])
    cyl((x - 0.2, y, z + 0.4), 0.281, 0.55, 'z', mm['chem_liquid'])
    cyl((x - 0.2, y, z + 1.02), 0.12, 0.05, 'z', mm['dark'])
    box((x + 0.3, y, z + 0.3), (0.25, 0.2, 0.3), mm['meter_head'], 0.02)                  # dosing pump
    cyl((x + 0.3, y - 0.12, z + 0.33), 0.08, 0.06, 'y', mm['paint_blue'])
    box((x + 0.3, y - 0.101, z + 0.4), (0.1, 0.004, 0.04), mm['lcd'])
    box((x + 0.4, y - 0.101, z + 0.25), (0.02, 0.004, 0.02), mm['led_g'] if running else mm['led_off'])
    return {'out': (x + 0.3, y, z + 0.5), 'top': (x, y, z + 1.2)}


def rpz(p, axis='x', mm=None):
    """reduced-pressure-zone backflow preventer assembly (gate valves + 2 checks + relief)"""
    mm = mm or M(); p = Vector(p); a = AX(axis)
    cyl_dir(p - a * 0.35, p + a * 0.35, 0.07, mm['bronze'])
    for s in (-0.18, 0.18): sphere(p + a * s, 0.1, mm['bronze'], (1.3, 1, 1))
    cyl_dir(p, p - Vector((0, 0, 0.25)), 0.05, mm['bronze'])
    cyl(p - Vector((0, 0, 0.3)), 0.07, 0.1, 'z', mm['bronze'], 20, r2=0.05)
    for s in (-0.45, 0.45): gate_valve(p + a * s, axis, 0.05, mm)
    return p + Vector((0, 0, 0.4))


def btu_calc(p, mm=None):
    mm = mm or M(); x, y, z = p
    box((x, y, z), (0.3, 0.12, 0.36), mm['meter_head'], 0.02)
    box((x, y - 0.061, z + 0.06), (0.2, 0.004, 0.1), mm['lcd'])
    for k in range(3): box((x - 0.06 + k * 0.06, y - 0.062, z - 0.08), (0.035, 0.004, 0.025), mm['dark'])
    return (x, y - 0.07, z + 0.25)


def oa_sensor(p, mm=None):
    mm = mm or M(); x, y, z = p
    cyl((x, y, z + 1.0), 0.03, 2.0, 'z', mm['steel'])
    for k in range(7): cyl((x, y, z + 1.8 + k * 0.045), 0.13 - k * 0.006, 0.02, 'z', mm['white_poly'], 28)
    box((x + 0.12, y, z + 1.5), (0.14, 0.08, 0.18), mm['meter_head'], 0.01)
    return (x, y, z + 2.2)


def sun_and_world(sc, energy=3.2, bg=(0.02, 0.025, 0.03), strength=0.6):
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 30)); sun = bpy.context.object
    sun.data.energy = energy; sun.rotation_euler = (math.radians(40), math.radians(-25), math.radians(35)); sun.data.angle = math.radians(8)
    world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
    world.node_tree.nodes['Background'].inputs[0].default_value = (*bg, 1)
    world.node_tree.nodes['Background'].inputs[1].default_value = strength
    return sun


def render_setup(sc, W, H, samples=64, transparent=True):
    sc.render.engine = 'CYCLES'; sc.cycles.samples = samples; sc.cycles.use_denoising = True
    try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception: pass
    sc.render.film_transparent = transparent
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    ids = [v.identifier for v in sc.view_settings.bl_rna.properties['view_transform'].enum_items]
    sc.view_settings.view_transform = 'AgX' if 'AgX' in ids else 'Filmic'
    try: sc.view_settings.look = 'AgX - Medium High Contrast' if 'AgX' in ids else 'None'
    except Exception: pass


def ortho_cam(sc, loc, target, scale, name='cam'):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object; cam.name = name
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = scale
    d = Vector(target) - cam.location
    cam.rotation_mode = 'QUATERNION'; cam.rotation_quaternion = d.to_track_quat('-Z', 'Y')
    return cam
