import multiprocessing
import time
import paho.mqtt.client as mqtt
import json
import numpy as np
from scipy.fft import fft, fftfreq
import time
from calc import analyze_wave
def on_connect(client, userdata, flags, rc):
  print("Connected with result code: " + str(rc))

  client.subscribe("device/tmp")




# Function for process 1
def process_one(shared_data):
    def on_message(client, userdata, message):
        # print(shared_data)
        msg = message.payload.decode()  # Decode the message payload
        # print("Received message from client")
        # print(msg)
        # if len(shared_data['value']) > 20:
        #     shared_data['value'] = shared_data['value'][-5:]
        #     shared_data['time'] = time.time()


        try:
            # Try to append the decoded message as an integer along with a timestamp
            shared_data['value'] = shared_data['value'] + [{'height': abs(float(msg)), 'timestamp': -shared_data['time'] + time.time()}]
            # print({'height': float(msg), 'timestamp': time.time()})
        except ValueError:
            # Handle the case where the conversion to integer fails
            print(f"Conversion problem: Unable to convert '{msg}' to an integer")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")    
  
    client = mqtt.Client("OCF")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883)
    client.loop_forever()


# Function for process 2
def process_two(shared_data):
    while True:
        if len(shared_data['value']) < 5 :
            print("No vals")
            time.sleep(10)
            continue
        heights = np.array([entry['height'] for entry in shared_data['value']])
        timestamps = np.array([entry['timestamp'] for entry in shared_data['value']])
        
        result = analyze_wave(heights, timestamps, 40)
        shared_data['value'] = []
        shared_data['time'] = time.time()
        shared_data['time'] = 0
        print(result)
        print("\n")
        # print(shared_data['value'])
        time.sleep(20)

if __name__ == "__main__":
    # Creating a manager to manage shared data
    with multiprocessing.Manager() as manager:
        # Create a shared dictionary
        shared_data = manager.dict()
        shared_data['time'] = time.time()
        shared_data['time'] = 0
        shared_data['value'] = [{'height': 0, 'timestamp':-shared_data['time'] + time.time()},{'height': 0, 'timestamp': -shared_data['time'] + time.time()}]  # Initialize shared variable

        # Creating two processes
        p1 = multiprocessing.Process(target=process_one, args=(shared_data,))
        p2 = multiprocessing.Process(target=process_two, args=(shared_data,))

        # Start both processes
        p1.start()
        p2.start()

        # Wait for both processes to finish
        p1.join()
        p2.join()

        print("Both processes finished execution.")
