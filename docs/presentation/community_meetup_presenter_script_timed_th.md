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
หัวข้อของผมคือการทำให้ Power BI ไม่ได้แค่สร้างได้เร็วขึ้น แต่ส่งขึ้น production ได้อย่างน่าเชื่อถือมากขึ้น  
โจทย์ที่ผมอยากชวนคิดมีประโยคเดียว คือใน enterprise BI คำถามยากไม่ใช่ “เราสร้างได้ไหม” เพราะวันนี้ส่วนใหญ่เราสร้างได้อยู่แล้ว  
คำถามจริงคือ “เรากล้าเชื่อมันไหมตอนใช้ตัดสินใจจริง”

**เน้นเป็นพิเศษ**

- trust in production
- public-safe examples
- โฟกัสที่ semantic model และ deployment validation

**Transition**

ถ้าตั้งโจทย์แบบนี้ เราจะเห็นทันทีว่า AI อย่างเดียวไม่พอ ต้องมี engineering discipline มารองรับ

### Slide 2 | 1:30-3:30

**เป้าหมาย:** Reframe เรื่อง AI จาก speed ไปสู่ trust  
**Key message:** AI ทำให้ build เร็วขึ้น แต่ engineering controls ทำให้ของที่ build นั้นไว้ใจได้

**Script**

เวลาพูดถึง AI กับ BI คนมักเริ่มจากเรื่องความเร็ว สร้างไวขึ้น เขียนไวขึ้น วิเคราะห์ไวขึ้น  
แต่ในโลก enterprise ปัญหาที่เจอบ่อยคือ KPI drift, TEST กับ PROD ค่อย ๆ ไม่เหมือนกัน, validation ยัง manual และย้อนดูหลักฐานไม่ได้  
เพราะฉะนั้น session นี้ผมจะเล่าอยู่บน 3 เสา คือ version control, guardrails, และ custom toolbox  
และขอขีดเส้นใต้เลยว่า เราโฟกัส semantic model กับ deployment validation ไม่ได้อ้างว่ากำลังทำ full report-page UI regression testing

**เน้นเป็นพิเศษ**

- trust มาก่อน speed
- scope boundary ต้องพูดให้ชัด
- 3 pillars ต้องฝังในหัวคนฟังตั้งแต่ต้น

**Transition**

ถ้าจะทำทั้งสามเสานี้ให้เกิดขึ้นจริง จุดเริ่มต้นต้องเป็นการทำให้ model กลายเป็นของที่ review และ diff ได้

### Slide 3 | 3:30-5:30

**เป้าหมาย:** ปู foundation ของ Pillar 1  
**Key message:** ถ้าไม่มี model-as-code ก็ไม่มี automation ที่จริงจัง

**Script**

PBIP คือ project, PBIR คือ report definition, และ semantic model อยู่ในรูป metadata ที่ tools อ่านได้  
พอทุกอย่างกลายเป็น text-based artifact ทุกการเปลี่ยนจะกลายเป็น Git diff แทนที่จะซ่อนอยู่ใน binary  
นั่นหมายความว่า reviewer ดู measure, relationship, หรือ report structure ผ่าน pull request ได้  
และ automation ก็เริ่มค้นหา object, generate checks, หรือ validate ก่อน deploy ได้จริง

**เน้นเป็นพิเศษ**

- inspectable artifacts
- Git diff แทน hidden change
- model-as-code ไม่ได้พิสูจน์ correctness แต่ทำให้ validation เป็นไปได้

**Transition**

แต่แค่เอา model มาเก็บใน Git ยังไม่พอ ถ้าตัว model เองไม่มีระเบียบ เครื่องมือก็ยังทำงานได้ไม่ดี

### Slide 4 | 5:30-7:00

**เป้าหมาย:** ทำให้คนฟังเห็นว่า model discipline คือ prerequisite  
**Key message:** naming standards และ star schema คือฐานของ automation ไม่ใช่เรื่อง cosmetic

**Script**

