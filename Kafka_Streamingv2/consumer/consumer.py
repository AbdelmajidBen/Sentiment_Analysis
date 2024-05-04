from kafka import KafkaConsumer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk
import re

# Download NLTK resources if not already present
nltk.download('punkt')
nltk.download('stopwords')

# Initialize stemmer and stopwords
stemmer = SnowballStemmer('english')
stop_words = set(stopwords.words('english'))

# Kafka consumer setup
consumer = KafkaConsumer('twitter', bootstrap_servers='kafka1:9092, kafka2:9092, kafka3:9092')

# Iterate over messages received from Kafka
for message in consumer:
    tweet = message.value.decode('utf-8')
    print("Tweet reçu de Kafka:", tweet)

    # Tokenize the tweet into words
    words = word_tokenize(tweet)

    # Filter out stopwords and perform stemming on remaining words
    filtered_words = [stemmer.stem(word.lower()) for word in words if word.lower() not in stop_words and re.match('^[a-zA-Z]+$', word)]

    # Print the filtered and stemmed words
    print("Mots filtrés et stemmés:", filtered_words)
