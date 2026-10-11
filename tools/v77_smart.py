"""V7.7 r5 layer (user request 2 Oct 2026 15:55): readable wire sheets + 'smart' operation features.
  A  Wire-sheet readability: big flat folders split into named sub-folders (Parameters by subsystem, Alarms by equipment,
     functional tests one folder per test) so every wire sheet shows one subject.
  B  Smart/PM       runtime-based preventive maintenance per equipment (hours since PM, % used, hours left, due / overdue,
                    PM DONE = reset of the PM totalizer), starts per day + short-cycling alarm
  C  Smart/FDD      predictive fault detection: chiller efficiency drift (filtered kW/RT vs baseline), pump hydraulic health
                    (kW vs affinity-law expectation), cooling-tower approach degradation, frozen-sensor detection
  D  Smart/Health   0-100 health score per equipment + 'health low' early-warning alarm, plant maintenance advisory
  E  Smart/Demand   Thai TOU peak (Mon-Fri 09:00-22:00) demand limiting: CHWST raised up to +2 K while plant kW > target
                    (disabled by default)"""
import re
import make_v6 as M6
import make_v7 as M7
import v77_fieldcx as FCX
from make_v6 import child, add_ext
from make_v7 import AND, OR, NOT, DLY, PULSE, SW, MATH, CMP, RATE, LIMIT, const

T, F = 'ConstantTrue', 'ConstantFalse'
PROF = FCX.PROF
tm = FCX.tm
PM_UNITS = [  # unit, run proof, kind, PM interval h, fault point
    ('CH01', 'CH01RunProof', 'chiller', 2000, 'CH01Fault'), ('CH02', 'CH02RunProof', 'chiller', 2000, 'CH02Fault'),
    ('CHP01', 'CHP01RunProof', 'pump', 4000, 'CHP01Fault'), ('CHP02', 'CHP02RunProof', 'pump', 4000, 'CHP02Fault'),
    ('CDP01', 'CDP01RunProof', 'pump', 4000, 'CDP01Fault'), ('CDP02', 'CDP02RunProof', 'pump', 4000, 'CDP02Fault'),
    ('CT01', 'CT01RunProof', 'tower', 2000, 'CT01Fault'), ('CT02', 'CT02RunProof', 'tower', 2000, 'CT02Fault'),
    ('AHU01', 'AHU01_Status', 'ahu', 1000, None), ('AHU02', 'AHU02_Status', 'ahu', 1000, None)]
REG = {'smart': []}


def alarm(S, f, name, src, t, fl, cls, text, note=''):
    S.bpoint(f, name, src, t, fl, note=note); M6.COS[name] = (True, cls, text); REG['smart'].append((name, cls, text))
    return name


def pen(S, f, name, cond, k):
    """numeric penalty k when cond is true"""
    return SW(S, f, name, cond, const(S, f'SM_K{k}', float(k), prec=0), 'Zero')


