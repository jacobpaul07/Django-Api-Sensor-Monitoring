import json

config_file_path = './App/JsonConfig/config.json'
com_file_path = './App/JsonConfig/com_setting.json'


def read_setting():
    try:
        with open(config_file_path) as f:
            json_string = json.load(f)
            f.close()
        return json_string
    except Exception as ex:
        print("Read Setting Error", ex)

def write_setting(json_file_content: str):
    try:
        json_object = json.dumps(json_file_content, indent=4)
        with open(config_file_path, 'w') as f:
            f.write(json_object)
            f.close()
    except Exception as ex:
        print("Write Setting Error", ex)


def read_com_setting():
    try:
        with open(com_file_path) as f:
            json_string = json.load(f)
            f.close()
        return json_string
    except Exception as ex:
        print("Read Com Setting Error", ex)

def write_com_setting(json_file_content: str):
    try:
        json_object = json.dumps(json_file_content, indent=4)
        with open(com_file_path, 'w') as f:
            f.write(json_object)
            f.close()
    except Exception as ex:
        print("Write Com Setting Error", ex)
