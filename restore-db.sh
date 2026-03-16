#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${COMPOSE_FILE:-$ROOT_DIR/docker-compose.home-server.yml}"
ENV_FILE="${ENV_FILE:-$ROOT_DIR/.env.home-server}"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  . "$ENV_FILE"
  set +a
fi

BACKUP_DIR="${BACKUP_DIR:-$HOME/.finpotok-backups}"
TARGET_DB="${TARGET_DB:-$ROOT_DIR/data/finance.db}"

if docker compose version >/dev/null 2>&1; then
  COMPOSE_BIN=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_BIN=(docker-compose)
else
  echo "Не найден docker compose. Установите docker-compose или compose-plugin."
  exit 1
fi

if [[ "${1:-}" != "" ]]; then
  SRC_BACKUP="$1"
else
  SRC_BACKUP="$(ls -1t "$BACKUP_DIR"/finance-*.db 2>/dev/null | head -n1 || true)"
fi

if [[ -z "$SRC_BACKUP" || ! -f "$SRC_BACKUP" ]]; then
  echo "Backup для восстановления не найден. Передайте путь первым аргументом."
  exit 1
fi

mkdir -p "$(dirname "$TARGET_DB")"
cp "$SRC_BACKUP" "$TARGET_DB"
echo "Восстановлено из backup: $SRC_BACKUP -> $TARGET_DB"

"${COMPOSE_BIN[@]}" -f "$COMPOSE_FILE" up -d --force-recreate finpotok-backend
echo "Backend перезапущен."
