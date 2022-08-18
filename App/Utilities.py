import os
import sys
import json
import time
import datetime
import threading
import dateutil.parser


from channels.layers import get_channel_layer
from MongoDB_Main import Document as Doc
from asgiref.sync import async_to_sync

thread_Lock = threading.Lock()


# Send To Websocket
def sentLiveData(data):
    text_data = json.dumps(data, indent=4)
    loaded_data = json.loads(text_data)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("notificationGroup", {
        "type": "chat_message",
        "message": loaded_data
    })


def write_result_file(json_content):
    try:
        thread_Lock.acquire()
        with open("./App/JsonDatabase/result.json", "w+") as result_file:
            json.dump(json_content, result_file, indent=4)
            result_file.close()
    except Exception as ex:
        print(ex)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, f_name, exc_tb.tb_lineno)
        print("Write Production File Error: ", ex)

    finally:
        thread_Lock.release()


def read_result_file():
    try:
        thread_Lock.acquire()
        file_path = "./App/JsonDatabase/result.json"
        file_status = os.path.isfile(file_path)
        if file_status:
            with open(file_path, 'r') as file:
                reason_code_list = json.load(file)
                file.close()
                return reason_code_list
        else:
            reason_code_list = []
            return reason_code_list

    except Exception as ex:
        print(ex)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, f_name, exc_tb.tb_lineno)
    finally:
        thread_Lock.release()


def send_to_database(result_file_contents, time_stamp):
    try:
        result_file_contents["last_updated_timestamp"] = dateutil.parser.parse(str(time_stamp))
        col = "LiveData"
        Doc().DB_Write(result_file_contents, col)
    except Exception as ex:
        print("DataBase Write Error: ", ex)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, f_name, exc_tb.tb_lineno)


def save_sensor_data(message):
    try:
        time_stamp = datetime.datetime.now()
        # loaded_data = json.loads(message)

        result_file_contents = read_result_file()
        result_file_contents["sensor_data"]: list = message
        result_file_contents["last_updated_timestamp"] = str(time_stamp)
        sentLiveData(result_file_contents)

        # Update Json Data
        write_result_file(json_content=result_file_contents)
        
        # Write data to DB
        thread = threading.Thread(target=send_to_database, args=[result_file_contents, time_stamp])
        thread.start()
    except Exception as ex:
        print("Error in save_sensor_data: ", ex)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, f_name, exc_tb.tb_lineno)
        print("Check the port or Restart the system and try again")

