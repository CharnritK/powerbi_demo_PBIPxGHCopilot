# Pre-Flight Checklist (30 นาทีก่อนขึ้นเวที)

## Environment
- [ ] `.env` มีค่าครบ — `CLIENT_ID`, `CLIENT_SECRET`, `TENANT_ID`, `GROUP_ID`, `DATASET_ID`
- [ ] `AUTH_MODE=service_principal` (หรือ delegated ถ้าใช้ device code)
- [ ] Terminal: `cd` เข้า repo root แล้ว activate `.venv`
- [ ] ทดสอบ auth ด้วย `python scripts/cli/check_auth.py` — ได้ token

## VS Code / Jupyter
- [ ] เปิด tabs ตามลำดับ demo:
  1. `README.md`
  2. `docs/architecture/repo-architecture.md`
  3. `demo-enterprise/.../pbip/` folder
  4. `Fact Sales.tmdl`
  5. `relationships.tmdl`
  6. `notebooks/02_service_principal_demo.ipynb`
  7. `notebooks/03_measure_validation_showcase.ipynb`
  8. `tests/measure-validation/templates/measure_validation_template.csv`
  9. `test-results/` (latest run)
- [ ] Notebook kernel เลือก `.venv` ของ repo
- [ ] Font size ขยายสำหรับ projector (Ctrl+= x3-4 ครั้ง)
- [ ] ปิด notifications, Do Not Disturb mode

## Live Demo Smoke Test
- [ ] รัน cell แรกของ notebook 02 — imports สำเร็จ
- [ ] รัน cell auth — ได้ token
- [ ] รัน cell list workspaces — เห็น workspace
- [ ] ถ้าไม่ผ่าน: ใช้ `test-results/` เป็น fallback ได้ทันที

## Presentation
- [ ] PowerPoint deck เปิดอยู่ที่ slide 1
- [ ] Cheat sheet (`cheat_sheet_th.md`) เปิดบนมือถือหรือพิมพ์ออกมา
- [ ] Timer ตั้งไว้ 25 นาที (เหลือ 5 นาที buffer)
- [ ] น้ำดื่ม

## ถ้า Live Demo พัง
ไม่ต้องตกใจ — พูดว่า:
> "live environment เป็นส่วนที่เปราะที่สุด ไม่ใช่ตัว repo — ผมจะสลับไปใช้ผลลัพธ์ที่บันทึกไว้แทนครับ"

แล้วเปิด:
1. `test-results/demo-dataset/.../run_summary.json`
2. `test-results/demo-dataset/.../report/report_summary.md`
3. `tests/measure-validation/templates/measure_validation_template.csv`
