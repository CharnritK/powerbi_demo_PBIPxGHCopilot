const PptxGenJS = require('pptxgenjs');
const {
  imageSizingCrop,
  imageSizingContain,
  safeOuterShadow,
  warnIfSlideHasOverlaps,
  warnIfSlideElementsOutOfBounds,
  calcTextBoxHeightSimple,
} = require('/home/oai/skills/slides/pptxgenjs_helpers');
const path = require('path');

const SESSION = {
  title: 'Enterprise BI Engineering: Building Trustworthy Power BI with PBIP/PBIR, GitHub Copilot & AI',
  titleLine1: 'Enterprise BI Engineering',
  titleLine2: 'Building Trustworthy Power BI',
  titleLine3: 'with PBIP/PBIR, GitHub Copilot & AI',
  subtitle: 'Version Control, Validation Guardrails\nand AI-Assisted Tooling for Trustworthy Power BI',
  focus: ['Trustworthy enterprise BI delivery', 'Developer-oriented practical demo'],
  framingTitle: 'AI Makes BI Faster. Engineering Makes BI Trustworthy.',
  framingSubtitle: 'Semantic model + deployment validation, not report-page UI regression testing',
  framingHook: 'In enterprise BI, the hardest question is not "Can we build it?"\nWe already can.\nThe real question is "Can we trust it in production?"',
};

const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'OpenAI';
pptx.company = 'OpenAI';
pptx.subject = SESSION.title;
pptx.title = SESSION.title;
pptx.lang = 'en-US';
pptx.theme = {
  headFontFace: 'Segoe UI',
  bodyFontFace: 'Segoe UI',
  lang: 'en-US'
};

const W = 13.333;
const H = 7.5;

const C = {
  bg: '1F2A2E',
  bg2: '243238',
  white: 'F7F7F7',
  text: '20232A',
  muted: '67707A',
  teal: '1FB5A9',
  coral: 'EF9191',
  blue: '4F7CD7',
  orange: 'D58A52',
  pass: '1FB5A9',
  fail: 'E06C6C',
  line: 'D9E2E8',
  card: 'EEF3F5',
  cardDark: '2A363D',
  soft: 'E8EEF1',
  code: '1E1E2E',
};

const assets = {
  hero: path.join(__dirname, 'community_meetup_assets', 'hero.png'),
  workflow: path.join(__dirname, 'community_meetup_assets', 'workflow.png'),
  stack: path.join(__dirname, 'community_meetup_assets', 'stack.png'),
};

function addBg(slide, dark=true) {
  slide.background = { color: dark ? C.bg : C.white };
}

function addTopBar(slide, label, color) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 10.65, y: 0.22, w: 2.15, h: 0.34,
    rectRadius: 0.04,
    fill: { color }, line: { color },
  });
  slide.addText(label, {
    x: 10.75, y: 0.285, w: 1.95, h: 0.2,
    fontFace: 'Segoe UI', fontSize: 11, bold: true,
    color: C.white, align: 'center', margin: 0,
  });
}

function addHeader(slide, title, subtitle='', dark=true) {
  const titleColor = dark ? C.white : C.text;
  const subColor = dark ? 'C7D2D9' : C.muted;
  slide.addText(title, {
    x: 0.6, y: 0.28, w: 9.4, h: 0.45,
    fontFace: 'Segoe UI', fontSize: 26, bold: true,
    color: titleColor, margin: 0,
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.6, y: 0.89, w: 2.6, h: 0.035,
    line: { color: C.coral, transparency: 100 }, fill: { color: C.coral },
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.6, y: 1.02, w: 10.0, h: 0.26,
      fontFace: 'Segoe UI', fontSize: 12.5,
      color: subColor, margin: 0,
    });
  }
}

function addFooter(slide, n) {
  slide.addText(String(n), {
    x: 12.45, y: 7.05, w: 0.35, h: 0.18,
    fontFace: 'Segoe UI', fontSize: 10, color: '91A0A8',
    align: 'right', margin: 0,
  });
}

function addTakeaway(slide, text, dark=true) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 0.6, y: 6.55, w: 12.1, h: 0.5,
    rectRadius: 0.04,
    fill: { color: dark ? '2C373D' : C.soft },
    line: { color: dark ? '2C373D' : C.soft },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.6, y: 6.55, w: 0.05, h: 0.5,
    fill: { color: C.coral }, line: { color: C.coral }
  });
  slide.addText(text, {
    x: 0.82, y: 6.66, w: 11.6, h: 0.22,
    fontFace: 'Segoe UI', fontSize: 13,
    color: dark ? 'D8E0E5' : C.text, margin: 0,
  });
}

function addCodeCard(slide, x, y, w, h, code) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.05,
    fill: { color: C.code },
    line: { color: C.code },
    shadow: safeOuterShadow('000000', 0.18, 45, 2, 1)
  });
  slide.addText(code, {
    x: x+0.18, y: y+0.16, w: w-0.32, h: h-0.25,
    fontFace: 'Cascadia Code', fontSize: 10.2,
    color: C.white, breakLine: false, margin: 0,
    valign: 'top', fit: 'shrink'
  });
}

function addBulletList(slide, x, y, w, items, dark=true, fontSize=15, bulletColor=C.teal) {
  const runs = [];
  items.forEach((t, i) => {
    runs.push({ text: '• ', options: { color: bulletColor, bold: true } });
    runs.push({ text: t, options: { color: dark ? C.white : C.text } });
    if (i !== items.length - 1) runs.push({ text: '\n' });
  });
  const h = Math.min(3.5, calcTextBoxHeightSimple(fontSize, items.length * 2, 1.28, 0.02));
  slide.addText(runs, {
    x, y, w, h,
    fontFace: 'Segoe UI', fontSize,
    margin: 0, breakLine: false, fit: 'shrink',
  });
}

function addInfoCard(slide, x, y, w, h, title, lines, dark=true, accent=C.teal) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.05,
    fill: { color: dark ? C.cardDark : C.card },
    line: { color: dark ? '324149' : 'DDE7EC', pt: 1 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x, y, w: 0.05, h,
    fill: { color: accent }, line: { color: accent },
  });
  slide.addText(title, {
    x: x+0.18, y: y+0.14, w: w-0.25, h: 0.24,
    fontFace: 'Segoe UI', fontSize: 13, bold: true,
    color: dark ? C.white : C.text, margin: 0,
  });
  slide.addText(lines.join('\n'), {
    x: x+0.18, y: y+0.42, w: w-0.28, h: h-0.5,
    fontFace: 'Segoe UI', fontSize: 11.5,
    color: dark ? 'D6DEE4' : C.muted, margin: 0,
    fit: 'shrink'
  });
}

