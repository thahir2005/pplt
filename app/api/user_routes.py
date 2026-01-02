from app.schemas.user import UserCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.schemas.user import UserUpdate
from app.core.security import get_current_user
from app.services.user_service import hash_password_sha256
from typing import List, Optional
from sqlalchemy import asc, desc
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
from fastapi import Query
from typing import List, Optional
from sqlalchemy import asc, desc

@router.post("/", status_code=201)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    new_user = User(
        email=user.email,
        hashed_password=hash_password_sha256(user.password),
    )

    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    db.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email
    }

@router.get("/", response_model=List[UserList])
def list_users(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    search: Optional[str] = Query(None, description="Search by email"),
    sort: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    query = db.query(User)

    # 🔍 Search (case-insensitive)
    if search:
        query = query.filter(User.email.ilike(f"%{search}%"))

    # 🔼🔽 Sorting
    if sort == "desc":
        query = query.order_by(desc(User.id))
    else:
        query = query.order_by(asc(User.id))

    users = query.offset(offset).limit(limit).all()
    return users
@router.get("/me")
def read_current_user(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }


@router.patch("/me")
def update_current_user(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if data.email:
        current_user.email = data.email

    if data.password:
        current_user.hashed_password = hash_password_sha256(data.password)
    db.commit()
    db.refresh(current_user)

    return {
        "id": current_user.id,
        "email": current_user.email
    }


@router.delete("/me", status_code=204)
def delete_current_user(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db.delete(current_user)
    db.commit()
