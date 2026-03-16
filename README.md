# Дипломный проект: учет доходов и расходов с диаграммами

Рабочий сайт: https://finpotok.mbpressf.ru

Полноценное fullstack-приложение на FastAPI + Vue 3 для учета финансов, аналитики и визуализации данных.

## Стек

- Backend: Python 3.11+, FastAPI, SQLAlchemy, SQLite, JWT
- Frontend: Vue 3 (Composition API), Vite, Pinia, Vue Router, TailwindCSS, Chart.js, Axios

## Возможности

- Регистрация и авторизация (JWT)
- Мультипользовательский режим
- CRUD транзакций доходов/расходов
- Категории (создание и редактирование)
- Фильтр по датам
- KPI Dashboard:
  - Общий доход
  - Общий расход
  - Баланс
  - Процент экономии
- Графики:
  - Doughnut: распределение по категориям
  - Line: динамика по месяцам
- Экспорт в CSV
- Импорт из CSV
- Локальное кеширование данных в frontend (localStorage)
- Темная/светлая тема
- Анимации переходов, hover-эффекты, skeleton loader

## Структура

- `main.py`
- `database.py`
- `models.py`
- `schemas.py`
- `auth_utils.py`
- `routers/`
  - `auth.py`
  - `transactions.py`
  - `categories.py`
  - `analytics.py`
- `src/`
  - `components/`
  - `views/`
  - `store/`
  - `services/`
  - `router/`
  - `assets/`

## API

- `POST /auth/register`
- `POST /auth/login`
- `GET /transactions`
- `POST /transactions`
- `DELETE /transactions/{id}`
- `GET /analytics/summary`
- `GET /analytics/by-category`
- `GET /analytics/by-month`
- `POST /orgs`
- `POST /orgs/join`
- `GET /orgs/me`
- `GET /orgs/{id}/dashboard`
- `POST /orgs/{id}/reports/generate`
- `GET /orgs/{id}/reports`
- `GET /orgs/{id}/exports/users.csv`
- `GET /orgs/{id}/exports/report.xlsx`
- `GET /orgs/{id}/exports/report.pdf`

Дополнительно:
- `GET /categories`
- `POST /categories`
- `PUT /categories/{id}`
- `GET /transactions/export/csv`
- `POST /transactions/import/csv`

## Пример данных

При первом запуске backend автоматически создается demo-пользователь:

- Email: `demo@example.com`
- Password: `demo1234`

И несколько категорий/транзакций для демонстрации графиков.

## Запуск проекта

### 1) Backend

```bash
cp .env.example .env
python3 -m pip install -r requirements.txt
uvicorn main:app --reload
```

Backend будет доступен на `http://127.0.0.1:8000`.

### 2) Frontend

```bash
cp .env.example .env
npm install
npm run dev
```

Frontend будет доступен на `http://127.0.0.1:5173`.

## Docker (структура подготовлена)

- `Dockerfile.backend`
- `Dockerfile.frontend`
- `Dockerfile.frontend.prod`
- `docker-compose.yml`
- `docker-compose.home-server.yml`
- `deploy-home.sh`
- `update-home.sh`
- `backup-db.sh`
- `restore-db.sh`

При необходимости можно поднять оба сервиса через Docker Compose.

## Деплой на домашний сервер через Traefik

Этот проект подготовлен под схему:

- `https://домен` -> фронтенд
- `https://домен/api` -> FastAPI backend

### Что использовать

- `docker-compose.home-server.yml`
- `.env.home-server.example`
- `deploy-home.sh`
- `update-home.sh`

### Первый запуск на домашнем сервере

```bash
cd ~/CODE/diplom_project_server/diplom_pra
cp .env.home-server.example .env.home-server
```

Заполните в `.env.home-server`:

- `APP_DOMAIN`
- `JWT_SECRET`
- `CORS_ORIGINS`
- `DATABASE_URL` (оставьте `sqlite:////app/data/finance.db`)
- `BACKUP_DIR` (например `/home/mb_press_f/.finpotok-backups`)
- `BACKUP_KEEP_DAYS` (например `30`)

Потом:

```bash
chmod +x deploy-home.sh update-home.sh backup-db.sh restore-db.sh
./deploy-home.sh
```

`deploy-home.sh` теперь автоматически:

- делает backup базы перед релизом;
- хранит backup вне папки проекта (по умолчанию в `~/.finpotok-backups`);
- проверяет количество транзакций до/после деплоя;
- откатывает базу из backup, если после релиза база внезапно стала пустой;
- пытается восстановить базу из последнего backup, если `data/finance.db` случайно удалили.

### Обновление после изменений

Если проект уже лежит на сервере как git-репозиторий:

```bash
./update-home.sh
```

По умолчанию обновляется ветка `main`. Если нужна другая:

```bash
BRANCH=main ./update-home.sh
```

### Регулярные backup (рекомендуется)

Разовый ручной backup:

```bash
./backup-db.sh
```

Восстановление из последнего backup:

```bash
./restore-db.sh
```

Запуск backup каждые 6 часов через cron:

```bash
(crontab -l 2>/dev/null; echo "0 */6 * * * cd ~/CODE/diplom_project_server/diplom_pra && ./backup-db.sh >> ~/finpotok-backup.log 2>&1") | crontab -
```

### Безопасная загрузка проекта по rsync (чтобы не удалить `data`)

Если обновляете код с локальной машины через `rsync --delete`, защищайте папку `data`:

```bash
rsync -az --delete --filter='P data/' --exclude '.git/' --exclude 'node_modules/' --exclude 'dist/' ./ mb_press_f@100.118.138.85:~/CODE/diplom_project_server/diplom_pra/
```

### Что важно для production

- SQLite хранится в `./data` рядом с compose-файлом
- frontend в production использует `/api`
- backend автоматически работает через `DATABASE_URL` из env
