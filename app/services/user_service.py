from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
import hashlib

def hash_password_sha256(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password_sha256(plain_password: str, hashed_password: str) -> bool:
    return hash_password_sha256(plain_password) == hashed_password

def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
           hashed_password=hash_password_sha256(user.password)    )
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    return db_user

def get_users(db: Session) -> list[User]:
    return db.query(User).all()

from fastapi import HTTPException, status

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password_sha256(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return user
