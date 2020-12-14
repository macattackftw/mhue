import json
import requests


class HueConnection:
    def __init__(self, connection_info_file: str):
        self.ip = None
        self.url = None
        self.username = None

        self._set_connection_data(connection_info_file)

    def _set_connection_data(self, connection_info_file):
        try:
            with open(connection_info_file, 'r') as f:
                data = json.load(f)
            self.ip = data['ip_address']
            self.username = data['username']
            self.url = f'http://{self.ip}/api/{self.username}/'
        except FileNotFoundError:
            print(f'File: {connection_info_file} not found.')
            exit(-1)

    def get_request(self, append_value: str) -> json:
        return requests.get(self.url + append_value).json()

    def put_request(self, append_value: str, data_value: dict) -> tuple:
        r = requests.put(self.url + append_value, data=json.dumps(data_value)).json()
        return ([item for keys in r for item in keys]).count('success') == len(data_value), r
