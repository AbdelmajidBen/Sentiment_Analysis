
from kafka import KafkaConsumer

consumer = KafkaConsumer('twitter_training', bootstrap_servers=['kafka1:9092', 'kafka2:9093', 'kafka3:9094'])
for message in consumer:
    tweet = message.value.decode('utf-8')
    print("Tweet reçu de Kafka:", tweet)

