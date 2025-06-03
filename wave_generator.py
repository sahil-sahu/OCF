import time
import math
import paho.mqtt.client as mqtt
import json
# MQTT Config
# BROKER = "localhost"         # Change to your broker's address
BROKER = "10.1.23.254"         # Change to your broker's address
PORT = 1883
TOPIC = "ocf_1"

# Wave parameters
AMPLITUDE = 1.0              # in meters
FREQUENCY = 1           # in Hz (wave cycles per second)
SAMPLING_RATE = 25          # in Hz
SLEEP_TIME = 1.0 / SAMPLING_RATE

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker" if rc == 0 else f"Failed to connect: {rc}")

client.on_connect = on_connect
client.connect(BROKER, PORT, 60)
client.loop_start()

print("Publishing simulated wave height data...")

start_time = time.time()

try:
    while True:
        current_time = time.time() - start_time  # seconds since start
        wave_height = AMPLITUDE * math.sin(2 * math.pi * FREQUENCY * current_time)

        # Publish as plain float string (e.g. "0.452")
        client.publish(TOPIC, json.dumps({"height":f"{wave_height*3+20}"}))
        # client.pu
        print(f"Published: {wave_height:.6f}")

        time.sleep(SLEEP_TIME)

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    client.loop_stop()
    client.disconnect()
