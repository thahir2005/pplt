from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Day 1 started successfully"}
