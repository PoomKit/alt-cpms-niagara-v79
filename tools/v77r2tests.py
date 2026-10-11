"""V7.7 r2 cases: field interface switching, P2P helpers, automated functional tests (offline model, FPT timers).
usage: v77r2tests.py v77_fpt.bog [out.csv]"""
import sys, csv, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim7 import Model6
from simstart import faithful

FPT = sys.argv[1]
BASE = [(0.0, {'PlantEnable': True, 'PlantLoadPct': 20.0}), (1.0, {'BootQualified': True})]
rows = []
def row(cid, title, ok, obs):
    rows.append({'id': cid, 'title': title, 'observed': obs, 'result': 'PASS' if ok else 'FINDING'})
    print(f"{cid:5} {'PASS' if ok else 'FINDING':8} {title}\n      {obs}", flush=True)
def fire(name, ms=2000):
    def f(m): m.st[name]['rem'] = ms / 1000.0; m.out[name] = True
    return f
def sim(events, dur, extra=(), every=1.0):
    m = faithful(Model6(FPT, ramps=False))
    return m, m.run(dur, BASE + list(events), sample=list(extra), every=every)
at = lambda tr, t, k: next(s[k] for tt, s in tr if tt >= t - 1e-6)

# X01 / X02 field input switching
K = ['CHWS', 'IO_CHWS', 'CH01Fault']
m, tr = sim([(50, {'IO_DriversInstalled': True, 'IO_ChwLoop_UseField': True, 'IO_CHWS': 9.5}), (80, {'IO_CHWS': None}),
             (100, {'IO_CH01_UseField': True}), (110, {'IO_CH01Fault': True}), (130, {'IO_CH01_UseField': False})], 150, K)
row('X01', 'simulation mode: field landing point is {null}, logic point keeps the emulated value',
    at(tr, 40, 'IO_CHWS') is None and at(tr, 40, 'CHWS') > 3, f"t40 IO_CHWS={at(tr, 40, 'IO_CHWS')} CHWS={at(tr, 40, 'CHWS'):.2f}")
row('X02', 'field mode: CHWS follows IO_CHWS; driver null -> fallback; manual DI follows field, back to manual in sim mode',
    abs(at(tr, 70, 'CHWS') - 9.5) < 1e-6 and abs(at(tr, 90, 'CHWS') - 7.0) < 1e-6 and at(tr, 120, 'CH01Fault') and not at(tr, 140, 'CH01Fault'),
    f"t70 {at(tr, 70, 'CHWS')} t90 {at(tr, 90, 'CHWS')} CH01Fault t120 {at(tr, 120, 'CH01Fault')} t140 {at(tr, 140, 'CH01Fault')}")
# X03 / X04 outputs, isolation, stroke
K = ['CH01StartCmd', 'IO_CH01StartCmd', 'IO_AHU01_ValveCmd']
m, tr = sim([(60, {'IO_DriversInstalled': True, 'IO_AllField': True}), (100, {'CX_TestMode': True, 'CX_P2P_CH01_Isolate': True}), (120, {'IO_CH01StartCmd': False}),
             (140, {'CX_P2P_AHU01_Stroke': True, 'CX_StrokeManualPct': 37.0})], 160, K)
row('X03', 'outputs: {null} in simulation, = logic command in field mode, released when isolated (P2P), operator override wins',
    at(tr, 50, 'IO_CH01StartCmd') is None and at(tr, 90, 'IO_CH01StartCmd') == at(tr, 90, 'CH01StartCmd') and at(tr, 110, 'IO_CH01StartCmd') is None
    and at(tr, 130, 'IO_CH01StartCmd') is False,
    f"t50 {at(tr, 50, 'IO_CH01StartCmd')} t90 {at(tr, 90, 'IO_CH01StartCmd')}/{at(tr, 90, 'CH01StartCmd')} t110 {at(tr, 110, 'IO_CH01StartCmd')} t130 {at(tr, 130, 'IO_CH01StartCmd')}")
row('X04', 'AO stroke (test mode) drives IO_AHU01_ValveCmd at priority 9', abs(at(tr, 150, 'IO_AHU01_ValveCmd') - 37) < 1e-6,
    f"t150 {at(tr, 150, 'IO_AHU01_ValveCmd')}")
# X07 field selected but drivers not installed -> stays in simulation, blocked indication
m, tr = sim([(30, {'IO_AllField': True})], 120, ['CHWS', 'CH01RunProof', 'IO_FieldBlockedSts', 'IO_AnyFieldSts'])
row('X07', 'FIELD selected without IO_DriversInstalled: plant keeps running on simulation, blocked indication on',
    at(tr, 110, 'IO_FieldBlockedSts') and not at(tr, 110, 'IO_AnyFieldSts') and at(tr, 110, 'CH01RunProof') and at(tr, 110, 'CHWS') > 3,
    f"blocked {at(tr, 110, 'IO_FieldBlockedSts')} anyField {at(tr, 110, 'IO_AnyFieldSts')} CH01 {at(tr, 110, 'CH01RunProof')} CHWS {at(tr, 110, 'CHWS'):.1f}")
# X05 run-all (no TEST MODE needed) functional test sequence
codes = [f'FT{i:02d}' for i in range(1, 11)]
K = [f'CX_{c}_Result' for c in codes] + ['CX_AutoSeqSts', 'CH01RunProof', 'CH02RunProof', 'CHP01RunProof', 'CHP02RunProof']
t0 = time.time()
m, tr = sim([(300, fire('CX_RunAllFire'))], float(os.environ.get('DUR', 2300)), K, every=5.0)
res = {c: m.out[f'CX_{c}_Result'] for c in codes}
for c in codes:
    t_run = next((tt for tt, s in tr if s[f'CX_{c}_Result'] == 1), None)
    row('X05' + c[2:], f'functional test {c} (run-all)', res[c] == 2, f"result {res[c]} started t={t_run} ({time.time() - t0:.0f}s wall)")
row('X06', 'run-all sequence finished', not m.out['CX_AutoSeqSts'], f"AutoSeq {m.out['CX_AutoSeqSts']}")
if len(sys.argv) > 2:
    with open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
