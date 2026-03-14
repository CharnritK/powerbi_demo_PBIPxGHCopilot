# Presenter Script by Time

อ้างอิง deck: `docs/presentation/community_meetup_deck_final_v7_th.md`  
เวอร์ชันนี้ออกแบบสำหรับ slot `30 นาที` โดยตั้งเป้าให้พูดเนื้อหาหลักจบใน `25:30-26:00` และเหลือ `4-4:30 นาที` สำหรับ buffer, reaction, หรือ Q&A สั้น

## Time Plan Summary

| เวลา | สไลด์ | เป้าหมายช่วง | Key message |
|---|---|---|---|
| 0:00-1:30 | 1 | เปิด session และตั้งโจทย์ | ปัญหาใหญ่ไม่ใช่ build ได้หรือไม่ แต่คือ trust ใน production |
| 1:30-3:30 | 2 | Reframe จาก AI hype ไปสู่ engineering | AI ทำให้เร็วขึ้น แต่ engineering ทำให้น่าเชื่อถือ |
| 3:30-5:30 | 3 | ปู foundation เรื่อง model-as-code | ถ้า asset ยัง inspect ไม่ได้ ก็ automate จริงจังไม่ได้ |
| 5:30-7:00 | 4 | ชี้ว่า model discipline คือ prerequisite | naming และ star schema ไม่ใช่ cosmetic แต่คือฐานของ automation |
| 7:00-9:30 | 5 | เปิด Pillar 2 ด้วย row-count guardrail | row count เป็น gate ที่เร็วและคุ้มค่าที่สุด |
| 9:30-11:30 | 6 | ยกระดับจาก structure ไปสู่ business outcome | measure validation บอกว่าผลลัพธ์ธุรกิจเปลี่ยนหรือไม่ |
| 11:30-14:00 | 7 | อธิบาย dimension-slice validation | grand total ปกติ ไม่ได้แปลว่าทุก slice ปกติ |
| 14:00-15:30 | 8 | วางกรอบเรื่อง expected deviation | exception ที่ดีต้องถูกบันทึก ไม่ใช่เงียบหาย |
| 15:30-18:00 | 9 | เปิด Pillar 3 เรื่อง Copilot/tooling | AI มีค่าตอนช่วย explain, refine, execute ตามมาตรฐานทีม |
| 18:00-19:30 | 10 | แสดง output ที่ทีมใช้ได้จริง | เป้าหมายคือ evidence ไม่ใช่คำพูดว่า “เช็กแล้ว” |
| 19:30-21:00 | 11 | สรุป pipeline และ operating model | หลาย interface ได้ แต่ logic ต้องชุดเดียวกัน |
| 21:00-22:30 | 12 | ปิดด้วย impact ระยะยาว | trust scale ได้เมื่อ knowledge และ template สะสม |
| 22:30-25:30 | 13 | สรุปภาพใหญ่และ call to action | AI จะปลอดภัยก็ต่อเมื่อ platform ถูกออกแบบมาดีพอ |
| 25:30-30:00 | Q&A | Buffer / audience questions | ใช้ตอบ doubt หลัก 2-3 ข้อและปิด session |

## Presenter Notes

### Slide 1 | 0:00-1:30

**เป้าหมาย:** เปิดให้คนฟังรู้ทันทีว่านี่ไม่ใช่ session เรื่อง AI ช่วยทำงานเร็วอย่างเดียว  
**Key message:** ใน enterprise BI คำถามสำคัญไม่ใช่ “ทำได้ไหม” แต่คือ “เชื่อถือได้ไหมตอนขึ้น production”

**Script**

สวัสดีครับ ขอบคุณทุกคนที่ยังอยู่ใน closing session วันนี้นะครับ

[หายใจ]

หัวข้อของผมคือ — ทำยังไงให้ Power BI ไม่ได้แค่สร้างได้เร็วขึ้น แต่ส่งขึ้น production ได้อย่างน่าเชื่อถือ

โจทย์มีประโยคเดียว:
**”ใน enterprise BI คำถามยากไม่ใช่ 'เราสร้างได้ไหม' แต่คือ 'เรากล้าเชื่อมันไหมตอนใช้ตัดสินใจจริง'”**

[pause — ให้ประโยคนี้ลงก่อน]

