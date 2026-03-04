from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth_utils import get_current_user
from database import get_db
from models import Category, User
from schemas import CategoryCreate, CategoryOut, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(Category)
        .filter(Category.user_id == current_user.id)
        .order_by(Category.name.asc())
        .all()
    )


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    normalized_name = payload.name.strip()
    existing = (
        db.query(Category)
        .filter(Category.user_id == current_user.id)
        .all()
    )
    duplicate = next(
        (item for item in existing if item.name.strip().casefold() == normalized_name.casefold()),
        None,
    )
    if duplicate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Категория с таким названием уже существует")

    category = Category(name=normalized_name, color=payload.color, user_id=current_user.id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id, Category.user_id == current_user.id)
        .first()
    )
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    if payload.name is not None:
        normalized_name = payload.name.strip()
        sibling_categories = (
            db.query(Category)
            .filter(Category.user_id == current_user.id, Category.id != category.id)
            .all()
        )
        duplicate = next(
            (item for item in sibling_categories if item.name.strip().casefold() == normalized_name.casefold()),
            None,
        )
        if duplicate:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Категория с таким названием уже существует")
        category.name = normalized_name
    if payload.color is not None:
        category.color = payload.color

    db.commit()
    db.refresh(category)
    return category
