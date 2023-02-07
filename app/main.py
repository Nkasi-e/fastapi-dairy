from fastapi import FastAPI
from .entries import entries_router, entries_model
from .db.database import engine

app = FastAPI()





@app.get("/")
async def root():
    return {"Message": "Welcome to Diary API, where logs are saved"}


app.include_router(user_router.router)
app.include_router(entries_router.router)
app.include_router(auth.router)
