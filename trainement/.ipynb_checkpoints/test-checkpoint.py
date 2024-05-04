from pyspark.ml import PipelineModel
from pyspark.ml.classification import OneVsRestModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import re


def clean_and_lowercase(text):
    # Convert the text to lowercase
    text_lower = text.lower()
    # Remove special characters, punctuation, and unnecessary symbols
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text_lower)
    # Return the cleaned text
    return cleaned_text

# Create a SparkSession
spark = SparkSession.builder \
    .appName("pipeline_twitter4") \
    .getOrCreate()

# Load the pipeline model from disk
model = OneVsRestModel.load("model")
input_string = "Hey My Nmae is ::"
pipeline_model = PipelineModel.load("preprocessing_pipeline1/")# Create a DataFrame with a single column named "Tweet_content"

# Create a DataFrame with a single column named "Tweet_content"
df = spark.createDataFrame([(input_string,)], ["Tweet_content"])


# Define the UDF
clean_and_lowercase_udf = udf(clean_and_lowercase, StringType())

df_cleaned = df.withColumn("cleaned_tweet", clean_and_lowercase_udf("Tweet_content"))

out_pipeline = pipeline_model.transform(df_cleaned)

new_prediction = model.transform(out_pipeline)

print(new_prediction.select("prediction").toPandas())