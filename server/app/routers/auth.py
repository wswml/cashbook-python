"""用户认证路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from app.models.database import get_db
from app.models.models import User
from app.models.schemas import UserCreate, UserLogin, Token
from app.utils.auth import get_password_hash, verify_password, create_access_token
from app.utils.common import success, error

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        return error("用户名已存在")

    # 创建用户
    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        name=user.name or user.username,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return success({"id": db_user.id, "username": db_user.username})


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        return error("用户名或密码错误", 401)

    access_token = create_access_token(data={"sub": str(db_user.id)})

    return success({
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "name": db_user.name
        }
    })
