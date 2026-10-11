# -*- coding: utf-8 -*-
"""V7.9 r4 equipment models built in Blender (bpy), exported as glTF binary for the 3D page and rendered (Cycles) for the Px pages.

Run with Blender 4.x or the `bpy` Python module (pip install bpy==4.5.0, Python 3.11):
    python3.11 tools/blender/equipment79.py graphics3d/models            # GLB only
    python3.11 tools/blender/equipment79.py graphics3d/models --render station/shared/px/img
Models are authored in the 3D page's local frame (metres, x = length, y = up, z = depth, origin = centre of the footprint at floor
level) through V() so pipe nozzles land where the page's pipe network connects. Named nodes are the parts the page animates:
  chiller: comp, evap, cond, panel, screen, beacon      pump: motor, volute, motorFan, shaft
  ahu: fanWheel, screen                                 vav: damper                       tower: fanStack (body only; water / fan stay live)
Sizes = R9 model (graphics3d/data/r9_model.json): chiller 3774 x 1771 x 2033, pump 1750 x 650 x 850, AHU 3600 x 1800 x 2100,
cooling tower cell 2600 x 2600 x 2700, VAV box 550 x 600 x 250 mm."""
import math, os, sys
import bpy
import bmesh
from mathutils import Vector, Euler

OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 'graphics3d/models'
RENDER = sys.argv[sys.argv.index('--render') + 1] if '--render' in sys.argv else None
MATS = {}


# ------------------------------------------------------------------ scene / helpers
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    MATS.clear()


def V(x, y, z):
    """page frame (x, y up, z) -> Blender (x, -z, y); glTF export (+Y up) maps it back"""
    return Vector((x, -z, y))


def mat(name, rgb, metal=0.0, rough=0.5, emit=None, alpha=1.0, coat=0.0):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1.0)
    b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    if coat: b.inputs['Coat Weight'].default_value = coat
    if emit:
        b.inputs['Emission Color'].default_value = (*emit, 1.0); b.inputs['Emission Strength'].default_value = 2.0
    if alpha < 1.0:
        b.inputs['Alpha'].default_value = alpha; m.blend_method = 'BLEND'
    MATS[name] = m
    return m


