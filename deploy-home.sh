#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${ENV_FILE:-$ROOT_DIR/.env.home-server}"
COMPOSE_FILE="${COMPOSE_FILE:-$ROOT_DIR/docker-compose.home-server.yml}"
BACKUP_KEEP_DAYS="${BACKUP_KEEP_DAYS:-30}"
BACKUP_DIR="${BACKUP_DIR:-$HOME/.finpotok-backups}"
AUTO_RESTORE_IF_MISSING="${AUTO_RESTORE_IF_MISSING:-1}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Не найден env-файл: $ENV_FILE"
  echo "Скопируйте .env.home-server.example -> .env.home-server и заполните домен/секреты."
  exit 1
fi

mkdir -p "$ROOT_DIR/data" "$BACKUP_DIR"

LEGACY_DB="$ROOT_DIR/finance.db"
PERSISTENT_DB="$ROOT_DIR/data/finance.db"
BACKUP_PATH=""

if docker compose version >/dev/null 2>&1; then
  COMPOSE_BIN=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_BIN=(docker-compose)
else
  echo "Не найден docker compose. Установите docker-compose или compose-plugin."
  exit 1
fi

set -a
. "$ENV_FILE"
set +a

if [[ "${DATABASE_URL:-sqlite:////app/data/finance.db}" != "sqlite:////app/data/finance.db" ]]; then
  echo "Внимание: DATABASE_URL=${DATABASE_URL:-unset}. Скрипт ожидает sqlite:////app/data/finance.db"
fi

get_tx_count() {
  local db_file="$1"
  if [[ ! -f "$db_file" ]]; then
    echo 0
    return
  fi

  if ! command -v sqlite3 >/dev/null 2>&1; then
    echo -1
    return
  fi

  local has_table
  has_table="$(sqlite3 "$db_file" "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='transactions';" 2>/dev/null || echo 0)"

  if [[ "$has_table" != "1" ]]; then
    echo 0
    return
  fi

  sqlite3 "$db_file" "SELECT COUNT(*) FROM transactions;" 2>/dev/null || echo 0
}

latest_backup_path() {
  ls -1t "$BACKUP_DIR"/finance-*.db 2>/dev/null | head -n1 || true
}

if [[ -f "$LEGACY_DB" && ! -f "$PERSISTENT_DB" ]]; then
  echo "Найдена старая база $LEGACY_DB, переношу в $PERSISTENT_DB"
  cp "$LEGACY_DB" "$PERSISTENT_DB"
fi

LATEST_BACKUP="$(latest_backup_path)"
if [[ ! -f "$PERSISTENT_DB" && "${AUTO_RESTORE_IF_MISSING}" == "1" && -n "$LATEST_BACKUP" ]]; then
  echo "Файл базы отсутствует. Восстанавливаю из последнего backup: $LATEST_BACKUP"
  cp "$LATEST_BACKUP" "$PERSISTENT_DB"
fi

PRE_TX_COUNT="$(get_tx_count "$PERSISTENT_DB")"
echo "Транзакций до деплоя: $PRE_TX_COUNT"

if [[ -f "$PERSISTENT_DB" ]]; then
  BACKUP_PATH="$BACKUP_DIR/finance-$(date +%Y%m%d-%H%M%S).db"
  cp "$PERSISTENT_DB" "$BACKUP_PATH"
  echo "Создан backup базы: $BACKUP_PATH"

  if command -v sqlite3 >/dev/null 2>&1; then
    sqlite3 "$PERSISTENT_DB" ".dump" | gzip -c > "${BACKUP_PATH}.sql.gz"
    echo "Создан SQL dump: ${BACKUP_PATH}.sql.gz"
  fi
fi

"${COMPOSE_BIN[@]}" \
  -f "$COMPOSE_FILE" \
  up -d --build

"${COMPOSE_BIN[@]}" \
  -f "$COMPOSE_FILE" \
  ps

POST_TX_COUNT="$(get_tx_count "$PERSISTENT_DB")"
echo "Транзакций после деплоя: $POST_TX_COUNT"

if [[ "$PRE_TX_COUNT" =~ ^[0-9]+$ ]] && [[ "$POST_TX_COUNT" =~ ^[0-9]+$ ]] && [[ "$PRE_TX_COUNT" -gt 0 ]] && [[ "$POST_TX_COUNT" -eq 0 ]] && [[ -n "$BACKUP_PATH" ]]; then
  echo "КРИТИЧНО: после деплоя база стала пустой. Выполняю авто-откат из $BACKUP_PATH"
  cp "$BACKUP_PATH" "$PERSISTENT_DB"
  "${COMPOSE_BIN[@]}" -f "$COMPOSE_FILE" up -d --force-recreate finpotok-backend
  echo "Откат выполнен. Проверьте логи backend."
  exit 1
fi

find "$BACKUP_DIR" -type f -name "finance-*.db" -mtime +"$BACKUP_KEEP_DAYS" -delete || true
find "$BACKUP_DIR" -type f -name "finance-*.sql.gz" -mtime +"$BACKUP_KEEP_DAYS" -delete || true
