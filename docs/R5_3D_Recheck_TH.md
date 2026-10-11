# ALT_CP_Ref_V7_9 r5 — 3D ใช้โมเดล Blender ครบทุกระบบ + ตรวจสอบซ้ำ (R9 water side / air side)

ฉบับ 11 ต.ค. 2026 · ต่อจาก r4 · branch `claude/focused-wright-jbl6he` (ยังไม่ merge เข้า `main`, ไม่ได้ deploy)

## 1. ไฟล์ที่ได้รับรอบนี้
ไฟล์ HTML 5 ไฟล์ (`ALT_V79_Building3D / AHU_AllAir / RentalFloor / Tenant_Metering / FloorBilling`) **เหมือนกับแพ็กเกจ R9
ที่นำเข้าใน r4 ทุก byte** — ข้อมูลระบบ water side / air side ของ R9 อยู่ใน `graphics3d/data/office79.json` และ `r9_model.json` แล้ว
รอบนี้จึงเติมส่วนที่หน้า 3D ของ r4 ยังไม่ได้แสดง และตรวจ logic กับจุดใน station ซ้ำทุกอุปกรณ์

## 2. สิ่งที่หน้า 3D ของ r4 ยังไม่แสดง (ยืนยันจากข้อมูล R9) → r5
| ข้อมูล R9 | จำนวน | r4 | r5 |
|---|---|---|---|
| เครื่องมือวัด / วาล์วบนท่อน้ำ (TT, PT, FM, BTU, MBFV, PICV) | 184 | ไม่แสดง | โมเดล Blender (instanced) + ไฟสถานะ + ค่าจริง |
| อุปกรณ์ AHU (VSD, SAT/RAT/MAT, filter/duct DP, OA airflow, OA/RA/relief damper) | 90 | ไม่แสดง | โมเดล Blender + ค่าจริง |
| MD (damper) | 168 | — | 123 ชุดเป็น damper ในกล่อง VAV (ผูก `VAV_*_DmpFb`) · 45 ชุด toilet / janitor exhaust แสดงเป็นโมเดล + logic ใหม่ |
| ท่อน้ำเย็นแยกชั้น riser → BTU meter → coil AHU | 24 เส้น | ไม่แสดง | ท่อหุ้มฉนวนตามสีบริการ + น้ำไหลเมื่อวาล์ว coil เปิด > 5 % |
| อุปกรณ์บนหลังคาตามแบบ (KEF, TEF, MAU, relief fan) | 4 | ไม่แสดง | โมเดล Blender (ไม่มีจุดใน station — แสดงว่าเป็นแบบ) |
| ช่องท่อ 5, ลิฟต์ 2, บันไดหนีไฟ 2, ประตูผู้เช่า 42 | — | ไม่แสดง | layer "ช่องท่อ / ลิฟต์ / บันไดหนีไฟ / ประตูผู้เช่า" |
| Cooling tower, OAU, พัดลม EF/CPEF/LSF/SEF, ถังขยายตัว ET-01, bypass DPB-01, ตู้ควบคุม CP-01 | 23 | รูปทรงพื้นฐาน (tower มี GLB แต่ไม่ได้ใช้) | โมเดล Blender ทั้งหมด (tower: แทนเฉพาะตัวถัง น้ำ/ใบพัด/ไอน้ำยังเคลื่อนไหวตามจริง) |

คลิกสองครั้งที่อุปกรณ์ → id, ประเภท, จุดใน station + slot path, ค่าปัจจุบัน, สถานะตามแบบ R9
ไฟสถานะ: เขียว = มีจุดและได้ค่า · ส้ม = มีจุดแต่ LIVE resolve ไม่ได้ · เทา = ไม่มีจุดใน station (แบบเท่านั้น)

## 3. โมเดล Blender ใหม่ (`tools/blender/equipment79.py`)
`oau` (OAU / MAU: หลังคากันฝน, hood + ตะแกรงนก), `roof_fan` (พัดลมหลังคาแบบโดม), `exptank` (ถัง diaphragm แดง),
`bypass` (ชุด DP bypass: globe valve + actuator + isolating valve + strainer), `panel` (ตู้ควบคุม 3 บาน, HMI, ไฟสถานะ)
และอุปกรณ์ภาคสนาม `dev_mbfv, dev_picv, dev_tt, dev_pt, dev_fm, dev_btu, dev_md, dev_vsd, dev_airtt, dev_airdp, dev_afms`
รวม GLB 21 ไฟล์ 1.8 MB · หน้า `ALT_V79_Building3D.html` 6.1 MB (R9 เดิม 6.3 MB)

## 4. การผูกจุด (`tools/r9_bindings.py` → `docs/R9_POINT_COVERAGE.csv`)
ผูกตามกฎชื่อ และยอมรับเฉพาะจุดที่มีอยู่จริงใน `registers/V7_COMPONENTS.csv` หรือ layer r4/r5 (CI ตรวจทุก push)
ผูกได้ **348 / 449** อุปกรณ์ · ใช้ค่า feedback ที่วัดจริงก่อนค่าคำสั่ง (VSD → `SpeedFb`, damper → `*DmpFb`, PICV → `PICVFb`)

