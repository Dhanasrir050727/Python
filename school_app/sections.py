from fastapi import APIRouter,HTTPException
from db import db
from models import Section

router=APIRouter()

@router.get("/")
def get_section():
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        sql="select * from sections"
        cursor.execute(sql)
        result=cursor.fetchall()

        return{"data":result}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        if connection:
            connection.close()

@router.post("/")
def add_section(sec:Section):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        sql="select * from sections where section_id=%s"
        cursor.execute(sql,(sec.sec_id))
        result=cursor.fetchone()

        if result:
            raise HTTPException(status_code=400,detail=f"Section {sec.sec_id} already exists")
        
        sql="insert into sections(section_id,section_name,class_id) values(%s,%s,%s)"
        cursor.execute(sql,(sec.sec_id,sec.sec_name,sec.c_id))
        connection.commit()

        return {"Message":"Section added successfully","data":sec.dict()}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        if connection:
            connection.close()
