from kafka import KafkaConsumer

consumer = KafkaConsumer('twitter_training', bootstrap_servers='localhost:9092')
for message in consumer:
    tweet = message.value.decode('utf-8')
    print("Tweet reçu de Kafka:", tweet)
