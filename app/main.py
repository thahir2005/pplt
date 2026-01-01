from fastapi import FastAPI

app = FastAPI(title="PPLT API")

@app.get("/")
def root():
    return {"status": "Day 2 structure ready"}
