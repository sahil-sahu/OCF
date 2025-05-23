import random
import time
from confluent_kafka import Producer

# Configuration parameters
conf = {
   'bootstrap.servers': 'kafka1:9092',  # Replace with your Kafka broker(s)
#    'bootstrap.servers': 'localhost:9090,localhost:9092,localhost:9094',  # Replace with your Kafka broker(s)
}

# Create Producer instance
producer = Producer(conf)

# Delivery callback function
def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result.
       Triggered by poll() or flush()."""
    # if err is not None:
    #     print(f"Message delivery failed: {err}")
    # else:
    #     print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# Function to produce random numbers
def produce_random_numbers():
    print("yo bro")
    try:
        while True:
            # Generate a random number
            random_number = random.randint(1, 100)
            print(random_number)
            # Produce the message to the randomLog topic
            producer.produce('ocf_1', key=str(random_number), value=str(random_number), callback=delivery_report)

            # Poll to ensure delivery reports are processed
            producer.poll(0)

            # Wait for a short time before producing the next message
            time.sleep(0.05)

    except KeyboardInterrupt:
        pass
    finally:
        # Flush to ensure all messages are delivered before closing
        producer.flush()
print("hello world!")

if __name__ == '__main__':
    produce_random_numbers()