function addSimpleTable(slide, x, y, w, h, rows, dark=true) {
  const bodyFill = dark ? C.cardDark : C.white;
  const altFill = dark ? '263239' : 'F4F8FA';
  const tableRows = rows.map((row, r) => row.map((val, c) => {
    const txt = String(val ?? '');
    let color = dark ? C.white : C.text;
    let fill = r === 0 ? C.bg2 : (r % 2 === 0 ? altFill : bodyFill);
    let bold = r === 0 || c === 0;
    if (r > 0 && c === 0) {
      if (txt.includes('PASS') || txt.includes('✅')) color = C.pass;
      if (txt.includes('FAIL') || txt.includes('❌')) color = C.fail;
      if (txt.includes('SKIP') || txt.includes('⏭')) color = '98A2A8';
    }
    return { text: txt, options: {
      fontFace: 'Segoe UI', fontSize: r === 0 ? 10.5 : 10.2,
      color, bold, align: r === 0 ? 'center' : 'left',
      fill, margin: 0.04,
      border: { type: 'solid', color: dark ? '3E4E57' : 'D7E0E6', pt: 1 },
      breakLine: false,
      valign: 'mid'
    }};
  }));
  slide.addTable(tableRows, { x, y, w, h, rowH: h / rows.length, margin: 0.04 });
}

function notesWithSources(script, sources=[]) {
  let note = `[TH Script]\n${script.trim()}\n`;
  if (sources.length) {
    note += `\n[Sources]\n` + sources.map(s => `- ${s}`).join('\n') + '\n';
  }
  return note;
}

const slides = [];

// Slide 1
slides.push(function(){
  const s = pptx.addSlide(); addBg(s, true);
  s.addImage({ path: assets.hero, ...imageSizingCrop(assets.hero, 0, 0, W, H) });
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: W, h: H, fill: { color: C.bg, transparency: 38 }, line: { color: C.bg, transparency: 100 } });
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: W, h: 0.66, fill: { color: C.teal, transparency: 8 }, line: { color: C.teal, transparency: 100 } });
  s.addText('Power Platform Bootcamp Thailand', { x: 0, y: 0.16, w: W, h: 0.28, align: 'center', margin: 0, fontFace: 'Segoe UI', fontSize: 20, color: C.white, bold: true });
  s.addShape(pptx.ShapeType.roundRect, { x: 0.64, y: 1.1, w: 6.6, h: 4.9, rectRadius: 0.06, fill: { color: C.bg, transparency: 10 }, line: { color: 'FFFFFF', transparency: 88 } });
  s.addText(SESSION.titleLine1, { x: 0.9, y: 1.42, w: 5.95, h: 0.5, fontFace: 'Segoe UI', fontSize: 30, color: C.white, bold: true, margin: 0 });
  s.addText(SESSION.titleLine2, { x: 0.9, y: 1.96, w: 5.95, h: 0.42, fontFace: 'Segoe UI', fontSize: 23, color: 'D7FBF6', bold: true, margin: 0, fit: 'shrink' });
  s.addText(SESSION.titleLine3, { x: 0.9, y: 2.34, w: 5.95, h: 0.34, fontFace: 'Segoe UI', fontSize: 16.5, color: 'D7FBF6', bold: true, margin: 0, fit: 'shrink' });
  s.addShape(pptx.ShapeType.rect, { x: 0.9, y: 2.78, w: 2.6, h: 0.04, fill: { color: C.coral }, line: { color: C.coral } });
  s.addText(SESSION.subtitle, {
    x: 0.9, y: 3.0, w: 5.95, h: 0.72, fontFace: 'Segoe UI', fontSize: 15, color: C.white, margin: 0, breakLine: false, fit: 'shrink'
  });
  s.addText('Charnrit Khongthanarat\nVis & Interaction Science Consultant, Accenture\nMarch 14, 2026 · AreaX, 4th Fl., Siam Paragon\nlinkedin.com/in/charnrit-khongthanarat', {
    x: 0.9, y: 4.25, w: 5.6, h: 1.2, fontFace: 'Segoe UI', fontSize: 12.5, color: 'EAF3F7', margin: 0, breakLine: false, fit: 'shrink'
  });
  addInfoCard(s, 8.95, 5.55, 3.55, 0.72, 'Session focus', SESSION.focus, true, C.coral);
  addFooter(s, 1);
  s.addNotes(notesWithSources(
`สวัสดีครับ ขอบคุณทุกคนที่ยังอยู่ในเซสชันสุดท้ายของวันนี้นะครับ
ผมชื่อชานฤทธิ์ ทำงานด้าน Power BI และ Enterprise BI Engineering เป็นหลัก ทั้งเรื่อง semantic model, CI/CD, validation และ governance
วันนี้ผมอยากชวนทุกคนมองอีกชั้นหนึ่งของ Power BI ครับ ไม่ใช่แค่สร้างรายงานให้สวยหรือใช้ AI ให้เร็วขึ้น แต่ทำอย่างไรให้ระบบ BI ของเราเชื่อถือได้ตอนขึ้น production
แกนของเซสชันนี้มี 3 เรื่อง คือ version control, validation guardrails และ custom toolbox ที่ใช้ GitHub Copilot ร่วมกับ workflow ของทีม
ทุกตัวอย่างในสไลด์นี้เป็นข้อมูลที่ sanitize แล้ว ไม่มีชื่อลูกค้า ไม่มีชื่อ dataset จริงครับ`
  ));
});

