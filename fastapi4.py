from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float= None

@app.post("/items/")
async def create_item(item:Item):
    return item