from kafka import KafkaConsumer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import nltk

nltk.download('punkt')
nltk.download('stopwords')
stemmer = SnowballStemmer('english')
stop_words = set(stopwords.words('english'))

consumer = KafkaConsumer('twitter_training', bootstrap_servers='localhost:9092')

for message in consumer:
    tweet = message.value.decode('utf-8')
    print("Tweet reçu de Kafka:", tweet)
    words = word_tokenize(tweet)
    filtered_words = [stemmer.stem(word.lower()) for word in words if word.lower() not in stop_words]
    
    print("Mots filtrés:", filtered_words)
