# ALT_CP_Ref_V7_9 — เพิ่ม/ลดอุปกรณ์ได้ + อาคาร 8 ชั้น + 3D LIVE

ฉบับวันที่ 8 ต.ค. 2026 · ต่อจาก V7.8 r11 (logic เดิมไม่เปลี่ยน) · station ใหม่ชื่อ `ALT_CP_Ref_V7_9` (FoxS 4927) ไม่ทับ V7.8

## 1. สิ่งที่เพิ่มในรุ่นนี้

| เรื่อง | รายละเอียด |
| --- | --- |
| อุปกรณ์สูงสุด | chiller, CHP, CDP, CT อย่างละ 6 slot (01-02 = เครื่องเดิม V7.8, 03-06 = slot ขยาย) + sensor slot SNS01... |
| ลดอุปกรณ์ | ตั้ง `<slot>_Installed` = false (เช่น `CH02_Installed`) → เครื่องนั้นไม่ถูกเลือก ไม่ถูกสั่งเดิน ใน 3D เป็นเงาจาง |
| เพิ่มอุปกรณ์ | ตั้ง `<slot>_Installed` = true (เช่น `CH03_Installed`) → logic นับเครื่องนั้นทันที ไม่ต้องแก้โปรแกรม |
| Supervisor | `Expansion/Supervisor` ตัดสินว่าเครื่องขยายต้องเดินกี่เครื่อง: ชดเชยเครื่องเดิมที่หาย + เพิ่ม stage เมื่อโหลดสูง/CHWS สูง |
| ปั๊ม/หอ | จำนวน CHP / CDP / CT ที่เดิน = จำนวน chiller ที่ต้องการน้ำ (รวม post-run) — เครื่องเดิมก่อน แล้วจึง slot 03→06 |
| ข้ามเครื่องเสีย | slot ที่ fault / maintenance / start fail ถูกข้าม เครื่องถัดไปเดินแทนอัตโนมัติ |
| Field IO | ทุก slot มีกลุ่ม `FieldIO/<slot>` (UseField, Protocol, CommFault) และอยู่ในทะเบียน Field IO อัตโนมัติ |
| Air side | ชั้น 2-8 มี AHU_F02..F08 ชั้นละ 1 ชุด + 4 zone (temp/RH, out-of-service, ค่าเฉลี่ย, ห้องร้อนสุด, alarm) |
| WebService | เพิ่ม `Services/WebService` แบบ HTTPS (HTTP redirect ไป HTTPS) ใช้ certificate เดิมของ platform |
| 3D | อาคาร 8 ชั้น 64 x 40 ม. ห้องเครื่องชั้น 1, CT บนดาดฟ้า, air side ทุกชั้น, layer, เลือกชั้น, ระบบอนาคต |
| 2D / BIM | แบบ M-000..M-601, IFC4 และ BOQ สร้างจากแบบจำลองเดียวกัน |

## 2. ทะเบียนอุปกรณ์ `ALT_V79_Equipment_Register.xlsx`

ไฟล์เดียวที่บอกว่าไซต์มีอะไรบ้าง: sheet Equipment / Sensors / AirSide / Systems

- เพิ่ม/ลดแบบเร็ว (ไม่สร้างใหม่): สลับ `<slot>_Installed` ใน Workbench แล้วต่อ Field IO กลุ่มนั้น
- เพิ่ม/ลดแบบครบชุด: แก้ทะเบียน → `python3 make_v79.py <src.bog> <groups.tsv> config_new.bog --register ALT_V79_Equipment_Register.xlsx`
  → ได้ config.bog + ทะเบียนจุด (POINT_LIST, FIELD_IO, ALARM, HISTORY) → `gen3d79.py` สร้างหน้า 3D + point mapping ใหม่ → `gen2d79.py` / `genbim79.py` สร้างแบบ/BOQ
- ระบบในอนาคต (fire alarm, sprinkler, lighting, power): ใส่อุปกรณ์ใน sheet Systems (ชั้น, X/Y/Z, Point) → ขึ้นใน 3D layer "ระบบอื่น" พร้อมสถานะ

