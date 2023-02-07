import os
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..db.database import get_db
from ..users.user_model import User
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(".env")


JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRES_IN = float(os.environ.get("ACCESS_TOKEN_EXPIRES_IN"))


class TokenData(BaseModel):
    id: Optional[str] = None


def create_access_token(data: dict):
    to_encode = data.copy()

    expires = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRES_IN)

    to_encode.update({"exp": expires})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
