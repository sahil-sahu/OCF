from confluent_kafka import Consumer, Producer
import json
import math
from collections import deque
from datetime import datetime

# Constants
G = 9.81        # gravity (m/s²)
RHO = 1025      # seawater density (kg/m³)
DEPTH = 5.0     # assumed depth (m)

# Kafka config
consumer_conf = {
    'bootstrap.servers': 'localhost:9090',
    'group.id': 'wave-analyzer',
    'auto.offset.reset': 'earliest'
}

producer_conf = {
    'bootstrap.servers': 'localhost:9090'
}

consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

consumer.subscribe(['ocf_1'])

# Keep track of recent values for zero-crossing
wave_history = deque(maxlen=100)
last_crossing_time = None

def get_timestamp():
    return datetime.utcnow().isoformat() + "Z"

def derive_wave_parameters(height, timestamp, period, depth=DEPTH):
    velocity = math.sqrt(G * depth)
    wavelength = period * velocity
    energy = (1/8) * RHO * G * height**2
    power = energy * velocity
    freq = 1 / period if period > 0 else 0

    return {
        'timestamp': timestamp,
        'depth': depth,
        'wave_height': height,
        'time_period': period,
        'frequency': freq,
        'wavelength': wavelength,
        'wave_velocity': velocity,
        'wave_energy': energy,
        'wave_power': power
    }

def detect_zero_crossing(current_height, previous_height):
    return previous_height < 0 and current_height >= 0

try:
    print("Listening to 'ocf' topic...")
    previous_height = None

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        try:
            height = float(msg.value().decode('utf-8'))  # value is just a float

            timestamp = get_timestamp()
            wave_history.append((timestamp, height))

            # Wait until we have enough data
            if previous_height is None:
                previous_height = height
                continue

            # Detect zero-crossing
            if detect_zero_crossing(height, previous_height):
                if last_crossing_time:
                    # Estimate period (time between crossings * 2)
                    t1 = datetime.fromisoformat(last_crossing_time.replace("Z", ""))
                    t2 = datetime.fromisoformat(timestamp.replace("Z", ""))
                    time_diff = (t2 - t1).total_seconds()
                    period = time_diff * 2  # One full wave

                    derived = derive_wave_parameters(
                        height=height,
                        timestamp=timestamp,
                        period=period
                    )

                    producer.produce('ocf_derive', json.dumps(derived).encode('utf-8'))
                    producer.flush()
                    print("Derived and sent:", derived)

                last_crossing_time = timestamp

            previous_height = height

        except Exception as e:
            print("Processing error:", e)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    consumer.close()
