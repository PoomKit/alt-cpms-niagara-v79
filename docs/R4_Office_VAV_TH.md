# ALT_CP_Ref_V7_9 r4 — ระบบปรับอากาศอาคารสำนักงาน (VAV) จากแบบ R9 + ปรับปรุงกราฟฟิก 3D / Px

ฉบับ 11 ต.ค. 2026 · ต่อจาก r3 · แหล่งข้อมูลแบบ: `ALT_V79_Office_R9_Runtime_20261011.zip` (OFFICE-B1-R9, coordinated concept)

## 1. สิ่งที่นำเข้าจากแพ็กเกจ R9

| รายการ | ที่อยู่ใน repo | หมายเหตุ |
|---|---|---|
| ข้อมูลแบบ (ห้อง 200, VAV 123, MD 168, หัวจ่าย 1,017, ท่อลม 2,341 ช่วง, เซนเซอร์ห้อง 200, มิเตอร์ชั้น 8, tenant 14) | `graphics3d/data/office79.json` | แยกจาก `ALT_V79_Building3D.html` ของ R9 (ตัด `ductShells` ที่เป็น mesh คำนวณล่วงหน้าออก) |
| geometry อาคาร R9 (ห้องเครื่องย้ายไปชั้นใต้ดิน B1) | `graphics3d/data/r9_model.json` | หน้า 3D ใช้ไฟล์นี้แทน MODEL เดิม |
| Px ใหม่ 15 หน้า, รูป `v79_2d/`, หน้า HTML 4 หน้า (Rental / AHU / Tenant / Billing) | `station/shared/px`, `station/shared/web` | หน้า HTML ทั้ง 4 เป็น DEMO (ไม่มี point จริง) ตามที่ R9 ส่งมา |
| `ALT_V79_Plant.px` (ภาพรวมแบบใหม่) | `station/shared/px/ALT_V79_Plant.px` | หน้า schematic 6 slot เดิมย้ายเป็น `ALT_V79_Plant_Details.px` (ฉบับ repo ครบกว่า R9 92 จุด) |

`ALT_V79_Building3D.html` ของ R9 ไม่ได้ใช้ตรง ๆ เพราะเป็น bundle ย่อที่ไม่มี source และย้อนการแก้ loader ของ r3 —
ความสามารถของ R9 (ห้อง/ท่อลม/VAV/ลมไหล) ถูกเขียนใหม่ใน `graphics3d/office79.js` และผูกจุดจริงของ station

## 2. Logic ใหม่ (`tools/v79_office.py`) — หลักการออกแบบ

| ส่วน | ลำดับการทำงาน | มาตรฐาน / แนวปฏิบัติอ้างอิง |
|---|---|---|
| VAV (123 ชุด) | โหมด occupied / occupied-standby (ห้องว่าง 5 นาที → setpoint +1 K, airflow ขั้นต่ำเหลือส่วนพื้นที่) / unoccupied · cooling loop → airflow setpoint Vmin..Vmax · airflow loop → damper · ส่ง request ให้ AHU · alarm airflow ต่ำ 70 %/50 %, damper ไม่ตาม, ห้องร้อน, CO2, RH, เซนเซอร์เสีย · out-of-service | ASHRAE Guideline 36 §5.6 (cooling-only VAV) |
| AHU ชั้น 2-8 | duct static setpoint แบบ Trim & Respond (25-250 Pa) → VSD · SAT setpoint แบบ T&R (12.8-18 °C) → PICV · RH ห้องกลับสูง → SAT ไม่เกิน 13 °C (ลดความชื้น) · ไม่มี economizer (ภูมิอากาศร้อนชื้น) · OA ตามค่าวัดจริง (airflow station) | ASHRAE G36 §5.16 · ASHRAE 90.1 (fan / reset) |
| อากาศภายนอก | Vbz = Rp·Pz + Ra·Az ต่อห้อง (5 L/s/คน + 0.6 L/s/m² ตามแบบ R9) · Vot = ΣVbz / Ev (0.8) · DCV: ห้องว่าง → ตัดส่วนคน · alarm เมื่อ OA ต่ำกว่า 90 % ของ Vot 10 นาที | ASHRAE 62.1 (Ventilation Rate Procedure, DCV) · มาตรฐานการระบายอากาศของ วสท. (ต้องตรวจค่าตามตารางฉบับที่ใช้จริง) |
| ความปลอดภัย | duct static สูงเกิน 375 Pa → หยุดพัดลม latch ต้องกด reset (G36 §5.16.8) · fire alarm → AHU หยุด, OA/relief ปิด (ระบบนี้ไม่ใช่ smoke control) · feedback ไม่ตามคำสั่ง (VSD, OA damper, PICV) → alarm | G36 · แนวปฏิบัติระบบแจ้งเหตุเพลิงไหม้ / ระบายควันของ วสท. (ต้องประสานผู้ออกแบบระบบดับเพลิง) |
| มิเตอร์ | BTU ชั้น = flow(m³/h) × 4.186 × ΔT / 3.6 (kW) + kWh · ΔT ต่ำ < 3 K มีน้ำไหล 30 นาที → low ΔT alarm · ΔT ติดลบ → meter fault · ผลรวม sub-meter tenant > มิเตอร์ชั้น 2 % → alarm · thermal billing ต่อ tenant **ปิด** (coil AHU ใช้ร่วม ตาม R9) | ASHRAE 90.1 §8.4 (metering), แนวปฏิบัติ M&V |
| Plant (slot 03-06) | freeze trip (LWT < `CH_FreezeTripTemp`, latch, reset เมื่อ > `CH_FreezeResetTemp`) · anti-recycle (min off 10 นาที) · CT basin low-low → หยุด tower · B1 น้ำท่วม (`PlantRoom_FloodSw`) → Emergency alarm + หยุด chiller (`CH_StopOnFlood`) | เหมือน CH01/02 (V7.7) · OEM chiller · ห้องเครื่องใต้ดิน |

