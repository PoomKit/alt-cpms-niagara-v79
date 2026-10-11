"""Offline model for V6 (generic, name-keyed). Review aid only — NOT Niagara runtime.

Adds to tools/sim.py: nested folders, priority-array writables (in8 override used by
tests, in10 simulation, in16 logic, fallback), extensions (Discrete/Numeric totalizer,
history 'active'), and the V6 kitControl types (Psychrometric [Stull 2011 wet-bulb,
Magnus dew point], Reset, Ramp, SineWave, NumericLatch, NotEqual, Counter, Add,
Multiply, Maximum, Minimum, Divide, AbsValue, GreaterThan, Limiter, LoopPoint with
output limits). Ramp / SineWave use the exact formulas disassembled from kitControl-rt.
"""
import math, zipfile, xml.etree.ElementTree as ET
from collections import defaultdict

TIMED = {'BooleanDelay', 'OneShot', 'MultiVibrator', 'NumericDelay', 'LoopPoint', 'Ramp', 'SineWave'}


def child(el, n):
    return next((c for c in el if c.tag == 'p' and c.get('n') == n), None)


def num(v, d=0.0):
    try: return float(v)
    except (TypeError, ValueError): return d


class Model6:
    def __init__(self, bog, dt=0.5, ramps=True):
        with zipfile.ZipFile(bog) as z:
            root = ET.fromstring(z.read('file.xml'))
        rp = next(e for e in root.iter('p') if e.get('n') in ('ChillerPlant', 'ReferencePlant'))
        self.C, self.inc, self.ext, self.hmap = {}, defaultdict(dict), {}, {}
        def walk(el):
            for c in el:
                if c.tag != 'p' or not c.get('t'): continue
                if c.get('t') == 'b:Folder': walk(c); continue
                if c.get('t') in ('b:WsAnnotation', 'b:PxView'): continue
                self.C[c.get('n')] = c; self.hmap[c.get('h')] = (c.get('n'), None)
                for x in c:
                    if x.get('h') and x.get('t') and x.get('t') != 'b:Link':
                        self.hmap[x.get('h')] = (c.get('n'), x.get('n'))
                        self.ext[(c.get('n'), x.get('n'))] = x.get('t')
        walk(rp)
        for n, c in self.C.items():
            for L in c:
                if L.get('t') == 'b:Link':
                    src = self.hmap.get(child(L, 'sourceOrd').get('v')[2:], (None, None))
                    self.inc[n][child(L, 'targetSlotName').get('v')] = (src, child(L, 'sourceSlotName').get('v'))
        self.dt, self.t, self.ramps = dt, 0.0, ramps
        self.out, self.st, self.force = {}, defaultdict(dict), {}
        self.extv = defaultdict(float)
        for n, c in self.C.items():
            t = self.typ(n)
            fb = child(c, 'fallback')
            if t == 'BooleanWritable':
                self.out[n] = (child(fb, 'value').get('v') == 'true') if fb is not None else False
            elif t == 'NumericWritable':
                self.out[n] = num(child(fb, 'value').get('v')) if fb is not None else 0.0
            else:
                self.out[n] = False if t in ('And', 'Or', 'Not', 'BooleanDelay', 'BooleanLatch', 'BooleanSwitch', 'OneShot', 'MultiVibrator',
                                              'GreaterThan', 'GreaterThanEqual', 'LessThan', 'LessThanEqual', 'NotEqual', 'Hysteresis',
                                              'BooleanToStatusBoolean') else 0.0
        self.order = self.topo()

    def typ(self, n): return self.C[n].get('t').split(':')[1]
    def prop(self, n, p, d=None):
        e = child(self.C[n], p)
        if e is None: return d
        if e.get('v') is not None: return e.get('v')
        v = child(e, 'value'); return v.get('v') if v is not None else d

    def topo(self):
        deps = {n: {s[0][0] for s in self.inc[n].values() if s[0][0] in self.C} for n in self.C}
        order, seen = [], set()
        def visit(n, stack):
            if n in seen or n in stack: return
            stack.add(n)
            for d in deps[n]: visit(d, stack)
            stack.discard(n); seen.add(n); order.append(n)
        import sys; sys.setrecursionlimit(10000)
        for n in self.C: visit(n, set())
        return order

    # ------------------------------------------------------------------ values
    def src_val(self, n, slot, default=None):
        s = self.inc[n].get(slot)
        if s is None:
            v = self.prop(n, slot)
            if v is None: return default
            return (v == 'true') if v in ('true', 'false') else num(v, default if default is not None else 0.0)
        (sn, ext), sslot = s
        if sn is None: return default
        if ext:                                     # extension slot
            et = self.ext[(sn, ext)]
            if et.endswith('HistoryExt'): return True
            return self.extv[(sn, ext, sslot)]
        v = self.out.get(sn, default)
        if sslot in ('outNot',): return not v
        if sslot in ('outWetBulbTemp', 'outDewPoint', 'outEnthalpy'): return self.st[sn].get(sslot, 0.0)
        return v

    def g(self, n, slot, d=None): return self.src_val(n, slot, d)

    def writable(self, n):
        if n in self.force: return self.force[n]                     # in8 override (tests)
        for slot in ('in10', 'in16'):
            if slot in self.inc[n]:
                (sn, _), _s = self.inc[n][slot]
                if slot == 'in10' and sn and self.typ(sn) in ('Ramp', 'SineWave') and not self.ramps: continue
                return self.g(n, slot)
        if 'fallback' in self.inc[n]: return self.g(n, 'fallback')
        return self.out[n] if n in self.out else 0.0

    def comb(self, n):
        t, g = self.typ(n), (lambda s, d=None: self.g(n, s, d))
        if t in ('BooleanWritable', 'NumericWritable'): return self.writable(n)
        if t == 'And': return all(bool(g(x, True)) for x in ('inA', 'inB', 'inC', 'inD'))
        if t == 'Or': return any(bool(g(x, False)) for x in ('inA', 'inB', 'inC', 'inD'))
        if t == 'Not': return not bool(g('in', False))
        if t == 'BooleanToStatusBoolean': return bool(g('in', False))
        if t == 'BooleanSwitch': return bool(g('inTrue', False)) if g('inSwitch', False) else bool(g('inFalse', False))
        if t == 'NumericSwitch': return num(g('inTrue')) if g('inSwitch', False) else num(g('inFalse'))
        if t == 'GreaterThanEqual': return num(g('inA')) >= num(g('inB'))
        if t == 'GreaterThan': return num(g('inA')) > num(g('inB'))
        if t == 'LessThanEqual': return num(g('inA')) <= num(g('inB'))
        if t == 'LessThan': return num(g('inA')) < num(g('inB'))
        if t == 'NotEqual': return num(g('inA')) != num(g('inB'))
        if t == 'Subtract': return num(g('inA')) - num(g('inB'))
        if t == 'Divide':
            b = num(g('inB')); return num(g('inA')) / b if b else float('nan')
        if t == 'AbsValue': return abs(num(g('inA')))
        linked = [s for s in ('inA', 'inB', 'inC', 'inD') if s in self.inc[n]]
        vals = [num(g(s)) for s in linked]
        if t == 'Add': return sum(vals)
        if t == 'Multiply': return math.prod(vals) if vals else 0.0
        if t == 'Maximum': return max(vals)
        if t == 'Minimum': return min(vals)
        if t == 'Limiter':
            return min(max(num(g('inA')), num(self.prop(n, 'inMin', '-1e18'))), num(self.prop(n, 'inMax', '1e18')))
        if t == 'Reset':
            x, il, ih = num(g('inA')), num(g('inputLowLimit')), num(g('inputHighLimit'))
            ol, oh = num(g('outputLowLimit')), num(g('outputHighLimit'))
            x = min(max(x, min(il, ih)), max(il, ih))
            return ol + (oh - ol) * ((x - il) / (ih - il) if ih != il else 0.0)
        if t == 'Hysteresis':
            x = num(g('in'))
            if x >= num(self.prop(n, 'inHigh', '1')): return True
            if x <= num(self.prop(n, 'inLow', '0')): return False
            return self.out[n]
        if t in ('BooleanLatch', 'NumericLatch'):
            clk = bool(g('clock', False)); s = self.st[n]; s['pend'] = clk
            if clk and not s.get('clk', False):
                return bool(g('in', False)) if t == 'BooleanLatch' else num(g('in'))
            return self.out[n]
        if t == 'Counter':
            s = self.st[n]; up, clr = bool(g('countUp', False)), bool(g('clearIn', False))
            s['pup'], s['pclr'] = up, clr
            v = s.get('base', self.out[n])
            if clr and not s.get('clr', False): v = 0.0
            if up and not s.get('up', False): v = v + 1.0
            return v
        if t == 'Psychrometric':
            T, RH = num(g('inTemp')), max(1.0, min(100.0, num(g('inHumidity'))))
            s = self.st[n]
            s['outWetBulbTemp'] = (T * math.atan(0.151977 * math.sqrt(RH + 8.313659)) + math.atan(T + RH) - math.atan(RH - 1.676331)
                                   + 0.00391838 * RH ** 1.5 * math.atan(0.023101 * RH) - 4.686035)
            a, b = 17.62, 243.12; gm = math.log(RH / 100) + a * T / (b + T)
            s['outDewPoint'] = b * gm / (a - gm)
            pw = 0.6112 * math.exp(17.62 * T / (243.12 + T)) * RH / 100; W = 0.622 * pw / (101.325 - pw)
            s['outEnthalpy'] = 1.006 * T + W * (2501 + 1.86 * T)
            return 0.0
        return self.out[n]

    def timers(self):
        dt = self.dt
        for n in self.C:
            t, g, s = self.typ(n), (lambda sl, d=None, n=n: self.g(n, sl, d)), self.st[n]
            if t == 'BooleanDelay':
                on, off = num(self.prop(n, 'onDelay', '1000')) / 1000, num(self.prop(n, 'offDelay', '1000')) / 1000
                x, o = bool(g('in', False)), self.out[n]
                if x != s.get('last', False): s['tm'] = 0.0; s['last'] = x
                if x != o:
                    s['tm'] = s.get('tm', 0.0) + dt
                    if s['tm'] + 1e-9 >= (on if x else off): self.out[n] = x
                else: s['tm'] = 0.0
            elif t == 'OneShot':
                x = bool(g('in', False))
                if x and not s.get('last', False): s['rem'] = num(self.prop(n, 'time', '500')) / 1000
                s['last'] = x; s['rem'] = max(0.0, s.get('rem', 0.0) - dt); self.out[n] = s['rem'] > 0
            elif t == 'MultiVibrator':
                per = num(self.prop(n, 'period', '1000')) / 1000; duty = num(self.prop(n, 'dutyCycle', '50')) / 100  # kitControl default 1 s
                self.out[n] = (self.t % per) < duty * per
            elif t in ('Ramp', 'SineWave'):
                per = num(self.prop(n, 'period', '30000')) / 1000; f = (self.t % per) / per
                amp, off = num(self.prop(n, 'amplitude', '50')), num(self.prop(n, 'offset', '50'))
                if t == 'SineWave': self.out[n] = amp * math.sin(2 * math.pi * f) + off
                else: self.out[n] = (off - amp) + (amp * f if f < 0.5 else amp * (1 - f)) * 4
            elif t == 'NumericDelay':
                s['acc'] = s.get('acc', 0.0) + dt
                if s['acc'] + 1e-9 >= num(self.prop(n, 'updateTime', '1000')) / 1000:
                    s['acc'] = 0.0; x, o, m = num(g('in')), num(self.out[n]), num(self.prop(n, 'maxStepSize', '1'))
                    self.out[n] = o + max(-m, min(m, x - o))
            elif t == 'LoopPoint':                       # BLoopPoint.calculatePoint (kitControl-rt bytecode)
                if not g('loopEnable', False): s['es'] = 0.0; self.out[n] = 0.0; continue
                e = num(g('setpoint')) - num(g('controlledVariable'))
                kp, ki = num(self.prop(n, 'proportionalConstant', '1')), num(self.prop(n, 'integralConstant', '0'))
                lo, hi = num(self.prop(n, 'minimumOutput', '0')), num(self.prop(n, 'maximumOutput', '100'))
                direct = self.prop(n, 'loopAction', 'direct') != 'reverse'
                es = s.get('es', 0.0)
                if ki:
                    es += dt * e; k = kp * ki / 60
                    x = -es if direct else es                   # anti-windup: integral term within [lo, hi]
                    x = max(lo / k, min(hi / k, x)); es = -x if direct else x
                s['es'] = es
                o = kp * e + kp * ki * es / 60
                if direct: o = -o
                if not ki: o += num(self.prop(n, 'bias', '0'))
                self.out[n] = max(lo, min(hi, o))
        for (pt, ex), et in self.ext.items():                          # totalizers
            if et == 'c:DiscreteTotalizerExt' and self.out.get(pt):
                self.extv[(pt, ex, 'elapsedActiveTimeNumeric')] += dt * 1000
            if et == 'c:NumericTotalizerExt':
                self.extv[(pt, ex, 'total')] += num(self.out.get(pt)) * dt / 3600

    def settle(self):
        for n in self.C:
            if self.typ(n) == 'Counter': self.st[n]['base'] = self.out[n]
        for _ in range(40):
            ch = False
            for n in self.order:
                if self.typ(n) in TIMED: continue
                v = self.comb(n)
                if v != self.out[n] and not (isinstance(v, float) and isinstance(self.out[n], float) and abs(v - self.out[n]) < 1e-9):
                    self.out[n] = v; ch = True
            if not ch: break
        else:
            raise RuntimeError('no settle at t=%.1f' % self.t)
        for n, s in self.st.items():
            if 'pend' in s: s['clk'] = s.pop('pend')
            if 'pup' in s: s['up'] = s.pop('pup'); s['clr'] = s.pop('pclr')

    def step(self):
        self.timers(); self.settle(); self.t += self.dt

    def run(self, until, events=(), sample=(), every=5.0):
        ev = sorted(events, key=lambda e: e[0]); i = 0; tr = []; nxt = 0.0
        self.settle()
        while self.t < until - 1e-9:
            while i < len(ev) and ev[i][0] <= self.t + 1e-9:
                e = ev[i][1]
                if callable(e): e(self)
                else:
                    for k, v in e.items():
                        if v is None: self.force.pop(k, None)
                        else: self.force[k] = v
                i += 1
            self.step()
            if sample and self.t >= nxt - 1e-9:
                tr.append((round(self.t, 1), {k: self.out[k] for k in sample})); nxt += every
        return tr