## 3. 3D กับ wire sheet (LIVE)

1. วาง `shared/web/ALT_V79_Building3D.html` และ `shared/px/ALT_V79_Building3D.px`
2. station ต้องมี WebService (มีแล้วใน V7.9) → เปิด `https://<host>/ord?file:^web/ALT_V79_Building3D.html` แล้ว login
3. หน้า 3D subscribe ทุกจุดผ่าน BajaScript: ค่าใน wire sheet เปลี่ยน → 3D เปลี่ยนทันที (รอบ ~1 วินาที)
   - เครื่องเดิน/หยุด, ความเร็ว, วาล์ว, น้ำไหล, สี zone ตามอุณหภูมิ, alarm, Installed (เงาจาง/ทึบ)
4. ปุ่ม **Point mapping** บอกจุดที่รับค่าแล้ว / ยังไม่ได้รับ
5. ใน Workbench: view `Px_Building3D_Live` บน ChillerPlant (ถ้า Workbench เปิดเป็นไฟล์ในเครื่อง หน้าจะขึ้น DEMO — ใช้ browser ตามข้อ 2)

## 4. ติดตั้ง station V7.9 (ไม่แตะ V7.8)

1. Workbench → Platform → Station Copier: copy `ALT_CP_Ref_V7_8` เป็นชื่อใหม่ `ALT_CP_Ref_V7_9` (ได้ไฟล์ Px เดิมใน `shared/px` ครบ)
2. stop station `ALT_CP_Ref_V7_9` → วาง `station/config.bog` ของโฟลเดอร์นี้ทับ `config.bog` **ของ V7_9 เท่านั้น**
3. วาง `station/shared/web/ALT_V79_Building3D.html` และ `station/shared/px/ALT_V79_Building3D.px` ลงโฟลเดอร์ shared ของ V7_9
4. start station → ต่อ Workbench ที่ FoxS **4927** → ตรวจ Services/WebService (HTTPS 443) ว่า Enabled และ port ไม่ชนกับ station อื่นที่เปิดอยู่
5. เปิด `https://localhost/ord?file:^web/ALT_V79_Building3D.html` → login → มุมบนต้องขึ้น **LIVE**

## 5. ผลทดสอบ offline

- V7.9 ใหม่ 16/16 PASS (X01-X11 เพิ่ม/ลดอุปกรณ์, Y01-Y05 air side ชั้น 2-8)
- ชุดเดิมรันซ้ำบน V7.9: v77 29/29 · r2 16/16 · r5 8/8 · r7 3/3 · r9 6/6 · v78 11/11 · r11 13/13 · v7 ผ่านทุกข้อที่รันเสร็จ (ไม่มี FINDING) — ผลอยู่ใน `tests/`
- 3D LIVE: ค่าจาก logic V7.9 (จำลอง) ส่งผ่าน BajaScript จำลอง → CH-02 ถอด (เงาจาง), CH-03 เดิน/วาล์ว 100 %, zone 31 °C เป็นสีแดง, วาล์ว AHU ชั้น 3 เปิดตาม — ไม่มี error

## 6. ข้อจำกัด / ต้องทำต่อ

- เครื่องขยาย (03-06) เดินตามลำดับ slot (03 ก่อน, ข้าม slot ที่ไม่พร้อม) — ยังไม่สลับเครื่องตามชั่วโมงเดิน
- เครื่องขยายใช้ logic แบบย่อ (request → valve → flow switch → start → proof) ยังไม่มี head-pressure / soft-load แบบเครื่องเดิม
- ยังไม่ได้ทดสอบบน Workbench/station จริง: ต้องตรวจ WebService เริ่มทำงาน (port 443 ชนกับ station อื่นหรือไม่) และ login ผ่าน browser
- แบบ 2D/3D เป็นแบบอ้างอิง ต้องออกแบบ/สำรวจยืนยันตามโครงการจริง
