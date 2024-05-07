from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
from pyspark.ml import PipelineModel
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import re

# Model and pipeline PATH
model_path = "/root/model"

# Import pipeline 
pipeline = PipelineModel.load(model_path)

def clean_and_lowercase(text):
    text_lower = text.lower()
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text_lower)
    return cleaned_text

# Config 
spark = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("TwitterSentimentAnalysis") \
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
df = df.withColumn("Tweet content", expr("string(value)")).drop("value")

clean_and_lowercase_udf = udf(clean_and_lowercase, StringType())

df = df.withColumn("cleaned_tweet", clean_and_lowercase_udf("Tweet content"))

# Define the function to apply transformations inside foreachBatch
def process_batch(df, epoch_id):
    # Apply transformations to the DataFrame
    transformed_df = pipeline.transform(df)
    
    # Write the transformed data to MongoDB
    transformed_df.select("prediction", "Tweet content").write \
        .format("com.mongodb.spark.sql.DefaultSource") \
        .mode("append") \
        .option("uri", "mongodb://admin:1234@mongodb:27017") \
        .option("database", "Twitter") \
        .option("collection", "tweets") \
        .save()

# Apply transformations and start the streaming query
query = df \
    .writeStream \
    .foreachBatch(process_batch) \
    .outputMode("append") \
    .start()

# Await termination of the streaming query
query.awaitTermination()
