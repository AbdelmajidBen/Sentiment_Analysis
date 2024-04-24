from kafka import KafkaProducer
import csv
import time

producer = KafkaProducer(bootstrap_servers='kafka1:9092')
csv_file = 'twitter_training.csv'
topic_name = 'twitter'
topic_name = topic_name.encode('utf-8')
def send_data_to_kafka():
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            tweet_id = row[0]  
            title = row[1]  
            sentiment = row[2]  
            tweet_text = row[3] 
            tweet_data = f"{tweet_id},{title},{sentiment},{tweet_text}"
            producer.send('twitter_training', topic_name)
            time.sleep(0.1)  
            print("Tweet envoyé à Kafka:", tweet_data)

if __name__ == "__main__":
    send_data_to_kafka()
