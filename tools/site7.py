"""V6.3 site-timing scenario suite (commissioning timer profile, start-up faithful model).
usage: site6.py v6.bog [out.csv]"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim7 import Model6
from simstart import faithful

BOG = sys.argv[1]
STEADY = {'PlantLoadPct': 50.0, 'CHWFlow': 150.0, 'CHWS': 7.0, 'CHWR': 12.0, 'CHWDP': 120.0, 'CDS': 29.0, 'CDR': 34.0,
          'CH01LoadPct': 50.0, 'CH02LoadPct': 0.0, 'OA_Temperature': 32.0, 'OA_Humidity': 65.0}
START = [(0.0, STEADY), (10.0, {'BootQualified': True}), (15.0, {'PlantEnable': True})]


def ft(tr, cond, after=0.0):
    for t, s in tr:
        if t >= after and cond(s): return t
    return None


def gap(tr, a, b):
    longest = cur = 0.0; prev = None
    for t, s in tr:
        if t < a or t > b: continue
        none = not (s['CH01StartSuccess'] or s['CH02StartSuccess'])
        if none and prev is not None: cur += t - prev
        elif not none: cur = 0.0
        longest = max(longest, cur); prev = t
    return longest


SAMPLE = ['CH01StartCmd', 'CH02StartCmd', 'CH01StartSuccess', 'CH02StartSuccess', 'CH01TimeoutLockout', 'CH02TimeoutLockout',
          'CHP01StartCmd', 'CT01StartCmd', 'CT01SpeedCmd', 'Stage2Request', 'PlantRunRequest', 'CT_LowTempCutout', 'CH01ValveOpenCmd']


def sim(events, dur, every=5.0, extra=(), start=True):
    m = faithful(Model6(BOG, ramps=False))
    tr = m.run(dur, (START if start else []) + list(events), sample=SAMPLE + list(extra), every=every)
    return m, tr


rows = []
def row(cid, title, expect, ok, obs):
    rows.append({'id': cid, 'area': 'Site timing', 'title': title, 'expectation': expect, 'observed': obs, 'result': 'PASS' if ok else 'FINDING'})


o = lambda m, n: m.lv(n)
# S01 fresh start with site timers
m, tr = sim([], 420)
t_cmd = ft(tr, lambda s: s['CH01StartCmd']); t_ok = ft(tr, lambda s: s['CH01StartSuccess']); t_p = ft(tr, lambda s: s['CHP01StartCmd'])
row('S01', 'Fresh start, site timers', 'Pumps/tower/valve first, chiller after anti-recycle (180 s), proof 45 s, no lockout',
    t_ok is not None and not o(m, 'CH01TimeoutLockout') and t_p < t_cmd, f"CHP01@{t_p}s CH01 cmd@{t_cmd}s proven@{t_ok}s lockout={o(m, 'CH01TimeoutLockout')}")
# S02 stage up / down with timers + min run
m, tr = sim([(420.0, {'PlantLoadPct': 120.0}), (1500.0, {'PlantLoadPct': 40.0})], 2700, every=10.0)
t_up = ft(tr, lambda s: s['CH02StartCmd'], 420); t_dn = ft(tr, lambda s: not s['CH02StartCmd'], (t_up or 0) + 10)
row('S02', 'Stage up after 10 min above 90 %, stage down after 15 min below 60 %', 'CH02 cmd ~600 s after load step; off ~900 s after load drop',
    t_up is not None and 1000 <= t_up <= 1040 and t_dn is not None and 2380 <= t_dn <= 2440,
    f"load 120 % @420 s -> CH02 cmd @{t_up}s; load 40 % @1500 s -> CH02 off @{t_dn}s")
# S03 lead overload with bad load calc
m, tr = sim([(420.0, {'PlantLoadPct': 50.0, 'CH01LoadPct': 98.0})], 1400, every=10.0)
t_ov = ft(tr, lambda s: s['CH02StartCmd'], 420)
row('S03', 'Lead chiller at 98 % while load calc says 50 % (flow meter drift)', 'Stage 2 after 10 min of lead overload and held',
    t_ov is not None and 1000 <= t_ov <= 1040 and o(m, 'CH02StartCmd'), f"CH02 cmd @{t_ov}s, still on at 1400 s = {o(m, 'CH02StartCmd')}")
# S04 stop: auxiliaries post-run 120 s
m, tr = sim([(600.0, {'PlantEnable': False})], 800, every=1.0)
a = ft(tr, lambda s: not s['CH01StartCmd'], 600); b = ft(tr, lambda s: not s['CHP01StartCmd'], 600)
row('S04', 'Normal stop', 'Chiller off first, pumps/tower/valve 120 s later', a is not None and b is not None and 118 <= b - a <= 122,
    f"CH01 off@{a}s CHP01 off@{b}s")
# S05 proof failure with site timers
m, tr = sim([(0.0, {'CH01RunProof': False})], 900, every=5.0)
t_l = ft(tr, lambda s: s['CH01TimeoutLockout']); t_2 = ft(tr, lambda s: s['CH02StartSuccess'])
row('S05', 'CH01 never proves (site timers)', 'Lockout 180 s after command, CH02 takes over',
    t_l is not None and t_2 is not None and t_2 > t_l, f"CH01 lockout@{t_l}s CH02 proven@{t_2}s")
# S06 tower low temperature cut-out
m, tr = sim([(420.0, {'CDS': 20.0}), (600.0, {'CDS': 22.0}), (700.0, {'CDS': 24.0})], 800, every=5.0)
at = lambda T, k: next(s[k] for t, s in tr if t >= T)
row('S06', 'Tower fan low-temperature cut-out (21 / 23 degC)', 'CDS 20 -> fan 0 %; 22 (band) -> stays 0 %; 24 -> fan back >= 20 %',
    at(415, 'CT01SpeedCmd') >= 20 and at(590, 'CT01SpeedCmd') == 0 and at(690, 'CT01SpeedCmd') == 0 and at(795, 'CT01SpeedCmd') >= 20 and at(590, 'CT_LowTempCutout'),
    f"CT01 speed @CDS29 {at(415, 'CT01SpeedCmd'):.0f} %, @20 {at(590, 'CT01SpeedCmd'):.0f} %, @22 {at(690, 'CT01SpeedCmd'):.0f} %, @24 {at(795, 'CT01SpeedCmd'):.0f} %")
def sched_ms(v):
    def f(m): m.out['MonthStartSchedule'] = v
    return f


# S07 schedule mode
def sched(v):
    def f(m): m.out['PlantSchedule'] = v
    return f
m, tr = sim([(0.0, {'PlantScheduleMode': True}), (300.0, sched(True))], 700, every=5.0)
t_run = ft(tr, lambda s: s['PlantRunRequest'])
row('S07', 'Plant follows schedule when PlantScheduleMode = Schedule', 'Off while schedule false, runs when schedule true',
    t_run is not None and t_run >= 300, f"PlantRunRequest @{t_run}s (schedule true @300 s)")
# S08 energy periods (TimeTrigger action links emulated; month rollover uses the real schedule edge + delay)
def day_end(m):
    for b in ('Plant_kWh', 'Aux_kWh', 'Cooling_RTh'):
        m.out[f'{b}_YesterdayLatch'] = m.out[f'{b}_Today']          # DayEndTrigger.fireTrigger -> latch
def day_start(m):
    for b in ('Plant_kWh', 'Aux_kWh', 'Cooling_RTh'):
        m.out[f'{b}_DayStartLatch'] = m.out[b]                       # DayStartTrigger.fireTrigger -> latch
m, tr = sim([(3900.0, day_end), (3901.0, day_start), (4000.0, sched_ms(True)), (4060.0, sched_ms(False))], 4300, every=60.0,
            extra=['Plant_kW', 'Plant_kWh', 'Plant_kWh_Today', 'Plant_kWh_Yesterday', 'Plant_kWh_Month', 'Plant_kWh_LastMonth'])
at = lambda T, k: next(s[k] for t, s in tr if t >= T)
y = o(m, 'Plant_kWh_Yesterday'); tod = o(m, 'Plant_kWh_Today'); mon = o(m, 'Plant_kWh_Month'); lm = o(m, 'Plant_kWh_LastMonth')
row('S08', 'Energy periods: today / yesterday / month / last month, kW/RT, cost', 'Yesterday latched at day end, today restarts, month rolls over on schedule edge',
    y > 0 and tod < y * 0.2 and lm > y and mon < lm * 0.2 and abs(o(m, 'Energy_Cost_THB_Yesterday') - y * 4.18) < 0.5,
    f"yesterday {y:.1f} kWh ({o(m, 'Plant_kW_per_RT_Yesterday'):.3f} kW/RT, {o(m, 'Energy_Cost_THB_Yesterday'):.0f} THB); today after 00:00 {tod:.1f} kWh; "
    f"last month {lm:.1f} kWh; month after rollover {mon:.1f} kWh; cumulative {o(m, 'Plant_kWh'):.1f} kWh")
# S09 restart auto-qualify with site timers
m, tr = sim([(0.0, dict(STEADY, PlantEnable=True))], 700, every=5.0, start=False)
t_ok = ft(tr, lambda s: s['CH01StartSuccess'])
row('S09', 'Station restart, nobody presses QUALIFY (site timers)', 'Auto-qualify 120 s + anti-recycle 180 s + proof 45 s',
    t_ok is not None and t_ok <= 400, f"CH01 proven @{t_ok}s without operator")

for x in rows:
    print(f"{x['id']:4} {x['result']:8} {x['title']}\n      {x['observed']}")
print('PASS', sum(x['result'] == 'PASS' for x in rows), '/', len(rows))
if len(sys.argv) > 2:
    with open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
