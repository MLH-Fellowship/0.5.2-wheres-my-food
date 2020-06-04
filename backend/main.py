import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from db.schemas.user_schemas import User, UserCreate
from db.schemas.order_schemas import Order, OrderCreate
from typing import List
from fastapi.staticfiles import StaticFiles
from db import models, crud
from db.database import SessionLocal, engine
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/test/", response_model=Order)
def create_order_for_user(order: OrderCreate, db: Session = Depends(get_db)):
    return {"message":"Hi from post"}


@app.post("/orders/", response_model=Order)
def create_order_for_user(order: OrderCreate, db: Session = Depends(get_db)):
    return crud.create_user_order(db=db, order=order)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
