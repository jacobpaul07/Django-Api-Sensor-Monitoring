# Importing all the necessary Libs
import os
import sys
import threading
import App.globalsettings as appsetting
from App.index import read_setting, read_com_setting
from App.RTUReaders.modbusRtuReader import read_rtu

# Initializing The StopThread as boolean-False
stopThread: bool = False


def modbus_rtu():
    try:
        data = read_setting()
        com_setting = read_com_setting()

        # Initializing Threading
        thread = threading.Thread(
            target=read_rtu,
            args=(com_setting, data, thread_callback,)
        )
        # Starting the Thread
        thread.start()
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, f_name, exc_tb.tb_lineno)
        print("Thread callback error: ", ex)


# Callback Function is defined
def thread_callback(settings, io_tags, callback):

    try:
        if appsetting.startRtuService:
            # Initializing Threading
            thread = threading.Thread(
                target=read_rtu,
                args=(settings, io_tags, callback)
            )
            # Starting the Thread
            thread.start()

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, f_name, exc_tb.tb_lineno)
        print("Thread callback error: ", ex)