หลายทีมอยากได้ automation แต่ model ยังตั้งชื่อไม่สม่ำเสมอ หรือ schema ยังไม่ discipline พอ  
ผลคือทั้ง reviewer และเครื่องมือเดายากเหมือนกัน ว่าอะไรคือ fact, อะไรคือ dimension, อะไรคือ measure สำคัญ  
เพราะฉะนั้น Fact/Dim naming, shared calendar, grain ที่ชัด, relationship ที่ตั้งใจออกแบบไว้ พวกนี้ไม่ใช่งานเอกสารสวย ๆ  
แต่มันคือสิ่งที่ทำให้ governance, review, และ validation แม่นขึ้น

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
เราเทียบ COUNTROWS ของตารางสำคัญระหว่าง TEST กับ PROD แล้วดูตาม tolerance ที่ทีมตกลงร่วมกัน เช่น บวกลบ 1%  
ข้อดีคือมันเร็ว อธิบายง่าย และจับปัญหาพื้นฐานได้ดีมาก เช่น partial load, partition ผิด, หรือ environment drift  
แต่ต้องพูดตรง ๆ ว่า row count ไม่ได้บอกว่า business logic ถูก มันบอกเพียงว่า data volume ที่ควรใกล้กัน ตอนนี้มันเบี่ยงหรือไม่

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

ต่อให้ schema ยังอยู่ครบ ถ้า KPI เปลี่ยน ผลกระทบจริงจะไปถึงคนตัดสินใจทันที  
เพราะฉะนั้นเราต้องเทียบ measure value โดยตรง ไม่ใช่ดูแค่ว่า object ยังอยู่ไหม  
เริ่มจาก grand total ก่อน ใช้ tolerance กับตัวเลข และ exact match กับ text  
แต่ผมอยากย้ำว่า TEST กับ PROD ให้ค่าตรงกัน ไม่ได้แปลว่า business truth ถูก 100% มันแปลว่า 2 environment นี้สอดคล้องกัน

**เน้นเป็นพิเศษ**

- compare DAX outcomes
- parity ไม่ใช่ UAT replacement
- outcome สำคัญกว่าแค่ object existence

**Transition**

อย่างไรก็ดี grand total อย่างเดียวอาจยังหลอกเราได้ เพราะปัญหาบางอย่างซ่อนอยู่ในบาง slice เท่านั้น

### Slide 7 | 11:30-14:00

**เป้าหมาย:** อธิบายว่าทำไมต้อง validate ตาม slice  
**Key message:** grand total ปกติ ไม่ได้แปลว่า Year, Site, Product หรือ dimension สำคัญจะปกติทั้งหมด

**Script**

นี่คือจุดที่หลายทีมเริ่มเห็น value จริง เพราะบางครั้ง total ดูปกติ แต่พอแตกตามปี ตาม site หรือตาม dimension สำคัญ เราเจอ drift ทันที  
แนวคิดคือให้ระบบ auto-discover object แล้ว generate template ชุดแรกออกมาเป็น YAML  
จากนั้นทีมค่อย refine ว่า measure ไหนสำคัญ dimension ไหนมี material business meaning และ filter ไหนควรใช้  
พูดอีกแบบคือ automation ช่วยเราทำ first draft ได้ แต่ final judgment ยังต้องอาศัยคนที่รู้ domain จริง

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

ถ้า TEST กับ PROD ตั้งใจต่างกัน เราต้องแยกให้ชัดว่าอันนี้คือ expected deviation ไม่ใช่ blind spot  
กรณีที่เป็น policy ระยะยาว เช่น TEST ถือ subset ของข้อมูล ควรเขียนไว้ใน `deviation.yaml` พร้อม reason, owner, และ expiry  
ถ้าเป็นแค่ debug run ชั่วคราว เช่น เพิ่ง partial refresh มา จะใช้ single-run exclusion ได้  
ประเด็นคือ temporary exclusion ต้องไม่ค่อย ๆ กลายเป็น policy ลับที่ไม่มีใครตรวจสอบ

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

