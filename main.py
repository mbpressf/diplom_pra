import os
from datetime import date, timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text

from auth_utils import get_password_hash
from database import Base, SessionLocal, engine
from models import Category, SavingsVault, Transaction, User
from routers import analytics, auth, categories, orgs, transactions, vault

app = FastAPI(title="Income & Expense Tracker API")

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
# Базовая CORS-конфигурация (можно переопределить через CORS_ORIGINS).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[item.strip() for item in cors_origins.split(",") if item.strip()],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    ensure_runtime_migrations()
    seed_example_data()
    ensure_default_vaults()
    deduplicate_categories()


@app.get("/")
def healthcheck():
    return {"status": "ok", "message": "Finance API is running"}


app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(analytics.router)
app.include_router(vault.router)
app.include_router(orgs.router)


def seed_example_data():
    """Наполняем БД демо-данными только при первом запуске."""
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            return

        demo_user = User(
            email="demo@example.com",
            hashed_password=get_password_hash("demo1234"),
            account_type="individual",
        )
        db.add(demo_user)
        db.flush()

        salary = Category(name="Зарплата", color="#22C55E", user_id=demo_user.id)
        food = Category(name="Еда", color="#EF4444", user_id=demo_user.id)
        transport = Category(name="Транспорт", color="#0EA5E9", user_id=demo_user.id)
        freelance = Category(name="Фриланс", color="#10B981", user_id=demo_user.id)
        db.add_all([salary, food, transport, freelance])
        db.flush()

        today = date.today()
        samples = [
            Transaction(amount=1800, type="income", category_id=salary.id, date=today - timedelta(days=20), description="Зарплата", user_id=demo_user.id),
            Transaction(amount=420, type="income", category_id=freelance.id, date=today - timedelta(days=10), description="Проект", user_id=demo_user.id),
            Transaction(amount=95, type="expense", category_id=food.id, date=today - timedelta(days=8), description="Продукты", user_id=demo_user.id),
            Transaction(amount=32, type="expense", category_id=transport.id, date=today - timedelta(days=6), description="Такси", user_id=demo_user.id),
            Transaction(amount=76, type="expense", category_id=food.id, date=today - timedelta(days=2), description="Кафе", user_id=demo_user.id),
        ]
        db.add_all(samples)
        db.add(SavingsVault(name="Финансовый сейф", balance=650, target_amount=3000, user_id=demo_user.id))
        db.commit()
    finally:
        db.close()


def ensure_default_vaults():
    """Создает сейф для каждого пользователя, у которого его еще нет."""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            existing = db.query(SavingsVault).filter(SavingsVault.user_id == user.id).first()
            if not existing:
                db.add(SavingsVault(name="Финансовый сейф", balance=0, target_amount=0, user_id=user.id))
        db.commit()
    finally:
        db.close()


def deduplicate_categories():
    """Сливает дубли категорий (по имени в рамках user_id) в одну категорию."""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        for user in users:
            categories = (
                db.query(Category)
                .filter(Category.user_id == user.id)
                .order_by(Category.id.asc())
                .all()
            )
            by_name = {}
            for category in categories:
                key = category.name.strip().casefold()
                if key not in by_name:
                    by_name[key] = category
                    continue

                keeper = by_name[key]
                # Переносим транзакции на сохраненную категорию.
                (
                    db.query(Transaction)
                    .filter(Transaction.category_id == category.id)
                    .update({Transaction.category_id: keeper.id}, synchronize_session=False)
                )
                db.delete(category)
        db.commit()
    finally:
        db.close()


def ensure_runtime_migrations():
    """Легкая миграция без Alembic для существующих инсталляций SQLite."""
    with engine.begin() as connection:
        inspector = inspect(connection)
        if "users" not in inspector.get_table_names():
            return

        user_columns = {column["name"] for column in inspector.get_columns("users")}
        if "account_type" not in user_columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN account_type VARCHAR NOT NULL DEFAULT 'individual'"))
