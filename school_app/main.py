from fastapi import FastAPI
from students import router as student_router
from sections import router as section_router
from subjects import router as subject_router
from teachers import router as teacher_router
from attendance import router as attendance_router

app=FastAPI()

app.include_router(student_router,prefix="/students")
app.include_router(section_router,prefix="/sections")
app.include_router(subject_router,prefix="/subjects")
app.include_router(teacher_router,prefix="/teachers")
app.include_router(attendance_router, prefix="/attendance")

@app.get("/")
def root():
    return {"message":"Api is running"}