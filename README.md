# Fraud Detection Pipeline

A real-time fraud detection system for banking transactions using Apache Kafka, Apache Spark, ClickHouse, and Grafana in a fully dockerized environment.

<img width="2557" height="1268" alt="Fraud-Detector-UI" src="https://github.com/user-attachments/assets/c901578c-af6f-44a3-a1ed-67b368b22336" />

## Architecture Overview

This project implements a complete real-time fraud detection pipeline with the following components:
- **Kafka Producer (Java)**: Streams banking transaction [dataset from Kaggle](https://www.kaggle.com/datasets/kartik2112/fraud-detection) (Only test set)
- **Apache Kafka Cluster**: Handles real-time data streaming and message queuing
- **Apache Spark Cluster**: Processes streaming data and performs fraud detection using a machine learning model
- **ClickHouse**: High-performance columnar database for data storage
- **Grafana**: Real-time data visualization and monitoring dashboard


### Fraud Detector Machine Learning Model

The fraud detection system uses an **XGBoost** model trained specifically for this project:
- **Dataset**: [Credit Card Transactions Fraud Detection Dataset, By Kartik Shenoy](https://www.kaggle.com/datasets/kartik2112/fraud-detection)
- **Performance Metrics**: Recall 92%, Precision 83%
- **Model Type**: Gradient Boosting Classifier
- **Features**: Transaction amount, merchant category, timestamp details, user behavior, and more

<img width="1407" height="891" alt="Fraud-Detector-Pipeline-Architecture" src="https://github.com/user-attachments/assets/d59aeb91-5cd8-42fd-a245-ece17ad51ae8" />


## Prerequisites

Before running the project, ensure you have the following installed:

- **Git**
- **Docker**
- **Test Set** in `producer/src/main/resources/fraudTest.csv` 


## Installation & Setup

1. Clone the Repository
2. Setup Docker Environment
3. Import Dataset and place it in `producer/src/main/resources/fraudTest.csv` 

### Start the Application

Build and start all services using Docker Compose:

```bash
docker compose up --build
```

### Access the Dashboard

Once all services are running:

1. Open your web browser
2. Navigate to `http://localhost:3000`
3. Login to Grafana with credentials:
   - **Username**: `admin`
   - **Password**: `admin`
4. Access the pre-configured fraud detection dashboard

## Pipeline Components

#### Kafka Producer
- **Language**: Java
- **Function**: Extracts and streams to Kafka banking transactions data

#### Kafka Cluster
- **Brokers:** 3 instances
- **Partitions**: 3
- **Replication**: 3
- **Topic**: `fraud-transactions`

#### Spark Cluster
- **Master**: 1 instance
- **Submit**: 1 instance
- **Workers**: 3 instances

#### ClickHouse
- **Database**: `default`
- **Table**: `fraud_predictions`

```sql
        -- Transactions table
        CREATE TABLE IF NOT EXISTS fraud_predictions (
            idx Int32,
            trans_date_trans_time DateTime,
            cc_num String,
            merchant String,
            category String,
            amt Float64,
            first String,
            last String,
            gender String,
            street String,
            city String,
            state String,
            zip String,
            lat Float64,
            long Float64,
            city_pop Int64,
            job String,
            dob Date32,
            trans_num String,
            unix_time Int64,
            merch_lat Float64,
            merch_long Float64,
            age Int64,
            hour Int64,
            day_of_week Int32,
            is_night UInt8,
            is_weekend UInt8,
            distance_user_to_merch Float64,
            log_amt Float64,
            log_city_pop Float64,
            log_distance Float64,
            user_id String,
            tx_count_user Int32,
            amt_mean_user Float64,
            fraud_probability Float64,
            fraud_prediction Int32,
            inserted_at DateTime DEFAULT now()
        )
        ENGINE = MergeTree
        PARTITION BY toYYYYMM(trans_date_trans_time)
        PRIMARY KEY (trans_date_trans_time, idx)
        ORDER BY (trans_date_trans_time, idx)
        SETTINGS index_granularity = 8192
```


## Contacts
- **E-Mail:** simonebrancato18@gmail.com
- **LinkedIn:** [Simone Brancato](https://www.linkedin.com/in/simonebrancato18/)
- **GitHub:** [Simone Brancato](https://github.com/SimoneBrancato)
