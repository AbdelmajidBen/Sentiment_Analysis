FROM bitnami/spark:3.5

USER root

# Install the required package
RUN /opt/bitnami/spark/bin/spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0
RUN /opt/bitnami/spark/bin/spark-shell --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.0
RUN pip install numpy pandas psutil


COPY trainement/twitter_training.csv /root/twitter_training.csv
#COPY trainement/model/ /root/model
COPY trainement/preprocessing_pipeline1 /root/pipeline
COPY trainement/trainement.py /root/trainement.py

RUN spark-submit /root/trainement.py

ENV SPARK_MODE=master \
    SPARK_RPC_AUTHENTICATION_ENABLED=no \
    SPARK_RPC_ENCRYPTION_ENABLED=no \
    SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no \
    SPARK_SSL_ENABLED=no \
    SPARK_USER=spark

# Expose port 8080
EXPOSE 8080

# Copy consumer.py into the container
COPY trainement/consumer.py /root/consumer.py

#RUN chmod +rx /root/consumer.py


# Set the entry point script


CMD /opt/bitnami/spark/sbin/start-master.sh & \
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0,org.mongodb.spark:mongo-spark-connector_2.12:3.0.0 /root/consumer.py
