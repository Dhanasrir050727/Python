from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

a=[67,33,18,7]

class Post_Item(BaseModel):
    value:int

class Patch_Item(BaseModel):
    index:int
    value:int

class Delete_Item(BaseModel):
    index:int

class Put_Item(BaseModel):
    array:list[int]

@app.get("/")
def root():
    return {"message":"API is running"}

# ---------- GET ----------
@app.get("/data")
def get_data():
    return a

# ---------- POST (add value) ----------
@app.post("/data")
def post_data(item:Post_Item):
    a.append(item.value)
    return a

# ---------- PATCH (update by index) ----------
@app.patch("/data")
def patch_data(item:Patch_Item):
    a[item.index]=item.value
    return a

# ---------- DELETE (remove by index) ----------
@app.delete("/data")
def delete_data(item:Delete_Item):
    a.pop(item.index)
    return a

# ---------- PUT (replace full array) ----------
@app.put("/data")
def put_data(item:Put_Item):
    a=item.array
    return a