"""V7.3 2-D sprites for the schematic Px pages, rendered from the SAME Blender assets as the 3-D views (tools/assets73.py):
front elevation, orthographic, slight top view.  Writes <outdir>/<name>.png + sprites73.json {name: {size, anchors(px)}}.
usage: python3 sprites73.py outdir [samples]"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
import assets73 as A

OUT = sys.argv[1]; SAMPLES = int(sys.argv[2]) if len(sys.argv) > 2 else 48
os.makedirs(OUT, exist_ok=True)
A.reset(); sc = bpy.context.scene
A.sun_and_world(sc, 3.0, strength=0.9)
bpy.ops.object.light_add(type='AREA', location=(-3, -8, 6)); ar = bpy.context.object; ar.data.energy = 900; ar.data.size = 8
ar.rotation_euler = (math.radians(55), 0, math.radians(-20))
LIGHTS = {o.name for o in bpy.data.objects}
A.render_setup(sc, 64, 64, SAMPLES)
bpy.ops.object.camera_add(); cam = bpy.context.object; cam.data.type = 'ORTHO'; sc.camera = cam
KEEP = LIGHTS | {cam.name}
RES = {}


def clear():
    for o in list(bpy.data.objects):
        if o.name not in KEEP: bpy.data.objects.remove(o, do_unlink=True)


def shoot(name, center, wpx, hpx, ppm, anchors, pitch=18.0, yaw=0.0):
    """render the current objects: image wpx x hpx, ppm pixels per metre, camera looking +y pitched down."""
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


mm = A.M()
R = 0.085            # 2-D pipe: 10 px at ~60 px/m

# ---- cooling tower, 2 cells: stopped (blades) and running (motion blur)
for state in ['off'] + [f'on_f{k}' for k in range(6)]:
    clear()
    k = int(state[-1]) if state != 'off' else 0
    an = A.tower((0, 0, 0), 2, mm, running=(state != 'off', state != 'off'), fan_angle=0.35 + k * math.tau / 36)
    # inlet stub (hot water, top left) + outlet stub (basin, left)
    ix, iy, iz = an['inlet']; ox, oy, oz = an['outlet']
    A.cyl_dir((ix - 0.5, iy, iz), (ix + 0.1, iy, iz), 0.16, mm['frp_dark'])
    A.cyl_dir((ox - 0.5, oy, oz), (ox + 0.1, oy, oz), 0.18, mm['frp_dark'])
    shoot(f'v73_ct2_{state}', (-0.25, 0, 2.75), 198, 194, 31, {'inlet': (ix - 0.5, iy, iz), 'outlet': (ox - 0.5, oy, oz),
          'cell1': an['cell1'], 'cell2': an['cell2'], 'basin': an['basin_front'], 'makeup': an['makeup']}, pitch=30)

# ---- butterfly valves (pipe stub shown so the joint is shaded like the pipe layer)
for mode in ('onoff', 'mod', 'man'):
    for orient in ('h', 'v'):
        clear()
        if orient == 'h':
            A.butterfly((0, 0, 0), 'x', r=R, mode='onoff' if mode == 'man' else mode, up='z', mm=mm, handwheel=(mode == 'man'))
            shoot(f'v73_bfv_{mode}_h', (0, 0, 0.26), 40, 52, 70, {'c': (0, 0, 0)}, pitch=14)
        else:
            A.butterfly((0, 0, 0), 'z', r=R, mode='onoff' if mode == 'man' else mode, up='x', mm=mm, handwheel=(mode == 'man'))
            shoot(f'v73_bfv_{mode}_v', (0.26, 0, 0), 52, 40, 70, {'c': (0, 0, 0)}, pitch=10)

# ---- electromagnetic flow meter (h / v), BTU meter (meter + calculator)
clear(); A.magmeter((0, 0, 0), 'x', r=R, mm=mm)
shoot('v73_fm_h', (0, 0, 0.18), 48, 56, 70, {'c': (0, 0, 0)}, pitch=14)
clear(); A.magmeter((0, 0, 0), 'z', r=R, mm=mm, up='x')
shoot('v73_fm_v', (0.18, 0, 0), 56, 48, 70, {'c': (0, 0, 0)}, pitch=10)
clear(); A.magmeter((0, 0, 0), 'x', r=R, mm=mm); A.btu_calc((0.52, -0.05, 0.45), mm)
A.cyl_dir((0.1, 0, 0.3), (0.4, 0, 0.35), 0.008, mm['cable'])
shoot('v73_btu_h', (0.2, 0, 0.26), 92, 64, 70, {'c': (0, 0, 0)}, pitch=14)

# ---- expansion tank, pot feeder, dosing skid, RPZ, solenoid, gate valve, VSD, chemical tank
clear(); a = A.exp_tank((0, 0, 0), mm, r=0.3, h=0.9)
shoot('v73_exptank', (0, 0, 0.75), 52, 96, 60, {'bottom': a['bottom']}, pitch=12)
clear(); a = A.pot_feeder((0, 0, 0), mm)
shoot('v73_potfeeder', (0.05, 0, 0.78), 60, 100, 62, {'in': a['in'], 'out': a['out']}, pitch=12)
clear(); a = A.dosing_skid((0, 0, 0), mm)
shoot('v73_dosing', (0.05, 0, 0.6), 84, 84, 62, {'out': a['out']}, pitch=14)
clear(); A.rpz((0, 0, 0), 'x', mm)
shoot('v73_rpz', (0, 0, 0.05), 96, 56, 80, {'c': (0, 0, 0)}, pitch=14)
clear(); A.solenoid((0, 0, 0), 'x', r=0.035, mm=mm)
shoot('v73_sol_h', (0, 0, 0.12), 28, 40, 80, {'c': (0, 0, 0)}, pitch=14)
clear(); A.gate_valve((0, 0, 0), 'x', 0.05, mm)
shoot('v73_gate_h', (0, 0, 0.14), 30, 42, 80, {'c': (0, 0, 0)}, pitch=14)
clear(); A.gate_valve((0, 0, 0), 'z', 0.05, mm, up='x')
shoot('v73_gate_v', (0.14, 0, 0), 42, 30, 80, {'c': (0, 0, 0)}, pitch=10)
for st in ('on', 'off'):
    clear(); A.vsd((0, 0, 0), mm, running=(st == 'on'))
    shoot(f'v73_vsd_{st}', (0, 0, 0.52), 40, 62, 56, {'top': (0, 0, 1.05)}, pitch=10)
clear(); A.oa_sensor((0, 0, 0), mm)
shoot('v73_oa', (0.05, 0, 1.6), 44, 96, 60, {'top': (0, 0, 2.2)}, pitch=10)

# running tower = animated GIF (6 frames, 60 deg / 6 blades = seamless loop); edges pre-blended on the page background
from PIL import Image
import numpy as np
BGC = np.array((0x12, 0x16, 0x1b), np.float32)
frames = []
for k in range(6):
    im = np.asarray(Image.open(os.path.join(OUT, f'v73_ct2_on_f{k}.png')).convert('RGBA')).astype(np.float32)
    a = im[..., 3:4] / 255.0
    rgb = im[..., :3] * a + BGC * (1 - a)
    rgba = np.concatenate([rgb, np.where(a > 0.35, 255, 0)], -1).astype(np.uint8)
    frames.append(Image.fromarray(rgba, 'RGBA'))
ref = frames[0].convert('RGB').quantize(255, method=Image.Quantize.MEDIANCUT)
out = []
for f in frames:
    q = f.convert('RGB').quantize(palette=ref, dither=Image.Dither.NONE)
    arr = np.asarray(q).copy(); arr[np.asarray(f)[..., 3] == 0] = 255
    q = Image.fromarray(arr, 'P'); q.putpalette(ref.getpalette()[:765] + [0, 0, 0])
    out.append(q)
out[0].save(os.path.join(OUT, 'v73_ct2_on.gif'), save_all=True, append_images=out[1:], duration=90, loop=0, transparency=255, disposal=2)
RES['v73_ct2_on'] = dict(RES['v73_ct2_on_f0'])
for k in range(6):
    RES.pop(f'v73_ct2_on_f{k}'); os.remove(os.path.join(OUT, f'v73_ct2_on_f{k}.png')) if k else None
json.dump(RES, open(os.path.join(OUT, 'sprites73.json'), 'w'), indent=1)
print('done', len(RES))
