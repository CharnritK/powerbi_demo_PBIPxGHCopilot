# Enterprise BI Engineering: Building Trustworthy Power BI with PBIP/PBIR, GitHub Copilot & AI

**30-Minute Closing Session — Power Platform Bootcamp Thailand (Final Content / v7)**

> Public-safe version.  
> All identifiers remain placeholders:  
> `<WORKSPACE>`, `<DATASET>`, `<TABLE>`, `<COLUMN>`, `<METRIC>`
>
> **Session scope:** This talk focuses on **semantic model + deployment validation**.  
> It does **not** cover report-page UI regression testing.

---

## Slide 1 — Title

**Enterprise BI Engineering: Building Trustworthy Power BI with PBIP/PBIR, GitHub Copilot & AI**

Subtitle: Version Control, Validation Guardrails, and AI-Assisted Tooling for Trustworthy Power BI

Event: Power Platform Bootcamp Thailand  
Speaker: Charnrit Khongthanarat · Vis & Interaction Science Consultant, Accenture  
Date: March 14, 2026 · AreaX, 4th Fl., Siam Paragon  
LinkedIn: www.linkedin.com/in/charnrit-khongthanarat

**On-slide callout:**
- Focus: enterprise trust, not only speed
- Public-safe examples only

**Speaker Script (TH):**
> สวัสดีครับ ขอบคุณทุกคนที่ยังอยู่ในเซสชันสุดท้ายของวันนี้นะครับ  
> ผมชื่อชานฤทธิ์ ทำงานด้าน Power BI และ Enterprise BI Engineering เป็นหลัก ทั้งเรื่อง semantic model, CI/CD, validation และ governance  
> วันนี้ผมอยากชวนทุกคนมองอีกชั้นหนึ่งของ Power BI ครับ ไม่ใช่แค่สร้างรายงานให้สวยหรือใช้ AI ให้เร็วขึ้น แต่ทำอย่างไรให้ระบบ BI ของเรา “เชื่อถือได้” ตอนขึ้น production  
> แกนของเซสชันนี้มี 3 เรื่อง คือ version control, validation guardrails และ custom toolbox ที่ใช้ GitHub Copilot ร่วมกับ workflow ของทีม  
> ทุกตัวอย่างในสไลด์นี้เป็นข้อมูลที่ sanitize แล้ว ไม่มีชื่อลูกค้า ไม่มีชื่อ dataset จริงครับ

---

## Slide 2 — The Shift

**AI Makes BI Faster. Engineering Makes BI Trustworthy.**

In enterprise BI, the hardest question is not **“Can we build it?”**  
It is **“Can we trust it in production?”**

**What goes wrong without engineering controls:**
- KPI drift reaches decision-makers before anyone notices
- TEST and PROD diverge after refreshes, schema changes, or relationship changes
- Validation is manual, inconsistent, and undocumented
- Teams can explain how they built a release, but not how they proved it was safe

**Scope of this session:**
- Semantic model + deployment validation
- Not report-page UI regression testing

**Three Pillars:**
1. **Version Control** — model and report definitions stored as text
2. **Guardrails** — automated validation before deployment
3. **Custom Toolbox** — Copilot + MCP + reusable templates + knowledge base

**Takeaway:** Trust in enterprise BI comes from repeatable engineering controls.

**Speaker Script (TH):**
> ถ้าเราพูดถึง AI กับ Power BI ส่วนใหญ่เราจะพูดถึงเรื่องความเร็วครับ สร้างได้ไวขึ้น เขียนได้ไวขึ้น วิเคราะห์ได้ไวขึ้น  
> แต่ในมุม enterprise คำถามที่ยากกว่าคือ “แล้วเราเชื่อมันได้หรือยังตอนขึ้น production”  
> ปัญหาที่ทีมเจอกันบ่อยคือ KPI drift โดยไม่มีใครรู้, TEST กับ PROD ค่อย ๆ ไม่เหมือนกันหลัง refresh หรือหลังมีการแก้ schema, และสุดท้าย validation ยังเป็นงาน manual ที่ไม่มีหลักฐานชัดเจน  
> เพราะฉะนั้นวันนี้ผมจะวางเรื่องนี้บน 3 เสา คือ version control, guardrails, และ custom toolbox  
> และขอระบุ scope ชัด ๆ เลยว่า เราโฟกัสที่ semantic model และ deployment validation ไม่ใช่การทดสอบ UI ของ report page ครับ

