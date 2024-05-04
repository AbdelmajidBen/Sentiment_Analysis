from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr

# Config 
spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("TwitterSentimentAnalysis") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()

# Read the data from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka1:9092,kafka2:9093,kafka3:9094") \
    .option("subscribe", "twitter") \
    .option("startingOffsets", "latest") \
    .option("header", "true") \
    .load()

# Decode the key column into strings
df = df.withColumn("key", expr("string(key)"))

# Decode the value column into strings if it's a string
df = df.withColumn("value", expr("string(value)"))

# Start the streaming query and write to console
query = df.select("value").writeStream.outputMode("append").format("console").option("truncate", "false").start()

# Wait for the streaming query to terminate
query.awaitTermination()
