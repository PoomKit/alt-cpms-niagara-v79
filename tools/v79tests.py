"""V7.9 add / remove equipment cases, offline model. usage: v79tests.py <v79_fpt.bog> [out.csv]"""
import sys, csv, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sim7 import Model6
from simstart import faithful
BOG = sys.argv[1]; rows = []
BASE = [(0.0, {'PlantEnable': True, 'PlantLoadPct': 70.0}), (1.0, {'BootQualified': True})]


def row(cid, title, ok, obs):
    rows.append({'id': cid, 'title': title, 'observed': obs, 'result': 'PASS' if ok else 'FINDING'})
    print(f"{cid:4} {'PASS' if ok else 'FINDING':8} {title}\n     {obs}", flush=True)


def sim(ev, dur, K, every=1.0, setup=None):
    m = faithful(Model6(BOG))
    if setup: setup(m)
    return m.run(dur, BASE + ev, sample=K, every=every)


first = lambda tr, k, v, t0=0: next((t for t, s in tr if t >= t0 and s[k] == v), None)
at = lambda tr, t, k: next(s[k] for tt_, s in tr if tt_ >= t - 1e-6)
ever = lambda tr, k: any(s[k] for t, s in tr)
EXP = ['CH03StartCmd', 'CH04StartCmd', 'CHP03StartCmd', 'CDP03StartCmd', 'CT03StartCmd']

# X01 nothing installed -> V7.8 behaviour
tr = sim([], 200.0, EXP + ['CHX_TargetNum', 'CH01StartCmd'])
row('X01', 'slots 03-06 not installed (register default): no expansion unit is ever asked to run, CH01 runs as before',
    not any(ever(tr, k) for k in EXP) and at(tr, 195, 'CHX_TargetNum') == 0 and ever(tr, 'CH01StartCmd'),
    f"expansion commands {[k for k in EXP if ever(tr, k)]}, target {at(tr, 195, 'CHX_TargetNum')}, CH01 started {first(tr, 'CH01StartCmd', True)}")

# X02 base unit removed -> expansion unit covers the deficit
K = ['CH02StartCmd', 'CH03StartCmd', 'CH03RunProof', 'CHX_TargetNum', 'CH03ValveOpenCmd']
tr = sim([(0.5, {'CH02_Installed': False, 'CH03_Installed': True, 'Stage2Request': True})], 200.0, K)
row('X02', 'CH02 removed (Installed off) + stage 2 asked -> CH02 never starts, CH03 starts in its place',
    not ever(tr, 'CH02StartCmd') and first(tr, 'CH03RunProof', True) is not None,
    f"CH02 started {ever(tr, 'CH02StartCmd')}; CH03 valves {first(tr, 'CH03ValveOpenCmd', True)}, start {first(tr, 'CH03StartCmd', True)}, running {first(tr, 'CH03RunProof', True)}; target {at(tr, 195, 'CHX_TargetNum')}")

# X03 extra stage up / down + pumps and tower follow
K = ['CH03StartCmd', 'CH04StartCmd', 'CHX_StageAdd', 'CHP03StartCmd', 'CDP03StartCmd', 'CT03StartCmd', 'CH01RunProofSelected', 'CH02RunProofSelected']
ev = [(0.5, {'CH03_Installed': True, 'CH04_Installed': True, 'CHP03_Installed': True, 'CDP03_Installed': True, 'CT03_Installed': True,
             'Stage2Request': True, 'CHWS': 6.7}), (60.0, {'CH01LoadPct': 95.0, 'CH02LoadPct': 95.0}), (160.0, {'CH01LoadPct': 40.0, 'CH02LoadPct': 40.0})]
tr = sim(ev, 260.0, K)
t3 = first(tr, 'CH03StartCmd', True); t3off = first(tr, 'CH03StartCmd', False, 160)
row('X03', 'both base chillers at 95 % load -> after the stage-up delay (test 15 s) CH03 is added (only one); load drops to 40 % -> CH03 removed',
    t3 is not None and t3 > 60 and not ever(tr, 'CH04StartCmd') and t3off is not None and at(tr, 255, 'CHX_StageAdd') == 0,
    f"CH03 start {t3}, stage at 150 s {at(tr, 150, 'CHX_StageAdd')}, CH04 started {ever(tr, 'CH04StartCmd')}, CH03 stop {t3off}, stage at 255 s {at(tr, 255, 'CHX_StageAdd')}")
