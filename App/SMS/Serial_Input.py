import os
import sys
import serial
import time
import App.globalsettings as app_setting
from App.index import read_usr

class SerialDevice:
    if not app_setting.serial_device_started:
        app_setting.serial_device_started = True
        SERIALPORT=os.environ['SERIALPORT']
        device = serial.Serial(port=SERIALPORT, baudrate=115200)
        
    def serial_write(self, tag_name, alert):
        try:
            users = read_usr()
            user_list:list = users["user"]
            for user in user_list:
                mobile_number = user["mobile"]
                message = "{0} {1} is {2}".format(mobile_number, tag_name, alert)
                self.device.write(bytes(message, 'utf-8'))
                time.sleep(5)
                data = self.device.readline()
                print(data)
                return data

        except Exception as ex:
            print("Arduino Error: Device not Detected", ex)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, f_name, exc_tb.tb_lineno)
            print("Check the port or Restart the system and try again")
