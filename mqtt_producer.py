import paho.mqtt.client as mqtt
import time
import json
import random

# MQTT Broker config
broker_address = "localhost"  # or your broker IP like "192.168.29.48"
broker_port = 1883
mqtt_topic = "ocf_1"

# MQTT Client setup
client = mqtt.Client("PythonPublisher")

def connect():
    print(f"Connecting to MQTT broker at {broker_address}:{broker_port}...")
    client.connect(broker_address, broker_port)
    print("Connected!")

# Sample payload generator
def generate_payload():
    return {
        "height": round(random.uniform(30.0, 60.0), 2)
    }

# Main loop
def publish_loop():
    while True:
        payload = generate_payload()
        payload_json = json.dumps(payload)
        client.publish(mqtt_topic, payload_json)
        print(f"Published to {mqtt_topic}: {payload_json}")
        time.sleep(0.05)  # Publish every 5 seconds

if __name__ == "__main__":
    connect()
    publish_loop()
