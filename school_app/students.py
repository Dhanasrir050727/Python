from fastapi import APIRouter,HTTPException
from db import db
from models import Student,StudentPost

router=APIRouter()

@router.get("/{id}")
def get_student(id:int):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        sql="select * from students where student_id=%s"
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
def add(s:StudentPost):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        sql="select * from students where admission_no=%s"
        cursor.execute(sql, (s.a_no, ))
        result=cursor.fetchone()
        if result:
            raise HTTPException(status_code=400,detail=f"Admission number {s.a_no} already exists")
        
        sql="insert into students(admission_no,student_name,gender,dob,phone,address,class_id,section_id) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,(s.a_no,s.name,s.gender,s.dob,s.phone,s.address,s.c_id,s.sec_id))
        connection.commit()

        return {"Message":"Student added successfully", "data": s.dict()}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        if connection:
            connection.close()

@router.patch("/{id}")
def patch_data(id: int, s: Student):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        fields=[]
        values=[]

        if s.name is not None:
            fields.append("student_name=%s")
            values.append(s.name)

        if s.dob is not None:
            fields.append("dob=%s")
            values.append(s.dob)

        if s.address is not None:
            fields.append("address=%s")
            values.append(s.address)

        if s.phone is not None:
            fields.append("phone=%s")
            values.append(s.phone)
        
        if s.c_id is not None:
            fields.append("class_id=%s")
            values.append(s.c_id)

        if s.sec_id is not None:
            fields.append("section_id=%s")
            values.append(s.sec_id)

        if not fields:
            raise HTTPException(status_code=400, detail="No data to update")

        values.append(id)

        sql=f"UPDATE students SET {', '.join(fields)} WHERE student_id=%s"
        cursor.execute(sql, tuple(values))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {"message": "Student updated successfully"}

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if connection:
            connection.close()


@router.put("/{id}")
def put_st(id:int,s:StudentPost):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        cursor.execute("SELECT * FROM students WHERE student_id=%s",(id,))
        result=cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail=f"Student {id} not found")
        
        sql="Update students set admission_no=%s,student_name=%s,gender=%s,dob=%s,phone=%s,address=%s,class_id=%s,section_id=%s where student_id=%s"
        cursor.execute(sql,(s.a_no,s.name,s.gender,s.dob,s.phone,s.address,s.c_id,s.sec_id,id))
        connection.commit()

        return {"Message":"Student updated successfully", "data": s.dict()}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    finally:
        if connection:
            connection.close()


@router.delete("/{id}")
def delete(id:int):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor()

        related_tables=[
            "attendance",
            "marks",
            "fees"
        ]
        # delete from child tables
        for table in related_tables:
            cursor.execute(
                f"DELETE FROM {table} WHERE student_id=%s",
                (id,)
            )

        # delete from parent table
        cursor.execute(
            "DELETE FROM students WHERE student_id=%s",
            (id,)
        )

        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {"message": "Student deleted from all related tables"}

    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if connection:
            connection.close()
