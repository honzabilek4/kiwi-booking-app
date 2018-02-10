import json
import requests
import argparse
import time

api_flights_url = 'https://api.skypicker.com/flights'
api_booking_url = 'http://128.199.48.38:8080/booking'

def get_args():
    parser = argparse.ArgumentParser(
        description='Book the cheapest or fastest flight between two destinations using Kiwi public api.')

    parser.add_argument('--date', type=str, required=True, help='Date of the flight in format yyyy-mm-dd.')
    parser.add_argument('--from', type=str, required=True, dest='from_dest', help='From destination in IATA code format')
    parser.add_argument('--to', type=str, required=True, help='To destination in IATA code format') 
    parser.add_argument('--bags', type=int, default=1, help='Number of bags to be added. (default is one)')

    flight_type_group = parser.add_mutually_exclusive_group()
    flight_type_group.add_argument('--one-way', action='store_true', default=True, help='Book one way ticket. (default)')
    flight_type_group.add_argument('--return', type=int, dest='return_flight', help='Number of days to stay.')           

    search_type_group = parser.add_mutually_exclusive_group()
    search_type_group.add_argument('--cheapest', action='store_true', default=True, 
                        help='Book cheapest flight. (default)')
    search_type_group.add_argument('--fastest', action='store_true', default=False,
                        help='Book the shortest flight between destinations.')

    args = parser.parse_args()
    return args

def build_request_params(args):
    params = dict()
    params['flyFrom'] = args.from_dest
    params['to'] = args.to
    params['bags'] = args.bags
    date = time.strptime(args.date,'%Y-%m-%d')
    params['dateFrom'] = time.strftime('%d/%m/%Y', date)
    params['dateTo'] = params['dateFrom']
    
    if (args.fastest == False):
        params['one_per_date'] = 1
    if (args.return_flight != None):
        params['daysInDestinationFrom'] = args.return_flight
        params['daysInDestinationTo'] = args.return_flight
    
    return params

def find_flights(payload):
    try:
        response = requests.get(api_flights_url,payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print('Http error: {}'.format(error))        
        return -1
    except requests.exceptions.RequestException as error:
        print('Request exception: {}'.format(error))

def main():
    args = get_args()
    request_params = build_request_params(args)
    print(request_params)
    flights = find_flights(request_params)
    print(flights)

if __name__ == '__main__':
    main()