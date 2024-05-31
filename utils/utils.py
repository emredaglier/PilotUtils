import xml.etree.ElementTree as ET
from utils.path import *
from utils.data import GetData, is_data_exist
import json

def parse_metar():
    metar = {}
    tree_metar = ET.parse(file_path_xml_metar)
    root_metar = tree_metar.getroot()

    for mtr in root_metar.iter('raw_text'):
        metar[mtr.text[:4]] = mtr.text[5:]

    return metar


def parse_taf():
    taf = {}
    tree_taf = ET.parse(file_path_xml_taf)
    root_taf = tree_taf.getroot()

    for tf in root_taf.iter('raw_text'):
        if tf.text[0].upper() == 'K':
            taf[tf.text[:4]] = tf.text[5:]
        else:
            taf[tf.text[4:8]] = tf.text[9:]

    return taf


def parse_stations():
    f = open(file_path_json_stations)

    data = json.load(f)

    return data


class Parse:
    def __init__(self, icao, no_refresh) -> None:
        self.icao = icao
        self.no_refresh = no_refresh

    def data_check(self):
        _get = GetData()
        if not is_data_exist():
            os.makedirs(data_folder)
            _get.get_data()

        if not self.no_refresh:
            _get.get_data()

    def main(self):
        self.data_check()

        _req = ReqData()

        data = {
            'METAR': _req.request_metar(self.icao),
            'TAF': _req.request_taf(self.icao)
        }

        iata, country, lat, lon, elev, name = _req.request_stations(self.icao)

        print_data = {
            'name': f'\n{name}\n',
            'iata': f'IATA:\t\t {iata}',
            'country': f'Country:\t {country}',
            'lat': f'Latitude:\t {lat}',
            'lon': f'Longitude:\t {lon}',
            'elev': f'Elevation:\t {elev}'
        }

        for _ in print_data.keys():
            print(print_data[_])

        print(f'\nMETAR:\t {data["METAR"]}')
        print(f'TAF:\t {data["TAF"]}')


class ReqData:
    def __init__(self) -> None:
        self.metar = parse_metar()
        self.taf = parse_taf()
        self.stations = parse_stations()

    def request_metar(self, icao: str) -> str:
        try:
            return self.metar[icao.upper()]

        except KeyError:
            return f'{icao.upper()} has not been found in the cached METAR data.'

    def request_taf(self, icao: str) -> str:
        try:
            return self.taf[icao.upper()]

        except KeyError:
            return f'{icao.upper()} has not been found in the cached TAF data.'

    def request_stations(self, icao: str):
        try:
            for val in self.stations:
                if val['icaoId'] == icao.upper():
                    name = val['site']

                    if 'Arpt' in name:
                        name = name.replace('Arpt', 'Airport')

                    if 'Intl' in name:
                        name = name.replace('Intl', 'International')
                        name += ' Airport'

                    return val['iataId'], val['country'], val['lat'], val['lon'], val['elev'], name


            print(f'{icao.upper()} has not been found in the cached Stations data.')
            exit()

        except:
            print(f'{icao.upper()} has not been found in the cached Stations data.')
            exit()

