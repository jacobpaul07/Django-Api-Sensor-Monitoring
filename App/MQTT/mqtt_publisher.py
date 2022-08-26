import json
import os
import sys

import paho.mqtt.client as mqtt


def mqtt_publish(message):
    try:
        mqtt_client = mqtt.Client("jacob-clientid")
        # Environmental Variables
        host = str(os.environ['MQTT_BROKER_IP'])  # '167.233.7.5'
        port = int(os.environ['MQTT_BROKER_PORT'])  # 1883
        topic = str(os.environ['MQTT_MESSAGE_TOPIC'])  # "Test/message"
        keepalive = 60
        mqtt_client.connect(host, port, keepalive)
        mqtt_client.loop_start()
        json_message = json.dumps(message)
        mqtt_client.publish(topic, json_message, qos=2)
        mqtt_client.loop_stop()

    except Exception as ex:
        print("Mqtt_Publisher Error: ", ex)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, f_name, exc_tb.tb_lineno)

def mqtt_gps_publish(message):
    try:
        mqtt_client = mqtt.Client("jacob-clientid")
        # Environmental Variables
        host = str(os.environ['MQTT_BROKER_IP'])  # '167.233.7.5'
        port = int(os.environ['MQTT_BROKER_PORT'])  # 1883
        topic = str(os.environ['MQTT_GPS_MESSAGE_TOPIC'])  # "IoT_SM/GPS"
        keepalive = 60
        mqtt_client.connect(host, port, keepalive)
        mqtt_client.loop_start()
        json_message = json.dumps(message)
        mqtt_client.publish(topic, json_message, qos=2)
        mqtt_client.loop_stop()

    except Exception as ex:
        print("Mqtt_Publisher Error: ", ex)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, f_name, exc_tb.tb_lineno)