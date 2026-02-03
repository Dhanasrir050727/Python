from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# ----- Sample array -----
my_array = [10, 20, 30, 40]

# ----- Pydantic model to validate POST data -----
class Item(BaseModel):
    value: int  # we expect a number

# ----- GET: Return the array -----
@app.get("/array")
def get_array():
    return my_array  # FastAPI automatically converts to JSON

# ----- POST: Add a new number to the array -----
@app.post("/array")
def add_item(item: Item):
    my_array.append(item.value)  # Add the new number
    return {"message": f"{item.value} added successfully", "array": my_array}
