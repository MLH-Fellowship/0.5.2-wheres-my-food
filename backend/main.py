import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status, Request, Response, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.schemas.user_schemas import User, UserCreate
from db.schemas.order_schemas import Order, OrderCreate
from typing import List
from datetime import datetime, timedelta
from auth.auth import authenticate_user, create_access_token
from auth.auth_schema import Token
from db import models, crud
from db.database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm
from auth.auth import get_current_active_user, get_admin_user

app = FastAPI()

origins = ["http://localhost", "http://localhost:8000", "http://localhost:5000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def health_check():
    return {"status": "cool 😎"}


@app.post("/token", response_model=Token)
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    import logging

    logger = logging.getLogger("api")
    logger.debug(form_data)
    print(form_data.username)
    print(form_data.password)
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    response.set_cookie(key="wmf_cookie", value=access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=User)
async def get_me(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_user = crud.get_user(db, user_id=current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/", response_model=User)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_admin_user), # This is commented for development and testin purposes
):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/orders/{email}", response_model=List[Order])
def get_order_for_user(
    email: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    orders = crud.get_users_orders(email=email, db=db, skip=skip, limit=limit)
    return orders
    

@app.post("/orders/", response_model=Order)
def create_order_for_user(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    existing_order = crud.get_order_by_foreign_id(db, order.order_id, order.platform_id)
    if existing_order is None:
        return crud.create_user_order(db=db, order=order)
    raise HTTPException(
        status_code=400, detail="Order ID already exists for that platform"
    )


@app.put("/orders/", response_model=Order)
def update_order_for_user(
    order_id=str,
    platform_id=int,
    new_status=int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    return crud.update_user_order(db, order_id, platform_id, new_status)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