// Slide 2
slides.push(function(){
  const s = pptx.addSlide(); addBg(s, false); addHeader(s, SESSION.framingTitle, SESSION.framingSubtitle, false); addFooter(s,2);
  s.addText(SESSION.framingHook, {
    x: 0.7, y: 1.45, w: 6.0, h: 1.15, fontFace: 'Segoe UI', fontSize: 22.5, bold: true, color: C.text, margin: 0, fit: 'shrink'
  });
  addInfoCard(s, 0.75, 2.75, 5.9, 2.55, 'What goes wrong without engineering controls', [
    'KPI drift reaches decision-makers before anyone notices',
    'TEST and PROD quietly diverge after refreshes or schema changes',
    'Validation is manual, inconsistent, and undocumented',
    'Teams can explain how they built a release, but not how they proved it was safe'
  ], false, C.coral);
  addTopBar(s, 'Session framing', C.blue);
  const chipY = 1.58;
  [['Version Control',C.blue,7.2],['Guardrails',C.teal,9.05],['Custom Toolbox',C.orange,10.9]].forEach(([t,c,x])=>{
    s.addShape(pptx.ShapeType.roundRect,{x,y:chipY,w:1.55,h:0.34,rectRadius:0.05,fill:{color:c},line:{color:c}});
    s.addText(t,{x:x+0.08,y:chipY+0.08,w:1.39,h:0.16,fontFace:'Segoe UI',fontSize:12,bold:true,color:C.white,align:'center',margin:0});
  });
  addInfoCard(s, 7.0, 2.2, 5.45, 1.05, 'Scope', ['Semantic model + deployment validation', 'Not report-page UI regression testing'], false, C.teal);
  addBulletList(s, 7.05, 3.55, 5.35, [
    'Version Control — model and report definitions stored as text',
    'Guardrails — automated validation before deployment',
    'Custom Toolbox — Copilot + MCP + reusable templates + knowledge base'
  ], false, 14);
  addTakeaway(s, 'Trust in enterprise BI comes from repeatable engineering controls.', false);
  s.addNotes(notesWithSources(`ถ้าเราพูดถึง AI กับ Power BI ส่วนใหญ่เราจะพูดถึงเรื่องความเร็วครับ สร้างได้ไวขึ้น เขียนได้ไวขึ้น วิเคราะห์ได้ไวขึ้น
แต่ในมุม enterprise คำถามที่ยากกว่าคือ แล้วเราเชื่อมันได้หรือยังตอนขึ้น production
ปัญหาที่ทีมเจอกันบ่อยคือ KPI drift โดยไม่มีใครรู้ TEST กับ PROD ค่อย ๆ ไม่เหมือนกันหลัง refresh หรือหลังมีการแก้ schema และสุดท้าย validation ยังเป็นงาน manual ที่ไม่มีหลักฐานชัดเจน
เพราะฉะนั้นวันนี้ผมจะวางเรื่องนี้บน 3 เสา คือ version control, guardrails, และ custom toolbox
และขอระบุ scope ชัด ๆ เลยว่า เราโฟกัสที่ semantic model และ deployment validation ไม่ใช่การทดสอบ UI ของ report page ครับ`));
});

// Slide 3
slides.push(function(){
  const s = pptx.addSlide(); addBg(s, false); addHeader(s, 'Pillar 1: Model as Code', 'PBIP project + PBIR report + TMDL semantic model', false); addTopBar(s, 'Pillar 1', C.blue); addFooter(s,3);
  addCodeCard(s, 0.7, 1.45, 5.3, 3.15, `Project/\n├── <DATASET>.pbip\n├── <DATASET>.Report/\n│   └── definition/         # PBIR files\n└── <DATASET>.SemanticModel/\n    └── definition/         # TMDL / model metadata`);
  addBulletList(s, 6.35, 1.55, 5.6, [
    'Every change becomes a Git diff instead of a hidden binary change',
    'Pull requests can review measures, relationships, and report structure',
    'Automation can discover measures and dimensions from source files',
    'CI/CD can validate before deployment instead of after a complaint'
  ], false, 14);
  addInfoCard(s, 6.35, 4.0, 2.65, 1.4, 'Prerequisites', ['Power BI Project workflow enabled', 'Git repo + PR discipline', 'Source files committed'], false, C.teal);
  addInfoCard(s, 9.15, 4.0, 2.65, 1.4, 'Boundaries', ['Improves reviewability', 'Does not prove data correctness by itself', 'UI testing is separate'], false, C.coral);
  addTakeaway(s, 'No model-as-code, no serious automation.', false);
  s.addNotes(notesWithSources(`จุดเริ่มต้นของ automation ที่จริงจังคือ model-as-code ครับ
ตรงนี้ผมอยากใช้คำให้แม่นนิดหนึ่ง PBIP คือ project PBIR คือ report definition และ semantic model จะอยู่ในโครงสร้างแบบ text เช่น TMDL
สิ่งที่ได้คือทุกการเปลี่ยนแปลงกลายเป็น Git diff เรารีวิว measure relationship หรือ report structure ผ่าน pull request ได้
นี่สำคัญมาก เพราะถ้า model ยังเป็นกล่องดำหรือเป็น binary file อย่างเดียว เราแทบจะ automate ได้ไม่จริง
แต่ต้องบอกขอบเขตด้วยว่า model-as-code ช่วยเรื่อง reviewability และ automation readiness นะครับ มันยังไม่ได้พิสูจน์ว่า data ถูกต้อง`, [
    'https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview',
    'https://learn.microsoft.com/en-us/power-bi/developer/embedded/projects-enhanced-report-format'
  ]));
});

