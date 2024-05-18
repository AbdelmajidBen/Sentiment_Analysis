from pyspark.sql import SparkSession
from pyspark.ml.feature import CountVectorizer, RegexTokenizer, StopWordsRemover, StringIndexer
from pyspark.ml.classification import NaiveBayes
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Create a Spark session
spark = SparkSession.builder \
    .appName("Sentiment Analysis with Naive Bayes") \
    .getOrCreate()

# Load the CSV file into a DataFrame
file_path = 'twitter_training.csv'
df = spark.read.csv(file_path, header=False, inferSchema=True)

# Define column names
df = df.withColumnRenamed('_c0', 'ID') \
       .withColumnRenamed('_c1', 'Topic') \
       .withColumnRenamed('_c2', 'Sentiment') \
       .withColumnRenamed('_c3', 'Text')

# Drop rows with null values
df = df.dropna()

# Prepare features and label
tokenizer = RegexTokenizer(inputCol='Text', outputCol='words', pattern='\\W')
remover = StopWordsRemover(inputCol='words', outputCol='filtered_words')
vectorizer = CountVectorizer(inputCol='filtered_words', outputCol='features')
indexer = StringIndexer(inputCol='Sentiment', outputCol='label')

# Split data into train and test sets
(train_data, test_data) = df.randomSplit([0.8, 0.2], seed=42)

# Create a Naive Bayes classifier
nb = NaiveBayes(featuresCol='features', labelCol='label', smoothing=1.0)

# Create a pipeline
pipeline = Pipeline(stages=[tokenizer, remover, vectorizer, indexer, nb])

# Train the model
model = pipeline.fit(train_data)

# Make predictions
predictions = model.transform(test_data)

# Evaluate the model
evaluator = MulticlassClassificationEvaluator(labelCol='label', predictionCol='prediction', metricName='accuracy')
accuracy = evaluator.evaluate(predictions)
print(f"Accuracy: {accuracy}")

# Stop the Spark session
spark.stop()
