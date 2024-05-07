from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from pyspark.ml import Pipeline
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer, IDF, StringIndexer
from pyspark.ml.classification import LinearSVC, OneVsRest
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import re

# Create a SparkSession
spark = SparkSession.builder \
    .appName("pipeline_twitter") \
    .getOrCreate()

# Read the CSV file into a DataFrame
df_twitter = spark.read.csv("../twitter_training.csv", header=False, inferSchema=True)

# Provide column names manually (replace with actual column names)
columns = ["Tweet ID", "Entity", "Sentiment", "Tweet content"]
df_twitter = df_twitter.toDF(*columns)

# Drop the 'Tweet ID' column
df_twitter = df_twitter.drop("Tweet ID")

# Drop rows with null values in the 'Tweet content' column
df_twitter = df_twitter.dropna(subset=["Tweet content"])

# Define the clean_and_lowercase function
def clean_and_lowercase(text):
    # Convert the text to lowercase
    text_lower = text.lower()
    # Remove special characters, punctuation, and unnecessary symbols
    cleaned_text = re.sub(r'[^\w\s]', '', text_lower)
    # Return the cleaned text
    return cleaned_text

# Define the UDF for clean_and_lowercase function
clean_and_lowercase_udf = udf(clean_and_lowercase, StringType())

# Apply the UDF to the 'Tweet content' column
df_twitter = df_twitter.withColumn("cleaned_tweet", clean_and_lowercase_udf("Tweet content"))

# Define preprocessing stages
indexer = StringIndexer(inputCol="Sentiment", outputCol="label")
tokenizer = Tokenizer(inputCol="cleaned_tweet", outputCol="tokens")
stop_words_remover = StopWordsRemover(inputCol="tokens", outputCol="filtered_tweet")
cv = CountVectorizer(inputCol="filtered_tweet", outputCol="raw_features")
idf = IDF(inputCol="raw_features", outputCol="features")

# Create a pipeline for preprocessing
data_preprocessing_pipeline = Pipeline(stages=[indexer, tokenizer, stop_words_remover, cv, idf])

# Fit the preprocessing pipeline to the data
preprocessing_model = data_preprocessing_pipeline.fit(df_twitter)
df_transformed = preprocessing_model.transform(df_twitter)


# Specify the path where you want to save the model
model_path = "preprocessing_pipeline1"
# Save the preprocessing model
#preprocessing_model.save(model_path)


# Split the data into train and test sets
train_data, test_data = df_transformed.randomSplit([0.8, 0.2], seed=42)

# Create a LinearSVC classifier
svm = LinearSVC(maxIter=10, regParam=0.1, featuresCol="features", labelCol="label")

# Create an OneVsRest classifier
ovr = OneVsRest(classifier=svm)

# Train the OneVsRest model
ovr_model = ovr.fit(train_data)

# Make predictions on the test data
predictions = ovr_model.transform(test_data)

# Evaluate the model
evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Accuracy SVM:", accuracy)

spark.stop()