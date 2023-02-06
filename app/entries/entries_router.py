from fastapi import APIRouter


router = APIRouter()


@router.get("/entries")
def get_entries():
    return {"Message": "New entries"}
