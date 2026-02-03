from fastapi import FastAPI
import psycopg2
from psycopg2.extras import DictCursor

app=FastAPI()

def db():
    return psycopg2.connect(
        host="localhost",
        database="school",
        user="postgres",
        password="Ds@270705",
    )
@app.get("/")
def root():
    return{"message":"Api is running."}

@app.get("/student1")
def get_student():
    connection=db()
    cursor=connection.cursor(cursor_factory=DictCursor)

    cursor.execute("SELECT * FROM student1;")
    result=cursor.fetchall()

    connection.close()

    st=[dict(row) for row in result]
    return{"students":st}