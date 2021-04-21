#!/usr/bin/env python3
"""
Find vaccine appointments at CVS in specific cities.

This script scrapes the CVS website looking for vaccine appointments in the
cities you specify.

:author: Bryce Macher
:author: Nitin Madnani
:date: March 2021
"""

import argparse
import time

import beepy
import requests

URL = "https://www.cvs.com"
REFERER_URL = f"{URL}/immunizations/covid-19-vaccine"
CVS_URL = f"{REFERER_URL}.vaccine-status.{{}}.json?vaccineinfo"
CVS_BOOKING_URL = f"{URL}/vaccine/intake/store/covid-screener/covid-qns"  # For display only


def get_args() -> dict:
    """Set up and return an argument parser."""
    parser = argparse.ArgumentParser(prog='vaccine.py')
    parser.add_argument("--total",
                        dest="total_hours",
                        type=int,
                        help="Total Number of hours for which to run the script",
                        default=3)
    parser.add_argument("--refresh",
                        dest="refresh_minutes",
                        help="Number of minutes after which to refresh results",
                        type=int,
                        default=1)
    parser.add_argument("--state",
                        help="State to search, e.g., NJ",
                        required=True)

    # For now, require one of these. But if none given, we could just show all.
    citygroup = parser.add_mutually_exclusive_group(required=True)
    citygroup.add_argument("--cities",
                            nargs='+',
                            help="Full names of cities to search, separated by whitespace. "
                           "Quote multiword cities like 'Falls Church'.")
    citygroup.add_argument("--cityfile",
                           help="Filename with cities, one per line.",
                           type=argparse.FileType('r'))

    # parse given command line arguments
    args = parser.parse_args()
    if args.cityfile:
        args.cities = [x.strip() for x in args.cityfile.readlines()]

    return args

def main():  # noqa: D103
    args = get_args()
    max_time = time.time() + args.total_hours * 60 * 60
    state_url = CVS_URL.format(args.state.lower())
    chosen_cities = [city.upper() for city in args.cities]

    # run for `args.total` hours or until Ctrl-C is pressed
    while time.time() < max_time:

        try:
            # get the latest response from CVS website
            response = requests.get(state_url, headers={"Referer": REFERER_URL})
            response.raise_for_status()
            payload = response.json()

            # save the status for the chosen cities in a dictionary
            statusdict = {item['city']: item['status']
                          for item in payload["responsePayloadData"]["data"][args.state]}

            # print out the values in the dictionary and make a sound to alert
            # the user if any of the chosen cities have appointments available
            print(time.ctime())
            AVAILABLE = False        # Becomes true if any are avail.
            for city, status in statusdict.items():
                if city not in chosen_cities:
                    continue
                print(f"{city:>25}: {status.replace('Available', '**AVAILABLE**')}")
                if status != 'Fully Booked' and not AVAILABLE:
                    beepy.beep(sound='coin')
                    AVAILABLE = True

            if AVAILABLE:
                print(f'Booking site: {CVS_BOOKING_URL}')

            # sleep for the given number of minutes
            # before refreshing again
            time.sleep(args.refresh_minutes * 60)
            print()
        except KeyboardInterrupt:
            print('Exiting ...')
            break


if __name__ == '__main__':
    main()
