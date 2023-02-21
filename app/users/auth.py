from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db.database import get_db
from .user_model import User
from .user_schema import (
    CreateUser,
    NewPasswordReset,
    UserOut,
    Token,
    PasswordReset,
)
from ..utils.helpers import hash_password, verify_password
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..utils.oauth2 import create_access_token
from app.config import settings
from jose import JWTError, jwt

from ..utils.mail import send_mail

router = APIRouter(tags=["Auth Section"])


def get_user_by_email(db: Session, email: str):
    query = db.query(User).filter(User.email == email).first()
    return query


@router.post(
    "/account/signup",
    response_description="User created successfully.",
    status_code=201,
    response_model=UserOut,
)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail=f"email already exists")
    if user.cpassword != user.password:
        raise HTTPException(status_code=404, detail=f"Password must match")
    del user.cpassword
    user.password = hash_password(user.password)

    # await send_mail(
    #     subject="Registration Confirmation",
    #     email_to=user.email,
    #     body=f"Hello {user.firstname} {user.lastname}! Your account with email {user.email} has been successfully created",
    # )

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post(
    "/login", response_model=Token, response_description="Login Successful"
)
def login_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User).filter(User.email == user_credentials.username).first()
    )
    if not user:
        raise HTTPException(status_code=403, detail=f"Invalid Credentials")
    is_password_correct = verify_password(
        user_credentials.password, user.password
    )
    if not is_password_correct:
        raise HTTPException(status_code=403, detail=f"Invalid Credentials")
    access_token = create_access_token(
        data={"user_id": user.id, "user_email": user.email}
    )
    return {
        "email": user.email,
        "access_token": access_token,
        "token_type": "Bearer",
    }


@router.post("/reset_password", response_description="Reset Password")
async def reset_password(
    user_email: PasswordReset, db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_email.email).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"email {user_email.email} is not a valid user email",
        )
    expires = timedelta(minutes=6)
    token = create_access_token(
        data={"user_id": user.id, "user_password": user.password},
        expires_delta=expires,
    )
    reset_link = f"http://localhost:3000/reset%password?token={token}"
    # await send_mail(
    #     subject="Password Reset",
    #     email_to=user_email.email,
    #     body=f"Your password reset link is: {reset_link}",
    # )
    return {
        "message": "A password reset link has been sent to your email",
        "reset_link": reset_link,
    }


@router.post("/reset_password/confirm")
async def create_new_password(
    token: str, new_password: NewPasswordReset, db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.algorithm]
        )
    except JWTError:
        raise HTTPException(
            status_code=400, detail=f"Token is invalid or has expired"
        )
    user_query = db.query(User).filter(User.id == payload["user_id"])
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found")
    if user.password != payload["user_password"]:
        raise HTTPException(
            status_code=403,
            detail=f"The reset token link has already been used",
        )
    if new_password.cpassword != new_password.password:
        raise HTTPException(status_code=400, detail=f"Password must match")
    del new_password.cpassword
    user.password = hash_password(new_password.password)
    update_password = new_password.dict(exclude_unset=True)
    user_query.filter(User.id == payload["user_id"]).update(
        update_password, synchronize_session=False
    )
    # await send_mail(
    #     subject="Password Reset Successful",
    #     email_to=user.email,
    #     body=f"You have successfully changed your password.",
    # )
    db.commit()
    db.refresh(user)
    return {"Message": "Password has been updated successfully"}
