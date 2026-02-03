from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Nested dictionary (database)
employees = {
    100: {
        "name": "John",
        "age": 30,
        "address": {
            "city": "Chennai",
            "pincode": 600001
        }
    },
    101:{
        "name":"Kani",
        "age":30,
        "address":{
            "city":"Bangalore",
            "pincode":560001
        }
    }
}

# ---------- Pydantic Models ----------

class Address(BaseModel):
    city:Optional[str]=None
    pincode:Optional[int]=None

class Employee(BaseModel):
    id:int
    name:Optional[str]=None
    age:Optional[int]=None
    address:Optional[Address]=None

@app.get("/")
def read_root():
    return {"message": "Welcome to the Employee API"}

# ---------- GET METHOD ----------
@app.get("/employees")
def get_employees():
    return employees

# ---------- POST METHOD ----------
@app.post("/employees")
def add_employee(emp: Employee):
    new_id = emp.id

    employees[new_id] = {
        "name": emp.name,
        "age": emp.age,
        "address": {
            "city": emp.address.city,
            "pincode": emp.address.pincode
        }
    }

    return employees

@app.delete("/employees")
def delete_employee(emp:Employee):
    if emp.id in employees:
        deleted_data=employees.pop(emp.id)
        return{"message":f"Employee with id {emp.id} has been deleted",
               "data": employees
               }
    else:
        return{"message":f"Employee with id {emp.id} not found"}
    
@app.patch("/employees")
def patch_employee(emp:Employee):
    if emp.id not in employees:
        return{"message":f"Employee id {emp.id} not found"}
    
    if emp.name is not None:
        employees[emp.id]["name"]=emp.name
        
    if emp.age is not None:
        employees[emp.id]["age"]=emp.age

    if emp.address is not None:
        if emp.address.city is not None:
            employees[emp.id]["address"]["city"]=emp.address.city
        if emp.address.pincode is not None:
            employees[emp.id]["address"]["pincode"]=emp.address.pincode
    return employees

@app.put("/employees")
def put_employee(emp:Employee):
    employees[emp.id]={
        "name": emp.name,
        "age": emp.age,
        "address": {
            "city": emp.address.city,
            "pincode": emp.address.pincode
        }
    }
    return employees[emp.id]