> ถ้าลืมทุกอย่าง พูดแค่: **”Trust in production สำคัญกว่า build speed”**

**ชวนคนฟัง:** “ใครเคยเจอบ้างครับ report ขึ้น production ไปแล้ว แต่ตัวเลขไม่ตรง?” [ยกมือ/พยักหน้า]

**Transition**

ถ้าตั้งโจทย์แบบนี้ เราจะเห็นทันทีว่า AI อย่างเดียวไม่พอ ต้องมี engineering discipline มารองรับ

### Slide 2 | 1:30-3:30

**เป้าหมาย:** Reframe เรื่อง AI จาก speed ไปสู่ trust  
**Key message:** AI ทำให้ build เร็วขึ้น แต่ engineering controls ทำให้ของที่ build นั้นไว้ใจได้

**Script**

เวลาพูดถึง AI กับ BI คนมักเริ่มจากเรื่องความเร็ว — สร้างไวขึ้น เขียนไวขึ้น

[หายใจ]

แต่ในโลก enterprise ปัญหาจริงคือ — KPI drift, TEST กับ PROD ค่อย ๆ ไม่เหมือนกัน, validation ยัง manual

session นี้ผมจะเล่าอยู่บน **3 เสา: version control, guardrails, และ custom toolbox**

และขอขีดเส้นใต้เลย — เราโฟกัส semantic model กับ deployment validation ไม่ใช่ full UI regression testing

> ถ้าลืมทุกอย่าง พูดแค่: **"3 เสา: version control, guardrails, custom toolbox"**

**Transition**

ถ้าจะทำทั้งสามเสานี้จริง จุดเริ่มต้นคือทำให้ model กลายเป็นของที่ review และ diff ได้

### Slide 3 | 3:30-5:30

**เป้าหมาย:** ปู foundation ของ Pillar 1  
**Key message:** ถ้าไม่มี model-as-code ก็ไม่มี automation ที่จริงจัง

**Script**

PBIP คือ project, PBIR คือ report definition, semantic model อยู่ในรูป metadata ที่ tools อ่านได้

[หายใจ]

พอทุกอย่างเป็น text-based — ทุกการเปลี่ยนกลายเป็น Git diff แทนที่จะซ่อนใน binary

reviewer ดู measure, relationship ผ่าน pull request ได้ — automation validate ก่อน deploy ได้จริง

> ถ้าลืมทุกอย่าง พูดแค่: **"PBIP ทำให้ Power BI กลายเป็น code ที่ diff ได้"**

**Transition**

แต่แค่เก็บใน Git ยังไม่พอ ถ้า model ไม่มีระเบียบ เครื่องมือก็ยังทำงานไม่ดี

### Slide 4 | 5:30-7:00

**เป้าหมาย:** ทำให้คนฟังเห็นว่า model discipline คือ prerequisite  
**Key message:** naming standards และ star schema คือฐานของ automation ไม่ใช่เรื่อง cosmetic

**Script**

หลายทีมอยากได้ automation — แต่ model ยังตั้งชื่อไม่สม่ำเสมอ schema ยังไม่ discipline

[หายใจ]

ผลคือทั้งคนและเครื่องมือเดายาก — อะไรคือ fact, อะไรคือ dimension, measure ไหนสำคัญ

Fact/Dim naming, shared calendar, grain ที่ชัด — พวกนี้ไม่ใช่เอกสารสวย ๆ แต่เป็นฐานของ automation

> ถ้าลืมทุกอย่าง พูดแค่: **"model ไม่มีระเบียบ = automation ไม่มีคุณภาพ"**

**เน้นเป็นพิเศษ**

- model quality กำหนด automation quality
- self-documenting model อ่านได้ทั้งคนและเครื่อง

**Transition**

เมื่อ foundation พร้อมแล้ว เราค่อยขึ้นมาที่เสาที่สอง ซึ่งเป็นหัวใจของความ trustworthy นั่นคือ guardrails

### Slide 5 | 7:00-9:30

**เป้าหมาย:** เปิด Pillar 2 ด้วยสิ่งที่จับต้องง่ายและคุ้มค่า  
**Key message:** row-count validation คือ deployment gate ที่เร็วที่สุดและได้ value สูงมาก

**Script**

guardrail แรกที่ผมแนะนำเสมอคือ row count ครับ

