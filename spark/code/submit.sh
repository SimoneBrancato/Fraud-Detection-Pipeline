#!/bin/bash

echo "Waiting for Spark cluster to be ready..."

# Aspetta che il master sia pronto
while ! curl -s http://spark-master:8080 > /dev/null 2>&1; do
  echo "Waiting for Spark master..."
  sleep 5
done

echo "Spark master is ready!"

# Wait for the workers to be ready
sleep 30

echo "Starting Spark application..."

# Esegue l'applicazione principale

pip install xgboost pandas numpy scikit-learn requests &&

sleep 30 &&

spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --total-executor-cores 3 \
  --executor-memory 2g \
  --driver-memory 1g \
  --conf spark.sql.adaptive.enabled=true \
  --conf spark.sql.adaptive.coalescePartitions.enabled=true \
  --conf spark.executorEnv.PYTHONPATH=/opt/bitnami/python/lib/python3.9/site-packages \
  --conf "spark.driver.extraJavaOptions=-Dcom.clickhouse.client.http.connection.provider=HTTP_URL_CONNECTION" \
  --conf "spark.executor.extraJavaOptions=-Dcom.clickhouse.client.http.connection.provider=HTTP_URL_CONNECTION" \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,com.clickhouse:clickhouse-jdbc:0.6.0,org.apache.httpcomponents.client5:httpclient5:5.2.1\
  /opt/bitnami/spark/apps/script.py