from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.schemas.auth import LoginRequest
from app.services.user_service import authenticate_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    return {
        "message": "Login successful",
        "user_id": user.id,
        "email": user.email
    }