// Slide 4
slides.push(function(){
  const s = pptx.addSlide(); addBg(s, true); addHeader(s, 'Enterprise Model Discipline', 'Naming standards + star schema = reliable automation', true); addTopBar(s, 'Pillar 1', C.blue); addFooter(s,4);
  addSimpleTable(s, 0.7, 1.5, 4.95, 2.55, [
    ['Convention','Example'],
    ['Fact/Dim prefixes','FactProductionOutput, DimCalendar'],
    ['Business-friendly measure names','Total Output, %Efficiency'],
    ['Helper prefix','_BaseFilter, _HoursRaw'],
    ['Display folders','Production / Quality / Finance'],
    ['Descriptions','Self-documenting model']
  ], true);
  s.addText('Star-schema example', {x:6.05, y:1.48, w:2.1, h:0.22, fontFace:'Segoe UI', fontSize:12, bold:true, color:'C7D2D9', margin:0});
  const cx = 9.1, cy = 3.05;
  const lineOpts = { line: { color: '9ACCC6', pt: 1.5, beginArrowType: 'none', endArrowType: 'triangle' } };
  s.addShape(pptx.ShapeType.line, { x: cx, y: cy-1.02, w: 0, h: 0.66, ...lineOpts });
  s.addShape(pptx.ShapeType.line, { x: cx-2.05, y: cy, w: 1.45, h: 0, ...lineOpts });
  s.addShape(pptx.ShapeType.line, { x: cx+0.6, y: cy, w: 1.45, h: 0, ...lineOpts });
  s.addShape(pptx.ShapeType.line, { x: cx, y: cy+0.18, w: 0, h: 0.7, ...lineOpts });
  [['DimCalendar',8.15,1.72,1.95],['DimProduct',6.55,2.72,1.95],['DimSite',10.1,2.72,1.9],['DimShift',8.2,4.06,1.95]].forEach(([t,x,y,w])=>{
    s.addShape(pptx.ShapeType.roundRect,{x,y,w,h:0.52,rectRadius:0.05,fill:{color:'334148'},line:{color:'334148'}});
    s.addText(t,{x:x+0.08,y:y+0.13,w:w-0.16,h:0.18,fontFace:'Segoe UI',fontSize:13.2,bold:true,color:C.white,margin:0,align:'center',fit:'shrink'});
  });
  s.addShape(pptx.ShapeType.roundRect,{x:7.85,y:2.78,w:2.55,h:0.64,rectRadius:0.05,fill:{color:C.teal},line:{color:C.teal},shadow:safeOuterShadow('000000',0.18,45,2,1)});
  s.addText(`FactProduction\nOutput`,{x:8.02,y:2.91,w:2.21,h:0.26,fontFace:'Segoe UI',fontSize:12.8,bold:true,color:C.white,margin:0,align:'center',fit:'shrink'});
  addBulletList(s, 0.75, 4.35, 5.0, [
    'Facts at clear grain: one row per ___',
    'Shared DimCalendar for time slicing',
    'Single-direction filters from dimension to fact',
    'Measures preferred over calculated columns',
    'Relationship intent documented'
  ], true, 13.4);
  addInfoCard(s, 10.55, 4.15, 2.0, 1.25, 'Boundary', ['Automation quality depends on model quality', 'Snowflake-heavy designs reduce tool accuracy'], true, C.coral);
  addTakeaway(s, 'Well-structured models are easier to govern, review, and validate.', true);
  s.addNotes(notesWithSources(`หลายทีมอยากได้ automation แต่ model ยังตั้งชื่อไม่สม่ำเสมอ หรือ schema ยังไม่ discipline พอ
ถ้าเป็นแบบนั้น เครื่องมือจะเดายาก และ reviewer ก็อ่านยากเหมือนกัน
เพราะฉะนั้น naming standard กับ star schema ไม่ใช่เรื่อง cosmetic แต่มันคือ prerequisite ของ automation
ถ้าเราใช้ Fact กับ Dim ชัดเจน มี shared calendar ระบุ grain และใช้ measure แทน calculated column เท่าที่ควร เครื่องมือจะค้นหา จัดกลุ่ม และสร้าง template ได้แม่นขึ้นมาก
พูดง่าย ๆ คือ model ที่ self-documenting จะทั้งคนอ่านรู้เรื่อง และ machine ก็อ่านรู้เรื่องด้วยครับ`));
});

// Slide 5
slides.push(function(){
  const s = pptx.addSlide(); addBg(s, true); addHeader(s, 'Pillar 2: Guardrails — Row Count Validation', 'COUNTROWS across TEST vs PROD — automated', true); addTopBar(s, 'Pillar 2', C.teal); addFooter(s,5);
  addCodeCard(s, 0.68, 1.48, 6.0, 3.2, `EVALUATE UNION(\n  ROW("tbl","Fact<TABLE>","cnt",COUNTROWS('Fact<TABLE>')),\n  ROW("tbl","Dim<TABLE>","cnt",COUNTROWS('Dim<TABLE>')),\n  ROW("tbl","DimCalendar","cnt",COUNTROWS('DimCalendar'))\n)\n# Run on TEST and PROD\n# Compare with tolerance, e.g. ±1%\n# Batch tables to stay inside query limits`);
  addSimpleTable(s, 6.95, 1.62, 5.65, 2.6, [
    ['Status','Table','TEST','PROD','Diff'],
    ['✅ PASS','Fact<TABLE>','1,245,302','1,245,302','0.00%'],
    ['✅ PASS','Fact<TABLE-B>','89,421','89,421','0.00%'],
    ['❌ FAIL','Fact<TABLE-C>','12,847','13,201','-2.68%'],
    ['✅ PASS','DimCalendar','3,652','3,652','0.00%'],
    ['⏭️ SKIP','Dim<TABLE>_v2','','','']
  ], true);
  addInfoCard(s, 0.72, 4.95, 3.8, 1.1, 'Prerequisites', ['Comparable TEST and PROD datasets', 'Query execution path enabled', 'Defined tolerance policy'], true, C.teal);
  addInfoCard(s, 4.72, 4.95, 3.8, 1.1, 'Limitations', ['Detects volume drift, not business-logic correctness', 'Intentional differences need documented exceptions'], true, C.coral);
  addInfoCard(s, 8.72, 4.95, 3.9, 1.1, 'Good for', ['Incomplete loads', 'Broken partitions', 'Environment drift'], true, C.blue);
  addTakeaway(s, 'Row-count checks are the fastest high-value deployment gate.', true);
  s.addNotes(notesWithSources(`Guardrail แรกที่คุ้มมากคือ row count ครับ
เรารัน COUNTROWS กับตารางสำคัญใน TEST และ PROD แล้วเทียบกันด้วย tolerance ที่ตกลงร่วมกัน เช่นบวกลบหนึ่งเปอร์เซ็นต์
ข้อดีคือมันเร็ว อธิบายง่าย และจับปัญหาพื้นฐานที่เจอบ่อยมาก เช่น load ไม่ครบ partition ผิด หรือ environment drift
แต่ผมอยากให้มองอย่างแม่นนะครับ row count ไม่ได้บอกว่าธุรกิจ logic ถูก มันบอกว่าปริมาณข้อมูลที่ควรจะเหมือนกัน ตอนนี้มันไม่เหมือน
ถ้า TEST กับ PROD ตั้งใจให้ต่างกันอยู่แล้ว เราต้อง declare exception ให้ชัด ไม่งั้นผล validation จะกลายเป็น noise ครับ`, [
    'https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/execute-queries',
    'https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/execute-queries-in-group'
  ]));
});

