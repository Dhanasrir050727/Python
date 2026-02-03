from fastapi import APIRouter,HTTPException
from db import db
from models import attendance

router=APIRouter()

@router.get("/{s_id}")
def show_attendance(s_id:int):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        sql="select * from attendance where student_id=%s"
        cursor.execute(sql,(s_id,))
        result=cursor.fetchone()

        return{"data":result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    finally:
        if connection:
            connection.close()

@router.post("/")
def mark_attendance(a:attendance):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        sql="insert into attendance(student_id,attendance_date,status) values(%s,%s,%s)"
        cursor.execute(sql,(a.s_id,a.a_date,a.status))
        connection.commit()

        return {"Message":"Attendance marked successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        if connection:
            connection.close()
