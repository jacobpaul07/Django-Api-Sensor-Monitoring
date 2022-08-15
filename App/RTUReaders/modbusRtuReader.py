import json
import threading

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from App.MQTT.mqtt_publisher import mqtt_publish
from channels.layers import get_channel_layer
from App.Utilities import save_sensor_data
from asgiref.sync import async_to_sync


def read_rtu(settings, io_tags, callback):
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
        # if open() is ok, read register
    try:
        if c.connect():
            # if True:
            # read 8 registers at address 0, store result in regs list

            for tags in io_tags["Sensors"]:
                register_data = c.read_input_registers(address=int(tags["address"]),
                                                       count=1,
                                                       unit=int(settings["unit_number"]))
                registerValue = register_data.registers

                data = {
                    "tagName": tags["devicename"],
                    "value": registerValue[0] / 10,
                }

                datas_list.append(data)
            mqtt_publish(message=datas_list)
            save_sensor_data(datas_list)

            print(datas_list)
            c.close()

    except Exception as exception:
        print("Device is not Connected Error:", exception)

    thread = threading.Thread(
        target=callback,
        args=(settings, io_tags, callback)
    )
    thread.start()

    return datas_list