// Slide 6
slides.push(function(){
  const s = pptx.addSlide(); addBg(s, true); addHeader(s, 'Measure Value Validation', 'Compare DAX outcomes, not just model structure', true); addTopBar(s, 'Pillar 2', C.teal); addFooter(s,6);
  addCodeCard(s, 0.68, 1.48, 6.0, 3.05, `EVALUATE UNION(\n  ROW("measure","<METRIC-A>","value",[<METRIC-A>]),\n  ROW("measure","<METRIC-B>","value",[<METRIC-B>]),\n  ROW("measure","<METRIC-C>","value",[<METRIC-C>])\n)\n# Grand-total comparison first\n# Numeric results use tolerance\n# Text results use exact match`);
  addSimpleTable(s, 6.95, 1.62, 5.65, 2.48, [
    ['Status','Measure','TEST','PROD','Diff'],
    ['✅ PASS','<METRIC-A>','45,231','45,231','0.00%'],
    ['✅ PASS','<METRIC-B>','87.34%','87.34%','0.00%'],
    ['❌ FAIL','<METRIC-C>','2,104.5','2,167.8','-2.92%'],
    ['✅ PASS','<METRIC-D>','1,890.2','1,890.2','0.00%'],
    ['⏭️ SKIP','[Internal]','','','']
  ], true);
  addInfoCard(s, 0.72, 4.82, 3.8, 1.18, 'Prerequisites', ['Ability to execute DAX queries', 'Selected measure set or discovery source', 'Tolerance and null-handling rules'], true, C.teal);
  addInfoCard(s, 4.72, 4.82, 3.8, 1.18, 'Limitations', ['Grand totals can hide slice-specific problems', 'Time-sensitive measures need careful handling'], true, C.coral);
  addInfoCard(s, 8.72, 4.82, 3.9, 1.18, 'Boundary', ['Deployment parity ≠ business truth', 'Still not a replacement for UAT or reconciliation'], true, C.blue);
  addTakeaway(s, 'Measure checks tell you whether the business result changed.', true);
  s.addNotes(notesWithSources(`ถัดมาคือ validation ที่ business รู้สึกจริงที่สุด คือการเทียบค่า measure ครับ
เพราะต่อให้ schema ไม่พัง แต่ถ้า KPI เปลี่ยน ผลกระทบจริงจะไปถึงคนตัดสินใจทันที
เราจึงต้องดู outcome ของ DAX โดยตรง ไม่ใช่ดูแค่ว่า object ยังอยู่ครบไหม
แต่ก็มี boundary ที่ต้องพูดให้ชัด คือถ้า TEST กับ PROD ให้ผลเท่ากัน ไม่ได้แปลว่า business truth ถูกหนึ่งร้อยเปอร์เซ็นต์ มันแปลว่า 2 environment นี้สอดคล้องกัน
ดังนั้นผมมองสิ่งนี้เป็น deployment guardrail ไม่ใช่ตัวแทนของ UAT หรือ source reconciliation ครับ`, [
    'https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/execute-queries'
  ]));
});

// Slide 7
slides.push(function(){
  const s = pptx.addSlide(); addBg(s, false); addHeader(s, 'Template-Driven Testing', 'Auto-discover → generate YAML → compare by dimension slice', false); addTopBar(s, 'Pillar 2', C.teal); addFooter(s,7);
  addCodeCard(s, 0.68, 1.46, 5.55, 3.1, `dataset: <DATASET>\ntolerance_pct: 1.0\n\nmeasures:\n  - name: <METRIC-A>\n    selected: true\n    category: output\n  - name: <METRIC-B>\n    selected: true\n    category: efficiency\n\ndimensions:\n  - table: DimCalendar\n    column: CalendarYear\n    selected: true\n    cardinality: 5\n\nfilters:\n  - table: DimCalendar\n    column: CalendarYear\n    operator: IN\n    values: ['2025', '2026']`);
  addCodeCard(s, 6.5, 1.46, 6.1, 2.12, `EVALUATE\nSUMMARIZECOLUMNS(\n  DimCalendar[CalendarYear],\n  Dim<TABLE>[<COLUMN>],\n  TREATAS({"2025","2026"}, DimCalendar[CalendarYear]),\n  "<METRIC-A>", [<METRIC-A>],\n  "<METRIC-B>", [<METRIC-B>]\n)`);
  addBulletList(s, 6.58, 3.9, 5.5, [
    'Grand total looks fine, but one site or one year is off',
    'A measure only breaks under specific filter context',
    'A business rule changed in one slice but not the overall total'
  ], false, 14);
  addInfoCard(s, 0.72, 4.95, 3.8, 1.08, 'Prerequisites', ['Discovery source for measures/dimensions', 'Curated dimension list with reasonable cardinality'], false, C.teal);
  addInfoCard(s, 4.72, 4.95, 3.8, 1.08, 'Limitations', ['Auto-selection is a strong first draft, not final judgment', 'High-cardinality slices can become slow or noisy'], false, C.coral);
  addInfoCard(s, 8.72, 4.95, 3.9, 1.08, 'Template principle', ['Domain owners still decide what is material'], false, C.blue);
  addTakeaway(s, 'Dimension slicing proves stability where the business actually operates.', false);
  s.addNotes(notesWithSources(`จุดที่หลายทีมเริ่มเห็น value จริง ๆ คือ slide นี้ครับ
เพราะบางครั้ง grand total ดูปกติ แต่พอแตกตามปี ตาม site หรือ dimension สำคัญบางตัว เราจะเจอ drift ที่ซ่อนอยู่
Template ทำให้กระบวนการนี้ reuse ได้ เราไม่ต้องเขียน query ใหม่ทุก release
ระบบสามารถ auto-discover แล้ว generate first draft ให้ได้ แต่ผมไม่อยากให้ตีความว่าเป็น blind automation นะครับ
คนที่รู้ business จริงยังต้องช่วยตัดสินว่า measure ไหนสำคัญ dimension ไหนเป็น material slice และ filter ไหนควรใช้เพื่อให้การทดสอบ meaningful`));
});

