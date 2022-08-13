import datetime
import json
import os
import sys
import threading

import dateutil.parser

from MongoDB_Main import Document as Doc
from channels.layers import get_channel_layer
from paho.mqtt import client as mqtt_client
from asgiref.sync import async_to_sync
from App.Utilities import read_result_file, write_result_file

# Environmental Variables
broker = str(os.environ['MQTT_BROKER_IP'])  # '167.233.7.5'
port = int(os.environ['MQTT_BROKER_PORT'])  # 1883
topic = str(os.environ['MQTT_MESSAGE_TOPIC'])  # "Test/message"

# broker = "167.233.7.5"
# port = 1883
# topic = "Test/message"
client_id = "jacobsubscriber-001"


# Send To Websocket
def sentLiveData(data):
    text_data = json.dumps(data, indent=4)
    loaded_data = json.loads(text_data)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("notificationGroup", {
        "type": "chat_message",
        "message": loaded_data
    })


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


def save_sensor_data(message):
    time_stamp = datetime.datetime.now()
    loaded_data = json.loads(message)

    result_file_contents = read_result_file()
    result_file_contents["sensor_data"]: list = loaded_data
    result_file_contents["last_updated_timestamp"] = str(time_stamp)
    sentLiveData(result_file_contents)

    # Update Json Data
    write_result_file(json_content=result_file_contents)
    # Write data to DB
    thread = threading.Thread(target=send_to_database, args=[result_file_contents, time_stamp])
    thread.start()


def send_to_database(result_file_contents, time_stamp):
    try:
        result_file_contents["last_updated_timestamp"] = dateutil.parser.parse(str(time_stamp))
        col = "LiveData"
        print(result_file_contents)
        Doc().DB_Write(result_file_contents, col)
    except Exception as ex:
        print("DataBase Write Error: ", ex)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, f_name, exc_tb.tb_lineno)


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