tp, tc, tt = first(tr, 'CHP03StartCmd', True), first(tr, 'CDP03StartCmd', True), first(tr, 'CT03StartCmd', True)
row('X04', '3 chillers need water -> third CHW pump, condenser pump and tower (expansion slot 03) start too, and stop after',
    None not in (tp, tc, tt) and not at(tr, 255, 'CHP03StartCmd'),
    f'CHP03 {tp}, CDP03 {tc}, CT03 {tt}; CHP03 at 255 s {at(tr, 255, "CHP03StartCmd")}')

# X05 start failure -> next slot
K = ['CH03StartCmd', 'CH04StartCmd', 'CH03_FailLatch', 'CH03_StartFailAlarm', 'CH04RunProof']
tr = sim([(0.5, {'CH02_Installed': False, 'CH03_Installed': True, 'CH04_Installed': True, 'Stage2Request': True, 'CH03RunProof': False})], 200.0, K)
tf, t4 = first(tr, 'CH03_FailLatch', True), first(tr, 'CH04RunProof', True)
row('X05', 'CH03 does not prove running -> latched out with alarm, CH04 (next slot) starts instead',
    tf is not None and t4 is not None and t4 > tf and at(tr, 195, 'CH03_StartFailAlarm'),
    f'CH03 fail latch {tf}, alarm {at(tr, 195, "CH03_StartFailAlarm")}, CH04 running {t4}')

# X06 maintenance skips a slot
K = ['CH03StartCmd', 'CH04StartCmd']
tr = sim([(0.5, {'CH02_Installed': False, 'CH03_Installed': True, 'CH03_Maintenance': True, 'CH04_Installed': True, 'Stage2Request': True})], 150.0, K)
row('X06', 'CH03 in maintenance -> skipped, CH04 runs', not ever(tr, 'CH03StartCmd') and ever(tr, 'CH04StartCmd'),
    f"CH03 {ever(tr, 'CH03StartCmd')}, CH04 {first(tr, 'CH04StartCmd', True)}")

# X07 base pump removed -> expansion pump
K = ['CHP02StartCmd', 'CHP03StartCmd', 'CHPX_Target']
tr = sim([(0.5, {'CHP02_Installed': False, 'CHP03_Installed': True, 'Stage2Request': True})], 200.0, K)
row('X07', 'CHP02 removed, two chillers need water -> CHP03 runs as the second chilled water pump',
    not ever(tr, 'CHP02StartCmd') and ever(tr, 'CHP03StartCmd'),
    f"CHP02 {ever(tr, 'CHP02StartCmd')}, CHP03 {first(tr, 'CHP03StartCmd', True)}, target {at(tr, 195, 'CHPX_Target')}")

# X08 master switch
K = ['CH03StartCmd']
tr = sim([(0.5, {'CHX_Enable': False, 'CH02_Installed': False, 'CH03_Installed': True, 'Stage2Request': True})], 150.0, K)
row('X08', 'CHX_Enable off -> expansion units never run (V7.8 behaviour)', not ever(tr, 'CH03StartCmd'), f"CH03 {ever(tr, 'CH03StartCmd')}")

# X09 base chiller removed
K = ['CH01StartCmd', 'CH02StartCmd']
tr = sim([(0.5, {'CH01_Installed': False})], 150.0, K)
row('X09', 'CH01 removed -> never started, CH02 runs', not ever(tr, 'CH01StartCmd') and ever(tr, 'CH02StartCmd'),
    f"CH01 {ever(tr, 'CH01StartCmd')}, CH02 {first(tr, 'CH02StartCmd', True)}")

# X10 sensor slot
K = ['SNS01_HighAlarm', 'SNS01_SensorFaultAlarm', 'SNS01_Valid']
tr = sim([(0.5, {'SNS01_Installed': True}), (10.0, {'SNS01_Value': 40.0}), (60.0, {'SNS01_Value': 80.0})], 110.0, K)
row('X10', 'sensor slot SNS01 (temperature): 40 C -> high alarm; 80 C (out of the believable range) -> sensor fault, high alarm cleared',
    at(tr, 55, 'SNS01_HighAlarm') and at(tr, 105, 'SNS01_SensorFaultAlarm') and not at(tr, 105, 'SNS01_HighAlarm'),
    f"high at 55 s {at(tr, 55, 'SNS01_HighAlarm')}, fault at 105 s {at(tr, 105, 'SNS01_SensorFaultAlarm')}, high at 105 s {at(tr, 105, 'SNS01_HighAlarm')}")

# X11 Field IO path of an expansion unit
K = ['CH03RunProof']
tr = sim([(0.5, {'IO_DriversInstalled': True, 'IO_CH03_UseField': True, 'IO_CH03RunProof': True})], 20.0, K)
row('X11', 'expansion unit uses the same Field IO layer: CH03 in FIELD mode reads IO_CH03RunProof', at(tr, 15, 'CH03RunProof') is True,
    f"CH03RunProof {at(tr, 15, 'CH03RunProof')}")

