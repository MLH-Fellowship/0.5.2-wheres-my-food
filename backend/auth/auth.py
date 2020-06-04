from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from sqlalchemy.orm import Session
from auth.auth_schema import TokenData
from db.crud import get_user_by_email
from db.models import User
from db.database import SessionLocal
from auth.auth_utils import (
    verify_password,
    get_password_hash,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    db = SessionLocal()
    user = get_user_by_email(db, email=token_data.username)
    db.close()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


async def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        return current_user
    raise HTTPException(status_code=401, detail="Non admin user")
