# ======================================================================= V7.3 T-cases
SP = 'CDS_Setpoint_ACTIVE'
CELLK = ['CT01_01StartCmd', 'CT01_02StartCmd', 'CT02_01StartCmd', 'CT02_02StartCmd', 'CT01StartCmd', 'CT02StartCmd', 'CT_LagStaged',
         'CT_CommonSpeed', 'CT01_01SpeedCmd']


def cds_rel(dk):
    """force CDS to the ACTIVE setpoint + dk (evaluated at event time)"""
    def f(m): m.force['CDS'] = m.out[SP] + dk
    return f


def fire(name, ms=2000):
    def f(m): m.st[name]['rem'] = ms / 1000.0; m.out[name] = True
    return f


# T01 one chiller: lead tower, both of its cells run, lag tower off
m, tr = sim(FPT, [], 150, extra=CELLK)
ok = o(m, 'CH01StartSuccess') and o(m, 'CT01_01StartCmd') and o(m, 'CT01_02StartCmd') and not o(m, 'CT02_01StartCmd') and not o(m, 'CT02StartCmd') \
    and abs(o(m, 'CT01_kW') - (o(m, 'CT01_01_kW') + o(m, 'CT01_02_kW'))) < 1e-6 and o(m, 'CT01RunProof')
row('T01', 'CT SOO', '1 chiller -> lead tower, both fan cells', 'CT-01/01 + CT-01/02 run (own VSD), CT-02 cells off; tower kW = sum of cells; tower proven = any cell',
    ok, ' '.join(f"{k}={int(o(m, k))}" for k in CELLK[:6]) + f" CT01 kW {o(m, 'CT01_kW'):.2f}")

# T02 initial speed after start, then PID
m, tr = sim(FPT, [(0.0, cds_rel(3.0))], 150, extra=['CT01_01SpeedCmd', 'CT01_01RunProof', 'CT_CommonSpeed'], every=0.5)
t_run = next((t for t, s_ in tr if s_['CT01_01RunProof']), None)
early = at(tr, t_run + 0.5, 'CT01_01SpeedCmd') if t_run else -1
row('T02', 'CT SOO', 'Fan start at initial speed, then PID', 'right after run proof speed = CT_InitialSpeed 40 %; after the hold it follows the CDS PID (CDS 3 K high -> ramps up)',
    t_run is not None and abs(early - 40) < 0.5 and o(m, 'CT01_01SpeedCmd') > 60, f"run @{t_run}s speed {early:.1f} % -> end {o(m, 'CT01_01SpeedCmd'):.1f} % (common {o(m, 'CT_CommonSpeed'):.1f} %)")

# T03 permissive: CDP running but no condenser water flow -> fans inhibited + alarm (valves open)
K = ['CT01StartCmd', 'CT01_01StartCmd', 'CT01ValveOpenCmd', 'CT_StartInhibitedAlarm', 'CDP01RunProof']
m, tr = sim(FPT, [(0.0, {'CDW_Flow': 0.0, 'CH01CDWFlowProof': False, 'CH02CDWFlowProof': False})], 30, extra=K)
s20 = {k: at(tr, 20, k) for k in K}
ok = s20['CDP01RunProof'] and s20['CT01ValveOpenCmd'] and not s20['CT01StartCmd'] and not s20['CT01_01StartCmd'] and s20['CT_StartInhibitedAlarm']
row('T03', 'CT SOO', 'Plant enable not satisfied (no condenser water flow)', 'CDP running + tower valves open, but no CDW flow -> fans inhibited; "CT start inhibited" alarm',
    ok, ' '.join(f"{k}={int(v)}" for k, v in s20.items()) + ' @20 s')

# T04 stage-up needs A (CDS > SP + 1) AND B (speed >= 90 %) for the delay
m, tr = sim(FPT, [(0.0, {'CT_CommonSpeed': 95.0}), (0.0, cds_rel(0.5)), (60.0, cds_rel(2.0))], 120, extra=CELLK, every=0.5)
a = at(tr, 58, 'CT_LagStaged')
t_st = next((t for t, s_ in tr if s_['CT_LagStaged']), None)
ok = not a and t_st is not None and 64 <= t_st <= 67 and o(m, 'CT02_01StartCmd') and o(m, 'CT02_02StartCmd') and o(m, 'CT01_01StartCmd')
row('T04', 'CT SOO', 'Stage LAG tower: CDS > SP+1.0 K AND speed >= 90 % for the delay', 'speed 95 % but CDS SP+0.5 -> no; CDS SP+2 -> lag after the staging delay (FPT 5 s), all 4 cells run',
    ok, f"@58s staged={a}; staged @{t_st}s (A true @60s); CT02 cells {o(m, 'CT02_01StartCmd')}/{o(m, 'CT02_02StartCmd')}")

