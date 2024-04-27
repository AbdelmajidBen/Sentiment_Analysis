from kafka import KafkaConsumer

consumer = KafkaConsumer('twitter', bootstrap_servers='kafka1:9092, kafka2:9092, kafka3:9092')

for message in consumer:
    tweet = message.value.decode('utf-8')
    print("Tweet reçu de Kafka:", tweet)
