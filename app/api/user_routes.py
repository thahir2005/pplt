from app.models.user import User
from fastapi import Query
from typing import List
from app.schemas.user import UserList

from app.core.security import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.schemas.user import UserCreate, UserOut
from app.services.user_service import create_user, get_users

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/", response_model=List[UserList])
def list_users(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    users = (
        db.query(User)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return users

@router.get("/me")
def read_current_user(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }
