from confluent_kafka import Consumer, KafkaException, KafkaError

# Configuration parameters
conf = {
    'bootstrap.servers': 'localhost:9092',  # Replace with your Kafka broker(s)
    'group.id': 'randomLog-consumer',          # Consumer group id
    'auto.offset.reset': 'earliest',        # Start reading at the earliest offset
    'enable.auto.commit': False             # Disable auto-commit of offsets
}

# Create Consumer instance
consumer = Consumer(conf)

# Subscribe to the topic
consumer.subscribe(['randomLog'])

# Function to handle consumed messages
def consume_all_messages():
    try:
        while True:
            # Poll for a message
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    print(f"Reached end of partition {msg.partition()} at offset {msg.offset()}")
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                # Message received, process it
                print(f"Received message: {msg.value().decode('utf-8')}")

                # Manually commit the message's offset after processing
                consumer.commit(asynchronous=False)

    except KeyboardInterrupt:
        pass
    finally:
        # Close down consumer to commit final offsets and leave the group cleanly
        consumer.close()

if __name__ == '__main__':
    consume_all_messages()
