from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..db.database import get_db
from ..users.user_model import User
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")


class TokenData(BaseModel):
    id: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(
            days=settings.access_token_expires_in
        )

    to_encode.update({"exp": expires})

    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.algorithm]
        )

        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail=f"Unauthorized access. Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()
    return user
