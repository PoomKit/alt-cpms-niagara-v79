"""Render an ORIGINAL generic wall-mount HVAC variable-speed-drive image (no manufacturer logo / trade dress) for the Px faceplates.
To use the official vendor product image (e.g. the project's ABB drive), replace shared/px/img/vsd_drive.png with it (same aspect).
usage: python3 vsd3d.py out.png [W H]"""
import sys, math
import bpy
from mathutils import Vector
OUT = sys.argv[1]; W = int(sys.argv[2]) if len(sys.argv) > 2 else 300; H = int(sys.argv[3]) if len(sys.argv) > 3 else 520
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene


def mat(n, rgb, metal=0.0, rough=0.4, emit=None, es=2.0):
    m = bpy.data.materials.new(n); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Metallic'].default_value = metal; b.inputs['Roughness'].default_value = rough
    if emit: b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = es
    return m


def box(p, s, m, bev=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=p); o = bpy.context.object; o.scale = s
    bpy.ops.object.transform_apply(scale=True)
    if bev: md = o.modifiers.new('b', 'BEVEL'); md.width = bev; md.segments = 4
    o.data.materials.append(m); return o


shell = mat('shell', (0.86, 0.87, 0.88), rough=0.35)
cover = mat('cover', (0.78, 0.79, 0.80), rough=0.45)
dark = mat('dark', (0.04, 0.045, 0.05), rough=0.5)
slot = mat('slot', (0.08, 0.085, 0.09), rough=0.8)
fin = mat('fin', (0.3, 0.32, 0.34), metal=0.8, rough=0.35)
lcd = mat('lcd', (0.02, 0.08, 0.1), emit=(0.25, 0.85, 1.0), es=1.4)
key = mat('key', (0.18, 0.19, 0.2), rough=0.5)
led = mat('led', (0.1, 0.9, 0.3), emit=(0.1, 1.0, 0.3), es=6)
accent = mat('accent', (0.15, 0.35, 0.6), rough=0.4)
# body (x = width, y = depth, z = height), front face at y = -0.09
box((0, 0, 0.31), (0.26, 0.18, 0.62), shell, 0.012)
box((0, -0.0905, 0.17), (0.235, 0.004, 0.30), cover, 0.004)             # lower terminal cover
for k in range(7):                                                         # ventilation slots
    box((0, -0.093, 0.05 + k * 0.018), (0.16, 0.003, 0.006), slot)
box((0, -0.093, 0.335), (0.235, 0.003, 0.012), accent)                    # accent line (neutral blue)
box((0, -0.0915, 0.47), (0.13, 0.006, 0.17), dark, 0.01)                  # control panel
box((0, -0.0955, 0.515), (0.105, 0.002, 0.055), lcd)                      # display
for i, dx in enumerate((-0.035, 0.0, 0.035)):
    box((dx, -0.0955, 0.455), (0.024, 0.004, 0.014), key, 0.002)
box((0, -0.0955, 0.425), (0.05, 0.004, 0.018), key, 0.003)
box((0.052, -0.0955, 0.405), (0.008, 0.003, 0.008), led)
for k in range(9):                                                         # side heatsink fins
    box((0.132, -0.07 + k * 0.017, 0.33), (0.012, 0.004, 0.46), fin)
for x in (-0.07, 0.07):                                                    # cable glands
    bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=0.03, location=(x, -0.02, -0.01)); o = bpy.context.object; o.data.materials.append(dark)
bpy.ops.object.camera_add(location=(0.55, -1.25, 0.72)); cam = bpy.context.object
cam.data.type = 'ORTHO'; cam.data.ortho_scale = 0.74
cam.rotation_mode = 'QUATERNION'; cam.rotation_quaternion = (Vector((0.0, 0.0, 0.3)) - cam.location).to_track_quat('-Z', 'Y'); sc.camera = cam
bpy.ops.object.light_add(type='AREA', location=(-0.6, -1.2, 1.2)); a = bpy.context.object; a.data.energy = 60; a.data.size = 1.5
a.rotation_euler = (math.radians(55), 0, math.radians(-25))
bpy.ops.object.light_add(type='SUN', location=(0, 0, 3)); s = bpy.context.object; s.data.energy = 2.0; s.rotation_euler = (math.radians(35), math.radians(20), math.radians(20))
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[1].default_value = 0.5
sc.render.engine = 'CYCLES'; sc.cycles.samples = 64; sc.cycles.use_denoising = True
sc.render.film_transparent = True; sc.render.resolution_x, sc.render.resolution_y = W, H
sc.render.image_settings.color_mode = 'RGBA'; sc.render.filepath = OUT
bpy.ops.render.render(write_still=True); print('ok', OUT)