# X12 V7.9 r3 rotation: the expansion slot with the fewest run hours starts first
def hours(**h):
    def f(m):
        for u, v in h.items(): m.extv[(f'{u}RunProof', 'Runtime', 'elapsedActiveTimeNumeric')] = v * 3600 * 1000.0
    return f


K = ['CH03StartCmd', 'CH04StartCmd']
tr = sim([(0.5, {'CH02_Installed': False, 'CH03_Installed': True, 'CH04_Installed': True, 'Stage2Request': True})], 150.0, K, setup=hours(CH03=500, CH04=100))
row('X12', 'rotation: CH03 500 h, CH04 100 h, one unit wanted -> CH04 starts, CH03 stays off',
    ever(tr, 'CH04StartCmd') and not ever(tr, 'CH03StartCmd'), f"CH03 {ever(tr, 'CH03StartCmd')}, CH04 {first(tr, 'CH04StartCmd', True)}")

# X13 base chiller trips at stage 2 -> expansion unit covers it (review finding R1)
K = ['CH03StartCmd', 'CHX_TargetNum']
tr = sim([(0.5, {'CH03_Installed': True, 'Stage2Request': True}), (60.0, {'CH01Fault': True})], 200.0, K)
row('X13', 'CH01 fault at stage 2 -> deficit 1, CH03 starts', ever(tr, 'CH03StartCmd') and at(tr, 195, 'CHX_TargetNum') >= 1,
    f"CH03 start {first(tr, 'CH03StartCmd', True, 60)}, target {at(tr, 195, 'CHX_TargetNum')}")

# X14 soft-load of an expansion chiller
K = ['CH03RunProof', 'CH03DemandLimitCmd']
tr = sim([(0.5, {'CH02_Installed': False, 'CH03_Installed': True, 'Stage2Request': True})], 120.0, K)
tp = first(tr, 'CH03RunProof', True)
row('X14', 'CH03 demand limit starts at 50 % and ramps to 100 % after run proof (test 5 %/s)',
    tp is not None and at(tr, tp, 'CH03DemandLimitCmd') <= 60 and at(tr, tp + 20, 'CH03DemandLimitCmd') >= 99,
    f"proof {tp}, limit at proof {tp is not None and at(tr, tp, 'CH03DemandLimitCmd')}, 20 s later {tp is not None and at(tr, tp + 20, 'CH03DemandLimitCmd')}")

