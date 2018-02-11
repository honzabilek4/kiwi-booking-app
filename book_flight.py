import json
import requests
import argparse
import time
import sys

API_FLIGHTS_URL = 'https://api.skypicker.com/flights'
API_BOOKING_URL = 'http://128.199.48.38:8080/booking'

DEFAULT_CURRENCY = 'EUR'
PERSONAL_DETAILS = {
    'lastName': 'Bílek',
    'firstName': 'Jan',
    'birthday': '2018-02-12',
    'title': 'Mr',
    'email': 'honza@elisiondesign.cz',
    'documentID': '4029240922'
}


def get_args():
    parser = argparse.ArgumentParser(
        description='Book the cheapest or fastest flight between two destinations using Kiwi public api.')
    parser.add_argument(
        '--date', type=str, required=True, help='Date of the flight in format yyyy-mm-dd.')
    parser.add_argument(
        '--from', type=str, required=True, dest='from_dest', help='From destination in IATA code format')
    parser.add_argument(
        '--to', type=str, required=True, help='To destination in IATA code format')
    parser.add_argument(
        '--bags', type=int, default=1, help='Number of bags to be added. (default is one)')

    flight_type_group = parser.add_mutually_exclusive_group()
    flight_type_group.add_argument(
        '--one-way', action='store_true', default=True, help='Book one way ticket. (default)')
    flight_type_group.add_argument(
        '--return', type=int, dest='return_flight', help='Number of days to stay.')

    search_type_group = parser.add_mutually_exclusive_group()
    search_type_group.add_argument(
        '--cheapest', action='store_true', default=True, help='Book cheapest flight. (default)')
    search_type_group.add_argument(
        '--fastest', action='store_true', default=False, help='Book the shortest flight between destinations.')

    args = parser.parse_args()
    return args


def build_request_params(args):
    params = dict()
    params['flyFrom'] = args.from_dest
    params['to'] = args.to
    params['bags'] = args.bags
    date = time.strptime(args.date, '%Y-%m-%d')
    params['dateFrom'] = time.strftime('%d/%m/%Y', date)
    params['dateTo'] = params.get('dateFrom')
    params['limit'] = 1

    if (args.fastest is True):
        params['sort'] = 'duration'
    else:
        params['sort'] = 'price'

    if (args.return_flight is not None):
        params['daysInDestinationFrom'] = args.return_flight
        params['daysInDestinationTo'] = args.return_flight
        params['typeFlight'] = 'round'

    return params


def find_flight(params):
    try:
        response = requests.get(API_FLIGHTS_URL, params)
        response.raise_for_status()
        found_flights = response.json().get('data')
        if(len(found_flights) > 0):
            return found_flights[0]
        else:
            raise Exception('No flights were found for specified parameters.')
    except requests.exceptions.HTTPError as error:
        print('Http error: {}'.format(error))
        return -1
    except requests.exceptions.RequestException as error:
        print('Request exception: {}'.format(error))
        return -1
    except Exception as error:
        print(error)
        sys.exit()


def book_flight(options, flight_data):
    payload = dict()
    payload['passengers'] = PERSONAL_DETAILS
    payload['currency'] = DEFAULT_CURRENCY
    payload['bags'] = options.bags
    payload['booking_token'] = flight_data.get('booking_token')
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            API_BOOKING_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as error:
        print('Http error: {}'.format(error))
        print(response.text)
        return -1
    except requests.exceptions.RequestException as error:
        print('Request exception: {}'.format(error))
        return -1


def print_flight_details(confirmation, flight_details):    
    cityFrom = flight_details.get('cityFrom')
    flyFrom = flight_details.get('flyFrom')
    cityTo = flight_details.get('cityTo')
    flyTo = flight_details.get('flyTo')
    flyDuration = flight_details.get('fly_duration')
    returnDuration = flight_details.get('return_duration')
    price = flight_details.get('price')
    
    print('Booking number: {}'.format(confirmation.get('pnr')))
    print('Confirmation status: {}'.format(confirmation.get('status')))    
    for route in flight_details.get('route'):
        print('From: {} {}'.format(route.get('cityFrom'), route.get('flyFrom')))        
        print('To: {} {}'.format(route.get('cityTo'), route.get('flyTo')))
    print('Duration: {}'.format(flyDuration))
    if returnDuration is not None:
        print('Return duration: {}'.format(returnDuration))
    print('–'*24)
    print('Total: {} {}'.format(price, DEFAULT_CURRENCY))

    # TODO: print back route


def main():
    arguments = get_args()
    request_params = build_request_params(arguments)
    flight_data = find_flight(request_params)
    confirmation = book_flight(arguments, flight_data)
    print_flight_details(confirmation, flight_data)


if __name__ == '__main__':
    main()
