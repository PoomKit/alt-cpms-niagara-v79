"""V7.4 unit conversion on the finished station model: kPa -> bar, m3/h -> gpm (US).

Propagates the physical quantity through the link graph (unit-preserving kitControl blocks), then scales every stored
number that carries that quantity: point / parameter fallback values, unlinked input slots, alarm limits, facets and
history facets, Limiter / Hysteresis / Reset constants, ramp amplitude / offset, NumericDelay step.  Multiply / Divide
boundaries are NOT touched automatically: they are listed and handled by the explicit FACTOR table (review item)."""
import re
import xml.etree.ElementTree as ET
import make_v6 as M6

FACT = {'P': 0.01, 'Q': 4.402867539}              # 1 kPa = 0.01 bar ; 1 m3/h = 4.402868 US gpm
SEED = {'u:kilopascal': 'P', 'u:cubic meters per hour': 'Q'}
NEWU = {'P': 'units=u:bar;bar;(m-1)(kg)(s-2);*100000.0;', 'Q': 'units=u:gallons per minute;gpm;(m3)(s-1);*6.30901964E-5;'}
OLDU = {'P': 'units=u:kilopascal;kPa;(m-1)(kg)(s-2);*1000.0;', 'Q': 'units=u:cubic meters per hour;m\u00b3/hr;(m3)(s-1);*2.777777777777778E-4;'}
PREC = {'P': 2, 'Q': 0}

# unit-preserving blocks: every listed numeric input carries the same quantity as the output
PRES = {'Add': ('inA', 'inB', 'inC', 'inD'), 'Subtract': ('inA', 'inB'), 'Minimum': ('inA', 'inB', 'inC', 'inD'),
        'Maximum': ('inA', 'inB', 'inC', 'inD'), 'Average': ('inA', 'inB', 'inC', 'inD'), 'Limiter': ('inA', 'inMin', 'inMax'),
        'NumericSwitch': ('inTrue', 'inFalse'), 'NumericDelay': ('in',), 'NumericLatch': ('in',), 'AbsValue': ('inA',),
        'Negative': ('inA',), 'NumericWritable': tuple(f'in{i}' for i in range(1, 17)) + ('fallback',), 'NumericPoint': ()}
# blocks whose inputs share one quantity but whose output is boolean / other
CMPT = {'GreaterThan', 'GreaterThanEqual', 'LessThan', 'LessThanEqual', 'Equal', 'NotEqual'}
CMP_IN = ('inA', 'inB')
AIR = re.compile(r'Airflow')                      # air volume flow stays m3/h (CMH) - only water flow -> gpm
NOT_SCALED = {'CoolingLoadRaw', 'CH01LoadKWCalc', 'CH02LoadKWCalc', 'Sim_CH01_QK', 'Sim_CH02_QK'}   # flow x dT x factor = kW (factor converted instead)


def links_of(el):
    for L in el:
        if L.tag == 'p' and L.get('t') == 'b:Link':
            yield (M6.child(L, 'sourceOrd').get('v')[2:], M6.child(L, 'sourceSlotName').get('v'), M6.child(L, 'targetSlotName').get('v'))


def typ(el): return el.get('t').split(':')[-1]


def quantity_of(el):
    f = M6.child(el, 'facets')
    if f is not None:
        for k, q in SEED.items():
            if k in (f.get('v') or ''): return q
    return None


WHY = {}


