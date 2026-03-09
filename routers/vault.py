from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth_utils import get_current_user
from database import get_db
from models import SavingsVault, Transaction, User
from schemas import VaultOut, VaultTransfer, VaultUpdate

router = APIRouter(prefix="/vault", tags=["Vault"])


def _get_net_balance(db: Session, user_id: int) -> float:
    transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    total_income = sum(item.amount for item in transactions if item.type == "income")
    total_expense = sum(item.amount for item in transactions if item.type == "expense")
    return round(total_income - total_expense, 2)


def _get_or_create_vault(db: Session, user_id: int) -> SavingsVault:
    vault = db.query(SavingsVault).filter(SavingsVault.user_id == user_id).first()
    if vault:
        return vault

    vault = SavingsVault(user_id=user_id, name="Финансовый сейф", balance=0, target_amount=0)
    db.add(vault)
    db.commit()
    db.refresh(vault)
    return vault


def _build_vault_response(db: Session, vault: SavingsVault) -> VaultOut:
    net_balance = _get_net_balance(db, vault.user_id)
    available_to_spend = round(net_balance - vault.balance, 2)
    progress_percent = round((vault.balance / vault.target_amount) * 100, 2) if vault.target_amount > 0 else 0

    return VaultOut(
        id=vault.id,
        name=vault.name,
        balance=round(vault.balance, 2),
        target_amount=round(vault.target_amount, 2),
        net_balance=net_balance,
        available_to_spend=available_to_spend,
        progress_percent=progress_percent,
    )


@router.get("", response_model=VaultOut)
def get_vault(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    vault = _get_or_create_vault(db, current_user.id)
    return _build_vault_response(db, vault)


@router.put("", response_model=VaultOut)
def update_vault(
    payload: VaultUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vault = _get_or_create_vault(db, current_user.id)

    if payload.name is not None:
        vault.name = payload.name.strip()
    if payload.target_amount is not None:
        vault.target_amount = payload.target_amount

    db.commit()
    db.refresh(vault)
    return _build_vault_response(db, vault)


@router.post("/deposit", response_model=VaultOut)
def deposit_to_vault(
    payload: VaultTransfer,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vault = _get_or_create_vault(db, current_user.id)
    net_balance = _get_net_balance(db, current_user.id)
    available_to_spend = round(net_balance - vault.balance, 2)

    if payload.amount > available_to_spend:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недостаточно свободных средств для перевода в сейф",
        )

    vault.balance = round(vault.balance + payload.amount, 2)
    db.commit()
    db.refresh(vault)
    return _build_vault_response(db, vault)


@router.post("/withdraw", response_model=VaultOut)
def withdraw_from_vault(
    payload: VaultTransfer,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vault = _get_or_create_vault(db, current_user.id)
    if payload.amount > vault.balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="В сейфе недостаточно средств для вывода",
        )

    vault.balance = round(vault.balance - payload.amount, 2)
    db.commit()
    db.refresh(vault)
    return _build_vault_response(db, vault)