---

## Slide 3 — Pillar 1: Model as Code

**PBIP Project + PBIR Report + TMDL Semantic Model**

```text
Project/
├── <DATASET>.pbip
├── <DATASET>.Report/
│   └── definition/         # PBIR files for pages, visuals, bookmarks
└── <DATASET>.SemanticModel/
    └── definition/         # TMDL / model metadata as text
```

**Why this matters:**
- Every change becomes a Git diff instead of a hidden binary change
- Pull requests can review measures, relationships, and report structure
- Automation can discover measures and dimensions from source files
- CI/CD can validate before deployment instead of after a complaint

**Prerequisites:**
- Power BI Project workflow enabled in your team
- Git repo and pull-request discipline
- PBIP/PBIR/TMDL files committed to source control

**Limitations / boundaries:**
- Model-as-code improves reviewability; it does not prove data correctness by itself
- Report UI behavior still needs separate testing if that matters

**Takeaway:** No model-as-code, no serious automation.

**Speaker Script (TH):**
> จุดเริ่มต้นของ automation ที่จริงจังคือ model-as-code ครับ  
> ตรงนี้ผมอยากใช้คำให้แม่นนิดหนึ่ง: PBIP คือ project, PBIR คือ report definition, และ semantic model จะอยู่ในโครงสร้างแบบ text เช่น TMDL  
> สิ่งที่ได้คือทุกการเปลี่ยนแปลงกลายเป็น Git diff เรารีวิว measure, relationship หรือ report structure ผ่าน pull request ได้  
> นี่สำคัญมาก เพราะถ้า model ยังเป็นกล่องดำหรือเป็น binary file อย่างเดียว เราแทบจะ automate ได้ไม่จริง  
> แต่ต้องบอกขอบเขตด้วยว่า model-as-code ช่วยเรื่อง reviewability และ automation readiness นะครับ มันยังไม่ได้พิสูจน์ว่า data ถูกต้อง จนกว่าเราจะมี validation layer ต่อจากนี้

---

## Slide 4 — Enterprise Model Discipline

**Naming Standards + Star Schema = Reliable Automation**

**Naming standards**

| Convention | Example |
|-----------|---------|
| Fact/Dim prefixes | `FactProductionOutput`, `DimCalendar` |
| Business-friendly measure names | `Total Output`, `%Efficiency` |
| `_` prefix for helper measures | `_BaseFilter`, `_HoursRaw` |
| Display folders by domain | Production / Quality / Finance |
| Descriptions on key tables and columns | Self-documenting model |

**Star schema discipline**
- Facts at clear grain: “one row per ___”
- Shared `DimCalendar` for time slicing
- Single-direction filters from dimension to fact
- Measures preferred over calculated columns where possible
- Relationship intent documented, especially role-playing dates

**Prerequisites:**
- Common modeling standards across the team
- Ownership of naming conventions and business definitions

**Limitations / boundaries:**
- Automation quality depends on model quality
- Inconsistent naming or snowflake-heavy design reduces tool accuracy

**Takeaway:** Well-structured models are easier to govern, review, and validate.

**Speaker Script (TH):**
> หลายทีมอยากได้ automation แต่ model ยังตั้งชื่อไม่สม่ำเสมอ หรือ schema ยังไม่ discipline พอ  
> ถ้าเป็นแบบนั้น เครื่องมือจะเดายาก และ reviewer ก็อ่านยากเหมือนกัน  
> เพราะฉะนั้น naming standard กับ star schema ไม่ใช่เรื่อง cosmetic ครับ แต่มันคือ prerequisite ของ automation  
> ถ้าเราใช้ Fact/Dim ชัดเจน, มี shared calendar, ระบุ grain, และใช้ measure แทน calculated column เท่าที่ควร เครื่องมือจะค้นหา, จัดกลุ่ม, และสร้าง template ได้แม่นขึ้นมาก  
> พูดง่าย ๆ คือ model ที่ self-documenting จะทั้งคนอ่านรู้เรื่อง และ machine ก็อ่านรู้เรื่องด้วยครับ

---

## Slide 5 — Pillar 2: Guardrails — Row Count Validation

**COUNTROWS Across TEST vs PROD — Automated**

