import os
import gzip

try:
    import requests
except ModuleNotFoundError:
    raise Exception('Please ensure that you\'ve activated the venv!\n\nRun \".venv\Scripts\\activate\" on Windows. Then run \"python app.py\"')

# Data will be stored in /data
from utils.path import *


def is_data_exist():
    if os.path.isfile(file_path_xml_metar) and os.path.isfile(file_path_xml_taf) and os.path.isfile(
            file_path_json_stations):
        return True

    return False


class GetData:
    def __init__(self) -> None:
        self.url_metar = 'https://aviationweather.gov/data/cache/metars.cache.xml.gz'
        self.url_taf = 'https://aviationweather.gov/data/cache/tafs.cache.xml.gz'
        self.url_stations = 'https://aviationweather.gov/data/cache/stations.cache.json.gz'

    def get_metar(self) -> None:
        response_metar = requests.get(self.url_metar)
        if response_metar.status_code == 200:
            with open(file_path_gz_metar, 'wb') as file:
                file.write(response_metar.content)
            with gzip.open(file_path_gz_metar, 'rb') as f_in:
                with open(file_path_xml_metar, 'wb') as f_out:
                    f_out.write(f_in.read())
            os.remove(file_path_gz_metar)

        else:
            raise Exception(f'Error during reaching API: Status Code: {response_metar.status_code}')

    def get_taf(self) -> None:
        response_taf = requests.get(self.url_taf)
        if response_taf.status_code == 200:
            with open(file_path_gz_taf, 'wb') as file:
                file.write(response_taf.content)
            with gzip.open(file_path_gz_taf, 'rb') as f_in:
                with open(file_path_xml_taf, 'wb') as f_out:
                    f_out.write(f_in.read())
            os.remove(file_path_gz_taf)

        else:
            raise Exception(f'Error during reaching API: Status Code: {response_taf.status_code}')

    def get_stations(self) -> None:
        response_stations = requests.get(self.url_stations)
        if response_stations.status_code == 200:
            with open(file_path_gz_stations, 'wb') as file:
                file.write(response_stations.content)
            with gzip.open(file_path_gz_stations, 'rb') as f_in:
                with open(file_path_json_stations, 'wb') as f_out:
                    f_out.write(f_in.read())
            os.remove(file_path_gz_stations)
        else:
            raise Exception(f'Error during reaching API: Status Code: {response_stations.status_code}')

    def get_data(self):
        self.get_metar()
        self.get_taf()
        self.get_stations()
