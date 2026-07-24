"""预算路由"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.models import Budget
from app.utils.auth import get_current_user_id
from app.utils.common import success, error

router = APIRouter(prefix="/api/entry/budget", tags=["预算"])


@router.get("/all")
def get_budgets(book_id: str, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """获取账本预算"""
    budgets = db.query(Budget).filter(
        Budget.book_id == book_id
    ).all()
    return success(budgets)


@router.post("/add")
def add_budget(book_id: str, month: str, budget: float, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """添加/更新预算"""
    existing = db.query(Budget).filter(
        Budget.book_id == book_id,
        Budget.month == month
    ).first()

    if existing:
        existing.budget = budget
        db.commit()
        db.refresh(existing)
        return success(existing)
    else:
        db_budget = Budget(
            book_id=book_id,
            user_id=user_id,
            month=month,
            budget=budget,
            used=0
        )
        db.add(db_budget)
        db.commit()
        db.refresh(db_budget)
        return success(db_budget)
