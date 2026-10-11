# altPlant — โมดูล Java สำหรับ Niagara 4.15 (ALT Reference V7.9)

## มีอะไรบ้าง
| Component | ทำอะไร |
|---|---|
| **ExpansionSupervisor** | ตัดสินว่า chiller ช่อง 03-06 ต้องเดินเครื่องไหน — กฎเดียวกับบล็อก `CHX_*` ใน `ChillerPlant/Expansion/Supervisor` (`tools/v79_scale.py`) |
| **ZoneAggregator** | ค่าเฉลี่ย/สูงสุด และจำนวนโซนเกินเกณฑ์ ของ Temp / RH / CO2 (สูงสุด 16 โซนต่อชั้น) |

ตัวคำนวณอยู่ใน `com.alt.plant.logic` (Java ล้วน ไม่ใช้ jar ของ Niagara) และมี unit test ที่ CI รันทุก push (`logic-test/LogicTest.java`)

### ExpansionSupervisor — กฎ (ตรงกับ wire sheet)
- **deficit** = max(0, PlantStage − จำนวน chiller เดิมที่ healthy) → เครื่องขยายเข้าแทนเครื่องเดิมที่หาย/trip
- **stageAdd +1** เมื่อ PlantRunRequest, Stage2Request, เครื่องขยายที่ต้องการเดินครบ, (โหลดเฉลี่ย ≥ upLoadPct **หรือ** CHWS สูงกว่าเกณฑ์) และยังมี slot ว่าง ต่อเนื่อง `upDelay` (10 นาที)
- **stageAdd −1** เมื่อถ้าลดหนึ่งเครื่องแล้วโหลดเฉลี่ยยัง < downLoadPct, CHWS ปกติ ต่อเนื่อง `downDelay` (15 นาที)
- PlantRunRequest ปิด → stageAdd = 0 · ค่า stageAdd ถูกเก็บใน station จึงไม่หายตอน restart
- **ลำดับ slot**: เครื่องที่เดินอยู่ก่อนเสมอ (ไม่สลับกลางคัน) → ชั่วโมงเดินน้อยสุด (`rotateByRuntime`) → เลข slot
- **fail-safe**: PlantStage / โหลดเครื่องเดิม / โหลดของเครื่องขยายที่เดิน มีสถานะ fault → คงผลเดิม ไม่เพิ่ม/ลด และ `fault` = true

### การต่อลิงก์
| Slot | ลิงก์จาก |
|---|---|
| enable / plantPermissive | `CHX_Enable` / `PlantPermissive` |
| plantRunRequest / stage2Request / plantStage | `PlantRunRequest` / `Stage2Request` / `PlantStage` |
| base01Healthy / base02Healthy | `CH01TrainHealthy` / `CH02TrainHealthy` |
| base01PostRun / base02PostRun | `CH01PostRun` / `CH02PostRun` |
| baseRunCount / baseLoadSum | `CH_RunNum` / `ChillerLoadSum` |
| chwsHigh / chwsDownOk | `ChwsAboveStageUpLimit` / `Stg_DownChwsOk` |
| slotNNInstalled / Available / Running | `CHnn_Installed` / `CHnn_Avail` / `CHnnRunProof` |
| slotNNValveOpen / Load / Hours | `CHnn_ValveLogic` / `CHnnLoadPct` / `CHnn_RuntimeHours` |
| **out** run03..run06 | = `CHX_Req03..06` |
| **out** chillersNeedingWater | = `CHX_ChillersNeedingWater` (เป้าหมายปั๊ม/CT) |

### ZoneAggregator
อินพุตที่ไม่ได้ลิงก์จะมีสถานะ null และถูกข้าม ใช้บล็อกเดียวได้กับทุกขนาดชั้น
`zonesValid` = จำนวนโซนที่มีค่าใดค่าหนึ่งใช้ได้ · `tempValid` / `rhValid` / `co2Valid` = จำนวนค่าที่ใช้ได้แต่ละชนิด

## วิธี build
1. ตรวจเวอร์ชัน gradle plugin ใน `<niagara_home>\etc\m2\repository\com\tridium\` แล้วแก้ `niagaraGradlePluginVersion` ใน `gradle.properties` ให้ตรง
2. ถ้ายังไม่มี gradle wrapper: Workbench → **Tools › New Module** (ชื่อ `altPlant`, part `rt`) แล้วคัดลอก `gradlew`, `gradlew.bat`, `gradle/` จากโปรเจกต์ที่ wizard สร้างมาไว้ในโฟลเดอร์นี้
3. เปิด Command Prompt ของ Niagara (`<niagara_home>\bin\console.exe`) → `cd altPlant` → `gradlew build`
4. ได้ไฟล์ `build\libs\altPlant-rt.jar` → คัดลอกไป `<niagara_home>\modules\` → restart Workbench และ station
- `module-include.xml` ประกาศ types ไว้แล้ว ถ้า build แจ้งว่า type ซ้ำ (annotation processor ลงทะเบียนให้เอง) ให้ลบบล็อก `<types>`

## Code signing
Niagara 4.15 ตรวจลายเซ็นโมดูล — ให้เซ็นด้วยใบรับรองของบริษัทเอง (`niagara-signing` ใน gradle, ตั้งค่าใน `~/.tridium/signing/signing.properties` หรือ `gradle.properties`)
แล้วเพิ่มใบรับรองนั้นใน **Workbench › Certificate Management › User Trust Store** และของ platform
**ไม่ต้องลดระดับ module verification** ของ station

## ทดสอบ
- unit test (ไม่ต้องมี Niagara):
  ```
  cd logic-test
  javac -d out ../altPlant-rt/src/com/alt/plant/logic/*.java LogicTest.java && java -cp out LogicTest
  ```
- ตรวจ type ของ component โดยไม่มี jar ของ Tridium: `ci-stubs/` (ดู `.github/workflows/ci.yml`)
- บน station ทดสอบ: ลาก `ExpansionSupervisor` จาก palette `altPlant` ลงโฟลเดอร์ทดสอบ ลิงก์ตามตารางด้านบนขนานกับบล็อก `CHX_*` เดิม
  แล้วเทียบ run03..run06 กับ `CHX_Req03..06` อย่างน้อย 1-2 สัปดาห์ก่อนสลับใช้งานจริง
- action `execute` (hidden) คำนวณทันที, `scanRate` ตั้งรอบสแกน