// Slide 8
slides.push(function(){
  const s = pptx.addSlide(); addBg(s, false); addHeader(s, 'Expected Deviations', 'Documented exceptions, not silent blind spots', false); addTopBar(s, 'Pillar 2', C.teal); addFooter(s,8);
  addCodeCard(s, 0.7, 1.5, 5.7, 2.7, `# deviation.yaml\nrow_counts:\n  Fact<TABLE>:\n    expected_diff_pct: 5.0\n    reason: TEST holds a daily subset only\n    approved_by: <OWNER>\n    expires: 2026-06-01\n\nmeasures:\n  <METRIC-A>:\n    expected_diff_pct: 3.0\n    reason: TEST contains only 9 months of history`);
  addCodeCard(s, 6.75, 1.5, 5.85, 2.1, `User: "Validate <DATASET>, but skip Fact<TABLE> row counts\n       — I just loaded a partial refresh"\n\nCopilot: "Skipping Fact<TABLE> for this run only.\n          Remaining checks continue."`);
  addSimpleTable(s, 6.75, 4.0, 5.85, 1.55, [
    ['Scenario','Recommended path'],
    ['Persistent + auditable','deviation.yaml'],
    ['Temporary + ad hoc','single-run exclusion'],
    ['CI/CD path','persistent only'],
    ['Debug path','temporary is acceptable']
  ], false);
  addInfoCard(s, 0.75, 4.5, 5.55, 1.05, 'Prerequisites & boundaries', ['Named owners, review cadence, and expiry policy', 'Too many deviations reduce trust in the gate'], false, C.coral);
  addTakeaway(s, 'Validation is only useful when expected differences are codified.', false);
  s.addNotes(notesWithSources(`คำถามที่คนมักถามต่อคือ แล้วถ้า TEST กับ PROD ตั้งใจให้ต่างกันล่ะ จะทำอย่างไร
คำตอบคือเราต้องแยก exception ที่ตั้งใจและอธิบายได้ ออกจาก blind spot ที่ไม่มีใครรู้
ถ้าเป็นความต่างที่ควรอยู่ระยะยาว เราควรเก็บไว้ใน deviation.yaml พร้อม owner reason และ expiry
แต่ถ้าเป็นแค่รัน debug ชั่วคราว เช่นเพิ่ง partial refresh มา เราอาจใช้ single-run exclusion ได้
ประเด็นสำคัญคือ temporary exclusion ต้องไม่กลายเป็น policy ลับที่ไม่มีใครตรวจสอบครับ`));
});

// Slide 9
slides.push(function(){
  const s = pptx.addSlide(); addBg(s, true); addHeader(s, 'Pillar 3: Custom Toolbox with Copilot', 'AI for BI engineering, not just BI analysis', true); addTopBar(s, 'Pillar 3', C.orange); addFooter(s,9);
  const cards = [
    {x:0.85, title:'Explain', color:C.blue, lines:['Clarify measure logic', 'Context and risks', 'What the metric really means']},
    {x:4.48, title:'Refine', color:C.teal, lines:['Improve template selections', 'Pick the right filters and slices', 'Turn first draft into test definition']},
    {x:8.11, title:'Execute', color:C.orange, lines:['Call MCP tools', 'Run validation workflow', 'Return structured evidence']},
  ];
  cards.forEach(c=>{
    s.addShape(pptx.ShapeType.roundRect,{x:c.x,y:1.72,w:3.0,h:2.65,rectRadius:0.06,fill:{color:C.cardDark},line:{color:'38464E',pt:1}});
    s.addShape(pptx.ShapeType.roundRect,{x:c.x+0.16,y:1.9,w:0.95,h:0.34,rectRadius:0.04,fill:{color:c.color},line:{color:c.color}});
    s.addText(c.title,{x:c.x+0.18,y:1.98,w:0.91,h:0.16,fontFace:'Segoe UI',fontSize:12,bold:true,color:C.white,align:'center',margin:0});
    addBulletList(s,c.x+0.2,2.45,2.55,c.lines,true,14,c.color);
  });
  addCodeCard(s, 0.85, 4.75, 3.0, 1.25, `"Are the right measures selected?"\n→ Missing: <METRIC-F>\n→ Add Dim<TABLE-B> for slicing`);
  addCodeCard(s, 4.48, 4.75, 3.0, 1.25, `"What context does <METRIC-B> need?"\n→ Needs Year + Site context\n→ Recommend Year × <COLUMN>`);
  addCodeCard(s, 8.11, 4.75, 3.0, 1.25, `"Validate <DATASET>"\n→ Resolve model\n→ Run checks\n→ Return structured report`);
  addTakeaway(s, 'Copilot becomes valuable when it explains, refines, and executes against your standards.', true);
  s.addNotes(notesWithSources(`ผมอยาก reposition Copilot ในเซสชันนี้ให้ต่างจากภาพจำทั่วไปนิดหนึ่งครับ
มันไม่ได้มีไว้แค่ช่วยตอบคำถามหรือเขียน prose แต่มีบทบาทใน workflow วิศวกรรมได้ 3 แบบ คือ explain refine และ execute
Explain คือช่วยอธิบายว่า measure นี้ meaningful ภายใต้ context แบบไหน
Refine คือช่วยปรับ template ให้ตรงกับ business reality มากขึ้น
และ Execute คือเรียกใช้ tool ผ่าน MCP แล้วคืนผลลัพธ์ที่มีหลักฐานกลับมา ไม่ใช่แค่คำแนะนำลอย ๆ`, [
    'https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/extend-copilot-chat-with-mcp'
  ]));
});

