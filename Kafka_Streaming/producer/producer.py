from kafka import KafkaProducer
import csv
import time

# Initialize the Kafka producer with the bootstrap servers
producer = KafkaProducer(bootstrap_servers='kafka1:9092, kafka2:9092, kafka3:9092')

# Specify the CSV file and topic name
csv_file = 'twitter_validation.csv'
topic_name = 'twitter'

def send_data_to_kafka():
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            tweet_id, title, sentiment, tweet_text = row
            tweet_data = f"{tweet_id},{title},{sentiment},{tweet_text}"
            # Send the message to the specified topic
            # Send the message to the specified topic with a key
            producer.send(topic_name, key=b'Tweet', value=tweet_text.encode('utf-8'))
            time.sleep(0.1)  
#            print("Tweet envoyé à Kafka:", tweet_data.encode('utf-8'))

if __name__ == "__main__":
    send_data_to_kafka()
