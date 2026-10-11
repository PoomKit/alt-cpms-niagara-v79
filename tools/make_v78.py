# -*- coding: utf-8 -*-
"""Build ALT_CP_Ref_V7_8 = V7.7 r9 (make_v77.py, imported unchanged) + V7.8 trial logic (v78_improve.py,
SOO improvement list, user request 6 Oct 2026).  New station name / FoxS port so V7.7 is not touched."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_v6 as M6
import make_v7 as M7
import make_v77                                           # noqa: F401  installs V7.6 + V7.7 r1..r9
import v78_improve                                        # noqa: F401  V7.8 trial logic (hooks FCX.field_io after r9)
import v78_finish                                         # noqa: F401  r11: remaining SOO items

M6.STATION = M7.STATION = 'ALT_CP_Ref_V7_8'
M7.FOXS_PORT = '4926'

if __name__ == '__main__':
    M7.main()
