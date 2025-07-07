#!/bin/bash

echo "Starting Spark Worker with Python dependencies..."

# Installa le dipendenze Python necessarie
echo "Installing Python dependencies..."
pip install xgboost pandas numpy scikit-learn

# Avvia il worker Spark
echo "Starting Spark worker..."
exec /opt/bitnami/scripts/spark/run.sh