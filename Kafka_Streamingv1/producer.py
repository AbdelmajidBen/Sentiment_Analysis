from kafka import KafkaConsumer, KafkaProducer
import threading

def producer_function():
    producer = KafkaProducer(bootstrap_servers=['kafka1:9092', 'kafka2:9093', 'kafka3:9094'])

    for i in range(5):
        tweet_data = "This is tweet {}".format(i)
        producer.send('twitter_training', value=bytes(tweet_data, 'utf-8'))
        print("Tweet envoyé à Kafka:", tweet_data)
        producer.flush()

def consumer_function():
    consumer = KafkaConsumer('twitter_training', bootstrap_servers=['kafka1:9092', 'kafka2:9093', 'kafka3:9094'])
    for message in consumer:
        tweet = message.value.decode('utf-8')
        print("Tweet reçu de Kafka:", tweet)

if __name__ == "__main__":
    producer_thread = threading.Thread(target=producer_function)
    consumer_thread = threading.Thread(target=consumer_function)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()
