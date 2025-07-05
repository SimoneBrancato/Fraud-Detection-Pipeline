#!/bin/bash

# Avvia il master in background
/opt/bitnami/scripts/spark/run.sh &

# Aspetta che Spark master sia pronto
echo "Attendo che Spark Master sia pronto..."
sleep 10  # oppure usa una logica più avanzata con curl e healthcheck

# Esegui lo spark-submit
spark-submit --master spark://spark:7077 /spark/script.py

# Mantieni il container attivo
wait
