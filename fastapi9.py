from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Sample in-memory data store
items = []

# Item model
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

# Create item endpoint
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    # Check if item with same ID already exists
    if any(existing_item.id == item.id for existing_item in items):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items.append(item)
    return item

# Read all items endpoint
@app.get("/items/", response_model=List[Item])
def read_items():
    return items

# Read single item endpoint
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = next((item for item in items if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Update item endpoint
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items):
        if item.id == item_id:
            items[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

# Delete item endpoint
@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    global items
    items = [item for item in items if item.id != item_id]
    return {"message": "Item deleted"}

