# Thai Presenter Notes

## Repo overview
อันนี้คือ repo ตัวอย่างที่ตั้งใจออกแบบให้เดโมง่ายครับ ด้านหน้าจะเป็น notebook เพื่อให้คนที่ไม่ใช่ developer ก็เห็น flow ได้ทันที  
ส่วนด้านหลังจะเป็น scripts แยกเป็นชิ้น ๆ เพื่อให้ทีมเทคนิคเอาไป reuse ต่อได้จริง  
แนวคิดคือ ทำให้เดโมดูง่าย แต่โครงสร้างยัง professional และขยายต่อได้

## PBIP sample
ตัวอย่างนี้ใช้ business case เรื่อง regional sales performance เพราะคนดูเข้าใจเร็ว  
data model ตั้งใจทำเป็น star schema เล็ก ๆ มี fact sales แล้วก็ dimension date, region, product, channel  
มันเล็กพอที่จะอธิบายบนสไลด์ได้ แต่ก็ยังพอให้เห็นภาพเรื่อง report, measure, และ DAX query

## Scripts
ส่วน scripts ผมแยกตามหน้าที่ชัดเจนครับ  
มี auth_service_principal, auth_delegated_user, ตัว load config, ตัว list workspaces, list datasets และ execute dax query  
เวลาพรีเซนต์ให้เน้นว่า notebook ไม่ได้เขียน logic ทุกอย่างซ้ำ แต่เรียกใช้ script พวกนี้อีกที ทำให้ maintain ง่าย

## Notebook demo
notebook จะเป็น entry point หลักของเดโม  
ไล่จาก load config ก่อน จากนั้นเลือก auth mode  
แล้วค่อย list workspace, list dataset, และยิง DAX query  
ข้อดีคือ audience จะเห็นผลลัพธ์เป็น table กับ chart ได้ทันที ไม่ต้องตาม command line เยอะ

## Service principal vs delegated auth
ถ้าเป็น service principal ให้เล่าว่าเหมาะกับ automation หรือ process ที่ไม่ต้องผูกกับ user คนใดคนหนึ่ง  
แต่ถ้าเป็น delegated auth จะเหมาะกับกรณีที่อยากให้การเข้าถึงสะท้อนสิทธิ์ของ user จริง  
จุดสำคัญที่ควรพูดคือ ถ้ามี RLS แล้วจะเป็นประเด็นมากขึ้น เพราะ service principal ไม่ใช่ทางที่เหมาะสำหรับ executeQueries บน dataset แบบนั้น

## Limitations and prerequisites
ตรงนี้ควรพูดตรง ๆ เลยครับว่า demo นี้ขึ้นกับ tenant settings และ permission จริงใน environment  
อีกเรื่องคือ executeQueries รองรับ DAX เท่านั้น  
แล้วถ้าจะทำเดโมให้ลื่นที่สุด ควรใช้ dataset หลักที่ยังไม่เปิด RLS ก่อน  
ถ้าจะสาธิต RLS ค่อยแยกเป็น advanced scenario เพิ่มอีกชุดหนึ่ง
