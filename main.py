# from fastapi import FastAPI

# app = FastAPI()

# items = []

# @app.get("/")
# def root():
#     return {"Hello ABdeljalil" : "YouCode"}

# @app.post("/items")
# def create_item(item: str):
#     items.append(item)
#     return item

# @app.get("/items/{item_id}")
# def get_item(item_id: int) -> str:
#     item = items[item_id]
#     return item



from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import database

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@app.post("/users/", response_model=models.User)
def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
    db_user = database.UserModel(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# READ
@app.get("/users/{user_id}", response_model=models.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(database.UserModel).filter(database.UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=list[models.User])
def read_users(db: Session = Depends(get_db)):
    return db.query(database.UserModel).all()

# UPDATE
@app.put("/users/{user_id}", response_model=models.User)
def update_user(user_id: int, user: models.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(database.UserModel).filter(database.UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

# DELETE
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(database.UserModel).filter(database.UserModel.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}
