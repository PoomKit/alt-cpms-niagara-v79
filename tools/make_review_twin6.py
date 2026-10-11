"""VIEW-ONLY review BOG for V6: user-free FPT wrapper + V6 ChillerPlant + V6 AlarmService.
No UserService / b:User (unsigned n4EnergyManager registers an agent on baja:User).
Not for station use: never copy into a stations folder or run it."""
import sys, os, zipfile, hashlib, xml.etree.ElementTree as ET
from copy import deepcopy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_symbols import check, fix
def load(p):
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None and z.namelist() == ['file.xml']
        return ET.fromstring(z.read('file.xml'))
wrapper, v6, out = sys.argv[1:4]
w, s = load(wrapper), load(v6)
st, sst = w.find('p'), s.find('p')
old = next(c for c in st if c.get('n') == 'ReferencePlant')
new = deepcopy(next(c for c in sst if c.get('n') == 'ChillerPlant')); new.tail = old.tail
for v in [c for c in new if c.get('t') == 'b:PxView']:   # file:^px has no station file space offline -> 'px file is not found'
    new.remove(v)
st[list(st).index(old)] = new
svc = next(c for c in st if c.get('n') == 'Services')
alarm = deepcopy(next(c for c in next(c for c in sst if c.get('n') == 'Services') if c.get('n') == 'AlarmService'))
svc.append(alarm)
# the wrapper HistoryService must not keep a link to a handle that no longer exists
fix(w)
assert check(w) == []
hs = {e.get('h') for e in w.iter('p') if e.get('h')}
broken = [e for e in w.iter('p') if e.get('n') == 'sourceOrd' and (e.get('v') or '').startswith('h:') and e.get('v')[2:] not in hs]
assert not broken, [b.get('v') for b in broken][:5]
assert sum(1 for e in w.iter('p') if e.get('t') in ('b:User', 'b:UserService')) == 0
if os.path.exists(out): raise SystemExit('refusing to overwrite ' + out)
with zipfile.ZipFile(out, 'x', compression=zipfile.ZIP_DEFLATED) as z:
    z.writestr('file.xml', ET.tostring(w, encoding='utf-8', xml_declaration=True))
print(out, hashlib.sha256(open(out, 'rb').read()).hexdigest().upper())