ค่าทุกค่าเป็น parameter ใน Workbench (โฟลเดอร์ `AirSide/Floors/Common`, `Metering/Floors/Common`, `Alarms/PlantRoom`) —
ค่า default เป็น design intent ต้องยืนยันด้วย TAB / commissioning และวิศวกรผู้รับผิดชอบ (EOR)

### จุดใน station
- ห้อง: `AirSide/Floors/Fnn/Rooms/<ห้อง>/RM_<ห้อง>_T, _RH, _CO2, _Occ` (+ `_SensorFaultAlarm`)
- VAV: `AirSide/Floors/Fnn/VAV/VAV_<ห้อง>/…_Airflow, _AirflowSP, _DmpCmd, _DmpFb, _CoolSPActive, _OOS` + alarm
- AHU: `AirSide/Floors/Fnn/AHU_Fnn_*` (SAT_SP, DuctSP_SP, OAFlowSP, PressureRequests, CoolingRequests …)
- มิเตอร์: `Metering/Floors/Fnn/BTU_Fnn_kW, FM_Fnn_Flow, TT_S/R_Fnn, PM_Fnn_kW/kWh, PM_Fnn_A/B_kW/kWh`
- ชั้น 1: VAV ล็อบบี้ / ศูนย์อาหาร 4 ชุดใช้ AHU01 / AHU02 (logic V7.8 เดิม)

## 3. การทดสอบ
- `tools/layer_sim.py` สร้าง station ทดสอบจาก layer V7.9 โดยไม่ต้องมี source bog (ค่าของ plant เดิมเป็น input ที่ test กำหนด)
- `tools/v79office_tests.py` 17 กรณี (O01-O14 ฝั่งแอร์ / มิเตอร์, P01-P03 ป้องกันของ chiller ขยายและน้ำท่วม B1) — ผลใน `tests/v79office_tests.csv`
- `tools/check_v79_refs.py` ตรวจการอ้างจุดทุกจุดของ layer · CI รันทั้งหมดทุก push
- ยังต้องรัน `tools/rebuild_v79.sh` กับ source bog จริง (X/Y tests เดิม) และ commissioning บน Workbench

## 4. กราฟฟิก
| ส่วน | รายละเอียด |
|---|---|
| Blender | `tools/blender/equipment79.py` สร้าง chiller, pump, cooling tower, AHU, VAV, พัดลม แบบพารามิเตอร์ (ขนาดตามแบบ R9) → GLB ใน `graphics3d/models/` และภาพ Px (Cycles) ชื่อ/ขนาดเดิม |
| หน้า 3D | ห้องเครื่อง B1 (เลือก "B1 ห้องเครื่อง", พื้นดินโปร่ง), โมเดล Blender แทนรูปทรงเดิมของ chiller / pump / AHU, layer ห้อง (สีตาม temp / RH / CO2 + ป้าย), ท่อลมตาม service, VAV / หัวจ่าย / เซนเซอร์ / มิเตอร์, ลมไหลเฉพาะช่วงที่ station ยืนยัน airflow, ดับเบิลคลิกห้อง = ข้อมูลห้อง + VAV |
| Px live | `ALT_V79_VAV_Overview.px` + `ALT_V79_F02_VAV.px` … `F08` (สร้างโดย `tools/gen_px79o.py`) ผูกจุดจริงทุกค่า, ปุ่ม reset latch, ลิงก์จากหน้า R9 และ `ALT_V79_Plant.px` |

### ใช้ Claude ร่วมกับ Blender
1. ติดตั้ง Blender 4.x (หรือ `pip install bpy==4.5.0` บน Python 3.11)
2. แก้รูปทรง/วัสดุใน `tools/blender/equipment79.py` (แต่ละอุปกรณ์เป็นฟังก์ชัน, ตำแหน่งในพิกัดของหน้า 3D ผ่าน `V()`)
3. `python3.11 tools/blender/equipment79.py graphics3d/models --render station/shared/px/img` → GLB + ภาพ Px
4. `python3 graphics3d/rebuild_page.py` → หน้า 3D ใหม่ (CI ตรวจว่าตรงกับ source)
ชื่อ node (`comp`, `evap`, `panel`, `screen`, `beacon`, `motor`, `fanWheel` …) คือส่วนที่หน้า 3D ใช้ animate/แสดง alarm — ห้ามเปลี่ยนชื่อ

## 5. ข้อจำกัด
- แบบ R9 เป็น coordinated concept: ขนาดท่อ, ESP, หัวจ่าย, โครงสร้าง, อัคคีภัย, ค่าระบายอากาศตามตารางมาตรฐานฉบับที่ใช้จริง ต้องให้วิศวกรรับรองก่อนก่อสร้าง
- ภาพลมใน 3D เป็น visual (ตาม airflow ที่วัดได้) ไม่ใช่ CFD
- จุดใหม่ต้องผูก Field IO / protocol จริง (Field IO register จะได้จุดใหม่หลัง build) และทดสอบ P2P
- ขนาด station เพิ่มประมาณ 16,000 component (VAV / ห้อง / มิเตอร์) — ควรรันบน Supervisor หรือแบ่ง JACE ต่อชั้นตามจริง
- Tenant thermal billing ปิดไว้จนกว่าจะมี BTU meter แยกต่อ tenant
