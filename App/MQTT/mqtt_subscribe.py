import os
import sys
import threading

from paho.mqtt import client as mqtt_client
from App.Utilities import save_sensor_data

# Environmental Variables
broker = str(os.environ['MQTT_BROKER_IP'])     # '167.233.7.5'
port = int(os.environ['MQTT_BROKER_PORT'])     # 1883
topic = [str(os.environ['MQTT_GPS_MESSAGE_TOPIC']) ]  # "Test/message"
client_id = "jacobsubscriber-001"


def connect_mqtt() -> mqtt_client:
    print("Connected to MQTT Broker!")
    def on_connect(client, userdata, flags, rc):
        if rc != 0:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id="jacobsubscriber", clean_session=False)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        print("------------------------------------------------------------")
        received_message = msg.payload.decode()
        save_sensor_data(received_message)

    client.subscribe(topic)
    client.on_message = on_message


def mqtt_subscribe():
    try:
        print("MQTT Subscriber Started")
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()

    except Exception as ex:
        print("MQTT Subscribe Error: ", ex)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, f_name, exc_tb.tb_lineno)

        print("Restarted")
        thread = threading.Thread(target=mqtt_subscribe, args=())
        thread.start()
