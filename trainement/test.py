from pyspark.ml import PipelineModel
from pyspark.ml.classification import OneVsRestModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import re




# Function to clean and lowercase text
def clean_and_lowercase(text):
    text_lower = text.lower()
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text_lower)
    return cleaned_text

# Create a SparkSession
spark = SparkSession.builder \
    .appName("pipeline_twitter4") \
    .getOrCreate()

# Load the pipeline model from disk
model = OneVsRestModel.load("model")
input_string = "Hey My Name is ::"
pipeline_model = PipelineModel.load("preprocessing_pipeline1/")

# Create a DataFrame with a single column named "Tweet_content"
df = spark.createDataFrame([(input_string,)], ["Tweet_content"])

# Define the UDF for cleaning and lowercase
clean_and_lowercase_udf = udf(clean_and_lowercase, StringType())

# Apply the UDF to clean and lowercase the text
df_cleaned = df.withColumn("cleaned_tweet", clean_and_lowercase_udf("Tweet_content"))

# Apply the preprocessing pipeline to the cleaned DataFrame
out_pipeline = pipeline_model.transform(df_cleaned)

# Make predictions using the model
new_prediction = model.transform(out_pipeline)

# Select only the "prediction" column from the DataFrame
predicted_values = new_prediction.select("prediction")

# If you want to convert the DataFrame to a list of predicted values, you can use the collect method
predicted_values_list = predicted_values.collect()

# Extract the predicted values from the list
predictions = [row.prediction for row in predicted_values_list]

# Print or return the predictions
print(predictions)
