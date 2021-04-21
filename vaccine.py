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

CVS_URL = "https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{}.json?vaccineinfo"
REFERER_URL = "https://www.cvs.com/immunizations/covid-19-vaccine"


def main():  # noqa: D103

    # set up an argument parser
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

    max_time = time.time() + args.total_hours * 60 * 60
    state_url = CVS_URL.format(args.state.lower())
    chosen_cities = [city.upper() for city in args.cities]

    # run for `args.total` hours or until Ctrl-C is pressed
    while time.time() < max_time:

        try:
            # get the latest response from CVS website
            response = requests.get(state_url, headers={"Referer": REFERER_URL})
            payload = response.json()

            # save the status for the chosen cities in a dictionary
            statusdict = {}
            for item in payload["responsePayloadData"]["data"][args.state]:
                city, status = item['city'], item['status']
                if city in chosen_cities:
                    statusdict[city] = status

            # print out the values in the dictionary and make a sound to alert
            # the user if any of the chosen cities have appointments available
            print(time.ctime())
            for city, status in statusdict.items():
                print(city, status)
                if status != 'Fully Booked':
                    beepy.beep(sound='coin')
                    break

            # sleep for the given number of minutes
            # before refreshing again
            time.sleep(args.refresh_minutes * 60)
            print()
        except KeyboardInterrupt:
            print('Exiting ...')
            break


if __name__ == '__main__':
    main()
