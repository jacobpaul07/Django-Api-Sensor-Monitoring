import json
import os
import sys
import threading
thread_Lock = threading.Lock()


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

