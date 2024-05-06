FROM bitnami/spark:3.5

USER root

# Install the required package
RUN /opt/bitnami/spark/bin/spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0


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
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 /root/consumer.py
