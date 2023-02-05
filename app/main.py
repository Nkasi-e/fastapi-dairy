from fastapi import FastAPI
from pydantic import Ba


app = FastAPI()


@app.get("/")
async def root():
    return {"Message": "Welcome to Diary API, where logs are saved"}
