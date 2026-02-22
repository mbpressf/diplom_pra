from collections import defaultdict
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from auth_utils import get_current_user
from database import get_db
from models import Transaction, User
from schemas import CategoryAnalyticsItem, MonthAnalyticsItem, SummaryOut

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def _get_transactions(db: Session, user_id: int, start_date: date | None, end_date: date | None):
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    return query.all()


@router.get("/summary", response_model=SummaryOut)
def summary(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transactions = _get_transactions(db, current_user.id, start_date, end_date)

    total_income = sum(t.amount for t in transactions if t.type == "income")
    total_expense = sum(t.amount for t in transactions if t.type == "expense")
    balance = total_income - total_expense
    savings_rate = ((balance / total_income) * 100) if total_income > 0 else 0

    return SummaryOut(
        total_income=round(total_income, 2),
        total_expense=round(total_expense, 2),
        balance=round(balance, 2),
        savings_rate=round(savings_rate, 2),
    )


@router.get("/by-category", response_model=list[CategoryAnalyticsItem])
def by_category(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transactions = _get_transactions(db, current_user.id, start_date, end_date)

    buckets = {}
    for tx in transactions:
        key = tx.category_id
        if key not in buckets:
            buckets[key] = {
                "category": tx.category.name if tx.category else "Без категории",
                "color": tx.category.color if tx.category else "#94A3B8",
                "amount": 0.0,
            }
        buckets[key]["amount"] += tx.amount

    result = []
    for value in buckets.values():
        payload = dict(value)
        payload["amount"] = round(payload["amount"], 2)
        result.append(CategoryAnalyticsItem(**payload))
    result.sort(key=lambda i: i.amount, reverse=True)
    return result


@router.get("/by-month", response_model=list[MonthAnalyticsItem])
def by_month(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transactions = _get_transactions(db, current_user.id, start_date, end_date)

    monthly = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for tx in transactions:
        key = tx.date.strftime("%Y-%m")
        monthly[key][tx.type] += tx.amount

    result = [
        MonthAnalyticsItem(
            month=month,
            income=round(values["income"], 2),
            expense=round(values["expense"], 2),
        )
        for month, values in sorted(monthly.items())
    ]
    return result