เทียบ COUNTROWS ระหว่าง TEST กับ PROD — tolerance เช่น บวกลบ 1%

[หายใจ]

มันเร็ว อธิบายง่าย จับ partial load, partition ผิด, environment drift ได้ดีมาก

**ชวนคนฟัง:** "ใครเคยเจอ TEST กับ PROD row count ต่างกันแบบไม่รู้ตัวบ้าง?" [ยกมือ]

แต่ต้องพูดตรง ๆ — row count ไม่ได้บอกว่า business logic ถูก มันบอกแค่ว่า volume เบี่ยงหรือไม่

> ถ้าลืมทุกอย่าง พูดแค่: **"row count = gate ที่เร็วและคุ้มค่าที่สุด"**

**เน้นเป็นพิเศษ**

- fastest high-value gate
- volume drift ไม่เท่ากับ business correctness
- ถ้า TEST กับ PROD ตั้งใจต่างกัน ต้องมี exception ที่ชัด

**Transition**

ถัดจาก volume parity คำถามที่ business สนใจกว่านั้นคือ แล้วผลลัพธ์ KPI ยังเหมือนเดิมไหม

### Slide 6 | 9:30-11:30

**เป้าหมาย:** พาคนฟังจาก structure check ไป outcome check  
**Key message:** schema check บอกว่า model เปลี่ยน ส่วน measure check บอกว่า business result เปลี่ยนหรือไม่

**Script**

ต่อให้ schema ยังอยู่ครบ — ถ้า KPI เปลี่ยน ผลกระทบถึงคนตัดสินใจทันที

[หายใจ]

เราต้องเทียบ measure value โดยตรง ไม่ใช่ดูแค่ว่า object ยังอยู่ไหม

เริ่มจาก grand total — tolerance กับตัวเลข, exact match กับ text

แต่ย้ำว่า TEST=PROD ไม่ได้แปลว่าถูก 100% — แปลว่า 2 environment สอดคล้องกัน

> ถ้าลืมทุกอย่าง พูดแค่: **"outcome check สำคัญกว่า schema check"**

**เน้นเป็นพิเศษ**

- compare DAX outcomes
- parity ไม่ใช่ UAT replacement
- outcome สำคัญกว่าแค่ object existence

**Transition**

อย่างไรก็ดี grand total อย่างเดียวอาจยังหลอกเราได้ เพราะปัญหาบางอย่างซ่อนอยู่ในบาง slice เท่านั้น

### Slide 7 | 11:30-14:00

> **ถ้าช้ากว่า 15:00:** ย่อ slide นี้เหลือ 1 นาที — พูดแค่ "grand total ปกติ ≠ ทุก slice ปกติ" แล้วข้ามไป Slide 8

**เป้าหมาย:** อธิบายว่าทำไมต้อง validate ตาม slice
**Key message:** grand total ปกติ ไม่ได้แปลว่า Year, Site, Product หรือ dimension สำคัญจะปกติทั้งหมด

**Script**

บางครั้ง total ดูปกติ — แต่พอแตกตามปี ตาม site เราเจอ drift ทันที

[หายใจ]

แนวคิดคือ auto-discover object แล้ว generate template ชุดแรก — ทีมค่อย refine ว่า measure ไหนสำคัญ

automation ช่วยทำ first draft ได้ แต่ final judgment ยังต้องอาศัยคนที่รู้ domain

> ถ้าลืมทุกอย่าง พูดแค่: **"grand total ปกติ ≠ ทุก slice ปกติ"**

**เน้นเป็นพิเศษ**

- dimension slicing proves business stability
- auto-discover เป็นจุดเริ่ม ไม่ใช่คำตัดสินสุดท้าย
- material slice ต้องมาจาก domain-owner review

**Transition**

พอเริ่ม validate ลึกขึ้น คำถามถัดไปที่ทุกคนถามแน่คือ ถ้าความต่างนั้นตั้งใจให้ต่างอยู่แล้วจะจัดการอย่างไร

### Slide 8 | 14:00-15:30

**เป้าหมาย:** วางกรอบเรื่อง exception handling  
**Key message:** expected deviation ต้องถูกเขียนให้ตรวจสอบได้ ไม่ใช่เก็บไว้ในความทรงจำคน

**Script**

