"""Field interface export: reads the protocol selected per group in the station (IO_<group>_Protocol) and writes one driver
point list per protocol (what to create under BacnetNetwork / ModbusNetwork / the I/O module, and which IO_ point to link).
usage: fieldio_export.py config.bog V7_7_FIELD_IO_REGISTER.csv outdir"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cx_report import bog_values, rcsv, PROTO

bog, reg, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
bv = bog_values(bog)
by = {}
for r in rcsv(reg):
    p = int(bv.get(f"IO_{r['Group']}_Protocol", r['Protocol']))
    if p in (1, 2): addr = dict(Device_Instance=r['BACnet_Device'], Object=r['BACnet_Object'],
                                Proxy_Type={'AI': 'NumericPoint', 'DI': 'BooleanPoint', 'DO': 'BooleanWritable', 'AO': 'NumericWritable'}[r['Type']])
    elif p in (3, 4): addr = dict(Unit_Id=r['Modbus_Unit'], Register=r['Modbus_Register'],
                                  Proxy_Type={'AI': 'NumericPoint', 'DI': 'BooleanPoint', 'DO': 'BooleanWritable', 'AO': 'NumericWritable'}[r['Type']])
    else: addr = dict(Module=r['IO_Module'], Channel=r['IO_Channel'], Signal=r['Signal'])
    link = (f"proxy.out -> {r['IO_Point']}.in16" if r['Direction'] == 'in' else f"{r['IO_Point']}.out -> proxy.in10")
    by.setdefault(p, []).append(dict(Group=r['Group'], Point=r['Point'], IO_Point=r['IO_Point'], Type=r['Type'], Unit=r['Unit'], **addr,
                                     Link=link, IO_Path=r['IO_Path']))
for p, rows in sorted(by.items()):
    fn = os.path.join(out, f"FIELDIO_{PROTO[p].replace('/', '_').replace(' ', '_').replace('-', '')}.csv")
    with open(fn, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(fn, len(rows))
