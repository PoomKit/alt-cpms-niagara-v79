# -*- coding: utf-8 -*-
"""Executable test station for the V7.9 layers (no source station needed).

Builds the V7.9 layer (v79_scale + v79_air + v79_office) on the stub station of check_v79_refs.py, turns every base component it
reads into a writable point (BooleanWritable / NumericWritable with a sensible default, tests override them like field inputs),
and writes a .bog the offline model (sim7.Model6) runs. Plant logic of the base station is NOT in this model: plant values the
layer reads (CHWS, schedules, fire alarm, AHU01 / AHU02 status ...) are inputs set by the test.
usage: python3 layer_sim.py <out.bog> [--timing fpt|site]"""
import csv, os, sys, zipfile
import xml.etree.ElementTree as ET
from collections import OrderedDict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_v6 as M6
import v77_fieldcx as FCX
import eqreg
import check_v79_refs as CR
import v79_scale as SC

BOOL_TYPES = ('BooleanWritable', 'And', 'Or', 'Not', 'BooleanDelay', 'BooleanLatch', 'BooleanSwitch', 'OneShot', 'MultiVibrator', 'GreaterThan',
              'GreaterThanEqual', 'LessThan', 'LessThanEqual', 'NotEqual', 'Hysteresis', 'BooleanSchedule', 'BooleanPoint')
DEFAULTS = {'ConstantTrue': True, 'ConstantFalse': False, 'Zero': 0.0, 'One': 1.0, 'HundredPct': 100.0, 'MsPerHour': 3600000.0, 'ZeroSpeed': 0.0,
            'NotFireAlarm': True, 'Sch_AHU': True, 'OA_Temperature': 33.0, 'CHWS': 7.0, 'CHWR': 12.5, 'CDS': 30.0, 'CDR': 35.0,
            'PlantPermissive': True, 'Gfx_ChwMain_Fwd': True, 'Gfx_CdwTotal_Fwd': True, 'AHU01_SAT': 14.0, 'AHU02_SAT': 14.0,
            'AHU01_Status': True, 'AHU02_Status': True, 'AHU01_ValveCmd': 50.0, 'AHU02_ValveCmd': 50.0, 'CH_HpvTempLow': 15.0,
            'CH_HpvTempHigh': 20.0, 'CH_HpvMinPos': 30.0, 'CH_HpvEnable': True, 'Zone_TempAlarmHigh': 27.0, 'Zone_RHAlarmHigh': 70.0, 'PctToFrac': 0.01, 'Two': 2.0,
            'CH_FreezeTripTemp': 3.0, 'CH_FreezeResetTemp': 5.0, 'CT_LevelLowLowPct': 15.0, 'CT_LevelLowLowResetPct': 30.0, 'CT_LeadSpeed': 60.0,
            'X_HzPerPct': 0.5}


def comp_types():
    return {r['Component']: r['Type'] for r in csv.DictReader(open(CR.COMPONENTS, encoding='utf-8-sig'))}


def build(timing='fpt', register=None):
    SC.REG = eqreg.load(register)
    FCX.PROF[0] = M6.TIMING[timing]
    rows = list(csv.DictReader(open(CR.COMPONENTS, encoding='utf-8-sig')))
    base = OrderedDict((r['Component'], r['Folder']) for r in rows)
    base2, created = CR.layer_base(base)
    S = CR.Stub(base2); SC.scale(S); SC.post(S)
    if S.errors: raise SystemExit('reference errors: ' + '; '.join(sorted(set(S.errors))[:10]))
    types = comp_types()
    for n in list(S.base):                                    # placeholders -> writable inputs
        el = S.comp[n]; t = types.get(n, '').split(':')[-1]
        boolean = t in BOOL_TYPES or isinstance(DEFAULTS.get(n), bool)
        el.set('t', 'c:BooleanWritable' if boolean else 'c:NumericWritable')
        fb = ET.SubElement(el, 'p', {'n': 'fallback', 't': 'b:StatusBoolean' if boolean else 'b:StatusNumeric'})
        v = DEFAULTS.get(n, False if boolean else 0.0)
        ET.SubElement(fb, 'p', {'n': 'value', 'v': str(bool(v)).lower() if boolean else repr(float(v))})
    return S


def write(S, path):
    root = ET.Element('bajaObjectGraph', {'version': '4.0'})
    st = ET.SubElement(root, 'p', {'n': 'Station', 't': 'b:Station'})
    cp = ET.SubElement(st, 'p', {'n': 'ChillerPlant', 't': 'b:Folder', 'h': 'fffff'})
    for el in S.comp.values(): cp.append(el)
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('file.xml', ET.tostring(root, encoding='unicode'))
    return path


if __name__ == '__main__':
    timing = sys.argv[sys.argv.index('--timing') + 1] if '--timing' in sys.argv else 'fpt'
    S = build(timing)
    print('wrote', write(S, sys.argv[1]), len(S.comp), 'components')
