import paho.mqtt.client as mqtt
import json


def on_connect(client, userdata, flags, rc):
  print("Connected with result code: " + str(rc))

  client.subscribe("ocf_1")


def on_message(client, userdata, message):
  msg = message.payload.decode()
  print(message.payload)
  print("Received message: " + message.topic + " " + msg)
  # if msg == "STATUS":
  #   message = {
  #       "id": "5531b435-3ac8-47c7-8075-53c9383003ea",
  #       "state": "ON",
  #       "type": "STATUS"
  #   }
  #   client.publish("ledcontrol", json.dumps(message))


client = mqtt.Client("innovateY")
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883)
message = {
    "sensors": [
        {
            "5531b435-3ac8-47c7-8075-53c9383003ea": True
        },
    ],
    "state": "ON",
    "type": "Yo"
}
# client.publish("ledcontrol", j
# son.dumps(message))

client.loop_forever()