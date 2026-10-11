"""Build ALT_CP_Ref_V7_6 = V7.5 (make_v75.py, imported unchanged) + V7.6 equipment sizing (user request 29 Sep 2026 22:31).

Design basis (values written in the legacy units kPa / m3/h, converted to bar / gpm by the V7.4 units pass):
  Chiller  300 RT magnetic-bearing (oil-free) centrifugal, variable primary flow
           evaporator max 720 gpm (2.4 gpm/RT), min 216 gpm (30 %), dP 20 ft @ 720 gpm; condenser 900 gpm, dP 25 ft; 170 kW (0.567 kW/RT)
  CHP      720 gpm @ 110 ft (33.5 m), 22 kW (30 hp) motor, ACH580-01-045A-4
  CDP      900 gpm @ 80 ft (24.4 m), 22 kW (30 hp) motor, ACH580-01-045A-4
  CT       crossflow, 900 gpm per tower (2 cells), range 5.3 K, approach 3.0 K @ 27 C WB, fan 5.5 kW per cell, ACH580-01-012A-4
usage: make_v76.py c_v5.bog c_v5.tsv out.bog --regdir reg76 [--timing fpt]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_v6 as M6
import make_v7 as M7
import make_v74 as M74
import make_v75 as M75
from make_v7 import const          # noqa: F401  (installs the V7.5 layer)

M6.STATION = M7.STATION = 'ALT_CP_Ref_V7_6'
M7.FOXS_PORT = '4924'
GPM = 4.402867539
FT = 2.98907                     # kPa per ft of water

SIZING = [  # (parameter, value in kPa / m3h / kW, note)
    ('CH01_RatedKW', 170.0, 'magnetic-bearing 300 RT, 0.567 kW/RT at AHRI full load'),
    ('CH02_RatedKW', 170.0, ''),
    ('CH01_MinFlow', 216 / GPM, 'evaporator min 216 gpm = 30 % of 720 gpm (VPF)'),
    ('CH02_MinFlow', 216 / GPM, ''),
    ('CH_ChwFlowLimit', 720 / GPM, 'evaporator max 720 gpm = 300 RT x 2.4 gpm/RT'),
    ('CH_CdwMinFlow', 360 / GPM, 'condenser min 360 gpm = 40 % of 900 gpm'),
    ('CHP_DesignHead', 110 * FT, 'CHP 720 gpm @ 110 ft'),
    ('CHP_RatedKW', 22.0, 'CHP motor 22 kW (30 hp)'),
    ('CDP_DesignFlow', 900 / GPM, 'CDP 900 gpm = 300 RT x 3 gpm/RT'),
    ('CDP_DesignHead', 80 * FT, 'CDP 900 gpm @ 80 ft'),
    ('CDP_RatedKW', 22.0, 'CDP motor 22 kW (30 hp)'),
    ('CT_CdwMinFlow', 360 / GPM, 'crossflow tower min 40 % (hot-water basin distribution)'),
    ('CT_Approach', 3.0, 'approach 3.0 K @ 27 C WB'),
    ('Sim_EvapDPk', 20 * FT / (720 / GPM) ** 2, 'SIM: evaporator 20 ft @ 720 gpm'),
    ('Sim_CondDPk', 25 * FT / (900 / GPM) ** 2, 'SIM: condenser 25 ft @ 900 gpm'),
    ('Sim_CH_PLFixed', 0.06, 'SIM: magnetic bearing - low fixed losses'),
    ('Sim_CH_PLVar', 0.94, ''),
    # system curve: design 2 x 720 gpm, index coil + valve 100 kPa, pump 110 ft, shut-off 1.2 x design head
    ('Sim_FlowRef', 1440 / GPM, 'SIM: plant design flow 2 x 720 gpm'),
    ('Sim_PumpShutoffDP', 1.2 * 110 * FT, 'SIM: shut-off head 1.2 x 110 ft'),
    ('Sim_BypFlowPerPct', 432 / GPM / 100, 'SIM: min-flow bypass valve: 432 gpm (2 x chiller min) fully open at the coil design dP'),
]


def sizing(S, prof):
    for n, v, note in SIZING:
        S.set_fallback(n, round(v, 6))
    S.log.append(('SIZING', '', 'V7.6', f'{len(SIZING)} parameters', 'equipment schedule', ''))


_units = M74.units


def hydraulic76(S, prof):
    """V7.6 hydraulic network (replaces the V7.5 DP formula and the first flow-limit fix).  ONE flow Q from the pump curve through
    the series system, so flow follows the VSD (affinity: 50 % speed -> ~50 % flow) and every valve changes it:
        pumps  : H = H0 s^2 - kp (Q/N)^2                     (H0 shut-off, N pumps in parallel, s = speed)
        system : H = (Kpipe + Kevap + Kloop) Q^2
          Kevap = 1 / Ge^2,  Ge = sum(chiller path open x FCV % x Gmax)      (evaporator branches in parallel)
          Kloop = 1 / Ct^2,  Ct = Cb + Cbp                                   (building coils // min-flow bypass)
          Cb = building demand / sqrt(coil design dP),  Cbp = bypass flow at design dP / sqrt(coil design dP)
        Q = s sqrt(H0 / (kp/N^2 + Kpipe + Kevap + Kloop));  loop dP = (Q/Ct)^2;  building = Q Cb/Ct;  bypass = Q Cbp/Ct
    Chiller: leaving water held at its setpoint, capacity (% load) follows the building load carried by this flow."""
    from make_v7 import MATH
    from make_v74 import relink_sim, drop_if_unused
    HY = 'Simulation/Hydraulic'
    S.param('Sim_PipeLossDesign', 48 * FT, 'kPa', folder=HY, note='SIM: plant piping + mains at the plant design flow (48 ft)')
    S.param('Sim_EvapBranchFlow', 720 / GPM, 'm3h', folder=HY, lo=1, note='SIM: evaporator branch flow with the FCV open ...')
    S.param('Sim_EvapBranchDP', 20 * FT, 'kPa', folder=HY, lo=1, note='SIM: ... at this branch dP (evaporator 20 ft)')
    S.param('Sim_PumpDesignFlow', 720 / GPM, 'm3h', folder=HY, lo=1, note='SIM: one pump design flow (its design head = CHP_DesignHead)')
    # pump curve droop kp = (H0 - Hdesign) / Qd^2, per pump -> / N^2 for N pumps in parallel
    MATH(S, HY, 'Sim_PumpDroop', 'Subtract', 'Sim_PumpShutoffDP', 'CHP_DesignHead')
    MATH(S, HY, 'Sim_PumpQd2', 'Multiply', 'Sim_PumpDesignFlow', 'Sim_PumpDesignFlow')
    MATH(S, HY, 'Sim_Kp1', 'Divide', 'Sim_PumpDroop', 'Sim_PumpQd2')
    MATH(S, HY, 'Sim_KpN', 'Divide', 'Sim_Kp1', 'Sim_PumpsOnSq')
    MATH(S, HY, 'Sim_FlowRef2', 'Multiply', 'Sim_FlowRef', 'Sim_FlowRef')
    MATH(S, HY, 'Sim_Kpipe', 'Divide', 'Sim_PipeLossDesign', 'Sim_FlowRef2')
    # evaporator branches (FCV feedback = opening)
    S.kc(HY, 'Sim_EvapBranchDPSqrt', 'SquareRoot', {'inA': 'Sim_EvapBranchDP'})
    MATH(S, HY, 'Sim_EvapGmax', 'Divide', 'Sim_EvapBranchFlow', 'Sim_EvapBranchDPSqrt')
    for n in ('01', '02'):
        MATH(S, HY, f'Sim_CH{n}_Ge', 'Multiply', f'Sim_CH{n}_ChwOn', f'CH{n}_ChwFCVFb', 'PctToFrac', 'Sim_EvapGmax')
    MATH(S, HY, 'Sim_GeSum', 'Add', 'Sim_CH01_Ge', 'Sim_CH02_Ge')
    MATH(S, HY, 'Sim_GeG', 'Maximum', 'Sim_GeSum', 'Tiny')
    MATH(S, HY, 'Sim_Ge2', 'Multiply', 'Sim_GeG', 'Sim_GeG')
    MATH(S, HY, 'Sim_Kevap', 'Divide', 'One', 'Sim_Ge2')
    # loop: building coils in parallel with the min-flow bypass (+ manual bypass)
    S.kc(HY, 'Sim_CoilDPSqrt', 'SquareRoot', {'inA': 'Sim_CoilDesignDP'})
    MATH(S, HY, 'Sim_Cb', 'Divide', 'Sim_BldgDemand', 'Sim_CoilDPSqrt')
    MATH(S, HY, 'Sim_Cbp', 'Divide', 'Sim_BypFlowRaw', 'Sim_CoilDPSqrt')
    MATH(S, HY, 'Sim_Ct', 'Add', 'Sim_Cb', 'Sim_Cbp')
    MATH(S, HY, 'Sim_CtG', 'Maximum', 'Sim_Ct', 'Tiny')
    MATH(S, HY, 'Sim_Ct2', 'Multiply', 'Sim_CtG', 'Sim_CtG')
    MATH(S, HY, 'Sim_Kloop', 'Divide', 'One', 'Sim_Ct2')
    MATH(S, HY, 'Sim_Ksum', 'Add', 'Sim_KpN', 'Sim_Kpipe', 'Sim_Kevap', 'Sim_Kloop')
    MATH(S, HY, 'Sim_QMax2', 'Divide', 'Sim_PumpShutoffDP', 'Sim_Ksum')
    S.kc(HY, 'Sim_QMax', 'SquareRoot', {'inA': 'Sim_QMax2'})
    MATH(S, HY, 'Sim_Q', 'Multiply', 'Sim_PumpSpeedFrac', 'Sim_QMax', 'Sim_LoopOn', note='plant flow from the pump curve (affinity)')
    S.npoint(HY, 'Sim_PlantFlow', 'Sim_Q', 'm3h', 0, kind='sim', note='emulated total CHW flow = pump curve x system curve')
    M6.NO_HISTORY.add('Sim_PlantFlow')
    MATH(S, HY, 'Sim_QoverCt', 'Divide', 'Sim_Q', 'Sim_CtG')
    MATH(S, HY, 'Sim_DpLoop', 'Multiply', 'Sim_QoverCt', 'Sim_QoverCt', note='loop dP = (Q / Ct)^2')
    S.rewire('Sim_DpErr', 'inA', 'Sim_DpLoop', 'Sim_DpCalc')
    MATH(S, HY, 'Sim_QBldg', 'Multiply', 'Sim_QoverCt', 'Sim_Cb', note='building flow = Q x Cb / Ct')
    MATH(S, HY, 'Sim_QByp', 'Multiply', 'Sim_QoverCt', 'Sim_Cbp', note='bypass flow = Q x Cbp / Ct')
    relink_sim(S, 'CHWFlow', 'Sim_QBldg', 'building flow = share of the pump flow through the coils')
    S.rewire('Sim_BypFlow', 'inA', 'Sim_QByp', 'Sim_BypFlowRaw')
    for n in ('Sim_BldgFlow', 'Sim_DpCalc', 'Sim_DpHead', 'Sim_SystemDen', 'Sim_SystemX', 'Sim_LossRatio', 'Sim_DemandRatio',
              'Sim_LossRef', 'Sim_PumpLossN'):
        drop_if_unused(S, n)
    drop_if_unused(S, 'Sim_PumpLossRef', 'Sim_PipeLossRef')


def flow_staging(S, prof):
    """VPF: start the 2nd chiller when the running chiller cannot pass the plant flow - its evaporator FCV is throttling to hold
    the max flow (720 gpm).  After the 2nd chiller starts the request is held while the plant evaporator flow stays above 80 %
    of one chiller's max flow (no stage cycling)."""
    from make_v7 import MATH, CMP, AND, OR, DLY
    ST = 'PlantControl/Staging'
    S.param('Stg_FcvLimitPct', 90.0, 'pct', folder=ST, note='FCV below this on a running chiller = flow-limited')
    for n in ('01', '02'):
        CMP(S, ST, f'Stg_CH{n}_FcvLow', 'LessThan', f'CH{n}_ChwFCVCmd', 'Stg_FcvLimitPct')
        AND(S, ST, f'Stg_CH{n}_FlowLimited', f'Stg_CH{n}_FcvLow', f'CH{n}RunProofSelected')
    OR(S, ST, 'Stg_FcvLimited', 'Stg_CH01_FlowLimited', 'Stg_CH02_FlowLimited')
    MATH(S, ST, 'Stg_FlowRatio', 'Divide', 'CHW_EvapFlowTotal', 'CH_ChwFlowLimit', note='plant evaporator flow / one chiller max flow')
    const(S, 'Stg_HoldRatio', 0.8, 'none', 2)
    CMP(S, ST, 'Stg_FlowAbove80', 'GreaterThanEqual', 'Stg_FlowRatio', 'Stg_HoldRatio')
    AND(S, ST, 'Stg_FlowHold', 'Stg_FlowAbove80', 'CH_BothRunning')
    OR(S, ST, 'Stg_FlowNeed', 'Stg_FcvLimited', 'Stg_FlowHold')
    site = prof is M6.TIMING['site']
    DLY(S, ST, 'Stg_FlowStageUp', 'Stg_FlowNeed', 300000 if site else 5000, 900000 if site else 8000, note='5 min on / 15 min off (site)')
    S.rewire('Stage2LoadOrTemp', 'inD', 'Stg_FlowStageUp', 'ConstantFalse')
    S.bpoint(ST, 'Stage2FlowRequest', 'Stg_FlowStageUp', 'Flow > 1 chiller', 'Normal', note='VPF: plant flow needs the 2nd evaporator')


def units76(S, prof):
    hydraulic76(S, prof)
    flow_staging(S, prof)
    sizing(S, prof)            # before the kPa -> bar / m3h -> gpm conversion
    _units(S, prof)


M74.units = units76
_px = [n for _, n in M7.PX_PLANT]
M7.PX_PLANT.insert(_px.index('ALT_V75_AiDtGuard') + 1, ('Design', 'ALT_V76_Design'))

if __name__ == '__main__':
    M7.main()
