from fastapi import FastAPI, HTTPException
import pymysql
from pydantic import BaseModel
from typing import Optional
from contextlib import contextmanager

app = FastAPI()

@contextmanager
def get_db():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="Ds@270705",
        database="school_management",
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        yield connection
    finally:
        connection.close()

class Student(BaseModel):
    student_id: Optional[int] = None
    admission_no: str
    student_name: str
    gender: str
    dob: str
    phone: str
    address: str
    class_id: int
    section_id: int

@app.get("/")
def root():
    return {"message": "Student API is running"}

@app.get("/students")
def get_all_students():
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        return {"data": cursor.fetchall()}

@app.get("/students/{student_id}")
def get_student(student_id: int):
    with get_db() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id=%s", (student_id,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
        
        return {"data": result}

@app.post("/students")
def add_student(student: Student):
    with get_db() as connection:
        cursor = connection.cursor()
        
        sql = """INSERT INTO students(admission_no, student_name, gender, dob, phone, address, class_id, section_id) 
                 VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (student.admission_no, student.student_name, student.gender, 
                            student.dob, student.phone, student.address, 
                            student.class_id, student.section_id))
        connection.commit()
        
        return {"message": "Student added successfully", "id": cursor.lastrowid}

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    with get_db() as connection:
        cursor = connection.cursor()
        
        sql = """UPDATE students SET admission_no=%s, student_name=%s, gender=%s, dob=%s, 
                 phone=%s, address=%s, class_id=%s, section_id=%s WHERE student_id=%s"""
        cursor.execute(sql, (student.admission_no, student.student_name, student.gender,
                            student.dob, student.phone, student.address,
                            student.class_id, student.section_id, student_id))
        connection.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
        
        return {"message": "Student updated successfully"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    with get_db() as connection:
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
        connection.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
        
        return {"message": f"Student {student_id} deleted successfully"}
