# altPlant — โมดูล Java สำหรับ Niagara 4.15 (ALT Reference V7.9)

## มีอะไรบ้าง
| Component | ทำอะไร | ต่อกับจุดไหนใน wire sheet V7.9 |
|---|---|---|
| **ExpansionSupervisor** | เพิ่ม/ลด chiller ช่อง 03-06 ตามโหลด (เหมือนบล็อก CHX_*) | in: PlantStage, CHX_AverageLoad, CHxx_Installed, CHxx available · out: run03..run06 → CHxx enable, chillersNeedingWater → เป้าหมายปั๊ม/CT |
| **ZoneAggregator** | ค่าเฉลี่ย/สูงสุด และจำนวนโซนเกินเกณฑ์ ของ Temp / RH / CO2 (สูงสุด 16 โซนต่อชั้น) | in: ZoneTemperatureAvg_xx, ZoneHumidityAvg_xx, ZoneCO2_xx · out: tempAvg, co2Max, zonesCo2High, anyAlarm |

อินพุตที่ไม่ได้ลิงก์จะมีสถานะ null และถูกข้าม ใช้บล็อกเดียวได้กับทุกขนาดชั้น

## วิธี build (แนะนำ)
1. Workbench → **Tools › New Module** → ชื่อ `altPlant`, part `rt` → ได้โปรเจกต์ gradle ตามเวอร์ชันเครื่องจริง
2. คัดลอก `altPlant-rt/src`, `module.palette`, `module.lexicon` ทับลงในโปรเจกต์ที่ wizard สร้าง
   (ไฟล์ `*.gradle.kts` ในโฟลเดอร์นี้เป็นตัวอย่าง ถ้าเวอร์ชัน plugin ไม่ตรง ให้ใช้ของ wizard)
3. เปิด Command Prompt ของ Niagara (`<niagara_home>\bin\console.exe`) → `cd altPlant` → `gradlew build`
4. ได้ไฟล์ `build\libs\altPlant-rt.jar` → คัดลอกไป `<niagara_home>\modules\` → restart Workbench และ station

## Code signing
Niagara 4.15 ตรวจลายเซ็นโมดูล — ให้เซ็นด้วยใบรับรองของบริษัทเอง (`niagara-signing` ใน gradle, ตั้งค่าใน `~/.tridium/signing/signing.properties` หรือ `gradle.properties`)
แล้วเพิ่มใบรับรองนั้นใน **Workbench › Certificate Management › User Trust Store** และของ platform
**ไม่ต้องลดระดับ module verification** ของ station

## ทดสอบ
- ลาก `ExpansionSupervisor` จาก palette `altPlant` ลงโฟลเดอร์ทดสอบ แล้วลิงก์ขนานกับบล็อก CHX_* เดิม เทียบผล run03..run06 ก่อนสลับใช้งานจริง
- action `execute` (hidden) คำนวณทันที, `scanRate` ตั้งรอบสแกน
