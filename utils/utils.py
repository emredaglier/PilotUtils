import xml.etree.ElementTree as ET
from utils.vars import *
from utils.data import GetData, is_data_exist
import json
from string import punctuation, digits

version_data = json_to_local()
def parse_metar():
    metar = {}
    tree_metar = ET.parse(file_path_xml_metar)
    root_metar = tree_metar.getroot()

    for vr in root_metar.iter('request_index'):
        version_data['metar'] = vr.text

    for mtr in root_metar.iter('raw_text'):
        metar[mtr.text[:4]] = mtr.text[5:]

    return metar


def parse_taf():
    taf = {}
    tree_taf = ET.parse(file_path_xml_taf)
    root_taf = tree_taf.getroot()

    for vr in root_taf.iter('request_index'):
        version_data['taf'] = vr.text

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
        self.check_str()

    def check_str(self):
        self.icao = str(self.icao)
        self.icao = self.icao.strip(digits)
        self.icao = self.icao.strip(punctuation)
        self.icao = self.icao.strip()
        self.icao = self.icao.upper()

    def data_check(self):
        _get = GetData()
        if not is_data_exist():
            os.makedirs(data_folder)
            os.makedirs(version)
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

        version_data = json_to_local()

        iata, country, lat, lon, elev, name = _req.request_stations(self.icao)

        print_data = {
            'head': '--------------------------------------------------------',
            'latest_cache': f'Cache Date:\t{version_data["date"]}',
            'refresh': f'Latest Cache:\t{True if self.no_refresh == False else False}',
            'name': f'\n{name}\n',
            '_seperator': '_______',
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
            return self.metar[icao]

        except KeyError:
            return f'{icao} has not been found in the cached METAR data.'

    def request_taf(self, icao: str) -> str:
        try:
            return self.taf[icao]

        except KeyError:
            return f'{icao} has not been found in the cached TAF data.'

    def request_stations(self, icao: str):
        try:
            for val in self.stations:
                if val['icaoId'] == icao:
                    name = val['site']

                    if 'Arpt' in name:
                        name = name.replace('Arpt', 'Airport')

                    if 'Intl' in name:
                        name = name.replace('Intl', 'International')
                        name += ' Airport'

                    return val['iataId'], val['country'], val['lat'], val['lon'], val['elev'], name

        except:
            print(f'{icao} has not been found in the cached Stations data.')
            exit()
