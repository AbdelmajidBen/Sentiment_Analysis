# Real-Time Twitter Sentiment Analysis with Kafka, PySpark, and Machine Learning

## Introduction
This project aims to perform real-time sentiment analysis on Twitter data using Apache Kafka, PySpark, and machine learning models. The project includes modules for data ingestion, preprocessing, model training, real-time prediction, and logging of results in MongoDB.

## Requirements
To run this project, you need to have the following installed:
- Apache Kafka
- Apache Zookeeper
- Python (version >= 3.6)
- Pipenv (for managing Python dependencies)

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your_username/twitter-sentiment-analysis.git

   cd twitter-sentiment-analysis
2. Install Python dependencies using Pipenv:
   ```bash
   pipenv install
## Starting Kafka and Zookeeper
  ### Start Zookeeper:
    bin/zookeeper-server-start.sh config/zookeeper.properties
  ### Start Kafka:
    bin/kafka-server-start.sh config/server.properties
## Files & Their Purposes:
  - producer.py: Python script for reading tweets from a CSV file and producing them to a Kafka topic.
  - consumer.py: Python script for consuming tweets from a Kafka topic and performing sentiment analysis using PySpark.
  - twitter_analysis.py: Python script for preprocessing Twitter data, training machine learning models, and predicting sentiment.
  - t1.py: Python script containing the logistic regression model training code for sentiment analysis.
## Execution:
  1.  Run the producer script to start producing tweets to the Kafka topic:
     ```bash
     python producer.py
  2. Run the consumer script to start consuming tweets from the Kafka topic and perform sentiment analysis:
        ```bash
     python consumer.py
     
  3. Execute the twitter_analysis.py script to preprocess data, train models, and make real-time predictions:
        ```bash
     python twitter_analysis.py
     
  4. Execute the t1.py script to train a logistic regression model for sentiment analysis:
        ```bash
     python t1.py
     
## Author :
Abdelmajid Benjelloun / Ayoub Bakkali / Salma Nidar 

## License
This project is licensed under the MIT License. See the LICENSE file for details.