def smart(S):
    prof = PROF[0]
    PMF, FDD, HF, DF = 'Smart/PM', 'Smart/FDD', 'Smart/Health', 'Smart/Demand'
    if 'Zero' not in S.comp: const(S, 'Zero', 0.0)
    # ---------------------------------------------------------------- common
    S.param('PM_DuePct', 90, 'pct', folder=PMF, prec=0, lo=50, hi=100, note='PM due warning at this % of the interval')
    S.param('SM_ChillerMaxStartsDay', 6, folder=PMF, prec=0, note='chiller starts per day before short-cycling alarm')
    S.param('SM_EquipMaxStartsDay', 12, folder=PMF, prec=0, note='pump / tower / AHU starts per day before short-cycling alarm')
    S.kc(PMF, 'SM_DayPulse', 'OneShot', props=[('time', 'b:RelTime', '2000')], note='00:00 daily pulse (DayStartTrigger)')
    S.link(S.comp['SM_DayPulse'], 'DayStartTrigger.fireTrigger', 'fire')
    S.param('FDD_EffDevLimitPct', 15, 'pct', folder=FDD, prec=0, note='chiller kW/RT above baseline by this % -> advisory')
    S.param('FDD_PumpDevLimitPct', 25, 'pct', folder=FDD, prec=0, note='pump kW vs affinity law deviation -> advisory')
    S.param('FDD_CtApproachMarginK', 2.0, folder=FDD, prec=1, note='tower approach above design (CT_Approach) by this K at fan >= 90 %')
    S.param('FDD_HealthLowLimit', 70, 'pct', folder=HF, prec=0, note='health score below this -> early-warning alarm')
    adv_all = []
    long_dly = tm(7200000, 120000)                                       # 2 h site / 2 min FPT
    # ---------------------------------------------------------------- per equipment
    for u, run, kind, interval, fault in PM_UNITS:
        if run not in S.comp: continue
        # PM totalizer (persistent; PM DONE = Runtime.resetElapsedActiveTime action)
        S.bpoint(PMF, f'PM_{u}_Run', run, 'Running', 'Stopped')
        add_ext(S, f'PM_{u}_Run', 'Runtime', 'c:DiscreteTotalizerExt')
        S.param(f'PM_{u}_IntervalH', interval, 'hr', folder=PMF, prec=0, note=f'{kind} service interval (manufacturer / site PM plan)')
        S.kc(PMF, f'PM_{u}_HoursCalc', 'Divide', {'inA': f'PM_{u}_Run:Runtime.elapsedActiveTimeNumeric', 'inB': 'MsPerHour'})
        S.npoint(PMF, f'PM_{u}_HoursSincePM', f'PM_{u}_HoursCalc', 'hr', 1, note='running hours since last PM DONE')
        MATH(S, PMF, f'PM_{u}_LeftCalc', 'Subtract', f'PM_{u}_HoursCalc', f'PM_{u}_IntervalH')
        MATH(S, PMF, f'PM_{u}_LeftNeg', 'Multiply', f'PM_{u}_LeftCalc', const(S, 'SM_Minus1', -1.0, prec=0))
        S.npoint(PMF, f'PM_{u}_HoursLeft', f'PM_{u}_LeftNeg', 'hr', 0, note='negative = overdue')
        MATH(S, PMF, f'PM_{u}_Frac', 'Divide', f'PM_{u}_HoursCalc', f'PM_{u}_IntervalH')
        MATH(S, PMF, f'PM_{u}_PctCalc', 'Multiply', f'PM_{u}_Frac', 'HundredPct')
        S.npoint(PMF, f'PM_{u}_UsedPct', f'PM_{u}_PctCalc', 'pct', 0)
        CMP(S, PMF, f'PM_{u}_DueCmp', 'GreaterThanEqual', f'PM_{u}_PctCalc', 'PM_DuePct')
        CMP(S, PMF, f'PM_{u}_OverCmp', 'GreaterThanEqual', f'PM_{u}_PctCalc', 'HundredPct')
        alarm(S, PMF, f'PM_{u}_DueAlarm', f'PM_{u}_DueCmp', 'PM due', 'OK', 'Warning', f'{u} preventive maintenance due (≥ PM_DuePct of interval)')
        alarm(S, PMF, f'PM_{u}_OverdueAlarm', f'PM_{u}_OverCmp', 'PM overdue', 'OK', 'Warning', f'{u} preventive maintenance overdue')
        # starts per day / short cycling
        S.kc(PMF, f'PM_{u}_StartCounter', 'Counter', {'countUp': run, 'clearIn': 'SM_DayPulse'}, note='starts today (cleared 00:00)')
        S.npoint(PMF, f'PM_{u}_StartsToday', f'PM_{u}_StartCounter', 'none', 0)
        CMP(S, PMF, f'PM_{u}_ShortCycleCmp', 'GreaterThan', f'PM_{u}_StartCounter',
            'SM_ChillerMaxStartsDay' if kind == 'chiller' else 'SM_EquipMaxStartsDay')
        alarm(S, PMF, f'PM_{u}_ShortCycleAlarm', f'PM_{u}_ShortCycleCmp', 'Short cycling', 'OK', 'Warning',
              f'{u} too many starts today (short cycling) - check staging deadband, min-run, load stability')
        # predictive diagnostics
        adv = []
        if kind == 'chiller':
            S.param(f'FDD_{u}_BaselineKwPerRt', 0.60, folder=FDD, prec=3,
                    note='commissioning baseline kW/RT at >= 30 % load (set from 2 weeks of clean-tube data)')
            CMP(S, FDD, f'FDD_{u}_LoadOk', 'GreaterThanEqual', f'{u}LoadPct', const(S, 'SM_LoadMinPct', 30.0, 'pct', prec=0))
            DLY(S, FDD, f'FDD_{u}_Valid', AND(S, FDD, f'FDD_{u}_ValidLogic', run, f'FDD_{u}_LoadOk'), tm(1800000, 60000))
            S.kc(FDD, f'FDD_{u}_FiltSel', 'NumericSwitch', {'inSwitch': f'FDD_{u}_Valid', 'inTrue': f'{u}_kW_per_RT'})
            RATE(S, FDD, f'FDD_{u}_FiltRate', f'FDD_{u}_FiltSel', 0.002, tm(10000, 1000))
            S.npoint(FDD, f'FDD_{u}_KwPerRtFilt', f'FDD_{u}_FiltRate', 'none', 3, note='slow-filtered kW/RT (held while not valid)')
            S.link(S.comp[f'FDD_{u}_FiltSel'], f'FDD_{u}_KwPerRtFilt', 'inFalse')
            MATH(S, FDD, f'FDD_{u}_Ratio', 'Divide', f'FDD_{u}_KwPerRtFilt', f'FDD_{u}_BaselineKwPerRt')
            MATH(S, FDD, f'FDD_{u}_DevFrac', 'Subtract', f'FDD_{u}_Ratio', const(S, 'One', 1.0, prec=0))
            MATH(S, FDD, f'FDD_{u}_DevCalc', 'Multiply', f'FDD_{u}_DevFrac', 'HundredPct')
            CMP(S, FDD, f'FDD_{u}_HasData', 'GreaterThan', f'FDD_{u}_KwPerRtFilt', 'Zero')
            SW(S, FDD, f'FDD_{u}_DevShow', f'FDD_{u}_HasData', f'FDD_{u}_DevCalc', 'Zero')
            S.npoint(FDD, f'FDD_{u}_EffDevPct', f'FDD_{u}_DevShow', 'pct', 1, note='+ = more kW per RT than baseline (0 until first valid data)')
            CMP(S, FDD, f'FDD_{u}_EffHigh', 'GreaterThanEqual', f'FDD_{u}_DevCalc', 'FDD_EffDevLimitPct')
            DLY(S, FDD, f'FDD_{u}_EffDly', AND(S, FDD, f'FDD_{u}_EffLogic', f'FDD_{u}_Valid', f'FDD_{u}_EffHigh'), long_dly)
            adv.append(alarm(S, FDD, f'FDD_{u}_EffDegradeAlarm', f'FDD_{u}_EffDly', 'Efficiency degraded', 'OK', 'Warning',
                             f'{u} kW/RT above baseline - check condenser / evaporator tube fouling, refrigerant charge, CDW flow'))
            for a in (f'{u}EvapApproachAlarm', f'{u}CondApproachAlarm'):
                if a in S.comp: adv.append(a)
        elif kind == 'pump':
            grp = u[:3]
            S.param(f'FDD_{u}_BaselineRatio', 1.0, folder=FDD, prec=2, note='kW / (rated kW x speed³) measured at commissioning')
            MATH(S, FDD, f'FDD_{u}_SpeedFrac', 'Divide', f'{u}SpeedCmd', 'HundredPct')
            MATH(S, FDD, f'FDD_{u}_Expected', 'Multiply', f'FDD_{u}_SpeedFrac', f'FDD_{u}_SpeedFrac', f'FDD_{u}_SpeedFrac', f'{grp}_RatedKW')
            MATH(S, FDD, f'FDD_{u}_ExpGuard', 'Maximum', f'FDD_{u}_Expected', const(S, 'SM_MinKw', 0.5, 'kW'))
            MATH(S, FDD, f'FDD_{u}_RatioRaw', 'Divide', f'{u}_kW', f'FDD_{u}_ExpGuard')
            CMP(S, FDD, f'FDD_{u}_SpeedOk', 'GreaterThanEqual', f'{u}SpeedCmd', const(S, 'SM_SpeedMinPct', 30.0, 'pct', prec=0))
            DLY(S, FDD, f'FDD_{u}_Valid', AND(S, FDD, f'FDD_{u}_ValidLogic', run, f'FDD_{u}_SpeedOk'), tm(600000, 30000))
            S.kc(FDD, f'FDD_{u}_FiltSel', 'NumericSwitch', {'inSwitch': f'FDD_{u}_Valid', 'inTrue': f'FDD_{u}_RatioRaw'})
            RATE(S, FDD, f'FDD_{u}_FiltRate', f'FDD_{u}_FiltSel', 0.005, tm(10000, 1000))
            S.npoint(FDD, f'FDD_{u}_RatioFilt', f'FDD_{u}_FiltRate', 'none', 2, note='filtered kW / affinity-law kW')
            S.link(S.comp[f'FDD_{u}_FiltSel'], f'FDD_{u}_RatioFilt', 'inFalse')
            MATH(S, FDD, f'FDD_{u}_Ratio', 'Divide', f'FDD_{u}_RatioFilt', f'FDD_{u}_BaselineRatio')
            MATH(S, FDD, f'FDD_{u}_DevFrac', 'Subtract', f'FDD_{u}_Ratio', 'One')
            MATH(S, FDD, f'FDD_{u}_DevCalc', 'Multiply', f'FDD_{u}_DevFrac', 'HundredPct')
            CMP(S, FDD, f'FDD_{u}_HasData', 'GreaterThan', f'FDD_{u}_RatioFilt', 'Zero')
            SW(S, FDD, f'FDD_{u}_DevShow', f'FDD_{u}_HasData', f'FDD_{u}_DevCalc', 'Zero')
            S.npoint(FDD, f'FDD_{u}_PerfDevPct', f'FDD_{u}_DevShow', 'pct', 1, note='+ = more power than expected, - = less (dry run / clogged)')
            S.kc(FDD, f'FDD_{u}_DevAbs', 'AbsValue', {'inA': f'FDD_{u}_DevCalc'})
            CMP(S, FDD, f'FDD_{u}_DevHigh', 'GreaterThanEqual', f'FDD_{u}_DevAbs', 'FDD_PumpDevLimitPct')
            DLY(S, FDD, f'FDD_{u}_PerfDly', AND(S, FDD, f'FDD_{u}_PerfLogic', f'FDD_{u}_Valid', f'FDD_{u}_DevHigh'), long_dly)
            adv.append(alarm(S, FDD, f'FDD_{u}_PumpPerfAlarm', f'FDD_{u}_PerfDly', 'Pump performance changed', 'OK', 'Warning',
                             f'{u} power differs from affinity-law expectation - check bearing / impeller wear, strainer, valve position, air'))
        elif kind == 'tower':
            MATH(S, FDD, f'FDD_{u}_ApproachExcess', 'Subtract', f'{u}_Approach', 'CT_Approach')
            CMP(S, FDD, f'FDD_{u}_ApproachHigh', 'GreaterThanEqual', f'FDD_{u}_ApproachExcess', 'FDD_CtApproachMarginK')
            CMP(S, FDD, f'FDD_{u}_FanHigh', 'GreaterThanEqual', f'{u}SpeedCmd', const(S, 'SM_FanHighPct', 90.0, 'pct', prec=0))
            DLY(S, FDD, f'FDD_{u}_ApproachDly', AND(S, FDD, f'FDD_{u}_ApproachLogic', run, f'FDD_{u}_FanHigh', f'FDD_{u}_ApproachHigh'), long_dly)
            adv.append(alarm(S, FDD, f'FDD_{u}_ApproachAlarm', f'FDD_{u}_ApproachDly', 'Tower degraded', 'OK', 'Warning',
                             f'{u} approach high at full fan - check fill fouling, nozzles, fan belt / blade pitch, water distribution'))
        # health score
        pens = []
        if fault and fault in S.comp: pens.append(pen(S, HF, f'HS_{u}_PFault', fault, 40))
        pens.append(pen(S, HF, f'HS_{u}_POver', f'PM_{u}_OverCmp', 20))
        pens.append(pen(S, HF, f'HS_{u}_PDue', f'PM_{u}_DueCmp', 10))
        pens.append(pen(S, HF, f'HS_{u}_PCycle', f'PM_{u}_ShortCycleCmp', 10))
        for i, a in enumerate(adv): pens.append(pen(S, HF, f'HS_{u}_PAdv{i}', a, 25 if i == 0 else 15))
        lvl, k = pens, 0
        while len(lvl) > 1:
            lvl = [MATH(S, HF, f'HS_{u}_Sum{(k := k + 1)}', 'Add', *lvl[j:j + 4]) for j in range(0, len(lvl), 4)]
        MATH(S, HF, f'HS_{u}_Raw', 'Subtract', 'HundredPct', lvl[0])
        LIMIT(S, HF, f'HS_{u}_Lim', f'HS_{u}_Raw', 0, 100)
        S.npoint(HF, f'Smart_{u}_Health', f'HS_{u}_Lim', 'pct', 0, note='100 = healthy; minus fault / PM / short-cycle / predictive penalties')
        CMP(S, HF, f'HS_{u}_LowCmp', 'LessThan', f'HS_{u}_Lim', 'FDD_HealthLowLimit')
        alarm(S, HF, f'Smart_{u}_HealthLowAlarm', f'HS_{u}_LowCmp', 'Health low', 'OK', 'Warning', f'{u} health score below limit - see Asset Health page')
        adv_all += adv
    # ---------------------------------------------------------------- frozen sensors
    S.kc(FDD, 'SM_SampleClock', 'MultiVibrator', props=[('period', 'b:RelTime', str(tm(1800000, 60000)))], note='sample every 30 min')
    S.param('FDD_FrozenTol', 0.02, folder=FDD, prec=3, note='change smaller than this between samples = frozen')
    for s in ('CHWR', 'CDR', 'OA_Temperature', 'CHWFlow'):
        if s not in S.comp: continue
        S.kc(FDD, f'FDD_{s}_Prev', 'NumericLatch', {'in': s, 'clock': 'SM_SampleClock'})
        MATH(S, FDD, f'FDD_{s}_Diff', 'Subtract', s, f'FDD_{s}_Prev')
        S.kc(FDD, f'FDD_{s}_DiffAbs', 'AbsValue', {'inA': f'FDD_{s}_Diff'})
        CMP(S, FDD, f'FDD_{s}_Same', 'LessThan', f'FDD_{s}_DiffAbs', 'FDD_FrozenTol')
        DLY(S, FDD, f'FDD_{s}_FrozenDly', AND(S, FDD, f'FDD_{s}_FrozenLogic', 'PlantRunRequest', f'FDD_{s}_Same'), tm(10800000, 300000))
        adv_all.append(alarm(S, FDD, f'FDD_{s}_FrozenAlarm', f'FDD_{s}_FrozenDly', 'Frozen', 'OK', 'Warning',
                             f'{s} reading has not changed for 3 h while plant runs - check sensor / transmitter / comms'))
    # plant advisory
    lvl, k = list(adv_all), 0
    while len(lvl) > 1:
        lvl = [OR(S, HF, f'SM_AdvOr{(k := k + 1)}', *lvl[j:j + 4]) for j in range(0, len(lvl), 4)]
    S.bpoint(HF, 'Smart_MaintAdvisory', lvl[0], 'Maintenance advisory', 'Normal', note='any predictive warning active')
    # ---------------------------------------------------------------- TOU demand limit
    el = M6.schedule_el(S, 'Sch_TouPeak', weekly=('09:00:00.000', '22:00:00.000'))
    wk = next(c for c in next(c for c in el if c.get('n') == 'schedule') if c.get('n') == 'week')
    for i, d in enumerate(c for c in wk if c.get('t') == 'sch:DailySchedule'):
        if i in (0, 6):                                                    # Sunday, Saturday = off-peak
            dy = next(c for c in d if c.get('n') == 'day')
            for c in list(dy): dy.remove(c)
    S.comp['Sch_TouPeak'] = el; S.folder_of['Sch_TouPeak'] = DF
    S.log.append(('ADD', DF, 'Sch_TouPeak', 'sch:BooleanSchedule', 'Mon-Fri 09:00-22:00', 'Thai TOU peak; add public holidays as special events'))
    S.bparam('DL_Enable', False, folder=DF, t='Enabled', f='Disabled', note='TOU peak demand limiting')
    S.param('DL_TargetKW', 400, 'kW', folder=DF, prec=0, note='plant kW target during TOU peak (from the demand-charge plan)')
    S.param('DL_MaxOffsetK', 2.0, folder=DF, prec=1, lo=0, hi=3, note='max CHWST raise (K)')
    S.param('DL_ChwstCeiling', 12.0, 'C', folder=DF, prec=1, note='CHWST never above this with demand limit')
    CMP(S, DF, 'DL_Over', 'GreaterThan', 'Plant_kW', 'DL_TargetKW')
    DLY(S, DF, 'DL_ActiveDly', AND(S, DF, 'DL_Logic', 'DL_Enable', 'Sch_TouPeak', 'DL_Over'), tm(300000, 20000), tm(600000, 40000))
    alarm(S, DF, 'DL_ActiveSts', 'DL_ActiveDly', 'Demand limiting', 'Normal', 'Warning', 'TOU peak demand limit active: CHWST raised')
    SW(S, DF, 'DL_OffsetTarget', 'DL_ActiveDly', 'DL_MaxOffsetK', 'Zero')
    RATE(S, DF, 'DL_OffsetRate', 'DL_OffsetTarget', 0.1, tm(60000, 5000))
    S.npoint(DF, 'DL_ChwstOffset', 'DL_OffsetRate', 'none', 2, note='K added to the active CHWST setpoint')
    MATH(S, DF, 'DL_ChwstSum', 'Add', 'ChwstActiveClamp', 'DL_OffsetRate')
    MATH(S, DF, 'DL_ChwstFinal', 'Minimum', 'DL_ChwstSum', 'DL_ChwstCeiling')
    S.rewire('CHW_LeavingTemperatureSetpoint_ACTIVE', 'in16', 'DL_ChwstFinal', 'ChwstActiveClamp')
    S.bpoint(DF, 'DL_PeakNow', 'Sch_TouPeak', 'PEAK (TOU)', 'Off-peak')
    S.log.append(('V7.7r5', 'Smart', 'PM / FDD / health / demand', f'{len(REG["smart"])} alarms', '', ''))


