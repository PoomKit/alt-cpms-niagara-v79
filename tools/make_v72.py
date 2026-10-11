"""Build ALT_CP_Ref_V7_2 = V7.1 (make_v71.py, imported unchanged) + V7.2 layer:
  1. Pump suction / discharge motorised valves follow the pump (reference: PUNN MV program, MV S/S with the equipment):
     open on the pump request, pump starts only when both are proven open, close 30 s after the pump has stopped
     (standby / failed / isolated pumps are closed). Close delay = 'mv_close_delay' (site 30 s).
  2. Chiller staging with settable thresholds: Stage_UpLoadPct (start the next chiller when the plant load / running chiller
     reaches X % of one chiller), Stage_DownLoadPct (stop the lag chiller at or below Y %); both replace fixed 90 / 60 %.
  3. Emulation: idle tower leaving-water TT = basin temperature (no negative range while stopped).
New station folder (does not touch V7 / V7.1).  usage: make_v72.py c_v5.bog c_v5.tsv out.bog --regdir reg72 [--timing fpt]
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_v6 as M6
import make_v7 as M7
import make_v71 as M71
from make_v7 import AND, OR, NOT, DLY, CMP, const, T, F, UNITS

M6.STATION = M7.STATION = 'ALT_CP_Ref_V7_2'
M7.FOXS_PORT = '4920'
M6.TIMING['site'].update(mv_close_delay=30000)
M6.TIMING['fpt'].update(mv_close_delay=2000)


def pump_valves_follow(S, prof):
    S.bparam('Pump_StandbyValvesOpen', False, folder='PlantControl/Points', t='Standby valves OPEN', f='Valves follow pump',
             note='False (default): pump valves open only with the pump. True: healthy standby pumps keep their valves open '
                  '(faster pump changeover - no valve stroke before the standby can start)')
    for eq in ('CHP', 'CDP'):
        for n in UNITS:
            u = f'{eq}{n}'; L = f'{u}/Logic'
            OR(S, L, f'{u}MVDemand', f'{u}Request', f'{u}StartCmd', f'{u}RunProof', note='open with the pump request / command / run')
            AND(S, L, f'{u}StandbyOpenOK', 'Pump_StandbyValvesOpen', f'{u}Healthy')
            S.rewire(f'{u}MVDemand', 'inD', f'{u}StandbyOpenOK', F)
            DLY(S, L, f'{u}MVDemandHold', f'{u}MVDemand', 0, prof['mv_close_delay'], note='close after the pump has stopped (coast-down)')
            S.rewire(f'{u}MVOpenLogic', 'inC', f'{u}MVDemandHold', T)
            # valve command failure is LATCHED (else the pool would re-select the pump every cycle); RESET clears it
            M7.sealin(S, L, f'{u}MVFailLatch', f'{u}MVFailAny', f'{u}ManualReset', note='valve failure latched until RESET')
            S.rewire(f'{u}FaultAny', 'inC', f'{u}MVFailLatch', f'{u}MVFailAny')
            S.bpoint('Alarms', f'{u}_MVFailLatchedAlarm', f'{u}MVFailLatch', 'Valve failed', 'Normal')
            M6.COS[f'{u}_MVFailLatchedAlarm'] = (True, 'Critical', f'{u} suction / discharge valve failed - pump locked out, press RESET')


def staging(S, prof):
    ST = 'PlantControl/Staging'
    S.param('Stage_UpLoadPct', float(prof['stage_hi']), 'pct', lo=30, hi=100,
            note='START the next chiller when plant load (or the running chiller) reaches this % of one chiller')
    S.param('Stage_DownLoadPct', float(prof['stage_lo']), 'pct', lo=10, hi=95,
            note='STOP the lag chiller when plant load falls to this % of one chiller')
    CMP(S, ST, 'StageUpLoadReached', 'GreaterThanEqual', 'PlantLoadPct', 'Stage_UpLoadPct')
    CMP(S, ST, 'StageDownLoadReached', 'LessThanEqual', 'PlantLoadPct', 'Stage_DownLoadPct')
    M7.sealin(S, ST, 'StageLoadHigh', 'StageUpLoadReached', 'StageDownLoadReached', note='settable hysteresis (replaces fixed 90 / 60 %)')
    S.rewire('StageLoadTimer', 'in', 'StageLoadHigh', 'AutoStage2Hysteresis')
    S.rewire('LeadOverload', 'inB', 'Stage_UpLoadPct', 'LeadOverloadPct')      # running chiller >= X % -> next chiller (same setting)
    M6.NO_HISTORY.discard('Stage_UpLoadPct')


def sim_fixes(S, prof):
    for n in UNITS:
        S.rewire(f'Sim_CT{n}_Outlet', 'inFalse', f'CT{n}_BasinTemp', 'CDR')


_v71 = M71.v71


def v72(S, prof):
    _v71(S, prof)
    pump_valves_follow(S, prof)
    staging(S, prof)
    sim_fixes(S, prof)


M71.v71 = v72
M7.PX_PLANT.insert(5, ('Valves', 'ALT_V71_Valves'))

if __name__ == '__main__':
    M7.main()