ถ้า TEST กับ PROD ตั้งใจต่างกัน — ต้องแยกให้ชัดว่านี่คือ expected deviation ไม่ใช่ blind spot

[หายใจ]

policy ระยะยาว เช่น TEST ถือ subset — เขียนใน `deviation.yaml` พร้อม reason, owner, expiry

temporary exclusion ต้องไม่ค่อย ๆ กลายเป็น policy ลับ

> ถ้าลืมทุกอย่าง พูดแค่: **"exception ต้องเขียนไว้ ไม่ใช่จำไว้"**

**เน้นเป็นพิเศษ**

- persistent vs temporary
- auditable exceptions
- reason ต้องเป็น business reason ไม่ใช่ technical excuse

**Transition**

เมื่อ foundation และ guardrails พร้อมแล้ว คำถามคือ AI เข้ามาช่วยตรงไหนแบบที่มีประโยชน์จริง ไม่ใช่แค่คุยสวย ๆ

### Slide 9 | 15:30-18:00

**เป้าหมาย:** เปิด Pillar 3 ให้ชัดว่า AI มีบทบาทใน engineering workflow  
**Key message:** Copilot มีค่าตอนช่วย explain, refine, และ execute ภายใต้มาตรฐานของทีม

**Script**

Copilot ใน workflow นี้ไม่ได้มีไว้แค่ถามตอบ — มี 3 บทบาท:

[หายใจ — นับ 3 อย่างช้า ๆ]

**explain** — อธิบายว่า measure นี้มี risk ตรงไหน
**refine** — ปรับ template ให้ตรง business reality
**execute** — เรียก tool แล้วคืนผลแบบมีหลักฐาน

**ชวนคนฟัง:** "ใครเคยใช้ Copilot ช่วยงาน BI บ้างครับ?" [ยกมือ]

แต่ ownership ยังเป็นของทีม — AI ช่วยทำงานดีขึ้น ไม่ได้มาแทน approval

> ถ้าลืมทุกอย่าง พูดแค่: **"Copilot = explain + refine + execute, ownership ยังเป็นของทีม"**

**เน้นเป็นพิเศษ**

- AI for BI engineering, not only BI analysis
- explain / refine / execute
- tool quality และ context quality กำหนดคุณภาพของ Copilot

**Transition**

เมื่อ workflow ทำงานแล้ว สิ่งที่ทีมควรได้กลับมาไม่ใช่แค่คำว่า pass หรือ fail แต่ต้องเป็น artifact ที่เอาไป review ต่อได้จริง

### Slide 10 | 18:00-19:30

**เป้าหมาย:** ทำให้ภาพ output concrete  
**Key message:** เป้าหมายคือ evidence-based validation report ไม่ใช่การบอกปากเปล่าว่า “ผมเช็กแล้ว”

**Script**

สิ่งที่ทีมควรได้กลับมาคือ validation report — scope ชัด กติกาชัด ผลชัด ย้อนดูได้

[หายใจ]

แนบ pull request ได้ เก็บเป็น audit artifact ได้ ผูกกับ deployment gate ได้

> ถ้าลืมทุกอย่าง พูดแค่: **"evidence ไม่ใช่คำพูดว่าเช็กแล้ว"**

**เน้นเป็นพิเศษ**

- evidence over assertion
- reviewable artifact
- gate rule ต้องประกาศล่วงหน้า

**Transition**

ถัดไปคือภาพรวมการทำงานจากต้นน้ำถึงปลายน้ำ ว่าทั้งหมดนี้ประกอบกันเป็น pipeline แบบไหน

### Slide 11 | 19:30-21:00

**เป้าหมาย:** สรุป operating model  
**Key message:** ไม่ว่าจะเริ่มจาก chat, CLI, หรือ notebook สุดท้ายต้องวิ่งเข้า logic เดียวกัน

**Script**

จะเข้าทาง Chat, CLI, หรือ Notebook ก็ได้ — แต่ rule, tolerance, output ต้องเหมือนกัน

เปลี่ยน interface แล้วผล validation เปลี่ยนตาม = ไม่ได้

> ถ้าลืมทุกอย่าง พูดแค่: **"หลาย interface ได้ แต่ logic ชุดเดียว"**

**เน้นเป็นพิเศษ**

- one pipeline, multiple interfaces
- interface เปลี่ยนได้ แต่ logic ห้าม drift