def analyze(S):
    comps = S.comp
    h2n = {e.get('h'): n for n, e in comps.items()}
    q = {n: quantity_of(e) for n, e in comps.items()}
    q = {n: v for n, v in q.items() if v and not AIR.search(n)}
    inc = {n: [(h2n.get(h), ss, ts) for h, ss, ts in links_of(e)] for n, e in comps.items()}
    # --- forward / backward propagation through unit-preserving blocks
    changed = True
    while changed:
        changed = False
        for n, e in comps.items():
            t = typ(e)
            if t in PRES and n not in q:
                for src, ss, ts in inc[n]:
                    if ts in PRES[t] and src in q and ss == 'out':
                        q[n] = q[src]; WHY[n] = ('fwd', src); changed = True; break
        for n, e in comps.items():                      # scaling blocks: q x dimensionless -> q ; q / dimensionless -> q ; Reset out
            t = typ(e)
            if n in q or AIR.search(n): continue
            ins = {ts: src for src, ss, ts in inc[n] if ss == 'out' or src in q}
            if t == 'Multiply':
                qs = [q[src] for ts, src in ins.items() if ts in ('inA', 'inB', 'inC', 'inD') and src in q]
                if len(qs) == 1 and n not in NOT_SCALED: q[n] = qs[0]; WHY[n] = ('mul', ins); changed = True
            elif t == 'Divide':
                a, b = ins.get('inA'), ins.get('inB')
                if a in q and b not in q: q[n] = q[a]; WHY[n] = ('div', a); changed = True
            elif t == 'Reset':
                for sl in ('outputLowLimit', 'outputHighLimit'):
                    if ins.get(sl) in q: q[n] = q[ins[sl]]; changed = True; break
        for n, e in comps.items():                      # backward: a preserving block with quantity -> its unit-less sources
            t = typ(e)
            if n in q and t in PRES and t not in ('NumericWritable', 'NumericPoint'):
                for src, ss, ts in inc[n]:
                    if ts in PRES[t] and src and src not in q and typ(comps[src]) in PRES and ss == 'out' and not shared(src, inc, comps):
                        q[src] = q[n]; WHY[src] = ('bwd', n); changed = True
    return q, inc


def shared(src, inc, comps):
    """a constant consumed by several unrelated blocks (ZeroSpeed, One, HundredPct...) is never re-united"""
    return src in ('ZeroSpeed', 'Zero', 'One', 'HundredPct', 'Half', 'Tiny', 'PctToFrac', 'Third', 'ZeroSpeed')


def report(S):
    q, inc = analyze(S)
    comps = S.comp
    out = []
    for n, e in comps.items():
        t = typ(e)
        ins = [(src, ts) for src, ss, ts in inc[n] if src in q]
        if not ins: continue
        if (t in ('Multiply', 'Divide') and n not in q) or t in ('LoopPoint', 'Reset') or (t not in PRES and t not in CMPT and t not in ('Multiply', 'Divide')):
            out.append((n, t, [(s, ts, q[s]) for s, ts in ins], q.get(n)))
    # q outputs produced without a q input (a hidden factor must carry the unit)
    for n, e in comps.items():
        t = typ(e)
        if n in q and t in ('Multiply', 'Divide'):
            ins = [(src, ts) for src, ss, ts in inc[n] if src in q]
            if not ins: out.append((n, t + ' NO-Q-INPUT', [(s, ts, None) for s, ss, ts in inc[n]], q[n]))
        if n in q and t in ('NumericWritable', 'NumericPoint'):
            for src, ss, ts in inc[n]:
                if src and src not in q and ts.startswith('in') and typ(comps[src]) not in ('Ramp', 'SineWave'):
                    out.append((n, 'POINT FED BY NON-Q', [(src, ts, typ(comps[src]))], q[n]))
    return q, out


def _scale_attr(el, factor):
    v = el.get('v')
    try:
        x = float(v)
    except (TypeError, ValueError):
        return False
    if v in ('+inf', '-inf') or x != x: return False
    el.set('v', repr(round(x * factor, 10)))
    return True


def _facets(el, qq):
    for f in el.iter('p'):
        if f.get('n') in ('facets', 'valueFacets') and f.get('v') and OLDU[qq] in f.get('v'):
            v = f.get('v').replace(OLDU[qq], NEWU[qq])
            v = re.sub(r'precision=i:\d+', f'precision=i:{PREC[qq]}', v)
            def sc(m):
                x = float(m.group(2))
                return f'{m.group(1)}={"d:" + repr(round(x * FACT[qq], 6))}'
            v = re.sub(r'(min|max)=d:(-?[0-9.]+(?:E-?[0-9]+)?)', sc, v)
            f.set('v', v)


