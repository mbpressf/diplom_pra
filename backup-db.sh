#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${ENV_FILE:-$ROOT_DIR/.env.home-server}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Не найден env-файл: $ENV_FILE"
  exit 1
fi

set -a
. "$ENV_FILE"
set +a

BACKUP_KEEP_DAYS="${BACKUP_KEEP_DAYS:-30}"
BACKUP_DIR="${BACKUP_DIR:-$HOME/.finpotok-backups}"
DB_PATH="${DB_PATH:-$ROOT_DIR/data/finance.db}"

if [[ ! -f "$DB_PATH" ]]; then
  echo "Файл базы не найден: $DB_PATH"
  exit 1
fi

mkdir -p "$BACKUP_DIR"

STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_PATH="$BACKUP_DIR/finance-$STAMP.db"
cp "$DB_PATH" "$BACKUP_PATH"
echo "Создан backup: $BACKUP_PATH"

if command -v sqlite3 >/dev/null 2>&1; then
  sqlite3 "$DB_PATH" ".dump" | gzip -c > "${BACKUP_PATH}.sql.gz"
  echo "Создан SQL dump: ${BACKUP_PATH}.sql.gz"
fi

find "$BACKUP_DIR" -type f -name "finance-*.db" -mtime +"$BACKUP_KEEP_DAYS" -delete || true
find "$BACKUP_DIR" -type f -name "finance-*.sql.gz" -mtime +"$BACKUP_KEEP_DAYS" -delete || true
