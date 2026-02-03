from fastapi import APIRouter,HTTPException
from db import db
from models import Teachers

router=APIRouter()

@router.get("/{id}")
def get_teach(id:int):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        sql="select * from teachers where teacher_id=%s"
        cursor.execute(sql,(id,))

        result=cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail=f"Student {id} not found")
        return{"data":result}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
    finally:
        if connection:
            connection.close()

@router.post("/")
def add(t:Teachers):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        sql="select * from teachers where teacher_id=%s"
        cursor.execute(sql, (t.teach_id, ))
        result=cursor.fetchone()
        if result:
            raise HTTPException(status_code=400,detail=f"Admission number {t.teach_id} already exists")
        
        sql="insert into teachers(teacher_id,teacher_name,phone,email,joining_date) values(%s,%s,%s,%s,%s)"
        cursor.execute(sql,(t.teach_id,t.teach_name,t.phone,t.email,t.join_date))
        connection.commit()

        return {"Message":"Student added successfully", "data": t.dict()}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        if connection:
            connection.close()