```python
EVALUATE UNION(
  ROW("tbl","Fact<TABLE>","cnt",COUNTROWS('Fact<TABLE>')),
  ROW("tbl","Dim<TABLE>","cnt",COUNTROWS('Dim<TABLE>')),
  ROW("tbl","DimCalendar","cnt",COUNTROWS('DimCalendar'))
)
# Run on TEST and PROD
# Compare with tolerance, e.g. ±1%
# Batch tables to stay inside query limits
```

**Example output**

| Status | Table | TEST | PROD | Diff | Note |
|--------|-------|------|------|------|------|
| ✅ PASS | Fact\<TABLE\> | 1,245,302 | 1,245,302 | 0.00% | |
| ✅ PASS | Fact\<TABLE-B\> | 89,421 | 89,421 | 0.00% | |
| ❌ FAIL | Fact\<TABLE-C\> | 12,847 | 13,201 | -2.68% | Exceeds tolerance |
| ✅ PASS | DimCalendar | 3,652 | 3,652 | 0.00% | |
| ⏭️ SKIP | Dim\<TABLE\>_v2 | | | | Duplicate variant |

**Prerequisites:**
- Comparable TEST and PROD datasets
- Query execution path enabled in your platform
- Defined tolerance policy and table-selection rules

**Limitations / boundaries:**
- Row counts detect volume drift, not business-logic correctness
- Datasets with intentional differences need documented exceptions
- Large models may need batching for performance and API/query limits

**Takeaway:** Row-count checks are the fastest high-value deployment gate.

**Speaker Script (TH):**
> Guardrail แรกที่คุ้มมากคือ row count ครับ  
> เรารัน COUNTROWS กับตารางสำคัญใน TEST และ PROD แล้วเทียบกันด้วย tolerance ที่ตกลงร่วมกัน เช่น ±1%  
> ข้อดีคือมันเร็ว อธิบายง่าย และจับปัญหาพื้นฐานที่เจอบ่อยมาก เช่น load ไม่ครบ, partition ผิด, หรือ environment drift  
> แต่ผมอยากให้มองอย่างแม่นนะครับ row count ไม่ได้บอกว่าธุรกิจ logic ถูก มันบอกว่า “ปริมาณข้อมูลที่ควรจะเหมือนกัน ตอนนี้มันไม่เหมือน”  
> ถ้า TEST กับ PROD ตั้งใจให้ต่างกันอยู่แล้ว เราต้อง declare exception ให้ชัด ไม่งั้นผล validation จะกลายเป็น noise ครับ

---

## Slide 6 — Measure Value Validation

**Compare DAX Outcomes, Not Just Model Structure**

```python
EVALUATE UNION(
  ROW("measure","<METRIC-A>","value",[<METRIC-A>]),
  ROW("measure","<METRIC-B>","value",[<METRIC-B>]),
  ROW("measure","<METRIC-C>","value",[<METRIC-C>])
)
# Grand-total comparison first
# Numeric results use tolerance
# Text results use exact match
```

**Example output**

| Status | Measure | TEST | PROD | Diff | Note |
|--------|---------|------|------|------|------|
| ✅ PASS | \<METRIC-A\> | 45,231 | 45,231 | 0.00% | |
| ✅ PASS | \<METRIC-B\> | 87.34% | 87.34% | 0.00% | |
| ❌ FAIL | \<METRIC-C\> | 2,104.5 | 2,167.8 | -2.92% | Exceeds tolerance |
| ✅ PASS | \<METRIC-D\> | 1,890.2 | 1,890.2 | 0.00% | |
| ⏭️ SKIP | [Internal] | | | | Both NULL |

**Prerequisites:**
- Ability to execute DAX queries against the model
- Selected measure set or measure-discovery source
- Agreed comparison tolerance and null-handling rules

**Limitations / boundaries:**
- Grand totals can hide slice-specific problems
- Parity between TEST and PROD does not replace source reconciliation or business UAT
- Non-deterministic or time-sensitive measures need careful handling

**Takeaway:** Schema checks tell you the model changed. Measure checks tell you whether the business result changed.

