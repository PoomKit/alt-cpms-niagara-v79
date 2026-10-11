"""V7.4 2-D sprites + faceplate images from assets74 (Blender, orthographic).  Writes <outdir>/<name>.png + sprites74.json.
  valves   v74_bfv_{onoff|mod}_{h|v}_{0..8}  (open 0..100 % in 12.5 % steps: actuator arrow turns + position bar), v74_bfv_man_{h|v}
  sensors  v74_tt_{top|bot|left|right}, v74_pt_{top|bot|left|right}, v74_fm_{h|v|vl}, v74_btu_h, v74_oa, v74_vsd_{on|off}
  faceplates v74_fp_{vsd_on|vsd_off|fm|btu|me96|oa|tt|pt}
usage: python3 sprites74.py outdir [samples]"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import assets73 as A
import assets74 as B

OUT = sys.argv[1]; SAMPLES = int(sys.argv[2]) if len(sys.argv) > 2 else 40
ONLY = sys.argv[3].split(',') if len(sys.argv) > 3 else None
os.makedirs(OUT, exist_ok=True)
A.reset(); sc = bpy.context.scene
A.sun_and_world(sc, 3.0, strength=0.9)
bpy.ops.object.light_add(type='AREA', location=(-3, -8, 6)); ar = bpy.context.object; ar.data.energy = 900; ar.data.size = 8
ar.rotation_euler = (math.radians(55), 0, math.radians(-20))
A.render_setup(sc, 64, 64, SAMPLES)
bpy.ops.object.camera_add(); cam = bpy.context.object; cam.data.type = 'ORTHO'; sc.camera = cam
KEEP = {o.name for o in bpy.data.objects}
JS = os.path.join(OUT, 'sprites74.json')
RES = json.load(open(JS)) if os.path.exists(JS) else {}
mm = B.M4()
R = 0.085
PIPE = {'chws': A.mat('pipe_chws', A.SVC['chws'], metal=0.25, rough=0.26, coat=0.5)}


def clear():
    for o in list(bpy.data.objects):
        if o.name not in KEEP: bpy.data.objects.remove(o, do_unlink=True)


def shoot(name, center, wpx, hpx, ppm, anchors, pitch=18.0, yaw=0.0):
    if ONLY and not any(name.startswith(o) for o in ONLY): return
    sc.render.resolution_x, sc.render.resolution_y = wpx, hpx
    cam.data.ortho_scale = max(wpx, hpx) / ppm
    p, yw = math.radians(pitch), math.radians(yaw)
    d = Vector((math.sin(yw) * math.cos(p), math.cos(yw) * math.cos(p), -math.sin(p)))
    cam.location = Vector(center) - d * 30
    cam.rotation_mode = 'QUATERNION'; cam.rotation_quaternion = d.to_track_quat('-Z', 'Y')
    sc.render.filepath = os.path.join(OUT, name + '.png')
    bpy.ops.render.render(write_still=True)
    an = {}
    for k, q in anchors.items():
        v = world_to_camera_view(sc, cam, Vector(q))
        an[k] = (round(v.x * wpx, 1), round((1 - v.y) * hpx, 1))
    RES[name] = {'size': [wpx, hpx], 'anchors': an}
    print('sprite', name, an, flush=True)


def stubs(axis, length=0.30):
    a = A.AX(axis)
    A.cyl_dir(-a * length, -a * 0.075, R, PIPE['chws']); A.cyl_dir(a * 0.075, a * length, R, PIPE['chws'])


# ---------------------------------------------------------------- butterfly valves, 9 positions
for mode in ('onoff', 'mod'):
    for orient in ('h', 'v'):
        for k in range(9):
            clear()
            if orient == 'h':
                an = B.bfv4((0, 0, 0), 'x', R, mode, 'z', k / 8, mm, moving=False)
                shoot(f'v74_bfv_{mode}_h_{k}', (0, 0, 0.255), 40, 56, 70, {'c': (0, 0, 0), 'top': an['top'], 'act': (0, 0, 0.378)}, pitch=24)
            else:
                an = B.bfv4((0, 0, 0), 'z', R, mode, 'x', k / 8, mm, moving=False)
                shoot(f'v74_bfv_{mode}_v_{k}', (0.255, 0, 0), 56, 40, 70, {'c': (0, 0, 0), 'top': an['top'], 'act': (0.378, 0, 0)}, pitch=14)
for orient in ('h', 'v'):
    clear()
    if orient == 'h':
        B.bfv4((0, 0, 0), 'x', R, 'onoff', 'z', 0, mm, handwheel=True)
        shoot('v74_bfv_man_h', (0, 0, 0.21), 40, 48, 70, {'c': (0, 0, 0)}, pitch=24)
    else:
        B.bfv4((0, 0, 0), 'z', R, 'onoff', 'x', 0, mm, handwheel=True)
        shoot('v74_bfv_man_v', (0.21, 0, 0), 48, 40, 70, {'c': (0, 0, 0)}, pitch=14)

# ---------------------------------------------------------------- temperature / pressure transmitters (4 orientations)
ORI = {'top': ('x', 'z', (0, 0, 0.16)), 'bot': ('x', '-z', (0, 0, -0.16)), 'left': ('z', '-x', (-0.16, 0, 0)), 'right': ('z', 'x', (0.16, 0, 0))}
for o, (pax, up, ctr) in ORI.items():
    clear()
    u = A.AX(up)
    B.rtd(u * R, up, mm, s=1.0)
    wpx, hpx = (30, 42) if o in ('top', 'bot') else (42, 30)
    shoot(f'v74_tt_{o}', ctr, wpx, hpx, 96, {'c': (0, 0, 0)}, pitch=20 if o in ('top', 'bot') else 12)
    clear()
    B.ptx(u * R, up, mm, s=1.0)
    ctr2 = tuple(c * 1.35 for c in ctr)
    wpx, hpx = (30, 50) if o in ('top', 'bot') else (50, 30)
    shoot(f'v74_pt_{o}', ctr2, wpx, hpx, 96, {'c': (0, 0, 0)}, pitch=20 if o in ('top', 'bot') else 12)

# ---------------------------------------------------------------- insertion magmeter (h, v right), BTU (meter + System-10)
clear(); B.ins_magmeter((0, 0, 0), 'z', R, mm)
shoot('v74_fm_h', (0, 0, 0.27), 36, 52, 84, {'c': (0, 0, 0)}, pitch=20)
clear(); B.ins_magmeter((0, 0, 0), 'x', R, mm)
shoot('v74_fm_v', (0.27, 0, 0), 52, 36, 84, {'c': (0, 0, 0)}, pitch=12)
clear(); B.ins_magmeter((0, 0, 0), '-x', R, mm)
shoot('v74_fm_vl', (-0.27, 0, 0), 52, 36, 84, {'c': (0, 0, 0)}, pitch=12)
clear(); a = B.ins_magmeter((0, 0, 0), 'z', R, mm)
bx = B.btu_system10((0.56, 0.02, 0.42), mm, s=0.9)
A.cyl_dir(a['head'] + Vector((0.075, 0, -0.03)), Vector(bx['cables'][0]) + Vector((0, 0, -0.04)), 0.007, mm['cable'])
shoot('v74_btu_h', (0.22, 0, 0.28), 94, 64, 76, {'c': (0, 0, 0)}, pitch=16)

# ---------------------------------------------------------------- small drive / OA sprites
for st in ('on', 'off'):
    clear(); B.ach580((0, 0, 0), mm, s=1.0, running=(st == 'on'))
    shoot(f'v74_vsd_{st}', (0, 0, 0.28), 40, 62, 100, {'top': (0, 0, 0.56)}, pitch=10, yaw=-12)
clear(); a = B.oa_shield((0, 0, 0), mm, s=1.0)
shoot('v74_oa', (-0.06, 0, 0.55), 40, 76, 64, {'top': a['top']}, pitch=10, yaw=-10)

# ---------------------------------------------------------------- faceplate images (large)
for st in ('on', 'off'):
    clear(); B.ach580((0, 0, 0), mm, s=1.0, running=(st == 'on'))
    shoot(f'v74_fp_vsd_{st}', (0, 0, 0.28), 200, 330, 520, {}, pitch=12, yaw=-24)
clear(); A.cyl_dir((-0.3, 0, 0), (0.3, 0, 0), R, PIPE['chws']); B.ins_magmeter((0, 0, 0), 'z', R, mm)
shoot('v74_fp_fm', (0, 0, 0.26), 220, 280, 420, {}, pitch=18, yaw=-22)
clear(); A.cyl_dir((-0.35, 0, 0), (0.35, 0, 0), R, PIPE['chws']); a = B.ins_magmeter((0, 0, 0), 'z', R, mm)
bx = B.btu_system10((0.62, 0.02, 0.42), mm, s=1.0)
A.cyl_dir(a['head'] + Vector((0.075, 0, -0.03)), Vector(bx['cables'][0]) + Vector((0, 0, -0.04)), 0.007, mm['cable'])
for k, xx in enumerate((-0.3, 0.3)):
    B.rtd((xx, 0, R), 'z', mm, s=1.0)
shoot('v74_fp_btu', (0.2, 0, 0.26), 330, 220, 300, {}, pitch=16, yaw=-18)
clear(); B.me96((0, 0, 0), mm, s=1.0)
shoot('v74_fp_me96', (0, 0, 0), 220, 220, 850, {}, pitch=8, yaw=-14)
clear(); a = B.oa_shield((0, 0, 0), mm, s=1.0)
shoot('v74_fp_oa', (-0.08, 0, 0.55), 200, 330, 270, {}, pitch=10, yaw=-18)
clear(); A.cyl_dir((-0.2, 0, 0), (0.2, 0, 0), R, PIPE['chws']); B.rtd((0, 0, R), 'z', mm)
shoot('v74_fp_tt', (0, 0, 0.16), 160, 200, 520, {}, pitch=20, yaw=-24)
clear(); A.cyl_dir((-0.2, 0, 0), (0.2, 0, 0), R, PIPE['chws']); B.ptx((0, 0, R), 'z', mm)
shoot('v74_fp_pt', (0, 0, 0.24), 160, 220, 480, {}, pitch=20, yaw=-24)

json.dump(RES, open(JS, 'w'), indent=1)
print('done', len(RES))
