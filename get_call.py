from fastapi import FastAPI,HTTPException
import pymysql
from pydantic import BaseModel

app=FastAPI()

class add(BaseModel):
    a_no:str
    name:str
    gender:str
    dob:str
    phone:str
    address:str
    c_id:int
    sec_id:int

def db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Ds@270705",
        database="school_management",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/")
def root():
    return {"message":"Api is running"}

@app.get("/favicon.ico")
def favicon():
    return{"Message":"Nothing"}

@app.get("/students/{id}")
def get_student(id:int):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        sql="select * from students where student_id=%s"
        cursor.execute(sql,(id,))
        re=cursor.fetchone()

        if re is None:
            raise HTTPException(status_code=404,detail=f"Student {id} not found")
    
        return {"data":re}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if connection:
            connection.close()

@app.post("/students/")
def add_student(s:add):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        sql="select * from students where admission_no=%s,(s.a_no,)"
        if cursor.fetchone:
            raise HTTPException(status_code=400,detail=f"Admission number {s.a_no} already exists")
        
        sql="insert into students(admission_no,student_name,gender,dob,phone,address,class_id,section_id) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(s.a_no,s.name,s.gender,s.dob,s.phone,s.address,s.c_id,s.sec_id))
        connection.commit()

        sql="select * from students"
        cursor.execute(sql)

        return {"Message":"Student added successfully", "data": s.dict()}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        if connection:
            connection.close()
