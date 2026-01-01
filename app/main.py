from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base
from app.models import user

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

@app.get("/")
def root():
    return {"db": "connected"}

