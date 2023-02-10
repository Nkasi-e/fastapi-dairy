from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db.database import get_db
from .user_schema import UserOut
from .user_model import User
from ..utils.oauth2 import get_current_user


router = APIRouter(tags=["User Section"])


@router.get("/users/profile", response_model=UserOut)
def get_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == current_user.id).first()
    return user
