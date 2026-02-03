from fastapi import FastAPI
import pymysql

app=FastAPI()

def db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Ds@270705",
        database="school_management",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/school/{id}")
def read_st(id:int):
    try:
        connection=db()
        cursor=connection.cursor()

        cursor.execute("select * from students where student_id=%s",(id,))
        result=cursor.fetchone()

        if result is None:
            return{"Message":f"No student found with ID {id}"}

        return{"data":result}
    except Exception as e:
        return{"error":str(e)}
    
    finally:
        if connection:
            connection.close()