def convert(S, extra_scale=()):
    """extra_scale: [(component, slot_or_prop, quantity)] for boundary constants reviewed by hand"""
    q, inc = analyze(S)
    comps = S.comp
    done = []
    for n, qq in q.items():
        e, t, k = comps[n], typ(comps[n]), FACT[qq]
        linked = {ts for _, _, ts in inc[n]}
        _facets(e, qq)
        if t in ('NumericWritable', 'NumericPoint'):
            fb = M6.child(e, 'fallback')
            if fb is not None and M6.child(fb, 'value') is not None and _scale_attr(M6.child(fb, 'value'), k): done.append((n, 'fallback'))
            for i in range(1, 17):
                s = M6.child(e, f'in{i}')
                if s is not None and f'in{i}' not in linked and M6.child(s, 'value') is not None and M6.child(s, 'value').get('v') not in (None, '0.0') \
                        and M6.child(s, 'status') is not None and 'null' not in (M6.child(s, 'status').get('v') or ''):
                    _scale_attr(M6.child(s, 'value'), k); done.append((n, f'in{i}'))
            for ext in e:                                   # alarm limits (OutOfRange algorithm)
                if ext.get('t') == 'a:AlarmSourceExt':
                    for p in ext.iter('p'):
                        if p.get('n') in ('highLimit', 'lowLimit', 'deadband') and _scale_attr(p, k): done.append((n, 'alarm ' + p.get('n')))
                if ext.get('t') == 'h:NumericCovHistoryExt':
                    for p in ext.iter('p'):
                        if p.get('n') == 'changeTolerance' and _scale_attr(p, k): done.append((n, 'cov tolerance'))
        elif t in PRES:
            for slot in PRES[t]:
                if slot in linked: continue
                s = M6.child(e, slot)
                if s is None: continue
                if s.get('v') is not None:
                    if _scale_attr(s, k): done.append((n, slot))
                elif M6.child(s, 'value') is not None:
                    if _scale_attr(M6.child(s, 'value'), k): done.append((n, slot))
            if t == 'NumericDelay':
                s = M6.child(e, 'maxStepSize')
                if s is not None and _scale_attr(s, k): done.append((n, 'maxStepSize'))
        elif t in ('Ramp', 'SineWave'):
            for p in ('amplitude', 'offset'):
                s = M6.child(e, p)
                if s is not None and _scale_attr(s, k): done.append((n, p))
    # comparators: an unlinked constant compared with a converted quantity
    for n, e in comps.items():
        if typ(e) in CMPT:
            src = {ts: s for s, _, ts in inc[n]}
            qs = {q[s] for ts, s in src.items() if s in q and ts in CMP_IN}
            if len(qs) == 1:
                qq = qs.pop()
                for slot in CMP_IN:
                    if slot not in src:
                        s = M6.child(e, slot)
                        if s is not None and M6.child(s, 'value') is not None and _scale_attr(M6.child(s, 'value'), FACT[qq]):
                            done.append((n, slot))
        if typ(e) == 'Hysteresis':
            src = {ts: s for s, _, ts in inc[n]}
            if src.get('in') in q:
                for p in ('inLow', 'inHigh'):
                    s = M6.child(e, p)
                    if s is not None and _scale_attr(s, FACT[q[src['in']]]): done.append((n, p))
        if typ(e) == 'LoopPoint':                         # gain is output-% per unit of the controlled variable
            src = {ts: s for s, _, ts in inc[n]}
            cv = src.get('controlledVariable')
            if cv in q:
                kp = M6.child(e, 'proportionalConstant')
                if kp is not None and _scale_attr(kp, 1.0 / FACT[q[cv]]): done.append((n, 'proportionalConstant /'))
                for slot in ('setpoint',):
                    if slot not in src:
                        sp = M6.child(e, slot)
                        if sp is not None:
                            tgt = M6.child(sp, 'value') if M6.child(sp, 'value') is not None else sp
                            if _scale_attr(tgt, FACT[q[cv]]): done.append((n, slot))
        if typ(e) == 'Reset':
            src = {ts: s for s, _, ts in inc[n]}
            groups = (('inA', 'inputLowLimit', 'inputHighLimit'), ('outputLowLimit', 'outputHighLimit'))
            for g in groups:
                qs = {q[src[sl]] for sl in g if src.get(sl) in q}
                if len(qs) == 1:
                    qq = qs.pop()
                    for sl in g:
                        if sl not in src:
                            x = M6.child(e, sl)
                            if x is not None:
                                tgt = M6.child(x, 'value') if M6.child(x, 'value') is not None else x
                                if _scale_attr(tgt, FACT[qq]): done.append((n, sl))
    for n, slot, qq in extra_scale:
        e = comps[n]; s = M6.child(e, slot)
        tgt = M6.child(s, 'value') if s is not None and s.get('v') is None and M6.child(s, 'value') is not None else s
        assert tgt is not None and _scale_attr(tgt, FACT[qq] if qq in FACT else qq), (n, slot)
        done.append((n, slot + ' (manual)'))
    return q, done
