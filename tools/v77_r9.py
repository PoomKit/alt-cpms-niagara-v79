# -*- coding: utf-8 -*-
"""V7.7 r9: logic changes from the SOO R1 review (JA/TH/EN, comments by gpt), applied on top of r7.
 1 C-02  post-run anchor: CHn post-run (valves / pumps / towers kept on 120 s) now starts when the LAST of
         request, start command and run proof drops  (was: request only, so it could expire while the compressor
         was still running down)                                          CHnPostRunSrc = OR(Request, StartCmd, RunProof)
 2 C-04  safety-trip reset needs evap leaving water >= CH_FreezeResetTemp (5 C) - the parameter existed but was unused
                                                                          CHn_SafetyResetOk / CHn_SafetyResetAllowed
 3 E-02  CHP start gate: with CHP_RequireCdpFirst (default true) a CHW pump is only STARTED when a condenser pump is
         proven; once running it is not stopped by a CDP change-over (start-only gate)    CHPn_CdpFirstGate
 4 T-04  biocide A and B never run together: a request waits while the other cycle is active
                                                                          CT_BioA_ReqFree / CT_BioB_ReqFree
Already satisfied (verified in v77r9tests): protection trip removes the chiller command without waiting for min-run;
trip latches are not auto-retried; FCU fan speeds are exclusive."""
import make_v6 as M6
import v77_fieldcx as FCX
from make_v7 import AND, OR, NOT, CMP

_fio = FCX.field_io


def fold(S, n):
    return S.folder_of[n]


def r9(S):
    for c in ('01', '02'):
        ch = 'CH' + c
        f = fold(S, f'{ch}PostRun')
        OR(S, f, f'{ch}PostRunSrc', f'{ch}Request', f'{ch}StartCmd', f'{ch}RunProof',
           note='r9: post-run starts when request, start command and run proof are all off')
        S.rewire(f'{ch}PostRun', 'in', f'{ch}PostRunSrc', f'{ch}Request')
        f = fold(S, f'{ch}_SafetyTripNotReset')
        CMP(S, f, f'{ch}_SafetyResetOk', 'GreaterThanEqual', f'{ch}_ChwSupplyTemp', 'CH_FreezeResetTemp',
            note='r9: evap leaving water warm enough to allow a safety-trip reset')
        AND(S, f, f'{ch}_SafetyResetAllowed', f'{ch}ManualReset', f'{ch}_SafetyResetOk')
        S.rewire(f'{ch}_SafetyTripNotReset', 'in', f'{ch}_SafetyResetAllowed', f'{ch}ManualReset')
    S.bparam('CHP_RequireCdpFirst', True, folder=fold(S, 'CDP_AnyProven'), t='CDP before CHP', f='Independent',
             note='r9: CHW pump start waits for a proven condenser pump (start-only gate)')
    f = fold(S, 'CDP_AnyProven')
    NOT(S, f, 'CHP_CdpFirstOff', 'CHP_RequireCdpFirst')
    for c in ('01', '02'):
        p = 'CHP' + c
        f = fold(S, f'{p}StartPermit')
        OR(S, f, f'{p}_CdpFirstGate', 'CHP_CdpFirstOff', 'CDP_AnyProvenBridge', f'{p}RunProof',
           note='r9: start gate only - a running CHW pump is not stopped by a CDP change-over')
        S.rewire(f'{p}StartPermit', 'inC', f'{p}_CdpFirstGate', 'ConstantTrue')
    f = fold(S, 'CT_BioA_Edge')
    NOT(S, f, 'CT_BioA_NotCycle', 'CT_BioA_Cycle'); NOT(S, f, 'CT_BioB_NotCycle', 'CT_BioB_Cycle')
    AND(S, f, 'CT_BioA_ReqFree', 'CT_BioA_Req', 'CT_BioB_NotCycle', note='r9: biocide A waits while B cycle runs')
    AND(S, f, 'CT_BioB_ReqFree', 'CT_BioB_Req', 'CT_BioA_NotCycle', note='r9: biocide B waits while A cycle runs')
    S.rewire('CT_BioA_Edge', 'in', 'CT_BioA_ReqFree', 'CT_BioA_Req')
    S.rewire('CT_BioB_Edge', 'in', 'CT_BioB_ReqFree', 'CT_BioB_Req')
    S.log.append(('V7.7r9', 'SOO R1 review', 'post-run anchor, freeze reset temp, CDP-before-CHP start gate, biocide A/B interlock', '', '', ''))


def field_io(S):
    r = _fio(S)
    r9(S)
    return r


FCX.field_io = field_io
