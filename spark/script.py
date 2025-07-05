from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SimpleTest").getOrCreate()

data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
df = spark.createDataFrame(data, ["Name", "Age"])

df.show()
spark.stop()