อุปกรณ์ที่ **ไม่มีจุดใน station** (101) — ต้องตัดสินใจว่าจะเพิ่มจุดหรือไม่:
| กลุ่ม | จำนวน | ข้อสังเกต |
|---|---|---|
| TT ที่ท่อน้ำเข้า/ออก coil AHU / OAU / MAU | 22 | ใช้ทำ commissioning / M&V ของ coil — ไม่จำเป็นต่อการควบคุม |
| MBFV ตัดน้ำของ coil | 22 | ถ้าเป็น motorised ต้องมี DO + end switch |
| MBFV ตัดน้ำรายชั้น S/R | 16 | เช่นเดียวกัน |
| PT coil AHU (11) + PT evaporator / condenser ของ CH03-06 (16) | 27 | CH01/02 ผูกกับ `CHnn_EvapDP / CondDP` แล้ว |
| AHU-01/02 (V7.8): MAT, OA airflow, RA / relief damper | 8 | logic AHU01/02 ของ V7.8 มีแค่ OA damper — ถ้าใช้แบบ R9 mixed-air ต้องเพิ่ม |
| KEF, TEF, MAU, relief fan บนหลังคา + PICV / อุปกรณ์ของ MAU | 4 + อุปกรณ์ | ยังไม่มีจุดและ logic ใน station (MAU มี coil น้ำเย็น ต้องมี sequence) |

## 5. ตรวจ logic ซ้ำ (ยืนยันจากข้อมูล)
| ประเด็น | ผล |
|---|---|
| R9 MD-EA 45 ชุด (toilet / janitor exhaust) "exhaust schedule / interlock" ไม่มี logic ใน station | **แก้แล้ว** `v79_office.exhaust_damper`: เปิดตามตาราง `Sch_AHU` (ASHRAE 62.1 Table 6-4: toilet exhaust ขณะมีผู้ใช้), `TE_ForceOpen`, ปิดเมื่อ fire alarm ถ้า `TE_CloseOnFire` (ตามแผนอัคคีภัยของโครงการ), end switch ไม่ตาม 2 นาที → alarm · test O15 / O16 |
| อุปกรณ์ AHU ชั้น 2-8 ผูกค่าคำสั่งแทนค่าวัด | **แก้แล้ว** ผูก feedback (`SpeedFb, OADmpFb, RADmpFb, RelDmpFb, PICVFb`) |
| ตารางเครื่องมือวัด R9 ไม่มี TT ท่อน้ำเย็นออกจาก chiller (มีแค่ CHR / CDS / CDR) | **ข้อสังเกตต่อผู้ออกแบบ** — station ใช้ `CHnn_ChwSupplyTemp` ควบคุม LWT และ freeze trip ต้องมีในแบบ |
| MAU / KEF / TEF / relief fan ตามแบบ R9 | ยังไม่มี logic — ต้องได้ sequence จากผู้ออกแบบก่อน (MAU: SAT / dehumidification, relief: building pressure) |

## 6. เทียบกับ station ที่ deploy จริง (`station/ALT_CP_Ref_V7_9.zip` บน main, อ่านอย่างเดียว)
`python3 tools/check_baseline_zip.py <zip>` (ไม่แตกไฟล์ ไม่อ่าน Services / users)
- component ของ build เต็มใน repo (`V7_COMPONENTS.csv` 11,429) **ไม่มีใน baseline 617 ตัว**: Field IO 256 (`IO_*`, `IOS_*`), zone CO2 / zone 121,
  sensor ของ CH03-06 และ pump / tower 03-06, simulation 56 → baseline เป็น build ก่อน r2 ของ repo
- จุดที่หน้า 3D อ่าน 2,553 จุด: ไม่มีใน baseline 2,123 (ส่วนใหญ่เป็น layer r4/r5 ที่ยังไม่ได้ใส่ใน config.bog)
- file ORD ใน config.bog ครบทั้ง 29 ไฟล์
→ ถ้านำหน้า 3D ใหม่ไปใช้กับ baseline ปัจจุบัน ค่าส่วนใหญ่จะแสดง "resolve ไม่ได้" จนกว่าจะ build config.bog ใหม่ด้วย layer r2-r5

## 7. การทดสอบ (สภาพแวดล้อม CI / Linux, ไม่ใช่ Niagara จริง)
| รายการ | ผล |
|---|---|
| `v79office_tests.py` (layer test station) | PASS 19/19 (ใหม่ O15, O16) |
| `check_v79_refs.py` (+ Excel register) | PASS 0 findings |
| `check_px.py`, Px generated up to date | PASS |
| `office_points.py --check`, `r9_bindings.py --check`, `rebuild_page.py --check` | PASS |
| Java logic unit tests | PASS 19/19 |
| Browser (Chromium / SwiftShader) DEMO + LIVE mock: GLB ทุกชนิด, 319 อุปกรณ์, 24 ท่อ, 4 หน่วยหลังคา, ไม่มี JS error | PASS |
| Niagara 4.15 Workbench / station runtime / BajaScript จริง | NOT RUN |

## 8. ยังต้องทำ
1. นำ r3-r5 เข้า `main` ผ่าน branch ใหม่จาก main โดยคง Gradle config ของ main (`0ac8664`) — รอการอนุมัติ
2. Build config.bog ใหม่ด้วย layer r2-r5 จาก source bog จริง แล้วทดสอบบน TEST station (ไม่แตะ reference station)
3. ตัดสินใจจุดที่ยังไม่มี (ตารางข้อ 4) และ sequence ของ MAU / KEF / TEF / relief fan
4. ผู้ออกแบบยืนยัน TT ท่อน้ำเย็นออกจาก chiller ในตารางเครื่องมือวัด
