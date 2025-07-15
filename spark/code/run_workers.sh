#!/bin/bash

echo "Starting Spark Worker with Python dependencies..."

# Install required dependencies
echo "Installing Python dependencies..."
pip install xgboost pandas numpy scikit-learn

# Start Spark Worker job
echo "Starting Spark worker..."
exec /opt/bitnami/scripts/spark/run.sh