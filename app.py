import argparse
from utils.utils import Parse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python executable for METAR and TAF data using aviationweather.gov API')
    parser.add_argument('ICAO', type=str, help='ICAO code of the desired airport.')
    parser.add_argument('--no-refresh', dest='no_refresh', action='store_true', help='Do not refresh the cached data. (If there is no file, the program will download the data anyways.)')

    args = parser.parse_args()

    _ = Parse(args.ICAO, no_refresh=args.no_refresh)
    _.main()
