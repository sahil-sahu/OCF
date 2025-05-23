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
    'bootstrap.servers': 'kafka0:9092',
    'group.id': 'wave-analyzer',
    'auto.offset.reset': 'earliest'
}

producer_conf = {
    'bootstrap.servers': 'kafka0:9092'
}

consumer = Consumer(consumer_conf)
producer = Producer(producer_conf)

consumer.subscribe(['ocf_1'])

# For detecting troughs (local minima)
second_previous_height = None
previous_height = None
last_crossing_time = None

def get_timestamp():
    return datetime.utcnow().isoformat() + "Z"

last_valid = {
    'time_period': None,
    'frequency': None,
    'wavelength': None,
}

def derive_wave_parameters(height, timestamp, period=None, depth=DEPTH):
    velocity = math.sqrt(G * height)
    wavelength = period * velocity if period else last_valid['wavelength']
    energy = (1/8) * RHO * G * height**2
    power = energy * velocity
    freq = 1 / period if period and period > 0 else last_valid['frequency']

    # Update cache if values are present
    if period:
        last_valid['time_period'] = period
        last_valid['frequency'] = freq
        last_valid['wavelength'] = wavelength

    return {
        'timestamp': timestamp,
        'depth': depth,
        'wave_height': height,
        'time_period': last_valid['time_period'],
        'frequency': last_valid['frequency'],
        'wavelength': last_valid['wavelength'],
        'wave_velocity': velocity,
        'wave_energy': energy,
        'wave_power': power
    }

print("Listening to 'ocf_1' topic...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        try:
            payload = msg.value().decode('utf-8')
            jsonLoad = json.loads(payload)
            height = float(str(jsonLoad.get("height", 0)).strip())

            timestamp = get_timestamp()

            # Detect trough
            period = None
            if second_previous_height is not None and previous_height is not None:
                if previous_height < second_previous_height and previous_height < height:
                    if last_crossing_time:
                        t1 = datetime.fromisoformat(last_crossing_time.replace("Z", ""))
                        t2 = datetime.fromisoformat(timestamp.replace("Z", ""))
                        period = (t2 - t1).total_seconds()
                    last_crossing_time = timestamp

            # Compute and send derived wave data
            derived = derive_wave_parameters(
                height=height,
                timestamp=timestamp,
                period=period
            )

            producer.produce('ocf_derive', json.dumps(derived).encode('utf-8'))
            producer.flush()
            print("Sent:", derived)

            # Update history
            second_previous_height = previous_height
            previous_height = height

        except Exception as e:
            print("Processing error:", e)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    consumer.close()