**Speaker Script (TH):**
> ถัดมาคือ validation ที่ business รู้สึกจริงที่สุด คือการเทียบค่า measure ครับ  
> เพราะต่อให้ schema ไม่พัง แต่ถ้า KPI เปลี่ยน ผลกระทบจริงจะไปถึงคนตัดสินใจทันที  
> เราจึงต้องดู outcome ของ DAX โดยตรง ไม่ใช่ดูแค่ว่า object ยังอยู่ครบไหม  
> แต่ก็มี boundary ที่ต้องพูดให้ชัด คือถ้า TEST กับ PROD ให้ผลเท่ากัน ไม่ได้แปลว่า business truth ถูก 100% มันแปลว่า 2 environment นี้สอดคล้องกัน  
> ดังนั้นผมมองสิ่งนี้เป็น deployment guardrail ไม่ใช่ตัวแทนของ UAT หรือ source reconciliation ครับ

---

## Slide 7 — Template-Driven Testing

**Auto-Discover → Generate YAML → Compare by Dimension Slice**

**Validation template**

```yaml
dataset: <DATASET>
tolerance_pct: 1.0

measures:
  - name: <METRIC-A>
    selected: true
    category: output
  - name: <METRIC-B>
    selected: true
    category: efficiency

dimensions:
  - table: DimCalendar
    column: CalendarYear
    selected: true
    cardinality: 5

filters:
  - table: DimCalendar
    column: CalendarYear
    operator: IN
    values: ['2025', '2026']
```

**Execution pattern**

```dax
EVALUATE
SUMMARIZECOLUMNS(
  DimCalendar[CalendarYear],
  Dim<TABLE>[<COLUMN>],
  TREATAS({"2025","2026"}, DimCalendar[CalendarYear]),
  "<METRIC-A>", [<METRIC-A>],
  "<METRIC-B>", [<METRIC-B>]
)
```

**What this catches**
- Grand total looks fine, but one site or one year is off
- A measure only breaks under specific filter context
- A business rule changed in one slice but not the overall total

**Prerequisites:**
- Discovery source for measures/dimensions
- Curated dimension list with reasonable cardinality
- Domain-owner review of what is material

**Limitations / boundaries:**
- Auto-selection is a starting point, not final judgment
- Too many high-cardinality slices can make validation slow or noisy
- Template quality depends on model semantics and domain knowledge

**Takeaway:** Grand totals prove surface stability. Dimension slicing proves business stability.

**Speaker Script (TH):**
> จุดที่หลายทีมเริ่มเห็น value จริง ๆ คือ slide นี้ครับ  
> เพราะบางครั้ง grand total ดูปกติ แต่พอแตกตามปี ตาม site หรือ dimension สำคัญบางตัว เราจะเจอ drift ที่ซ่อนอยู่  
> Template ทำให้กระบวนการนี้ reuse ได้ เราไม่ต้องเขียน query ใหม่ทุก release  
> ระบบสามารถ auto-discover แล้ว generate first draft ให้ได้ แต่ผมไม่อยากให้ตีความว่าเป็น blind automation นะครับ  
> คนที่รู้ business จริงยังต้องช่วยตัดสินว่า measure ไหนสำคัญ dimension ไหนเป็น material slice และ filter ไหนควรใช้เพื่อให้การทดสอบ meaningful

---

## Slide 8 — Expected Deviations

**Documented Exceptions, Not Silent Blind Spots**

**Persistent baseline override**

```yaml
# deviation.yaml
row_counts:
  Fact<TABLE>:
    expected_diff_pct: 5.0
    reason: TEST holds a daily subset only
    approved_by: <OWNER>
    expires: 2026-06-01

measures:
  <METRIC-A>:
    expected_diff_pct: 3.0
    reason: TEST contains only 9 months of history
```

**Single-run temporary exclusion**

```text
User: "Validate <DATASET>, but skip Fact<TABLE> row counts
       — I just loaded a partial refresh"

Copilot: "Skipping Fact<TABLE> for this run only.
          Remaining checks continue."
```

**Use the right mechanism**
- **Persistent + auditable** → `deviation.yaml`
- **Temporary + ad hoc** → single-run exclusion
- **CI/CD path** → persistent only
- **Debug path** → temporary is acceptable

**Prerequisites:**
- Named owners for exception approval
- Review cadence and expiry policy
- Clear distinction between debug runs and production gates

**Limitations / boundaries:**
- Too many deviations reduce trust in the gate
- Temporary exclusions should not become permanent hidden policy
- Exceptions must explain business reason, not just technical inconvenience

