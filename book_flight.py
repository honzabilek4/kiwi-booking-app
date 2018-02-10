import json
import requests
import argparse

api_flights_url = 'https://api.skypicker.com/flights'
api_booking_url = 'http://128.199.48.38:8080/booking'

parser = argparse.ArgumentParser(
    description='Book the cheapest or fastest flight between two destinations using Kiwi public api.')

parser.add_argument('--date', type=str, required=True, help='Date of the flight in format yyyy-mm-dd.')
parser.add_argument('--from', type=str, required=True, help='From destination in IATA code format')
parser.add_argument('--to', type=str, required=True, help='To destination in IATA code format') 
parser.add_argument('--bags', type=int, default=1, help='Number of bags to be added. (default is one)')

flight_type_group = parser.add_mutually_exclusive_group()
flight_type_group.add_argument('--one-way', action='store_true', default=True, help='Book one way ticket. (default)')
flight_type_group.add_argument('--return', type=int, help='Number of days to stay.')           

search_type_group = parser.add_mutually_exclusive_group()
search_type_group.add_argument('--cheapest', action='store_true', default=True, 
                    help='Book cheapest flight. (default)')
search_type_group.add_argument('--fastest', action='store_true', default=False,
                    help='Book the shortest flight between destinations.')


args = parser.parse_args()
print(args)