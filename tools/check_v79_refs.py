# -*- coding: utf-8 -*-
"""Offline reference check of the V7.9 layer (v79_scale + v79_air) without the source station.

The V7.9 builder runs on a stub station that already holds every component of the last full build
(registers/V7_COMPONENTS.csv) except the ones the V7.9 layer creates itself. It then reports
  * links / rewires that read a component that does not exist (typo, wrong order, removed point)
  * components created twice
  * rewires whose old source is not the expected one (on components created by the V7.9 layer)
usage: python3 check_v79_refs.py [--register ALT_V79_Equipment_Register.xlsx]   exit code 1 on any finding."""
import csv, os, sys, xml.etree.ElementTree as ET
from collections import OrderedDict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_v6 as M6
import make_v7 as M7                                      # noqa: F401
import v77_fieldcx as FCX
import eqreg
import v79_scale as SC
import v79_air                                            # noqa: F401  wraps SC.scale
import v79_office                                         # noqa: F401  wraps SC.scale (r4)
import v79_r6                                             # noqa: F401  wraps SC.scale (r6)

COMPONENTS = os.path.join(HERE, '..', 'registers', 'V7_COMPONENTS.csv')


class Stub(M6.Station):
    """M6.Station without a bog: base components are placeholders, new components are real elements."""
    def __init__(self, base, tolerant=False):
        self.nh = 0x100000
        stub = self

        class Comp(OrderedDict):
            def __missing__(self, name):                    # tolerant pass: any name read but never built = base input
                if not tolerant: raise KeyError(name)
                stub.base.add(name); stub.folder_of[name] = 'Base'; stub.meta[name] = {}
                el = self[name] = ET.Element('p', {'n': name, 'h': stub.h(), 't': 'base'}); return el
        self.comp, self.folder_of, self.meta, self.log, self.ext_handle = Comp(), {}, {}, [], {}
        if tolerant:
            from collections import defaultdict
            self.folder_of = defaultdict(lambda: 'Base')
        self.base, self.errors = set(), []
        for name, folder in base.items():
            self.comp[name] = ET.Element('p', {'n': name, 'h': self.h(), 't': 'base'})
            self.folder_of[name] = folder; self.meta[name] = {}; self.base.add(name)

    def handle(self, name):
        if '.' in name: name = name.split('.')[0]
        if name not in self.comp and isinstance(self.folder_of, dict) and type(self.folder_of) is not dict:
            return self.comp[name].get('h')                 # tolerant pass
        if name not in self.comp:
            self.errors.append(f'missing component: {name}'); return '0'
        return self.comp[name].get('h')

    def link(self, target_el, src, tslot):
        s = src.split('.', 1)[0]
        if s not in self.ext_handle and s not in self.comp and type(self.folder_of) is not dict and ':' not in s:
            self.comp[s]                                     # tolerant pass: creates the base placeholder
        if s not in self.ext_handle and s not in self.comp:
            self.errors.append(f'{target_el.get("n")}.{tslot} reads missing {src}'); return
        return super().link(target_el, src, tslot)

    def add(self, folder, name, typ, links=None, props=(), fallback=None, facets=None, note=''):
        if name in self.comp:
            if name in self.base:                          # built again by the V7.9 layer: replace the placeholder
                del self.comp[name]; self.base.discard(name)
            else:
                self.errors.append(f'duplicate component: {name}'); return name
        return super().add(folder, name, typ, links, props, fallback, facets, note)

    def rewire(self, target, tslot, new_src, old_src=None):
        if target not in self.comp: self.errors.append(f'rewire of missing {target}.{tslot}'); return
        if target in self.base:                            # base component: links are not known offline, check the source only
            if new_src.split('.', 1)[0] not in self.comp: self.errors.append(f'rewire {target}.{tslot} <- missing {new_src}')
            return
        try:
            super().rewire(target, tslot, new_src, old_src)
        except SystemExit as e:
            self.errors.append(str(e))

    def set_fallback(self, name, value):
        if name in self.base: return
        return super().set_fallback(name, value)


def layer_base(base):
    """pass 1 on an empty station: every component the V7.9 layers build (constants included) -> the base is the r2 component
    list without them (removed or renamed V7.9 names must not be found there)."""
    S1 = Stub({}, tolerant=True)
    SC.scale(S1); SC.post(S1)
    created = {n for n in S1.comp if n not in S1.base}
    v79_folders = (SC.EX, 'Simulation/Expansion', 'Parameters/Expansion', f'{M7.AIR}/Floors', f'{M7.AIR}/Simulation/Floors', 'Metering/Floors')
    return OrderedDict((n, f) for n, f in base.items() if n not in created and not f.startswith(v79_folders)), created


def main():
    reg = None
    if '--register' in sys.argv: reg = sys.argv[sys.argv.index('--register') + 1]
    SC.REG = eqreg.load(reg)
    rows = list(csv.DictReader(open(COMPONENTS, encoding='utf-8-sig')))
    base = OrderedDict((r['Component'], r['Folder']) for r in rows)
    FCX.PROF[0] = M6.TIMING['fpt']
    base2, created = layer_base(base)
    S = Stub(base2)
    SC.scale(S); SC.post(S)
    errs = sorted(set(S.errors))
    for e in errs: print('FINDING', e)
    print(f'V7.9 layer: {len(created)} components created, {len(base2)} base components, {len(errs)} findings')
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
