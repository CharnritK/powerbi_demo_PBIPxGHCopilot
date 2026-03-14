# Cheat Sheet — 30 นาที

> ถ้าลืมทุกอย่าง พูด 3 อย่างนี้:
> 1. "Trust in production สำคัญกว่า build speed"
> 2. "PBIP ทำให้ Power BI กลายเป็น code ที่ review ได้"
> 3. "Guardrails ต้องมาก่อน deployment ไม่ใช่หลังมีคนร้องเรียน"

---

## Timeline + One-Liner + Action

| เวลา | Slide | พูดอะไร (1 บรรทัด) | ทำอะไร |
|-------|-------|---------------------|--------|
| 0:00 | 1 | "คำถามยากไม่ใช่สร้างได้ไหม แต่เชื่อถือได้ไหม" | เปิด deck |
| 1:30 | 2 | "AI เร็วขึ้น แต่ engineering ทำให้ไว้ใจได้" | — |
| 3:30 | 3 | "ถ้า inspect ไม่ได้ ก็ automate ไม่ได้" | — |
| 5:30 | 4 | "naming + star schema = ฐานของ automation" | — |
| 7:00 | 5 | "row count = gate ที่เร็วและคุ้มค่าที่สุด" | — |
| 9:30 | 6 | "schema check vs outcome check ต่างกัน" | — |
| 11:30 | 7 | "grand total ปกติ ≠ ทุก slice ปกติ" | *(ถ้าช้า: ย่อ slide นี้)* |
| 14:00 | 8 | "exception ต้องเขียนไว้ ไม่ใช่จำไว้" | — |
| 15:30 | 9 | "Copilot = explain + refine + execute" | — |
| 18:00 | 10 | "evidence ไม่ใช่คำพูดว่าเช็กแล้ว" | — |
| 19:30 | 11 | "หลาย interface ได้ แต่ logic ชุดเดียว" | — |
| 21:00 | 12 | "trust scale ได้เมื่อ template สะสม" | *(ถ้าช้า: ย่อ slide นี้)* |
| 22:30 | 13 | "platform ต้องดีพอให้ AI ทำงานปลอดภัย" | สรุป 3 next steps |
| 25:30 | Q&A | รับคำถาม 2-3 ข้อ | — |

---

## Time Check Points

- **7:00** — ถ้ายังไม่ถึง Slide 5: ย่อ Slide 3-4 ให้สั้นลง
- **15:00** — ถ้ายังไม่ถึง Slide 8: ข้าม Slide 7 detail, สรุปด้วยปาก
- **22:00** — ถ้ายังไม่ถึง Slide 13: ข้ามไป closing ทันที

---

## Recovery Phrases (ถ้าหลุด/ตื่นเต้น)

- "กลับมาที่ประเด็นหลัก..."
- "สิ่งสำคัญที่อยากให้จำกลับไปคือ..."
- "ถ้าสรุปสั้น ๆ คือ..."
- *(หายใจลึก แล้วอ่านบรรทัดถัดไปจาก cheat sheet)*

---

## Live Demo — ลำดับกด

1. เปิด `README.md` — "repo นี้คือ demo แบบ engineering"
2. โชว์ folder tree — "notebook คือผิว engineering อยู่ข้างใน"
3. เปิด `Fact Sales.tmdl` — "measure + hidden column ที่ review ได้ใน Git"
4. เปิด `relationships.tmdl` — "star schema จริง ไม่ใช่ placeholder"
5. **รัน notebook 02** — auth → workspaces → datasets
6. **รัน notebook 03** — validation template → execute → save results
7. เปิด `measure_validation_template.csv` — "validation อยู่ใน CSV ที่ review ได้"
8. เปิด `test-results/.../run_summary.json` — "หลักฐานที่ย้อนดูได้"

---

## ถ้า Demo พัง — Pivot Script

> "live environment เป็นส่วนที่เปราะที่สุด ไม่ใช่ตัว repo
> ผมจะสลับไปใช้ผลลัพธ์ที่บันทึกไว้แทนครับ"

เปิด `test-results/` → `run_summary.json` → `report_summary.md`
แล้วพูดต่อเรื่อง evidence-based validation ได้เลย

---

## Q&A — คำตอบสั้น

| คำถาม | ตอบ |
|--------|-----|
| Row count พิสูจน์ correctness ได้ไหม? | ไม่ได้ — พิสูจน์ volume parity เท่านั้น |
| TEST=PROD แปลว่า KPI ถูก? | ไม่ — แปลว่า 2 environment สอดคล้อง ต้องมี UAT ต่อ |
| Copilot แทน reviewer ได้ไหม? | ไม่ได้ — ช่วย explain/refine/execute แต่ ownership ยังเป็นของทีม |

---

## Closing (ท่องจำ)

> "คำถามไม่ใช่ว่า AI ช่วยสร้างเร็วแค่ไหน
> แต่คือ platform ของเราถูกออกแบบมาดีพอ
> ให้ AI เข้ามาช่วยได้อย่างปลอดภัยหรือยัง"
