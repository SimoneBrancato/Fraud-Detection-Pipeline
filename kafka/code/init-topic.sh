#!/bin/bash

# Verifica che il nome del topic sia stato fornito
if [ -z "$KAFKA_TOPIC" ] || [ -z "$KAFKA_BOOTSTRAP_SERVER" ]; then
  echo "[FATAL-ERROR] FATAL ERROR: Environment variables not defined."
  exit 1
fi

sleep 30

echo "[INIT-TOPIC] Creating '$KAFKA_TOPIC' topic..."

/opt/bitnami/kafka/bin/kafka-topics.sh \
  --create \
  --topic "$KAFKA_TOPIC" \
  --partitions 3 \
  --replication-factor 3 \
  --if-not-exists \
  --bootstrap-server "$KAFKA_BOOTSTRAP_SERVER"

echo "[INIT-TOPIC] Successfully created '$KAFKA_TOPIC' topic."