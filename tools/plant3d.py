"""Render the V7.1 '3D plant' background (isometric, Blender/Cycles via the bpy module) + 2-D anchor points for live Px overlays.
Geometry follows the V7.1 plant: 2 chillers (evaporator + condenser barrels, water boxes, compressor), 2 CHW pumps, 2 CDW pumps,
2 cooling towers on a roof deck, headers in the colour standard (CHWS blue, CHWR light blue, CDWS yellow, CDWR orange).
usage: python3 plant3d.py out.png anchors.json [W H samples]"""
import sys, json, math
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

OUT, ANCH = sys.argv[1], sys.argv[2]
W = int(sys.argv[3]) if len(sys.argv) > 3 else 1920
H = int(sys.argv[4]) if len(sys.argv) > 4 else 940
SAMPLES = int(sys.argv[5]) if len(sys.argv) > 5 else 96

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
C = {'chws': (0.02, 0.16, 0.75), 'chwr': (0.16, 0.62, 0.92), 'cdws': (0.95, 0.72, 0.02), 'cdwr': (0.93, 0.33, 0.02)}
MATS = {}


def mat(name, rgb, metal=0.0, rough=0.45, emit=None):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1)
    b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    if emit:
        b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = 3.0
    MATS[name] = m
    return m


def obj(o, m):
    o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = len(p.vertices) == 4      # caps stay flat
    return o


def cyl(p, r, depth, axis='z', m=None, verts=40):
    rot = {'x': (0, math.pi / 2, 0), 'y': (math.pi / 2, 0, 0), 'z': (0, 0, 0)}[axis]
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=p, rotation=rot)
    return obj(bpy.context.object, m)


def box(p, s, m, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=p)
    o = bpy.context.object; o.scale = s
    if bevel:
        bpy.ops.object.transform_apply(scale=True)
        mod = o.modifiers.new('b', 'BEVEL'); mod.width = bevel; mod.segments = 3
    o.data.materials.append(m)
    return o


def sphere(p, r, m):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=p, segments=24, ring_count=12)
    return obj(bpy.context.object, m)


def pipe(pts, svc, r=0.16):
    m = mat(svc, C[svc], metal=0.25, rough=0.28)
    for a, b in zip(pts, pts[1:]):
        a, b = Vector(a), Vector(b); d = b - a
        L = d.length
        if L < 1e-6: continue
        bpy.ops.mesh.primitive_cylinder_add(vertices=28, radius=r, depth=L, location=(a + b) / 2)
        o = bpy.context.object
        o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
        obj(o, m)
    for q in pts[1:-1]: sphere(q, r * 1.02, m)
    fl = mat('flange', (0.25, 0.27, 0.3), metal=0.8, rough=0.35)
    for q, nxt in ((pts[0], pts[1]), (pts[-1], pts[-2])):
        d = (Vector(nxt) - Vector(q)).normalized()
        c = Vector(q) + d * 0.05
        bpy.ops.mesh.primitive_cylinder_add(vertices=28, radius=r * 1.45, depth=0.06, location=c)
        o = bpy.context.object; o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
        obj(o, fl)


ANCHORS = {}


def anchor(name, p): ANCHORS[name] = p


# ---------------------------------------------------------------- materials
floor = mat('floor', (0.035, 0.04, 0.045), rough=0.8)
white = mat('shell', (0.82, 0.84, 0.86), metal=0.35, rough=0.3)
steel = mat('steel', (0.35, 0.37, 0.4), metal=0.8, rough=0.35)
dark = mat('dark', (0.06, 0.07, 0.08), rough=0.6)
panelm = mat('panel', (0.55, 0.57, 0.6), metal=0.2, rough=0.4)
blue_m = mat('motor', (0.12, 0.2, 0.42), metal=0.4, rough=0.35)
volute = mat('volute', (0.1, 0.32, 0.6), metal=0.5, rough=0.3)
tower = mat('tower', (0.42, 0.45, 0.48), metal=0.2, rough=0.55)
louvre = mat('louvre', (0.12, 0.13, 0.14), rough=0.7)
concrete = mat('concrete', (0.2, 0.21, 0.22), rough=0.9)
green = mat('led', (0.1, 0.8, 0.3), emit=(0.1, 1.0, 0.3))

