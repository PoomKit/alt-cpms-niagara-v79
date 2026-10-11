import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Vector
import assets73 as A, assets74 as B
OUT = sys.argv[1]; which = sys.argv[2].split(',') if len(sys.argv) > 2 else None
A.reset(); sc = bpy.context.scene
A.sun_and_world(sc, 3.0, strength=0.9)
bpy.ops.object.light_add(type='AREA', location=(-3, -8, 6)); ar = bpy.context.object; ar.data.energy = 900; ar.data.size = 8
ar.rotation_euler = (math.radians(55), 0, math.radians(-20))
A.render_setup(sc, 64, 64, 24)
bpy.ops.object.camera_add(); cam = bpy.context.object; cam.data.type = 'ORTHO'; sc.camera = cam
KEEP = {o.name for o in bpy.data.objects}
def clear():
    for o in list(bpy.data.objects):
        if o.name not in KEEP: bpy.data.objects.remove(o, do_unlink=True)
def shoot(name, center, w, h, ppm, pitch=18, yaw=-20):
    sc.render.resolution_x, sc.render.resolution_y = w, h
    cam.data.ortho_scale = max(w, h) / ppm
    p, yw = math.radians(pitch), math.radians(yaw)
    d = Vector((math.sin(yw) * math.cos(p), math.cos(yw) * math.cos(p), -math.sin(p)))
    cam.location = Vector(center) - d * 30; cam.rotation_mode = 'QUATERNION'; cam.rotation_quaternion = d.to_track_quat('-Z', 'Y')
    sc.render.filepath = os.path.join(OUT, name + '.png'); bpy.ops.render.render(write_still=True)
mm = B.M4()
jobs = {
 'rtd': lambda: (A.cyl_dir((-0.25,0,0),(0.25,0,0),0.085,mm['steel']), B.rtd((0,0,0.085),'z',mm)),
 'ptx': lambda: (A.cyl_dir((-0.25,0,0),(0.25,0,0),0.085,mm['steel']), B.ptx((0,0,0.085),'z',mm)),
 'bfv0': lambda: (A.cyl_dir((-0.3,0,0),(0.3,0,0),0.085,A.mat('p',(0.03,0.22,0.85),0.25,0.26)), B.bfv4((0,0,0),'x',0.085,'onoff','z',0.0,mm)),
 'bfv50': lambda: (A.cyl_dir((-0.3,0,0),(0.3,0,0),0.085,A.mat('p',(0.03,0.22,0.85),0.25,0.26)), B.bfv4((0,0,0),'x',0.085,'mod','z',0.5,mm, moving=True)),
 'bfv100': lambda: (A.cyl_dir((-0.3,0,0),(0.3,0,0),0.085,A.mat('p',(0.03,0.22,0.85),0.25,0.26)), B.bfv4((0,0,0),'x',0.085,'onoff','z',1.0,mm)),
 'fm': lambda: (A.cyl_dir((-0.3,0,0),(0.3,0,0),0.085,A.mat('p',(0.03,0.22,0.85),0.25,0.26)), B.ins_magmeter((0,0,0),'z',0.085,mm)),
 'btu': lambda: B.btu_system10((0,0,0),mm),
 'me96': lambda: B.me96((0,0,0),mm),
 'ach580': lambda: B.ach580((0,0,0),mm),
 'oa': lambda: B.oa_shield((0,0,0),mm),
}
views = {'rtd': ((0,0,0.2),260,300,900), 'ptx': ((0,0,0.2),260,300,900), 'bfv0': ((0,0,0.25),300,380,650), 'bfv50': ((0,0,0.25),300,380,650),
         'bfv100': ((0,0,0.25),300,380,650), 'fm': ((0,0,0.3),300,380,650), 'btu': ((0,0,0),300,360,800), 'me96': ((0,0,0),300,300,1100),
         'ach580': ((0,0,0.28),300,420,650), 'oa': ((-0.08,0,0.6),300,420,330)}
for k, f in jobs.items():
    if which and k not in which: continue
    clear(); f(); c, w, h, ppm = views[k]; shoot(k, c, w, h, ppm)
print('ok')