# ---------------------------------------------------------------- A  folder reorganisation for readable wire sheets
PARAM_GROUPS = [
    (r'^(ConstantTrue|ConstantFalse|Zero|One|Hundred|HundredPct|FiftyPct|MsPerHour|Stage(Zero|One|Two)|Pct_to_Frac|ZeroSpeed|CX_K\d|SM_|CX_FT\d+_InjValue)', 'Constants'),
    (r'^(CH_|CH0\d_|MinLoadForKpi|LeadOverload|Stage)', 'Chillers'), (r'^(CHP_|CDP_|Pump_|Press_)', 'Pumps'),
    (r'^(CT_|Tower)', 'CoolingTowers'), (r'^(CHW|CHWS|CHWDP|DP_|Byp|CHWFlow|ChwsNot|Bypass|LowFlow|HB_|AI_)', 'ChwLoop_AI'),
    (r'^(CDS|CDW|CDR|CdsNot)', 'CdwLoop'), (r'^(OA_)', 'OutdoorAir'),
    (r'^(Tariff|Baseline|CO2_|BTU|Meter|kW_per|Water_kW|Amps_|HzPer|LoadSource|MeterFixed|PlantReset)', 'Energy'),
    (r'^(Plant|Rotation|Runtime|Boot|Load)', 'Plant'), (r'^Sim_', 'Simulation'),
    (r'^(MinusOne|Two|Three|Seven|Fourteen|Half|HalfC|Quarter|Third|Tiny|SecPerMin|PctToFrac|GpmHrToM3)$', 'Constants'),
    (r'^(Valid_|AHU|OAU|FCU|Fcu|EF0|Ef|CPEF|Cpef|LSF|SEF|Air|OAD_|Fan_|Press)', 'AirSide'),
    (r'^(MV_|VFD_|PF_|PM_Main|Makeup|Stg_|MinDeltaT|FixedCDP|ChwstNot|KpiMin)', 'Equipment')]