// Slide 10
slides.push(function(){
  const s = pptx.addSlide(); addBg(s, false); addHeader(s, 'What You Actually Get', 'A structured validation report — ready for review', false); addTopBar(s, 'Artifact', C.teal); addFooter(s,10);
  addCodeCard(s, 0.72, 1.5, 5.4, 3.15, `# Dataset Validation Report ✅ PASS\n\nDataset: <DATASET>\nCompared: TEST vs PROD\nTimestamp: 2026-03-14 14:23 → 14:25\nTolerance: row counts ±1%, measures ±1%\n\nSummary:\n- Schema comparison: PASS\n- Row count validation: PASS\n- Measure validation: PASS\n- Risk assessment: PASS\n\nOverall: 103 passed, 0 failed`);
  addBulletList(s, 6.55, 1.68, 5.25, [
    'Attach to pull request as evidence',
    'Store as an audit artifact',
    'Review risk flags before deployment',
    'Use detailed failures for root-cause analysis'
  ], false, 15);
  addInfoCard(s, 6.55, 3.7, 5.25, 1.05, 'Gate rule', ['Deployment proceeds only when critical failures = 0.'], false, C.coral);
  addInfoCard(s, 6.55, 4.95, 2.45, 1.0, 'Prerequisites', ['Standard report format', 'Agreed pass/fail semantics'], false, C.teal);
  addInfoCard(s, 9.35, 4.95, 2.45, 1.0, 'Boundary', ['Risk flags still need human interpretation'], false, C.blue);
  addTakeaway(s, 'The goal is not “I checked it.” The goal is evidence, scope, and result.', false);
  s.addNotes(notesWithSources(`สิ่งที่ทีมได้กลับมาไม่ควรเป็นแค่ข้อความว่าผมเช็กแล้วนะครับ
สิ่งที่ควรได้คือ validation report ที่บอก scope ชัด rule ชัด ผลชัด และย้อนกลับไปดูได้
ตรงนี้มี value มากทั้งในมุม reviewer audit trail และ root-cause analysis
ถ้ามี failure เรารู้ว่าพังตรงไหน ถ้ามี warning เรารู้ว่าต้องพิจารณาอะไรเพิ่มเติม
และที่สำคัญคือเราสามารถผูก report นี้กับ deployment gate ได้เลย ว่าถ้ายังมี critical failure อยู่ deployment จะไม่ไปต่อครับ`));
});

// Slide 11
slides.push(function(){
  const s = pptx.addSlide(); addBg(s, true); addHeader(s, 'Behind the Workflow', 'What the engine calls and what the repo actually contains', true); addTopBar(s, 'Workflow', C.orange); addFooter(s,11);
  s.addShape(pptx.ShapeType.roundRect,{x:0.8,y:1.42,w:11.8,h:1.2,rectRadius:0.06,fill:{color:'1B2429'},line:{color:'304047',pt:1}});
  s.addImage({ path: assets.workflow, ...imageSizingContain(assets.workflow, 1.05, 1.58, 11.3, 0.88) });
  const chips = [
    ['List workspaces',0.92,C.blue],
    ['List datasets',3.18,C.teal],
    ['Execute DAX',5.38,C.orange],
    ['Compare results',7.58,C.teal],
    ['Write report',9.82,C.coral],
  ];
  chips.forEach(([label,x,color], i)=>{
    s.addShape(pptx.ShapeType.roundRect,{x,y:2.7,w:1.78,h:0.28,rectRadius:0.04,fill:{color},line:{color}});
    s.addText(label,{x:x+0.05,y:2.77,w:1.68,h:0.12,fontFace:'Segoe UI',fontSize:10.4,bold:true,color:C.white,align:'center',margin:0,fit:'shrink'});
    if (i<chips.length-1) {
      s.addShape(pptx.ShapeType.line,{x:x+1.78,y:2.84,w:0.38,h:0,line:{color:'94A8B2',pt:1.2,endArrowType:'triangle'}});
    }
  });
  addCodeCard(s, 0.78, 3.0, 5.75, 2.35, `# Engine example
GET  /groups?filter=name eq '<WORKSPACE>'
GET  /groups/{groupId}/datasets
POST /groups/{groupId}/datasets/{datasetId}/executeQueries

{
  "queries": [
    {"query": "EVALUATE ROW(\"cnt\", COUNTROWS('Fact<TABLE>'))"}
  ]
}`);
  addCodeCard(s, 6.75, 3.0, 5.78, 2.35, `# Repo example
bi-platform/
├── powerbi/
│   └── <DATASET>.pbip
├── validation/
│   ├── execute_queries.py
│   ├── templates/<DATASET>.yaml
│   └── reports/
├── knowledge/
│   ├── conventions/
│   └── domains/
└── optional-data-engineering/`);
  addInfoCard(s, 0.82, 5.68, 5.72, 0.62, 'Why this helps the audience', ['They see the engine is simple: resolve → query → compare → report'], true, C.teal);
  addInfoCard(s, 6.78, 5.68, 5.72, 0.62, 'Repo takeaway', ['PBIP files, validation code, templates, and knowledge can live together'], true, C.coral);
  addTakeaway(s, 'Make the automation concrete enough to trust, but abstract enough to stay client-safe.', true);
  s.addNotes(notesWithSources(`สไลด์นี้ผมอยากเปิดให้เห็นหลังบ้านมากขึ้นอีกนิดครับ
สิ่งที่เกิดขึ้นจริงไม่ได้ซับซ้อนเกินเข้าใจ มันคือการ resolve workspace หา dataset แล้วส่ง DAX query ไป execute จากนั้นค่อย compare และเขียน report ออกมา
ฝั่งขวาคือภาพของ repo ที่ทีมมักอยากเห็น ว่าถ้าเราทำจริง ไฟล์ Power BI โค้ด validation template และ knowledge base จะวางอยู่ตรงไหน
สารสำคัญไม่ใช่ว่าทุกทีมต้องใช้โครงสร้างนี้เป๊ะ แต่คือทุกอย่างควรถูกจัดวางให้อ่านรู้เรื่อง ดูแลได้ และ review ได้
ถ้าทีมมี external coding repo ของ data engineer ก็แยกได้ครับ ขอแค่ contract ระหว่าง repo ชัด เช่น input output ownership และ deployment boundary`, [
    'https://learn.microsoft.com/en-us/rest/api/power-bi/groups/get-groups',
    'https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/get-datasets-in-group',
    'https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/execute-queries-in-group'
  ]));
});

