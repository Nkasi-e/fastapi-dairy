from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"Message": "Welcome to Diary API, where logs are saved"}
