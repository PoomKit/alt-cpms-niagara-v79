# -*- coding: utf-8 -*-
"""V7.9 IFC4 + BOM/BOQ + COBie from model79.py (installed scope: slots with Installed = N are left out; headers / tees for them stay)."""
import os, sys, types, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOTUS = os.environ.get('LOTUS_DIR', os.path.join(ROOT, 'lotus'))       # V7.8 drafting / BIM / alarm-effect helpers (not in this repo)
if not os.path.isdir(LOTUS): raise SystemExit(f'lotus helpers not found at {LOTUS}: set LOTUS_DIR (see README, "Missing inputs")')
sys.path.insert(0, LOTUS); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'graphics3d'))
import model79 as M
src = open(os.path.join(LOTUS, 'genbim.py'), encoding='utf-8').read().replace(
    "'bypass': ('IfcBuildingElementProxy', None)}",
    "'bypass': ('IfcBuildingElementProxy', None), 'ahu': ('IfcUnitaryEquipment', 'AIRHANDLER'), 'fcu': ('IfcUnitaryEquipment', 'USERDEFINED'), 'fan': ('IfcFan', 'USERDEFINED')}")
GB = types.ModuleType('genbim79core'); GB.__file__ = os.path.join(LOTUS, 'genbim.py')
sys.modules['genbim79core'] = GB
exec(compile(src.replace("if __name__ == '__main__':", "if False:"), 'genbim.py', 'exec'), GB.__dict__)
sh = types.SimpleNamespace(**{k: getattr(M, k) for k in dir(M) if not k.startswith('__')})
inst = lambda s: not s or M.INST.get(s, True)
sh.EQ = [e for e in M.EQ + M.AIR_EQ if e.get('installed', True)]
sh.PIPES = [p for p in M.PIPES if inst(p.get('slot'))]
ids = {p['id'] for p in sh.PIPES}
sh.VALVES = [v for v in M.VALVES if v['pipe'] in ids]
sh.PIPE_BY_ID = {p['id']: p for p in sh.PIPES}
sh.PROJECT = dict(M.PROJECT, name='CPMS Reference Building V7.9')
def _on(pt, q): return M._on(pt, q)
def tees():
    old = M.PIPES; M.PIPES = sh.PIPES
    try: return M.tees()
    finally: M.PIPES = old
def flow_span(p):
    old = M.PIPES; M.PIPES = sh.PIPES
    try: return M.flow_span(p)
    finally: M.PIPES = old
sh.tees, sh.flow_span = tees, flow_span
GB.MD = sh; GB.PR.MD = sh
GB.R = {'h': M.ROOF_Z - 1, 'slab': M.B['slab'], 'x': M.B['x'], 'y': M.B['y']}
OUT = os.path.join(os.environ.get('V79_OUT', os.path.join(ROOT, 'out')), 'bim'); os.makedirs(OUT, exist_ok=True); GB.OUT = OUT
if __name__ == '__main__':
    Q = GB.qty(); ifc = GB.build_ifc(Q); boq = GB.build_boq(Q, ifc)
    shutil.move(ifc, f'{OUT}/ALT_V79_Building.ifc'); shutil.move(boq, f'{OUT}/ALT_V79_BOM_BOQ.xlsx')
    print('installed scope: equipment', len(sh.EQ), 'pipes', len(sh.PIPES), 'valves', len(sh.VALVES))
