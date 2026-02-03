from fastapi import FastAPI,HTTPException
import psycopg2
from psycopg2.extras import DictCursor
from pydantic import BaseModel
from typing import Optional

app=FastAPI()

class postemp(BaseModel):
    id:int
    name:str
    email:str
    j_id:int

class patchemp(BaseModel):
    name:Optional[str]=None
    email:Optional[str]=None
    j_id:Optional[int]=None

class putemp(BaseModel):
    name:str
    email:str
    j_id:int

def db():
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="Ds@270705",
        database="employee"
    )

@app.get("/")
def get_data():
    return {"message":"Welcome to postgreSQL API's"}

@app.get("/employee")
def get_employees():
    connection=None
    try:
        connection=db()
        cursor=connection.cursor(cursor_factory=DictCursor)

        cursor.execute("select * from employee1")
        result=cursor.fetchall()

        result=[dict(row) for row in result]
        return{"data":result}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
    finally:
        if connection:
            connection.close()

@app.get("/employee/{emp_id}")
def get_employee(emp_id:int):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor(cursor_factory=DictCursor)

        cursor.execute("select * from employee1 where id=%s",(emp_id,))
        result=cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404,detail="Employee not found")
        return{"data":dict(result)}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
    finally:
        if connection:
            connection.close()

@app.delete("/employee/{emp_id}")
def delete_employee(emp_id:int):
     connection=None
     try:
        connection=db()
        cursor=connection.cursor(cursor_factory=DictCursor)
        
        cursor.execute("delete from employee1 where id=%s returning *",(emp_id,))
        result=cursor.fetchone()

        if cursor.rowcount==0:
            raise HTTPException(status_code=404,detail=f"Employee {emp_id} id not found")
            
        connection.commit()

        return{"message":"Employee deleted successfully",
               "deleted record is ":dict(result)}
     
     except Exception as e:
         raise HTTPException(status_code=500,detail=str(e))
     finally:
         if connection:
             connection.close()

@app.post("/employee")
def add_employee(emp:postemp):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor(cursor_factory=DictCursor)

        cursor.execute("insert into employee1(id, name, email, job_id) values(%s, %s, %s, %s) returning *", 
                      (emp.id, emp.name, emp.email, emp.j_id))
        result=cursor.fetchone()
        connection.commit()

        return{"message":"Employee added successfully", "data":dict(result)}
    
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
    finally:
        if connection:
            connection.close()

@app.patch("/employee/{emp_id}")
def update_employee(emp_id:int, emp:patchemp):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor(cursor_factory=DictCursor)

        query="update employee1 set "
        params=[]

        if emp.name is not None:
            query+="name=%s, "
            params.append(emp.name)
        if emp.email is not None:
            query+="email=%s, "
            params.append(emp.email)
        if emp.j_id is not None:
            query+="job_id=%s, "
            params.append(emp.j_id)

        if not params:
            raise HTTPException(status_code=400, detail="No fields to update")

        query=query.rstrip(", ")
        query+=" where id=%s returning *"
        params.append(emp_id)

        cursor.execute(query, params)
        result=cursor.fetchone()

        if cursor.rowcount==0:
            raise HTTPException(status_code=404, detail=f"Employee {emp_id} id not found")

        connection.commit()

        return{"message":"Employee updated successfully", "data":dict(result)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if connection:
            connection.close()

@app.put("/employee/{emp_id}")
def put_employee(emp_id:int,emp:putemp):
    connection=None
    try:
        connection=db()
        cursor=connection.cursor(cursor_factory=DictCursor)

        cursor.execute("update employee1 set name=%s,email=%s,job_id=%s where id=%s returning *",(emp.name,emp.email,emp.j_id,emp_id))
        result=cursor.fetchone()

        if result is None:
            raise HTTPException(status_code=404,detail="Employee not found")
        connection.commit()
        return{"message":"Employee updated successfully","data":dict(result)}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
    finally:
        if connection:
            connection.close()  