# ---------------------------------------------------------------- floor / roof deck
box((2.5, 0, -0.05), (34, 20, 0.1), floor)
for gx in range(-14, 20, 2): box((gx, 0, 0.002), (0.02, 20, 0.004), mat('grid', (0.07, 0.08, 0.09), rough=0.9))
for gy in range(-10, 11, 2): box((2.5, gy, 0.002), (34, 0.02, 0.004), mat('grid', (0.07, 0.08, 0.09), rough=0.9))
box((13.0, 0, 3.4), (8.5, 12.5, 0.25), concrete)                       # roof deck for the towers
for x in (9.1, 16.9):
    for y in (-5.9, 5.9): box((x, y, 1.7), (0.35, 0.35, 3.4), concrete)
box((-12.5, 0, 2.3), (0.3, 3.2, 4.6), mat('wall', (0.16, 0.2, 0.26), rough=0.7))   # building riser wall (CHW to building)
box((-12.5, 0, 4.72), (0.36, 3.3, 0.2), steel)

# ---------------------------------------------------------------- chillers
CHY = {'01': -3.2, '02': 3.2}
for n, y in CHY.items():
    ev_z, cd_z = 0.95, 2.05
    cyl((0, y, ev_z), 0.62, 4.6, 'x', white); cyl((0, y, cd_z), 0.55, 4.4, 'x', white)
    for x in (-2.35, 2.35):                                                  # water boxes
        cyl((x, y, ev_z), 0.68, 0.18, 'x', panelm); cyl((x * 0.97, y, cd_z), 0.6, 0.16, 'x', panelm)
    for x in (-1.6, 1.6):                                                    # tube-sheet rings + feet
        cyl((x, y, ev_z), 0.66, 0.08, 'x', panelm); box((x, y, 0.2), (0.25, 1.4, 0.4), steel)
    cyl((0.4, y, 2.95), 0.42, 1.2, 'x', panelm)                              # compressor
    cyl((-0.6, y, 2.85), 0.18, 0.9, 'z', panelm)                             # suction elbow
    box((-0.2, y - 0.75, 1.55), (1.3, 0.25, 1.0), dark, 0.03)                # control panel
    box((-0.2, y - 0.885, 1.75), (0.35, 0.02, 0.2), mat('hmi', (0.05, 0.2, 0.35), emit=(0.1, 0.4, 0.9)))
    anchor(f'CH{n}', (0, y, 3.4)); anchor(f'CH{n}_panel', (-0.2, y - 0.9, 1.3))
    # nozzles: evaporator (left end, x-) and condenser (right end, x+)
    pipe([(-2.45, y - 0.25, ev_z), (-3.3, y - 0.25, ev_z)], 'chws'); pipe([(-2.45, y + 0.25, ev_z), (-4.1, y + 0.25, ev_z)], 'chwr')
    pipe([(2.4, y - 0.22, cd_z), (3.2, y - 0.22, cd_z)], 'cdwr'); pipe([(2.4, y + 0.22, cd_z), (4.0, y + 0.22, cd_z)], 'cdws')
    anchor(f'CH{n}_chw', (-3.3, y, ev_z + 0.45)); anchor(f'CH{n}_cdw', (3.4, y, cd_z + 0.45))

# ---------------------------------------------------------------- pumps
def pump(p, facing, n, svc_in, svc_out, tag):
    x, y = p; s = 1 if facing > 0 else -1
    box((x, y, 0.12), (2.0, 0.8, 0.24), steel, 0.02)                       # base frame
    cyl((x - s * 0.35, y, 0.62), 0.3, 0.95, 'x', blue_m)                    # motor
    cyl((x - s * 0.9, y, 0.62), 0.22, 0.12, 'x', dark)                      # fan cover
    cyl((x + s * 0.45, y, 0.62), 0.12, 0.25, 'x', steel)                    # coupling guard
    cyl((x + s * 0.72, y, 0.66), 0.36, 0.3, 'x', volute)                    # volute
    cyl((x + s * 0.95, y, 0.62), 0.15, 0.3, 'x', volute)                    # suction nozzle
    cyl((x + s * 0.72, y, 1.05), 0.14, 0.4, 'z', volute)                    # discharge nozzle
    anchor(tag, (x, y, 1.3))
    return (x + s * 1.1, y, 0.62), (x + s * 0.72, y, 1.25)