# T05 de-stage: 1 chiller AND CDS < SP - 0.5 AND speed <= low for the delay; then minimum stop
m, tr = sim(FPT, [(0.0, {'CT_CommonSpeed': 95.0}), (0.0, cds_rel(2.0)), (60.0, {'CT_CommonSpeed': 30.0}), (60.0, cds_rel(-1.0)),
                  (70.0, {'CT_CommonSpeed': 95.0}), (70.0, cds_rel(2.0))], 110, extra=CELLK, every=0.5)
t_off = next((t for t, s_ in tr if t > 60 and not s_['CT_LagStaged']), None)
t_on = next((t for t, s_ in tr if t_off and t > t_off and s_['CT_LagStaged']), None)
ok = at(tr, 59, 'CT_LagStaged') and t_off is not None and 67 <= t_off <= 70 and not at(tr, t_off + 1, 'CT02_01StartCmd') and at(tr, t_off + 1, 'CT01_01StartCmd') \
    and t_on is not None and t_on - t_off >= 10.5
row('T05', 'CT SOO', 'De-stage LAG tower + minimum stop', 'CDS SP-1 and speed 30 % -> lag off after the de-staging delay (FPT 8 s), lead stays; lag cannot restart before its minimum stop (FPT 6 s) even if staging is met at once',
    ok, f"lag off @{t_off}s (cond @60s), lead on {at(tr, (t_off or 0) + 1, 'CT01_01StartCmd')}; lag re-staged @{t_on}s (cond again @70s -> waits min-stop 6 s + delay 5 s)")

# T06 two chillers -> both towers; reduction locked out
m, tr = sim(FPT, [(0.0, {'PlantLoadPct': 150.0}), (150.0, {'CT_CommonSpeed': 20.0}), (150.0, cds_rel(-2.0))], 260, extra=CELLK)
ok = o(m, 'CH02StartSuccess') and o(m, 'CT01StartCmd') and o(m, 'CT02StartCmd') and o(m, 'CT_LagStaged') and all(o(m, c) for c in CELLK[:4])
row('T06', 'CT SOO', '2 chillers -> both towers, no reduction', 'stage 2: CT01 + CT02 (4 cells) and the reduction conditions are ignored while 2 chillers run',
    ok, f"CH02={o(m, 'CH02StartSuccess')} CT01={o(m, 'CT01StartCmd')} CT02={o(m, 'CT02StartCmd')} cells={[int(o(m, c)) for c in CELLK[:4]]}")

# T07 back to 1 chiller: lag stays until the reduction conditions hold (SOO dual -> reduce loop)
m, tr = sim(FPT, [(0.0, {'PlantLoadPct': 150.0}), (150.0, {'PlantLoadPct': 40.0}), (150.0, {'CT_CommonSpeed': 60.0}), (150.0, cds_rel(0.0)),
                  (400.0, {'CT_CommonSpeed': 20.0}), (400.0, cds_rel(-1.5))], 440, extra=CELLK + ['Pool_Need2'])
t1 = next((t for t, s_ in tr if t > 150 and not s_['Pool_Need2']), None)
ok = t1 is not None and at(tr, 395, 'CT_LagStaged') and at(tr, 395, 'CT02StartCmd') and not o(m, 'CT_LagStaged') and not o(m, 'CT02StartCmd')
row('T07', 'CT SOO', '2 -> 1 chiller: lag tower kept until reduction conditions', 'after CH02 stops both towers keep running (CDS at SP, speed 60 %); CDS SP-1.5 + speed 20 % -> lag off after the delay',
    ok, f"1 chiller @{t1}s; @395s lag={at(tr, 395, 'CT_LagStaged')} CT02={at(tr, 395, 'CT02StartCmd')}; end lag={o(m, 'CT_LagStaged')} CT02={o(m, 'CT02StartCmd')}")

