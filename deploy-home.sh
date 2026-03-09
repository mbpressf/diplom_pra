#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${ENV_FILE:-$ROOT_DIR/.env.home-server}"
COMPOSE_FILE="${COMPOSE_FILE:-$ROOT_DIR/docker-compose.home-server.yml}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Не найден env-файл: $ENV_FILE"
  echo "Скопируйте .env.home-server.example -> .env.home-server и заполните домен/секреты."
  exit 1
fi

mkdir -p "$ROOT_DIR/data" "$ROOT_DIR/data/backups"

LEGACY_DB="$ROOT_DIR/finance.db"
PERSISTENT_DB="$ROOT_DIR/data/finance.db"

if [[ -f "$LEGACY_DB" && ! -f "$PERSISTENT_DB" ]]; then
  echo "Найдена старая база $LEGACY_DB, переношу в $PERSISTENT_DB"
  cp "$LEGACY_DB" "$PERSISTENT_DB"
fi

if [[ -f "$PERSISTENT_DB" ]]; then
  BACKUP_PATH="$ROOT_DIR/data/backups/finance-$(date +%Y%m%d-%H%M%S).db"
  cp "$PERSISTENT_DB" "$BACKUP_PATH"
  echo "Создан backup базы: $BACKUP_PATH"
fi

if command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_BIN=(docker-compose)
elif docker compose version >/dev/null 2>&1; then
  COMPOSE_BIN=(docker compose)
else
  echo "Не найден docker compose. Установите docker-compose или compose-plugin."
  exit 1
fi

set -a
. "$ENV_FILE"
set +a

"${COMPOSE_BIN[@]}" \
  -f "$COMPOSE_FILE" \
  up -d --build

"${COMPOSE_BIN[@]}" \
  -f "$COMPOSE_FILE" \
  ps