HDR = {}
for n, y in (('01', -3.2), ('02', 3.2)):
    suc, dis = pump((-7.0, y + (0.0)), 1, n, 'chwr', 'chwr', f'CHP{n}')       # CHP: suction faces +x (toward header)
    HDR[f'CHP{n}'] = (suc, dis)
    suc2, dis2 = pump((7.4, y), 1, n, 'cdws', 'cdws', f'CDP{n}')
    HDR[f'CDP{n}'] = (suc2, dis2)

# CHW: pump discharge -> header -> evaporator inlets (CHWR colour), evaporator outlets -> CHWS header -> building
for n, y in CHY.items():
    suc, dis = HDR[f'CHP{n}']
    pipe([suc, (-5.4, y, 0.62), (-5.4, y, 0.62)], 'chwr')
    pipe([dis, (dis[0], dis[1], 2.2), (-4.1, dis[1], 2.2), (-4.1, y + 0.25, 2.2), (-4.1, y + 0.25, 0.95)], 'chwr')
    pipe([(-3.3, y - 0.25, 0.95), (-3.3, y - 0.25, 3.8)], 'chws')
pipe([(-5.4, -3.2, 0.62), (-5.4, 3.2, 0.62)], 'chwr')                        # CHP suction header
pipe([(-5.4, 0, 0.62), (-5.4, 0, 0.3), (-12.3, 0, 0.3)], 'chwr')            # CHWR from building
pipe([(-3.3, -3.45, 3.8), (-3.3, 0.0, 3.8), (-3.3, 2.95, 3.8)], 'chws')
pipe([(-3.3, 0.0, 3.8), (-12.3, 0.0, 3.8)], 'chws')                           # CHWS to building
anchor('CHWS', (-8.5, 0, 4.3)); anchor('CHWR', (-8.5, 0, 0.8)); anchor('BUILDING', (-12.3, 0, 4.9))
# CDW: condenser outlets -> CDWR riser -> towers; tower outlets -> CDWS -> CDP suction -> CDP discharge -> condenser inlets
for n, y in CHY.items():
    pipe([(3.2, y - 0.22, 2.05), (3.2, y - 0.22, 4.4)], 'cdwr')
    suc, dis = HDR[f'CDP{n}']
    pipe([dis, (dis[0], dis[1], 1.5), (4.0, dis[1], 1.5), (4.0, y + 0.22, 1.5), (4.0, y + 0.22, 2.05)], 'cdws')
    pipe([suc, (8.9, y, 0.62)], 'cdws')
pipe([(3.2, -3.42, 4.4), (3.2, 2.98, 4.4)], 'cdwr')
TY = {'01': -3.2, '02': 3.2}
for n, y in TY.items():
    pipe([(3.2, y - 0.22 if n == '01' else y - 0.22, 4.4), (10.6, y - 0.22, 4.4), (10.6, y - 0.22, 5.2), (11.1, y - 0.22, 5.2)], 'cdwr')
    pipe([(11.1, y + 0.45, 4.05), (8.9, y + 0.45, 4.05), (8.9, y + 0.45, 0.62)], 'cdws')
pipe([(8.9, -2.75, 0.62), (8.9, 3.65, 0.62)], 'cdws')
anchor('CDWR', (6.5, 0, 4.9)); anchor('CDWS', (8.9, 0, 1.4))

# ---------------------------------------------------------------- cooling towers (on the roof deck)
for n, y in TY.items():
    cx = 13.2
    box((cx, y, 5.4), (4.0, 3.6, 3.6), tower, 0.04)
    for k in range(9):                                                       # air-inlet louvres (both long sides)
        z = 3.9 + k * 0.17
        for sy in (-1, 1): box((cx, y + sy * 1.81, z), (3.7, 0.04, 0.07), louvre)
    for k in range(9):
        z = 3.9 + k * 0.17
        box((cx - 2.01, y, z), (0.04, 3.3, 0.07), louvre)
    box((cx, y, 7.28), (4.05, 3.65, 0.16), steel)
    cyl((cx, y, 7.7), 1.15, 0.7, 'z', tower, 48)                            # fan stack
    cyl((cx, y, 8.06), 1.08, 0.04, 'z', dark, 48)
    for a in range(4):                                                       # fan blades
        ang = a * math.pi / 2 + 0.3
        box((cx + math.cos(ang) * 0.52, y + math.sin(ang) * 0.52, 8.04), (0.95, 0.2, 0.02), steel).rotation_euler = (0, 0, ang)
    cyl((cx, y, 8.08), 0.16, 0.06, 'z', steel)
    for sx in (-1, 1):                                                       # handrail
        box((cx + sx * 2.0, y, 7.75), (0.04, 3.6, 0.04), steel)
    anchor(f'CT{n}', (cx, y, 8.6)); anchor(f'CT{n}_basin', (cx - 2.1, y, 3.9))
    pipe([(11.1, y - 0.22, 5.2), (11.2, y - 0.22, 5.2)], 'cdwr')