# T08 one cell VFD fault: other cell continues; lead tower degraded -> lag staged at once
m, tr = sim(FPT, [(100.0, {'CT01_01VfdFault': True})], 160, extra=CELLK)
ok = at(tr, 95, 'CT01_01StartCmd') and not o(m, 'CT01_01StartCmd') and o(m, 'CT01_02StartCmd') and o(m, 'CT01StartCmd') and o(m, 'CT02_01StartCmd') \
    and not at(tr, 95, 'CT02StartCmd')
row('T08', 'Cells', 'CT-01/01 VFD fault', 'CT-01/01 stops, CT-01/02 keeps running (tower stays on); lead lost a cell -> CT-02 staged at once',
    ok, f"CT01/01 {o(m, 'CT01_01StartCmd')} CT01/02 {o(m, 'CT01_02StartCmd')} CT02 {at(tr, 95, 'CT02StartCmd')} -> {o(m, 'CT02StartCmd')} cells healthy sts {o(m, 'CT01_CellsHealthy')}")

# T09 cell fails to prove -> latched alarm -> RESET
m, tr = sim(FPT, [(60.0, {'CT01_01RunProof': False}), (120.0, {'CT01_01RunProof': None}), (130.0, fire('CT01_01ResetFire'))], 170, extra=['CT01_01_FailAlarm', 'CT01_01StartCmd'])
ok = at(tr, 125, 'CT01_01_FailAlarm') and not at(tr, 125, 'CT01_01StartCmd') and not o(m, 'CT01_01_FailAlarm') and o(m, 'CT01_01StartCmd')
row('T09', 'Cells', 'Cell fails to prove -> latched -> RESET', 'no run status 5 s (FPT) -> cell failed + alarm (held after the fault clears); RESET -> cell back in service',
    ok, f"@125s alarm {at(tr, 125, 'CT01_01_FailAlarm')} cmd {at(tr, 125, 'CT01_01StartCmd')}; after RESET alarm {o(m, 'CT01_01_FailAlarm')} cmd {o(m, 'CT01_01StartCmd')}")

# T10 both cells of the lead tower out -> tower unavailable -> CT02 leads
m, tr = sim(FPT, [(0.0, {'CT01_01InAuto': False, 'CT01_02_ServiceIsolate': True})], 150, extra=CELLK)
ok = not o(m, 'CT01StartCmd') and o(m, 'CT02StartCmd') and o(m, 'CT02_01StartCmd') and not o(m, 'CT01Healthy') and o(m, 'CT_Lead') is False
row('T10', 'Cells', 'Both cells of CT-01 unavailable', 'CT-01 unhealthy (no fan cell) -> CT-02 becomes lead; CT-01/01 not-in-auto alarm',
    ok, f"CT01 healthy {o(m, 'CT01Healthy')} cmd {o(m, 'CT01StartCmd')}; CT02 {o(m, 'CT02StartCmd')}; lead {'CT01' if o(m, 'CT_Lead') else 'CT02'}; alarm {o(m, 'CT01_01_NotInAutoAlarm')}")

# T11 basin LOW-LOW on the lead tower
K = ['CT01StartCmd', 'CT02StartCmd', 'CT01ValveOpenCmd', 'CT01_OutletMVCmd', 'CT01_MakeupValveCmd', 'CT01BasinLowLowLevelAlarm']
m, tr = sim(FPT, [(100.0, {'CT01_LowLowLevelSwitch': True, 'CT01_BasinLevel': 10.0}), (180.0, {'CT01_LowLowLevelSwitch': False, 'CT01_BasinLevel': 40.0})], 260, extra=K)
s1 = {k: at(tr, 170, k) for k in K}
ok = s1['CT01BasinLowLowLevelAlarm'] and not s1['CT01StartCmd'] and not s1['CT01ValveOpenCmd'] and not s1['CT01_OutletMVCmd'] and s1['CT01_MakeupValveCmd'] \
    and s1['CT02StartCmd'] and at(tr, 170, 'CH01StartSuccess') and not o(m, 'CT01BasinLowLowLevelAlarm')
row('T11', 'Basin', 'CT-01 basin LOW-LOW', 'CT-01 fans stop, inlet + outlet valves close, emergency make-up opens, Critical alarm; CT-02 takes over; chiller stays on; clears when refilled',
    ok, ' '.join(f"{k}={int(v)}" for k, v in s1.items()) + f" CH01={at(tr, 170, 'CH01StartSuccess')}; end alarm {o(m, 'CT01BasinLowLowLevelAlarm')}")

