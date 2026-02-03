from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pymysql

app = FastAPI()

# Pydantic model for menu item
class MenuItem(BaseModel):
    id: int
    re_name: str
    price: float
    force_error: Optional[bool] = False 

# Function to get DB connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Ds@270705',
        database='numbers'
    )

@app.get("/")
def read_root():
    return {"Message": "Welcome to the Menu API"}

@app.get("/{table_name}")
def get_menus(table_name: str):
    """Fetch all menu items from a specific table"""
    connection = get_db_connection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        results = cursor.fetchall()
        return {"menus": results}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

@app.post("/add_menu")
def add_menu(item: MenuItem):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        tables = ['menu1', 'menu2', 'menu3'] 
        for table in tables:
            if table == 'menu2' and item.force_error:
                # Simulate an error on menu2 for testing rollback
                raise Exception("Simulated error on menu2 insert")
            
            sql = f"INSERT INTO {table} (id, re_name, price) VALUES (%s, %s, %s)"
            cursor.execute(sql, (item.id, item.re_name, item.price))

        # Commit all inserts if no error
        connection.commit()
        return {"message": "All menu items committed successfully!"}

    except Exception as e:
        # Rollback if any error occurs
        connection.rollback()
        return {"error": str(e), "message": "All changes rolled back!"}

    finally:
        cursor.close()
        connection.close()
