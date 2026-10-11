# -*- coding: utf-8 -*-
"""V7.7 r7: AI (cloud) interface.
The AI platform connects from the cloud (not BACnet / field wiring) and finds points by the custom tag melco:pointNameString.
AI-WRITE points (heartbeat + AI setpoints) are taken out of the field-IO (BACnet / Modbus / hard-wired) register and get:
  <pt>.in10  <- written by the cloud connector (priority 10)
  <pt>.in16  <- IOS_<pt> = AI_SourceCloud ? {null} : simulation ramp / beat counter
so in CLOUD mode the value comes only from the AI write (or the point fallback when nothing was written); the existing
heartbeat detector + AI_ValuesValid range checks decide AI_Available, and the plant falls back to LOCAL setpoints when the
heartbeat stops (6 min pre-disconnect, 12 min disconnect).  Everything else the AI reads only."""
import make_v6 as M6
import v77_fieldcx as FCX
from make_v6 import child

CLOUD_W = ['HeartbeatTimestampSetpoint', 'CHW_LeavingTemperatureSetpoint_AI', 'CHWDP_Setpoint_AI', 'CDS_Setpoint_AI']
F = 'AI_Cloud'
_fp, _fio = FCX.field_points, FCX.field_io


def field_points(S):
    return [p for p in _fp(S) if p[0] not in CLOUD_W]


def cloud(S):
    S.bparam('AI_SourceCloud', False, folder=F, t='CLOUD (real AI)', f='SIMULATION (test ramps)',
             note='r7: true at site = AI values come only from the cloud write (in10); simulation ramps released')
    for n in CLOUD_W:
        el = S.comp[n]; sw = 'IOS_' + n
        S.kc(F, sw, 'NumericSwitch', {'inSwitch': 'AI_SourceCloud', 'inTrue': 'IO_NullN'})
        L10 = [c for c in el if c.get('t') == 'b:Link' and child(c, 'targetSlotName').get('v') == 'in10']
        if L10:
            L = L10[0]; el.remove(L); child(L, 'targetSlotName').set('v', 'inFalse'); L.set('n', 'Link2'); S.comp[sw].append(L)
        else:
            S.link(S.comp[sw], 'IO_NullN', 'inFalse')
        S.link(el, sw, 'in16')
    S.log.append(('V7.7r7', F, f'{len(CLOUD_W)} AI write points', 'cloud connector writes in10 (tag melco:pointNameString); sim -> in16 via IOS_', '', ''))


def field_io(S):
    r = _fio(S)
    cloud(S)
    return r


FCX.field_points = field_points
FCX.field_io = field_io