# T12 both basins dry -> condenser pumps stop (dry-run protection)
m, tr = sim(FPT, [(100.0, {'CT01_LowLowLevelSwitch': True, 'CT02_LowLowLevelSwitch': True})], 160, extra=['CDP01StartCmd'])
ok = at(tr, 95, 'CDP01StartCmd') and not o(m, 'CDP01StartCmd') and not o(m, 'CDP02StartCmd') and o(m, 'CT_AllBasinsDryAlarm')
row('T12', 'Basin', 'Both basins LOW-LOW', 'CDPs stopped (no water to pump), Emergency alarm', ok,
    f"CDP01 {at(tr, 95, 'CDP01StartCmd')} -> {o(m, 'CDP01StartCmd')} CDP02 {o(m, 'CDP02StartCmd')} alarm {o(m, 'CT_AllBasinsDryAlarm')}")

# T13 CDS sensor invalid -> all towers (fail-safe speed)
m, tr = sim(FPT, [(100.0, {'CDSSensorHealthy': False})], 180, extra=CELLK)
ok = o(m, 'CT02StartCmd') and o(m, 'CT01StartCmd') and abs(o(m, 'CT01_01SpeedCmd') - o(m, 'CT_FailSafeSpeed')) < 1.0 and not at(tr, 95, 'CT02StartCmd')
row('T13', 'CT SOO', 'CDS sensor invalid', 'both towers run at the fail-safe speed (heat rejection first)', ok,
    f"CT02 {at(tr, 95, 'CT02StartCmd')} -> {o(m, 'CT02StartCmd')}; cell speed {o(m, 'CT01_01SpeedCmd'):.1f} % (fail-safe {o(m, 'CT_FailSafeSpeed'):.0f})")

# T14 CHW loop fill: 180 -> 200 kPa, leak lock-out, RESET
K = ['CHW_FillValveCmd', 'CHW_FillLockoutAlarm']
m, tr = sim(FPT, [(10.0, {'CHW_ExpansionTankPressure': 170.0}), (20.0, {'CHW_ExpansionTankPressure': 190.0}), (30.0, {'CHW_ExpansionTankPressure': 205.0}),
                  (40.0, {'CHW_ExpansionTankPressure': 170.0}), (90.0, {'CHW_ExpansionTankPressure': 205.0}), (95.0, fire('CHW_FillResetFire'))], 110, extra=K)
seq = [at(tr, t, 'CHW_FillValveCmd') for t in (8, 18, 28, 38, 55, 85)]
ok = seq == [False, True, True, False, True, False] and at(tr, 85, 'CHW_FillLockoutAlarm') and not o(m, 'CHW_FillLockoutAlarm') and o(m, 'CHW_FillVolume') > 0
row('T14', 'Make-up', 'CHW loop fill + leak lock-out', 'open < 180 kPa, stays open to 200 kPa; filling > 20 s (FPT) -> valve locked closed + Critical alarm; RESET clears',
    ok, f"valve @8/18/28/38/55/85 s = {seq}; lockout @85s {at(tr, 85, 'CHW_FillLockoutAlarm')} after RESET {o(m, 'CHW_FillLockoutAlarm')}; fill {o(m, 'CHW_FillVolume'):.3f} m3")

# T15 bleed-off + dosing
m, tr = sim(FPT, [(0.0, {'CT01_BasinLevel': 75.0, 'CT02_BasinLevel': 75.0}), (60.0, {'CT_Conductivity': 2100.0}), (90.0, {'CT_Conductivity': 1900.0}), (120.0, {'CT_Conductivity': 1700.0}),
                  (130.0, {'CT01_BasinLevel': 60.0})], 150, extra=['CT_BleedValveCmd', 'CT_ChemDosingPumpCmd'])
seq = [at(tr, t, 'CT_BleedValveCmd') for t in (55, 85, 115, 145)]
ok = seq == [False, True, True, False] and o(m, 'CT_ChemDosingPumpCmd') and not at(tr, 125, 'CT_ChemDosingPumpCmd')
row('T15', 'Treatment', 'Bleed-off (conductivity) + dosing', 'bleed opens > 2000 uS/cm, holds to 1800; dosing pump runs with make-up water',
    ok, f"bleed @55/85/115/145 s = {seq}; dosing {at(tr, 125, 'CT_ChemDosingPumpCmd')} -> {o(m, 'CT_ChemDosingPumpCmd')} (make-up opened @130s)")