def regroup(S):
    moved = 0
    for n in list(S.comp):
        f = S.folder_of[n]
        if f == 'Parameters':
            S.folder_of[n] = 'Parameters/' + next((g for rx, g in PARAM_GROUPS if re.search(rx, n)), 'General'); moved += 1
        elif f == 'Alarms':
            m = re.match(r'^(CH0\d|CHP0\d|CDP0\d|CT0\d)', n)
            S.folder_of[n] = 'Alarms/' + (m.group(1) if m else 'Plant'); moved += 1
        elif f in ('Smart/PM', 'Smart/FDD', 'Smart/Health'):
            m = re.match(r'^(?:PM|FDD|HS|Smart)_([A-Z]+\d\d|CHWR|CDR|OA_Temperature|CHWFlow)_', n)
            S.folder_of[n] = f + '/' + (m.group(1).replace('OA_Temperature', 'Sensors').replace('CHWR', 'Sensors').replace('CDR', 'Sensors')
                                        .replace('CHWFlow', 'Sensors') if m else 'Common'); moved += 1
        elif f == 'Commissioning/FunctionalTest':
            m = re.match(r'^CX_(FT\d+)_', n)
            S.folder_of[n] = f + '/' + (m.group(1) if m else 'RunAll'); moved += 1
    S.log.append(('V7.7r5', 'regroup', f'{moved} components moved to sub-folders', 'Parameters / Alarms / FunctionalTest', '', ''))
    print('r5: regrouped', moved)


_orig_instrument = FCX._instrument


def _instrument_r5(S):
    regroup(S)
    return _orig_instrument(S)


FCX._instrument = _instrument_r5
_fcx_instrument = M6.instrument


def instrument_r5(S):
    smart(S)
    regroup(S)                      # before field_io so registers carry final paths; again before histories (new CX blocks)
    return _fcx_instrument(S)


M6.instrument = instrument_r5
