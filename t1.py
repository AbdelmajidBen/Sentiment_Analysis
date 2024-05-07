from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer, IDF, StringIndexer
from pyspark.ml.classification import LinearSVC
from pyspark.sql.connect.functions import from_json
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, StructType, StructField
import re
import nltk
from nltk.stem import WordNetLemmatizer

# Initialiser SparkSession
spark = SparkSession.builder \
    .appName("TwitterStreamProcessing") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()

# Définir le schéma pour les données Twitter
columns = ["Entity", "Sentiment", "Tweet content"]
schema = StructType([
    StructField(name, StringType(), True) for name in columns
])

# Lire les données en streaming depuis Kafka
df_twitter_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka1:9092, kafka2:9093, kafka3:9094") \
    .option("subscribe", "twitter_training") \
    .load() \
    .selectExpr("CAST(value AS STRING)")

# Convertir les données JSON en DataFrame
df_twitter_stream = df_twitter_stream.select(from_json(df_twitter_stream.value, schema).alias("data")).select("data.*")

# Définir les fonctions de prétraitement
def clean_and_preprocess(text):
    text_lower = text.lower()
    cleaned_text = re.sub(r'[^\w\s]', '', text_lower)
    tokens = cleaned_text.split()
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(lemmatized_tokens)

# Créer les UDF pour les fonctions de prétraitement
clean_and_preprocess_udf = udf(clean_and_preprocess, StringType())

# Créer les étapes de la pipeline de traitement des données
tokenizer = Tokenizer(inputCol="Tweet content", outputCol="tokens")
stop_words_remover = StopWordsRemover(inputCol="tokens", outputCol="filtered_tweet")
cv = CountVectorizer(inputCol="filtered_tweet", outputCol="raw_features")
idf = IDF(inputCol="raw_features", outputCol="features")
indexer = StringIndexer(inputCol="Sentiment", outputCol="label")

# Créer la pipeline
pipeline = Pipeline(stages=[tokenizer, stop_words_remover, cv, idf, indexer])

# Entraîner le pipeline sur les données d'entraînement
train_data = spark.read.csv("twitter_training.csv", header=True, schema=schema)
pipeline_model = pipeline.fit(train_data)

# Appliquer le pipeline sur les données en streaming
df_processed_stream = pipeline_model.transform(df_twitter_stream)

# Entraîner le modèle SVM
svm = LinearSVC(maxIter=10, regParam=0.1, featuresCol="features", labelCol="label")
svm_model = svm.fit(df_processed_stream)

# Afficher les coefficients du modèle SVM
print("SVM Coefficients: " + str(svm_model.coefficients))

# Effectuer des prédictions sur les données en streaming
predictions = svm_model.transform(df_processed_stream)

# Afficher les prédictions
predictions.select("Tweet content", "prediction").show()

# Démarrer la lecture en continu et attendre que le traitement se termine
query = predictions \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
