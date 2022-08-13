import json

config_file_path = './App/JsonConfig/config.json'
com_file_path = './App/JsonConfig/com_setting.json'


def read_setting():
    with open(config_file_path) as f:
        json_string = json.load(f)
        f.close()
    return json_string


def write_setting(json_file_content: str):
    json_object = json.dumps(json_file_content, indent=4)
    with open(config_file_path, 'w') as f:
        f.write(json_object)
        f.close()


def read_com_setting():
    with open(com_file_path) as f:
        json_string = json.load(f)
        f.close()
    return json_string


