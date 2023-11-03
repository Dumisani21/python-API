from fastapi import FastAPI, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


storage = {
        1: {
            "name" : "Shampoo",
            "price" : 50.0,
            "brand" : "Head & Shoulders"
            }
        }

@app.get("/get-item/{item_id}")
def get_item(item_id: int):
    if item_id in storage:
        return storage[item_id]
    return {"msg": "item does not exists"}

@app.get("/get-by-name")
def get_item(name: str = None):
    for item_id in storage:
        if storage[item_id]["name"] == name:
            return storage[item_id]
    raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Item name not found")


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in storage:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Item ID already exists")

    storage[item_id] = {"name": item.name, "price": item.price, "brand": item.brand}
    return {"msg": "item inserted successfully"}


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in storage:
        return {"Error": "Item ID does not exists"}

    storage.update(item)
    return item

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item you want to deletef")):
    if item_id in storage:
        del storage[item_id]
        return {"msg": "item was deleted"}
    return HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Item ID does not exists")
