import os
from datetime import date, timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth_utils import get_password_hash
from database import Base, SessionLocal, engine
from models import Category, Transaction, User
from routers import analytics, auth, categories, transactions

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
    seed_example_data()


@app.get("/")
def healthcheck():
    return {"status": "ok", "message": "Finance API is running"}


app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(analytics.router)


def seed_example_data():
    """Наполняем БД демо-данными только при первом запуске."""
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            return

        demo_user = User(email="demo@example.com", hashed_password=get_password_hash("demo1234"))
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
        db.commit()
    finally:
        db.close()