def srgb(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


def P():
    """material palette (PBR values for painted steel, insulation, cast iron, galvanised, FRP)"""
    return dict(
        paint=mat('chiller_paint', srgb('#d9d4c4'), 0.35, 0.38, coat=0.4), paintDark=mat('chiller_paint_dark', srgb('#a9a391'), 0.4, 0.42, coat=0.3),
        insul=mat('armaflex', srgb('#1d1f22'), 0.0, 0.82), steel=mat('steel', srgb('#8d939a'), 0.9, 0.32), bolt=mat('bolt', srgb('#6a6e72'), 1.0, 0.25),
        iron=mat('cast_iron_blue', srgb('#2f5e8f'), 0.45, 0.4, coat=0.3), motor=mat('motor_grey', srgb('#5d6b78'), 0.5, 0.45, coat=0.2),
        galv=mat('galvanised', srgb('#a7adb2'), 0.85, 0.42), concrete=mat('concrete', srgb('#9b9a96'), 0.0, 0.92), black=mat('rubber', srgb('#151515'), 0.0, 0.7),
        panel=mat('panel_ral7035', srgb('#c9ccc8'), 0.2, 0.45, coat=0.2), screen=mat('screen', srgb('#06263a'), 0.0, 0.2, emit=srgb('#0d4d6b')),
        green=mat('beacon', srgb('#1b1b1b'), 0.0, 0.3, emit=srgb('#22c55e')), yellow=mat('guard_yellow', srgb('#f2c12e'), 0.2, 0.45, coat=0.3),
        copper=mat('copper', srgb('#b87333'), 1.0, 0.3), frp=mat('frp_white', srgb('#e8ece9'), 0.0, 0.48, coat=0.2), fill=mat('fill_pack', srgb('#33413f'), 0.0, 0.95),
        louver=mat('louver', srgb('#7c8a86'), 0.1, 0.6), ahuPanel=mat('ahu_panel', srgb('#dfe3e5'), 0.3, 0.38, coat=0.3), coil=mat('coil_fins', srgb('#c7b289'), 0.8, 0.35),
        gauge=mat('gauge_face', srgb('#f4f4f0'), 0.0, 0.3), glass=mat('gauge_glass', srgb('#dfefff'), 0.0, 0.05, alpha=0.25))


def finish(o, m, name=None, smooth=True, bevel=0.0):
    if name: o.name = name
    o.data.materials.clear(); o.data.materials.append(m)
    if bevel:
        b = o.modifiers.new('bevel', 'BEVEL'); b.width = bevel; b.segments = 2; b.limit_method = 'ANGLE'
    if smooth:
        for p in o.data.polygons: p.use_smooth = True
        o.modifiers.new('wn', 'WEIGHTED_NORMAL').keep_sharp = True
    return o


def box(sx, sy, sz, c, m, name=None, bevel=0.012):
    """size in page frame (x, y up, z)"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=V(*c))
    o = bpy.context.object; o.scale = (sx, sz, sy)
    bpy.ops.object.transform_apply(scale=True)
    return finish(o, m, name, smooth=bool(bevel), bevel=bevel)


def cyl(r, length, c, axis, m, name=None, n=48, bevel=0.006, r2=None, open_ends=False):
    """cylinder along a page axis 'x' | 'y' | 'z' (open_ends: no caps, e.g. fan stacks / casings)"""
    fill = 'NOTHING' if open_ends else 'NGON'
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=n, radius=r, depth=length, location=V(*c), end_fill_type=fill)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=n, radius1=r, radius2=r2, depth=length, location=V(*c), end_fill_type=fill)
    o = bpy.context.object
    o.rotation_euler = {'x': Euler((0, math.pi / 2, 0)), 'y': Euler((0, 0, 0)), 'z': Euler((math.pi / 2, 0, 0))}[axis]
    bpy.ops.object.transform_apply(rotation=True)
    if open_ends:
        sol = o.modifiers.new('wall', 'SOLIDIFY'); sol.thickness = 0.012
    return finish(o, m, name, bevel=bevel)


def torus(R, r, c, axis, m, name=None, arc=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, major_segments=48, minor_segments=12, location=V(*c))
    o = bpy.context.object
    o.rotation_euler = {'x': Euler((0, math.pi / 2, 0)), 'y': Euler((0, 0, 0)), 'z': Euler((math.pi / 2, 0, 0))}[axis]
    bpy.ops.object.transform_apply(rotation=True)
    return finish(o, m, name, bevel=0)


def sphere(r, c, m, name=None, half=False, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40, ring_count=20, radius=r, location=V(*c))
    o = bpy.context.object; o.scale = (scale[0], scale[2], scale[1]); bpy.ops.object.transform_apply(scale=True)
    if half:
        bm = bmesh.new(); bm.from_mesh(o.data)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -1e-4], context='VERTS'); bm.to_mesh(o.data); bm.free()
    return finish(o, m, name, bevel=0)


def flange(c, axis, ro, ri, t, m, bolts=8, bm=None):
    """pipe flange + bolt circle (realism at every nozzle / water box)"""
    cyl(ro, t, c, axis, m, n=48, bevel=0.003)
    rb = (ro + ri) / 2
    for i in range(bolts):
        a = 2 * math.pi * i / bolts
        if axis == 'x': p = (c[0], c[1] + rb * math.cos(a), c[2] + rb * math.sin(a))
        elif axis == 'y': p = (c[0] + rb * math.cos(a), c[1], c[2] + rb * math.sin(a))
        else: p = (c[0] + rb * math.cos(a), c[1] + rb * math.sin(a), c[2])
        cyl(t * 0.45, t * 1.9, p, axis, bm or P()['bolt'], n=6, bevel=0)
    return []


def gauge(c, axis, m=None):
    """pressure / temperature gauge on a stem: dial face + glass + bezel"""
    pal = P()
    cyl(0.008, 0.08, (c[0], c[1] + 0.04, c[2]), 'y', pal['steel'], n=12, bevel=0)
    cyl(0.045, 0.025, (c[0], c[1] + 0.1, c[2]), axis, pal['steel'], n=32)
    off = {'x': (0.013, 0, 0), 'z': (0, 0, 0.013), 'y': (0, 0.013, 0)}[axis]
    cyl(0.04, 0.002, (c[0] + off[0], c[1] + 0.1 + off[1], c[2] + off[2]), axis, pal['gauge'], n=32, bevel=0)
    return []


def group(name, objs):
    """join objects into one named node (the page looks it up by name)"""
    objs = [o for o in objs if o]
    if not objs: return None
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    for o in objs:
        bpy.context.view_layer.objects.active = o
        for md in list(o.modifiers): bpy.ops.object.modifier_apply(modifier=md.name)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1: bpy.ops.object.join()
    o = bpy.context.object; o.name = name; o.data.name = name
    return o


def collect(fn):
    """run a builder and return the objects it created"""
    before = set(bpy.data.objects)
    fn()
    return [o for o in bpy.data.objects if o not in before]


def export(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for o in bpy.data.objects:
        if o.modifiers:
            bpy.context.view_layer.objects.active = o
            for md in list(o.modifiers): bpy.ops.object.modifier_apply(modifier=md.name)
    bpy.ops.export_scene.gltf(filepath=path, export_format='GLB', export_yup=True, export_apply=True, export_texcoords=False,
                              export_normals=True, export_cameras=False, export_lights=False, use_selection=False)
    print('GLB', path, os.path.getsize(path) // 1024, 'kB', len(bpy.data.objects), 'nodes')


# ------------------------------------------------------------------ equipment
def chiller(L=3.774, W=1.771, H=2.033):
    """water-cooled screw chiller, 334 TR: condenser + insulated evaporator, water boxes, compressor + motor, oil separators, starter panel"""
    p = P()
    box(L + 0.3, 0.1, W + 0.3, (0, -0.05, 0), p['concrete'], 'pad', bevel=0.02)
    rails = collect(lambda: [box(L, 0.18, 0.12, (0, 0.09, z), p['steel'], bevel=0.008) for z in (-0.7, 0.7)] +
                    [box(0.1, 0.18, W * 0.92, (x, 0.09, 0), p['steel'], bevel=0.008) for x in (-L * 0.45, 0, L * 0.45)])
    group('skid', rails)
    sup = collect(lambda: [box(0.25, 0.55, W * 0.8, (s * L * 0.36, 0.45, 0), p['paintDark'], bevel=0.015) for s in (-1, 1)] +
                  [box(0.16, 0.04, 0.16, (s * L * 0.42, 0.02, z), p['black']) for s in (-1, 1) for z in (-0.7, 0.7)])
    group('supports', sup)
    # condenser shell + weld seams + water boxes with bolted covers
    cond = collect(lambda: [cyl(0.36, L * 0.86, (0, 0.62, -0.22), 'x', p['paint'], n=64)] +
                   [torus(0.362, 0.006, (x, 0.62, -0.22), 'x', p['paintDark']) for x in (-L * 0.2, L * 0.2)])
    group('cond', cond)
    evap = collect(lambda: [cyl(0.42, L * 0.9, (0, 1.08, 0.18), 'x', p['insul'], n=64, bevel=0.01)] +
                   [torus(0.423, 0.008, (x, 1.08, 0.18), 'x', p['black']) for x in (-L * 0.3, 0, L * 0.3)])
    group('evap', evap)
    wb = []
    for s in (-1, 1):
        wb += collect(lambda s=s: [cyl(0.44, 0.12, (s * L * 0.455, 1.08, 0.18), 'x', p['paintDark'], n=64),
                                   sphere(0.44, (s * L * 0.515, 1.08, 0.18), p['paintDark'], half=False, scale=(0.18, 1, 1))])
        wb += collect(lambda s=s: flange((s * L * 0.42, 1.08, 0.18), 'x', 0.5, 0.43, 0.03, p['paintDark'], bolts=24))
        wb += collect(lambda s=s: [cyl(0.38, 0.12, (s * L * 0.44, 0.62, -0.22), 'x', p['paintDark'], n=64),
                                   sphere(0.38, (s * L * 0.5, 0.62, -0.22), p['paintDark'], scale=(0.16, 1, 1))])
        wb += collect(lambda s=s: flange((s * L * 0.41, 0.62, -0.22), 'x', 0.44, 0.38, 0.03, p['paintDark'], bolts=20))
    group('waterboxes', wb)
    # nozzles with flanges (same points as the page pipe network), gauges and thermowells
    noz = []
    for y, zs in ((1.08, (0.43, -0.07)), (0.62, (-0.42, -0.02))):
        for z in zs:
            x0 = -L * 0.5 - 0.05
            noz += collect(lambda y=y, z=z, x0=x0: [cyl(0.11, 0.5, (x0, y, z), 'x', p['steel'])])
            noz += collect(lambda y=y, z=z, x0=x0: flange((x0 - 0.25, y, z), 'x', 0.19, 0.12, 0.03, p['iron'], bolts=8))
            noz += collect(lambda y=y, z=z, x0=x0: gauge((x0 + 0.05, y + 0.1, z), 'z'))
            noz += collect(lambda y=y, z=z, x0=x0: [cyl(0.012, 0.12, (x0 + 0.15, y + 0.15, z), 'y', p['steel'], n=12, bevel=0)])
    group('nozzles', noz)
    # compressor (named: the page vibrates it when running), motor with fins and terminal box
    comp = collect(lambda: [box(L * 0.36, 0.55, 0.62, (L * 0.05, 1.72, 0.05), p['paint'], bevel=0.05)] +
                   [box(0.02, 0.5, 0.64, (L * 0.05 + x, 1.72, 0.05), p['paintDark'], bevel=0.004) for x in (-0.4, -0.2, 0.0, 0.2, 0.4)] +
                   [cyl(0.26, 0.5, (L * 0.26, 1.72, 0.05), 'x', p['paintDark'], n=48)] +
                   [box(0.5, 0.012, 0.03, (L * 0.26, 1.72 + 0.27 * math.cos(a), 0.05 + 0.27 * math.sin(a)), p['paintDark'], bevel=0)
                    for a in [i * math.pi / 9 for i in range(18)]] +
                   [box(0.22, 0.2, 0.16, (L * 0.26, 2.02, 0.05), p['panel'], bevel=0.01)])
    group('comp', comp)
    oil = []
    for x, z in ((-L * 0.28, -0.45), (-L * 0.1, -0.45)):
        oil += collect(lambda x=x, z=z: [cyl(0.17, 0.9, (x, 1.25, z), 'y', p['paint']), sphere(0.17, (x, 1.7, z), p['paint'], half=True),
                                         sphere(0.17, (x, 0.8, z), p['paint'], scale=(1, 0.5, 1))])
    oil += collect(lambda: [torus(0.32, 0.07, (-L * 0.19, 1.72, -0.45), 'z', p['paint'])])
    oil += collect(lambda: [cyl(0.035, 0.9, (L * 0.15, 1.45, -0.35), 'x', p['copper'], n=16), cyl(0.035, 0.5, (L * 0.33, 1.2, -0.35), 'y', p['copper'], n=16)])
    group('refrigerant', oil)
    # starter / controller panel, HMI screen, status beacon (named)
    group('panel', collect(lambda: [box(0.32, 1.1, 0.95, (L * 0.5 + 0.02, 1.25, 0.25), p['panel'], bevel=0.015),
                                    box(0.01, 1.04, 0.004, (L * 0.5 + 0.185, 1.25, 0.25), p['paintDark'], bevel=0),
                                    box(0.03, 0.12, 0.03, (L * 0.5 + 0.2, 1.1, 0.6), p['steel'], bevel=0.005),
                                    cyl(0.03, 0.3, (L * 0.5 + 0.02, 0.55, 0.25), 'y', p['black'], n=16, bevel=0)]))
    o = box(0.004, 0.16, 0.3, (L * 0.5 + 0.187, 1.45, 0.25), p['screen'], 'screen', bevel=0)
    o = cyl(0.04, 0.1, (L * 0.5 + 0.02, 1.86, 0.6), 'y', p['green'], 'beacon', n=24, bevel=0.003)


def pump(L=1.75, W=0.65, H=0.85):
    """end-suction pump on a concrete inertia base: volute, coupling guard, TEFC motor with fins and fan cowl, flanged suction / discharge"""
    p = P()
    group('base', collect(lambda: [box(L + 0.25, 0.3, W + 0.35, (0, 0.15, 0), p['concrete'], bevel=0.02),
                                   box(L, 0.06, W, (0, 0.33, 0), p['steel'], bevel=0.006)] +
                          [box(0.12, 0.12, 0.5, (s * L * 0.45, 0.05, 0), p['steel'], bevel=0.008) for s in (-1, 1)] +
                          [cyl(0.03, 0.08, (s * L * 0.45, 0.13, z), 'y', p['yellow'], n=12, bevel=0) for s in (-1, 1) for z in (-0.15, 0.15)]))
    group('motor', collect(lambda: [cyl(0.21, 0.62, (L * 0.22, 0.6, 0), 'x', p['motor'], n=48)] +
                           [box(0.58, 0.04, 0.012, (L * 0.22, 0.6 + 0.225 * math.sin(a), 0.225 * math.cos(a)), p['motor'], bevel=0)
                            for a in [i * math.pi / 12 for i in range(24)]] +
                           [box(0.16, 0.14, 0.14, (L * 0.22, 0.86, 0), p['motor'], bevel=0.01), box(0.5, 0.06, 0.3, (L * 0.22, 0.36, 0), p['motor'], bevel=0.01),
                            cyl(0.2, 0.12, (L * 0.22 + 0.36, 0.6, 0), 'x', p['motor'], n=48)]))
    cyl(0.12, 0.03, (L * 0.22 + 0.43, 0.6, 0), 'x', p['black'], 'motorFan', n=6, bevel=0)
    group('guard', collect(lambda: [box(0.32, 0.2, 0.22, (-L * 0.07, 0.6, 0), p['yellow'], bevel=0.02)]))
    cyl(0.035, 0.3, (-L * 0.07, 0.6, 0), 'x', p['galv'], 'shaft', n=16, bevel=0)
    group('volute', collect(lambda: [cyl(0.3, 0.22, (-L * 0.3, 0.62, 0), 'z', p['iron'], n=64, bevel=0.02),
                                     cyl(0.18, 0.12, (-L * 0.3, 0.62, -0.15), 'z', p['iron'], n=48),
                                     box(0.2, 0.25, 0.2, (-L * 0.24, 0.42, 0), p['iron'], bevel=0.02)]))
    group('isolator', collect(lambda: [box(0.04, 0.9, 0.04, (L * 0.48, 0.75, W * 0.42), p['galv'], bevel=0.004),
                                       box(0.16, 0.22, 0.1, (L * 0.48, 1.25, W * 0.42), p['panel'], bevel=0.01),
                                       cyl(0.03, 0.03, (L * 0.48, 1.29, W * 0.42 + 0.06), 'z', p['yellow'], n=16, bevel=0)]))
    cyl(0.018, 0.02, (L * 0.48, 1.19, W * 0.42 + 0.055), 'z', p['green'], 'beacon', n=16, bevel=0)
    group('nozzles', collect(lambda: [cyl(0.1, 0.3, (-L * 0.44, 0.62, 0), 'x', p['iron'])] +
                             flange((-L * 0.44 - 0.15, 0.62, 0), 'x', 0.17, 0.11, 0.025, p['iron']) +
                             [cyl(0.09, 0.32, (-L * 0.3, 0.95, 0), 'y', p['iron'])] +
                             flange((-L * 0.3, 1.11, 0), 'y', 0.16, 0.1, 0.025, p['iron']) +
                             gauge((-L * 0.3 + 0.12, 0.98, 0), 'z')))


def tower(L=2.6, D=2.6, H=2.7, blades=None):
    """counter-flow induced-draft cell body: FRP casing with ribs, air-inlet louvres, fill, fan stack, motor; the page keeps the live
    parts (water, fan blades, plume, curtain) and the handrail / ladder"""
    p = P()
    group('casing', collect(lambda: [box(L, 0.55, D, (0, 0.275, 0), p['frp'], bevel=0.02)] +
                            [box(L, H - 0.55, 0.06, (0, 0.55 + (H - 0.55) / 2, s * D / 2), p['frp'], bevel=0.01) for s in (-1, 1)] +
                            [box(0.06, H - 0.6, 0.08, (x, 0.55 + (H - 0.55) / 2, s * (D / 2 + 0.03)), p['frp'], bevel=0.01)
                             for s in (-1, 1) for x in (-L * 0.33, 0, L * 0.33)] +
                            [box(L, 0.1, D, (0, H, 0), p['frp'], bevel=0.01)]))
    group('louvres', collect(lambda: [box(0.04, 0.05, D - 0.2, (s * (L / 2 - 0.03), 0.62 + i * 0.12, 0), p['louver'], bevel=0.004)
                                      for s in (-1, 1) for i in range(int((H - 1.0) / 0.12))]))
    group('fill', collect(lambda: [box(0.55, H - 1.1, D - 0.3, (s * (L / 2 - 0.55), 0.55 + (H - 1.1) / 2 + 0.05, 0), p['fill'], bevel=0) for s in (-1, 1)]))
    group('fanStack', collect(lambda: [cyl(1.08, 0.5, (0, H + 0.3, 0), 'y', p['frp'], n=64, r2=0.86, bevel=0.0, open_ends=True)] +
                              [torus(1.0, 0.03, (0, H + 0.1, 0), 'y', p['frp'])]))
    group('fanMotor', collect(lambda: [box(0.34, 0.3, 0.3, (0.95, H + 0.25, -0.75), p['motor'], bevel=0.02),
                                       box(0.24, 0.2, 0.14, (1.15, H + 0.25, -0.45), p['panel'], bevel=0.01)]))
    if blades is not None:                                  # render only: the page draws its own spinning blades
        for i in range(6):
            a = blades + i * math.pi / 3
            box(0.85, 0.025, 0.2, (0.48 * math.cos(a), H + 0.42, 0.48 * math.sin(a)), p['black'], bevel=0)


def fan(blades=0.0):
    """axial exhaust / supply fan in a galvanised casing (Px fan symbol)"""
    p = P()
    group('casing', collect(lambda: [cyl(0.62, 0.5, (0, 0, 0), 'z', p['galv'], n=64, bevel=0.0, open_ends=True), torus(0.62, 0.03, (0, 0, 0.25), 'z', p['galv']),
                                     torus(0.62, 0.03, (0, 0, -0.25), 'z', p['galv']), cyl(0.14, 0.3, (0, 0, -0.05), 'z', p['motor'], n=32)] +
                            [box(1.2, 0.03, 0.03, (0, 0, 0.2), p['steel'], bevel=0), box(0.03, 1.2, 0.03, (0, 0, 0.2), p['steel'], bevel=0)]))
    for i in range(6):
        a = blades + i * math.pi / 3
        box(0.42, 0.16, 0.02, (0.33 * math.cos(a), 0.33 * math.sin(a), 0.12), p['black'], bevel=0)


def ahu(L=3.6, W=1.8, H=2.1):
    """modular double-skin AHU: mixing box with OA louvre, filter, CHW coil, plug fan sections; access doors, handles, drain pan"""
    p = P()
    secs = [(-L / 2, -L / 2 + 0.7, 'mix'), (-L / 2 + 0.7, -L / 2 + 1.2, 'filter'), (-L / 2 + 1.2, -L / 2 + 2.1, 'coil'), (-L / 2 + 2.1, L / 2, 'fan')]
    objs = []
    for x0, x1, kind in secs:
        objs += collect(lambda x0=x0, x1=x1: [box(x1 - x0 - 0.01, H, W, ((x0 + x1) / 2, H / 2 + 0.12, 0), p['ahuPanel'], bevel=0.02)])
        objs += collect(lambda x0=x0, x1=x1: [box(0.04, H + 0.02, W + 0.02, (x1, H / 2 + 0.12, 0), p['steel'], bevel=0.006)])
        if kind in ('filter', 'fan', 'coil'):
            dx = (x1 - x0) * 0.7
            objs += collect(lambda x0=x0, x1=x1, dx=dx: [box(dx, H * 0.8, 0.02, ((x0 + x1) / 2, H / 2 + 0.12, W / 2 + 0.012), p['ahuPanel'], bevel=0.008),
                                                       box(0.03, 0.14, 0.04, ((x0 + x1) / 2 + dx * 0.4, H / 2 + 0.12, W / 2 + 0.03), p['black'], bevel=0.005),
                                                       box(0.06, 0.03, 0.03, ((x0 + x1) / 2 - dx * 0.48, H * 0.8, W / 2 + 0.03), p['steel']),
                                                       box(0.06, 0.03, 0.03, ((x0 + x1) / 2 - dx * 0.48, H * 0.3, W / 2 + 0.03), p['steel'])])
    objs += collect(lambda: [box(L, 0.12, W, (0, 0.06, 0), p['steel'], bevel=0.006)])
    objs += collect(lambda: [box(0.02, 0.06, W * 0.85, (-L / 2 - 0.01, 0.4 + i * 0.09, 0), p['louver'], bevel=0.003) for i in range(14)])
    objs += collect(lambda: [box(0.02, H * 0.6, 0.5, (-L / 2 + 1.65, H * 0.55, W / 2 + 0.02), p['coil'], bevel=0)])   # coil header face
    objs += collect(lambda: [cyl(0.05, 0.4, (-L / 2 + 1.45, 0.6 + i * 0.9, W / 2 + 0.2), 'z', p['steel'], n=24) for i in (0, 1)])
    objs += collect(lambda: [box(0.9, 0.06, 0.4, (-L / 2 + 1.65, 0.16, W / 2 - 0.25), p['steel'], bevel=0.006)])        # drain pan lip
    group('casing', objs)
    group('fanWheel', collect(lambda: [cyl(H * 0.3, 0.25, (L * 0.25, H / 2 + 0.12, 0), 'z', p['steel'], n=48)] +
                              [box(H * 0.26, 0.04, 0.22, (L * 0.25 + H * 0.15 * math.cos(a), H / 2 + 0.12 + H * 0.15 * math.sin(a), 0), p['black'], bevel=0)
                               for a in [i * math.pi / 5 for i in range(10)]]))
    box(0.5, 0.19, 0.004, (-L * 0.25, H * 0.85, W / 2 + 0.03), p['screen'], 'screen', bevel=0)


def vav():
    """pressure-independent VAV box: round inlet with flow cross, rectangular casing, actuator + controller enclosure"""
    p = P()
    group('casing', collect(lambda: [box(0.55, 0.25, 0.6, (0, 0, 0), p['galv'], bevel=0.008),
                                     cyl(0.12, 0.25, (-0.4, 0, 0), 'x', p['galv'], n=32),
                                     box(0.2, 0.22, 0.04, (0.05, 0, 0.32), p['panel'], bevel=0.006),
                                     box(0.14, 0.12, 0.05, (-0.2, 0, 0.33), p['black'], bevel=0.008)] +
                            [cyl(0.004, 0.1, (-0.5, 0, 0.03 * i), 'z', p['steel'], n=8, bevel=0) for i in (-1, 1)]))
    box(0.01, 0.2, 0.2, (-0.3, 0, 0), p['steel'], 'damper', bevel=0)


# ------------------------------------------------------------------ renders (Px sprites)
def render_setup(w, h, run, transparent=True, cam_loc=(5, -6, 3.5), target=(0, 0, 0.9), ortho=None):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 48; sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = w * 2, h * 2
    sc.render.film_transparent = transparent; sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Base Contrast'
    world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True
    world.node_tree.nodes['Background'].inputs['Color'].default_value = (0.82, 0.85, 0.88, 1); world.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.9
    bpy.ops.object.light_add(type='SUN', location=(4, -3, 8)); sun = bpy.context.object; sun.data.energy = 3.5; sun.rotation_euler = Euler((0.75, 0.15, 0.6))
    bpy.ops.object.light_add(type='AREA', location=(-4, -5, 4)); a = bpy.context.object; a.data.energy = 400; a.data.size = 4
    a.rotation_euler = (V(0, 0, 0) - a.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.ops.object.camera_add(location=cam_loc); cam = bpy.context.object; sc.camera = cam
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat('-Z', 'Y').to_euler()
    if ortho:
        cam.data.type = 'ORTHO'; cam.data.ortho_scale = ortho
    else:
        cam.data.lens = 50
    for o in bpy.data.objects:
        if o.name.startswith('beacon') and o.type == 'MESH':
            b = o.data.materials[0].node_tree.nodes['Principled BSDF']
            b.inputs['Emission Strength'].default_value = 6.0 if run else 0.0


def render(path, w, h, bg=None):
    import tempfile
    sc = bpy.context.scene
    tmp = os.path.join(tempfile.mkdtemp(), 'r.png'); sc.render.filepath = tmp
    bpy.ops.render.render(write_still=True)
    from PIL import Image
    im = Image.open(tmp).convert('RGBA').resize((w, h), Image.LANCZOS)
    if bg:
        b = Image.new('RGBA', im.size, bg + (255,)); b.alpha_composite(im); im = b.convert('RGB')
    return im


def fit_camera(obj_names=None, margin=1.05):
    """frame every mesh: camera pulled back along its view axis, ortho scale from the bounding box seen by the camera"""
    sc = bpy.context.scene; cam = sc.camera
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ Vector(c) for o in bpy.data.objects if o.type == 'MESH' for c in o.bound_box]
    centre = sum(pts, Vector()) / len(pts)
    fwd = cam.matrix_world.to_quaternion() @ Vector((0, 0, -1))
    cam.location = centre - fwd * 40.0
    cam.data.clip_start, cam.data.clip_end = 0.1, 200.0
    bpy.context.view_layer.update()
    inv = cam.matrix_world.inverted(); loc = [inv @ p for p in pts]
    xs = [p.x for p in loc]; ys = [p.y for p in loc]
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    cam.location = cam.matrix_world @ Vector((cx, cy, 0))
    rx, ry = sc.render.resolution_x, sc.render.resolution_y
    cam.data.ortho_scale = max((max(xs) - min(xs)) * margin, (max(ys) - min(ys)) * margin * rx / ry)


def sprites(outdir):
    """Px pictures from the same models (same file names and sizes as the R9 / r2 pictures, so no Px page changes):
    3/4 views with transparent background (run = status lamp lit, towers = fan turning) and side / front views on white for the
    overview symbols (v79_2d)."""
    from PIL import Image
    d2 = os.path.join(outdir, 'v79_2d')

    def shot(fn, size, run, cam, tgt, bg=None, margin=1.05, bar=False, **kw):
        reset(); fn(**kw); render_setup(size[0], size[1], run, cam_loc=cam, target=tgt, ortho=1.0); fit_camera(margin=margin)
        im = render(None, *size, bg=bg)
        if bar:                                             # status bar under the symbol: green = running, grey = stopped
            from PIL import ImageDraw
            h = max(3, size[1] // 30); ImageDraw.Draw(im).rectangle([2, size[1] - h - 1, size[0] - 3, size[1] - 2], fill=(46, 204, 113) if run else (160, 168, 176))
        return im

    def gif(frames, path):
        pal = [f.convert('RGB').convert('P', palette=Image.ADAPTIVE) if f.mode != 'RGBA' else f.convert('P', palette=Image.ADAPTIVE) for f in frames]
        pal[0].save(path, save_all=True, append_images=pal[1:], duration=120, loop=0, disposal=2)

    iso_ch, iso_p, iso_t = ((6.2, -5.4, 3.6), (0, 0, 0.9)), ((3.4, -3.6, 2.0), (0, 0, 0.5)), ((5.5, -6.5, 5.0), (0, 0, 1.6))
    for run in (False, True):
        shot(chiller, (260, 164), run, *iso_ch).save(os.path.join(outdir, f"v79_chiller_{'on' if run else 'off'}.png"))
        im = shot(pump, (112, 73), run, *iso_p)
        im.save(os.path.join(outdir, f"v79_pump_l_{'on' if run else 'off'}.png"))
        im.transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(outdir, f"v79_pump_r_{'on' if run else 'off'}.png"))
    shot(tower, (212, 203), False, *iso_t, blades=0.0).save(os.path.join(outdir, 'v79_ct_off.png'))
    frames = [shot(tower, (212, 203), True, *iso_t, blades=i * math.pi / 18) for i in range(6)]
    bgf = [Image.alpha_composite(Image.new('RGBA', f.size, (255, 255, 255, 0)), f) for f in frames]
    bgf[0].save(os.path.join(outdir, 'v79_ct_on.gif'), save_all=True, append_images=bgf[1:], duration=120, loop=0, disposal=2, transparency=0)
    side, white = ((0.6, -9, 1.4), (0, 0, 1.0)), (255, 255, 255)
    for fname, fn, size in (('chiller', chiller, (320, 120)), ('pump', pump, (128, 80)), ('tower', tower, (240, 136))):
        off = shot(fn, size, False, *side, bg=white, margin=1.12, bar=True)
        off.save(os.path.join(d2, f'{fname}_off.png'))
        if fname == 'tower':
            gif([shot(tower, size, True, *side, bg=white, margin=1.12, bar=True, blades=i * math.pi / 18) for i in range(6)], os.path.join(d2, 'tower_run.gif'))
        else:
            on = shot(fn, size, True, *side, bg=white, margin=1.12, bar=True)
            gif([on, on], os.path.join(d2, f'{fname}_run.gif'))
            if fname == 'pump':
                off.transpose(Image.FLIP_LEFT_RIGHT).save(os.path.join(d2, 'pump_mirror_off.png'))
                gif([on.transpose(Image.FLIP_LEFT_RIGHT)] * 2, os.path.join(d2, 'pump_mirror_run.gif'))
    front = ((0, -9, 0.1), (0, 0, 0))
    shot(fan, (48, 48), False, *front, bg=(243, 245, 245), margin=1.12, bar=True).save(os.path.join(d2, 'fan_off.png'))
    gif([shot(fan, (48, 48), True, *front, bg=(243, 245, 245), margin=1.12, bar=True, blades=i * math.pi / 18) for i in range(6)], os.path.join(d2, 'fan_run.gif'))
    print('Px pictures rendered into', outdir)


if __name__ == '__main__':
    for name, fn in (('chiller', chiller), ('pump', pump), ('tower', tower), ('ahu', ahu), ('vav', vav)):
        reset(); fn(); export(os.path.join(OUT, f'{name}.glb'))
    if RENDER: sprites(RENDER)
