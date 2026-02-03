import pymysql
import os
from dotenv import load_dotenv

load_dotenv("sql_py.env")

connection=pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database="sample"
)

print("\n Database connected successfully\n")

cursor=connection.cursor()


#------------- table show ---------------
sql="SELECT * FROM employee"
cursor.execute(sql)

result=cursor.fetchall()

for r in result:
    id,name,role=r
    print(f" Id : {id}, Name : {name}, role: {role}")

print("\n Database connection closed\n")

connection.close()