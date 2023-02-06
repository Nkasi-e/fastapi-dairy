from fastapi import APIRouter


router = APIRouter()


@router.get("/users")
def get_user():
    return {"username": "welcome new user"}
