#!/bin/sh

set -e

# Inizializzazione client
mc alias set myminio http://localhost:9000 admin password

# Crea il bucket solo se non esiste
if ! mc ls myminio | grep -q warehouse; then
  echo "📦 Creo il bucket warehouse..."
  mc mb myminio/warehouse
else
  echo "✅ Il bucket warehouse esiste già."
fi
