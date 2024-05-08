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
df_twitter = spark.read.csv("/root/twitter_training.csv", header=False, inferSchema=True)

# Provide column names manually (replace with actual column names)
columns = ["Tweet ID", "Entity", "Sentiment", "TweetContent"]
df_twitter = df_twitter.toDF(*columns)

# Drop the 'Tweet ID' column
df_twitter = df_twitter.drop("Tweet ID")

# Drop rows with null values in the 'Tweet content' column
df_twitter = df_twitter.dropna(subset=["TweetContent"])

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
df_twitter = df_twitter.withColumn("cleaned_tweet", clean_and_lowercase_udf("TweetContent"))


indexer = StringIndexer(inputCol="Sentiment", outputCol="label")
tokenizer = Tokenizer(inputCol="cleaned_tweet", outputCol="tokens")
stop_words_remover = StopWordsRemover(inputCol="tokens", outputCol="filtered_tweet")
cv = CountVectorizer(inputCol="filtered_tweet", outputCol="raw_features")
idf = IDF(inputCol="raw_features", outputCol="features")

# Add indexer, lemmatization, and the rest of the pipeline stages
df_twitter = indexer.fit(df_twitter).transform(df_twitter)


train_data, test_data = df_twitter.randomSplit([0.8, 0.2], seed=42)


# Assuming you have defined tokenizer, stop_words_remover, cv, idf, train_data, and test_data earlier in your code

# Create a LinearSVC object
svm = LinearSVC(maxIter=10, regParam=0.1, featuresCol="features", labelCol="label")

# Create an OneVsRest object
ovr = OneVsRest(classifier=svm)

# Create a Pipeline for data preprocessing and classification
data_preprocessing_pipeline = Pipeline(stages=[tokenizer, stop_words_remover, cv, idf, ovr])

# Fit the pipeline to the training data
pipeline_model = data_preprocessing_pipeline.fit(train_data)


model_path = "/root/model"
pipeline_model.save(model_path)



spark.stop()