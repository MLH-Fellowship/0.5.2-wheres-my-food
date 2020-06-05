import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
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


@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register")
def login(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/dashboard")
def login(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=User)
async def get_me(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
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
    user = crud.create_user(db=db, user=user)
    return user


# @app.get("/dashboard/<int:user_id>'")
# def dashboard(request: Request):
#     return templates.TemplateResponse("register.html", {"request": request})


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
    return templates.TemplateResponse(
        "users.html", {"request": request, "user_id": user_id}
    )


@app.post("/test/", response_model=Order)
def create_order_for_user(order: OrderCreate, db: Session = Depends(get_db)):
    return {"message": "Hi from post"}


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
