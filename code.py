import pymysql
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Ds@270705",
        database="students",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/students")
def get_students_info():
    return {"message": "Please connect your tablename"}

class Student(BaseModel):
    id: int
    name: str
    course: str

@app.get("/students/{table_name}")
def get_students(table_name: str):
    try:
        allowed_tables = ["student1", "student2", "student3"]
        if table_name not in allowed_tables:
            return {"error": "Invalid table name"}
        
        connection = get_db()
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return {"data": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/students")
def add_student(student: Student):
    try:
        connection = get_db()
        cursor = connection.cursor()

        cursor.callproc("add_student", (student.id, student.name, student.course))
        connection.commit()

        cursor.execute("SELECT * FROM student1")
        s1 = cursor.fetchall()

        cursor.execute("SELECT * FROM student2")
        s2 = cursor.fetchall()

        cursor.execute("SELECT * FROM student3")
        s3 = cursor.fetchall()

        cursor.close()
        connection.close()

        return {"message": "Student added to all 3 tables", "student1": s1, "student2": s2, "student3": s3}
    except Exception as e:
        return {"error": str(e)}