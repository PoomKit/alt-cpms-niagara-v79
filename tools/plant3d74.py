"""V7.4 3-D plant = plant3d73 scene with the V7.4 equipment models (assets74): butterfly valves (lug body + quarter-turn actuator),
insertion magmeters + System-10 BTU, RTD with DIN head, pressure transmitters, ACH580-form drives, OA radiation shield.
Same geometry / anchors as V7.3, so the Px card placement stays valid.   usage: python3 plant3d74.py outdir view[,view] [W H samples]"""
import sys, os, runpy
import bpy
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import assets73 as A
import assets74 as B

_before = lambda: set(bpy.data.objects.keys())


def _rotz(names, p, rz):
    import math
    from mathutils import Matrix
    if not rz: return
    R = Matrix.Translation(Vector(p)) @ Matrix.Rotation(rz, 4, 'Z') @ Matrix.Translation(-Vector(p))
    for n in names:
        o = bpy.data.objects[n]; o.matrix_world = R @ o.matrix_world


def butterfly(p, axis, r=0.16, mode='onoff', up='z', mm=None, handwheel=False):
    return B.bfv4(p, axis, r, mode, up, 1.0, B.M4(), handwheel=handwheel)['top']


def magmeter(p, axis, r=0.16, mm=None, up='z'):
    return B.ins_magmeter(p, up, r, B.M4(), s=max(1.0, r / 0.085))['top']


def tt(p, up='z', mm=None):
    return B.rtd(p, up, B.M4(), s=1.6)


def pt_gauge(p, up='z', mm=None):
    return B.ptx(p, up, B.M4(), s=1.6)


def vsd(p, mm=None, running=True, rotz=0.0, scale=1.0):
    b = _before()
    a = B.ach580(p, B.M4(), s=1.8 * scale, running=running)
    _rotz(_before() - b, p, rotz)
    x, y, z = p
    return (x, y - 0.22 * scale, z + 1.0 * scale)


def btu_calc(p, mm=None):
    B.btu_system10(p, B.M4(), s=1.2)
    x, y, z = p
    return (x, y - 0.07, z + 0.25)


def oa_sensor(p, mm=None):
    a = B.oa_shield(p, B.M4(), s=2.0)
    return a['top']


A.butterfly, A.magmeter, A.tt, A.pt_gauge, A.vsd, A.btu_calc, A.oa_sensor = butterfly, magmeter, tt, pt_gauge, vsd, btu_calc, oa_sensor
sys.argv = [os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plant3d73.py')] + sys.argv[1:]
runpy.run_path(sys.argv[0], run_name='__main__')
