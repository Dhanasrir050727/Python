from fastapi import FastAPI
from pydantic import BaseModel

details=FastAPI()

data_dict=[
    {
        "id":1,"name":"Alice","age":30
    },
    {
        "id":2,"name":"Bob","age":25
    }
]

class Post_User(BaseModel):
    id:int
    name:str
    age:int

class Delete_User(BaseModel):
    id:int

class Patch_User(BaseModel):
    id:int
    name:str

class Put_Users(BaseModel):
    new:list[dict]

@details.get("/")
def root():
    return {"message": "API is running"}

# ---------- GET ----------
@details.get("/users")
def get_users():
    return data_dict

# ---------- POST (add user) ----------
@details.post("/users")
def post_user(user:Post_User):
    data_dict.append(user.dict())
    return data_dict

# ---------- DELETE (remove user by id) ----------
@details.delete("/users")
def delete_user(user:Delete_User):
    global data_dict
    data_dict=[u for u in data_dict if u["id"]!=user.id]
    return data_dict

# ---------- PATCH (update user name by id) ----------
@details.patch("/users")
def patch_user(user:Patch_User):
    for u in data_dict:
        if u["id"]==user.id:
            u["name"]=user.name
            return data_dict
    return {"error":"User not found"}

# ---------- PUT (replace full user list) ----------
@details.put("/users")
def put_users(users:Put_Users):
    global data_dict
    data_dict=users.new
    return data_dict