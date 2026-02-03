from fastapi import FastAPI
import pymysql
from pydantic import BaseModel
from typing import Optional

app=FastAPI()

class Student(BaseModel):
    id:Optional[int]=None
    name:Optional[str]=None
    course:Optional[str]=None
    
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
    return{"Database connected successfully"}

@app.get("/students")
def get_st():
    connection=get_db()
    cursor=connection.cursor()

    sql="select * from student1"
    cursor.execute(sql)
    result=cursor.fetchall()

    connection.close()

    return{"data":result}

@app.post("/students")
def post_stu(stu:Student):
    connection=get_db()
    cursor=connection.cursor()

    sql="insert into student1(id,name,course)values(%s,%s,%s)"
    cursor.execute(sql,(stu.id,stu.name,stu.course))

    sql="select * from student1"
    cursor.execute(sql)
    r1=cursor.fetchall()

    sql="select * from student2"
    cursor.execute(sql)
    r2=cursor.fetchall()
    

    sql="select * from student3"
    cursor.execute(sql)
    r3=cursor.fetchall()
    
    connection.commit()
    connection.close()

    return{
        "message":"The new row have been added",
        "data1":r1,
        "data2":r2,
        "data3":r3
    }

@app.delete("/students")
def delete_stu(stu:Student):
    connection=get_db()
    cursor=connection.cursor()

    sql="delete from student1 where id=%s"
    cursor.execute(sql,(stu.id,))
    connection.commit()

    sql="select * from student1"
    cursor.execute(sql)
    result=cursor.fetchall()
    connection.close()

    return{
        "message":"The row have been updated",
        "data":result
    }
