from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db.database import get_db
from .user_model import User
from .user_schema import CreateUser, UserOut, Token
from ..utils.helpers import hash_password, verify_password
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..utils.oauth2 import create_access_token
from ..utils.mail import send_email_async

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

    await send_email_async(
        subject="Registration Confirmation",
        email_to=user.email,
        body=f"Hello {user.firstname} {user.lastname}! Your account with email {user.email} has been successfully created",
    )

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
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
