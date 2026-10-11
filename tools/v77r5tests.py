"""V7.7 r5 cases: PM, short cycling, predictive FDD, health score, TOU demand limit (offline model, FPT timers)."""
import sys, csv, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim7 import Model6
from simstart import faithful
FPT = sys.argv[1]; rows = []
BASE = [(0.0, {'PlantEnable': True, 'PlantLoadPct': 70.0}), (1.0, {'BootQualified': True})]
def row(cid, title, ok, obs):
    rows.append({'id': cid, 'title': title, 'observed': obs, 'result': 'PASS' if ok else 'FINDING'}); print(f"{cid:4} {'PASS' if ok else 'FINDING':8} {title}\n     {obs}", flush=True)
def sim(ev, dur, K, ramps=True):
    m = faithful(Model6(FPT, ramps=ramps)); return m, m.run(dur, BASE + ev, sample=K, every=10.0)
def setout(**kv):
    def f(m):
        for k, v in kv.items(): m.out[k] = v
    return f
at = lambda tr, t, k: next(s[k] for tt, s in tr if tt >= t - 1e-6)
K = ['PM_CH01_HoursSincePM', 'PM_CH01_UsedPct', 'PM_CH01_DueAlarm', 'PM_CH01_OverdueAlarm', 'Smart_CH01_Health', 'PM_CH01_StartsToday',
     'FDD_CH01_KwPerRtFilt', 'FDD_CH01_EffDevPct', 'FDD_CH01_EffDegradeAlarm', 'FDD_CHP01_PerfDevPct', 'FDD_CHP01_PumpPerfAlarm',
     'FDD_CT01_ApproachAlarm', 'Smart_MaintAdvisory', 'FDD_CHWR_FrozenAlarm', 'FDD_OA_Temperature_FrozenAlarm', 'Smart_CHP01_Health']
m, tr = sim([(5, {'PM_CH01_IntervalH': 0.1, 'FDD_CH01_BaselineKwPerRt': 0.40, 'SM_LoadMinPct': 5.0}), (400, {'CHP01_kW': 18.0}),
             (400, {'CT01_Approach': 8.0, 'CT01SpeedCmd': 95.0}), (300, {'CHWR': 12.0})], 900, K)
e = tr[-1][1]
row('S01', 'PM hours accumulate; due (90 %) and overdue (100 %) alarms', e['PM_CH01_HoursSincePM'] > 0.1 and e['PM_CH01_DueAlarm'] and e['PM_CH01_OverdueAlarm'],
    f"hours {e['PM_CH01_HoursSincePM']:.3f} used {e['PM_CH01_UsedPct']:.0f} % due {e['PM_CH01_DueAlarm']} over {e['PM_CH01_OverdueAlarm']}")
row('S02', 'starts per day counted', e['PM_CH01_StartsToday'] >= 1, f"starts {e['PM_CH01_StartsToday']}")
row('S03', 'chiller efficiency drift vs baseline -> advisory', e['FDD_CH01_EffDegradeAlarm'] and e['FDD_CH01_EffDevPct'] > 15,
    f"filt {e['FDD_CH01_KwPerRtFilt']:.3f} dev {e['FDD_CH01_EffDevPct']:.0f} % alarm {e['FDD_CH01_EffDegradeAlarm']}")
row('S04', 'pump kW above affinity-law expectation -> advisory', e['FDD_CHP01_PumpPerfAlarm'], f"dev {e['FDD_CHP01_PerfDevPct']:.0f} % alarm {e['FDD_CHP01_PumpPerfAlarm']}")
row('S05', 'tower approach high at full fan -> advisory', e['FDD_CT01_ApproachAlarm'], f"alarm {e['FDD_CT01_ApproachAlarm']}")
row('S06', 'frozen sensor detected; moving sensor not flagged', e['FDD_CHWR_FrozenAlarm'] and not e['FDD_OA_Temperature_FrozenAlarm'],
    f"CHWR {e['FDD_CHWR_FrozenAlarm']} OA {e['FDD_OA_Temperature_FrozenAlarm']}")
row('S07', 'health score falls with PM / predictive penalties; advisory on', e['Smart_CH01_Health'] <= 45 and e['Smart_MaintAdvisory'] and e['Smart_CHP01_Health'] <= 75,
    f"CH01 {e['Smart_CH01_Health']:.0f} CHP01 {e['Smart_CHP01_Health']:.0f} advisory {e['Smart_MaintAdvisory']}")
K2 = ['DL_ActiveSts', 'DL_ChwstOffset', 'CHW_LeavingTemperatureSetpoint_ACTIVE', 'Plant_kW']
m, tr = sim([(5, {'DL_Enable': True, 'DL_TargetKW': 50.0}), (5, setout(Sch_TouPeak=True)), (400, {'DL_Enable': False})], 700, K2)
row('S08', 'TOU peak demand limit raises CHWST by DL_MaxOffsetK, releases when disabled',
    at(tr, 390, 'DL_ActiveSts') and abs(at(tr, 390, 'DL_ChwstOffset') - 2.0) < 0.05 and at(tr, 690, 'DL_ChwstOffset') < 0.05,
    f"t390 active {at(tr, 390, 'DL_ActiveSts')} offset {at(tr, 390, 'DL_ChwstOffset'):.2f} CHWST {at(tr, 390, 'CHW_LeavingTemperatureSetpoint_ACTIVE'):.2f} (t60 {at(tr, 60, 'CHW_LeavingTemperatureSetpoint_ACTIVE'):.2f}) t690 offset {at(tr, 690, 'DL_ChwstOffset'):.2f}")
if len(sys.argv) > 2:
    with open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
