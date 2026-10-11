"""V7.3 zone floor plan (Blender / Cycles): cut-away 3-D plan of the reference floor, rooms = AirPlug / Sense-T zones.
Orthographic camera pitched about the X axis only, so every rectangular room projects to an axis-aligned rectangle ->
the Px page overlays a live temperature-coloured rectangle + value card exactly on each room.
usage: python3 floor73.py out.png rooms.json [W H samples]"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import assets73 as A

OUT, RJ = sys.argv[1], sys.argv[2]
W = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
H = int(sys.argv[4]) if len(sys.argv) > 4 else 820
SAMPLES = int(sys.argv[5]) if len(sys.argv) > 5 else 64
A.reset(); sc = bpy.context.scene; mm = A.M()
ROOMS = {  # code: (x0, y0, x1, y1)  metres; y grows away from the viewer
    '01_0101': (0, 0, 14, 12), '01_0102': (14, 0, 22, 12), '01_0103': (22, 0, 40, 12), '01_0104': (40, 0, 60, 12),
    '01_0112': (0, 12, 60, 15),
    '01_0105': (0, 15, 10, 30), '01_0106': (10, 15, 18, 30), '01_0107': (18, 15, 32, 30), '01_0108': (32, 15, 42, 30),
    '01_0109': (42, 15, 48, 24), '01_0110': (48, 15, 54, 24), '01_0111': (54, 15, 60, 24)}
CORE = (42, 24, 60, 30)
floor_m = A.mat('room_floor', (0.42, 0.45, 0.48), rough=0.7)
floor_alt = A.mat('room_floor2', (0.38, 0.41, 0.44), rough=0.7)
wall_m = A.mat('pwall', (0.86, 0.87, 0.88), rough=0.6)
wall_top = A.mat('pwall_top', (0.30, 0.32, 0.34), rough=0.6)
glass = A.mat('pglass', (0.55, 0.75, 0.85), rough=0.05, alpha=0.35)
furn = A.mat('furn', (0.36, 0.38, 0.41), rough=0.5)
furn_l = A.mat('furn_l', (0.78, 0.76, 0.72), rough=0.5)
rack = A.mat('rack', (0.08, 0.09, 0.1), rough=0.4)
core_m = A.mat('core', (0.28, 0.29, 0.30), rough=0.8)
puck = A.mat('puck', (0.97, 0.97, 0.97), rough=0.3)
puck_led = A.mat('puck_led', (0.1, 0.7, 1.0), emit=(0.1, 0.6, 1.0), es=6.0)
WH, WT = 2.0, 0.2                                                   # cut-away wall height / thickness
A.box((30, 15, -0.3), (62, 32, 0.6), A.mat('slab', (0.20, 0.21, 0.22), rough=0.9))
for i, (code, (x0, y0, x1, y1)) in enumerate(ROOMS.items()):
    A.box(((x0 + x1) / 2, (y0 + y1) / 2, 0.01), (x1 - x0 - 0.02, y1 - y0 - 0.02, 0.02), floor_m if i % 2 == 0 else floor_alt)
A.box(((CORE[0] + CORE[2]) / 2, (CORE[1] + CORE[3]) / 2, 0.5), (CORE[2] - CORE[0], CORE[3] - CORE[1], 1.0), core_m)
for k in range(6):                                                  # stairs in the core
    A.box((CORE[0] + 2 + k * 0.6, 27, 0.1 + k * 0.15), (0.6, 3.5, 0.2 + k * 0.3), wall_m)


def wall(x0, y0, x1, y1, door=None, glazed=False, doors=()):
    """wall segment along x or y with door gaps (centre, width)"""
    doors = sorted(list(doors) + ([door] if door else []))
    segs, a = [], (x0 if y0 == y1 else y0)
    for c, w in doors:
        segs.append((a, c - w / 2)); a = c + w / 2
    segs.append((a, x1 if y0 == y1 else y1))
    segs = [(p, y0, q, y1) if y0 == y1 else (x0, p, x1, q) for p, q in segs]
    for a, b, c_, d in segs:
        L = max(abs(c_ - a), abs(d - b))
        if L < 0.05: continue
        s = (L, WT, WH) if b == d else (WT, L, WH)
        A.box(((a + c_) / 2, (b + d) / 2, WH / 2), s, glass if glazed else wall_m)
        A.box(((a + c_) / 2, (b + d) / 2, WH + 0.02), (s[0], s[1], 0.04), wall_top)


# external walls (front facade glazed)
wall(0, 0, 60, 0, glazed=True); wall(0, 30, 60, 30); wall(0, 0, 0, 30); wall(60, 0, 60, 30)
# corridor walls with doors
wall(0, 12, 60, 12, doors=((7, 2.0), (18, 1.6), (31, 1.6), (50, 1.6)))
wall(0, 15, 60, 15, doors=((5, 1.4), (14, 1.4), (25, 1.6), (37, 1.4), (45, 1.2), (51, 1.2), (57, 1.2)))
for x, d in ((14, 6), (22, 6), (40, 6)): wall(x, 0, x, 12, door=(d, 1.6))
for x in (10, 18, 32, 42, 48, 54): wall(x, 15, x, 30 if x <= 42 else 24)
wall(42, 24, 60, 24)
for x0, x1, dc in ((10, 18, 14), (18, 32, 25), (32, 42, 37)): pass
# furniture
for cx in range(24, 39, 4):                                         # open office desks
    for cy in (3, 7):
        A.box((cx, cy, 0.38), (3.2, 1.4, 0.05), furn_l); A.box((cx, cy, 0.19), (3.0, 1.2, 0.36), furn)
for cx in range(43, 59, 4):
    for cy in (3, 7):
        A.box((cx, cy, 0.38), (3.2, 1.4, 0.05), furn_l); A.box((cx, cy, 0.19), (3.0, 1.2, 0.36), furn)
A.box((7, 5, 0.5), (6, 1.0, 1.0), furn_l)                                     # lobby counter
for cx, cy in ((3, 8), (11, 8), (4, 3)): A.box((cx, cy, 0.25), (2.2, 1.2, 0.5), furn)
A.box((18, 6, 0.5), (4, 1.0, 1.0), furn_l)                                    # reception desk
for x0, x1 in ((0, 10), (10, 18)):                                            # meeting tables
    A.box(((x0 + x1) / 2, 22.5, 0.38), (min(6, x1 - x0 - 2.5), 2.4, 0.06), furn_l)
for cx in range(20, 31, 3):                                                   # training rows
    for cy in (18, 22, 26): A.box((cx, cy, 0.38), (2.4, 1.0, 0.06), furn_l)
A.box((37, 22, 0.38), (4, 2, 0.06), furn_l); A.box((37, 22, 0.19), (3.6, 1.6, 0.36), furn)
for k in range(4): A.box((43.5 + k * 1.1, 19.5, 1.0), (0.8, 1.1, 2.0), rack)  # server racks
A.box((51, 16.5, 0.5), (5, 0.8, 1.0), furn_l)                                 # pantry counter
for k in range(3): A.box((55.5 + k * 1.4, 21, 0.9), (1.0, 3.0, 1.8), furn)    # storage shelves
# Sense-T / AirPlug sensor puck in every zone (wall mounted)
SENS = {}
for code, (x0, y0, x1, y1) in ROOMS.items():
    px, py = (x0 + 1.0, y1 - 0.25) if code != '01_0112' else (30, 14.75)
    A.cyl((px, py, WH - 0.2), 0.16, 0.08, 'y', puck, 24); A.cyl((px, py - 0.045, WH - 0.2), 0.03, 0.01, 'y', puck_led, 12)
    SENS[code] = (px, py, WH - 0.2)

A.sun_and_world(sc, 1.6, strength=0.5)
bpy.ops.object.light_add(type='AREA', location=(30, -10, 40)); ar = bpy.context.object; ar.data.energy = 9000; ar.data.size = 40
ar.rotation_euler = (math.radians(20), 0, 0)
A.render_setup(sc, W, H, SAMPLES)
PITCH = math.radians(52)
d = Vector((0, math.cos(PITCH), -math.sin(PITCH)))
tgt = Vector((30, 15, 0))
cam = A.ortho_cam(sc, tgt - d * 80, tgt, 63.0); sc.camera = cam
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
res = {}
for code, (x0, y0, x1, y1) in list(ROOMS.items()) + [('CORE', CORE)]:
    a = world_to_camera_view(sc, cam, Vector((x0, y0, 0))); b = world_to_camera_view(sc, cam, Vector((x1, y1, 0)))
    res[code] = {'rect': [round(a.x * W, 1), round((1 - b.y) * H, 1), round(b.x * W, 1), round((1 - a.y) * H, 1)]}
    if code in SENS:
        s = world_to_camera_view(sc, cam, Vector(SENS[code])); res[code]['sensor'] = [round(s.x * W, 1), round((1 - s.y) * H, 1)]
json.dump({'size': [W, H], 'rooms': res}, open(RJ, 'w'), indent=1)
print('floor ok', OUT)