// Slide 12
slides.push(function(){
  const s = pptx.addSlide(); addBg(s, false); addHeader(s, 'Scale, Impact & Knowledge', 'From manual spot-checks to compounding confidence', false); addTopBar(s, 'Impact', C.blue); addFooter(s,12);
  addSimpleTable(s, 0.72, 1.55, 6.05, 3.0, [
    ['Metric','Before','After'],
    ['Validation time / dataset','2–4 hours manual','3–5 min automated'],
    ['Measures checked','~10 spot-checked','Broad coverage with slicing'],
    ['Drift detection','After complaints','Before deployment'],
    ['Test definition','Rebuilt every cycle','Reusable YAML templates'],
    ['Team onboarding','Tribal knowledge','Shared patterns and standards']
  ], false);
  addCodeCard(s, 7.15, 1.58, 5.4, 2.1, `knowledge/\n├── conventions/\n│   ├── naming.md\n│   ├── data-model.md\n│   └── business-logic.md\n├── domains/\n│   ├── production/\n│   ├── quality/\n│   └── finance/\n└── solved-problems.md`);
  addBulletList(s, 7.2, 4.0, 5.2, [
    'Conventions define naming and modeling expectations',
    'Domain docs describe business logic and edge cases',
    'Solved problems become reusable validation patterns',
    'New team members inherit templates instead of folklore'
  ], false, 13.5);
  addInfoCard(s, 0.75, 4.95, 5.95, 1.0, 'Boundary', ['Representative outcomes, not universal benchmarks', 'Gains depend on model quality and ownership clarity'], false, C.coral);
  addTakeaway(s, 'Templates accumulate, standards harden, and trust scales.', false);
  s.addNotes(notesWithSources(`คุณค่าที่แท้จริงของระบบแบบนี้ไม่ใช่แค่ทำให้เร็วขึ้นครั้งเดียวครับ
แต่มันทำให้ทุก validation cycle ครั้งถัดไปดีขึ้นเรื่อย ๆ
เพราะ template ถูก reuse ได้ knowledge base โตขึ้น solved problems ถูกเก็บไว้ และ onboarding คนใหม่ง่ายขึ้น
จากเดิมที่ทีมพึ่ง tribal knowledge หรือคนเก่งไม่กี่คน เราค่อย ๆ เปลี่ยนเป็นระบบที่แชร์มาตรฐานร่วมกันได้
ตัวเลข before after บนสไลด์นี้ให้มองเป็น representative outcome นะครับ ผลจริงจะขึ้นกับ maturity ของ model และ process ของแต่ละทีม`));
});

// Slide 13
slides.push(function(){
  const s = pptx.addSlide(); addBg(s, true); addHeader(s, 'The Paradigm Shift', 'Is your BI platform ready for agentic operation?', true); addTopBar(s, 'Closing', C.coral); addFooter(s,13);
  s.addText(`You can scale BI delivery with AI very quickly.\nYou can scale trustworthy BI delivery only when these layers work together.`, {
    x: 0.75, y: 1.65, w: 5.9, h: 1.05, fontFace: 'Segoe UI', fontSize: 24, bold: true, color: C.white, margin: 0, fit: 'shrink'
  });
  addBulletList(s, 0.8, 3.0, 5.45, [
    'Enable model-as-code in your delivery workflow',
    'Add row-count and measure validation before deployment',
    'Turn your best validation logic into reusable templates and tools'
  ], true, 15, C.coral);
  addInfoCard(s, 0.8, 4.95, 5.45, 0.95, 'Final framing', ['Each solution has prerequisites', 'Each solution has limitations', 'Design consciously — do not promise magic'], true, C.teal);
  [
    {x:7.02,y:4.42,w:5.05,h:0.9,color:'30414A',label:'PBIP / Git + Copilot / KB',sub:'What enables repeatability'},
    {x:7.55,y:3.48,w:3.98,h:0.82,color:C.teal,label:'Guardrails / Validation Gates',sub:'What keeps trust'},
    {x:8.08,y:2.62,w:2.92,h:0.72,color:C.coral,label:'Insights & Visuals',sub:'What users see'},
  ].forEach((layer)=>{
    s.addShape(pptx.ShapeType.roundRect,{x:layer.x,y:layer.y,w:layer.w,h:layer.h,rectRadius:0.06,fill:{color:layer.color},line:{color:layer.color},shadow:safeOuterShadow('000000',0.16,45,2,1)});
    s.addText(layer.label,{x:layer.x+0.18,y:layer.y+0.2,w:layer.w-0.36,h:0.18,fontFace:'Segoe UI',fontSize:15.5,bold:true,color:C.white,margin:0,align:'center',fit:'shrink'});
    s.addText(layer.sub,{x:layer.x+0.18,y:layer.y+0.5,w:layer.w-0.36,h:0.12,fontFace:'Segoe UI',fontSize:10.5,color:'E5EEF2',margin:0,align:'center'});
  });
  s.addShape(pptx.ShapeType.line,{x:9.55,y:3.32,w:0,h:0.14,line:{color:'94D8D2',pt:1.2,endArrowType:'triangle'}});
  s.addShape(pptx.ShapeType.line,{x:9.55,y:4.26,w:0,h:0.14,line:{color:'94D8D2',pt:1.2,endArrowType:'triangle'}});
  s.addText('Trust scales when the foundation is engineered, not improvised.', {x:7.0,y:5.6,w:5.3,h:0.22,fontFace:'Segoe UI',fontSize:11.5,color:'B9C9D1',align:'center',margin:0});
  addTakeaway(s, 'The question is not whether AI can help build Power BI faster. The question is whether your BI platform is engineered well enough to let AI operate safely.', true);
  s.addNotes(notesWithSources(`ผมอยากปิดด้วยภาพนี้ครับ
สิ่งที่ผู้ใช้เห็นคือ insights และ visuals แต่สิ่งที่ทำให้มันน่าเชื่อถือคือชั้น guardrails และ foundation ด้าน model as code กับ custom toolbox
เพราะฉะนั้นเวลาเราพูดถึง AI ในงาน BI ผมคิดว่าคำถามไม่ใช่แค่ว่า AI ทำให้เราสร้างได้เร็วขึ้นไหม
แต่คือ platform ของเราถูกออกแบบมาดีพอหรือยัง ที่จะให้ AI เข้ามาช่วยทำงานได้อย่างปลอดภัยและตรวจสอบได้
และผมตั้งใจใส่ prerequisite กับ limitation ของแต่ละแนวทางไว้ใน deck นี้ เพราะในโลก enterprise ไม่มี solution ไหนเป็น magic ครับ มีแต่ solution ที่ออกแบบอย่างรู้ขอบเขตของมัน`));
});

slides.forEach(fn => fn());

// Validate a subset of cleaner slides (tables and full-slide artwork can create false positives)
[1,2,8,10,12].forEach(idx => {
  const sl = pptx._slides[idx];
  if (sl) {
    warnIfSlideHasOverlaps(sl, pptx);
    warnIfSlideElementsOutOfBounds(sl, pptx);
  }
});

(async () => {
  await pptx.writeFile({ fileName: path.join(__dirname, 'community_meetup_pbir_copilot_v9.pptx') });
})();
