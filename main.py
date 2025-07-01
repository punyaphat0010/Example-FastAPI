# main.py

from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/items")
def create_item(item: Item):
    return { "request_body": item }

@app.put("/item/{item_id}")
def update_item(item_id: int, item: Item):
    return {"id": item_id, "request_body": item}

@app.delete("/item/{item_id}")
def delete(item_id: int):
    return {"message": f"Item {item_id} delete"}