**Takeaway:** Validation is only useful when expected differences are codified.

**Speaker Script (TH):**
> คำถามที่คนมักถามต่อคือ แล้วถ้า TEST กับ PROD ตั้งใจให้ต่างกันล่ะ จะทำอย่างไร  
> คำตอบคือเราต้องแยก “exception ที่ตั้งใจและอธิบายได้” ออกจาก “blind spot ที่ไม่มีใครรู้”  
> ถ้าเป็นความต่างที่ควรอยู่ระยะยาว เช่น TEST มีข้อมูลแค่ subset เราควรเก็บไว้ใน deviation.yaml พร้อม owner, reason และ expiry  
> แต่ถ้าเป็นแค่รัน debug ชั่วคราว เช่นเพิ่ง partial refresh มา เราอาจใช้ single-run exclusion ได้  
> ประเด็นสำคัญคือ temporary exclusion ต้องไม่กลายเป็น policy ลับที่ไม่มีใครตรวจสอบครับ

---

## Slide 9 — Pillar 3: Custom Toolbox with Copilot

**AI for BI Engineering, Not Just BI Analysis**

**Three Copilot modes**
1. **Explain** — clarify measure logic, context, and risks
2. **Refine** — improve template selections, filters, and slices
3. **Execute** — call MCP tools and return structured evidence

**Use Case 1 — Review the template**
```text
"Are the right measures selected?"
→ Missing: <METRIC-F>
→ Add Dim<TABLE-B> for slicing
→ Narrow to recent periods
```

**Use Case 2 — Explain measure context**
```text
"What context does <METRIC-B> need?"
→ Needs Year + Site context
→ Exclude divide-by-zero cases
→ Recommend Year × <COLUMN>
```

**Use Case 3 — Execute the workflow**
```text
"Validate <DATASET>"
→ Resolve model
→ Run row-count checks
→ Run measure checks
→ Return structured report
```

**Prerequisites:**
- Team standards and knowledge base written down
- MCP tools or equivalent tool interface available
- Safe access model for Copilot-assisted workflows

**Limitations / boundaries:**
- Copilot quality depends on tool design and context quality
- It should assist decisions, not replace ownership and approval
- Natural language convenience does not remove platform constraints

**Takeaway:** Copilot becomes valuable when it explains, refines, and executes against your standards.

**Speaker Script (TH):**
> ผมอยาก reposition Copilot ในเซสชันนี้ให้ต่างจากภาพจำทั่วไปนิดหนึ่งครับ  
> มันไม่ได้มีไว้แค่ช่วยตอบคำถามหรือเขียน prose แต่มีบทบาทใน workflow วิศวกรรมได้ 3 แบบ คือ explain, refine และ execute  
> Explain คือช่วยอธิบายว่า measure นี้ meaningful ภายใต้ context แบบไหน  
> Refine คือช่วยปรับ template ให้ตรงกับ business reality มากขึ้น  
> และ Execute คือเรียกใช้ tool ผ่าน MCP แล้วคืนผลลัพธ์ที่มีหลักฐานกลับมา ไม่ใช่แค่คำแนะนำลอย ๆ  
> แต่ ownership ยังเป็นของทีมเสมอครับ AI ช่วยเราทำงานดีขึ้น ไม่ได้มาแทน approval process

---

## Slide 10 — What You Actually Get

**A Structured Validation Report — Ready for Review**

```markdown
# Dataset Validation Report ✅ PASS

Dataset: <DATASET>
Compared: TEST vs PROD
Timestamp: 2026-03-14 14:23 → 14:25
Tolerance: row counts ±1%, measures ±1%

Summary:
- Schema comparison: PASS
- Row count validation: PASS
- Measure validation: PASS
- Risk assessment: PASS

Overall: 103 passed, 0 failed
```

**Enterprise uses**
- Attach to pull request as evidence
- Store as an audit artifact
- Review risk flags before deployment
- Use detailed failures for root-cause analysis

**Gate rule:** Deployment proceeds only when critical failures = 0.

**Prerequisites:**
- Standard report format and storage location
- Agreement on pass/fail and warning semantics

**Limitations / boundaries:**
- A report is useful only if people trust the rules behind it
- Risk flags still require human interpretation in context

**Takeaway:** The goal is not “I checked it.” The goal is “Here is the evidence, the scope, and the result.”

