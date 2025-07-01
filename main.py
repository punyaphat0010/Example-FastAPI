# main.py

from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from fastapi import FastAPI, Depends, HTTPException
from typing import Union, List, Optional
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ItemDB(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)

Base.metadata.create_all(bind=engine)

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True



app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/", response_model=List[ItemResponse])
async def read_all_items(db: Session = Depends(get_db)):
    return db.query(ItemDB).all()

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemDB(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/item/{item_id}")
def update_item(item_id: int, item: ItemBase):
    return {"id": item_id, "request_body": item}

@app.delete("/item/{item_id}")
def delete(item_id: int):
    return {"message": f"Item {item_id} delete"}