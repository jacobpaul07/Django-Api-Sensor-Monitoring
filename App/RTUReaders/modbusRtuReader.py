from datetime import datetime
import json, time
import sys, os
import threading
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from App.MQTT.mqtt_publisher import mqtt_publish
from channels.layers import get_channel_layer
from App.Utilities import save_sensor_data
from asgiref.sync import async_to_sync
from App.Utilities import read_result_file
from App.SMS.Serial_Input import SerialDevice


print("Jacob")
def read_rtu(settings, config, callback):
    datas_list = []
    c = ModbusClient(method=settings["method"], port=settings["port"],
                     timeout=int(settings["timeout"]),
                     stopbits=int(settings["stop_bit"]),
                     bytesize=int(settings["data_bit"]),
                     parity=settings["parity"],
                     baudrate=int(settings["baud_rate"]))

    # open or reconnect TCP to server
    if not c.connect():
        print("unable to connect to", settings["port"])
        time.sleep(5)
        # if open() is ok, read register
    try:
        if c.connect():
            # if True:
            # read 8 registers at address 0, store result in regs list
            now = datetime.now()
            result_file = read_result_file()
            for tags in config["sensors"]:
                tag_address=int(tags["address"])
                unit_number=int(settings["unit_number"])
                span_high=int(tags["span_high"])
                span_low=int(tags["span_low"])
                sensor_name=tags["devicename"]

                register_data = c.read_input_registers(address=tag_address, count=1, unit=unit_number)
                registerValue = register_data.registers

                sensor_data_list = list(filter(lambda x: (x["tagName"] == sensor_name), result_file["sensor_data"]))
                previous_alert_time = sensor_data_list[0]['alert_timestamp']

                data = {
                    "tagName": sensor_name,
                    "value": registerValue[0] / 10,
                    "alert_timestamp": previous_alert_time
                    }

                datas_list.append(data)

                tag_name = data["tagName"]
                tag_value = data["value"]

                if previous_alert_time != "":
                    # previous_alert_time_pds = pandas.to_datetime(previous_alert_time)
                    previous_alert_time_pds = datetime.strptime(previous_alert_time, '%Y-%m-%d %H:%M:%S.%f')
                    alert_time_difference = now - previous_alert_time_pds
                    difference_seconds = alert_time_difference.seconds

                else:
                    difference_seconds = 0
                
                if difference_seconds >= 600 or difference_seconds==0:
                    if tag_value > span_high:
                        alert_msg = "High - {0}".format(tag_value) 
                        SerialDevice().serial_write(config=config, tag_name=tag_name, alert=alert_msg)
                        data["alert_timestamp"]=str(now)
                    
                    elif tag_value < span_low:
                        alert_msg = "Low - {0}".format(tag_value) 
                        SerialDevice().serial_write(config=config, tag_name=tag_name, alert=alert_msg)
                        data["alert_timestamp"]=str(now)

            mqtt_publish(message=datas_list)
            save_sensor_data(datas_list)
            c.close()

    except Exception as exception:
        print("Device is not Connected Error:", exception)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, f_name, exc_tb.tb_lineno)
        print("Check the port or Restart the system and try again")

    thread = threading.Thread(
        target=callback,
        args=(settings, config, callback)
    )
    thread.start()

    return datas_list


def send_alert(config, tag_name, alert):
    user_config = config["user"]
    mobile_number = user_config["mobile"]
    message = "{0} {1} is {2}".format(mobile_number, tag_name, alert)
    SerialDevice.serial_write(message)
    time.sleep(2)
