import csv
import io
from datetime import date, datetime

from fastapi import APIRouter, Depends, File, HTTPException, Query, Response, UploadFile, status
from sqlalchemy.orm import Session, joinedload

from auth_utils import get_current_user
from database import get_db
from models import Category, Transaction, User
from schemas import TransactionCreate, TransactionOut

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=list[TransactionOut])
def list_transactions(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(Transaction)
        .options(joinedload(Transaction.category))
        .filter(Transaction.user_id == current_user.id)
    )
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    return query.order_by(Transaction.date.desc(), Transaction.id.desc()).all()


@router.post("", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = (
        db.query(Category)
        .filter(Category.id == payload.category_id, Category.user_id == current_user.id)
        .first()
    )
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    transaction = Transaction(
        amount=payload.amount,
        type=payload.type,
        category_id=payload.category_id,
        date=payload.date,
        description=payload.description,
        user_id=current_user.id,
    )
    db.add(transaction)
    db.commit()

    result = (
        db.query(Transaction)
        .options(joinedload(Transaction.category))
        .filter(Transaction.id == transaction.id)
        .first()
    )
    return result


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id, Transaction.user_id == current_user.id)
        .first()
    )
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    db.delete(transaction)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/export/csv")
def export_csv(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(Transaction)
        .options(joinedload(Transaction.category))
        .filter(Transaction.user_id == current_user.id)
    )
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    rows = query.order_by(Transaction.date.asc()).all()

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["id", "amount", "type", "category", "date", "description"])
    for item in rows:
        writer.writerow([item.id, item.amount, item.type, item.category.name, item.date.isoformat(), item.description])

    return Response(
        content=buffer.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"},
    )


@router.post("/import/csv")
async def import_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # CSV формат: amount,type,category,date,description
    content = await file.read()
    decoded = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))

    imported = 0
    for row in reader:
        try:
            amount = float(row.get("amount", "0"))
            tx_type = row.get("type", "").strip()
            category_name = row.get("category", "Без категории").strip() or "Без категории"
            tx_date = datetime.strptime(row.get("date", ""), "%Y-%m-%d").date()
            description = row.get("description", "").strip()
        except (ValueError, TypeError):
            continue

        if tx_type not in {"income", "expense"} or amount <= 0:
            continue

        category = (
            db.query(Category)
            .filter(Category.user_id == current_user.id, Category.name == category_name)
            .first()
        )
        if not category:
            category = Category(name=category_name, color="#94A3B8", user_id=current_user.id)
            db.add(category)
            db.flush()

        db.add(
            Transaction(
                amount=amount,
                type=tx_type,
                category_id=category.id,
                date=tx_date,
                description=description,
                user_id=current_user.id,
            )
        )
        imported += 1

    db.commit()
    return {"imported": imported}