ผมอยาก reposition Copilot ให้ต่างจากภาพจำทั่วไปนิดหนึ่ง คือไม่ได้มีไว้แค่ถามตอบหรือช่วยเขียน prose  
ใน workflow นี้มันมี 3 บทบาท คือ explain, refine, และ execute  
explain คือช่วยอธิบายว่า measure นี้ meaningful ภายใต้ context ไหน มี risk ตรงไหน  
refine คือช่วยปรับ template ให้ตรงกับ business reality มากขึ้น  
execute คือเรียกใช้ tool ผ่าน MCP หรือ interface ที่ทีมกำหนด แล้วคืนผลแบบมีหลักฐานกลับมา  
แต่ ownership ยังเป็นของทีมเสมอ AI ช่วยให้ทำงานดีขึ้น ไม่ได้มาแทน approval process

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

สิ่งที่ทีมควรได้กลับมาคือ validation report ที่บอก scope ชัด กติกาชัด ผลชัด และย้อนกลับไปดูได้  
report แบบนี้เอาไปแนบ pull request, เก็บเป็น audit artifact, หรือใช้ root-cause analysis ต่อได้  
และที่สำคัญ มันสามารถผูกกับ deployment gate ได้ ว่าถ้ายังมี critical failure อยู่ deployment จะไม่ผ่าน

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

slide นี้เอาไว้ย้ำ operating model ครับ  
user จะเข้ามาทาง Copilot Chat, CLI, หรือ Notebook ก็ได้ แต่ comparison rule, tolerance policy, และ output format ต้องเหมือนกัน  
เราไม่ต้องการให้เปลี่ยน interface แล้วผล validation เปลี่ยนตาม  
ดังนั้นหลาย entry point ทำได้ แต่ control model ต้องเป็นชุดเดียว

**เน้นเป็นพิเศษ**

- one pipeline, multiple interfaces
- interface เปลี่ยนได้ แต่ logic ห้าม drift

**Transition**

ถ้าทำได้แบบนี้ value จะไม่ใช่แค่รอบนี้รอบเดียว แต่จะสะสมไปเรื่อย ๆ ในระดับทีม

### Slide 12 | 21:00-22:30

**เป้าหมาย:** ปิดเรื่อง impact และการสะสมความเชื่อมั่น  
**Key message:** template, standards, และ knowledge base ทำให้ trust scale ได้

**Script**

คุณค่าจริงของระบบแบบนี้ไม่ใช่แค่ทำให้เร็วขึ้นครั้งเดียว  
แต่มันทำให้ validation cycle ถัดไปดีขึ้นเรื่อย ๆ เพราะ template reuse ได้ knowledge base โตขึ้น และ solved problems ไม่หายไปกับคนเก่งไม่กี่คน  
จากเดิมที่ทีมพึ่ง tribal knowledge เราจะค่อย ๆ เปลี่ยนเป็น shared patterns และ shared standards  
ตัวเลข before/after บนสไลด์นี้ให้มองเป็น representative outcome ไม่ใช่สัญญาว่าทุกทีมจะได้เท่ากัน

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

สิ่งที่ผู้ใช้เห็นคือ insights และ visuals แต่สิ่งที่ทำให้มันน่าเชื่อถือคือชั้น guardrails และ foundation ด้าน model-as-code กับ custom toolbox  
เพราะฉะนั้น เวลาพูดถึง AI ในงาน BI ผมคิดว่าคำถามไม่ใช่แค่ว่า AI ช่วยเราสร้างเร็วขึ้นไหม  
แต่คือ platform ของเราถูกออกแบบมาดีพอหรือยัง ที่จะให้ AI เข้ามาช่วยงานได้อย่างปลอดภัย ตรวจสอบได้ และไม่สร้างความเสี่ยงเพิ่ม  
ถ้าจะกลับไปทำต่อหลัง session นี้ ผมแนะนำ 3 อย่าง  
หนึ่ง เปิดใช้ model-as-code ใน workflow ให้จริง  
สอง เพิ่ม row-count และ measure validation ก่อน deployment  
สาม เอา logic ที่ดีที่สุดของทีมมาทำเป็น template และ tool ที่ reuse ได้  
ขอบคุณครับ และยินดีรับคำถามต่อ

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
