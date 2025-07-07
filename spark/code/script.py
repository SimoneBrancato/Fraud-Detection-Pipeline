from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_csv
import math
import joblib
import pandas as pd
import numpy as np

print("=== Fraud Detection with XGBoost ===")

# Crea SparkSession
spark = SparkSession.builder \
    .appName("FraudDetectionStreaming") \
    .master("spark://spark-master:7077") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("Loading XGBoost model...")
model_path = '/opt/bitnami/spark/apps/xgb_full_pipeline.pkl'

# Carica il modello XGBoost
try:
    model_pipeline = joblib.load(model_path)
    print("✓ XGBoost model loaded successfully")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    exit(1)

print("Starting Kafka stream...")

# Legge lo stream da Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka1:9092,kafka2:9092,kafka3:9092") \
    .option("subscribe", "fraud-transactions") \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load()

# Decodifica i messaggi Kafka
parsed_df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "timestamp")

csv_schema_str = "index string, trans_date_trans_time string, cc_num string," \
" merchant string, category string, amt double, first string, last string, gender string," \
" street string, city string, state string, zip string, lat double, long double," \
" city_pop int, job string, dob string, trans_num string, unix_time int, merch_lat double," \
" merch_long double, is_fraud int"

# Parsa il CSV
df_csv = parsed_df.select(
    from_csv(col("value"), csv_schema_str, {"header": "false", "inferSchema": "false"}).alias("csv_data")
).select(
    col("csv_data.index").alias("index"),
    col("csv_data.trans_date_trans_time").alias("trans_date_trans_time"),
    col("csv_data.cc_num").alias("cc_num"),
    col("csv_data.merchant").alias("merchant"),
    col("csv_data.category").alias("category"),
    col("csv_data.amt").alias("amt"),
    col("csv_data.first").alias("first"),
    col("csv_data.last").alias("last"),
    col("csv_data.gender").alias("gender"),
    col("csv_data.street").alias("street"),
    col("csv_data.city").alias("city"),
    col("csv_data.state").alias("state"),
    col("csv_data.zip").alias("zip"),
    col("csv_data.lat").alias("lat"),
    col("csv_data.long").alias("long"),
    col("csv_data.city_pop").alias("city_pop"),
    col("csv_data.job").alias("job"),
    col("csv_data.dob").alias("dob"),
    col("csv_data.trans_num").alias("trans_num"),
    col("csv_data.unix_time").alias("unix_time"),
    col("csv_data.merch_lat").alias("merch_lat"),
    col("csv_data.merch_long").alias("merch_long"),
)

# Define haversine UDF
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate haversine distance between two points
    """
    if any(x is None for x in [lat1, lon1, lat2, lon2]):
        return None
    
    R = 6371  # Earth radius in km
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def preprocess_and_predict(batch_df, batch_id):
    """
    PySpark version of the feature engineering pipeline
    """

    count = batch_df.count()
    print(f"Processing batch {batch_id} with {count} records")

    if count == 0:
        print("Empty batch, skipping...")
        return
    
    try:

        # Convert to Pandas per mantenere logica identica
        pandas_df = batch_df.toPandas()
        
        # Applica la funzione originale (adattata)
        pandas_df['dob'] = pd.to_datetime(pandas_df['dob'])
        pandas_df['trans_date_trans_time'] = pd.to_datetime(pandas_df['trans_date_trans_time'])
        pandas_df['age'] = (pandas_df['trans_date_trans_time'] - pandas_df['dob']).dt.days // 365
        pandas_df['hour'] = pandas_df['trans_date_trans_time'].dt.hour
        pandas_df['day_of_week'] = pandas_df['trans_date_trans_time'].dt.dayofweek
        pandas_df['is_night'] = pandas_df['hour'].apply(lambda x: 1 if x < 6 or x >= 22 else 0)
        pandas_df['is_weekend'] = pandas_df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
        
        # Distanza (assumendo che haversine sia disponibile)
        pandas_df['distance_user_to_merch'] = pandas_df.apply(
            lambda row: haversine(row['lat'], row['long'], row['merch_lat'], row['merch_long']), axis=1
        )
        
        # Log transforms
        pandas_df['log_amt'] = np.log1p(pandas_df['amt'])
        pandas_df['log_city_pop'] = np.log1p(pandas_df['city_pop'])
        pandas_df['log_distance'] = np.log1p(pandas_df['distance_user_to_merch'])
        
        # Statistiche utente SOLO per questo batch
        pandas_df['user_id'] = pandas_df['cc_num'].astype(str)
        pandas_df.sort_values(['user_id', 'trans_date_trans_time'], inplace=True)
        pandas_df['tx_count_user'] = pandas_df.groupby('user_id').cumcount()
        pandas_df['amt_mean_user'] = pandas_df.groupby('user_id')['amt'].transform(
            lambda x: x.rolling(10, min_periods=1).mean()
        )
        
        # Keep only required columns
        required_columns = [
            'age', 'hour', 'day_of_week', 'is_night', 'is_weekend',
            'log_amt', 'log_city_pop', 'log_distance', 'tx_count_user', 'amt_mean_user',
            'gender', 'category', 'state', 'job'
        ]
        
        processed_df = pandas_df[required_columns]

        # Applica il modello
        predictions = model_pipeline.predict(processed_df)
        probabilities = model_pipeline.predict_proba(processed_df)
        
        # Aggiungi predizioni al DataFrame
        pandas_df['fraud_prediction'] = predictions
        pandas_df['fraud_probability'] = probabilities[:, 1]

        fraud_transactions = pandas_df.query('fraud_prediction == 1')

        if len(fraud_transactions) > 0:
            print(f"🚨 FRAUD ALERT: {len(fraud_transactions)} fraudulent transactions detected!")
            print(fraud_transactions[['merchant', 'amt', 'fraud_probability']].to_string(index=False))
        else:
            print("\n✅ No fraud detected in this batch")

        result_df = spark.createDataFrame(pandas_df)

        result_df.select(col("trans_date_trans_time"), col("merchant"), col("amt"), col("first"), col("last"), col("city"), col("fraud_prediction"), col("fraud_probability")).show(10, truncate=False)

    except Exception as e:
        print(f"Error processing batch {batch_id}: {str(e)}")

print("Starting stream processing...")

query = df_csv.writeStream \
    .foreachBatch(preprocess_and_predict) \
    .trigger(processingTime='10 seconds') \
    .start() \
    .awaitTermination()