**Speaker Script (TH):**
> สิ่งที่ทีมได้กลับมาไม่ควรเป็นแค่ข้อความว่า “ผมเช็กแล้วนะ” ครับ  
> สิ่งที่ควรได้คือ validation report ที่บอก scope ชัด, rule ชัด, ผลชัด และย้อนกลับไปดูได้  
> ตรงนี้มี value มากทั้งในมุม reviewer, audit trail และ root-cause analysis  
> ถ้ามี failure เรารู้ว่าพังตรงไหน ถ้ามี warning เรารู้ว่าต้องพิจารณาอะไรเพิ่มเติม  
> และที่สำคัญคือเราสามารถผูก report นี้กับ deployment gate ได้เลย ว่าถ้ายังมี critical failure อยู่ deployment จะไม่ไปต่อครับ

---

## Slide 11 — End-to-End Pipeline

**From Source Files to Deployment Evidence**

```text
Generate Template
      ↓
Refine with Copilot
      ↓
Execute Queries on TEST + PROD
      ↓
Compare Results with Tolerance
      ↓
Publish Report / Gate Deployment
```

**Three run modes**
1. **Copilot Chat** — natural-language trigger for the workflow
2. **CLI** — repeatable for CI/CD pipelines
3. **Notebook** — interactive exploration during development

**Prerequisites:**
- Clear workflow ownership from generation to approval
- Stable auth strategy for each run mode
- Consistent template and output conventions

**Limitations / boundaries:**
- Different interfaces should not produce different logic
- Automation still needs operational monitoring and maintenance

**Takeaway:** One pipeline, multiple interfaces, one consistent control model.

**Speaker Script (TH):**
> Slide นี้เอาไว้สรุป operating model ครับ  
> ไม่ว่าคุณจะเริ่มจาก Copilot Chat, CLI หรือ Notebook สุดท้ายควรวิ่งเข้า logic ชุดเดียวกัน  
> เราไม่อยากให้ interface เปลี่ยนแล้วผล validation เปลี่ยนตาม  
> เพราะฉะนั้นสิ่งที่ต้องคงที่คือ template, comparison rule, tolerance policy และ output format  
> มองอีกแบบคือ user จะเข้า workflow ทางไหนก็ได้ แต่ control model ต้องเป็นเรื่องเดียวกันครับ

---

## Slide 12 — Scale, Impact & Knowledge

**From Manual Spot-Checks to Compounding Confidence**

| Metric | Before | After |
|--------|--------|-------|
| Validation time / dataset | 2–4 hours manual | 3–5 min automated |
| Measures checked | ~10 spot-checked | Broad coverage with slicing |
| Drift detection | After complaints | Before deployment |
| Test definition | Rebuilt every cycle | Reusable YAML templates |
| Team onboarding | Tribal knowledge | Shared patterns and standards |

**Knowledge base compounds value**
- Conventions define naming and modeling expectations
- Domain docs describe business logic and edge cases
- Solved problems become reusable validation patterns
- New team members inherit templates instead of folklore

**Prerequisites:**
- Standards documented in a shareable knowledge base
- Team discipline to keep templates and docs current

**Limitations / boundaries:**
- These are representative outcomes, not universal benchmarks
- Gains depend on model quality, platform maturity, and ownership clarity

**Takeaway:** Templates accumulate, standards harden, and trust scales.

**Speaker Script (TH):**
> คุณค่าที่แท้จริงของระบบแบบนี้ไม่ใช่แค่ทำให้เร็วขึ้นครั้งเดียวครับ  
> แต่มันทำให้ทุก validation cycle ครั้งถัดไปดีขึ้นเรื่อย ๆ  
> เพราะ template ถูก reuse ได้ knowledge base โตขึ้น solved problems ถูกเก็บไว้ และ onboarding คนใหม่ง่ายขึ้น  
> จากเดิมที่ทีมพึ่ง tribal knowledge หรือคนเก่งไม่กี่คน เราค่อย ๆ เปลี่ยนเป็นระบบที่แชร์มาตรฐานร่วมกันได้  
> ตัวเลข before/after บนสไลด์นี้ให้มองเป็น representative outcome นะครับ ผลจริงจะขึ้นกับ maturity ของ model และ process ของแต่ละทีม

---

## Slide 13 — The Paradigm Shift