**Transition**

ถ้าทำได้แบบนี้ value จะไม่ใช่แค่รอบนี้รอบเดียว แต่จะสะสมไปเรื่อย ๆ ในระดับทีม

### Slide 12 | 21:00-22:30

> **ถ้าช้ากว่า 22:00:** ข้าม slide นี้ ไปปิดที่ Slide 13 ทันที

**เป้าหมาย:** ปิดเรื่อง impact และการสะสมความเชื่อมั่น
**Key message:** template, standards, และ knowledge base ทำให้ trust scale ได้

**Script**

คุณค่าจริงไม่ใช่แค่เร็วขึ้นครั้งเดียว — แต่ validation cycle ถัดไปดีขึ้นเรื่อย ๆ

template reuse ได้ knowledge base โตขึ้น solved problems ไม่หายไปกับคนเก่งไม่กี่คน

> ถ้าลืมทุกอย่าง พูดแค่: **"shared knowledge แทน tribal knowledge"**

**เน้นเป็นพิเศษ**

- compounding confidence
- onboarding ง่ายขึ้น
- shared knowledge แทน tribal knowledge

**Transition**

สุดท้ายผมอยากปิดด้วยคำถามใหญ่ที่สุดของ session นี้

### Slide 13 | 22:30-25:30

**เป้าหมาย:** ปิด session ให้กลับไปที่โจทย์ใหญ่  
**Key message:** คำถามไม่ใช่ว่า AI ช่วย build ได้เร็วแค่ไหน แต่คือ platform ของเราถูกออกแบบมาดีพอให้ AI ทำงานอย่างปลอดภัยหรือยัง

**Script**

ผู้ใช้เห็น insights และ visuals — แต่สิ่งที่ทำให้น่าเชื่อถือคือ guardrails ข้างใต้

[หายใจ — ช้าลง เตรียมปิด]

**คำถามสำคัญไม่ใช่ว่า AI ช่วยสร้างเร็วแค่ไหน — แต่คือ platform เราดีพอให้ AI ทำงานปลอดภัยหรือยัง**

[pause]

ถ้าจะกลับไปทำต่อ — ผมแนะนำ 3 อย่าง:

1. เปิดใช้ model-as-code ให้จริง
2. เพิ่ม row-count และ measure validation ก่อน deployment
3. เอา logic ที่ดีที่สุดของทีมมาทำเป็น template ที่ reuse ได้

ขอบคุณครับ ยินดีรับคำถามต่อ [ยิ้ม + ผ่อนคลาย]

> ถ้าลืมทุกอย่าง จำแค่: **"platform ต้องดีพอ ก่อน AI จะช่วยได้ปลอดภัย"**

**เน้นเป็นพิเศษ**

- engineered platform before agentic operation
- 3 next steps ต้องพูดชัดและสั้น
- จบด้วย trust ไม่ใช่ novelty

## Q&A Buffer | 25:30-30:00

ถ้ามีเวลาเหลือ ให้รับคำถามโดยเริ่มจาก 3 เรื่องที่คนมักถามมากที่สุด

1. `Row count พิสูจน์ correctness ได้ไหม`
คำตอบสั้น: ไม่ได้ มันพิสูจน์ volume parity ไม่ใช่ business truth

2. `TEST กับ PROD match กัน แปลว่า KPI ถูกแล้วไหม`
คำตอบสั้น: ไม่ใช่ แปลว่า 2 environment สอดคล้องกัน แต่ยังต้องมี source reconciliation และ UAT

3. `Copilot แทน reviewer หรือ owner ได้ไหม`
คำตอบสั้น: ไม่ได้ Copilot ช่วย explain, refine, execute แต่ ownership และ approval ยังเป็นของทีม

## Speaking Reminders

- ถ้าต้องตัดเวลา ให้ตัดรายละเอียดใน Slide 7 และ Slide 12 ก่อน
- ถ้ามี room energy ดี ให้ขยายตัวอย่างใน Slide 5 หรือ Slide 9 แทนการเพิ่ม slide ใหม่
- อย่าใช้คำที่ทำให้คนเข้าใจว่า session นี้ครอบคลุม pixel-perfect UI regression testing
- ทุกครั้งที่พูดถึง AI ให้พากลับมาที่คำว่า `trust`, `control`, และ `evidence`
