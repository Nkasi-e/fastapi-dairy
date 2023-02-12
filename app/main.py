from fastapi import FastAPI
 test-branch
from fastapi.middleware.cors import CORSMiddleware
from .users import user_router, user_model, auth
= master
from .entries import entries_router, entries_model
from .db.database import engine

app = FastAPI()





origins = [
    "*",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"Message": "Welcome to Diary API, where logs are saved"}


app.include_router(user_router.router)
app.include_router(entries_router.router)
app.include_router(auth.router)