**Is Your BI Platform Ready for Agentic Operation?**

```text
Insights and Visuals
        ↑
Validation Guardrails
        ↑
Model as Code + Custom Toolbox
```

You can scale BI delivery with AI very quickly.  
You can scale **trustworthy** BI delivery only when these layers work together.

**Three next steps**
1. Enable model-as-code in your delivery workflow
2. Add row-count and measure validation before deployment
3. Turn your best validation logic into reusable templates and tools

**Final framing for the audience:**
- Each solution has prerequisites
- Each solution has limitations
- That is normal — the goal is to design consciously, not promise magic

**Closing line:**  
**The question is not whether AI can help build Power BI faster. The question is whether your BI platform is engineered well enough to let AI operate safely.**

**Speaker Script (TH):**
> ผมอยากปิดด้วยภาพนี้ครับ  
> สิ่งที่ผู้ใช้เห็นคือ insights และ visuals แต่สิ่งที่ทำให้มันน่าเชื่อถือคือชั้น guardrails และ foundation ด้าน model-as-code กับ custom toolbox  
> เพราะฉะนั้นเวลาเราพูดถึง AI ในงาน BI ผมคิดว่าคำถามไม่ใช่แค่ว่า AI ทำให้เราสร้างได้เร็วขึ้นไหม  
> แต่คือ platform ของเราถูกออกแบบมาดีพอหรือยัง ที่จะให้ AI เข้ามาช่วยทำงานได้อย่างปลอดภัยและตรวจสอบได้  
> และผมตั้งใจใส่ prerequisite กับ limitation ของแต่ละแนวทางไว้ใน deck นี้ เพราะในโลก enterprise ไม่มี solution ไหนเป็น magic ครับ มีแต่ solution ที่ออกแบบอย่างรู้ขอบเขตของมัน  
> ขอบคุณมากครับ ยินดีรับคำถามต่อ หรือ connect กันทาง LinkedIn ได้ครับ

---

## Audience Doubt Checklist (Presenter Backup)

### Slide 2
- **Possible doubt:** “Is this about report UI testing too?”
- **Answer:** No. This session focuses on semantic model and deployment validation.

### Slide 3
- **Possible doubt:** “Are you using PBIR as shorthand for everything?”
- **Answer:** No. PBIP is the project, PBIR is the report layer, and the semantic model is stored as text/TMDL-style metadata.

### Slide 5
- **Possible doubt:** “Does row count prove correctness?”
- **Answer:** No. It proves high-value environment parity for data volume, not business logic correctness.

### Slide 6
- **Possible doubt:** “If TEST and PROD match, does that mean the KPI is correct?”
- **Answer:** No. It means the environments are consistent. Source reconciliation and UAT still matter.

### Slide 7
- **Possible doubt:** “Can the generator decide everything automatically?”
- **Answer:** No. It creates a strong first draft; domain owners still decide what is material.

### Slide 8
- **Possible doubt:** “Can’t we just skip failing checks?”
- **Answer:** Only as a temporary debug action. Production-grade exceptions must be documented and auditable.

### Slide 9
- **Possible doubt:** “Is Copilot just chatting, or is it actually doing something?”
- **Answer:** It can explain, refine, and execute through tools — but it still operates within platform constraints and team controls.

### Slide 10
- **Possible doubt:** “Who decides pass/fail?”
- **Answer:** The team defines the rules in advance; the report makes the decision evidence-based and reviewable.

### Slide 11
- **Possible doubt:** “Will Copilot mode, CLI mode, and Notebook mode behave differently?”
- **Answer:** They should not. Different entry points must converge on the same validation logic.

### Slide 12
- **Possible doubt:** “Are these time savings guaranteed?”
- **Answer:** No. They are representative outcomes that depend on model quality and platform maturity.

### Slide 13
- **Possible doubt:** “Are you saying AI replaces BI engineering?”
- **Answer:** The opposite. AI increases the need for BI engineering discipline.

---

## Optional Q&A Backup — RLS / Auth Discussion

**If asked:** “What about datasets with RLS?”

Suggested answer:
- For non-RLS datasets, service principal automation is usually the cleanest path.
- For RLS-sensitive datasets, use delegated user context for validation personas.
- Treat persona-based validation as part of the design, not as an afterthought.
- Keep the deck focused on the control model; move auth specifics into Q&A unless the audience asks.
