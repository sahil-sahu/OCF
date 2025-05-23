#!/bin/bash

# Wait for Kafka to start
sleep 1

kafka-topics.sh --create --topic connect-offsets --bootstrap-server localhost:9092 --partitions 1 --replication-factor 2
kafka-topics.sh --create --topic connect-configs --bootstrap-server localhost:9092 --partitions 1 --replication-factor 2
kafka-topics.sh --create --topic connect-status --bootstrap-server localhost:9092 --partitions 1 --replication-factor 2

# Configure the cleanup policy for the connect-offsets topic
kafka-configs.sh --alter --entity-type topics --entity-name connect-offsets --add-config cleanup.policy=compact --bootstrap-server localhost:9092
kafka-configs.sh --alter --entity-type topics --entity-name connect-status --add-config cleanup.policy=compact --bootstrap-server localhost:9092
kafka-configs.sh --alter --entity-type topics --entity-name connect-configs --add-config cleanup.policy=compact --bootstrap-server localhost:9092
