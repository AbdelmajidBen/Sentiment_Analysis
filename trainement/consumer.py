from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, current_timestamp
from pyspark.ml import PipelineModel
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from pyspark.ml.functions import vector_to_array  # Import added
import re
from pyspark.sql.functions import lit
import psutil  # Import the psutil library for system monitoring


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
df = df.withColumn("TweetContent", expr("string(value)")).drop("value")

clean_and_lowercase_udf = udf(clean_and_lowercase, StringType())

df = df.withColumn("cleaned_tweet", clean_and_lowercase_udf("TweetContent"))

def get_system_usage():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage

# Define the function to apply transformations inside foreachBatch
def process_batch(df, epoch_id):
    # Get CPU and memory usage
    cpu_usage, memory_usage = get_system_usage()
    
    # Apply transformations to the DataFrame
    transformed_df = pipeline.transform(df)
    
    # Add timestamp column
    transformed_df = transformed_df.withColumn("timestamp", current_timestamp())
    
    # Convert rawPrediction column to array
    transformed_df = transformed_df.withColumn("rawPredictionArray", vector_to_array("rawPrediction"))
    
    # Add CPU and memory usage columns
    transformed_df = transformed_df.withColumn("cpu_usage", lit(cpu_usage))
    transformed_df = transformed_df.withColumn("memory_usage", lit(memory_usage))
    
    # Write the transformed data to MongoDB
    transformed_df.select("timestamp", "prediction", "TweetContent", "rawPredictionArray", "cpu_usage", "memory_usage").write \
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
