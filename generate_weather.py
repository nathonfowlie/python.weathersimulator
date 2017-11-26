import arrow
import argparse
import json
import os
import pytz
import sys

from arrow.parser import ParserError
from colorama import Fore, init, deinit
from jsonschema import validate, ValidationError
from random import uniform
from timezonefinder import TimezoneFinder

from weathersimulator.weather import WeatherCondition
from pkg_resources import get_distribution

DEFAULT_DATA_FILE = 'data/locations.json'
DEFAULT_START_DATE = '1970-01-01 00:00:00'
DEFAULT_END_DATE = '1970-03-31 00:00:00'

actual_start_date = None
actual_end_date = None

def init_arg_parser():
    """
    Initialises the argument parser used to process user input.

    :return: Returns an argparse.ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(description='Simple weather simulator which generates realistic weather data.')

    parser.add_argument('-v', '--version', help='show program version', action='store_true')

    parser.add_argument('-f', '--file',
                        help='JSON data file containing location definitions (default: data/locations.json).',
                        action='store', dest='file', metavar='FILE', default=DEFAULT_DATA_FILE)

    parser.add_argument('-s', '--start', help='Starting date for the generated weather data.', action='store',
                        dest='start', metavar='DD/MM/YYYY', default=DEFAULT_START_DATE)

    parser.add_argument('-e', '--end', help='Ending date for the generated weather data.', action='store', dest='end',
                        metavar='DD/MM/YYYY', default=DEFAULT_END_DATE)

    return parser


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def validate_data_file(data_file):
    """
    Verifies that the data file is accessible and in the correct format.

    :param data_file: Relative or absolute path to the data file containing location information.

    :return: None
    """
    if not os.path.isfile(data_file):
        print(Fore.RED + 'Unable to locate data file - {0}.'.format(data_file))
        exit(0)

    schema_file = os.path.join(os.path.dirname(get_script_path()),'schema.json')

    with open(schema_file) as location_schema_file:
        schema = json.load(location_schema_file)

    with open(data_file) as location_file:
        location_records = json.load(location_file)

    try:
        validate(location_records, schema)
    except ValidationError as jve:
        print(Fore.RED + 'Data file is corrupt or not in the correct format - {0}\n{1}'.format(data_file, jve.message))
        exit(0)


def validate_args(args):
    """
    Validates user input prior to execution of the weather simulator.

    :param args: User provided arguments.

    :return: Returns a dictionary containing the validated user arguments, including any default args.
    """
    if args.version:
        print('Simple Weather Simulator {0}'.format(get_distribution(__name__).version))
        exit(0)

    absolute_path = os.path.abspath(args.file) if args.file else os.path.abspath(DEFAULT_DATA_FILE)
    validate_data_file(absolute_path)

    try:
        start_date = arrow.get(args.start)
    except ParserError as pe:
        print(Fore.RED + 'Start date should be in the format YYYY-MM-DD HH:mm:ss')
        exit(0)

    try:
        end_date = arrow.get(args.end)
    except ParserError as pe:
        print(Fore.RED + 'End date should be in the format YYYY-MM-DD HH:mm:ss')
        exit(0)

    return args


def generate(start_date, end_date, data_file):
    """
    Generates the weather data and outputs to stdout.

    :param data_file: Absolute path to the source data file.
    :param start_date: The starting date to begin generating weather data for.
    :param end_date: The end date to stop generating weather date for.
    """
    location_records = []

    with open(data_file) as location_file:
        location_records = json.load(location_file)

    current_date = start_date

    while current_date <= end_date:
        current_month = current_date.datetime.month - 1

        for location in location_records:
            tf = TimezoneFinder()
            timezone_str = tf.timezone_at(lng=location['longitude'], lat=location['latitude'])
            tz = pytz.timezone(timezone_str)

            weather_condition = WeatherCondition(
                name=location['name'],
                latitude=location['latitude'],
                longitude=location['longitude'],
                elevation=location['elevation'],
                temperature=uniform(location['temps']['min'][current_month], location['temps']['max'][current_month]),
                datetime = current_date.astimezone(tz)
            )

            weather_condition.calculate()
            print(weather_condition)

        current_date = current_date.replace(days=1)


def main():
    """
    Main entrypoint for the weather simulator.

    :return: Returns a non-zero code on error.
    """
    # Initialise colorama for coloured terminal output
    init(autoreset=True)

    parser = init_arg_parser()
    args = validate_args(parser.parse_args())

    start_date = arrow.get(args.start)
    end_date = arrow.get(args.end)

    generate(start_date, end_date, args.file)

    deinit()


if __name__ == '__main__':
    main()