# T16 bypass: min-flow valve on evaporator flow, bypass flow meter removed, manual bypass alarm
m, tr = sim(FPT, [(0.0, {'CH01_ChwFlow': 200.0}), (80.0, {'CH01_ChwFlow': 45.0}), (200.0, {'CHW_BypassManualOpen': True})], 220, extra=['CHW_BypassValveCmd'])
ok = at(tr, 75, 'CHW_BypassValveCmd') < 1 and o(m, 'CHW_BypassValveCmd') > 5 and o(m, 'CHW_BypassManualOpenAlarm') and 'CHW_BypassFlow' not in m.C
row('T16', 'Bypass', 'Min-flow bypass valve (modulating)', 'evaporator flow 200 > 66 m3/h -> closed; 45 m3/h -> opens; no bypass flow meter; manual bypass open -> alarm',
    ok, f"valve {at(tr, 75, 'CHW_BypassValveCmd'):.1f} -> {o(m, 'CHW_BypassValveCmd'):.1f} % (SP {o(m, 'CHW_BypassMinFlowSP'):.0f} m3/h); manual alarm {o(m, 'CHW_BypassManualOpenAlarm')}; FT removed {'CHW_BypassFlow' not in m.C}")

# T17 zones (Sense-T / AirPlug)
z = '01_0103'
m, tr = sim(FPT, [(0.0, {f'ZoneTemperatureAvg_{z}': 29.0, 'ZoneTemperatureAvg_01_0104': 29.0, 'ZoneOutOfService_01_0104': True}),
                  (20.0, {'AirPlug_GatewayOnline': False})], 30, extra=[f'Zone_{z}_TempHighAlarm'])
ts = [o(m, f'ZoneTemperatureAvg_01_010{i}') for i in (1, 2, 3, 4)]
ok = at(tr, 15, f'Zone_{z}_TempHighAlarm') and not at(tr, 15, 'Zone_01_0104_TempHighAlarm') and o(m, 'AirPlug_GatewayOfflineAlarm') \
    and abs(o(m, 'Zone_AHU01_AvgTemp') - sum(ts) / 4) < 0.05
row('T17', 'Zones', 'Zone T / RH (Sense-T / AirPlug)', '29 degC -> over-temperature alarm after the delay; zone out of service -> no alarm; gateway offline alarm; AHU01 average of its 4 zones',
    ok, f"alarm {z} {at(tr, 15, f'Zone_{z}_TempHighAlarm')} OOS zone {at(tr, 15, 'Zone_01_0104_TempHighAlarm')}; gateway alarm {o(m, 'AirPlug_GatewayOfflineAlarm')}; AHU01 avg {o(m, 'Zone_AHU01_AvgTemp'):.2f}")

# T18 site timers: staging delay 10 min, de-staging 30 min
STEADY = {'PlantLoadPct': 50.0, 'CHWFlow': 150.0, 'ModeCmd_UI': False}
SB = [(0.0, STEADY), (10.0, {'BootQualified': True}), (15.0, {'PlantEnable': True})]
m, tr = sim(SITE, SB + [(400.0, {'CT_CommonSpeed': 95.0}), (400.0, cds_rel(2.0)), (1200.0, {'CT_CommonSpeed': 20.0}), (1200.0, cds_rel(-1.0))], 3100,
            extra=['CT_LagStaged', 'CT02_01RunProof'], every=5.0, base=False)
t_up = next((t for t, s_ in tr if s_['CT_LagStaged']), None)
t_dn = next((t for t, s_ in tr if t_up and t > t_up and not s_['CT_LagStaged']), None)
ok = t_up is not None and 995 <= t_up <= 1010 and t_dn is not None and 2995 <= t_dn <= 3010
row('T18', 'CT SOO', 'Site timers: 10 min staging / 30 min de-staging', 'conditions from 400 s -> lag staged ~1000 s; reduce conditions from 1200 s -> lag off ~3000 s',
    ok, f"staged @{t_up}s, de-staged @{t_dn}s; CT02/01 proven {o(m, 'CT02_01RunProof')}")