# ---------------- air side floors 2-8
if True:
    K = ['AHU_F02_StartCmd', 'AHU_F02_Status', 'AHU_F02_ValveCmd', 'Zone_F02_AvgTemp', 'AHU_F03_StartCmd']
    tr = sim([(0.5, {'AirX_ManualOn': True, 'AHU_F03_Installed': False})], 600.0, K, every=5.0)
    row('Y01', 'floor 2 AHU: starts (manual run), proves running, CHW valve brings the floor average from 29 C towards 24 C; floor 3 AHU not installed -> never starts',
        at(tr, 30, 'AHU_F02_Status') and max(s['Zone_F02_AvgTemp'] for t, s in tr) > 25.5 and 23.0 < at(tr, 595, 'Zone_F02_AvgTemp') < 25.0
        and at(tr, 595, 'AHU_F02_ValveCmd') > 20 and not ever(tr, 'AHU_F03_StartCmd'),
        f"F02 running {first(tr, 'AHU_F02_Status', True)}, valve at 595 s {at(tr, 595, 'AHU_F02_ValveCmd'):.0f} %, average peak {max(s['Zone_F02_AvgTemp'] for t, s in tr):.1f} -> {at(tr, 595, 'Zone_F02_AvgTemp'):.1f} C; F03 started {ever(tr, 'AHU_F03_StartCmd')}")
    K = ['AHU_F02_StartCmd']
    tr = sim([(0.5, {'AirX_ManualOn': True}), (60.0, {'FireAlarmSignal': True})], 90.0, K)
    row('Y02', 'fire alarm stops the floor AHU', at(tr, 50, 'AHU_F02_StartCmd') and not at(tr, 85, 'AHU_F02_StartCmd'),
        f"before {at(tr, 50, 'AHU_F02_StartCmd')}, after fire {at(tr, 85, 'AHU_F02_StartCmd')}")
    K = ['Zone_F02_AvgTemp', 'Zone_F02_HottestTemp']
    tr = sim([(0.5, {'ZoneTemperatureAvg_02_0201': 24.0, 'ZoneTemperatureAvg_02_0202': 24.0, 'ZoneTemperatureAvg_02_0203': 24.0,
                     'ZoneTemperatureAvg_02_0204': 35.0}), (20.0, {'ZoneOutOfService_02_0204': True})], 40.0, K)
    row('Y03', 'zone out of service is left out of the floor average and the hottest zone',
        abs(at(tr, 15, 'Zone_F02_AvgTemp') - 26.75) < .01 and abs(at(tr, 35, 'Zone_F02_AvgTemp') - 24.0) < .01 and at(tr, 35, 'Zone_F02_HottestTemp') == 24.0,
        f"average {at(tr, 15, 'Zone_F02_AvgTemp'):.2f} -> {at(tr, 35, 'Zone_F02_AvgTemp'):.2f}, hottest {at(tr, 35, 'Zone_F02_HottestTemp')}")
    K = ['AHU_F02_ValveCmd']
    tr = sim([(0.5, {'AirX_ManualOn': True, 'AHU_F02_RA_RH': 75.0, 'ZoneTemperatureAvg_02_0201': 22.0, 'ZoneTemperatureAvg_02_0202': 22.0,
                     'ZoneTemperatureAvg_02_0203': 22.0, 'ZoneTemperatureAvg_02_0204': 22.0})], 60.0, K)
    row('Y04', 'cold floor but return RH 75 % -> CHW valve held at the dehumidification minimum (60 %)', abs(at(tr, 55, 'AHU_F02_ValveCmd') - 60.0) < .5,
        f"valve {at(tr, 55, 'AHU_F02_ValveCmd')}")
    K = ['AHU_F02_FailAlarm', 'AHU_F02_StartCmd']
    tr = sim([(0.5, {'AirX_ManualOn': True, 'AHU_F02_Status': False})], 40.0, K)
    row('Y05', 'floor AHU without run proof -> start failure alarm, command removed', at(tr, 35, 'AHU_F02_FailAlarm') and not at(tr, 35, 'AHU_F02_StartCmd'),
        f"alarm {at(tr, 35, 'AHU_F02_FailAlarm')}, cmd {at(tr, 35, 'AHU_F02_StartCmd')}")
    K = ['Zone_F02_AvgTemp', 'Zone_F02_AllOutOfServiceAlarm', 'AHU_F02_ValveCmd']
    tr = sim([(0.5, {'AirX_ManualOn': True, **{f'ZoneOutOfService_02_020{z}': True for z in range(1, 5)}})], 60.0, K)
    row('Y06', 'every zone of floor 2 out of service -> floor average = setpoint (not 0 C) + alarm',
        abs(at(tr, 55, 'Zone_F02_AvgTemp') - 24.0) < .01 and at(tr, 55, 'Zone_F02_AllOutOfServiceAlarm'),
        f"average {at(tr, 55, 'Zone_F02_AvgTemp')}, alarm {at(tr, 55, 'Zone_F02_AllOutOfServiceAlarm')}, valve {at(tr, 55, 'AHU_F02_ValveCmd')}")
    K = ['Zone_F02_AvgRH']
    tr = sim([(0.5, {'ZoneHumidityAvg_02_0201': 60.0, 'ZoneHumidityAvg_02_0202': 60.0, 'ZoneHumidityAvg_02_0203': 60.0,
                     'ZoneHumidityAvg_02_0204': 90.0, 'ZoneOutOfService_02_0204': True})], 20.0, K)
    row('Y07', 'floor RH average leaves out the zone out of service', abs(at(tr, 15, 'Zone_F02_AvgRH') - 60.0) < .5,
        f"RH average {at(tr, 15, 'Zone_F02_AvgRH')}")
    K = ['AHU_F02_RA_CO2', 'AHU_F02_OADamperCmd']
    tr = sim([(0.5, {'AirX_ManualOn': True})], 600.0, K, every=5.0)
    row('Y08', 'simulated CO2: occupied floor settles between 600 and 1000 ppm with the OA damper modulating',
        600 < at(tr, 595, 'AHU_F02_RA_CO2') < 1000 and 20 < at(tr, 595, 'AHU_F02_OADamperCmd') < 100,
        f"RA CO2 {at(tr, 595, 'AHU_F02_RA_CO2'):.0f} ppm, OA damper {at(tr, 595, 'AHU_F02_OADamperCmd'):.0f} %")

if len(sys.argv) > 2:
    with open(sys.argv[2], 'w', newline='', encoding='utf-8') as fo:
        w = csv.DictWriter(fo, fieldnames=['id', 'title', 'observed', 'result']); w.writeheader(); w.writerows(rows)
print(f"{sum(r['result'] == 'PASS' for r in rows)}/{len(rows)} PASS")
sys.exit(0 if all(r['result'] == 'PASS' for r in rows) else 1)
