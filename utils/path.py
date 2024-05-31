import os

current_directory = os.path.dirname(os.path.realpath(__file__))
file_path_gz_metar = os.path.join(current_directory, 'data\data_metar.gz')
file_path_xml_metar = os.path.join(current_directory, 'data\data_metar.xml')

file_path_json_stations = os.path.join(current_directory, 'data\.stations.json')
file_path_gz_stations = os.path.join(current_directory, 'data\.stations.gz')

file_path_gz_taf = os.path.join(current_directory, 'data\data_taf.gz')
file_path_xml_taf = os.path.join(current_directory, 'data\data_taf.xml')

data_folder = os.path.join(current_directory, 'data')