from fastapi import APIRouter,HTTPException
from db import db
from models import Subject

router=APIRouter()

@router.get("/")
def get_sub():
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        sql="select * from subjects"
        cursor.execute(sql)
        result=cursor.fetchall()
        
        return{"data":result}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        if connection:
            connection.close()


@router.post("/")
def add_sub(sub:Subject):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        sql="select * from subjects where subject_id=%s"
        cursor.execute(sql,(sub.sub_id,))
        result=cursor.fetchone()

        if result:
            raise HTTPException(status_code=400,detail=f"subject id {sub.sub_id} already exists")
        
        sql="insert into subjects(subject_id,subject_name,teacher_id) values(%s,%s,%s)"
        cursor.execute(sql,(sub.sub_id,sub.sub_name,sub.teach_id))
        connection.commit()

        return {"Message":"subtion added successfully","data":sub.dict()}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        if connection:
            connection.close()