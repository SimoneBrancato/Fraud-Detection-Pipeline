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

pip install xgboost pandas numpy scikit-learn &&

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
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0,org.apache.hadoop:hadoop-aws:3.3.2,software.amazon.awssdk:bundle:2.20.20 \
  --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
  --conf spark.sql.catalog.iceberg=org.apache.iceberg.spark.SparkCatalog \
  --conf spark.sql.catalog.iceberg.type=hadoop \
  --conf spark.sql.catalog.iceberg.io-impl=org.apache.iceberg.aws.s3.S3FileIO \
  --conf spark.sql.catalog.iceberg.warehouse=s3a://iceberg/ \
  --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
  --conf spark.hadoop.fs.s3a.access.key=admin \
  --conf spark.hadoop.fs.s3a.secret.key=password \
  --conf spark.hadoop.fs.s3a.path.style.access=true \
  --conf spark.hadoop.fs.s3a.connection.ssl.enabled=false \
  /opt/bitnami/spark/apps/script.py