# ---------------------------------------------------------------- motorised valves (V7.1b): red actuator = on/off isolation, green = modulating
act_onoff = mat('act_onoff', (0.75, 0.08, 0.06), metal=0.2, rough=0.4)
act_mod = mat('act_mod', (0.1, 0.55, 0.25), metal=0.2, rough=0.4)
vbody = mat('vbody', (0.18, 0.19, 0.21), metal=0.7, rough=0.35)


def valve3d(p, axis, mod=False, r=0.16):
    x, y, z = p
    cyl(p, r * 1.55, 0.16, axis, vbody)                                   # wafer body
    up = (0, 0, 1) if axis in ('x', 'y') else (1, 0, 0)
    sx, sy, sz = x + up[0] * r * 2.2, y + up[1] * r * 2.2, z + up[2] * r * 2.2
    cyl(((x + sx) / 2, (y + sy) / 2, (z + sz) / 2), 0.04, r * 1.6, 'z' if axis != 'z' else 'x', steel)   # stem
    box((sx, sy, sz), (0.3, 0.22, 0.2) if axis != 'z' else (0.2, 0.22, 0.3), act_mod if mod else act_onoff, 0.02)


for n, y in CHY.items():
    valve3d((-3.7, y + 0.25, 0.95), 'x')                 # CHW inlet ISO
    valve3d((-2.9, y - 0.25, 0.95), 'x', mod=True)       # CHW outlet FCV
    valve3d((3.6, y + 0.22, 2.05), 'x')                  # CDW inlet ISO
    valve3d((2.8, y - 0.22, 2.05), 'x', mod=True)        # CDW outlet HPV
    valve3d((-5.62, y, 0.62), 'x')                       # CHP suction
    valve3d((-6.28, y, 1.75), 'z')                       # CHP discharge
    valve3d((8.72, y, 0.62), 'x')                        # CDP suction
    valve3d((6.0, y, 1.5), 'x')                          # CDP discharge
for n, y in TY.items():
    valve3d((10.6, y - 0.22, 4.8), 'z')                  # tower inlet
    valve3d((10.0, y + 0.45, 4.05), 'x')                 # tower outlet

# ---------------------------------------------------------------- camera + light
bpy.ops.object.camera_add(location=(-17.5, -26.0, 21.0))
cam = bpy.context.object
cam.data.type = 'ORTHO'; cam.data.ortho_scale = 36.0
target = Vector((1.8, 0.6, 4.4))
d = target - cam.location
cam.rotation_mode = 'QUATERNION'; cam.rotation_quaternion = d.to_track_quat('-Z', 'Y')
sc.camera = cam
bpy.ops.object.light_add(type='SUN', location=(0, 0, 30)); sun = bpy.context.object
sun.data.energy = 3.2; sun.rotation_euler = (math.radians(40), math.radians(-25), math.radians(35)); sun.data.angle = math.radians(8)
bpy.ops.object.light_add(type='AREA', location=(-8, -12, 14)); ar = bpy.context.object; ar.data.energy = 1800; ar.data.size = 12
ar.rotation_euler = (math.radians(50), 0, math.radians(-30))
world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (0.02, 0.025, 0.03, 1); world.node_tree.nodes['Background'].inputs[1].default_value = 0.6

sc.render.engine = 'CYCLES'; sc.cycles.samples = SAMPLES; sc.cycles.use_denoising = True
try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
sc.render.film_transparent = True
sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
sc.view_settings.view_transform = 'AgX' if 'AgX' in [v.identifier for v in sc.view_settings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
res = {}
for k, p in ANCHORS.items():
    v = world_to_camera_view(sc, cam, Vector(p))
    res[k] = (round(v.x * W, 1), round((1 - v.y) * H, 1))
json.dump({'size': [W, H], 'anchors': res}, open(ANCH, 'w'), indent=1)
print('rendered', OUT, len(res), 'anchors')
