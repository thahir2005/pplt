
from app.api.auth_routes import router as auth_router
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base
from app.models import user
from app.api.user_routes import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"status": "Day 5 CRUD ready"}
