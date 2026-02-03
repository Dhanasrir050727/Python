from fastapi import FastAPI
import pymysql
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

app=FastAPI()

load_dotenv("sql_py.env")

class Worker(BaseModel):
    id:Optional[int]=None
    name:Optional[str]=None
    salary:Optional[int]=None

def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor 
        )

@app.get("/")
def root():
    return{
        "message":"Database is connected"
    }

#----------- Show the table -------------
@app.get("/workers")
def get_worker():
    connection=get_db()
    cursor=connection.cursor()

    sql="select * from workers"
    cursor.execute(sql)
    result=cursor.fetchall()

    connection.close()
    return result

#----------- insert one row -------------
@app.post("/workers")
def post_worker(work:Worker):
        connection=get_db()
        cursor=connection.cursor()

        sql="insert into workers(id,name,salary)values(%s,%s,%s)"
        cursor.execute(sql,(work.id,work.name,work.salary))
        connection.commit()

        cursor.execute("select * from workers")
        all_data=cursor.fetchall()
        connection.close()
        return{
            "Message":"The new row have been added",
            "data":all_data
        }

#----------- remove one row -------------
@app.delete("/workers")
def delete_worker(work:Worker):
     connection=get_db()
     cursor=connection.cursor()

     sql="delete from workers where id=%s"
     cursor.execute(sql,(work.id,))
     connection.commit()

     cursor.execute("select * from workers")
     all_data=cursor.fetchall()
     connection.close()

     return{
        "Message":"The row have been deleted",
        "data":all_data
    }

#----------- update one row -------------
@app.patch("/workers")
def patch_worker(work: Worker):
    connection = get_db()
    cursor = connection.cursor()

    # name + salary
    if work.name is not None and work.salary is not None:
        cursor.execute(
            "UPDATE workers SET name=%s, salary=%s WHERE id=%s",
            (work.name, work.salary, work.id)
        )

    # only name
    elif work.name is not None:
        cursor.execute(
            "UPDATE workers SET name=%s WHERE id=%s",
            (work.name, work.id)
        )

    # only salary
    elif work.salary is not None:
        cursor.execute(
            "UPDATE workers SET salary=%s WHERE id=%s",
            (work.salary, work.id)
        )

    else:
        return {"message": "Nothing to update"}

    connection.commit()

    cursor.execute("SELECT * FROM workers")
    data = cursor.fetchall()

    connection.close()

    return {
        "message": "Updated successfully",
        "data": data
    }

#----------- replace the table -------------
@app.put("/workers")
def put_worker(work:Worker):
    connection=get_db()
    cursor=connection.cursor()

    cursor.execute("truncate table workers")

    sql="insert into workers(id,name,salary)values(%s,%s,%s)"
    cursor.execute(sql,(work.id,work.name,work.salary))
    connection.commit()

    cursor.execute("select * from workers")
    data=cursor.fetchall()
    connection.close()

    return{
        "message":" The table have been replaced",
        "data":data
    }